import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pandas_ta as ta
import yfinance as yf
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from backtesting import Strategy, Backtest
import pandas_ta as ta

def create_client(API_KEY,API_SECRET,BASE_URL):
    alpaca_client = TradingClient(API_KEY,API_SECRET,paper=True)
    return alpaca_client


def append_indicator_for_strategy(stock_data, backcandles):
    stock_data["VWAP"]=ta.vwap(stock_data.High, stock_data.Low, stock_data.Close, stock_data.Volume)
    stock_data['RSI']=ta.rsi(stock_data.Close, length=20)
    my_bbands = ta.bbands(stock_data.Close, length=20, std=2.0)
    stock_data=stock_data.join(my_bbands)

    VWAPsignal = [0]*len(stock_data)

    for row in range(backcandles, len(stock_data)):
        upt = 1
        dnt = 1
        for i in range(row-backcandles, row+1):
            if max(stock_data.Open.iloc[i], stock_data.Close.iloc[i])>=stock_data.VWAP.iloc[i]:
                dnt=0
            if min( stock_data.Open.iloc[i], stock_data.Close.iloc[i])<= stock_data.VWAP.iloc[i]:
                upt=0
        if upt==1 and dnt==1:
            VWAPsignal[row]=3
        elif upt==1:
            VWAPsignal[row]=2
        elif dnt==1:
            VWAPsignal[row]=1

    stock_data['VWAPSignal'] = VWAPsignal
    return stock_data


def TotalSignal(stock_data, l):
    BBU_14_2_0 = stock_data.get('BBU_20_2.0', pd.Series([0.0]*len(stock_data)))[l]
    if stock_data.VWAPSignal.iloc[l] == 2 and stock_data.Close.iloc[l] <= BBU_14_2_0 and stock_data.RSI.iloc[l] < 45:
        return 2
    if stock_data.VWAPSignal.iloc[l] == 1 and stock_data.Close.iloc[l] >= BBU_14_2_0 and stock_data.RSI.iloc[l] > 55:
        return 1
    return 0


def signal_generator(stock_data, backcandles):
    TotSignal = [0] * len(stock_data)
    for row in range(backcandles, len(stock_data)): 
        TotSignal[row] = TotalSignal(stock_data, row)

    stock_data['TotalSignal'] = TotSignal
    return stock_data


def pointposbreak(stock_data):
    if stock_data['TotalSignal']==1:
        return stock_data['High']+1e-4
    elif stock_data['TotalSignal']==2:
        return stock_data['Low']-1e-4
    else:
        return np.nan

def breakpoint_generator(stock_data):
    stock_data['pointposbreak'] = stock_data.apply(lambda row: pointposbreak(row), axis=1)
    return stock_data


def final_signal(stock_data):
    dfpl = stock_data.copy()
    dfpl['ATR']=ta.atr(dfpl.High, dfpl.Low, dfpl.Close, length=7)
    return dfpl

# def SIGNAL(dfpl):
#     return dfpl.TotalSignal



def placing_order(df, api, symbol):
    orders = []
    signal = 1
    slatr = 1.2*df.ATR.iloc[-1]
    TPSLRatio = 1.5
    if signal==2 or df.RSI.iloc[-1]<=10:
        sl1 = df.Close[-1] - slatr
        tp1 = df.Close[-1] + slatr*TPSLRatio
        order = MarketOrderRequest(
			symbol = symbol,
			qty = 1,
            take_profit={'limit_price':tp1},
            stop_loss={'stop_price': sl1},
			side = OrderSide.BUY,
			time_in_force = TimeInForce.DAY)
        api.submit_order(order)
        orders.append(order)
    elif signal==1 or df.RSI.iloc[-1]>=90:         
        sl1 = df.Close[-1] + slatr
        tp1 = df.Close[-1] - slatr*TPSLRatio
        order = MarketOrderRequest(
            symbol = symbol, qty = 1,
            take_profit={'limit_price':tp1},
            stop_loss={'stop_price': sl1},
            side = OrderSide.SELL,
            time_in_force = 'gtc')
        api.submit_order(order)
        orders.append(order)
    return orders
