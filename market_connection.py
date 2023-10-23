import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_ta as ta
import time
import yfinance as yf
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce

def create_client(API_KEY,API_SECRET,BASE_URL):
    alpaca_client = TradingClient(API_KEY,API_SECRET,paper=True)
    return alpaca_client

def append_indicator_for_startegy(df):
    # qqe mod
    qqe_value = ta.qqe(df['Close'])
    # hull suite len = 60 mul = 3
    hull_suite = ta.hma(df['Close'], 60, 3)
    # volume oscillator
    volume_oscillator = ta.pvo(df['Volume'], 12, 26, 9, False)
    # add above to df
    qqe_value = qqe_value[qqe_value.columns[0]]
    volume_oscillator = volume_oscillator[volume_oscillator.columns[0]]

    df['qqe_value'] = qqe_value
    df['hull_suite'] = hull_suite
    df['volume_oscillator'] = volume_oscillator
    
    return df


def signal_generation(df,volumelimit,qqelimit):
    df['signal'] = 0;#0,-1 sell,1 buy

    #blue in qqe green in hull price above bar
    df.loc[(df['qqe_value'] > qqelimit) & (df['hull_suite'] > df['Close']) & (df['volume_oscillator'] > volumelimit), 'signal'] = 1

    df.loc[(df['qqe_value'] < qqelimit) & (df['hull_suite'] < df['Close']) & (df['volume_oscillator'] < -volumelimit), 'signal'] = -1
    return df

def generate(df):
    df1=df.copy()
    df1 = append_indicator_for_startegy(df1)
    df1 = signal_generation(df1,0.1,50)     # Volumelimit and qqelimit
    return df1
    
# def testspecific(df , volumelimit,qqelimit=50,profitstop=1.05,lossstop=0.95):
#     df1=df.copy()
#     df1 = append_indicator_for_startegy(df1)
#     df1 = signal_generation(df1,volumelimit,1,qqelimit,profitstop,lossstop)	 # Volumelimit and qqelimit
    
# pp = data[0].copy()

# pp = append_indicator_for_startegy(pp)
# pp = signal_generation(pp,0.1,2,50,1.05,0.95)
# print(pp.loc[pp['signal'] == 1])

# for i in range(len(data)):
#     # test only for valid data
#     if len(data[i]) > 0:
#         #params
#         # df ,amount to be tetsted ,
#         # volumelinit lower to place order 
#         # followoriginal 1 2 3 1 original 2 duplicate 3 both RECOMMENDED 2
#         # qqelimit in qqe value
#         # profitstop obv
#         # lossstop obv
#         prft = testspecific(data[i],100000,0.1,2,50,20,0.95)
#         #print name and actual stock loss
#         print(dataNames[i],"found",prft,"actual",data[i]['Close'][len(data[i])-1]/data[i]['Close'][0]*100)# obv cant get actual

def placing_order(df, alpaca_client, symbol, flag):
    orders = []
    signal = df.signal.iloc[-1]
    if (signal == 1):
        order = MarketOrderRequest(
			symbol = symbol,
			qty = 3,
			side = OrderSide.BUY,
			time_in_force = TimeInForce.DAY)
        alpaca_client.submit_order(order)
        orders.append(order)
        time.sleep(10)
    elif signal == -1:
        order = MarketOrderRequest(
            symbol = symbol,
            qty = 3,
            side = OrderSide.SELL,
            time_in_force = 'gtc')
        alpaca_client.submit_order(order)
        orders.append(order)
        time.sleep(10)
    if len(orders) > 0:
        flag = False
    return orders, flag