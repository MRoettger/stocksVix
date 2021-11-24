from pandas.core.frame import DataFrame
from pandas_datareader import data as pdr
import pandas as pd
import matplotlib.pyplot as plt 
import matplotlib as mpl
import yfinance as yf
from datetime import date, datetime

#set selected Stock
stock_name = "SPY"
#set Start and End Date for selected stocks 
start_date = "2012-02-01"
end_date = datetime.now().strftime("%Y-%m-%d")
#interval: data interval (intraday data cannot extend last 60 days) Valid intervals are: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
data_stock = pdr.get_data_yahoo(stock_name, start=start_date, end=end_date,interval="wk")
data_vix = pdr.get_data_yahoo("^VIX", start=start_date, end=end_date, interval="wk")

#rename and filter date from Stocks
data_stock = data_stock.loc[:,['Open','Close']]
data_stock["Stock_diff_a"]= (data_stock['Open']-data_stock['Close'])*-1
data_stock["Stock_diff_p"]= (data_stock['Close']/data_stock['Open']-1)*100
data_stock.rename(columns={"Open": "Stock_Open", "Close": "Stock_Close"},inplace=True)

#rename and filter date from VIX
data_vix = data_vix.loc[:, ['Open','Close']]
data_vix["vix_diff_a"]= (data_vix['Open']-data_vix['Close'])*-1
data_vix["vix_diff_p"]= (data_vix['Close']/data_vix['Open']-1)*100
data_vix.rename(columns={"Open": "vix_Open", "Close": "vix_Close"},inplace=True)


#Concat Dataframes over join  
result = pd.concat([data_stock,data_vix], axis=1, join='inner')

#add weeknumber on Insertion index 0
result.insert(0, "Week_number", result.index.weekofyear,allow_duplicates=True)


print(result)

#export to Excel
result.to_excel('export/output.xlsx', sheet_name='Sheet_name')
#print(matplotlib.get_backend())

data1 = result.loc[:,['Stock_Close']]
data2 = result.loc[:,['vix_Close']]

fig, ax1 = plt.subplots()

color = 'tab:blue'
ax1.set_xlabel('time')
ax1.plot(data1, color=color)
ax1.set_ylabel('index', color=color)

ax2 = ax1.twinx()
color = 'tab:grey'
ax2.set_ylabel('volatility', color=color)  # we already handled the x-label with ax1
ax2.plot(data2, color=color)
ax2.tick_params(axis='y', labelcolor=color)
ax2.axhline(y=20, color='b', linestyle='-')
fig.tight_layout()

#plt.plot(result.loc[:,['Stock_Close','vix_Close']])
#plt.ylabel('stock Value')
#plt.axhline(y=22, color='b', linestyle='-')
plt.show()

#print(result.unstack())
#print(data_vix.describe(include='all'))