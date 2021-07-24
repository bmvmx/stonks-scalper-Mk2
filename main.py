#====================================== STONKS SCALPER MK2  ===========================================================
import numpy as np
import matplotlib.pyplot as plt
from numpy.lib.utils import info
import yfinance as yf
import  yahoo_fin.stock_info as si
import pandas as pd
import argparse as ap
#from operator import itemgetter
import time
from bs4 import BeautifulSoup

from tabulate import tabulate
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
    parser.add_argument("--a",action="store_true",dest="also",help="-a used to add other companies in same sector")
    parser.add_argument("--v",action="store_true",dest="valuation",help="-v gives all the ratios for the respective stocks ")
    parser.add_argument("--save",action="store_true",help="to save the dataset to a file")
    parser.add_argument("--f",dest="financial",type=str,help="--f gives the financial data like the balance sheet , income statement etc  , bs - balance sheet , is - incomestatement , cs - cash flow")

    args = parser.parse_args()
    
    if args.stocks:
        
        overview_table = select_stocks_overview2(args.stocks)

    else:    
    
        overview_table = select_stocks_overview2(preset_stock_list)
    
     
    if args.also:

        stocks = select_similiar_stocks(args.stocks,args.historical if args.historical else "ytd",overview_table)
    else:

        stocks=[]

    if args.valuation:
        
        stock_valuation(stocks if stocks else args.stocks)

    if args.historical:
        
        preview_historical(stocks if stocks else args.stocks,args.historical)
     
    
    if args.financial:
        
        stock_financial(stocks if stocks else args.stocks,args.financial)
#=================================  OVERVIEW  ==========================================

def select_stocks_overview2(*args,**kwargs):
    # ISSUE : implement multithreading to stop the delays when more than 2 stocks are selected

    time_dur1 = time.time()
    
    df = stock_picker(args[0])
    print(df)
    return df
    

def stock_picker(*args,**kwargs):
    #this new function will just select stocks passed to him as a list and also the sectors/ratios/anything that can 
    # be passed to info() and give out a dataframe

    stock_list = args[0]
    if len(args)>1:
        info_list = args[1]
    else:
        info_list=[]

    stock_data=[]
    if info_list:
        stock_data.append(info_list)
       
    else:
        info_list = ["sector","marketCap","country","trailingPE","currentPrice","52WeekChange","dividendYield"]
        stock_data.append(info_list)
    for i in stock_list:
        list1 = list(map(yf.Ticker(i).info.get,info_list))
        list1.insert(0,i)
        stock_data.append(list1)
    return pd.DataFrame(stock_data[1:],columns=["symbol",*stock_data[0]])



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
    # print(df_head)

    #saving the sector data

    path = os.path.join(os.getcwd(),"stonks-scalper-Mk2\\sector-tables\\")
    df_head.to_csv(path+sector+".csv")

    # ISSUE : the problem now is that the sector table doesn't have all the same fields as the stock table 
    # thus have to come up with another function which selects the missing fields 

    overview_table = args[2]
    #print(overview_table.columns.values,df_head.columns.values)
    overview_table_cols = overview_table.columns.values
    df_head_cols = df_head.columns.values
    #residue_list = list(set([x.lower() for x in overview_table.columns.values]) and set([x.lower() for x in df_head.columns.values]))
    residue_list = list(overview_table_cols)
    for i in range(len(overview_table_cols)):
        for j in range(i,len(df_head_cols)):
            if overview_table_cols[i].lower() in [x.lower() for x in df_head_cols[j].split(" ")]:
                residue_list.remove(overview_table_cols[i])

    #print(residue_list)

    #for test commit

    #retrieved teh missing columns , now gotta use yfinance to get teh data again
    # an improvement can be made by creating a funciton shared by both select_stocks_overview2 and select_similiar_stocks
    # which is left for future rn , im too lazy 
    
    stock_list = list(df_head.iloc[:,0])
    df = stock_picker(stock_list,residue_list)


    #now merging the datframes 

    df = pd.concat([overview_table,df])
    df.reset_index(drop=True)
    print(df)
    return args_list+stock_list




#========================================= STOCK VALUATION ==============================================================

def stock_valuation(*args):
    ratios = ["currentRatio","quickRatio","priceToBook","shortRatio","forwardPE","pegRatio","ytdReturn","ebitda"]
    stock_list = args[0]
    df = stock_picker(stock_list,ratios)
    print("\n")
    print(df)


def stock_financial(*args):
    stock_list = args[0]
    options={"bs":"get_balance_sheet","is":"get_income_statement","cs":"get_cash_flow"}
    key = args[1]
    
    
    
    df = pd.DataFrame()

    for ch in stock_list:
        str_method = "si.{}('{}')".format(options[key],ch)
        print(str_method)
        
        if not df.empty:

            f_data = eval(str_method)
            df = pd.concat([df.iloc[:,1],f_data.iloc[:,1]],axis=1)
        else:
            df =  eval(str_method)
            continue
        
    df.columns = stock_list
    pd.options.display.float_format = '{:,.2f}'.format
    print(df)
    


    #gotta print the table in a better format
    #issue : can either print data in a pretty table format or can format the data in a better way

    #added the balance sheet functionality , now gotta add income statement and a ratio one

    
#implementing save feature which saves the database to a file
# def dataset_save(df):
#     path = os.path.join(os.getcwd(),"stonks-scalper-Mk2\\sector-tables\\")
#     df.to_csv(path+"recent_database"+".csv")


select_stocks()
    


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

"""

============================== WHAT TO DO NEXT  ======================================

 Now we need to create a comparison analysis for stocks
    -stocks can vary in numbers from 1 at least to 10 from the sector
    -different criteria like overview(sector , Industry ,Market Cap , Volume etc)
    -valuation(all teh diff ratios)
    -financial(dividends , ROE , ROA , ROI , Earnings)
    -historical(historical price performance using a chart)
    -sentiment from finbrain , yahoo finance etc(?)

    from this list , we've done the first task and second
    now for the valuation ,financial , historical(done) , sentiment



"""