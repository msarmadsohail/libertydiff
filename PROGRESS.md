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
