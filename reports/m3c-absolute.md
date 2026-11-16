# Extracted `inv_1`: percentage and absolute error

`checker/compare.py` now writes signed `absolute_error_ps` and prints median/worst absolute error in picoseconds alongside percentage error. Values are converted from Liberty nanoseconds using 1 ns = 1000 ps.

Validation:

- Foundry against itself: **247,352 points**, zero percentage and absolute error at every point.
- One `cell_fall` value increased by 10%: exactly one nonzero point, 10% and **1.43656 ps**.

Extracted hand-run `inv_1` grid, **196 points**:

| Table | Points | Median % | Worst % | Median absolute | Worst absolute | >10% and >5 ps |
|---|---:|---:|---:|---:|---:|---:|
| `cell_fall` | 49 | 14.0110% | 235.211% | 22.3268 ps | 123.020 ps | 0 |
| `cell_rise` | 49 | 15.9622% | 59.4392% | 38.5548 ps | 196.598 ps | 43 |
| `fall_transition` | 49 | 8.57741% | 17.2634% | 7.45750 ps | 159.565 ps | 1 |
| `rise_transition` | 49 | 14.4705% | 27.2874% | 11.4437 ps | 408.860 ps | 25 |
| **All tables** | **196** | **14.3659%** | **235.211%** | **15.8202 ps** | **408.860 ps** | **127** |

Across all 196 points, 148 exceed 10%, 145 exceed 5 ps, and **127 exceed both 10% and 5 ps**. The large percentage errors on `cell_fall` at near-zero delays do not coincide with >5 ps absolute error; conversely, most rising-delay errors are substantial in both measures.
