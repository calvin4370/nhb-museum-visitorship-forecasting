## Summary Report (IHC)

```
Branch:    test/run-pipelines-9a2
Generated: 21 Sep 2026 4.26pm
```

### Model Evaluation Results + Predictions

<table><thead><tr><th>Model</th><th>RMSE</th><th>MAPE</th><th>FY2026</th><th>FY2027</th></tr></thead><tbody><tr><td>XGBoost</td><td>4.69</td><td>23.82%</td><td>219.9</td><td>217.7</td></tr><tr><td>SARIMAX</td><td>4.72</td><td>29.05%</td><td>214.5</td><td>214.5</td></tr><tr><td>Support Vector Regression</td><td>4.89</td><td>27.15%</td><td>211.2</td><td>211.5</td></tr><tr><td>Random Forest Regressor</td><td>5.80</td><td>28.98%</td><td>214.1</td><td>211.5</td></tr><tr><td>Holt-Winters exponential smoothing</td><td>6.19</td><td>35.66%</td><td>201.0</td><td>192.4</td></tr><tr><td>LSTM</td><td>6.22</td><td>38.54%</td><td>240.3</td><td>226.5</td></tr><tr><td>Baseline Monthly Mean</td><td>8.79</td><td>33.24%</td><td>216.6</td><td>216.6</td></tr></tbody></table>

### Total Visitors ('000s) by Financial Year (XGBoost)

<table align="left"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2016</td><td>138.9</td></tr><tr><td>FY2017</td><td>185.5</td></tr><tr><td>FY2018</td><td>236.3</td></tr><tr><td>FY2019</td><td>210.5</td></tr><tr><td>FY2020</td><td>37.6</td></tr><tr><td>FY2021</td><td>46.5</td></tr></tbody></table><table align="right"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2022</td><td>148.6</td></tr><tr><td>FY2023</td><td>216.2</td></tr><tr><td>FY2024</td><td>215.3</td></tr><tr><td>FY2025</td><td>218.2</td></tr><tr><td>FY2026 (Prediction)</td><td>219.9</td></tr><tr><td>FY2027 (Prediction)</td><td>217.7</td></tr></tbody></table><br clear="all">

![](eval/jj-new-eval-plots/IHC_eval_xgb_timeplot.png)

**Deepavali months: actual vs predicted (XGBoost)**

| Month | Actual | Predicted | Difference | % difference |
|---|---|---|---|---|
| 2024-10 | 43.90 | 30.59 | -13.31 | -30.31% |
| 2025-10 | 38.30 | 31.17 | -7.13 | -18.63% |
| 2026-11 | -- | 27.96 | -- | -- |
| 2027-10 | -- | 39.10 | -- | -- |

![](predict/jj-new-predict-plots/IHC_predict_top3_timeplot.png)
