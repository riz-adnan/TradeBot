# import datetime
# import schedule
# import time
# from sqlalchemy.orm import Session
# from .. import models, schemas

# # Define the start and end times in ET
# start_time = datetime.time(9, 30)
# end_time = datetime.time(15, 30)

# dataNames =["AAPL","MSFT","AMZN","GOOG","META","TSLA","NVDA","PYPL","INTC","NFLX","ADBE","CSCO","CMCSA","PEP","AVGO","TXN","QCOM","ADP","COST","TMUS"]

# def strategy1(API_KEY, API_SECRET, BASE_URL):
#     alpaca_client = mc.create_client(API_KEY,API_SECRET,BASE_URL)
#     backcandles = 15
#     for i in dataNames:
#         stock_data = yf.download(i, start=date.today()-timedelta(days = 50), end=date.today())
#         stock_data = mc2.append_indicator_for_strategy(stock_data, backcandles)
#         stock_data = mc2.signal_generator(stock_data, backcandles)
#         stock_data = mc2.breakpoint_generator(stock_data)
#         dfpl = mc2.final_signal(stock_data)
#         orders = mc2.placing_order(dfpl, alpaca_client, i)
#         print(orders)

# def strategy2(API_KEY, API_SECRET, BASE_URL):
#     alpaca_client = mc1.create_client(API_KEY,API_SECRET,BASE_URL)
#     flag = True
#     for i in dataNames:
#         stock_data=yf.download(i, start=date.today()-timedelta(days = 50), end=date.tooday())
#         df1 = mc1.generate(stock_data)
#         orders,flag = mc1.placing_order(df1,alpaca_client,i, flag)
#         if flag == False:
#             break
#     print(orders)

# def strategy1_for_all(db: Session):
#     users = db.query(models.Users).all()
#     for i in range(len(users)):
#         strategy1(users[i]['api_key_public'], users[i]['api_key_private'], users[i]['base_url'])

# def strategy2_for_all(db: Session):
#     users = db.query(models.Users).all()
#     for i in range(len(users)):
#         strategy2(users[i]['api_key_public'], users[i]['api_key_private'], users[i]['base_url'])

# # Schedule the job to run every 5 minutes during market hours (Monday to Friday)
# schedule.every(5).minutes.do(strategy1_for_all)
# schedule.every(1).day.do(strategy2_for_all)

# # Start the scheduler
# while True:
#     # Check if the current day is a weekday (Monday to Friday)
#     today = datetime.datetime.now().astimezone().strftime("%A")
#     if today in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]:
#         # Check if the current time is within market hours
#         now = datetime.datetime.now().astimezone().time()
#         if start_time <= now <= end_time:
#             schedule.run_pending()
#     time.sleep(60)  # Sleep for 60 seconds

import schedule
import time

print("Started !")

def opener():
    print("Hello after 4 seconds")

schedule.every(4).seconds.do(opener)

while True:
    schedule.run_pending()
     # Sleep for 60 seconds