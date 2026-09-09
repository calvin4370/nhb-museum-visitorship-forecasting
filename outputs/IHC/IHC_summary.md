## Summary Report (IHC)

```
Branch:    test/run-pipelines-8a
Generated: 9 Sep 2026 2.39pm
```

### Model Evaluation Results + Predictions

<table><thead><tr><th>Model</th><th>RMSE</th><th>MAPE</th><th>FY2026</th><th>FY2027</th></tr></thead><tbody><tr><td>Support Vector Regression</td><td>6.03</td><td>26.27%</td><td>206.6</td><td>205.6</td></tr><tr><td>Random Forest Regressor</td><td>6.94</td><td>35.44%</td><td>226.9</td><td>216.5</td></tr><tr><td>LSTM</td><td>7.00</td><td>37.52%</td><td>216.9</td><td>220.3</td></tr><tr><td>XGBoost</td><td>7.55</td><td>35.09%</td><td>210.1</td><td>211.5</td></tr><tr><td>Baseline Monthly Mean</td><td>8.79</td><td>33.24%</td><td>216.6</td><td>216.6</td></tr><tr><td>Holt-Winters exponential smoothing</td><td>11.97</td><td>72.50%</td><td>218.0</td><td>223.6</td></tr></tbody></table>

### Total Visitors ('000s) by Financial Year (Support Vector Regression)

<table align="left"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2016</td><td>138.9</td></tr><tr><td>FY2017</td><td>185.5</td></tr><tr><td>FY2018</td><td>236.3</td></tr><tr><td>FY2019</td><td>210.5</td></tr><tr><td>FY2020</td><td>37.6</td></tr><tr><td>FY2021</td><td>46.5</td></tr></tbody></table><table align="right"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2022</td><td>148.6</td></tr><tr><td>FY2023</td><td>216.2</td></tr><tr><td>FY2024</td><td>215.3</td></tr><tr><td>FY2025</td><td>218.2</td></tr><tr><td>FY2026 (Prediction)</td><td>206.6</td></tr><tr><td>FY2027 (Prediction)</td><td>205.6</td></tr></tbody></table><br clear="all">

![](eval/jj-new-eval-plots/IHC_eval_svr_timeplot.png)

**Deepavali months: actual vs predicted (Support Vector Regression)**

| Month | Actual | Predicted | Difference | % difference |
|---|---|---|---|---|
| 2024-10 | 43.90 | 24.75 | -19.15 | -43.62% |
| 2025-10 | 38.30 | 34.17 | -4.13 | -10.79% |
| 2026-11 | -- | 20.62 | -- | -- |
| 2027-10 | -- | 31.76 | -- | -- |

![](predict/jj-new-predict-plots/IHC_predict_top3_timeplot.png)
