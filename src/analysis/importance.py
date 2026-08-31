"""Permutation importance on the eval test set: shuffle a feature, measure how
much RMSE worsens. Model-agnostic and in metric units, so it compares across
models -- unlike each library's own impurity or gain score."""
import numpy as np
import pandas as pd
from sklearn.metrics import root_mean_squared_error

# Correlated columns mask each other when shuffled alone, so groups permute together
FEATURE_GROUPS = {
    "lags": lambda f: [c for c in f if c.startswith("lag_")],
    "calendar": lambda f: [c for c in f if c in ("sin_month", "cos_month")],
    "seasonal_level": lambda f: [c for c in f if c == "monthly_avg"],
    "regime_flags": lambda f: [c for c in f if c in ("is_covid", "is_closed")],
    "events": lambda f: [c for c in f if c == "is_deepavali"],
    "exogenous": lambda f: [c for c in f if c == "intl_arrivals"],
}


def permutation_importance(predict, test_data, features, n_repeats=5, random_state=42):
    """Score each feature and feature group by the RMSE cost of shuffling it.

    Args:
        predict (callable): Maps a raw feature DataFrame to predictions.
        test_data (pd.DataFrame): Eval test frame with `features` and 'value'.
        features (list[str]): Columns the model was fitted on.
        n_repeats (int): Shuffles per column, averaged.
        random_state (int): Seed for the shuffling.

    Returns:
        pd.DataFrame: 'feature', 'group', 'importance_rmse', 'baseline_rmse'.
    """
    # Error before any shuffling: the reference every score is measured against
    rng = np.random.default_rng(random_state)
    frame = test_data.copy().reset_index(drop=True)
    actual = frame["value"].values
    baseline = root_mean_squared_error(actual, predict(frame[features]))

    # One target per column, plus one per group this museum actually has features for
    targets = [(f, "single", [f]) for f in features]
    for name, select in FEATURE_GROUPS.items():
        cols = select(features)
        if cols:
            targets.append((name, "group", cols))

    # Break each target in turn; how far RMSE rises above the baseline is its score
    rows = []
    for name, kind, cols in targets:

        # Averaged over repeats, since one shuffle is a noisy draw
        scores = []
        for _ in range(n_repeats):

            # A group is destroyed by shuffling all of its columns at once
            shuffled = frame.copy()
            for c in cols:
                shuffled[c] = rng.permutation(shuffled[c].values)
            scores.append(root_mean_squared_error(actual, predict(shuffled[features])))

        rows.append(
            {
                "feature": name,
                "group": kind,
                "importance_rmse": float(np.mean(scores) - baseline),
                "baseline_rmse": float(baseline),
            }
        )

    # Sort by costliest feature first
    return pd.DataFrame(rows).sort_values("importance_rmse", ascending=False)
