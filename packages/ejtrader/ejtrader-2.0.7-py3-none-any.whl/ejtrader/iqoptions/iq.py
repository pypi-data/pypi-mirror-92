import logging
import time
import os
from ejtrader_iq.stable_api import IQ_Option
import pandas as pd


def iq_login(verbose = False, iq = None, checkConnection = False,email=None, password=None,AccountType=None):
    
    if verbose:
        logging.basicConfig(level=logging.DEBUG,format='%(asctime)s %(message)s')

    if iq == None:
      print("Trying to connect to IqOption")
      
      iq=IQ_Option(email,password) # YOU HAVE TO ADD YOUR USERNAME AND PASSWORD
      iq.connect()

    if iq != None:
      while True:
        if iq.check_connect() == False:
          print('Error when trying to connect')
          print(iq)
          print("Retrying")
          iq.connect()
        else:
          if not checkConnection:
            print('Successfully Connected! Account type : ' + AccountType)
          break
        time.sleep(3)
    if AccountType == "DEMO":
        iq.change_balance("PRACTICE") # PRACTICE or REAL
        
    elif AccountType == "REAL":
        iq.change_balance("REAL") # PRACTICE or REAL
        

    return iq


def iq_buy_binary(iq,contract,symbol,timeframe):
    
    done,id = iq.buy(contract,symbol,"call",timeframe)
    
    if not done:
        print('Error call')
        print(done, id)
        exit(0)
    
    return id


def iq_sell_binary(iq,contract,symbol,timeframe):
    
    done,id = iq.buy(contract,symbol,"put",timeframe)
    
    if not done:
        print('Error put')
        print(done, id)
        exit(0)
    
    return id
  
def iq_get_candles(iq,symbol,timeframe):
    timeframe = timeframe * 60
    iq_login(iq = iq, checkConnection = True)
    return  iq.get_candles(symbol, int(timeframe), 1000, time.time())

    
def iq_get_all_candles(iq,symbol,timeframe,start_candle):
     
    
    final_data = []
    
    for x in range(1):
        iq_login(iq = iq, checkConnection = True)
        timeframe = timeframe * 60
        data = iq.get_candles(symbol, 300, 1000, start_candle)
        start_candle = data[0]['to']-1
        final_data.extend(data)
    return final_data

def iq_get_data(iq,symbol,symbols,timeframe): 
    timeframe = timeframe * 60
    start_candle = time.time()
    actives = symbols
    final_data = pd.DataFrame()
    for active in actives:
        current = iq_get_all_candles(iq,symbol,int(timeframe),start_candle)
        main = pd.DataFrame()
        useful_frame = pd.DataFrame()
        for candle in current:
            useful_frame = pd.DataFrame(list(candle.values()),index = list(candle.keys())).T.drop(columns = ['at'])
            useful_frame = useful_frame.set_index(useful_frame['id']).drop(columns = ['id'])
            main = main.append(useful_frame)
            main.drop_duplicates()
        if active == symbol:
            final_data = main.drop(columns = {'from','to'})
        else:
            main = main.drop(columns = {'from','to','open','min','max'})
            main.columns = [f'close_{active}',f'volume_{active}']
            final_data = final_data.join(main)
    final_data = final_data.loc[~final_data.index.duplicated(keep = 'first')]
    return final_data
    
def iq_fast_data(iq,symbol,timeframe): 
    iq_login(iq = iq, checkConnection = True)
    timeframe = timeframe * 60
    candles = iq.get_candles(symbol,int(timeframe),300,time.time())
    useful_frame = pd.DataFrame()
    main = pd.DataFrame()
    for candle in candles:
        useful_frame = pd.DataFrame(list(candle.values()),index = list(candle.keys())).T.drop(columns = ['at'])
        useful_frame = useful_frame.set_index(useful_frame['id']).drop(columns = ['id'])
        main = main.append(useful_frame)
        
    return main
    
def iq_get_balance(iq):
    return iq.get_balance()

def iq_market_isOpen(iq):
    isOpen = []
    opened_market=iq.get_all_open_time()
    
    for type_name, data in opened_market.items():
        for Asset,value in data.items():
            if value['open'] == True:
                value = 'open'
            else:
                value = 'close'
            result = {
            "Asset": Asset,
            "Type" : type_name, 
            "Status" : value
             }
            isOpen.append(result)
        
    return isOpen



def iq_get_payout(iq,symbol='EURUSD',typed='turbo'):
    payout = iq.get_all_profit()   
    return payout[symbol][typed]
