"""
Regenerate every museum's feature importance report from the CSVs already on
disk, without re-running the pipelines.
"""
import sys
from pathlib import Path

# Add the project root to the path so we can import src.visualisation.feature_report
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def main():
    # Need to import config and the report builder here, not at module level, because
    # the script is run from scripts/ and not the project root, so the imports would
    from config import MUSEUM_CODES
    from src.visualisation.feature_report import build_report

    for museum_code in MUSEUM_CODES.values():
        written = build_report(museum_code)
        if written:
            print(f"  wrote {written}")


if __name__ == "__main__":
    main()
