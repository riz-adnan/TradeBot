'use client'

import { useState, useRef, useEffect } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'

import { portfolioUrl } from '@/lib/content'

export default function MobileMenu() {
  const pathname = usePathname()

  const [mobileNavOpen, setMobileNavOpen] = useState<boolean>(false)

  const trigger = useRef<HTMLButtonElement>(null)
  const mobileNav = useRef<HTMLDivElement>(null)

  // close the mobile menu on click outside
  useEffect(() => {
    const clickHandler = ({ target }: { target: EventTarget | null }): void => {
      if (!mobileNav.current || !trigger.current) return;
      if (!mobileNavOpen || mobileNav.current.contains(target as Node) || trigger.current.contains(target as Node)) return;
      setMobileNavOpen(false)
    };
    document.addEventListener('click', clickHandler)
    return () => document.removeEventListener('click', clickHandler)
  })

  // close the mobile menu if the esc key is pressed
  useEffect(() => {
    const keyHandler = ({ keyCode }: { keyCode: number }): void => {
      if (!mobileNavOpen || keyCode !== 27) return;
      setMobileNavOpen(false)
    };
    document.addEventListener('keydown', keyHandler)
    return () => document.removeEventListener('keydown', keyHandler)
  })

  // To show the current active link
  function findActiveLink(path: string) {
    return pathname === path ? 'text-emerald-200 bg-white/10' : 'text-slate-300'
  }

  const navItems = [
    { href: '/', label: 'Home' },
    { href: '/prediction', label: 'Prediction' },
    { href: '/trade', label: 'Trade' },
    { href: '/achievements', label: 'Achievements' },
  ]

  return (
    <div className="md:hidden">
      {/* Hamburger button */}
      <button
        ref={trigger}
        className={`hamburger ${mobileNavOpen && 'active'}`}
        aria-controls="mobile-nav"
        aria-expanded={mobileNavOpen}
        onClick={() => setMobileNavOpen(!mobileNavOpen)}
      >
        <span className="sr-only">Menu</span>
        <svg
          className="w-6 h-6 fill-current text-gray-300 hover:text-gray-200 transition duration-150 ease-in-out"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
        >
          <rect y="4" width="24" height="2" rx="1" />
          <rect y="11" width="24" height="2" rx="1" />
          <rect y="18" width="24" height="2" rx="1" />
        </svg>
      </button>

      {/*Mobile navigation */}
      <nav
        id="mobile-nav"
        ref={mobileNav}
        className="absolute top-full z-20 left-0 w-full px-4 sm:px-6 overflow-hidden transition-all duration-300 ease-in-out"
        style={mobileNavOpen ? { maxHeight: mobileNav.current?.scrollHeight, opacity: 1 } : { maxHeight: 0, opacity: 0.8 }}
      >
        <ul className="rounded-b-2xl border border-white/10 bg-slate-950/95 px-4 py-3 shadow-2xl shadow-black/40">
          {navItems.map((item) => (
            <li key={item.href}>
              <Link
                href={item.href}
                className={`my-1 flex rounded-lg px-4 py-3 text-sm font-semibold transition hover:bg-white/5 hover:text-white ${findActiveLink(item.href)}`}
                onClick={() => setMobileNavOpen(false)}
              >
                {item.label}
              </Link>
            </li>
          ))}
          <li>
            <a
              href={portfolioUrl}
              target="_blank"
              rel="noreferrer"
              className="my-1 flex rounded-lg px-4 py-3 text-sm font-semibold text-emerald-100 transition hover:bg-emerald-400/10"
              onClick={() => setMobileNavOpen(false)}
            >
              Portfolio
            </a>
          </li>
        </ul>
      </nav>
    </div>
  )
}
