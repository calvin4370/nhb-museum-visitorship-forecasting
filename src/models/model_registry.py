"""Normalizes all 8 forecasting models to one uniform call shape so the
pipeline can loop over them generically:

    adapter(train_data, test_data, full_data, run_eval, features, best_params=None)
        -> (model_eval, forecast, best_params, fitted)

`fitted` is a Fitted holding the trained estimator for saving, and where the
model has a tabular feature interface, a callable to predict raw rows with it.

`features` is the museum's tabular feature list; models that do not read it
(hw, lstm, timegpt, baseline) absorb it in their adapter rather than their
own signature.
"""
from config import h, MODEL_KEYS, lstm_channels
from src.models.randomforest import randomforest
from src.models.xgboost_model import xgb
from src.models.lstm import lstm
from src.models.timegpt import timegpt
from src.models.holtwinters import hw
from src.models.sarimax import sarimax_model
from src.models.baseline import baseline
from src.models.svr import support_vec


def _tunable_adapter(model_fn):
    """rf / xgb / svr / sarimax: train on `features`, accept + return best_params."""
    def adapter(train_data, test_data, full_data, run_eval, features, best_params=None):
        return model_fn(train_data, test_data, run_eval, features, best_params=best_params)
    return adapter


def _univariate_tunable_adapter(model_fn):
    """hw: tunable, but forecasts off 'value' alone."""
    def adapter(train_data, test_data, full_data, run_eval, features, best_params=None):
        return model_fn(train_data, test_data, run_eval, best_params=best_params)
    return adapter


def _lstm_adapter(train_data, test_data, full_data, run_eval, features, best_params=None):
    """lstm has a different signature (full_data, run_eval, h), no tuning, and
    reads the museum's non-lag features as per-timestep channels."""
    model_eval, forecast, fitted = lstm(full_data, run_eval, h, lstm_channels(features))
    return model_eval, forecast, None, fitted


def _simple_adapter(model_fn):
    """timegpt / baseline: no tunable hyperparameters, and no model object to save."""
    def adapter(train_data, test_data, full_data, run_eval, features, best_params=None):
        model_eval, forecast = model_fn(train_data, test_data, run_eval)
        return model_eval, forecast, None, None
    return adapter


MODEL_REGISTRY = {
    "rf": _tunable_adapter(randomforest),
    "xgb": _tunable_adapter(xgb),
    "svr": _tunable_adapter(support_vec),
    "hw": _univariate_tunable_adapter(hw),
    "sarimax": _tunable_adapter(sarimax_model),
    "lstm": _lstm_adapter,
    "timegpt": _simple_adapter(timegpt),
    "baseline": _simple_adapter(baseline),
}

# Ensure model registry keys match the config's MODEL_KEYS list
assert list(MODEL_REGISTRY) == MODEL_KEYS, (
    f"MODEL_REGISTRY keys {list(MODEL_REGISTRY)} do not match config.MODEL_KEYS {MODEL_KEYS}"
)
