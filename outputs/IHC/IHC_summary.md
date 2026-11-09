## Summary Report (IHC)

```
Branch:    feature/more-event-features
Generated: 6 Nov 2026 5.42pm
```

### Model Evaluation Results + Predictions

<table><thead><tr><th>Model</th><th>RMSE</th><th>MAPE</th><th>FY2026</th><th>FY2027</th></tr></thead><tbody><tr><td>Support Vector Regression</td><td>4.83</td><td>26.96%</td><td>210.4</td><td>210.6</td></tr><tr><td>SARIMAX</td><td>5.04</td><td>25.52%</td><td>212.2</td><td>215.5</td></tr><tr><td>XGBoost</td><td>5.64</td><td>26.09%</td><td>218.3</td><td>218.2</td></tr><tr><td>Random Forest Regressor</td><td>6.33</td><td>27.75%</td><td>211.1</td><td>210.3</td></tr><tr><td>Holt-Winters exponential smoothing</td><td>6.38</td><td>25.60%</td><td>228.6</td><td>239.5</td></tr><tr><td>LSTM</td><td>6.57</td><td>35.99%</td><td>240.9</td><td>223.5</td></tr><tr><td>Baseline Monthly Mean</td><td>9.77</td><td>40.23%</td><td>216.6</td><td>216.6</td></tr></tbody></table>

### Total Visitors ('000s) by Financial Year (Support Vector Regression)

<table align="left"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2016</td><td>138.9</td></tr><tr><td>FY2017</td><td>185.5</td></tr><tr><td>FY2018</td><td>236.3</td></tr><tr><td>FY2019</td><td>210.5</td></tr><tr><td>FY2020</td><td>37.6</td></tr><tr><td>FY2021</td><td>46.5</td></tr></tbody></table><table align="right"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2022</td><td>148.6</td></tr><tr><td>FY2023</td><td>216.2</td></tr><tr><td>FY2024</td><td>215.3</td></tr><tr><td>FY2025</td><td>218.2</td></tr><tr><td>FY2026 (Prediction)</td><td>210.4</td></tr><tr><td>FY2027 (Prediction)</td><td>210.6</td></tr></tbody></table><br clear="all">

![](eval/jj-new-eval-plots/IHC_eval_svr_timeplot.png)

**Deepavali months: actual vs predicted (Support Vector Regression)**

| Month | Actual | Predicted | Difference | % difference |
|---|---|---|---|---|
| 2024-10 | 43.90 | 30.26 | -13.64 | -31.07% |
| 2025-10 | 38.30 | 33.07 | -5.23 | -13.67% |
| 2026-11 | -- | 31.59 | -- | -- |
| 2027-10 | -- | 40.02 | -- | -- |

![](predict/jj-new-predict-plots/IHC_predict_top3_timeplot.png)
