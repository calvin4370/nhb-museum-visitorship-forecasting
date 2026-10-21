## Summary Report (MHC)

```
Branch:    test/run-pipelines-8e
Generated: 20 Oct 2026 5.55pm
```

### Model Evaluation Results + Predictions

<table><thead><tr><th>Model</th><th>RMSE</th><th>MAPE</th><th>FY2026</th><th>FY2027</th></tr></thead><tbody><tr><td>LSTM</td><td>1.58</td><td>604903602089953664.00%</td><td>535.0</td><td>705.4</td></tr><tr><td>Support Vector Regression</td><td>3.82</td><td>1623689701143279872.00%</td><td>568.2</td><td>642.8</td></tr><tr><td>Holt-Winters exponential smoothing</td><td>4.92</td><td>1823584433231552768.00%</td><td>-19.9</td><td>-61.3</td></tr><tr><td>Random Forest Regressor</td><td>6.33</td><td>2725472596350528512.00%</td><td>489.7</td><td>624.7</td></tr><tr><td>XGBoost</td><td>8.05</td><td>3275675265878516736.00%</td><td>532.8</td><td>618.3</td></tr><tr><td>Baseline Monthly Mean</td><td>8.26</td><td>3450535714501395456.00%</td><td>0.0</td><td>0.0</td></tr><tr><td>SARIMAX</td><td>8.53</td><td>3237939459608104448.00%</td><td>408.0</td><td>448.8</td></tr></tbody></table>

### Total Visitors ('000s) by Financial Year (LSTM)

<table align="left"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2014</td><td>109.1</td></tr><tr><td>FY2015</td><td>504.2</td></tr><tr><td>FY2016</td><td>558.1</td></tr><tr><td>FY2017</td><td>718.1</td></tr><tr><td>FY2018</td><td>741.6</td></tr><tr><td>FY2019</td><td>675.1</td></tr><tr><td>FY2020</td><td>59.5</td></tr></tbody></table><table align="right"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2021</td><td>84.7</td></tr><tr><td>FY2022</td><td>171.5</td></tr><tr><td>FY2023</td><td>0.0</td></tr><tr><td>FY2024</td><td>0.0</td></tr><tr><td>FY2025</td><td>0.0</td></tr><tr><td>FY2026 (Prediction)</td><td>535.0</td></tr><tr><td>FY2027 (Prediction)</td><td>705.4</td></tr></tbody></table><br clear="all">

![](eval/jj-new-eval-plots/MHC_eval_lstm_timeplot.png)

![](predict/jj-new-predict-plots/MHC_predict_top3_timeplot.png)
