# Museum Visitorship Forecasting
Last updated on *6 Nov 2026* (results from the `feature/more-event-features` run on 6 Nov 2026)

## Overview
Forecasts monthly visitorship for five National Heritage Board (NHB) museums up to `h` months ahead of training data. The forecasts are meant to serve as an additional reference point during workplan target setting.

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

Both series are fetched by `src/data/singstat_api.py`. If the saved files in `data/raw/` already cover the configured window and contain every selected museum, they are reused (only the rows inside the window are used, and the files themselves are left untouched) and no API call is made; pass `--refresh` to force a fresh fetch. As SingStat publishes a few months late, a fresh fetch that still does not cover the window stops the run rather than padding the missing months. The run also stops, naming the month, if any series it uses has more than one row for the same month.

Two flags change where the data comes from:
- `--call-singstat-api` downloads both series into `data/raw/` and exits, without running the pipeline
- `--manual-data VISITORS_CSV INTL_ARRIVALS_CSV` runs on those two files only and never calls the API. Give the visitorship file first and the arrivals file second, e.g. `python main.py --manual-data data/manual/museum_ts.csv data/manual/intl_arrivals.csv`. They must be in the same format as the `data/raw/` files and cover the whole window, and are trimmed to it the same way

The requested window is set by `START_YEAR`/`START_MONTH` and `END_YEAR`/`END_MONTH` in `config.py` (monthly). Raw responses are written to `data/raw/museum_ts.csv` and `data/raw/intl_arrivals.csv` for reference.


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

> **If `Activate.ps1` fails with "running scripts is disabled on this system"**, it's because PowerShell won't run `.ps1` script files by default as a safety measure against downloaded scripts running silently. Run the following command to allow scripts **you created locally** to be run (You only need to do this once, and scripts downloaded from the internet still need a trusted digital signature, or they stay blocked):
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

bash/zsh (Mac/Linux)
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

bash/zsh (Mac/Linux)
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
`python main.py` trains 7 models each for 5 museums

Run `python main.py --help` to see the available flag arguments

```
usage: python main.py [-h] [--museum MUSEUM_CODE [MUSEUM_CODE ...]]
                      [--models MODEL [MODEL ...]] [--regen-outputs]
                      [--refresh | --call-singstat-api | --manual-data VISITORS_CSV INTL_ARRIVALS_CSV]

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
  --regen-outputs       Skip all model training and rebuild the plots and summary reports from the last run's saved predictions.
                        Reads data/processed/ and the per-model prediction CSVs already under outputs/, so no data is fetched and nothing is refitted.
                        
  --refresh, -r         Re-fetch both series from the SingStat API even if the files in data/raw/ already cover the configured window.
                        Omit to reuse the saved files where they do, which skips the API call entirely.
                        
  --call-singstat-api   Download both series from the SingStat API into data/raw/, then exit without running the pipeline.
                        
  --manual-data VISITORS_CSV INTL_ARRIVALS_CSV
                        Run on these two files only, instead of data/raw/ (the SingStat API is not called).
                        Same format as data/raw/museum_ts.csv and data/raw/intl_arrivals.csv, covering the whole window in config.py,
                        e.g. python main.py --manual-data data/manual/museum_ts.csv data/manual/intl_arrivals.csv
```

<br>

