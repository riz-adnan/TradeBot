from pathlib import Path
import pickle
from typing import Dict, List, Literal

from alpaca.trading.client import TradingClient
from alpaca.trading.enums import OrderClass, OrderSide, TimeInForce
from alpaca.trading.requests import (
    MarketOrderRequest,
    StopLossRequest,
    TakeProfitRequest,
)
from fastapi import APIRouter, HTTPException, status
import numpy as np
import pandas as pd
import pandas_ta as ta
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.callbacks import EarlyStopping, ModelCheckpoint
from tensorflow.keras.layers import (
    Attention,
    Concatenate,
    Dense,
    Dropout,
    Embedding,
    Flatten,
    GlobalAveragePooling1D,
    Input,
    LSTM,
)
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.optimizers import Adam
import yfinance as yf

from .. import schemas


router = APIRouter(prefix="/trading", tags=["trading"])

Mode = Literal["daily", "intraday"]

BASE_MODEL_DIR = Path("models")
FEATURE_COLUMNS = [
    "Close",
    "Volume",
    "RSI",
    "VWAP",
    "BBU",
    "BBM",
    "BBL",
    "MACD_12_26_9",
    "MACDh_12_26_9",
    "MACDs_12_26_9",
    "ATR",
    "EMA_20",
    "EMA_50",
    "returns",
    "volatility",
]


def normalize_ticker(ticker: str) -> str:
    ticker = ticker.strip().upper()
    if not ticker:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Ticker cannot be empty.",
        )
    return ticker


def shared_model_paths(mode: Mode) -> Dict[str, Path]:
    model_dir = BASE_MODEL_DIR / mode
    return {
        "model": model_dir / f"shared_{mode}.keras",
        "scaler": model_dir / f"shared_{mode}_scaler.pkl",
        "ticker_map": model_dir / "ticker_map.pkl",
    }


def flatten_yfinance_columns(df: pd.DataFrame) -> pd.DataFrame:
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df


def download_market_data(ticker: str, mode: Mode, for_training: bool) -> pd.DataFrame:
    if mode == "daily":
        period = "5y" if for_training else "1y"
        interval = "1d"
    else:
        period = "60d" if for_training else "10d"
        interval = "5m"

    df = yf.download(
        ticker,
        period=period,
        interval=interval,
        auto_adjust=False,
        progress=False,
    )
    df = flatten_yfinance_columns(df)
    if df.empty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No market data found for {ticker}.",
        )
    return df


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    required_columns = {"High", "Low", "Close", "Volume"}
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Missing required market columns: {sorted(missing_columns)}",
        )

    df["RSI"] = ta.rsi(df["Close"], length=14)
    df["VWAP"] = ta.vwap(df["High"], df["Low"], df["Close"], df["Volume"])

    bollinger_bands = ta.bbands(df["Close"], length=20, std=2.0)
    if bollinger_bands is not None:
        bb_cols = list(bollinger_bands.columns)

        lower_col = [c for c in bb_cols if c.startswith("BBL_")][0]
        middle_col = [c for c in bb_cols if c.startswith("BBM_")][0]
        upper_col = [c for c in bb_cols if c.startswith("BBU_")][0]

        df["BBL"] = bollinger_bands[lower_col]
        df["BBM"] = bollinger_bands[middle_col]
        df["BBU"] = bollinger_bands[upper_col]

    macd = ta.macd(df["Close"], fast=12, slow=26, signal=9)
    if macd is not None:
        df = df.join(macd)

    df["ATR"] = ta.atr(df["High"], df["Low"], df["Close"], length=14)
    df["EMA_20"] = ta.ema(df["Close"], length=20)
    df["EMA_50"] = ta.ema(df["Close"], length=50)
    df["returns"] = df["Close"].pct_change()
    df["volatility"] = df["returns"].rolling(window=20).std()

    return df.dropna()


def create_target(df: pd.DataFrame, horizon: int, threshold: float) -> pd.DataFrame:
    df = df.copy()
    future_return = df["Close"].shift(-horizon) / df["Close"] - 1
    df["target"] = (future_return > threshold).astype(int)
    return df.iloc[:-horizon].dropna()


def make_sequences(
    df: pd.DataFrame,
    sequence_length: int,
    scaler: MinMaxScaler,
    ticker_id: int | None = None,
):
    missing_features = [column for column in FEATURE_COLUMNS if column not in df.columns]
    if missing_features:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Missing feature columns: {missing_features}",
        )

    scaled_features = scaler.transform(df[FEATURE_COLUMNS])
    targets = df["target"].to_numpy()

    X: List[np.ndarray] = []
    y: List[int] = []
    ticker_ids: List[int] = []
    for index in range(sequence_length, len(scaled_features)):
        X.append(scaled_features[index - sequence_length:index])
        y.append(int(targets[index]))
        if ticker_id is not None:
            ticker_ids.append(ticker_id)

    if not X:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Not enough market data to create model sequences.",
        )

    if ticker_id is None:
        return np.asarray(X), np.asarray(y)
    return np.asarray(X), np.asarray(y), np.asarray(ticker_ids)


