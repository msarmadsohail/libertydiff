"""Command-line entry point for libertydiff."""

import argparse

from .compare import main as compare_main


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="libertydiff",
        description="Compare Liberty timing tables point by point.",
    )
    subparsers = parser.add_subparsers(dest="command")
    compare_parser = subparsers.add_parser("compare", help="compare two Liberty files")
    compare_parser.add_argument("generated")
    compare_parser.add_argument("foundry")
    compare_parser.add_argument("--output", default="comparison.csv")
    args = parser.parse_args()
    if args.command == "compare":
        compare_main([args.generated, args.foundry, "--output", args.output])
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
