# Milestone 3c closing evidence

This report states whether the measured gap follows the kit, follows the simulator, or cannot be separated. It does not recommend a direction.

## Method agreement on SkyWater

Hand-run and CharLib extracted `inv_1` grids matched at **196 of 196 points**. Median absolute differences between methods were below 1 ps for every table:

| Table | Median method difference | Worst method difference |
|---|---:|---:|
| `cell_fall` | 0.189200 ps | 8.38200 ps |
| `cell_rise` | 0.295000 ps | 354.519 ps |
| `fall_transition` | 0.946200 ps | 241.055 ps |
| `rise_transition` | 0.468900 ps | 208.029 ps |

The worst disagreements occur at the slowest input and largest load. Most of the grid therefore does not show two independent large implementation errors.

## SkyWater versus IHP

All figures use CharLib with ngspice 44.2 and each kit's typical models. SkyWater `inv_1` uses the Magic-extracted netlist; IHP `sg13g2_inv_1` uses its supplied schematic netlist with junction geometry. Each row covers **196 points**.

| Kit/cell | Median % | Worst % | Median absolute | Worst absolute |
|---|---:|---:|---:|---:|
| SkyWater `inv_1`, extracted | 14.6039% | 260.480% | not recorded in 3b | not recorded in 3b |
| SkyWater `inv_1`, hand-run extracted | 14.3659% | 235.211% | 15.8202 ps | 408.860 ps |
| IHP `sg13g2_inv_1` | 4.65003% | 64.5966% | 15.2825 ps | 240.681 ps |

For a second SkyWater cell, schematic `nand2_1`, CharLib gives median **9.11900%** and **15.0047 ps**, worst **284.899%** and **224.695 ps**, over **392 points**.

The IHP Liberty header names IHP Microelectronics, a 2025 date and revision 0.1.4, but does not name the tool that produced it. Its separate model files identify PSP 103.6 for ngspice; that does not establish the Liberty producer.

## Interpretation

- **The percentage gap follows the kit/model/library combination much more than it follows ngspice alone.** The same simulator and CharLib revision produce a 4.65003% median on IHP versus 14.6039% on extracted SkyWater `inv_1`, a difference of 9.95387 percentage points over 196 points each. If the gap were a uniform ngspice limitation, similarly large median errors would be expected on both kits; they are not observed.
- **The gap is not absent on IHP.** Its worst percentage is 64.5966%, and its median absolute error is 15.2825 ps, close to the SkyWater hand-run median of 15.8202 ps. Thus absolute residuals and extreme-grid behavior are shared to some degree, while percentage error is substantially kit-dependent.
- **The evidence cannot isolate model physics from foundry characterization methodology.** The kits use different transistor models, netlist content, grids and unknown Liberty-production flows. The IHP header does not identify its producer. No controlled substitution of one kit's models into the other's flow was performed.

**Conclusion: the large percentage gap primarily follows the kit/model/library combination, not the simulator alone; shared absolute residuals remain, and model-versus-foundry-method effects cannot be told apart by these runs.**

**STOP: no recommendation.**