def build_advanced_lstm(input_shape, ticker_count: int) -> Model:
    feature_input = Input(shape=input_shape, name="features")
    ticker_input = Input(shape=(1,), name="ticker_id")

    x = LSTM(128, return_sequences=True)(feature_input)
    x = Dropout(0.3)(x)
    x = LSTM(64, return_sequences=True)(x)
    x = Dropout(0.3)(x)
    x = Attention()([x, x])
    x = GlobalAveragePooling1D()(x)

    embedding_dim = min(16, max(2, ticker_count))
    ticker_embedding = Embedding(
        input_dim=ticker_count,
        output_dim=embedding_dim,
        name="ticker_embedding",
    )(ticker_input)
    ticker_embedding = Flatten()(ticker_embedding)

    x = Concatenate()([x, ticker_embedding])
    x = Dense(64, activation="relu")(x)
    x = Dropout(0.3)(x)
    x = Dense(32, activation="relu")(x)
    outputs = Dense(1, activation="sigmoid")(x)

    model = Model(inputs=[feature_input, ticker_input], outputs=outputs)
    model.compile(
        optimizer=Adam(learning_rate=0.0005),
        loss="binary_crossentropy",
        metrics=["accuracy"],
    )
    return model


def mode_settings(mode: Mode) -> Dict[str, float | int]:
    if mode == "daily":
        return {"sequence_length": 60, "horizon": 1, "threshold": 0.002}
    return {"sequence_length": 48, "horizon": 3, "threshold": 0.0005}


def prepare_training_frame(ticker: str, mode: Mode) -> pd.DataFrame:
    settings = mode_settings(mode)
    df = download_market_data(ticker, mode, for_training=True)
    df = add_features(df)
    return create_target(
        df,
        horizon=int(settings["horizon"]),
        threshold=float(settings["threshold"]),
    )


def train_model_for_tickers(tickers: List[str], mode: Mode) -> Dict[str, str | int | Dict]:
    normalized_tickers = [normalize_ticker(ticker) for ticker in tickers]
    normalized_tickers = list(dict.fromkeys(normalized_tickers))
    if not normalized_tickers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one ticker is required.",
        )

    settings = mode_settings(mode)
    sequence_length = int(settings["sequence_length"])
    paths = shared_model_paths(mode)
    paths["model"].parent.mkdir(parents=True, exist_ok=True)

    ticker_map = {
        ticker: ticker_id
        for ticker_id, ticker in enumerate(normalized_tickers)
    }
    prepared_frames = {
        ticker: prepare_training_frame(ticker, mode)
        for ticker in normalized_tickers
    }
    if not prepared_frames:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="No training data could be prepared.",
        )

    scaler = MinMaxScaler()
    scaler.fit(
        pd.concat(
            [df[FEATURE_COLUMNS] for df in prepared_frames.values()],
            axis=0,
        )
    )

    X_parts = []
    y_parts = []
    ticker_id_parts = []
    samples_by_ticker = {}
    for ticker, df in prepared_frames.items():
        X, y, ticker_ids = make_sequences(
            df,
            sequence_length,
            scaler,
            ticker_map[ticker],
        )
        X_parts.append(X)
        y_parts.append(y)
        ticker_id_parts.append(ticker_ids)
        samples_by_ticker[ticker] = int(len(X))

    X_train = np.concatenate(X_parts, axis=0)
    y_train = np.concatenate(y_parts, axis=0)
    ticker_ids_train = np.concatenate(ticker_id_parts, axis=0).reshape(-1, 1)

    if len(np.unique(y_train)) < 2:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Training target has only one class. Try more tickers or more varied data.",
        )

    model = build_advanced_lstm(
        (X_train.shape[1], X_train.shape[2]),
        ticker_count=len(ticker_map),
    )
    callbacks = [
        EarlyStopping(
            monitor="val_loss",
            patience=8,
            restore_best_weights=True,
        ),
        ModelCheckpoint(
            filepath=str(paths["model"]),
            monitor="val_loss",
            save_best_only=True,
        ),
    ]
    history = model.fit(
        {"features": X_train, "ticker_id": ticker_ids_train},
        y_train,
        validation_split=0.2,
        epochs=50,
        batch_size=32,
        callbacks=callbacks,
        verbose=0,
        shuffle=False,
    )
    model.save(paths["model"])

    with paths["scaler"].open("wb") as scaler_file:
        pickle.dump(scaler, scaler_file)
    with paths["ticker_map"].open("wb") as ticker_map_file:
        pickle.dump(ticker_map, ticker_map_file)

    return {
        "mode": mode,
        "tickers": normalized_tickers,
        "samples": int(len(X_train)),
        "samples_by_ticker": samples_by_ticker,
        "model_path": str(paths["model"]),
        "scaler_path": str(paths["scaler"]),
        "ticker_map_path": str(paths["ticker_map"]),
        "epochs_trained": len(history.history.get("loss", [])),
    }


