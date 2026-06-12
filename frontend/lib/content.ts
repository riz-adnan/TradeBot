export const portfolioUrl = "https://adnanrizvi.netlify.app";
export const githubUrl = "https://github.com/riz-adnan/TradeBot";

export const roiImages = [
  {
    src: "/images/test1.png",
    title: "ROI Snapshot I",
    caption: "Backtested signal performance from the ML trading workflow.",
  },
  {
    src: "/images/test2.png",
    title: "ROI Snapshot II",
    caption: "Model behavior under a separate ticker and market regime.",
  },
  {
    src: "/images/test3.png",
    title: "ROI Snapshot III",
    caption: "Paper-trading research output presented from the project archive.",
  },
  {
    src: "/images/test4.png",
    title: "ROI Snapshot IV",
    caption: "Additional return curve evidence from the existing project assets.",
  },
  {
    src: "/images/test5.png",
    title: "ROI Snapshot V",
    caption: "Validation visual retained from the original hackathon work.",
  },
];

export const architecturePoints = [
  "Shared model trained on multiple top US stock tickers",
  "LSTM layers for sequential market pattern learning",
  "Attention mechanism for focusing on important historical candles",
  "Ticker embedding to learn stock-specific behavior",
  "Technical indicators: RSI, EMA, ATR, MACD, Bollinger Bands, VWAP, returns, and volatility",
];

export const methodologyPoints = [
  "Data collected from historical OHLCV stock candles",
  "Feature engineering with technical indicators",
  "Separate daily and intraday models",
  "Daily model predicts next-day movement",
  "Intraday model predicts short-term 5-minute or 15-minute movement",
  "Backend returns decision, confidence, RSI, EMA, ATR, and current price",
];

