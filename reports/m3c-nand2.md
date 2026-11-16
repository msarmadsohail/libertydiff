# Schematic `nand2_1` with CharLib

CharLib commit `987e90f`, ngspice 44.2, schematic netlist, typical models, 25 °C, 1.8 V. Four workers; 790 characterization operations in 606.47 s. Two arcs (`A->Y`, `B->Y`), four tables and 49 points per arc/table: **392 points total**.

| Table | Points | Median % | Worst % | Median absolute | Worst absolute |
|---|---:|---:|---:|---:|---:|
| `cell_fall` | 98 | 14.4638% | 284.899% | 22.3349 ps | 107.248 ps |
| `cell_rise` | 98 | 8.51349% | 24.1366% | 14.9431 ps | 214.134 ps |
| `fall_transition` | 98 | 7.53092% | 57.4552% | 10.5418 ps | 82.5215 ps |
| `rise_transition` | 98 | 8.85481% | 41.3873% | 11.7748 ps | 224.695 ps |
| **All tables** | **392** | **9.11900%** | **284.899%** | **15.0047 ps** | **224.695 ps** |

The second cell has lower median percentage error than the extracted inverter grid, but its worst near-zero falling-delay percentage remains large. Absolute errors show substantial rising-transition and rising-delay residuals at the extremes.

Commands:

```sh
charlib run /work/work/m3-charlib.yml --output /work/work/m3c-nand2.lib -j 4 --filter 'sky130_fd_sc_hd__nand2_1$'
python checker/compare.py work/m3c-nand2.lib <foundry.lib> --output work/m3c-nand2-comparison.csv
```
