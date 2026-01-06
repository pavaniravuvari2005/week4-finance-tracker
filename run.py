#!/usr/bin/env python3
"""
run.py - Main runner script for the finance tracker
"""

import sys
import os

# Add the finance_tracker package to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from finance_tracker.main import main

if __name__ == "__main__":
    main()