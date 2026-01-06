"""
utils.py - Utility functions for the application
"""

import re
from datetime import datetime
from typing import Optional


def validate_date(date_str: str) -> bool:
    """Validate date string in YYYY-MM-DD format"""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def validate_amount(amount_str: str) -> Optional[float]:
    """Validate and parse amount string"""
    try:
        amount = float(amount_str)
        if amount <= 0:
            return None
        return round(amount, 2)
    except ValueError:
        return None


def get_current_date() -> str:
    """Get current date in YYYY-MM-DD format"""
    return datetime.now().strftime("%Y-%m-%d")


def format_currency(amount: float) -> str:
    """Format amount as currency"""
    return f"${amount:,.2f}"


def get_month_name(month_num: int) -> str:
    """Get month name from month number"""
    months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    return months[month_num - 1] if 1 <= month_num <= 12 else "Unknown"


def safe_input(prompt: str, validation_func=None, error_msg: str = "Invalid input. Please try again."):
    """Get validated input from user"""
    while True:
        try:
            user_input = input(prompt).strip()
            if validation_func is None or validation_func(user_input):
                return user_input
            else:
                print(f"✗ {error_msg}")
        except KeyboardInterrupt:
            print("\n\nOperation cancelled by user.")
            raise
        except EOFError:
            print("\n\nEnd of input.")
            raise


def clear_screen():
    """Clear terminal screen"""
    print("\n" * 100)  # Simple method - prints many newlines


def print_header(title: str):
    """Print a formatted header"""
    print("\n" + "=" * 60)
    print(f"          {title}")
    print("=" * 60)


def print_menu(title: str, options: list):
    """Print a formatted menu"""
    print_header(title)
    for i, option in enumerate(options, 1):
        print(f"{i}. {option}")
    print("=" * 60)