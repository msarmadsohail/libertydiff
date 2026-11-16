# CharLib measured error

CharLib 2.1.0, commit `987e90f5286b11c3a548749f93b689a7b8723003`, run on all ten cells at typical/25 °C/1.8 V. Four parallel workers; elapsed time 3,953.83 s (65 min 53.83 s), including 7,509 characterization operations. The generated Liberty file contains delay and transition tables for every requested cell.

| Cell | Points compared | Median absolute error | Worst absolute error |
|---|---:|---:|---:|
| `inv_1` | 196 | 49.8439% | 1546.16% |
| `inv_2` | 196 | 36.9028% | 5120.29% |
| `buf_1` | 196 | 62.1515% | 4525.44% |
| `nand2_1` | 392 | 57.0440% | 2371.38% |
| `nand3_1` | 588 | 58.6632% | 1313.19% |
| `nor2_1` | 392 | 46.3576% | 6795.10% |
| `nor3_1` | 588 | 49.6970% | 2607.70% |
| `and2_1` | 392 | 52.4148% | 2990.00% |
| `or2_1` | 392 | 50.2738% | 3280.66% |
| `xor2_1` | 392 | 57.7225% | 1555.74% |
| **All cells** | **3,724** | **53.2228%** | **6795.10%** |

Each single-input cell contributes four tables × 49 points; each two-input cell contributes two arcs × four tables × 49 points; each three-input cell contributes three arcs × four tables × 49 points. The checker matched CharLib's rounded grid values to the foundry grids.

## Reproduction and limitations

- Native Windows installation failed before characterization: PySpice imports Unix-only `fcntl`.
- Docker image `cellchar-charlib:987e90f-trixie-np2`: `python:3.12-trixie`, Debian `ngspice` 44.2, CharLib commit above, and its modified PySpice at `da81c4d013c9140c8833711be05c52299b260e16`.
- The image uses NumPy 2.5.5. PySpice emits a binary-compatibility warning on import, but the run exits 0 and writes all ten cells. NumPy 1 could not be used because this CharLib revision calls `numpy.trapezoid`.
- The model include selects only typical `nfet_01v8` and `pfet_01v8_hvt` models, sets `ngbehavior=ps`, `scale=1e-6`, and disables mismatch. These are the same physical model settings as the hand-run bench.
- Command: `docker run --rm -v <repo>:/work -v <pdk-version>:/pdk cellchar-charlib:987e90f-trixie-np2 charlib run /work/work/m3-charlib.yml --output /work/work/m3-charlib-results -j 4`.
- Comparison: `python libertydiff/compare.py work/m3-charlib.lib <foundry.lib> --output work/m3-charlib-comparison.csv`.

The very large worst errors are measured results, not clipped or adjusted values. They should be interpreted alongside the hand-run result and the grid/arc conventions before choosing a project direction.
