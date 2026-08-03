from pathlib import Path

import pandas as pd

# One CSV per event, each row a single dated occurrence of it
EVENT_RANGES_DIR = Path(__file__).parent / "event_ranges"


class EventRange:
    """One dated occurrence of an event, as a month range on the time axis."""

    def __init__(self, name, code, start, end):
        """
        Args:
            name: Full event name, e.g. "Deepavali".
            code: Short label drawn on the plot, e.g. "Dpvl".
            start: Month-start Timestamp of this occurrence's first month.
            end: Month-start Timestamp of this occurrence's last month.
        """
        self.name = name
        self.code = code
        self.start = start
        self.end = end

    def __repr__(self):
        return f"EventRange({self.name!r}, {self.code!r}, {self.start:%Y-%m}, {self.end:%Y-%m})"

    @classmethod
    def from_csv(cls, path):
        """Read one event's occurrences from a CSV of name, code, start, end.

        Args:
            path: CSV to read, with start and end as YYYY-MM.

        Returns:
            list[EventRange]: One entry per row, in file order.
        """
        df = pd.read_csv(path)
        return [
            cls(
                row["name"],
                row["code"],
                pd.Timestamp(row["start"]),
                pd.Timestamp(row["end"]),
            )
            for _, row in df.iterrows()
        ]

    @classmethod
    def from_folder(cls, folder=EVENT_RANGES_DIR, names=None):
        """Read event CSVs from a folder into one flat list.

        Args:
            folder: Folder of per-event CSVs; defaults to event_ranges/ beside this module.
            names: File stems to read, e.g. ["ramadan"]; defaults to every CSV in the folder.

        Returns:
            list[EventRange]: All occurrences, grouped by event in the order read.
        """
        folder = Path(folder)
        paths = sorted(folder.glob("*.csv")) if names is None else [folder / f"{n}.csv" for n in names]

        events = []
        for path in paths:
            events.extend(cls.from_csv(path))
        return events