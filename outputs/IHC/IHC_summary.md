## Summary Report (IHC)

```
Branch:    test/run-pipelines-7a
Generated: 9 Sep 2026 11.37am
```

### Model Evaluation Results + Predictions

<table><thead><tr><th>Model</th><th>RMSE</th><th>MAPE</th><th>FY2026</th><th>FY2027</th></tr></thead><tbody><tr><td>Holt-Winters exponential smoothing</td><td>6.19</td><td>35.66%</td><td>201.0</td><td>192.4</td></tr><tr><td>LSTM</td><td>6.29</td><td>38.34%</td><td>241.9</td><td>233.5</td></tr><tr><td>XGBoost</td><td>6.52</td><td>30.11%</td><td>220.1</td><td>221.5</td></tr><tr><td>Random Forest Regressor</td><td>6.54</td><td>30.15%</td><td>211.2</td><td>210.4</td></tr><tr><td>SARIMAX</td><td>8.69</td><td>33.77%</td><td>212.8</td><td>215.0</td></tr><tr><td>Baseline Monthly Mean</td><td>8.79</td><td>33.24%</td><td>216.6</td><td>216.6</td></tr></tbody></table>

### Total Visitors ('000s) by Financial Year (Holt-Winters exponential smoothing)

<table align="left"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2016</td><td>138.9</td></tr><tr><td>FY2017</td><td>185.5</td></tr><tr><td>FY2018</td><td>236.3</td></tr><tr><td>FY2019</td><td>210.5</td></tr><tr><td>FY2020</td><td>37.6</td></tr><tr><td>FY2021</td><td>46.5</td></tr></tbody></table><table align="right"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2022</td><td>148.6</td></tr><tr><td>FY2023</td><td>216.2</td></tr><tr><td>FY2024</td><td>215.3</td></tr><tr><td>FY2025</td><td>218.2</td></tr><tr><td>FY2026 (Prediction)</td><td>201.0</td></tr><tr><td>FY2027 (Prediction)</td><td>192.4</td></tr></tbody></table><br clear="all">

![](eval/jj-new-eval-plots/IHC_eval_hw_timeplot.png)

**Deepavali months: actual vs predicted (Holt-Winters exponential smoothing)**

| Month | Actual | Predicted | Difference | % difference |
|---|---|---|---|---|
| 2024-10 | 43.90 | 26.35 | -17.55 | -39.98% |
| 2025-10 | 38.30 | 27.93 | -10.37 | -27.06% |
| 2026-11 | -- | 16.12 | -- | -- |
| 2027-10 | -- | 27.34 | -- | -- |

![](predict/jj-new-predict-plots/IHC_predict_top3_timeplot.png)
