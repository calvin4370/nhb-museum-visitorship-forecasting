# Hyperparameter tuning report

## Search budget

| Model | Museum | Trials | Best value | Best at trial |
|---|---|---|---|---|
| rf | IHC | 50 | 3.791 | 46 |
| xgb | IHC | 50 | 5.001 | 18 |
| svr | IHC | 50 | 4.688 | 23 |
| hw | IHC | 50 | 6.768 | 41 |
| sarimax | IHC | 42 | 4.436 | 29 |

## rf

### Chosen values

| Parameter | Range | IHC |
|---|---|---|
| n_estimators | 100 to 1000 step 100 | 1000 |
| max_depth | 5 to 30 | 5 |
| min_samples_split | 2 to 20 | 12 |
| min_samples_leaf | 1 to 10 | 6 |
| max_features | sqrt, log2, None | None |
| bootstrap | True, False | False |

### Importance

| Parameter | IHC |
|---|---|
| n_estimators | 0.010 |
| max_depth | 0.016 |
| min_samples_split | 0.120 |
| min_samples_leaf | 0.033 |
| max_features | 0.784 |
| bootstrap | 0.036 |

## xgb

### Chosen values

| Parameter | Range | IHC |
|---|---|---|
| n_estimators | 100 to 1000 step 100 | 200 |
| max_depth | 3 to 10 | 7 |
| learning_rate | 0.01 to 0.3 | 0.251 |
| subsample | 0.5 to 1.0 | 0.6519 |
| colsample_bytree | 0.5 to 1.0 | 0.7177 |
| min_child_weight | 1 to 10 | 7 |

### Importance

| Parameter | IHC |
|---|---|
| n_estimators | 0.362 |
| max_depth | 0.052 |
| learning_rate | 0.101 |
| subsample | 0.310 |
| colsample_bytree | 0.066 |
| min_child_weight | 0.110 |

## svr

### Chosen values

| Parameter | Range | IHC |
|---|---|---|
| kernel | linear, rbf, poly | linear |
| C | 0.001 to 1000.0 | 0.07975 |
| epsilon | 0.001 to 1.0 | 0.2288 |

### Importance

| Parameter | IHC |
|---|---|
| kernel | 0.711 |
| C | 0.178 |
| epsilon | 0.112 |

## hw

### Chosen values

| Parameter | Range | IHC |
|---|---|---|
| smoothing_level | 0.0 to 1.0 | 0.277 |
| smoothing_trend | 0.0 to 1.0 | 0.05528 |
| smoothing_seasonal | 0.0 to 1.0 | 0.191 |
| trend | add, mul | add |
| seasonal | add, mul | add |

### Importance

| Parameter | IHC |
|---|---|
| smoothing_level | 0.001 |
| smoothing_trend | 0.946 |
| smoothing_seasonal | 0.053 |
| trend | 0.000 |
| seasonal | 0.000 |

## sarimax

### Chosen values

| Parameter | Range | IHC |
|---|---|---|
| p | 0 to 5 | 4 |
| d | 0 to 2 | 1 |
| q | 0 to 5 | 2 |
| P | 0 to 2 | 1 |
| D | 0 to 1 | 1 |
| Q | 0 to 2 | 0 |

### Importance

| Parameter | IHC |
|---|---|
| p | 0.877 |
| d | 0.094 |
| q | 0.007 |
| P | 0.003 |
| D | 0.001 |
| Q | 0.019 |
