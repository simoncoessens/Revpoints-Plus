"use client";
import { useState } from "react";
import { ArrowLeft, Search, SlidersHorizontal } from "lucide-react";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { TransactionDetailsSheet } from "@/components/transaction-details-sheet";

// Sample transaction data
const transactions = [
  {
    id: "mcdonalds1",
    amount: "-1,71 €",
    merchant: "McDonald's",
    date: "Today, 17:46",
    location: "08820 El Prat de Llobregat Barcelona, Spain",
    status: "Pending",
    statusDate: "14 May",
    card: "Visa •••9598",
    points: "0,85",
    category: "Restaurants",
    logoUrl: "/mcdonalds-logo.png",
  },
  {
    id: "catalana1",
    amount: "-3 €",
    merchant: "Catalana Del Pa Sa G. T",
    date: "Today, 09:21",
    location: "Barcelona, Spain",
    status: "Pending",
    statusDate: "14 May",
    card: "Visa •••9598",
    points: "1,50",
    category: "Restaurants",
  },
  {
    id: "monroe1",
    amount: "-3,50 €",
    merchant: "La Monroe",
    date: "Yesterday, 22:58",
    location: "Barcelona, Spain",
    status: "Pending",
    statusDate: "14 May",
    card: "Visa •••9598",
    points: "1,75",
    category: "Restaurants",
  },
  {
    id: "monroe2",
    amount: "-3 €",
    merchant: "La Monroe",
    date: "Yesterday, 22:57",
    location: "Barcelona, Spain",
    status: "Pending",
    statusDate: "14 May",
    card: "Visa •••9598",
    points: "1,50",
    category: "Restaurants",
  },
  {
    id: "ali1",
    amount: "-12,30 €",
    merchant: "Ali Restaurant",
    date: "Yesterday, 22:10",
    location: "Barcelona, Spain",
    status: "Pending",
    statusDate: "14 May",
    card: "Visa •••9598",
    points: "6,15",
    category: "Restaurants",
  },
  {
    id: "empanada1",
    amount: "-3,50 €",
    merchant: "Empanadaclubgrandegracia 1",
    date: "Yesterday, 17:48",
    location: "Barcelona, Spain",
    status: "Pending",
    statusDate: "14 May",
    card: "Visa •••9598",
    points: "1,75",
    category: "Restaurants",
  },
  {
    id: "arbitrade1",
    amount: "-1,20 €",
    merchant: "Arbitrade",
    date: "Yesterday, 11:13",
    location: "Barcelona, Spain",
    status: "Pending",
    statusDate: "14 May",
    card: "Visa •••9598",
    points: "0,60",
    category: "Services",
  },
];

export default function TransactionsPage() {
  const [selectedTransaction, setSelectedTransaction] = useState<
    (typeof transactions)[0] | null
  >(null);
  const [isTransactionSheetOpen, setIsTransactionSheetOpen] = useState(false);

  const handleTransactionClick = (transaction: (typeof transactions)[0]) => {
    setSelectedTransaction(transaction);
    setIsTransactionSheetOpen(true);
  };

  const closeTransactionSheet = () => {
    setIsTransactionSheetOpen(false);
  };

  // Group transactions by date
  const todayTransactions = transactions.filter((t) =>
    t.date.includes("Today")
  );
  const yesterdayTransactions = transactions.filter((t) =>
    t.date.includes("Yesterday")
  );

  // Calculate totals
  const todayTotal = todayTransactions.reduce((sum, t) => {
    const amount = Number.parseFloat(
      t.amount.replace("€", "").replace(",", ".").trim()
    );
    return sum + amount;
  }, 0);

  const yesterdayTotal = yesterdayTransactions.reduce((sum, t) => {
    const amount = Number.parseFloat(
      t.amount.replace("€", "").replace(",", ".").trim()
    );
    return sum + amount;
  }, 0);

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
            <Input
              className="w-full bg-gray-800 border-0 rounded-full pl-10 text-gray-200"
              placeholder="Search"
            />
          </div>
          <Button
            variant="ghost"
            size="icon"
            className="rounded-full bg-blue-500 h-10 w-10"
          >
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
            <span className="text-lg font-medium">
              {todayTotal.toFixed(2).replace(".", ",")} €
            </span>
          </div>

          <div className="bg-gray-900 rounded-lg overflow-hidden">
            {todayTransactions.map((transaction) => (
              <div
                key={transaction.id}
                className="p-4 flex items-center justify-between border-b border-gray-800 last:border-b-0 cursor-pointer"
                onClick={() => handleTransactionClick(transaction)}
              >
                <div className="flex items-center">
                  <div className="h-12 w-12 rounded-full bg-orange-500 flex items-center justify-center mr-4">
                    {transaction.id === "mcdonalds1" ? (
                      <div className="text-yellow-400 text-2xl font-bold">
                        M
                      </div>
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
                    <div className="font-medium text-lg">
                      {transaction.merchant}
                    </div>
                    <div className="text-sm text-gray-400">
                      {transaction.date.split(", ")[1]}
                    </div>
                  </div>
                </div>
                <div className="font-medium text-lg">{transaction.amount}</div>
              </div>
            ))}
          </div>
        </div>

        {/* Yesterday */}
        <div className="mb-6">
          <div className="flex justify-between items-center mb-2">
            <h2 className="text-xl font-semibold">Yesterday</h2>
            <span className="text-lg font-medium">
              {yesterdayTotal.toFixed(2).replace(".", ",")} €
            </span>
          </div>

          <div className="bg-gray-900 rounded-lg overflow-hidden">
            {yesterdayTransactions.map((transaction) => (
              <div
                key={transaction.id}
                className="p-4 flex items-center justify-between border-b border-gray-800 last:border-b-0 cursor-pointer"
                onClick={() => handleTransactionClick(transaction)}
              >
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
                    <div className="font-medium text-lg">
                      {transaction.merchant}
                    </div>
                    <div className="text-sm text-gray-400">
                      {transaction.date.split(", ")[1]}
                    </div>
                  </div>
                </div>
                <div className="font-medium text-lg">{transaction.amount}</div>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Home indicator */}
      <div className="flex justify-center pb-2 pt-1">
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
