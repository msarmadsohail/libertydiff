# IHP SG13G2 smallest inverter

Fetched with ciel 3.2.0: `ihp-sg13g2` version `cc9afba57e0ec1b5ba77e6bbb638ba9dbe5866b8`, libraries `sg13g2_stdcell` and `sg13g2_pr`. Cell: `sg13g2_inv_1`, the smallest numbered inverter. Typical corner: `sg13g2_stdcell_typ_1p20V_25C.lib`, 1.2 V, 25 °C.

## Liberty header and producer

The header states:

> `comment : "IHP Microelectronics GmbH, 2025";`
>
> `date : "$Date: Tue Nov  4 21:19:14 2025 $";`
>
> `revision : "$Revision: 0.1.4 $";`

It declares 50% delay thresholds, 20%/80% slew thresholds and slew derating 1. **No simulator or characterizer producer is named anywhere in the Liberty header.** The kit's separate `cornerMOSlv.lib` identifies its device model as `NGSPICE`, `PSP 103.6`, revision `200310`; that is the transistor model, not evidence of what produced the Liberty file.

## Simulation setup

The kit supplies Verilog-A PSP source but no compiled OSDI modules. OpenVAF Reloaded `v24.0.2mob` compiled `psp103.va` and `psp103_nqs.va`; image `cellchar-openvaf:latest` supplies LLVM 18 and ngspice 44.2. A local `.spiceinit` loads both modules with `osdi` before circuit parsing. CharLib commit `987e90f`, unchanged code, four workers.

The full run completed **395 operations in 4,728.70 s** (78 min 48.70 s). Four tables × 49 points: **196 points**.

| Table | Points | Median % | Worst % | Median absolute | Worst absolute |
|---|---:|---:|---:|---:|---:|
| `cell_fall` | 49 | 5.24872% | 15.4169% | 18.6680 ps | 162.189 ps |
| `cell_rise` | 49 | 3.91871% | 13.1912% | 15.8840 ps | 141.687 ps |
| `fall_transition` | 49 | 6.23063% | 64.5966% | 15.8230 ps | 240.681 ps |
| `rise_transition` | 49 | 3.13145% | 49.9944% | 11.0090 ps | 200.955 ps |
| **All tables** | **196** | **4.65003%** | **64.5966%** | **15.2825 ps** | **240.681 ps** |

The IHP median percentage error is much lower than SkyWater's, although absolute errors remain nonzero and transition errors still peak at extreme grid points.

Commands:

```sh
charlib run /work/work/m3c-ihp.yml --output /work/work/m3c-ihp.lib -j 4
python checker/compare.py work/m3c-ihp.lib <ihp-foundry.lib> --output work/m3c-ihp-comparison.csv
```
