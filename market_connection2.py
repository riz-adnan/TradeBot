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
    slatr = 1.2 * (max(predictions) - min(predictions))  # Example stop loss and take profit calculation
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

