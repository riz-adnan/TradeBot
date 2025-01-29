"use client"

import React, { useState, useEffect } from 'react'
import Image from 'next/image'
import Link from 'next/link'

import TestimonialImage01 from '@/public/images/testimonial-01.jpg'
import TestimonialImage02 from '@/public/images/testimonial-02.jpg'
import TestimonialImage03 from '@/public/images/testimonial-03.jpg'

export default function Testimonials() {
  const [testimonials, setTestimonials] = useState([
    {
      id: 1,
      name: 'Anastasia Dan',
      company: 'UX Board',
      image: TestimonialImage01,
      text: 'This trade bot has revolutionized my investing game! Its LSTM and ML techniques deliver accurate predictions and solid profits. It’s an essential tool for any serious trader.',
    },
    {
      id: 2,
      name: 'Anastasia Dan',
      company: 'UX Board',
      image: TestimonialImage02,
      text: 'This trade bot has revolutionized my investing game! Its LSTM and ML techniques deliver accurate predictions and solid profits. It’s an essential tool for any serious trader.',
    },
    {
      id: 3,
      name: 'Anastasia Dan',
      company: 'UX Board',
      image: TestimonialImage03,
      text: 'This trade bot has revolutionized my investing game! Its LSTM and ML techniques deliver accurate predictions and solid profits. It’s an essential tool for any serious trader.',
    },
    {
      id: 4,
      name: 'Anastasia Dan',
      company: 'UX Board',
      image: TestimonialImage01,
      text: 'This trade bot has revolutionized my investing game! Its LSTM and ML techniques deliver accurate predictions and solid profits. It’s an essential tool for any serious trader.',
    },
    {
      id: 5,
      name: 'Anastasia Dan',
      company: 'UX Board',
      image: TestimonialImage02,
      text: 'This trade bot has revolutionized my investing game! Its LSTM and ML techniques deliver accurate predictions and solid profits. It’s an essential tool for any serious trader.',
    },
    {
      id: 6,
      name: 'Anastasia Dan',
      company: 'UX Board',
      image: TestimonialImage03,
      text: 'This trade bot has revolutionized my investing game! Its LSTM and ML techniques deliver accurate predictions and solid profits. It’s an essential tool for any serious trader.',
    },
  ])

  useEffect(() => {
    // Fetch testimonials from an API
  }, [])

  return (
    <section>
      <div className="max-w-6xl mx-auto px-4 sm:px-6">
        <div className="py-12 md:py-20 border-t border-gray-800">

          {/* Section header */}
          <div className="max-w-3xl mx-auto text-center pb-12 md:pb-20">
            <h2 className="h2 mb-4">Not only we say!</h2>
            <p className="text-xl text-gray-400">See what are the views of the others on our product and service</p>
          </div>

          {/* Testimonials */}
          <div className="max-w-sm mx-auto lg:max-w-none">
            <div className="flex overflow-x-auto hide-scroll-bar space-x-6 lg:grid-cols-3 items-start">
              {testimonials.map((testimony) => (
                <div
                  key={testimony.id}
                  className="flex flex-col h-full p-6 bg-gray-800 flex-shrink-0 w-[300px]"
                  data-aos="fade-up"
                >
                  <div>
                    <div className="relative inline-flex flex-col mb-4">
                      <Image
                        className="rounded-full"
                        src={testimony.image}
                        width={48}
                        height={48}
                        alt="Testimonial"
                      />
                      <svg
                        className="absolute top-0 right-0 -mr-3 w-6 h-5 fill-current text-purple-600"
                        viewBox="0 0 24 20"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path d="M0 13.517c0-2.346.611-4.774 1.833-7.283C3.056 3.726 4.733 1.648 6.865 0L11 2.696C9.726 4.393 8.777 6.109 8.152 7.844c-.624 1.735-.936 3.589-.936 5.56v4.644H0v-4.531zm13 0c0-2.346.611-4.774 1.833-7.283 1.223-2.508 2.9-4.586 5.032-6.234L24 2.696c-1.274 1.697-2.223 3.413-2.848 5.148-.624 1.735-.936 3.589-.936 5.56v4.644H13v-4.531z" />
                      </svg>
                    </div>
                  </div>
                  <blockquote className="text-lg text-gray-400 grow">— {testimony.text}</blockquote>
                  <div className="text-gray-700 font-medium mt-6 pt-5 border-t border-gray-700">
                    <cite className="text-gray-200 not-italic">{testimony.name}</cite> -{' '}
                    <Link
                      className="text-purple-600 hover:text-gray-200 transition duration-150 ease-in-out"
                      href="#0"
                    >
                      {testimony.company}
                    </Link>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <style jsx>{`
            .hide-scroll-bar {
              -ms-overflow-style: none; /* Internet Explorer 10+ */
              scrollbar-width: none; /* Firefox */
            }

            .hide-scroll-bar::-webkit-scrollbar {
              display: none; /* Safari and Chrome */
            }
          `}</style>

        </div>
      </div>
    </section>
  )
}
