export const portfolioUrl = "https://adnanrizvi.netlify.app";
export const githubUrl = "https://github.com/riz-adnan/TradeBot";

export const roiImages = [
  {
    src: "/images/test1.png",
    title: "Adnan Rizvi Portfolio",
    caption: "12% growth from Dec 24 - March 25",
  },
  {
    src: "/images/test2.png",
    title: "Prakhar Moses Portfolio",
    caption: "10% growth from Dec 24 - March 25.",
  },
  {
    src: "/images/test3.png",
    title: "Nandhvardhan Portfolio",
    caption: "14% growth from Dec 24 - March 25",
  },
  {
    src: "/images/test4.png",
    title: "Vaibhav Mishra Portfolio",
    caption: "12% growth from Dec 24 - March 25",
  },
  {
    src: "/images/test5.png",
    title: "Adarsh Dwivedi Portfolio",
    caption: "11% growth from Dec 24 - March 25",
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
  "If registered under trade, backend automatically executes trade for the registered users"
];

