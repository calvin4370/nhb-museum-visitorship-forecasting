import numpy as np
import pandas as pd
import os

from src.features.data_prep import prepare_eval_data, prepare_predict_data
from src.data.singstat_api import singstat_api
from src.visualisation.timeplot import timeplot, forecast_table

from src.models.randomforest import randomforest
from src.models.xgboost_model import xgb
from src.models.lstm import lstm
from src.models.timegpt import timegpt
from src.models.holtwinters import hw
from src.models.sarimax import sarimax_model
from src.models.baseline import baseline
from src.models.svr import support_vec

# ------------------------------ CONSTANTS ------------------------------ #
MUSEUM_CODES = {
    "Asian Civilisations Museum": "ACM",
    "National Museum Of Singapore": "NMS",
    "Peranakan Museum": "PM",
    "Indian Heritage Centre": "IHC",
    "Malay Heritage Centre": "MHC",
}
START_YEAR, START_MONTH = 2013, "Jan"
END_YEAR, END_MONTH = 2025, "Mar"

h = 24  # set prediction/forecast periods ahead, default 2 years (i.e., 24 months)
# ----------------------------------------------------------------------- #

MUSEUMS = list(MUSEUM_CODES.keys())


# ---------------------------- MODEL REGISTRY ---------------------------- #
# Adapter functions to normalize all 8 models to one call shape where:
# Inputs: (train, test, full, run_eval, best_params=None)
# Outputs: (model_eval, forecast, best_params)
def _tunable_adapter(model_fn):
    """
    rf / xgb / svr / hw / sarimax: accept + return best_params.
    """
    def adapter(train_data, test_data, full_data, run_eval, best_params=None):
        return model_fn(train_data, test_data, run_eval, best_params=best_params)
    return adapter


def _lstm_adapter(train_data, test_data, full_data, run_eval, best_params=None):
    """
    lstm has a different signature (full_data, run_eval, h) and no tuning.
    """
    model_eval, forecast = lstm(full_data, run_eval, h)
    return model_eval, forecast, None


def _simple_adapter(model_fn):
    """
    timegpt / baseline: no tunable hyperparameters.
    """
    def adapter(train_data, test_data, full_data, run_eval, best_params=None):
        model_eval, forecast = model_fn(train_data, test_data, run_eval)
        return model_eval, forecast, None
    return adapter


MODEL_REGISTRY = {
    "rf": _tunable_adapter(randomforest),
    "xgb": _tunable_adapter(xgb),
    "svr": _tunable_adapter(support_vec),
    "hw": _tunable_adapter(hw),
    "sarimax": _tunable_adapter(sarimax_model),
    "lstm": _lstm_adapter,
    "timegpt": _simple_adapter(timegpt),
    "baseline": _simple_adapter(baseline),
}
# ----------------------------------------------------------------------- #


# Call SingStat API to get the museum visitorship and international arrivals data
visitors = singstat_api("M891071", START_YEAR, START_MONTH, END_YEAR, END_MONTH)
arrivals = singstat_api("M550001", START_YEAR, START_MONTH, END_YEAR, END_MONTH)

# Export to csv
visitors.to_csv("./data/raw/museum_ts.csv", index=False)
arrivals.to_csv("./data/raw/intl_arrivals.csv", index=False)


def run_museum_pipeline(museum):
    """
    Train and perform hyperparameter tuning for all 8 models for one museum,
    pick the best model by lowest RMSE, then predict with only that model,
    reusing its tuned hyperparameters. All of this museum's outputs (plots,
    model_eval, predictions) are written to outputs/{museum_code}/ as they're produced.
    """
    museum_code = MUSEUM_CODES[museum]
    os.makedirs(f"./outputs/{museum_code}", exist_ok=True)

    # Filter for the museum's visitors
    museum_ts = visitors.loc[visitors.loc[:, "Data Series"] == museum, :]

    # Train and evaluate all models, performing hyperparameter tuning where applicable
    train_data, test_data, full_data = prepare_eval_data(museum_ts)
    full_data.to_csv(f"./data/processed/{museum_code}_eval.csv", index=False)

    eval_rows = []      # [(key, [Model, RMSE, MAPE]), ...]   (one per surviving model)
    tuned_params = {}   # key -> best_params (or None for non-tunable models)
    pretty_names = {}   # key -> pretty model name (e.g. "XGBoost"), for plot titles

    for key, model_fn in MODEL_REGISTRY.items():
        try:
            model_eval, forecast, best_params = model_fn(
                train_data, test_data, full_data, True
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
        timeplot(
            f"./outputs/{museum_code}/{museum_code}_eval_{key}_timeplot.png",
            f"{museum} — {model_eval[0]} Eval",
            train_data, test_data, forecast, True,
        )

    if not eval_rows:
        raise RuntimeError(f"All models failed eval for {museum}; cannot select a winner")

    model_eval_df = pd.DataFrame(
        [row for _, row in eval_rows], columns=["Model", "RMSE", "MAPE"]
    )
    model_eval_df["Institution"] = museum
    model_eval_df = model_eval_df[["Institution", "Model", "RMSE", "MAPE"]]

    # Format metrics and write this museum's eval results
    model_eval_df_formatted = model_eval_df.copy()
    model_eval_df_formatted["RMSE"] = model_eval_df_formatted["RMSE"].apply(lambda x: f"{x:.2f}")
    model_eval_df_formatted["MAPE"] = model_eval_df_formatted["MAPE"].apply(lambda x: f"{x:.2%}")
    model_eval_df_formatted.to_csv(f"./outputs/{museum_code}/{museum_code}_model_eval.csv", index=False)

    # Select the best model based on lowest RMSE
    best_idx = model_eval_df["RMSE"].idxmin()
    best_key = eval_rows[best_idx][0]
    print(f"  [{museum}] winning model: {best_key} (RMSE={model_eval_df.loc[best_idx, 'RMSE']:.2f})")

    # Predict with only the winning model
    predict_train, predict_test, predict_full = prepare_predict_data(museum_ts, h)
    predict_full.to_csv(f"./data/processed/{museum_code}_predict.csv", index=False)
    _, forecast, _ = MODEL_REGISTRY[best_key](
        predict_train, predict_test, predict_full, False,
        best_params=tuned_params[best_key],
    )
    timeplot(
        f"./outputs/{museum_code}/{museum_code}_predict_{best_key}_timeplot.png",
        f"{museum} — {pretty_names[best_key]} Predict",
        predict_train, predict_test, forecast, False,
    )

    forecast_df = forecast_table(best_key, np.asarray(forecast))
    forecast_df["Institution"] = museum
    forecast_df["Month"] = predict_test["timestamp"].dt.month
    forecast_df["Year"] = predict_test["timestamp"].dt.year
    forecast_df = forecast_df[["Institution", "Model", "Year", "Month", "Prediction"]]
    forecast_df.to_csv(f"./outputs/{museum_code}/{museum_code}_{best_key}_predictions.csv", index=False)


# Run the pipeline for each museum -- each museum writes its own outputs directly
for museum in MUSEUMS:
    print(f"=== {museum} ===")
    run_museum_pipeline(museum)
    print(f"=== {museum} complete ===\n")
