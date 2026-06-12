import Link from 'next/link'
import MobileMenu from './mobile-menu'
import Image from 'next/image'
import { usePathname } from 'next/navigation'

import { portfolioUrl } from '@/lib/content'

export default function Header() {
  const pathname = usePathname()

  function findActiveLink(path: string) {
    return pathname === path ? 'text-emerald-200 bg-white/10' : 'text-slate-300 hover:text-white hover:bg-white/5'
  }

  const navItems = [
    { href: '/', label: 'Home' },
    { href: '/prediction', label: 'Prediction' },
    { href: '/trade', label: 'Trade' },
    { href: '/achievements', label: 'Achievements' },
  ]

  return (
    <header className="fixed top-0 w-full z-30 border-b border-white/10 bg-[#05070d]/80 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-20">
          <div className="shrink-0 mr-4">
            <Link href="/" className="flex items-center gap-3" aria-label="Trading ML home">
              <Image
                src="/images/Logo.png"
                alt="Logo"
                width={44}
                height={44}
                className="h-11 w-11 rounded-lg object-cover"
              />
              <span className="hidden text-sm font-bold uppercase tracking-wide text-white sm:block">
                AlphaQuant
              </span>
            </Link>
          </div>

          <nav className="hidden md:flex md:grow">
            <ul className="flex grow justify-end flex-wrap items-center gap-2">
              {navItems.map((item) => (
                <li key={item.href}>
                  <Link
                    href={item.href}
                    className={`rounded-lg px-4 py-2 text-sm font-semibold transition ${findActiveLink(item.href)}`}
                  >
                    {item.label}
                  </Link>
                </li>
              ))}
              <li>
                <a
                  href="https://github.com/riz-adnan/TradeBot"
                  target="_blank"
                  rel="noreferrer"
                  className="rounded-lg border border-emerald-300/30 bg-emerald-400/10 px-4 py-2 text-sm font-semibold text-emerald-100 transition hover:bg-emerald-400/20"
                >
                  Documentation
                </a>
              </li>
            </ul>
          </nav>

          <MobileMenu />

        </div>
      </div>
    </header>
  )
}
