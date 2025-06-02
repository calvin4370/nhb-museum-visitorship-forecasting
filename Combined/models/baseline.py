import pandas as pd
import numpy as np

from sklearn.metrics import mean_absolute_percentage_error, root_mean_squared_error

def baseline(train_data, test_data, eval):
    # Baseline model is defined as the monthly average of museum visitorship over past 3 years (i.e., 36 months)
    baseline_horizon = 36
    baseline_train_data = train_data[-baseline_horizon:]
    baseline_train_data["baseline_avg"] = baseline_train_data.groupby(baseline_train_data["month"])["value"].transform("mean")
    baseline_avg = baseline_train_data[["month", "baseline_avg"]].drop_duplicates()
    test_data = pd.merge(test_data, baseline_avg, on="month", how="left")

    forecast = test_data["baseline_avg"]

    if eval:
        # Metrics Calculation
        rmse_baseline = root_mean_squared_error(test_data["value"], test_data["baseline_avg"])
        mape_baseline = mean_absolute_percentage_error(test_data["value"], test_data["baseline_avg"])

        model_eval = ["Baseline Monthly Mean", rmse_baseline, mape_baseline]

    else:
        model_eval = []

    return model_eval, forecast