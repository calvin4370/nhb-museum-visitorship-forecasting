"""
Shared configuration for the visitor forecasting pipeline: which
institutions to forecast for, the reference data range, and the forecast
horizon.
"""

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
# The model will be evaluated on the last 80% of months of this range.
# Forecasted months will be appended to the end of this range
START_YEAR, START_MONTH = 2014, "Jan"
END_YEAR, END_MONTH = 2026, "Mar"

# Number of months to forecast, default 2 years (i.e., 24 months)
h = 24

# Short model keys, in the order the pipeline runs them. 
MODEL_KEYS = ["rf", "xgb", "svr", "hw", "sarimax", "lstm", "timegpt", "baseline"]
