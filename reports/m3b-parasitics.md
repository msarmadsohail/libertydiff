# Schematic versus extracted `inv_1`

The kit does not ship an extracted `inv_1` netlist in its `spice/` or `cdl/` directories. The CDL adds device-level area/perimeter information but no wiring-capacitor network. Magic layout exists at `libs.ref/sky130_fd_sc_hd/mag/sky130_fd_sc_hd__inv_1.mag`.

Debian bookworm's Magic 8.3.105 could not parse the kit technology file. Magic **8.3.703**, built from source in Docker image `cellchar-magic:latest`, extracted it successfully:

```sh
magic -dnull -noconsole -T /pdk/sky130A/libs.tech/magic/sky130A.tech /work/work/m3b-extract.tcl
```

The extracted netlist contains source/drain areas and perimeters plus 14 explicit capacitors. Both grids use the same corrected ramp, 49 simulations and 196 table points.

| Table | Schematic median | Extracted median | Schematic worst | Extracted worst |
|---|---:|---:|---:|---:|
| `cell_fall` | 19.5153% | 14.0110% | 353.502% | 235.211% |
| `cell_rise` | 12.7534% | 15.9622% | 34.5282% | 59.4392% |
| `fall_transition` | 16.9830% | 8.57741% | 47.9710% | 17.2634% |
| `rise_transition` | 11.3403% | 14.4705% | 31.2534% | 27.2874% |
| **All tables (196 points each)** | **14.9399%** | **14.3659%** | **353.502%** | **235.211%** |

Parasitics materially improve falling delay and falling transition, slightly worsen rising delay, and reduce the overall median by 0.574 percentage points. The largest residual errors remain at slow inputs and small loads for delay; both extracted transition-table worst cases occur at 1.5 ns input and 0.181284 pF load.

An initial extracted run accidentally retained the schematic include and was discarded. All logs were deleted before the verified run; generated decks were checked to contain `work/m3b-inv_1-extracted.spice`.

Commands:

```sh
python work/m3b-run-grid-extracted.py
python checker/compare.py work/m3b-inv-grid-extracted.json <foundry.lib> --output work/m3b-inv-grid-extracted-comparison.csv
```
