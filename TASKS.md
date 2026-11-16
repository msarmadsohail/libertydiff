# Tasks

Do them in order. Mark each `[x]` when its "Done when" check has been run and recorded in `PROGRESS.md`. Items marked *(check)* are unverified and must be confirmed by a command before they are relied on.

The ten cells used throughout milestones 2 to 4, all from `sky130_fd_sc_hd`:
`inv_1`, `inv_2`, `buf_1`, `nand2_1`, `nand3_1`, `nor2_1`, `nor3_1`, `and2_1`, `or2_1`, `xor2_1`.

The corner used throughout: typical transistors, 25 °C, 1.8 V.

## Milestone 1 — tools and inputs (branch `m1-tools`)

- [x] **1.1 Install ngspice locally.** Try a micromamba environment under `.tools/` (`micromamba-win-64` from the mamba-org releases page, `MAMBA_ROOT_PREFIX` inside `.tools/`, package `ngspice` from conda-forge) *(check)*. Fall back to the official Windows build, then to Docker.
  Done when: `ngspice --version` prints a version, and a three-line RC circuit simulates and its measured time constant is within 1% of R×C.

- [x] **1.2 Fetch the SkyWater 130 nm kit.** Use the `ciel` package (formerly `volare`) *(check the command; fetch only what is needed if it supports that)* into `pdk/`.
  Done when: these three files exist and their sizes are recorded *(check each path)*:
  the foundry Liberty file `sky130_fd_sc_hd__tt_025C_1v80.lib`, the cell netlists `sky130_fd_sc_hd.spice`, and the ngspice model file `sky130.lib.spice`.

- [x] **1.3 Write `scripts/env.ps1` and `scripts/env.sh`** that put the local tools on PATH for one shell and set a `PDK_ROOT` variable.
  Done when: a fresh shell that sources the script can run `ngspice --version`.

- [x] **1.4 Record the measurement rules.** Write `checker/read_rules.py`, which reads the foundry Liberty file header and prints: delay threshold, slew thresholds, slew derating factor if any, units, and for `inv_1` the input-transition grid and load-capacitance grid of its delay table. Save the output as `docs/measurement-rules.md`.
  Done when: the file exists and every value in it is followed by the line number it came from.

## Milestone 2 — one point by hand (branch `m2-smoke`)

- [x] **2.1 Simulate one inverter point.** Hand-write a test bench for `inv_1`: one input transition time and one load taken from the middle of the grid in `docs/measurement-rules.md`, rising and falling input.
  Done when: ngspice runs without errors and prints both delays and both output transition times, measured at the thresholds from task 1.4.

- [x] **2.2 Write the checker.** `checker/compare.py` takes a generated Liberty file (or a small JSON of measured points) and the foundry file, and writes a table: cell, arc, table, point, generated value, foundry value, percentage error. It also prints the median and the worst error.
  Done when: fed the foundry file against itself it reports zero error at every point, and fed a copy with one value changed by 10% it reports exactly that point.

- [x] **2.3 Compare the hand-run point.** Run the checker on the result of 2.1.
  Done when: `reports/m2-smoke.md` states the four percentage errors and the exact simulator options used.

- [x] **2.4 Simulator sensitivity.** Repeat 2.1 with a tighter time step and tighter tolerances.
  Done when: the report states how much the four numbers moved. If they moved by more than 1%, find settings where they stop moving and record them as the project defaults.

## Milestone 3 — measure the existing tools (branch `m3-incumbents`)

- [x] **3.1 CharLib.** Install `stineje/CharLib` under `.tools/`, run it on the ten cells at the corner above, and run the checker on its output.
  Done when: `reports/m3-charlib.md` holds the per-cell error table, with the number of table points compared for each cell, or a precise account of why it could not be run.

- [x] **3.2 libretto.** Same for `snishizawa/libretto`.
  Done when: `reports/m3-libretto.md` exists in the same form.

- [x] **3.3 Read the others.** Read the README and code layout of `vyges-tools/char` and of lctime from the LibreCell project (hosted on Codeberg) *(check the location)*. Do not install them.
  Done when: `reports/m3-others.md` states, for each, the licence, what it claims to produce, whether it publishes any accuracy figure against a foundry file, and the date of its last change.

