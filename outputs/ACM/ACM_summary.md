## Summary Report (ACM)

```
Branch:    feature/more-event-features
Generated: 10 Nov 2026 10.01am
```

### Run Config

```
Data Window:           Jan 2014 - Mar 2026
Training Period:       Jan 2015 - Dec 2023 (108 months)
Evaluation Period:     Jan 2024 - Mar 2026 (27 months)
Prediction Period:     Apr 2026 - Mar 2028 (24 months)
COVID Period:          1 Apr 2020 - 13 Feb 2023
Museum:                Asian Civilisations Museum (ACM)
Base Features:         sin_month, cos_month, monthly_avg, is_covid, is_closed, intl_arrivals, lag_1 - lag_12
ACM-specific Features: None
```

### Model Evaluation Results + Predictions

<table><thead><tr><th>Model</th><th>RMSE</th><th>MAPE</th><th>FY2026</th><th>FY2027</th></tr></thead><tbody><tr><td>Random Forest Regressor</td><td>7.13</td><td>13.99%</td><td>495.4</td><td>482.7</td></tr><tr><td>Support Vector Regression</td><td>7.31</td><td>14.44%</td><td>475.1</td><td>472.6</td></tr><tr><td>XGBoost</td><td>7.75</td><td>14.25%</td><td>491.3</td><td>492.9</td></tr><tr><td>LSTM</td><td>9.75</td><td>23.69%</td><td>467.3</td><td>454.5</td></tr><tr><td>SARIMAX</td><td>9.91</td><td>21.02%</td><td>638.3</td><td>739.6</td></tr><tr><td>Holt-Winters exponential smoothing</td><td>12.04</td><td>21.03%</td><td>728.0</td><td>883.1</td></tr><tr><td>Baseline Monthly Mean</td><td>15.85</td><td>30.54%</td><td>452.0</td><td>452.0</td></tr></tbody></table>

### Total Visitors ('000s) by Financial Year (Random Forest Regressor)

<table align="left"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2014</td><td>78.2</td></tr><tr><td>FY2015</td><td>413.4</td></tr><tr><td>FY2016</td><td>522.4</td></tr><tr><td>FY2017</td><td>483.7</td></tr><tr><td>FY2018</td><td>572.7</td></tr><tr><td>FY2019</td><td>586.8</td></tr><tr><td>FY2020</td><td>153.2</td></tr></tbody></table><table align="right"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2021</td><td>197.1</td></tr><tr><td>FY2022</td><td>372.8</td></tr><tr><td>FY2023</td><td>424.4</td></tr><tr><td>FY2024</td><td>401.6</td></tr><tr><td>FY2025</td><td>529.9</td></tr><tr><td>FY2026 (Prediction)</td><td>495.4</td></tr><tr><td>FY2027 (Prediction)</td><td>482.7</td></tr></tbody></table><br clear="all">

![](eval/jj-new-eval-plots/ACM_eval_rf_timeplot.png)

![](predict/jj-new-predict-plots/ACM_predict_top3_timeplot.png)
