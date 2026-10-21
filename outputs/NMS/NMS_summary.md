## Summary Report (NMS)

```
Branch:    test/run-pipelines-8e
Generated: 20 Oct 2026 5.38pm
```

### Model Evaluation Results + Predictions

<table><thead><tr><th>Model</th><th>RMSE</th><th>MAPE</th><th>FY2026</th><th>FY2027</th></tr></thead><tbody><tr><td>XGBoost</td><td>18.08</td><td>18.17%</td><td>1,032.9</td><td>994.0</td></tr><tr><td>SARIMAX</td><td>20.01</td><td>19.07%</td><td>977.0</td><td>983.4</td></tr><tr><td>Support Vector Regression</td><td>21.10</td><td>15.83%</td><td>918.7</td><td>899.6</td></tr><tr><td>Random Forest Regressor</td><td>21.43</td><td>18.17%</td><td>1,013.0</td><td>966.7</td></tr><tr><td>LSTM</td><td>22.72</td><td>18.73%</td><td>930.9</td><td>927.3</td></tr><tr><td>Baseline Monthly Mean</td><td>36.40</td><td>30.13%</td><td>1,040.0</td><td>1,040.0</td></tr><tr><td>Holt-Winters exponential smoothing</td><td>43.75</td><td>35.34%</td><td>1,275.8</td><td>1,375.8</td></tr></tbody></table>

### Total Visitors ('000s) by Financial Year (XGBoost)

<table align="left"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2014</td><td>153.4</td></tr><tr><td>FY2015</td><td>783.1</td></tr><tr><td>FY2016</td><td>811.4</td></tr><tr><td>FY2017</td><td>930.7</td></tr><tr><td>FY2018</td><td>977.6</td></tr><tr><td>FY2019</td><td>1,003.8</td></tr><tr><td>FY2020</td><td>359.7</td></tr></tbody></table><table align="right"><thead><tr><th width="138">FY</th><th width="148">Total Visitors ('000s)</th></tr></thead><tbody><tr><td>FY2021</td><td>369.6</td></tr><tr><td>FY2022</td><td>852.9</td></tr><tr><td>FY2023</td><td>1,065.4</td></tr><tr><td>FY2024</td><td>998.1</td></tr><tr><td>FY2025</td><td>1,056.5</td></tr><tr><td>FY2026 (Prediction)</td><td>1,032.9</td></tr><tr><td>FY2027 (Prediction)</td><td>994.0</td></tr></tbody></table><br clear="all">

![](eval/jj-new-eval-plots/NMS_eval_xgb_timeplot.png)

![](predict/jj-new-predict-plots/NMS_predict_top3_timeplot.png)
