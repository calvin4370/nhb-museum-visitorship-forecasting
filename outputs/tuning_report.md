# Hyperparameter tuning report

## Search budget

| Model | Museum | Trials | Best value | Best at trial |
|---|---|---|---|---|
| rf | ACM | 50 | 3.917 | 13 |
| rf | NMS | 50 | 17.74 | 33 |
| rf | TPM | 50 | 1.563 | 49 |
| rf | IHC | 50 | 4.698 | 12 |
| xgb | ACM | 50 | 4.282 | 44 |
| xgb | NMS | 50 | 19.93 | 39 |
| xgb | TPM | 50 | 1.067 | 48 |
| xgb | IHC | 50 | 4.771 | 46 |
| hw | ACM | 50 | 7.371 | 43 |
| hw | NMS | 50 | 76.81 | 48 |
| hw | TPM | 50 | 7.755 | 41 |
| hw | IHC | 50 | 7.272 | 44 |
| sarimax | ACM | 50 | 9.495 | 40 |
| sarimax | NMS | 50 | 22.32 | 48 |
| sarimax | TPM | 50 | 3.68 | 48 |
| sarimax | IHC | 11 | 4.313 | 8 |

## rf

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC |
|---|---|---|---|---|---|
| n_estimators | 100 to 1000 step 100 | 300 | 300 | 900 | 300 |
| max_depth | 5 to 30 | 17 | 6 | 20 | 18 |
| min_samples_split | 2 to 20 | 9 | 3 | 4 | 8 |
| min_samples_leaf | 1 to 10 | 4 | 6 | 1 | 7 |
| max_features | sqrt, log2, None | None | None | None | None |
| bootstrap | True, False | True | True | False | True |

### Importance

| Parameter | ACM | NMS | TPM | IHC |
|---|---|---|---|---|
| n_estimators | 0.031 | 0.012 | 0.014 | 0.007 |
| max_depth | 0.013 | 0.464 | 0.678 | 0.016 |
| min_samples_split | 0.083 | 0.032 | 0.030 | 0.022 |
| min_samples_leaf | 0.016 | 0.079 | 0.032 | 0.115 |
| max_features | 0.169 | 0.174 | 0.055 | 0.133 |
| bootstrap | 0.688 | 0.239 | 0.192 | 0.706 |

## xgb

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC |
|---|---|---|---|---|---|
| n_estimators | 100 to 1000 step 100 | 100 | 600 | 500 | 500 |
| max_depth | 3 to 10 | 10 | 4 | 5 | 8 |
| learning_rate | 0.01 to 0.3 | 0.02788 | 0.2776 | 0.0917 | 0.01047 |
| subsample | 0.5 to 1.0 | 0.5949 | 0.5412 | 0.9656 | 0.6066 |
| colsample_bytree | 0.5 to 1.0 | 0.8528 | 0.5052 | 0.8344 | 0.5497 |
| min_child_weight | 1 to 10 | 1 | 9 | 4 | 9 |

### Importance

| Parameter | ACM | NMS | TPM | IHC |
|---|---|---|---|---|
| n_estimators | 0.078 | 0.041 | 0.014 | 0.028 |
| max_depth | 0.031 | 0.112 | 0.008 | 0.202 |
| learning_rate | 0.257 | 0.112 | 0.042 | 0.421 |
| subsample | 0.543 | 0.520 | 0.151 | 0.129 |
| colsample_bytree | 0.056 | 0.052 | 0.349 | 0.152 |
| min_child_weight | 0.036 | 0.163 | 0.436 | 0.069 |

## hw

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC |
|---|---|---|---|---|---|
| smoothing_level | 0.0 to 1.0 | 0.5655 | 0.4108 | 0.1742 | 0.7577 |
| smoothing_trend | 0.0 to 1.0 | 0.05033 | 0.09913 | 0.06758 | 0.09069 |
| smoothing_seasonal | 0.0 to 1.0 | 0.02838 | 0.8379 | 0.7462 | 0.007799 |
| trend | add, mul | add | add | add | add |
| seasonal | add, mul | add | add | add | add |

### Importance

| Parameter | ACM | NMS | TPM | IHC |
|---|---|---|---|---|
| smoothing_level | 0.150 | 0.819 | 0.808 | 0.028 |
| smoothing_trend | 0.753 | 0.140 | 0.053 | 0.219 |
| smoothing_seasonal | 0.096 | 0.042 | 0.140 | 0.753 |
| trend | 0.000 | 0.000 | 0.000 | 0.000 |
| seasonal | 0.000 | 0.000 | 0.000 | 0.000 |

## sarimax

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC |
|---|---|---|---|---|---|
| p | 0 to 5 | 0 | 0 | 3 | 3 |
| d | 0 to 2 | 1 | 0 | 0 | 0 |
| q | 0 to 5 | 3 | 0 | 1 | 5 |
| P | 0 to 2 | 2 | 0 | 1 | 2 |
| D | 0 to 1 | 0 | 1 | 1 | 1 |
| Q | 0 to 2 | 0 | 1 | 0 | 2 |

### Importance

| Parameter | ACM | NMS | TPM | IHC |
|---|---|---|---|---|
| p | 0.158 | 0.011 | 0.002 | 0.544 |
| d | 0.580 | 0.910 | 0.976 | 0.233 |
| q | 0.108 | 0.008 | 0.005 | 0.067 |
| P | 0.049 | 0.008 | 0.001 | 0.029 |
| D | 0.019 | 0.013 | 0.013 | 0.078 |
| Q | 0.085 | 0.050 | 0.003 | 0.048 |
