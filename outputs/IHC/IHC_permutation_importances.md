# [IHC] Permutation Importances

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
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>lags</code></td><td style="text-align:left;padding:4px 10px;"><code>lag_1</code>, <code>lag_2</code>, <code>lag_3</code>, <code>lag_4</code>, <code>lag_5</code>, <code>lag_6</code>, <code>lag_7</code>, <code>lag_8</code>, <code>lag_9</code>, <code>lag_10</code>, <code>lag_11</code>, <code>lag_12</code></td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>calendar</code></td><td style="text-align:left;padding:4px 10px;"><code>cos_month</code>, <code>sin_month</code></td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>seasonal_level</code></td><td style="text-align:left;padding:4px 10px;"><code>monthly_avg</code></td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>regime_flags</code></td><td style="text-align:left;padding:4px 10px;"><code>is_covid</code></td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>events</code></td><td style="text-align:left;padding:4px 10px;"><code>is_deepavali</code></td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>exogenous</code></td><td style="text-align:left;padding:4px 10px;"><code>intl_arrivals</code></td></tr></tbody>
</table>

## Models

Ordered by eval RMSE, best first.


### LSTM

|  |  |
|---|---|
| RMSE | 6.17 |
| MAPE | 38.02% |

Not scored: this model reads no feature columns, so there is nothing to permute.


### Holt-Winters exponential smoothing

|  |  |
|---|---|
| RMSE | 6.19 |
| MAPE | 35.66% |

Not scored: this model reads no feature columns, so there is nothing to permute.


### XGBoost

|  |  |
|---|---|
| RMSE | 6.52 |
| MAPE | 30.11% |

**By feature group**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>seasonal_level</code></td><td style="text-align:right;padding:4px 10px;">1.18</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>events</code></td><td style="text-align:right;padding:4px 10px;">0.39</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>calendar</code></td><td style="text-align:right;padding:4px 10px;">0.36</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>exogenous</code></td><td style="text-align:right;padding:4px 10px;">0.25</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>regime_flags</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lags</code></td><td style="text-align:right;padding:4px 10px;">-0.05</td></tr></tbody>
</table>

**By individual feature**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>monthly_avg</code></td><td style="text-align:right;padding:4px 10px;">2.08</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_3</code></td><td style="text-align:right;padding:4px 10px;">0.42</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>is_deepavali</code></td><td style="text-align:right;padding:4px 10px;">0.39</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_6</code></td><td style="text-align:right;padding:4px 10px;">0.30</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>cos_month</code></td><td style="text-align:right;padding:4px 10px;">0.17</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>sin_month</code></td><td style="text-align:right;padding:4px 10px;">0.16</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>intl_arrivals</code></td><td style="text-align:right;padding:4px 10px;">0.16</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_12</code></td><td style="text-align:right;padding:4px 10px;">0.07</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>is_covid</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_9</code></td><td style="text-align:right;padding:4px 10px;">-0.02</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_5</code></td><td style="text-align:right;padding:4px 10px;">-0.03</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_10</code></td><td style="text-align:right;padding:4px 10px;">-0.07</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_8</code></td><td style="text-align:right;padding:4px 10px;">-0.11</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_11</code></td><td style="text-align:right;padding:4px 10px;">-0.19</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_1</code></td><td style="text-align:right;padding:4px 10px;">-0.20</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_7</code></td><td style="text-align:right;padding:4px 10px;">-0.22</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_4</code></td><td style="text-align:right;padding:4px 10px;">-0.31</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_2</code></td><td style="text-align:right;padding:4px 10px;">-0.38</td></tr></tbody>
</table>

### Random Forest Regressor

|  |  |
|---|---|
| RMSE | 6.54 |
| MAPE | 30.15% |

**By feature group**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>seasonal_level</code></td><td style="text-align:right;padding:4px 10px;">1.63</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lags</code></td><td style="text-align:right;padding:4px 10px;">0.38</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>exogenous</code></td><td style="text-align:right;padding:4px 10px;">0.07</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>calendar</code></td><td style="text-align:right;padding:4px 10px;">0.04</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>regime_flags</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>events</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr></tbody>
</table>

