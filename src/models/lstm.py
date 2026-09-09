import os

import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error

from src.models.fitted import Fitted
from src.features.transform import from_log, to_log, smearing_factor, value_scaled

# Suppress TensorFlow logging before importing it. 
# Set back to normal after import to only skip the 2 initialisation messages
_stderr_fd = os.dup(2)
os.dup2(os.open(os.devnull, os.O_WRONLY), 2)
import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM, Dense
os.dup2(_stderr_fd, 2)


def lstm(data, eval, h, feature_cols):
    # Fitted in log space when enabled. 'value' and monthly_avg are on the
    # target's scale, so they move with it; the flags and calendar terms do not
    logged = data.copy()
    for column in ["value", *value_scaled(feature_cols)]:
        if column in logged.columns:
            logged[column] = to_log(logged[column])

    features = logged[feature_cols].values          # (N, n_features)
    target = logged['value'].values.reshape(-1, 1)  # (N, 1)

    # Set seed for reproducibility
    random_state = 42
    tf.random.set_seed(random_state)
    tf.config.experimental.enable_op_determinism()

    # Determine the train/test boundary first so the scalers can be fit on the
    # training slice only. Fitting on the full series would leak the test (and,
    # in predict mode, the synthetic future) min/max into normalization.
    time_steps = 12
    if eval:
        train_size = int(len(features) * 0.8)
    else:
        train_size = len(features) - h

    # Normalize features and target 
    # Fit scalers on train data ONLY
    feature_scaler = MinMaxScaler(feature_range=(0, 1))
    features_scaled = feature_scaler.fit(features[:train_size]).transform(features)
    target_scaler = MinMaxScaler(feature_range=(0, 1))
    target_scaled = target_scaler.fit(target[:train_size]).transform(target)
    n_features = features_scaled.shape[1]

    # Define a function to create sequences for LSTM: a window of `time_steps`
    # feature rows (X) predicting the next target row (y).
    def create_sequences(X_data, y_data, time_steps):
        X, y = [], []
        for i in range(len(X_data) - time_steps):
            X.append(X_data[i:i + time_steps])
            y.append(y_data[i + time_steps])
        return np.array(X), np.array(y)

    # Create train-test split (80-20), ensuring no missing rows.
    # Include the last `time_steps` rows of training in test
    X_train_raw = features_scaled[:train_size]
    y_train_raw = target_scaled[:train_size]
    X_test_raw = features_scaled[train_size - time_steps:]
    y_test_raw = target_scaled[train_size - time_steps:]

    # Create sequences
    X_train, y_train = create_sequences(X_train_raw, y_train_raw, time_steps)
    X_test, y_test = create_sequences(X_test_raw, y_test_raw, time_steps)

    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(time_steps, n_features)),
        LSTM(50, return_sequences=False),
        Dense(25),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mean_squared_error')

    # Train the model
    model.fit(X_train, y_train, batch_size=1, epochs=50, verbose=0)

    # Predict values
    test_predict = model.predict(X_test)

    # Undo the MinMax scaling, then the log transform, so predictions are visitors.
    # Smearing comes from the model's own in-sample residuals, both in log space
    train_fit = target_scaler.inverse_transform(model.predict(X_train, verbose=0))
    smearing = smearing_factor(
        target_scaler.inverse_transform(y_train).ravel(), train_fit.ravel()
    )
    test_predict = from_log(target_scaler.inverse_transform(test_predict), smearing)

    if eval:
        # Actuals go back to visitors too, so the metrics below are unchanged
        y_test_inv = from_log(target_scaler.inverse_transform(y_test))

        # Compute RMSE and MAPE
        rmse_lstm = np.sqrt(mean_squared_error(y_test_inv, test_predict))
        mape_lstm = mean_absolute_percentage_error(y_test_inv, test_predict)

        model_eval = ['LSTM', rmse_lstm, mape_lstm]
    else:
        model_eval = []

    return model_eval, test_predict, Fitted(model)