## Project Structure
```
visitor_forecast/
├── main.py                   # Entry point: check or fetch data, then run the pipeline per museum
├── config.py                 # Museums, date range, horizon, feature sets, model keys
├── requirements.txt
├── notebooks/
│   └── 01_eda.ipynb          # Exploratory data analysis
├── scripts/
│   ├── examine_deepavali.py               # Reports the best model's Deepavali-month accuracy for IHC
│   ├── generate_permutation_importances.py  # Rebuilds importance reports from CSVs on disk
│   ├── generate_tuning_report.py          # Rebuilds the tuning report from the saved Optuna studies
│   └── testing/              # One-off scripts used to probe the SingStat API's limits
├── src/
│   ├── cli.py                # Argument parsing, museum-code and model-key validation
│   ├── pipeline.py           # Per-museum orchestration: evaluate, rank, forecast, report
│   ├── analysis/
│   │   ├── artifacts.py      # Saves each fitted model to outputs/models/{CODE}/
│   │   ├── deepavali.py      # IHC Deepavali-month actual vs predicted report
│   │   ├── importance.py     # Permutation importance on the eval test set
│   │   ├── tuning.py         # Persists each Optuna study to outputs/tuning/
│   │   └── tuning_report.py  # Summarises every saved study into outputs/tuning_report.md
│   ├── data/
│   │   ├── raw_data.py       # Loads data/raw/ (or --manual-data files) when it covers the window, else calls the API
│   │   └── singstat_api.py   # SingStat TableBuilder client (request chunking, throttling)
│   ├── features/
│   │   └── data_prep.py      # Feature engineering, train/test preparation, imputation
│   ├── events/
│   │   ├── event_range.py    # Loader for dated event occurrences
│   │   ├── event_ranges/     # One CSV per event, one row per occurrence (deepavali.csv is used for IHC; national_day.csv and singapore_night_festival.csv are built into features but switched off)
│   │   ├── month_range.py    # Loader for fixed-calendar events
│   │   └── month_ranges.csv  # Events that fall in the same month every year
│   ├── models/               # The eight forecasting models, plus model_registry.py and fitted.py
│   └── visualisation/
│       ├── timeplot.py       # Evaluation and forecast plots
│       ├── jj_new_plots.py   # Seaborn versions of the evaluation and forecast plots
│       ├── summary.py        # Financial-year totals and the summary reports
│       ├── feature_report.py # Turns permutation-importance CSVs into a markdown report
│       └── eda.py            # Plotting helpers used only by the notebook
├── data/                     # Generated at runtime
│   ├── raw/                  # Raw API responses
│   └── processed/            # Engineered features per museum
└── outputs/                  # Generated at runtime, one folder per museum
    ├── models/               # Fitted model artifacts per museum (gitignored)
    └── tuning/               # Saved Optuna studies (gitignored)
```

<br>

## Configuration
### `config.py`

| Setting | Controls |
| --- | --- |
| `MUSEUM_CODES` | Which museums to forecast. Keys must match the SingStat series name exactly; the codes can be configured and are used in CLI flags, output folders and filenames. |
| `START_YEAR`/`START_MONTH`, `END_YEAR`/`END_MONTH` | The historical window requested from SingStat for training, e.g. Jan 2014 - Mar 2026 |
| `COVID_START`, `COVID_END` | The period flagged by `is_covid`, and excluded when computing historical monthly averages. |
| `h` | Forecast horizon in months (default 24). Forecasting starts the month after `END_YEAR`/`END_MONTH`. |
| `TEST_MONTHS` | Length of the evaluation test set: the last `TEST_MONTHS` months of the window, the same for every museum. Each museum must still have more than 36 training months, or the run stops. |
| `MODEL_KEYS` | Which models run, and in what order. Must match the keys in `src/models/model_registry.py`. |
| `MODEL_NAMES` | The display name each model key reports itself as in the output tables. |
| `BASE_FEATURES` | The feature set every museum's tabular models train on. |
| `MUSEUM_FEATURES` | Per-museum overrides of that feature set. The ACM, NMS and TPM entries (National Day and Night Festival features) are commented out; uncomment them to switch those features on. |


<!--
<br>

### `.env`
- For environment variables (currently not yet implemented)
-->


<br>

## Methodology
### Models Trained
| Key | Model | Sees | Tuned |
| --- | --- | --- | --- |
| `baseline` | Calendar-month mean of the last 36 months | history only | — |
| `hw` | Holt-Winters exponential smoothing, 12-month seasonality | history only | Optuna |
| `sarimax` | SARIMAX, orders `(p,d,q)(P,D,Q,12)` searched, features as standardised regressors, stationarity and invertibility enforced | full feature set | Optuna |
| `rf` | Random Forest | full feature set | Optuna |
| `xgb` | XGBoost | full feature set | Optuna |
| `svr` | Support Vector Regression, kernel searched (`linear`/`rbf`/`poly`), features standardised | full feature set | Optuna |
| `lstm` | Two stacked LSTM layers (50 units) → Dense(25) → Dense(1), 12-month input window, 50 epochs. Scalers are fitted on training data only | `value` plus every non-lag feature, as per-timestep channels | — |

Note: `timegpt` is not implemented yet


<br>

### Features
The target column is `value`, which represents monthly museum visitorship (in thousands).

`BASE_FEATURES` includes all the features most multivariate models take.

