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
| n_estimators | 0.031 | 0.025 | 0.036 | 0.012 | 0.013 |
| max_depth | 0.004 | 0.453 | 0.664 | 0.011 | 0.000 |
| min_samples_split | 0.075 | 0.079 | 0.005 | 0.017 | 0.004 |
| min_samples_leaf | 0.005 | 0.080 | 0.036 | 0.069 | 0.047 |
| max_features | 0.276 | 0.158 | 0.061 | 0.131 | 0.877 |
| bootstrap | 0.608 | 0.206 | 0.197 | 0.760 | 0.059 |

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
| n_estimators | 0.052 | 0.039 | 0.032 | 0.008 | 0.021 |
| max_depth | 0.017 | 0.118 | 0.022 | 0.093 | 0.018 |
| learning_rate | 0.280 | 0.122 | 0.035 | 0.055 | 0.103 |
| subsample | 0.473 | 0.475 | 0.158 | 0.254 | 0.668 |
| colsample_bytree | 0.119 | 0.089 | 0.315 | 0.020 | 0.092 |
| min_child_weight | 0.059 | 0.157 | 0.438 | 0.570 | 0.099 |

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
| kernel | 0.801 | 0.903 | 0.805 | 0.955 | 0.743 |
| C | 0.013 | 0.027 | 0.043 | 0.023 | 0.111 |
| epsilon | 0.186 | 0.071 | 0.151 | 0.021 | 0.146 |

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
| smoothing_level | 0.113 | 0.785 | 0.813 | 0.037 | 0.102 |
| smoothing_trend | 0.774 | 0.132 | 0.065 | 0.151 | 0.409 |
| smoothing_seasonal | 0.113 | 0.084 | 0.122 | 0.812 | 0.489 |
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
| p | 0.065 | 0.015 | 0.138 | 0.044 | 0.048 |
| d | 0.499 | 0.329 | 0.286 | 0.676 | 0.051 |
| q | 0.097 | 0.396 | 0.306 | 0.239 | 0.837 |
| P | 0.111 | 0.111 | 0.117 | 0.021 | 0.017 |
| D | 0.171 | 0.033 | 0.067 | 0.008 | 0.029 |
| Q | 0.057 | 0.117 | 0.087 | 0.013 | 0.018 |
