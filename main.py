from fastapi import FastAPI, Depends
# from trade.database import engine, SessionLocal
from trade.routers import user, authentication, trading
# from trade.routers import investment, sip, sop, admin
import market_connection as mc1
import market_connection2 as mc2
import yfinance as yf
from datetime import date, timedelta
import datetime
import schedule
import time
from sqlalchemy.orm import Session
from trade import schemas, mongodb
import pytz


app = FastAPI()
# models.Base.metadata.create_all(engine)

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(trading.router)
# app.include_router(admin.router)
# app.include_router(investment.router)
# app.include_router(sip.router)
# app.include_router(sop.router)





















# ------------------------------- Strategies -------------------------------
# dataNames =["AAPL","MSFT","AMZN","GOOG","META","TSLA","NVDA","PYPL","INTC","NFLX","ADBE","CSCO","CMCSA","PEP","AVGO","TXN","QCOM","ADP","COST","TMUS"]

# API_KEY = "PKGBPHMS9V35JY3B1QUH"
# API_SECRET = "stBGcuXV3aLgOR7FSLc4eT0brvJYlQisZoxZRJrZ"
# BASE_URL = "https://paper-api.alpaca.markets"

# alpaca_client = mc.create_client(API_KEY,API_SECRET,BASE_URL)

# ------------------------------- Strategy 1 -------------------------------

# flag = True
# for i in dataNames:
#     stock_data=yf.download(i, start=date.today()-timedelta(days = 50), end=date.tooday())
#     df1 = mc.generate(stock_data)
#     orders,flag = mc.placing_order(df1,alpaca_client,i, flag)
#     if flag == False:
#         break
# print(orders)



'''# # def my_task():
# #     current_time = datetime.now().time()
# #     if current_time >= datetime.strptime("09:30:00", "%H:%M:%S").time() and current_time <= datetime.strptime("15:30:00", "%H:%M:%S").time():
# #         mc.signal_generation(df,0.5,0.5)
# #         mc.generate(df)

# # # Schedule the task to run on weekdays (Monday to Friday) from 9:30 am to 3:30 pm
# # schedule.every().day.at("09:30").do(my_task)
# # schedule.every().day.at("10:30").do(my_task)
# # schedule.every().day.at("11:30").do(my_task)
# # schedule.every().day.at("12:30").do(my_task)
# # schedule.every().day.at("13:30").do(my_task)
# # schedule.every().day.at("14:30").do(my_task)
# # schedule.every().day.at("15:30").do(my_task)

# # # Run the scheduler loop
# # while True:
# #     schedule.run_pending()
# #     time.sleep(1)'''



# ------------------------------- Strategy 2 -------------------------------

# backcandles = 15
# for i in dataNames:
#     stock_data = yf.download(i, start=date.today()-timedelta(days = 50), end=date.today())
#     stock_data = mc2.append_indicator_for_strategy(stock_data, backcandles)
#     stock_data = mc2.signal_generator(stock_data, backcandles)
#     stock_data = mc2.breakpoint_generator(stock_data)
#     dfpl = mc2.final_signal(stock_data)
#     orders = mc2.placing_order(dfpl, alpaca_client, i)
#     print(orders)
































# import numpy as np
# import pandas as pd
# import matplotlib.pyplot as plt
# import pandas_ta as ta
# from datetime import date, timedelta
# import yfinance as yf
# from alpaca.trading.client import TradingClient
# from alpaca.trading.requests import MarketOrderRequest
# from alpaca.trading.enums import OrderSide, TimeInForce
# from backtesting import Strategy, Backtest

# def create_client(API_KEY,API_SECRET,BASE_URL):
#     api = TradingClient(API_KEY,API_SECRET,paper=True)
#     return api

# API_KEY = "PKGBPHMS9V35JY3B1QUH"
# API_SECRET = "stBGcuXV3aLgOR7FSLc4eT0brvJYlQisZoxZRJrZ"
# BASE_URL = "https://paper-api.alpaca.markets"
# api = create_client(API_KEY,API_SECRET,BASE_URL)

# stock_selected="ZOMATO.NS"

