"""Print measurement rules with their source lines in the foundry Liberty file."""

import argparse
import re
from pathlib import Path


def source(path: Path, number: int) -> str:
    return f"{path.name}:{number}"


def assignment(lines: list[str], name: str) -> tuple[str, int]:
    pattern = re.compile(rf"^\s*{re.escape(name)}\s*:\s*(.+?)\s*;\s*$")
    for number, line in enumerate(lines, 1):
        match = pattern.match(line)
        if match:
            return match.group(1).strip('"'), number
    raise ValueError(f"Missing library attribute: {name}")


def cell_fall_table(lines: list[str]) -> tuple[int, int, int]:
    cell_pattern = re.compile(r'^\s*cell \("sky130_fd_sc_hd__inv_1"\) \{\s*$')
    start = next(i for i, line in enumerate(lines) if cell_pattern.match(line))
    depth = 0
    for i in range(start, len(lines)):
        depth += lines[i].count("{") - lines[i].count("}")
        if depth == 0:
            raise ValueError("inv_1 has no cell_fall delay table")
        if re.match(r'^\s*cell_fall \("del_1_7_7"\) \{\s*$', lines[i]):
            table_start = i
            break
    index_1 = table_start + 1
    index_2 = table_start + 2
    if "index_1" not in lines[index_1] or "index_2" not in lines[index_2]:
        raise ValueError("Unexpected inv_1 cell_fall table layout")
    return table_start + 1, index_1 + 1, index_2 + 1


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("liberty", type=Path)
    args = parser.parse_args()
    lines = args.liberty.read_text(encoding="utf-8").splitlines()

    print("# Measurement rules")
    print()
    print(f"Source: `{args.liberty}`")
    print()
    print("## Thresholds and units")
    print()
    names = [
        "input_threshold_pct_rise",
        "input_threshold_pct_fall",
        "output_threshold_pct_rise",
        "output_threshold_pct_fall",
        "slew_lower_threshold_pct_rise",
        "slew_lower_threshold_pct_fall",
        "slew_upper_threshold_pct_rise",
        "slew_upper_threshold_pct_fall",
        "slew_derate_from_library",
        "time_unit",
        "voltage_unit",
        "current_unit",
        "leakage_power_unit",
        "pulling_resistance_unit",
    ]
    for name in names:
        value, number = assignment(lines, name)
        print(f"- `{name}`: {value} ({source(args.liberty, number)})")
    for number, line in enumerate(lines, 1):
        if "capacitive_load_unit" in line:
            print(f"- `capacitive_load_unit`: {line.strip()} ({source(args.liberty, number)})")
            break

    table, index_1, index_2 = cell_fall_table(lines)
    print()
    print("## `inv_1` delay-table grids")
    print()
    print(f"Table: `cell_fall (\"del_1_7_7\")` ({source(args.liberty, table)})")
    print(f"- Input-transition grid, `index_1`: {lines[index_1 - 1].strip()} ({source(args.liberty, index_1)})")
    print(f"- Load-capacitance grid, `index_2`: {lines[index_2 - 1].strip()} ({source(args.liberty, index_2)})")


if __name__ == "__main__":
    main()
