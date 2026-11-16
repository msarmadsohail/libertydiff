# Other characterizers: source review

Reviewed by cloning source for inspection only; neither tool was installed or run.

## `vyges-tools/char`

- **Repository and revision:** <https://github.com/vyges-tools/char>, commit `f37564573069561614fd440bc0f527c9ae452ad0`.
- **Licence:** Apache License 2.0 (`LICENSE`).
- **Code layout:** dependency-free Rust (`Cargo.toml`); `src/` separates job parsing, arc derivation, SPICE deck generation, simulation engine, Liberty output, library parallelism, datasets and surrogate models. `examples/` and Rust tests are included.
- **Claimed output:** Liberty NLDM delay and output-transition tables from ngspice sweeps; multi-arc and sequential characterization; optional LVF, CCS and power. It also supports library-level parallel runs and surrogate-filled grids.
- **Published accuracy against a foundry file:** the README gives narrative measurements, not a reproducible per-cell error table. Its “Current state (2026-05-31)” section reports `inv_2` `cell_rise` 7% and `rise_transition` 6%, weighted error around 13–20%, and an approximately 15% ngspice/vendor floor at large load. It explicitly says it is “not publishing headline accuracy numbers” for surrogate accuracy. No point counts or full cell-by-cell results accompany the foundry comparisons.
- **Last change:** 2026-11-15, commit subject `ci: check the shared build settings (vyges-tools/build-config v0.1.0)`.

## LibreCell `lctime`

- **Repository and revision:** <https://codeberg.org/librecell/lctime>, commit `e57d3c57d8816871e392c393b8c79011221055f4`. The Codeberg location was confirmed by a successful clone.
- **Licence:** AGPL-3.0-or-later for the package (`pyproject.toml` and REUSE metadata); documentation files carry their own SPDX identifiers.
- **Code layout:** Python package under `src/lctime/`, separated into `characterization`, `logic`, `liberty`, `lccommon` and transistor sizing. It includes examples, tests and command-line entry points `lctime`, `sp2bool`, `libertymerge` and `libertyviz`.
- **Claimed output:** input capacitances and Liberty timing delays for combinational cells; recognition of transistor-network logic; setup, hold, removal and recovery constraints for sequential cells; NLDM visualization and Liberty merging.
- **Published accuracy against a foundry file:** none found in the README, source comments or tests. The documentation explains how to characterize cells and visualize results but publishes no numerical comparison against a foundry Liberty file.
- **Last change:** 2026-04-30, commit subject `improve log message`.
