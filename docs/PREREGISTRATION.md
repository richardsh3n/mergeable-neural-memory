# Bounded pilot preregistration: mergeable neural memory

Protocol date: **2026-10-09** (client-provided date). Status: **pre-run protocol**; the local SHA freeze, when created, is recorded separately in `results/freeze.json`. This is a local, exploratory pilot protocol. It has not been registered with an external registry, accepted by a venue, or validated by results.

The frozen source of numerical settings is `configs/pilot.json`. The pre-run freeze manifest must record the SHA-256 hashes of this document, that configuration, the executed source, tests, and dependency lock file. An actual UTC freeze timestamp must come from the clock at freeze time; it must not be inferred from this document's date. No training or outcome evaluation may begin before that manifest is saved.

## 1. Question and permitted conclusion

Can a learned symmetric operation combine two fixed-size neural states so that a frozen neural reader answers queries requiring facts held by both parties, including when some distractor facts appear in both parties?

This experiment concerns **small synthetic relational worlds**, not an LLM backbone, natural-language memory, human-like memory, autonomous agents, or a general memory architecture. Fixed state size establishes a capacity-matched comparison. It does not establish optimal compression, equal total training cost, or an inference-efficiency advantage.

The main operation is commutative by construction and has an empty-input identity. Associativity and idempotence are **not** guaranteed. They must not be described as proved properties of the learned operation. A successful primary comparison supports superiority over the specified MAXSET comparator on this pilot distribution, not superiority over every baseline or general neural-memory systems.

## 2. Frozen task and information boundaries

Each world has six entities and two directed functional relations. Each subject–relation target is sampled independently from the six entities. Relations are **not permutations or bijections**. Entity IDs are renamed by a fresh random permutation for every world. The entity alphabet is shared between training and testing; the held-out objects are newly sampled worlds and evidence splits, not previously unseen vocabulary.

All registered evidence has revision tag zero. Corrections, temporal precedence, conflict resolution, deletion, and continual updates are reserved for a follow-up. A reserved revision embedding does not constitute an evaluated revision capability.

For evaluation, each world supplies one shared pair of evidence sets and four distinct queries: two one-hop and two two-hop queries. A two-hop query asks for `r2(r1(subject))`, with `r2` the other relation. Its needed path edges, when present, belong exclusively to opposite parties. Critical edges are assigned by relation with a random party flip. Overlap is sampled on noncritical facts. Nonrequired distractors are retained with probability 0.85.

Each query path has a 0.20 deletion opportunity: with that probability, one path edge is removed from both parties. Shared path edges can make this affect more than one query. Consequently, **0.20 is not a guaranteed unknown-answer class fraction**. Actual known/unknown counts must be reported. The evaluator's deduplicated union determines the labels, including the unknown label when its path cannot be executed.

For every known two-hop evaluation query, an evaluator-only ambiguity oracle must establish that each private party's facts admit at least two different answers under the independent-functional-mapping model. A missing direct lookup alone is insufficient: a complete constant second relation can otherwise reveal the answer without the first edge. Worlds failing the ambiguity requirement are rejected by the generator, before any model prediction is inspected. Counts and generator failures must be disclosed.

The model encoder receives only local event tensors and padding masks. The query reader receives only the merged state and query. The merger receives only its two numerical states. Labels, gold intermediates, raw union facts, required-edge annotations, ambiguity results, source ownership, overlap labels, world IDs, and reference-answer tables are prohibited at inference. The evaluator may retain these solely for supervision and auditing. No raw event list accompanies the merged state.

## 3. State capacity and architecture

Every stored state has 12 slots × 24 coordinates, all float32: **288 floats = 1,152 payload bytes**. No per-world persistent metadata or auxiliary memory is allowed. If a method gains such metadata, its bytes must be counted and that comparison is an amendment, not the registered experiment. Queries and shared model weights are not per-world memory; parameter counts and checkpoint bytes must nevertheless be reported separately.

During two-party merging, two input states are simultaneously available. This requires 2,304 input-state payload bytes, plus one 1,152-byte output and temporary computation. The 1,152-byte bound is the retained output-state size, not peak runtime memory. Float precision and tensor dtype must be checked from actual tensors.

