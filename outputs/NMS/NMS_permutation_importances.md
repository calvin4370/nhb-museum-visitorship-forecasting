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
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>lags</code></td><td style="text-align:left;padding:4px 10px;"><code>lag_1</code>, <code>lag_2</code>, <code>lag_3</code>, <code>lag_4</code>, <code>lag_5</code>, <code>lag_6</code>, <code>lag_7</code>, <code>lag_8</code>, <code>lag_9</code>, <code>lag_10</code>, <code>lag_11</code>, <code>lag_12</code></td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>calendar</code></td><td style="text-align:left;padding:4px 10px;"><code>cos_month</code>, <code>sin_month</code></td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>seasonal_level</code></td><td style="text-align:left;padding:4px 10px;"><code>monthly_avg</code></td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>regime_flags</code></td><td style="text-align:left;padding:4px 10px;"><code>is_closed</code>, <code>is_covid</code></td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>exogenous</code></td><td style="text-align:left;padding:4px 10px;"><code>intl_arrivals</code></td></tr></tbody>
</table>

## Models

Ordered by eval RMSE, best first.


### XGBoost

|  |  |
|---|---|
| RMSE | 16.34 |
| MAPE | 17.40% |

**By feature group**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>lags</code></td><td style="text-align:right;padding:4px 10px;">7.39</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>calendar</code></td><td style="text-align:right;padding:4px 10px;">4.46</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>seasonal_level</code></td><td style="text-align:right;padding:4px 10px;">4.09</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>exogenous</code></td><td style="text-align:right;padding:4px 10px;">3.07</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>regime_flags</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr></tbody>
</table>

**By individual feature**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>monthly_avg</code></td><td style="text-align:right;padding:4px 10px;">4.97</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>sin_month</code></td><td style="text-align:right;padding:4px 10px;">3.48</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_12</code></td><td style="text-align:right;padding:4px 10px;">2.28</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>intl_arrivals</code></td><td style="text-align:right;padding:4px 10px;">1.62</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_10</code></td><td style="text-align:right;padding:4px 10px;">1.55</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_11</code></td><td style="text-align:right;padding:4px 10px;">1.01</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_9</code></td><td style="text-align:right;padding:4px 10px;">0.82</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_3</code></td><td style="text-align:right;padding:4px 10px;">0.79</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>cos_month</code></td><td style="text-align:right;padding:4px 10px;">0.57</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_5</code></td><td style="text-align:right;padding:4px 10px;">0.51</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_1</code></td><td style="text-align:right;padding:4px 10px;">0.37</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_2</code></td><td style="text-align:right;padding:4px 10px;">0.30</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_4</code></td><td style="text-align:right;padding:4px 10px;">0.25</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_6</code></td><td style="text-align:right;padding:4px 10px;">0.15</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_7</code></td><td style="text-align:right;padding:4px 10px;">0.07</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>is_closed</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>is_covid</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_8</code></td><td style="text-align:right;padding:4px 10px;">-0.51</td></tr></tbody>
</table>

### Support Vector Regression

|  |  |
|---|---|
| RMSE | 19.67 |
| MAPE | 15.18% |

**By feature group**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>seasonal_level</code></td><td style="text-align:right;padding:4px 10px;">9.18</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lags</code></td><td style="text-align:right;padding:4px 10px;">4.67</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>exogenous</code></td><td style="text-align:right;padding:4px 10px;">3.30</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>calendar</code></td><td style="text-align:right;padding:4px 10px;">0.19</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>regime_flags</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr></tbody>
</table>

