"""Optional log transform of the target.

Everything outside a model stays in visitors: each model transforms on the way
in and inverts on the way out, so metrics, plots and tables are untouched.
"""
import numpy as np

from config import LOG_TARGET

# Columns measured in visitors, so they share the target's scale and must be
# transformed with it. intl_arrivals is a different series and is left alone.
def value_scaled(features):
    """Which of a museum's feature columns are on the target's scale."""
    return [f for f in features if f.startswith("lag_") or f == "monthly_avg"]


def to_log(values):
    """Visitors -> model space. log1p keeps closure months (0 visitors) at 0."""
    return np.log1p(values) if LOG_TARGET else values


def from_log(values, smearing=1.0):
    """Model space -> visitors, with the back-transform bias corrected.

    expm1 of a mean-of-logs is the conditional median, which understates the
    mean of a skewed distribution. `smearing` is Duan's correction factor.
    """
    return np.expm1(values) * smearing if LOG_TARGET else values


def smearing_factor(actual_log, predicted_log):
    """Duan's smearing estimator from a model's own training residuals.

    Args:
        actual_log (array-like): Training target in log space.
        predicted_log (array-like): The model's in-sample predictions, log space.

    Returns:
        float: Multiplier for expm1 output; 1.0 when the transform is off.
    """
    if not LOG_TARGET:
        return 1.0
    residuals = np.asarray(actual_log) - np.asarray(predicted_log)
    return float(np.mean(np.exp(residuals)))


def log_frame(df, features):
    """A copy of `df` with the target and every value-scaled feature logged."""
    if not LOG_TARGET:
        return df
    out = df.copy()
    for column in ["value", *value_scaled(features)]:
        if column in out.columns:
            out[column] = to_log(out[column])
    return out
