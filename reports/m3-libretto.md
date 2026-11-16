# libretto run result

libretto commit `4ccaeb17c485c051db8bb326dd84b9ea112e3a7f` was installed under `.tools/` and run in Docker image `cellchar-charlib:987e90f-trixie-np2` (`python:3.12-trixie`, ngspice 44.2), using four simulation threads at typical/25 °C/1.8 V.

**No valid per-cell error table could be produced.** Zero table points were accepted for comparison.

## What happened

1. The first runs returned exit code 0 and claimed ten generated cells, but printed `Failed to lunch spice` for every simulation. Inspection showed that libretto unconditionally prefixes model and netlist includes with `../`, so the configured absolute paths did not exist.
2. A local source change removed that prefix for combinational decks. A second local change saves the starting directory and restores it after characterization; the original `os.chdir("../")` did not reliably return to the project directory before export.
3. With those fixes, ngspice read the models and cell netlist and began transient simulations. The run generated 24 decks for the first inverter arc, then stalled in four energy simulations (`..._e.sp`). After more than 31 minutes total, `docker top` showed each of those four ngspice processes at 99% CPU with approximately 56–63 minutes of CPU time and no new decks. The container was stopped.
4. Earlier partial Liberty output was not compared: it came from failed simulations and contained uninitialized/zero results. The final run did not produce a complete valid Liberty file.

Command for the final attempt:

```sh
python3 script/libretto.py -b /work/work/m3-libretto.cmd
```

Working directory inside the container: `/work/.tools/src/libretto`. Configuration and logs are under ignored `work/m3-libretto*`; generated decks are under ignored `.tools/src/libretto/work/m3-libretto-work/`.

The failure is a non-terminating energy-measurement simulation in this revision/configuration, not evidence about the accuracy of a successfully characterized table.
