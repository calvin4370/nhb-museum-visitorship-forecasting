"""Persist a run's fitted models under outputs/models/{MUSEUM_CODE}/."""
import os
import shutil

import joblib

MODELS_DIR = "./outputs/models"

# statsmodels and keras carry their own formats; everything else pickles
EXTENSIONS = {"sarimax": "pkl", "lstm": "keras"}


def museum_dir(museum_code):
    """Return the museum's artifact directory, emptied of any previous run."""
    path = os.path.join(MODELS_DIR, museum_code)

    # Gitignored files survive a checkout, so clear another branch's run first
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path, exist_ok=True)
    return path


def save_model(path, key, fitted):
    """Write one fitted model, using its library's format where it has one.

    Args:
        path (str): The museum's artifact directory.
        key (str): Short model key, e.g. "rf".
        fitted (Fitted | None): Container holding the estimator; None saves nothing.

    Returns:
        str | None: The file written, or None if the model has nothing to save.
    """
    # baseline and timegpt hold no estimator to write
    if fitted is None or fitted.model is None:
        return None

    target = os.path.join(path, f"{key}.{EXTENSIONS.get(key, 'joblib')}")

    # HoltWintersResults has no .save(), so it pickles with the sklearn models
    if key in ("sarimax", "lstm"):
        fitted.model.save(target)
    else:
        joblib.dump(fitted.model, target)
    return target
