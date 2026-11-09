## Summary Report (TPM)

```
Branch:    feature/more-event-features
Generated: 6 Nov 2026 5.21pm
```

### Model Evaluation Results + Predictions

<table><thead><tr><th>Model</th><th>RMSE</th><th>MAPE</th><th>FY2026</th><th>FY2027</th></tr></thead><tbody><tr><td>SARIMAX</td><td>3.51</td><td>22.85%</td><td>120.0</td><td>158.8</td></tr><tr><td>XGBoost</td><td>3.59</td><td>24.60%</td><td>209.6</td><td>224.3</td></tr><tr><td>Support Vector Regression</td><td>3.72</td><td>19.80%</td><td>244.5</td><td>312.9</td></tr><tr><td>Random Forest Regressor</td><td>4.06</td><td>21.44%</td><td>217.9</td><td>237.2</td></tr><tr><td>LSTM</td><td>8.33</td><td>52.54%</td><td>258.2</td><td>304.3</td></tr><tr><td>Baseline Monthly Mean</td><td>10.17</td><td>68.14%</td><td>170.1</td><td>170.1</td></tr><tr><td>Holt-Winters exponential smoothing</td><td>26.09</td><td>186.24%</td><td>150.2</td><td>128.1</td></tr></tbody></table>

### Total Visitors ('000s) by Financial Year (SARIMAX)

<table align="left"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2014</td><td>102.8</td></tr><tr><td>FY2015</td><td>470.6</td></tr><tr><td>FY2016</td><td>551.8</td></tr><tr><td>FY2017</td><td>381.5</td></tr><tr><td>FY2018</td><td>223.3</td></tr><tr><td>FY2019</td><td>0.0</td></tr><tr><td>FY2020</td><td>0.0</td></tr></tbody></table><table align="right"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2021</td><td>0.0</td></tr><tr><td>FY2022</td><td>35.1</td></tr><tr><td>FY2023</td><td>172.6</td></tr><tr><td>FY2024</td><td>170.1</td></tr><tr><td>FY2025</td><td>167.6</td></tr><tr><td>FY2026 (Prediction)</td><td>120.0</td></tr><tr><td>FY2027 (Prediction)</td><td>158.8</td></tr></tbody></table><br clear="all">

![](eval/jj-new-eval-plots/TPM_eval_sarimax_timeplot.png)

![](predict/jj-new-predict-plots/TPM_predict_top3_timeplot.png)
