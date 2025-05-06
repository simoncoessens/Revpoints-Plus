"use client"
import { ArrowLeft, Search, SlidersHorizontal } from "lucide-react"
import { Input } from "@/components/ui/input"
import { Button } from "@/components/ui/button"
import Link from "next/link"

export default function TransactionsPage() {
  return (
    <div className="flex flex-col min-h-screen bg-black text-white">
      {/* Status bar - just for visual representation */}
      <div className="flex justify-between items-center p-4">
        <div className="text-lg font-semibold">10:12</div>
        <div className="flex items-center gap-1">
          <div className="h-3 w-3 rounded-full bg-white"></div>
          <div className="h-3 w-3 rounded-full bg-white"></div>
          <div className="h-3 w-3 rounded-full bg-white"></div>
          <div className="h-4 w-6 rounded-sm bg-yellow-400 ml-1 flex items-center justify-center text-[10px] text-black font-bold">
            85
          </div>
        </div>
      </div>

      {/* Header */}
      <div className="px-4 py-2">
        <Link href="/" className="inline-block mb-4">
          <ArrowLeft className="h-6 w-6" />
        </Link>
        <h1 className="text-4xl font-bold mb-6">Transactions</h1>

        <div className="flex items-center gap-2 mb-8">
          <div className="relative flex-1">
            <div className="absolute inset-y-0 left-3 flex items-center pointer-events-none">
              <Search className="h-4 w-4 text-gray-400" />
            </div>
            <Input className="w-full bg-gray-800 border-0 rounded-full pl-10 text-gray-200" placeholder="Search" />
          </div>
          <Button variant="ghost" size="icon" className="rounded-full bg-blue-500 h-10 w-10">
            <SlidersHorizontal className="h-5 w-5" />
          </Button>
        </div>
      </div>

      {/* Transactions list */}
      <div className="flex-1 px-4">
        {/* Today */}
        <div className="mb-6">
          <div className="flex justify-between items-center mb-2">
            <h2 className="text-xl font-semibold">Today</h2>
            <span className="text-lg font-medium">-3 €</span>
          </div>

          <div className="bg-gray-900 rounded-lg overflow-hidden">
            <Link href="/transaction/catalana" className="block">
              <div className="p-4 flex items-center justify-between">
                <div className="flex items-center">
                  <div className="h-12 w-12 rounded-full bg-orange-500 flex items-center justify-center mr-4">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className="text-white"
                    >
                      <path d="M8 3v3a2 2 0 0 1-2 2H3" />
                      <path d="M21 3v3a2 2 0 0 0 2 2h3" />
                      <path d="M3 16v3a2 2 0 0 0 2 2h3" />
                      <path d="M16 21v-3a2 2 0 0 1 2-2h3" />
                      <path d="M7 12h10" />
                      <path d="M12 7v10" />
                    </svg>
                  </div>
                  <div>
                    <div className="font-medium text-lg">Catalana Del Pa Sa G. T</div>
                    <div className="text-sm text-gray-400">09:21</div>
                  </div>
                </div>
                <div className="font-medium text-lg">-3 €</div>
              </div>
            </Link>
          </div>
        </div>

        {/* Yesterday */}
        <div className="mb-6">
          <div className="flex justify-between items-center mb-2">
            <h2 className="text-xl font-semibold">Yesterday</h2>
            <span className="text-lg font-medium">-23,50 €</span>
          </div>

          <div className="bg-gray-900 rounded-lg overflow-hidden">
            <Link href="/transaction/monroe1" className="block">
              <div className="p-4 flex items-center justify-between border-b border-gray-800">
                <div className="flex items-center">
                  <div className="h-12 w-12 rounded-full bg-white flex items-center justify-center mr-4">
                    <div className="h-7 w-7 border-2 border-black rounded-full"></div>
                  </div>
                  <div>
                    <div className="font-medium text-lg">La Monroe</div>
                    <div className="text-sm text-gray-400">22:58</div>
                  </div>
                </div>
                <div className="font-medium text-lg">-3,50 €</div>
              </div>
            </Link>

            <Link href="/transaction/monroe2" className="block">
              <div className="p-4 flex items-center justify-between border-b border-gray-800">
                <div className="flex items-center">
                  <div className="h-12 w-12 rounded-full bg-white flex items-center justify-center mr-4">
                    <div className="h-7 w-7 border-2 border-black rounded-full"></div>
                  </div>
                  <div>
                    <div className="font-medium text-lg">La Monroe</div>
                    <div className="text-sm text-gray-400">22:57</div>
                  </div>
                </div>
                <div className="font-medium text-lg">-3 €</div>
              </div>
            </Link>

            <Link href="/transaction/ali" className="block">
              <div className="p-4 flex items-center justify-between border-b border-gray-800">
                <div className="flex items-center">
                  <div className="h-12 w-12 rounded-full bg-orange-500 flex items-center justify-center mr-4">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className="text-white"
                    >
                      <path d="M8 3v3a2 2 0 0 1-2 2H3" />
                      <path d="M21 3v3a2 2 0 0 0 2 2h3" />
                      <path d="M3 16v3a2 2 0 0 0 2 2h3" />
                      <path d="M16 21v-3a2 2 0 0 1 2-2h3" />
                      <path d="M7 12h10" />
                      <path d="M12 7v10" />
                    </svg>
                  </div>
                  <div>
                    <div className="font-medium text-lg">Ali Restaurant</div>
                    <div className="text-sm text-gray-400">22:10</div>
                  </div>
                </div>
                <div className="font-medium text-lg">-12,30 €</div>
              </div>
            </Link>

            <Link href="/transaction/empanada" className="block">
              <div className="p-4 flex items-center justify-between border-b border-gray-800">
                <div className="flex items-center">
                  <div className="h-12 w-12 rounded-full bg-orange-500 flex items-center justify-center mr-4">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      width="24"
                      height="24"
                      viewBox="0 0 24 24"
                      fill="none"
                      stroke="currentColor"
                      strokeWidth="2"
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      className="text-white"
                    >
                      <path d="M8 3v3a2 2 0 0 1-2 2H3" />
                      <path d="M21 3v3a2 2 0 0 0 2 2h3" />
                      <path d="M3 16v3a2 2 0 0 0 2 2h3" />
                      <path d="M16 21v-3a2 2 0 0 1 2-2h3" />
                      <path d="M7 12h10" />
                      <path d="M12 7v10" />
                    </svg>
                  </div>
                  <div>
                    <div className="font-medium text-lg">Empanadaclubgrandegracia 1</div>
                    <div className="text-sm text-gray-400">17:48</div>
                  </div>
                </div>
                <div className="font-medium text-lg">-3,50 €</div>
              </div>
            </Link>

            <Link href="/transaction/arbitrade" className="block">
              <div className="p-4 flex items-center justify-between">
                <div className="flex items-center">
                  <div className="h-12 w-12 rounded-full bg-white flex items-center justify-center mr-4">
                    <div className="text-[8px] text-black font-bold">service vendita</div>
                  </div>
                  <div>
                    <div className="font-medium text-lg">Arbitrade</div>
                    <div className="text-sm text-gray-400">11:13</div>
                  </div>
                </div>
                <div className="font-medium text-lg">-1,20 €</div>
              </div>
            </Link>
          </div>
        </div>

        {/* 3 May */}
        <div className="mb-6">
          <div className="flex justify-between items-center mb-2">
            <h2 className="text-xl font-semibold">3 May</h2>
            <span className="text-lg font-medium">-105,78 €</span>
          </div>
        </div>
      </div>

      {/* Home indicator */}
      <div className="flex justify-center pb-2 pt-1">
        <div className="w-32 h-1 bg-white rounded-full"></div>
      </div>
    </div>
  )
}
