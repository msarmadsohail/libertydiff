# Blueprint

## What it is
A chip is built from a library of small logic cells: inverters, NAND gates, flip-flops. Before any design tool can use a cell it needs a data sheet: how long the cell takes to switch, how much power it draws and how much load its pins present, for every combination of input speed and output load. That data sheet is a Liberty file (`.lib`). The tool that produces it runs thousands of circuit simulations per cell and is called a characteriser.

This project is a free characteriser: cell netlists and transistor models in, a Liberty file out.

## What it stands in for
Cadence Liberate and Synopsys SiliconSmart, which are licensed commercial tools.

## Why it is checkable
The open chip kits (SkyWater 130 nm, GF 180 nm, IHP 130 nm) ship the foundry's own Liberty files next to the cell netlists. The tool characterises a cell and the result is compared number by number with the foundry file. No paid licence is needed anywhere. One cell, one timing arc and one corner form an independent pass/fail unit.

## The target
Not "the first open characteriser": CharLib and libretto exist. The target is a permissively licensed characteriser that publishes its measured error against the foundry Liberty files, cell by cell. That published error is the product.

Whether this is worth building is decided by measurement first (milestones 1 to 3 in `TASKS.md`), not assumed.

## Pipeline
1. Read the cell's transistor-level netlist and its logic function.
2. Find the arcs: for each input-to-output path, the other input values that let that path switch.
3. Build a test bench for each arc, input transition time and output load.
4. Simulate with ngspice, many runs in parallel.
5. Measure delay and transition at the thresholds the foundry file declares.
6. Write the Liberty file.
7. Compare against the foundry file and write the error report.

Language: Python, with ngspice run as a separate program.

## Layout
| Path | Holds | Tracked by git |
|---|---|---|
| `cellchar/` | The characteriser | yes |
| `checker/` | The comparison tool and the held-out cell list. The only code allowed to read the foundry file | yes |
| `scripts/` | Environment and helper scripts | yes |
| `reports/` | Measured results | yes |
| `docs/` | This file and the recorded measurement rules | yes |
| `.tools/`, `pdk/`, `work/` | Local tools, chip-kit data, scratch | no |

## Version 0 scope
SkyWater 130 nm, `sky130_fd_sc_hd`, one corner (typical, 25 °C, 1.8 V), ten combinational cells, delay and output-transition tables (the NLDM model) and input pin capacitance.

## The check
- Each table point is compared with the foundry value and the percentage error recorded. The tolerance that counts as a pass is set after the first measurements, because the foundry used a commercial simulator and an exact match is not possible.
- Four of the ten cells are held out: the characteriser is developed without them and run on them once at the end. The published figure comes from those.

## Known risks
- The free simulator may differ from the foundry's by more than any useful tolerance. Milestone 2 measures this on the simplest case.
- The foundry file states its thresholds but not every simulator option.
- Flip-flop setup and hold times need a search over input timing and are the hard part; version 0 leaves them out on purpose.
- A full library is hundreds of thousands of simulations.
- `vyges-tools/char`, a project with the same aim, first appeared in November 2026.
