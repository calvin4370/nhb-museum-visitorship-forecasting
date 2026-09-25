# Museum Visitorship Forecasting
Last updated on *14 Aug 2026* (after adding `is_closed` feature)

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

> **If `Activate.ps1` fails with "running scripts is disabled on this system"**, it's because PowerShell won't run `.ps1` script files by default as a safety measure against downloaded scripts running silently. Run the following command to allow scripts **you created locally* to be run (You only need to do this once, and scripts downloaded from the internet still need a trusted digital signature, or they stay blocked):
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```


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
| `MUSEUM_CODES` | Which museums to forecast. Keys must match the SingStat series name exactly; the codes can be configured and are used in CLI flags, output folders and filenames. |
| `START_YEAR`/`START_MONTH`, `END_YEAR`/`END_MONTH` | The historical window requested from SingStat for training. e.g. Jan 2014 - Mar 2026|
| `COVID_START`, `COVID_END` | The period flagged by `is_covid`, and excluded when computing historical monthly averages. |
| `h` | Forecast horizon in months (default 24). Forecasting starts the month after `END_YEAR`/`END_MONTH`. |
| `MODEL_KEYS` | Which models run, and in what order. Must match the keys in `src/models/model_registry.py`. |
| `BASE_FEATURES` | The feature set every museum's tabular models train on. |
| `MUSEUM_FEATURES` | Per-museum overrides of that feature set. |

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
    - Museums that opened later (currently only IHC, whose first month is May 2015) do not get 0s appended to fill the front of the training window


#### Model Training
- Models are trained on the 80% training set
- Models which include hyperparameter tuning are validated on held out portions of the training set through 50 Optuna trials
    - All five tuned models (`hw`, `sarimax`, `svr`, `rf` and `xgb`) use the same rolling-origin validation: `TimeSeriesSplit(n_splits=3, test_size=12)`, averaging RMSE across the 3 folds
    - Each fold validates a full 12-month season, so no calendar month is over- or under-represented in the score
    - All five Optuna objective functions minimise RMSE.
- Models are evaluated on the 20% held out test set to calculate evaluation metrics e.g. RMSE, MAPE
- Tuned hyperparameters are reused to refit the final prediction models using the full 100% historical series.


#### Forecasting
- All surviving models are used to produce a forecast, and their predictions are output in order of their evaluation performance (best first)
- Museums whose data ends before the configured window (e.g. MHC being closed from 30 Oct 2022 - 25 April 2026) are padded with 0-visitor months, so every museum forecasts the same `h` months from the same starting point.
- A `h=24` months future frame is built to facilitate predictions for each model. Known future features like `sin_month`, `cos_month` are filled in. lag feature values for the 1st forecasted year are filled in from the end of the training data where known.
- COVID months (defined in `config.py`) and months where the museum was closed were excluded from the calculation of historical monthly averages (for the `monthly_avg` feature)
    - Including them dragged the averages ~14–34% below current levels and tended to make the models underpredict future visitorship
- Musuems are assumed to be open throughout the forecast period, so `is_closed` is set to `0` for all `h` months
- Unknown future feature values like lag features and `intl_arrivals` are filled in from full training period historical monthly means. Similarly, the defined COVID period is excluded from these calculations to prevent underrepresenting future feature values and underpredicting future museum visitorship.

<br>

## Outputs
Each run writes singstat API data to `data/` and writes one folder per museum (with its own museum code, `CODE`) under `outputs/`

```
outputs/{CODE}/
├── {CODE}_summary.txt                          # Human-readable report (see below)
├── {CODE}_model_eval.csv                       # Institution, Model, RMSE, MAPE (lowest-RMSE first)
├── eval/
│   └── {CODE}_eval_{model}_timeplot.png        # Test-period fit, one per model
└── predict/
    ├── {CODE}_predict_{model}_timeplot.png     # Forecast, one per model
    ├── {CODE}_predict_top3_timeplot.png        # Top 3 models by RMSE, overlaid
    └── {CODE}_{model}_predictions.csv          # Institution, Model, Year, Month, Prediction
