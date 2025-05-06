"use client";

import { useState, useEffect } from "react";
import {
  X,
  SplitSquareVertical,
  ChevronRight,
  Download,
  Clock,
} from "lucide-react";
import { Switch } from "@/components/ui/switch";
import Link from "next/link";
import Image from "next/image";

interface TransactionDetailsSheetProps {
  isOpen: boolean;
  onClose: () => void;
  transaction: {
    id: string;
    amount: string;
    merchant: string;
    date: string;
    location?: string;
    status?: string;
    statusDate?: string;
    card?: string;
    points?: string;
    category?: string;
    icon?: string;
    logoUrl?: string;
  };
}

export function TransactionDetailsSheet({
  isOpen,
  onClose,
  transaction,
}: TransactionDetailsSheetProps) {
  const [isVisible, setIsVisible] = useState(false);

  useEffect(() => {
    if (isOpen) {
      setIsVisible(true);
    } else {
      const timer = setTimeout(() => {
        setIsVisible(false);
      }, 300);
      return () => clearTimeout(timer);
    }
  }, [isOpen]);

  if (!isVisible) return null;

  return (
    <div
      className="fixed inset-0 z-50 bg-black/50 transition-opacity duration-300"
      style={{ opacity: isOpen ? 1 : 0 }}
    >
      <div
        className="fixed inset-x-0 bottom-0 z-50 rounded-t-3xl bg-gray-900 transition-transform duration-300 ease-out"
        style={{ transform: isOpen ? "translateY(0)" : "translateY(100%)" }}
      >
        <div className="flex flex-col max-h-[90vh] overflow-auto">
          <div className="sticky top-0 bg-gray-900 pt-4 px-4 z-10">
            <button onClick={onClose} className="p-2 -ml-2">
              <X className="h-6 w-6" />
            </button>
          </div>

          <div className="px-4 pb-8">
            <div className="flex justify-between items-start mb-2">
              <div>
                <h1 className="text-5xl font-bold mb-1">
                  {transaction.amount}
                </h1>
                <h2 className="text-2xl text-blue-400 mb-1">
                  {transaction.merchant}
                </h2>
                <p className="text-gray-400">{transaction.date}</p>
              </div>
              <div className="h-16 w-16 rounded-full bg-red-600 flex items-center justify-center overflow-hidden">
                {transaction.logoUrl ? (
                  <Image
                    src={transaction.logoUrl || "/placeholder.svg"}
                    alt={transaction.merchant}
                    width={40}
                    height={40}
                    className="object-contain"
                  />
                ) : (
                  <div className="text-yellow-400 text-3xl font-bold">M</div>
                )}
              </div>
            </div>

            <button className="flex items-center justify-center gap-2 w-full py-3 px-4 bg-gray-800 rounded-full mb-6">
              <SplitSquareVertical className="h-4 w-4" />
              <span>Split bill</span>
            </button>

            {/* Map */}
            {transaction.location && (
              <div className="rounded-lg overflow-hidden mb-4">
                <div className="relative h-48 w-full">
                  <Image
                    src="/map.png"
                    alt="Map location"
                    fill
                    className="object-cover"
                  />
                  <div className="absolute bottom-4 left-4 flex items-center">
                    <div className="flex items-center bg-black/30 px-2 py-1 rounded">
                      <Image
                        src="/map.png"
                        alt="Apple Maps"
                        width={60}
                        height={20}
                      />
                      <span className="text-xs text-white/70 ml-2">Legal</span>
                    </div>
                  </div>
                </div>
                <div className="bg-gray-800 p-4 flex justify-between items-center">
                  <span>{transaction.location}</span>
                  <ChevronRight className="h-5 w-5 text-gray-400" />
                </div>
              </div>
            )}

            {/* Status */}
            {transaction.status && (
              <div className="bg-gray-800 rounded-lg p-4 mb-4">
                <h3 className="text-gray-400 mb-2">Status</h3>
                <div className="flex items-start">
                  <p className="text-white">
                    <span className="font-medium">
                      {transaction.status} • Will be automatically reverted on{" "}
                      {transaction.statusDate} if unclaimed by merchant.{" "}
                    </span>
                    <Link href="#" className="text-blue-400">
                      Learn more
                    </Link>
                  </p>
                </div>
              </div>
            )}

            {/* Card */}
            {transaction.card && (
              <div className="bg-gray-800 rounded-lg p-4 mb-4 flex justify-between items-center">
                <h3 className="text-gray-400">Card</h3>
                <div className="flex items-center text-blue-400">
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
                    className="mr-2"
                  >
                    <rect width="20" height="14" x="2" y="5" rx="2" />
                    <line x1="2" x2="22" y1="10" y2="10" />
                  </svg>
                  <span>{transaction.card}</span>
                </div>
              </div>
            )}

            {/* Statement */}
            <div className="bg-gray-800 rounded-lg p-4 mb-4 flex justify-between items-center">
              <h3 className="text-gray-400">Statement</h3>
              <div className="flex items-center text-blue-400">
                <Download className="h-5 w-5 mr-2" />
                <span>Download</span>
              </div>
            </div>

            {/* Points earned */}
            {transaction.points && (
              <div className="bg-gray-800 rounded-lg p-4 mb-4 flex justify-between items-center">
                <h3 className="text-gray-400">Points earned</h3>
                <div className="flex items-center text-blue-400">
                  <Clock className="h-5 w-5 mr-2" />
                  <span>{transaction.points}</span>
                </div>
              </div>
            )}

            {/* Exclude from analytics */}
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-gray-400">Exclude from analytics</h3>
              <Switch />
            </div>

            {/* Category */}
            {transaction.category && (
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
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
