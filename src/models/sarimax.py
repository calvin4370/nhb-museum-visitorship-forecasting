import pandas as pd
import numpy as np

import optuna
from statsmodels.tsa.statespace.sarimax import SARIMAX
from src.models.fitted import Fitted
from src.analysis.tuning import create_study
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_percentage_error, root_mean_squared_error

import warnings

warnings.filterwarnings('ignore')

def sarimax_model(train_data, test_data, eval, features, best_params=None):
    # Target the caller's feature list predicts
    target = "value"

    # Set seed for reproducibility
    random_state = 42

    # Standardise exogenous features
    scaler = StandardScaler()
    train_exog = pd.DataFrame(
        scaler.fit_transform(train_data[features]),
        columns=features, index=train_data.index,
    )
    test_exog = pd.DataFrame(
        scaler.transform(test_data[features]),
        columns=features, index=test_data.index,
    )

    # If best_params is provided, use it
    # Else, perform hyperparameter optimization with Optuna
    if best_params is None:
        def objective(trial):
            # Define the search space
            # Non-seasonal params
            p = trial.suggest_int('p', 0, 5)
            d = trial.suggest_int('d', 0, 2)
            q = trial.suggest_int('q', 0, 5)
            # Seasonal params
            P = trial.suggest_int('P', 0, 2)
            D = trial.suggest_int('D', 0, 1)
            Q = trial.suggest_int('Q', 0, 2)

            # Rolling-origin folds, each validating a full 12-month season. Endog
            # stays unscaled -- only exog needs standardising
            tscv = TimeSeriesSplit(n_splits=3, test_size=12)
            errors = []

            try:
                for train_idx, val_idx in tscv.split(train_data):
                    tr_endog = train_data[target].iloc[train_idx]
                    val_endog = train_data[target].iloc[val_idx]
                    tr_exog = train_exog.iloc[train_idx]
                    val_exog = train_exog.iloc[val_idx]

                    fitted_model = SARIMAX(
                        endog=tr_endog,
                        exog=tr_exog,
                        order=(p, d, q),
                        seasonal_order=(P, D, Q, 12),
                        enforce_stationarity=True,
                        enforce_invertibility=True
                    ).fit(disp=False)

                    val_forecast = fitted_model.get_forecast(
                        steps=len(val_idx), exog=val_exog
                    )
                    errors.append(
                        root_mean_squared_error(val_endog, val_forecast.predicted_mean)
                    )
                return np.mean(errors)

            except Exception as e:
                return float('inf')

        sampler = optuna.samplers.TPESampler(seed=random_state)
        study = create_study(train_data, "sarimax", sampler)
        study.optimize(objective, n_trials=50)
        best_params = study.best_params

    # Train the best model
    best_model = SARIMAX(
        endog=train_data[target],
        exog=train_exog,
        order=(best_params["p"], best_params["d"], best_params["q"]),
        seasonal_order=(best_params["P"], best_params["D"], best_params["Q"], 12),
        enforce_stationarity=True,
        enforce_invertibility=True,
    )
    best_model_fitted = best_model.fit()

    # Forecasting
    forecast_periods = len(test_data["value"])
    forecast = best_model_fitted.get_forecast(steps=forecast_periods, exog=test_exog)
    test_data["Forecast"] = forecast.predicted_mean.values

    if eval:    
        # Metrics Calculation
        rmse_sarimax = root_mean_squared_error(test_data["value"], test_data["Forecast"])
        mape_sarimax = mean_absolute_percentage_error(test_data["value"], test_data["Forecast"])

        model_eval = ['SARIMAX', rmse_sarimax, mape_sarimax]
    else:
        model_eval = []

    # Exog is standardised, so raw rows are scaled before being forecast on
    def predict_exog(X):
        exog = pd.DataFrame(scaler.transform(X[features]), columns=features, index=X.index)
        return best_model_fitted.get_forecast(steps=len(X), exog=exog).predicted_mean.values

    return model_eval, test_data["Forecast"], best_params, Fitted(best_model_fitted, predict_exog)