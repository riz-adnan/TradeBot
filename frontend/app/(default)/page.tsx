import Image from "next/image";
import { FiActivity, FiBarChart2, FiCpu, FiShield } from "react-icons/fi";

import {
  Eyebrow,
  PageShell,
  PrimaryLink,
  RoiGallery,
  SecondaryLink,
  Section,
  SiteFooter,
} from "@/components/finance-shell";
import {
  architecturePoints,
  methodologyPoints,
  portfolioUrl,
} from "@/lib/content";

export const metadata = {
  title: "TradeBot - ML Trading System",
  description: "LSTM Attention trading research system for daily and intraday market prediction.",
};

export default function Home() {
  return (
    <PageShell>
      <Section className="pt-32 sm:pt-36 lg:pt-40">
        <div className="grid items-center gap-12 lg:grid-cols-[1.08fr_0.92fr]">
          <div>
            <Eyebrow>1st Prize Winner — Blaze.ai ML Hackathon</Eyebrow>
            <h1 className="max-w-4xl text-4xl font-black leading-tight text-white sm:text-5xl lg:text-6xl">
              AlphaQuant: LSTM Attention trading intelligence for daily and high-frequency trading and signals
            </h1>
            <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-300">
              This project uses an LSTM + Attention based architecture to analyze market
              time-series data and generate prediction signals for daily and high-frequency trading.
            </p>
            <p className="mt-5 max-w-2xl rounded-lg border border-amber-300/30 bg-amber-400/10 p-4 text-sm leading-6 text-amber-100">
              This project is for educational and paper-trading purposes only. It is not financial advice.
            </p>
            <div className="mt-8 flex flex-col gap-3 sm:flex-row">
              <PrimaryLink href="/prediction">Try Prediction</PrimaryLink>
              <SecondaryLink href="/achievements">View Achievements</SecondaryLink>
              <SecondaryLink href="/trade">Paper Trade</SecondaryLink>
            </div>
            <a
              href={portfolioUrl}
              target="_blank"
              rel="noreferrer"
              className="mt-6 inline-flex text-sm font-semibold text-emerald-200 hover:text-emerald-100"
            >
              Portfolio: adnanrizvi.netlify.app
            </a>
          </div>

          <div className="relative">
            <div className="overflow-hidden rounded-lg border border-white/10 bg-slate-950/70 shadow-2xl shadow-black/40">
              <div className="border-b border-white/10 px-5 py-4">
                <p className="text-sm font-semibold text-slate-300">Live model signal preview</p>
              </div>
              <div className="grid gap-4 p-5">
                {[
                  ["AAPL", "BUY", "72.4%", "+ RSI 58.2"],
                  ["NVDA", "HOLD", "51.8%", "EMA compression"],
                  ["TSLA", "SELL", "31.5%", "ATR elevated"],
                ].map(([ticker, decision, confidence, note]) => (
                  <div key={ticker} className="grid grid-cols-[72px_1fr_auto] items-center gap-4 rounded-lg border border-white/10 bg-white/[0.04] p-4">
                    <span className="font-bold text-white">{ticker}</span>
                    <div>
                      <div className="h-2 rounded-full bg-slate-800">
                        <div
                          className={`h-2 rounded-full ${decision === "BUY" ? "bg-emerald-400" : decision === "SELL" ? "bg-rose-400" : "bg-amber-300"}`}
                          style={{ width: confidence }}
                        />
                      </div>
                      <p className="mt-2 text-xs text-slate-400">{note}</p>
                    </div>
                    <span className="rounded-full border border-white/10 px-3 py-1 text-xs font-bold text-slate-100">
                      {decision}
                    </span>
                  </div>
                ))}
              </div>
            </div>
            <div className="mt-5 grid grid-cols-3 gap-3 text-center">
              {[
                ["20", "Tickers"],
                ["2", "Model modes"],
                ["HF", "Deployed API"],
              ].map(([value, label]) => (
                <div key={label} className="rounded-lg border border-white/10 bg-white/[0.04] p-4">
                  <div className="text-2xl font-black text-white">{value}</div>
                  <div className="mt-1 text-xs text-slate-400">{label}</div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </Section>

      <Section className="py-20">
        <div className="grid gap-6 md:grid-cols-4">
          {[
            [FiCpu, "Shared model", "Multi-stock training with ticker embeddings."],
            [FiActivity, "Signal engine", "Decision, confidence, price, RSI, EMA, and ATR."],
            [FiBarChart2, "Dual horizon", "Daily next-day and intraday short-window prediction."],
            [FiShield, "Paper only", "Alpaca paper execution with ATR bracket risk controls."],
          ].map(([Icon, title, copy]) => (
            <div key={String(title)} className="rounded-lg border border-white/10 bg-white/[0.04] p-6">
              <Icon className="h-6 w-6 text-emerald-300" aria-hidden="true" />
              <h2 className="mt-5 text-lg font-bold text-white">{String(title)}</h2>
              <p className="mt-3 text-sm leading-6 text-slate-400">{String(copy)}</p>
            </div>
          ))}
        </div>
      </Section>

      <Section className="py-8">
        <div className="grid gap-10 lg:grid-cols-2">
          <div>
            <Eyebrow>Architecture</Eyebrow>
            <h2 className="text-3xl font-black text-white">A sequence model built for market context</h2>
            <div className="mt-8 grid gap-3">
              {architecturePoints.map((point) => (
                <div key={point} className="rounded-lg border border-white/10 bg-white/[0.04] p-4 text-sm leading-6 text-slate-300">
                  {point}
                </div>
              ))}
            </div>
          </div>
          <div>
            <Eyebrow>Methodology</Eyebrow>
            <h2 className="text-3xl font-black text-white">From OHLCV candles to deployable trade signals</h2>
            <div className="mt-8 grid gap-3">
              {methodologyPoints.map((point) => (
                <div key={point} className="rounded-lg border border-white/10 bg-white/[0.04] p-4 text-sm leading-6 text-slate-300">
                  {point}
                </div>
              ))}
            </div>
          </div>
        </div>
      </Section>

      <Section className="py-20">
        <div className="mb-8 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <Eyebrow>ROI Showcase</Eyebrow>
            <h2 className="text-3xl font-black text-white">Research visuals from the winning system</h2>
          </div>
          <SecondaryLink href="/achievements">Open gallery</SecondaryLink>
        </div>
        <RoiGallery compact />
      </Section>

      <Section className="pb-20">
        <div className="relative overflow-hidden rounded-lg border border-white/10 bg-white/[0.04] p-8 md:p-10">
          <div className="grid gap-8 lg:grid-cols-[1fr_340px] lg:items-center">
            <div>
              <h2 className="text-3xl font-black text-white">Ready to test the deployed model?</h2>
              <p className="mt-4 max-w-2xl text-slate-300">
                Query the Hugging Face model API for confidence, indicators, and a model-generated paper-trading decision.
              </p>
              <div className="mt-7 flex flex-col gap-3 sm:flex-row">
                <PrimaryLink href="/prediction">Run Prediction</PrimaryLink>
                <SecondaryLink href="/trade">Execute Paper Trade</SecondaryLink>
              </div>
            </div>
            <div className="relative aspect-[4/3] overflow-hidden rounded-lg border border-white/10 bg-slate-950">
              <Image
                src="/images/hero-image-01.jpg"
                alt="Trading dashboard visual"
                fill
                sizes="340px"
                className="object-cover opacity-80"
              />
            </div>
          </div>
        </div>
      </Section>

      <SiteFooter />
    </PageShell>
  )
}
