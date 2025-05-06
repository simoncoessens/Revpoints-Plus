"use client"

import type React from "react"

import { useState } from "react"
import { ArrowLeft, BarChart3, Menu, Megaphone, Upload, Bot, ArrowRightLeft } from "lucide-react"
import { Button } from "@/components/ui/button"
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card"
import { Badge } from "@/components/ui/badge"
import { Progress } from "@/components/ui/progress"
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs"
import Link from "next/link"

export default function CampaignsPage() {
  const [uploadedMenu, setUploadedMenu] = useState<File | null>(null)
  const [showProposal, setShowProposal] = useState(false)

  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setUploadedMenu(e.target.files[0])
    }
  }

  const generateCampaign = () => {
    // In a real app, this would send the menu to an AI service
    setShowProposal(true)
  }

  return (
    <div className="flex flex-col min-h-screen bg-black text-white">
      {/* Status bar - just for visual representation */}
      <div className="flex justify-between items-center p-4">
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
      <div className="px-4 py-2 flex items-center justify-between">
        <div className="flex items-center">
          <Link href="/" className="mr-4">
            <ArrowLeft className="h-6 w-6" />
          </Link>
          <div>
            <h1 className="text-2xl font-bold">RevPoint Campaigns</h1>
            <p className="text-gray-400 text-sm">Bar de La FIB</p>
          </div>
        </div>
        <Button variant="ghost" size="icon" className="rounded-full bg-gray-700/70">
          <Menu className="h-5 w-5" />
        </Button>
      </div>

      {/* Tabs */}
      <div className="px-4 py-2">
        <Tabs defaultValue="active" className="w-full">
          <TabsList className="grid w-full grid-cols-2 bg-gray-800">
            <TabsTrigger value="active">Active Campaigns</TabsTrigger>
            <TabsTrigger value="create">Create Campaign</TabsTrigger>
          </TabsList>

          <TabsContent value="active" className="mt-4 space-y-4">
            {/* Active Campaign Card */}
            <Card className="bg-gray-800 border-0">
              <CardHeader className="pb-2">
                <div className="flex justify-between items-start">
                  <div>
                    <CardTitle className="text-xl">Happy Hour Special</CardTitle>
                    <CardDescription>Exclusive RevPoint discount</CardDescription>
                  </div>
                  <Badge className="bg-purple-600">Active</Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-400">Campaign period:</span>
                  <span className="font-medium">May 5 - June 5</span>
                </div>

                <div className="space-y-1">
                  <div className="flex justify-between text-sm">
                    <span>Campaign usage</span>
                    <span>45/100</span>
                  </div>
                  <Progress value={45} className="h-2" />
                </div>

                <div className="bg-gray-700/50 rounded-lg p-4">
                  <h3 className="font-medium mb-2">Offer Details</h3>
                  <p className="text-sm text-gray-300">
                    Customers get 2-for-1 on all draft beers when they pay with RevPoints between 4-7pm, Monday to
                    Thursday.
                  </p>
                </div>

                <div className="flex items-center gap-2">
                  <div className="h-10 w-10 rounded-full bg-purple-600 flex items-center justify-center">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path
                        d="M12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z"
                        fill="currentColor"
                      />
                      <path
                        d="M18 12C18 15.3137 15.3137 18 12 18C8.68629 18 6 15.3137 6 12C6 8.68629 8.68629 6 12 6C15.3137 6 18 8.68629 18 12Z"
                        stroke="currentColor"
                        strokeWidth="2"
                      />
                      <path d="M14 6L16.5 2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                      <path d="M10 6L7.5 2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                      <path d="M18 10L22 8.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                      <path d="M18 14L22 15.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                      <path d="M14 18L16.5 22" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                      <path d="M10 18L7.5 22" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                      <path d="M6 14L2 15.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                      <path d="M6 10L2 8.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                    </svg>
                  </div>
                  <div>
                    <p className="text-sm font-medium">RevPoints Exclusive</p>
                    <p className="text-xs text-gray-400">100 points minimum spend</p>
                  </div>
                </div>
              </CardContent>
              <CardFooter>
                <Button variant="outline" className="w-full">
                  View Details
                </Button>
              </CardFooter>
            </Card>

            {/* Second Campaign Card */}
            <Card className="bg-gray-800 border-0">
              <CardHeader className="pb-2">
                <div className="flex justify-between items-start">
                  <div>
                    <CardTitle className="text-xl">Student Discount</CardTitle>
                    <CardDescription>RevPoint rewards for students</CardDescription>
                  </div>
                  <Badge className="bg-purple-600">Active</Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center justify-between">
                  <span className="text-sm text-gray-400">Campaign period:</span>
                  <span className="font-medium">May 1 - July 31</span>
                </div>

                <div className="space-y-1">
                  <div className="flex justify-between text-sm">
                    <span>Campaign usage</span>
                    <span>78/200</span>
                  </div>
                  <Progress value={39} className="h-2" />
                </div>

                <div className="bg-gray-700/50 rounded-lg p-4">
                  <h3 className="font-medium mb-2">Offer Details</h3>
                  <p className="text-sm text-gray-300">
                    Students get 15% off their total bill when paying with RevPoints. Valid any day with student ID.
                  </p>
                </div>

                <div className="flex items-center gap-2">
                  <div className="h-10 w-10 rounded-full bg-purple-600 flex items-center justify-center">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <path
                        d="M12 15C13.6569 15 15 13.6569 15 12C15 10.3431 13.6569 9 12 9C10.3431 9 9 10.3431 9 12C9 13.6569 10.3431 15 12 15Z"
                        fill="currentColor"
                      />
                      <path
                        d="M18 12C18 15.3137 15.3137 18 12 18C8.68629 18 6 15.3137 6 12C6 8.68629 8.68629 6 12 6C15.3137 6 18 8.68629 18 12Z"
                        stroke="currentColor"
                        strokeWidth="2"
                      />
                      <path d="M14 6L16.5 2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                      <path d="M10 6L7.5 2" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                      <path d="M18 10L22 8.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                      <path d="M18 14L22 15.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                      <path d="M14 18L16.5 22" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                      <path d="M10 18L7.5 22" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                      <path d="M6 14L2 15.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                      <path d="M6 10L2 8.5" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
                    </svg>
                  </div>
                  <div>
                    <p className="text-sm font-medium">RevPoints Exclusive</p>
                    <p className="text-xs text-gray-400">50 points minimum spend</p>
                  </div>
                </div>
              </CardContent>
              <CardFooter>
                <Button variant="outline" className="w-full">
                  View Details
                </Button>
              </CardFooter>
            </Card>
          </TabsContent>

          <TabsContent value="create" className="mt-4 space-y-6">
            <Card className="bg-gray-800 border-0">
              <CardHeader>
                <CardTitle className="flex items-center gap-2">
                  <Bot className="h-5 w-5 text-purple-400" />
                  Campaign AI Assistant
                </CardTitle>
                <CardDescription>
                  Upload your menu and our AI will suggest the perfect RevPoint campaign for your business
                </CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {!uploadedMenu ? (
                  <div className="border-2 border-dashed border-gray-600 rounded-lg p-6 text-center">
                    <Upload className="h-10 w-10 mx-auto mb-4 text-gray-400" />
                    <p className="mb-2 text-sm text-gray-300">Upload your bar menu to get started</p>
                    <p className="text-xs text-gray-400 mb-4">PDF, JPG or PNG (max 10MB)</p>
                    <div className="relative">
                      <input
                        type="file"
                        className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                        onChange={handleFileUpload}
                        accept=".pdf,.jpg,.jpeg,.png"
                      />
                      <Button variant="outline" className="w-full">
                        Select File
                      </Button>
                    </div>
                  </div>
                ) : (
                  <div className="space-y-4">
                    <div className="flex items-center justify-between bg-gray-700/50 p-3 rounded-lg">
                      <div className="flex items-center gap-2">
                        <div className="bg-purple-600/20 p-2 rounded-md">
                          <svg
                            width="20"
                            height="20"
                            viewBox="0 0 24 24"
                            fill="none"
                            xmlns="http://www.w3.org/2000/svg"
                          >
                            <path
                              d="M14 2H6C5.46957 2 4.96086 2.21071 4.58579 2.58579C4.21071 2.96086 4 3.46957 4 4V20C4 20.5304 4.21071 21.0391 4.58579 21.4142C4.96086 21.7893 5.46957 22 6 22H18C18.5304 22 19.0391 21.7893 19.4142 21.4142C19.7893 21.0391 20 20.5304 20 20V8L14 2Z"
                              stroke="currentColor"
                              strokeWidth="2"
                              strokeLinecap="round"
                              strokeLinejoin="round"
                            />
                            <path
                              d="M14 2V8H20"
                              stroke="currentColor"
                              strokeWidth="2"
                              strokeLinecap="round"
                              strokeLinejoin="round"
                            />
                          </svg>
                        </div>
                        <div>
                          <p className="text-sm font-medium">{uploadedMenu.name}</p>
                          <p className="text-xs text-gray-400">Menu uploaded successfully</p>
                        </div>
                      </div>
                      <Button
                        variant="ghost"
                        size="sm"
                        className="text-red-400 hover:text-red-300"
                        onClick={() => setUploadedMenu(null)}
                      >
                        Remove
                      </Button>
                    </div>

                    <Button className="w-full bg-purple-600 hover:bg-purple-700" onClick={generateCampaign}>
                      Generate Campaign Ideas
                    </Button>

                    {showProposal && (
                      <div className="mt-6 space-y-4">
                        <div className="bg-gray-700/50 p-4 rounded-lg">
                          <div className="flex items-center gap-2 mb-3">
                            <Bot className="h-5 w-5 text-purple-400" />
                            <h3 className="font-medium">AI Campaign Proposal</h3>
                          </div>

                          <div className="space-y-4">
                            <div className="bg-gray-800 p-3 rounded-md">
                              <h4 className="font-medium text-purple-400 mb-1">Tapas Tuesday</h4>
                              <p className="text-sm text-gray-300 mb-2">
                                Based on your menu, I recommend a "Tapas Tuesday" campaign where customers can get 3
                                tapas for the price of 2 when paying with RevPoints.
                              </p>
                              <div className="text-xs text-gray-400">
                                <p>• Target audience: Students and faculty looking for after-class snacks</p>
                                <p>• Recommended timing: Tuesdays 3-7pm</p>
                                <p>• RevPoints requirement: 75 points minimum</p>
                              </div>
                            </div>

                            <div className="bg-gray-800 p-3 rounded-md">
                              <h4 className="font-medium text-purple-400 mb-1">Weekend Beer Bundle</h4>
                              <p className="text-sm text-gray-300 mb-2">
                                Your beer selection is impressive! Create a "Weekend Beer Bundle" offering a flight of 4
                                craft beers at a 20% discount when paid with RevPoints.
                              </p>
                              <div className="text-xs text-gray-400">
                                <p>• Target audience: Weekend visitors and craft beer enthusiasts</p>
                                <p>• Recommended timing: Friday-Sunday</p>
                                <p>• RevPoints requirement: 120 points minimum</p>
                              </div>
                            </div>

                            <Button className="w-full">Use This Proposal</Button>
                          </div>
                        </div>
                      </div>
                    )}
                  </div>
                )}
              </CardContent>
            </Card>

            <Card className="bg-gray-800 border-0">
              <CardHeader>
                <CardTitle>Campaign Benefits</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div className="flex items-center gap-3">
                  <div className="h-10 w-10 rounded-full bg-purple-600/20 flex items-center justify-center">
                    <Megaphone className="h-5 w-5 text-purple-400" />
                  </div>
                  <div>
                    <p className="font-medium">Increased Visibility</p>
                    <p className="text-sm text-gray-400">Your business will be featured in the RevPoints app</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <div className="h-10 w-10 rounded-full bg-purple-600/20 flex items-center justify-center">
                    <Users className="h-5 w-5 text-purple-400" />
                  </div>
                  <div>
                    <p className="font-medium">New Customers</p>
                    <p className="text-sm text-gray-400">Attract RevPoints users looking for exclusive deals</p>
                  </div>
                </div>

                <div className="flex items-center gap-3">
                  <div className="h-10 w-10 rounded-full bg-purple-600/20 flex items-center justify-center">
                    <TrendingUp className="h-5 w-5 text-purple-400" />
                  </div>
                  <div>
                    <p className="font-medium">Higher Average Order</p>
                    <p className="text-sm text-gray-400">RevPoints users spend 22% more on average</p>
                  </div>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>

      {/* Bottom navigation */}
      <div className="fixed bottom-0 left-0 right-0 bg-gray-900 border-t border-gray-800 p-4 flex justify-between items-center">
        <Link href="/" className="flex flex-col items-center text-gray-500">
          <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" className="h-6 w-6">
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

        <Link href="/analytics" className="flex flex-col items-center text-gray-500">
          <BarChart3 className="h-6 w-6" />
          <span className="text-xs mt-1">Analytics</span>
        </Link>

        <div className="flex flex-col items-center text-gray-500">
          <ArrowRightLeft className="h-6 w-6" />
          <span className="text-xs mt-1">Payments</span>
        </div>

        <div className="flex flex-col items-center text-white">
          <Megaphone className="h-6 w-6" />
          <span className="text-xs mt-1">Campaigns</span>
        </div>

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
      <div className="fixed bottom-0 left-0 right-0 flex justify-center pb-2 pt-1 bg-gray-900">
        <div className="w-32 h-1 bg-white rounded-full"></div>
      </div>
    </div>
  )
}

function Users(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2" />
      <circle cx="9" cy="7" r="4" />
      <path d="M22 21v-2a4 4 0 0 0-3-3.87" />
      <path d="M16 3.13a4 4 0 0 1 0 7.75" />
    </svg>
  )
}

function TrendingUp(props: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      {...props}
      xmlns="http://www.w3.org/2000/svg"
      width="24"
      height="24"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <polyline points="22 7 13.5 15.5 8.5 10.5 2 17" />
      <polyline points="16 7 22 7 22 13" />
    </svg>
  )
}
