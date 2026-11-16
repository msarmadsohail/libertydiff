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

- [x] **2.2 Write the checker.** `libertydiff/compare.py` takes a generated Liberty file (or a small JSON of measured points) and the foundry file, and writes a table: cell, arc, table, point, generated value, foundry value, percentage error. It also prints the median and the worst error.
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

- [x] **3b.3 Full inverter grid.** Run all 49 points of `inv_1` for the four tables (196 points) with the corrected bench.
  Done when: `reports/m3b-inv-grid.md` gives median and worst error per table, and says where the error concentrates (small loads, large loads, fast inputs, slow inputs).

- [x] **3b.4 Parasitics.** The kit's `inv_1` netlist has two transistors and no wiring capacitance or junction areas, while the foundry table came from an extracted layout. Find out whether the kit ships extracted netlists. If not, extract `inv_1` from its layout under `libs.ref/sky130_fd_sc_hd/mag` with Magic (in Docker if needed), including parasitic capacitance, and rerun task 3b.3 on the extracted netlist.
  Done when: the report compares median and worst error per table, schematic netlist against extracted netlist, over the same 196 points.

- [x] **3b.5 Re-check the CharLib measurement.** A worst error of 6795% is a setup fault, not an accuracy figure. Look at the ten worst points and find the cause (units, thresholds, how the input transition is defined, missing points). Change only the configuration, not CharLib's code, and rerun `inv_1` only.
  Done when: `reports/m3b-charlib.md` names the cause and gives the `inv_1` error table before and after, with point counts.

- [x] **3b.6 STOP — revised decision report.** Rewrite the evidence for the three options in `reports/m3b-decision.md` using the corrected numbers. Do not choose. Stop.

## Milestone 3c — is the gap in the tools or in the kit? (branch `m3c-gap`)

Milestone 3b showed a hand-written bench and CharLib landing on almost the same error (median about 14 to 15% over 196 points). Two independent methods agreeing with each other but not with the foundry file points at the models or the foundry file, not at the characteriser. These tasks test that.

- [x] **3c.1 Do the two methods agree with each other?** Compare, point by point, the hand-run extracted grid against the CharLib extracted rerun for `inv_1` (196 points).
  Done when: `reports/m3c-agreement.md` gives the median and worst difference between the two methods, per table.

- [x] **3c.2 Report absolute error as well as percentage.** The owner authorises one change to `libertydiff/compare.py`: add an absolute-error column in picoseconds and print its median and worst. Percentages of near-zero delays (small load, slow input) are misleading on their own. The identity and 10% perturbation tests must still pass.
  Done when: the `inv_1` extracted grid is re-reported with both measures, and the report states how many of the 196 points are off by more than 10% and also by more than 5 ps.

- [x] **3c.3 A second cell.** Run CharLib on `nand2_1` with the schematic netlist and compare with the corrected checker.
  Done when: `reports/m3c-nand2.md` gives the per-table error with point counts, in both measures.

- [x] **3c.4 A second kit.** Fetch the IHP SG13G2 kit *(check how; `ciel` may support it)*, find its standard-cell Liberty file and netlists, read the Liberty header for how and with what tool it was produced, and run CharLib on its smallest inverter at the typical corner.
  Done when: `reports/m3c-ihp.md` gives the error table with point counts in both measures, and quotes whatever the header says about the tool that produced the file. If the kit cannot be fetched or run after three attempts, say why.

- [x] **3c.5 STOP — closing report.** `reports/m3c-closing.md`: state, with the numbers, whether the gap follows the kit (present on SkyWater, absent or different on IHP), follows the simulator (present on both), or cannot be told apart. Do not recommend. Stop.

## Change of direction (owner, 2026-11-17)

Milestones 1 to 3c answered the original question: a new characteriser is not worth building, because CharLib already matches an independent hand bench at 196 of 196 points, and the remaining error follows the chip kit. The old milestone 4 (build a characteriser) is cancelled.

What is worth publishing is what this repository already half is: **a tool that compares Liberty files point by point, and a reproducible benchmark of how closely open tools reproduce the foundry Liberty files on open chip kits.** Nobody publishes that table. Milestones 5 to 8 build it. Read `docs/SPEC.md` before starting.

There are no stop gates until task 8.5. If a task is blocked after three honest attempts, mark it `BLOCKED`, record why, and go on to the next task that does not depend on it.

## Milestone 5 — the comparison tool as a package (branch `m5-package`)

- [x] **5.1 Package layout.** Move the comparison code into a Python package `libertydiff/` with a `pyproject.toml` (name `libertydiff`, Apache-2.0, Python 3.10+, no dependencies outside the standard library unless one is justified in `PROGRESS.md`). Keep `checker/` as a thin wrapper or remove it and update every reference.
  Done when: `pip install -e .` works in a fresh virtual environment under `.venv/` and `python -m libertydiff --help` prints usage.

- [x] **5.2 Liberty reader.** One reader that returns, for every cell, pin, timing arc and table: the two axes with their variable names, the values, and the units from the library header. It must handle both axis orders (input transition first or load first), scalar tables, and quoted multi-line value lists.
  Done when: unit tests pass on small hand-written Liberty snippets for each of those cases, and the reader parses the SkyWater and IHP foundry files completely, reporting the cell and table counts.

- [x] **5.3 Comparison.** `libertydiff compare A.lib B.lib` matches cells, arcs and tables between two files, aligns axes by variable name not by position, and reports each point's value in both files, the percentage difference and the absolute difference in picoseconds. Points present in only one file are listed, never silently dropped. Options: `--cells` to restrict, `--csv` and `--json` outputs, `--summary` for median and worst per cell and per table.
  Done when: a file compared with itself gives zero at every point; a copy with one value changed by 10% reports exactly that point; a copy with axes swapped and values transposed reports zero difference; unit tests cover all three.

