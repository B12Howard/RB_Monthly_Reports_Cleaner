import numpy as np
import pandas as pd
import re
#import seaborn as sns
#import matplotlib.pyplot as plt
from glob import glob
import get_file_names
from columnFiller import columnFillerFunc

regex_pattern = 'Data/*'
strip_regex_pattern = 'Data\/'
stripped_file_names_list = get_file_names.get_file_names(regex_pattern) #create time series ticks
filenames_array = glob(regex_pattern)
filenames_array.sort()
agg_df = pd.DataFrame()
months_count = 0

categories = ["ALCOHOL", "APPETIZER", "APPETIZERS", "BEEF", "BEER", "BOILED NOODLES", "CHICKEN",
"CHOP SUEY", "CHOW FUN", "CHOW FUN", "CHOW MEIN", "CLAY POT", "DESSERT", "EGG FOO YOUNG", "EXTRA", "FISH", "NON-ALCOHOLIC MIX", "HAPPY HOUR ", "LAMB", "LO MEIN", "MU-SHU", "PORK", "RICE",
"SALAD", "SANDWICHES", "SEAFOOD", "SODA", "SOFT DRINKS", "SOUP", "SPECIAL", "SWEET AND SOUR", "VEGETARIAN", "WINES"]

#Create the Data Frame with all the files that match filename regex_pattern
for single_file_name in filenames_array:
    data = np.loadtxt(single_file_name, delimiter='\n', dtype=str, skiprows=8)
    rmLeading = map(lambda v: re.sub(r'^\s{10,18}', '', v) ,data) #^\s{13,18} removes leadin white spaces from each line
    rmLeading = map(lambda v: re.sub(r'Broccoli  ', 'Broccoli ', v) ,rmLeading) #replace spaces to semicolons
    rmLeading = map(lambda v: re.sub(r'SPC71', 'SPC7 ', v) ,rmLeading) #special case SPC71 replace with SPC7, messes up parsing

    rmLeading = map(lambda v: re.sub(r'^\s{3}', '', v) ,rmLeading) #^\s{3} remove leading 3 speaces
    rmLeading = map(lambda v: re.sub(r'^Others|Group', '', v) ,rmLeading) #remove others from beginning of line
    rmLeading = map(lambda v: re.sub(r'^\s{6,8}', '', v) ,rmLeading) #^\s leading 3 speaces special case of Others
    rmLeading = map(lambda v: re.sub(r'\s{2,}', ';', v) ,rmLeading) #replace double spaces to semicolons

    rmLeading = pd.Series(rmLeading)
    noSpaces_mask = rmLeading.str.contains(r'(?!^\s)|'.join(categories), na=False, regex=True)     #mask to remove all lines with leading space
    rmLeading = rmLeading[noSpaces_mask]

    df = pd.DataFrame(rmLeading)
    pd.set_option('display.max_colwidth', -1)


    df['Category'], df['ItemNo'], df['Description'], df['Price'], df['Quantity'], df['Revenue'], df['Tax'], *rest = df[0].str.split(';').str
    df.drop(labels=0, axis=1, inplace=True)
    df.reset_index(inplace=True)

    with pd.option_context('display.max_rows', None, 'display.max_columns', None): #set display in CL
        print(df)
    columnFillerFunc(df)

    #create date column in dataframe
    temp_date_string = re.sub(strip_regex_pattern, '', single_file_name)
    date_month = re.sub('(\d{2})(-)(\d{4})', r'\1', temp_date_string)
    date_year = re.sub('(\d{2})(-)(\d{4})', r'\3', temp_date_string)
    temp_date_string = date_year + "-" + date_month + "-" + str(1)
    #format date year-month-day default to first day

    #Convert columns to appropriate data types
    df['Date'] = pd.to_datetime(temp_date_string, format="%Y/%m/%d")
    df[['Price']] = df[['Price']].apply(pd.to_numeric, errors='coerce')
    df[['Quantity']] = df[['Quantity']].apply(pd.to_numeric, errors='coerce')
    df[['Revenue']] = df[['Revenue']].apply(pd.to_numeric, errors='coerce')
    df[['Tax']] = df[['Tax']].apply(pd.to_numeric, errors='coerce')

    agg_df = agg_df.append(df)
    #months_count += 1

pd.set_option('display.expand_frame_repr', False)

#    print(df)
#print(df.dtypes)
agg_df.to_csv('rb.csv')
with pd.option_context('display.max_rows', None, 'display.max_columns', None): #set display in CL
    print(agg_df)
#print("nmer of nulls")
print(agg_df.isnull().sum())
#print(agg_df.dtypes)
