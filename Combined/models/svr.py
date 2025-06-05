
import pandas as pd
import numpy as np

import optuna
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
from sklearn.metrics import mean_absolute_percentage_error, root_mean_squared_error


def support_vec(train_data, test_data, eval):
    # Set seed for random forest
    random_state = 42

    # Define features and target
    features = ["sin_month", "cos_month", "monthly_avg", "is_covid"] + [
        f"lag_{i}" for i in range(1, 13)
    ]
    target = "value"

    # SVR requires features to be scaled
    scaler = StandardScaler()
    X_train_scaled =pd.DataFrame(scaler.fit_transform(train_data[features]), columns=train_data[features].columns, index=train_data[features].index)
    X_test_scaled = scaler.transform(test_data[features])
    y_train = train_data[target]

    # New train dataset containing scaled features
    train_data = pd.concat([X_train_scaled, y_train], axis=1)


    def objective(trial, data=train_data, val_size=10):
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

        # Split data into train and validation sets
        train_data = data[:-val_size]
        val_data = data[-val_size:]

        # Try fitting the model with suggested params
        try:    
            model.fit(train_data[features], train_data[target])
            y_pred = model.predict(val_data[features])
            rmse = root_mean_squared_error(val_data[target], y_pred)
            return rmse

        except Exception as e:
            return float('inf')
        
    sampler = optuna.samplers.TPESampler(seed=random_state)
    study = optuna.create_study(direction="minimize", sampler=sampler)
    study.optimize(objective, n_trials=50)

    # Train the best model
    best_params = study.best_params
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

    return model_eval, forecast
