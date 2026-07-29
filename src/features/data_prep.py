import numpy as np
import pandas as pd


def sin_cos_month(df):
    # Cyclical encoding of month
    df["month"] = df["timestamp"].dt.month
    df["sin_month"] = np.sin(2 * np.pi * df["month"] / 12)
    df["cos_month"] = np.cos(2 * np.pi * df["month"] / 12)
    return df


def is_covid(df):
    # Create COVID indicator, COVID impact captured between Apr 2020 to Feb 2023
    covid_start = pd.Timestamp("2020-04-01")
    covid_end = pd.Timestamp("2023-02-13")
    df["is_covid"] = (
        (df["timestamp"] >= covid_start) & (df["timestamp"] <= covid_end)
    ).astype(int)
    return df


def engineer_features(museum_ts):
    df = museum_ts.copy()
    df["timestamp"] = pd.to_datetime(df["Reporting Period"], format="%Y %b")
    df.rename(columns={"Value": "value"}, inplace=True)

    # Cast visitorship to numeric, coercing any non-numeric values (e.g., "-") to NaN. These will be dropped later.
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    # Cyclocal encoding of month
    df = sin_cos_month(df)

    # Create lag features (1 to 12 months)
    for lag in range(1, 13):
        df[f"lag_{lag}"] = df["value"].shift(lag)
    df.dropna(inplace=True) # Drop NaN rows created by lagging or coerced "-" values

    # Create COVID indicator
    df = is_covid(df)

    return df


def add_monthly_avg(train_data, test_data):
    """
    Monthly average computed on train only (avoid leakage), merged into test.
    """
    train_data = train_data.copy()
    train_data["monthly_avg"] = train_data.groupby(train_data["month"])[
        "value"
    ].transform("mean")

    # Get a df of unique month -> monthly_avg pairs from train data only
    monthly_avg = train_data[["month", "monthly_avg"]].drop_duplicates()

    # Merge monthly_avg into test_data on month, left join to keep all test rows
    test_data = pd.merge(test_data, monthly_avg, on="month", how="left")

    return train_data, test_data


def prepare_eval_data(museum_ts):
    """
    Build an 80/20 chronological train/test split
    """
    df = engineer_features(museum_ts)

    split_point = int(len(df) * 0.8)
    train_data = df[:split_point]
    test_data = df[split_point:]

    # Create monthly average feature for train and test using only train data to avoid leakage
    train_data, test_data = add_monthly_avg(train_data, test_data)

    return train_data, test_data, df


def prepare_predict_data(museum_ts, h):
    """
    Build a full-history train set plus a synthetic h-month-ahead future
    frame to for model to forecast.
    """
    df = engineer_features(museum_ts)
    train_data = df

    # Create a synthetic future frame for h months ahead
    last_date = df["timestamp"].max()
    forecast_horizon = pd.date_range(
        start=last_date + pd.DateOffset(months=1), periods=h, freq="MS"
    )
    test_data = pd.DataFrame({"timestamp": forecast_horizon, "value": np.nan})
    test_data["Data Series"] = df["Data Series"].iloc[-1]
    test_data = sin_cos_month(test_data)
    test_data = is_covid(test_data)

    # Concatenate the last 12 months of actual data with the synthetic future frame
    new_df = df.tail(12)
    new_df = pd.concat([new_df, test_data], axis=0, join="outer")

    # Create lag features (1 to 12 months); missing ones imputed by monthly average
    for lag in range(1, 13):
        test_data[f"lag_{lag}"] = new_df["value"].shift(lag)

    train_data, test_data = add_monthly_avg(train_data, test_data)

    # Impute missing lag features with monthly averages
    # Note: Decision made to impute missing lag features with monthly averages 
    # instead recursive forecasting to avoid error propagation
    test_data["value"] = test_data["monthly_avg"]
    for lag in range(1, 13):
        test_data[f"lag_imp_{lag}"] = test_data["value"].shift(lag)
        test_data[f"lag_{lag}"] = test_data[f"lag_{lag}"].fillna(0) + test_data[
            f"lag_imp_{lag}"
        ].fillna(0)
    for lag in range(1, 13):
        test_data.drop(f"lag_imp_{lag}", axis=1, inplace=True)

    full_data = pd.concat([df, test_data], axis=0, join="outer")
    return train_data, test_data, full_data
