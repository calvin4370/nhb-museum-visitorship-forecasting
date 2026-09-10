"""
Searches for the max number of time periods SingStat's API accepts per one request.

Also confirms whether the API length issue is based on number of time periods or
url length.

UPDATE: Results show that the API limits the number of time periods (YYYY MMM)
per request to 24), and url length does not affect call success.
"""

from pathlib import Path
from urllib.request import Request, urlopen
import urllib.error
from inspect_singstat_api_output import HDR, next_month, build_time_filter

# ------------------------------ CONFIG ------------------------------ #
RESOURCE_ID = "M891071"  # museum visitorship; use "M550001" for intl arrivals
START_YEAR, START_MONTH = 2013, "Jan"  # anchor date the search counts forward from
SEARCH_UPPER_BOUND = 200  # n_periods assumed to fail -- must exceed the real cap
PAD_LENGTHS = [200, 1000, 2000, 10000]  # offset-padding sizes tested in step 2
OUTPUT_PATH = Path(__file__).parent / "outputs" / "find_api_call_limits_report.txt"
# -------------------------------------------------------------------- #


def log(message, report):
    """Print a line and echo the same line to the report file."""
    print(message)
    report.write(message + "\n")


def advance(year, month, n_steps):
    """
    Step forward n_steps months from (year, month), wrapping the year at Dec->Jan.
    """
    for _ in range(n_steps):
        month = next_month(month)
        if month == "Jan":
            year += 1
    return year, month


def request_ok(offset="0", n_periods=10, start_year=START_YEAR, start_month=START_MONTH):
    """
    offset is passed through as-is so it can be padded with zeros for the
    length-vs-count check below without touching timeFilter at all.

    build_time_filter() (imported) takes a start AND end date, not a period
    count -- so n_periods is converted into an end date (n_periods - 1 months
    after start) before calling it, e.g. n_periods=24 from 2013 Jan produces
    an end date of 2014 Dec, giving 24 consecutive months inclusive.
    """
    end_year, end_month = advance(start_year, start_month, n_periods - 1)
    time_filter = build_time_filter(start_year, start_month, end_year, end_month)
    url = (
        f"https://tablebuilder.singstat.gov.sg/api/table/tabledata/"
        f"{RESOURCE_ID}?offset={offset}&timeFilter={time_filter}"
    )
    try:
        urlopen(Request(url, headers=HDR)).read()
        return True, len(url)
    except urllib.error.HTTPError:
        return False, len(url)


if __name__ == "__main__":
    OUTPUT_PATH.parent.mkdir(exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as report:
        log("Binary searching for the max valid period count...", report)

        low, high = 1, SEARCH_UPPER_BOUND
        while high - low > 1:
            mid = (low + high) // 2
            ok, _ = request_ok(n_periods=mid)
            low, high = (mid, high) if ok else (low, mid)
            log(
                f"  n_periods={mid:3d} -> {'OK' if ok else 'FAIL'}  (range now {low}-{high})",
                report,
            )
        log(f"\nMax valid periods per request: {low}\n", report)

        log("Confirming this is a period-count cap, not a URL-length cap...", report)
        _, failing_len = request_ok(n_periods=low + 1)
        for pad in PAD_LENGTHS:
            ok, url_len = request_ok(offset="0" * pad, n_periods=10)
            status = "OK" if ok else "FAIL"
            log(
                f"  offset padded to {pad:4d} zeros -> url_len={url_len:5d} "
                f"(vs failing request's url_len={failing_len}) -> {status}",
                report,
            )
    print(f"\nReport written to {OUTPUT_PATH}")
