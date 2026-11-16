# Revised milestone 3 decision evidence

This report replaces the milestone 3 evidence with corrected bench and comparison results. It does not choose a project direction.

## Corrected hand-run measurements

The milestone 2 ramp used the 20%–80% transition as the full 0–100% ramp. Correcting the full ramp to `transition / 0.6` changed the single-point errors as follows (four points):

| Table | Before | After |
|---|---:|---:|
| `cell_fall` | -31.8481% | -15.1304% |
| `cell_rise` | -11.6454% | +7.62445% |
| `fall_transition` | -29.4216% | -10.3498% |
| `rise_transition` | +1.96942% | +4.18491% |
| **Median absolute** | **20.5335%** | **8.98713%** |

Using the kit's typical model content did not move any of the four values at printed precision. The full top-level model file fails on unrelated device models in this environment.

## Full `inv_1` grid

Each result below covers **196 points** (49 slew/load points × four tables).

| Netlist | Median absolute error | Worst absolute error |
|---|---:|---:|
| Schematic | 14.9399% | 353.502% |
| Magic-extracted | 14.3659% | 235.211% |

| Table | Schematic median | Extracted median | Schematic worst | Extracted worst |
|---|---:|---:|---:|---:|
| `cell_fall` | 19.5153% | 14.0110% | 353.502% | 235.211% |
| `cell_rise` | 12.7534% | 15.9622% | 34.5282% | 59.4392% |
| `fall_transition` | 16.9830% | 8.57741% | 47.9710% | 17.2634% |
| `rise_transition` | 11.3403% | 14.4705% | 31.2534% | 27.2874% |

Error concentrates at small loads, especially slow-input/small-load delay points. Parasitics improve falling delay and transition but do not make the full grid uniformly close.

## CharLib re-check

The original extreme errors were primarily a checker fault: CharLib writes load-first, input-second tables with transposed values. The checker now handles that layout and still passes its 247,352-point identity test and single 10% perturbation test.

CharLib itself already generates the correct 20%–80% ramp. Only its YAML netlist was changed for the rerun, from schematic to the same Magic-extracted `inv_1` netlist. No CharLib code changed.

| Table | Original output, corrected comparison median | Extracted rerun median | Original worst | Extracted worst |
|---|---:|---:|---:|---:|
| `cell_fall` | 19.7187% | 14.2442% | 405.277% | 260.480% |
| `cell_rise` | 12.7737% | 16.1605% | 29.0396% | 51.1604% |
| `fall_transition` | 16.5853% | 12.9923% | 47.6455% | 71.4996% |
| `rise_transition` | 10.8570% | 14.8491% | 31.0912% | 52.2703% |
| **All 196 points** | **14.9399%** | **14.6039%** | **405.277%** | **260.480%** |

The extracted rerun took 187.75 s for 395 operations with four workers. The earlier ten-cell run's published error table is invalid because of the checker orientation fault; it has not been rerun with the corrected checker and extracted netlists.

## Other tools

- libretto: no valid result; energy simulations stalled after local path fixes.
- `vyges-tools/char`: source-only review; selected narrative accuracy figures, no complete per-cell benchmark.
- LibreCell `lctime`: source-only review; no published numerical foundry comparison found.

## Evidence for the three options

1. **An existing tool is already within a few percent everywhere, so contribute there:** not supported by the corrected `inv_1` evidence. CharLib's extracted-run median is 14.6039% over 196 points, with per-table medians 12.9923–16.1605% and worst 260.480%. Only one inverter was rerun; no ten-cell corrected claim is made.
2. **The hand-run point is itself far off, so the simulator is the limit:** the corrected single point is closer (median 8.98713% over four points), but the full extracted grid still has median 14.3659% over 196 points and worst 235.211%. This supports a significant residual simulator/model/extraction gap, not a conclusion that the simulator alone is the limit.
3. **Existing tools are well off but the hand-run point is close, so build:** partially supported but not clean. CharLib remains well off on the measured inverter, while the hand-run single point is within 4.18491–15.1304% signed error across four values. The full hand-run grid is not uniformly close, and CharLib's result is very similar to the hand-run result, suggesting shared bench/model limitations rather than a clear implementation advantage.

**STOP: no direction selected.**
