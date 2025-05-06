"use client"
import { X, SplitSquareVertical, ChevronRight, Download, Clock } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Switch } from "@/components/ui/switch"
import Link from "next/link"
import { useRouter } from "next/navigation"
import Image from "next/image"

export default function TransactionDetailPage({ params }: { params: { id: string } }) {
  const router = useRouter()

  // This would normally come from an API or database
  // For demo purposes, we're hardcoding the transaction data
  const transaction = {
    id: params.id,
    amount: "-3 €",
    merchant: "Catalana Del Pa Sa G. T",
    date: "Today, 09:21",
    location: "Barcelona Barcelona, Spain",
    status: "Pending",
    statusDate: "14 May",
    card: "Visa •••9598",
    points: "1,50",
    category: "Restaurants",
    icon: "restaurant",
  }

  return (
    <div className="flex flex-col min-h-screen bg-gray-900 text-white">
      {/* Status bar - just for visual representation */}
      <div className="flex justify-between items-center p-4">
        <div className="text-lg font-semibold">10:14</div>
        <div className="flex items-center gap-1">
          <div className="h-3 w-3 rounded-full bg-white"></div>
          <div className="h-3 w-3 rounded-full bg-white"></div>
          <div className="h-3 w-3 rounded-full bg-white"></div>
          <div className="h-4 w-6 rounded-sm bg-yellow-400 ml-1 flex items-center justify-center text-[10px] text-black font-bold">
            84
          </div>
        </div>
      </div>

      {/* Transaction details */}
      <div className="flex-1 px-4 pb-4">
        <div className="flex justify-between items-start mb-6">
          <button onClick={() => router.back()} className="p-2">
            <X className="h-6 w-6" />
          </button>
        </div>

        <div className="flex justify-between items-center mb-2">
          <div>
            <h1 className="text-5xl font-bold mb-1">{transaction.amount}</h1>
            <h2 className="text-2xl text-blue-400 mb-1">{transaction.merchant}</h2>
            <p className="text-gray-400">{transaction.date}</p>
          </div>
          <div className="h-16 w-16 rounded-full bg-orange-500 flex items-center justify-center">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="32"
              height="32"
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
        </div>

        <Button variant="outline" className="rounded-full bg-gray-800 border-0 mb-6 flex items-center gap-2">
          <SplitSquareVertical className="h-4 w-4" />
          Split bill
        </Button>

        {/* Map */}
        <div className="rounded-lg overflow-hidden mb-4">
          <div className="relative h-48 w-full">
            <Image src="/placeholder.svg?height=200&width=600" alt="Map of Barcelona" fill className="object-cover" />
            <div className="absolute inset-0 bg-blue-900/30"></div>
            <div className="absolute bottom-4 left-4 flex items-center">
              <Image
                src="/placeholder.svg?height=30&width=80"
                alt="Apple Maps"
                width={80}
                height={30}
                className="mr-2"
              />
              <span className="text-xs text-white/70">Legal</span>
            </div>
          </div>
          <div className="bg-gray-800 p-4 flex justify-between items-center">
            <span>{transaction.location}</span>
            <ChevronRight className="h-5 w-5 text-gray-400" />
          </div>
        </div>

        {/* Status */}
        <div className="bg-gray-800 rounded-lg p-4 mb-4">
          <h3 className="text-gray-400 mb-2">Status</h3>
          <div className="flex items-start">
            <p className="text-white">
              <span className="font-medium">
                {transaction.status} • Will be automatically reverted on {transaction.statusDate} if unclaimed by
                merchant.{" "}
              </span>
              <Link href="#" className="text-blue-400">
                Learn more
              </Link>
            </p>
          </div>
        </div>

        {/* Card */}
        <div className="bg-gray-800 rounded-lg p-4 mb-4 flex justify-between items-center">
          <h3 className="text-gray-400">Card</h3>
          <div className="flex items-center">
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="text-blue-400 mr-2"
            >
              <rect width="20" height="14" x="2" y="5" rx="2" />
              <line x1="2" x2="22" y1="10" y2="10" />
            </svg>
            <span className="text-blue-400">{transaction.card}</span>
          </div>
        </div>

        {/* Statement */}
        <div className="bg-gray-800 rounded-lg p-4 mb-4 flex justify-between items-center">
          <h3 className="text-gray-400">Statement</h3>
          <div className="flex items-center text-blue-400">
            <Download className="h-5 w-5 mr-2" />
            <span>Download</span>
          </div>
        </div>

        {/* Points earned */}
        <div className="bg-gray-800 rounded-lg p-4 mb-4 flex justify-between items-center">
          <h3 className="text-gray-400">Points earned</h3>
          <div className="flex items-center text-blue-400">
            <Clock className="h-5 w-5 mr-2" />
            <span>{transaction.points}</span>
          </div>
        </div>

        {/* Exclude from analytics */}
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-gray-400">Exclude from analytics</h3>
          <Switch />
        </div>

        {/* Category */}
        <div className="flex justify-between items-center">
          <h3 className="text-gray-400">Category</h3>
          <div className="flex items-center">
            <div className="w-[200px] h-1 bg-gradient-to-r from-gray-700 via-gray-600 to-blue-500 rounded-full mr-2"></div>
            <svg
              xmlns="http://www.w3.org/2000/svg"
              width="20"
              height="20"
              viewBox="0 0 24 24"
              fill="none"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
              className="text-blue-400 mr-2"
            >
              <path d="M8 3v3a2 2 0 0 1-2 2H3" />
              <path d="M21 3v3a2 2 0 0 0 2 2h3" />
              <path d="M3 16v3a2 2 0 0 0 2 2h3" />
              <path d="M16 21v-3a2 2 0 0 1 2-2h3" />
              <path d="M7 12h10" />
              <path d="M12 7v10" />
            </svg>
            <span className="text-blue-400">{transaction.category}</span>
          </div>
        </div>
      </div>
    </div>
  )
}
