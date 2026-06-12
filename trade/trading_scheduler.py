from datetime import datetime, time, timedelta
from typing import Any, Dict, List
from zoneinfo import ZoneInfo

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import GetOrdersRequest
from alpaca.trading.enums import QueryOrderStatus
from apscheduler.schedulers.background import BackgroundScheduler

from . import mongodb


TICKERS = [
    "AAPL",
    "MSFT",
    "NVDA",
    "AMZN",
    "GOOG",
    "META",
    "TSLA",
    "AVGO",
    "COST",
    "NFLX",
    "ADBE",
    "AMD",
    "PEP",
    "CSCO",
    "QCOM",
    "INTC",
    "PYPL",
    "TXN",
    "CMCSA",
    "TMUS",
]

MODE = "intraday"
MAX_TRADES_PER_USER_PER_DAY = 3
NEW_YORK_TZ = ZoneInfo("America/New_York")

scheduler = BackgroundScheduler(timezone=NEW_YORK_TZ)
last_run_summary: Dict[str, Any] = {
    "last_run_time": None,
    "users_scanned": 0,
    "trades_placed": 0,
    "skipped": 0,
    "errors": 0,
    "market_open": False,
}


def is_market_open(now: datetime | None = None) -> bool:
    now = now or datetime.now(NEW_YORK_TZ)
    if now.weekday() >= 5:
        return False
    return time(9, 30) <= now.time() <= time(16, 0)


def get_users_with_alpaca_keys() -> List[Dict[str, Any]]:
    return list(
        mongodb.users.find(
            {
                "api_key_public": {"$exists": True, "$nin": ["", None]},
                "api_key_private": {"$exists": True, "$nin": ["", None]},
            }
        )
    )


def serialize_mongo_user_id(user: Dict[str, Any]) -> str:
    return str(user.get("_id") or user.get("id") or user.get("email") or "unknown")


def market_day_bounds(now: datetime | None = None) -> tuple[datetime, datetime]:
    now = now or datetime.now(NEW_YORK_TZ)
    start = datetime.combine(now.date(), time.min, tzinfo=NEW_YORK_TZ)
    end = start + timedelta(days=1)
    return start, end


def count_trades_today(user: Dict[str, Any]) -> int:
    start, end = market_day_bounds()
    return mongodb.trade_logs.count_documents(
        {
            "user_id": serialize_mongo_user_id(user),
            "order_status": "placed",
            "created_at": {"$gte": start, "$lt": end},
        }
    )


def is_valid_price(value: Any) -> bool:
    try:
        return float(value) > 0
    except (TypeError, ValueError):
        return False


def is_strong_signal(signal: Dict[str, Any]) -> bool:
    decision = signal.get("decision")
    try:
        probability = float(signal.get("predicted_probability"))
    except (TypeError, ValueError):
        return False

    if not is_valid_price(signal.get("current_price")) or not is_valid_price(signal.get("ATR")):
        return False
    if decision == "BUY":
        return probability >= 0.70
    if decision == "SELL":
        return probability <= 0.30
    return False


def make_alpaca_client(user: Dict[str, Any]) -> TradingClient:
    return TradingClient(
        user["api_key_public"],
        user["api_key_private"],
        paper=True,
    )


def has_open_order_or_position(user: Dict[str, Any], ticker: str) -> bool:
    client = make_alpaca_client(user)

    orders = client.get_orders(
        filter=GetOrdersRequest(status=QueryOrderStatus.OPEN)
    )
    for order in orders:
        if getattr(order, "symbol", "").upper() == ticker:
            return True

    try:
        client.get_open_position(ticker)
        return True
    except Exception:
        return False


def log_trade_action(
    user: Dict[str, Any],
    ticker: str,
    signal: Dict[str, Any] | None,
    order_status: str,
    order_response: Any = None,
    reason_skipped: str | None = None,
) -> None:
    signal = signal or {}
    mongodb.trade_logs.insert_one(
        {
            "user_id": serialize_mongo_user_id(user),
            "ticker": ticker,
            "mode": signal.get("mode", MODE),
            "signal": signal,
            "decision": signal.get("decision"),
            "predicted_probability": signal.get("predicted_probability"),
            "current_price": signal.get("current_price"),
            "RSI": signal.get("RSI"),
            "EMA_20": signal.get("EMA_20"),
            "EMA_50": signal.get("EMA_50"),
            "ATR": signal.get("ATR"),
            "order_status": order_status,
            "order_response": order_response,
            "reason_skipped": reason_skipped,
            "created_at": datetime.now(NEW_YORK_TZ),
        }
    )


