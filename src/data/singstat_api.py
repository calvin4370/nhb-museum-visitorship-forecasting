import pandas as pd
import numpy as np

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
