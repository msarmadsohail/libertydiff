# Working rules for this repository

Read this file, then `docs/SPEC.md`, then `TASKS.md`, then `PROGRESS.md`, at the start of every working stretch. The chat history is not reliable over a long run; these files are the memory.

## What this project is
A tool that compares Liberty (`.lib`) files point by point, and a reproducible benchmark of how closely open tools reproduce the foundry Liberty files on open chip kits. Full description: `docs/SPEC.md`.

## How to work
1. Take the first task in `TASKS.md` that is not marked done. Do only that task.
2. Each task has a "Done when" check. A task is done only when that check has been run and its output is recorded.
3. After every task, append an entry to `PROGRESS.md`: date, task id, what was done, the exact command that proves it, the result, and anything that surprised you.
4. Commit after every task. One short lower-case line, no trailer, no emoji.
5. Work on a branch per milestone (`m1-tools`, `m2-smoke`, ...) and merge it into `main` locally when the milestone is finished. Everything stays on this machine: never push, never add a remote, never open a pull request, never use the `gh` tool. The owner publishes the branches later.
6. If a task cannot be completed after three honest attempts, write what was tried and why it failed in `PROGRESS.md`, mark the task `BLOCKED`, and go on to the next task that does not depend on it. Stop only if nothing else can proceed. Never invent a result.

## Stop gates
Tasks marked **STOP** end the run. Write the report the task asks for and wait for the owner. Do not continue past a stop gate on your own judgement.

## Rules that are never broken
- **Nothing in this repository adjusts, fits or corrects generated values towards the foundry values.** The tool measures differences; it never reduces them.
- **No fudge factors.** No per-cell constants, correction tables or scale factors tuned to make a comparison pass. Every constant has a physical reason written beside it.
- **Never weaken a test or a "Done when" check to make something pass.** If a check is wrong, say so in `PROGRESS.md` and stop.
- **Report numbers with their base.** Never "12 cells pass"; always "12 of 14 cells within 5%, at 49 table points each".
- **Verify before asserting.** A path, version or command is a fact only after a command showed it. Items marked *(check)* in the blueprint are unverified.
- **Nothing system-wide.** Tools go under `.tools/`, chip-kit data under `pdk/`, scratch under `work/`. All three are ignored by git. Do not change PATH, the registry or global git settings.
- **No secrets in the repository.** Never print, log or commit an API key or token.
- **Commit identity is already set for this repository.** Do not change it and do not pass `-c user.email`.

## Environment
- Windows 11. Shells: PowerShell and Git Bash. Python 3.11 and 3.12, `uv`, Node, Docker Desktop are installed.
- If a tool will not install natively, run it in a Docker container and record the image and command in `PROGRESS.md`.
- **On Windows, never run `ngspice.exe`.** It is the windowed program: it opens a window and a dialog box and then waits for a person to click, which hangs an unattended run. Always use `ngspice_con.exe`, and for simulations always in batch mode: `ngspice_con.exe -b deck.sp -o work/deck.log`. Every deck ends with `.end` and exits on its own. Wherever a task says `ngspice`, read `ngspice_con.exe`.
- Any command that could open a window or wait for input gets a timeout.
- Simulations are processor-bound. Run them in parallel, but leave two cores free.

## What not to do
- Do not widen scope beyond `TASKS.md`. Do not start writing a characteriser.
- Do not rewrite working code for style.
- Do not add dependencies without writing one line in `PROGRESS.md` saying why.
