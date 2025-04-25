import pandas as pd
import numpy as np

import optuna
from statsmodels.tsa.statespace.sarimax import SARIMAX
from sklearn.metrics import mean_absolute_percentage_error, root_mean_squared_error

import warnings

warnings.filterwarnings('ignore')

def sarimax_model(train_data, test_data):
    # Set seed for random forest
    random_state = 42

    # Define features and target
    features = ["sin_month", "cos_month", "monthly_avg"] + [
        f"lag_{i}" for i in range(1, 13)
    ]
    target = "value"

    def objective(trial, data=train_data, val_size=10):
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
            fitted_model = model.fit()
            return fitted_model.aic

        except Exception as e:
            return float('inf')

    sampler = optuna.samplers.TPESampler(seed=random_state)
    study = optuna.create_study(direction="minimize", sampler=sampler)
    study.optimize(objective, n_trials=50)
    
    # Train the best model
    best_params = study.best_params
    best_model = SARIMAX(
        endog=train_data[target], 
        exog=train_data[features]
        )
    best_model_fitted = best_model.fit(**best_params)

    # Forecasting
    forecast_periods = len(test_data["value"])
    forecast = best_model_fitted.get_forecast(steps=forecast_periods, exog=test_data[features])
    test_data["Forecast"] = forecast.predicted_mean.values

    # Metrics Calculation
    rmse_sarimax = root_mean_squared_error(test_data["value"], test_data["Forecast"])
    mape_sarimax = mean_absolute_percentage_error(test_data["value"], test_data["Forecast"])

    model_eval= ['SARIMAX', rmse_sarimax, mape_sarimax]
    
    return model_eval, test_data["Forecast"]