The common event encoder learns entity/relation embeddings, event features, and soft routing into slots. It uses sum pooling for the main operation, SUM, MEAN, and DeepSets. MAXSET instead uses coordinatewise maximum pooling of the **same learned event features and encoder weights**, then coordinatewise maximum of its two states. MAXSET therefore uses a different pooling rule; it is not simply maximum applied to the main method's stored sum states. All methods ingest identical local facts and retain the same number and precision of state coordinates.

The common reader performs two learned attention reads. Its second subject embedding uses its own predicted first-hop distribution; it receives no oracle intermediate at inference. Two reads and intermediate supervision are explicit task-specific inductive biases.

The main per-slot merger uses symmetric features `[a+b, abs(a-b), a*b]`, a 72→64→24 residual network with a hidden Tanh, and an input-magnitude gate that vanishes when either input is zero. It has 6,232 trainable parameters. This gives input commutativity and the empty-state identity. The DeepSets control is `rho(phi(a) + phi(b))`, with shared 24→64→24 `phi` and 24→64→24 `rho`, each using a hidden Tanh, for 6,320 trainable parameters. It is a trained permutation-invariant control, not a novelty claim about DeepSets; it has no guaranteed empty-input identity. Actual parameter counts must be verified in the run manifest.

## 4. Training, stopping, and comparator fairness

Training seeds are **11, 23, and 37**. CPU execution uses one thread and deterministic settings. There is no hyperparameter search or outcome-based checkpoint selection.

Stage 1 trains one shared encoder/reader per seed for 1,500 steps, batch size 64, AdamW learning rate 0.003 and weight decay 0.0001. The four modes cycle equally: deduplicated full-union sum encoding; split SUM; split MEAN; split MAXSET. The training generator samples one query per world, with two-hop probability 0.70, distractor overlap probability 0.30, and missing-path probability 0.20. This differs from the four-query shared-context evaluation design and must be disclosed.

After Stage 1, encoder/reader weights are frozen. The main merger and DeepSets comparator each receive 1,000 additional training steps, batch size 64, AdamW learning rate 0.002 and weight decay 0.0001. Both receive the same stage-2 evidence distribution, supervision types, and training budget. They may not use test worlds to tune architecture, loss weights, stopping, or thresholds.

The answer objective is final-answer cross-entropy plus **0.30 × first-hop cross-entropy** in both stages. For each learned merger, add **0.10 × relative state MSE** against the frozen encoder's deduplicated full-union sum state. Relative state MSE is mean squared error across the batch and state coordinates divided by the target state's mean squared magnitude, clamped below at `1e-6`. There is **no idempotence loss**. The teacher has access to deduplicated combined evidence during training; this privileged training signal must be disclosed. It is not available to the merger at inference.

The final scheduled checkpoint is used for every seed. NaN/Inf loss, tensor truncation, failed information-boundary checks, or a crash is a failed run. Preserve its logs. A numerical or implementation repair after freeze requires an explicit amendment and new hashes. A low-performing checkpoint is not a reason to extend training or choose an earlier checkpoint.

SUM, MEAN, and MAXSET have no separately trained merger. The main method consequently has additional parameters and training compared with these arithmetic baselines. The experiment is **capacity matched, not total-training-budget matched**. DeepSets controls for having an additional learned symmetric merger. Report all comparator outcomes even when they contradict the main hypothesis.

Full-union sum re-encoding and full-union max re-encoding are privileged references with access to the combined raw evidence. They are not state-only competitors or mathematically guaranteed performance upper bounds: reader imperfections can make another representation score better. MAXSET should match its corresponding max re-encoding up to floating-point tolerance on nonempty evidence, including overlap; that algebraic property is a diagnostic reference.

## 5. Test worlds and analysis units

For each training seed, generate 1,000 held-out worlds at each distractor overlap probability **0.00, 0.25, and 0.50**: 3,000 worlds and 12,000 query rows per trained fit. Evaluation RNG uses the frozen offset **100003**, the training seed, and the condition offset specified in the executed source. These are independent seeded streams from training. The three fits use different held-out world sets. Within a fit and condition, every method sees the exact same worlds, evidence, and queries.

Reproducibility from the specified seeds and generator must be checked. Independent seeds do not logically guarantee that a finite sampled world never repeats; do not claim an exhaustive disjointness proof without checking it. No test outcome may select the checkpoint or modify the protocol.

The primary analysis includes only **known two-hop queries at overlap 0.50** that meet the private-ambiguity check. For each world, average correctness over its eligible queries. Worlds with zero eligible queries are excluded from this primary statistic using labels and query type alone, before model outcomes. Report eligible world and query counts for every seed, and all-world counts separately.

