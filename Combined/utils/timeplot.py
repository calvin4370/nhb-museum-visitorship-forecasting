import pandas as pd
from plotnine import (
    aes,
    geom_line,
    geom_ribbon,
    ggplot,
    labs,
    scale_x_datetime,
    theme_classic
)
import matplotlib.pyplot as plt

def timeplot(model_name, train_data, test_data, forecast, eval):
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
        ).merge(test_data_new[["timestamp", "lower_ci", "upper_ci"]], on="timestamp", how="left")
    
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
        ).merge(test_data_new[["timestamp", "lower_ci", "upper_ci"]], on="timestamp", how="left")        

    # Corrected visualization without explicit upper/lower bound lines
    confidence_plot = (
        ggplot(forecast_plot_data, aes(x="timestamp"))
        + geom_line(aes(y="value", color="Type"))
        + geom_ribbon(aes(ymin="lower_ci", ymax="upper_ci", fill="Type"), alpha=0.2)
        + scale_x_datetime(date_breaks="2 years", date_labels="%Y")
        + labs(
            title="Forecast with Confidence Intervals",
            x="Year",
            y="Monthly Visitorship ('000)",
        )
        + theme_classic()
    )
    confidence_plot.save(f"./timeplot_output/{model_name}_timeplot.png")
    plt.close()

def forecast_table(model_name, forecast):
    forecast_df = pd.DataFrame(forecast, columns=["Prediction"])
    forecast_df["Model"] = model_name
    return forecast_df