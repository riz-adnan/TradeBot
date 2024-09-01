"use client"

export default function NavButton({ task, text, type }: { task: Function, text: string, type: string }) {
    return (
        <button
            className={`relative inline-flex items-center justify-center p-0.5 mb-2 me-2 overflow-hidden text-sm font-medium text-gray-900 rounded-xl group bg-gradient-to-br from-pink-500 to-orange-400 ${type === text ? 'from-pink-500 to-orange-400 hover:text-white' : 'text-white'} dark:text-white hover:ring-2 hover:outline-none hover:ring-pink-200 dark:hover:ring-pink-800`}
            onClick={() => task()}
        >
            <span className={`relative w-[24rem] px-12 py-2.5 font-bold text-lg transition-all ease-in duration-75 bg-gray-900 rounded-lg ${type === text ? 'bg-opacity-0' : ''}`}>
                {text} Money
            </span>
        </button>
    )
}