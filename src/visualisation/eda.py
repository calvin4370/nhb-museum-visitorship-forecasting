import calendar

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
import seaborn as sns

# Half a month either side of an event, so a single-month one is spotlit rather than a hairline
HALF_MONTH = pd.DateOffset(days=15)


def _label_levels(ranges, starts, ends):
    """Assign each range a stacking level so labels on overlapping ranges do not collide.

    Args:
        ranges: Sequence of ranges, in draw order.
        starts: Callable returning a range's start.
        ends: Callable returning a range's end.

    Returns:
        list[int]: Level per range -- how many earlier ranges it overlaps.
    """
    return [
        sum(
            1
            for prev in ranges[:i]
            if starts(prev) <= ends(r) and starts(r) <= ends(prev)
        )
        for i, r in enumerate(ranges)
    ]


def _label_anchor(start, end, lo, hi):
    """Place a band's label, pinning it inside the axes when the band sits at an edge.

    Args:
        start: Left edge of the band.
        end: Right edge of the band.
        lo: Left axis bound.
        hi: Right axis bound.

    Returns:
        tuple: (x position, horizontal alignment) for the label.
    """
    margin = (hi - lo) / 12
    if start - lo < margin:
        return start, "left"
    if hi - end < margin:
        return end, "right"
    return start + (end - start) / 2, "center"


def get_shape(df):
    """Return a DataFrame's shape as a formatted string.

    Args:
        df: DataFrame to inspect.

    Returns:
        str: Shape formatted as "(N rows, M cols)".
    """
    num_rows, num_cols = df.shape
    return f"({num_rows:,} rows, {num_cols} cols)"


def get_freq_dist(series, index_name=None, count_name="Count", sort_by="count", dp=1):
    """Build a frequency distribution (count and proportion) for a Series.

    Args:
        series: Series to summarise.
        index_name: Optional name for the resulting table's index.
        count_name: Header for the count column.
        sort_by: "count" to sort by frequency descending, or "index" to sort by index.
        dp: Decimal places for the proportion (%).

    Returns:
        pd.DataFrame: Table with the count and "Proportion (%)" columns.
    """
    counts = series.value_counts()
    props = series.value_counts(normalize=True).mul(100).round(dp)

    # Add count and proportion (%) column
    freq_table = pd.concat([counts, props.rename("Proportion (%)")], axis=1)
    freq_table.columns = [count_name, "Proportion (%)"]

    if sort_by == "index":
        freq_table = freq_table.sort_index(ascending=True)
    else:
        freq_table = freq_table.sort_values(count_name, ascending=False)

    freq_table[count_name] = freq_table[count_name].apply(lambda x: f"{x:,}")

    if index_name:
        freq_table.index.name = index_name

    return freq_table


def _month_runs(months):
    """Group month-start timestamps into (start, end) runs of consecutive months.

    Args:
        months: Iterable of month-start Timestamps.

    Returns:
        list[tuple]: One (start, end) Timestamp pair per contiguous run.
    """
    runs = []
    for t in sorted(months):
        # Extend the current run if this month directly follows it, else start a new one
        if runs and t == runs[-1][1] + pd.DateOffset(months=1):
            runs[-1] = (runs[-1][0], t)
        else:
            runs.append((t, t))
    return runs


