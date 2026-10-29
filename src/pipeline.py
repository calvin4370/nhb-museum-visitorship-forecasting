"""Per-museum orchestration: eval all models, rank by RMSE, predict with
EVERY surviving model (each reusing its own tuned hyperparameters), and write
all of that museum's outputs to outputs/{museum_code}/.

write_tuning_report() is the one exception: it spans every museum, so callers
run it once after the loop rather than inside it."""

import os

import numpy as np
import pandas as pd

from config import MUSEUM_CODES, MODEL_NAMES, h, features_for
from src.features.data_prep import prepare_eval_data, prepare_predict_data
from src.visualisation.timeplot import timeplot, forecast_table, top_n_timeplot
from src.visualisation.jj_new_plots import EVAL_DIR, PREDICT_DIR, new_timeplot, new_top_n_timeplot
from src.visualisation.summary import FY_totals, write_summary_txt, write_summary_md
from src.models.model_registry import MODEL_REGISTRY
from src.analysis.artifacts import museum_dir, save_model
from src.visualisation.feature_report import build_report
from src.analysis.importance import permutation_importance
from src.analysis.deepavali import build_report as build_deepavali_report
from src.analysis.tuning_report import build_report as build_tuning_report


def write_tuning_report():
    """Summarise the saved Optuna studies into outputs/tuning_report.md.

    Cross-museum, unlike everything else here, so callers run it once after
    every museum rather than inside the per-museum loop.

    Returns:
        str | None: The file written, or None if no studies were found.
    """
    written = build_tuning_report()
    print(f"wrote {written}" if written else "no studies found under outputs/tuning/")
    return written


def clear_model_outputs(museum_code, keys):
    """Delete the per-model files each key would regenerate this run.

    A model that raises mid-run leaves last run's predictions and plots on disk,
    where the deepavali report and any cross-branch comparison read them as if
    they were current. Clearing first means anything still present afterwards
    was actually produced by this run.

    Args:
        museum_code (str): Short museum code, e.g. "IHC".
        keys (iterable[str]): Short model keys about to be run.
    """
    for key in keys:
        stale = [
            f"./outputs/{museum_code}/eval/{museum_code}_{key}_predictions.csv",
            f"./outputs/{museum_code}/eval/{museum_code}_eval_{key}_timeplot.png",
            f"./outputs/{museum_code}/eval/{EVAL_DIR}/{museum_code}_eval_{key}_timeplot.png",
            f"./outputs/{museum_code}/predict/{museum_code}_{key}_predictions.csv",
            f"./outputs/{museum_code}/predict/{museum_code}_predict_{key}_timeplot.png",
            f"./outputs/{museum_code}/predict/{PREDICT_DIR}/{museum_code}_predict_{key}_timeplot.png",
        ]
        for path in stale:
            if os.path.exists(path):
                os.remove(path)


