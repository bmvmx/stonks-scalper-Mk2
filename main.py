#====================================== STONKS SCALPER MK2  ===========================================================
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import argparse as ap
from operator import itemgetter



sector_list = ["Consumer Cyclical","Consumer Defensive","Energy","Financials","Health Care","Industrials","Information Technology","Materials","Real Estate","Comm Services","Utilities"]

  

    
def select_sector():
  
    for ch in range(len(sector_list)):
       print("#"+str(ch)+" "+sector_list[ch])

    Sector_no= int(input("Enter the sector you want to serch for"))
    return sector_list[Sector_no]
    

def select_stocks():
    #need to modify it to take only one stock and return stocks similiar to it

    preset_stock_list = ["AAPL","AMZN","F"]
    parser = ap.ArgumentParser()
    parser.add_argument("--stocks",type=str,help="add all the stock ticker symbols after this " , nargs="*")
    parser.add_argument("--historical",type=str ,help="generate a historical data table  , usage : --historical (period e.g. 1mo/3mo/6mo/1y/2y/5y/ytd/max)")
    parser.add_argument("--a",action="store_true",dest="also",help="-a used to add otehr companies in same sector")
    args = parser.parse_args()
    
    if args.stocks:
        
        select_stocks_overview2(args.stocks)
    else:    
    
        select_stocks_overview2(preset_stock_list)
    
     #need to define functions to represent historical data as well as selecting similiar stocks
    if args.also:

        select_similiar_stocks(args.stocks,args.historical)

    # if args.historical:

    #     preview_historical(args.stocks,args.historical)




def select_stocks_overview2(*args,**kwargs):
    info_list=["sector","marketCap","country","trailingPE","currentPrice","52WeekChange","dividendYield"]
    arg_list = args[0]
    stock_data=[]
    stock_data.append(["symbol"]+info_list)
    for i in arg_list:
        list1 = list(map(yf.Ticker(i).info.get,info_list))
        list1.insert(0,i)
        stock_data.append(list1)
        
    print(pd.DataFrame(stock_data))


def select_similiar_stocks(*args):
    

def select_stocks_overview(*args,**kwargs):
    
# get ticker symbols for the stocks with some preset tickers and sort them in the order asked i.e. top_gainers , top_losers , new_high , new_low etc
# get ticker data from yfinance api and append it to a dataframe and get some preset data from the
# already present dataframes

#===================UPDATE=======================

# The individual stock selection and plotting is working , now I need to select the respective stock sector and implement the "-a"(also) argument
# which will get similiar stocks and plot them too
# after that we will work on selecting and sorting the data of all those stocks plotted in the form of a table
# and store that table for future reference aka the LSTM model probably


#test version : where we just sift data from all available dataframes for the given stocks
    stock_data = []
    info_list=["sector","marketCap","country","trailingPE","currentPrice","52WeekChange","dividendYield"]
    n = len(info_list)+1
    
    list_args = args[0]

   
    for arg in list_args:
        
        stock_data.append(arg)
        arg = yf.Ticker(str(arg))
        for ch in info_list:
            try:
                stock_data.append(arg.info[str(ch)])
            except:
                stock_data.append("NaN")
    df1 = pd.DataFrame([stock_data[i * n:(i + 1) * n] for i in range((len(stock_data) + n - 1) // n )],columns=["Symbol"]+info_list)
    print(df1)
    df1.to_csv("Sector-data\\stocks_overview.csv")



select_stocks()