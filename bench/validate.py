"""Validate benchmark definitions against installed chip kits."""

import argparse
from pathlib import Path
import re
import tomllib


def kit_root(definition: dict, pdk_root: Path) -> Path:
    if definition["family"] == "sky130A":
        return pdk_root / "ciel" / "sky130" / "versions" / definition["version"]
    if definition["family"] == "ihp-sg13g2":
        return pdk_root / "ciel" / "ihp-sg13" / "versions" / definition["version"]
    raise ValueError(f"Unsupported kit family: {definition['family']}")


def validate(definition_path: Path, pdk_root: Path) -> None:
    definitions = tomllib.loads(definition_path.read_text())
    for kit_name, definition in definitions.items():
        root = kit_root(definition, pdk_root)
        netlist_path = root / definition["netlist"]
        foundry_path = root / definition["foundry"]
        netlist = netlist_path.read_text()
        foundry = foundry_path.read_text()
        prefix = definition["library"] + "__" if definition["family"] == "sky130A" else "sg13g2_"
        for cell in definition["cells"]:
            full_name = prefix + cell
            if not re.search(rf"(?mi)^\s*\.subckt\s+{re.escape(full_name)}\s", netlist):
                raise ValueError(f"{kit_name}: {full_name} missing from {netlist_path}")
            if not re.search(rf'\bcell\s*\(\s*"?{re.escape(full_name)}"?\s*\)', foundry):
                raise ValueError(f"{kit_name}: {full_name} missing from {foundry_path}")
        print(f"{kit_name}: {len(definition['cells'])} of {len(definition['cells'])} cells present in netlist and Liberty")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--definition", type=Path, default=Path("bench/benchmark.toml"))
    parser.add_argument("--pdk-root", type=Path, default=Path("pdk"))
    args = parser.parse_args()
    validate(args.definition, args.pdk_root)


if __name__ == "__main__":
    main()
