#!/usr/bin/env python3
"""
NaturalTest: Plain-English Browser Automation Tool.
Takes natural language test cases and runs them automatically in a browser.

Usage:
    python run_test.py --test "Log in as a customer and verify the dashboard is shown" --url "https://phptravels.net"
    python run_test.py --test "Log in as a customer and verify the dashboard is shown" --url "https://phptravels.com/demo"
    python run_test.py --file examples/sample_tests.txt
    python run_test.py --interactive
"""

import sys
from pathlib import Path

# Ensure package is on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from natural_test.cli import main

if __name__ == "__main__":
    main()

