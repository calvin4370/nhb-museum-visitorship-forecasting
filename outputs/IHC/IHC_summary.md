## Summary Report (IHC)

```
Branch:    feature/widen-hyperparameter-tuning
Generated: 9 Sep 2026 10.53am
```

### Model Evaluation Results + Predictions

<table><thead><tr><th>Model</th><th>RMSE</th><th>MAPE</th><th>FY2026</th><th>FY2027</th></tr></thead><tbody><tr><td>LSTM</td><td>5.97</td><td>37.70%</td><td>237.3</td><td>230.2</td></tr><tr><td>Holt-Winters exponential smoothing</td><td>6.19</td><td>35.66%</td><td>201.0</td><td>192.4</td></tr><tr><td>XGBoost</td><td>6.61</td><td>27.97%</td><td>213.3</td><td>210.3</td></tr><tr><td>Random Forest Regressor</td><td>6.62</td><td>30.43%</td><td>211.1</td><td>209.9</td></tr><tr><td>SARIMAX</td><td>7.88</td><td>28.75%</td><td>214.4</td><td>213.3</td></tr><tr><td>Baseline Monthly Mean</td><td>8.79</td><td>33.24%</td><td>216.6</td><td>216.6</td></tr></tbody></table>

### Total Visitors ('000s) by Financial Year (LSTM)

<table align="left"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2016</td><td>138.9</td></tr><tr><td>FY2017</td><td>185.5</td></tr><tr><td>FY2018</td><td>236.3</td></tr><tr><td>FY2019</td><td>210.5</td></tr><tr><td>FY2020</td><td>37.6</td></tr><tr><td>FY2021</td><td>46.5</td></tr></tbody></table><table align="right"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2022</td><td>148.6</td></tr><tr><td>FY2023</td><td>216.2</td></tr><tr><td>FY2024</td><td>215.3</td></tr><tr><td>FY2025</td><td>218.2</td></tr><tr><td>FY2026 (Prediction)</td><td>237.3</td></tr><tr><td>FY2027 (Prediction)</td><td>230.2</td></tr></tbody></table><br clear="all">

![](eval/jj-new-eval-plots/IHC_eval_lstm_timeplot.png)

**Deepavali months: actual vs predicted (LSTM)**

| Month | Actual | Predicted | Difference | % difference |
|---|---|---|---|---|
| 2024-10 | 43.90 | 30.94 | -12.96 | -29.51% |
| 2025-10 | 38.30 | 31.19 | -7.11 | -18.56% |
| 2026-11 | -- | 23.49 | -- | -- |
| 2027-10 | -- | 37.78 | -- | -- |

![](predict/jj-new-predict-plots/IHC_predict_top3_timeplot.png)
