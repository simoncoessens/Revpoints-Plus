"use client";
import {
  Search,
  Menu,
  Plus,
  MoreHorizontal,
  Info,
  Coins,
  Diamond,
  ChevronRight,
  Heart,
} from "lucide-react";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import Link from "next/link";
import Image from "next/image";

export default function RevPointsPage() {
  return (
    <div className="flex flex-col min-h-screen bg-black text-white overflow-hidden relative">
      {/* Background pattern - purple waves */}
      <div
        className="absolute inset-0 z-0 opacity-70"
        style={{
          backgroundImage: "url('/purple-wave-pattern.png')",
          backgroundSize: "cover",
          backgroundPosition: "center",
        }}
      />

      {/* Status bar - just for visual representation */}
      <div className="flex justify-between items-center p-4 relative z-10">
        <div className="text-lg font-semibold">14:23</div>
        <div className="flex items-center gap-1">
          <div className="h-3 w-3 rounded-full bg-white"></div>
          <div className="h-3 w-3 rounded-full bg-white"></div>
          <div className="h-3 w-3 rounded-full bg-white"></div>
          <div className="h-4 w-6 rounded-sm bg-yellow-400 ml-1 flex items-center justify-center text-[10px] text-black font-bold">
            70
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
          <Menu className="h-5 w-5" />
        </Button>
      </div>

      {/* Points section */}
      <div className="flex flex-col items-center justify-center mt-12 mb-6 relative z-10">
        <div className="text-gray-300 text-lg mb-2">Metal plan</div>
        <div className="flex items-center mb-1">
          <div className="h-8 w-8 bg-white rounded-md flex items-center justify-center mr-2">
            <Diamond className="h-5 w-5 text-black" />
          </div>
          <span className="text-6xl font-semibold">1.149</span>
        </div>

        <div className="flex items-center text-gray-300 text-sm mb-4">
          <span>1 point / 2 € spent</span>
          <Info className="h-4 w-4 ml-1" />
        </div>

        <Button
          variant="secondary"
          className="rounded-full bg-gray-700/70 text-white px-8"
        >
          Upgrade
        </Button>
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
          <span className="text-sm">Earn</span>
        </div>

        <div className="flex flex-col items-center">
          <Button
            variant="ghost"
            size="icon"
            className="h-14 w-14 rounded-full bg-gray-700/70 mb-2"
          >
            <Coins className="h-6 w-6" />
          </Button>
          <span className="text-sm">Redeem</span>
        </div>

        <div className="flex flex-col items-center">
          <Button
            variant="ghost"
            size="icon"
            className="h-14 w-14 rounded-full bg-gray-700/70 mb-2"
          >
            <Diamond className="h-6 w-6" />
          </Button>
          <span className="text-sm">Plan perks</span>
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

      {/* Uber Eats style content */}
      <div className="flex-1 mt-4 relative z-10 overflow-auto pb-20">
        <div className="bg-gray-900/90 rounded-t-3xl p-4">
          {/* Places you might like section */}
          <div className="mb-8">
            <div className="flex justify-between items-center mb-2">
              <h2 className="text-2xl font-bold">Places you might like</h2>
              <Button variant="ghost" size="sm" className="p-0">
                <ChevronRight className="h-6 w-6" />
              </Button>
            </div>
            <div className="text-sm text-gray-400 mb-4">Sponsored</div>

            <div className="flex gap-4 overflow-x-auto pb-4 -mx-4 px-4">
              {/* Restaurant Card 1 */}
              <div className="min-w-[280px] bg-gray-800 rounded-xl overflow-hidden">
                <div className="relative h-40 w-full">
                  <div className="absolute top-3 left-0 bg-red-600 text-white px-3 py-1 z-10 rounded-r-md text-sm font-medium">
                    Buy 1, Get 1 Free
                  </div>
                  <Image
                    src="https://dynamic-media-cdn.tripadvisor.com/media/photo-o/26/93/31/13/caption.jpg?w=900&h=500&s=1"
                    alt="La Uramakeria"
                    fill
                    className="object-cover"
                  />
                  <div className="absolute bottom-3 left-3 bg-black/70 px-3 py-1 rounded-md"></div>
                  <button className="absolute top-3 right-3 bg-white/20 p-1 rounded-full backdrop-blur-sm">
                    <Heart className="h-5 w-5 text-white" />
                  </button>
                </div>
                <div className="p-3">
                  <h3 className="text-lg font-semibold">La Uramakeria</h3>
                  <div className="flex flex-col gap-1">
                    <div className="text-sm text-gray-400">Restaurant</div>
                    <div className="font-medium">La Uramakeria</div>
                    <div className="text-sm text-gray-400">Fast Food</div>
                  </div>
                </div>
              </div>

              {/* Restaurant Card 2 */}
              <div className="min-w-[280px] bg-gray-800 rounded-xl overflow-hidden">
                <div className="relative h-40 w-full">
                  <div className="absolute top-3 left-0 bg-red-600 text-white px-3 py-1 z-10 rounded-r-md text-sm font-medium flex items-center gap-1">
                    <svg
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        d="M12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z"
                        fill="currentColor"
                      />
                      <path
                        d="M18 12C18 15.3137 15.3137 18 12 18C8.68629 18 6 15.3137 6 12C6 8.68629 8.68629 6 12 6C15.3137 6 18 8.68629 18 12Z"
                        stroke="currentColor"
                        strokeWidth="2"
                      />
                      <path
                        d="M14 6L16.5 2"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                      />
                      <path
                        d="M10 6L7.5 2"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                      />
                      <path
                        d="M18 10L22 8.5"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                      />
                      <path
                        d="M18 14L22 15.5"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                      />
                      <path
                        d="M14 18L16.5 22"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                      />
                      <path
                        d="M10 18L7.5 22"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                      />
                      <path
                        d="M6 14L2 15.5"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                      />
                      <path
                        d="M6 10L2 8.5"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                      />
                    </svg>
                    Top Offer • Buy 1, Get 1
                  </div>
                  <Image
                    src="https://dynamic-media-cdn.tripadvisor.com/media/photo-o/14/8b/0d/25/20180909-181918-largejpg.jpg?w=1200&h=-1&s=1"
                    alt="ALOHA"
                    fill
                    className="object-cover"
                  />
                  <button className="absolute top-3 right-3 bg-white/20 p-1 rounded-full backdrop-blur-sm">
                    <Heart className="h-5 w-5 text-white" />
                  </button>
                </div>
                <div className="p-3">
                  <h3 className="text-lg font-semibold">ALOHA</h3>
                  <div className="flex flex-col gap-1">
                    <div className="text-sm text-gray-400">Restaurant</div>
                    <div className="font-medium">ALOHA</div>
                    <div className="text-sm text-gray-400">Fast Food</div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Stores near you section */}
          <div className="mb-8">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl font-bold">Stores near you</h2>
              <Button variant="ghost" size="sm" className="p-0">
                <ChevronRight className="h-6 w-6" />
              </Button>
            </div>

            <div className="flex gap-4 overflow-x-auto pb-4 -mx-4 px-4">
              {/* Store 1 */}
              <div className="flex flex-col items-center min-w-[80px]">
                <div className="h-12 w-12 rounded-full bg-orange-500 flex items-center justify-center">
                  <div className="text-yellow-400 text-xl font-bold">M</div>
                </div>
                <div className="text-sm mt-2">Mercadona</div>
              </div>

              {/* Store 2 */}
              <div className="flex flex-col items-center min-w-[80px]">
                <div className="h-12 w-12 rounded-full bg-orange-500 flex items-center justify-center">
                  <div className="text-yellow-400 text-xl font-bold">N</div>
                </div>
                <div className="text-sm mt-2">Naturalia</div>
              </div>

              {/* Store 3 */}
              <div className="flex flex-col items-center min-w-[80px]">
                <div className="h-12 w-12 rounded-full bg-orange-500 flex items-center justify-center">
                  <div className="text-yellow-400 text-xl font-bold">D</div>
                </div>
                <div className="text-sm mt-2">Decathlon</div>
              </div>

              {/* Store 4 */}
              <div className="flex flex-col items-center min-w-[80px]">
                <div className="h-12 w-12 rounded-full bg-orange-500 flex items-center justify-center">
                  <div className="text-yellow-400 text-xl font-bold">S</div>
                </div>
                <div className="text-sm mt-2">Subway</div>
              </div>

              {/* Store 5 */}
              <div className="flex flex-col items-center min-w-[80px]">
                <div className="h-12 w-12 rounded-full bg-orange-500 flex items-center justify-center">
                  <div className="text-yellow-400 text-xl font-bold">H</div>
                </div>
                <div className="text-sm mt-2">Honest Greens</div>
              </div>
            </div>
          </div>

          {/* Order again section */}
          <div className="mb-8">
            <div className="flex justify-between items-center mb-4">
              <h2 className="text-2xl font-bold">Order again</h2>
              <Button variant="ghost" size="sm" className="p-0">
                <ChevronRight className="h-6 w-6" />
              </Button>
            </div>

            <div className="flex gap-4 overflow-x-auto pb-4 -mx-4 px-4">
              {/* Order 1 */}
              <div className="min-w-[280px] bg-gray-800 rounded-xl overflow-hidden">
                <div className="relative h-40 w-full">
                  <Image
                    src="https://upload.wikimedia.org/wikipedia/fr/thumb/e/ea/Mcdonalds_France_2009_logo.svg/1200px-Mcdonalds_France_2009_logo.svg.png"
                    alt="Previous order"
                    fill
                    className="object-cover"
                  />
                </div>
                <div className="p-3">
                  <h3 className="text-lg font-semibold">McDonald's</h3>
                  <div className="flex flex-col gap-1">
                    <div className="text-sm text-gray-400">Restaurant</div>
                    <div className="font-medium">McDonald's</div>
                    <div className="text-sm text-gray-400">Fast Food</div>
                  </div>
                </div>
              </div>

              {/* Order 2 */}
              <div className="min-w-[280px] bg-gray-800 rounded-xl overflow-hidden">
                <div className="relative h-40 w-full">
                  <div className="absolute top-3 left-0 bg-red-600 text-white px-3 py-1 z-10 rounded-r-md text-sm font-medium flex items-center gap-1">
                    <svg
                      width="16"
                      height="16"
                      viewBox="0 0 24 24"
                      fill="none"
                      xmlns="http://www.w3.org/2000/svg"
                    >
                      <path
                        d="M12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z"
                        fill="currentColor"
                      />
                      <path
                        d="M18 12C18 15.3137 15.3137 18 12 18C8.68629 18 6 15.3137 6 12C6 8.68629 8.68629 6 12 6C15.3137 6 18 8.68629 18 12Z"
                        stroke="currentColor"
                        strokeWidth="2"
                      />
                      <path
                        d="M14 6L16.5 2"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                      />
                      <path
                        d="M10 6L7.5 2"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                      />
                      <path
                        d="M18 10L22 8.5"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                      />
                      <path
                        d="M18 14L22 15.5"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                      />
                      <path
                        d="M14 18L16.5 22"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                      />
                      <path
                        d="M10 18L7.5 22"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                      />
                      <path
                        d="M6 14L2 15.5"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                      />
                      <path
                        d="M6 10L2 8.5"
                        stroke="currentColor"
                        strokeWidth="2"
                        strokeLinecap="round"
                      />
                    </svg>
                    Top Offer • Buy 1, Get 1
                  </div>
                  <Image
                    src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQpMepwXGrRyxdKVwoiHE4K7-A0NSG8Ru9KOg&s"
                    alt="Previous order"
                    fill
                    className="object-cover"
                  />
                </div>
                <div className="p-3">
                  <h3 className="text-lg font-semibold">La Salumeria</h3>
                  <div className="flex flex-col gap-1">
                    <div className="text-sm text-gray-400">Restaurant</div>
                    <div className="text-sm text-gray-400">Local food</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom navigation */}
      <div className="fixed bottom-0 left-0 right-0 bg-gray-900 border-t border-gray-800 p-4 flex justify-between items-center z-20">
        <Link href="/" className="flex flex-col items-center text-gray-500">
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
          <span className="text-xs mt-1">Home</span>
        </Link>

        <Link href="#" className="flex flex-col items-center text-gray-500">
          <svg
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6"
          >
            <path
              d="M23 6L13.5 15.5L8.5 10.5L1 18"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M17 6H23V12"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <span className="text-xs mt-1">Invest</span>
        </Link>

        <Link href="#" className="flex flex-col items-center text-gray-500">
          <svg
            viewBox="0 0 24 24"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
            className="h-6 w-6"
          >
            <path
              d="M17 1L21 5L17 9"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M3 11V9C3 7.93913 3.42143 6.92172 4.17157 6.17157C4.92172 5.42143 5.93913 5 7 5H21"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M7 23L3 19L7 15"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
            <path
              d="M21 13V15C21 16.0609 20.5786 17.0783 19.8284 17.8284C19.0783 18.5786 18.0609 19 17 19H3"
              stroke="currentColor"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
          <span className="text-xs mt-1">Payments</span>
        </Link>

        <Link href="#" className="flex flex-col items-center text-gray-500">
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
        </Link>

        <div className="flex flex-col items-center text-white">
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
        </div>
      </div>

      {/* Home indicator */}
      <div className="flex justify-center pb-2 pt-1 bg-gray-900">
        <div className="w-32 h-1 bg-white rounded-full"></div>
      </div>
    </div>
  );
}
