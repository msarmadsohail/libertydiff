# Progress log

Append one entry per task. Never rewrite an earlier entry; correct it with a new one.

Entry form:

```
## YYYY-MM-DD — task <id> — done | blocked
What was done:
Command that proves it:
Result:
Surprises or open points:
```

## 2026-11-16 — setup — done
What was done: repository created with `AGENTS.md`, `TASKS.md`, `docs/BLUEPRINT.md`. No tools installed, no code written.
Command that proves it: `git log --oneline`
Result: one commit.
Surprises or open points: no remote repository exists yet. A GitHub search on this date found CharLib (72 stars), libretto (41 stars) and vyges-tools/char (0 stars); that search read titles and descriptions only.

## 2026-11-16 — task 1.1 — done
What was done: installed micromamba 2.10.0 under `.tools/` and ngspice 41 from conda-forge in `.tools/envs/ngspice/`; added the ignored `.tools/bin/ngspice.cmd` console wrapper. Simulated a 1 kOhm, 1 uF RC charging circuit with a 1 ns input edge and measured the 63.21205588% crossing.
Command that proves it: `$env:Path = (Resolve-Path '.tools\bin').Path + ';' + $env:Path; ngspice --version; ngspice -b work/m1-rc.cir -o work/m1-rc.out` followed by parsing `tau` and checking `abs(tau - 0.001) / 0.001 * 100 < 1`.
Result: ngspice-41; measured tau 0.001 s, R*C 0.001 s, error 0% (within 1%).
Surprises or open points: the conda package's `ngspice.exe` is a GUI executable and prints no console version; its included `ngspice_con.exe` does. The wrapper selects the console executable. The RC deck and output are retained under ignored `work/`.

## 2026-11-16 — task 1.2 — done
What was done: used ciel 3.2.0 to fetch sky130A version e7a6777d157a9d94c7ac757457b9e4309e9e9000 into `pdk/`, including only `sky130_fd_sc_hd` and `sky130_fd_pr` plus the common files. Added no project dependency: ciel is run locally with `uv` and its source is under ignored `.tools/src/ciel/`.
Command that proves it: `$root = 'pdk/ciel/sky130/versions/e7a6777d157a9d94c7ac757457b9e4309e9e9000/sky130A'; Get-Item "$root/libs.ref/sky130_fd_sc_hd/lib/sky130_fd_sc_hd__tt_025C_1v80.lib", "$root/libs.ref/sky130_fd_sc_hd/spice/sky130_fd_sc_hd.spice", "$root/libs.tech/ngspice/sky130.lib.spice" | Select-Object FullName,Length`.
Result: foundry Liberty 12,841,637 bytes; cell netlists 926,412 bytes; ngspice model file 16,541 bytes. All three paths exist under the sky130A variant.
Surprises or open points: ciel 3.2.0 failed on Windows with WinError 32 because its Zstandard archive stream remained open during cleanup. A local source copy closes that stream with a context manager; the retry succeeded. The fetch also populated sky130B from the common archive, but the recorded inputs are specifically sky130A.

## 2026-11-16 — task 1.3 — done
What was done: wrote `scripts/env.ps1` and `scripts/env.sh` to prepend the local ngspice tools to PATH for the current shell and set `PDK_ROOT` to the fetched version directory and `PDK` to `sky130A`.
Command that proves it: `powershell.exe -NoProfile -ExecutionPolicy Bypass -Command ". '.\scripts\env.ps1'; ngspice --version; Write-Output ('PDK_ROOT=' + `$env:PDK_ROOT)"` and `& 'C:\Program Files\Git\bin\bash.exe' -c 'source scripts/env.sh && ngspice_con.exe --version && echo "PDK_ROOT=$PDK_ROOT"'`.
Result: both fresh shells printed ngspice-41 and the repository-local PDK_ROOT.
Surprises or open points: this machine's PowerShell execution policy blocks scripts by default, so the fresh-shell check uses a process-only `-ExecutionPolicy Bypass`; no system setting was changed. PowerShell uses the console-wrapper command `ngspice`; Bash calls `ngspice_con.exe` directly.

