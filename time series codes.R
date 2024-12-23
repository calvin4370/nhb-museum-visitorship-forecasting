library(lubridate)
library(ggplot2)
library(forecast)
library(Metrics)
library(tidyverse)
library(zoo)
library(xts)

set.seed(123)

acm_ts = read.csv("C:/Users/xueli/OneDrive/Desktop/NHB/Visitor Forecast/acm_ts.csv")

#create date variable
acm_ts$Reporting.Period = parse_date_time(acm_ts$Reporting.Period, "Y b")

#drop unused variable
acm_ts=subset(acm_ts, select=-c(Data.Series))

#convert to time series object for time series modelling
acm_ts = ts(acm_ts$Value, frequency=12, start=c(2014,1), end=c(2024,10))

#split train test
ts_train_test_split = function(ts_data,s_prop){
  n = length(ts_data)
  train_size = floor(n * s_prop)
  time_index = time(ts_data)
  h = n - train_size
  
  train_data = window(ts_data, end = time_index[train_size])
  test_data = window(ts_data, start = time_index[train_size + 1])
  return(list(train_data, test_data, h))
}

result = ts_train_test_split(acm_ts, 0.8)
acm_ts_train = result[[1]]
acm_ts_test = result[[2]]
h = result[[3]]

#utility function to create dates from time series object
ts_dates_func = function(ts_data){
  start_year_mon = start(ts_data)
  end_year_mon = end(ts_data)
  dates = seq(as.Date(as.yearmon(paste(start_year_mon[1], start_year_mon[2]), "%Y %m")), as.Date(as.yearmon(paste(end_year_mon[1], end_year_mon[2]), "%Y %m")), by="month")
  
  return(dates)
}

#replace data points between Apr-Jun 2020 to remove COVID effect, done by interpolation
interpolation_func = function(ts_data){
  #dates from training time series
  dates = ts_dates_func(ts_data)
  
  #define Covid period
  covid_start = as.Date("2020-04-01")
  covid_end = as.Date("2020-06-30")
  
  #convert time series to dataframe for manipulation
  df = data.frame(date=dates, value=as.vector(ts_data))
  df = df %>%
    mutate(is_covid = date>=covid_start & date<=covid_end)
  
  #apply interpolation
  non_covid_df = df %>% filter(!is_covid)
  
  interp_func = approxfun(x = as.numeric(non_covid_df$date),
                          y = non_covid_df$value,
                          method = "linear",
                          rule = 2)
  
  df = df %>%
    mutate(interpolated = interp_func(as.numeric(date)))
  
  #convert back to time series
  ts_interpolated = ts(df$interpolated, start=start(ts_data), frequency=frequency(ts_data))
  return(ts_interpolated)
}

#turned off interpolation as it is not affecting modelling results
#acm_ts_train = interpolation_func(acm_ts_train)



#time series analysis
#decompose time series: trend, seasonal and random components
acm_ts_train_components = decompose(acm_ts_train)
acm_ts_train_components$seasonal
#largest factor is in March (3.70) and lowest is for December (-3.22), this indicates there's peak in visitors in Mar and trough in visitors in Dec. 
plot(acm_ts_train_components)


#autocorrelation tests for model assumptions
acf_test = function(res){
  #acf plot
  #to see if any lags exceed significant bounds
  acf(res, na.action=na.pass, lag.max=50)
  
  #Ljung-Box test
  #to see if p-value is <0.05
  print(Box.test(res, lag=50, type="Ljung-Box"))
  
  #line plot for residuals
  #to see if residuals are roughly constant variance across time
  plot.ts(res)
}

#model evaluation metrics
#rmse, mape
eval_metric = function(test_df, pred_df){
  rmse = rmse(test_df, pred_df)
  mape = mape(test_df, pred_df)
  
  return(list(rmse, mape))
}

#plot actual v.s. predicted
plot_actual_pred = function(full_df, pred_df){
  #dates from test time series
  dates1 = ts_dates_func(full_df)
  
  dates2 = ts_dates_func(pred_df)
  
  #create xts objects
  full_xts = xts(full_df, order.by=dates1)
  pred_xts = xts(pred_df, order.by=dates2)
  
  #combine time series
  comb = merge(full_xts, pred_xts)
  
  #plot
  autoplot(comb, facets=NULL) +
    labs(title="Actual v.s. Predicted",
         x="Date",
         y="Visitorship") +
    scale_colour_manual(values=c("black","red"),
                        labels=c('Actual',"Predicted"))
}


#Model 1: Holt-Winters exponential smoothing with trend and additive seasonal component
HW_param_func = function(ts_data){
  #param grid
  alpha_range = seq(0.1, 0.9, by=0.1)
  beta_range = seq(0.1, 0.9, by=0.1)
  gamma_range = seq(0.1, 0.9, by=0.1)
  
  #initialise for storing param and RMSE
  best_params = list(alpha=NA, beta=NA, gamma=NA)
  best_rmse = Inf
  
  #fit model and perform grid search
  for (alpha in alpha_range){
    for (beta in beta_range){
      for (gamma in gamma_range){
        #fit HW model
        HW_model = HoltWinters(ts_data, alpha=alpha, beta=beta, gamma=gamma)
        
        #calculate RMSE
        rmse = sqrt((HW_model$SSE)/length(ts_data))
        
        #update best params if rmse is lower
        if (rmse < best_rmse){
          best_rmse = rmse
          best_params$alpha = alpha
          best_params$beta = beta
          best_params$gamma = gamma
        }
      }
    }
  }
  return(best_params)
}

#fit final model based on best params
HW_param = HW_param_func(acm_ts_train)
HW_model = HoltWinters(acm_ts_train, alpha=HW_param$alpha, beta=HW_param$beta, gamma=HW_param$gamma)
HW_for = forecast:::forecast.HoltWinters(HW_model, h=h)

#output
#1.forecast plot with confidence intervals
plot(HW_for)
#2.autocorrelation test
acf_test(HW_for$residuals)
#3. plot of actual v.s. predicted
HW_pred = HW_for[[4]]
plot_actual_pred(acm_ts, HW_pred)
#4. evaluation metrics for cross comparison across models
M1_result = eval_metric(acm_ts_test, HW_pred)
print(M1_result)
