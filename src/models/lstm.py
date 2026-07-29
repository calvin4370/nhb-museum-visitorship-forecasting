import os

import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error

# Suppress TensorFlow logging before importing it. 
# Set back to normal after import to only skip the 2 initialisation messages
_stderr_fd = os.dup(2)
os.dup2(os.open(os.devnull, os.O_WRONLY), 2)
import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM, Dense
os.dup2(_stderr_fd, 2)


def lstm(data, eval, h):
    # Use only the 'Value' column for LSTM forecasting
    values = data['value'].values.reshape(-1, 1)

    # Set seed, try to control randomness
    random_state = 42
    tf.random.set_seed(random_state)
    tf.config.experimental.enable_op_determinism()

    # Determine the train/test boundary first so the scaler can be fit on the
    # training slice only. Fitting on the full series would leak the test (and,
    # in predict mode, the synthetic future) min/max into normalization.
    time_steps = 12
    if eval:
        train_size = int(len(values) * 0.8)
    else:
        train_size = len(values) - h

    # Normalize the values -- fit scaler on train data ONLY
    scaler = MinMaxScaler(feature_range=(0, 1))
    values_scaled = scaler.fit(values[:train_size]).transform(values)

    # Define a function to create sequences for LSTM
    def create_sequences(data, time_steps):
        X, y = [], []
        for i in range(len(data) - time_steps):
            X.append(data[i:i + time_steps])
            y.append(data[i + time_steps])
        return np.array(X), np.array(y)

    # Create train-test split (80-20), ensuring no missing rows.
    # Include the last `time_steps` rows of training in test
    train = values_scaled[:train_size]
    test = values_scaled[train_size - time_steps:]

    # Create sequences
    X_train, y_train = create_sequences(train, time_steps)
    X_test, y_test = create_sequences(test, time_steps)

    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=(time_steps, 1)),# need to change the number if add more exo variables
        LSTM(50, return_sequences=False),
        Dense(25),
        Dense(1)
    ])

    model.compile(optimizer='adam', loss='mean_squared_error')

    # Train the model
    model.fit(X_train, y_train, batch_size=1, epochs=50, verbose=0)

    # Predict values
    test_predict = model.predict(X_test)

    # Inverse scale the predictions and actual values
    test_predict = scaler.inverse_transform(test_predict)

    if eval:
        # Inverse scale the predictions and actual values
        y_test_inv = scaler.inverse_transform(y_test)

        # Compute RMSE and MAPE
        rmse_lstm = np.sqrt(mean_squared_error(y_test_inv, test_predict))
        mape_lstm = mean_absolute_percentage_error(y_test_inv, test_predict)

        model_eval = ['LSTM', rmse_lstm, mape_lstm]
    else:
        model_eval = []

    return model_eval, test_predict
