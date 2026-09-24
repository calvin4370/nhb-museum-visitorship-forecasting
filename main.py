import os

from config import MUSEUM_CODES, START_YEAR, START_MONTH, END_YEAR, END_MONTH
from src.cli import parse_args, resolve_museum_selection, resolve_model_selection
from src.data.singstat_api import singstat_api
from src.pipeline import run_museum_pipeline


def main():
    # Setup command-line argument passing
    args = parse_args()
    museums = resolve_museum_selection(args.museum) if args.museum else list(MUSEUM_CODES.keys())
    models = resolve_model_selection(args.models) if args.models else None

    # Call SingStat API to retrieve museum visitorship and international arrivals data
    visitors = singstat_api("M891071", START_YEAR, START_MONTH, END_YEAR, END_MONTH)
    arrivals = singstat_api("M550001", START_YEAR, START_MONTH, END_YEAR, END_MONTH)

    # Save to csv
    os.makedirs("./data/raw", exist_ok=True)
    visitors.to_csv("./data/raw/museum_ts.csv", index=False)
    arrivals.to_csv("./data/raw/intl_arrivals.csv", index=False)

    for museum in museums:
        print(f"=== {museum} ===")
        run_museum_pipeline(museum, visitors, arrivals, models)
        print(f"=== {museum} complete ===\n")


if __name__ == "__main__":
    main()
