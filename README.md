# Visitor Forecast 

add: remember to update deepavali.csv manually

## Project folder structure 
Look at Combined folder (where all the codes are consolidated at)  
```
Combined/  
├── data/                # Data files from singstat api calls  
  ├── intl_arrivals.csv  
  ├── museum_ts.csv  
├── models/                # Python codes for different models  
  ├── baseline.py
  ├── holtwinters.py
  ├── lstm.py  
  ├── randomforest.py
  ├── sarimax.py
  ├── svr.py
  ├── timegpt.py  
  ├── xgboost.py
├── timeplot_output/      #Time plot outputs of actual v.s. predicted values
  ├── baseline_timeplot.png
  ├── hw_timeplot.png
  ├── lstm_timeplot.png
  ├── rf_timeplot.png
  ├── sarimax_timeplot.png
  ├── svr_timeplot.png
  ├── timegpt_timeplot.png
  ├── xgb_timeplot.png
├── utils/  
  ├── data_prep.py         # Data preparation codes  
  ├── singstat_api.py      # Singstat Table Builder API calls
  ├── timeplot.py          # Functions to output timeplots and predictions data frame
├── main.py                # Run main.py  
├── model_eval.csv         # Output for model evaluation
├── predictions.csv         # Output for model prediction  
├── requirements.txt       # requirements.txt for python codes
```

## Data files
- acm_ts.csv: museum visitorship of ACM
- intl_arrivals.csv: international arrivals\
Both data are pulled via api calls from Singstat Table Builder website.

## Notes
1. requirements.txt only contains required packages under python but not R.
2. Most classical time series modelling are readily available in R, hence R is used for that purpose. 
