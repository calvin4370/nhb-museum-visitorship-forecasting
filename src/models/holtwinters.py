import pandas as pd
import numpy as np

import optuna
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_percentage_error, root_mean_squared_error

def hw(train_data, test_data, eval, best_params=None):
    # Prepare input data for Holt Winters
    train_X = train_data.set_index("timestamp")["value"]
    train_X = train_X.asfreq('MS')
    seasonal_periods = 12

    random_state = 42

    # If best_params is provided, use it
        # Else, perform hyperparameter optimization with Optuna
    if best_params is None:
        def objective(trial, data=train_X, seasonal_periods=12):
            # Define the hyperparameter search space
            params = {
                'smoothing_level': trial.suggest_float('smoothing_level', 0, 1),
                'smoothing_trend': trial.suggest_float('smoothing_trend', 0, 1),
                'smoothing_seasonal': trial.suggest_float('smoothing_seasonal', 0, 1)
            }

            # Define the trend type
            trend = trial.suggest_categorical('trend', ['add','mul'])
            seasonal = trial.suggest_categorical('seasonal', ['add','mul'])

            # Rolling-origin folds, each validating a full 12-month season
            tscv = TimeSeriesSplit(n_splits=3, test_size=12)
            errors = []

            try:
                for train_idx, val_idx in tscv.split(data):
                    tr, val = data.iloc[train_idx], data.iloc[val_idx]
                    fitted_model = ExponentialSmoothing(
                        tr,
                        seasonal_periods=seasonal_periods,
                        trend=trend,
                        seasonal=seasonal
                    ).fit(**params)
                    errors.append(
                        root_mean_squared_error(val, fitted_model.forecast(len(val_idx)))
                    )
                return np.mean(errors)

            except Exception as e:
                return float('inf')

        sampler = optuna.samplers.TPESampler(seed=random_state)
        study = optuna.create_study(direction="minimize", sampler=sampler)
        study.optimize(objective, n_trials=50)
        best_params = study.best_params

    # Extract trend/seasonal from best_params as they are constructor args, not .fit()
    # args -- keep them in best_params itself (don't mutate/pop) so the same dict can be
    # returned and reused as-is for a later call.
    trend = best_params['trend']
    seasonal = best_params['seasonal']
    fit_params = {k: v for k, v in best_params.items() if k not in ('trend', 'seasonal')}

    best_model = ExponentialSmoothing(
        train_X,
        seasonal_periods=seasonal_periods,
        trend=trend,
        seasonal=seasonal
    )
    best_model_fitted = best_model.fit(**fit_params)

    # Forecasting
    forecast_periods = len(test_data["value"])
    forecast = best_model_fitted.forecast(forecast_periods)
    test_data["Forecast"] = forecast.values

    if eval:
        # Metrics Calculation
        rmse_hw = root_mean_squared_error(test_data["value"], test_data["Forecast"])
        mape_hw = mean_absolute_percentage_error(test_data["value"], test_data["Forecast"])

        model_eval= ['Holt-Winters exponential smoothing', rmse_hw, mape_hw]
    else:
        model_eval = []

    return model_eval, forecast.values, best_params