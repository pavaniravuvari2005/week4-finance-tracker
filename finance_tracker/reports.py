"""
reports.py - Generates various reports and visualizations
"""

from datetime import datetime
from typing import List, Dict
from .expense import Expense


class ReportGenerator:
    """Generates various expense reports and visualizations"""
    
    def generate_monthly_report(self, expenses: List[Expense], year: int, month: int) -> Dict:
        """Generate detailed monthly report"""
        month_expenses = []
        total = 0.0
        category_totals = {}
        
        for expense in expenses:
            try:
                exp_date = datetime.strptime(expense.date, "%Y-%m-%d")
                if exp_date.year == year and exp_date.month == month:
                    month_expenses.append(expense)
                    total += expense.amount
                    category_totals[expense.category] = category_totals.get(expense.category, 0) + expense.amount
            except ValueError:
                continue
        
        # Sort expenses by date
        month_expenses.sort(key=lambda x: x.date)
        
        # Get top 3 categories
        top_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:3]
        
        # Calculate average daily expense
        days_in_month = self._days_in_month(year, month)
        avg_daily = total / days_in_month if days_in_month > 0 else 0
        
        return {
            "year": year,
            "month": month,
            "month_name": datetime(year, month, 1).strftime("%B"),
            "total_expenses": len(month_expenses),
            "total_amount": total,
            "average_daily": avg_daily,
            "category_totals": category_totals,
            "top_categories": top_categories,
            "expenses": month_expenses
        }
    
    def generate_category_report(self, expenses: List[Expense]) -> Dict[str, Dict]:
        """Generate category-wise breakdown"""
        category_totals = {}
        category_counts = {}
        category_expenses = {}
        
        for expense in expenses:
            category = expense.category
            category_totals[category] = category_totals.get(category, 0) + expense.amount
            category_counts[category] = category_counts.get(category, 0) + 1
            
            if category not in category_expenses:
                category_expenses[category] = []
            category_expenses[category].append(expense)
        
        total_all = sum(category_totals.values())
        
        # Calculate percentages
        category_percentages = {}
        for category, total in category_totals.items():
            percentage = (total / total_all * 100) if total_all > 0 else 0
            category_percentages[category] = percentage
        
        # Sort by total amount (descending)
        sorted_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)
        
        return {
            "category_totals": category_totals,
            "category_counts": category_counts,
            "category_percentages": category_percentages,
            "sorted_categories": sorted_categories,
            "total_all": total_all,
            "category_expenses": category_expenses
        }
    
    def generate_statistics(self, expenses: List[Expense]) -> Dict:
        """Generate overall statistics"""
        if not expenses:
            return {
                "total_expenses": 0,
                "total_amount": 0,
                "average_expense": 0,
                "min_expense": 0,
                "max_expense": 0,
                "expenses_by_month": {},
                "expenses_by_day": {}
            }
        
        # Basic statistics
        amounts = [exp.amount for exp in expenses]
        total_amount = sum(amounts)
        
        # Monthly totals
        monthly_totals = {}
        for expense in expenses:
            try:
                exp_date = datetime.strptime(expense.date, "%Y-%m-%d")
                month_key = f"{exp_date.year}-{exp_date.month:02d}"
                monthly_totals[month_key] = monthly_totals.get(month_key, 0) + expense.amount
            except ValueError:
                continue
        
        # Day of week analysis
        day_totals = {"Monday": 0, "Tuesday": 0, "Wednesday": 0, "Thursday": 0, "Friday": 0, "Saturday": 0, "Sunday": 0}
        for expense in expenses:
            try:
                exp_date = datetime.strptime(expense.date, "%Y-%m-%d")
                day_name = exp_date.strftime("%A")
                day_totals[day_name] = day_totals.get(day_name, 0) + expense.amount
            except ValueError:
                continue
        
        return {
            "total_expenses": len(expenses),
            "total_amount": total_amount,
            "average_expense": total_amount / len(expenses) if expenses else 0,
            "min_expense": min(amounts) if amounts else 0,
            "max_expense": max(amounts) if amounts else 0,
            "expenses_by_month": monthly_totals,
            "expenses_by_day": day_totals
        }
    
    def print_category_chart(self, category_report: Dict, width: int = 50):
        """Print a simple text-based bar chart of category spending"""
        print("\n" + "=" * (width + 20))
        print("CATEGORY SPENDING BREAKDOWN")
        print("=" * (width + 20))
        
        sorted_categories = category_report["sorted_categories"]
        total_all = category_report["total_all"]
        
        if not sorted_categories:
            print("No expenses to display")
            return
        
        max_amount = max(category_report["category_totals"].values())
        
        for category, amount in sorted_categories:
            percentage = (amount / total_all * 100) if total_all > 0 else 0
            bar_length = int((amount / max_amount) * width) if max_amount > 0 else 0
            bar = "█" * bar_length
            
            print(f"{category:<20} ${amount:>10.2f} {percentage:>6.1f}% {bar}")
        
        print("-" * (width + 20))
        print(f"{'TOTAL':<20} ${total_all:>10.2f} {'100.0':>6}%")
        print("=" * (width + 20))
    
    def print_monthly_report(self, monthly_report: Dict):
        """Print formatted monthly report"""
        print(f"\n{'='*60}")
        print(f"MONTHLY REPORT: {monthly_report['month_name']} {monthly_report['year']}")
        print(f"{'='*60}")
        
        print(f"\n📊 Summary:")
        print(f"   Total Expenses: {monthly_report['total_expenses']}")
        print(f"   Total Amount:   ${monthly_report['total_amount']:.2f}")
        print(f"   Average Daily:  ${monthly_report['average_daily']:.2f}")
        
        print(f"\n🏷️  Top Categories:")
        for i, (category, amount) in enumerate(monthly_report['top_categories'], 1):
            percentage = (amount / monthly_report['total_amount'] * 100) if monthly_report['total_amount'] > 0 else 0
            print(f"   {i}. {category}: ${amount:.2f} ({percentage:.1f}%)")
        
        print(f"\n📝 Recent Expenses:")
        if monthly_report['expenses']:
            recent_expenses = monthly_report['expenses'][-5:]  # Last 5 expenses
            for expense in recent_expenses:
                print(f"   • {expense.date}: ${expense.amount:.2f} - {expense.category}")
        else:
            print("   No expenses for this month")
        
        print(f"\n{'='*60}")
    
    def _days_in_month(self, year: int, month: int) -> int:
        """Get number of days in a month"""
        if month == 2:
            # Check for leap year
            if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                return 29
            else:
                return 28
        elif month in [4, 6, 9, 11]:
            return 30
        else:
            return 31