# Corrected `inv_1` full grid

All 49 slew/load points for `inv_1`, four tables, **196 table points**. Corrected 20%–80% input ramp, schematic netlist, typical models, 25 °C, 1.8 V. All 49 simulations completed; no failed measurements.

| Table | Points | Median absolute error | Worst absolute error | Worst point (input ns, load pF) |
|---|---:|---:|---:|---|
| `cell_fall` | 49 | 19.5153% | 353.502% | 1.5, 0.0005 |
| `cell_rise` | 49 | 12.7534% | 34.5282% | 1.5, 0.00133517 |
| `fall_transition` | 49 | 16.9830% | 47.9710% | 0.01, 0.0005 |
| `rise_transition` | 49 | 11.3403% | 31.2534% | 0.01, 0.0005 |
| **All tables** | **196** | **14.9399%** | **353.502%** | 1.5, 0.0005 |

## Where error concentrates

Median absolute error across all four tables:

| Input transition (ns) | Median | Worst |
|---|---:|---:|
| 0.01 | 16.6754% | 47.9710% |
| 0.0230506 | 16.5724% | 32.4162% |
| 0.0531329 | 15.0506% | 37.0909% |
| 0.122474 | 14.1730% | 46.4040% |
| 0.282311 | 13.1111% | 66.4566% |
| 0.650743 | 13.8745% | 118.093% |
| 1.5 | 13.6978% | 353.502% |

| Load (pF) | Median | Worst |
|---|---:|---:|
| 0.0005 | 23.5042% | 353.502% |
| 0.00133517 | 16.7829% | 174.289% |
| 0.00356533 | 11.6216% | 79.8738% |
| 0.00952062 | 9.86320% | 39.0480% |
| 0.0254232 | 12.5907% | 21.4921% |
| 0.0678883 | 13.9088% | 17.8818% |
| 0.181284 | 15.1745% | 25.9799% |

The strongest concentration is **small loads**, especially the 0.0005 pF column. The worst delay error occurs at the **slowest input and smallest load**, where the output can cross before the input 50% reference and the foundry delay is small. Transition errors are largest at the **fastest input and smallest load**. Large loads have lower median error than the smallest two columns, although their median rises again slightly at 0.181284 pF.

Commands:

```sh
python work/m3b-run-grid.py
python checker/compare.py work/m3b-inv-grid.json <foundry.lib> --output work/m3b-inv-grid-comparison.csv
```
