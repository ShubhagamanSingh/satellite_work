"""
run_pipeline.py
===============
Master Execution Interface for the NASA SMAP Soil Moisture Prediction Project.

Usage:
  python run_pipeline.py                     # Run end-to-end training & visualization on authentic NASA data
  python run_pipeline.py --earthdata-login   # Authenticate and download latest granules from NASA Earthdata
  python run_pipeline.py --manuscript        # Generate the academic Word paper (.docx)
  python run_pipeline.py --offline           # Run in calibrated physical proxy mode (zero login)
"""

import sys
import os

# Ensure codes/ directory is in path
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
CODES_DIR = os.path.join(ROOT_DIR, "codes")
if CODES_DIR not in sys.path:
    sys.path.insert(0, CODES_DIR)

if __name__ == "__main__":
    if "--manuscript" in sys.argv:
        from generate_word_manuscript import build_paper
        out_doc = os.path.join(ROOT_DIR, "docs", "Enhanced_Soil_Moisture_Prediction_Paper.docx")
        print(f"[Manuscript Engine] Generating full academic paper into: {out_doc}...")
        build_paper(out_doc)
    else:
        from main_reproduce import main
        main()
