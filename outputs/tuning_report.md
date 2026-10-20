# Hyperparameter tuning report

## Search budget

| Model | Museum | Trials | Best value | Best at trial |
|---|---|---|---|---|
| rf | ACM | 50 | 3.92 | 13 |
| rf | NMS | 50 | 17.73 | 35 |
| rf | TPM | 50 | 1.487 | 16 |
| rf | IHC | 50 | 4.658 | 43 |
| rf | MHC | 50 | 13.07 | 17 |
| xgb | ACM | 50 | 4.103 | 14 |
| xgb | NMS | 50 | 20.37 | 19 |
| xgb | TPM | 50 | 0.9548 | 43 |
| xgb | IHC | 50 | 4.348 | 24 |
| xgb | MHC | 50 | 12.38 | 0 |
| svr | ACM | 50 | 4.837 | 26 |
| svr | NMS | 50 | 17.09 | 44 |
| svr | TPM | 50 | 1.833 | 45 |
| svr | IHC | 50 | 3.376 | 45 |
| svr | MHC | 50 | 8.175 | 25 |
| hw | ACM | 50 | 7.371 | 43 |
| hw | NMS | 50 | 76.81 | 48 |
| hw | TPM | 50 | 7.755 | 41 |
| hw | IHC | 50 | 7.272 | 44 |
| hw | MHC | 50 | 10.35 | 37 |
| sarimax | ACM | 50 | 9.016 | 43 |
| sarimax | NMS | 50 | 26.8 | 19 |
| sarimax | TPM | 50 | 4.236 | 49 |
| sarimax | IHC | 50 | 3.61 | 43 |
| sarimax | MHC | 50 | 9.865 | 38 |

## rf

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| n_estimators | 100 to 1000 step 100 | 300 | 400 | 300 | 200 | 900 |
| max_depth | 5 to 30 | 17 | 30 | 21 | 13 | 24 |
| min_samples_split | 2 to 20 | 9 | 8 | 7 | 10 | 7 |
| min_samples_leaf | 1 to 10 | 4 | 6 | 1 | 2 | 7 |
| max_features | sqrt, log2, None | None | None | sqrt | None | sqrt |
| bootstrap | True, False | True | True | False | True | False |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| n_estimators | 0.018 | 0.061 | 0.051 | 0.024 | 0.010 |
| max_depth | 0.006 | 0.024 | 0.124 | 0.016 | 0.001 |
| min_samples_split | 0.121 | 0.052 | 0.094 | 0.015 | 0.004 |
| min_samples_leaf | 0.015 | 0.012 | 0.138 | 0.068 | 0.056 |
| max_features | 0.179 | 0.209 | 0.377 | 0.142 | 0.849 |
| bootstrap | 0.661 | 0.642 | 0.217 | 0.736 | 0.081 |

## xgb

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| n_estimators | 100 to 1000 step 100 | 1000 | 400 | 900 | 1000 | 400 |
| max_depth | 3 to 10 | 6 | 5 | 9 | 7 | 10 |
| learning_rate | 0.01 to 0.3 | 0.1496 | 0.2657 | 0.04386 | 0.1639 | 0.2223 |
| subsample | 0.5 to 1.0 | 0.7766 | 0.505 | 0.8963 | 0.6987 | 0.7993 |
| colsample_bytree | 0.5 to 1.0 | 0.9086 | 0.8303 | 0.7645 | 0.8834 | 0.578 |
| min_child_weight | 1 to 10 | 2 | 8 | 2 | 1 | 2 |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| n_estimators | 0.041 | 0.031 | 0.026 | 0.020 | 0.016 |
| max_depth | 0.050 | 0.036 | 0.018 | 0.053 | 0.028 |
| learning_rate | 0.080 | 0.093 | 0.031 | 0.052 | 0.100 |
| subsample | 0.755 | 0.174 | 0.108 | 0.298 | 0.640 |
| colsample_bytree | 0.027 | 0.063 | 0.108 | 0.023 | 0.133 |
| min_child_weight | 0.048 | 0.602 | 0.709 | 0.554 | 0.083 |

## svr

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| kernel | linear, rbf, poly | linear | linear | rbf | linear | linear |
| C | 0.001 to 1000.0 | 1.122 | 3.273 | 36.45 | 3.804 | 0.5914 |
| epsilon | 0.001 to 1.0 | 0.6058 | 0.533 | 0.01905 | 0.001941 | 0.2466 |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| kernel | 0.872 | 0.911 | 0.759 | 0.961 | 0.749 |
| C | 0.007 | 0.019 | 0.150 | 0.019 | 0.106 |
| epsilon | 0.121 | 0.069 | 0.090 | 0.020 | 0.145 |

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
| smoothing_level | 0.150 | 0.823 | 0.860 | 0.030 | 0.121 |
| smoothing_trend | 0.759 | 0.127 | 0.057 | 0.191 | 0.379 |
| smoothing_seasonal | 0.091 | 0.050 | 0.083 | 0.779 | 0.499 |
| trend | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| seasonal | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

## sarimax

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| p | 0 to 5 | 0 | 4 | 5 | 1 | 2 |
| d | 0 to 2 | 0 | 0 | 1 | 0 | 0 |
| q | 0 to 5 | 0 | 5 | 2 | 1 | 1 |
| P | 0 to 2 | 1 | 1 | 0 | 0 | 2 |
| D | 0 to 1 | 1 | 1 | 0 | 1 | 0 |
| Q | 0 to 2 | 1 | 1 | 0 | 2 | 0 |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| p | 0.066 | 0.005 | 0.093 | 0.013 | 0.025 |
| d | 0.366 | 0.966 | 0.891 | 0.965 | 0.913 |
| q | 0.116 | 0.006 | 0.010 | 0.002 | 0.029 |
| P | 0.034 | 0.004 | 0.002 | 0.003 | 0.018 |
| D | 0.348 | 0.020 | 0.004 | 0.007 | 0.005 |
| Q | 0.069 | 0.000 | 0.001 | 0.010 | 0.010 |
