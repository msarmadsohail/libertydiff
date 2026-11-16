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
