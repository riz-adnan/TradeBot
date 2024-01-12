from fastapi import FastAPI, Depends
from trade.routers import user, authentication, trading
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

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(trading.router)