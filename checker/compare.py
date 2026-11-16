"""Compare generated NLDM timing points with a foundry Liberty file."""

import argparse
import csv
import json
import re
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path

TABLES = ("cell_rise", "cell_fall", "rise_transition", "fall_transition")


@dataclass(frozen=True)
class Point:
    cell: str
    arc: str
    table: str
    input_transition: float
    load: float
    value: float


def blocks(text: str, header: re.Pattern[str]):
    for match in header.finditer(text):
        start = match.end() - 1
        depth = 0
        for end in range(start, len(text)):
            if text[end] == "{":
                depth += 1
            elif text[end] == "}":
                depth -= 1
                if depth == 0:
                    yield match, text[start + 1:end]
                    break


def attribute(body: str, name: str) -> str | None:
    match = re.search(rf"\b{re.escape(name)}\s*:\s*([^;]+);", body)
    return match.group(1).strip().strip('"') if match else None


def index(body: str, name: str) -> list[float]:
    match = re.search(rf"\b{name}\s*\((.*?)\)\s*;", body, re.DOTALL)
    if not match:
        raise ValueError(f"Missing {name}")
    return [float(value) for value in match.group(1).strip().strip('"').split(",")]


def table_values(body: str) -> list[float]:
    match = re.search(r"\bvalues\s*\((.*?)\)\s*;", body, re.DOTALL)
    if not match:
        raise ValueError("Missing table values")
    return [float(value) for value in re.findall(r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?", match.group(1))]


def read_liberty(path: Path) -> dict[tuple, Point]:
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.DOTALL)
    tokens = re.findall(r'"[^"\n]*"|[{}():;,\\]|[^\s{}():;,\\]+', text)
    points = {}
    cell = output = related = None
    timing_related = None
    i = 0

    def skip_group(start: int) -> int:
        depth = 0
        while start < len(tokens):
            if tokens[start] == "{":
                depth += 1
            elif tokens[start] == "}":
                depth -= 1
                if depth == 0:
                    return start + 1
            start += 1
        raise ValueError("Unclosed Liberty group")

    def parse_table(start: int, table: str) -> int:
        end = skip_group(start)
        body = " ".join(tokens[start + 1:end - 1])
        nonlocal timing_related
        if "index_1" not in body or "values" not in body:
            return end
        arc_related = timing_related if timing_related is not None else related
        first = index(body, "index_1")
        second = index(body, "index_2")
        if "input_net_transition" in body or "input_transition_time" in body:
            inputs, loads = first, second
        elif abs(first[0] - 0.01) < abs(second[0] - 0.01):
            inputs, loads = first, second
        else:
            inputs, loads = second, first
        values = table_values(body)
        if len(values) != len(inputs) * len(loads):
            raise ValueError(f"Wrong value count for {cell} {arc_related}->{output} {table}")
        for row, input_transition in enumerate(inputs):
            for column, load in enumerate(loads):
                value = values[row * len(loads) + column]
                point = Point(cell, f"{arc_related}->{output}", table, input_transition, load, value)
                points[(cell, point.arc, table, row, column)] = point
        return end

    while i < len(tokens):
        token = tokens[i]
        if token == "cell" and i + 1 < len(tokens) and tokens[i + 1] == "(":
            cell = tokens[i + 2].strip('"')
            output = None
            related = None
            i += 3
        elif token == "pin" and cell is not None and i + 1 < len(tokens) and tokens[i + 1] == "(":
            output = tokens[i + 2].strip('"')
            related = None
            i += 3
        elif token == "pg_pin":
            i = skip_group(next(j for j in range(i, len(tokens)) if tokens[j] == "{"))
        elif token == "timing":
            start = next(j for j in range(i, len(tokens)) if tokens[j] == "{")
            end = skip_group(start)
            timing_related = next(
                (tokens[j + 2].strip('"') for j in range(start, end - 2)
                 if tokens[j] == "related_pin" and tokens[j + 1] == ":"),
                None,
            )
            i += 1
        elif token == "related_pin" and i + 1 < len(tokens) and tokens[i + 1] == ":":
            related = tokens[i + 2].strip('"')
            i += 3
        elif token in ("internal_power", "leakage_power"):
            i = skip_group(next(j for j in range(i, len(tokens)) if tokens[j] == "{"))
        elif token in TABLES and (related is not None or timing_related is not None):
            while i < len(tokens) and tokens[i] != "{":
                i += 1
            i = parse_table(i, token)
        else:
            i += 1
    return points


def read_json(path: Path) -> dict[tuple, Point]:
    records = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(records, dict):
        records = records["points"]
    points = {}
    for record in records:
        point = Point(
            cell=record["cell"],
            arc=record["arc"],
            table=record["table"],
            input_transition=float(record["input_transition"]),
            load=float(record["load"]),
            value=float(record["value"]),
        )
        key = (point.cell, point.arc, point.table, point.input_transition, point.load)
        points[key] = point
    return points


def match_foundry(point: Point, foundry_by_value: dict[tuple, list[Point]]) -> Point:
    key = (point.cell, point.arc, point.table, point.input_transition, point.load)
    candidates = foundry_by_value.get(key, [])
    if len(candidates) != 1:
        raise ValueError(f"No unique foundry point for {point}")
    return candidates[0]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("generated", type=Path, help="Generated Liberty file or JSON point list")
    parser.add_argument("foundry", type=Path, help="Foundry Liberty file")
    parser.add_argument("--output", type=Path, default=Path("comparison.csv"))
    args = parser.parse_args()

    foundry = read_liberty(args.foundry)
    generated = read_liberty(args.generated) if args.generated.suffix == ".lib" else read_json(args.generated)
    foundry_by_value = {}
    for candidate in foundry.values():
        key = (candidate.cell, candidate.arc, candidate.table, candidate.input_transition, candidate.load)
        foundry_by_value.setdefault(key, []).append(candidate)
    rows = []
    for key, generated_point in generated.items():
        if args.generated.suffix == ".lib":
            foundry_point = foundry[key]
        else:
            foundry_point = match_foundry(generated_point, foundry_by_value)
        error = (generated_point.value - foundry_point.value) / foundry_point.value * 100
        rows.append({
            "cell": generated_point.cell,
            "arc": generated_point.arc,
            "table": generated_point.table,
            "point": f"{generated_point.input_transition:g},{generated_point.load:g}",
            "generated": generated_point.value,
            "foundry": foundry_point.value,
            "percentage_error": error,
        })
    with args.output.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]) if rows else ["cell"])
        writer.writeheader()
        writer.writerows(rows)
    errors = [abs(row["percentage_error"]) for row in rows]
    print(f"Compared {len(rows)} points; report: {args.output}")
    if errors:
        print(f"Median absolute error: {statistics.median(errors):.6g}%")
        print(f"Worst absolute error: {max(errors):.6g}%")
        for row in rows:
            if abs(row["percentage_error"]) > 1e-9:
                print(row)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, json.JSONDecodeError) as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(1)
