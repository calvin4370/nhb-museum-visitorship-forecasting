## Summary Report (TPM)

```
Branch:    test/run-pipelines-7b
Generated: 16 Sep 2026 9.46am
```

### Model Evaluation Results + Predictions

<table><thead><tr><th>Model</th><th>RMSE</th><th>MAPE</th><th>FY2026</th><th>FY2027</th></tr></thead><tbody><tr><td>Random Forest Regressor</td><td>2.52</td><td>14.62%</td><td>202.2</td><td>225.9</td></tr><tr><td>Support Vector Regression</td><td>3.63</td><td>17.96%</td><td>177.6</td><td>207.4</td></tr><tr><td>XGBoost</td><td>3.79</td><td>21.11%</td><td>214.0</td><td>260.3</td></tr><tr><td>LSTM</td><td>5.95</td><td>37.82%</td><td>261.7</td><td>304.4</td></tr><tr><td>Baseline Monthly Mean</td><td>10.17</td><td>68.14%</td><td>170.1</td><td>170.1</td></tr><tr><td>Holt-Winters exponential smoothing</td><td>12.93</td><td>88.56%</td><td>166.6</td><td>171.6</td></tr><tr><td>SARIMAX</td><td>14.93</td><td>100.71%</td><td>41.8</td><td>-18.1</td></tr></tbody></table>

### Total Visitors ('000s) by Financial Year (Random Forest Regressor)

<table align="left"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2014</td><td>102.8</td></tr><tr><td>FY2015</td><td>470.6</td></tr><tr><td>FY2016</td><td>551.8</td></tr><tr><td>FY2017</td><td>381.5</td></tr><tr><td>FY2018</td><td>223.3</td></tr><tr><td>FY2019</td><td>0.0</td></tr><tr><td>FY2020</td><td>0.0</td></tr></tbody></table><table align="right"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2021</td><td>0.0</td></tr><tr><td>FY2022</td><td>35.1</td></tr><tr><td>FY2023</td><td>172.6</td></tr><tr><td>FY2024</td><td>170.1</td></tr><tr><td>FY2025</td><td>167.6</td></tr><tr><td>FY2026 (Prediction)</td><td>202.2</td></tr><tr><td>FY2027 (Prediction)</td><td>225.9</td></tr></tbody></table><br clear="all">

![](eval/jj-new-eval-plots/TPM_eval_rf_timeplot.png)

![](predict/jj-new-predict-plots/TPM_predict_top3_timeplot.png)
