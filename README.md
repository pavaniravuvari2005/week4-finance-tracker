# Personal Finance Tracker

A comprehensive personal finance tracking application that helps users manage their expenses, categorize spending, and generate insightful reports.

# Project Structure

week4-finance-tracker/

├── finance_tracker/          # Main package

│   ├── __init__.py

│   ├── main.py              # Main application with menu system

│   ├── expense.py           # Expense data model

│   ├── expense_manager.py   # Expense management logic

│   ├── file_handler.py      # File operations (save/load/backup)

│   ├── reports.py           # Report generation

│   └── utils.py             # Utility functions

├── data/                    # Data storage

│   ├── expenses.json        # Main data file

│   ├── backup/             # Automatic backups

│   └── exports/            # CSV exports

├── tests/                   # Unit tests

│   ├── test_expense.py

│   ├── test_file_handler.py

│   └── test_reports.py

├── requirements.txt         # Python dependencies

├── README.md               # This file

├── run.py                  # Entry point script

└── .gitignore             # Git ignore file

## Features

- **Expense Management**: Add, view, search, and delete expenses
- **Categorization**: Organize expenses into categories (Food, Transport, Entertainment, etc.)
- **Data Persistence**: Save and load data from JSON files with automatic backups
- **Budget Tracking**: Set monthly budgets and track spending against them
- **Reports & Analytics**:
  - Monthly expense reports
  - Category-wise spending breakdown
  - Statistics dashboard
  - Budget status reports
- **Import/Export**: Export data to CSV for external analysis
- **Backup System**: Automatic backups with restore functionality
- **Error Handling**: Comprehensive error handling and data validation

