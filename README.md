# libertydiff

Compare two Liberty (`.lib`) timing files point by point.

**Status: early.** The comparison tool works and is tested. A reproducible benchmark that uses it, on open chip kits, is being built; its results tables are not here yet.

## What it does

Given a generated Liberty file and a reference one, `libertydiff`:

- matches cells, timing arcs and tables between the two files;
- aligns table axes by variable name, not by position, so a table written load-first compares correctly against one written transition-first;
- reports every point: the value in each file, the percentage difference, and the absolute difference in picoseconds;
- lists points that exist in only one file instead of dropping them;
- summarises median and worst difference per cell and per table, always with the number of points compared.

It does not say which file is right. It measures differences.

## Install

Python 3.10 or newer. No dependencies outside the standard library.

```sh
git clone https://github.com/msarmadsohail/libertydiff.git
cd libertydiff
pip install -e .
```

## Use

```sh
# median and worst difference per cell and table
python -m libertydiff compare generated.lib reference.lib --summary

# one cell, every point written to a CSV file
python -m libertydiff compare generated.lib reference.lib --cells sky130_fd_sc_hd__inv_1 --csv points.csv
```

| Option | Meaning |
|---|---|
| `--cells A B ...` | compare only the named cells |
| `--summary` | print median and worst per cell and table |
| `--csv FILE` | write one row per point |
| `--json FILE` | write the differences and the summary as JSON |
| `--min-abs PS` | report separately the points whose absolute difference is below this many picoseconds |

`--min-abs` exists because a large percentage of a near-zero delay is not a meaningful error. Percentage and picosecond figures are always given together.

## Why it exists

Comparing a characterised cell against a foundry file is easy to get wrong in ways that still produce plausible numbers. Two such mistakes happened while this project was taking its first measurements:

- **The input transition was applied as the full ramp time.** The foundry tables define it as the 20%-to-80% time, so the full linear ramp lasts the table value divided by 0.6. Getting this wrong made one inverter point look 20% off when it was 9% off.
- **A table was read with its axes in the wrong order.** One tool writes load first and transition second. Reading it the other way round produced a median error of 53% and a worst case of 6795%, none of it real.

The tool handles the second case by construction. The first is a property of the test bench, and the benchmark states its ramp definition explicitly.

## First measurements

These came before the benchmark harness existed and cover three cells on two kits. They are here to show what the tool reports, not as a result about any library.

Generated with CharLib running ngspice 44.2 at each kit's typical corner, compared against the foundry Liberty file shipped with the kit. Delay and transition tables.

| Kit and cell | Netlist | Points compared | Median difference | Worst difference |
|---|---|---:|---:|---:|
| SkyWater 130 nm, `sky130_fd_sc_hd__inv_1` | extracted with Magic | 196 | 14.6% | 260.5% |
| SkyWater 130 nm, `sky130_fd_sc_hd__nand2_1` | schematic | 392 | 9.1% (15.0 ps) | 284.9% (224.7 ps) |
| IHP 130 nm, `sg13g2_inv_1` | schematic | 196 | 4.7% (15.3 ps) | 64.6% (240.7 ps) |

A hand-written ngspice test bench, independent of CharLib, was run on the same SkyWater inverter with the same extracted netlist. Its results matched CharLib's at 196 of 196 points, with a median difference between the two methods below 1 ps in each of the four tables. Against the foundry file the hand bench gave a median of 14.4% (15.8 ps) over the same 196 points.

How to read this:

- The two methods agree with each other and both differ from the foundry file, so the difference is unlikely to come from the characterisation method.
- In picoseconds the two kits look alike; the percentage is larger on the SkyWater inverter.
- The largest percentages are at the smallest load with the slowest input, where the delay itself is close to zero.
- Nothing here separates the effect of the transistor models from the effect of how each foundry file was produced.

## What this does not show

- Three cells is three cells. No statement is made about a whole library.
- Sequential cells, setup and hold times, power tables and the CCS model are not covered.
- How the foundry files were produced is not known.
- ngspice is the only simulator used.
- Nothing is compared with measured silicon.

## Planned

- One pinned container with ngspice, Magic and CharLib, so a run can be repeated exactly.
- A benchmark definition covering ten combinational cells on each of SkyWater `sky130_fd_sc_hd` and IHP `sg13g2_stdcell`, with schematic and extracted netlists.
- Results tables per kit, per cell and per table, with point counts, in percent and picoseconds.

## Tests

```sh
pip install -e ".[test]"
pytest
```

The tests use small fixtures and need no chip kit.

## Licence

Apache-2.0. A `LICENSE` file will be added with the first release.

CharLib, ngspice, Magic and the chip kits are separate projects under their own licences. They are used as external tools and data, and none of them is included in this repository.