# stock_data=yf.download(stock_selected,start=date.today()-timedelta(days = 50),end=date.today(), interval="5m")
# print(stock_data)

# import pandas_ta as ta

# stock_data["VWAP"]=ta.vwap(stock_data.High, stock_data.Low, stock_data.Close, stock_data.Volume)
# stock_data['RSI']=ta.rsi(stock_data.Close, length=20)
# my_bbands = ta.bbands(stock_data.Close, length=20, std=2.0)
# stock_data=stock_data.join(my_bbands)


# VWAPsignal = [0]*len(stock_data)
# backcandles = 15

# for row in range(backcandles, len(stock_data)):
#     upt = 1
#     dnt = 1
#     for i in range(row-backcandles, row+1):
#         if max(stock_data.Open.iloc[i], stock_data.Close.iloc[i])>=stock_data.VWAP.iloc[i]:
#             dnt=0
#         if min( stock_data.Open.iloc[i], stock_data.Close.iloc[i])<= stock_data.VWAP.iloc[i]:
#             upt=0
#     if upt==1 and dnt==1:
#         VWAPsignal[row]=3
#     elif upt==1:
#         VWAPsignal[row]=2
#     elif dnt==1:
#         VWAPsignal[row]=1

# stock_data['VWAPSignal'] = VWAPsignal


# def TotalSignal(l):
#     BBU_14_2_0 = stock_data.get('BBU_14_2.0', pd.Series([0.0]*len(stock_data)))[l]
#     if stock_data.VWAPSignal.iloc[l] == 2 and stock_data.Close.iloc[l] <= BBU_14_2_0 and stock_data.RSI.iloc[l] < 45:
#         return 2
#     if stock_data.VWAPSignal.iloc[l] == 1 and stock_data.Close.iloc[l] >= BBU_14_2_0 and stock_data.RSI.iloc[l] > 55:
#         return 1
#     return 0

# TotSignal = [0] * len(stock_data)
# for row in range(backcandles, len(stock_data)): 
#     TotSignal[row] = TotalSignal(row)

# stock_data['TotalSignal'] = TotSignal


# def pointposbreak(x):
#     if x['TotalSignal']==1:
#         return x['High']+1e-4
#     elif x['TotalSignal']==2:
#         return x['Low']-1e-4
#     else:
#         return np.nan

# stock_data['pointposbreak'] = stock_data.apply(lambda row: pointposbreak(row), axis=1)



# # import plotly.graph_objects as go
# # from plotly.subplots import make_subplots
# # from datetime import datetime
# # st=10400
# # dfpl = stock_data[st:st+350]
# # dfpl.reset_index(inplace=True)
# # fig = go.Figure(data=[go.Candlestick(x=dfpl.index,
# #                 open=dfpl['Open'],
# #                 high=dfpl['High'],
# #                 low=dfpl['Low'],
# #                 close=dfpl['Close']),
# #                 go.Scatter(x=dfpl.index, y=dfpl.VWAP, 
# #                            line=dict(color='blue', width=1), 
# #                            name="VWAP"), 
# #                 go.Scatter(x=dfpl.index, y=dfpl['BBL_14_2.0'], 
# #                            line=dict(color='green', width=1), 
# #                            name="BBL"),
# #                 go.Scatter(x=dfpl.index, y=dfpl['BBU_14_2.0'], 
# #                            line=dict(color='green', width=1), 
# #                            name="BBU")])

# # fig.add_scatter(x=dfpl.index, y=dfpl['pointposbreak'], mode="markers",
# #                 marker=dict(size=10, color="MediumPurple"),
# #                 name="Signal")
# # fig.show()



# dfpl = stock_data.copy()
# import pandas_ta as ta
# dfpl['ATR']=ta.atr(dfpl.High, dfpl.Low, dfpl.Close, length=7)
# #help(ta.atr)
# def SIGNAL():
#     return dfpl.TotalSignal


# # from backtesting import Strategy
# # from backtesting import Backtest

# # class MyStrat(Strategy):
# #     initsize = 0.99
# #     mysize = initsize
# #     def init(self):
# #         super().init()
# #         self.signal1 = self.I(SIGNAL)

