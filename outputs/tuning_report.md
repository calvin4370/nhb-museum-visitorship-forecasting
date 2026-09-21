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
| n_estimators | 0.030 | 0.027 | 0.041 | 0.029 | 0.015 |
| max_depth | 0.012 | 0.568 | 0.632 | 0.012 | 0.003 |
| min_samples_split | 0.046 | 0.030 | 0.004 | 0.012 | 0.001 |
| min_samples_leaf | 0.035 | 0.112 | 0.039 | 0.075 | 0.043 |
| max_features | 0.224 | 0.099 | 0.070 | 0.115 | 0.879 |
| bootstrap | 0.652 | 0.165 | 0.213 | 0.757 | 0.059 |

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
| n_estimators | 0.056 | 0.052 | 0.026 | 0.010 | 0.029 |
| max_depth | 0.026 | 0.127 | 0.007 | 0.091 | 0.027 |
| learning_rate | 0.323 | 0.113 | 0.031 | 0.043 | 0.074 |
| subsample | 0.500 | 0.491 | 0.147 | 0.247 | 0.695 |
| colsample_bytree | 0.052 | 0.085 | 0.341 | 0.038 | 0.103 |
| min_child_weight | 0.044 | 0.132 | 0.447 | 0.572 | 0.071 |

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
| kernel | 0.815 | 0.927 | 0.740 | 0.952 | 0.730 |
| C | 0.021 | 0.019 | 0.067 | 0.027 | 0.074 |
| epsilon | 0.164 | 0.054 | 0.193 | 0.021 | 0.197 |

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
| smoothing_level | 0.132 | 0.806 | 0.798 | 0.025 | 0.106 |
| smoothing_trend | 0.760 | 0.136 | 0.064 | 0.211 | 0.535 |
| smoothing_seasonal | 0.108 | 0.058 | 0.138 | 0.765 | 0.359 |
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
| p | 0.100 | 0.009 | 0.002 | 0.007 | 0.039 |
| d | 0.640 | 0.899 | 0.975 | 0.971 | 0.892 |
| q | 0.109 | 0.008 | 0.006 | 0.003 | 0.029 |
| P | 0.047 | 0.009 | 0.001 | 0.002 | 0.026 |
| D | 0.018 | 0.017 | 0.012 | 0.008 | 0.006 |
| Q | 0.086 | 0.058 | 0.004 | 0.009 | 0.009 |