def run_auto_trade_scan(force: bool = False) -> Dict[str, Any]:
    from .routers.trading import get_prediction_from_hf, place_bracket_order

    now = datetime.now(NEW_YORK_TZ)
    market_open = is_market_open(now)
    summary = {
        "last_run_time": now.isoformat(),
        "users_scanned": 0,
        "trades_placed": 0,
        "skipped": 0,
        "errors": 0,
        "market_open": market_open,
    }

    if not market_open and not force:
        last_run_summary.update(summary)
        return summary

    users = get_users_with_alpaca_keys()
    summary["users_scanned"] = len(users)

    for user in users:
        trades_today = count_trades_today(user)
        user_id = serialize_mongo_user_id(user)

        if trades_today >= MAX_TRADES_PER_USER_PER_DAY:
            for ticker in TICKERS:
                log_trade_action(
                    user,
                    ticker,
                    None,
                    "skipped",
                    reason_skipped="daily max trades per user reached",
                )
                summary["skipped"] += 1
            continue

        for ticker in TICKERS:
            if trades_today >= MAX_TRADES_PER_USER_PER_DAY:
                break

            try:
                signal = get_prediction_from_hf(ticker, MODE)
                signal_ticker = str(signal.get("ticker") or ticker).upper()

                if not is_strong_signal(signal):
                    log_trade_action(
                        user,
                        signal_ticker,
                        signal,
                        "skipped",
                        reason_skipped="signal not strong enough or invalid price/ATR",
                    )
                    summary["skipped"] += 1
                    continue

                if has_open_order_or_position(user, signal_ticker):
                    log_trade_action(
                        user,
                        signal_ticker,
                        signal,
                        "skipped",
                        reason_skipped="open order or position already exists for ticker",
                    )
                    summary["skipped"] += 1
                    continue

                order = place_bracket_order(
                    ticker=signal_ticker,
                    decision=signal["decision"],
                    current_price=float(signal["current_price"]),
                    atr=float(signal["ATR"]),
                    api_key=user["api_key_public"],
                    api_secret=user["api_key_private"],
                )
                log_trade_action(
                    user,
                    signal_ticker,
                    signal,
                    "placed",
                    order_response=order,
                )
                trades_today += 1
                summary["trades_placed"] += 1

            except Exception as exc:
                log_trade_action(
                    user,
                    ticker,
                    None,
                    "error",
                    reason_skipped=f"user={user_id}: {str(exc)}",
                )
                summary["errors"] += 1

    last_run_summary.update(summary)
    return summary


def auto_trade_job() -> None:
    run_auto_trade_scan(force=False)


def start_scheduler() -> Dict[str, Any]:
    if not scheduler.get_job("auto_paper_trading"):
        scheduler.add_job(
            auto_trade_job,
            "interval",
            minutes=5,
            id="auto_paper_trading",
            replace_existing=True,
            max_instances=1,
            coalesce=True,
        )
    if not scheduler.running:
        scheduler.start()
    elif scheduler.state == 2:
        scheduler.resume()
    return get_scheduler_status()


def stop_scheduler() -> Dict[str, Any]:
    if scheduler.running:
        scheduler.pause()
    return get_scheduler_status()


def shutdown_scheduler() -> None:
    if scheduler.running:
        scheduler.shutdown(wait=False)


def get_scheduler_status() -> Dict[str, Any]:
    job = scheduler.get_job("auto_paper_trading")
    next_run_time = getattr(job, "next_run_time", None) if job else None
    return {
        "running": scheduler.running and scheduler.state == 1,
        "last_run_time": last_run_summary.get("last_run_time"),
        "next_run_time": next_run_time.isoformat() if next_run_time else None,
        "users_scanned_last_run": last_run_summary.get("users_scanned", 0),
        "trades_placed_last_run": last_run_summary.get("trades_placed", 0),
        "skipped_last_run": last_run_summary.get("skipped", 0),
        "errors_last_run": last_run_summary.get("errors", 0),
        "market_open_last_run": last_run_summary.get("market_open", False),
    }
