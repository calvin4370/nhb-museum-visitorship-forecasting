# Hyperparameter tuning report

## Search budget

| Model | Museum | Trials | Completed | Best value | Best at trial |
|---|---|---|---|---|---|
| rf | ACM | 50 | 50 | 3.917 | 13 |
| rf | NMS | 50 | 50 | 17.74 | 33 |
| rf | TPM | 50 | 50 | 1.563 | 49 |
| rf | IHC | 50 | 50 | 4.815 | 24 |
| rf | MHC | 50 | 50 | 13.07 | 17 |
| xgb | ACM | 50 | 50 | 4.282 | 44 |
| xgb | NMS | 50 | 50 | 19.93 | 39 |
| xgb | TPM | 50 | 50 | 1.067 | 48 |
| xgb | IHC | 50 | 50 | 4.283 | 30 |
| xgb | MHC | 50 | 50 | 12.38 | 0 |
| svr | ACM | 50 | 50 | 4.3 | 18 |
| svr | NMS | 50 | 50 | 17.73 | 25 |
| svr | TPM | 50 | 50 | 1.917 | 47 |
| svr | IHC | 50 | 50 | 3.341 | 35 |
| svr | MHC | 50 | 50 | 8.175 | 25 |
| hw | ACM | 50 | 50 | 6.984 | 28 |
| hw | NMS | 50 | 50 | 31.47 | 42 |
| hw | TPM | 50 | 50 | 6.706 | 5 |
| hw | IHC | 50 | 50 | 6.641 | 22 |
| hw | MHC | 50 | 50 | 8.373 | 31 |
| sarimax | ACM | 50 | 50 | 9.495 | 40 |
| sarimax | NMS | 50 | 50 | 22.32 | 48 |
| sarimax | TPM | 50 | 50 | 3.68 | 48 |
| sarimax | IHC | 50 | 50 | 3.214 | 3 |
| sarimax | MHC | 50 | 50 | 9.865 | 38 |

## rf

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| n_estimators | 100 to 1000 step 100 | 300 | 300 | 900 | 1000 | 900 |
| max_depth | 5 to 30 | 17 | 6 | 20 | 27 | 24 |
| min_samples_split | 2 to 20 | 9 | 3 | 4 | 2 | 7 |
| min_samples_leaf | 1 to 10 | 4 | 6 | 1 | 7 | 7 |
| max_features | sqrt, log2, None | None | None | None | None | sqrt |
| bootstrap | True, False | True | True | False | True | False |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| n_estimators | 0.027 | 0.015 | 0.044 | 0.015 | 0.015 |
| max_depth | 0.022 | 0.368 | 0.557 | 0.070 | 0.001 |
| min_samples_split | 0.080 | 0.038 | 0.021 | 0.014 | 0.002 |
| min_samples_leaf | 0.013 | 0.124 | 0.047 | 0.230 | 0.052 |
| max_features | 0.198 | 0.148 | 0.074 | 0.189 | 0.864 |
| bootstrap | 0.660 | 0.307 | 0.256 | 0.482 | 0.066 |

## xgb

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| n_estimators | 100 to 1000 step 100 | 100 | 600 | 500 | 200 | 400 |
| max_depth | 3 to 10 | 10 | 4 | 5 | 6 | 10 |
| learning_rate | 0.01 to 0.3 | 0.02788 | 0.2776 | 0.0917 | 0.2332 | 0.2223 |
| subsample | 0.5 to 1.0 | 0.5949 | 0.5412 | 0.9656 | 0.8094 | 0.7993 |
| colsample_bytree | 0.5 to 1.0 | 0.8528 | 0.5052 | 0.8344 | 0.9074 | 0.578 |
| min_child_weight | 1 to 10 | 1 | 9 | 4 | 2 | 2 |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| n_estimators | 0.058 | 0.028 | 0.026 | 0.044 | 0.025 |
| max_depth | 0.026 | 0.114 | 0.019 | 0.075 | 0.037 |
| learning_rate | 0.300 | 0.122 | 0.027 | 0.154 | 0.128 |
| subsample | 0.469 | 0.519 | 0.155 | 0.150 | 0.607 |
| colsample_bytree | 0.108 | 0.054 | 0.301 | 0.150 | 0.110 |
| min_child_weight | 0.039 | 0.164 | 0.472 | 0.427 | 0.094 |

## svr

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| kernel | linear, rbf, poly | linear | linear | rbf | linear | linear |
| C | 0.001 to 1000.0 | 2.102 | 13.32 | 292.6 | 6.705 | 0.5914 |
| epsilon | 0.001 to 1.0 | 0.03556 | 0.06662 | 0.04705 | 0.001749 | 0.2466 |
| gamma | 0.001 to 1.0 | n/a | n/a | 0.02888 | n/a | n/a |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| kernel | 0.839 | 0.940 | 0.802 | 0.921 | 0.814 |
| C | 0.026 | 0.020 | 0.024 | 0.037 | 0.069 |
| epsilon | 0.134 | 0.040 | 0.173 | 0.042 | 0.117 |
| gamma | nan | nan | nan | nan | nan |

## hw

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| smoothing_level | 0.0 to 1.0 | 0.7474 | 0.1388 | 0.1834 | 0.8857 | 0.9131 |
| smoothing_trend | 0.0 to 1.0 | 0.0741 | 0.3625 | 0.3042 | 0.1015 | 0.001787 |
| smoothing_seasonal | 0.0 to 1.0 | 0.0005285 | 0.1489 | 0.5248 | 0.07509 | 0.06696 |
| trend | add | add | add | add | add | add |
| seasonal | add | add | add | add | add | add |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| smoothing_level | 0.081 | 0.142 | 0.204 | 0.282 | 0.070 |
| smoothing_trend | 0.849 | 0.716 | 0.715 | 0.641 | 0.719 |
| smoothing_seasonal | 0.069 | 0.142 | 0.081 | 0.077 | 0.211 |
| trend | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| seasonal | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |

## sarimax

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| p | 0 to 5 | 0 | 0 | 3 | 2 | 2 |
| d | 0 to 2 | 1 | 0 | 0 | 0 | 0 |
| q | 0 to 5 | 3 | 0 | 1 | 3 | 1 |
| P | 0 to 2 | 2 | 0 | 1 | 0 | 2 |
| D | 0 to 1 | 0 | 1 | 1 | 0 | 0 |
| Q | 0 to 2 | 0 | 1 | 0 | 1 | 0 |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| p | 0.114 | 0.009 | 0.002 | 0.060 | 0.022 |
| d | 0.691 | 0.923 | 0.977 | 0.886 | 0.911 |
| q | 0.068 | 0.021 | 0.006 | 0.018 | 0.032 |
| P | 0.049 | 0.010 | 0.001 | 0.017 | 0.025 |
| D | 0.019 | 0.021 | 0.010 | 0.002 | 0.003 |
| Q | 0.058 | 0.016 | 0.004 | 0.017 | 0.007 |
