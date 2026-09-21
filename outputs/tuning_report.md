# Hyperparameter tuning report

## Search budget

| Model | Museum | Trials | Best value | Best at trial |
|---|---|---|---|---|
| rf | ACM | 50 | 3.917 | 13 |
| rf | NMS | 50 | 17.74 | 33 |
| rf | TPM | 50 | 1.563 | 49 |
| rf | IHC | 50 | 4.658 | 43 |
| rf | MHC | 50 | 13.07 | 17 |
| xgb | ACM | 50 | 4.282 | 44 |
| xgb | NMS | 50 | 19.93 | 39 |
| xgb | TPM | 50 | 1.067 | 48 |
| xgb | IHC | 50 | 4.348 | 24 |
| xgb | MHC | 50 | 12.38 | 0 |
| svr | ACM | 50 | 4.3 | 18 |
| svr | NMS | 50 | 17.73 | 25 |
| svr | TPM | 50 | 1.917 | 47 |
| svr | IHC | 50 | 3.376 | 45 |
| svr | MHC | 50 | 8.175 | 25 |
| hw | ACM | 50 | 7.371 | 43 |
| hw | NMS | 50 | 76.81 | 48 |
| hw | TPM | 50 | 7.755 | 41 |
| hw | IHC | 50 | 7.272 | 44 |
| hw | MHC | 50 | 10.35 | 37 |
| sarimax | ACM | 50 | 3.655 | 30 |
| sarimax | NMS | 50 | 21.48 | 10 |
| sarimax | TPM | 50 | 2.448 | 22 |
| sarimax | IHC | 50 | 2.742 | 18 |
| sarimax | MHC | 50 | 8.624 | 7 |

## rf

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| n_estimators | 100 to 1000 step 100 | 300 | 300 | 900 | 200 | 900 |
| max_depth | 5 to 30 | 17 | 6 | 20 | 13 | 24 |
| min_samples_split | 2 to 20 | 9 | 3 | 4 | 10 | 7 |
| min_samples_leaf | 1 to 10 | 4 | 6 | 1 | 2 | 7 |
| max_features | sqrt, log2, None | None | None | None | None | sqrt |
| bootstrap | True, False | True | True | False | True | False |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| n_estimators | 0.033 | 0.011 | 0.046 | 0.010 | 0.026 |
| max_depth | 0.024 | 0.462 | 0.624 | 0.016 | 0.001 |
| min_samples_split | 0.100 | 0.093 | 0.034 | 0.017 | 0.006 |
| min_samples_leaf | 0.028 | 0.079 | 0.040 | 0.048 | 0.064 |
| max_features | 0.174 | 0.116 | 0.059 | 0.127 | 0.847 |
| bootstrap | 0.642 | 0.238 | 0.197 | 0.782 | 0.056 |

## xgb

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| n_estimators | 100 to 1000 step 100 | 100 | 600 | 500 | 1000 | 400 |
| max_depth | 3 to 10 | 10 | 4 | 5 | 7 | 10 |
| learning_rate | 0.01 to 0.3 | 0.02788 | 0.2776 | 0.0917 | 0.1639 | 0.2223 |
| subsample | 0.5 to 1.0 | 0.5949 | 0.5412 | 0.9656 | 0.6987 | 0.7993 |
| colsample_bytree | 0.5 to 1.0 | 0.8528 | 0.5052 | 0.8344 | 0.8834 | 0.578 |
| min_child_weight | 1 to 10 | 1 | 9 | 4 | 1 | 2 |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| n_estimators | 0.045 | 0.033 | 0.029 | 0.017 | 0.024 |
| max_depth | 0.024 | 0.096 | 0.011 | 0.069 | 0.019 |
| learning_rate | 0.272 | 0.098 | 0.037 | 0.076 | 0.125 |
| subsample | 0.484 | 0.502 | 0.128 | 0.245 | 0.595 |
| colsample_bytree | 0.130 | 0.057 | 0.419 | 0.028 | 0.119 |
| min_child_weight | 0.046 | 0.214 | 0.376 | 0.565 | 0.119 |

## svr

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| kernel | linear, rbf, poly | linear | linear | rbf | linear | linear |
| C | 0.001 to 1000.0 | 2.102 | 13.32 | 292.6 | 3.804 | 0.5914 |
| epsilon | 0.001 to 1.0 | 0.03556 | 0.06662 | 0.04705 | 0.001941 | 0.2466 |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| kernel | 0.757 | 0.928 | 0.817 | 0.957 | 0.748 |
| C | 0.019 | 0.014 | 0.058 | 0.024 | 0.111 |
| epsilon | 0.224 | 0.058 | 0.126 | 0.019 | 0.140 |

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
| smoothing_level | 0.134 | 0.818 | 0.861 | 0.035 | 0.105 |
| smoothing_trend | 0.761 | 0.148 | 0.048 | 0.192 | 0.477 |
| smoothing_seasonal | 0.106 | 0.034 | 0.091 | 0.773 | 0.418 |
| trend | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| seasonal | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

## sarimax

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| p | 0 to 5 | 4 | 5 | 2 | 0 | 0 |
| d | 0 to 2 | 0 | 1 | 1 | 1 | 2 |
| q | 0 to 5 | 0 | 5 | 3 | 2 | 1 |
| P | 0 to 2 | 0 | 2 | 1 | 1 | 1 |
| D | 0 to 1 | 1 | 1 | 1 | 0 | 0 |
| Q | 0 to 2 | 1 | 2 | 0 | 0 | 1 |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| p | 0.041 | 0.019 | 0.088 | 0.054 | 0.051 |
| d | 0.413 | 0.371 | 0.285 | 0.639 | 0.049 |
| q | 0.070 | 0.379 | 0.348 | 0.273 | 0.848 |
| P | 0.088 | 0.046 | 0.114 | 0.019 | 0.012 |
| D | 0.298 | 0.042 | 0.056 | 0.006 | 0.033 |
| Q | 0.091 | 0.144 | 0.109 | 0.009 | 0.007 |
