import sys

from config import MUSEUM_CODES
from src.cli import parse_args, resolve_museum_selection, resolve_model_selection
from src.data.singstat_api import singstat_api
from src.data.raw_data import fetch_raw_data, load_raw_data, load_manual_data, warn_short_series
from src.pipeline import (
    run_museum_pipeline,
    regen_museum_outputs,
    write_tuning_report,
)

def main():
    # Ensure that our debug statements are printed in chronological order with the library logs.
    # This fixes an issue where optuna's first study's output prints before the museums banner
    sys.stdout.reconfigure(line_buffering=True)

    # Setup command-line argument passing
    args = parse_args()
    museums = resolve_museum_selection(args.museum) if args.museum else list(MUSEUM_CODES.keys())
    models = resolve_model_selection(args.models) if args.models else None

     # Regenerate outputs/ if requested, then exit
    if args.regen_outputs:
        for museum in museums:
            print(f"=== {museum} (regenerating outputs) ===")
            regen_museum_outputs(museum)
            print(f"=== {museum} complete ===\n")
        write_tuning_report()
        return

    # Update data/raw/ from SingStat if requested, then exit
    if args.call_singstat_api:
        try:
            fetch_raw_data()
        except RuntimeError as e:
            print(f"[data] API call failed: {e}")
            sys.exit(1)
        return

    # Museum visitorship and international arrivals, from the manual files if given, else
    # data/raw/ where the saved files cover the configured window, else the SingStat API
    try:
        if args.manual_data:
            visitors, arrivals = load_manual_data(*args.manual_data, museums)
        else:
            visitors, arrivals = load_raw_data(museums, refresh=args.refresh)
    except RuntimeError as e:
        print(f"[data] {e}")
        sys.exit(1)
    warn_short_series(visitors, museums)

    for museum in museums:
        print(f"=== {museum} ===")
        run_museum_pipeline(museum, visitors, arrivals, models)
        print(f"=== {museum} complete ===\n")

    write_tuning_report()


if __name__ == "__main__":
    main()