def load_saved_model_scaler_and_ticker_map(mode: Mode):
    paths = shared_model_paths(mode)
    if (
        not paths["model"].exists()
        or not paths["scaler"].exists()
        or not paths["ticker_map"].exists()
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Shared {mode} model not found. Please train it first.",
        )

    model = load_model(paths["model"])
    with paths["scaler"].open("rb") as scaler_file:
        scaler = pickle.load(scaler_file)
    with paths["ticker_map"].open("rb") as ticker_map_file:
        ticker_map = pickle.load(ticker_map_file)
    return model, scaler, ticker_map


def generate_trade_decision(signal: Dict[str, float]) -> str:
    probability = signal["predicted_probability"]
    current_price = signal["current_price"]
    rsi = signal["RSI"]
    ema_20 = signal["EMA_20"]
    ema_50 = signal["EMA_50"]

    if probability >= 0.65 and current_price > ema_20 > ema_50 and rsi < 70:
        return "BUY"
    if probability <= 0.35 and current_price < ema_20 < ema_50 and rsi > 30:
        return "SELL"
    return "HOLD"


def predict_for_ticker(ticker: str, mode: Mode) -> Dict[str, float | str]:
    ticker = normalize_ticker(ticker)
    settings = mode_settings(mode)
    sequence_length = int(settings["sequence_length"])
    model, scaler, ticker_map = load_saved_model_scaler_and_ticker_map(mode)
    if ticker not in ticker_map:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticker {ticker} was not included in the shared {mode} model. Please train it first.",
        )

    df = download_market_data(ticker, mode, for_training=False)
    df = add_features(df)
    if len(df) < sequence_length:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=f"Not enough latest data for {ticker}; need at least {sequence_length} candles.",
        )

    latest_features = df[FEATURE_COLUMNS].tail(sequence_length)
    scaled_features = scaler.transform(latest_features)
    X = np.expand_dims(scaled_features, axis=0)
    ticker_id = np.asarray([[ticker_map[ticker]]])
    probability = float(
        model.predict(
            {"features": X, "ticker_id": ticker_id},
            verbose=0,
        )[0][0]
    )
    latest = df.iloc[-1]

    signal = {
        "ticker": ticker,
        "mode": mode,
        "ticker_id": int(ticker_map[ticker]),
        "predicted_probability": probability,
        "current_price": float(latest["Close"]),
        "RSI": float(latest["RSI"]),
        "EMA_20": float(latest["EMA_20"]),
        "EMA_50": float(latest["EMA_50"]),
        "ATR": float(latest["ATR"]),
    }
    signal["decision"] = generate_trade_decision(signal)
    return signal


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


def train_for_tickers(tickers: List[str], mode: Mode) -> Dict[str, List[Dict]]:
    if not tickers:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one ticker is required.",
        )

    return {"mode": mode, "trained": train_model_for_tickers(tickers, mode)}


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
        signal = predict_for_ticker(ticker, mode)
        if signal["decision"] == "HOLD":
            results.append({**signal, "message": "HOLD: no order placed."})
            continue

        order = place_bracket_order(
            ticker=signal["ticker"],
            decision=signal["decision"],
            current_price=signal["current_price"],
            atr=signal["ATR"],
            api_key=api_key,
            api_secret=api_secret,
        )
        results.append({**signal, "order": order})
    return {"mode": mode, "results": results}


@router.post("/train/daily", status_code=status.HTTP_201_CREATED)
def train_daily(request: schemas.TrainRequest):
    return train_for_tickers(request.tickers, "daily")


@router.post("/train/intraday", status_code=status.HTTP_201_CREATED)
def train_intraday(request: schemas.TrainRequest):
    return train_for_tickers(request.tickers, "intraday")


@router.post("/predict/daily")
def predict_daily(request: schemas.PredictRequest):
    return predict_for_ticker(request.ticker, "daily")


@router.post("/predict/intraday")
def predict_intraday(request: schemas.PredictRequest):
    return predict_for_ticker(request.ticker, "intraday")


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