| Feature | Description | Used in |
| --- | --- | --- |
| `sin_month`, `cos_month` | Cyclical encoding of the calendar month, so December and January sit next to each other | `BASE_FEATURES` |
| `monthly_avg` | Mean visitorship for that calendar month. Computed on training data only, with COVID and closed months excluded | `BASE_FEATURES` |
| `lag_1` … `lag_12` (12 features) | Visitorship in the time periods 1 to 12 months earlier | `BASE_FEATURES` (except LSTM) |
| `is_covid` | `1` for months inside `COVID_START`–`COVID_END`. `0` otherwise. | `BASE_FEATURES` |
| `intl_arrivals` | Total international visitor arrivals that month | `BASE_FEATURES` |
| `is_closed` | `1` when reported visitorship is zero, `0` otherwise. SingStat sometimes reports closed months as `"-"`, which is imputed with 0 visitors | `BASE_FEATURES` |
| `is_deepavali` | `1` when Deepavali falls in that month, from `src/events/event_ranges/deepavali.csv`. 2020 and 2021 are left out of that file, as IHC was affected by COVID in both years | only IHC |
| `is_post_deepavali` | `1` in the month right after each Deepavali month in `deepavali.csv`, `0` otherwise | only IHC |
| `prev_deepavali_value` | On Deepavali months, visitorship at the most recent Deepavali month that was actually observed; `0` on every other month. Test and forecast months carry the last Deepavali value in their training data, since later ones would not be known yet | only IHC |
| `is_nat_day_oh`, `post_nat_day_oh`, `prev_nat_day_oh_value` | The same three features for the National Day open house each August, from `national_day.csv`. 2020 and 2021 are left out of that file, as COVID affected both years | ACM, NMS (switched off) |
| `is_snf`, `post_snf`, `prev_snf_value` | The same three features for the Singapore Night Festival each August, from `singapore_night_festival.csv`. Aug 2019 and Aug 2022 are left out, as TPM was closed then (2020 and 2021 had no festival) | TPM (switched off) |


<br>

### Pipeline
#### Preprocessing
- Each museum's rows are sorted oldest first before lag features and the split are built, so the order of the input files does not matter.
- The first 12 months of every museum's history are dropped, since their lag features cannot be filled.
- Historical visitorship data is split chronologically: the last `TEST_MONTHS` months form the test set and everything before them the training set, so every museum is tested on the same months.
- Months with `"-"`/`NA` visitorship (when museums were closed after their first month of operation onwards) are kept and imputed with `0` where necessary, and `is_closed` is set to `1` 
    - Museums that opened later (currently only IHC, whose first month is May 2015) do not get 0s appended to fill the front of the training window


#### Model Training
- Models are trained on the training set
- Models which include hyperparameter tuning are validated on held out portions of the training set through `N_TRIALS` Optuna trials (set in `config.py`)
    - All five tuned models (`hw`, `sarimax`, `svr`, `rf` and `xgb`) use the same rolling-origin validation: `TimeSeriesSplit(n_splits=3, test_size=12)`, averaging RMSE across the 3 folds
    - Each fold validates a full 12-month season, so no calendar month is over- or under-represented in the score
    - All five Optuna objective functions minimise RMSE.
    - Every study is saved to `outputs/tuning/`, and summarised across all museums in `outputs/tuning_report.md`
- Models are evaluated on the held out `TEST_MONTHS` test set to calculate evaluation metrics e.g. RMSE, MAPE
- Tuned hyperparameters are reused to refit the final prediction models using the full 100% historical series.


#### Forecasting
- All surviving models are used to produce a forecast, and their predictions are output in order of their evaluation performance (best first)
- Museums whose data ends before the configured window (e.g. MHC, whose SingStat series stopped during its Nov 2022 – Apr 2026 closure) are padded with zero-visitor months, so every museum forecasts the same `h` months from the same starting point.
- An `h`-month future frame is built to facilitate predictions for each model. Known future features like `sin_month`, `cos_month` and the Deepavali flags are filled in. Lag feature values for the 1st forecasted year are filled in from the end of the training data where known.
- COVID months (defined in `config.py`) and months where the museum was closed were excluded from the calculation of historical monthly averages (for the `monthly_avg` feature)
    - Including them dragged the averages ~14–34% below current levels and tended to make the models underpredict future visitorship
- Museums are assumed to be open throughout the forecast period, so `is_closed` is set to `0` for all `h` months
- Unknown future feature values like lag features and `intl_arrivals` are filled in from full training period historical monthly means. Similarly, the defined COVID period is excluded from these calculations to prevent underrepresenting future feature values and underpredicting future museum visitorship.

