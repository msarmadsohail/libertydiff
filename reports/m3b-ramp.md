# Corrected input ramp

The table's input transition is the 20%–80% time. With slew derating 1.0, the full linear 0–100% ramp is `0.122474 / 0.6 = 0.204123333333 ns`. Only the two PWL edge durations changed from the milestone 2 bench; model includes, load, thresholds and numerical options are unchanged.

One `inv_1` arc at input transition 0.122474 ns and load 0.00952062 pF; four table points compared.

| Table | Foundry (ns) | Before (ns) | Before error | After (ns) | After error |
|---|---:|---:|---:|---:|---:|
| `cell_fall` | 0.0872580 | 0.0594680 | -31.8481% | 0.0740555 | -15.1304% |
| `cell_rise` | 0.1211221 | 0.107017 | -11.6454% | 0.130357 | +7.62445% |
| `fall_transition` | 0.0598601 | 0.0422483 | -29.4216% | 0.0536647 | -10.3498% |
| `rise_transition` | 0.0916769 | 0.0934824 | +1.96942% | 0.0955135 | +4.18491% |

Median absolute error: 20.5335% before, 8.98713% after. Worst absolute error: 31.8481% before, 15.1304% after.

The corrected values agree with the owner review's approximately -15%, +8%, -10% and +4%.

Command:

```sh
ngspice_con.exe -b work/m3b-inv_1-ramp.cir -o work/m3b-inv_1-ramp.log
python checker/compare.py work/m3b-inv_1-ramp.json <foundry.lib> --output work/m3b-inv_1-ramp-comparison.csv
```
