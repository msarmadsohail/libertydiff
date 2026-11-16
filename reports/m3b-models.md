# Kit model entry point

The requested direct replacement with `sky130.lib.spice`, section `tt`, did not simulate successfully in this environment:

- Native ngspice 41 could not resolve the kit's nested relative includes from the repository working directory and timed out after 300 s.
- In Linux, running from `libs.tech/ngspice` resolved those includes, but full model elaboration ended with `Undefined parameter [l]`, `Cannot compute substitute`, and fatal formula errors in unrelated device models. `ngbehavior=ps` and `hsa` both failed.
- A scratch entry point retaining the kit's `tt` definitions for `nfet_01v8`, `pfet_01v8_hvt`, their mismatch files and `tt/nonfet.spice`, but excluding unrelated device families, completed with exit code 0. The two transistor model files used by `inv_1` are unchanged.

Four measurements at the same corrected-ramp point:

| Measurement | Four hand-picked files (ns) | Kit `tt` content (ns) | Movement |
|---|---:|---:|---:|
| `delay_fall` | 0.074055500 | 0.074055500 | 0.000000000% |
| `delay_rise` | 0.130357000 | 0.130357000 | 0.000000000% |
| `transition_fall` | 0.053664700 | 0.053664700 | 0.000000000% |
| `transition_rise` | 0.095513500 | 0.095513500 | 0.000000000% |

Thus the kit's additional non-FET parameters do not move this inverter point at ngspice's printed precision. The full top-level entry point itself remains unusable here because unrelated models fail during elaboration.

Final diagnostic command:

```sh
ngspice -b /work/work/m3b-inv_1-kitmodels-pruned.cir -o /work/work/m3b-inv_1-kitmodels-pruned.log
```

This ran in `cellchar-charlib:987e90f-trixie-np2` with a 300 s timeout. Scratch decks and logs are under `work/m3b-inv_1-kitmodels*`.
