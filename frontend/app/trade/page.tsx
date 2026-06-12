"use client";

import { useEffect, useMemo, useState } from "react";
import type { FormEvent } from "react";
import { FiExternalLink, FiLoader, FiLogOut } from "react-icons/fi";

import {
  DecisionBadge,
  Eyebrow,
  PageShell,
  Section,
  SiteFooter,
} from "@/components/finance-shell";
import {
  PredictionMode,
  STOCK_TICKERS,
  executeDaily,
  executeIntraday,
  login,
  signup,
} from "@/lib/api";

type StoredUser = {
  name?: string;
  email: string;
};

const storageKeys = {
  user: "trading_user",
  apiKey: "alpaca_api_key",
  apiSecret: "alpaca_api_secret",
  token: "auth_token",
};

function maskSecret(secret: string) {
  if (!secret) return "Not saved";
  return "************";
}

function Field({
  label,
  type = "text",
  value,
  onChange,
  placeholder,
}: {
  label: string;
  type?: string;
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
}) {
  return (
    <label className="block">
      <span className="text-sm font-semibold text-slate-300">{label}</span>
      <input
        type={type}
        value={value}
        onChange={(event) => onChange(event.target.value)}
        placeholder={placeholder}
        className="mt-2 w-full rounded-lg border-white/10 bg-slate-950 text-white placeholder:text-slate-600 focus:border-emerald-300 focus:ring-emerald-300"
      />
    </label>
  );
}

