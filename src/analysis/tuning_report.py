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
    """Write the tuning report. Returns the path, or None if no studies exist."""
    studies = load_studies()
    if not studies:
        return None

    codes = [c for c in MUSEUM_CODES.values() if any(k[0] == c for k in studies)]
    keys = [k for k in MODEL_KEYS if any(s[1] == k for s in studies)]

    lines = ["# Hyperparameter tuning report", ""]

    # How late in the budget each search peaked, and what it reached
    budget = pd.DataFrame(
        [
            {
                "Model": key,
                "Museum": code,
                "Trials": len(studies[(code, key)].trials),
                "Best value": _format(studies[(code, key)].best_value),
                "Best at trial": studies[(code, key)].best_trial.number,
            }
            for key in keys
            for code in codes
            if (code, key) in studies
        ]
    )
    lines += ["## Search budget", "", _md_table(budget), ""]

    for key in keys:
        present = [c for c in codes if (c, key) in studies]
        reference = studies[(present[0], key)].best_trial
        params = list(reference.params)

        lines += [f"## {key}", "", "### Chosen values", ""]
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
