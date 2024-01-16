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

     def strategy1(API_KEY, API_SECRET, BASE_URL):
          alpaca_client = mc1.create_client(API_KEY,API_SECRET,BASE_URL)
          backcandles = 15
          for i in dataNames:
               stock_data = yf.download(i, start=date.today()-timedelta(days = 50), end=date.today())
               stock_data = mc2.append_indicator_for_strategy(stock_data, backcandles)
               stock_data = mc2.signal_generator(stock_data, backcandles)
               stock_data = mc2.breakpoint_generator(stock_data)
               dfpl = mc2.final_signal(stock_data)
               orders = mc2.placing_order(dfpl, alpaca_client, i)
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