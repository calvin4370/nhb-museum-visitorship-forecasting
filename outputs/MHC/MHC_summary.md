## Summary Report (MHC)

```
Branch:    test/run-pipelines-7b
Generated: 9 Sep 2026 2.50pm
```

### Model Evaluation Results + Predictions

<table><thead><tr><th>Model</th><th>RMSE</th><th>MAPE</th><th>FY2026</th><th>FY2027</th></tr></thead><tbody><tr><td>XGBoost</td><td>0.13</td><td>45704918092762072.00%</td><td>470.8</td><td>733.4</td></tr><tr><td>Random Forest Regressor</td><td>0.85</td><td>380796167223740480.00%</td><td>442.1</td><td>683.6</td></tr><tr><td>Holt-Winters exponential smoothing</td><td>4.92</td><td>1823584433231552768.00%</td><td>-19.9</td><td>-61.3</td></tr><tr><td>SARIMAX</td><td>5.72</td><td>2073647935685850368.00%</td><td>540.0</td><td>618.5</td></tr><tr><td>LSTM</td><td>6.0</td><td>2555973406224110592.00%</td><td>533.7</td><td>691.6</td></tr><tr><td>Baseline Monthly Mean</td><td>8.26</td><td>3450535714501395456.00%</td><td>0.0</td><td>0.0</td></tr></tbody></table>

### Total Visitors ('000s) by Financial Year (XGBoost)

<table align="left"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2014</td><td>109.1</td></tr><tr><td>FY2015</td><td>504.2</td></tr><tr><td>FY2016</td><td>558.1</td></tr><tr><td>FY2017</td><td>718.1</td></tr><tr><td>FY2018</td><td>741.6</td></tr><tr><td>FY2019</td><td>675.1</td></tr><tr><td>FY2020</td><td>59.5</td></tr></tbody></table><table align="right"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2021</td><td>84.7</td></tr><tr><td>FY2022</td><td>171.5</td></tr><tr><td>FY2023</td><td>0.0</td></tr><tr><td>FY2024</td><td>0.0</td></tr><tr><td>FY2025</td><td>0.0</td></tr><tr><td>FY2026 (Prediction)</td><td>470.8</td></tr><tr><td>FY2027 (Prediction)</td><td>733.4</td></tr></tbody></table><br clear="all">

![](eval/jj-new-eval-plots/MHC_eval_xgb_timeplot.png)

![](predict/jj-new-predict-plots/MHC_predict_top3_timeplot.png)
