import { ArrowDownIcon, ArrowUpIcon, CreditCard, DollarSign, Home, ShoppingBag, Utensils } from "lucide-react"

export function RecentTransactions() {
  const transactions = [
    {
      id: 1,
      description: "Grocery Shopping",
      amount: -120.5,
      date: "Today",
      icon: ShoppingBag,
      type: "expense",
    },
    {
      id: 2,
      description: "Salary Deposit",
      amount: 4935.25,
      date: "Yesterday",
      icon: DollarSign,
      type: "income",
    },
    {
      id: 3,
      description: "Restaurant Bill",
      amount: -85.3,
      date: "Yesterday",
      icon: Utensils,
      type: "expense",
    },
    {
      id: 4,
      description: "Rent Payment",
      amount: -1200.0,
      date: "May 1",
      icon: Home,
      type: "expense",
    },
    {
      id: 5,
      description: "Credit Card Payment",
      amount: -450.0,
      date: "Apr 29",
      icon: CreditCard,
      type: "expense",
    },
  ]

  return (
    <div className="space-y-4">
      {transactions.map((transaction) => (
        <div key={transaction.id} className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className={`p-2 rounded-full ${transaction.type === "income" ? "bg-green-100" : "bg-red-100"}`}>
              <transaction.icon
                className={`h-4 w-4 ${transaction.type === "income" ? "text-green-600" : "text-red-600"}`}
              />
            </div>
            <div>
              <p className="text-sm font-medium leading-none">{transaction.description}</p>
              <p className="text-xs text-muted-foreground">{transaction.date}</p>
            </div>
          </div>
          <div
            className={`font-medium ${
              transaction.type === "income" ? "text-green-600" : "text-red-600"
            } flex items-center`}
          >
            {transaction.type === "income" ? (
              <ArrowUpIcon className="h-4 w-4 mr-1" />
            ) : (
              <ArrowDownIcon className="h-4 w-4 mr-1" />
            )}
            ${Math.abs(transaction.amount).toFixed(2)}
          </div>
        </div>
      ))}
    </div>
  )
}
