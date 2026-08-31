"""Container pairing a fitted model with a callable that predicts from a raw
feature frame, so callers need not know about per-model scaling."""


class Fitted:
    """A fitted model and, where meaningful, how to predict raw feature rows with it.

    Args:
        model: The fitted estimator, saved as the run's artifact.
        predict (callable | None): Maps a raw feature DataFrame to predictions.
            None for models with no tabular feature interface.
    """

    def __init__(self, model, predict=None):
        self.model = model
        self.predict = predict
