# Exploratory follow-up protocol

This small CPU run investigates mechanisms after the archived negative result.
The v0.1 configuration, source, manuscript, evaluation endpoint, and artifacts
are historical inputs. The v0.2 experiment on the separate research branch is
prior evidence. Neither experiment is rerun by this protocol. The runner
records input hashes before scoring or fitting and uses a new output directory.

## Frozen-encoder continuation challenge

Use all three v0.1 checkpoints, with no neural-model updates. Generate pairs of
functional worlds that differ in exactly one local fact, the target of a
particular continuation edge `u --r2--> x`. The other party's evidence is an
identical bridge `s --r1--> u` in both worlds. The bridge is absent from the
local evidence. The local two-hop target is unknown in both variants. Both
variants' joint targets are known and different. The encoder receives no query.
Sample each of the 12 continuation keys equally. Keep each variant pair
together in independent probe-training and evaluation streams.

Evaluate exact numeric equality of local float32 tensors and record normalized
pair distances. Exact equality with different joint labels is a direct
counterexample for a deterministic state-only merger/reader on that pair.
Near equality and unsuccessful readout are diagnostic only. Evaluate the
frozen reader on local direct-edge recall, local unknown, merged two-hop
accuracy, and full-reencode two-hop accuracy, separately for sum and max states.
The sum merge here is disjoint. Fit one regularized linear readout per key on
training local states, using the local edge's object as the label. Center and
scale by training-state RMS before fitting. Use the same
fit with shuffled training labels as a control. The probe predicts one of six
entities, chance 1/6. Readout success shows recoverability under this probe,
while probe failure can reflect model class, data, or regularization.

## Three-party tests on v0.1 weights

Reuse the three archived fits and compare symmetric residual, DeepSets, SUM,
MEAN, and MAXSET. Generate a fresh six-entity, two-relation world with three
known two-hop queries. Assign their critical edges exclusively to AB, BC, and
CA respectively. Require six distinct critical keys and independently validate
that every query remains ambiguous after removing either of its two required
parties. Distractor overlap is sampled at 0 and 0.5 with a duplicate in one other
party when selected. The sampler counts rejected attempts. This tests three
parties contributing to one common set of queries. Each individual query uses
two parties and two reads.

Measure swapped-order, reassociated, and self-merged states with relative
L2 error, top-1 agreement, and world-macro correctness. Evaluate all twelve ordered three-leaf binary trees (six input permutations
with both bracketings). Test source redelivery
after A+B+C at 1, 2, 4, and 8 repeats, self-delivery of the full aggregate,
and within-party duplicate events before encoding. Compare to privileged
deduplicated pooled-union references. Report the conditional descriptive
results for every fit, method, overlap, and variant. No retraining for three
parties or tuning from results.

## Capacity and baselines

Cross 32, 96, and 192 retained float32 bytes with 2 and 8 functional relation
types, at 12 entities and two reader slots. Keep hop depth fixed. Relation count
increases the maximum number of stored facts at the same budget. State width
also changes parameter count, so record counts and treat this as a joint
payload and model-width intervention. A dense functional table with unknown
code needs 12 bytes at 2 relations and 48 at 8 relations. Only the 32-byte,
8-relation cell is below that table's size. This is distinct from a lower bound
for the distribution of sampled sparse worlds.

Retain v0.1 evaluation units: four queries sharing evidence (two one-hop and two
two-hop), known two-hop world-macro accuracy, single-party ambiguity checks,
and the unknown class. Across methods and fit seeds, evaluate the same fresh
worlds within each relation count and overlap. Measure mean overlap and union
size, realized unknown rates, all-query accuracy and unknown recall. Preserve
every fit. The two new fit seeds and the two overlap strata give descriptive
results only. No new hypothesis test or substitution for the frozen endpoint.

Train shared (v0.1 four-mode cycle), dedicated SUM, and dedicated MAXSET
backbones on matched streams and identical 240-step budgets. Keep the writer
and two-read architecture intact. Compare shared SUM and MAXSET, shared
deduplicated sum and max re-encoding, dedicated SUM and MAXSET, their replay
references, and a byte-matched packed functional table. The table stores
deterministic key-prefix entries when bytes are insufficient. It abstains on
unretained keys and merges without replay in conflict-free worlds. Also evaluate
the raw union label oracle as a privileged implementation check. At the
96-byte and two-relation cell, include paired residual fits with and without
the full-state consistency loss, same backbone, initialization, data stream,
objective otherwise, and 160 steps each. Plain shared SUM is the zero-residual
control. Run all the specified cells, final checkpoints only.

## Reproducibility

Run CPU with deterministic PyTorch settings and one thread. Use
`requirements.lock.txt`, fresh output, archived checkpoint hash verification,
and distinct seeds for training and held-out worlds. Persist seeds, complete
evaluation predictions and corpora, training traces, final parameters,
per-condition rejection counters, and artifact hashes. This is a local,
exploratory run. Larger fit budgets, precision-matched architectural comparisons,
new readers or writers, and three-hop behavior require a separate decision.