def run_museum_pipeline(museum, visitors, arrivals, models=None):
    """
    Train and perform hyperparameter tuning for all 8 models for one museum.
    Every best tuned model then predicts, reusing its own tuned hyperparameters. 
    Eval plots are saved to outputs/{museum_code}/eval/, 
    predict plots + per-model predictions go to outputs/{museum_code}/predict/,
    {museum_code}_model_eval.csv (sorted lowest-RMSE-first) and {museum_code}_summary.txt
    (eval table + FY totals) go directly under outputs/{museum_code}/.
    """
    museum_code = MUSEUM_CODES[museum]
    os.makedirs(f"./outputs/{museum_code}/eval", exist_ok=True)
    os.makedirs(f"./outputs/{museum_code}/predict", exist_ok=True)
    os.makedirs("./data/processed", exist_ok=True)

    # Filter for the museum's visitors
    museum_ts = visitors.loc[visitors.loc[:, "Data Series"] == museum, :]

    # Resolved once so eval and predict tune and forecast on the same features
    features = features_for(museum_code)

    # Train and evaluate all models, performing hyperparameter tuning where applicable
    train_data, test_data, full_data = prepare_eval_data(museum_ts, arrivals)
    full_data.to_csv(f"./data/processed/{museum_code}_eval.csv", index=False)

    # Fail loudly here rather than deep inside a model mid-run. Checked on
    # train_data, not full_data: monthly_avg is added by the train/test split
    missing = [f for f in features if f not in train_data.columns]
    if missing:
        raise ValueError(f"{museum_code} features not engineered: {', '.join(missing)}")

    eval_rows = []  # [(key, [Model, RMSE, MAPE]), ...]   (one per surviving model)
    importance_rows = []  # per-model permutation importance frames
    tuned_params = {}  # key -> best_params (or None for non-tunable models)
    pretty_names = {}  # key -> pretty model name (e.g. "XGBoost"), for plot titles

    selected_models = (
        MODEL_REGISTRY if models is None
        else {key: MODEL_REGISTRY[key] for key in models}
    )

    # Ensure that any leftover outputs from a previous run are cleared before this run starts
    # in case any models in this run fails, the old results will not be used in the report
    clear_model_outputs(museum_code, selected_models)

    for key, model_fn in selected_models.items():
        try:
            model_eval, forecast, best_params, fitted = model_fn(
                train_data, test_data, full_data, True, features
            )
        except Exception as e:
            print(f"  [{museum}] {key} failed during eval, skipping: {e}")
            continue

        if not model_eval:
            print(f"  [{museum}] {key} returned no eval metrics, skipping")
            continue

        eval_rows.append((key, model_eval))
        tuned_params[key] = best_params
        pretty_names[key] = model_eval[0]

        # Scored on eval, the only labelled data: the predict horizon has no actuals
        if fitted is not None and fitted.predict is not None:
            scores = permutation_importance(fitted.predict, test_data, features)
            scores.insert(0, "model", key)
            importance_rows.append(scores)

        # Save eval-period predictions
        eval_forecast_df = forecast_table(key, np.asarray(forecast).ravel())
        eval_forecast_df["Institution"] = museum
        eval_forecast_df["Year"] = test_data["timestamp"].dt.year.values
        eval_forecast_df["Month"] = test_data["timestamp"].dt.month.values
        eval_forecast_df["Actual"] = test_data["value"].values
        eval_forecast_df = eval_forecast_df[
            ["Institution", "Model", "Year", "Month", "Actual", "Prediction"]
        ]
        eval_forecast_df.to_csv(
            f"./outputs/{museum_code}/eval/{museum_code}_{key}_predictions.csv",
            index=False,
        )

        timeplot(
            f"./outputs/{museum_code}/eval/{museum_code}_eval_{key}_timeplot.png",
            f"{museum_code} — {model_eval[0]} Eval",
            train_data,
            test_data,
            forecast,
            True,
        )
        new_timeplot(
            f"./outputs/{museum_code}/eval/{museum_code}_eval_{key}_timeplot.png",
            f"{museum_code} — {model_eval[0]} Eval",
            train_data,
            test_data,
            forecast,
            True,
        )

    if not eval_rows:
        raise RuntimeError(
            f"All models failed eval for {museum}; cannot select a winner"
        )

    model_eval_df = pd.DataFrame(
        [row for _, row in eval_rows], columns=["Model", "RMSE", "MAPE"]
    )
    model_eval_df["Institution"] = museum
    model_eval_df["_key"] = [key for key, _ in eval_rows]
    model_eval_df = model_eval_df[["Institution", "Model", "RMSE", "MAPE", "_key"]]

    # Sort rows by lowest-RMSE first
    model_eval_df = model_eval_df.sort_values("RMSE").reset_index(drop=True)

    # Format metrics and write this museum's eval results
    model_eval_df_formatted = model_eval_df.drop(columns="_key").copy()
    model_eval_df_formatted["RMSE"] = model_eval_df_formatted["RMSE"].apply(
        lambda x: f"{x:.2f}"
    )
    model_eval_df_formatted["MAPE"] = model_eval_df_formatted["MAPE"].apply(
        lambda x: f"{x:.2%}"
    )
    model_eval_df_formatted.to_csv(
        f"./outputs/{museum_code}/{museum_code}_model_eval.csv", index=False
    )

    best_key = model_eval_df.iloc[0]["_key"]
    print(
        f"  [{museum}] winning model: {best_key} (RMSE={model_eval_df.iloc[0]['RMSE']:.2f})"
    )

    # Predict with every surviving model, each reusing its own tuned hyperparameters
    predict_train, predict_test, predict_full = prepare_predict_data(museum_ts, arrivals, h)
    predict_full.to_csv(f"./data/processed/{museum_code}_predict.csv", index=False)

    per_model_fy = {}  # key -> Series (FY label -> total predicted visitors)
    per_model_forecast = {}  # key -> raw forecast array, for the top-3 overlay plot
    winner_forecast_fy = (
        None  # Series for just the winning model, used in the FY totals table
    )

    # Fresh directory per run
    artifact_dir = museum_dir(museum_code)

    for key in model_eval_df["_key"]:
        _, forecast, _, fitted = MODEL_REGISTRY[key](
            predict_train,
            predict_test,
            predict_full,
            False,
            features,
            best_params=tuned_params[key],
        )

        # The predict-mode fit is the one that produced the shipped forecast
        save_model(artifact_dir, key, fitted)

        # Save the timeplot to outputs/{museum_code}/predict/
        timeplot(
            f"./outputs/{museum_code}/predict/{museum_code}_predict_{key}_timeplot.png",
            f"{museum_code} — {pretty_names[key]} Predict",
            predict_train,
            predict_test,
            forecast,
            False,
        )
        new_timeplot(
            f"./outputs/{museum_code}/predict/{museum_code}_predict_{key}_timeplot.png",
            f"{museum_code} — {pretty_names[key]} Predict",
            predict_train,
            predict_test,
            forecast,
            False,
        )

        # Save the per-model predictions to outputs/{museum_code}/predict/
        forecast_df = forecast_table(key, np.asarray(forecast))
        forecast_df["Institution"] = museum
        forecast_df["Month"] = predict_test["timestamp"].dt.month
        forecast_df["Year"] = predict_test["timestamp"].dt.year
        forecast_df = forecast_df[
            ["Institution", "Model", "Year", "Month", "Prediction"]
        ]
        forecast_df.to_csv(
            f"./outputs/{museum_code}/predict/{museum_code}_{key}_predictions.csv",
            index=False,
        )

        # Compute the per-model FY totals, and store in per_model_fy[key]
        # .ravel() handles LSTM's (n, 1) forecast shape -- the dict-based
        # DataFrame constructor requires strictly 1-D arrays, unlike
        # forecast_table()'s positional constructor above, which accepts either.
        fy_series = FY_totals(
            pd.DataFrame(
                {
                    "timestamp": predict_test["timestamp"],
                    "value": np.asarray(forecast).ravel(),
                }
            )
        )
        per_model_fy[key] = fy_series
        per_model_forecast[key] = np.asarray(forecast).ravel()
        if key == best_key:
            winner_forecast_fy = fy_series

    # Overlay plot: top 3 models by RMSE, each its own color, with a legend.
    # model_eval_df["_key"] is already sorted lowest-RMSE-first.
    top3_keys = list(model_eval_df["_key"])[:3]
    top_n_timeplot(
        f"./outputs/{museum_code}/predict/{museum_code}_predict_top3_timeplot.png",
        f"{museum_code} — Top 3 Models Predict",
        predict_train,
        predict_test,
        [(key, per_model_forecast[key]) for key in top3_keys],
    )
    new_top_n_timeplot(
        f"./outputs/{museum_code}/predict/{museum_code}_predict_top3_timeplot.png",
        f"{museum_code} — Top 3 Models Predict",
        predict_train,
        predict_test,
        [(key, per_model_forecast[key]) for key in top3_keys],
    )

    # Table: total visitors by FY, including historical actuals + winning model's forecast.
    hist_fy = FY_totals(predict_train)
    fy_table = hist_fy.add(winner_forecast_fy, fill_value=0).sort_index().reset_index()
    fy_table.columns = ["FY", "Total Visitors ('000s)"]

    # Tag forecasted FYs with "(Prediction)" in the FY column
    predicted_fys = set(winner_forecast_fy.index)
    fy_table["FY"] = fy_table["FY"].apply(
        lambda fy: f"{fy} (Prediction)" if fy in predicted_fys else fy
    )
    fy_table["Total Visitors ('000s)"] = fy_table["Total Visitors ('000s)"].apply(
        lambda x: f"{x:,.1f}"
    )

    # Table: every surviving model's own forecast FY totals, alongside its eval metrics
    fy_cols = sorted({fy for series in per_model_fy.values() for fy in series.index})
    per_model_rows = []
    for _, row in model_eval_df.iterrows():
        key = row["_key"]
        per_model_rows.append(
            {
                "Model": row["Model"],
                "RMSE": f"{row['RMSE']:.2f}",
                "MAPE": f"{row['MAPE']:.2%}",
                **{fy: f"{per_model_fy[key].get(fy):,.1f}" for fy in fy_cols},
            }
        )
    per_model_fy_df = pd.DataFrame(per_model_rows)

    # One importance table per museum
    if importance_rows:
        importance = pd.concat(importance_rows, ignore_index=True)
        importance.insert(0, "Institution", museum)
        importance.to_csv(f"{artifact_dir}/permutation_importance.csv", index=False)


    # Write the summary report to outputs/{museum_code}/{museum_code}_summary.txt
    write_summary_txt(
        f"./outputs/{museum_code}/{museum_code}_summary.txt",
        museum_code=museum_code,
        eval_table=model_eval_df_formatted.drop(columns="Institution"),
        fy_table=fy_table,
        per_model_fy_table=per_model_fy_df,
    )
    # IHC only; returns None for every other museum
    deepavali_report = build_deepavali_report(museum_code)
    if deepavali_report:
        print(f"  wrote {deepavali_report}")

    write_summary_md(
        f"./outputs/{museum_code}/{museum_code}_summary.md",
        museum_code=museum_code,
        eval_table=model_eval_df_formatted.drop(columns="Institution"),
        fy_table=fy_table,
        per_model_fy_table=per_model_fy_df,
    )

    # Generate the permutation importance report
    build_report(museum_code)