**By individual feature**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>monthly_avg</code></td><td style="text-align:right;padding:4px 10px;">2.43</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_6</code></td><td style="text-align:right;padding:4px 10px;">0.22</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_3</code></td><td style="text-align:right;padding:4px 10px;">0.21</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>intl_arrivals</code></td><td style="text-align:right;padding:4px 10px;">0.06</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>cos_month</code></td><td style="text-align:right;padding:4px 10px;">0.04</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_1</code></td><td style="text-align:right;padding:4px 10px;">0.03</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_12</code></td><td style="text-align:right;padding:4px 10px;">0.02</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_5</code></td><td style="text-align:right;padding:4px 10px;">0.02</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_9</code></td><td style="text-align:right;padding:4px 10px;">0.02</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>sin_month</code></td><td style="text-align:right;padding:4px 10px;">0.01</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_11</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_2</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>is_deepavali</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>is_covid</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_8</code></td><td style="text-align:right;padding:4px 10px;">-0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_4</code></td><td style="text-align:right;padding:4px 10px;">-0.02</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_10</code></td><td style="text-align:right;padding:4px 10px;">-0.03</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_7</code></td><td style="text-align:right;padding:4px 10px;">-0.06</td></tr></tbody>
</table>

### Support Vector Regression

|  |  |
|---|---|
| RMSE | 6.63 |
| MAPE | 32.93% |

**By feature group**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>seasonal_level</code></td><td style="text-align:right;padding:4px 10px;">1.19</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>events</code></td><td style="text-align:right;padding:4px 10px;">0.68</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>exogenous</code></td><td style="text-align:right;padding:4px 10px;">0.20</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lags</code></td><td style="text-align:right;padding:4px 10px;">0.06</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>calendar</code></td><td style="text-align:right;padding:4px 10px;">0.02</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>regime_flags</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr></tbody>
</table>

**By individual feature**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>monthly_avg</code></td><td style="text-align:right;padding:4px 10px;">1.71</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>is_deepavali</code></td><td style="text-align:right;padding:4px 10px;">0.66</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_3</code></td><td style="text-align:right;padding:4px 10px;">0.49</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_4</code></td><td style="text-align:right;padding:4px 10px;">0.20</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>intl_arrivals</code></td><td style="text-align:right;padding:4px 10px;">0.12</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_6</code></td><td style="text-align:right;padding:4px 10px;">0.10</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_12</code></td><td style="text-align:right;padding:4px 10px;">0.07</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_7</code></td><td style="text-align:right;padding:4px 10px;">0.04</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>cos_month</code></td><td style="text-align:right;padding:4px 10px;">0.02</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_5</code></td><td style="text-align:right;padding:4px 10px;">0.01</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_2</code></td><td style="text-align:right;padding:4px 10px;">0.01</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>sin_month</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>is_covid</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_8</code></td><td style="text-align:right;padding:4px 10px;">-0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_1</code></td><td style="text-align:right;padding:4px 10px;">-0.09</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_11</code></td><td style="text-align:right;padding:4px 10px;">-0.10</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_10</code></td><td style="text-align:right;padding:4px 10px;">-0.13</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_9</code></td><td style="text-align:right;padding:4px 10px;">-0.19</td></tr></tbody>
</table>

### SARIMAX

|  |  |
|---|---|
| RMSE | 8.69 |
| MAPE | 33.77% |

**By feature group**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>lags</code></td><td style="text-align:right;padding:4px 10px;">1.15</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>events</code></td><td style="text-align:right;padding:4px 10px;">1.10</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>exogenous</code></td><td style="text-align:right;padding:4px 10px;">0.21</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>seasonal_level</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>calendar</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>regime_flags</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr></tbody>
</table>

**By individual feature**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>is_deepavali</code></td><td style="text-align:right;padding:4px 10px;">1.08</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_2</code></td><td style="text-align:right;padding:4px 10px;">0.46</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_4</code></td><td style="text-align:right;padding:4px 10px;">0.27</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_10</code></td><td style="text-align:right;padding:4px 10px;">0.24</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>intl_arrivals</code></td><td style="text-align:right;padding:4px 10px;">0.19</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_9</code></td><td style="text-align:right;padding:4px 10px;">0.11</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_8</code></td><td style="text-align:right;padding:4px 10px;">0.10</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_3</code></td><td style="text-align:right;padding:4px 10px;">0.08</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_5</code></td><td style="text-align:right;padding:4px 10px;">0.07</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_1</code></td><td style="text-align:right;padding:4px 10px;">0.06</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_6</code></td><td style="text-align:right;padding:4px 10px;">0.01</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>monthly_avg</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>cos_month</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>is_covid</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>sin_month</code></td><td style="text-align:right;padding:4px 10px;">-0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_11</code></td><td style="text-align:right;padding:4px 10px;">-0.02</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_7</code></td><td style="text-align:right;padding:4px 10px;">-0.07</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_12</code></td><td style="text-align:right;padding:4px 10px;">-0.30</td></tr></tbody>
</table>

### Baseline Monthly Mean

|  |  |
|---|---|
| RMSE | 8.79 |
| MAPE | 33.24% |

Not scored: this model reads no feature columns, so there is nothing to permute.

