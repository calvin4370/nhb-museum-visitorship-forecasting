# Hyperparameter tuning report

## Search budget

| Model | Museum | Trials | Best value | Best at trial |
|---|---|---|---|---|
| rf | ACM | 50 | 3.612 | 24 |
| rf | NMS | 50 | 17.13 | 28 |
| rf | TPM | 50 | 1.522 | 34 |
| rf | IHC | 50 | 4.519 | 37 |
| rf | MHC | 50 | 13.2 | 48 |
| xgb | ACM | 50 | 3.639 | 44 |
| xgb | NMS | 50 | 14.61 | 43 |
| xgb | TPM | 50 | 1.273 | 33 |
| xgb | IHC | 50 | 4.137 | 28 |
| xgb | MHC | 50 | 11.78 | 49 |
| svr | ACM | 50 | 3.842 | 42 |
| svr | NMS | 50 | 18.6 | 32 |
| svr | TPM | 50 | 1.659 | 32 |
| svr | IHC | 50 | 3.067 | 41 |
| svr | MHC | 50 | 8.63 | 10 |
| hw | ACM | 50 | 7.371 | 43 |
| hw | NMS | 50 | 76.81 | 48 |
| hw | TPM | 50 | 7.755 | 41 |
| hw | IHC | 50 | 7.272 | 44 |
| hw | MHC | 50 | 10.35 | 37 |
| sarimax | ACM | 50 | 9.332 | 43 |
| sarimax | NMS | 50 | 24.21 | 5 |
| sarimax | TPM | 50 | 3.546 | 44 |
| sarimax | IHC | 50 | 2.869 | 12 |
| sarimax | MHC | 50 | 10 | 27 |

## rf

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| n_estimators | 100 to 1000 step 100 | 200 | 200 | 400 | 600 | 400 |
| max_depth | 5 to 30 | 15 | 24 | 10 | 28 | 7 |
| min_samples_split | 2 to 20 | 4 | 5 | 2 | 5 | 4 |
| min_samples_leaf | 1 to 10 | 4 | 6 | 1 | 1 | 2 |
| max_features | sqrt, log2, None | None | None | log2 | sqrt | sqrt |
| bootstrap | True, False | True | True | False | True | True |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| n_estimators | 0.071 | 0.042 | 0.025 | 0.044 | 0.003 |
| max_depth | 0.031 | 0.030 | 0.181 | 0.006 | 0.004 |
| min_samples_split | 0.019 | 0.042 | 0.048 | 0.008 | 0.003 |
| min_samples_leaf | 0.044 | 0.237 | 0.044 | 0.098 | 0.012 |
| max_features | 0.254 | 0.133 | 0.329 | 0.316 | 0.973 |
| bootstrap | 0.580 | 0.516 | 0.373 | 0.529 | 0.005 |

## xgb

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| n_estimators | 100 to 1000 step 100 | 200 | 800 | 900 | 200 | 1000 |
| max_depth | 3 to 10 | 3 | 10 | 10 | 6 | 4 |
| learning_rate | 0.01 to 0.3 | 0.01054 | 0.2642 | 0.07964 | 0.1363 | 0.09155 |
| subsample | 0.5 to 1.0 | 0.9624 | 0.6997 | 0.9602 | 0.5819 | 0.7205 |
| colsample_bytree | 0.5 to 1.0 | 0.9869 | 0.8057 | 0.8466 | 0.6794 | 0.6528 |
| min_child_weight | 1 to 10 | 9 | 7 | 2 | 3 | 1 |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| n_estimators | 0.066 | 0.039 | 0.037 | 0.018 | 0.059 |
| max_depth | 0.246 | 0.044 | 0.041 | 0.012 | 0.014 |
| learning_rate | 0.377 | 0.017 | 0.078 | 0.097 | 0.478 |
| subsample | 0.164 | 0.041 | 0.063 | 0.177 | 0.047 |
| colsample_bytree | 0.088 | 0.036 | 0.213 | 0.163 | 0.068 |
| min_child_weight | 0.059 | 0.824 | 0.568 | 0.532 | 0.333 |

## svr

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| kernel | linear, rbf, poly | linear | linear | rbf | linear | rbf |
| C | 0.001 to 1000.0 | 0.8937 | 2.947 | 112.2 | 251.3 | 395.2 |
| epsilon | 0.001 to 1.0 | 0.2453 | 0.01087 | 0.06085 | 0.9023 | 0.1226 |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| kernel | 0.941 | 0.704 | 0.848 | 0.907 | 0.907 |
| C | 0.028 | 0.286 | 0.132 | 0.026 | 0.024 |
| epsilon | 0.031 | 0.010 | 0.020 | 0.067 | 0.069 |

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
| smoothing_level | 0.101 | 0.765 | 0.863 | 0.015 | 0.106 |
| smoothing_trend | 0.777 | 0.162 | 0.064 | 0.191 | 0.400 |
| smoothing_seasonal | 0.122 | 0.073 | 0.073 | 0.794 | 0.495 |
| trend | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| seasonal | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

## sarimax

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| p | 0 to 5 | 3 | 3 | 3 | 1 | 3 |
| d | 0 to 2 | 1 | 0 | 1 | 0 | 0 |
| q | 0 to 5 | 2 | 0 | 3 | 5 | 1 |
| P | 0 to 2 | 2 | 2 | 1 | 0 | 0 |
| D | 0 to 1 | 0 | 1 | 0 | 1 | 0 |
| Q | 0 to 2 | 1 | 2 | 1 | 2 | 0 |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| p | 0.097 | 0.063 | 0.068 | 0.032 | 0.079 |
| d | 0.407 | 0.566 | 0.375 | 0.520 | 0.446 |
| q | 0.208 | 0.038 | 0.097 | 0.049 | 0.260 |
| P | 0.082 | 0.104 | 0.025 | 0.045 | 0.142 |
| D | 0.077 | 0.029 | 0.375 | 0.008 | 0.052 |
| Q | 0.129 | 0.199 | 0.060 | 0.345 | 0.021 |
