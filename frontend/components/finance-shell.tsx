import Image from "next/image";
import Link from "next/link";
import type { ReactNode } from "react";
import { FiArrowUpRight } from "react-icons/fi";

import { githubUrl, portfolioUrl, roiImages } from "@/lib/content";

export function PageShell({ children }: { children: ReactNode }) {
  return (
    <main className="min-h-screen bg-[#05070d] text-slate-100">
      <div className="fixed inset-0 -z-10 bg-[linear-gradient(135deg,#05070d_0%,#0b1f2a_38%,#111827_64%,#05070d_100%)]" />
      {children}
    </main>
  );
}

export function Section({
  children,
  className = "",
}: {
  children: ReactNode;
  className?: string;
}) {
  return (
    <section className={`mx-auto w-full max-w-7xl px-4 sm:px-6 lg:px-8 ${className}`}>
      {children}
    </section>
  );
}

export function Eyebrow({ children }: { children: ReactNode }) {
  return (
    <p className="mb-4 inline-flex rounded-full border border-emerald-400/30 bg-emerald-400/10 px-4 py-2 text-xs font-semibold uppercase tracking-wide text-emerald-200">
      {children}
    </p>
  );
}

export function PrimaryLink({
  href,
  children,
}: {
  href: string;
  children: ReactNode;
}) {
  return (
    <Link
      href={href}
      className="inline-flex items-center justify-center gap-2 rounded-lg bg-emerald-400 px-5 py-3 text-sm font-bold text-slate-950 shadow-lg shadow-emerald-500/20 transition hover:bg-emerald-300"
    >
      {children}
      <FiArrowUpRight aria-hidden="true" />
    </Link>
  );
}

export function SecondaryLink({
  href,
  children,
}: {
  href: string;
  children: ReactNode;
}) {
  return (
    <Link
      href={href}
      className="inline-flex items-center justify-center rounded-lg border border-white/15 bg-white/5 px-5 py-3 text-sm font-semibold text-white transition hover:border-emerald-300/50 hover:bg-white/10"
    >
      {children}
    </Link>
  );
}

export function DecisionBadge({ decision }: { decision?: string }) {
  const value = decision || "WAITING";
  const color =
    value === "BUY"
      ? "border-emerald-300/40 bg-emerald-400/15 text-emerald-200"
      : value === "SELL"
        ? "border-rose-300/40 bg-rose-400/15 text-rose-200"
        : value === "HOLD"
          ? "border-amber-300/40 bg-amber-400/15 text-amber-100"
          : "border-slate-300/30 bg-slate-400/10 text-slate-200";

  return (
    <span className={`inline-flex rounded-full border px-4 py-2 text-sm font-bold ${color}`}>
      {value}
    </span>
  );
}

export function RoiGallery({ compact = false }: { compact?: boolean }) {
  const images = compact ? roiImages.slice(0, 3) : roiImages;

  return (
    <div className="grid gap-5 md:grid-cols-2 lg:grid-cols-3">
      {images.map((image) => (
        <figure
          key={image.src}
          className="group overflow-hidden rounded-lg border border-white/10 bg-white/[0.04] shadow-2xl shadow-black/30 transition hover:-translate-y-1 hover:border-emerald-300/40"
        >
          <div className="relative aspect-[16/10] overflow-hidden bg-slate-950">
            <Image
              src={image.src}
              alt={image.title}
              fill
              sizes="(min-width: 1024px) 33vw, (min-width: 768px) 50vw, 100vw"
              className="object-cover transition duration-500 group-hover:scale-105"
            />
          </div>
          <figcaption className="p-5">
            <h3 className="text-base font-semibold text-white">{image.title}</h3>
            <p className="mt-2 text-sm leading-6 text-slate-400">{image.caption}</p>
          </figcaption>
        </figure>
      ))}
    </div>
  );
}

export function SiteFooter() {
  return (
    <footer className="border-t border-white/10 py-10">
      <Section className="flex flex-col gap-4 text-sm text-slate-400 md:flex-row md:items-center md:justify-between">
        <p>Built by Adnan Rizvi</p>
        <div className="flex flex-wrap gap-4">
          <a className="hover:text-emerald-200" href={portfolioUrl} target="_blank" rel="noreferrer">
            Portfolio
          </a>
          <a className="hover:text-emerald-200" href="https://github.com/riz-adnan" target="_blank" rel="noreferrer">
            GitHub
          </a>
        </div>
      </Section>
    </footer>
  );
}
