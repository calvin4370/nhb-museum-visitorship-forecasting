# Hyperparameter tuning report

## Search budget

| Model | Museum | Trials | Best value | Best at trial |
|---|---|---|---|---|
| rf | IHC | 50 | 4.699 | 12 |
| xgb | IHC | 50 | 4.856 | 46 |
| svr | IHC | 50 | 4.138 | 46 |
| hw | IHC | 50 | 7.272 | 44 |
| sarimax | IHC | 50 | 3.806 | 8 |

## rf

### Chosen values

| Parameter | Range | IHC |
|---|---|---|
| n_estimators | 100 to 1000 step 100 | 300 |
| max_depth | 5 to 30 | 18 |
| min_samples_split | 2 to 20 | 8 |
| min_samples_leaf | 1 to 10 | 7 |
| max_features | sqrt, log2, None | None |
| bootstrap | True, False | True |

### Importance

| Parameter | IHC |
|---|---|
| n_estimators | 0.004 |
| max_depth | 0.002 |
| min_samples_split | 0.034 |
| min_samples_leaf | 0.108 |
| max_features | 0.155 |
| bootstrap | 0.696 |

## xgb

### Chosen values

| Parameter | Range | IHC |
|---|---|---|
| n_estimators | 100 to 1000 step 100 | 100 |
| max_depth | 3 to 10 | 5 |
| learning_rate | 0.01 to 0.3 | 0.0668 |
| subsample | 0.5 to 1.0 | 0.5171 |
| colsample_bytree | 0.5 to 1.0 | 0.664 |
| min_child_weight | 1 to 10 | 9 |

### Importance

| Parameter | IHC |
|---|---|
| n_estimators | 0.114 |
| max_depth | 0.081 |
| learning_rate | 0.162 |
| subsample | 0.348 |
| colsample_bytree | 0.222 |
| min_child_weight | 0.072 |

## svr

### Chosen values

| Parameter | Range | IHC |
|---|---|---|
| kernel | linear, rbf, poly | linear |
| C | 0.001 to 1000.0 | 0.511 |
| epsilon | 0.001 to 1.0 | 0.9951 |

### Importance

| Parameter | IHC |
|---|---|
| kernel | 0.866 |
| C | 0.018 |
| epsilon | 0.116 |

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
| smoothing_level | 0.006 |
| smoothing_trend | 0.228 |
| smoothing_seasonal | 0.766 |
| trend | 0.000 |
| seasonal | 0.000 |

## sarimax

### Chosen values

| Parameter | Range | IHC |
|---|---|---|
| p | 0 to 5 | 3 |
| d | 0 to 2 | 0 |
| q | 0 to 5 | 5 |
| P | 0 to 2 | 2 |
| D | 0 to 1 | 1 |
| Q | 0 to 2 | 2 |

### Importance

| Parameter | IHC |
|---|---|
| p | 0.021 |
| d | 0.929 |
| q | 0.028 |
| P | 0.006 |
| D | 0.008 |
| Q | 0.008 |
