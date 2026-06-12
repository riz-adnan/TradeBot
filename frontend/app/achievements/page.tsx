import {
  Eyebrow,
  PageShell,
  RoiGallery,
  Section,
  SiteFooter,
} from "@/components/finance-shell";

export const metadata = {
  title: "Achievements - AlphaQuant AI",
  description: "Hackathon achievements and ROI visuals for the ML trading system.",
};

const metrics = [
  "Hackathon Winner",
  "Daily + Intraday Models",
  "LSTM + Attention",
  "Paper Trading Ready",
  "Multi-stock Training",
];

export default function AchievementsPage() {
  return (
    <PageShell>
      <Section className="pt-32 sm:pt-36">
        <Eyebrow>1st Prize Winner — Blaze.ai ML Hackathon</Eyebrow>
        <div className="grid gap-8 lg:grid-cols-[0.95fr_1.05fr] lg:items-end">
          <div>
            <h1 className="text-4xl font-black text-white sm:text-5xl">Our Achievements</h1>
            <p className="mt-5 text-lg leading-8 text-slate-300">
              The project combines an LSTM + Attention architecture, multi-stock shared training,
              daily and intraday prediction, and Alpaca paper-trading execution into one research system.
            </p>
          </div>
          <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
            {metrics.map((metric) => (
              <div key={metric} className="rounded-lg border border-white/10 bg-white/[0.04] p-4">
                <p className="text-sm font-bold text-white">{metric}</p>
              </div>
            ))}
          </div>
        </div>
      </Section>

      <Section className="py-16">
        <div className="mb-8">
          <h2 className="text-3xl font-black text-white">ROI Gallery</h2>
          <p className="mt-3 max-w-3xl text-slate-400">
            Existing project visuals are preserved and presented as a responsive gallery for the model research story.
          </p>
        </div>
        <RoiGallery />
      </Section>

      <SiteFooter />
    </PageShell>
  );
}
