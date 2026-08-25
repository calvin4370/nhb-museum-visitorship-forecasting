"""
Shared configuration for the visitor forecasting pipeline: which
institutions to forecast for, the reference data range, and the forecast
horizon.
"""

import pandas as pd

# These are the full names of the museums (as stated in the SingStat tableBuilder API) to forecast for, and their corresponding short codes
# Make sure to use the full names as they appear in the SingStat tableBuilder API, as they are used to filter the data for each museum.
# The codes can be whatever you want
MUSEUM_CODES = {
    "Asian Civilisations Museum": "ACM",
    "National Museum Of Singapore": "NMS",
    "Peranakan Museum": "TPM",
    "Indian Heritage Centre": "IHC",
    "Malay Heritage Centre": "MHC",
}

# Reference data range for the time series to be used for training
# The model will be evaluated on the last 20% of months of this range.
# Forecasted months will be appended to the end of this range
START_YEAR, START_MONTH = 2014, "Jan"
END_YEAR, END_MONTH = 2026, "Mar"

# Period flagged by the is_covid feature:
COVID_START = pd.Timestamp("2020-04-01") # Apr 2020 (circuit breaker, museums shut)
COVID_END = pd.Timestamp("2023-02-13") # 13 Feb 2023 (DORSCON Green, remaining border restrictions lifted)

# When True the COVID months are cut out of every museum's history entirely, so the
# months after COVID lag straight onto the months before it. Leaves is_covid all-zero.
EXCLUDE_COVID_PERIOD = True

# Number of months to forecast, default 2 years (i.e., 24 months)
h = 24

# Short model keys, in the order the pipeline runs them.
MODEL_KEYS = ["rf", "xgb", "svr", "hw", "sarimax", "lstm", "timegpt", "baseline"]

# Features every museum's tabular models (rf, xgb, svr, sarimax) train on
BASE_FEATURES = ["sin_month", "cos_month", "monthly_avg", "is_closed", "intl_arrivals"] + [
    f"lag_{i}" for i in range(1, 13)
] # NOTE: for tests 6a and 6b, is_covid was removed

# Per-museum overrides; a museum absent here uses BASE_FEATURES as-is
MUSEUM_FEATURES = {"IHC": BASE_FEATURES + ["is_deepavali"]}


def lstm_channels(features):
    """Return the per-timestep channels the LSTM should read.

    Args:
        features (list[str]): A museum's tabular feature list.

    Returns:
        list[str]: 'value' plus every non-lag feature. The 12-step input window
            already supplies the lag columns, so passing them again would feed
            the same history back once per timestep.
    """
    return ["value"] + [f for f in features if not f.startswith("lag_")]


def features_for(museum_code):
    """Return the feature list a museum's tabular models should use.

    Args:
        museum_code (str): Short museum code, e.g. "IHC".

    Returns:
        list[str]: The museum's override if it has one, else BASE_FEATURES.
    """
    return MUSEUM_FEATURES.get(museum_code, BASE_FEATURES)
