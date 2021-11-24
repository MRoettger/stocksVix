"""module to import and analyse CSV File
"""
import pandas as pd
from pandas.core.frame import DataFrame

data:DataFrame = pd.read_csv('importData/DAX.csv',sep=",",parse_dates=["Date"],header=0,decimal=".")

OPEN_INFO = str( data["Open"].describe(include='all'))
CLOSE_INFO = str( data["Close"].describe(include='all'))

print('----')
data['Weekday']= data["Date"].dt.dayofweek
data['WeekandYear'] = data["Date"].dt.weekofyear.astype(str) +data["Date"].dt.year.astype(str)
data['Yearday']= data["Date"].dt.dayofyear

df_m_f = data[(data["Weekday"]== 0) |(data["Weekday"]== 4)]
df_f = data[(data["Weekday"]== 4)]

if df_m_f["Weekday"].head(1).values[0] != 2:
    df_f = data[(data["Weekday"]== 4)]
    df_m = data[(data["Weekday"]== 0)]

    df_m = df_m.loc[:, ['Date','Open','Weekday','WeekandYear']]
    print(df_m)
    df_f = df_f.loc[:, ['Close','WeekandYear']]
    result = df_f.set_index('WeekandYear').join(df_m.set_index('WeekandYear'))

    result.set_index('Date')
    result2 = result.loc[:, ['Date','Open','Close']]

    result2['value']= result2['Open']/result2['Close'] - 1
    result2.to_excel('export/output.xlsx', sheet_name='Sheet_name')
