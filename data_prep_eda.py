import pandas as pd
import numpy as np

from plotnine import aes, ggplot, geom_line, scale_x_date, scale_y_continuous, ylab, xlab, facet_wrap, labs
from mizani.breaks import date_breaks
from mizani.formatters import date_format

import json
from urllib.request import Request,urlopen


# api call to singstat table builder
# function to loop through months
def next_month(month):
    months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    current_index = months.index(month)
    next_index = (current_index + 1) % 12
    return months[next_index]

#  function to extract keys and values pairs
def extract_keys_values(row):
    keys = [item['key'] for item in row]
    values = [item['value'] for item in row]
    return pd.Series([keys, values])

# main function for api call
# params needed: resourceId, start year, start month, end year, end month
def singstat_api(resourceId, start_year, start_month, end_year, end_month):

    # ====== Headers ======
    hdr = {'User-Agent': 'Mozilla/5.0', "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,/;q=0.8"}
     
    # ====== Parameters ======
    resourceId = resourceId
    offset = "0"
    timeFilter = ""
 
    # ====== Function to manipulate timeFilter ======
    start = {"year": start_year,
        "month": start_month}
    end = {"year": end_year,
        "month": end_month}
     
    timeFilter_list = []
    current_year = start['year']
    current_month = start['month']

    while current_year <= end['year']:
        if current_year == end['year'] and current_month == end['month']:
            timeFilter_list.append(f"{current_year}%20{current_month}")
            break
        timeFilter_list.append(f"{current_year}%20{current_month}")
        current_month = next_month(current_month)
        if current_month == 'Jan':
            current_year += 1
    timeFilter = ','.join(timeFilter_list)
 
    # ====== Get data ======
    url = f"https://tablebuilder.singstat.gov.sg/api/table/tabledata/{resourceId}?offset={offset}&timeFilter={timeFilter}"
    request = Request(url,headers=hdr)
    data = urlopen(request).read()
    data

    # ====== Decode the bytes data, convert into dictionary and extract data into df ======
    decoded_data = data.decode('utf-8')
    data_dict = json.loads(decoded_data)
    data_dict = data_dict['Data']
    singstat_df = pd.DataFrame(data_dict['row'])
    singstat_df

    # ====== Manipulate the df to a suitable data processing format ======
    
    melted_df = singstat_df.copy()
     
    # 1. Drop columns ["seriesNo", "uoM", "footnote"]
    melted_df.drop(columns=["seriesNo", "uoM", "footnote"], inplace=True)
     
    # ======
     
    # 2. Rename "rowText" to "Data Series"
    melted_df.rename(columns={"rowText": "Data Series"}, inplace=True)

    # ======
     
    # 3. Split "columns" into "Reporting Period" and "Value"
    
    # Apply the function to the 'columns' column
    melted_df[['Reporting Period', 'Value']] = melted_df['columns'].apply(extract_keys_values)
     
    # Drop the 'columns' column
    melted_df.drop(columns=['columns'], inplace=True)
    
    # Use the explode method to flatten the lists
    #melted_df = melted_df.apply(pd.Series.explode)
    melted_df = melted_df.set_index("Data Series").apply(pd.Series.explode).reset_index()

    # ======
    return melted_df
 
# 2 api calls made: museum visitorship and international arrivals
visitors = singstat_api("M891071", 2014, "Jan", 2024, "Dec")
arrivals = singstat_api("M550001", 2014, "Jan", 2024, "Dec")

# filter museum visitorship data to only ACM data series
# output both data series (acm_ts.csv, intl_arrivals.csv)
acm_ts = visitors.loc[visitors.loc[:,"Data Series"]=="Asian Civilisations Museum",:]
acm_ts.to_csv("./acm_ts.csv", index=False)

arrivals.to_csv("./intl_arrivals.csv", index=False)


# EDA
# (1) time plots
# data preprocessing 
acm_ts = pd.read_csv("./acm_ts.csv")

# create datetime variable
acm_ts['Reporting_Period'] = acm_ts['Reporting Period'].apply(lambda x: pd.to_datetime(x, format='%Y %b'))

# create integer month and year variables
acm_ts['Year'] = acm_ts['Reporting_Period'].dt.year
acm_ts['Month'] = acm_ts['Reporting_Period'].dt.month

# append monthly mean
monthly_mean = pd.DataFrame(acm_ts.groupby('Month')['Value'].mean().reset_index())
monthly_mean = monthly_mean.rename(columns={'Value' : 'Monthly_Mean'})
acm_ts = pd.merge(acm_ts, monthly_mean, on=['Month'], how='left')

# plotting
plot1 = (ggplot(acm_ts, aes(x='Reporting_Period', y='Value')) 
         + geom_line(colour='#008FD5', size=2) 
         + scale_x_date(breaks=date_breaks('1 year'), labels=date_format('%Y')) 
         + ylab('Visitorship (Thousands)') 
         + xlab('')
         + labs(title='ACM visitorship across time, 2014-2024'))

plot1.save("plot1.png")

plot2 =(ggplot(acm_ts, aes(x='Reporting_Period', y='Value', group=1))
        + geom_line(aes(y='Monthly_Mean'), colour='gray', size=1.5) 
        + geom_line(aes(y='Value'), colour='#008FD5', size=1.5)
        + scale_x_date(labels=date_format('%b')) 
        + facet_wrap('~Year', scales='free_x')
        + ylab('Visitorship (Thousands)') 
        + xlab('')
        + labs(title='ACM visitorship and monthly mean, 2014-2024'))

plot2.save("plot2.png")


# (2) measure correlation between museum visitorship and international arrivals
# data preprocessing
arrivals = pd.read_csv("./intl_arrivals.csv")
arrivals = arrivals.loc[arrivals.loc[:,"Data Series"] == "Total International Visitor Arrivals By Inbound Tourism Markets",:]
arrivals.rename(columns={"Value":"Arrivals"}, inplace=True)
arrivals.drop('Data Series', axis=1, inplace=True)

acm_ts = pd.read_csv("./acm_ts.csv")
# convert thousands to number
acm_ts.Value = acm_ts.Value.apply(lambda x: x*1000)
acm_ts.rename(columns={"Value":"Visitors"}, inplace=True)
acm_ts.drop('Data Series', axis=1, inplace=True)

# combine dataframes (visitors and arrivals)
comb = pd.merge(acm_ts, arrivals, on=['Reporting Period'], how='left')

# correlation coefficient
pearson_corr = comb['Visitors'].corr(comb['Arrivals'], method='pearson')
spearman_corr = comb['Visitors'].corr(comb['Arrivals'], method='spearman')

# Print the results
print("Pearson Correlation Coefficient:", pearson_corr)
print("Spearman Rank Correlation Coefficient:", spearman_corr)