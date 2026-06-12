import os
from typing import Dict, List, Literal

from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderClass, OrderSide, TimeInForce
from alpaca.trading.requests import (
    MarketOrderRequest,
    StopLossRequest,
    TakeProfitRequest,
)
from fastapi import APIRouter, HTTPException, status
import requests

from .. import schemas
from ..trading_scheduler import (
    get_scheduler_status,
    run_auto_trade_scan,
    start_scheduler,
    stop_scheduler,
)


router = APIRouter(prefix="/trading", tags=["trading"])

Mode = Literal["daily", "intraday"]

MODEL_API_URL = os.getenv(
    "MODEL_API_URL",
    "https://rizvizwizard-trading-model-api.hf.space",
).rstrip("/")


def normalize_ticker(ticker: str) -> str:
    ticker = ticker.strip().upper()
    if not ticker:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ticker cannot be empty.",
        )
    return ticker


def get_prediction_from_hf(ticker: str, mode: Mode) -> dict:
    if mode not in {"daily", "intraday"}:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Mode must be "daily" or "intraday".',
        )

    try:
        response = requests.post(
            f"{MODEL_API_URL}/predict/{mode}",
            json={"ticker": normalize_ticker(ticker)},
            timeout=60,
        )

        if response.status_code != 200:
            try:
                detail = response.json()
            except Exception:
                detail = response.text

            raise HTTPException(
                status_code=response.status_code,
                detail={
                    "message": "HF model API returned an error",
                    "hf_detail": detail,
                },
            )

        return response.json()

    except requests.exceptions.Timeout:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            detail="Model API timeout",
        )
    except requests.exceptions.RequestException as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Model API unavailable: {str(exc)}",
        )


def place_bracket_order(
    ticker: str,
    decision: str,
    current_price: float,
    atr: float,
    api_key: str,
    api_secret: str,
) -> Dict:
    if decision == "BUY":
        side = OrderSide.BUY
        take_profit_price = current_price + 2 * atr
        stop_loss_price = current_price - atr
    elif decision == "SELL":
        side = OrderSide.SELL
        take_profit_price = current_price - 2 * atr
        stop_loss_price = current_price + atr
    else:
        return {"ticker": ticker, "message": "HOLD: no order placed."}

    if take_profit_price <= 0 or stop_loss_price <= 0:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Invalid ATR bracket prices for {ticker}.",
        )

    client = TradingClient(api_key, api_secret, paper=True)
    order_request = MarketOrderRequest(
        symbol=ticker,
        qty=1,
        side=side,
        time_in_force=TimeInForce.DAY,
        order_class=OrderClass.BRACKET,
        take_profit=TakeProfitRequest(limit_price=round(take_profit_price, 2)),
        stop_loss=StopLossRequest(stop_price=round(stop_loss_price, 2)),
    )
    order = client.submit_order(order_request)
    if hasattr(order, "model_dump"):
        return order.model_dump(mode="json")
    return order.dict()


def execute_for_tickers(
    tickers: List[str],
    mode: Mode,
    api_key: str,
    api_secret: str,
) -> Dict[str, List[Dict]]:
    if not tickers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one ticker is required.",
        )

    results = []
    for ticker in tickers:
        signal = get_prediction_from_hf(ticker, mode)
        decision = signal.get("decision")

        if decision == "HOLD":
            results.append({**signal, "message": "HOLD: no order placed."})
            continue

        if decision not in {"BUY", "SELL"}:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail={
                    "message": "HF model API returned an invalid decision",
                    "signal": signal,
                },
            )

        try:
            order = place_bracket_order(
                ticker=signal["ticker"],
                decision=decision,
                current_price=float(signal["current_price"]),
                atr=float(signal["ATR"]),
                api_key=api_key,
                api_secret=api_secret,
            )
        except KeyError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail={
                    "message": f"HF model API response missing required field: {exc.args[0]}",
                    "signal": signal,
                },
            )

        results.append({**signal, "order": order})

    return {"mode": mode, "results": results}


@router.post("/predict/daily")
def predict_daily(request: schemas.PredictRequest):
    return get_prediction_from_hf(request.ticker, "daily")


@router.post("/predict/intraday")
def predict_intraday(request: schemas.PredictRequest):
    return get_prediction_from_hf(request.ticker, "intraday")


@router.post("/execute/daily")
def execute_daily(request: schemas.ExecuteTradeRequest):
    return execute_for_tickers(
        request.tickers,
        "daily",
        request.api_key,
        request.api_secret,
    )


@router.post("/execute/intraday")
def execute_intraday(request: schemas.ExecuteTradeRequest):
    return execute_for_tickers(
        request.tickers,
        "intraday",
        request.api_key,
        request.api_secret,
    )


@router.get("/auto/status")
def auto_trading_status():
    return get_scheduler_status()


@router.post("/auto/run-once")
def auto_trading_run_once():
    return run_auto_trade_scan(force=True)


@router.post("/auto/start")
def auto_trading_start():
    return start_scheduler()


@router.post("/auto/stop")
def auto_trading_stop():
    return stop_scheduler()
