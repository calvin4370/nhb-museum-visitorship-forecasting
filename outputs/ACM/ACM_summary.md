## Summary Report (ACM)

```
Branch:    test/run-pipelines-8d
Generated: 20 Oct 2026 4.47pm
```

### Model Evaluation Results + Predictions

<table><thead><tr><th>Model</th><th>RMSE</th><th>MAPE</th><th>FY2026</th><th>FY2027</th></tr></thead><tbody><tr><td>XGBoost</td><td>7.05</td><td>13.79%</td><td>488.9</td><td>486.3</td></tr><tr><td>Random Forest Regressor</td><td>7.12</td><td>13.96%</td><td>495.6</td><td>483.0</td></tr><tr><td>Support Vector Regression</td><td>7.41</td><td>14.05%</td><td>474.3</td><td>470.8</td></tr><tr><td>SARIMAX</td><td>7.67</td><td>15.73%</td><td>488.9</td><td>486.0</td></tr><tr><td>LSTM</td><td>8.63</td><td>20.61%</td><td>465.0</td><td>453.8</td></tr><tr><td>Holt-Winters exponential smoothing</td><td>10.10</td><td>16.85%</td><td>713.9</td><td>837.8</td></tr><tr><td>Baseline Monthly Mean</td><td>15.85</td><td>30.54%</td><td>452.0</td><td>452.0</td></tr></tbody></table>

### Total Visitors ('000s) by Financial Year (XGBoost)

<table align="left"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2014</td><td>78.2</td></tr><tr><td>FY2015</td><td>413.4</td></tr><tr><td>FY2016</td><td>522.4</td></tr><tr><td>FY2017</td><td>483.7</td></tr><tr><td>FY2018</td><td>572.7</td></tr><tr><td>FY2019</td><td>586.8</td></tr><tr><td>FY2020</td><td>153.2</td></tr></tbody></table><table align="right"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2021</td><td>197.1</td></tr><tr><td>FY2022</td><td>372.8</td></tr><tr><td>FY2023</td><td>424.4</td></tr><tr><td>FY2024</td><td>401.6</td></tr><tr><td>FY2025</td><td>529.9</td></tr><tr><td>FY2026 (Prediction)</td><td>488.9</td></tr><tr><td>FY2027 (Prediction)</td><td>486.3</td></tr></tbody></table><br clear="all">

![](eval/jj-new-eval-plots/ACM_eval_xgb_timeplot.png)

![](predict/jj-new-predict-plots/ACM_predict_top3_timeplot.png)
