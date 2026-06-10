from fastapi import FastAPI
from trade.routers import user, authentication, trading


app = FastAPI()

app.include_router(authentication.router)
app.include_router(user.router)
app.include_router(trading.router)
