"""Recursive (iterated) multi-step forecasting.

The predict-period frame arrives with lag features filled from real history where
they exist and from the seasonal climatology where they do not. This module
replaces the climatology half: each step's prediction is written into the lag
columns of the rows that lag back to it, so the model forecasts off its own
earlier output instead of a historical monthly mean.
"""
import numpy as np

N_LAGS = 12


def bound_prediction(prediction, fallback, upper=None):
    """Keep one recursive step finite and physically possible.

    A model fed its own output can diverge, and a single overflow to inf or nan
    poisons the lag features of every later row. Substitute the seasonal mean for
    a non-finite step, and hold the rest in [0, upper] -- visitorship cannot be
    negative, and a forecast far above anything on record is not a forecast.

    Args:
        prediction (float): The model's raw output for this step.
        fallback (float): Value to use when `prediction` is not finite.
        upper (float | None): Ceiling; None leaves the step unbounded above.

    Returns:
        float: The bounded prediction.
    """
    if not np.isfinite(prediction):
        prediction = float(fallback)
    prediction = max(float(prediction), 0.0)
    return prediction if upper is None else min(prediction, float(upper))


def recursive_forecast(predict_row, test_data, features, upper=None):
    """Forecast one row at a time, feeding each prediction into later rows' lags.

    Args:
        predict_row (callable): Takes a one-row DataFrame of `features` and
            returns that row's prediction as a float.
        test_data (pd.DataFrame): Future frame carrying `features` and a 'value'
            column. Not mutated; a copy is used.
        features (list[str]): Feature columns, in the order the model was fitted on.
        upper (float | None): Ceiling for each step, see bound_prediction.

    Returns:
        np.ndarray: One prediction per row of `test_data`, in row order.
    """
    frame = test_data.copy().reset_index(drop=True)
    predictions = []

    for i in range(len(frame)):
        prediction = bound_prediction(
            predict_row(frame.loc[[i], features]), frame.loc[i, "monthly_avg"], upper
        )
        predictions.append(prediction)
        frame.loc[i, "value"] = prediction

        # Row i+lag's lag_{lag} is exactly the value at row i, so overwrite the
        # climatology that prepare_predict_data put there
        for lag in range(1, N_LAGS + 1):
            if i + lag < len(frame):
                frame.loc[i + lag, f"lag_{lag}"] = prediction

    return np.array(predictions)
