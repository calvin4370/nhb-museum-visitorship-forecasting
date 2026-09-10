"""Normalizes all 8 forecasting models to one uniform call shape so the
pipeline can loop over them generically:

    adapter(train_data, test_data, full_data, run_eval, best_params=None)
        -> (model_eval, forecast, best_params)
"""
from config import h
from src.models.randomforest import randomforest
from src.models.xgboost_model import xgb
from src.models.lstm import lstm
from src.models.timegpt import timegpt
from src.models.holtwinters import hw
from src.models.sarimax import sarimax_model
from src.models.baseline import baseline
from src.models.svr import support_vec


def _tunable_adapter(model_fn):
    """rf / xgb / svr / hw / sarimax: accept + return best_params."""
    def adapter(train_data, test_data, full_data, run_eval, best_params=None):
        return model_fn(train_data, test_data, run_eval, best_params=best_params)
    return adapter


def _lstm_adapter(train_data, test_data, full_data, run_eval, best_params=None):
    """lstm has a different signature (full_data, run_eval, h) and no tuning."""
    model_eval, forecast = lstm(full_data, run_eval, h)
    return model_eval, forecast, None


def _simple_adapter(model_fn):
    """timegpt / baseline: no tunable hyperparameters."""
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
