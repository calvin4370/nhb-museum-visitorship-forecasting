import pandas as pd
from plotnine import (
    aes,
    element_rect,
    element_text,
    geom_line,
    geom_ribbon,
    ggplot,
    labs,
    scale_color_manual,
    scale_x_datetime,
    theme,
    theme_classic,
)
import matplotlib.pyplot as plt

# Actual stays red; models get distinct, easily-told-apart colors regardless
# of how many of the top N are shown.
_TOP_N_COLORS = ["blue", "darkgreen", "orange", "purple", "brown"]


def timeplot(save_path, title_prefix, train_data, test_data, forecast, eval):
    test_data_new = test_data.copy()
    # Add in the model forecast into test data series
    test_data_new["Forecast"] = forecast

    # Merge confidence intervals with forecast data
    test_data_new.loc[:, "lower_ci"] = (
        test_data_new["Forecast"] - 1.96 * test_data_new["Forecast"].std()
    )
    test_data_new.loc[:, "upper_ci"] = (
        test_data_new["Forecast"] + 1.96 * test_data_new["Forecast"].std()
    )

    if eval:
        forecast_plot_data = pd.concat(
            [
                pd.DataFrame(
                    {
                        "timestamp": train_data["timestamp"],
                        "value": train_data["value"],
                        "Type": "Actual",
                    }
                ),
                pd.DataFrame(
                    {
                        "timestamp": test_data_new["timestamp"],
                        "value": test_data_new["value"],
                        "Type": "Actual",
                    }
                ),
                pd.DataFrame(
                    {
                        "timestamp": test_data_new["timestamp"],
                        "value": test_data_new["Forecast"],
                        "Type": "Predicted",
                    }
                ),
            ]
        ).merge(
            test_data_new[["timestamp", "lower_ci", "upper_ci"]],
            on="timestamp",
            how="left",
        )

    else:
        forecast_plot_data = pd.concat(
            [
                pd.DataFrame(
                    {
                        "timestamp": train_data["timestamp"],
                        "value": train_data["value"],
                        "Type": "Actual",
                    }
                ),
                pd.DataFrame(
                    {
                        "timestamp": test_data_new["timestamp"],
                        "value": test_data_new["Forecast"],
                        "Type": "Predicted",
                    }
                ),
            ]
        ).merge(
            test_data_new[["timestamp", "lower_ci", "upper_ci"]],
            on="timestamp",
            how="left",
        )

    # Title uses the full, human-readable prefix (museum + model + mode) plus
    # the actual year range plotted; save_path is the separate, compact filename.
    start_year = forecast_plot_data["timestamp"].dt.year.min()
    end_year = forecast_plot_data["timestamp"].dt.year.max()
    plot_title = f"{title_prefix} ({start_year}-{end_year})"

    # Plot and save the time series with confidence intervals
    confidence_plot = (
        ggplot(forecast_plot_data, aes(x="timestamp"))
        + geom_line(aes(y="value", color="Type"))
        + geom_ribbon(aes(ymin="lower_ci", ymax="upper_ci", fill="Type"), alpha=0.2)
        + scale_x_datetime(date_breaks="2 years", date_labels="%Y")
        + labs(
            title=plot_title,
            x="Year",
            y="Monthly Visitorship ('000s)",
        )
        + theme_classic()
    )
    confidence_plot.save(save_path)
    plt.close()


def top_n_timeplot(save_path, title_prefix, train_data, test_data, model_forecasts):
    """
    Overlay several models' predict-mode forecasts on one plot, alongside the
    historical actuals, each as its own color/legend entry.

    model_forecasts: ordered list of (model_code, forecast_array) tuples --
    model_code is the short registry key (e.g. "xgb"), used as the legend
    label; the order given is the order plotted/legend order.
    """
    frames = [
        pd.DataFrame(
            {
                "timestamp": train_data["timestamp"],
                "value": train_data["value"],
                "Model": "Actual",
            }
        )
    ]
    for model_code, forecast in model_forecasts:
        frames.append(
            pd.DataFrame(
                {
                    "timestamp": test_data["timestamp"],
                    "value": forecast,
                    "Model": model_code,
                }
            )
        )
    plot_data = pd.concat(frames)

    # Make sure the legend order is Actual, then models by lowest RMSE first
    legend_order = ["Actual"] + [model_code for model_code, _ in model_forecasts]
    plot_data["Model"] = pd.Categorical(
        plot_data["Model"], categories=legend_order, ordered=True
    )

    # Fixed color mapping (not the default hue scale, which reassigns shades
    # depending on how many categories exist) -- Actual is always red, models
    # get distinct colors in rank order, always including blue for 1st place.
    color_map = {"Actual": "red"}
    for model_code, color in zip(legend_order[1:], _TOP_N_COLORS):
        color_map[model_code] = color

    start_year = plot_data["timestamp"].dt.year.min()
    end_year = plot_data["timestamp"].dt.year.max()
    plot_title = f"{title_prefix} ({start_year}-{end_year})"

    comparison_plot = (
        ggplot(plot_data, aes(x="timestamp", y="value", color="Model"))
        + geom_line()
        + scale_x_datetime(date_breaks="2 years", date_labels="%Y")
        + scale_color_manual(values=color_map)
        + labs(
            title=plot_title,
            x="Year",
            y="Monthly Visitorship ('000s)",
        )
        + theme_classic()
        + theme(
            legend_title=element_text(size=8),
            legend_text=element_text(size=7),
            legend_key_size=10,
            legend_position="inside",
            legend_position_inside=(0.98, 0.98),
            legend_justification_inside=(1, 1),
            legend_background=element_rect(fill="white", color="black"),
        )
    )
    comparison_plot.save(save_path)
    plt.close()


def forecast_table(model_name, forecast):
    forecast_df = pd.DataFrame(forecast, columns=["Prediction"])
    forecast_df["Model"] = model_name
    return forecast_df
