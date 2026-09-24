from pathlib import Path

import pandas as pd

# Fixed-calendar events only, in one CSV alongside this module
MONTH_RANGES_CSV = Path(__file__).parent / "month_ranges.csv"


class MonthRange:
    """A recurring event as a calendar-month window, for the seasonal profile plot."""

    def __init__(self, name, start_month, end_month):
        """
        Args:
            name: Full event name, e.g. "National Day".
            start_month: First calendar month of the event (1-12).
            end_month: Last calendar month of the event (1-12).
        """
        self.name = name
        self.start_month = start_month
        self.end_month = end_month

    def __repr__(self):
        return f"MonthRange({self.name!r}, {self.start_month}, {self.end_month})"

    @classmethod
    def from_csv(cls, path=MONTH_RANGES_CSV):
        """Read fixed-calendar events from a CSV of name, start_month, end_month.

        Args:
            path: CSV to read; defaults to month_ranges.csv beside this module.

        Returns:
            list[MonthRange]: One entry per row, in file order.
        """
        df = pd.read_csv(path)

        # Months are stored as short codes (e.g. "Aug") for readability
        to_month = lambda code: pd.to_datetime(code, format="%b").month
        return [
            cls(row["name"], to_month(row["start_month"]), to_month(row["end_month"]))
            for _, row in df.iterrows()
        ]