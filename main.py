import sys

from config import MUSEUM_CODES
from src.cli import parse_args, resolve_museum_selection, resolve_model_selection
from src.data.raw_data import load_raw_data
from src.pipeline import run_museum_pipeline


def main():
    # Ensure that our debug statements are printed in chronological order with the library logs.
    # This fixes an issue where optuna's first study's output prints before the museums banner
    sys.stdout.reconfigure(line_buffering=True)

    # Setup command-line argument passing
    args = parse_args()
    museums = resolve_museum_selection(args.museum) if args.museum else list(MUSEUM_CODES.keys())
    models = resolve_model_selection(args.models) if args.models else None

    # Museum visitorship and international arrivals, from data/raw/ where the saved
    # files already cover the configured window, else from the SingStat API
    try:
        visitors, arrivals = load_raw_data(museums, refresh=args.refresh)
    except RuntimeError as e:
        print(f"[data] API call failed: {e}")
        sys.exit(1)

    for museum in museums:
        print(f"=== {museum} ===")
        run_museum_pipeline(museum, visitors, arrivals, models)
        print(f"=== {museum} complete ===\n")


if __name__ == "__main__":
    main()
