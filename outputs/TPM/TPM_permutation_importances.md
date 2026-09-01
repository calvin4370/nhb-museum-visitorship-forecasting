# [TPM] Permutation Importances

Permutation importance shuffles one column of the evaluation set and measures how
much worse the forecast gets. The number below is the **rise in RMSE**, in the same units as
the forecast itself (thousands of visitors), so it is comparable across models and museums.

- A **large** value means the model leans on that column: breaking it costs accuracy.
- A value near **zero** means the model barely uses it.
- A **negative** value means shuffling helped slightly, which is noise, not signal.

Scores are measured on the eval test set, the only period with actual visitor numbers to
compare against. The predict horizon has no actuals, so nothing can be scored there.

Individual columns understate their own worth when they are correlated: shuffling `lag_1`
barely hurts while `lag_2` and `monthly_avg` still carry almost the same information. The
grouped tables shuffle every column in a group at once, so the group score is the honest
measure of what that block of features contributes. A group's score is **not** the sum of its
members' scores.

## Feature groups

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Group</th><th style="text-align:left;padding:4px 10px;">Features</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>lags</code></td><td style="text-align:left;padding:4px 10px;"><code>lag_1</code>, <code>lag_2</code>, <code>lag_3</code>, <code>lag_4</code>, <code>lag_5</code>, <code>lag_6</code>, <code>lag_7</code>, <code>lag_8</code>, <code>lag_9</code>, <code>lag_10</code>, <code>lag_11</code>, <code>lag_12</code></td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>calendar</code></td><td style="text-align:left;padding:4px 10px;"><code>cos_month</code>, <code>sin_month</code></td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>seasonal_level</code></td><td style="text-align:left;padding:4px 10px;"><code>monthly_avg</code></td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>regime_flags</code></td><td style="text-align:left;padding:4px 10px;"><code>is_closed</code>, <code>is_covid</code></td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>exogenous</code></td><td style="text-align:left;padding:4px 10px;"><code>intl_arrivals</code></td></tr></tbody>
</table>

## Models

Ordered by eval RMSE, best first.


### Support Vector Regression

|  |  |
|---|---|
| RMSE | 2.43 |
| MAPE | 11.05% |

**By feature group**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>seasonal_level</code></td><td style="text-align:right;padding:4px 10px;">3.16</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>calendar</code></td><td style="text-align:right;padding:4px 10px;">1.84</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lags</code></td><td style="text-align:right;padding:4px 10px;">0.41</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>regime_flags</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>exogenous</code></td><td style="text-align:right;padding:4px 10px;">-0.06</td></tr></tbody>
</table>

**By individual feature**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>monthly_avg</code></td><td style="text-align:right;padding:4px 10px;">3.31</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>sin_month</code></td><td style="text-align:right;padding:4px 10px;">1.50</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_1</code></td><td style="text-align:right;padding:4px 10px;">0.39</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_7</code></td><td style="text-align:right;padding:4px 10px;">0.26</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>cos_month</code></td><td style="text-align:right;padding:4px 10px;">0.17</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_2</code></td><td style="text-align:right;padding:4px 10px;">0.06</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_10</code></td><td style="text-align:right;padding:4px 10px;">0.06</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_3</code></td><td style="text-align:right;padding:4px 10px;">0.06</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_8</code></td><td style="text-align:right;padding:4px 10px;">0.02</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_9</code></td><td style="text-align:right;padding:4px 10px;">0.02</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_11</code></td><td style="text-align:right;padding:4px 10px;">0.02</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_6</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>is_closed</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>is_covid</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_5</code></td><td style="text-align:right;padding:4px 10px;">-0.02</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_4</code></td><td style="text-align:right;padding:4px 10px;">-0.04</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>intl_arrivals</code></td><td style="text-align:right;padding:4px 10px;">-0.06</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_12</code></td><td style="text-align:right;padding:4px 10px;">-0.18</td></tr></tbody>
</table>

### XGBoost

|  |  |
|---|---|
| RMSE | 3.29 |
| MAPE | 22.28% |

**By feature group**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>seasonal_level</code></td><td style="text-align:right;padding:4px 10px;">1.33</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lags</code></td><td style="text-align:right;padding:4px 10px;">0.64</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>calendar</code></td><td style="text-align:right;padding:4px 10px;">0.05</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>regime_flags</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>exogenous</code></td><td style="text-align:right;padding:4px 10px;">-0.00</td></tr></tbody>
</table>

