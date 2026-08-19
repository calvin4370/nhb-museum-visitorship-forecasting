import numpy as np
import pandas as pd

from config import COVID_START, COVID_END, END_YEAR, END_MONTH
from src.events.event_range import EventRange

# SingStat Table Series name
INTL_ARRIVALS_SERIES = "Total International Visitor Arrivals By Place Of Residence"

# Last month of the configured data window, the anchor every museum forecasts on from
PERIOD_END = pd.to_datetime(f"{END_YEAR} {END_MONTH}", format="%Y %b")


class ImputeRange:
    """A labelled month range to impute, e.g. the test period or the predict period."""

    def __init__(self, label, start, end):
        """
        Args:
            label (str): Name drawn on the plot, e.g. "Predict period".
            start (pd.Timestamp): Month-start Timestamp of the range's first month.
            end (pd.Timestamp): Month-start Timestamp of the range's last month.
        """
        self.label = label
        self.start = start
        self.end = end

    def __repr__(self):
        return f"ImputeRange({self.label!r}, {self.start:%Y-%m}, {self.end:%Y-%m})"


def sin_cos_month(df):
    # Cyclical encoding of month
    df["month"] = df["timestamp"].dt.month
    df["sin_month"] = np.sin(2 * np.pi * df["month"] / 12)
    df["cos_month"] = np.cos(2 * np.pi * df["month"] / 12)
    return df


def is_covid(df):
    # Create COVID indicator over the period defined in config
    df["is_covid"] = (
        (df["timestamp"] >= COVID_START) & (df["timestamp"] <= COVID_END)
    ).astype(int)
    return df


def is_closed(df):
    # A reported zero means the museum took no visitors that month
    df["is_closed"] = (df["value"] == 0).astype(int)
    return df


def add_event_flag(df, event_stem, col):
    """Flag the months covered by any occurrence of one recorded event.

    Args:
        df (pd.DataFrame): Frame with a 'timestamp' column.
        event_stem (str): Event CSV stem in event_ranges/, e.g. "deepavali".
        col (str): Name of the indicator column to add.

    Returns:
        pd.DataFrame: The same frame with `col` added, 1 inside an occurrence else 0.
    """
    occurrences = EventRange.from_folder(names=[event_stem])

    # A month counts if it falls inside any one of the event's occurrences
    covered = pd.Series(False, index=df.index)
    for event in occurrences:
        covered |= df["timestamp"].between(event.start, event.end)

    # Convert booleans to 0/1 to represent whether that event occurred in that month, and add to the frame
    df[col] = covered.astype(int)
    return df


def add_event_features(df):
    """Add every event indicator the models can draw on.

    Args:
        df (pd.DataFrame): Frame with a 'timestamp' column.

    Returns:
        pd.DataFrame: The same frame with one indicator column per event.
    """
    # Computed for every museum; the per-museum feature list decides who uses them
    return add_event_flag(df=df, event_stem="deepavali", col="is_deepavali")


def add_intl_arrivals(df, arrivals):
    """
    Merges total international visitor arrivals into the df
    """
    arr = arrivals.loc[
        arrivals["Data Series"] == INTL_ARRIVALS_SERIES,
        ["Reporting Period", "Value"],
    ].copy()
    arr.rename(columns={"Value": "intl_arrivals"}, inplace=True)
    arr["intl_arrivals"] = pd.to_numeric(arr["intl_arrivals"])
    return df.merge(arr, on="Reporting Period", how="left")


def engineer_features(museum_ts, arrivals):
    df = museum_ts.copy()
    df["timestamp"] = pd.to_datetime(df["Reporting Period"], format="%Y %b")
    df.rename(columns={"Value": "value"}, inplace=True)
    # SingStat's API returns numeric values as JSON strings (dtype object) --
    # cast explicitly. Non-numeric placeholders (e.g. "-", closed months) coerce
    # to NaN and are imputed as 0 visitors rather than dropped.
    df["value"] = pd.to_numeric(df["value"], errors="coerce").fillna(0)

    # Flag closures only after the coercion above, so imputed months count as closed
    df = is_closed(df)

    # Add international arrivals column
    df = add_intl_arrivals(df, arrivals)

    # Cyclical encoding of month
    df = sin_cos_month(df)

    # Arrivals are a separate SingStat table and can be published later than the visitorship one.
    if df["intl_arrivals"].isna().any():
        raise ValueError("No international arrivals data to impute from")

    # Create lag features (1 to 12 months)
    for lag in range(1, 13):
        df[f"lag_{lag}"] = df["value"].shift(lag)

    # Drop only the 12 leading months the lag features cannot fill
    df.dropna(subset=[f"lag_{lag}" for lag in range(1, 13)], inplace=True)

    # Create COVID features
    df = is_covid(df)

    # Add event features (for now only is_deepavali)
    df = add_event_features(df)

    return df


