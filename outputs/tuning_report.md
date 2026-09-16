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
| sarimax | ACM | 50 | 9.495 | 40 |
| sarimax | NMS | 50 | 22.32 | 48 |
| sarimax | TPM | 50 | 3.68 | 48 |
| sarimax | IHC | 50 | 3.61 | 43 |
| sarimax | MHC | 50 | 9.865 | 38 |

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
| n_estimators | 0.023 | 0.017 | 0.052 | 0.013 | 0.013 |
| max_depth | 0.033 | 0.469 | 0.699 | 0.011 | 0.001 |
| min_samples_split | 0.089 | 0.032 | 0.007 | 0.018 | 0.002 |
| min_samples_leaf | 0.034 | 0.093 | 0.035 | 0.071 | 0.041 |
| max_features | 0.178 | 0.141 | 0.045 | 0.150 | 0.867 |
| bootstrap | 0.644 | 0.248 | 0.163 | 0.738 | 0.075 |

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
| n_estimators | 0.062 | 0.057 | 0.027 | 0.015 | 0.019 |
| max_depth | 0.017 | 0.127 | 0.012 | 0.046 | 0.031 |
| learning_rate | 0.336 | 0.118 | 0.032 | 0.048 | 0.127 |
| subsample | 0.488 | 0.451 | 0.133 | 0.296 | 0.667 |
| colsample_bytree | 0.062 | 0.076 | 0.347 | 0.024 | 0.067 |
| min_child_weight | 0.035 | 0.171 | 0.449 | 0.571 | 0.089 |

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
| kernel | 0.826 | 0.948 | 0.813 | 0.964 | 0.723 |
| C | 0.019 | 0.025 | 0.052 | 0.016 | 0.102 |
| epsilon | 0.155 | 0.027 | 0.135 | 0.020 | 0.175 |

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
| smoothing_level | 0.149 | 0.766 | 0.816 | 0.017 | 0.103 |
| smoothing_trend | 0.725 | 0.158 | 0.039 | 0.219 | 0.341 |
| smoothing_seasonal | 0.127 | 0.076 | 0.144 | 0.764 | 0.555 |
| trend | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| seasonal | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

## sarimax

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| p | 0 to 5 | 0 | 0 | 3 | 1 | 2 |
| d | 0 to 2 | 1 | 0 | 0 | 0 | 0 |
| q | 0 to 5 | 3 | 0 | 1 | 1 | 1 |
| P | 0 to 2 | 2 | 0 | 1 | 0 | 2 |
| D | 0 to 1 | 0 | 1 | 1 | 1 | 0 |
| Q | 0 to 2 | 0 | 1 | 0 | 2 | 0 |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| p | 0.074 | 0.010 | 0.003 | 0.007 | 0.026 |
| d | 0.678 | 0.917 | 0.978 | 0.969 | 0.912 |
| q | 0.090 | 0.006 | 0.005 | 0.002 | 0.032 |
| P | 0.053 | 0.010 | 0.001 | 0.004 | 0.015 |
| D | 0.016 | 0.013 | 0.011 | 0.007 | 0.004 |
| Q | 0.089 | 0.044 | 0.003 | 0.011 | 0.011 |
