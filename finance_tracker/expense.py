"""
expense.py - Expense data model and validation
"""

from datetime import datetime
from dataclasses import dataclass
from typing import Optional


@dataclass
class Expense:
    """Represents a single expense entry"""
    id: str
    date: str
    amount: float
    category: str
    description: str
    
    # Optional attributes
    tags: Optional[list] = None
    
    def __post_init__(self):
        """Validate expense data after initialization"""
        self.validate()
    
    def validate(self):
        """Validate all expense fields"""
        # Validate date format (YYYY-MM-DD)
        try:
            datetime.strptime(self.date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Date must be in YYYY-MM-DD format")
        
        # Validate amount
        if not isinstance(self.amount, (int, float)):
            raise ValueError("Amount must be a number")
        if self.amount <= 0:
            raise ValueError("Amount must be positive")
        
        # Validate category
        if not self.category or not self.category.strip():
            raise ValueError("Category cannot be empty")
        
        # Validate description
        if not self.description or not self.description.strip():
            raise ValueError("Description cannot be empty")
        
        # Initialize tags if None
        if self.tags is None:
            self.tags = []
    
    def to_dict(self):
        """Convert expense to dictionary for serialization"""
        return {
            "id": self.id,
            "date": self.date,
            "amount": float(self.amount),
            "category": self.category,
            "description": self.description,
            "tags": self.tags
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create Expense instance from dictionary"""
        return cls(
            id=data.get("id", ""),
            date=data.get("date", ""),
            amount=data.get("amount", 0.0),
            category=data.get("category", ""),
            description=data.get("description", ""),
            tags=data.get("tags", [])
        )
    
    def __str__(self):
        return f"{self.date} - ${self.amount:.2f} - {self.category}: {self.description}"