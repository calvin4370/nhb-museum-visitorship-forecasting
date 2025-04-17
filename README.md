# Visitor Forecast 

## Project folder structure 
Look at Combined folder (where all the codes are consolidated at)  
```
Combined/  
├── data/                # Data files from singstat api calls  
  ├── intl_arrivals.csv  
  ├── museum_ts.csv  
├── models/                # Python codes for different models  
  ├── lstm.py  
  ├── randomforest.py  
  ├── timegpt.py  
  ├── xgboost.py
├── timeplot_output/      #Time plot outputs of actual v.s. predicted values
  ├── lstm_timeplot.png
  ├── rf_timeplot.png
  ├── timegpt_timeplot.png
  ├── xgb_timeplot.png
├── utils/  
  ├── data_prep.py         # Data preparation codes  
  ├── singstat_api.py      # Singstat Table Builder API calls  
├── main.py                # Run main.py  
├── model_eval.csv         # Output for model evaluation  
├── requirements.txt       # requirements.txt for python codes
```

## Data files
- acm_ts.csv: museum visitorship of ACM
- intl_arrivals.csv: international arrivals\
Both data are pulled via api calls from Singstat Table Builder website.

## Notes
1. requirements.txt only contains required packages under python but not R.
2. Most classical time series modelling are readily available in R, hence R is used for that purpose. 
