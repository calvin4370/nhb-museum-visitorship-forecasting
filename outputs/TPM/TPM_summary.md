## Summary Report (TPM)

```
Branch:    test/run-pipelines-8c2
Generated: 21 Sep 2026 3.36pm
```

### Model Evaluation Results + Predictions

<table><thead><tr><th>Model</th><th>RMSE</th><th>MAPE</th><th>FY2026</th><th>FY2027</th></tr></thead><tbody><tr><td>SARIMAX</td><td>4.37</td><td>22.59%</td><td>154.0</td><td>178.5</td></tr><tr><td>Baseline Monthly Mean</td><td>10.17</td><td>68.14%</td><td>170.1</td><td>170.1</td></tr><tr><td>XGBoost</td><td>10.41</td><td>62.74%</td><td>194.9</td><td>209.1</td></tr><tr><td>Holt-Winters exponential smoothing</td><td>12.93</td><td>88.56%</td><td>166.6</td><td>171.6</td></tr><tr><td>Support Vector Regression</td><td>18.60</td><td>110.72%</td><td>244.5</td><td>312.9</td></tr><tr><td>LSTM</td><td>20.50</td><td>129.79%</td><td>260.3</td><td>305.5</td></tr><tr><td>Random Forest Regressor</td><td>20.87</td><td>113.11%</td><td>218.1</td><td>237.8</td></tr></tbody></table>

### Total Visitors ('000s) by Financial Year (SARIMAX)

<table align="left"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2014</td><td>102.8</td></tr><tr><td>FY2015</td><td>470.6</td></tr><tr><td>FY2016</td><td>551.8</td></tr><tr><td>FY2017</td><td>381.5</td></tr><tr><td>FY2018</td><td>223.3</td></tr><tr><td>FY2019</td><td>0.0</td></tr><tr><td>FY2020</td><td>0.0</td></tr></tbody></table><table align="right"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2021</td><td>0.0</td></tr><tr><td>FY2022</td><td>35.1</td></tr><tr><td>FY2023</td><td>172.6</td></tr><tr><td>FY2024</td><td>170.1</td></tr><tr><td>FY2025</td><td>167.6</td></tr><tr><td>FY2026 (Prediction)</td><td>154.0</td></tr><tr><td>FY2027 (Prediction)</td><td>178.5</td></tr></tbody></table><br clear="all">

![](eval/jj-new-eval-plots/TPM_eval_sarimax_timeplot.png)

![](predict/jj-new-predict-plots/TPM_predict_top3_timeplot.png)
