import numpy as np
import pandas as pd

def sin_cos_month(df):
    # Feature Engineering
    df["month"] = df["timestamp"].dt.month
    df["sin_month"] = np.sin(2 * np.pi * df["month"] / 12)
    df["cos_month"] = np.cos(2 * np.pi * df["month"] / 12)
    return df

def is_covid(df):
    # Create COVID indicator, COVID impact captured between Apr 2020 to Feb 2023
    covid_start = pd.Timestamp('2020-04-01')
    covid_end = pd.Timestamp('2023-02-13')
    df["is_covid"] = ((df["timestamp"]>=covid_start) & (df["timestamp"]<=covid_end)).astype(int)    
    return df

def data_prep(split_ind, h):
    # Load and preprocess data
    df = pd.read_csv('./data/museum_ts.csv')
    df["timestamp"] = pd.to_datetime(df["Reporting Period"], format="%Y %b")
    df.rename(columns={"Value": "value"}, inplace=True)

    # Feature Engineering
    df = sin_cos_month(df)

    # Create lag features (1 to 12 months)
    for lag in range(1, 13):
        df[f"lag_{lag}"] = df["value"].shift(lag)

    # Drop NaN rows created by lagging
    df.dropna(inplace=True)

    # Create COVID indicator
    df = is_covid(df)

    #Train-test split for model evaluation
    if split_ind:
        # Train-test split (80-20)
        split_point = int(len(df) * 0.8)
        train_data = df[:split_point]
        test_data = df[split_point:]

    #No train-test split for actual model prediction
    else:
        #train_data is all available data points
        train_data = df
        
        #test_data is 24 months ahead
        last_date = df["timestamp"].max()

        forecast_horizon = pd.date_range(
            start = last_date + pd.DateOffset(months=1),
            periods = h,
            freq='MS'
        )

        test_data = pd.DataFrame({
            "timestamp": forecast_horizon,
            "value": np.nan
        })
        test_data["Data Series"] = df["Data Series"].iloc[-1]
        test_data = sin_cos_month(test_data)
        test_data = is_covid(test_data)
        
        new_df = df.tail(12)
        new_df = pd.concat([new_df,test_data], axis=0, join="outer")

        # Create lag features (1 to 12 months), for missing lag features it is imputed by monthly average
        for lag in range(1, 13):
            test_data[f"lag_{lag}"] = new_df["value"].shift(lag)

    # Monthly average calculated after train-test split to avoid data leakage
    train_data["monthly_avg"] = train_data.groupby(train_data["month"])["value"].transform("mean")
    monthly_avg = train_data[["month", "monthly_avg"]].drop_duplicates()
    test_data = pd.merge(test_data, monthly_avg, on="month", how="left")

    if split_ind==False:
        # Impute missing lag features with monthly averages
        test_data["value"] = test_data["monthly_avg"]

        for lag in range(1, 13):
            test_data[f"lag_imp_{lag}"] = test_data["value"].shift(lag)
            test_data[f"lag_{lag}"] = test_data[f"lag_{lag}"].fillna(0) + test_data[f"lag_imp_{lag}"].fillna(0)

        for lag in range(1, 13):
            test_data.drop(f"lag_imp_{lag}", axis=1, inplace=True)

        df = pd.concat([df,test_data], axis=0, join="outer")

    return train_data, test_data, df
