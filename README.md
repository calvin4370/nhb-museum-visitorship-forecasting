# Museum Visitorship Forecasting

## Overview
Forecasts monthly visitorship for five National Heritage Board (NHB) museums up to 24 months ahead of training data. The forecasts are meant to serve as an additional reference point during workplan target setting.

**Museum Scope:**
| Code | Museum |
| --- | --- |
| ACM | Asian Civilisations Museum |
| NMS | National Museum of Singapore |
| TPM | The Peranakan Museum |
| IHC | Indian Heritage Centre |
| MHC | Malay Heritage Centre |

Both the historical window for training and the forecast horizon are configurable (see [Configuration](#configuration)). 

Read [Limitations](#limitations) before using any figure for planning.


<br>

## Data Source

### SingStat TableBuilder API
| Series | Table ID | Used as |
| --- | --- | --- |
| Monthly museum visitorship | `M891071` | forecast target (`value`) |
| Total international visitor arrivals | `M550001` | exogenous feature (`intl_arrivals`) |

Both series are fetched at runtime by `src/data/singstat_api.py`.

The requested window is set by `START_YEAR`/`START_MONTH` and `END_YEAR`/`END_MONTH` in `config.py` (currently Jan 2014 – Mar 2026, monthly). Raw responses are written to `data/raw/museum_ts.csv` and `data/raw/intl_arrivals.csv` for reference.


<br>

## Quick Start

This project makes use of **Python 3.11.9** and several package versions require this specific Python version.

#### 1. Using `uv` to isolate both Python and package versions (recommended)
Windows Powershell
```powershell
pip install uv
uv venv --python 3.11.9
.venv\Scripts\Activate.ps1
uv pip install -r requirements.txt
```

bash/zsh (Max/Linux)
```bash
pip install uv
uv venv --python 3.11.9
source .venv/bin/activate
uv pip install -r requirements.txt
```

**Alternatively, if you use base `venv`, you need to install and run the correct python version too (3.11.9)**
Windows Powershell
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

bash/zsh (Max/Linux)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### 2. Run the pipeline for all museums and models
```bash
python main.py
```

<br>

## Usage
`python main.py` trains 8 models each for 5 museums

Run `python main.py --help` to see the available flag arguments

```
usage: python main.py [-h] [--museum MUSEUM_CODE [MUSEUM_CODE ...]] [--models MODEL [MODEL ...]]

Run the museum visitorship forecasting pipeline.

options:
  -h, --help            show this help message and exit
  --museum MUSEUM_CODE [MUSEUM_CODE ...], -m MUSEUM_CODE [MUSEUM_CODE ...]
                        Run for specific museums only (case-insensitive codes, e.g. python main.py --museum ACM TPM to only run pipelines for ACM and TPM).
                        Choices: ACM, NMS, TPM, IHC, MHC
                        Omit to run all museums.
                        
  --models MODEL [MODEL ...], -M MODEL [MODEL ...]
                        Run specific models only (case-insensitive keys, e.g. python main.py --models rf xgb lstm to only run the RF, XGB, and LSTM models).
                        Choices: rf, xgb, svr, hw, sarimax, lstm, timegpt, baseline
                        Omit to run all models.
```

<br>

## Project Structure
```
visitor_forecast/
├── main.py                   # Entry point: fetch data, then run the pipeline per museum
├── config.py                 # Museums, date range, horizon, feature sets, model keys
├── requirements.txt
├── notebooks/
│   └── 01_eda.ipynb          # Exploratory data analysis
├── scripts/testing/          # One-off scripts used to probe the SingStat API's limits
├── src/
│   ├── cli.py                # Argument parsing, museum-code and model-key validation
│   ├── pipeline.py           # Per-museum orchestration: evaluate, rank, forecast, report
│   ├── data/
│   │   └── singstat_api.py   # SingStat TableBuilder client (request chunking, throttling)
│   ├── features/
│   │   └── data_prep.py      # Feature engineering, train/test preparation, imputation
│   ├── events/
│   │   ├── event_range.py    # Loader for dated event occurrences
│   │   ├── event_ranges/     # One CSV per event, one row per occurrence
│   │   ├── month_range.py    # Loader for fixed-calendar events
│   │   └── month_ranges.csv  # Events that fall in the same month every year
│   ├── models/               # The eight forecasting models, plus model_registry.py
│   └── visualisation/
│       ├── timeplot.py       # Evaluation and forecast plots
│       ├── summary.py        # Financial-year totals and the summary report
│       └── eda.py            # Plotting helpers used only by the notebook
├── data/                     # Generated at runtime
│   ├── raw/                  # Raw API responses
│   └── processed/            # Engineered features per museum
└── outputs/                  # Generated at runtime, one folder per museum
```

<br>

## Configuration
### `config.py`

| Setting | Controls |
| --- | --- |
| `MUSEUM_CODES` | Which museums to forecast. Keys must match the SingStat series name exactly; the codes are yours to choose and are used in CLI flags, output folders and filenames. |
| `START_YEAR`/`START_MONTH`, `END_YEAR`/`END_MONTH` | The historical window requested from SingStat for training. e.g. Jan 2014 - Mar 2026|
| `COVID_START`, `COVID_END` | The period flagged by `is_covid`, and excluded when computing historical monthly averages. |
| `h` | Forecast horizon in months (default 24). Forecasting starts the month after `END_YEAR`/`END_MONTH`. |
| `MODEL_KEYS` | Which models run, and in what order. Must match the keys in `src/models/model_registry.py`. |
| `BASE_FEATURES` | The feature set every museum's tabular models train on. |
| `MUSEUM_FEATURES` | Per-museum overrides of that feature set. |


<br>

### `.env`
- For environment variables (currently not yet implemented)


<br>

## Methodology
### Models Trained
| Key | Model | Sees | Tuned |
| --- | --- | --- | --- |
| `baseline` | Calendar-month mean of the last 36 months | history only | — |
| `hw` | Holt-Winters exponential smoothing, 12-month seasonality | history only | Optuna |
| `sarimax` | SARIMAX, orders `(p,d,q)(P,D,Q,12)` searched, features as standardised regressors | full feature set | Optuna |
| `rf` | Random Forest | full feature set | Optuna |
| `xgb` | XGBoost | full feature set | Optuna |
| `svr` | Support Vector Regression, kernel searched (`linear`/`rbf`/`poly`) | full feature set | Optuna |
| `lstm` | Two stacked LSTM layers (50 units) → Dense(25) → Dense(1), 12-month input window, 50 epochs | feature set except lag features | — |

Note: `timegpt` is not currently implemented yet


<br>

### Features
The target column is `value`, which represents monthly museum visitorship (in thousands).

`BASE_FEATURES` includes all the features most multivariate models take.

| Feature | Description | Used in |
| --- | --- | --- |
| `sin_month`, `cos_month` | Cyclical encoding of the calendar month, so December and January sit next to each other | `BASE_FEATURES` |
| `monthly_avg` | Mean visitorship for that calendar month. Computed on training data only, with COVID months excluded | `BASE_FEATURES` |
| `lag_1` … `lag_12` (12 features) | Visitorship in the time periods 1 to 12 months earlier | `BASE_FEATURES` (except LSTM) |
| `is_covid` | `1` for months inside `COVID_START`–`COVID_END`. `0` otherwise. | `BASE_FEATURES` |
| `intl_arrivals` | Total international visitor arrivals that month | `BASE_FEATURES` |
| `is_deepavali` | `1` when Deepavali falls in that month. see [Methodology](#methodology) | only IHC |
| `is_closed` | `1` when reported visitorship is zero, `0` otherwise. SingStat sometimes reports closed months as `"-"`, which is imputed with 0 visitors | `BASE_FEATURES` |


<br>

### Pipeline
#### Preprocessing
- The first 12 months of every museum's history are dropped, since their lag features cannot be filled.
- Historical visitorship data is split into a chronological `80/20` train-test split.
- Months with `"-"`/`NA` visitorship (when museums were closed *after their first month of operation onwards) are kept and imputed with `0` where necessary, and `is_closed` is set to `1` 
    - Museums that opened later (currently only TPM) do not get 0s appended to fill the front of the training window


#### Model Training
- Models are trained on the 80% training set
- Models which include hyperparameter tuning are validated on a held out portion of the training set through 50 Optuna trials
    - For `hw`, `sarimax` and `svr`, a single trailing 10-month holdout is used for validation
    - For `rf` and `xgb`, `TimeSeriesSplit(n_splits=3)` is used to average out RMSE across the 3 folds
    - All five Optuna objective functions minimise RMSE.
- Models are evaluated on the 20% held out test set to calculate evaluation metrics e.g. RMSE, MAPE
- Tuned hyperparameters are reused to refit the final prediction models using the full 100% historical series.


#### Forecasting
- All surviving models are used to produce a forecast, and their predictions are output in order of their evaluation performance (best first)
- Museums whose data ends before the configured window (e.g. MHC being closed from 30 Oct 2022 - 25 April 2026) are padded with zero-visitor months, so every museum forecasts the same `h` months from the same starting point.
- A `h=24` months future frame is built to facilitate predictions for each model. Known future features like `sin_month`, `cos_month` are filled in. lag feature values for the 1st forecasted year are filled in from the end of the training data where known.
- COVID months (defined in `config.py`) were excluded from the calculation of historical monthly averages (for the `monthly_avg` feature)
    - Including them dragged the averages ~14–34% below current levels and tended to make the models underpredict future visitorship
- Musuems are assumbed to be open throughout the forecast period, so `is_closed` is set to `0` for all `h` months
- Unknown future feature values like lag features and `intl_arrivals` are imputed from full training period historical monthly means. Similarly, the defined COVID period is excluded from these calculations to prevent underrepresenting future feature values and underpredicting future museum visitorship.

<br>

## Outputs


<br>

## Results


<br>

## Limitations
add: remember to update deepavali.csv manually

<br>

## Roadmap


