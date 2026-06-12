export const BACKEND_URL =
  process.env.NEXT_PUBLIC_BACKEND_URL || "http://127.0.0.1:8000";

export type PredictionMode = "daily" | "intraday";

export type PredictionSignal = {
  ticker: string;
  mode: string;
  ticker_id?: number;
  predicted_probability: number;
  current_price: number;
  RSI: number;
  EMA_20: number;
  EMA_50: number;
  ATR: number;
  decision: "BUY" | "SELL" | "HOLD" | string;
  [key: string]: unknown;
};

async function parseResponse(response: Response) {
  const contentType = response.headers.get("content-type") || "";
  const payload = contentType.includes("application/json")
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    const message =
      typeof payload === "string"
        ? payload
        : payload?.detail
          ? JSON.stringify(payload.detail)
          : "Request failed";
    throw new Error(message);
  }

  return payload;
}

async function postJson(path: string, body: unknown) {
  const response = await fetch(`${BACKEND_URL}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(body),
  });
  return parseResponse(response);
}

export function predictDaily(ticker: string): Promise<PredictionSignal> {
  return postJson("/trading/predict/daily", { ticker });
}

export function predictIntraday(ticker: string): Promise<PredictionSignal> {
  return postJson("/trading/predict/intraday", { ticker });
}

export function executeDaily(
  ticker: string,
  apiKey: string,
  apiSecret: string,
) {
  return postJson("/trading/execute/daily", {
    tickers: [ticker],
    api_key: apiKey,
    api_secret: apiSecret,
  });
}

export function executeIntraday(
  ticker: string,
  apiKey: string,
  apiSecret: string,
) {
  return postJson("/trading/execute/intraday", {
    tickers: [ticker],
    api_key: apiKey,
    api_secret: apiSecret,
  });
}

export async function login(email: string, password: string) {
  const body = new URLSearchParams();
  body.set("username", email);
  body.set("password", password);

  const response = await fetch(`${BACKEND_URL}/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/x-www-form-urlencoded",
    },
    body,
  });

  return parseResponse(response);
}

export function signup(
  name: string,
  email: string,
  password: string,
  apiKey: string,
  apiSecret: string,
) {
  return postJson("/user/", {
    username: name,
    email,
    password,
    api_key_public: apiKey,
    api_key_private: apiSecret,
    base_url: "paper",
  });
}

export const STOCK_TICKERS = [
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
];