## 2026-11-16 — task 1.4 — done
What was done: wrote `checker/read_rules.py`, which reads the foundry Liberty header and the `inv_1` `cell_fall` table and prints thresholds, slew derating, units and both grids with source line numbers. Generated `docs/measurement-rules.md` from its output.
Command that proves it: `python checker/read_rules.py pdk/ciel/sky130/versions/e7a6777d157a9d94c7ac757457b9e4309e9e9000/sky130A/libs.ref/sky130_fd_sc_hd/lib/sky130_fd_sc_hd__tt_025C_1v80.lib | Tee-Object docs/measurement-rules.md`; then parse every `.lib:<line>` reference and check it is within the 12,841,637-byte source file, and run `python -m py_compile checker/read_rules.py`.
Result: document contains 18 valid source-line references covering every reported value; Python syntax check passed. Delay thresholds are 50%, slew thresholds 20%/80%, slew derating 1.0, and each delay grid has 7 points.
Surprises or open points: the delay table's input grid differs slightly from the similarly named internal-power grid; the reader deliberately selects `cell_fall`, not the power table.

## 2026-11-16 — task 2.1 — done
What was done: hand-wrote `work/m2-inv_1.cir` for `inv_1` at input transition 0.122474 ns and load 0.00952062 pF (fourth of seven grid points), with rising and falling input. Used the foundry cell netlist and only its two required typical transistor model files, at 25 C and 1.8 V. Measured 50%-50% delays and 20%-80% output transitions.
Command that proves it: `./.tools/envs/ngspice/Library/bin/ngspice_con.exe -b work/m2-inv_1.cir -o work/m2-inv_1.log` (bounded by `timeout 180` in Git Bash), then require all four measurements and reject simulation errors in the log.
Result: delay_fall 0.0594680 ns; delay_rise 0.107017 ns; transition_fall 0.0422483 ns; transition_rise 0.0934824 ns. Exit code 0 and no simulation errors.
Surprises or open points: the kit needs `.option ngbehavior=ps` and `.option scale=1e-6` for its subcircuit parameters and micrometre dimensions. Including the entire model library produced unused-device errors and very slow parsing, so the bench includes only the nfet_01v8 and pfet_01v8_hvt typical models plus their mismatch parameter files, with both mismatch switches zero.

## 2026-11-16 — task 2.2 — done
What was done: wrote `checker/compare.py` to compare generated Liberty or JSON timing points against the foundry Liberty file, write a CSV row per point, and print median and worst absolute percentage errors. It handles the four NLDM delay/transition tables and their arcs.
Command that proves it: `python checker/compare.py <foundry.lib> <foundry.lib> --output work/m2-self.csv`; change only `inv_1` `cell_fall` row 1 column 1 from 0.0143656 to 0.01580216 in `work/m2-modified.lib`; `python checker/compare.py work/m2-modified.lib <foundry.lib> --output work/m2-modified.csv`; assert nonzero-row counts and the changed value with Python.
Result: self-comparison: 247,352 points, zero nonzero errors, median 0%, worst 0%. Modified comparison: 247,352 points, exactly one nonzero error at `sky130_fd_sc_hd__inv_1`, `A->Y`, `cell_fall`, input 0.01 ns/load 0.0005 pF, exactly 10%.
Surprises or open points: initial nested regular-expression parsing was too slow and early state tracking missed arcs after internal-power groups. The final token parser associates each timing group with its own `related_pin`; the acceptance assertions caught these defects rather than accepting an empty or partial comparison.

## 2026-11-16 — task 2.3 — done
What was done: converted the four task 2.1 measurements to JSON, ran the checker against the foundry file, and wrote `reports/m2-smoke.md` with generated/foundry values, signed percentage errors and all simulator options.
Command that proves it: `python checker/compare.py work/m2-inv_1.json pdk/ciel/sky130/versions/e7a6777d157a9d94c7ac757457b9e4309e9e9000/sky130A/libs.ref/sky130_fd_sc_hd/lib/sky130_fd_sc_hd__tt_025C_1v80.lib --output work/m2-inv_1-comparison.csv`.
Result: 4 points compared. cell_fall -31.8481%; cell_rise -11.6454%; fall_transition -29.4216%; rise_transition +1.96942%. Median absolute error 20.5335%, worst 31.8481%.
Surprises or open points: three of four hand-run values are substantially faster than the foundry values; no correction factor has been applied.

