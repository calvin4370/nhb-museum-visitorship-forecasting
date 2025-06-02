import pandas as pd
import numpy as np

import optuna
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_percentage_error, root_mean_squared_error

def hw(train_data, test_data, eval):
    # Prepare input data for Holt Winters
    train_X = train_data.set_index("timestamp")["value"]
    train_X = train_X.asfreq('MS')
    seasonal_periods = 12
    
    random_state = 42

    # Hyperparameter optimization with Optuna
    def objective(trial, data=train_X, seasonal_periods=12, val_size=10):
        # Define the hyperparameter search space
        params = {
            'smoothing_level': trial.suggest_float('smoothing_level', 0, 1),
            'smoothing_trend': trial.suggest_float('smoothing_trend', 0, 1),
            'smoothing_seasonal': trial.suggest_float('smoothing_seasonal', 0, 1)        
        }

        # Define the trend type
        trend = trial.suggest_categorical('trend', ['add','mul'])
        seasonal = trial.suggest_categorical('seasonal', ['add','mul'])

        # Split data into train and validation sets
        train_data = data[:-val_size]
        val_data = data[-val_size:]

        try:
            # Fit model
            model = ExponentialSmoothing(
                train_data,
                seasonal_periods = seasonal_periods,
                trend = trend,
                seasonal = seasonal
                )
            
            # Train model with suggested parameters
            fitted_model = model.fit(**params)
            
            #Generate forecast for validation set
            forecast = fitted_model.forecast(val_size)

            # Calculate error
            rmse = root_mean_squared_error(val_data, forecast)
            return rmse
        
        except Exception as e:
            return float('inf')

    sampler = optuna.samplers.TPESampler(seed=random_state)
    study = optuna.create_study(direction="minimize", sampler=sampler)
    study.optimize(objective, n_trials=50)

    # Train the best model
    best_params = study.best_params
    # Extract best trend and seasonal params from the best params as they are handled separately from smoothing parameters
    trend = best_params['trend']
    seasonal = best_params['seasonal']
    del best_params['trend']
    del best_params['seasonal']

    best_model = ExponentialSmoothing(
        train_X,
        seasonal_periods=seasonal_periods,
        trend=trend,
        seasonal=seasonal
    )
    best_model_fitted = best_model.fit(**best_params)

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
        
    return model_eval, forecast.values