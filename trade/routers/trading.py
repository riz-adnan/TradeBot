from typing import List
from fastapi import APIRouter, Depends, status
from .. import schemas, oauth2
import datetime
import pytz
import schedule
import time
from datetime import date, timedelta
from sqlalchemy.orm import Session
from .. import schemas
# from ..database import SessionLocal, engine
from .. import mongodb
import market_connection as mc1
import market_connection2 as mc2
import yfinance as yf
import numpy as np
import pandas as pd
import pandas_ta as ta
import yfinance as yf
from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import gradio as gr

router = APIRouter(
    prefix = '/trading',
    tags = ['trading']
)

users = mongodb.users
user_helper = mongodb.user_helper


# -------------------------- Trade --------------------------
# Define the start and end times in ET
@router.post('/', status_code = status.HTTP_201_CREATED)
def trading():
     start_time = datetime.time(9, 30)
     end_time = datetime.time(15, 30)
     new_york_timezone = pytz.timezone('America/New_York')
     # session = SessionLocal()

     dataNames =["AAPL","MSFT","AMZN","GOOG","META","TSLA","NVDA","PYPL","INTC","NFLX","ADBE","CSCO","CMCSA","PEP","AVGO","TXN","QCOM","ADP","COST","TMUS"]

     

     

     def create_client(API_KEY, API_SECRET, BASE_URL):
          alpaca_client = TradingClient(API_KEY, API_SECRET, paper=True)
          return alpaca_client

     def append_indicators(stock_data):
          stock_data["VWAP"] = ta.vwap(stock_data.High, stock_data.Low, stock_data.Close, stock_data.Volume)
          stock_data['RSI'] = ta.rsi(stock_data.Close, length=20)
          my_bbands = ta.bbands(stock_data.Close, length=20, std=2.0)
          stock_data = stock_data.join(my_bbands)
          return stock_data

     def prepare_data(stock_data, sequence_length):
          stock_data = stock_data.dropna()
          data = stock_data[['Close', 'RSI', 'VWAP', 'BBU_20_2.0', 'BBM_20_2.0', 'BBL_20_2.0']]
          scaler = MinMaxScaler()
          scaled_data = scaler.fit_transform(data)

          X = []
          y = []
          for i in range(sequence_length, len(scaled_data)):
               X.append(scaled_data[i-sequence_length:i])
               y.append(scaled_data[i, 0])  # Predict the Close price

          X, y = np.array(X), np.array(y)
          return X, y, scaler

     def build_lstm_model(input_shape):
          model = Sequential()
          model.add(LSTM(units=50, return_sequences=True, input_shape=input_shape))
          model.add(Dropout(0.2))
          model.add(LSTM(units=50, return_sequences=False))
          model.add(Dropout(0.2))
          model.add(Dense(units=25))
          model.add(Dense(units=1))

          model.compile(optimizer='adam', loss='mean_squared_error')
          return model

     def train_model(model, X_train, y_train, epochs=50, batch_size=32):
          model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1)
          return model

     def generate_predictions(model, data, scaler, sequence_length):
          scaled_data = scaler.transform(data)
          X_test = []
          for i in range(sequence_length, len(scaled_data)):
               X_test.append(scaled_data[i-sequence_length:i])

          X_test = np.array(X_test)
          predictions = model.predict(X_test)
          predictions = scaler.inverse_transform(np.concatenate((predictions, np.zeros((predictions.shape[0], data.shape[1]-1))), axis=1))[:, 0]
          return predictions

     def placing_order(predictions, api, symbol, current_price, rsi):
          orders = []
          slatr = 1.2 * (max(predictions) - min(predictions))  
          TPSLRatio = 1.5

          for i in range(len(predictions)):
               if predictions[i] > current_price and rsi <= 10:
                    sl1 = current_price - slatr
                    tp1 = current_price + slatr * TPSLRatio
                    order = MarketOrderRequest(
                         symbol=symbol,
                         qty=1,
                         take_profit={'limit_price': tp1},
                         stop_loss={'stop_price': sl1},
                         side=OrderSide.BUY,
                         time_in_force=TimeInForce.DAY)
                    api.submit_order(order)
                    orders.append(order)
               elif predictions[i] < current_price and rsi >= 90:
                    sl1 = current_price + slatr
                    tp1 = current_price - slatr * TPSLRatio
                    order = MarketOrderRequest(
                         symbol=symbol,
                         qty=1,
                         take_profit={'limit_price': tp1},
                         stop_loss={'stop_price': sl1},
                         side=OrderSide.SELL,
                         time_in_force=TimeInForce.DAY)
                    api.submit_order(order)
                    orders.append(order)
          return orders

     # Gradio Interface
     def predict_and_trade(stock_ticker, api_key, api_secret, base_url):
          tickers = [ticker.strip() for ticker in stock_ticker.split(',')]
          results = []

          for ticker in tickers:
               # Fetch data
               stock_data = yf.download(ticker, period="1y", interval="1d")
               stock_data.columns = stock_data.columns.droplevel(1)
               stock_data = append_indicators(stock_data)

               # Prepare data
               sequence_length = 60
               X, y, scaler = prepare_data(stock_data, sequence_length)

               # Build and train the model
               input_shape = (X.shape[1], X.shape[2])
               model = build_lstm_model(input_shape)
               model = train_model(model, X, y)

               # Make predictions
               predictions = generate_predictions(model, stock_data[['Close', 'RSI', 'VWAP', 'BBU_20_2.0', 'BBM_20_2.0', 'BBL_20_2.0']], scaler, sequence_length)
               predict_value = 0
               for i in range(len(predictions)):
                    if not np.isnan(predictions[i]):
                         predict_value = predictions[i]
                         break



               # Create the Alpaca client
               client = create_client(api_key, api_secret, base_url)

               # Place orders based on predictions
               current_price = stock_data['Close'].iloc[-1]
               rsi = stock_data['RSI'].iloc[-1]
               print("error in placing order")
               orders = placing_order(predictions, client, ticker, current_price, rsi)
               print("error in appending result")
               results.append([
                    ticker,

                    [order.json() for order in orders],

                    "predictions : ",
                    predict_value,

               ])
          print("error in returning")
          return results

     def strategy1(API_KEY, API_SECRET, BASE_URL):
         
          for i in dataNames:
               predict_and_trade(i, API_KEY, API_SECRET, BASE_URL)
               print(orders)

     def strategy2(API_KEY, API_SECRET, BASE_URL):
          alpaca_client = mc1.create_client(API_KEY,API_SECRET,BASE_URL)
          flag = True
          for i in dataNames:
               stock_data=yf.download(i, start=date.today()-timedelta(days = 50), end=date.tooday())
               df1 = mc1.generate(stock_data)
               orders,flag = mc1.placing_order(df1,alpaca_client,i, flag)
               if flag == False:
                    break
          print(orders)

     def strategy1_for_all():
          users_list = []
          for user in users.find():
               users_list.append(user_helper(user))
          for i in users_list:
               strategy1(i['api_key_public'], i['api_key_private'], i['base_url'])

     def strategy2_for_all():
          users_list = []
          for user in users.find():
               users_list.append(user_helper(user))
          for i in users_list:
               strategy2(i['api_key_public'], i['api_key_private'], i['base_url'])

     # Schedule the job to run every 5 minutes during market hours (Monday to Friday)
     schedule.every(5).seconds.do(strategy1_for_all)
     schedule.every(1).day.do(strategy2_for_all)

     # Start the scheduler
     while True:
          try:
               # Check if the current day is a weekday (Monday to Friday)
               today = datetime.datetime.now().strftime("%A")
               if today in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
                    # Check if the current time is within market hours
                    now = datetime.datetime.now()
                    new_york_time = now.astimezone(new_york_timezone).time()
                    if start_time <= new_york_time <= end_time:
                         print("Successfull able to do!")
                         schedule.run_pending()
          except Exception as e:
               print(f"An error occurred: {str(e)}")