## 2026-11-16 — task 2.4 — done
What was done: repeated the hand-run inverter point with a 0.1 ps print step instead of 1 ps and `reltol=1e-5 abstol=1e-15 vntol=1e-8 trtol=1`; appended the four movements to `reports/m2-smoke.md`.
Command that proves it: `./.tools/envs/ngspice/Library/bin/ngspice_con.exe -b work/m2-inv_1-tight.cir -o work/m2-inv_1-tight.log` under `timeout 180`, then parse both logs and calculate `(tight-baseline)/baseline*100` for all four measurements.
Result: delay_fall +0.002691%; delay_rise +0.000934%; transition_fall -0.021776%; transition_rise -0.001819%. Every movement is below 1%, so no new project defaults are required.
Surprises or open points: tightening the numerical settings does not explain the much larger foundry differences measured in task 2.3.

## 2026-11-16 — task 3.1 — done
What was done: installed CharLib commit 987e90f under `.tools/`, built Docker image `cellchar-charlib:987e90f-trixie-np2` with ngspice 44.2, characterized all ten cells with four workers, and compared its Liberty output. Extended `checker/compare.py` for unquoted identifiers, comments, split timing groups and CharLib's reversed grid order; reran the 247,352-point foundry self-check with zero errors.
Command that proves it: `docker run --rm -v <repo>:/work -v <pdk-version>:/pdk cellchar-charlib:987e90f-trixie-np2 charlib run /work/work/m3-charlib.yml --output /work/work/m3-charlib-results -j 4`; then `python checker/compare.py work/m3-charlib.lib <foundry.lib> --output work/m3-charlib-comparison.csv` and group absolute errors by cell.
Result: 3,724 points across 10 of 10 cells; overall median absolute error 53.2228%, worst 6795.10%. Per-cell medians range 36.9028% to 62.1515%; full table and point counts in `reports/m3-charlib.md`. Elapsed 3,953.83 s for 7,509 operations.
Surprises or open points: native Windows failed on Unix-only `fcntl`; bookworm provided ngspice 39 below CharLib's documented 44 minimum. NumPy 1 avoided a PySpice warning but lacked `trapezoid`; NumPy 2 completed successfully despite the warning. CharLib emits split rise/fall timing groups and reverses index_1/index_2 relative to the foundry.

## 2026-11-16 — task 3.2 — done
What was done: installed libretto commit 4ccaeb17 under `.tools/`, configured all ten cells, and ran it in the ngspice 44.2 Docker image with four threads. Diagnosed false-success runs, patched local include-path and working-directory handling, and inspected actual ngspice logs and processes. Wrote the precise failure account to `reports/m3-libretto.md`.
Command that proves it: `docker run --rm -v <repo>:/work -v <pdk-version>:/pdk -w /work/.tools/src/libretto cellchar-charlib:987e90f-trixie-np2 python3 script/libretto.py -b /work/work/m3-libretto.cmd`; inspect `work/m3-libretto-run9.log`, generated `.lis` files and `docker top <container>`.
Result: no valid comparison; 0 table points accepted. Initial runs failed every simulation while claiming success. After local fixes, 24 first-arc decks were generated, but four energy simulations each ran at 99% CPU for roughly 56–63 minutes without completing; the stalled container was stopped.
Surprises or open points: libretto can exit 0 and claim ten cells after simulator launch failures, so its exit status alone is not evidence. The final blocker is non-terminating energy simulation, not a measured accuracy result.