- [x] **3.4 STOP — decision report.** Write `reports/m3-decision.md` with: the hand-run inverter errors from milestone 2; each existing tool's median and worst error per cell with the point counts; how long each took; and which of these three the numbers support:
  1. an existing tool is already within a few percent everywhere, so contribute there;
  2. the hand-run point is itself far off, so the simulator is the limit;
  3. existing tools are well off but the hand-run point is close, so build.
  Do not choose. State the evidence and stop.

## Milestone 3b — fix the test bench, then measure again (branch `m3b-bench`)

An owner-side review of milestone 2 found the hand-run test bench was wrong, so the milestone 3 decision report cannot be used yet. See `reports/m3-review.md`.

- [x] **3b.1 Correct the input ramp.** The foundry table's input transition is a 20%-to-80% time with slew derating 1.0, so the full 0-to-100% linear ramp lasts transition / 0.6. The milestone 2 bench used the transition value as the full ramp. Fix the bench and rerun the task 2.1 point.
  Done when: `reports/m3b-ramp.md` shows the four errors before and after. The review measured about -15%, +8%, -10% and +4% after the fix; a result far from those means something else changed.

- [x] **3b.2 Load the models the kit's way.** Replace the four hand-picked model includes with the kit's top-level file `sky130.lib.spice`, section `tt`, and rerun the same point.
  Done when: the report states how much each of the four numbers moved.

- [ ] **3b.3 Full inverter grid.** Run all 49 points of `inv_1` for the four tables (196 points) with the corrected bench.
  Done when: `reports/m3b-inv-grid.md` gives median and worst error per table, and says where the error concentrates (small loads, large loads, fast inputs, slow inputs).

- [ ] **3b.4 Parasitics.** The kit's `inv_1` netlist has two transistors and no wiring capacitance or junction areas, while the foundry table came from an extracted layout. Find out whether the kit ships extracted netlists. If not, extract `inv_1` from its layout under `libs.ref/sky130_fd_sc_hd/mag` with Magic (in Docker if needed), including parasitic capacitance, and rerun task 3b.3 on the extracted netlist.
  Done when: the report compares median and worst error per table, schematic netlist against extracted netlist, over the same 196 points.

- [ ] **3b.5 Re-check the CharLib measurement.** A worst error of 6795% is a setup fault, not an accuracy figure. Look at the ten worst points and find the cause (units, thresholds, how the input transition is defined, missing points). Change only the configuration, not CharLib's code, and rerun `inv_1` only.
  Done when: `reports/m3b-charlib.md` names the cause and gives the `inv_1` error table before and after, with point counts.

- [ ] **3b.6 STOP — revised decision report.** Rewrite the evidence for the three options in `reports/m3b-decision.md` using the corrected numbers. Do not choose. Stop.

## Milestone 4 — version 0 (branch `m4-v0`), only after the owner opens it

- [ ] **4.1 Fix the held-out list.** Write `checker/heldout.txt` with four of the ten cells, chosen by the owner. Code under `cellchar/` is developed against the other six only.
- [ ] **4.2 Netlist reader.** `cellchar/netlist.py` extracts one cell's sub-circuit and its pin list from the kit's netlist file.
  Done when: unit tests cover all ten cells and the pin lists match the kit's own cell documentation.
- [ ] **4.3 Arc finder.** Given a cell's logic function, list every input-to-output path and the values of the other inputs that let it switch.
  Done when: unit tests cover all ten cells; `xor2_1` has both of its non-unate arcs.
- [ ] **4.4 Test-bench writer.** Generate the ngspice deck for one arc, one input transition, one load, using the project default options from task 2.4.
  Done when: the generated deck for the 2.1 point gives the same four numbers as the hand-written one, within 0.1%.
- [ ] **4.5 Runner.** Run all points of a cell in parallel, with a timeout per run and a retry, and collect the measurements.
  Done when: `inv_1` completes and the run time and failure count are recorded.
- [ ] **4.6 Liberty writer.** Write delay tables, transition tables and input pin capacitance in Liberty syntax.
  Done when: the checker parses the output without errors.
- [ ] **4.7 Six-cell run.** Characterise the six development cells and run the checker.
  Done when: `reports/m4-dev.md` holds the per-cell error table with point counts.
- [ ] **4.8 STOP — held-out run.** Characterise the four held-out cells once, with no code changes afterwards, and write `reports/m4-heldout.md`. Stop.

## Out of scope until the owner opens it
Flip-flops and latches, setup and hold times, power and leakage, other corners, GF 180 nm and IHP 130 nm, the CCS model, a second check with OpenSTA, packaging and a public release.
