# Milestone 2 smoke comparison

One `sky130_fd_sc_hd__inv_1` arc (`A->Y`), at input transition 0.122474 ns and output load 0.00952062 pF: the fourth of seven points on each grid. Four table points compared.

| Table | Generated (ns) | Foundry (ns) | Error |
|---|---:|---:|---:|
| `cell_fall` | 0.0594680 | 0.0872580 | -31.8481% |
| `cell_rise` | 0.107017 | 0.1211221 | -11.6454% |
| `fall_transition` | 0.0422483 | 0.0598601 | -29.4216% |
| `rise_transition` | 0.0934824 | 0.0916769 | +1.96942% |

Median absolute error: 20.5335%. Worst absolute error: 31.8481%.

## Simulator and options

- ngspice 41, `ngspice_con.exe -b work/m2-inv_1.cir -o work/m2-inv_1.log`.
- `.temp 25`; supply 1.8 V; typical `nfet_01v8` and `pfet_01v8_hvt` models.
- `.option ngbehavior=ps` for the kit's subcircuit parameter syntax.
- `.option scale=1e-6` because the kit expresses device geometry in micrometres.
- `.param mc_mm_switch=0 mc_pr_switch=0`: no mismatch or random process variation.
- `.tran 0.001n 5n` (1 ps print step; ngspice's internal adaptive time step).
- Default simulator tolerances; no explicit `reltol`, `abstol`, `vntol`, `trtol`, or `method` option.
- Linear input from 0 to 1.8 V over 0.122474 ns, then 1.8 to 0 V over the same duration.
- Delay measured between 50% input and 50% output crossings; output transition measured between 20% and 80% crossings. Slew derating is 1.0.

Command:

```powershell
python libertydiff\compare.py work\m2-inv_1.json pdk\ciel\sky130\versions\e7a6777d157a9d94c7ac757457b9e4309e9e9000\sky130A\libs.ref\sky130_fd_sc_hd\lib\sky130_fd_sc_hd__tt_025C_1v80.lib --output work\m2-inv_1-comparison.csv
```

## Simulator sensitivity

The tightened run used `.tran 0.0001n 5n` (0.1 ps print step), `.option reltol=1e-5 abstol=1e-15 vntol=1e-8 trtol=1`, and otherwise identical settings.

| Measurement | Baseline (ns) | Tightened (ns) | Movement |
|---|---:|---:|---:|
| `delay_fall` | 0.059468000 | 0.059469600 | +0.002691% |
| `delay_rise` | 0.107017000 | 0.107018000 | +0.000934% |
| `transition_fall` | 0.042248300 | 0.042239100 | -0.021776% |
| `transition_rise` | 0.093482400 | 0.093480700 | -0.001819% |

All four movements are below 1%, so no tighter project defaults are required by this check.
