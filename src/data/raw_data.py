"""
Raw data for a run: reuse the saved SingStat CSVs in data/raw/ when they cover the configured
window, otherwise fetch from the API. --manual-data runs on manual CSVs instead and never calls
the API. Each path prints a short trail to stdout so a captured log shows where the data came from.
"""
import math
import os
from datetime import datetime

import pandas as pd

from config import START_YEAR, START_MONTH, END_YEAR, END_MONTH
from src.data.singstat_api import singstat_api, MAX_PERIODS_PER_REQUEST
from src.features.data_prep import INTL_ARRIVALS_SERIES

RAW_DIR = "./data/raw"

# Table ID -> (label used in the log, file the response is saved to)
SERIES = {
    "M891071": ("museum visitorship", f"{RAW_DIR}/museum_ts.csv"),
    "M550001": ("international arrivals", f"{RAW_DIR}/intl_arrivals.csv"),
}

# The window config asks SingStat for, which the data must cover to be usable
WINDOW_START = pd.to_datetime(f"{START_YEAR} {START_MONTH}", format="%Y %b")
WINDOW_END = pd.to_datetime(f"{END_YEAR} {END_MONTH}", format="%Y %b")


def _log(message, indent=0):
    print(f"[data] {'  ' if indent else ''}{message}")


def _saved_at(path):
    """
    When a file was last written, as e.g. "8 Sep 2026 7.56pm".

    Built manually rather than with strftime, as its no-leading-zero codes differ per os.
    """
    saved = datetime.fromtimestamp(os.path.getmtime(path))
    hour = saved.hour % 12 or 12
    meridiem = "am" if saved.hour < 12 else "pm"
    return f"{saved.day} {saved:%b} {saved.year} {hour}.{saved:%M}{meridiem}"


def _months(df):
    """The distinct reporting months in a raw frame, as Timestamps."""
    return pd.to_datetime(df["Reporting Period"], format="%Y %b").drop_duplicates()


def _why_unusable(df, label, required):
    """Why a frame can't be used, or None if it covers the window and has every required series."""
    months = _months(df)

    # A museum that closed part-way reports fewer months than the window, so the
    # coverage check is on the frame as a whole rather than per series
    if months.min() > WINDOW_START or months.max() < WINDOW_END:
        return (
            f"{label} covers {months.min():%b %Y} - {months.max():%b %Y}, "
            f"need {WINDOW_START:%b %Y} - {WINDOW_END:%b %Y}"
        )
    absent = [s for s in required if s not in set(df["Data Series"])]
    if absent:
        return f"{label} is missing {', '.join(absent)}"
    return None


def _load_usable(path, required):
    """Read one data file, or log why it cannot be used.

    Args:
        path (str): The CSV to read.
        required (list[str]): Data Series that must be present in the file.

    Returns:
        pd.DataFrame | None: The frame if it covers the window, else None.
    """
    if not os.path.exists(path):
        _log(f"{path} not found")
        return None

    df = pd.read_csv(path)
    problem = _why_unusable(df, path, required)
    if problem:
        _log(problem)
        return None

    _log(
        f"Found {path} ({len(_months(df))} months, {df['Data Series'].nunique()} series, "
        f"saved {_saved_at(path)})"
    )
    return df


def fetch_raw_data():
    """Fetch both series from SingStat and save them under data/raw/.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: visitorship and arrivals frames.

    Raises:
        RuntimeError: If any request fails; singstat_api names the table and period.
    """
    _log("Initiating API call to SingStat TableBuilder")

    # Periods are requested in chunks, so report the number of calls each table takes
    n_months = (WINDOW_END.year - WINDOW_START.year) * 12 + WINDOW_END.month - WINDOW_START.month + 1
    n_requests = math.ceil(n_months / MAX_PERIODS_PER_REQUEST)

    os.makedirs(RAW_DIR, exist_ok=True)
    frames = {}
    for resource_id, (label, path) in SERIES.items():
        try:
            df = singstat_api(resource_id, START_YEAR, START_MONTH, END_YEAR, END_MONTH)
        except RuntimeError:
            _log(f"{resource_id} {label} - FAILED", indent=1)
            raise

        df.to_csv(path, index=False)
        frames[resource_id] = df
        _log(
            f"{resource_id} {label} - {n_requests} requests - OK "
            f"({len(_months(df))} months, {df['Data Series'].nunique()} series)",
            indent=1,
        )

    _log(f"API call success - written to {RAW_DIR}/")
    return frames["M891071"], frames["M550001"]


def load_raw_data(museums, refresh=False):
    """Visitorship and arrivals from data/raw/ where it covers the window, else from the API.

    Args:
        museums (list[str]): Full museum names this run needs.
        refresh (bool): Fetch from the API even if the saved files would do.

    Raises:
        RuntimeError: If an API request fails, or SingStat hasn't published the whole window yet.
    """
    _log(
        f"Checking raw data for {', '.join(museums)} | "
        f"window {WINDOW_START:%b %Y} - {WINDOW_END:%b %Y}"
    )

    if refresh:
        _log("--refresh given, ignoring any saved files")
    else:
        visitors = _load_usable(SERIES["M891071"][1], museums)
        arrivals = _load_usable(SERIES["M550001"][1], [INTL_ARRIVALS_SERIES])
        if visitors is not None and arrivals is not None:
            _log("No API call needed - proceeding to pipeline")
            return visitors, arrivals

    visitors, arrivals = fetch_raw_data()

    # SingStat lags a few months, so a fresh download can still fall short of the window
    problems = [
        p for p in (
            _why_unusable(visitors, "SingStat visitorship", museums),
            _why_unusable(arrivals, "SingStat arrivals", [INTL_ARRIVALS_SERIES]),
        ) if p
    ]
    if problems:
        for p in problems:
            _log(p)
        raise RuntimeError(
            "SingStat hasn't published the whole window yet. "
            "Run with --manual-data, or move END_YEAR/END_MONTH in config.py earlier."
        )
    return visitors, arrivals


def load_manual_data(visitors_path, arrivals_path, museums):
    """Visitorship and arrivals from manual files only, in the same format as data/raw/.

    Raises:
        RuntimeError: If either file is missing, doesn't cover the window, or lacks a series.
    """
    _log("Using manual data only - data/raw/ and the SingStat API are not used")
    _log(
        f"Checking manual data for {', '.join(museums)} | "
        f"window {WINDOW_START:%b %Y} - {WINDOW_END:%b %Y}"
    )
    visitors = _load_usable(visitors_path, museums)
    arrivals = _load_usable(arrivals_path, [INTL_ARRIVALS_SERIES])
    if visitors is None or arrivals is None:
        raise RuntimeError(
            "Manual data can't be used. Check both files cover the window in config.py "
            "and include every museum and the arrivals series."
        )
    return visitors, arrivals


def warn_short_series(visitors, museums):
    """Warn when a museum's data stops before the window ends, as later months are padded with 0 visitors."""
    for museum in museums:
        last = _months(visitors[visitors["Data Series"] == museum]).max()
        if last < WINDOW_END:
            _log(
                f"WARNING: {museum} data ends {last:%b %Y}, so "
                f"{last + pd.DateOffset(months=1):%b %Y} - {WINDOW_END:%b %Y} will be treated as closed (0 visitors)"
            )
