import Link from 'next/link'
import MobileMenu from './mobile-menu'
import Image from 'next/image'
import { usePathname } from 'next/navigation'

// Importting Context
import { useAccount } from '@/context/AccountContext'

export default function Header() {
  const pathname = usePathname()
  const { accountId, logout } = useAccount()

  function findActiveLink(path: string) {
    return pathname === path ? 'text-yellow-400' : 'text-purple-600'
  }

  return (
    <header className="absolute w-full z-30">
      <div className="max-w-6xl mx-auto px-4 sm:px-6">
        <div className="flex items-center justify-between h-20">
          {/* Site branding */}
          <div className="shrink-0 mr-4">
            {/* Logo */}
            <Link href="/" className="block" aria-label="Cruip">
              <Image
                src="/images/logo.png"
                alt="Logo"
                width={128}
                height={20}
                className='rounded-xl h-14'
              />
            </Link>
          </div>

          {/* Desktop navigation */}
          <nav className="hidden md:flex md:grow">
            {/* Desktop sign in links */}
            <ul className="flex grow justify-end flex-wrap items-center">
              <li>
                <Link
                  href="/"
                  className={`font-medium hover:text-gray-200 px-4 py-3 flex items-center transition duration-150 ease-in-out ${findActiveLink('/')}`}
                >
                  Home
                </Link>
              </li>
              <li>
                <Link
                  href="/wallet"
                  className={`font-medium hover:text-gray-200 px-4 py-3 flex items-center transition duration-150 ease-in-out ${findActiveLink('/wallet')}`}
                >
                  Wallet
                </Link>
              </li>
              <li>
                <Link
                  href="/trade"
                  className={`font-medium hover:text-gray-200 px-4 py-3 flex items-center transition duration-150 ease-in-out ${findActiveLink('/trade')}`}
                >
                  Trade
                </Link>
              </li>
              <li>
                <Link
                  href="/ourPrediction"
                  className={`font-medium hover:text-gray-200 px-4 py-3 flex items-center transition duration-150 ease-in-out ${findActiveLink('/ourPrediction')}`}
                >
                  Our Predictions
                </Link>
              </li>
              {accountId && accountId !== '' ? (<>
                
                <li>
                  <button
                    onClick={logout}
                    className="font-medium hover:text-gray-200 px-4 py-3 flex items-center transition duration-150 ease-in-out text-yellow-400"
                  >Log Out</button>
                </li>
              </>) : (
              <><li>
                <Link
                  href="/signin"
                  className="font-medium hover:text-gray-200 px-4 py-3 flex items-center transition duration-150 ease-in-out text-yellow-400"
                >
                  Sign in
                </Link>
              </li>
                
              </>)}
            </ul>
          </nav>

          <MobileMenu />

        </div>
      </div>
    </header>
  )
}
