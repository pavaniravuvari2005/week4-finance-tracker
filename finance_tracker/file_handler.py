"""
file_handler.py - Handles file operations for data persistence
"""

import json
import csv
import os
import shutil
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path
from .expense import Expense


class FileHandler:
    """Handles all file operations including save, load, backup, and export"""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize with data directory"""
        self.data_dir = Path(data_dir)
        self.backup_dir = self.data_dir / "backup"
        self.export_dir = self.data_dir / "exports"
        
        # Create directories if they don't exist
        self.data_dir.mkdir(exist_ok=True)
        self.backup_dir.mkdir(exist_ok=True)
        self.export_dir.mkdir(exist_ok=True)
        
        # Main data file
        self.data_file = self.data_dir / "expenses.json"
        self.backup_file = self.backup_dir / f"expenses_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    
    def save_expenses(self, expenses: List[Expense]) -> bool:
        """Save expenses to JSON file with backup"""
        try:
            # Create backup of existing file if it exists
            if self.data_file.exists():
                self._create_backup()
            
            # Convert expenses to dictionary format
            data = {
                "expenses": [exp.to_dict() for exp in expenses],
                "metadata": {
                    "saved_at": datetime.now().isoformat(),
                    "total_expenses": len(expenses),
                    "total_amount": sum(exp.amount for exp in expenses)
                }
            }
            
            # Write to file
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            print(f"✓ Data saved successfully to {self.data_file}")
            return True
            
        except PermissionError:
            print(f"✗ Permission denied: Cannot write to {self.data_file}")
            return False
        except Exception as e:
            print(f"✗ Error saving data: {e}")
            return False
    
    def load_expenses(self) -> List[Expense]:
        """Load expenses from JSON file"""
        try:
            if not self.data_file.exists():
                print(f"ℹ️  No data file found at {self.data_file}. Starting with empty expenses.")
                return []
            
            with open(self.data_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Convert dictionary to Expense objects
            expenses = []
            for exp_data in data.get("expenses", []):
                try:
                    expense = Expense.from_dict(exp_data)
                    expenses.append(expense)
                except ValueError as e:
                    print(f"⚠️  Skipping invalid expense data: {e}")
            
            print(f"✓ Loaded {len(expenses)} expenses from {self.data_file}")
            return expenses
            
        except json.JSONDecodeError:
            print(f"✗ Error: Data file is corrupted or invalid JSON format")
            return []
        except Exception as e:
            print(f"✗ Error loading data: {e}")
            return []
    
    def _create_backup(self):
        """Create a backup of the data file"""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"expenses_backup_{timestamp}.json"
            
            shutil.copy2(self.data_file, backup_file)
            print(f"✓ Backup created: {backup_file}")
            
            # Keep only last 5 backups
            self._cleanup_old_backups(max_backups=5)
            
        except Exception as e:
            print(f"⚠️  Could not create backup: {e}")
    
    def _cleanup_old_backups(self, max_backups: int = 5):
        """Keep only the most recent backups"""
        try:
            backup_files = list(self.backup_dir.glob("expenses_backup_*.json"))
            backup_files.sort(key=os.path.getmtime, reverse=True)
            
            for old_backup in backup_files[max_backups:]:
                old_backup.unlink()
                print(f"🗑️  Removed old backup: {old_backup}")
        except Exception as e:
            print(f"⚠️  Could not clean up old backups: {e}")
    
    def export_to_csv(self, expenses: List[Expense], filename: str = None) -> str:
        """Export expenses to CSV file"""
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = self.export_dir / f"expenses_export_{timestamp}.csv"
            else:
                filename = self.export_dir / filename
            
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['id', 'date', 'amount', 'category', 'description', 'tags']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for expense in expenses:
                    row = expense.to_dict()
                    row['tags'] = ', '.join(row['tags'])  # Convert list to string
                    writer.writerow(row)
            
            print(f"✓ Data exported to {filename}")
            return str(filename)
            
        except Exception as e:
            print(f"✗ Error exporting to CSV: {e}")
            return ""
    
    def import_from_csv(self, filename: str) -> List[Expense]:
        """Import expenses from CSV file"""
        try:
            filepath = self.export_dir / filename if not Path(filename).is_absolute() else Path(filename)
            
            if not filepath.exists():
                print(f"✗ File not found: {filepath}")
                return []
            
            expenses = []
            with open(filepath, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        # Parse tags from string
                        tags = [tag.strip() for tag in row['tags'].split(',')] if row['tags'] else []
                        
                        expense = Expense(
                            id=row['id'],
                            date=row['date'],
                            amount=float(row['amount']),
                            category=row['category'],
                            description=row['description'],
                            tags=tags
                        )
                        expenses.append(expense)
                    except (ValueError, KeyError) as e:
                        print(f"⚠️  Skipping invalid row: {e}")
            
            print(f"✓ Imported {len(expenses)} expenses from {filepath}")
            return expenses
            
        except Exception as e:
            print(f"✗ Error importing from CSV: {e}")
            return []
    
    def restore_from_backup(self, backup_filename: str = None) -> List[Expense]:
        """Restore expenses from a backup file"""
        try:
            if backup_filename:
                backup_file = self.backup_dir / backup_filename
            else:
                # Get the most recent backup
                backup_files = list(self.backup_dir.glob("expenses_backup_*.json"))
                if not backup_files:
                    print("✗ No backup files found")
                    return []
                
                backup_files.sort(key=os.path.getmtime, reverse=True)
                backup_file = backup_files[0]
            
            if not backup_file.exists():
                print(f"✗ Backup file not found: {backup_file}")
                return []
            
            # Copy backup to main data file
            shutil.copy2(backup_file, self.data_file)
            print(f"✓ Restored from backup: {backup_file}")
            
            # Load the restored data
            return self.load_expenses()
            
        except Exception as e:
            print(f"✗ Error restoring from backup: {e}")
            return []
    
    def list_backups(self) -> List[str]:
        """List all available backup files"""
        try:
            backup_files = list(self.backup_dir.glob("expenses_backup_*.json"))
            backup_files.sort(key=os.path.getmtime, reverse=True)
            
            backups = []
            for backup in backup_files:
                mod_time = datetime.fromtimestamp(os.path.getmtime(backup))
                size_kb = os.path.getsize(backup) / 1024
                backups.append({
                    'filename': backup.name,
                    'size_kb': f"{size_kb:.1f}",
                    'modified': mod_time.strftime("%Y-%m-%d %H:%M:%S")
                })
            
            return backups
            
        except Exception as e:
            print(f"✗ Error listing backups: {e}")
            return []