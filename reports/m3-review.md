# Review of milestones 1 to 3

Reviewer: owner side, 2026-11-16. The agent's work was careful and honestly reported. The decision report cannot be used yet, because the hand-run test bench has a setup error and the CharLib figures show a setup fault.

## Finding 1 — the input ramp was too fast
The foundry table's input transition (0.122474 ns at the tested point) is a 20%-to-80% time with slew derating 1.0. A linear ramp with that 20%-to-80% time lasts 0.122474 / 0.6 = 0.204123 ns from 0 to 100%. The bench ramped 0 to 100% in 0.122474 ns.

Same deck with only the ramp corrected (`work/review-inv_1-ramp.cir`, ngspice 41), one grid point, four values:

| Table | Foundry (ns) | Milestone 2 bench | Corrected ramp |
|---|---:|---:|---:|
| `cell_fall` | 0.0873 | 0.0595 (-31.8%) | 0.0741 (-15.1%) |
| `cell_rise` | 0.1211 | 0.1070 (-11.6%) | 0.1304 (+7.6%) |
| `fall_transition` | 0.0599 | 0.0422 (-29.4%) | 0.0537 (-10.3%) |
| `rise_transition` | 0.0917 | 0.0935 (+2.0%) | 0.0955 (+4.2%) |

Median absolute error over these four values: 20.5% before, 9.0% after. This is one grid point of 49.

## Finding 2 — the netlist has no parasitics
The kit's `inv_1` sub-circuit is two transistors with width and length only: no wiring capacitance, no source or drain areas. The foundry table was characterised from an extracted layout. Missing capacitance makes a cell look faster, which fits the falling-edge results. Not yet measured.

## Finding 3 — the CharLib figures are not an accuracy measurement
A median of 53% and a worst case of 6795% across 3,724 points indicate a configuration or units fault, quite possibly the same transition-definition error as finding 1. They say nothing yet about how accurate CharLib is.

## Finding 4 — models were included file by file
The bench includes four individual model files. The kit's intended entry point is `sky130.lib.spice`, section `tt`. Effect unknown; cheap to check.

## What follows
Milestone 3b in `TASKS.md`. No decision among the three options until it is done.
