import numpy as np
import pandas as pd

def data_prep():
    # Load and preprocess data
    df = pd.read_csv('./data/museum_ts.csv')
    df["timestamp"] = pd.to_datetime(df["Reporting Period"], format="%Y %b")
    df.rename(columns={"Value": "value"}, inplace=True)

    # Feature Engineering
    df["month"] = df["timestamp"].dt.month
    df["sin_month"] = np.sin(2 * np.pi * df["month"] / 12)
    df["cos_month"] = np.cos(2 * np.pi * df["month"] / 12)

    # Create lag features (1 to 12 months)
    for lag in range(1, 13):
        df[f"lag_{lag}"] = df["value"].shift(lag)

    #df["monthly_avg"] = df.groupby(df["month"])["value"].transform("mean")

    # Drop NaN rows created by lagging
    df.dropna(inplace=True)

    # Train-test split (80-20)
    split_point = int(len(df) * 0.8)
    train_data = df[:split_point]
    test_data = df[split_point:]

    # Monthly average calculated after train-test split to avoid data leakage
    train_data["monthly_avg"] = train_data.groupby(train_data["month"])["value"].transform("mean")
    test_data["monthly_avg"] = train_data.groupby(train_data["month"])["value"].transform("mean")

    return train_data, test_data, df