<br>

## Outputs
Each run writes SingStat API data to `data/raw/` whenever the API is called, and writes one folder per museum (with its own museum code, `CODE`) under `outputs/`. Before each model runs, its outputs from any previous run are deleted, so a model that fails leaves no stale files behind.

```
outputs/{CODE}/
├── {CODE}_summary.txt                          # Plain-text report (see below)
├── {CODE}_summary.md                           # The same report in markdown, with the key plots embedded
├── {CODE}_model_eval.csv                       # Institution, Model, RMSE, MAPE (lowest-RMSE first)
├── {CODE}_permutation_importances.md           # Per-model feature importances, ranked by model RMSE
├── {CODE}_deepavali.md                         # IHC only: best model's Deepavali-month actual vs predicted
├── eval/
│   ├── {CODE}_eval_{model}_timeplot.png        # Test-period fit, one per model
│   ├── {CODE}_{model}_predictions.csv          # Institution, Model, Year, Month, Actual, Prediction
│   └── jj-new-eval-plots/                      # Seaborn versions of the test-period plots
└── predict/
    ├── {CODE}_predict_{model}_timeplot.png     # Forecast, one per model
    ├── {CODE}_predict_top3_timeplot.png        # Top 3 models by RMSE, overlaid
    ├── {CODE}_{model}_predictions.csv          # Institution, Model, Year, Month, Prediction
    └── jj-new-predict-plots/                   # Seaborn versions of the forecast plots
```

Across all museums, each run also writes:

```
outputs/
├── tuning_report.md                            # Every Optuna study: trials (and how many completed), best RMSE, when it was found, chosen values and parameter importance
├── tuning/{CODE}_{model}.db                    # The saved Optuna studies (gitignored)
└── models/{CODE}/                              # Fitted models and raw permutation importances (gitignored)
    ├── {model}.joblib                          # rf, xgb, svr, hw
    ├── sarimax.pkl
    ├── lstm.keras
    └── permutation_importance.csv
```


### `{CODE}_summary.txt`

The main pipeline results summary for each museum. It opens with the branch, the time it was generated and the run's settings from `config.py`, followed by two tables:

| Table | Contents |
| --- | --- |
| **1. Model Evaluation Results + Predictions** | Every model's RMSE and MAPE on the test period, ranked lowest-RMSE-first, alongside its own FY forecast totals |
| **2. Total Visitors by Financial Year** | Historical actuals and the winning model's forecast in one column. |

`{CODE}_summary.md` holds the same tables, with the winning model's test-period plot and the top-3 forecast plot embedded. For IHC, it also includes the Deepavali-month table.


<br>

## Results

