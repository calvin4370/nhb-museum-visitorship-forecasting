# Hyperparameter tuning report

## Search budget

| Model | Museum | Trials | Completed | Best value | Best at trial |
|---|---|---|---|---|---|
| rf | ACM | 50 | 50 | 3.917 | 13 |
| rf | NMS | 50 | 50 | 17.74 | 33 |
| rf | TPM | 50 | 50 | 1.563 | 49 |
| rf | IHC | 50 | 50 | 4.658 | 43 |
| rf | MHC | 50 | 50 | 13.07 | 17 |
| xgb | ACM | 50 | 50 | 4.282 | 44 |
| xgb | NMS | 50 | 50 | 19.93 | 39 |
| xgb | TPM | 50 | 50 | 1.067 | 48 |
| xgb | IHC | 50 | 50 | 4.348 | 24 |
| xgb | MHC | 50 | 50 | 12.38 | 0 |
| svr | ACM | 50 | 50 | 4.3 | 18 |
| svr | NMS | 50 | 50 | 17.73 | 25 |
| svr | TPM | 50 | 50 | 1.917 | 47 |
| svr | IHC | 50 | 50 | 3.376 | 45 |
| svr | MHC | 50 | 50 | 8.175 | 25 |
| hw | ACM | 50 | 50 | 7.371 | 43 |
| hw | NMS | 50 | 50 | 76.81 | 48 |
| hw | TPM | 50 | 50 | 7.755 | 41 |
| hw | IHC | 50 | 50 | 7.272 | 44 |
| hw | MHC | 50 | 50 | 10.35 | 37 |
| sarimax | ACM | 50 | 50 | 9.495 | 40 |
| sarimax | NMS | 50 | 50 | 22.32 | 48 |
| sarimax | TPM | 50 | 50 | 3.68 | 48 |
| sarimax | IHC | 50 | 50 | 3.61 | 43 |
| sarimax | MHC | 50 | 50 | 9.865 | 38 |

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
| n_estimators | 0.003 | 0.022 | 0.050 | 0.022 | 0.012 |
| max_depth | 0.010 | 0.511 | 0.641 | 0.008 | 0.003 |
| min_samples_split | 0.103 | 0.051 | 0.023 | 0.026 | 0.003 |
| min_samples_leaf | 0.012 | 0.068 | 0.033 | 0.063 | 0.039 |
| max_features | 0.179 | 0.128 | 0.060 | 0.118 | 0.881 |
| bootstrap | 0.694 | 0.221 | 0.194 | 0.764 | 0.061 |

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
| n_estimators | 0.085 | 0.029 | 0.037 | 0.018 | 0.017 |
| max_depth | 0.026 | 0.118 | 0.017 | 0.060 | 0.029 |
| learning_rate | 0.222 | 0.141 | 0.026 | 0.053 | 0.098 |
| subsample | 0.519 | 0.463 | 0.167 | 0.246 | 0.665 |
| colsample_bytree | 0.088 | 0.063 | 0.311 | 0.024 | 0.110 |
| min_child_weight | 0.060 | 0.186 | 0.442 | 0.599 | 0.081 |

## svr

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| kernel | linear, rbf, poly | linear | linear | rbf | linear | linear |
| C | 0.001 to 1000.0 | 2.102 | 13.32 | 292.6 | 3.804 | 0.5914 |
| epsilon | 0.001 to 1.0 | 0.03556 | 0.06662 | 0.04705 | 0.001941 | 0.2466 |
| gamma | 0.001 to 1.0 | n/a | n/a | 0.02888 | n/a | n/a |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| kernel | 0.773 | 0.942 | 0.853 | 0.972 | 0.795 |
| C | 0.021 | 0.025 | 0.057 | 0.015 | 0.069 |
| epsilon | 0.206 | 0.032 | 0.091 | 0.013 | 0.136 |
| gamma | nan | nan | nan | nan | nan |

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
| smoothing_level | 0.136 | 0.779 | 0.856 | 0.017 | 0.129 |
| smoothing_trend | 0.780 | 0.160 | 0.047 | 0.159 | 0.529 |
| smoothing_seasonal | 0.084 | 0.061 | 0.097 | 0.824 | 0.342 |
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
| p | 0.061 | 0.007 | 0.002 | 0.008 | 0.047 |
| d | 0.767 | 0.890 | 0.976 | 0.969 | 0.879 |
| q | 0.061 | 0.007 | 0.007 | 0.003 | 0.040 |
| P | 0.052 | 0.009 | 0.001 | 0.002 | 0.019 |
| D | 0.016 | 0.016 | 0.011 | 0.008 | 0.004 |
| Q | 0.042 | 0.071 | 0.003 | 0.010 | 0.012 |
