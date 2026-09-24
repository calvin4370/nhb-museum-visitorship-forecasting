"""Command-line argument parsing and museum-code/model-key validation for main.py."""
import argparse
import sys

from config import MUSEUM_CODES, MODEL_KEYS

# main.py help messages
museum_flag_help = f"""Run for specific museums only (case-insensitive codes, e.g. python main.py --museum ACM TPM to only run pipelines for ACM and TPM).
Choices: {', '.join(MUSEUM_CODES.values())}
Omit to run all museums.

"""

model_flag_help = f"""Run specific models only (case-insensitive keys, e.g. python main.py --models rf xgb lstm to only run the RF, XGB, and LSTM models).
Choices: {', '.join(MODEL_KEYS)}
Omit to run all models.
"""

def parse_args():
    # Set up the command-line argument parser
    parser = argparse.ArgumentParser(
        prog="python main.py",
        description="Run the museum visitorship forecasting pipeline.",
        formatter_class=argparse.RawTextHelpFormatter, # allows my single string help messages to use newslines to split lines
    )

    # --museum / -m flag for selecting specific museums to run
    parser.add_argument(
        "--museum", "-m",
        nargs="+",
        type=str,
        default=None,
        metavar="MUSEUM_CODE",
        help=museum_flag_help,
    )

    # --models / -M flag for selecting specific models to run
    parser.add_argument(
        "--models", "-M",
        nargs="+",
        type=str,
        default=None,
        metavar="MODEL",
        help=model_flag_help,
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


def resolve_model_selection(raw_keys):
    """
    Validate CLI model keys (case-insensitive) against the model registry.
    Prints one error line per invalid key; if none of the given keys are valid,
    exits without running anything. Valid keys among an otherwise invalid list
    still get run.
    """
    selected = []
    for raw_key in raw_keys:
        key = raw_key.lower()
        if key not in MODEL_KEYS:
            print(f'"{raw_key}" is not a valid model. Choose from: {", ".join(MODEL_KEYS)}.')
            continue
        if key not in selected:
            selected.append(key)

    # If no valid model keys were provided, exit without running anything
    if not selected:
        print("No valid models provided. Exiting now.")
        sys.exit(1)

    return selected
