"""
Regenerate every museum's feature importance report from the CSVs already on
disk, without re-running the pipelines.
"""
import sys

from config import MUSEUM_CODES
from src.visualisation.feature_report import build_report

# Add the project root to the path so we can import from src and config
sys.path.insert(0, ".")

# Regenerate every museum's feature importance report from the CSVs already on disk
for museum_code in MUSEUM_CODES.values():
    written = build_report(museum_code)
    if written:
        print(f"  wrote {written}")
