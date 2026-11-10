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
| n_estimators | 0.010 | 0.014 | 0.006 | 0.010 | 0.013 |
| max_depth | 0.014 | 0.425 | 0.716 | 0.096 | 0.001 |
| min_samples_split | 0.109 | 0.063 | 0.004 | 0.019 | 0.004 |
| min_samples_leaf | 0.013 | 0.130 | 0.037 | 0.164 | 0.044 |
| max_features | 0.184 | 0.119 | 0.065 | 0.246 | 0.880 |
| bootstrap | 0.670 | 0.249 | 0.173 | 0.464 | 0.059 |

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
| n_estimators | 0.055 | 0.038 | 0.021 | 0.050 | 0.019 |
| max_depth | 0.021 | 0.081 | 0.010 | 0.067 | 0.020 |
| learning_rate | 0.300 | 0.149 | 0.028 | 0.177 | 0.147 |
| subsample | 0.477 | 0.457 | 0.131 | 0.151 | 0.673 |
| colsample_bytree | 0.105 | 0.047 | 0.334 | 0.155 | 0.074 |
| min_child_weight | 0.042 | 0.228 | 0.476 | 0.399 | 0.065 |

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
| kernel | 0.840 | 0.933 | 0.813 | 0.929 | 0.739 |
| C | 0.022 | 0.019 | 0.053 | 0.031 | 0.111 |
| epsilon | 0.138 | 0.048 | 0.133 | 0.040 | 0.150 |
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
| smoothing_level | 0.064 | 0.143 | 0.201 | 0.236 | 0.068 |
| smoothing_trend | 0.868 | 0.705 | 0.700 | 0.694 | 0.734 |
| smoothing_seasonal | 0.068 | 0.152 | 0.098 | 0.070 | 0.197 |
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
| p | 0.083 | 0.024 | 0.003 | 0.084 | 0.027 |
| d | 0.634 | 0.916 | 0.975 | 0.867 | 0.910 |
| q | 0.127 | 0.030 | 0.005 | 0.023 | 0.023 |
| P | 0.054 | 0.004 | 0.001 | 0.011 | 0.027 |
| D | 0.022 | 0.011 | 0.012 | 0.003 | 0.004 |
| Q | 0.080 | 0.015 | 0.004 | 0.012 | 0.009 |
