import pandas as pd
import numpy as np

import optuna
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_percentage_error, root_mean_squared_error

import warnings

warnings.filterwarnings('ignore')

def sarimax_model(train_data, test_data, eval, best_params=None):
    # Define features and target
    features = ["sin_month", "cos_month", "monthly_avg", "is_covid", "intl_arrivals"] + [
        f"lag_{i}" for i in range(1, 13)
    ]
    target = "value"

    # Set seed for reproducibility
    random_state = 42

    # Standardise exogenous features
    exog_scaler = StandardScaler()
    train_scaled = train_data.copy()
    train_scaled[features] = exog_scaler.fit_transform(train_data[features])
    test_scaled = test_data.copy()
    test_scaled[features] = exog_scaler.transform(test_data[features])

    # If best_params is provided, use it
    # Else, perform hyperparameter optimization with Optuna
    if best_params is None:
        def objective(trial, data=train_scaled, val_size=10):
            # Define the search space
            # Non-seasonal params
            p = trial.suggest_int('p', 0, 5)
            d = trial.suggest_int('d', 0, 2)
            q = trial.suggest_int('q', 0, 5)
            # Seasonal params
            P = trial.suggest_int('P', 0, 2)
            D = trial.suggest_int('D', 0, 1)
            Q = trial.suggest_int('Q', 0, 2)

            # Split data into train and validation sets
            train_data = data[:-val_size]
            val_data = data[-val_size:]

            # Try fitting the model with suggested params
            try:
                model = SARIMAX(
                    endog=train_data[target],
                    exog=train_data[features],
                    order=(p, d, q),
                    seasonal_order=(P, D, Q, 12),
                    enforce_stationarity=False,
                    enforce_invertibility=False
                )

                # Train model with suggested parameters
                fitted_model = model.fit(disp=False)

                # Score on held-out val_data
                val_forecast = fitted_model.get_forecast(steps=val_size, exog=val_data[features])
                return root_mean_squared_error(val_data[target], val_forecast.predicted_mean)

            except Exception as e:
                return float('inf')

        sampler = optuna.samplers.TPESampler(seed=random_state)
        study = optuna.create_study(direction="minimize", sampler=sampler)
        study.optimize(objective, n_trials=50)
        best_params = study.best_params

    # Train the best model
    best_model = SARIMAX(
        endog=train_scaled[target],
        exog=train_scaled[features],
        order=(best_params["p"], best_params["d"], best_params["q"]),
        seasonal_order=(best_params["P"], best_params["D"], best_params["Q"], 12),
        enforce_stationarity=False,
        enforce_invertibility=False,
    )
    best_model_fitted = best_model.fit()

    # Forecasting
    forecast_periods = len(test_data["value"])
    forecast = best_model_fitted.get_forecast(steps=forecast_periods, exog=test_scaled[features])
    test_data["Forecast"] = forecast.predicted_mean.values

    if eval:    
        # Metrics Calculation
        rmse_sarimax = root_mean_squared_error(test_data["value"], test_data["Forecast"])
        mape_sarimax = mean_absolute_percentage_error(test_data["value"], test_data["Forecast"])

        model_eval = ['SARIMAX', rmse_sarimax, mape_sarimax]
    else:
        model_eval = []

    return model_eval, test_data["Forecast"], best_params