def exclude_covid(df):
    """Drop the rows falling inside the configured COVID period.

    Args:
        df (pd.DataFrame): Frame with a 'timestamp' column.

    Returns:
        pd.DataFrame: Only the rows outside COVID_START..COVID_END.
    """
    return df[(df["timestamp"] < COVID_START) | (df["timestamp"] > COVID_END)]


def exclude_closed(df):
    """Drop the rows where the museum was closed (0 visitors).

    Args:
        df (pd.DataFrame): Frame with an 'is_closed' column.

    Returns:
        pd.DataFrame: Only the rows the museum was open for.
    """
    return df[df["is_closed"] == 0]


def add_monthly_avg(train_data, test_data):
    """
    Monthly average computed on train only (avoid leakage), merged into test.
    COVID months are excluded so the average reflects normal visitorship.
    """
    train_data = train_data.copy()

    # Average over non-COVID months only, then map back onto every train row
    # Note: I didnt exclude_closed() here as that worsened RMSE for some reason
    normal_months = exclude_covid(train_data)
    monthly_means = normal_months.groupby("month")["value"].mean()
    if monthly_means.isna().any() or len(monthly_means) < train_data["month"].nunique():
        raise ValueError("Some calendar months have no open non-COVID data to average")
    train_data["monthly_avg"] = train_data["month"].map(monthly_means)

    # Get a df of unique month -> monthly_avg pairs from train data only
    monthly_avg = train_data[["month", "monthly_avg"]].drop_duplicates()

    # Merge monthly_avg into test_data on month, left join to keep all test rows
    test_data = pd.merge(test_data, monthly_avg, on="month", how="left")

    return train_data, test_data


def impute_monthly_avg(df, impute_ranges, window_years=None):
    """Impute a monthly series over given ranges with the historical calendar-month mean.

    Each range is filled from history strictly before that range starts, so a
    range lying inside the data is never imputed from itself.

    Args:
        df (pd.DataFrame): Frame with 'timestamp' and 'value' columns.
        impute_ranges (list[ImputeRange]): Labelled ranges to impute, inclusive of
            both endpoints.
        window_years (int | None): Years of history before each range to average
            over; None uses all history available before the range.

    Returns:
        pd.DataFrame: 'label', 'timestamp' and imputed 'value', one row per imputed month.
    """
    history = df[["timestamp", "value"]].sort_values("timestamp")

    frames = []
    for impute_range in impute_ranges:
        # Only history before the range, optionally limited to a trailing window
        source = history[history["timestamp"] < impute_range.start]
        if window_years is not None:
            source = source[
                source["timestamp"]
                >= impute_range.start - pd.DateOffset(years=window_years)
            ]

        # Mean per calendar month, mapped onto every month in the range
        monthly_avg = source.groupby(source["timestamp"].dt.month)["value"].mean()
        months = pd.date_range(impute_range.start, impute_range.end, freq="MS")
        frames.append(
            pd.DataFrame(
                {
                    "label": impute_range.label,
                    "timestamp": months,
                    "value": months.month.map(monthly_avg),
                }
            )
        )

    return pd.concat(frames, ignore_index=True)


def prepare_eval_data(museum_ts, arrivals):
    """
    Build an 80/20 chronological train/test split
    """
    # Padded as prepare_predict_data does, so a museum whose data stops early still
    # splits on the same months as the rest rather than seven months earlier
    df = engineer_features(pad_to_period_end(museum_ts), arrivals)

    split_point = int(len(df) * 0.8)
    train_data = df[:split_point]
    test_data = df[split_point:]

    # Create monthly average feature for train and test using only train data to avoid leakage
    train_data, test_data = add_monthly_avg(train_data, test_data)

    # full_data needs to be recreated from train_data and test_data to keep the added monthly_avg
    full_data = pd.concat([train_data, test_data], ignore_index=True)

    return train_data, test_data, full_data


