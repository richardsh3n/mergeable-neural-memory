# Adversarial protocol review

Review date: **2026-10-09** (client-provided date). Scope: the bounded synthetic pilot in `PREREGISTRATION.md`. This document records design threats and release conditions; it does not report trained results or external peer review.

## Principal assessment

The pilot can test whether an additionally trained symmetric merger improves joint-evidence query accuracy under distractor overlap. It cannot establish a new general memory theory, a human-memory analogue, a neural CRDT, superior LLM memory, strong compression, or compute efficiency. A positive result against MAXSET alone is a narrow comparator result. DeepSets and arithmetic baselines must remain visible.

## Threats and required treatment

| Threat | Required treatment |
|---|---|
| A missing edge is still inferable | Independently sample relational targets rather than use bijections. For every known two-hop test query, require at least two consistent answers for each private party. The evaluator-only ambiguity oracle may not enter inference. |
| Shortcut from entity names | Rename all entities per world, including facts and query. Report shared vocabulary and task-specific two-read inductive bias. This is not unseen-entity generalization. |
| Shortcut from labels or full evidence | Model methods receive only their declared event/state/query arguments. Poisoning labels and reference tensors after state creation must leave inference unchanged. |
| False same-representation comparison | MAXSET uses max pooling of shared features; the main method uses sum pooling. Match input facts, state shape, precision, and shared weights; disclose the pooling difference. |
| Extra training mistaken for an architectural advantage | Disclose the main merger's extra parameters, answer labels, union-state teacher, and training. Include DeepSets with the same learned-merger budget. No equal-total-cost claim against arithmetic baselines. |
| Unknown class dominates accuracy | Report realized class fractions and known/unknown metrics. A 0.20 edge-deletion opportunity is not a 20% unknown class guarantee. Use known two-hop queries for H1. |
| Pseudoreplication | Keep four-query worlds intact in the bootstrap. The primary statistic is world macro, then an equal-weight mean of three fits. State that the CI conditions on these fits. |
| Successful stratum selected after testing | Freeze overlap 0.50, known two-hop queries, learned–MAXSET contrast, metric and bootstrap seed before fitting. Secondary findings do not replace H1. |
| State count ignores hidden storage | Retained output is exactly 1,152 float32 payload bytes. Count any per-world metadata or auxiliary state. Report two input states and transient buffers separately from retained state. |
| Algebraic labels exceed guarantees | The main operation is commutative and has an empty-input identity by construction. Idempotence and associativity require measurement and are not guaranteed by symmetric input features. |
| Numerical probes mistaken for semantic tests | Cross-world three-state defects are numerical probes. Same-world three-party semantic integration needs a separate partition and label audit. An untrained unit test does not prove a trained capability. |
| Re-encoding called an upper bound | Treat full-union re-encoding as a privileged raw-evidence reference, not a guaranteed performance bound or state-only competitor. |
| Finite state called strong compression | The six-entity toy relation table contains far less information than 1,152 bytes. This pilot does not impose a convincing information-capacity bottleneck. |
| Future capabilities reported as completed | Revisions, corrections, conflicts, deletion, incompatible encoders and LLM-scale memory are follow-ups. Reserved embeddings or toy test utilities do not demonstrate them. |

## Standard algebraic limitation: exact merging needs union congruence

Let `E` map finite fact sets to memory states. An exact state-only merger satisfying

`m(E(A), E(B)) = E(A union B)`

for every pair exists on the image of `E` **if and only if** equality of encoded states is a congruence for union:

`E(A) = E(A')  =>  E(A union B) = E(A' union B)` for every `B`.

Necessity follows by applying the same merger to equal first inputs and the same second input. For sufficiency, define the merger using any representatives of each state. The congruence condition makes changing the first representative harmless; commutativity of set union gives the same fact for the second representative. Thus the operation is well defined. On reachable states, exact set union then supplies commutativity, associativity, idempotence and the empty-set identity.

This is a standard quotient/congruence argument, **not a claimed novel theorem**. It does not show that this neural encoder satisfies the condition, or that an approximately trained merger inherits exact laws. Query-answer equivalence is weaker than identical encoded states and requires its own sufficiency condition; do not conflate the two.

A scalar counterexample makes the limitation concrete. Let a fact's numeric value be its feature, and let `E(A)` be the sum of distinct facts. Then `E({1,2}) = E({3}) = 3`. Merging either with the state of `{1}` would require both 3 and 4 as outputs: `{1,2} union {1}` encodes to 3, whereas `{3} union {1}` encodes to 4. No exact state-only set-union merger can meet both requirements. Lossy collisions can therefore destroy information needed for deduplication, even when the input states coincide.

## Pre-run gate

Before fitting, verify the executed source and final configuration match the preregistration, including DeepSets, world-macro H1, the fixed budgets, and the absence of revision examples. Run meaningful checks of state dtype/bytes, inference information boundaries, private ambiguity, renaming, shared-world grouping, deterministic generation, and the MAXSET/re-encoding algebra.

Then save a freeze manifest with an observed UTC time and SHA-256 hashes of protocol, configuration, executed source, tests, and dependencies. Training logs must begin after that freeze. A checksum computed after training does not establish pre-run registration. The freeze is local; do not describe it as an external registered report.

At reporting time, verify all three final checkpoints and all comparator predictions exist, primary world/query counts are present, and the bootstrap can be reconstructed from saved per-world outputs. State controls, duplication and merge-tree diagnostics must be labeled by what was actually executed. Unsupported H1, stronger arithmetic baselines, instability, and omitted diagnostics belong in the main report.

## Independent pre-freeze implementation review

The finalized core and configuration were read independently before any learning run. The ambiguity oracle enumerates all consistent missing-edge completions under independent mappings; the reader and mergers have no label/reference arguments. Four-query worlds remain contiguous, `swapped_B` rolls whole-world blocks, and predictions record donor IDs. Main and DeepSets training reset the same stage-2 data RNG, use the frozen shared network, and have the stated loss and step budgets. The primary bootstrap averages eligible queries within each world, then worlds within each fit, and equally weights the three fits. Its synthetic unequal-query-count test separates world macro from query micro.

An independent run of the complete test suite passed **19 tests** before freeze; these include untrained schema/gradient and theory checks and do not constitute performance evaluation. No blocking inconsistency was found. Known limitations remain the different SUM/MAXSET pooling representations, weak one-row numerical associativity probe, absence of semantic three-party/within-party-duplication experiments, small vocabulary and generous state budget, and confidence intervals conditional on three fitted models. These are disclosed limits, not capabilities supported by test passing.
