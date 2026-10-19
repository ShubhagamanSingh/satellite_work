"""
main_reproduce.py
=================
Master Execution Wrapper for NASA SMAP Soil Moisture Prediction Pipeline.
Delegates to codes/main_reproduce.py.
"""

import sys
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CODES_DIR = os.path.join(ROOT_DIR, "codes")
if CODES_DIR not in sys.path:
    sys.path.insert(0, CODES_DIR)

from main_reproduce import main

if __name__ == "__main__":
    main()