def plot_monthly_visitorship(df, title, xmin, xmax, ylabel="Monthly visitorship ('000s)", highlight_missing=True, train_test=False, y_millions=False):
    """Plot a monthly series (e.g. museum visitorship or arrivals) over a shared date range.

    When enabled, zero months are shaded orange and missing months red, so gaps
    and closures are visible against the fixed [xmin, xmax] x-axis.

    Args:
        df: DataFrame with 'timestamp' and 'value' columns.
        title: Title to display above the plot.
        xmin: Left x-axis bound (shared across series).
        xmax: Right x-axis bound (shared across series).
        ylabel: Y-axis label (default is museum visitorship in thousands).
        highlight_missing: If True, shade zero months orange and missing months red;
            "onlyorange" shades both orange for a cleaner look; False disables shading.
        train_test: If given as (train_start, split, test_end), shade the train span
            green and the test span blue (behind other shading) and label each.
        y_millions: If True, label y ticks in millions instead of a 1e6 offset.
    """
    # Line of visitorship over time, on a fixed x range
    _, ax = plt.subplots(figsize=(12, 3))
    sns.lineplot(data=df, x="timestamp", y="value", ax=ax)
    ax.set_xlim(xmin, xmax)

    # Optionally shade train (green) / test (blue) spans behind everything, labelled on top
    if train_test:
        train_start, split, test_end = train_test
        ax.axvspan(train_start, split, color="green", alpha=0.12, zorder=-1)
        ax.axvspan(split, test_end, color="blue", alpha=0.12, zorder=-1)
        xt = ax.get_xaxis_transform()  # x in data coords, y in axes fraction
        ax.text(train_start + (split - train_start) / 2, 0.96, "Train", transform=xt,
                ha="center", va="top", color="green", fontweight="bold")
        ax.text(split + (test_end - split) / 2, 0.96, "Test", transform=xt,
                ha="center", va="top", color="darkblue", fontweight="bold")

    # Optionally shade zero months (orange) and missing months -- absent rows or NaN (red)
    if highlight_missing:
        full_idx = pd.date_range(xmin, xmax, freq="MS")
        zero_months = pd.DatetimeIndex(df.loc[df["value"] == 0, "timestamp"])
        missing_months = full_idx.difference(pd.DatetimeIndex(df["timestamp"]))
        missing_months = missing_months.union(pd.DatetimeIndex(df.loc[df["value"].isna(), "timestamp"]))

        # "onlyorange" collapses the missing colour into orange for a cleaner look
        missing_color = "orange" if highlight_missing == "onlyorange" else "red"

        # Draw each as merged contiguous blocks; a lone month becomes a single 1.5-wide line
        for months, color in [(zero_months, "orange"), (missing_months, missing_color)]:
            for start, end in _month_runs(months):
                if start == end:
                    ax.axvline(start, color=color, linewidth=1.5, zorder=0)
                else:
                    ax.axvspan(start, end, color=color, alpha=0.3, linewidth=0, zorder=0)

    # Vertical line at each year boundary
    for year in range(xmin.year, xmax.year + 1):
        ax.axvline(pd.Timestamp(year=year, month=1, day=1), color="lightgray", linewidth=1, zorder=0)

    # Ticks only at each January, labelled with the year
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    # Y ticks in millions, so no 1e6 offset sits above the axis
    if y_millions:
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v / 1e6:g}"))

    # Labels, bold title, and clean styling (no gridlines)
    ax.set_title(title, fontweight="bold")
    ax.set_xlabel("")
    ax.set_ylabel(ylabel)
    ax.set_ylim(bottom=0)  # anchor y-axis at 0 so zero months sit on the x-axis
    ax.grid(False)
    sns.despine()
    plt.tight_layout()
    plt.show()


