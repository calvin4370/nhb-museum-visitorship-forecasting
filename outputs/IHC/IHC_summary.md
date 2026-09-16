## Summary Report (IHC)

```
Branch:    test/run-pipelines-8c
Generated: 16 Sep 2026 12.34pm
```

### Model Evaluation Results + Predictions

<table><thead><tr><th>Model</th><th>RMSE</th><th>MAPE</th><th>FY2026</th><th>FY2027</th></tr></thead><tbody><tr><td>SARIMAX</td><td>3.95</td><td>19.52%</td><td>218.7</td><td>218.9</td></tr><tr><td>Support Vector Regression</td><td>4.79</td><td>27.34%</td><td>211.2</td><td>211.5</td></tr><tr><td>XGBoost</td><td>5.64</td><td>26.63%</td><td>219.9</td><td>217.7</td></tr><tr><td>Random Forest Regressor</td><td>5.88</td><td>28.35%</td><td>214.1</td><td>211.5</td></tr><tr><td>LSTM</td><td>6.11</td><td>36.58%</td><td>236.4</td><td>224.7</td></tr><tr><td>Holt-Winters exponential smoothing</td><td>6.19</td><td>35.66%</td><td>201.0</td><td>192.4</td></tr><tr><td>Baseline Monthly Mean</td><td>8.79</td><td>33.24%</td><td>216.6</td><td>216.6</td></tr></tbody></table>

### Total Visitors ('000s) by Financial Year (SARIMAX)

<table align="left"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2016</td><td>138.9</td></tr><tr><td>FY2017</td><td>185.5</td></tr><tr><td>FY2018</td><td>236.3</td></tr><tr><td>FY2019</td><td>210.5</td></tr><tr><td>FY2020</td><td>37.6</td></tr><tr><td>FY2021</td><td>46.5</td></tr></tbody></table><table align="right"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2022</td><td>148.6</td></tr><tr><td>FY2023</td><td>216.2</td></tr><tr><td>FY2024</td><td>215.3</td></tr><tr><td>FY2025</td><td>218.2</td></tr><tr><td>FY2026 (Prediction)</td><td>218.7</td></tr><tr><td>FY2027 (Prediction)</td><td>218.9</td></tr></tbody></table><br clear="all">

![](eval/jj-new-eval-plots/IHC_eval_sarimax_timeplot.png)

**Deepavali months: actual vs predicted (SARIMAX)**

| Month | Actual | Predicted | Difference | % difference |
|---|---|---|---|---|
| 2024-10 | 43.90 | 32.19 | -11.71 | -26.68% |
| 2025-10 | 38.30 | 37.13 | -1.17 | -3.06% |
| 2026-11 | -- | 30.05 | -- | -- |
| 2027-10 | -- | 39.26 | -- | -- |

![](predict/jj-new-predict-plots/IHC_predict_top3_timeplot.png)
