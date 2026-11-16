"""Compare Liberty timing tables by cell, arc, table and named axes."""

from dataclasses import asdict, dataclass
import csv
import json
import math
from pathlib import Path
import statistics

from .reader import Library, Table, read_library


@dataclass(frozen=True)
class PointDifference:
    cell: str
    arc: str
    table: str
    axes: dict[str, float]
    value_a: float
    value_b: float
    percentage_difference: float | None
    absolute_difference_ps: float


@dataclass(frozen=True)
class UnmatchedTable:
    cell: str
    arc: str
    table: str
    present_in: str
    points: int


@dataclass(frozen=True)
class Summary:
    cell: str
    table: str
    points_compared: int
    points_unmatched: int
    median_percentage: float | None
    worst_percentage: float | None
    median_absolute_ps: float
    worst_absolute_ps: float


@dataclass(frozen=True)
class Comparison:
    differences: tuple[PointDifference, ...]
    unmatched: tuple[UnmatchedTable, ...]

    def summary(self, min_abs: float = 0.0) -> tuple[Summary, ...]:
        groups: dict[tuple[str, str], list[PointDifference]] = {}
        for difference in self.differences:
            groups.setdefault((difference.cell, difference.table), []).append(difference)
        unmatched_counts: dict[tuple[str, str], int] = {}
        for unmatched in self.unmatched:
            key = (unmatched.cell, unmatched.table)
            unmatched_counts[key] = unmatched_counts.get(key, 0) + unmatched.points
        summaries = []
        for (cell, table), points in sorted(groups.items()):
            included = [point for point in points if abs(point.absolute_difference_ps) >= min_abs]
            percentages = [abs(point.percentage_difference) for point in included
                           if point.percentage_difference is not None and math.isfinite(point.percentage_difference)]
            absolute = [abs(point.absolute_difference_ps) for point in included]
            summaries.append(Summary(
                cell, table, len(included), unmatched_counts.get((cell, table), 0),
                statistics.median(percentages) if percentages else None,
                max(percentages) if percentages else None,
                statistics.median(absolute) if absolute else 0.0,
                max(absolute) if absolute else 0.0,
            ))
        for (cell, table), count in sorted(unmatched_counts.items()):
            if (cell, table) not in groups:
                summaries.append(Summary(cell, table, 0, count, None, None, 0.0, 0.0))
        return tuple(summaries)


def _table_map(library: Library) -> dict[tuple[str, str, str], Table]:
    return {(table.cell, table.arc, table.name): table for table in library.tables}


def _point_values(table: Table) -> dict[tuple[tuple[str, float], ...], float]:
    if not table.axes:
        return {(): table.values[0]}
    if len(table.axes) != 2:
        raise ValueError(f"Unsupported axis count in {table.cell} {table.name}")
    first, second = table.axes
    return {
        tuple(sorted(((first.name, first.values[row]), (second.name, second.values[column])))): value
        for row in range(len(first.values))
        for column in range(len(second.values))
        for value in [table.values[row * len(second.values) + column]]
    }


def compare_libraries(a: Library, b: Library) -> Comparison:
    """Compare A against B; all values are converted to picoseconds using header units."""
    tables_a = _table_map(a)
    tables_b = _table_map(b)
    differences = []
    unmatched = []
    for key in sorted(tables_a.keys() | tables_b.keys()):
        if key not in tables_a:
            table = tables_b[key]
            unmatched.append(UnmatchedTable(key[0], key[1], key[2], "B", math.prod(len(axis.values) for axis in table.axes) or 1))
            continue
        if key not in tables_b:
            table = tables_a[key]
            unmatched.append(UnmatchedTable(key[0], key[1], key[2], "A", math.prod(len(axis.values) for axis in table.axes) or 1))
            continue
        table_a, table_b = tables_a[key], tables_b[key]
        points_a = _point_values(table_a)
        points_b = _point_values(table_b)
        if set(points_a) != set(points_b):
            missing = len(set(points_a) ^ set(points_b))
            unmatched.append(UnmatchedTable(key[0], key[1], key[2], "axes", missing))
        for axes in sorted(points_a.keys() & points_b.keys()):
            value_a = points_a[axes] * a.units.time_ps
            value_b = points_b[axes] * b.units.time_ps
            absolute = value_a - value_b
            percentage = absolute / value_b * 100 if value_b != 0 else None
            differences.append(PointDifference(key[0], key[1], key[2], dict(axes), value_a, value_b,
                                               percentage, absolute))
    return Comparison(tuple(differences), tuple(unmatched))


def compare_paths(a: str | Path, b: str | Path, cells: list[str] | None = None) -> Comparison:
    library_a = read_library(a)
    library_b = read_library(b)
    if cells is not None:
        selected = set(cells)
        library_a = Library({name: tables for name, tables in library_a.cells.items() if name in selected}, library_a.units)
        library_b = Library({name: tables for name, tables in library_b.cells.items() if name in selected}, library_b.units)
    return compare_libraries(library_a, library_b)


def write_csv(comparison: Comparison, path: str | Path) -> None:
    with Path(path).open("w", newline="", encoding="utf-8") as stream:
        fields = ["cell", "arc", "table", "axes", "value_a", "value_b",
                  "percentage_difference", "absolute_difference_ps"]
        writer = csv.DictWriter(stream, fieldnames=fields)
        writer.writeheader()
        for point in comparison.differences:
            writer.writerow({
                "cell": point.cell, "arc": point.arc, "table": point.table,
                "axes": json.dumps(point.axes, sort_keys=True),
                "value_a": point.value_a, "value_b": point.value_b,
                "percentage_difference": point.percentage_difference,
                "absolute_difference_ps": point.absolute_difference_ps,
            })


def write_json(comparison: Comparison, path: str | Path, min_abs: float = 0.0) -> None:
    payload = {
        "points_compared": len(comparison.differences),
        "points_unmatched": sum(item.points for item in comparison.unmatched),
        "differences": [asdict(point) for point in comparison.differences],
        "unmatched": [asdict(item) for item in comparison.unmatched],
        "summary": [asdict(item) for item in comparison.summary(min_abs)],
    }
    Path(path).write_text(json.dumps(payload, indent=2), encoding="utf-8")


def summary_text(comparison: Comparison, min_abs: float = 0.0) -> str:
    lines = [f"Compared {len(comparison.differences)} points; unmatched {sum(item.points for item in comparison.unmatched)} points; min-abs {min_abs:g} ps"]
    lines.append("cell | table | compared | unmatched | median % | worst % | median ps | worst ps")
    for item in comparison.summary(min_abs):
        median_pct = "n/a" if item.median_percentage is None else f"{item.median_percentage:.6g}"
        worst_pct = "n/a" if item.worst_percentage is None else f"{item.worst_percentage:.6g}"
        lines.append(f"{item.cell} | {item.table} | {item.points_compared} | {item.points_unmatched} | {median_pct} | {worst_pct} | {item.median_absolute_ps:.6g} | {item.worst_absolute_ps:.6g}")
    if comparison.unmatched:
        lines.append("Unmatched tables:")
        for item in comparison.unmatched:
            lines.append(f"{item.cell} | {item.arc} | {item.table} | {item.present_in} | {item.points}")
    return "\n".join(lines)
