"use client";

import { useState, useEffect } from "react";
import {
  Search,
  BarChart3,
  Menu,
  Plus,
  ArrowRightLeft,
  Building2,
  MoreHorizontal,
} from "lucide-react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { cn } from "@/lib/utils";
import Link from "next/link";
import { TransactionDetailsSheet } from "@/components/transaction-details-sheet";

interface Transaction {
  id: string;
  merchant: string;
  date: string;
  amount: string;
  currency: string;
  location?: string;
  status?: string;
  statusDate?: string;
  card?: string;
  points?: string;
  category?: string;
  logoUrl?: string;
}

export default function RevolutApp() {
  const [activeTab, setActiveTab] = useState("home");
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [selectedTransaction, setSelectedTransaction] =
    useState<Transaction | null>(null);
  const [isTransactionSheetOpen, setIsTransactionSheetOpen] = useState(false);

  useEffect(() => {
    fetch("/api/transactions")
      .then((response) => response.json())
      .then((data) => {
        // Transform the data to match our interface and filter out Uber Eats
        const transformedData = data
          .filter((t: any) => t.merchant_name !== "Uber Eats")
          .map((t: any) => ({
            id: t.id,
            merchant: t.merchant_name,
            date: t.timestamp,
            amount: t.amount,
            currency: t.currency,
            location: t.location,
            status: t.status,
            statusDate: t.statusDate,
            card: t.card,
            points: t.points,
            category: t.category,
            logoUrl: t.logoUrl,
          }));
        setTransactions(transformedData);
      })
      .catch((error) => console.error("Error fetching transactions:", error));
  }, []);

  const handleTransactionClick = (transaction: Transaction) => {
    setSelectedTransaction(transaction);
    setIsTransactionSheetOpen(true);
  };

  const closeTransactionSheet = () => {
    setIsTransactionSheetOpen(false);
  };

  return (
    <div className="flex flex-col min-h-screen bg-black text-white overflow-hidden relative">
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
          <div className="absolute top-0 right-0 h-2 w-2 bg-red-500 rounded-full z-10"></div>
          <AvatarImage src="/placeholder.svg?height=40&width=40" alt="User" />
          <AvatarFallback>U</AvatarFallback>
        </Avatar>

        <div className="flex-1 mx-2">
          <div className="relative">
            <div className="absolute inset-y-0 left-3 flex items-center pointer-events-none">
              <Search className="h-4 w-4 text-gray-400" />
            </div>
            <Input
              className="w-full bg-gray-700/70 border-0 rounded-full pl-10 text-gray-200"
              placeholder="Search"
            />
          </div>
        </div>

        <Button
          variant="ghost"
          size="icon"
          className="rounded-full bg-gray-700/70"
        >
          <BarChart3 className="h-5 w-5" />
        </Button>

        <Button
          variant="ghost"
          size="icon"
          className="rounded-full bg-gray-700/70 ml-2"
        >
          <Menu className="h-5 w-5" />
        </Button>
      </div>

      {/* Balance section */}
      <div className="flex flex-col items-center justify-center mt-12 mb-6 relative z-10">
        <div className="text-gray-300 text-sm mb-1">Personal · EUR</div>
        <div className="flex items-baseline">
          <span className="text-6xl font-semibold">541</span>
          <span className="text-3xl font-semibold">,85 €</span>
        </div>

        <Button
          variant="secondary"
          className="mt-4 rounded-full bg-gray-700/70 text-white px-6"
        >
          Accounts
        </Button>

        <div className="flex gap-1 mt-6">
          <div className="h-1.5 w-1.5 rounded-full bg-white"></div>
          <div className="h-1.5 w-1.5 rounded-full bg-white/60"></div>
          <div className="h-1.5 w-1.5 rounded-full bg-white/60"></div>
          <div className="h-1.5 w-1.5 rounded-full bg-white/60"></div>
        </div>
      </div>

      {/* Action buttons */}
      <div className="flex justify-between px-8 py-4 relative z-10">
        <div className="flex flex-col items-center">
          <Button
            variant="ghost"
            size="icon"
            className="h-14 w-14 rounded-full bg-gray-700/70 mb-2"
          >
            <Plus className="h-6 w-6" />
          </Button>
          <span className="text-sm">Add money</span>
        </div>

        <div className="flex flex-col items-center">
          <Button
            variant="ghost"
            size="icon"
            className="h-14 w-14 rounded-full bg-gray-700/70 mb-2"
          >
            <ArrowRightLeft className="h-6 w-6" />
          </Button>
          <span className="text-sm">Move</span>
        </div>

        <div className="flex flex-col items-center">
          <Button
            variant="ghost"
            size="icon"
            className="h-14 w-14 rounded-full bg-gray-700/70 mb-2"
          >
            <Building2 className="h-6 w-6" />
          </Button>
          <span className="text-sm">Details</span>
        </div>

        <div className="flex flex-col items-center">
          <Button
            variant="ghost"
            size="icon"
            className="h-14 w-14 rounded-full bg-gray-700/70 mb-2"
          >
            <MoreHorizontal className="h-6 w-6" />
          </Button>
          <span className="text-sm">More</span>
        </div>
      </div>

      {/* Transactions */}
      <div className="flex-1 mt-4 relative z-10">
        <div className="bg-gray-900/90 rounded-t-3xl p-4">
          <div className="space-y-4">
            {transactions.slice(0, 3).map((transaction) => (
              <div
                key={transaction.id}
                className="flex items-center justify-between py-2 cursor-pointer"
                onClick={() => handleTransactionClick(transaction)}
              >
                <div className="flex items-center">
                  <div className="h-10 w-10 rounded-full bg-orange-500 flex items-center justify-center mr-3">
                    {transaction.logoUrl ? (
                      <img
                        src={transaction.logoUrl}
                        alt={transaction.merchant}
                        className="h-6 w-6"
                      />
                    ) : (
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
                    )}
                  </div>
                  <div>
                    <div className="font-medium">{transaction.merchant}</div>
                    <div className="text-sm text-gray-400">
                      {transaction.date}
                    </div>
                  </div>
                </div>
                <div className="font-medium">
                  {transaction.amount} {transaction.currency}
                </div>
              </div>
            ))}

            <Link href="/transactions" className="w-full">
              <Button variant="ghost" className="w-full text-center py-2">
                See all
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
            activeTab !== "home" && "text-gray-500"
          )}
          onClick={() => setActiveTab("home")}
        >
          <div className="h-6 w-6">
            <svg
              viewBox="0 0 24 24"
              fill="none"
              xmlns="http://www.w3.org/2000/svg"
              className="h-6 w-6"
            >
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

        <div
          className={cn(
            "flex flex-col items-center",
            activeTab === "invest" && "text-white",
            activeTab !== "invest" && "text-gray-500"
          )}
          onClick={() => setActiveTab("invest")}
        >
          <BarChart3 className="h-6 w-6" />
          <span className="text-xs mt-1">Invest</span>
        </div>

        <div
          className={cn(
            "flex flex-col items-center",
            activeTab === "payments" && "text-white",
            activeTab !== "payments" && "text-gray-500"
          )}
          onClick={() => setActiveTab("payments")}
        >
          <ArrowRightLeft className="h-6 w-6" />
          <span className="text-xs mt-1">Payments</span>
        </div>

        <div
          className={cn(
            "flex flex-col items-center",
            activeTab === "crypto" && "text-white",
            activeTab !== "crypto" && "text-gray-500"
          )}
          onClick={() => setActiveTab("crypto")}
        >
          <svg
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6"
          >
            <path
              d="M9 8H15M9 16H15M12 4V20M7.8 20H16.2C17.8802 20 18.7202 20 19.362 19.673C19.9265 19.3854 20.3854 18.9265 20.673 18.362C21 17.7202 21 16.8802 21 15.2V8.8C21 7.11984 21 6.27976 20.673 5.63803C20.3854 5.07354 19.9265 4.6146 19.362 4.32698C18.7202 4 17.8802 4 16.2 4H7.8C6.11984 4 5.27976 4 4.63803 4.32698C4.07354 4.6146 3.6146 5.07354 3.32698 5.63803C3 6.27976 3 7.11984 3 8.8V15.2C3 16.8802 3 17.7202 3.32698 18.362C3.6146 18.9265 4.07354 19.3854 4.63803 19.673C5.27976 20 6.11984 20 7.8 20Z"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <span className="text-xs mt-1">Crypto</span>
        </div>

        <Link
          href="/revpoints"
          className="flex flex-col items-center text-gray-500"
        >
          <svg
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6"
          >
            <path
              d="M12 8V16M8 12H16M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <span className="text-xs mt-1">RevPoints</span>
        </Link>
      </div>

      {/* Home indicator */}
      <div className="flex justify-center pb-2 pt-1 bg-gray-900">
        <div className="w-32 h-1 bg-white rounded-full"></div>
      </div>

      {/* Transaction Details Sheet */}
      {selectedTransaction && (
        <TransactionDetailsSheet
          isOpen={isTransactionSheetOpen}
          onClose={closeTransactionSheet}
          transaction={selectedTransaction}
        />
      )}
    </div>
  );
}
