"""Persist each Optuna study under outputs/tuning/, so a run's hyperparameter
search can be inspected afterwards instead of being discarded with the function
that created it. Purely a record: the search itself is unchanged.
"""
import os
import optuna
from config import MUSEUM_CODES

STUDY_DIR = "./outputs/tuning"


def museum_code_from(train_data):
    """Short code for the museum a training frame belongs to.

    Args:
        train_data (pd.DataFrame): Frame carrying the 'Data Series' column.

    Returns:
        str: The museum's short code, or 'UNKNOWN' if the name is unrecognised.
    """
    return MUSEUM_CODES.get(train_data["Data Series"].iloc[0], "UNKNOWN")


def create_study(train_data, key, sampler):
    """An Optuna study backed by sqlite at outputs/tuning/{CODE}_{key}.db.

    A file left by a previous run is deleted rather than resumed, so each db
    holds exactly one run's trials.

    Args:
        train_data (pd.DataFrame): The museum's training frame.
        key (str): Short model key, e.g. "rf".
        sampler: The sampler the study should use.

    Returns:
        optuna.Study: Same direction and sampler as before, now persisted.
    """
    os.makedirs(STUDY_DIR, exist_ok=True)
    name = f"{museum_code_from(train_data)}_{key}"
    path = os.path.join(STUDY_DIR, f"{name}.db")

    # Clear any exisitng run's study if necessary
    if os.path.exists(path):
        os.remove(path)

    return optuna.create_study(
        direction="minimize",
        sampler=sampler,
        storage=f"sqlite:///{path}",
        study_name=name,
    )
