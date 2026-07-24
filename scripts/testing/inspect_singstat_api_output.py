"""
Calls the SingStat Table Builder API and outputs the raw JSON response to
outputs/singstat_schema_sample.json, for inspection of the schema and data structure.
"""

import json
from pathlib import Path
from urllib.request import Request, urlopen

# ------------------------------ CONFIG ------------------------------ #
RESOURCE_ID = "M891071"  # museum visitorship; use "M550001" for intl arrivals
START_YEAR, START_MONTH = 2024, "Apr"
END_YEAR, END_MONTH = 2026, "Mar"
OUTPUT_PATH = Path(__file__).parent / "outputs" / "singstat_schema_sample.json"
# ---------------------------- CONSTANTS ----------------------------- #
MONTHS = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec",
]
# -------------------------------------------------------------------- #


def next_month(month):
    return MONTHS[(MONTHS.index(month) + 1) % 12]


def build_time_filter(start_year, start_month, end_year, end_month):
    periods = []  # list of periods in the format "YYYY%20MMM" e.g. "2023%20Mar"
    year, month = start_year, start_month
    while year <= end_year:
        periods.append(f"{year}%20{month}")
        if year == end_year and month == end_month:
            break
        month = next_month(month)
        if month == "Jan":
            year += 1
    return ",".join(periods)  # time_filter argument for API call


def fetch_raw(resource_id, start_year, start_month, end_year, end_month):
    time_filter = build_time_filter(start_year, start_month, end_year, end_month)
    url = (
        f"https://tablebuilder.singstat.gov.sg/api/table/tabledata/"
        f"{resource_id}?offset=0&timeFilter={time_filter}"
    )
    hdr = {
        "User-Agent": "Mozilla/5.0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8",
    }
    request = Request(url, headers=hdr)
    data = urlopen(request).read()
    return (json.loads(data.decode("utf-8")), url, time_filter)


if __name__ == "__main__":
    parsed, url, time_filter = fetch_raw(
        RESOURCE_ID, START_YEAR, START_MONTH, END_YEAR, END_MONTH
    )

    period_count = time_filter.count(",") + 1
    print(f"RESOURCE_ID: {RESOURCE_ID}")
    print(f"Number of periods requested: {period_count}")
    print(f"timeFilter length: {len(time_filter)} chars")
    print(f"Full URL length: {len(url)} chars")
    print(f"Rows returned (Institutions): {len(parsed['Data']['row'])}")
    print(f"Cols returned (Time periods): {len(parsed['Data']['row'][0]['columns'])}")

    OUTPUT_PATH.write_text(
        json.dumps(parsed, indent=2, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Raw response written to {OUTPUT_PATH}")
