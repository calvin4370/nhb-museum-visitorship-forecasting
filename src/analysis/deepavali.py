"""
Report how the best model performed in the Deepavali months of IHC.

Only IHC has the is_deepavali feature activated, so every other museum returns
nothing rather than an empty report.
"""
import pathlib

import pandas as pd

from config import MODEL_NAMES

DEEPAVALI_CSV = "./src/events/event_ranges/deepavali.csv"

# Only examine for IHC, since the other museums dont have is_deepavali feature activated
MUSEUM_CODE = "IHC"

TABLE_HEADER = [
    "| Month | Actual | Predicted | Difference | % difference |",
    "|---|---|---|---|---|",
]


def _read_predictions(path, deepavali):
    """Rows of a saved prediction csv that fall on a Deepavali month."""
    if not pathlib.Path(path).exists():
        return None
    frame = pd.read_csv(path)
    frame["timestamp"] = pd.to_datetime(
        dict(year=frame["Year"], month=frame["Month"], day=1)
    )
    return frame


def deepavali_months(museum_code=MUSEUM_CODE):
    """Best model's Deepavali-month predictions, or None if unavailable.

    Args:
        museum_code (str): Museum to report on; anything but IHC returns None.

    Returns:
        tuple | None: (best_name, eval_frame, predict_frame, evaluated, predicted).
    """
    if museum_code != MUSEUM_CODE:
        return None

    eval_path = f"./outputs/{museum_code}/{museum_code}_model_eval.csv"
    if not pathlib.Path(eval_path).exists():
        return None

    # The eval table is written lowest-RMSE-first, so the winner is row one
    best_name = pd.read_csv(eval_path).iloc[0]["Model"]
    best_key = {name: key for key, name in MODEL_NAMES.items()}.get(best_name)
    if best_key is None:
        return None

    deepavali = pd.read_csv(DEEPAVALI_CSV)
    deepavali["start"] = pd.to_datetime(deepavali["start"])

    # Eval predictions carry their own actuals, so no other source is needed
    evaluated = _read_predictions(
        f"./outputs/{museum_code}/eval/{museum_code}_{best_key}_predictions.csv", deepavali
    )
    if evaluated is None:
        return None
    eval_months = evaluated[evaluated["timestamp"].isin(deepavali["start"])].sort_values("timestamp")

    # The predict horizon has no actuals, so only the forecast is shown for it
    predicted = _read_predictions(
        f"./outputs/{museum_code}/predict/{museum_code}_{best_key}_predictions.csv", deepavali
    )
    predict_months = (
        predicted[predicted["timestamp"].isin(deepavali["start"])].sort_values("timestamp")
        if predicted is not None else pd.DataFrame()
    )
    return best_name, eval_months, predict_months, evaluated, predicted


def table_lines(museum_code=MUSEUM_CODE):
    """The markdown table of Deepavali months, header included, or None."""
    found = deepavali_months(museum_code)
    if found is None:
        return None
    _, eval_months, predict_months, _, _ = found

    rows = []
    for row in eval_months.itertuples():
        difference = row.Prediction - row.Actual
        percent = difference / row.Actual * 100 if row.Actual else float("nan")
        rows.append(
            f"| {row.timestamp:%Y-%m} | {row.Actual:.2f} | {row.Prediction:.2f} "
            f"| {difference:+.2f} | {percent:+.2f}% |"
        )
    for row in predict_months.itertuples():
        rows.append(f"| {row.timestamp:%Y-%m} | -- | {row.Prediction:.2f} | -- | -- |")
    return TABLE_HEADER + rows if rows else None


def build_report(museum_code=MUSEUM_CODE):
    """Write outputs/{code}/{code}_deepavali.md. Returns the path, or None."""
    found = deepavali_months(museum_code)
    if found is None:
        return None
    best_name, eval_months, predict_months, evaluated, predicted = found

    def listed(frame):
        return ", ".join(f"{t:%Y-%m}" for t in frame["timestamp"]) if len(frame) else "None"

    periods = (
        f"[{listed(eval_months)}] fall inside the eval period "
        f"{evaluated['timestamp'].min():%Y-%m} to {evaluated['timestamp'].max():%Y-%m}"
    )
    if len(predict_months):
        periods += (
            f", and {listed(predict_months)} inside the predict period "
            f"{predicted['timestamp'].min():%Y-%m} to {predicted['timestamp'].max():%Y-%m}"
        )

    report = [
        f"# [{museum_code}] Deepavali month: Actual vs Predicted",
        "",
        f"Deepavali months are read from {DEEPAVALI_CSV}. {periods}.",
        "",
        f"**Best model:** {best_name}",
        "- A positive difference means the model over-predicted.",
        "- A negative difference means the model under-predicted.",
        "",
        "## Deepavali months in the eval + predict period",
        "",
        *(table_lines(museum_code) or []),
    ]

    target = f"./outputs/{museum_code}/{museum_code}_deepavali.md"
    pathlib.Path(target).write_text("\n".join(report) + "\n", encoding="utf-8")
    return target
