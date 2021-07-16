#====================================== STONKS SCALPER MK2  ===========================================================
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import pandas as pd
import argparse as ap
#from operator import itemgetter
import time
from bs4 import BeautifulSoup
import csv
import requests
import os


sector_list = ["Basic Materials","Communication Services","Consumer Cyclical","Consumer Defensive","Energy","Financial Services","Healthcare","Industrials","Real Estate","Technology","Utilities"]



    
# def select_sector():
  
#     for ch in range(len(sector_list)):
#        print("#"+str(ch)+" "+sector_list[ch])

#     Sector_no= int(input("Enter the sector you want to serch for"))
#     ret_str =  sector_list[Sector_no]
#     ret_str=ret_str.lower()
#     ret_str = "ms_"+ret_str.replace(" ","_")
#     return ret_str
    

def select_stocks():
    #need to modify it to take only one stock and return stocks similiar to it

    preset_stock_list = ["AAPL","AMZN","F"]
    parser = ap.ArgumentParser()
    parser.add_argument("--stocks",type=str,help="add all the stock ticker symbols after this " , nargs="*")
    parser.add_argument("--historical",type=str ,help="generate a historical data table  , usage : --historical (period e.g. 1mo/3mo/6mo/1y/2y/5y/ytd/max)")
    parser.add_argument("--a",action="store_true",dest="also",help="-a used to add otehr companies in same sector")
    args = parser.parse_args()
    
    if args.stocks:
        
        overview_table = select_stocks_overview2(args.stocks)

    else:    
    
        overview_table = select_stocks_overview2(preset_stock_list)
    
     #need to define functions to represent historical data as well as selecting similiar stocks
    if args.also:

        select_similiar_stocks(args.stocks,args.historical if args.historical else "ytd",overview_table)

    if args.historical:

        preview_historical(args.stocks,args.historical)


#=================================  OVERVIEW  ==========================================

def select_stocks_overview2(*args,**kwargs):
    # ISSUE : implement multithreading to stop the delays when more than 2 stocks are selected
    print("in overview2")
    time_dur1 = time.time()
    info_list=["sector","marketCap","country","trailingPE","currentPrice","52WeekChange","dividendYield"]
    arg_list = args[0]
    
    stock_data=[]
    stock_data.append(["symbol"]+info_list)
    for i in arg_list:
        list1 = list(map(yf.Ticker(i).info.get,info_list))
        list1.insert(0,i)
        stock_data.append(list1)

    time_dur2 = time.time()
    print(time_dur2-time_dur1)
    print("done overview")   
    print(pd.DataFrame(stock_data[1:],columns=stock_data[0]))
    return pd.DataFrame(stock_data[1:],columns=stock_data[0])


#================================  HISTORICAL PLOT  =====================================================

def preview_historical(stocks,period="ytd"):
    # generate a graph using pyplot of all the stocks , period may or maynot be defined
    # -s to compare with similiar companies , -a (also) for comparing with other companies
    
    # import stock data using yfinance historical , store it in a list and print the plot.
    stock_data=[]
    print(stocks)
    plt.figure(figsize=(10,8))
    plt.grid(linestyle="-")
    plt.xlabel("Date")
    plt.ylabel("Share Price")
    

    for arg in stocks:
        stock_data.append(arg)
        arg = yf.Ticker(arg)
        df = pd.DataFrame(arg.history(period=period))
        #print(df.head())
       
        plt.plot(df.loc[:,"Close"])
    plt.legend(stocks)    
    plt.show()

#============================================== SELECTING SIMILIAR STOCKS  =================================================


def select_similiar_stocks(*args):
    #downloading database of a sector from yfinance , sorting by market cap and selecting 
    # top 5 stocks to compare with    
    #trying to use beautiful soup 

    args_list = args[0]
    sector = yf.Ticker(args_list[0]).info["sector"]

    #string manipulation
    sector = sector.lower()
    sector = "ms_"+sector.replace(" ","_")

    url = "https://finance.yahoo.com/sector/"
    
    page = requests.get(url+sector)


    soup = BeautifulSoup(page.content,"html.parser")
    result = soup.find("table")
    data=[]
    #got the respective sector table , now gotta parse it properly using a parser
    rows = result.find_all("tr")
    for row in rows[:-1]:
        if row == rows[0]:
            cols = row.find_all("th")
        else:
            cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols[:-1]]
        data.append(cols)
    
    df = pd.DataFrame(data[1:],columns=data[0])
    print("\n")
    df.sort_values(by=[df.columns.values[7]],inplace=True,ascending=False)
    
    
    #the data has been sorted , now just need to get 5 values 
    df_head = df.head()
    print(df_head)

    #saving the sector data

    path = os.path.join(os.getcwd(),"stonks-scalper-Mk2\\sector-tables\\")
    df_head.to_csv(path+sector+".csv")

    # ISSUE : the problem now is that the sector table doesn't have all the same fields as the stock table 
    # thus have to come up with another function which selects the missing fields 

    overview_table = args[2]
    print(overview_table.columns.values,df_head.columns.values)
    overview_table_cols = overview_table.columns.values
    df_head_cols = df_head.columns.values
    #residue_list = list(set([x.lower() for x in overview_table.columns.values]) and set([x.lower() for x in df_head.columns.values]))
    residue_list = list(overview_table_cols)
    for i in range(len(overview_table_cols)):
        for j in range(i,len(df_head_cols)):
            if overview_table_cols[i].lower() in [x.lower() for x in df_head_cols[j].split(" ")]:
                residue_list.remove(overview_table_cols[i])

    print(residue_list)
    #for test commit

    #retrieved teh missing columsn , now gotta use yfinance to get teh data again
    # an improvement can be made by creating a funciton shared by both select_stocks_overview2 and select_similiar_stocks
    # which is left for future rn , im too lazy 
    #f = csv.writer(open("https://finance.yahoo.com/"))


select_stocks()
#select_sector()    

# get ticker symbols for the stocks with some preset tickers and sort them in the order asked i.e. top_gainers , top_losers , new_high , new_low etc
# get ticker data from yfinance api and append it to a dataframe and get some preset data from the
# already present dataframes

#===================UPDATE=======================

# The individual stock selection and plotting is working , now I need to select the respective stock sector and implement the "-a"(also) argument
# which will get similiar stocks and plot them too
# after that we will work on selecting and sorting the data of all those stocks plotted in the form of a table
# and store that table for future reference aka the LSTM model probably


#test version : where we just sift data from all available dataframes for the given stocks




"""
=========================== For future purposes =====================================

will implement historical in stocks overview using this :

data = yf.download(
        tickers = arg_list,
        threads = True,
        group_by="ticker",
    )
    data = data
    for t in arg_list:
        print(t)
        print(data.loc[:,t].tail())

    time_dur2 = time.time()
    print(time_dur2-time_dur1)

"""