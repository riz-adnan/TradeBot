# 🚀 AI-Powered Algorithmic Trading Platform

## 🏆 1st Prize Winner — Blaze.ai ML Hackathon

An end-to-end AI-powered algorithmic trading platform that combines deep learning, quantitative finance, cloud deployment, and automated paper trading.

The platform leverages a multi-stock LSTM + Attention architecture trained on historical market data to generate trading signals for both daily and intraday trading. Predictions are served through a scalable model API and can be executed automatically using Alpaca Paper Trading.

---

# 📌 Overview

This project was built to explore whether modern sequence models can identify meaningful patterns in financial time series data and convert them into actionable trading signals.

The system consists of:

- Deep Learning Prediction Engine
- LSTM + Attention Architecture
- Multi-Stock Shared Training
- Hugging Face Model Serving
- FastAPI Trading Backend
- Alpaca Paper Trading Integration
- Automated Trade Scheduler
- Interactive Trading Dashboard
- MongoDB User & Trade Storage

The platform supports:

- Daily Predictions
- Intraday Predictions
- Paper Trade Execution
- Automated Strategy Execution
- Multi-User Trading Infrastructure

---



# 🏗 System Architecture

```text
                    Historical Market Data
                               │
                               ▼
                        Feature Engineering
                               │
                               ▼
                    LSTM + Attention Models
                               │
                               ▼
                    Hugging Face Model API
                               │
            ┌──────────────────┴──────────────────┐
            ▼                                     ▼
      Prediction API                     Trade Execution API
            │                                     │
            ▼                                     ▼
      Frontend Dashboard                Alpaca Paper Trading
            │                                     │
            └──────────────┬──────────────────────┘
                           ▼
                       MongoDB
```

---

# 🌐 Live Demo & Deployment

## Frontend Application

🔗 Live Website

https://free-trade-bot.netlify.app/

The frontend provides:

- Interactive prediction dashboard
- Paper trading interface
- Automated trading controls
- Portfolio management
- Trading analytics
- Project methodology and architecture
- Achievements showcase

---

## Model Inference Service

🤗 Hugging Face Space

https://huggingface.co/spaces/rizvizwizard/trading-model-api

The machine learning models are deployed separately on Hugging Face Spaces.

Responsibilities:

- Daily prediction inference
- Intraday prediction inference
- Feature processing
- Model serving
- Scalable API access

Available endpoints:

```http
POST /predict/daily
POST /predict/intraday
```

Example request:

```json
{
  "ticker": "AAPL"
}
```

Example response:

```json
{
  "ticker": "AAPL",
  "mode": "intraday",
  "ticker_id": 0,
  "predicted_probability": 0.81,
  "current_price": 291.5,
  "RSI": 27.4,
  "EMA_20": 292.5,
  "EMA_50": 292.4,
  "ATR": 0.63,
  "decision": "BUY"
}
```

---

## Backend Infrastructure

The backend is built using FastAPI and acts as the orchestration layer between:

- Frontend
- Hugging Face Models
- MongoDB
- Alpaca Paper Trading

Backend responsibilities:

- User authentication
- Alpaca key management
- Trade execution
- Automated trading scheduler
- Trade logging
- Portfolio management
- Risk management

---

## Deployment Architecture

```text
┌─────────────────────────────┐
│       React Frontend        │
│      (Netlify Hosting)      │
└──────────────┬──────────────┘
               │
               ▼
┌─────────────────────────────┐
│      FastAPI Backend        │
│         (Render)            │
└──────────────┬──────────────┘
               │
      ┌────────┴────────┐
      ▼                 ▼
┌─────────────┐   ┌─────────────┐
│ HuggingFace │   │  MongoDB    │
│   Models    │   │   Atlas     │
└─────────────┘   └─────────────┘
      │
      ▼
┌─────────────────────────────┐
│  Alpaca Paper Trading API   │
└─────────────────────────────┘
```

# 🧠 Machine Learning Methodology

## Problem Statement

Financial markets are sequential systems where future movement often depends on historical context.

Traditional machine learning models struggle to capture:

- Temporal dependencies
- Momentum shifts
- Trend reversals
- Volatility clustering

Therefore, a sequence-learning architecture was chosen.

---

# 📊 Data Collection

Market data is collected using:

- Yahoo Finance API
- Daily OHLCV Candles
- Intraday OHLCV Candles

Data includes:

- Open
- High
- Low
- Close
- Volume

---

# 🔬 Feature Engineering

Raw prices alone rarely provide enough predictive power.

The platform generates a rich set of technical indicators:

## Momentum Indicators

### RSI (Relative Strength Index)

Measures overbought and oversold conditions.

## Trend Indicators

### EMA 20

Short-term trend indicator.

### EMA 50

Medium-term trend indicator.

## Volatility Indicators

### ATR (Average True Range)

Measures market volatility.

### Rolling Volatility

Captures recent market instability.

## Volume Indicators

### VWAP

Volume Weighted Average Price.

Helps determine fair value zones.

## Mean Reversion Indicators

### Bollinger Bands

- Upper Band
- Middle Band
- Lower Band

Useful for identifying price extremes.

