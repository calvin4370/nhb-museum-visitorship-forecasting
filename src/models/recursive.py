"""Recursive (iterated) multi-step forecasting.

The predict-period frame arrives with lag features filled from real history where
they exist and from the seasonal climatology where they do not. This module
replaces the climatology half: each step's prediction is written into the lag
columns of the rows that lag back to it, so the model forecasts off its own
earlier output instead of a historical monthly mean.
"""
import numpy as np

N_LAGS = 12


def recursive_forecast(predict_row, test_data, features):
    """Forecast one row at a time, feeding each prediction into later rows' lags.

    Args:
        predict_row (callable): Takes a one-row DataFrame of `features` and
            returns that row's prediction as a float.
        test_data (pd.DataFrame): Future frame carrying `features` and a 'value'
            column. Not mutated; a copy is used.
        features (list[str]): Feature columns, in the order the model was fitted on.

    Returns:
        np.ndarray: One prediction per row of `test_data`, in row order.
    """
    frame = test_data.copy().reset_index(drop=True)
    predictions = []

    for i in range(len(frame)):
        prediction = predict_row(frame.loc[[i], features])
        predictions.append(prediction)
        frame.loc[i, "value"] = prediction

        # Row i+lag's lag_{lag} is exactly the value at row i, so overwrite the
        # climatology that prepare_predict_data put there
        for lag in range(1, N_LAGS + 1):
            if i + lag < len(frame):
                frame.loc[i + lag, f"lag_{lag}"] = prediction

    return np.array(predictions)
