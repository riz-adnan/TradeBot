"use client";

// export const metadata = {
//     title: 'Sign Up - Open PRO',
//     description: 'Page description',
// }

import Link from 'next/link'
import Image from 'next/image'
import { useState } from 'react'

// Import context
import { useAccount } from '@/context/AccountContext';

export default function SignUp() {
    const { signup } = useAccount()

    // Define states
    const [name, setName] = useState('')
    const [email, setEmail] = useState('')
    const [privateApi, setPrivateApi] = useState('')
    const [publicApi, setPublicApi] = useState('')
    const [baseUrl, setBaseUrl] = useState('')
    const [password, setPassword] = useState('')
    const [confirmPassword, setConfirmPassword] = useState('')

    // Define Functions
    const handleSignup = async (e: any) => {
        e.preventDefault()
        signup(name, email, password, privateApi, publicApi, baseUrl, confirmPassword)
    }

    return (
        <main className="min-h-screen flex items-stretch text-white ">
            <div className="lg:flex w-1/2 hidden bg-gray-500 bg-no-repeat bg-cover relative items-center" style={{ backgroundImage: "url(https://images.unsplash.com/photo-1577495508048-b635879837f1?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=675&q=80)" }}>
                <div className="absolute bg-black opacity-60 inset-0 z-0"></div>
                <div className="w-full px-24 z-10">
                    <h1 className="text-5xl font-bold text-left tracking-wide">Keep it special</h1>
                    <p className="text-3xl my-4">Your money has worth beyond your imagination!</p>
                </div>
                <div className="bottom-0 absolute p-4 text-center right-0 left-0 flex justify-center space-x-4">
                    <Link href='https://x.com/shnprakh' className='cursor-pointer transform transition-transform duration-2000 ease-in-out hover:scale-150'>
                        <svg fill="#fff" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z" /></svg>
                    </Link>
                    <Link href='' className='cursor-pointer transform transition-transform duration-2000 ease-in-out hover:scale-150'>
                        <svg fill="#fff" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M9 8h-3v4h3v12h5v-12h3.642l.358-4h-4v-1.667c0-.955.192-1.333 1.115-1.333h2.885v-5h-3.808c-3.596 0-5.192 1.583-5.192 4.615v3.385z" /></svg>
                    </Link>
                    <Link href='https://www.linkedin.com/in/prakhar-moses-a5173a264/' className='cursor-pointer transform transition-transform duration-2000 ease-in-out hover:scale-150'>
                        <svg fill="#ffffff" height="24" width="24" version="1.1" id="Layer_1" xmlns="http://www.w3.org/2000/svg" xmlnsXlink="http://www.w3.org/1999/xlink" viewBox="0 0 310 310" xmlSpace="preserve" stroke="#ffffff">
                            <g id="SVGRepo_bgCarrier" strokeWidth="0" />
                            <g id="SVGRepo_tracerCarrier" strokeLinecap="round" strokeLinejoin="round" />
                            <g id="SVGRepo_iconCarrier"> <g id="XMLID_801_"> <path id="XMLID_802_" d="M72.16,99.73H9.927c-2.762,0-5,2.239-5,5v199.928c0,2.762,2.238,5,5,5H72.16c2.762,0,5-2.238,5-5V104.73 C77.16,101.969,74.922,99.73,72.16,99.73z" /> <path id="XMLID_803_" d="M41.066,0.341C18.422,0.341,0,18.743,0,41.362C0,63.991,18.422,82.4,41.066,82.4 c22.626,0,41.033-18.41,41.033-41.038C82.1,18.743,63.692,0.341,41.066,0.341z" /> <path id="XMLID_804_" d="M230.454,94.761c-24.995,0-43.472,10.745-54.679,22.954V104.73c0-2.761-2.238-5-5-5h-59.599 c-2.762,0-5,2.239-5,5v199.928c0,2.762,2.238,5,5,5h62.097c2.762,0,5-2.238,5-5v-98.918c0-33.333,9.054-46.319,32.29-46.319 c25.306,0,27.317,20.818,27.317,48.034v97.204c0,2.762,2.238,5,5,5H305c2.762,0,5-2.238,5-5V194.995 C310,145.43,300.549,94.761,230.454,94.761z" /> </g> </g>
                        </svg>
                    </Link>
                </div>
            </div>
            <div className="lg:w-1/2 w-full flex items-center justify-center text-center md:px-16 px-0 z-0 bg-[#161616]">
                <div className="absolute lg:hidden z-10 inset-0 bg-gray-500 bg-no-repeat bg-cover items-center" style={{ backgroundImage: "url(https://images.unsplash.com/photo-1577495508048-b635879837f1?ixid=MXwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHw%3D&ixlib=rb-1.2.1&auto=format&fit=crop&w=675&q=80)" }}>
                    <div className="absolute bg-black opacity-60 inset-0 z-0"></div>
                </div>
                <div className="w-full py-6 z-20">
                    <h1 className="mt-16 flex justify-center">
                        <Image
                            src="/images/logo.png"
                            alt="Logo"
                            width={128}
                            height={20}
                            className='rounded-xl h-14'
                        />
                    </h1>
                    <div className="py-6 space-x-2">
                        <span className="w-10 h-10 items-center justify-center inline-flex rounded-full font-bold text-lg border-2 border-white hover:text-black hover:bg-white cursor-pointer">f</span>
                        <span className="w-10 h-10 items-center justify-center inline-flex rounded-full font-bold text-lg border-2 border-white hover:text-black hover:bg-white cursor-pointer">G</span>
                        <span className="w-10 h-10 items-center justify-center inline-flex rounded-full font-bold text-lg border-2 border-white hover:text-black hover:bg-white cursor-pointer">in</span>
                    </div>
                    <p className="text-gray-100">
                        or use email your account
                    </p>
                    <form onSubmit={handleSignup} className="sm:w-2/3 w-full px-4 lg:px-0 mx-auto">
                        <div className="pb-1 pt-4">
                            <input type="text" name="name" id="name" placeholder="Full name" value={name} onChange={(e: any) => setName(e.target.value)} className="block w-full p-3 text-md rounded-lg bg-black" />
                        </div>
                        <div className="py-1">
                            <input type="email" name="email" id="email" placeholder="Email" value={email} onChange={(e: any) => setEmail(e.target.value)} className="block w-full p-3 text-md rounded-lg bg-black" />
                        </div>
                        <div className="py-1">
                            <input type="password" name="privateapi" id="privateapi" placeholder="Private API Key" value={privateApi} onChange={(e: any) => setPrivateApi(e.target.value)} className="block w-full p-3 text-md rounded-lg bg-black" />
                        </div>
                        <div className="py-1">
                            <input type="text" name="privateapi" id="privateapi" placeholder="Private API Key" value={publicApi} onChange={(e: any) => setPublicApi(e.target.value)} className="block w-full p-3 text-md rounded-lg bg-black" />
                        </div>
                        <div className="py-1">
                            <input className="block w-full p-3 text-md rounded-lg bg-black" type="password" name="password" id="password" placeholder="Password" value={password} onChange={(e: any) => setPassword(e.target.value)} />
                        </div>
                        <div className="py-1">
                            <input className="block w-full p-3 text-md rounded-lg bg-black" type="password" name="password" id="password" placeholder="Password" value={confirmPassword} onChange={(e: any) => setConfirmPassword(e.target.value)} />
                        </div>
                        <div className="px-4 pb-2 pt-4">
                            <button type="submit" className="uppercase block w-full p-4 text-lg rounded-full bg-indigo-500 hover:bg-indigo-600 focus:outline-none">sign up</button>
                        </div>
                        <div className="text-center text-gray-400">
                            Already have an account! &nbsp;
                            <Link href="/signin" className=' hover:underline text-blue-400 hover:text-blue-500'>Sign In</Link>
                        </div>

                        <div className="p-4 text-center right-0 left-0 flex justify-center space-x-4 mt-16 lg:hidden ">
                            <Link href="#">
                                <svg fill="#fff" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M24 4.557c-.883.392-1.832.656-2.828.775 1.017-.609 1.798-1.574 2.165-2.724-.951.564-2.005.974-3.127 1.195-.897-.957-2.178-1.555-3.594-1.555-3.179 0-5.515 2.966-4.797 6.045-4.091-.205-7.719-2.165-10.148-5.144-1.29 2.213-.669 5.108 1.523 6.574-.806-.026-1.566-.247-2.229-.616-.054 2.281 1.581 4.415 3.949 4.89-.693.188-1.452.232-2.224.084.626 1.956 2.444 3.379 4.6 3.419-2.07 1.623-4.678 2.348-7.29 2.04 2.179 1.397 4.768 2.212 7.548 2.212 9.142 0 14.307-7.721 13.995-14.646.962-.695 1.797-1.562 2.457-2.549z" /></svg>
                            </Link>
                            <Link href="#">
                                <svg fill="#fff" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M9 8h-3v4h3v12h5v-12h3.642l.358-4h-4v-1.667c0-.955.192-1.333 1.115-1.333h2.885v-5h-3.808c-3.596 0-5.192 1.583-5.192 4.615v3.385z" /></svg>
                            </Link>
                            <Link href="#">
                                <svg fill="#fff" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z" /></svg>
                            </Link>
                        </div>
                    </form>
                </div>
            </div>
        </main>
    )
}