**By individual feature**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>monthly_avg</code></td><td style="text-align:right;padding:4px 10px;">1.29</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_2</code></td><td style="text-align:right;padding:4px 10px;">0.20</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_6</code></td><td style="text-align:right;padding:4px 10px;">0.17</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_4</code></td><td style="text-align:right;padding:4px 10px;">0.15</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_1</code></td><td style="text-align:right;padding:4px 10px;">0.14</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_7</code></td><td style="text-align:right;padding:4px 10px;">0.08</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>cos_month</code></td><td style="text-align:right;padding:4px 10px;">0.06</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>sin_month</code></td><td style="text-align:right;padding:4px 10px;">0.06</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_8</code></td><td style="text-align:right;padding:4px 10px;">0.03</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_9</code></td><td style="text-align:right;padding:4px 10px;">0.02</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_11</code></td><td style="text-align:right;padding:4px 10px;">0.01</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_5</code></td><td style="text-align:right;padding:4px 10px;">0.01</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>intl_arrivals</code></td><td style="text-align:right;padding:4px 10px;">0.01</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_12</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_10</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>is_closed</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>is_covid</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_3</code></td><td style="text-align:right;padding:4px 10px;">-0.00</td></tr></tbody>
</table>

### Random Forest Regressor

|  |  |
|---|---|
| RMSE | 4.06 |
| MAPE | 21.44% |

**By feature group**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>seasonal_level</code></td><td style="text-align:right;padding:4px 10px;">2.88</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lags</code></td><td style="text-align:right;padding:4px 10px;">0.55</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>calendar</code></td><td style="text-align:right;padding:4px 10px;">0.06</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>exogenous</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>regime_flags</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr></tbody>
</table>

**By individual feature**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>monthly_avg</code></td><td style="text-align:right;padding:4px 10px;">3.05</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_7</code></td><td style="text-align:right;padding:4px 10px;">0.17</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_12</code></td><td style="text-align:right;padding:4px 10px;">0.08</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>sin_month</code></td><td style="text-align:right;padding:4px 10px;">0.04</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_8</code></td><td style="text-align:right;padding:4px 10px;">0.01</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_5</code></td><td style="text-align:right;padding:4px 10px;">0.01</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>cos_month</code></td><td style="text-align:right;padding:4px 10px;">0.01</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_1</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_11</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_4</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>is_closed</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>is_covid</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_2</code></td><td style="text-align:right;padding:4px 10px;">-0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_3</code></td><td style="text-align:right;padding:4px 10px;">-0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_6</code></td><td style="text-align:right;padding:4px 10px;">-0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>intl_arrivals</code></td><td style="text-align:right;padding:4px 10px;">-0.01</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_9</code></td><td style="text-align:right;padding:4px 10px;">-0.04</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_10</code></td><td style="text-align:right;padding:4px 10px;">-0.07</td></tr></tbody>
</table>

### SARIMAX

|  |  |
|---|---|
| RMSE | 5.31 |
| MAPE | 29.97% |

**By feature group**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>exogenous</code></td><td style="text-align:right;padding:4px 10px;">0.01</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>calendar</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lags</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>regime_flags</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>seasonal_level</code></td><td style="text-align:right;padding:4px 10px;">-0.00</td></tr></tbody>
</table>

**By individual feature**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>monthly_avg</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>cos_month</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_6</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>is_covid</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>is_closed</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_1</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_2</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_3</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_4</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_5</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_8</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_9</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_10</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_11</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_12</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_7</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>sin_month</code></td><td style="text-align:right;padding:4px 10px;">-0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>intl_arrivals</code></td><td style="text-align:right;padding:4px 10px;">-0.01</td></tr></tbody>
</table>

### LSTM

|  |  |
|---|---|
| RMSE | 9.23 |
| MAPE | 63.11% |

Not scored: this model reads no feature columns, so there is nothing to permute.


### Baseline Monthly Mean

|  |  |
|---|---|
| RMSE | 10.17 |
| MAPE | 68.14% |

Not scored: this model reads no feature columns, so there is nothing to permute.


### Holt-Winters exponential smoothing

|  |  |
|---|---|
| RMSE | 12.93 |
| MAPE | 88.56% |

Not scored: this model reads no feature columns, so there is nothing to permute.