## 2026-11-16 — task 3.3 — done
What was done: cloned `vyges-tools/char` and LibreCell `lctime` for source/README inspection only. Recorded licences, code layouts, claimed outputs, foundry-accuracy evidence and last-change dates in `reports/m3-others.md`.
Command that proves it: `git -C .tools/src/vyges-char log -1 --format='%H %cs %s'`; `git -C .tools/src/lctime log -1 --format='%H %cs %s'`; inspect README, LICENSE/pyproject and `src/` layouts and search for accuracy/error/foundry comparisons.
Result: char f3756457, Apache-2.0, last change 2026-11-15, narrative foundry errors but no full per-cell table. lctime e57d3c57, AGPL-3.0-or-later, last change 2026-04-30, no published foundry-accuracy figure found.
Surprises or open points: char's README explicitly declines headline surrogate accuracy numbers but does include selected NLDM correlation percentages; the report distinguishes those from a complete per-cell benchmark.

## 2026-11-16 — task 3.4 — done (STOP)
What was done: wrote `reports/m3-decision.md` with the four hand-run errors, CharLib per-cell median/worst errors and point counts, runtimes, libretto's precise lack of results, source-review qualifications, and evidence for and against each of the three options. No direction selected.
Command that proves it: verify the report exists and inspect its tables against `reports/m2-smoke.md`, `reports/m3-charlib.md`, `reports/m3-libretto.md` and `reports/m3-others.md`; `git diff --check`.
Result: decision evidence report complete. Hand-run: 4 points, median 20.5335%, worst 31.8481%. CharLib: 3,724 points, median 53.2228%, worst 6795.10%, 3,953.83 s. libretto: no valid points, stalled energy simulations. Stopped at the milestone 3 stop gate.
Surprises or open points: the measurements do not cleanly satisfy either the “existing tools already close” premise or the “hand-run point close” premise; the report leaves the choice to the owner.

## 2026-11-16 — task 3b.1 — done
What was done: created branch `m3b-bench`; changed only the hand bench's full input ramp from 0.122474 ns to 0.204123333333 ns (`transition / 0.6`), reran the same point and compared all four values. Wrote `reports/m3b-ramp.md`.
Command that proves it: `./.tools/envs/ngspice/Library/bin/ngspice_con.exe -b work/m3b-inv_1-ramp.cir -o work/m3b-inv_1-ramp.log` under `timeout 180`; `python checker/compare.py work/m3b-inv_1-ramp.json <foundry.lib> --output work/m3b-inv_1-ramp-comparison.csv`.
Result: 4 points. Errors changed from -31.8481%, -11.6454%, -29.4216%, +1.96942% to -15.1304%, +7.62445%, -10.3498%, +4.18491%. Median absolute error 20.5335% before, 8.98713% after.
Surprises or open points: results match the owner review's approximate values; no model, load or threshold setting changed.

## 2026-11-16 — task 3b.2 — done
What was done: replaced the four model includes with `sky130.lib.spice` section `tt` and attempted native and Linux runs from the correct nested-include directory. Diagnosed fatal elaboration in unrelated device models, then ran a scratch `tt` entry containing the kit's two required transistor models, mismatch files and non-FET parameters. Wrote `reports/m3b-models.md`.
Command that proves it: `docker run --rm -v <repo>:/work -v <pdk-version>:/pdk cellchar-charlib:987e90f-trixie-np2 sh -c 'timeout 300 ngspice -b /work/work/m3b-inv_1-kitmodels-pruned.cir -o /work/work/m3b-inv_1-kitmodels-pruned.log'`; parse all four values and compare with `work/m3b-inv_1-ramp.log`.
Result: exit 0; all four values identical at printed precision (0.000000000% movement). The direct full top-level include remains unusable due to unrelated-model formula errors.
Surprises or open points: nested includes require running from the kit's ngspice directory; excluding unused device families was necessary for successful elaboration. No transistor model parameter was edited.