def plot_imputed_period(df, imputed, impute_ranges, title, xmin, xmax, ylabel="Monthly visitorship ('000s)", y_millions=False):
    """Plot actual monthly visitorship against values imputed over labelled ranges.

    Actuals are drawn in red and imputed months in light green with a dot per
    month, each range shaded, bounded by vertical green lines and labelled along
    the top. Where a range lies inside the data both lines are visible, and the
    gap between them is the imputation error.

    Args:
        df (pd.DataFrame): Actuals, with 'timestamp' and 'value' columns.
        imputed (pd.DataFrame): Imputed months, with 'timestamp' and 'value' columns.
        impute_ranges (list[ImputeRange]): The labelled ranges `imputed` covers.
        title (str): Title to display above the plot.
        xmin (pd.Timestamp): Left x-axis bound.
        xmax (pd.Timestamp): Right x-axis bound; extend past the data for future ranges.
        ylabel (str): Y-axis label (default is museum visitorship in thousands).
        y_millions (bool): If True, label y ticks in millions instead of a 1e6 offset.
    """
    # Reindex both onto every month in range so gaps show as breaks in the line
    full_idx = pd.date_range(xmin, xmax, freq="MS")
    actual = df.set_index("timestamp")["value"].reindex(full_idx)
    imputed_line = imputed.set_index("timestamp")["value"].reindex(full_idx)

    # Carry the last actual month before each range into the green line so they meet
    for impute_range in impute_ranges:
        prior = actual.loc[actual.index < impute_range.start].last_valid_index()
        if prior is not None:
            imputed_line.loc[prior] = actual.loc[prior]

    _, ax = plt.subplots(figsize=(12, 3))
    ax.plot(full_idx, actual.values, color="#c44e52", label="Actual", zorder=3)
    ax.plot(full_idx, imputed_line.values, color="#8fd694", marker="o", markersize=3,
            label="Imputed", zorder=4)
    ax.set_xlim(xmin, xmax)

    # Shade each range, mark its boundaries, and label it along the top
    xt = ax.get_xaxis_transform()  # x in data coords, y in axes fraction
    for impute_range in impute_ranges:
        ax.axvspan(impute_range.start, impute_range.end, color="#8fd694", alpha=0.15, zorder=0)
        for edge in (impute_range.start, impute_range.end):
            ax.axvline(edge, color="#55a868", linewidth=1.2, zorder=1)
        ax.text(impute_range.start + (impute_range.end - impute_range.start) / 2, 0.96,
                impute_range.label, transform=xt, ha="center", va="top",
                color="#55a868", fontweight="bold")

    # Vertical line at each year boundary
    for year in range(xmin.year, xmax.year + 1):
        ax.axvline(pd.Timestamp(year=year, month=1, day=1), color="lightgray", linewidth=1, zorder=0)

    # Ticks only at each January, labelled with the year
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    # Y ticks in millions, so no 1e6 offset sits above the axis
    if y_millions:
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v / 1e6:g}"))

    ax.set_title(title, fontweight="bold")
    ax.set_xlabel("")
    ax.set_ylabel(ylabel)
    ax.set_ylim(bottom=0)
    ax.grid(False)
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    sns.despine()
    plt.tight_layout()
    plt.show()


def plot_covid_period(df, title, xmin, xmax, covid_start, covid_end, ylabel="Monthly visitorship ('000s)", y_millions=False):
    """Plot a monthly series against the COVID period, with bad months marked as dots.

    Zero months get an orange dot, missing months a red dot at 0, and any line
    segment joining two such months is drawn red, so runs of bad data stand out
    against the shaded COVID window.

    Args:
        df: DataFrame with 'timestamp' and 'value' columns.
        title: Title to display above the plot.
        xmin: Left x-axis bound (shared across series).
        xmax: Right x-axis bound (shared across series).
        covid_start: Start of the COVID period to shade.
        covid_end: End of the COVID period to shade.
        ylabel: Y-axis label (default is museum visitorship in thousands).
        y_millions: If True, label y ticks in millions instead of a 1e6 offset.
    """
    # Reindex onto every month in range; absent months count as missing and plot at 0
    full_idx = pd.date_range(xmin, xmax, freq="MS")
    series = df.set_index("timestamp")["value"].reindex(full_idx)
    missing = series.isna()
    zero = series == 0
    series = series.fillna(0)

    # Line over the fixed x range, with the COVID period shaded light blue behind it
    _, ax = plt.subplots(figsize=(12, 3))
    ax.axvspan(covid_start, covid_end, color="lightblue", alpha=0.5, zorder=0)
    ax.plot(full_idx, series.values, zorder=2)
    ax.set_xlim(xmin, xmax)

    # Label the shaded span, on top of the plot
    xt = ax.get_xaxis_transform()  # x in data coords, y in axes fraction
    ax.text(covid_start + (covid_end - covid_start) / 2, 0.96, "COVID Period", transform=xt,
            ha="center", va="top", color="black", fontweight="bold")

    # Segments between two flagged months redrawn in red
    flagged = (zero | missing).values
    for i in range(len(series) - 1):
        if flagged[i] and flagged[i + 1]:
            ax.plot(full_idx[i:i + 2], series.values[i:i + 2], color="red", zorder=3)

    # A dot on each flagged month: orange for zero, red for missing
    for mask, color in [(zero, "orange"), (missing, "red")]:
        ax.scatter(full_idx[mask], series.values[mask], color=color, s=22, zorder=4)

    # Vertical line at each year boundary
    for year in range(xmin.year, xmax.year + 1):
        ax.axvline(pd.Timestamp(year=year, month=1, day=1), color="lightgray", linewidth=1, zorder=1)

    # Ticks only at each January, labelled with the year
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    # Y ticks in millions, so no 1e6 offset sits above the axis
    if y_millions:
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v / 1e6:g}"))

    # Labels, bold title, and clean styling (no gridlines)
    ax.set_title(title, fontweight="bold")
    ax.set_xlabel("")
    ax.set_ylabel(ylabel)
    ax.set_ylim(bottom=0)
    ax.grid(False)
    sns.despine()
    plt.tight_layout()
    plt.show()


