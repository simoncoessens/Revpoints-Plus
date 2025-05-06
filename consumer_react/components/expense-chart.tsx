"use client"

import { useEffect, useState } from "react"
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from "recharts"
import { Card } from "@/components/ui/card"

const data = [
  { name: "Jan", income: 3200, expenses: 1800, savings: 1400 },
  { name: "Feb", income: 3400, expenses: 2100, savings: 1300 },
  { name: "Mar", income: 3100, expenses: 1900, savings: 1200 },
  { name: "Apr", income: 3500, expenses: 2300, savings: 1200 },
  { name: "May", income: 3800, expenses: 2200, savings: 1600 },
  { name: "Jun", income: 4100, expenses: 2400, savings: 1700 },
  { name: "Jul", income: 4300, expenses: 2600, savings: 1700 },
  { name: "Aug", income: 4500, expenses: 2700, savings: 1800 },
  { name: "Sep", income: 4200, expenses: 2500, savings: 1700 },
  { name: "Oct", income: 4600, expenses: 2800, savings: 1800 },
  { name: "Nov", income: 4800, expenses: 2900, savings: 1900 },
  { name: "Dec", income: 4935, expenses: 2864, savings: 2071 },
]

export function ExpenseChart() {
  const [isMounted, setIsMounted] = useState(false)

  useEffect(() => {
    setIsMounted(true)
  }, [])

  if (!isMounted) {
    return (
      <Card className="w-full h-[350px] flex items-center justify-center">
        <p className="text-muted-foreground">Loading chart...</p>
      </Card>
    )
  }

  return (
    <ResponsiveContainer width="100%" height={350}>
      <LineChart
        data={data}
        margin={{
          top: 5,
          right: 30,
          left: 20,
          bottom: 5,
        }}
      >
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="name" />
        <YAxis />
        <Tooltip formatter={(value) => [`$${value}`, undefined]} labelFormatter={(label) => `Month: ${label}`} />
        <Legend />
        <Line type="monotone" dataKey="income" stroke="#4ade80" strokeWidth={2} activeDot={{ r: 8 }} name="Income" />
        <Line type="monotone" dataKey="expenses" stroke="#f43f5e" strokeWidth={2} name="Expenses" />
        <Line type="monotone" dataKey="savings" stroke="#3b82f6" strokeWidth={2} name="Savings" />
      </LineChart>
    </ResponsiveContainer>
  )
}
