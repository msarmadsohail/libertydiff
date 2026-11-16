# Hand-run versus CharLib extracted `inv_1`

Point-by-point comparison of the hand-run extracted grid and the CharLib extracted rerun. CharLib rounds grid labels, so points were matched by table and canonical row/column index, not formatted coordinate strings. **196 of 196 points matched.**

Differences are absolute generated-value differences in picoseconds.

| Table | Points | Median difference | Worst difference | Worst point (input ns, load pF) |
|---|---:|---:|---:|---|
| `cell_fall` | 49 | 0.189200 ps | 8.38200 ps | 1.5, 0.00952062 |
| `cell_rise` | 49 | 0.295000 ps | 354.519 ps | 1.5, 0.181284 |
| `fall_transition` | 49 | 0.946200 ps | 241.055 ps | 1.5, 0.181284 |
| `rise_transition` | 49 | 0.468900 ps | 208.029 ps | 1.5, 0.181284 |

The methods agree closely at most points: every table's median difference is below 1 ps. The largest disagreements concentrate at the slowest input and largest load, especially `cell_rise`, where the hand run gives 1.57774 ns and CharLib gives 1.932259 ns. Thus the two methods are not identical at the transient-window extremes, but their close agreement over most of the grid supports a shared model/bench gap rather than independent large implementation errors.
