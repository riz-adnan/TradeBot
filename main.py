from fastapi import FastAPI
from trade.routers import user, authentication, trading
from trade.trading_scheduler import shutdown_scheduler, start_scheduler
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(trading.router)


@app.on_event("startup")
def startup_auto_trading_scheduler():
    start_scheduler()


@app.on_event("shutdown")
def shutdown_auto_trading_scheduler():
    shutdown_scheduler()
