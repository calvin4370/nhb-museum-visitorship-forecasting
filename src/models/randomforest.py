import numpy as np
import pandas as pd

import optuna
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_percentage_error, root_mean_squared_error
from sklearn.model_selection import TimeSeriesSplit

from src.models.fitted import Fitted
from src.analysis.tuning import create_study
from src.features.transform import from_log, log_frame, smearing_factor
def randomforest(train_data, test_data, eval, features, best_params=None):
    # Target the caller's feature list predicts
    target = "value"

    # Set seed for random forest
    random_state = 42

    # Fitted in log space when enabled; both frames pass through unchanged if not
    train_log = log_frame(train_data, features)
    test_log = log_frame(test_data, features)

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
            tscv = TimeSeriesSplit(n_splits=3, test_size=12)
            errors = []

            for train_idx, val_idx in tscv.split(train_log):
                train_X = train_log.iloc[train_idx][features]
                train_y = train_log.iloc[train_idx][target]
                val_X = train_log.iloc[val_idx][features]

                model.fit(train_X, train_y)
                predictions = model.predict(val_X)

                # Scored in visitors, so best_value compares across branches
                errors.append(root_mean_squared_error(
                    train_data.iloc[val_idx][target], from_log(predictions)
                ))

            return np.mean(errors)


        sampler = optuna.samplers.TPESampler(seed=random_state)
        study = create_study(train_data, "rf", sampler)
        study.optimize(objective, n_trials=50)
        best_params = study.best_params

    # Train the best model
    best_model = RandomForestRegressor(**best_params, random_state=random_state)
    best_model.fit(train_log[features], train_log[target])

    # Duan's smearing correction, from this model's own training residuals
    smearing = smearing_factor(train_log[target], best_model.predict(train_log[features]))

    # Forecasting, inverted back to visitors before anything downstream sees it
    forecast = from_log(best_model.predict(test_log[features]), smearing)
    test_data["Forecast"] = forecast

    if eval:
        # Metrics Calculation
        rmse_rf = root_mean_squared_error(test_data["value"], test_data["Forecast"])
        mape_rf = mean_absolute_percentage_error(test_data["value"], test_data["Forecast"])

        model_eval = ['Random Forest Regressor', rmse_rf, mape_rf]
    else:
        model_eval = []

    # permutation_importance passes raw rows, so the callable makes the round trip
    def predict_raw(X):
        return from_log(best_model.predict(log_frame(X, features)[features]), smearing)

    return model_eval, forecast, best_params, Fitted(best_model, predict_raw)

