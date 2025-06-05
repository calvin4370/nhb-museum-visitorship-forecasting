import numpy as np
import pandas as pd

import optuna
from sklearn.metrics import mean_absolute_percentage_error, root_mean_squared_error
from sklearn.model_selection import TimeSeriesSplit
from xgboost import XGBRegressor

def xgb(train_data, test_data, eval):
    # Define features and target
    features = ["sin_month", "cos_month", "monthly_avg", "is_covid"] + [
        f"lag_{i}" for i in range(1, 13)
    ]
    target = "value"
    
    # Set seed for random forest
    random_state = 42

    # Hyperparameter optimization with Optuna
    def objective(trial):
        params = {
            "n_estimators": trial.suggest_int("n_estimators", 100, 1000, step=100),
            "max_depth": trial.suggest_int("max_depth", 3, 10),
            "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3),
            "subsample": trial.suggest_float("subsample", 0.5, 1.0),
            "colsample_bytree": trial.suggest_float("colsample_bytree", 0.5, 1.0),
            "min_child_weight": trial.suggest_int("min_child_weight", 1, 10),
        }

        model = XGBRegressor(**params, random_state=random_state)
        tscv = TimeSeriesSplit(n_splits=3)
        errors = []

        for train_idx, val_idx in tscv.split(train_data):
            train_X = train_data.iloc[train_idx][features]
            train_y = train_data.iloc[train_idx][target]
            val_X = train_data.iloc[val_idx][features]
            val_y = train_data.iloc[val_idx][target]

            model.fit(train_X, train_y)
            predictions = model.predict(val_X)
            errors.append(root_mean_squared_error(val_y, predictions))

        return np.mean(errors)

    sampler = optuna.samplers.TPESampler(seed=random_state)
    study = optuna.create_study(direction="minimize", sampler=sampler)
    study.optimize(objective, n_trials=50)

    # Train the best model
    best_params = study.best_params
    best_model = XGBRegressor(**best_params, random_state=random_state)
    best_model.fit(train_data[features], train_data[target])

    # Forecasting
    forecast = best_model.predict(test_data[features])
    test_data["Forecast"] = forecast

    if eval:
        # Metrics Calculation
        rmse_xgb = root_mean_squared_error(test_data["value"], test_data["Forecast"])
        mape_xgb = mean_absolute_percentage_error(test_data["value"], test_data["Forecast"])
        
        model_eval = ['XGBoost', rmse_xgb, mape_xgb]
    else:
        model_eval = []
        
    return model_eval, forecast
