"""
Turn a museum's permutation-importance CSV into a readable markdown report,
ranked by model eval performance
"""
import os

import pandas as pd

from src.analysis.importance import FEATURE_GROUPS

MODELS_DIR = "./outputs/models"
PRETTY_NAMES = {
    "rf": "Random Forest Regressor",
    "xgb": "XGBoost",
    "svr": "Support Vector Regression",
    "hw": "Holt-Winters exponential smoothing",
    "sarimax": "SARIMAX",
    "lstm": "LSTM",
    "timegpt": "TimeGPT",
    "baseline": "Baseline Monthly Mean",
}

# A MAPE this large means the actuals contain zeros, so the ratio is meaningless
# Report will replace it with "*"
MAPE_LIMIT = 10.0

# Intro for feature importance report
INTRO = """Permutation importance shuffles one column of the evaluation set and measures how
much worse the forecast gets. The number below is the **rise in RMSE**, in the same units as
the forecast itself (thousands of visitors), so it is comparable across models and museums.

- A **large** value means the model leans on that column: breaking it costs accuracy.
- A value near **zero** means the model barely uses it.
- A **negative** value means shuffling helped slightly, which is noise, not signal.

Scores are measured on the eval test set, the only period with actual visitor numbers to
compare against. The predict horizon has no actuals, so nothing can be scored there.

Individual columns understate their own worth when they are correlated: shuffling `lag_1`
barely hurts while `lag_2` and `monthly_avg` still carry almost the same information. The
grouped tables shuffle every column in a group at once, so the group score is the honest
measure of what that block of features contributes. A group's score is **not** the sum of its
members' scores."""


def _table(rows, headers, aligns):
    """Render one HTML table; numeric columns are right-aligned."""
    head = "".join(
        f'<th style="text-align:{a};padding:4px 10px;">{h}</th>'
        for h, a in zip(headers, aligns)
    )
    body = "".join(
        "<tr>"
        + "".join(
            f'<td style="text-align:{a};padding:4px 10px;">{c}</td>'
            for c, a in zip(row, aligns)
        )
        + "</tr>"
        for row in rows
    )
    return (
        '<table style="border-collapse:collapse;">\n'
        f"<thead><tr>{head}</tr></thead>\n<tbody>{body}</tbody>\n</table>"
    )


def _groups_table(features):
    """A table of feature groups and their members, for the report's intro section."""
    rows = [
        (f"<code>{name}</code>", ", ".join(f"<code>{c}</code>" for c in cols))
        for name, select in FEATURE_GROUPS.items()
        if (cols := select(features))
    ]
    return _table(rows, ["Group", "Features"], ["left", "left"])


def _metrics_table(rmse, mape):
    """Render the model's eval metrics as a table, with MAPE capped at MAPE_LIMIT."""
    shown = "*" if pd.isna(mape) or abs(mape) > MAPE_LIMIT else f"{mape:.2%}"
    return f"|  |  |\n|---|---|\n| RMSE | {rmse:.2f} |\n| MAPE | {shown} |"


def _importance_table(scores):
    """Render a table of feature importance scores, with the feature name in code font"""
    rows = [
        (f"<code>{r.feature}</code>", f"{r.importance_rmse:.2f}")
        for r in scores.itertuples()
    ]
    return _table(rows, ["Feature", "Importance (RMSE)"], ["left", "right"])


def build_report(museum_code):
    """Write one museum's markdown report, or skip if it has no importance scores.

    Args:
        museum_code (str): Short museum code, e.g. "ACM".

    Returns:
        str | None: The file written, or None if the inputs were missing.
    """
    importance_path = f"{MODELS_DIR}/{museum_code}/permutation_importance.csv"
    eval_path = f"./outputs/{museum_code}/{museum_code}_model_eval.csv"
    if not os.path.exists(importance_path) or not os.path.exists(eval_path):
        print(f"  [{museum_code}] no permutation importance to report, skipping")
        return None

    importance = pd.read_csv(importance_path)
    evaluation = pd.read_csv(eval_path)

    # Eval metrics arrive formatted for display, so parse them back to numbers
    evaluation["RMSE"] = pd.to_numeric(evaluation["RMSE"])
    evaluation["MAPE"] = pd.to_numeric(evaluation["MAPE"].str.rstrip("%")) / 100
    evaluation = evaluation.sort_values("RMSE")

    scored = {
        key: group.drop(columns=["Institution", "model"])
        for key, group in importance.groupby("model")
    }
    # Sorted so lag_2 precedes lag_10 rather than following it
    features = sorted(
        importance.loc[importance["group"] == "single", "feature"].unique(),
        key=lambda f: (0, int(f.split("_")[1])) if f.startswith("lag_") else (1, f),
    )

    # Build the report in parts, then write it to disk at once.
    parts = [
        f"# [{museum_code}] Permutation Importances\n",
        INTRO,
        "\n## Feature groups\n",
        _groups_table(features),
        "\n## Models\n",
        "Ordered by eval RMSE, best first.\n",
    ]

    # One section per model, keeping unscored models in their ranked position
    for row in evaluation.itertuples():
        key = next((k for k, v in PRETTY_NAMES.items() if v == row.Model), None)
        parts.append(f"\n### {row.Model}\n")
        parts.append(_metrics_table(row.RMSE, row.MAPE))

        if key not in scored:
            parts.append(
                "\nNot scored: this model reads no feature columns, "
                "so there is nothing to permute.\n"
            )
            continue

        table = scored[key].sort_values("importance_rmse", ascending=False)
        parts.append("\n**By feature group**\n")
        parts.append(_importance_table(table[table["group"] == "group"]))
        parts.append("\n**By individual feature**\n")
        parts.append(_importance_table(table[table["group"] == "single"]))

    target = f"./outputs/{museum_code}/{museum_code}_permutation_importances.md"
    with open(target, "w", encoding="utf-8") as f:
        f.write("\n".join(parts) + "\n")
    return target
