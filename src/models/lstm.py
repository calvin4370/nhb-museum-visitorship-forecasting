import numpy as np
import pandas as pd

from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error

import tensorflow as tf
from keras.models import Sequential
from keras.layers import LSTM, Dense

def lstm(data, eval, h):
    # Use only the 'Value' column for LSTM forecasting
    values = data['value'].values.reshape(-1, 1)
    
    # Set seed, try to control randomness
    random_state = 42
    tf.random.set_seed(random_state)
    tf.config.experimental.enable_op_determinism()

    # Normalize the values
    scaler = MinMaxScaler(feature_range=(0, 1))
    values_scaled = scaler.fit_transform(values)

    # Define a function to create sequences for LSTM
    def create_sequences(data, time_steps):
        X, y = [], []
        for i in range(len(data) - time_steps):
            X.append(data[i:i + time_steps])
            y.append(data[i + time_steps])
        return np.array(X), np.array(y)
    
    # Create train-test split (80-20), ensuring no missing rows
    time_steps = 12
    if eval:
        train_size = int(len(values_scaled) * 0.8)

        # Include the last `time_steps` rows of training in test
        train = values_scaled[:train_size]
        test = values_scaled[train_size - time_steps:]

        # Create sequences
        X_train, y_train = create_sequences(train, time_steps)
        X_test, y_test = create_sequences(test, time_steps)
    
    else:
        train_size = int(len(values_scaled)) - h
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
