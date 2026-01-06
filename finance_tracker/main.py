"""
main.py - Main application with menu system
"""

import sys
from datetime import datetime
from .expense_manager import ExpenseManager
from .file_handler import FileHandler
from .reports import ReportGenerator
from .utils import (
    validate_date, validate_amount, get_current_date,
    format_currency, safe_input, print_header, print_menu
)


class FinanceTracker:
    """Main finance tracker application"""
    
    def __init__(self):
        """Initialize the application"""
        self.expense_manager = ExpenseManager()
        self.file_handler = FileHandler()
        self.report_generator = ReportGenerator()
        
        # Load existing data
        self.load_data()
    
    def load_data(self):
        """Load expenses from file"""
        expenses = self.file_handler.load_expenses()
        for expense in expenses:
            self.expense_manager.expenses.append(expense)
        
        # Update categories from loaded expenses
        for expense in expenses:
            if expense.category not in self.expense_manager.categories:
                self.expense_manager.add_category(expense.category)
    
    def save_data(self):
        """Save expenses to file"""
        self.file_handler.save_expenses(self.expense_manager.expenses)
    
    def run(self):
        """Run the main application loop"""
        print_header("PERSONAL FINANCE TRACKER")
        print("Welcome to your personal finance manager!")
        print("Track expenses, set budgets, and generate insightful reports.\n")
        
        while True:
            try:
                self.show_main_menu()
            except KeyboardInterrupt:
                print("\n\n⚠️  Interrupted by user. Saving data...")
                self.save_data()
                print("Goodbye!")
                sys.exit(0)
            except Exception as e:
                print(f"\n⚠️  An error occurred: {e}")
                print("Returning to main menu...")
    
    def show_main_menu(self):
        """Display main menu and handle user choice"""
        menu_options = [
            "Add New Expense",
            "View All Expenses",
            "Search Expenses",
            "Monthly Reports",
            "Category Analysis",
            "Set/Update Budget",
            "Budget Status",
            "Statistics Dashboard",
            "Export/Import Data",
            "Backup/Restore",
            "Exit"
        ]
        
        print_menu("MAIN MENU", menu_options)
        
        choice = safe_input("\nEnter your choice (1-11): ", 
                          lambda x: x.isdigit() and 1 <= int(x) <= 11,
                          "Please enter a number between 1 and 11")
        
        actions = {
            '1': self.add_expense,
            '2': self.view_expenses,
            '3': self.search_expenses,
            '4': self.monthly_reports,
            '5': self.category_analysis,
            '6': self.set_budget,
            '7': self.budget_status,
            '8': self.statistics_dashboard,
            '9': self.export_import_menu,
            '10': self.backup_restore_menu,
            '11': self.exit_application
        }
        
        actions[choice]()
    
    def add_expense(self):
        """Add a new expense"""
        print_header("ADD NEW EXPENSE")
        
        # Get date (default to today)
        default_date = get_current_date()
        date_input = safe_input(
            f"Enter date (YYYY-MM-DD) [Default: {default_date}]: ",
            lambda x: not x or validate_date(x),
            "Invalid date format. Use YYYY-MM-DD"
        )
        date = date_input if date_input else default_date
        
        # Get amount
        while True:
            amount_input = safe_input("Enter amount ($): ")
            amount = validate_amount(amount_input)
            if amount is not None:
                break
            print("✗ Invalid amount. Please enter a positive number.")
        
        # Get category
        print("\nAvailable categories:")
        for i, category in enumerate(self.expense_manager.categories, 1):
            print(f"{i}. {category}")
        
        while True:
            cat_choice = safe_input(
                f"\nSelect category (1-{len(self.expense_manager.categories)}) or enter new category: "
            )
            
            if cat_choice.isdigit() and 1 <= int(cat_choice) <= len(self.expense_manager.categories):
                category = self.expense_manager.categories[int(cat_choice) - 1]
                break
            elif cat_choice:  # New category
                category = cat_choice
                self.expense_manager.add_category(category)
                break
            else:
                print("✗ Please select a category or enter a new one.")
        
        # Get description
        description = safe_input("Enter description: ", 
                               lambda x: bool(x.strip()),
                               "Description cannot be empty")
        
        # Get tags (optional)
        tags_input = safe_input("Enter tags (comma-separated, optional): ")
        tags = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
        
        # Add expense
        expense = self.expense_manager.add_expense(date, amount, category, description, tags)
        print(f"\n✓ Expense added successfully!")
        print(f"  ID: {expense.id}")
        print(f"  Date: {expense.date}")
        print(f"  Amount: {format_currency(expense.amount)}")
        print(f"  Category: {expense.category}")
        print(f"  Description: {expense.description}")
        
        # Auto-save
        self.save_data()
        input("\nPress Enter to continue...")
    
    def view_expenses(self):
        """View all expenses"""
        print_header("ALL EXPENSES")
        
        expenses = self.expense_manager.get_all_expenses()
        
        if not expenses:
            print("No expenses recorded yet.")
            input("\nPress Enter to continue...")
            return
        
        # Sort by date (most recent first)
        expenses.sort(key=lambda x: x.date, reverse=True)
        
        # Filter options
        print("\nFilter options:")
        print("1. View all")
        print("2. This month")
        print("3. Last 30 days")
        print("4. By category")
        
        filter_choice = safe_input("\nSelect filter (1-4): ",
                                 lambda x: x in ['1', '2', '3', '4'],
                                 "Please select 1-4")
        
        filtered_expenses = expenses
        
        if filter_choice == '2':
            # This month
            current = datetime.now()
            filtered_expenses = self.expense_manager.get_expenses_by_month(current.year, current.month)
        elif filter_choice == '3':
            # Last 30 days
            cutoff_date = datetime.now().timestamp() - (30 * 24 * 60 * 60)
            filtered_expenses = [exp for exp in expenses 
                               if datetime.strptime(exp.date, "%Y-%m-%d").timestamp() > cutoff_date]
        elif filter_choice == '4':
            # By category
            print("\nAvailable categories:")
            for i, cat in enumerate(self.expense_manager.categories, 1):
                print(f"{i}. {cat}")
            
            cat_choice = safe_input(f"\nSelect category (1-{len(self.expense_manager.categories)}): ",
                                  lambda x: x.isdigit() and 1 <= int(x) <= len(self.expense_manager.categories),
                                  "Invalid category selection")
            
            category = self.expense_manager.categories[int(cat_choice) - 1]
            filtered_expenses = self.expense_manager.get_expenses_by_category(category)
        
        if not filtered_expenses:
            print(f"\nNo expenses found for the selected filter.")
            input("\nPress Enter to continue...")
            return
        
        # Display expenses
        print(f"\n{'='*80}")
        print(f"{'Date':<12} {'Category':<20} {'Amount':>12} {'Description':<30}")
        print(f"{'='*80}")
        
        total = 0
        for expense in filtered_expenses:
            print(f"{expense.date:<12} {expense.category:<20} {format_currency(expense.amount):>12} {expense.description[:30]:<30}")
            total += expense.amount
        
        print(f"{'='*80}")
        print(f"{'TOTAL':<32} {format_currency(total):>12}")
        print(f"{'='*80}")
        
        # Additional options
        print("\nOptions:")
        print("1. View detailed expense")
        print("2. Delete expense")
        print("3. Return to main menu")
        
        option = safe_input("\nSelect option (1-3): ",
                          lambda x: x in ['1', '2', '3'],
                          "Please select 1-3")
        
        if option == '1':
            self.view_expense_details()
        elif option == '2':
            self.delete_expense()
        
        input("\nPress Enter to continue...")
    
    def view_expense_details(self):
        """View details of a specific expense"""
        expense_id = safe_input("\nEnter expense ID: ")
        expense = self.expense_manager.get_expense(expense_id)
        
        if expense:
            print_header("EXPENSE DETAILS")
            print(f"ID:          {expense.id}")
            print(f"Date:        {expense.date}")
            print(f"Amount:      {format_currency(expense.amount)}")
            print(f"Category:    {expense.category}")
            print(f"Description: {expense.description}")
            print(f"Tags:        {', '.join(expense.tags) if expense.tags else 'None'}")
        else:
            print("✗ Expense not found.")
    
    def delete_expense(self):
        """Delete an expense"""
        expense_id = safe_input("\nEnter expense ID to delete: ")
        
        confirm = safe_input(f"Are you sure you want to delete expense {expense_id}? (yes/no): ",
                           lambda x: x.lower() in ['yes', 'no', 'y', 'n'],
                           "Please enter 'yes' or 'no'")
        
        if confirm.lower() in ['yes', 'y']:
            if self.expense_manager.remove_expense(expense_id):
                print("✓ Expense deleted successfully.")
                self.save_data()
            else:
                print("✗ Expense not found.")
        else:
            print("✗ Deletion cancelled.")
    
    def search_expenses(self):
        """Search expenses by keyword"""
        print_header("SEARCH EXPENSES")
        
        keyword = safe_input("Enter search keyword: ",
                           lambda x: bool(x.strip()),
                           "Search term cannot be empty")
        
        results = self.expense_manager.search_expenses(keyword)
        
        if not results:
            print(f"\nNo expenses found matching '{keyword}'.")
            input("\nPress Enter to continue...")
            return
        
        print(f"\nFound {len(results)} expense(s):")
        print(f"{'='*80}")
        print(f"{'Date':<12} {'Category':<20} {'Amount':>12} {'Description':<30}")
        print(f"{'='*80}")
        
        total = 0
        for expense in results:
            print(f"{expense.date:<12} {expense.category:<20} {format_currency(expense.amount):>12} {expense.description[:30]:<30}")
            total += expense.amount
        
        print(f"{'='*80}")
        print(f"{'TOTAL':<32} {format_currency(total):>12}")
        print(f"{'='*80}")
        
        input("\nPress Enter to continue...")
    
    def monthly_reports(self):
        """Generate monthly reports"""
        print_header("MONTHLY REPORTS")
        
        print("1. Current month report")
        print("2. Specific month report")
        print("3. Monthly comparison")
        
        choice = safe_input("\nSelect option (1-3): ",
                          lambda x: x in ['1', '2', '3'],
                          "Please select 1-3")
        
        if choice == '1':
            current = datetime.now()
            report = self.report_generator.generate_monthly_report(
                self.expense_manager.expenses, current.year, current.month
            )
            self.report_generator.print_monthly_report(report)
        
        elif choice == '2':
            year = int(safe_input("Enter year (YYYY): ",
                                lambda x: x.isdigit() and len(x) == 4,
                                "Invalid year"))
            
            month = int(safe_input("Enter month (1-12): ",
                                 lambda x: x.isdigit() and 1 <= int(x) <= 12,
                                 "Invalid month"))
            
            report = self.report_generator.generate_monthly_report(
                self.expense_manager.expenses, year, month
            )
            self.report_generator.print_monthly_report(report)
        
        elif choice == '3':
            self.monthly_comparison()
        
        input("\nPress Enter to continue...")
    
    def monthly_comparison(self):
        """Compare monthly spending"""
        print_header("MONTHLY COMPARISON")
        
        monthly_totals = self.expense_manager.get_monthly_totals()
        
        if not monthly_totals:
            print("No monthly data available.")
            return
        
        print(f"\n{'Month':<10} {'Total Amount':>15} {'# Expenses':>12}")
        print("-" * 40)
        
        for month, total in sorted(monthly_totals.items(), reverse=True):
            month_expenses = self.expense_manager.get_expenses_by_month(
                int(month.split('-')[0]), int(month.split('-')[1])
            )
            count = len(month_expenses)
            print(f"{month:<10} {format_currency(total):>15} {count:>12}")
        
        print("-" * 40)
    
    def category_analysis(self):
        """Analyze spending by category"""
        print_header("CATEGORY ANALYSIS")
        
        report = self.report_generator.generate_category_report(self.expense_manager.expenses)
        
        if not report["category_totals"]:
            print("No expenses recorded yet.")
            input("\nPress Enter to continue...")
            return
        
        # Print category chart
        self.report_generator.print_category_chart(report)
        
        # Additional options
        print("\nOptions:")
        print("1. View expenses by category")
        print("2. Return to main menu")
        
        option = safe_input("\nSelect option (1-2): ",
                          lambda x: x in ['1', '2'],
                          "Please select 1-2")
        
        if option == '1':
            print("\nAvailable categories:")
            for i, category in enumerate(report["sorted_categories"], 1):
                cat, total = category
                print(f"{i}. {cat}: {format_currency(total)}")
            
            cat_choice = safe_input(f"\nSelect category (1-{len(report['sorted_categories'])}): ",
                                  lambda x: x.isdigit() and 1 <= int(x) <= len(report['sorted_categories']),
                                  "Invalid category selection")
            
            selected_cat = report["sorted_categories"][int(cat_choice) - 1][0]
            cat_expenses = report["category_expenses"][selected_cat]
            
            print(f"\nExpenses in '{selected_cat}':")
            print(f"{'='*60}")
            for expense in cat_expenses:
                print(f"{expense.date}: {format_currency(expense.amount)} - {expense.description}")
            print(f"{'='*60}")
            print(f"Total: {format_currency(sum(exp.amount for exp in cat_expenses))}")
        
        input("\nPress Enter to continue...")
    
    def set_budget(self):
        """Set or update budget for categories"""
        print_header("SET/UPDATE BUDGET")
        
        print("Available categories:")
        for i, category in enumerate(self.expense_manager.categories, 1):
            current_budget = self.expense_manager.budgets.get(category, 0)
            print(f"{i}. {category} {'(Budget: ' + format_currency(current_budget) + ')' if current_budget else ''}")
        
        cat_choice = safe_input(f"\nSelect category (1-{len(self.expense_manager.categories)}): ",
                              lambda x: x.isdigit() and 1 <= int(x) <= len(self.expense_manager.categories),
                              "Invalid category selection")
        
        category = self.expense_manager.categories[int(cat_choice) - 1]
        
        while True:
            budget_input = safe_input(f"Enter monthly budget for {category} ($): ")
            budget = validate_amount(budget_input)
            if budget is not None:
                break
            print("✗ Invalid amount. Please enter a positive number.")
        
        self.expense_manager.set_budget(category, budget)
        print(f"\n✓ Budget set for {category}: {format_currency(budget)}")
        
        input("\nPress Enter to continue...")
    
    def budget_status(self):
        """Check budget vs actual spending"""
        print_header("BUDGET STATUS")
        
        status = self.expense_manager.get_budget_status()
        
        if not status:
            print("No budgets set. Use 'Set/Update Budget' to create budgets.")
            input("\nPress Enter to continue...")
            return
        
        print(f"\n{'Category':<20} {'Budget':>12} {'Actual':>12} {'Remaining':>12} {'% Used':>10}")
        print("-" * 70)
        
        for category, data in status.items():
            remaining = data['remaining']
            percent = data['percentage']
            
            # Color coding for remaining amount
            remaining_str = format_currency(remaining)
            if remaining < 0:
                remaining_str = f"❌ {remaining_str}"  # Over budget
            elif remaining < data['budget'] * 0.1:  # Less than 10% remaining
                remaining_str = f"⚠️  {remaining_str}"
            else:
                remaining_str = f"✓ {remaining_str}"
            
            print(f"{category:<20} {format_currency(data['budget']):>12} {format_currency(data['actual']):>12} "
                  f"{remaining_str:>12} {percent:>9.1f}%")
        
        print("-" * 70)
        
        # Summary
        total_budget = sum(data['budget'] for data in status.values())
        total_actual = sum(data['actual'] for data in status.values())
        total_remaining = total_budget - total_actual
        
        print(f"\n📊 Summary:")
        print(f"  Total Budget:    {format_currency(total_budget)}")
        print(f"  Total Spent:     {format_currency(total_actual)}")
        print(f"  Total Remaining: {format_currency(total_remaining)}")
        print(f"  Overall Usage:   {(total_actual/total_budget*100):.1f}%")
        
        input("\nPress Enter to continue...")
    
    def statistics_dashboard(self):
        """Display statistics dashboard"""
        print_header("STATISTICS DASHBOARD")
        
        stats = self.report_generator.generate_statistics(self.expense_manager.expenses)
        
        if stats['total_expenses'] == 0:
            print("No expenses recorded yet.")
            input("\nPress Enter to continue...")
            return
        
        print("\n📈 OVERALL STATISTICS")
        print(f"  Total Expenses:      {stats['total_expenses']}")
        print(f"  Total Amount:        {format_currency(stats['total_amount'])}")
        print(f"  Average Expense:     {format_currency(stats['average_expense'])}")
        print(f"  Smallest Expense:    {format_currency(stats['min_expense'])}")
        print(f"  Largest Expense:     {format_currency(stats['max_expense'])}")
        
        print("\n📅 MONTHLY TREND")
        if stats['expenses_by_month']:
            for month, total in sorted(stats['expenses_by_month'].items(), reverse=True)[:6]:  # Last 6 months
                print(f"  {month}: {format_currency(total)}")
        else:
            print("  No monthly data")
        
        print("\n📊 SPENDING BY DAY OF WEEK")
        if stats['expenses_by_day']:
            for day, total in stats['expenses_by_day'].items():
                print(f"  {day[:3]}: {format_currency(total)}")
        else:
            print("  No day-based data")
        
        input("\nPress Enter to continue...")
    
    def export_import_menu(self):
        """Export/import data menu"""
        print_header("EXPORT/IMPORT DATA")
        
        print("1. Export to CSV")
        print("2. Import from CSV")
        print("3. Return to main menu")
        
        choice = safe_input("\nSelect option (1-3): ",
                          lambda x: x in ['1', '2', '3'],
                          "Please select 1-3")
        
        if choice == '1':
            filename = safe_input("Enter filename (or press Enter for default): ")
            exported_file = self.file_handler.export_to_csv(
                self.expense_manager.expenses,
                filename if filename else None
            )
            if exported_file:
                print(f"✓ Data exported to: {exported_file}")
        
        elif choice == '2':
            print("\nAvailable CSV files:")
            csv_files = list(self.file_handler.export_dir.glob("*.csv"))
            if not csv_files:
                print("  No CSV files found in exports folder.")
                filename = safe_input("\nEnter full path to CSV file: ")
            else:
                for i, file in enumerate(csv_files, 1):
                    print(f"{i}. {file.name}")
                
                file_choice = safe_input(f"\nSelect file (1-{len(csv_files)}) or enter filename: ")
                
                if file_choice.isdigit() and 1 <= int(file_choice) <= len(csv_files):
                    filename = csv_files[int(file_choice) - 1].name
                else:
                    filename = file_choice
            
            imported_expenses = self.file_handler.import_from_csv(filename)
            if imported_expenses:
                confirm = safe_input(f"Import {len(imported_expenses)} expenses? (yes/no): ",
                                   lambda x: x.lower() in ['yes', 'no', 'y', 'n'],
                                   "Please enter 'yes' or 'no'")
                
                if confirm.lower() in ['yes', 'y']:
                    self.expense_manager.expenses.extend(imported_expenses)
                    self.save_data()
                    print("✓ Data imported successfully.")
                else:
                    print("✗ Import cancelled.")
        
        input("\nPress Enter to continue...")
    
    def backup_restore_menu(self):
        """Backup and restore menu"""
        print_header("BACKUP/RESTORE")
        
        print("1. Create backup")
        print("2. Restore from backup")
        print("3. List backups")
        print("4. Return to main menu")
        
        choice = safe_input("\nSelect option (1-4): ",
                          lambda x: x in ['1', '2', '3', '4'],
                          "Please select 1-4")
        
        if choice == '1':
            self.save_data()  # This automatically creates a backup
        
        elif choice == '2':
            backups = self.file_handler.list_backups()
            if not backups:
                print("No backup files available.")
            else:
                print("\nAvailable backups:")
                for i, backup in enumerate(backups, 1):
                    print(f"{i}. {backup['filename']} ({backup['size_kb']} KB, {backup['modified']})")
                
                backup_choice = safe_input(f"\nSelect backup (1-{len(backups)}) or 'c' to cancel: ")
                
                if backup_choice.lower() != 'c' and backup_choice.isdigit() and 1 <= int(backup_choice) <= len(backups):
                    selected_backup = backups[int(backup_choice) - 1]['filename']
                    
                    confirm = safe_input(f"Restore from {selected_backup}? (yes/no): ",
                                       lambda x: x.lower() in ['yes', 'no', 'y', 'n'],
                                       "Please enter 'yes' or 'no'")
                    
                    if confirm.lower() in ['yes', 'y']:
                        restored_expenses = self.file_handler.restore_from_backup(selected_backup)
                        if restored_expenses:
                            self.expense_manager.expenses = restored_expenses
                            print("✓ Data restored successfully.")
        
        elif choice == '3':
            backups = self.file_handler.list_backups()
            if not backups:
                print("No backup files available.")
            else:
                print("\nBackup files:")
                for backup in backups:
                    print(f"  • {backup['filename']} ({backup['size_kb']} KB, {backup['modified']})")
        
        input("\nPress Enter to continue...")
    
    def exit_application(self):
        """Exit the application"""
        print_header("EXIT APPLICATION")
        
        print("Saving data...")
        self.save_data()
        
        print("\nThank you for using Personal Finance Tracker!")
        print("Goodbye! 👋\n")
        
        sys.exit(0)


def main():
    """Main entry point"""
    try:
        app = FinanceTracker()
        app.run()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n⚠️  An unexpected error occurred: {e}")
        print("Please report this issue.")
        sys.exit(1)


if __name__ == "__main__":
    main()