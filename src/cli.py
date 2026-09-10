"""Command-line argument parsing and museum-code validation for main.py."""
import argparse
import sys

from config import MUSEUM_CODES


def parse_args():
    parser = argparse.ArgumentParser(description="Run the museum visitorship forecasting pipeline.")
    parser.add_argument(
        "--museum", "-m",
        nargs="+",
        type=str,
        default=None,
        help="Run for specific museums only (case-insensitive codes, e.g. python main.py --museum ACM PM). Omit to run all museums.",
    )
    return parser.parse_args()


def resolve_museum_selection(raw_codes):
    """
    Validate and resolve CLI museum codes (case-insensitive) into full museum
    names. Prints one error line per invalid code; if none of the given codes
    are valid, exits without running anything. Valid codes among an otherwise
    invalid list still get run.
    """
    name_by_code = {code: name for name, code in MUSEUM_CODES.items()}
    selected = []
    for raw_code in raw_codes:
        name = name_by_code.get(raw_code.upper())
        if name is None:
            print(f'"{raw_code}" is not a valid museum code. See README.md for more information.')
            continue
        if name not in selected:
            selected.append(name)

    # If no valid museum codes were provided, exit without running anything
    if not selected:
        print("No valid museum codes provided. Exiting now.")
        sys.exit(1)

    return selected
