"""
Report how the best model performed in the Deepavali months of IHC, from the
prediction CSVs already on disk, without re-running the pipeline.
"""
import sys
from pathlib import Path

# Running a script puts scripts/ on the path, not the project root, so add it.
# Resolved from this file rather than the cwd, so the script runs from anywhere
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def main():
    # Imported here, not at module level, so the path insert above takes effect first
    from src.analysis.deepavali import MUSEUM_CODE, build_report

    written = build_report(MUSEUM_CODE)
    print(f"  wrote {written}" if written else f"  [{MUSEUM_CODE}] nothing to report")


if __name__ == "__main__":
    main()
