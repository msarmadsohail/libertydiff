"""Command-line entry point for libertydiff."""

import argparse

from .diff import compare_paths, summary_text, write_csv, write_json


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="libertydiff",
        description="Compare Liberty timing tables point by point.",
    )
    subparsers = parser.add_subparsers(dest="command")
    compare_parser = subparsers.add_parser("compare", help="compare two Liberty files")
    compare_parser.add_argument("generated")
    compare_parser.add_argument("foundry")
    compare_parser.add_argument("--cells", nargs="+", help="restrict comparison to named cells")
    compare_parser.add_argument("--csv", help="write point differences as CSV")
    compare_parser.add_argument("--json", help="write differences and summary as JSON")
    compare_parser.add_argument("--summary", action="store_true", help="print median and worst per cell and table")
    compare_parser.add_argument("--min-abs", type=float, default=0.0, help="summary threshold in picoseconds")
    args = parser.parse_args()
    if args.command == "compare":
        comparison = compare_paths(args.generated, args.foundry, args.cells)
        if args.csv:
            write_csv(comparison, args.csv)
        if args.json:
            write_json(comparison, args.json, args.min_abs)
        if args.summary or not (args.csv or args.json):
            print(summary_text(comparison, args.min_abs))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
