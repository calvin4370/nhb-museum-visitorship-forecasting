import numpy as np
import pandas as pd

from src.feature_engineering.data_prep import data_prep
from src.data.singstat_api import singstat_api
from src.visualisation.timeplot import timeplot, forecast_table

from src.models.randomforest import randomforest
from src.models.xgboost_model import xgb
from src.models.lstm import lstm
from src.models.timegpt import timegpt
from src.models.holtwinters import hw
from src.models.sarimax import sarimax_model
from src.models.baseline import baseline
from src.models.svr import support_vec

# Set institution param
#museum = "Asian Civilisations Museum"
#museum = "National Museum Of Singapore"
museum = "Peranakan Museum"
#museum = "Indian Heritage Centre"


# Set eval indicator (True = Run model evaluation; False = Run model prediction)
eval = False
if eval:
    split_ind = True
else:
    split_ind = False

# Set prediction/forecast periods ahead, default 2 years (i.e., 24 months)
h = 24

# 2 api calls made: museum visitorship and international arrivals
visitors = singstat_api("M891071", 2013, "Jan", 2025, "Mar")
arrivals = singstat_api("M550001", 2013, "Jan", 2025, "Mar")

# Filter specific museum visitorship data
# output both data series (museum time series and STB international arrival time series)
museum_ts = visitors.loc[visitors.loc[:,"Data Series"]==f"{museum}",:]
museum_ts.to_csv("./data/museum_ts.csv", index=False)
arrivals.to_csv("./data/intl_arrivals.csv", index=False)

# Data preparation to prepare train and test data
train_data, test_data, full_data = data_prep(split_ind=split_ind, h=h)

def main(train_data, test_data, full_data):
    # Create list to store model evaluation results
    model_eval = []

    model_eval_rf, rf_forecast = randomforest(train_data, test_data, eval)
    model_eval.append(model_eval_rf)
    timeplot("rf", train_data, test_data, rf_forecast, eval)
    
    model_eval_xgb, xgb_forecast = xgb(train_data, test_data, eval)
    model_eval.append(model_eval_xgb)
    timeplot("xgb", train_data, test_data, xgb_forecast, eval)

    model_eval_lstm, lstm_forecast = lstm(full_data, eval, h)
    model_eval.append(model_eval_lstm)
    timeplot("lstm", train_data, test_data, lstm_forecast, eval)

    model_eval_timegpt, timegpt_forecast = timegpt(train_data, test_data, eval)
    model_eval.append(model_eval_timegpt)
    timeplot("timegpt", train_data, test_data, timegpt_forecast, eval)

    model_eval_hw, hw_forecast = hw(train_data, test_data, eval)
    model_eval.append(model_eval_hw)
    timeplot("hw", train_data, test_data, hw_forecast, eval)

    model_eval_sarimax, sarimax_forecast = sarimax_model(train_data, test_data, eval)
    model_eval.append(model_eval_sarimax)
    timeplot("sarimax", train_data, test_data, sarimax_forecast, eval)

    model_eval_baseline, baseline_forecast = baseline(train_data, test_data, eval)
    model_eval.append(model_eval_baseline)
    timeplot("baseline", train_data, test_data, baseline_forecast, eval)

    model_eval_svr, svr_forecast = support_vec(train_data, test_data, eval)
    model_eval.append(model_eval_svr)
    timeplot("svr", train_data, test_data, svr_forecast, eval)

    if eval:
        model_eval_df = pd.DataFrame(model_eval, columns=['Model', 'RMSE', 'MAPE'])

        # Formatting metrics
        model_eval_df_formatted = model_eval_df.copy()
        model_eval_df_formatted['RMSE'] = model_eval_df_formatted['RMSE'].apply(lambda x: f'{x:.2f}')
        model_eval_df_formatted['MAPE'] = model_eval_df_formatted['MAPE'].apply(lambda x: f'{x:.2%}')

        model_eval_df_formatted.to_csv("./model_eval.csv", index=False)

    else:
        # Output forecast figures
        rf_forecast = forecast_table("rf", rf_forecast)
        xgb_forecast = forecast_table("xgb", xgb_forecast)
        lstm_forecast = forecast_table("lstm", lstm_forecast)
        timegpt_forecast = forecast_table("timegpt", timegpt_forecast)
        hw_forecast = forecast_table("hw", hw_forecast)
        sarimax_forecast = forecast_table("sarimax", sarimax_forecast.values)
        baseline_forecast = forecast_table("baseline", baseline_forecast.values)
        svr_forecast = forecast_table ("svr", svr_forecast)

        forecast_overall = pd.concat(
            [rf_forecast, 
            xgb_forecast, 
            lstm_forecast,
            timegpt_forecast,
            hw_forecast, 
            sarimax_forecast, 
            baseline_forecast,
            svr_forecast], axis=0)
        forecast_overall["Institution"] = museum
        forecast_overall["Month"] = test_data["timestamp"].dt.month
        forecast_overall["Year"] = test_data["timestamp"].dt.year
        forecast_overall = forecast_overall[["Institution", "Model", "Year", "Month", "Prediction"]]
        forecast_overall.to_csv("./predictions.csv", index=False)


main(train_data, test_data, full_data)
