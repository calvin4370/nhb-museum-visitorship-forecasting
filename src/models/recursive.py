"""Recursive (iterated) multi-step forecasting: each predicted month becomes the
lag input for the months that follow it."""
import numpy as np

N_LAGS = 12


def bound_prediction(prediction, fallback, upper=None):
    """Keep one recursive step finite and non-negative.

    Args:
        prediction (float): The model's raw output.
        fallback (float): Used when `prediction` is not finite.
        upper (float | None): Ceiling; None leaves it unbounded above.

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
        predict_row (callable): Maps a one-row feature frame to a float.
        test_data (pd.DataFrame): Future frame; copied, not mutated.
        features (list[str]): Feature columns in fitted order.
        upper (float | None): Per-step ceiling, see bound_prediction.

    Returns:
        np.ndarray: One prediction per row, in row order.
    """
    frame = test_data.copy().reset_index(drop=True)
    predictions = []

    for i in range(len(frame)):
        prediction = bound_prediction(
            predict_row(frame.loc[[i], features]), frame.loc[i, "monthly_avg"], upper
        )
        predictions.append(prediction)
        frame.loc[i, "value"] = prediction

        # Row i+lag reads row i as its lag_{lag}
        for lag in range(1, N_LAGS + 1):
            if i + lag < len(frame):
                frame.loc[i + lag, f"lag_{lag}"] = prediction

    return np.array(predictions)
