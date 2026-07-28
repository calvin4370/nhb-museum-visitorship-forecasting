import numpy as np
import pandas as pd

import optuna
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error, root_mean_squared_error
from sklearn.model_selection import TimeSeriesSplit

def randomforest(train_data, test_data, eval, best_params=None):
    # Define features and target
    features = ["sin_month", "cos_month", "monthly_avg", "is_covid", "intl_arrivals"] + [
        f"lag_{i}" for i in range(1, 13)
    ]
    target = "value"

    # Set seed for random forest
    random_state = 42

    # If best_params is provided, use it
    # Else, perform hyperparameter optimization with Optuna
    if best_params is None:
        def objective(trial):
            params = {
                "n_estimators": trial.suggest_int("n_estimators", 100, 1000, step=100),
                "max_depth": trial.suggest_int("max_depth", 5, 30),
                "min_samples_split": trial.suggest_int("min_samples_split", 2, 20),
                "min_samples_leaf": trial.suggest_int("min_samples_leaf", 1, 10),
                "max_features": trial.suggest_categorical(
                    "max_features", ["sqrt", "log2", None]
                ),
                "bootstrap": trial.suggest_categorical("bootstrap", [True, False]),
            }

            model = RandomForestRegressor(**params, random_state=random_state)
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
        best_params = study.best_params

    # Train the best model
    best_model = RandomForestRegressor(**best_params, random_state=random_state)
    best_model.fit(train_data[features], train_data[target])

    # Forecasting
    forecast = best_model.predict(test_data[features])
    test_data["Forecast"] = forecast

    if eval:
        # Metrics Calculation
        rmse_rf = root_mean_squared_error(test_data["value"], test_data["Forecast"])
        mape_rf = mean_absolute_percentage_error(test_data["value"], test_data["Forecast"])

        model_eval = ['Random Forest Regressor', rmse_rf, mape_rf]
    else:
        model_eval = []

    return model_eval, forecast, best_params