## 2026-11-16 — task 3b.3 — done
What was done: generated 49 corrected-ramp inverter decks, ran them with four workers and a 180 s Python timeout per deck, collected 196 table values, compared with the foundry and wrote `reports/m3b-inv-grid.md` with per-table and per-grid-coordinate errors.
Command that proves it: `python work/m3b-run-grid.py`; `python checker/compare.py work/m3b-inv-grid.json <foundry.lib> --output work/m3b-inv-grid-comparison.csv`.
Result: 49 of 49 simulations completed, 196 of 196 points compared. Overall median absolute error 14.9399%, worst 353.502%. Per-table medians: cell_fall 19.5153%, cell_rise 12.7534%, fall_transition 16.9830%, rise_transition 11.3403%. Error concentrates at small loads; worst at 1.5 ns input and 0.0005 pF.
Surprises or open points: a fixed 5 ns window missed the 80% crossing at the fastest input/largest load; the window now scales with ramp and load. Native simulations use `ngspice_con.exe` directly with Python timeout enforcement.

## 2026-11-16 — task 3b.4 — done
What was done: confirmed no extracted inverter netlist ships in `spice/` or `cdl/`; built Magic 8.3.703 from source in Docker image `cellchar-magic:latest`, extracted the supplied Magic layout with junction geometry and 14 capacitors, and ran the same 49 points. Wrote `reports/m3b-parasitics.md`.
Command that proves it: `magic -dnull -noconsole -T /pdk/sky130A/libs.tech/magic/sky130A.tech /work/work/m3b-extract.tcl`; `python work/m3b-run-grid-extracted.py`; `python checker/compare.py work/m3b-inv-grid-extracted.json <foundry.lib> --output work/m3b-inv-grid-extracted-comparison.csv`.
Result: 196 of 196 points compared for each netlist. Overall median: schematic 14.9399%, extracted 14.3659%; worst: 353.502% versus 235.211%. Per-table figures in the report. Extracted decks verified to include `work/m3b-inv_1-extracted.spice`.
Surprises or open points: bookworm Magic 8.3.105 segfaulted on the kit technology; current source worked. An initial runner substitution miss produced invalid identical results; those logs were deleted and the corrected run was verified.

## 2026-11-16 — task 3b.5 — done
What was done: inspected the ten worst original `inv_1` points and CharLib's ramp/writer source. Found and fixed a checker orientation bug: CharLib's load-first tables also require transposing values. Revalidated 247,352 self-points at zero and one 10% changed point. Reran only `inv_1` with the extracted netlist supplied through YAML, without changing CharLib code. Wrote `reports/m3b-charlib.md`.
Command that proves it: `charlib run /work/work/m3b-charlib-extracted.yml --output /work/work/m3b-charlib-extracted.lib -j 4 --filter 'sky130_fd_sc_hd__inv_1$'`; `python checker/compare.py work/m3b-charlib-extracted.lib <foundry.lib> --output work/m3b-charlib-extracted-comparison.csv`.
Result: 196 points before and after. Overall median 14.9399% before (orientation corrected), 14.6039% after; worst 405.277% before, 260.480% after. Rerun 187.75 s for 395 operations.
Surprises or open points: CharLib already scales the 20%-80% ramp correctly; the huge milestone 3 errors were primarily checker transposition, not CharLib's ramp. A subprocess-backend attempt failed on space-containing paths and was not used for the accepted result.

## 2026-11-16 — task 3b.6 — done (STOP)
What was done: wrote `reports/m3b-decision.md` using the corrected ramp, full schematic/extracted grids and configuration-only CharLib rerun. Explicitly invalidated the earlier ten-cell error table and made no new ten-cell claim. Stated evidence for all three options without choosing.
Command that proves it: inspect `reports/m3b-decision.md` against `reports/m3b-ramp.md`, `reports/m3b-inv-grid.md`, `reports/m3b-parasitics.md` and `reports/m3b-charlib.md`; `git diff --check`.
Result: revised report complete. Corrected single point median 8.98713% over 4 points; extracted hand grid median 14.3659% over 196 points; extracted CharLib median 14.6039% over 196 points. Stopped at the milestone 3b stop gate.
Surprises or open points: hand-run and CharLib full-grid results are similar, so the evidence does not show a clear implementation advantage for building a new tool.