# #     def next(self):
# #         super().next()
# #         slatr = 1.2*self.data.ATR[-1]
# #         TPSLRatio = 1.5

# #         if len(self.trades)>0:
# #             if self.trades[-1].is_long and self.data.RSI[-1]>=90:
# #                 self.trades[-1].close()
# #             elif self.trades[-1].is_short and self.data.RSI[-1]<=10:
# #                 self.trades[-1].close()
        
# #         if self.signal1==2 and len(self.trades)==0:
# #             sl1 = self.data.Close[-1] - slatr
# #             tp1 = self.data.Close[-1] + slatr*TPSLRatio
# #             self.buy(sl=sl1, tp=tp1, size=self.mysize)
        
# #         elif self.signal1==1 and len(self.trades)==0:         
# #             sl1 = self.data.Close[-1] + slatr
# #             tp1 = self.data.Close[-1] - slatr*TPSLRatio
# #             self.sell(sl=sl1, tp=tp1, size=self.mysize)

# # bt = Backtest(dfpl, MyStrat, cash=100, margin=1/10, commission=0.00)
# # stat = bt.run()
# # stat
# print(dfpl)

# # class MyStrat(Strategy):
# #     initsize = 0.99
# #     mysize = initsize
# #     def init(self):
# #         super().init()
# #         self.signal1 = self.I(SIGNAL)

# #     def next(self):
# #         super().next()
# #         slatr = 1.2*self.data.ATR[-1]
# #         TPSLRatio = 1.5
# #         orders = []
# #         c = 0

# #         if len(self.trades)>0:
# #             if self.trades[-1].is_long and self.data.RSI[-1]>=90:
# #                 self.trades[-1].close()
# #             elif self.trades[-1].is_short and self.data.RSI[-1]<=10:
# #                 self.trades[-1].close()
# #         c+=1
        
# #         if self.signal1==2 and len(self.trades)==0:
# #             sl1 = self.data.Close[-1] - slatr
# #             tp1 = self.data.Close[-1] + slatr*TPSLRatio
# #             order = MarketOrderRequest(
# #                 symbol = 'TSLA',
# #                 qty = 1,
# #                 side = OrderSide.BUY,
# #                 time_in_force = TimeInForce.DAY)
# #             api.submit_order(order)
# #             orders.append(order)
        
# #         elif self.signal1==1 and len(self.trades)==0:         
# #             sl1 = self.data.Close[-1] + slatr
# #             tp1 = self.data.Close[-1] - slatr*TPSLRatio
# #             order = MarketOrderRequest(symbol = 'TSLA', qty = 1, side = OrderSide.SELL,time_in_force = 'gtc')
# #             api.submit_order(order)
# #             orders.append(order)
# #         print(orders)

# # bt = Backtest(dfpl, MyStrat, margin=1/10, commission=0.00)
# # stat = bt.run()
# # print(stat)


# def placing_order(df, api, symbol):
#     # pos_held = False
#     orders = []
#     signal = 1
#     slatr = 1.2*df.ATR.iloc[-1]
#     TPSLRatio = 1.5
#     if signal==2 or df.RSI.iloc[-1]<=10:
#         sl1 = df.Close[-1] - slatr
#         tp1 = df.Close[-1] + slatr*TPSLRatio
#         order = MarketOrderRequest(
# 			symbol = symbol,
# 			qty = 1,
#             take_profit={'limit_price':tp1},
#             stop_loss={'stop_price': sl1},
# 			side = OrderSide.BUY,
# 			time_in_force = TimeInForce.DAY)
#         api.submit_order(order)
#         orders.append(order)
#     elif signal==1 or df.RSI.iloc[-1]>=90:         
#         sl1 = df.Close[-1] + slatr
#         tp1 = df.Close[-1] - slatr*TPSLRatio
#         order = MarketOrderRequest(
#             symbol = symbol, qty = 1,
#             take_profit={'limit_price':tp1},
#             stop_loss={'stop_price': sl1},
#             side = OrderSide.SELL,
#             time_in_force = 'gtc')
#         api.submit_order(order)
#         orders.append(order)
#     return orders
# orders = placing_order(dfpl, api, 'TSLA')
# print(orders)