def pad_to_period_end(museum_ts):
    """Pad a museum's raw series with zero-visitor rows up to the configured end month.

    Only months at or after the museum's first record are added, so one that opened
    late keeps its true start instead of gaining zeros for months before it existed.
    Padding keeps every museum's history ending at PERIOD_END, which is what lets the
    positional lag features below stay aligned to the calendar.

    Args:
        museum_ts (pd.DataFrame): Raw SingStat rows for one museum.

    Returns:
        pd.DataFrame: The same rows plus a zero-valued row per absent month, in date order.
    """
    df = museum_ts.copy()
    months = pd.to_datetime(df["Reporting Period"], format="%Y %b")

    # Months the API returned nothing for, between this museum's first record and the end
    absent = pd.date_range(months.min(), PERIOD_END, freq="MS").difference(
        pd.DatetimeIndex(months)
    )
    if absent.empty:
        return df

    # Reporting Period must be a real label so add_intl_arrivals can still merge on it
    padding = pd.DataFrame(
        {
            "Data Series": df["Data Series"].iloc[0],
            "Reporting Period": absent.strftime("%Y %b"),
            "Value": 0,
        }
    )
    padded = pd.concat([df, padding], ignore_index=True)

    # engineer_features shifts by position, so the rows have to be in date order
    order = pd.to_datetime(padded["Reporting Period"], format="%Y %b")
    return padded.assign(_order=order).sort_values("_order").drop(columns="_order").reset_index(drop=True)


def prepare_predict_data(museum_ts, arrivals, h):
    """
    Build a full-history train set plus a synthetic h-month-ahead future
    frame to for model to forecast.
    """
    full_data = engineer_features(pad_to_period_end(museum_ts), arrivals)

    # The lag features below are built by position, so a history that stops short of
    # PERIOD_END would shift every one of them without raising anything
    if full_data["timestamp"].max() != PERIOD_END:
        raise ValueError(
            f"History ends {full_data['timestamp'].max():%Y-%m}, expected {PERIOD_END:%Y-%m}; "
            "lag features would be misaligned"
        )

    # Every museum forecasts the same h months on from the configured end of the data,
    # rather than from its own last reported month
    forecast_horizon = pd.date_range(
        start=PERIOD_END + pd.DateOffset(months=1), periods=h, freq="MS"
    )
    future_frame = pd.DataFrame({"timestamp": forecast_horizon, "value": np.nan})
    future_frame["Data Series"] = full_data["Data Series"].iloc[-1]
    future_frame = sin_cos_month(future_frame)
    future_frame = is_covid(future_frame)
    future_frame = add_event_features(future_frame)

    # Assume museums stay open throughout prediction period
    future_frame["is_closed"] = 0

    # Concatenate the last 12 months of actual data with the synthetic future frame
    new_df = full_data.tail(12)
    new_df = pd.concat([new_df, future_frame], axis=0, join="outer")

    # Create lag features (1 to 12 months); missing ones imputed by monthly average
    for lag in range(1, 13):
        future_frame[f"lag_{lag}"] = new_df["value"].shift(lag)

    full_data, future_frame = add_monthly_avg(full_data, future_frame)

    # Impute missing lag features with monthly averages
    # Note: Decision made to impute missing lag features with monthly averages 
    # instead recursive forecasting to avoid error propagation
    future_frame["value"] = future_frame["monthly_avg"]
    for lag in range(1, 13):
        future_frame[f"lag_imp_{lag}"] = future_frame["value"].shift(lag)
        future_frame[f"lag_{lag}"] = future_frame[f"lag_{lag}"].fillna(0) + future_frame[
            f"lag_imp_{lag}"
        ].fillna(0)
    for lag in range(1, 13):
        future_frame.drop(f"lag_imp_{lag}", axis=1, inplace=True)

    # Do the same for international arrivals, excluding COVID only: arrivals are a
    # national series, unaffected by whether this one museum was closed
    arrivals_monthly_avg = exclude_covid(full_data).groupby("month")["intl_arrivals"].mean()
    if arrivals_monthly_avg.isna().any() or len(arrivals_monthly_avg) < 12:
        raise ValueError("Some calendar months have no non-COVID arrivals to average")
    future_frame["intl_arrivals"] = future_frame["month"].map(arrivals_monthly_avg)

    # must concat full_data + future_frame, to preserve monthly_avg and intl_arrivals features for future_frame
    combined_history = pd.concat([full_data, future_frame], axis=0, join="outer")
    return full_data, future_frame, combined_history
