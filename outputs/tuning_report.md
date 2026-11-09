# Hyperparameter tuning report

## Search budget

| Model | Museum | Trials | Completed | Best value | Best at trial |
|---|---|---|---|---|---|
| rf | ACM | 100 | 100 | 3.781 | 57 |
| rf | NMS | 100 | 100 | 17.61 | 80 |
| rf | TPM | 100 | 100 | 1.557 | 51 |
| rf | IHC | 100 | 100 | 4.815 | 24 |
| rf | MHC | 100 | 100 | 13.06 | 57 |
| xgb | ACM | 100 | 100 | 4.238 | 74 |
| xgb | NMS | 100 | 100 | 19.75 | 69 |
| xgb | TPM | 100 | 100 | 0.9773 | 52 |
| xgb | IHC | 100 | 100 | 3.971 | 94 |
| xgb | MHC | 100 | 100 | 11.77 | 93 |
| svr | ACM | 100 | 100 | 4.21 | 79 |
| svr | NMS | 100 | 100 | 17.65 | 81 |
| svr | TPM | 100 | 100 | 1.917 | 47 |
| svr | IHC | 100 | 100 | 3.341 | 98 |
| svr | MHC | 100 | 100 | 8.018 | 73 |
| hw | ACM | 100 | 100 | 6.757 | 93 |
| hw | NMS | 100 | 100 | 34.74 | 94 |
| hw | TPM | 100 | 100 | 5.915 | 94 |
| hw | IHC | 100 | 100 | 9.526 | 25 |
| hw | MHC | 100 | 100 | 8.351 | 63 |
| sarimax | ACM | 100 | 100 | 7.988 | 50 |
| sarimax | NMS | 100 | 100 | 22.32 | 48 |
| sarimax | TPM | 100 | 100 | 2.899 | 87 |
| sarimax | IHC | 100 | 100 | 3.214 | 3 |
| sarimax | MHC | 100 | 100 | 9.865 | 38 |

## rf

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| n_estimators | 100 to 1000 step 100 | 400 | 200 | 1000 | 1000 | 1000 |
| max_depth | 5 to 30 | 13 | 14 | 20 | 27 | 20 |
| min_samples_split | 2 to 20 | 10 | 12 | 4 | 2 | 7 |
| min_samples_leaf | 1 to 10 | 1 | 7 | 1 | 7 | 7 |
| max_features | sqrt, log2, None | None | None | None | None | log2 |
| bootstrap | True, False | True | True | False | True | False |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| n_estimators | 0.007 | 0.006 | 0.070 | 0.009 | 0.007 |
| max_depth | 0.015 | 0.012 | 0.139 | 0.026 | 0.002 |
| min_samples_split | 0.072 | 0.022 | 0.042 | 0.018 | 0.003 |
| min_samples_leaf | 0.011 | 0.121 | 0.324 | 0.139 | 0.054 |
| max_features | 0.203 | 0.254 | 0.168 | 0.249 | 0.870 |
| bootstrap | 0.691 | 0.585 | 0.256 | 0.559 | 0.065 |

## xgb

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| n_estimators | 100 to 1000 step 100 | 100 | 400 | 400 | 600 | 100 |
| max_depth | 3 to 10 | 10 | 10 | 4 | 6 | 4 |
| learning_rate | 0.01 to 0.3 | 0.03785 | 0.2799 | 0.08636 | 0.2886 | 0.2538 |
| subsample | 0.5 to 1.0 | 0.6168 | 0.6875 | 0.9642 | 0.7585 | 0.9429 |
| colsample_bytree | 0.5 to 1.0 | 0.8668 | 0.6035 | 0.9962 | 0.8799 | 0.912 |
| min_child_weight | 1 to 10 | 1 | 8 | 4 | 1 | 2 |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| n_estimators | 0.048 | 0.021 | 0.014 | 0.042 | 0.011 |
| max_depth | 0.024 | 0.012 | 0.005 | 0.063 | 0.042 |
| learning_rate | 0.252 | 0.028 | 0.014 | 0.148 | 0.110 |
| subsample | 0.536 | 0.700 | 0.172 | 0.268 | 0.680 |
| colsample_bytree | 0.119 | 0.028 | 0.249 | 0.122 | 0.035 |
| min_child_weight | 0.021 | 0.211 | 0.546 | 0.357 | 0.121 |

## svr

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| kernel | linear, rbf, poly | linear | linear | rbf | linear | linear |
| C | 0.001 to 1000.0 | 1.831 | 14.34 | 292.6 | 5.96 | 0.452 |
| epsilon | 0.001 to 1.0 | 0.01807 | 0.1184 | 0.04705 | 0.001233 | 0.2813 |
| gamma | 0.001 to 1.0 | n/a | n/a | 0.02888 | n/a | n/a |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| kernel | 0.862 | 0.923 | 0.747 | 0.944 | 0.716 |
| C | 0.018 | 0.020 | 0.014 | 0.040 | 0.158 |
| epsilon | 0.120 | 0.058 | 0.238 | 0.015 | 0.126 |
| gamma | nan | nan | nan | nan | nan |

## hw

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| smoothing_level | 0.0 to 1.0 | 0.6051 | 0.9379 | 0.08809 | 0.001166 | 0.846 |
| smoothing_trend | 0.0 to 1.0 | 0.1075 | 0.03228 | 0.2318 | 0.9629 | 0.001514 |
| smoothing_seasonal | 0.0 to 1.0 | 0.0694 | 0.13 | 0.6972 | 0.9138 | 0.03448 |
| trend | add, mul | add | add | add | add | add |
| seasonal | add, mul | add | add | add | add | add |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| smoothing_level | 0.068 | 0.180 | 0.804 | 0.658 | 0.120 |
| smoothing_trend | 0.861 | 0.810 | 0.098 | 0.247 | 0.521 |
| smoothing_seasonal | 0.070 | 0.011 | 0.097 | 0.095 | 0.360 |
| trend | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| seasonal | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

## sarimax

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| p | 0 to 5 | 0 | 0 | 1 | 2 | 2 |
| d | 0 to 2 | 1 | 0 | 0 | 0 | 0 |
| q | 0 to 5 | 3 | 0 | 0 | 3 | 1 |
| P | 0 to 2 | 2 | 0 | 1 | 0 | 2 |
| D | 0 to 1 | 0 | 1 | 1 | 0 | 0 |
| Q | 0 to 2 | 1 | 1 | 0 | 1 | 0 |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| p | 0.020 | 0.009 | 0.004 | 0.026 | 0.022 |
| d | 0.833 | 0.947 | 0.974 | 0.907 | 0.939 |
| q | 0.041 | 0.021 | 0.006 | 0.021 | 0.016 |
| P | 0.073 | 0.005 | 0.001 | 0.014 | 0.016 |
| D | 0.011 | 0.017 | 0.013 | 0.020 | 0.002 |
| Q | 0.024 | 0.002 | 0.003 | 0.011 | 0.005 |
