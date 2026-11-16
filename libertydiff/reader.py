"""Structural Liberty reader for NLDM timing tables."""

from dataclasses import dataclass
from pathlib import Path
import re


TIME_UNITS = {"s": 1e12, "ms": 1e9, "us": 1e6, "ns": 1e3, "ps": 1.0, "fs": 1e-3}
CAPACITANCE_UNITS = {"f": 1e15, "mf": 1e12, "uf": 1e9, "nf": 1e6, "pf": 1e3, "ff": 1.0, "af": 1e-3}


@dataclass(frozen=True)
class Units:
    time_ps: float
    capacitance_ff: float


@dataclass(frozen=True)
class Axis:
    name: str
    values: tuple[float, ...]


@dataclass(frozen=True)
class Table:
    cell: str
    pin: str
    related_pin: str
    name: str
    template: str
    axes: tuple[Axis, ...]
    values: tuple[float, ...]
    units: Units

    @property
    def arc(self) -> str:
        return f"{self.related_pin}->{self.pin}"


@dataclass(frozen=True)
class Library:
    cells: dict[str, tuple[Table, ...]]
    units: Units

    @property
    def tables(self) -> tuple[Table, ...]:
        return tuple(table for tables in self.cells.values() for table in tables)


TABLE_NAMES = {"cell_rise", "cell_fall", "rise_transition", "fall_transition"}
INPUT_AXES = {"input_net_transition", "input_transition_time", "related_pin_transition", "constrained_pin_transition"}
LOAD_AXES = {"total_output_net_capacitance", "output_net_capacitance", "load_capacitance"}
TOKEN = re.compile(r'"(?:[^"\\]|\\.)*"|[{}():;,\\]|[^\s{}():;,\\]+')
NUMBER = re.compile(r"[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?")


def _tokens(text: str) -> list[str]:
    text = re.sub(r"/\*.*?\*/", " ", text, flags=re.DOTALL)
    return TOKEN.findall(text)


def _unit_value(value: str, scales: dict[str, float], default: float) -> float:
    match = re.match(r"^\s*([-+0-9.eE]+)\s*([a-zA-Z]+)?\s*$", value.strip('"'))
    if not match:
        raise ValueError(f"Invalid unit: {value}")
    factor = float(match.group(1))
    suffix = (match.group(2) or "").lower()
    if suffix and suffix not in scales:
        raise ValueError(f"Unsupported unit: {value}")
    return factor * scales.get(suffix, default)


def _numbers(tokens: list[str]) -> tuple[float, ...]:
    values = []
    for token in tokens:
        if token == "\\":
            continue
        values.extend(float(item) for item in NUMBER.findall(token))
    return tuple(values)


def _parse_group(tokens: list[str], start: int) -> tuple[list[str], int]:
    if tokens[start] != "{":
        raise ValueError("Expected group")
    depth = 0
    for index in range(start, len(tokens)):
        if tokens[index] == "{":
            depth += 1
        elif tokens[index] == "}":
            depth -= 1
            if depth == 0:
                return tokens[start + 1:index], index + 1
    raise ValueError("Unclosed Liberty group")


def _members(tokens: list[str]):
    index = 0
    while index < len(tokens):
        name = tokens[index]
        if index + 1 < len(tokens) and tokens[index + 1] == ":":
            end = tokens.index(";", index + 2)
            yield name, None, tokens[index + 2:end]
            index = end + 1
        elif index + 1 < len(tokens) and tokens[index + 1] == "(":
            depth = 0
            end = index + 1
            while end < len(tokens):
                if tokens[end] == "(":
                    depth += 1
                elif tokens[end] == ")":
                    depth -= 1
                    if depth == 0:
                        break
                end += 1
            args = tokens[index + 2:end]
            if end + 1 < len(tokens) and tokens[end + 1] == "{":
                body, next_index = _parse_group(tokens, end + 1)
                yield name, args, body
                index = next_index
            else:
                yield name, args, []
                index = end + 1
        else:
            index += 1


