"""Anlayse Finance Main Module
"""
from datetime import datetime
from pandas.core.frame import DataFrame
from pandas_datareader import data as pdr
import pandas as pd

from Moduls.print_plot_modul import print_plot

# request in the Console the Index
STOCK_NAME = input("Aktien Kürzel ? ")
# set selected Stock
if len(STOCK_NAME)==0:
    STOCK_NAME = "SPY"

# set Start and End Date for selected stocks
START_DATE = "2012-02-01"
END_DATE = datetime.now().strftime("%Y-%m-%d")

# interval: data interval (intraday data cannot extend last 60 days)
# Valid intervals are: m, h, d, d, wk, mo, mo
data_stock = pdr.get_data_yahoo(STOCK_NAME, start=START_DATE, end=END_DATE,interval="wk")
data_vix = pdr.get_data_yahoo("^VIX", start=START_DATE, end=END_DATE, interval="wk")

def analyse_stock_data(stock_dataframe:DataFrame):
    """Analyse Stock

    Args:
        data_stock (DataFrame):
    """
    stock_dataframe = stock_dataframe.loc[:,['Open','Close']]
    stock_dataframe["Stock_diff_a"]= (stock_dataframe['Open']-stock_dataframe['Close'])*-1
    stock_dataframe["Stock_diff_p"]= (stock_dataframe['Close']/stock_dataframe['Open']-1)*100
    stock_dataframe.rename(columns={"Open": "Stock_Open", "Close": "Stock_Close"},inplace=True)
    return stock_dataframe

def analyse_vix_data(vix_dataframe):
    """Analyse vix data

    Args:
        data_vix ([type]): vix Data
    """
    vix_dataframe = vix_dataframe.loc[:, ['Open','Close']]
    vix_dataframe["vix_diff_a"]= (vix_dataframe['Open']-vix_dataframe['Close'])*-1
    vix_dataframe["vix_diff_p"]= (vix_dataframe['Close']/vix_dataframe['Open']-1)*100
    vix_dataframe.rename(columns={"Open": "vix_Open", "Close": "vix_Close"},inplace=True)
    return vix_dataframe

data_stock = analyse_stock_data(data_stock)
data_vix = analyse_vix_data(data_vix)


#Concat Dataframes over join
result = pd.concat([data_stock,data_vix], axis=1, join='inner')

#add weeknumber on Insertion index 0
result.insert(0, "Week_number", result.index.weekofyear,allow_duplicates=True)

#export to Excel
result.to_excel('export/output.xlsx', sheet_name='stocks')

print_plot(result)
print(result["Stock_diff_p"].describe(include='all'))