def plot_seasonal_profile(df, title, xmin, xmax, exclude_ranges, month_ranges, footnote="", exclude_missing=True, ylabel="Average monthly visitors"):
    """Plot mean visitorship per calendar month, with fixed-calendar events highlighted.

    Args:
        df: DataFrame with 'timestamp' and 'value' columns.
        title: Title to display above the plot.
        xmin: Start of the date range to average over.
        xmax: End of the date range to average over.
        exclude_ranges: Iterable of (start, end) date ranges to leave out, e.g. COVID.
        month_ranges: Iterable of MonthRange to highlight, coloured from Set3.
        footnote: Small grey note under the plot, e.g. what was excluded.
        exclude_missing: If True, leave zero and missing months out of the
            aggregation so closures do not drag the mean down.
        ylabel: Y-axis label.
    """
    # Restrict to the date range, then drop each excluded range
    data = df[df["timestamp"].between(xmin, xmax)]
    for start, end in exclude_ranges:
        data = data[~data["timestamp"].between(start, end)]

    # Closure and gap months are not seasonality, so leave them out by default
    if exclude_missing:
        data = data[data["value"].notna() & (data["value"] != 0)]

    # Mean visitorship for each calendar month, over every year kept
    profile = data.groupby(data["timestamp"].dt.month)["value"].mean().reindex(range(1, 13))

    # Line with a dot on every month
    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(profile.index, profile.values, marker="o", zorder=3)
    ax.set_xlim(0.5, 12.5)

    # Each event spans half a month either side, labelled in full and stacked when overlapping
    month_ranges = list(month_ranges)
    colors = sns.color_palette("Set3", len(month_ranges))
    levels = _label_levels(month_ranges, lambda r: r.start_month, lambda r: r.end_month)
    xt = ax.get_xaxis_transform()  # x in data coords, y in axes fraction
    for mr, color, level in zip(month_ranges, colors, levels):
        start, end = mr.start_month - 0.5, mr.end_month + 0.5
        ax.axvspan(start, end, color=color, zorder=0)
        x, ha = _label_anchor(start, end, 0.5, 12.5)
        ax.text(x, 0.97 - 0.08 * level, mr.name, transform=xt, ha=ha, va="top", fontsize=8)

    # Ticks at every month, labelled with the short month code
    ax.set_xticks(range(1, 13))
    ax.set_xticklabels(calendar.month_abbr[1:])

    # Headroom above the line so the labels do not sit on top of a peak
    ax.set_ylim(0, profile.max() * (1.1 + 0.08 * max(levels, default=0)))

    # Small grey note under the plot, with room reserved for it
    if footnote:
        fig.text(0.01, 0.01, footnote, fontsize=8, color="grey")

    # Labels, bold title, and clean styling (no gridlines)
    ax.set_title(title, fontweight="bold")
    ax.set_xlabel("Month")
    ax.set_ylabel(ylabel)
    ax.set_ylim(bottom=0)
    ax.grid(False)
    sns.despine()
    plt.tight_layout(rect=(0, 0.04, 1, 1) if footnote else None)
    plt.show()


def event_colors(event_ranges, palette="Set3"):
    """Map each event name to its own colour, in the order the events appear.

    Args:
        event_ranges (Iterable[EventRange]): Events to colour.
        palette (str | list): Anything sns.color_palette accepts -- a palette
            name, or an explicit colour list to draw from.

    Returns:
        dict[str, tuple]: Event name to RGB colour.
    """
    names = list(dict.fromkeys(e.name for e in event_ranges))
    return dict(zip(names, sns.color_palette(palette, len(names))))


