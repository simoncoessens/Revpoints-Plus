"use client"

import { useState } from "react"
import { Search, BarChart3, Menu, Plus, ArrowRightLeft, Megaphone, MoreHorizontal, ArrowUpRight } from "lucide-react"
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { cn } from "@/lib/utils"
import Link from "next/link"
import { Badge } from "@/components/ui/badge"

export default function VendorDashboard() {
  const [activeTab, setActiveTab] = useState("home")

  return (
    <div className="flex flex-col min-h-screen bg-black text-white overflow-hidden relative">
      {/* Background pattern */}
      <div
        className="absolute inset-0 z-0 opacity-50"
        style={{
          backgroundImage: "url('/wave-pattern.png')",
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      />

      {/* Status bar - just for visual representation */}
      <div className="flex justify-between items-center p-4 relative z-10">
        <div className="text-lg font-semibold">10:08</div>
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
      <div className="flex items-center justify-between px-4 py-2 relative z-10">
        <Avatar className="h-10 w-10 border-2 border-white relative">
          <div className="absolute top-0 right-0 h-2 w-2 bg-green-500 rounded-full z-10"></div>
          <AvatarImage src="/placeholder.svg?height=40&width=40" alt="Business" />
          <AvatarFallback>BF</AvatarFallback>
        </Avatar>

        <div className="flex-1 mx-2">
          <div className="relative">
            <div className="absolute inset-y-0 left-3 flex items-center pointer-events-none">
              <Search className="h-4 w-4 text-gray-400" />
            </div>
            <Input
              className="w-full bg-gray-700/70 border-0 rounded-full pl-10 text-gray-200"
              placeholder="Search transactions"
            />
          </div>
        </div>

        <Button variant="ghost" size="icon" className="rounded-full bg-gray-700/70">
          <BarChart3 className="h-5 w-5" />
        </Button>

        <Button variant="ghost" size="icon" className="rounded-full bg-gray-700/70 ml-2">
          <Menu className="h-5 w-5" />
        </Button>
      </div>

      {/* Business name and badge */}
      <div className="px-4 py-2 relative z-10">
        <div className="flex items-center">
          <h1 className="text-2xl font-bold">Bar de La FIB</h1>
          <Badge className="ml-2 bg-green-600">Business Account</Badge>
        </div>
        <p className="text-gray-400 text-sm">Campus Nord, Barcelona</p>
      </div>

      {/* Balance section */}
      <div className="flex flex-col items-center justify-center mt-6 mb-6 relative z-10">
        <div className="text-gray-300 text-sm mb-1">Business · EUR</div>
        <div className="flex items-baseline">
          <span className="text-6xl font-semibold">3,541</span>
          <span className="text-3xl font-semibold">,85 €</span>
        </div>

        <Button variant="secondary" className="mt-4 rounded-full bg-gray-700/70 text-white px-6">
          Accounts
        </Button>

        <div className="flex gap-1 mt-6">
          <div className="h-1.5 w-1.5 rounded-full bg-white"></div>
          <div className="h-1.5 w-1.5 rounded-full bg-white/60"></div>
          <div className="h-1.5 w-1.5 rounded-full bg-white/60"></div>
          <div className="h-1.5 w-1.5 rounded-full bg-white/60"></div>
        </div>
      </div>

      {/* Today's earnings */}
      <div className="px-4 py-2 relative z-10">
        <div className="bg-gray-800/80 rounded-lg p-4">
          <h2 className="text-lg font-medium mb-2">Today's Earnings</h2>
          <div className="flex items-center justify-between">
            <div className="text-3xl font-bold">542,75 €</div>
            <div className="flex items-center text-green-400">
              <ArrowUpRight className="h-5 w-5 mr-1" />
              <span>+12% from yesterday</span>
            </div>
          </div>
          <div className="mt-2 text-sm text-gray-400">78 transactions today</div>
        </div>
      </div>

      {/* Action buttons */}
      <div className="flex justify-between px-8 py-4 relative z-10">
        <div className="flex flex-col items-center">
          <Button variant="ghost" size="icon" className="h-14 w-14 rounded-full bg-gray-700/70 mb-2">
            <Plus className="h-6 w-6" />
          </Button>
          <span className="text-sm">New Sale</span>
        </div>

        <div className="flex flex-col items-center">
          <Button variant="ghost" size="icon" className="h-14 w-14 rounded-full bg-gray-700/70 mb-2">
            <ArrowRightLeft className="h-6 w-6" />
          </Button>
          <span className="text-sm">Transfer</span>
        </div>

        <div className="flex flex-col items-center">
          <Button variant="ghost" size="icon" className="h-14 w-14 rounded-full bg-gray-700/70 mb-2">
            <Megaphone className="h-6 w-6" />
          </Button>
          <span className="text-sm">Campaigns</span>
        </div>

        <div className="flex flex-col items-center">
          <Button variant="ghost" size="icon" className="h-14 w-14 rounded-full bg-gray-700/70 mb-2">
            <MoreHorizontal className="h-6 w-6" />
          </Button>
          <span className="text-sm">More</span>
        </div>
      </div>

      {/* Transactions */}
      <div className="flex-1 mt-4 relative z-10">
        <div className="bg-gray-900/90 rounded-t-3xl p-4">
          <h2 className="text-xl font-semibold mb-4">Recent Transactions</h2>
          <div className="space-y-4">
            <div className="flex items-center justify-between py-2">
              <div className="flex items-center">
                <div className="h-10 w-10 rounded-full bg-green-500 flex items-center justify-center mr-3">
                  <ArrowUpRight className="h-5 w-5 text-white" />
                </div>
                <div>
                  <div className="font-medium">Payment from Student</div>
                  <div className="text-sm text-gray-400">Today, 09:21</div>
                </div>
              </div>
              <div className="font-medium text-green-400">+5,50 €</div>
            </div>

            <div className="flex items-center justify-between py-2">
              <div className="flex items-center">
                <div className="h-10 w-10 rounded-full bg-green-500 flex items-center justify-center mr-3">
                  <ArrowUpRight className="h-5 w-5 text-white" />
                </div>
                <div>
                  <div className="font-medium">Payment from Professor</div>
                  <div className="text-sm text-gray-400">Today, 08:45</div>
                </div>
              </div>
              <div className="font-medium text-green-400">+8,75 €</div>
            </div>

            <div className="flex items-center justify-between py-2">
              <div className="flex items-center">
                <div className="h-10 w-10 rounded-full bg-green-500 flex items-center justify-center mr-3">
                  <ArrowUpRight className="h-5 w-5 text-white" />
                </div>
                <div>
                  <div className="font-medium">Payment from Student Group</div>
                  <div className="text-sm text-gray-400">Today, 08:30</div>
                </div>
              </div>
              <div className="font-medium text-green-400">+24,50 €</div>
            </div>

            <div className="flex items-center justify-between py-2">
              <div className="flex items-center">
                <div className="h-10 w-10 rounded-full bg-red-500 flex items-center justify-center mr-3">
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
                    className="text-white"
                  >
                    <path d="M7 10l5 5 5-5" />
                    <path d="M12 15V3" />
                  </svg>
                </div>
                <div>
                  <div className="font-medium">Supplier Payment</div>
                  <div className="text-sm text-gray-400">Yesterday, 16:20</div>
                </div>
              </div>
              <div className="font-medium text-red-400">-120,30 €</div>
            </div>

            <div className="flex items-center justify-between py-2">
              <div className="flex items-center">
                <div className="h-10 w-10 rounded-full bg-green-500 flex items-center justify-center mr-3">
                  <ArrowUpRight className="h-5 w-5 text-white" />
                </div>
                <div>
                  <div className="font-medium">Payment from Faculty Event</div>
                  <div className="text-sm text-gray-400">Yesterday, 14:15</div>
                </div>
              </div>
              <div className="font-medium text-green-400">+185,00 €</div>
            </div>

            <Link href="/transactions" className="w-full">
              <Button variant="ghost" className="w-full text-center py-2">
                See all transactions
              </Button>
            </Link>
          </div>
        </div>
      </div>

      {/* Bottom navigation */}
      <div className="bg-gray-900 border-t border-gray-800 p-4 flex justify-between items-center relative z-10">
        <div
          className={cn(
            "flex flex-col items-center",
            activeTab === "home" && "text-white",
            activeTab !== "home" && "text-gray-500",
          )}
          onClick={() => setActiveTab("home")}
        >
          <div className="h-6 w-6">
            <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="h-6 w-6">
              <path
                d="M12 2L3 9V20C3 20.5304 3.21071 21.0391 3.58579 21.4142C3.96086 21.7893 4.46957 22 5 22H19C19.5304 22 20.0391 21.7893 20.4142 21.4142C20.7893 21.0391 21 20.5304 21 20V9L12 2Z"
                stroke="currentColor"
                strokeWidth="2"
                strokeLinecap="round"
                strokeLinejoin="round"
              />
            </svg>
          </div>
          <span className="text-xs mt-1">Home</span>
        </div>

        <Link href="/analytics" className="flex flex-col items-center text-gray-500">
          <BarChart3 className="h-6 w-6" />
          <span className="text-xs mt-1">Analytics</span>
        </Link>

        <div
          className={cn(
            "flex flex-col items-center",
            activeTab === "payments" && "text-white",
            activeTab !== "payments" && "text-gray-500",
          )}
          onClick={() => setActiveTab("payments")}
        >
          <ArrowRightLeft className="h-6 w-6" />
          <span className="text-xs mt-1">Payments</span>
        </div>

        <Link href="/campaigns" className="flex flex-col items-center text-gray-500">
          <Megaphone className="h-6 w-6" />
          <span className="text-xs mt-1">Campaigns</span>
        </Link>

        <Link href="/revpoints" className="flex flex-col items-center text-gray-500">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="h-6 w-6">
            <path
              d="M12 8V16M8 12H16M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <span className="text-xs mt-1">More</span>
        </Link>
      </div>

      {/* Home indicator */}
      <div className="flex justify-center pb-2 pt-1 bg-gray-900">
        <div className="w-32 h-1 bg-white rounded-full"></div>
      </div>
    </div>
  )
}