**By individual feature**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>monthly_avg</code></td><td style="text-align:right;padding:4px 10px;">10.25</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>intl_arrivals</code></td><td style="text-align:right;padding:4px 10px;">2.14</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_8</code></td><td style="text-align:right;padding:4px 10px;">1.61</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_12</code></td><td style="text-align:right;padding:4px 10px;">1.51</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_1</code></td><td style="text-align:right;padding:4px 10px;">1.39</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>cos_month</code></td><td style="text-align:right;padding:4px 10px;">0.02</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_4</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>is_covid</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>is_closed</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_10</code></td><td style="text-align:right;padding:4px 10px;">-0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_9</code></td><td style="text-align:right;padding:4px 10px;">-0.08</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_3</code></td><td style="text-align:right;padding:4px 10px;">-0.14</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_5</code></td><td style="text-align:right;padding:4px 10px;">-0.14</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_11</code></td><td style="text-align:right;padding:4px 10px;">-0.16</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_7</code></td><td style="text-align:right;padding:4px 10px;">-0.26</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>sin_month</code></td><td style="text-align:right;padding:4px 10px;">-0.38</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_2</code></td><td style="text-align:right;padding:4px 10px;">-0.42</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_6</code></td><td style="text-align:right;padding:4px 10px;">-0.46</td></tr></tbody>
</table>

### Random Forest Regressor

|  |  |
|---|---|
| RMSE | 21.68 |
| MAPE | 18.90% |

**By feature group**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>seasonal_level</code></td><td style="text-align:right;padding:4px 10px;">5.86</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lags</code></td><td style="text-align:right;padding:4px 10px;">2.91</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>exogenous</code></td><td style="text-align:right;padding:4px 10px;">0.18</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>regime_flags</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>calendar</code></td><td style="text-align:right;padding:4px 10px;">-0.02</td></tr></tbody>
</table>

**By individual feature**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>monthly_avg</code></td><td style="text-align:right;padding:4px 10px;">7.41</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_12</code></td><td style="text-align:right;padding:4px 10px;">3.01</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_1</code></td><td style="text-align:right;padding:4px 10px;">0.33</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_6</code></td><td style="text-align:right;padding:4px 10px;">0.16</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>intl_arrivals</code></td><td style="text-align:right;padding:4px 10px;">0.12</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_9</code></td><td style="text-align:right;padding:4px 10px;">0.09</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_7</code></td><td style="text-align:right;padding:4px 10px;">0.08</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_3</code></td><td style="text-align:right;padding:4px 10px;">0.05</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_11</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>is_closed</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>is_covid</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_2</code></td><td style="text-align:right;padding:4px 10px;">-0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_5</code></td><td style="text-align:right;padding:4px 10px;">-0.01</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>sin_month</code></td><td style="text-align:right;padding:4px 10px;">-0.02</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_10</code></td><td style="text-align:right;padding:4px 10px;">-0.02</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>cos_month</code></td><td style="text-align:right;padding:4px 10px;">-0.05</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_4</code></td><td style="text-align:right;padding:4px 10px;">-0.06</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_8</code></td><td style="text-align:right;padding:4px 10px;">-0.09</td></tr></tbody>
</table>

### LSTM

|  |  |
|---|---|
| RMSE | 23.46 |
| MAPE | 18.90% |

Not scored: this model reads no feature columns, so there is nothing to permute.


### SARIMAX

|  |  |
|---|---|
| RMSE | 26.38 |
| MAPE | 32.35% |

**By feature group**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>exogenous</code></td><td style="text-align:right;padding:4px 10px;">3.66</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>calendar</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lags</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>regime_flags</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>seasonal_level</code></td><td style="text-align:right;padding:4px 10px;">-0.00</td></tr></tbody>
</table>

**By individual feature**

<table style="border-collapse:collapse;">
<thead><tr><th style="text-align:left;padding:4px 10px;">Feature</th><th style="text-align:right;padding:4px 10px;">Importance (RMSE)</th></tr></thead>
<tbody><tr><td style="text-align:left;padding:4px 10px;"><code>intl_arrivals</code></td><td style="text-align:right;padding:4px 10px;">2.45</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>sin_month</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>cos_month</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_8</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_6</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_1</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_2</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_3</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_4</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_5</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_7</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_10</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_9</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_11</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>lag_12</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>is_covid</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>is_closed</code></td><td style="text-align:right;padding:4px 10px;">0.00</td></tr><tr><td style="text-align:left;padding:4px 10px;"><code>monthly_avg</code></td><td style="text-align:right;padding:4px 10px;">-0.00</td></tr></tbody>
</table>

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