def regen_museum_outputs(museum):
    """
    Rebuild one museum's plots and summary reports from the last run's saved
    predictions, without refitting anything. Reads the cached feature frames in
    data/processed/ and the per-model prediction CSVs already under outputs/.
    """
    museum_code = MUSEUM_CODES[museum]
    key_by_name = {name: key for key, name in MODEL_NAMES.items()}

    # The eval split is positional, so it reproduces exactly from the cached frame
    eval_full = pd.read_csv(f"./data/processed/{museum_code}_eval.csv", parse_dates=["timestamp"])
    split_point = int(len(eval_full) * 0.8)
    train_data, test_data = eval_full[:split_point], eval_full[split_point:]

    # Predict frame is history plus exactly h synthetic future rows on the end
    predict_full = pd.read_csv(f"./data/processed/{museum_code}_predict.csv", parse_dates=["timestamp"])
    predict_train, predict_test = predict_full[:-h], predict_full[-h:]

    # Model order and metrics come from the eval table, already sorted by RMSE
    eval_table = pd.read_csv(f"./outputs/{museum_code}/{museum_code}_model_eval.csv")
    keys = [key_by_name[name] for name in eval_table["Model"]]
    best_key = keys[0]

    # Redraw each model's eval plot from its saved eval-period predictions
    for key in keys:
        path = f"./outputs/{museum_code}/eval/{museum_code}_{key}_predictions.csv"
        if not os.path.exists(path):
            print(f"  [{museum}] no saved eval predictions for {key}, skipping its plot")
            continue
        timeplot(
            f"./outputs/{museum_code}/eval/{museum_code}_eval_{key}_timeplot.png",
            f"{museum_code} - {MODEL_NAMES[key]} Eval",
            train_data,
            test_data,
            pd.read_csv(path)["Prediction"].values,
            True,
        )
        new_timeplot(
            f"./outputs/{museum_code}/eval/{museum_code}_eval_{key}_timeplot.png",
            f"{museum_code} — {MODEL_NAMES[key]} Eval",
            train_data,
            test_data,
            pd.read_csv(path)["Prediction"].values,
            True,
        )

    # Redraw each predict plot, collecting the forecasts the tables are built from
    per_model_fy = {}
    per_model_forecast = {}
    for key in keys:
        path = f"./outputs/{museum_code}/predict/{museum_code}_{key}_predictions.csv"
        if not os.path.exists(path):
            print(f"  [{museum}] no saved predictions for {key}, skipping its plot")
            continue
        forecast = pd.read_csv(path)["Prediction"].values
        timeplot(
            f"./outputs/{museum_code}/predict/{museum_code}_predict_{key}_timeplot.png",
            f"{museum_code} - {MODEL_NAMES[key]} Predict",
            predict_train,
            predict_test,
            forecast,
            False,
        )
        new_timeplot(
            f"./outputs/{museum_code}/predict/{museum_code}_predict_{key}_timeplot.png",
            f"{museum_code} — {MODEL_NAMES[key]} Predict",
            predict_train,
            predict_test,
            forecast,
            False,
        )
        per_model_forecast[key] = forecast
        per_model_fy[key] = FY_totals(
            pd.DataFrame({"timestamp": predict_test["timestamp"], "value": forecast})
        )

    if best_key not in per_model_fy:
        raise RuntimeError(
            f"{museum_code}: no saved predictions for the winning model ({best_key})"
        )

    # Overlay plot: the same top 3 by RMSE the run itself would have picked
    top3_keys = [key for key in keys if key in per_model_forecast][:3]
    top_n_timeplot(
        f"./outputs/{museum_code}/predict/{museum_code}_predict_top3_timeplot.png",
        f"{museum_code} - Top 3 Models Predict",
        predict_train,
        predict_test,
        [(key, per_model_forecast[key]) for key in top3_keys],
    )
    new_top_n_timeplot(
        f"./outputs/{museum_code}/predict/{museum_code}_predict_top3_timeplot.png",
        f"{museum_code} — Top 3 Models Predict",
        predict_train,
        predict_test,
        [(key, per_model_forecast[key]) for key in top3_keys],
    )

    # Table: historical actuals plus the winner's forecast, totalled by FY
    winner_forecast_fy = per_model_fy[best_key]
    hist_fy = FY_totals(predict_train)
    fy_table = hist_fy.add(winner_forecast_fy, fill_value=0).sort_index().reset_index()
    fy_table.columns = ["FY", "Total Visitors ('000s)"]
    predicted_fys = set(winner_forecast_fy.index)
    fy_table["FY"] = fy_table["FY"].apply(
        lambda fy: f"{fy} (Prediction)" if fy in predicted_fys else fy
    )
    fy_table["Total Visitors ('000s)"] = fy_table["Total Visitors ('000s)"].apply(
        lambda x: f"{x:,.1f}"
    )

    # Table:every model's forecast FY totals beside its eval metrics. RMSE and MAPE
    # are already formatted in the eval csv, so they carry straight over
    fy_cols = sorted({fy for series in per_model_fy.values() for fy in series.index})
    per_model_rows = []
    for _, row in eval_table.iterrows():
        key = key_by_name[row["Model"]]
        if key not in per_model_fy:
            continue
        per_model_rows.append(
            {
                "Model": row["Model"],
                "RMSE": row["RMSE"],
                "MAPE": row["MAPE"],
                **{fy: f"{per_model_fy[key].get(fy):,.1f}" for fy in fy_cols},
            }
        )
    per_model_fy_df = pd.DataFrame(per_model_rows)

    summary_args = dict(
        museum_code=museum_code,
        eval_table=eval_table.drop(columns="Institution"),
        fy_table=fy_table,
        per_model_fy_table=per_model_fy_df,
    )
    write_summary_txt(f"./outputs/{museum_code}/{museum_code}_summary.txt", **summary_args)
    # IHC only; returns None for every other museum
    deepavali_report = build_deepavali_report(museum_code)
    if deepavali_report:
        print(f"  wrote {deepavali_report}")

    write_summary_md(f"./outputs/{museum_code}/{museum_code}_summary.md", **summary_args)

    # Rebuilt from the importance CSV the last run saved, so nothing is refitted
    build_report(museum_code)
