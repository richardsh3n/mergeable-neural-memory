# Claim ledger

This ledger distinguishes the proposed research agenda from executed evidence.

| Claim | Evidence required | Status after locked pilot |
|---|---|---|
| Fixed-size neural state | All persisted coordinates and metadata counted | Verified: 12 × 24 float32 coordinates = 1,152 payload bytes; shared weights and temporary allocations separate |
| No event replay at merge/read | Function input and storage audit | Verified inference boundary: merger receives two tensors, reader state/query; union teacher is training-only; replay references separately labeled |
| Useful cross-party relations | Held-out known two-hop queries, local ambiguity checks, A/B controls | Limited support in this task: residual 78.85%, private A/B about 5.85%/5.77%, swapped B 16.15%; three fits vary greatly |
| Better than strong simple pooling | Paired held-out comparison and all baseline results | Unsupported: residual − MAXSET −0.47pp, conditional 95% CI [−1.23,+0.32]pp; MAXSET strongest evaluated nonreplay mean |
| Commutativity | Symmetric architecture plus numerical tests | Constructed symmetry; zero observed normalized defect for candidate on registered states |
| Associativity and idempotence | State and behavior diagnostics | Not guaranteed: candidate relative defects 0.1486 / 0.6360; associativity probe weak and not semantic |
| Strong compression | Increasing entity/event counts under same byte budget | Not tested; tiny pilot fits in an explicit table much smaller than the neural state |
| Semantic duplicate recognition | Natural-language aliases, event identity and provenance | Not tested |
| Continued learning after merge | New writes and corrections after merging | Follow-on study; not in the primary pilot |
| LLM memory improvement | Real pretrained language backbone and natural-language evaluation | Not tested |
| Human-like cognition / consciousness | Outside this study | No claim |
| Novel architecture or priority | More literature review and a distinct effective mechanism | Provisional; no first-ever claim |

Training uses executable labels and a deduplicated full-state teacher. That is
privileged supervision during training, not information available at inference.
The learned merger has extra trainable parameters and optimization steps. Equal
persistent-state bytes do not imply equal training cost or equal total compute.

The synthetic reader takes typed entity/relation IDs and has two explicit read
passes. It does not learn arbitrary natural-language parsing, unbounded inference
depth, new entity vocabularies, or the general meaning of a relationship.

Any result written after the pilot must identify its exact stratum and seed scope.
An advantage over max alone is not an advantage over every simple baseline.

The frozen primary result is negative; all outcomes are preserved. `results/audit.json`
passes 173 assertions and independently reproduces the primary effect and interval.
The missing generator rejection-attempt counters remain an explicit reporting
omission. No pretrained LLM result, strong compression result or publication-level
architecture claim is supported by this archive.