From the `feature/more-event-features` run on 6 Nov 2026. It matches the `test/run-pipelines-8c` run (16 Sep 2026) except for:
- the LSTM, which varies between runs
- the SARIMAX forecasts, as SingStat has since revised Feb 2026 international arrivals (see [Limitations](#limitations))
- IHC, now tested on the same last `TEST_MONTHS` months as the other museums (Jan 2024 – Mar 2026, previously Apr 2024 – Mar 2026). Retuning on its shorter training set chose a different SARIMAX order, so SVR now wins

### Model Performance
| Museum | Winning model | RMSE | MAPE | Decrease in RMSE vs `baseline` |
| --- | --- | --- | --- | --- |
| ACM | Random Forest | 7.13 | 13.99% | −55% |
| NMS | XGBoost | 16.34 | 17.40% | −55% |
| TPM | SARIMAX | 2.93 | 17.26% | −71% |
| IHC | SVR | 4.74 | 26.42% | −51% |
| MHC | LSTM | 1.70 | * | −79% |

* For MHC, all models' MAPEs exploded during evaluation as this run's held out test set falls entirely within its closure from Nov 2022, where visitorship was 0 (See [Limitations](#limitations))

* RMSE is in thousands of visitors and is **not comparable across museums**: TPM's 2.93 and NMS's 16.34 mostly reflect that NMS is roughly six times larger. Use MAPE for cross-museum comparison.

### Model Forecasts
From each museum's winning model. FY runs April–March. FY total visitorship is reported **in thousands**.

| Museum | FY2025 (actual) | FY2026 ('000s) | FY2027 ('000s) |
| --- | --- | --- | --- |
| ACM | 529.9 | 495.4 | 482.7 |
| NMS | 1,056.5 | 1,042.5 | 1,007.5 |
| TPM | 167.6 | 146.7 | 167.5 |
| IHC | 218.2 | 210.2 | 210.5 |
| MHC | 0.0 (closed) | 519.9 | 704.9 |

By museum,

#### ACM

<table>
  <thead>
    <tr><th>Model</th><th>RMSE</th><th>MAPE</th><th>FY2026 ('000s)</th><th>FY2027 ('000s)</th></tr>
  </thead>
  <tbody>
    <tr><td><b>Random Forest Regressor</b></td><td>7.13</td><td>13.99%</td><td>495.4</td><td>482.7</td></tr>
    <tr><td>Support Vector Regression</td><td>7.31</td><td>14.44%</td><td>475.1</td><td>472.6</td></tr>
    <tr><td>XGBoost</td><td>7.75</td><td>14.25%</td><td>491.3</td><td>492.9</td></tr>
    <tr><td>LSTM</td><td>9.62</td><td>23.47%</td><td>470.8</td><td>460.5</td></tr>
    <tr><td>SARIMAX</td><td>9.91</td><td>21.02%</td><td>638.3</td><td>739.6</td></tr>
    <tr><td>Holt-Winters exponential smoothing</td><td>10.10</td><td>16.85%</td><td>713.9</td><td>837.8</td></tr>
    <tr><td>Baseline Monthly Mean</td><td>15.85</td><td>30.54%</td><td>452.0</td><td>452.0</td></tr>
  </tbody>
</table>

#### NMS

<table>
  <thead>
    <tr><th>Model</th><th>RMSE</th><th>MAPE</th><th>FY2026 ('000s)</th><th>FY2027 ('000s)</th></tr>
  </thead>
  <tbody>
    <tr><td><b>XGBoost</b></td><td>16.34</td><td>17.40%</td><td>1,042.5</td><td>1,007.5</td></tr>
    <tr><td>Support Vector Regression</td><td>19.61</td><td>14.77%</td><td>904.8</td><td>912.3</td></tr>
    <tr><td>SARIMAX</td><td>20.07</td><td>20.48%</td><td>1,006.4</td><td>1,028.7</td></tr>
    <tr><td>Random Forest Regressor</td><td>21.68</td><td>18.90%</td><td>1,030.7</td><td>977.9</td></tr>
    <tr><td>LSTM</td><td>23.26</td><td>17.97%</td><td>930.7</td><td>931.1</td></tr>
    <tr><td>Baseline Monthly Mean</td><td>36.40</td><td>30.13%</td><td>1,040.0</td><td>1,040.0</td></tr>
    <tr><td>Holt-Winters exponential smoothing</td><td>43.75</td><td>35.34%</td><td>1,275.8</td><td>1,375.8</td></tr>
  </tbody>
</table>

#### TPM

<table>
  <thead>
    <tr><th>Model</th><th>RMSE</th><th>MAPE</th><th>FY2026 ('000s)</th><th>FY2027 ('000s)</th></tr>
  </thead>
  <tbody>
    <tr><td><b>SARIMAX</b></td><td>2.93</td><td>17.26%</td><td>146.7</td><td>167.5</td></tr>
    <tr><td>XGBoost</td><td>3.29</td><td>22.28%</td><td>194.9</td><td>209.1</td></tr>
    <tr><td>Support Vector Regression</td><td>3.72</td><td>19.80%</td><td>244.5</td><td>312.9</td></tr>
    <tr><td>Random Forest Regressor</td><td>4.06</td><td>21.44%</td><td>218.1</td><td>237.8</td></tr>
    <tr><td>LSTM</td><td>7.15</td><td>46.13%</td><td>251.5</td><td>285.5</td></tr>
    <tr><td>Baseline Monthly Mean</td><td>10.17</td><td>68.14%</td><td>170.1</td><td>170.1</td></tr>
    <tr><td>Holt-Winters exponential smoothing</td><td>12.93</td><td>88.56%</td><td>166.6</td><td>171.6</td></tr>
  </tbody>
</table>

#### IHC

<table>
  <thead>
    <tr><th>Model</th><th>RMSE</th><th>MAPE</th><th>FY2026 ('000s)</th><th>FY2027 ('000s)</th></tr>
  </thead>
  <tbody>
    <tr><td><b>Support Vector Regression</b></td><td>4.74</td><td>26.42%</td><td>210.2</td><td>210.5</td></tr>
    <tr><td>SARIMAX</td><td>5.04</td><td>25.52%</td><td>212.2</td><td>215.5</td></tr>
    <tr><td>XGBoost</td><td>5.07</td><td>23.85%</td><td>220.1</td><td>212.5</td></tr>
    <tr><td>Random Forest Regressor</td><td>6.33</td><td>27.75%</td><td>211.1</td><td>210.3</td></tr>
    <tr><td>Holt-Winters exponential smoothing</td><td>6.38</td><td>25.60%</td><td>228.6</td><td>239.5</td></tr>
    <tr><td>LSTM</td><td>6.52</td><td>35.48%</td><td>234.5</td><td>221.7</td></tr>
    <tr><td>Baseline Monthly Mean</td><td>9.77</td><td>40.23%</td><td>216.6</td><td>216.6</td></tr>
  </tbody>
</table>

Deepavali months for the winning model (SVR). A negative difference means the model under-predicted.

| Month | Actual | Predicted | Difference | % difference |
| --- | --- | --- | --- | --- |
| 2024-10 | 43.90 | 30.62 | -13.28 | -30.26% |
| 2025-10 | 38.30 | 33.50 | -4.80 | -12.54% |
| 2026-11 | -- | 31.56 | -- | -- |
| 2027-10 | -- | 40.01 | -- | -- |

#### MHC

<table>
  <thead>
    <tr><th>Model</th><th>RMSE</th><th>MAPE</th><th>FY2026 ('000s)</th><th>FY2027 ('000s)</th></tr>
  </thead>
  <tbody>
    <tr><td><b>LSTM</b></td><td>1.70</td><td>n/a</td><td>519.9</td><td>704.9</td></tr>
    <tr><td>Support Vector Regression</td><td>3.75</td><td>n/a</td><td>535.2</td><td>632.5</td></tr>
    <tr><td>XGBoost</td><td>4.56</td><td>n/a</td><td>532.2</td><td>648.4</td></tr>
    <tr><td>Random Forest Regressor</td><td>4.66</td><td>n/a</td><td>433.4</td><td>631.1</td></tr>
    <tr><td>Holt-Winters exponential smoothing</td><td>4.92</td><td>n/a</td><td>-19.9</td><td>-61.3</td></tr>
    <tr><td>SARIMAX</td><td>5.50</td><td>n/a</td><td>340.0</td><td>339.1</td></tr>
    <tr><td>Baseline Monthly Mean</td><td>8.26</td><td>n/a</td><td>0.0</td><td>0.0</td></tr>
  </tbody>
</table>

Holt-Winters forecasts negative visitorship for MHC, as nothing in the pipeline clips forecasts at zero.



See `outputs/{MUSEUM_CODE}` for full results

<br>

## Limitations
#### Year 2's forecast is a flattened seasonal baseline
- As the prediction period's unknown lag features and `intl_arrivals` are filled in with historical full training period monthly means (excluding COVID from the calculations), the 2nd forecast year is made up entirely of filled-in lag features and `intl_arrivals` and will thus lead to a repeating seasonal trend (for models RF, XGBoost, SVR and LSTM)

#### Some museums have long closed periods with no visitors
- Some museums were not open throughout the configured window:
    - IHC only opened in May 2015
    - TPM was closed for redevelopment from Apr 2019 to Jan 2023, reopening Feb 2023
    - MHC was closed from Nov 2022 until it reopened on 25 Apr 2026
- For MHC, evaluation MAPE explodes while its test set falls entirely within its closure period

#### SingStat revises recent months after publishing
- SingStat sometimes revises recently published figures. Feb 2026 international arrivals went from 1,500,996 (used in the 8c run) to 1,500,997, which moved TPM's SARIMAX forecast from 154.0 to 146.7 ('000s, FY2026)
- To reproduce a past run exactly, run it on that run's committed `data/raw/` files rather than a fresh fetch

#### Manual maintenance of input files
- `deepavali.csv`, which contains the specific months each year when Deepavali occurs AND IHC organises a Deepavali open house (it hovers between Oct and Nov) must be extended manually. The Singaporean government only gazettes official Deepavali holiday dates 1.5-2 years in advance
    - 2020 and 2021, when no open house was held due to COVID, are deliberately left out of `deepavali.csv`, so they must not be added back when extending it


<br>

## Roadmap
- Implement TimeGPT models, .env for storing TimeGPT API keys
- Adjust MHC's training window such that test set isn't completely 0
- Trim the lag feature set to remove useless lag features