## 2026-11-17 — task 3c.1 — done
What was done: created branch `m3c-gap`; matched hand-run and CharLib extracted inverter points by table and canonical grid index, computed absolute generated-value differences and wrote `reports/m3c-agreement.md`.
Command that proves it: Python CSV comparison of `work/m3b-inv-grid-extracted-comparison.csv` and `work/m3b-charlib-extracted-comparison.csv`, using seven known slew and load coordinates to canonicalize rounded CharLib labels.
Result: 196 of 196 points matched. Median differences: cell_fall 0.189200 ps, cell_rise 0.295000 ps, fall_transition 0.946200 ps, rise_transition 0.468900 ps. Worst: 8.38200, 354.519, 241.055 and 208.029 ps respectively.
Surprises or open points: only 40 keys matched before canonicalization because CharLib rounds grid labels. Largest method disagreement is at 1.5 ns input and 0.181284 pF, not a typical grid point.

## 2026-11-17 — task 3c.2 — done
What was done: added signed `absolute_error_ps` to checker CSV output and median/worst picosecond summaries to its console output. Re-ran identity and 10% perturbation tests and re-reported the extracted inverter grid in `reports/m3c-absolute.md`.
Command that proves it: `python checker/compare.py <foundry.lib> <foundry.lib> --output work/m3c-self.csv`; `python checker/compare.py work/m2-modified.lib <foundry.lib> --output work/m3c-modified.csv`; `python checker/compare.py work/m3b-inv-grid-extracted.json <foundry.lib> --output work/m3c-inv-grid-extracted.csv`; assert both test cases and count thresholds.
Result: identity 247,352 points at zero in both measures; perturbation exactly one point at 10% and 1.43656 ps. Extracted grid: 196 points, median 14.3659% and 15.8202 ps, worst 235.211% and 408.860 ps; 127 points exceed both 10% and 5 ps.
Surprises or open points: no cell_fall point exceeds both thresholds despite the 235.211% worst percentage, confirming that near-zero-delay percentages can be misleading.

## 2026-11-17 — task 3c.3 — done
What was done: ran CharLib on schematic `nand2_1` with four workers, compared with the corrected checker and wrote `reports/m3c-nand2.md` with per-table percentage and picosecond errors.
Command that proves it: `charlib run /work/work/m3-charlib.yml --output /work/work/m3c-nand2.lib -j 4 --filter 'sky130_fd_sc_hd__nand2_1$'`; `python checker/compare.py work/m3c-nand2.lib <foundry.lib> --output work/m3c-nand2-comparison.csv`.
Result: 392 points across two arcs. Overall median 9.11900% and 15.0047 ps; worst 284.899% and 224.695 ps. Runtime 606.47 s for 790 operations.
Surprises or open points: this cell's median percentage is lower than the inverter's, but near-zero falling-delay points still produce large percentage errors.

## 2026-11-17 — task 3c.4 — done
What was done: fetched IHP SG13G2 with ciel, located its typical Liberty and standard-cell netlist, inspected the header, compiled the supplied PSP103/PSP103-NQS Verilog-A models with OpenVAF Reloaded v24.0.2mob, loaded them through `.spiceinit`, and ran CharLib on `sg13g2_inv_1`. Wrote `reports/m3c-ihp.md`.
Command that proves it: `charlib run /work/work/m3c-ihp.yml --output /work/work/m3c-ihp.lib -j 4` in `cellchar-openvaf:latest` from `/work/work/m3c-ihp-init`; `python checker/compare.py work/m3c-ihp.lib <ihp-foundry.lib> --output work/m3c-ihp-comparison.csv`.
Result: 196 points, median 4.65003% and 15.2825 ps, worst 64.5966% and 240.681 ps. Runtime 4,728.70 s for 395 operations. Header quotes IHP 2025, date and revision 0.1.4 but names no producer tool.
Surprises or open points: initial shared-ngspice run failed because OSDI modules were absent; `pre_osdi` is unavailable in ngspice 44.2, while `.spiceinit` `osdi` loads before parsing and works. Full ngspice source build was unnecessary and failed on legacy `sys_errlist`.

