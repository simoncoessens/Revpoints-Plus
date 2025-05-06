import { Progress } from "@/components/ui/progress"

export function BudgetCards() {
  const budgets = [
    {
      id: 1,
      category: "Housing",
      allocated: 1500,
      spent: 1200,
      remaining: 300,
      percentage: 80,
    },
    {
      id: 2,
      category: "Food & Dining",
      allocated: 800,
      spent: 650.25,
      remaining: 149.75,
      percentage: 81,
    },
    {
      id: 3,
      category: "Transportation",
      allocated: 500,
      spent: 420.8,
      remaining: 79.2,
      percentage: 84,
    },
    {
      id: 4,
      category: "Entertainment",
      allocated: 400,
      spent: 320.45,
      remaining: 79.55,
      percentage: 80,
    },
  ]

  return (
    <div className="space-y-4">
      {budgets.map((budget) => (
        <div key={budget.id} className="space-y-2">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium">{budget.category}</p>
              <p className="text-xs text-muted-foreground">
                ${budget.spent.toFixed(2)} of ${budget.allocated.toFixed(2)}
              </p>
            </div>
            <div className="text-sm font-medium">${budget.remaining.toFixed(2)} left</div>
          </div>
          <Progress value={budget.percentage} className="h-2" />
          <div className="flex justify-between text-xs text-muted-foreground">
            <span>{budget.percentage}% spent</span>
            <span>{100 - budget.percentage}% remaining</span>
          </div>
        </div>
      ))}
    </div>
  )
}
