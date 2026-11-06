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
| hw | ACM | 50 | 50 | 7.371 | 43 |
| hw | NMS | 50 | 50 | 76.81 | 48 |
| hw | TPM | 50 | 50 | 7.755 | 41 |
| hw | IHC | 50 | 50 | 9.526 | 25 |
| hw | MHC | 50 | 50 | 10.35 | 37 |
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
| n_estimators | 0.024 | 0.023 | 0.041 | 0.031 | 0.009 |
| max_depth | 0.025 | 0.421 | 0.680 | 0.071 | 0.003 |
| min_samples_split | 0.098 | 0.039 | 0.005 | 0.020 | 0.003 |
| min_samples_leaf | 0.026 | 0.086 | 0.037 | 0.168 | 0.059 |
| max_features | 0.159 | 0.159 | 0.060 | 0.223 | 0.843 |
| bootstrap | 0.667 | 0.272 | 0.177 | 0.487 | 0.083 |

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
| n_estimators | 0.052 | 0.027 | 0.011 | 0.025 | 0.016 |
| max_depth | 0.031 | 0.083 | 0.019 | 0.057 | 0.027 |
| learning_rate | 0.297 | 0.120 | 0.039 | 0.187 | 0.064 |
| subsample | 0.495 | 0.488 | 0.159 | 0.158 | 0.672 |
| colsample_bytree | 0.077 | 0.087 | 0.370 | 0.186 | 0.149 |
| min_child_weight | 0.047 | 0.195 | 0.401 | 0.387 | 0.072 |

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
| kernel | 0.786 | 0.926 | 0.737 | 0.943 | 0.722 |
| C | 0.023 | 0.018 | 0.072 | 0.019 | 0.116 |
| epsilon | 0.190 | 0.055 | 0.191 | 0.037 | 0.162 |
| gamma | nan | nan | nan | nan | nan |

## hw

### Chosen values

| Parameter | Range | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|---|
| smoothing_level | 0.0 to 1.0 | 0.5655 | 0.4108 | 0.1742 | 0.001166 | 0.5336 |
| smoothing_trend | 0.0 to 1.0 | 0.05033 | 0.09913 | 0.06758 | 0.9629 | 0.009219 |
| smoothing_seasonal | 0.0 to 1.0 | 0.02838 | 0.8379 | 0.7462 | 0.9138 | 0.3363 |
| trend | add, mul | add | add | add | add | add |
| seasonal | add, mul | add | add | add | add | add |

### Importance

| Parameter | ACM | NMS | TPM | IHC | MHC |
|---|---|---|---|---|---|
| smoothing_level | 0.152 | 0.755 | 0.848 | 0.520 | 0.129 |
| smoothing_trend | 0.775 | 0.179 | 0.052 | 0.303 | 0.360 |
| smoothing_seasonal | 0.073 | 0.066 | 0.099 | 0.177 | 0.511 |
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
| p | 0.123 | 0.006 | 0.002 | 0.055 | 0.031 |
| d | 0.659 | 0.912 | 0.973 | 0.878 | 0.903 |
| q | 0.062 | 0.010 | 0.008 | 0.015 | 0.029 |
| P | 0.048 | 0.007 | 0.001 | 0.018 | 0.026 |
| D | 0.013 | 0.019 | 0.013 | 0.003 | 0.005 |
| Q | 0.095 | 0.047 | 0.004 | 0.030 | 0.006 |