export default function TradePage() {
  const [activeTab, setActiveTab] = useState<"login" | "signup">("login");
  const [user, setUser] = useState<StoredUser | null>(null);
  const [apiKey, setApiKey] = useState("");
  const [apiSecret, setApiSecret] = useState("");
  const [ticker, setTicker] = useState("AAPL");
  const [mode, setMode] = useState<PredictionMode>("daily");
  const [authLoading, setAuthLoading] = useState(false);
  const [tradeLoading, setTradeLoading] = useState(false);
  const [error, setError] = useState("");
  const [tradeResponse, setTradeResponse] = useState<any>(null);

  const [loginEmail, setLoginEmail] = useState("");
  const [loginPassword, setLoginPassword] = useState("");
  const [signupName, setSignupName] = useState("");
  const [signupEmail, setSignupEmail] = useState("");
  const [signupPassword, setSignupPassword] = useState("");
  const [signupApiKey, setSignupApiKey] = useState("");
  const [signupApiSecret, setSignupApiSecret] = useState("");

  useEffect(() => {
    const storedUser = localStorage.getItem(storageKeys.user);
    const storedApiKey = localStorage.getItem(storageKeys.apiKey);
    const storedApiSecret = localStorage.getItem(storageKeys.apiSecret);

    if (storedUser) setUser(JSON.parse(storedUser));
    if (storedApiKey) setApiKey(storedApiKey);
    if (storedApiSecret) setApiSecret(storedApiSecret);
  }, []);

  const hasKeys = Boolean(apiKey && apiSecret);
  const primaryResult = useMemo(() => {
    const first = tradeResponse?.results?.[0];
    return first || null;
  }, [tradeResponse]);

  async function handleLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setAuthLoading(true);
    setError("");

    try {
      const data = await login(loginEmail, loginPassword);
      const nextUser = { email: loginEmail };
      localStorage.setItem(storageKeys.user, JSON.stringify(nextUser));
      if (data?.access_token) localStorage.setItem(storageKeys.token, data.access_token);
      setUser(nextUser);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed.");
    } finally {
      setAuthLoading(false);
    }
  }

  async function handleSignup(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setAuthLoading(true);
    setError("");

    try {
      await signup(signupName, signupEmail, signupPassword, signupApiKey, signupApiSecret);
      const nextUser = { name: signupName, email: signupEmail };
      localStorage.setItem(storageKeys.user, JSON.stringify(nextUser));
      localStorage.setItem(storageKeys.apiKey, signupApiKey);
      localStorage.setItem(storageKeys.apiSecret, signupApiSecret);
      setUser(nextUser);
      setApiKey(signupApiKey);
      setApiSecret(signupApiSecret);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Signup failed.");
    } finally {
      setAuthLoading(false);
    }
  }

  function saveKeys() {
    localStorage.setItem(storageKeys.apiKey, apiKey);
    localStorage.setItem(storageKeys.apiSecret, apiSecret);
    setError("");
  }

  function logout() {
    localStorage.removeItem(storageKeys.user);
    localStorage.removeItem(storageKeys.apiKey);
    localStorage.removeItem(storageKeys.apiSecret);
    localStorage.removeItem(storageKeys.token);
    setUser(null);
    setApiKey("");
    setApiSecret("");
    setTradeResponse(null);
  }

  async function executeTrade() {
    setTradeLoading(true);
    setError("");
    setTradeResponse(null);

    try {
      const response =
        mode === "daily"
          ? await executeDaily(ticker, apiKey, apiSecret)
          : await executeIntraday(ticker, apiKey, apiSecret);
      setTradeResponse(response);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Trade execution failed.");
    } finally {
      setTradeLoading(false);
    }
  }

  return (
    <PageShell>
      <Section className="pt-32 sm:pt-36">
        <Eyebrow>Alpaca Paper Trading Only</Eyebrow>
        <div className="grid gap-10 lg:grid-cols-[0.9fr_1.1fr]">
          <div>
            <h1 className="text-4xl font-black text-white sm:text-5xl">Paper Trading Console</h1>
            <p className="mt-5 text-lg leading-8 text-slate-300">
              Only Alpaca paper trading is supported. We do not support real-money trading in this demo.
            </p>
            <div className="mt-5 rounded-lg border border-amber-300/30 bg-amber-400/10 p-4 text-sm leading-6 text-amber-100">
              Use paper trading only. Do not use this as financial advice.
            </div>
            <a
              href="https://alpaca.markets/docs/"
              target="_blank"
              rel="noreferrer"
              className="mt-6 inline-flex items-center gap-2 rounded-lg border border-emerald-300/30 bg-emerald-400/10 px-5 py-3 text-sm font-bold text-emerald-100 hover:bg-emerald-400/20"
            >
              How to get Alpaca API keys
              <FiExternalLink aria-hidden="true" />
            </a>
          </div>

          <div className="rounded-lg border border-white/10 bg-white/[0.04] p-5">
            {user ? (
              <div>
                <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                  <div>
                    <p className="text-sm text-slate-400">Signed in as</p>
                    <p className="mt-1 font-bold text-white">{user.name || user.email}</p>
                  </div>
                  <button
                    type="button"
                    onClick={logout}
                    className="inline-flex items-center justify-center gap-2 rounded-lg border border-white/10 px-4 py-2 text-sm font-semibold text-slate-200 hover:bg-white/10"
                  >
                    <FiLogOut aria-hidden="true" />
                    Logout
                  </button>
                </div>

                {hasKeys ? (
                  <div className="mt-5 rounded-lg border border-emerald-300/20 bg-emerald-400/10 p-4 text-sm text-emerald-100">
                    You are already part of our paper trading system.
                  </div>
                ) : (
                  <div className="mt-5 rounded-lg border border-white/10 bg-slate-950/60 p-4">
                    <p className="text-sm text-slate-300">
                      Portfolio sync will appear here after backend portfolio endpoint is connected.
                      Add your Alpaca paper keys locally to enable execution.
                    </p>
                  </div>
                )}

                <div className="mt-5 grid gap-4 sm:grid-cols-2">
                  <Field label="Alpaca API Key" value={apiKey} onChange={setApiKey} />
                  <Field
                    label="Alpaca API Secret"
                    type="password"
                    value={apiSecret}
                    onChange={setApiSecret}
                  />
                </div>
                <p className="mt-3 text-xs text-slate-500">Saved secret preview: {maskSecret(apiSecret)}</p>
                <button
                  type="button"
                  onClick={saveKeys}
                  className="mt-4 rounded-lg border border-white/10 px-4 py-2 text-sm font-semibold text-slate-200 hover:bg-white/10"
                >
                  Save paper keys locally
                </button>
              </div>
            ) : (
              <div>
                <div className="grid grid-cols-2 rounded-lg border border-white/10 bg-slate-950/60 p-1">
                  {(["login", "signup"] as const).map((tab) => (
                    <button
                      key={tab}
                      type="button"
                      onClick={() => setActiveTab(tab)}
                      className={`rounded-md px-4 py-2 text-sm font-bold capitalize transition ${
                        activeTab === tab
                          ? "bg-emerald-400 text-slate-950"
                          : "text-slate-300 hover:bg-white/10"
                      }`}
                    >
                      {tab}
                    </button>
                  ))}
                </div>

                {activeTab === "login" ? (
                  <form onSubmit={handleLogin} className="mt-5 grid gap-4">
                    <Field label="Email" type="email" value={loginEmail} onChange={setLoginEmail} />
                    <Field label="Password" type="password" value={loginPassword} onChange={setLoginPassword} />
                    <button
                      type="submit"
                      disabled={authLoading}
                      className="inline-flex items-center justify-center gap-2 rounded-lg bg-emerald-400 px-5 py-3 text-sm font-bold text-slate-950 hover:bg-emerald-300 disabled:opacity-60"
                    >
                      {authLoading && <FiLoader className="animate-spin" aria-hidden="true" />}
                      Login
                    </button>
                  </form>
                ) : (
                  <form onSubmit={handleSignup} className="mt-5 grid gap-4">
                    <Field label="Name" value={signupName} onChange={setSignupName} />
                    <Field label="Email / ID" type="email" value={signupEmail} onChange={setSignupEmail} />
                    <Field label="Password" type="password" value={signupPassword} onChange={setSignupPassword} />
                    <Field label="Alpaca API Key" value={signupApiKey} onChange={setSignupApiKey} />
                    <Field
                      label="Alpaca API Secret"
                      type="password"
                      value={signupApiSecret}
                      onChange={setSignupApiSecret}
                    />
                    <button
                      type="submit"
                      disabled={authLoading}
                      className="inline-flex items-center justify-center gap-2 rounded-lg bg-emerald-400 px-5 py-3 text-sm font-bold text-slate-950 hover:bg-emerald-300 disabled:opacity-60"
                    >
                      {authLoading && <FiLoader className="animate-spin" aria-hidden="true" />}
                      Signup
                    </button>
                  </form>
                )}
              </div>
            )}

            {error && (
              <div className="mt-5 rounded-lg border border-rose-300/30 bg-rose-400/10 p-4 text-sm text-rose-100">
                {error}
              </div>
            )}
          </div>
        </div>
      </Section>

      {user && hasKeys && (
        <Section className="py-12">
          <div className="rounded-lg border border-white/10 bg-white/[0.04] p-5 md:p-7">
            <div className="grid gap-4 md:grid-cols-[1fr_1fr_auto] md:items-end">
              <label className="block">
                <span className="text-sm font-semibold text-slate-300">Ticker</span>
                <select
                  value={ticker}
                  onChange={(event) => setTicker(event.target.value)}
                  className="mt-2 w-full rounded-lg border-white/10 bg-slate-950 text-white focus:border-emerald-300 focus:ring-emerald-300"
                >
                  {STOCK_TICKERS.map((symbol) => (
                    <option key={symbol} value={symbol}>
                      {symbol}
                    </option>
                  ))}
                </select>
              </label>
              <label className="block">
                <span className="text-sm font-semibold text-slate-300">Mode</span>
                <select
                  value={mode}
                  onChange={(event) => setMode(event.target.value as PredictionMode)}
                  className="mt-2 w-full rounded-lg border-white/10 bg-slate-950 text-white focus:border-emerald-300 focus:ring-emerald-300"
                >
                  <option value="daily">Daily</option>
                  <option value="intraday">Intraday</option>
                </select>
              </label>
              <button
                type="button"
                onClick={executeTrade}
                disabled={tradeLoading}
                className="inline-flex h-[42px] items-center justify-center gap-2 rounded-lg bg-emerald-400 px-5 text-sm font-bold text-slate-950 hover:bg-emerald-300 disabled:opacity-60"
              >
                {tradeLoading && <FiLoader className="animate-spin" aria-hidden="true" />}
                Execute Paper Trade
              </button>
            </div>

            <div className="mt-8 rounded-lg border border-white/10 bg-slate-950/60 p-5">
              <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <p className="text-sm text-slate-400">Execution response</p>
                  <h2 className="mt-2 text-2xl font-black text-white">
                    {primaryResult ? `${primaryResult.ticker} ${primaryResult.mode}` : "No paper trade submitted yet"}
                  </h2>
                </div>
                <DecisionBadge decision={primaryResult?.decision} />
              </div>

              {primaryResult && (
                <div className="mt-6 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
                  {[
                    ["Confidence", `${(Number(primaryResult.predicted_probability) * 100).toFixed(1)}%`],
                    ["Current Price", `$${Number(primaryResult.current_price).toFixed(2)}`],
                    ["ATR", Number(primaryResult.ATR).toFixed(2)],
                    ["Order Status", primaryResult.message ? "No order placed" : "Order submitted"],
                  ].map(([label, value]) => (
                    <div key={label} className="rounded-lg border border-white/10 bg-white/[0.04] p-4">
                      <p className="text-sm text-slate-400">{label}</p>
                      <p className="mt-2 text-lg font-bold text-white">{value}</p>
                    </div>
                  ))}
                </div>
              )}

              {tradeResponse && (
                <pre className="mt-6 max-h-80 overflow-auto rounded-lg border border-white/10 bg-black/50 p-4 text-xs leading-5 text-slate-300">
                  {JSON.stringify(tradeResponse, null, 2)}
                </pre>
              )}
            </div>
          </div>
        </Section>
      )}

      <SiteFooter />
    </PageShell>
  );
}
