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


<br>

## Project Structure


<br>

## Configuration


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


