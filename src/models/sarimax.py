import pandas as pd
import numpy as np

import optuna
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tools.sm_exceptions import ConvergenceWarning
from config import N_TRIALS
from src.models.fitted import Fitted
from src.analysis.tuning import create_study, museum_code_from
from sklearn.model_selection import TimeSeriesSplit
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_percentage_error, root_mean_squared_error

import warnings

# statsmodels falls back to zeros when its starting values are unusable, so these are harmless
STARTING_VALUE_WARNINGS = r"Non-stationary starting|Non-invertible starting|Too few observations to estimate starting"


def fit_counting(model, counts, **fit_kwargs):
    """
    Fit a SARIMAX model with the starting-value warnings silenced. Convergence warnings are
    counted in `counts` rather than printed per fit; any other warning is passed on as usual.
    """
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        warnings.filterwarnings("ignore", message=STARTING_VALUE_WARNINGS, category=UserWarning)
        fitted = model.fit(**fit_kwargs)

    counts["fits"] += 1
    counts["not_converged"] += any(issubclass(w.category, ConvergenceWarning) for w in caught)
    for w in caught:
        if not issubclass(w.category, ConvergenceWarning):
            warnings.warn_explicit(w.message, w.category, w.filename, w.lineno)
    return fitted


def monthly_index(df):
    """The frame's months as a date index, so statsmodels can date its forecasts instead of warning."""
    return pd.DatetimeIndex(df["timestamp"], freq="MS")


def sarimax_model(train_data, test_data, eval, features, best_params=None):
    # Target the caller's feature list predicts
    target = "value"

    # Set seed for reproducibility
    random_state = 42

    # Standardise exogenous features
    scaler = StandardScaler()
    train_exog = pd.DataFrame(
        scaler.fit_transform(train_data[features]),
        columns=features, index=monthly_index(train_data),
    )
    test_exog = pd.DataFrame(
        scaler.transform(test_data[features]),
        columns=features, index=monthly_index(test_data),
    )
    train_endog = train_data[target].set_axis(monthly_index(train_data))

    # If best_params is provided, use it
    # Else, perform hyperparameter optimization with Optuna
    if best_params is None:
        tuning_fits = {"fits": 0, "not_converged": 0}

        def objective(trial):
            # Define the search space
            # Non-seasonal params
            p = trial.suggest_int('p', 0, 5)
            d = trial.suggest_int('d', 0, 2)
            q = trial.suggest_int('q', 0, 5)
            # Seasonal params
            P = trial.suggest_int('P', 0, 2)
            D = trial.suggest_int('D', 0, 1)
            Q = trial.suggest_int('Q', 0, 2)

            # Optuna can suggest settings it has already tried, so reuse that trial's score rather than refitting
            for done in trial.study.get_trials(deepcopy=False, states=[optuna.trial.TrialState.COMPLETE]):
                if done.params == trial.params:
                    return done.value

            # Rolling-origin folds, each validating a full 12-month season. Endog
            # stays unscaled -- only exog needs standardising
            tscv = TimeSeriesSplit(n_splits=3, test_size=12)
            errors = []

            try:
                for train_idx, val_idx in tscv.split(train_data):
                    tr_endog = train_endog.iloc[train_idx]
                    val_endog = train_endog.iloc[val_idx]
                    tr_exog = train_exog.iloc[train_idx]
                    val_exog = train_exog.iloc[val_idx]

                    fitted_model = fit_counting(
                        SARIMAX(
                            endog=tr_endog,
                            exog=tr_exog,
                            order=(p, d, q),
                            seasonal_order=(P, D, Q, 12),
                            enforce_stationarity=True,
                            enforce_invertibility=True
                        ),
                        tuning_fits,
                        disp=False,
                    )

                    val_forecast = fitted_model.get_forecast(
                        steps=len(val_idx), exog=val_exog
                    )
                    errors.append(
                        root_mean_squared_error(val_endog, val_forecast.predicted_mean)
                    )
                return np.mean(errors)

            except Exception as e:
                return float('inf')

        sampler = optuna.samplers.TPESampler(seed=random_state)
        study = create_study(train_data, "sarimax", sampler)
        study.optimize(objective, n_trials=N_TRIALS)
        distinct = len({tuple(sorted(t.params.items())) for t in study.trials})
        print(
            f"  [sarimax] {museum_code_from(train_data)}: {len(study.trials)} trials, {distinct} distinct settings, "
            f"{tuning_fits['not_converged']} of {tuning_fits['fits']} tuning fits did not converge"
        )
        best_params = study.best_params

    # Train the best model
    best_model = SARIMAX(
        endog=train_endog,
        exog=train_exog,
        order=(best_params["p"], best_params["d"], best_params["q"]),
        seasonal_order=(best_params["P"], best_params["D"], best_params["Q"], 12),
        enforce_stationarity=True,
        enforce_invertibility=True,
    )
    final_fit = {"fits": 0, "not_converged": 0}
    best_model_fitted = fit_counting(best_model, final_fit)
    if final_fit["not_converged"]:
        print(f"  [sarimax] {museum_code_from(train_data)}: final fit did not converge")

    # Forecasting
    forecast_periods = len(test_data["value"])
    forecast = best_model_fitted.get_forecast(steps=forecast_periods, exog=test_exog)
    test_data["Forecast"] = forecast.predicted_mean.values

    if eval:    
        # Metrics Calculation
        rmse_sarimax = root_mean_squared_error(test_data["value"], test_data["Forecast"])
        mape_sarimax = mean_absolute_percentage_error(test_data["value"], test_data["Forecast"])

        model_eval = ['SARIMAX', rmse_sarimax, mape_sarimax]
    else:
        model_eval = []

    # Exog is standardised, so raw rows are scaled before being forecast on
    def predict_exog(X):
        exog = pd.DataFrame(scaler.transform(X[features]), columns=features, index=monthly_index(X))
        return best_model_fitted.get_forecast(steps=len(X), exog=exog).predicted_mean.values

    return model_eval, test_data["Forecast"], best_params, Fitted(best_model_fitted, predict_exog)