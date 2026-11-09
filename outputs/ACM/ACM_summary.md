## Summary Report (ACM)

```
Branch:    feature/more-event-features
Generated: 6 Nov 2026 4.06pm
```

### Model Evaluation Results + Predictions

<table><thead><tr><th>Model</th><th>RMSE</th><th>MAPE</th><th>FY2026</th><th>FY2027</th></tr></thead><tbody><tr><td>Random Forest Regressor</td><td>7.12</td><td>13.96%</td><td>493.2</td><td>475.9</td></tr><tr><td>XGBoost</td><td>7.22</td><td>13.63%</td><td>485.1</td><td>489.7</td></tr><tr><td>Support Vector Regression</td><td>7.34</td><td>14.45%</td><td>474.8</td><td>472.3</td></tr><tr><td>LSTM</td><td>9.41</td><td>22.42%</td><td>468.3</td><td>457.9</td></tr><tr><td>SARIMAX</td><td>9.65</td><td>16.44%</td><td>581.2</td><td>632.4</td></tr><tr><td>Holt-Winters exponential smoothing</td><td>13.89</td><td>24.33%</td><td>774.8</td><td>989.3</td></tr><tr><td>Baseline Monthly Mean</td><td>15.85</td><td>30.54%</td><td>452.0</td><td>452.0</td></tr></tbody></table>

### Total Visitors ('000s) by Financial Year (Random Forest Regressor)

<table align="left"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2014</td><td>78.2</td></tr><tr><td>FY2015</td><td>413.4</td></tr><tr><td>FY2016</td><td>522.4</td></tr><tr><td>FY2017</td><td>483.7</td></tr><tr><td>FY2018</td><td>572.7</td></tr><tr><td>FY2019</td><td>586.8</td></tr><tr><td>FY2020</td><td>153.2</td></tr></tbody></table><table align="right"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2021</td><td>197.1</td></tr><tr><td>FY2022</td><td>372.8</td></tr><tr><td>FY2023</td><td>424.4</td></tr><tr><td>FY2024</td><td>401.6</td></tr><tr><td>FY2025</td><td>529.9</td></tr><tr><td>FY2026 (Prediction)</td><td>493.2</td></tr><tr><td>FY2027 (Prediction)</td><td>475.9</td></tr></tbody></table><br clear="all">

![](eval/jj-new-eval-plots/ACM_eval_rf_timeplot.png)

![](predict/jj-new-predict-plots/ACM_predict_top3_timeplot.png)
