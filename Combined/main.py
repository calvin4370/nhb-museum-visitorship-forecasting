import numpy as np
import pandas as pd

from utils.data_prep import data_prep
from utils.singstat_api import singstat_api
from utils.timeplot import timeplot

from models.randomforest import randomforest
from models.xgboost import xgb
from models.lstm import lstm
from models.timegpt import timegpt
from models.holtwinters import hw
from models.sarimax import sarimax_model
from models.baseline import baseline
from models.svr import support_vec

# Set institution param
museum = "Asian Civilisations Museum"

# 2 api calls made: museum visitorship and international arrivals
visitors = singstat_api("M891071", 2013, "Jan", 2024, "Dec")
arrivals = singstat_api("M550001", 2013, "Jan", 2024, "Dec")

# Filter specific museum visitorship data
# output both data series (museum time series and STB international arrival time series)
museum_ts = visitors.loc[visitors.loc[:,"Data Series"]==f"{museum}",:]
museum_ts.to_csv("./data/museum_ts.csv", index=False)
arrivals.to_csv("./data/intl_arrivals.csv", index=False)

# Data preparation to prepare train and test data
train_data, test_data, full_data = data_prep()

def main(train_data, test_data, full_data):
    # Create list to store model evaluation results
    model_eval = []

    model_eval_rf, rf_forecast = randomforest(train_data, test_data)
    model_eval.append(model_eval_rf)
    timeplot("rf", train_data, test_data, rf_forecast)
    
    model_eval_xgb, xgb_forecast = xgb(train_data, test_data)
    model_eval.append(model_eval_xgb)
    timeplot("xgb", train_data, test_data, xgb_forecast)

    model_eval_lstm, lstm_forecast = lstm(full_data)
    model_eval.append(model_eval_lstm)
    timeplot("lstm", train_data, test_data, lstm_forecast)

    #model_eval_timegpt, timegpt_forecast = timegpt(train_data, test_data)
    #model_eval.append(model_eval_timegpt)
    #timeplot("timegpt", train_data, test_data, timegpt_forecast)

    model_eval_hw, hw_forecast = hw(train_data, test_data)
    model_eval.append(model_eval_hw)
    timeplot("hw", train_data, test_data, hw_forecast)

    model_eval_sarimax, sarimax_forecast = sarimax_model(train_data, test_data)
    model_eval.append(model_eval_sarimax)
    timeplot("sarimax", train_data, test_data, sarimax_forecast)

    model_eval_baseline, baseline_forecast = baseline(train_data, test_data)
    model_eval.append(model_eval_baseline)
    timeplot("baseline", train_data, test_data, baseline_forecast)

    model_eval_svr, svr_forecast = support_vec(train_data, test_data)
    model_eval.append(model_eval_svr)
    timeplot("svr", train_data, test_data, svr_forecast)

    model_eval_df = pd.DataFrame(model_eval, columns=['Model', 'RMSE', 'MAPE'])

    # Formatting metrics
    model_eval_df_formatted = model_eval_df.copy()
    model_eval_df_formatted['RMSE'] = model_eval_df_formatted['RMSE'].apply(lambda x: f'{x:.2f}')
    model_eval_df_formatted['MAPE'] = model_eval_df_formatted['MAPE'].apply(lambda x: f'{x:.2%}')

    model_eval_df_formatted.to_csv("./model_eval.csv", index=False)

main(train_data, test_data, full_data)