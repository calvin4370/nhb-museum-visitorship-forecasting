import pandas as pd
import numpy as np
import os

from nixtla import NixtlaClient

from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error

from utilsforecast.losses import mae, mse, rmse, mape, smape

def timegpt(train_data, test_data):
    # Initialize NixtlaClient
    nixtla_api_key = os.getenv('nixtla_api_key')
    nixtla_client = NixtlaClient(api_key=f"{nixtla_api_key}")

    # Prepare Exogenous DataFrame for Future Predictions
    future_dates = test_data[['timestamp']].copy()
    future_dates['sin_month'] = np.sin(2 * np.pi * future_dates['timestamp'].dt.month / 12)
    future_dates['cos_month'] = np.cos(2 * np.pi * future_dates['timestamp'].dt.month / 12)
    future_dates['monthly_avg'] = test_data['monthly_avg'].values
    future_dates['lag_1'] = train_data['value'].iloc[-1]  # Last value from train as lag_1
    future_dates['lag_12'] = train_data['value'].iloc[-12]  # Value 12 months back as lag_12

    # Forecast using Nixtla
    forecast_horizon = len(test_data)
    finetune_steps = 10  # Number of fine-tuning steps
    finetune_loss = 'mae'  # Mean Absolute Error as the loss function for fine-tuning
    #finetune_loss = 'rmse'  # tried tuning for rmse but got both worse results fr rmse and mape

    forecast_df = nixtla_client.forecast(
        df=train_data[['timestamp', 'value', 'sin_month', 'cos_month', 'monthly_avg', 'lag_1', 'lag_12']],
        h=forecast_horizon,
        time_col="timestamp",
        target_col="value",
        X_df=future_dates,  # Future exogenous variables for predictions
        date_features=True,  # Automatically adds date-related features
        model='timegpt-1',  # Suitable for longer-term forecasts
        finetune_steps=finetune_steps,  # Fine-tuning steps
        finetune_loss=finetune_loss  # Fine-tuning loss function
    )

    # Parse forecast results
    forecast_df['timestamp'] = pd.to_datetime(forecast_df['timestamp'])
    forecast_df.set_index('timestamp', inplace=True)
    forecast = forecast_df['TimeGPT'].values

    # Metrics Calculation
    rmse_timegpt = np.sqrt(mean_squared_error(test_data['value'], forecast_df['TimeGPT']))
    mape_timegpt = mean_absolute_percentage_error(test_data['value'], forecast_df['TimeGPT'])

    model_eval= ['TimeGPT', rmse_timegpt, mape_timegpt]

    return model_eval, forecast