"""
Summarise the Optuna studies saved by the last pipeline run into
outputs/tuning_report.md, without re-running anything.
"""
import sys
from pathlib import Path

# Running a script puts scripts/ on the path, not the project root, so add it.
# Resolved from this file rather than the cwd, so the script runs from anywhere
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


def main():
    # Imported here, not at module level, so the path insert above takes effect first
    from src.analysis.tuning_report import build_report

    written = build_report()
    print(f"  wrote {written}" if written else "  no studies found under outputs/tuning/")


if __name__ == "__main__":
    main()
