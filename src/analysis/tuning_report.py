"""
Summarise every Optuna study saved under outputs/tuning/ into one markdown
report: where each search landed inside its range, how much each parameter
mattered, and how late in the budget the best trial was found.
"""
import os
import re

import optuna
import pandas as pd

from config import MODEL_KEYS, MUSEUM_CODES
from src.analysis.tuning import STUDY_DIR

REPORT_PATH = "./outputs/tuning_report.md"


def _range_of(distribution):
    """Human-readable search space for one parameter."""
    if hasattr(distribution, "choices"):
        return ", ".join(str(c) for c in distribution.choices)
    step = getattr(distribution, "step", None)
    span = f"{distribution.low} to {distribution.high}"
    return f"{span} step {step}" if step not in (None, 1) else span


def _format(value):
    """Round floats for display, leave everything else alone."""
    return f"{value:.4g}" if isinstance(value, float) else str(value)


def load_studies():
    """Every saved study, keyed by (museum_code, model_key)."""
    studies = {}
    if not os.path.isdir(STUDY_DIR):
        return studies
    for filename in sorted(os.listdir(STUDY_DIR)):
        match = re.fullmatch(r"(.+)_(.+)\.db", filename)
        if not match:
            continue
        code, key = match.groups()
        name = f"{code}_{key}"
        try:
            studies[(code, key)] = optuna.load_study(
                study_name=name, storage=f"sqlite:///{STUDY_DIR}/{filename}"
            )
        except Exception as error:
            print(f"  could not load {filename}: {error}")
    return studies


def _md_table(frame):
    """A DataFrame as a markdown pipe table."""
    header = "| " + " | ".join(frame.columns) + " |"
    divider = "|" + "|".join(["---"] * len(frame.columns)) + "|"
    rows = [
        "| " + " | ".join(str(v) for v in row) + " |"
        for row in frame.astype(str).values
    ]
    return "\n".join([header, divider] + rows)


def build_report(path=REPORT_PATH):
    """Summarise every saved Optuna study into outputs/tuning_report.md.

    The report contains:
    - search budget table (one row per museum and model)
    - chosen-values table
    - importance table (one column per museum and one row per parameter)

    Args:
        path (str): Where to write the report.

    Returns:
        str | None: The path written, or None if outputs/tuning/ holds no studies.
    """
    # Load all saved studies
    studies = load_studies()
    if not studies:
        return None

    # Museums and models with at least one study, in config order so every table lists them the same way
    codes = [c for c in MUSEUM_CODES.values() if any(k[0] == c for k in studies)]
    keys = [k for k in MODEL_KEYS if any(s[1] == k for s in studies)]

    # A study whose first objective raised, or that was interrupted, has no completed
    # trial and so no best trial: it stays in the budget table but gets no other tables
    completed = {k: s.get_trials(states=[optuna.trial.TrialState.COMPLETE]) for k, s in studies.items()}

    lines = ["# Hyperparameter tuning report", ""]

    # One row per museum and model: the best CV RMSE and which trial found it.
    # A best trial near the end of the budget means the search was still improving
    budget = pd.DataFrame(
        [
            {
                "Model": key,
                "Museum": code,
                "Trials": len(studies[(code, key)].trials),
                "Completed": len(completed[(code, key)]),
                "Best value": _format(studies[(code, key)].best_value) if completed[(code, key)] else "none completed",
                "Best at trial": studies[(code, key)].best_trial.number if completed[(code, key)] else "-",
            }
            for key in keys
            for code in codes
            if (code, key) in studies
        ]
    )
    lines += ["## Search budget", "", _md_table(budget), ""]

    # One section per model, comparing museums side by side
    for key in keys:
        present = [c for c in codes if completed.get((c, key))]
        if not present:
            continue
        reference = studies[(present[0], key)].best_trial
        params = list(reference.params)

        lines += [f"## {key}", "", "### Chosen values", ""]

        # The value each museum's best trial chose, next to its search range;
        # a value at the edge of the range suggests widening it
        chosen = pd.DataFrame(
            [
                {
                    "Parameter": p,
                    "Range": _range_of(reference.distributions[p]),
                    **{
                        c: _format(studies[(c, key)].best_trial.params.get(p, ""))
                        for c in present
                    },
                }
                for p in params
            ]
        )
        lines += [_md_table(chosen), "", "### Importance", ""]

        # How much each parameter moved the CV score across trials; nan when Optuna can't compute it
        scores = {}
        for c in present:
            try:
                scores[c] = optuna.importance.get_param_importances(studies[(c, key)])
            except Exception:
                scores[c] = {}
        importance = pd.DataFrame(
            [
                {"Parameter": p, **{c: f"{scores[c].get(p, float('nan')):.3f}" for c in present}}
                for p in params
            ]
        )
        lines += [_md_table(importance), ""]

    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    return path