def _attribute(tokens: list[str], name: str) -> str | None:
    for member_name, args, body in _members(tokens):
        if member_name == name and args is None:
            return " ".join(body).strip('"')
    return None


def _axis(templates: dict[str, tuple[str, ...]], template: str, index: int, values: tuple[float, ...]) -> Axis:
    name = templates.get(template, (None, None))[index - 1] if template in templates else None
    if name is None:
        raise ValueError(f"Unknown axis variable for template {template}: index_{index}")
    return Axis(name, values)


def read_library(path: str | Path) -> Library:
    """Read all NLDM timing tables, preserving axis variable names and header units."""
    path = Path(path)
    tokens = _tokens(path.read_text(encoding="utf-8"))
    if not tokens or tokens[0] != "library":
        raise ValueError(f"Not a Liberty file: {path}")
    start = tokens.index("{")
    library_body, _ = _parse_group(tokens, start)
    templates: dict[str, tuple[str, ...]] = {}
    cells: dict[str, tuple[Table, ...]] = {}
    time_unit = "1ns"
    capacitance_unit = "1pf"
    for name, args, body in _members(library_body):
        if name == "time_unit" and args is None:
            time_unit = " ".join(body).strip('"')
        elif name == "capacitive_load_unit" and args is not None:
            capacitance_unit = "".join(args).replace('"', "")
        elif name in {"lu_table_template", "power_lut_template"} and args is not None:
            template = args[0].strip('"')
            variables = []
            for variable_name, variable_args, variable_body in _members(body):
                if variable_name in {"variable_1", "variable_2"} and variable_args is None:
                    variables.append(" ".join(variable_body).strip('"'))
            templates[template] = tuple(variables)
        elif name == "cell" and args is not None:
            cell_name = args[0].strip('"')
            tables = []
            for pin_name, pin_args, pin_body in _members(body):
                if pin_name != "pin" or pin_args is None:
                    continue
                output = pin_args[0].strip('"')
                for timing_name, timing_args, timing_body in _members(pin_body):
                    if timing_name != "timing":
                        continue
                    related = _attribute(timing_body, "related_pin") or ""
                    for table_name, table_args, table_body in _members(timing_body):
                        if table_name not in TABLE_NAMES or table_args is None:
                            continue
                        template = table_args[0].strip('"')
                        axes: dict[int, tuple[float, ...]] = {}
                        values: tuple[float, ...] | None = None
                        for member_name, member_args, member_body in _members(table_body):
                            if member_name in {"index_1", "index_2"} and member_args is not None:
                                axes[int(member_name[-1])] = _numbers(member_args)
                            elif member_name == "values" and member_args is not None:
                                values = _numbers(member_args)
                        if values is None:
                            continue
                        if not axes:
                            if len(values) != 1:
                                raise ValueError(f"Scalar table has {len(values)} values")
                        elif len(values) != len(axes.get(1, ())) * len(axes.get(2, ())):
                            raise ValueError(f"Wrong value count in {cell_name} {table_name}")
                        axis_objects = tuple(_axis(templates, template, i, axes[i]) for i in sorted(axes))
                        tables.append(Table(cell_name, output, related, table_name, template,
                                            axis_objects, values, Units(1.0, 1.0)))
            cells[cell_name] = tuple(tables)
    units = Units(
        _unit_value(time_unit, TIME_UNITS, 1e3),
        _unit_value(capacitance_unit.split(",")[0], CAPACITANCE_UNITS, 1e3)
        * CAPACITANCE_UNITS.get(capacitance_unit.split(",")[-1].strip().strip('"').lower(), 1e3) / 1e3,
    )
    tables = tuple(table for cell_tables in cells.values() for table in cell_tables)
    cells = {
        name: tuple(Table(table.cell, table.pin, table.related_pin, table.name, table.template,
                          table.axes, table.values, units) for table in cell_tables)
        for name, cell_tables in cells.items()
    }
    return Library(cells, units)
