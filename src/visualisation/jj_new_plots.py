"""Seaborn versions of the eval and predict timeplots, in the long shape the EDA
notebook uses. Written alongside the plotnine originals rather than replacing
them, since the existing plots are sized for the team's slide template.

Each plot lands in a subfolder of the original's directory -- jj-new-eval-plots/
or jj-new-predict-plots/ -- under the same filename.
"""
import os

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

EVAL_DIR = "jj-new-eval-plots"
PREDICT_DIR = "jj-new-predict-plots"

# Actual stays red, matching top_n_timeplot; the single forecast line is blue,
# the same colour the top-ranked model gets in the overlay plot
ACTUAL_COLOR = "red"
FORECAST_COLOR = "blue"
TOP_N_COLORS = ["blue", "darkgreen", "orange", "purple", "brown"]

FIGSIZE = (12, 3)
YLABEL = "Monthly Visitorship ('000s)"


def new_plot_path(original_path, eval):
    """Redirect a plot path into this module's subfolder, creating it if needed.

    Args:
        original_path (str): Where the plotnine version is saved.
        eval (bool): True for eval-mode plots, False for predict-mode.

    Returns:
        str: Path in the sibling subfolder, under the same filename.
    """
    directory = os.path.join(
        os.path.dirname(original_path), EVAL_DIR if eval else PREDICT_DIR
    )
    os.makedirs(directory, exist_ok=True)
    return os.path.join(directory, os.path.basename(original_path))


def _style_axes(ax, plot_data, title):
    """Apply the EDA notebook's house style: year gridlines, January ticks,
    bold title, no grid, despined."""
    xmin = plot_data["timestamp"].min()
    xmax = plot_data["timestamp"].max()
    ax.set_xlim(xmin, xmax)

    # Vertical line at each year boundary
    for year in range(xmin.year, xmax.year + 1):
        ax.axvline(
            pd.Timestamp(year=year, month=1, day=1),
            color="lightgray",
            linewidth=1,
            zorder=0,
        )

    # Ticks only at each January, labelled with the year
    ax.xaxis.set_major_locator(mdates.YearLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))

    ax.set_title(title, fontweight="bold")
    ax.set_xlabel("")
    ax.set_ylabel(YLABEL)

    # 25% headroom above the tallest plotted point, so the legend has room to sit
    # in the top-right corner without covering the series
    plotted = [
        np.nanmax(line.get_ydata()) for line in ax.get_lines() if len(line.get_ydata())
    ]
    if plotted:
        ax.set_ylim(0, max(plotted) * 1.25)
    ax.grid(False)
    sns.despine()


def _plot_title(title_prefix, plot_data):
    """Title carries the year range actually plotted, as the originals do."""
    start_year = plot_data["timestamp"].dt.year.min()
    end_year = plot_data["timestamp"].dt.year.max()
    return f"{title_prefix} ({start_year}-{end_year})"


def new_timeplot(original_path, title_prefix, train_data, test_data, forecast, eval):
    """One model's forecast against the actuals, saved in the new subfolder.

    Args:
        original_path (str): Path the plotnine version is saved to; the new plot
            goes in a subfolder beside it, under the same filename.
        title_prefix (str): Museum, model and mode, e.g. "IHC - XGBoost Eval".
        train_data (pd.DataFrame): Rows before the split, with 'timestamp'/'value'.
        test_data (pd.DataFrame): Rows after it; in predict mode 'value' is synthetic.
        forecast (array-like): The model's predictions for test_data's months.
        eval (bool): True to also draw the test-period actuals.
    """
    test_new = test_data.copy()
    test_new["Forecast"] = forecast

    # Actuals run through the test period in eval mode; in predict mode there are none
    actual = pd.concat([train_data, test_new]) if eval else train_data
    plot_data = pd.concat([actual[["timestamp"]], test_new[["timestamp"]]])

    _, ax = plt.subplots(figsize=FIGSIZE)
    sns.lineplot(x=actual["timestamp"], y=actual["value"], ax=ax,
                 color=ACTUAL_COLOR, label="Actual")
    sns.lineplot(x=test_new["timestamp"], y=test_new["Forecast"], ax=ax,
                 color=FORECAST_COLOR, label="Predicted")

    _style_axes(ax, plot_data, _plot_title(title_prefix, plot_data))
    ax.legend(fontsize=7, frameon=True, loc="upper right")
    plt.tight_layout()
    plt.savefig(new_plot_path(original_path, eval), dpi=300)
    plt.close()


def new_top_n_timeplot(original_path, title_prefix, train_data, test_data, model_forecasts):
    """Several models' predict-mode forecasts overlaid on the historical actuals.

    Args:
        original_path (str): Path the plotnine version is saved to.
        title_prefix (str): Museum and description, e.g. "IHC - Top 3 Models Predict".
        train_data (pd.DataFrame): Historical rows, with 'timestamp'/'value'.
        test_data (pd.DataFrame): Forecast horizon rows.
        model_forecasts (list): Ordered (model_code, forecast) pairs, best first.
    """
    plot_data = pd.concat([train_data[["timestamp"]], test_data[["timestamp"]]])

    _, ax = plt.subplots(figsize=FIGSIZE)
    sns.lineplot(x=train_data["timestamp"], y=train_data["value"], ax=ax,
                 color=ACTUAL_COLOR, label="Actual")

    # Same fixed rank-order colours as the plotnine overlay, so the two agree
    for (model_code, forecast), color in zip(model_forecasts, TOP_N_COLORS):
        sns.lineplot(x=test_data["timestamp"], y=forecast, ax=ax,
                     color=color, label=model_code)

    _style_axes(ax, plot_data, _plot_title(title_prefix, plot_data))
    ax.legend(fontsize=7, frameon=True, loc="upper right")
    plt.tight_layout()
    plt.savefig(new_plot_path(original_path, False), dpi=300)
    plt.close()
