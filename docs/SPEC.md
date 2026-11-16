# Specification: libertydiff and the open-kit Liberty benchmark

## What is being built
1. **libertydiff**, a small command-line tool and Python package that compares two Liberty (`.lib`) files point by point.
2. **A benchmark** that uses it: how closely an open characteriser (CharLib, running ngspice) reproduces the foundry Liberty files that ship with open chip kits, cell by cell, with the method and versions pinned so anyone can rerun it.

## Who it is for
- Someone who has characterised a cell and wants to know how far the result is from a reference.
- Someone choosing between open chip kits or open tools who wants numbers with point counts, not impressions.
- Maintainers of a kit or a characteriser who want a regression check.

## Why it is worth having
Earlier work in this repository found that the open tools publish no per-cell accuracy tables against foundry files, and that a correct comparison is easy to get wrong in two ways: defining the input transition as the full ramp instead of the 20%-to-80% time, and reading a table whose axes are in the other order. Both mistakes produced plausible-looking wrong numbers here. A tool that handles them, and a benchmark that states its method, removes that trap for the next person.

## What it must get right
- **Axes are matched by variable name**, never by position.
- **Units come from the library header** and are converted, never assumed.
- **Every summary states how many points were compared and how many were not matched.**
- **Percentage and absolute differences are always reported together.** A 200% difference on a 2-picosecond delay and a 10% difference on a 2-nanosecond delay are different things.
- **Nothing is dropped silently:** missing cells, arcs, tables and failed simulations are listed.

## What it must not claim
- It does not say which side is right. A difference between a generated file and a foundry file can come from the transistor models, the netlist, the simulator, or how the foundry produced its file. The benchmark reports differences.
- Results on a handful of cells are results on those cells. No statement about a whole library unless the whole library was run.
- No statement about the accuracy of silicon. Nothing here is compared with a measured chip.

## What this does not show
- Sequential cells, setup and hold times, power, and the CCS model are not covered.
- The foundry files' own production methods are not known.
- The free simulator is the only simulator used.

## Quality bar
- `pytest` passes with no chip kit installed.
- Every number in the README can be traced to a file under `results/`.
- A person with Docker and Python can reproduce one cell's result with two commands.

## Standing rules
`AGENTS.md` applies in full, with two changes for milestones 5 to 8:
- The old rule that only `checker/` may read the foundry file existed to stop a characteriser copying the answer. There is no characteriser now. Its replacement: **nothing in this repository may adjust, fit or correct generated values towards the foundry values.** The tool measures differences; it never reduces them.
- **Tests are never weakened to pass.** A failing test is fixed in the code or reported as a finding.
