# Milestone 3 decision evidence

This report states evidence only. It does not choose among the three project directions.

## Hand-run inverter

One `inv_1` arc at input transition 0.122474 ns and load 0.00952062 pF; four table points compared. ngspice 41, typical models, 25 °C, 1.8 V.

| Table | Generated (ns) | Foundry (ns) | Error |
|---|---:|---:|---:|
| `cell_fall` | 0.0594680 | 0.0872580 | -31.8481% |
| `cell_rise` | 0.107017 | 0.1211221 | -11.6454% |
| `fall_transition` | 0.0422483 | 0.0598601 | -29.4216% |
| `rise_transition` | 0.0934824 | 0.0916769 | +1.96942% |

Median absolute error: 20.5335%; worst: 31.8481%. Tightening the print step and tolerances moved each result by at most 0.021776%, so numerical convergence does not explain these differences.

## Existing tools

### CharLib

Commit `987e90f5286b11c3a548749f93b689a7b8723003`; ngspice 44.2 in `python:3.12-trixie`; four workers. Runtime: 3,953.83 s (65 min 53.83 s), 7,509 characterization operations.

| Cell | Points | Median absolute error | Worst absolute error |
|---|---:|---:|---:|
| `inv_1` | 196 | 49.8439% | 1546.16% |
| `inv_2` | 196 | 36.9028% | 5120.29% |
| `buf_1` | 196 | 62.1515% | 4525.44% |
| `nand2_1` | 392 | 57.0440% | 2371.38% |
| `nand3_1` | 588 | 58.6632% | 1313.19% |
| `nor2_1` | 392 | 46.3576% | 6795.10% |
| `nor3_1` | 588 | 49.6970% | 2607.70% |
| `and2_1` | 392 | 52.4148% | 2990.00% |
| `or2_1` | 392 | 50.2738% | 3280.66% |
| `xor2_1` | 392 | 57.7225% | 1555.74% |
| **All** | **3,724** | **53.2228%** | **6795.10%** |

### libretto

Commit `4ccaeb17c485c051db8bb326dd84b9ea112e3a7f`; ngspice 44.2 in the same container family; four threads. No valid table points or runtime-to-completion are available. After local include-path and working-directory fixes, four energy simulations each consumed roughly 56–63 minutes of CPU without completing; the stalled container was stopped. Earlier runs falsely returned success after simulator launch failures, so their output was rejected.

### Source-only reviews

- `vyges-tools/char`: Apache-2.0; last change 2026-11-15. Its README reports selected foundry-correlation figures (`inv_2` rise delay 7%, rise transition 6%, weighted error around 13–20%) but no complete per-cell table or point counts. It was not installed or run in this milestone.
- LibreCell `lctime`: AGPL-3.0-or-later; last change 2026-04-30. No published numerical foundry-Liberty accuracy comparison found. It was not installed or run.

## Evidence bearing on the three options

1. **Contribute to an existing tool because it is within a few percent everywhere:** the measured CharLib result does not show this: median errors are 36.9028–62.1515% per cell over 3,724 total points. libretto produced no valid tables. The source-only char review has selected single-digit examples but insufficient full-table evidence.
2. **The simulator is the limit because the hand-run point is far off:** the hand-run median absolute error is 20.5335% over four points, with worst 31.8481%. This is a substantial discrepancy at the tested point. Numerical sensitivity is negligible by comparison. char's README also describes an approximately 15% ngspice/vendor floor at large load, but that is external narrative evidence rather than this project's measurement.
3. **Build because existing tools are well off but the hand-run point is close:** CharLib is well off in this run, but the hand-run point is not uniformly close: only `rise_transition` is within 2%; the other three errors are 11.6454–31.8481%. The evidence therefore does not cleanly satisfy this option's hand-run premise.

**STOP: no direction selected.**
