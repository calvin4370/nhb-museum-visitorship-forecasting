## Summary Report (IHC)

```
Branch:    test/run-pipelines-8b
Generated: 16 Sep 2026 10.31am
```

### Model Evaluation Results + Predictions

<table><thead><tr><th>Model</th><th>RMSE</th><th>MAPE</th><th>FY2026</th><th>FY2027</th></tr></thead><tbody><tr><td>Support Vector Regression</td><td>5.37</td><td>28.04%</td><td>208.3</td><td>207.2</td></tr><tr><td>LSTM</td><td>6.11</td><td>37.61%</td><td>233.8</td><td>225.5</td></tr><tr><td>Holt-Winters exponential smoothing</td><td>6.19</td><td>35.66%</td><td>201.0</td><td>192.4</td></tr><tr><td>Random Forest Regressor</td><td>6.62</td><td>30.44%</td><td>211.1</td><td>209.9</td></tr><tr><td>XGBoost</td><td>6.85</td><td>29.40%</td><td>206.9</td><td>205.2</td></tr><tr><td>Baseline Monthly Mean</td><td>8.79</td><td>33.24%</td><td>216.6</td><td>216.6</td></tr><tr><td>SARIMAX</td><td>8.92</td><td>40.79%</td><td>215.8</td><td>223.6</td></tr></tbody></table>

### Total Visitors ('000s) by Financial Year (Support Vector Regression)

<table align="left"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2016</td><td>138.9</td></tr><tr><td>FY2017</td><td>185.5</td></tr><tr><td>FY2018</td><td>236.3</td></tr><tr><td>FY2019</td><td>210.5</td></tr><tr><td>FY2020</td><td>37.6</td></tr><tr><td>FY2021</td><td>46.5</td></tr></tbody></table><table align="right"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2022</td><td>148.6</td></tr><tr><td>FY2023</td><td>216.2</td></tr><tr><td>FY2024</td><td>215.3</td></tr><tr><td>FY2025</td><td>218.2</td></tr><tr><td>FY2026 (Prediction)</td><td>208.3</td></tr><tr><td>FY2027 (Prediction)</td><td>207.2</td></tr></tbody></table><br clear="all">

![](eval/jj-new-eval-plots/IHC_eval_svr_timeplot.png)

**Deepavali months: actual vs predicted (Support Vector Regression)**

| Month | Actual | Predicted | Difference | % difference |
|---|---|---|---|---|
| 2024-10 | 43.90 | 27.35 | -16.55 | -37.70% |
| 2025-10 | 38.30 | 29.24 | -9.06 | -23.66% |
| 2026-11 | -- | 23.88 | -- | -- |
| 2027-10 | -- | 34.30 | -- | -- |

![](predict/jj-new-predict-plots/IHC_predict_top3_timeplot.png)