## 6. One primary hypothesis and decision rule

**H1:** The learned symmetric merger has higher world-macro accuracy than MAXSET on the primary subset.

For each fit, calculate each eligible world's paired accuracy difference, learned minus MAXSET. Average these differences over eligible worlds, then take an equal-weight mean across the three fits. This is the primary effect. Raw machine-readable metrics use accuracy fractions; multiply by 100 when reporting percentage points. Query-micro accuracy is a secondary statistic.

Construct a paired world-cluster percentile bootstrap with **5,000 resamples**, RNG seed **20261008**. Resample eligible whole-world difference scores independently within each fit, preserving all within-world query dependence; calculate each fit's mean and the equal-weight mean across the three fits. Report the 2.5th and 97.5th percentiles.

The pilot supports H1 only if the 95% interval's lower bound is strictly above zero. Otherwise report H1 as unsupported. No other stratum, baseline, aggregation, or threshold can replace this primary comparison after seeing results. The interval is conditional on these three trained fits; it does not quantify generalization over arbitrary training seeds. Also report all three fit-specific effects and their range.

If another baseline equals or exceeds the main result, say so. A positive primary contrast against MAXSET does not establish that the learned merger is the best method. No secondary comparison is promoted to confirmatory status; no multiplicity-corrected omnibus superiority claim is made.

## 7. Prespecified secondary outcomes and diagnostics

Report one-hop, two-hop, known-answer and unknown-answer performance at all overlap levels; accuracy for SUM, MEAN, MAXSET, DeepSets, A-only, B-only, zero state, and full re-encoding references; query-micro accuracy; actual class fractions; and confidence calibration in 10 fixed-width bins. Calibration is descriptive and does not establish a calibrated abstention mechanism.

For trained states, report normalized state differences for input commutativity, `merge(a,a)` versus `a`, and the two three-input merge trees. The defect is `sqrt(mean((output1-output2)^2) / max(mean(A^2), 1e-6))` within each evaluation batch, then averaged across batches. The same formula and floor apply to every method, using that method's input representation. State equality and answer equality are separate outcomes. Algebraic defects measured using states from different worlds are valid numerical probes but **not** evidence of correct three-party semantic integration. Meaningful three-party answer tests need one common world and a specified three-party evidence partition; if absent, list them as unperformed follow-up work.

Zero and private-party states are required controls. The `swapped_B` control replaces B with the previous world's B state within each 25-world evaluation batch, by a circular roll of four query rows. Keep the original query and original labels, and save the donor world ID in evaluator output. This preserves the four-query grouping and uses a distinct donor world ID. It is a destructive control for dependence on correctly matched evidence, not an alternative model.

Within-party fact duplication robustness and same-world three-party merge-tree answer accuracy are **unperformed follow-up work** in this first pilot. The idempotence state probe alone does not establish either. The numerical associativity probe uses a third reachable state obtained by a one-row circular roll of A in the evaluation batch; repeated query rows mean some third states coincide with A. It is not a semantic three-party test. Unit tests of untrained tensors do not constitute trained-model evidence for these capabilities.

Report actual timing scope, parameter counts, checkpoint size, retained-state bytes, and execution environment. Any measured merge/read timing that excludes encoding, data generation, or training is descriptive component timing only. This pilot makes no end-to-end speed, energy, or storage-efficiency claim.

## 8. Reporting, freeze, and amendments

Preserve the frozen manifest, complete configuration, source, dependencies, tests, training logs, final checkpoints, and per-world/per-query predictions sufficient to reproduce the paired analysis. Write results for every seed and comparator, including failures and negative findings. Aggregate tables alone are insufficient for the registered bootstrap audit.

The initial report must distinguish planned, implemented, executed, and supported items. Corrections, larger entity vocabularies, tight capacity sweeps, independently trained incompatible encoders, continual learning, natural-language encoders, and LLM-scale experiments remain follow-ups unless separately frozen and run.

Any post-freeze change to data, architecture, training, test worlds, metrics, or stopping must be recorded with its reason, timing relative to result inspection, old and new hashes, and whether all affected runs were restarted. Preserve the original frozen protocol. Post-result analyses are exploratory. No GitHub publication or external submission is authorized by this local protocol.
