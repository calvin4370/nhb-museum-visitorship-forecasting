
import pandas as pd
import numpy as np

import optuna
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import TimeSeriesSplit

from src.models.fitted import Fitted
from src.analysis.tuning import create_study
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_percentage_error, root_mean_squared_error


def support_vec(train_data, test_data, eval, features, best_params=None):
    # Set seed for reproducibility
    random_state = 42

    # Target the caller's feature list predicts
    target = "value"

    # SVR requires features to be scaled
    scaler = StandardScaler()
    X_train_scaled = pd.DataFrame(scaler.fit_transform(train_data[features]), columns=train_data[features].columns, index=train_data[features].index)
    X_test_scaled = scaler.transform(test_data[features])
    y_train = train_data[target]

    # Kept because train_data below is replaced by a features-only frame, which
    # no longer carries the museum column the study name is built from
    museum_frame = train_data

    # New train dataset containing scaled features
    train_data = pd.concat([X_train_scaled, y_train], axis=1)

    # If best_params is provided, use it
    # Else, perform hyperparameter optimization with Optuna
    if best_params is None:
        def objective(trial, data=train_data):
            # Define hyperparameter search space
            kernel = trial.suggest_categorical('kernel', ['linear', 'rbf', 'poly'])
            C = trial.suggest_loguniform('C', 1e-3, 1e3)
            epsilon = trial.suggest_loguniform('epsilon', 1e-3, 1)

            # Additional parameters based on kernel
            if kernel == 'poly':
                degree = trial.suggest_int('degree', 2, 5)
            if kernel in ['rbf', 'poly']:
                gamma = trial.suggest_loguniform('gamma', 1e-3, 1)

            # Create SVR model with trial parameters
            if kernel == 'linear':
                model = SVR(kernel=kernel, C=C, epsilon=epsilon)
            elif kernel == 'poly':
                model = SVR(kernel=kernel, C=C, epsilon=epsilon, degree=degree, gamma=gamma)
            else:
                model = SVR(kernel=kernel, C=C, epsilon=epsilon, gamma=gamma)

            # Rolling-origin folds, each validating a full 12-month season
            tscv = TimeSeriesSplit(n_splits=3, test_size=12)
            errors = []

            try:
                for train_idx, val_idx in tscv.split(data):
                    tr, val = data.iloc[train_idx], data.iloc[val_idx]
                    model.fit(tr[features], tr[target])
                    errors.append(
                        root_mean_squared_error(val[target], model.predict(val[features]))
                    )
                return np.mean(errors)

            except Exception as e:
                return float('inf')

        sampler = optuna.samplers.TPESampler(seed=random_state)
        study = create_study(museum_frame, "svr", sampler)
        study.optimize(objective, n_trials=50)
        best_params = study.best_params

    # Train the best model
    best_model = SVR(**best_params)
    best_model.fit(X_train_scaled, y_train)

    # Forecasting
    forecast = best_model.predict(X_test_scaled)
    test_data["Forecast"] = forecast

    # Metrics Calculation
    if eval:
        rmse_svr = root_mean_squared_error(test_data["value"], test_data["Forecast"])
        mape_svr = mean_absolute_percentage_error(test_data["value"], test_data["Forecast"])

        model_eval = ['Support Vector Regression', rmse_svr, mape_svr]
    else:
        model_eval = []

    # SVR was fitted on scaled inputs, so raw rows go through the same scaler
    fitted = Fitted(best_model, lambda X: best_model.predict(scaler.transform(X)))
    return model_eval, forecast, best_params, fitted
