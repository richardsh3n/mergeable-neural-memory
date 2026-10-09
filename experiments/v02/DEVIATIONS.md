# v0.2 protocol deviations

## D1 — training random-number stream

**Registered text:** `PREREGISTRATION.md` specifies a per-step seed of `420000 + fit seed x 10000 + step`.

**Executed behavior:** `run.py` seeded one NumPy generator per fit with `420000 + fit seed x 10000`, then consumed it sequentially across optimizer steps. The local and future arms each restarted that same stream; their step-level corpus hashes and attempt counts match exactly.

**Impact:** The paired arm contrast remains matched and uses fresh generated worlds, but the exact per-step corpus sequence differs from the written protocol. This is a protocol deviation, so the result must be described as a *locally preregistered diagnostic with a disclosed RNG-seeding deviation*, not as a perfectly protocol-conformant confirmatory result. No endpoint, exclusion, stopping rule, model, or outcome was changed in response. Future confirmatory work must either re-run with per-step reseeding from a fresh freeze or preregister the continuous-stream design explicitly.

## D2 — result serialization after inference

The complete frozen evaluation ran and wrote all per-query probabilities. The original process then failed while serializing a NumPy boolean in the aggregate summary. A post-hoc script aggregates the archived rows without rerunning training or inference; it is hashed in `POSTHOC.json`.

## D3 — audit-control assembly on first invocation

The initial invocation stopped before outcome metrics because the three-party audit helper repeated the same evidence four times per world. The retained log documents the failure. The control was corrected to partition each world's evidence once, then the full run was restarted. No metrics were produced or inspected in the failed invocation.
