#!/usr/bin/env python3
"""Alias runner for NaturalTest."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from natural_test.cli import main

if __name__ == "__main__":
    main()

