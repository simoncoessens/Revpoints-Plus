"use client"

import { useState } from "react"
import {
  ArrowLeft,
  Calendar,
  Clock,
  Coffee,
  Download,
  TrendingUp,
  Users,
  Utensils,
  Wine,
  Beer,
  CreditCard,
  Wallet,
  ArrowRightLeft,
} from "lucide-react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Tabs, TabsList, TabsTrigger } from "@/components/ui/tabs"
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select"
import Link from "next/link"
import { ChartContainer } from "@/components/ui/chart"
import {
  AreaChart,
  Area,
  BarChart,
  Bar,
  PieChart,
  Pie,
  Cell,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts"
import { BarChart3 } from "lucide-react"

// Sample data for the charts
const salesData = [
  { name: "Mon", sales: 1200 },
  { name: "Tue", sales: 980 },
  { name: "Wed", sales: 1400 },
  { name: "Thu", sales: 1800 },
  { name: "Fri", sales: 2400 },
  { name: "Sat", sales: 2800 },
  { name: "Sun", sales: 1900 },
]

const monthlyData = [
  { name: "Jan", sales: 28000 },
  { name: "Feb", sales: 25000 },
  { name: "Mar", sales: 32000 },
  { name: "Apr", sales: 34000 },
  { name: "May", sales: 39000 },
  { name: "Jun", sales: 42000 },
  { name: "Jul", sales: 48000 },
  { name: "Aug", sales: 51000 },
  { name: "Sep", sales: 47000 },
  { name: "Oct", sales: 43000 },
  { name: "Nov", sales: 38000 },
  { name: "Dec", sales: 45000 },
]

const productData = [
  { name: "Beer", value: 45, color: "#4ade80" },
  { name: "Coffee", value: 20, color: "#f97316" },
  { name: "Food", value: 25, color: "#3b82f6" },
  { name: "Wine", value: 10, color: "#ec4899" },
]

const hourlyData = [
  { hour: "8-10", customers: 15, sales: 120 },
  { hour: "10-12", customers: 25, sales: 250 },
  { hour: "12-14", customers: 65, sales: 780 },
  { hour: "14-16", customers: 35, sales: 420 },
  { hour: "16-18", customers: 40, sales: 480 },
  { hour: "18-20", customers: 75, sales: 900 },
  { hour: "20-22", customers: 90, sales: 1350 },
  { hour: "22-00", customers: 60, sales: 900 },
]

const topProducts = [
  { id: 1, name: "Estrella Damm", category: "Beer", sales: 450, profit: 675 },
  { id: 2, name: "Café con Leche", category: "Coffee", sales: 320, profit: 480 },
  { id: 3, name: "Bocadillo Jamón", category: "Food", sales: 280, profit: 560 },
  { id: 4, name: "Patatas Bravas", category: "Food", sales: 250, profit: 375 },
  { id: 5, name: "Voll Damm", category: "Beer", sales: 220, profit: 330 },
]

const paymentMethods = [
  { name: "Card", value: 65, color: "#3b82f6" },
  { name: "Cash", value: 25, color: "#22c55e" },
  { name: "Mobile", value: 10, color: "#f97316" },
]

export default function AnalyticsPage() {
  const [timeframe, setTimeframe] = useState("week")

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
            <h1 className="text-2xl font-bold">Analytics</h1>
            <p className="text-gray-400 text-sm">Bar de La FIB</p>
          </div>
        </div>
        <Button variant="outline" size="icon" className="rounded-full">
          <Download className="h-4 w-4" />
        </Button>
      </div>

      {/* Time period selector */}
      <div className="px-4 py-2">
        <Select value={timeframe} onValueChange={setTimeframe}>
          <SelectTrigger className="w-full bg-gray-800 border-0">
            <SelectValue placeholder="Select timeframe" />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value="day">Today</SelectItem>
            <SelectItem value="week">This Week</SelectItem>
            <SelectItem value="month">This Month</SelectItem>
            <SelectItem value="year">This Year</SelectItem>
          </SelectContent>
        </Select>
      </div>

      {/* Summary cards */}
      <div className="px-4 py-2 grid grid-cols-2 gap-4">
        <Card className="bg-gray-800 border-0">
          <CardHeader className="pb-2">
            <CardDescription>Total Sales</CardDescription>
            <CardTitle className="text-xl">€11,580</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-xs text-green-400 flex items-center">
              <TrendingUp className="h-3 w-3 mr-1" />
              +12.5% from last week
            </div>
          </CardContent>
        </Card>
        <Card className="bg-gray-800 border-0">
          <CardHeader className="pb-2">
            <CardDescription>Customers</CardDescription>
            <CardTitle className="text-xl">842</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-xs text-green-400 flex items-center">
              <TrendingUp className="h-3 w-3 mr-1" />
              +8.2% from last week
            </div>
          </CardContent>
        </Card>
        <Card className="bg-gray-800 border-0">
          <CardHeader className="pb-2">
            <CardDescription>Avg. Order Value</CardDescription>
            <CardTitle className="text-xl">€13.75</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-xs text-green-400 flex items-center">
              <TrendingUp className="h-3 w-3 mr-1" />
              +2.1% from last week
            </div>
          </CardContent>
        </Card>
        <Card className="bg-gray-800 border-0">
          <CardHeader className="pb-2">
            <CardDescription>Profit Margin</CardDescription>
            <CardTitle className="text-xl">42%</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-xs text-green-400 flex items-center">
              <TrendingUp className="h-3 w-3 mr-1" />
              +1.5% from last week
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Sales over time chart */}
      <div className="px-4 py-4">
        <Card className="bg-gray-800 border-0">
          <CardHeader>
            <div className="flex justify-between items-center">
              <CardTitle>Sales Over Time</CardTitle>
              <Tabs defaultValue="week" className="w-[200px]">
                <TabsList className="grid w-full grid-cols-3 bg-gray-700">
                  <TabsTrigger value="week">Week</TabsTrigger>
                  <TabsTrigger value="month">Month</TabsTrigger>
                  <TabsTrigger value="year">Year</TabsTrigger>
                </TabsList>
              </Tabs>
            </div>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <ChartContainer
                config={{
                  sales: {
                    label: "Sales",
                    color: "#3b82f6",
                  },
                }}
              >
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart
                    data={timeframe === "year" ? monthlyData : salesData}
                    margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
                  >
                    <defs>
                      <linearGradient id="colorSales" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.8} />
                        <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                      </linearGradient>
                    </defs>
                    <XAxis dataKey="name" stroke="#888888" fontSize={12} tickLine={false} axisLine={false} />
                    <YAxis
                      stroke="#888888"
                      fontSize={12}
                      tickLine={false}
                      axisLine={false}
                      tickFormatter={(value) => `€${value}`}
                    />
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#444444" />
                    <Tooltip
                      content={({ active, payload }) => {
                        if (active && payload && payload.length) {
                          return (
                            <div className="rounded-lg border bg-background p-2 shadow-sm">
                              <div className="grid grid-cols-2 gap-2">
                                <div className="flex flex-col">
                                  <span className="text-[0.70rem] uppercase text-muted-foreground">Date</span>
                                  <span className="font-bold text-muted-foreground">{payload[0].payload.name}</span>
                                </div>
                                <div className="flex flex-col">
                                  <span className="text-[0.70rem] uppercase text-muted-foreground">Sales</span>
                                  <span className="font-bold">€{payload[0].value}</span>
                                </div>
                              </div>
                            </div>
                          )
                        }
                        return null
                      }}
                    />
                    <Area type="monotone" dataKey="sales" stroke="#3b82f6" fillOpacity={1} fill="url(#colorSales)" />
                  </AreaChart>
                </ResponsiveContainer>
              </ChartContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Product breakdown */}
      <div className="px-4 py-2 grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card className="bg-gray-800 border-0">
          <CardHeader>
            <CardTitle>Product Categories</CardTitle>
            <CardDescription>Sales by product type</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px] flex items-center justify-center">
              <ChartContainer
                config={{
                  beer: {
                    label: "Beer",
                    color: "#4ade80",
                  },
                  coffee: {
                    label: "Coffee",
                    color: "#f97316",
                  },
                  food: {
                    label: "Food",
                    color: "#3b82f6",
                  },
                  wine: {
                    label: "Wine",
                    color: "#ec4899",
                  },
                }}
              >
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={productData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    >
                      {productData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value) => [`${value}%`, "Percentage"]} />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </ChartContainer>
            </div>
          </CardContent>
        </Card>

        <Card className="bg-gray-800 border-0">
          <CardHeader>
            <CardTitle>Payment Methods</CardTitle>
            <CardDescription>How customers pay</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px] flex items-center justify-center">
              <ChartContainer
                config={{
                  card: {
                    label: "Card",
                    color: "#3b82f6",
                  },
                  cash: {
                    label: "Cash",
                    color: "#22c55e",
                  },
                  mobile: {
                    label: "Mobile",
                    color: "#f97316",
                  },
                }}
              >
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={paymentMethods}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      outerRadius={80}
                      fill="#8884d8"
                      dataKey="value"
                      label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
                    >
                      {paymentMethods.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value) => [`${value}%`, "Percentage"]} />
                    <Legend />
                  </PieChart>
                </ResponsiveContainer>
              </ChartContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Hourly traffic */}
      <div className="px-4 py-4">
        <Card className="bg-gray-800 border-0">
          <CardHeader>
            <CardTitle>Hourly Traffic</CardTitle>
            <CardDescription>Customer traffic and sales by hour</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="h-[300px]">
              <ChartContainer
                config={{
                  customers: {
                    label: "Customers",
                    color: "#3b82f6",
                  },
                  sales: {
                    label: "Sales (€)",
                    color: "#4ade80",
                  },
                }}
              >
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={hourlyData} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#444444" />
                    <XAxis dataKey="hour" stroke="#888888" />
                    <YAxis yAxisId="left" orientation="left" stroke="#3b82f6" />
                    <YAxis yAxisId="right" orientation="right" stroke="#4ade80" />
                    <Tooltip
                      content={({ active, payload }) => {
                        if (active && payload && payload.length) {
                          return (
                            <div className="rounded-lg border bg-background p-2 shadow-sm">
                              <div className="grid grid-cols-3 gap-2">
                                <div className="flex flex-col">
                                  <span className="text-[0.70rem] uppercase text-muted-foreground">Time</span>
                                  <span className="font-bold text-muted-foreground">{payload[0].payload.hour}</span>
                                </div>
                                <div className="flex flex-col">
                                  <span className="text-[0.70rem] uppercase text-muted-foreground">Customers</span>
                                  <span className="font-bold text-blue-400">{payload[0].value}</span>
                                </div>
                                <div className="flex flex-col">
                                  <span className="text-[0.70rem] uppercase text-muted-foreground">Sales</span>
                                  <span className="font-bold text-green-400">€{payload[1].value}</span>
                                </div>
                              </div>
                            </div>
                          )
                        }
                        return null
                      }}
                    />
                    <Legend />
                    <Bar yAxisId="left" dataKey="customers" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                    <Bar yAxisId="right" dataKey="sales" fill="#4ade80" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </ChartContainer>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Top selling products */}
      <div className="px-4 py-2">
        <Card className="bg-gray-800 border-0">
          <CardHeader>
            <CardTitle>Top Selling Products</CardTitle>
            <CardDescription>Best performing items</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {topProducts.map((product) => (
                <div key={product.id} className="flex items-center justify-between">
                  <div className="flex items-center">
                    <div className="mr-4">
                      {product.category === "Beer" && <Beer className="h-8 w-8 text-green-400" />}
                      {product.category === "Coffee" && <Coffee className="h-8 w-8 text-orange-400" />}
                      {product.category === "Food" && <Utensils className="h-8 w-8 text-blue-400" />}
                      {product.category === "Wine" && <Wine className="h-8 w-8 text-pink-400" />}
                    </div>
                    <div>
                      <div className="font-medium">{product.name}</div>
                      <div className="text-sm text-gray-400">{product.category}</div>
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="font-medium">{product.sales} units</div>
                    <div className="text-sm text-green-400">€{product.profit}</div>
                  </div>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Business insights */}
      <div className="px-4 py-4 mb-20">
        <Card className="bg-gray-800 border-0">
          <CardHeader>
            <CardTitle>Business Insights</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div className="flex items-center">
                <div className="bg-blue-500/20 p-2 rounded-full mr-4">
                  <Clock className="h-5 w-5 text-blue-400" />
                </div>
                <div>
                  <div className="font-medium">Peak Hours</div>
                  <div className="text-sm text-gray-400">Your busiest time is between 8PM and 10PM</div>
                </div>
              </div>

              <div className="flex items-center">
                <div className="bg-green-500/20 p-2 rounded-full mr-4">
                  <Calendar className="h-5 w-5 text-green-400" />
                </div>
                <div>
                  <div className="font-medium">Best Day</div>
                  <div className="text-sm text-gray-400">Friday generates 30% of your weekly revenue</div>
                </div>
              </div>

              <div className="flex items-center">
                <div className="bg-orange-500/20 p-2 rounded-full mr-4">
                  <Users className="h-5 w-5 text-orange-400" />
                </div>
                <div>
                  <div className="font-medium">Customer Retention</div>
                  <div className="text-sm text-gray-400">65% of customers are returning visitors</div>
                </div>
              </div>

              <div className="flex items-center">
                <div className="bg-pink-500/20 p-2 rounded-full mr-4">
                  <CreditCard className="h-5 w-5 text-pink-400" />
                </div>
                <div>
                  <div className="font-medium">Payment Preference</div>
                  <div className="text-sm text-gray-400">Card payments have increased by 15% this month</div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Bottom navigation placeholder */}
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

        <div className="flex flex-col items-center text-white">
          <BarChart3 className="h-6 w-6" />
          <span className="text-xs mt-1">Analytics</span>
        </div>

        <div className="flex flex-col items-center text-gray-500">
          <ArrowRightLeft className="h-6 w-6" />
          <span className="text-xs mt-1">Payments</span>
        </div>

        <div className="flex flex-col items-center text-gray-500">
          <Wallet className="h-6 w-6" />
          <span className="text-xs mt-1">Business</span>
        </div>

        <div className="flex flex-col items-center text-gray-500">
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
        </div>
      </div>

      {/* Home indicator */}
      <div className="fixed bottom-0 left-0 right-0 flex justify-center pb-2 pt-1 bg-gray-900">
        <div className="w-32 h-1 bg-white rounded-full"></div>
      </div>
    </div>
  )
}
