# Hyperparameter tuning report

## Search budget

| Model | Museum | Trials | Best value | Best at trial |
|---|---|---|---|---|
| rf | IHC | 50 | 4.658 | 43 |
| xgb | IHC | 50 | 4.348 | 24 |
| svr | IHC | 50 | 3.376 | 45 |
| hw | IHC | 50 | 7.272 | 44 |
| sarimax | IHC | 50 | 3.61 | 43 |

## rf

### Chosen values

| Parameter | Range | IHC |
|---|---|---|
| n_estimators | 100 to 1000 step 100 | 200 |
| max_depth | 5 to 30 | 13 |
| min_samples_split | 2 to 20 | 10 |
| min_samples_leaf | 1 to 10 | 2 |
| max_features | sqrt, log2, None | None |
| bootstrap | True, False | True |

### Importance

| Parameter | IHC |
|---|---|
| n_estimators | 0.023 |
| max_depth | 0.030 |
| min_samples_split | 0.017 |
| min_samples_leaf | 0.057 |
| max_features | 0.128 |
| bootstrap | 0.746 |

## xgb

### Chosen values

| Parameter | Range | IHC |
|---|---|---|
| n_estimators | 100 to 1000 step 100 | 1000 |
| max_depth | 3 to 10 | 7 |
| learning_rate | 0.01 to 0.3 | 0.1639 |
| subsample | 0.5 to 1.0 | 0.6987 |
| colsample_bytree | 0.5 to 1.0 | 0.8834 |
| min_child_weight | 1 to 10 | 1 |

### Importance

| Parameter | IHC |
|---|---|
| n_estimators | 0.012 |
| max_depth | 0.050 |
| learning_rate | 0.062 |
| subsample | 0.220 |
| colsample_bytree | 0.025 |
| min_child_weight | 0.630 |

## svr

### Chosen values

| Parameter | Range | IHC |
|---|---|---|
| kernel | linear, rbf, poly | linear |
| C | 0.001 to 1000.0 | 3.804 |
| epsilon | 0.001 to 1.0 | 0.001941 |

### Importance

| Parameter | IHC |
|---|---|
| kernel | 0.969 |
| C | 0.019 |
| epsilon | 0.012 |

## hw

### Chosen values

| Parameter | Range | IHC |
|---|---|---|
| smoothing_level | 0.0 to 1.0 | 0.7577 |
| smoothing_trend | 0.0 to 1.0 | 0.09069 |
| smoothing_seasonal | 0.0 to 1.0 | 0.007799 |
| trend | add, mul | add |
| seasonal | add, mul | add |

### Importance

| Parameter | IHC |
|---|---|
| smoothing_level | 0.025 |
| smoothing_trend | 0.184 |
| smoothing_seasonal | 0.791 |
| trend | 0.000 |
| seasonal | 0.000 |

## sarimax

### Chosen values

| Parameter | Range | IHC |
|---|---|---|
| p | 0 to 5 | 1 |
| d | 0 to 2 | 0 |
| q | 0 to 5 | 1 |
| P | 0 to 2 | 0 |
| D | 0 to 1 | 1 |
| Q | 0 to 2 | 2 |

### Importance

| Parameter | IHC |
|---|---|
| p | 0.008 |
| d | 0.955 |
| q | 0.003 |
| P | 0.003 |
| D | 0.005 |
| Q | 0.027 |
