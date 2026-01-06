import unittest
from datetime import datetime
from finance_tracker.expense import Expense
import uuid


class TestExpense(unittest.TestCase):
    
    def test_valid_expense_creation(self):
        """Test creating a valid expense"""
        expense = Expense(
            id=str(uuid.uuid4())[:8],
            date="2024-01-15",
            amount=25.50,
            category="Food",
            description="Lunch at cafe"
        )
        
        self.assertEqual(expense.date, "2024-01-15")
        self.assertEqual(expense.amount, 25.50)
        self.assertEqual(expense.category, "Food")
        self.assertEqual(expense.description, "Lunch at cafe")
        self.assertEqual(expense.tags, [])
    
    def test_invalid_date(self):
        """Test expense with invalid date format"""
        with self.assertRaises(ValueError):
            Expense(
                id="test123",
                date="15-01-2024",  # Wrong format
                amount=25.50,
                category="Food",
                description="Lunch"
            )
    
    def test_invalid_amount(self):
        """Test expense with invalid amount"""
        with self.assertRaises(ValueError):
            Expense(
                id="test123",
                date="2024-01-15",
                amount=-10,  # Negative amount
                category="Food",
                description="Lunch"
            )
    
    def test_to_dict_conversion(self):
        """Test converting expense to dictionary"""
        expense = Expense(
            id="test123",
            date="2024-01-15",
            amount=25.50,
            category="Food",
            description="Lunch",
            tags=["meal", "restaurant"]
        )
        
        expense_dict = expense.to_dict()
        
        self.assertEqual(expense_dict["id"], "test123")
        self.assertEqual(expense_dict["date"], "2024-01-15")
        self.assertEqual(expense_dict["amount"], 25.50)
        self.assertEqual(expense_dict["category"], "Food")
        self.assertEqual(expense_dict["description"], "Lunch")
        self.assertEqual(expense_dict["tags"], ["meal", "restaurant"])
    
    def test_from_dict_creation(self):
        """Test creating expense from dictionary"""
        expense_data = {
            "id": "test123",
            "date": "2024-01-15",
            "amount": 25.50,
            "category": "Food",
            "description": "Lunch",
            "tags": ["meal", "restaurant"]
        }
        
        expense = Expense.from_dict(expense_data)
        
        self.assertEqual(expense.id, "test123")
        self.assertEqual(expense.date, "2024-01-15")
        self.assertEqual(expense.amount, 25.50)
        self.assertEqual(expense.category, "Food")
        self.assertEqual(expense.description, "Lunch")
        self.assertEqual(expense.tags, ["meal", "restaurant"])


if __name__ == "__main__":
    unittest.main()