def plot_event_periods(df, title, xmin, xmax, event_ranges, colors=None, palette="Set3", ylabel="Monthly visitorship ('000s)", y_millions=False):
    """Plot the monthly series once per event, each event in its own colour.

    One plot per event keeps the highlights readable.

    Args:
        df (pd.DataFrame): Frame with 'timestamp' and 'value' columns.
        title (str): Title to display above each plot; the event name is appended.
        xmin (pd.Timestamp): Left x-axis bound (shared across series).
        xmax (pd.Timestamp): Right x-axis bound (shared across series).
        event_ranges (Iterable[EventRange]): Events, covering any number of names.
        colors (dict | None): Optional event name to colour map, so colours stay
            consistent across calls that each plot only some of the events.
        palette (str | list): Palette used when `colors` is not given (default "Set3").
        ylabel (str): Y-axis label (default is museum visitorship in thousands).
        y_millions (bool): If True, label y ticks in millions instead of a 1e6 offset.
    """
    # One colour per event, unless the caller supplied a shared map
    event_ranges = [e for e in event_ranges if e.end >= xmin and e.start <= xmax]
    names = list(dict.fromkeys(e.name for e in event_ranges))
    colors = colors or event_colors(event_ranges, palette)

    # A plot of its own for each event
    for name in names:
        occurrences = [e for e in event_ranges if e.name == name]
        _plot_one_event(df, f"{title} ({name})", xmin, xmax, occurrences, colors[name], ylabel, y_millions)


def _plot_one_event(df, title, xmin, xmax, occurrences, color, ylabel, y_millions):
    """Plot a monthly series with every occurrence of a single event highlighted.

    Args:
        df: DataFrame with 'timestamp' and 'value' columns.
        title: Title to display above the plot.
        xmin: Left x-axis bound.
        xmax: Right x-axis bound.
        occurrences: EventRange list for one event, already clipped to the range.
        color: Colour for every band of this event.
        ylabel: Y-axis label.
        y_millions: If True, label y ticks in millions instead of a 1e6 offset.
    """
    # Reindex onto every month in range so gaps in the series show as gaps
    full_idx = pd.date_range(xmin, xmax, freq="MS")
    series = df.set_index("timestamp")["value"].reindex(full_idx)

    # Line over the fixed x range
    _, ax = plt.subplots(figsize=(12, 3))
    line, = ax.plot(full_idx, series.values, zorder=3)
    ax.set_xlim(xmin, xmax)

    # Each occurrence spans half a month either side, labelled with the event code
    xt = ax.get_xaxis_transform()  # x in data coords, y in axes fraction
    for event in occurrences:
        start, end = event.start - HALF_MONTH, event.end + HALF_MONTH
        ax.axvspan(start, end, color=color, zorder=0)
        x, ha = _label_anchor(start, end, xmin, xmax)
        ax.text(x, 0.97, event.code, transform=xt, ha=ha, va="top", fontsize=8)

        # Dot on each month the event covers
        months = pd.date_range(event.start, event.end, freq="MS")
        ax.scatter(months, series.reindex(months).values, color=line.get_color(), s=18, zorder=4)

    # Vertical line at each year boundary
    for year in range(xmin.year, xmax.year + 1):
        ax.axvline(pd.Timestamp(year=year, month=1, day=1), color="lightgray", linewidth=1, zorder=1)

    # Ticks only at each January, labelled with the year
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    # Y ticks in millions, so no 1e6 offset sits above the axis
    if y_millions:
        ax.yaxis.set_major_formatter(FuncFormatter(lambda v, _: f"{v / 1e6:g}"))

    # Headroom above the line so the labels do not sit on top of a peak
    top = series.max()
    ax.set_ylim(0, top * 1.12 if top else None)

    # Labels, bold title, and clean styling (no gridlines)
    ax.set_title(title, fontweight="bold")
    ax.set_xlabel("")
    ax.set_ylabel(ylabel)
    ax.grid(False)
    sns.despine()
    plt.tight_layout()
    plt.show()