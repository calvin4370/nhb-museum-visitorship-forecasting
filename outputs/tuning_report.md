# Hyperparameter tuning report

## Search budget

| Model | Museum | Trials | Best value | Best at trial |
|---|---|---|---|---|
| rf | ACM | 50 | 3.882 | 32 |
| rf | NMS | 50 | 17.78 | 35 |
| rf | TPM | 50 | 2.159 | 32 |
| rf | IHC | 50 | 4.746 | 14 |
| rf | MHC | 50 | 13.08 | 19 |
| xgb | ACM | 50 | 4.491 | 33 |
| xgb | NMS | 50 | 19.14 | 33 |
| xgb | TPM | 50 | 2.769 | 22 |
| xgb | IHC | 50 | 4.551 | 41 |
| xgb | MHC | 50 | 12.73 | 1 |
| hw | ACM | 50 | 7.371 | 43 |
| hw | NMS | 50 | 76.81 | 48 |
| hw | TPM | 50 | 7.755 | 41 |
| hw | IHC | 50 | 7.272 | 44 |
| hw | MHC | 50 | 10.35 | 37 |
| sarimax | ACM | 50 | 7.69 | 6 |
| sarimax | NMS | 50 | 26.75 | 33 |
| sarimax | TPM | 50 | 4.446 | 48 |
| sarimax | IHC | 50 | 4.303 | 25 |
| sarimax | MHC | 50 | 10.59 | 6 |

## rf

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| n_estimators | 100 to 1000 step 100 | 900 | 400 | 700 | 900 | 900 |
| max_depth | 5 to 30 | 11 | 7 | 15 | 17 | 19 |
| min_samples_split | 2 to 20 | 10 | 4 | 5 | 2 | 17 |
| min_samples_leaf | 1 to 10 | 5 | 6 | 2 | 7 | 7 |
| max_features | sqrt, log2, None | None | None | None | None | log2 |
| bootstrap | True, False | True | True | False | True | False |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| n_estimators | 0.047 | 0.027 | 0.414 | 0.001 | 0.002 |
| max_depth | 0.014 | 0.378 | 0.035 | 0.009 | 0.010 |
| min_samples_split | 0.019 | 0.059 | 0.063 | 0.013 | 0.014 |
| min_samples_leaf | 0.054 | 0.147 | 0.060 | 0.071 | 0.028 |
| max_features | 0.198 | 0.123 | 0.138 | 0.111 | 0.897 |
| bootstrap | 0.669 | 0.266 | 0.290 | 0.795 | 0.050 |

## xgb

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| n_estimators | 100 to 1000 step 100 | 700 | 700 | 1000 | 1000 | 100 |
| max_depth | 3 to 10 | 3 | 6 | 5 | 7 | 9 |
| learning_rate | 0.01 to 0.3 | 0.0101 | 0.2998 | 0.1282 | 0.1247 | 0.1843 |
| subsample | 0.5 to 1.0 | 0.9947 | 0.5389 | 0.7068 | 0.6858 | 0.854 |
| colsample_bytree | 0.5 to 1.0 | 0.9539 | 0.9956 | 0.8593 | 0.8407 | 0.5103 |
| min_child_weight | 1 to 10 | 10 | 9 | 1 | 1 | 10 |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| n_estimators | 0.032 | 0.007 | 0.026 | 0.051 | 0.070 |
| max_depth | 0.045 | 0.084 | 0.012 | 0.018 | 0.042 |
| learning_rate | 0.060 | 0.134 | 0.025 | 0.152 | 0.436 |
| subsample | 0.422 | 0.417 | 0.067 | 0.139 | 0.174 |
| colsample_bytree | 0.108 | 0.093 | 0.070 | 0.345 | 0.165 |
| min_child_weight | 0.333 | 0.265 | 0.801 | 0.294 | 0.113 |

## hw

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| smoothing_level | 0.0 to 1.0 | 0.5655 | 0.4108 | 0.1742 | 0.7577 | 0.5336 |
| smoothing_trend | 0.0 to 1.0 | 0.05033 | 0.09913 | 0.06758 | 0.09069 | 0.009219 |
| smoothing_seasonal | 0.0 to 1.0 | 0.02838 | 0.8379 | 0.7462 | 0.007799 | 0.3363 |
| trend | add, mul | add | add | add | add | add |
| seasonal | add, mul | add | add | add | add | add |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| smoothing_level | 0.138 | 0.782 | 0.859 | 0.003 | 0.117 |
| smoothing_trend | 0.731 | 0.157 | 0.031 | 0.199 | 0.476 |
| smoothing_seasonal | 0.131 | 0.061 | 0.110 | 0.798 | 0.407 |
| trend | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| seasonal | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

## sarimax

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| p | 0 to 5 | 1 | 5 | 1 | 2 | 1 |
| d | 0 to 2 | 0 | 0 | 0 | 0 | 0 |
| q | 0 to 5 | 4 | 1 | 4 | 0 | 4 |
| P | 0 to 2 | 1 | 0 | 1 | 2 | 1 |
| D | 0 to 1 | 0 | 1 | 1 | 1 | 0 |
| Q | 0 to 2 | 1 | 1 | 0 | 2 | 1 |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| p | 0.038 | 0.003 | 0.003 | 0.175 | 0.070 |
| d | 0.726 | 0.940 | 0.978 | 0.694 | 0.758 |
| q | 0.058 | 0.005 | 0.013 | 0.026 | 0.019 |
| P | 0.034 | 0.016 | 0.001 | 0.021 | 0.005 |
| D | 0.006 | 0.034 | 0.002 | 0.060 | 0.047 |
| Q | 0.137 | 0.003 | 0.003 | 0.024 | 0.101 |
