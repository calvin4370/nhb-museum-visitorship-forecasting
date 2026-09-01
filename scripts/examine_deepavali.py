"""
Report how the best model performed in the Deepavali months of IHC
"""
import sys
from pathlib import Path

# Running a script puts scripts/ on the path, not the project root, so add it.
# Resolved from this file rather than the cwd, so the script runs from anywhere
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

DEEPAVALI_CSV = "./src/events/event_ranges/deepavali.csv"

# Only examine for IHC, since the other museums dont have is_deepavali feature activated
MUSEUM_CODE = "IHC"

# The eval table names models in full; prediction files are named by short key
MODEL_KEYS = {
    "Random Forest Regressor": "rf",
    "XGBoost": "xgb",
    "Support Vector Regression": "svr",
    "Holt-Winters exponential smoothing": "hw",
    "SARIMAX": "sarimax",
    "LSTM": "lstm",
    "TimeGPT": "timegpt",
    "Baseline Monthly Mean": "baseline",
}


def main():
    import pandas as pd

    deepavali = pd.read_csv(DEEPAVALI_CSV)
    deepavali["start"] = pd.to_datetime(deepavali["start"])

    eval_path = f"./outputs/{MUSEUM_CODE}/{MUSEUM_CODE}_model_eval.csv"
    if not Path(eval_path).exists():
        print(f"  [{MUSEUM_CODE}] no eval results, nothing to report")
        return

    # The eval table is written lowest-RMSE-first, so the winner is row one
    evaluation = pd.read_csv(eval_path)
    best_name = evaluation.iloc[0]["Model"]
    best_key = MODEL_KEYS.get(best_name)

    predictions_path = (
        f"./outputs/{MUSEUM_CODE}/eval/{MUSEUM_CODE}_{best_key}_predictions.csv"
    )
    if best_key is None or not Path(predictions_path).exists():
        print(f"  [{MUSEUM_CODE}] no saved eval predictions for {best_name}")
        return

    # Eval predictions carry their own actuals, so no other source is needed
    evaluated = pd.read_csv(predictions_path)
    evaluated["timestamp"] = pd.to_datetime(
        dict(year=evaluated["Year"], month=evaluated["Month"], day=1)
    )
    eval_months = evaluated[
        evaluated["timestamp"].isin(deepavali["start"])
    ].sort_values("timestamp")

    # The predict horizon has no actuals, so only the forecast is shown for it
    predict_path = (
        f"./outputs/{MUSEUM_CODE}/predict/{MUSEUM_CODE}_{best_key}_predictions.csv"
    )
    predict_months = pd.DataFrame()
    if Path(predict_path).exists():
        predicted = pd.read_csv(predict_path)
        predicted["timestamp"] = pd.to_datetime(
            dict(year=predicted["Year"], month=predicted["Month"], day=1)
        )
        predict_months = predicted[
            predicted["timestamp"].isin(deepavali["start"])
        ].sort_values("timestamp")

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
        f"# [{MUSEUM_CODE}] Deepavali month: Actual vs Predicted",
        "",
        f"Deepavali months are read from {DEEPAVALI_CSV}. {periods}.",
        "",
        f"**Best model:** {best_name}",
        "- A positive difference means the model over-predicted.",
        "- A negative difference means the model under-predicted.",
        "",
        "## Deepavali months in the eval + predict period",
        "",
        "| Month | Actual | Predicted | Difference | % difference |",
        "|---|---|---|---|---|",
        *rows,
    ]

    target = f"./outputs/{MUSEUM_CODE}/{MUSEUM_CODE}_deepavali.md"
    Path(target).write_text("\n".join(report) + "\n", encoding="utf-8")
    print(f"  wrote {target}")


if __name__ == "__main__":
    main()
