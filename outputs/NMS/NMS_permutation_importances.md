# [NMS] Permutation Importances

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
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>lags</code></td><td style="text-align:left;padding:4px 10px;"><code>lag_1</code>, <code>lag_2</code>, <code>lag_3</code>, <code>lag_4</code>, <code>lag_5</code>, <code>lag_6</code>, <code>lag_7</code>, <code>lag_8</code>, <code>lag_9</code>, <code>lag_10</code>, <code>lag_11</code>, <code>lag_12</code></td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>calendar</code></td><td style="text-align:left;padding:4px 10px;"><code>cos_month</code>, <code>sin_month</code></td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>seasonal_level</code></td><td style="text-align:left;padding:4px 10px;"><code>monthly_avg</code></td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>regime_flags</code></td><td style="text-align:left;padding:4px 10px;"><code>is_covid</code></td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>exogenous</code></td><td style="text-align:left;padding:4px 10px;"><code>intl_arrivals</code></td></tr></tbody>
</table>

## Models

Ordered by eval RMSE, best first.


### XGBoost

|  |  |
|---|---|
| RMSE | 17.81 |
| MAPE | 19.13% |

**By feature group**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>seasonal_level</code></td><td style="text-align:right;padding:4px 10px;">10.21</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lags</code></td><td style="text-align:right;padding:4px 10px;">10.08</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>calendar</code></td><td style="text-align:right;padding:4px 10px;">1.13</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>exogenous</code></td><td style="text-align:right;padding:4px 10px;">1.03</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>regime_flags</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr></tbody>
</table>

**By individual feature**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>monthly_avg</code></td><td style="text-align:right;padding:4px 10px;">10.56</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_12</code></td><td style="text-align:right;padding:4px 10px;">3.07</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_10</code></td><td style="text-align:right;padding:4px 10px;">2.94</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>intl_arrivals</code></td><td style="text-align:right;padding:4px 10px;">2.48</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_6</code></td><td style="text-align:right;padding:4px 10px;">1.02</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_11</code></td><td style="text-align:right;padding:4px 10px;">0.87</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_1</code></td><td style="text-align:right;padding:4px 10px;">0.63</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>sin_month</code></td><td style="text-align:right;padding:4px 10px;">0.60</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>cos_month</code></td><td style="text-align:right;padding:4px 10px;">0.34</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_7</code></td><td style="text-align:right;padding:4px 10px;">0.26</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_9</code></td><td style="text-align:right;padding:4px 10px;">0.15</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_3</code></td><td style="text-align:right;padding:4px 10px;">0.14</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_4</code></td><td style="text-align:right;padding:4px 10px;">0.03</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>is_covid</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_5</code></td><td style="text-align:right;padding:4px 10px;">-0.08</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_2</code></td><td style="text-align:right;padding:4px 10px;">-0.29</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_8</code></td><td style="text-align:right;padding:4px 10px;">-1.30</td></tr></tbody>
</table>

### Random Forest Regressor

|  |  |
|---|---|
| RMSE | 21.41 |
| MAPE | 18.73% |

**By feature group**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>seasonal_level</code></td><td style="text-align:right;padding:4px 10px;">5.83</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lags</code></td><td style="text-align:right;padding:4px 10px;">4.39</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>exogenous</code></td><td style="text-align:right;padding:4px 10px;">0.15</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>regime_flags</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>calendar</code></td><td style="text-align:right;padding:4px 10px;">-0.03</td></tr></tbody>
</table>

**By individual feature**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>monthly_avg</code></td><td style="text-align:right;padding:4px 10px;">7.62</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_12</code></td><td style="text-align:right;padding:4px 10px;">3.57</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_1</code></td><td style="text-align:right;padding:4px 10px;">0.66</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>intl_arrivals</code></td><td style="text-align:right;padding:4px 10px;">0.23</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_7</code></td><td style="text-align:right;padding:4px 10px;">0.18</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_2</code></td><td style="text-align:right;padding:4px 10px;">0.07</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_6</code></td><td style="text-align:right;padding:4px 10px;">0.06</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_3</code></td><td style="text-align:right;padding:4px 10px;">0.05</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_11</code></td><td style="text-align:right;padding:4px 10px;">0.01</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>is_covid</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_9</code></td><td style="text-align:right;padding:4px 10px;">-0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_10</code></td><td style="text-align:right;padding:4px 10px;">-0.01</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_5</code></td><td style="text-align:right;padding:4px 10px;">-0.01</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>sin_month</code></td><td style="text-align:right;padding:4px 10px;">-0.02</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_8</code></td><td style="text-align:right;padding:4px 10px;">-0.05</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>cos_month</code></td><td style="text-align:right;padding:4px 10px;">-0.05</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_4</code></td><td style="text-align:right;padding:4px 10px;">-0.07</td></tr></tbody>
</table>

### SARIMAX

|  |  |
|---|---|
| RMSE | 23.15 |
| MAPE | 27.17% |

**By feature group**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>lags</code></td><td style="text-align:right;padding:4px 10px;">7.54</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>exogenous</code></td><td style="text-align:right;padding:4px 10px;">3.66</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>calendar</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>seasonal_level</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>regime_flags</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr></tbody>
</table>

**By individual feature**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>intl_arrivals</code></td><td style="text-align:right;padding:4px 10px;">3.59</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_1</code></td><td style="text-align:right;padding:4px 10px;">2.35</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_12</code></td><td style="text-align:right;padding:4px 10px;">1.54</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_3</code></td><td style="text-align:right;padding:4px 10px;">1.30</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_10</code></td><td style="text-align:right;padding:4px 10px;">0.59</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_8</code></td><td style="text-align:right;padding:4px 10px;">0.58</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_7</code></td><td style="text-align:right;padding:4px 10px;">0.23</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_2</code></td><td style="text-align:right;padding:4px 10px;">0.23</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_11</code></td><td style="text-align:right;padding:4px 10px;">0.18</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_4</code></td><td style="text-align:right;padding:4px 10px;">0.14</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_9</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>sin_month</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>monthly_avg</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>cos_month</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>is_covid</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_5</code></td><td style="text-align:right;padding:4px 10px;">-0.32</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_6</code></td><td style="text-align:right;padding:4px 10px;">-0.80</td></tr></tbody>
</table>

### LSTM

|  |  |
|---|---|
| RMSE | 23.45 |
| MAPE | 18.81% |

Not scored: this model reads no feature columns, so there is nothing to permute.


### Baseline Monthly Mean

|  |  |
|---|---|
| RMSE | 36.40 |
| MAPE | 30.13% |

Not scored: this model reads no feature columns, so there is nothing to permute.


### Holt-Winters exponential smoothing

|  |  |
|---|---|
| RMSE | 43.75 |
| MAPE | 35.34% |

Not scored: this model reads no feature columns, so there is nothing to permute.

