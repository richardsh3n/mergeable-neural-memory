# Memory Beyond Its Host: Update-Compatible Migration of Persistent Neural State

**Working proposal, 15 October 2026.** No study has been run or externally registered. Proposed titles describe questions, not established contributions.

## Abstract

A long-lived assistant should survive changes to the model hosting it. Reading an exported memory once is insufficient: after migration, the target must accept new observations, correct old facts, and preserve useful behavior through further upgrades. This proposal studies update-compatible migration of bounded numerical memory. A migration map must approximately preserve both query behavior and the result of future writes. We compare read-only adapters, migration maps trained on write transitions, canonical symbolic stores, and full-history reconstruction. The central endpoint is correctness on a frozen mixed old/new query set after migration and continued updates. This is a narrower question than generic cross-model memory transfer, which already has direct precedents. A successful study would establish a useful operational contract for writable memory; a failed comparison against a compact symbolic representation would argue against a learned-state solution for the tested tasks.

## Question and formal contract

Let host A use writer U_A and reader R_A, and host B use U_B and R_B. Let F_AB map an A-state into a B-state. Require two properties on held-out states, observations x, and queries q:

1. Read preservation: R_B(F_AB(s), q) approximately matches R_A(s, q) when A is correct.
2. Update compatibility: R_B(F_AB(U_A(s, x)), q) approximately matches R_B(U_B(F_AB(s), x), q).

The second property asks whether migration before an observation and migration after the same observation produce equivalent usable memory. Compare predictions, not coordinate distances: latent coordinates can be arbitrary. Also compare both paths to task truth, since two wrong readers can agree. For a sequence A → B → C, test old facts, B-written facts, and C-written facts separately. Cyclic state reconstruction is a diagnostic; it can be satisfied by degenerate maps and cannot substitute for task accuracy.

## Motivation and nearest prior work

The current project's frozen-state merging experiments do not test incompatible encoders or model upgrades. This proposal addresses that limit without claiming that portability is new. Goyal and Ray study model-upgrade effects on raw history, retrieval, notes, and fixed-schema graphs. Li et al.'s latest arXiv version studies frozen learned-memory reuse through target-side readers. Memp studies writable procedural memory and transfer between stronger and weaker models. MEMORYLLM establishes self-updatable latent memory. These predecessors motivate a specific distinction: repeated migration of a **bounded episodic state whose post-migration writes must remain usable**, evaluated through the update contract above. Whether that exact distinction remains novel requires a broader full-text and code audit.

## Hypotheses and candidate mechanism

H1: training migration on both reads and held-out write transitions reduces post-migration old/new query error relative to a read-only adapter under equal fitting budgets.

H2: one-step read preservation will not reliably predict performance after many target-side updates or a second migration.

H3: a canonical symbolic representation will remain a strong or superior baseline on simple fact tasks; a learned representation is justified only if it offers a useful cost/quality frontier on richer tasks.

A candidate mechanism is a small state adapter trained on paired states and update trajectories from development worlds, with read-loss and update-compatibility loss. The source and target backbones remain frozen during adapter fitting. No user-specific test histories, hidden answers, or retained source state may be accessed at target inference. Global adapter parameters, per-instance state, version tags, serialization metadata, fitting data, and fitting compute must all be disclosed separately.

## Controlled study

Begin with independently trained small encoder/writer/reader systems using different initialization, width, and slot layouts. Then, only after a feasibility gate, attach analogous memory interfaces to two small pretrained model families. Toy encoder migration does not establish LLM portability.

Generate seeded event streams with new facts, explicit corrections, temporal ordering, and unknown answers. Hold out entire entities, world mechanisms, and update patterns where feasible. Use three schedules: migrate then read; migrate then write; migrate, write, migrate again. Preserve a never-migrated reference for each host. Freeze query pools before tuning. Exact labels come from an evaluator-only event state; the model never sees that state.

Baselines: no migration/empty memory; identity or simple linear map where dimensions permit; read-only trained adapter; write-compatible adapter; text summary; fixed-schema symbolic store; and privileged full-history re-encoding. Re-encoding has extra source access and is a recovery reference, not a fair state-only competitor. Match adaptation examples, optimizer steps, state bytes, and reader access. Report parameter and compute differences rather than claiming equality where interfaces differ.

Primary endpoint: world-macro accuracy on a preregistered equally weighted old/new query set after migration and a fixed number of new writes. Report each stratum, unknown-answer calibration, update-contract disagreement, repeated-migration drift, migration latency, bytes and adaptation cost. Use paired world bootstrap intervals and show fit-level variation. Fix the number of writes, schedules, state budgets, minimum benefit, clean-host competence requirement, and sample size using an excluded pilot; do not select the best schedule after seeing final results.

## Stop criteria and execution

Stop the architecture claim if clean hosts are already unreliable, a read-only adapter matches the candidate after continued writes, or gains rely on retaining raw history or uncounted metadata. If canonical symbolic memory dominates at matched resources, report that result and constrain the claim to representation-specific behavior. Near-perfect agreement with low ground-truth accuracy fails the contract test.

Deliver in stages: exact-state simulator and protocol; independent-encoder diagnostic; preregistered held-out comparison; two-family LLM replication only if warranted. Practical applications include replacing local models, upgrading a personal assistant, and moving an episodic state between capable and inexpensive hosts. The protocol does not promise lossless transfer of arbitrary experiences.

## Primary references

- Goyal and Ray. [Does Your Agent's Memory Survive a Model Upgrade? A Controlled Study of Memory Portability](https://arxiv.org/abs/2609.05339v1), 2026.
- Li et al. [Frozen Memory Is Not Enough: Rethinking External Memory as Extraction](https://arxiv.org/abs/2608.17050v3), 2026. This is the verified v3 title; earlier search records use a different title.
- Fang et al. [Memp: Exploring Agent Procedural Memory](https://arxiv.org/abs/2508.06433v4), 2025–2026.
- Wang et al. [MEMORYLLM: Towards Self-Updatable Large Language Models](https://arxiv.org/abs/2402.04624v2), 2024.