```


### `{CODE}_summary.txt`

The main pipeline results summary for each museum. Three tables:

| Table | Contents |
| --- | --- |
| **1. Model Evaluation** | Every model's RMSE and MAPE on the test period, ranked lowest-RMSE-first |
| **2. Total Visitors by Financial Year** | Historical actuals and the winning model's forecast in one column. |
| **3. Forecast FY Totals by Model** | Every model's own FY totals alongside its RMSE and MAPE |


<br>

## Results

### Model Performance
| Museum | Winning model | RMSE | MAPE | Decrease in RMSE vs `baseline` |
| --- | --- | --- | --- | --- |
| ACM | Random Forest | 7.13 | 13.99% | −55% |
| NMS | XGBoost | 16.34 | 17.40% | −55% |
| TPM | SARIMAX | 2.93 | 17.26% | −71% |
| IHC | LSTM | 6.06 | 36.33% | −31% |
| MHC | LSTM | 2.16 | * | −74% |

* For MHC, all models' MAPEs exploded during evaluation as its held out test set is entirely included in its closure from Nov 2022 to Mar 2026, where visitorship was 0 (See [Limitations](#limitations))

* RMSE is in thousands of visitors and is **not comparable across museums**: TPM's 2.93 and NMS's 16.34 mostly reflect that NMS is roughly six times larger. Use MAPE for cross-museum comparison.

### Model Forecasts
From each museum's winning model. FY runs April–March. FY total visitorship is reported **in thousands**.

| Museum | FY2025 (actual) | FY2026 ('000s) | FY2027 ('000s) |
| --- | --- | --- | --- |
| ACM | 529.9 | 495.4 | 482.7 |
| NMS | 1,056.5 | 1,042.5 | 1,007.5 |
| IHC | 218.2 | 240.7 | 233.4 |
| TPM | 167.6 | 154.0 | 178.5 |
| MHC | 0.0 (closed) | 537.2 | 706.4 |

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
    <tr><td>LSTM</td><td>9.40</td><td>22.78%</td><td>471.4</td><td>464.9</td></tr>
    <tr><td>SARIMAX</td><td>9.91</td><td>21.02%</td><td>638.3</td><td>739.5</td></tr>
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
    <tr><td>LSTM</td><td>23.91</td><td>19.28%</td><td>930.6</td><td>925.7</td></tr>
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
    <tr><td><b>SARIMAX</b></td><td>2.93</td><td>17.26%</td><td>154.0</td><td>178.5</td></tr>
    <tr><td>XGBoost</td><td>3.29</td><td>22.28%</td><td>194.9</td><td>209.1</td></tr>
    <tr><td>Support Vector Regression</td><td>3.72</td><td>19.80%</td><td>244.5</td><td>312.9</td></tr>
    <tr><td>Random Forest Regressor</td><td>4.06</td><td>21.44%</td><td>218.1</td><td>237.8</td></tr>
    <tr><td>LSTM</td><td>7.84</td><td>52.10%</td><td>256.9</td><td>306.6</td></tr>
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
    <tr><td><b>LSTM</b></td><td>6.06</td><td>36.33%</td><td>240.7</td><td>233.4</td></tr>
    <tr><td>Holt-Winters exponential smoothing</td><td>6.19</td><td>35.66%</td><td>201.0</td><td>192.4</td></tr>
    <tr><td>Support Vector Regression</td><td>6.21</td><td>30.04%</td><td>208.5</td><td>207.6</td></tr>
    <tr><td>XGBoost</td><td>6.61</td><td>27.97%</td><td>213.3</td><td>210.3</td></tr>
    <tr><td>Random Forest Regressor</td><td>6.62</td><td>30.43%</td><td>211.1</td><td>209.9</td></tr>
    <tr><td>SARIMAX</td><td>7.88</td><td>28.75%</td><td>214.4</td><td>213.3</td></tr>
    <tr><td>Baseline Monthly Mean</td><td>8.79</td><td>33.24%</td><td>216.6</td><td>216.6</td></tr>
  </tbody>
</table>

#### MHC

<table>
  <thead>
    <tr><th>Model</th><th>RMSE</th><th>MAPE</th><th>FY2026 ('000s)</th><th>FY2027 ('000s)</th></tr>
  </thead>
  <tbody>
    <tr><td><b>LSTM</b></td><td>2.16</td><td>n/a</td><td>537.2</td><td>706.4</td></tr>
    <tr><td>Support Vector Regression</td><td>3.75</td><td>n/a</td><td>535.2</td><td>632.5</td></tr>
    <tr><td>XGBoost</td><td>4.56</td><td>n/a</td><td>532.2</td><td>648.4</td></tr>
    <tr><td>Random Forest Regressor</td><td>4.66</td><td>n/a</td><td>433.4</td><td>631.1</td></tr>
    <tr><td>Holt-Winters exponential smoothing</td><td>4.92</td><td>n/a</td><td>-19.9</td><td>-61.3</td></tr>
    <tr><td>SARIMAX</td><td>5.50</td><td>n/a</td><td>341.3</td><td>341.9</td></tr>
    <tr><td>Baseline Monthly Mean</td><td>8.26</td><td>n/a</td><td>0.0</td><td>0.0</td></tr>
  </tbody>
</table>



See `outputs/{MUSEUM_CODE}` for full results

<br>

## Limitations
#### Year 2's forecast is a flattened seasonal baseline
- As prediction period unknown lag features and `intl_arrivals` are filled in with historical full training period monthly means (excluding COVID from the calculations), the 2nd forecast year, is made up entirely of filled-in lag features and `intl_arrivals` and will thus lead to a repeating seasonal trend (for models RF, XGBoost, SVR and LSTM)

#### The 95% band on the plots is a constant, not a true prediction interval
- The band is drawn as `Forecast ± 1.96 × std(Forecast)` (`src/visualisation/timeplot.py`), so its width is a single scalar applied to every month of the horizon
<!--
- It is derived from the spread of the forecast itself, not from forecast error, so a strongly seasonal forecast gets a wide band while a flat one gets a narrow band — the opposite of how confident each actually is
- It does not widen further into the horizon, even though uncertainty grows the further ahead a forecast goes
- Nothing ties it to residuals, so it carries no coverage guarantee and should not be read as a calibrated 95% interval. SARIMAX's own `get_forecast(...).conf_int()` is available but currently unused
-->

#### Some museums have long closed periods with no visitors
- While the historical training period used is Jan 2014 to Mar 2026, some museums were not open throughout it:
    - IHC only opened in May 2015
    - TPM was closed for redevelopment from Apr 2019 to Jan 2023, reopening Feb 2023
    - MHC was closed from Nov 2022 to Mar 2026 (the end of historical data) and reopened in Apr 2026 (start of predict period)
- For MHC, evaluation MAPE is exploded as its test set falls entirely within its closure period

#### Manual maintenance of input files
- `deepavali.csv`, which contains the specific months each year when Deepavali occurs (it hovers between Oct and Nov) must be extended manually. The Singaporean government only gazettes official Deepavali holiday dates 1.5-2 years in advance


<br>

## Roadmap
- Implement TimeGPT models, .env for storing TimeGPT API keys
- Trim the lag feature set to remove useless lag features
