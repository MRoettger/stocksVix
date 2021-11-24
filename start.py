import numpy as np
import pandas as pd
from numpy import genfromtxt
from datetime import date, datetime


df = pd.read_csv('importData/DAX.csv',sep=",",parse_dates=["Date"],header=0,decimal=".",
#index_col="Date"
)

indexsize = str( df.index.size)
open_info = str( df["Open"].describe(include='all'))
close_info = str( df["Close"].describe(include='all'))
#print("Datensätzen: " + indexsize)

print('----')
df['Weekday']= df["Date"].dt.dayofweek
 
df['WeekandYear'] = df["Date"].dt.weekofyear.astype(str) +df["Date"].dt.year.astype(str)
df['Yearday']= df["Date"].dt.dayofyear

df_m_f = df[(df["Weekday"]== 0) |(df["Weekday"]== 4)]
df_f = df[(df["Weekday"]== 4)]

if df_m_f["Weekday"].head(1).values[0] != 2:
    df_f = df[(df["Weekday"]== 4)]
    df_m = df[(df["Weekday"]== 0)]
    #add new Fram on Top 
    del df_m['Close']
    del df_m['High']
    del df_m['Low']
    del df_m['Adj Close']
    del df_m['Volume']
    del df_m['Yearday']
    df_f = df_f.loc[:, ['Close','WeekandYear']]
    result = df_f.set_index('WeekandYear').join(df_m.set_index('WeekandYear'))

   
    result.set_index('Date')
    #print(df_m)
    #print(df_f)
    result2 = result.loc[:, ['Date','Open','Close']]
   
    result2['value']= result2['Open']/result2['Close'] - 1
    #print(result2)
    #print(result2['value'].describe(include='all'))
    result2.to_excel('export/output.xlsx', sheet_name='Sheet_name')

   # result = df_f.join([df_m], lsuffix='WeekandYear')
    #print(df_f)



#df_m_f['test']= df_m_f["Open"]/df_m_f["Close"]

#print(df_m_f)
#print(df_m_f["Weekday"].head(1).values[0])






