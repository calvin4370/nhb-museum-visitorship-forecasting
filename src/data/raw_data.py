"""
If raw SingStat data is present for a run: reuse the saved CSVs when they already cover the
configured window, otherwise fetch from the API. Either path prints a short trail
to stdout so a captured log shows whether an API call happened and how it went.
"""
import math
import os
from datetime import datetime

import pandas as pd

from config import START_YEAR, START_MONTH, END_YEAR, END_MONTH
from src.data.singstat_api import singstat_api, MAX_PERIODS_PER_REQUEST

RAW_DIR = "./data/raw"

# Table ID -> (label used in the log, file the response is saved to)
SERIES = {
    "M891071": ("museum visitorship", f"{RAW_DIR}/museum_ts.csv"),
    "M550001": ("international arrivals", f"{RAW_DIR}/intl_arrivals.csv"),
}

# The window config asks SingStat for, which the saved files must cover to be reusable
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


def _load_usable(path, museums):
    """Read one saved raw file, or explain why it cannot be reused.

    Args:
        path (str): The CSV to read.
        museums (list[str] | None): Museum series that must be present, or None to
            skip that check (the arrivals file carries no museums).

    Returns:
        pd.DataFrame | None: The frame if it covers the window, else None.
    """
    if not os.path.exists(path):
        _log(f"{path} not found")
        return None

    df = pd.read_csv(path)
    months = _months(df)

    # A museum that closed part-way reports fewer months than the window, so the
    # coverage check is on the file as a whole rather than per series
    if months.min() > WINDOW_START or months.max() < WINDOW_END:
        _log(
            f"{path} covers {months.min():%b %Y} - {months.max():%b %Y}, "
            f"need {WINDOW_START:%b %Y} - {WINDOW_END:%b %Y}"
        )
        return None

    if museums is not None:
        absent = [m for m in museums if m not in set(df["Data Series"])]
        if absent:
            _log(f"{path} is missing {', '.join(absent)}")
            return None

    series_count = df["Data Series"].nunique()
    _log(
        f"Found {path} ({len(months)} months, {series_count} series, "
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
    """Raw visitorship and arrivals for a run, from disk where possible.

    Args:
        museums (list[str]): Full museum names this run needs.
        refresh (bool): Fetch from the API even if the saved files would do.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: visitorship and arrivals frames.
    """
    _log(
        f"Checking raw data for {', '.join(museums)} | "
        f"window {WINDOW_START:%b %Y} - {WINDOW_END:%b %Y}"
    )

    if refresh:
        _log("--refresh given, ignoring any saved files")
        return fetch_raw_data()

    visitors = _load_usable(SERIES["M891071"][1], museums)
    arrivals = _load_usable(SERIES["M550001"][1], None)
    if visitors is not None and arrivals is not None:
        _log("No API call needed - proceeding to pipeline")
        return visitors, arrivals

    return fetch_raw_data()