## MACD Components

- MACD
- MACD Signal
- MACD Histogram

Used to capture momentum shifts and trend strength.

---

# 🤖 Model Architecture

The project uses a shared multi-stock architecture.

Instead of training one model per stock, a single model learns patterns across multiple leading US equities.

## Training Universe

- AAPL
- MSFT
- NVDA
- AMZN
- GOOG
- META
- TSLA
- AVGO
- COST
- NFLX
- ADBE
- AMD
- PEP
- CSCO
- QCOM
- INTC
- PYPL
- TXN
- CMCSA
- TMUS

---

## Architecture

```text
Input Sequence
      │
      ▼
LSTM Layer (128 Units)
      │
      ▼
Dropout
      │
      ▼
LSTM Layer (64 Units)
      │
      ▼
Attention Layer
      │
      ▼
Global Pooling
      │
      ▼
Ticker Embedding
      │
      ▼
Concatenation
      │
      ▼
Dense Layers
      │
      ▼
Prediction Output
```

### Why LSTM?

LSTMs are designed to learn long-term dependencies in sequential data.

They help capture:

- Trends
- Cycles
- Market momentum
- Historical dependencies

### Why Attention?

Not every historical candle is equally important.

Attention allows the model to focus on:

- Significant reversals
- Volatility spikes
- Momentum breakouts
- Trend confirmation zones

instead of treating all historical data equally.

### Why Shared Multi-Stock Training?

Traditional trading systems often train:

```text
1 model → 1 stock
```

This creates:

- Poor generalization
- Limited training data
- Overfitting

Instead:

```text
20 stocks → 1 model
```

Benefits:

- More training data
- Better generalization
- Reduced overfitting
- Cross-market learning

---

# 📈 Prediction Modes

## Daily Model

Objective:

Predict next-day market direction.

Uses:

- 5 years of daily data
- Longer-term patterns
- Swing trading signals

## Intraday Model

Objective:

Predict short-term movement.

Uses:

- 5-minute candles
- Recent market structure
- Scalping and intraday opportunities

---

# ☁ Model Serving

Training occurs offline on Kaggle GPU infrastructure.

Models are exported and deployed to Hugging Face Spaces.

Benefits:

- Dedicated inference layer
- Faster backend deployment
- Smaller production footprint
- Independent model updates

Endpoints:

```http
POST /predict/daily
POST /predict/intraday
```

---

# ⚙ Trading Backend

The FastAPI backend is responsible for:

- User Management
- Authentication
- Alpaca Integration
- Trade Execution
- Auto Trading Scheduler
- Trade Logging

The backend does not perform inference.

Inference is delegated to the Hugging Face model API.

---

# 💰 Trade Execution Logic

The model returns:

```json
{
  "decision": "BUY",
  "predicted_probability": 0.82
}
```

Trading decisions are filtered through risk controls.

## BUY Conditions

- High confidence prediction
- Trend confirmation
- EMA alignment
- Acceptable volatility

## SELL Conditions

- Strong bearish signal
- Momentum weakness
- Trend breakdown

## HOLD Conditions

No trade executed.

---

# 🛡 Risk Management

Each trade uses bracket orders.

For BUY:

```text
Take Profit = Price + 2 × ATR
Stop Loss  = Price - ATR
```

For SELL:

```text
Take Profit = Price - 2 × ATR
Stop Loss  = Price + ATR
```

Risk-to-reward ratio:

```text
2 : 1
```

---

# 🤖 Automated Trading Engine

Every 5 minutes:

1. Load registered users
2. Fetch Alpaca paper credentials
3. Scan supported stocks
4. Request predictions
5. Apply confidence filters
6. Execute trades
7. Log all activity

Safety controls:

- Maximum trades per day
- One active position per ticker
- Paper trading only
- Confidence thresholds

---

# 🗄 Database

MongoDB stores:

## Users

- User Information
- Alpaca Credentials
- Authentication Data

## Trade Logs

- Prediction
- Signal
- Decision
- Execution Status
- Order Metadata
- Timestamp

---

# 🎨 Frontend

The frontend provides:

### Landing Page

Project overview and methodology.

### Prediction Dashboard

Generate predictions for:

- Daily Trading
- Intraday Trading

Displays:

- Confidence
- RSI
- EMA20
- EMA50
- ATR
- Current Price
- Decision

### Trade Dashboard

Paper trade execution using Alpaca.

### Achievements Page

Showcases:

- Hackathon Win
- Trading Results
- ROI Screenshots
- Project Highlights

---

# 🔒 Disclaimer

This project is intended solely for:

- Research
- Education
- Experimentation
- Paper Trading

It does not constitute financial advice.

Trading financial instruments involves substantial risk.

---

# 👨‍💻 Author

## Adnan Rizvi

Portfolio: https://adnanrizvi.netlify.app

IIT Tirupati

AI Engineer | Software Engineer | Quantitative ML Enthusiast

---

# 🏆 Achievement

🥇 1st Prize Winner — Blaze.ai ML Hackathon

Built and deployed an end-to-end AI trading platform integrating deep learning, cloud deployment, automated paper trading, and modern ML engineering practices.
