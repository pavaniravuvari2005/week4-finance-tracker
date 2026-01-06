"""
expense_manager.py - Manages collections of expenses
"""

import uuid
from datetime import datetime
from typing import List, Dict, Optional
from .expense import Expense


class ExpenseManager:
    """Manages a collection of expenses with various operations"""
    
    # Common expense categories
    DEFAULT_CATEGORIES = [
        "Food & Dining",
        "Transportation",
        "Shopping",
        "Entertainment",
        "Bills & Utilities",
        "Healthcare",
        "Education",
        "Personal Care",
        "Travel",
        "Other"
    ]
    
    def __init__(self):
        self.expenses: List[Expense] = []
        self.categories = self.DEFAULT_CATEGORIES.copy()
        self.budgets: Dict[str, float] = {}
    
    def add_expense(self, date: str, amount: float, category: str, description: str, tags: List[str] = None) -> Expense:
        """Add a new expense"""
        # Generate unique ID
        expense_id = str(uuid.uuid4())[:8]
        
        # Create expense
        expense = Expense(
            id=expense_id,
            date=date,
            amount=amount,
            category=category,
            description=description,
            tags=tags if tags else []
        )
        
        # Add to list
        self.expenses.append(expense)
        return expense
    
    def remove_expense(self, expense_id: str) -> bool:
        """Remove an expense by ID"""
        for i, expense in enumerate(self.expenses):
            if expense.id == expense_id:
                self.expenses.pop(i)
                return True
        return False
    
    def get_expense(self, expense_id: str) -> Optional[Expense]:
        """Get expense by ID"""
        for expense in self.expenses:
            if expense.id == expense_id:
                return expense
        return None
    
    def get_all_expenses(self) -> List[Expense]:
        """Get all expenses"""
        return self.expenses.copy()
    
    def get_expenses_by_category(self, category: str) -> List[Expense]:
        """Get all expenses in a specific category"""
        return [exp for exp in self.expenses if exp.category == category]
    
    def get_expenses_by_month(self, year: int, month: int) -> List[Expense]:
        """Get all expenses for a specific month"""
        result = []
        for expense in self.expenses:
            try:
                exp_date = datetime.strptime(expense.date, "%Y-%m-%d")
                if exp_date.year == year and exp_date.month == month:
                    result.append(expense)
            except ValueError:
                continue
        return result
    
    def search_expenses(self, keyword: str) -> List[Expense]:
        """Search expenses by keyword in description or category"""
        keyword = keyword.lower()
        result = []
        for expense in self.expenses:
            if (keyword in expense.description.lower() or 
                keyword in expense.category.lower() or
                any(keyword in tag.lower() for tag in expense.tags)):
                result.append(expense)
        return result
    
    def get_total_spent(self) -> float:
        """Calculate total amount spent"""
        return sum(exp.amount for exp in self.expenses)
    
    def get_category_totals(self) -> Dict[str, float]:
        """Calculate total spent per category"""
        totals = {}
        for expense in self.expenses:
            totals[expense.category] = totals.get(expense.category, 0) + expense.amount
        return totals
    
    def get_monthly_totals(self) -> Dict[str, float]:
        """Calculate total spent per month"""
        totals = {}
        for expense in self.expenses:
            try:
                exp_date = datetime.strptime(expense.date, "%Y-%m-%d")
                month_key = f"{exp_date.year}-{exp_date.month:02d}"
                totals[month_key] = totals.get(month_key, 0) + expense.amount
            except ValueError:
                continue
        return totals
    
    def add_category(self, category: str):
        """Add a new category"""
        if category not in self.categories:
            self.categories.append(category)
    
    def set_budget(self, category: str, amount: float):
        """Set budget for a category"""
        self.budgets[category] = amount
    
    def get_budget_status(self) -> Dict[str, Dict[str, float]]:
        """Get budget vs actual spending"""
        category_totals = self.get_category_totals()
        status = {}
        
        for category, budget in self.budgets.items():
            actual = category_totals.get(category, 0)
            remaining = budget - actual
            status[category] = {
                "budget": budget,
                "actual": actual,
                "remaining": remaining,
                "percentage": (actual / budget * 100) if budget > 0 else 0
            }
        
        return status
    
    def clear_all(self):
        """Clear all expenses"""
        self.expenses.clear()