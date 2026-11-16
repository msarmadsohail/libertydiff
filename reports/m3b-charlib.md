# CharLib `inv_1` re-check

## Cause of the ten worst points

The ten worst original `inv_1` comparisons were all at slow inputs (0.650743 or 1.5 ns), mostly at the smallest loads. Two separate issues were found:

1. **Checker table-orientation fault.** CharLib writes `index_1` as load and `index_2` as input transition. Its values rows vary input transition, so the table is transposed relative to the foundry layout. The milestone 3 checker swapped the indices but did not transpose the values. This manufactured very large errors. The checker now transposes those values; its 247,352-point self-check remains zero and the single 10% perturbation test still identifies exactly one point.
2. **Missing layout parasitics in the configuration.** CharLib's own `slew_pwl` already uses `t_slew / (high_threshold - low_threshold)`, so its input ramp was not wrong. The original configuration used the two-transistor schematic netlist. The rerun changes only the configured netlist to the Magic-extracted netlist from task 3b.4; CharLib code is unchanged.

A separate `ngspice-subprocess` attempt failed because CharLib's generated paths contain spaces. Directly running the generated deck succeeded and confirmed its ramp and original measured value. The accepted rerun uses the original `ngspice-shared` backend.

## Before and after

Both rows sets contain **196 points** (four tables × 49 grid points). “Before” is the original CharLib output recompared with the orientation fault fixed.

| Table | Before median | After median | Before worst | After worst |
|---|---:|---:|---:|---:|
| `cell_fall` | 19.7187% | 14.2442% | 405.277% | 260.480% |
| `cell_rise` | 12.7737% | 16.1605% | 29.0396% | 51.1604% |
| `fall_transition` | 16.5853% | 12.9923% | 47.6455% | 71.4996% |
| `rise_transition` | 10.8570% | 14.8491% | 31.0912% | 52.2703% |
| **All tables** | **14.9399%** | **14.6039%** | **405.277%** | **260.480%** |

The extracted-netlist rerun completed 395 characterization operations in 187.75 s with four workers. It improves falling delay and overall worst error, but not every transition-table error.

Commands:

```sh
charlib run /work/work/m3b-charlib-extracted.yml --output /work/work/m3b-charlib-extracted.lib -j 4 --filter 'sky130_fd_sc_hd__inv_1$'
python checker/compare.py work/m3b-charlib-extracted.lib <foundry.lib> --output work/m3b-charlib-extracted-comparison.csv
```