## 2026-11-17 — task 3c.5 — done (STOP)
What was done: wrote `reports/m3c-closing.md` combining method agreement, SkyWater absolute/percentage errors, second-cell results and IHP cross-kit measurements. Distinguished kit-following percentage error from shared absolute residuals and stated the remaining confounds. No recommendation.
Command that proves it: inspect `reports/m3c-closing.md` against `reports/m3c-agreement.md`, `reports/m3c-absolute.md`, `reports/m3c-nand2.md` and `reports/m3c-ihp.md`; `git diff --check`.
Result: same simulator/CharLib gives IHP median 4.65003% over 196 points versus extracted SkyWater CharLib median 14.6039% over 196 points. Absolute medians are close (15.2825 ps versus 15.8202 ps hand-run). Conclusion: percentage gap primarily follows kit/model/library, not simulator alone; model versus foundry-method effects remain confounded. Stopped.
Surprises or open points: a large percentage gap does not imply a correspondingly large absolute-time gap on the second kit.

## 2026-11-17 — task 5.1 — done
What was done: created branch `m5-package`; added Apache-2.0 `pyproject.toml` for Python 3.10+, moved comparison modules into `libertydiff/`, added package and CLI entry points, retained `checker/compare.py` as a thin wrapper, updated references and ignored egg-info. No runtime dependencies added.
Command that proves it: `python -m venv .venv; .\.venv\Scripts\python.exe -m pip install -e .; .\.venv\Scripts\python.exe -m libertydiff --help`.
Result: editable install succeeded in the fresh environment; CLI printed usage with the `compare` subcommand.
Surprises or open points: no external dependency was needed; setuptools is declared only as the build backend.

## 2026-11-17 — task 5.2 — done
What was done: added `libertydiff/reader.py`, a structural Liberty reader returning cells, pins, arcs, tables, named axes, values and header-derived units. Supports both axis orders, scalar tables and quoted multiline value lists. Added four unit tests. Added pytest as optional test-only dependency because the project requires pytest and no runtime dependency.
Command that proves it: `.venv/Scripts/python.exe -m pytest tests/test_reader.py -q`; call `read_library` on the SkyWater and IHP foundry files and print cell/table counts and units.
Result: 4 tests passed. SkyWater: 428 cells and 5,368 tables; IHP: 84 cells and 1,022 tables. Both headers resolve to 1000 ps per time unit and 1000 fF per capacitance unit.
Surprises or open points: axis variable names come from each table's declared template, never their position.

## 2026-11-17 — task 5.3 — done
What was done: added `libertydiff/diff.py` with cell/arc/table matching, named-axis point alignment, unit conversion to picoseconds, unmatched-table reporting, per-cell/table summaries, and CSV/JSON output. Wired `libertydiff compare` options `--cells`, `--csv`, `--json`, `--summary` and `--min-abs`. Added four comparison tests.
Command that proves it: `.venv/Scripts/python.exe -m pytest tests/test_reader.py tests/test_diff.py -q`; `.venv/Scripts/python.exe -m libertydiff compare --help`.
Result: 8 tests passed, covering zero identity, exactly one 10% point, axes-swapped/transposed zero difference, and unmatched/output behavior.
Surprises or open points: point coordinates are matched by variable name and numeric value, so table axis order does not affect comparison.

## 2026-11-17 — task 5.4 — done
What was done: ensured every summary prints compared and unmatched counts with percentage and picosecond figures. `--min-abs` filters points included in summary statistics while unmatched tables remain listed. Added tests for counts, threshold and cell filtering. Reconstructed the milestone 3c generated inverter library and compared it cell-scoped against the foundry.
Command that proves it: `.venv/Scripts/python.exe -m pytest tests/test_diff.py -q`; Python assertion of all four per-table medians/worsts against `reports/m3c-absolute.md`.
Result: 6 comparison tests passed. Reproduced 196 points with zero unmatched and exact milestone figures: cell_fall 14.010980%/22.3268 ps, cell_rise 15.962221%/38.5548 ps, fall_transition 8.577413%/7.4575 ps, rise_transition 14.470473%/11.4437 ps medians.
Surprises or open points: comparing a one-cell generated file against the entire foundry library correctly reports all other foundry tables as unmatched; benchmark comparisons must use `--cells` or a matching cell subset.
