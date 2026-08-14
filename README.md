# Museum Visitorship Forecasting

add: remember to update deepavali.csv manually

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


<br>

## Outputs


<br>

## Results


<br>

## Limitations


<br>

## Roadmap