- [x] **5.4 Honest summaries.** The summary always prints the number of points compared and the number unmatched, and gives both percentage and picosecond figures. Add `--min-abs` so that points whose absolute difference is below a threshold can be reported separately, because a large percentage of a near-zero delay is not a meaningful error.
  Done when: unit tests cover the counts and the threshold, and the SkyWater `inv_1` comparison from milestone 3c is reproduced to the same figures.

- [ ] **5.5 Tests.** `pytest` runs the whole test suite in under a minute with no chip kit installed (tests use small fixtures under `tests/fixtures/`, never the foundry files).
  Done when: `pytest` passes in the fresh virtual environment and the number of tests is recorded.

## Milestone 6 — the benchmark harness (branch `m6-harness`)

- [ ] **6.1 One pinned container.** A single `docker/Dockerfile` with pinned versions of ngspice, Magic and CharLib (by commit), building reproducibly. Record the image digest.
  Done when: the image builds from scratch and `docker run` prints the three versions.

- [ ] **6.2 Benchmark definition.** `bench/benchmark.toml` lists, per chip kit: kit version, library, corner, foundry Liberty file, netlist source, and the cells. Start from: SkyWater `sky130_fd_sc_hd` with the ten cells used in milestone 3, and IHP `sg13g2_stdcell` with its ten nearest equivalents *(check the names)*.
  Done when: a script validates the file and confirms every listed cell exists in its kit's netlist and foundry Liberty file.

- [ ] **6.3 Runner.** `python -m bench.run --kit <name> [--cells ...]` fetches the kit if missing, runs CharLib in the container for each cell with the correct 20%-to-80% input transition and the foundry file's own grid, saves the generated Liberty file and a run record (versions, wall time, failures) under `work/`, and resumes after interruption without redoing finished cells.
  Done when: it reproduces the milestone 3c figures for SkyWater `inv_1` (schematic netlist) and IHP `sg13g2_inv_1` within 0.1 percentage point of the median.

- [ ] **6.4 Results tables.** `python -m bench.report` runs `libertydiff` on every finished cell and writes `results/<kit>.csv` (one row per point) and `results/<kit>.md` (one row per cell and table: points compared, points unmatched, median and worst in percent and picoseconds).
  Done when: both files exist for both kits and the Markdown tables carry the point counts.

- [ ] **6.5 Independent cross-check.** Keep the hand-written bench from milestone 3b as `bench/handbench.py`, able to run one cell's full grid without CharLib. Run it for one inverter per kit.
  Done when: `results/crosscheck.md` gives, per kit, the median and worst difference between CharLib and the hand bench over the stated number of points.

## Milestone 7 — run it (branch `m7-results`)

- [ ] **7.1 SkyWater, ten cells, schematic netlists.**
  Done when: `results/sky130_fd_sc_hd.md` covers all ten cells, or names each cell that failed and why.
- [ ] **7.2 SkyWater, ten cells, extracted netlists.** Extract each cell with Magic including parasitic capacitance and rerun.
  Done when: the results file shows schematic against extracted, per cell.
- [ ] **7.3 IHP, ten cells.**
  Done when: `results/sg13g2_stdcell.md` covers all ten or names the failures.
- [ ] **7.4 A third kit if it is cheap.** Try GF 180 nm (`gf180mcu_fd_sc_mcu7t5v0`) with five cells. Give it three attempts; if the kit or models will not run, record why and move on.
- [ ] **7.5 Second corner.** For each kit that worked, one slow and one fast corner on the inverter only, to show whether the gap moves with corner.
  Done when: the results state the figures per corner with point counts.

## Milestone 8 — make it publishable (branch `m8-release`)

- [ ] **8.1 README.** What the tool does, a two-minute quick start for `libertydiff compare`, how to reproduce the benchmark, the headline results table with point counts, and a "What this does not show" section taken from `docs/SPEC.md`. No claim that any tool or kit is wrong: the tables state differences, not blame.
- [ ] **8.2 Findings page.** `docs/findings.md`: the measured differences per kit, the two early mistakes that produced wrong figures (the ramp definition and the table orientation) and how they were caught, and what remains unexplained.
- [ ] **8.3 Licence and notices.** Apache-2.0 `LICENSE`. CharLib, ngspice and Magic are used as external tools inside the container and are not copied into this repository; state their licences and pinned versions in `docs/third-party.md`. Do not commit any foundry file. *(Check that the kits' licences allow publishing generated Liberty files; if unsure, publish the difference tables only and say so.)*
- [ ] **8.4 Continuous testing.** `.github/workflows/tests.yml` running `pytest` on Python 3.10 and 3.12. It cannot run until the owner publishes; verify it locally by running the same commands.
- [ ] **8.5 STOP — release candidate.** Create a branch `release` from `main` whose tree contains only what a user of the tool needs: `libertydiff/`, `bench/`, `docker/`, `tests/`, `results/`, `docs/findings.md`, `docs/third-party.md`, `README.md`, `LICENSE`, `pyproject.toml`, `.github/workflows/`, `.gitignore`. It must not contain `AGENTS.md`, `TASKS.md`, `PROGRESS.md`, `.github/agents/`, `.github/copilot-instructions.md`, `docs/BLUEPRINT.md`, `docs/SPEC.md`, `reports/` or `checker/`. Confirm `pytest` passes on that branch. Write `reports/m8-release.md` on `main` listing what is in the branch, every task that was blocked, and every figure in the README with the file it came from. Do not push. Stop.

## Out of scope
Writing a new characteriser. Flip-flops and latches, setup and hold times, power and leakage tables, the CCS model, a check with OpenSTA, publishing to PyPI, pushing to any remote.
