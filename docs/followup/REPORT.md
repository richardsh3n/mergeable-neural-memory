# Follow-up experiment report

**2026-11-18 · bounded synthetic diagnostics · exploratory**

The frozen phase-one result remains **78.85% for the symmetric residual
versus 79.33% for MAXSET**, a paired difference of **−0.47 percentage points**
with a conditional 95% interval of **[−1.23, +0.32]**. The 173-assertion
artifact audit reconstructed the result. H1 remains unsupported. The prior
v0.2 writer-adaptation experiment measured +11.82 points versus local-only
adaptation, conditional on three inherited fits. Its world-macro fit means
were 79.54% versus 67.72%. The progression gate failed and a seeding deviation
was documented. [Frozen v0.1 report](../PILOT_REPORT.md) ·
[Existing v0.2 archive](https://github.com/richardsh3n/mergeable-neural-memory/tree/dd0354217812841d4535576eea3d8071cd8bf3d6/experiments/v02)

## What the frozen encoder kept

Each fit and pooling rule saw the same 576 held-out counterfactual pairs.
The variants have the same local two-hop label (unknown) and diverge after an
identical bridge arrives. Ridge readouts use 96 training pairs per key from
an independent stream. Reported percentages count variants separately.
The shuffled-target probe is a control against the 16.67% chance level.

| Fit | Pool | Exact collision pairs | Probe | Shuffled probe | Frozen direct fact | Frozen local unknown recall | Frozen union two-hop |
|---:|---|---:|---:|---:|---:|---:|---:|
| 11 | SUM | 0/576 | 100.00% | 16.49% | 99.83% | 100.00% | 100.00% |
| 11 | MAX | 0/576 | 98.70% | 16.06% | 99.83% | 100.00% | 100.00% |
| 23 | SUM | 0/576 | 100.00% | 16.06% | 92.88% | 20.05% | 86.28% |
| 23 | MAX | 0/576 | 92.45% | 16.23% | 95.23% | 19.70% | 90.54% |
| 37 | SUM | 0/576 | 85.50% | 16.23% | 73.44% | 52.60% | 52.52% |
| 37 | MAX | **2/576** | 78.21% | 16.32% | 74.22% | 47.22% | 53.73% |

Fit 37's MAX states were equal in pairs `113` and `297`. In pair `113`,
changing the edge `(entity 1, relation 0)` from target 0 to target 5 left
the input state unchanged. Adding `(entity 4, relation 1, entity 1)`
requires a different answer to query `(4, 1, 0)`. A deterministic system
given the same two states and query can answer at most one variant correctly.
This proves a concrete loss for that writer on the constructed task. The
collision rate is specific to this dense corpus, and the absence of collisions
in other cells leaves losslessness unresolved.

Fit 37's SUM state carries a signal for the future edge (85.50% probe), yet
its native two-hop accuracy is 52.52%. For both pooling rules, union re-encoding
and the disjoint state-only merge yield identical top-1 scores across all fits.
A weak residual merger alone cannot explain this gap. The probe diagnoses
readability of one edge in a specialized decoder. It does not measure
information in bits or establish that the native reader is the sole bottleneck.

## Three real parties and repeated delivery

Three known two-hop queries require AB, BC and CA respectively within each
world. Individual queries need two sources. Both overlap settings contain
128 worlds and 384 queries per inherited fit. Means weight fits equally.
Sampled overlap applies to distractor duplication. We rejected 198 worlds
with shared critical keys at overlap 0 and 194 at overlap 0.5.

| Method | (AB)C at 0 overlap | (AB)C at 0.5 | 12-tree accuracy range at 0.5 | A(BC) answer agreement at 0.5 | After 1 / 2 / 4 / 8 A redeliveries at 0.5 |
|---|---:|---:|---:|---:|---:|
| Symmetric residual | 78.13% | 79.34% | 78.21–79.34% | 95.14% | 74.83% / 62.67% / 45.49% / 38.19% |
| DeepSets | 38.72% | 34.98% | 34.98–37.41% | 62.59% | 22.14% / 14.76% / 10.24% / 9.29% |
| SUM | 76.13% | 76.65% | 76.65–76.65% | 100.00% | 69.53% / 59.64% / 49.83% / 47.22% |
| MEAN | 74.22% | 68.66% | 68.49–68.75% | 78.04% | 54.17% / 42.01% / 32.47% / 4.17% |
| MAXSET | 78.39% | 80.38% | 80.38–80.38% | 100.00% | 80.38% / 80.38% / 80.38% / 80.38% |

All methods passed the sampled swap check with zero state difference. At
overlap 0.5, residual reassociation has mean relative L2 **0.0612** and
self-merge of the aggregate has **0.6655**. Duplicating A's events before
encoding preserved 83.51% of residual answers and 100% of MAXSET answers.
The residual and DeepSets are symmetric by construction. SUM's tree
difference is consistent with float32 rounding. MEAN passes self-merge
and changes under re-bracketing. MAXSET's state matched full-union max
re-encoding exactly on this run and stayed identical across all trees and
redeliveries. It still made errors, as the continuation test predicts can occur.
These are delivery diagnostics for identical tuples using archived two-party
weights on a new three-way partition. They provide no guarantee for corrections,
conflicts or independently trained writers.

## Capacity pressure and baseline fairness

Two new fits per cell used the same held-out corpus within each relation
count and overlap. Widths 4, 12 and 24 at two slots used 32, 96 and 192 bytes.
At overlap 0.5 the two-relation corpus averaged 20.29 union facts and the
eight-relation corpus 81.92. Actual intersection-over-union averaged 42.28%
and 47.87%. Both had 117 worlds with a known two-hop query. The realized
unknown rates were 22.27% and 19.53% of all queries, respectively.

The table gives known two-hop world-macro accuracy at overlap 0.5,
with equal means over seeds 101 and 307.

| Relations | Payload | Shared SUM | Shared MAXSET | Dedicated SUM | Dedicated MAXSET | Packed table |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 32 B | 0.00% | 0.00% | 0.00% | 0.00% | 100.00% |
| 2 | 96 B | 0.00% | 0.00% | 0.00% | 0.00% | 100.00% |
| 2 | 192 B | 0.00% | 0.00% | 0.00% | 0.21% | 100.00% |
| 8 | 32 B | 0.00% | 0.00% | 0.00% | 0.00% | 38.03% |
| 8 | 96 B | 0.00% | 0.00% | 0.00% | 0.00% | 100.00% |
| 8 | 192 B | 0.00% | 0.00% | 0.00% | 0.00% | 100.00% |

With disjoint evidence, all neural cells scored 0.00% on this endpoint.
The truncated packed table scored 42.02% at 32 bytes and 8 relations,
and all full-table cells scored 100.00%. The byte-matched table is a
substantive state-only competitor for these typed IDs. It stores 64 of 96
keys at 32 bytes and 8 relations. Full tables need 12 or 48 bytes,
depending on relation count. Their exact lookup exploits the problem schema.

Across both strata, the shared arms, dedicated SUM and both residual
ablations always predicted unknown. Dedicated MAXSET made a few known
predictions. In the 192-byte, two-relation, overlap-0.5 cell its per-fit
scores were 0.00% and 0.43%. The maximum observed full-reencode score
also came from that same MAXSET fit. The residual state-teacher ablation
at 96 bytes and two relations tied the answer-only and plain SUM arms
at **0.00%** in both strata. This floor prevents a causal interpretation
of the ablation. The 240-step fits are a feasibility check. The two-slot
reader, training length, width and curriculum are all plausible contributors
to collapse. Parameter counts varied from 19,497 to 26,061 across cells.
This run yields neither a learned capacity curve nor a ranking of
trainable baselines that have learned the task.

## Evidence and verification

The [protocol](PROTOCOL.md) and configuration were recorded before running.
All cells and final fits are in the machine-readable results, including
failed cells. The read-only auditor independently reconstructed **974**
score cells and labels from the saved evidence, and verified all 12
checkpoint hashes in the full local run. The published evidence includes
predictions, held-out facts, fit traces, and input and output hashes.
A fresh rerun on the same environment reproduced the result JSON, compressed
per-query evidence and all 12 checkpoints byte for byte. The run timestamp
is recorded separately. The final test suite passed 27 tests. All 46 original
package paths still match their published hashes. See [reproduction commands](README.md).
