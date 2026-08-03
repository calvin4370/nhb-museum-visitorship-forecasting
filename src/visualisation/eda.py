import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns


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


def plot_monthly_visitorship(df, title, xmin, xmax, ylabel="Monthly visitorship ('000s)", highlight_missing=True, train_test=False):
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
                ha="center", va="top", color="blue", fontweight="bold")

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

    # Labels, bold title, and clean styling (no gridlines)
    ax.set_title(title, fontweight="bold")
    ax.set_xlabel("")
    ax.set_ylabel(ylabel)
    ax.set_ylim(bottom=0)  # anchor y-axis at 0 so zero months sit on the x-axis
    ax.grid(False)
    sns.despine()
    plt.tight_layout()
    plt.show()