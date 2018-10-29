###Function parses lines incorrectly parsed and fills in corresponding NaN columns
###Number of spaces between numbers must equal number of NaN in the row, if not parse
###Iterate over rows that have a NaN, then compare number of spaces in the column to the
###number of nulls in the rowself.
###process the case accordingly
import re
import numpy as np
import pandas as pd

def columnFillerFunc(df):
    nanMask = df.isna().any() #find which rows have at least 1 NaN, use as mask
    nanCounter = df.isnull().sum(axis=1) #find number of Nans in each skiprows
    #print("inside columnFillerFunc")
    #make a dataframe to get only rows with at least 1 nan value

    #special case: category and itemNo are smashed together... only by visual inspection can this be seen...
    #separate and repopulate columns
    mask0 = df.loc[:, 'Description'].str.contains('->', case=False)#drop all rows with -> no data or no way to get the data without manual copy paste
    mask01 =  df.loc[:, 'ItemNo'].str.contains('->', case=False)
    mask001 = pd.concat((mask0, mask01), axis=1)
    select001 = mask001.all(axis=1)
    mask1 = df.loc[:,'Category'].str.contains('SWEET AND SOUR', case=False)
    mask2 = df.loc[:,'Category'].str.contains('BOILED NOODLES', case=False)
    mask3 = df.loc[:,'ItemNo'].str.contains('ICE 2', case=False)
    mask4 = df.loc[:,'Category'].str.contains('NON-ALCOHOLIC', case=False)
    mask5 = df.loc[:,'Category'].str.contains('VEGETARIAN', case=False)
    mask6 = df.loc[:,'Category'].str.contains('LO MEIN', case=False)
    #print(df[mask1])

    for idx, row in df[mask0].iterrows():
        #print("drop "  + str(row))
        df.drop(index=idx, inplace=True)

    for idx, row in df[mask01].iterrows():
        #print("drop "  + str(row))
        df.drop(index=idx, inplace=True)

    for idx, row in df[mask1].iterrows():
        if(len(row.str.contains('SWEET AND SOUR', case=False))):
            category = re.sub(r'(SWEET AND SOUR) (\d+)', r'\1', row.Category)
            itemNo = re.sub(r'(SWEET AND SOUR) (\d+)', r'\2', row.Category)
            df.at[idx, 'Tax'] = row.Revenue
            df.at[idx, 'Revenue'] = row.Quantity
            df.at[idx, 'Quantity'] = row.Price
            df.at[idx, 'Price'] = row.Description
            df.at[idx, 'Description'] = row.ItemNo
            df.at[idx, 'ItemNo'] = itemNo
            df.at[idx, 'Category'] = category

    for idx, row in df[mask2].iterrows():
        if(len(row.str.contains('NOODLES', case=False))):
            category = re.sub(r'(BOILED NOODLES) (\d+)', r'\1', row.Category)
            itemNo = re.sub(r'(BOILED NOODLES) (\d+)', r'\2', row.Category)
            #print("category " + category)
            #print("itemNo " + itemNo)
            df.at[idx, 'Tax'] = row.Revenue
            df.at[idx, 'Revenue'] = row.Quantity
            df.at[idx, 'Quantity'] = row.Price
            df.at[idx, 'Price'] = row.Description
            df.at[idx, 'Description'] = row.ItemNo
            df.at[idx, 'ItemNo'] = itemNo
            df.at[idx, 'Category'] = category

    #special case ice cream Description and ItemNo together together by a space, need to separate
    for idx, row in df[mask3].iterrows():
        #print("in mask 3")
        if(pd.isna(row.Tax)):
            df.at[idx, 'Tax'] = row.Revenue
            df.at[idx, 'Revenue'] = row.Quantity
            df.at[idx, 'Quantity'] = row.Price
            df.at[idx, 'Price'] = row.Description
        else:
            df.at[idx, 'Revenue'] = row.Quantity
            df.at[idx, 'Quantity'] = row.Price
            df.at[idx, 'Price'] = row.Description
        string = re.sub(r'(ICE \d)', r'\1;', row.ItemNo)
        #print(string)
        df.at[idx, 'ItemNo'], df.at[idx, 'Description'] = string.split(';', 1)

    for idx, row in df[mask4].iterrows():
        if(len(row.str.contains('NON-ALCOHOLIC', case=False))):
            category = re.sub(r'(NON-ALCOHOLIC) (\w+\d+)', r'\1', row.Category)
            itemNo = re.sub(r'(NON-ALCOHOLIC) (\w+\d+)', r'\2', row.Category)
            df.at[idx, 'Tax'] = row.Revenue
            df.at[idx, 'Revenue'] = row.Quantity
            df.at[idx, 'Quantity'] = row.Price
            df.at[idx, 'Price'] = row.Description
            df.at[idx, 'Description'] = row.ItemNo
            df.at[idx, 'ItemNo'] = itemNo
            df.at[idx, 'Category'] = category

    for idx, row in df[mask5].iterrows(): #drop all Vegetarian categories
        df.drop(index=idx, inplace=True)

    for idx, row in df[mask6].iterrows(): #drop all LO MEIN categories
        df.drop(index=idx, inplace=True)


    for idx, row in df.iterrows():
        print("current working row " + str(row))
    #    if(len(re.findall(r'^\s+', df.at[idx, 'Tax']))):#find all leading spaces
    #        print("before " + str(df.at[idx, 'Tax']))
    #        df.at[idx, 'Tax'] = re.sub(r'^\s+',r'', df.at[idx, 'Tax'])
    #        print("after " + df.at[idx, 'Tax'])
        df.at[idx, 'Tax'] = str(df.at[idx, 'Tax']).strip(' ')
        if(pd.isna(row.Tax)): #if Tax column is NaN

            if(row.Revenue): #if row.Revenue is not NaN then find all single white space

                print("inside if after testing row.Revenue")
                string = str(row.Revenue).strip()
                print(df.at[idx, 'Description'])
                print(string)
                numWhiteSpace = re.findall('\s', string)
                print(len(numWhiteSpace))
                #print(np.count(row))
                if(len(numWhiteSpace) == 1): #if number of white space in Revenue equals 1 nan
                    print(string.split(' ',1))
                    df.at[idx, 'Revenue'], df.at[idx, 'Tax'] = string.split(' ', 1)#split Revenue by white space, assign second number to Tax
                if(len(numWhiteSpace) == 0):
                    df.at[idx, 'Tax'] = row.Revenue
                    df.at[idx, 'Revenue'] = np.nan

            if(pd.isna(row.Revenue)): #if row.Revenue is Nan
                string = str(row.Quantity).strip()
                string2 = str(row.Price).strip()
                numWhiteSpace = re.findall('\s', string)
                numWhiteSpace2 = re.findall('\s', string2)
                #print("inside row.Revenue==np.nan")
                print("number white spaces " + str(len(numWhiteSpace)==1))
                if(len(numWhiteSpace) == 1): #if number of white space equals number of NaN in the row
                    df.at[idx, 'Revenue'], df.at[idx, 'Tax'] = string.split(' ',1) #split Revenue by white space, assign second number to Tax
                    if(len(numWhiteSpace2) == 0):
                        string2 = re.sub(r'(\.[0-9]{2})(?=[^\s])',r'\1 ', df.at[idx, 'Price']) # substitutes in the entire substring matched by the RE then \s adds a space
                    df.at[idx, 'Price'], df.at[idx, 'Quantity'] = str(string2).split(' ',1)
                    #print(string)
                    #print(str(string2).split(' ',2))
                elif(len(numWhiteSpace) == 2):
                    df.at[idx, 'Quantity'], df.at[idx, 'Revenue'], df.at[idx, 'Tax'] = string.split(' ',2) #split Revenue by white space, assign second number to Tax

                else: #all numbers are in the Price column
                    #need to take into account numbers smashed together eg. 2542.328293.93, insert a space after matching pattern (\.[0-9])(?=[^\s])
                    #print("Inside else@@@@! " + str(row))
                    splitNumber = re.sub(r'(\.[0-9]{2})(?=[^\s])',r'\1 ', df.at[idx, 'Price']) # substitutes in the entire substring matched by the RE then \s adds a space
                    #print("Inside else! " + splitNumber + " " + str(row))
                    df.at[idx, 'Price'], df.at[idx, 'Quantity'], df.at[idx, 'Revenue'], df.at[idx, 'Tax'] = str(splitNumber).split(' ', 3)

        #case for when revenue is nan but tax has a value
        if(pd.isna(df.at[idx, 'Revenue'])):
            string = str(df.at[idx, 'Quantity']).strip()
            string2 = str(df.at[idx, 'Price']).strip()
            #print("strings " + string + " " + string2)
            numWhiteSpace = re.findall('\s', string)
            numWhiteSpace2 = re.findall('\s', string2)
            if(len(numWhiteSpace) == 1): #if number of white space equals number of NaN in the row
                #print("==1 if " + string.split(' ',1))
                df.at[idx, 'Quantity'], df.at[idx, 'Revenue'] = string.split(' ',1) #split Revenue by white space, assign second number to Tax
            if(len(numWhiteSpace) == 0):#if num white spaces is zero use the price column
                #print("==0 if item name " + str(df.at[idx, 'ItemNo']) +" " + str(df.at[idx, 'Description'])  + " " + str(string2.split(' ',1)))
                df.at[idx, 'Revenue'] = df.at[idx, 'Quantity']
                df.at[idx, 'Price'], df.at[idx, 'Quantity'] = str(string2).split(' ',1)

        #print("before inside if where tax has whitespaces " + str(df.at[idx, 'Tax']))

        if(len(re.findall(r'\d\s\d', df.at[idx, 'Tax']))): #case where tax has white spaces
            print("inside if where tax has white spaces " + str(df.at[idx, 'Description']))
            whitespaces = len(re.findall('\s',df.at[idx, 'Tax']))
            shift1 = df.at[idx, 'Revenue']
            shift2 = df.at[idx, 'Quantity']
            shift3 = df.at[idx, 'Price']

            df.at[idx, 'Revenue'], df.at[idx, 'Tax'] = df.at[idx, 'Tax'].split(' ', whitespaces)

            #print("Tax split " + str(df.at[idx, 'Tax'].split(' ', whitespaces)))
            df.at[idx, 'Quantity'] = shift1
            df.at[idx, 'Price'] = shift2
            df.at[idx, 'Description'] = df.at[idx, 'Description'] + " " + (shift3)

        if(len(re.findall(r'\d\s+$',df.at[idx, 'Tax']))): #cases where there is a new line
            #print("lines with a space" + str(df.at[idx, 'Description']))
            df.at[idx, 'Tax'] = re.sub(r'\s+','', df.at[idx, 'Tax'])

        if(re.findall(r'with$',df.at[idx, 'Description'])): #find all items ending with "with" then append category name to it
            #print("inside with if " + df.at[idx, 'Description'])
            df.at[idx, 'Description'] = df.at[idx, 'Description'] + " " + str(df.at[idx, 'Category']).capitalize()
        if(re.findall(r'Fried$',df.at[idx, 'Description'])): #find all items ending with "with" then append category name to it
            #print("inside with if " + df.at[idx, 'Description'])
            df.at[idx, 'Description'] = df.at[idx, 'Description'] + " " + str(df.at[idx, 'Category']).capitalize()
