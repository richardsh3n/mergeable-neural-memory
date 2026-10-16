# Round 5: nearest-work boundary and separation from earlier proposals

**Targeted primary-source scan, 16 October 2026.** This is an initial literature map, not a systematic novelty certificate, full-text audit, or reproduction. Titles below follow the primary entries observed today; some differ from older search records. Exact claims belong to the individual sketches.

| Topic | Existing primary work | What the proposed study must add |
|---|---|---|
| 1: concurrent consolidation | [MemTxn](https://arxiv.org/abs/2607.27834); [BEGIN AI TRANSACTION](https://arxiv.org/abs/2608.05412) | A controlled slow lossy-writer race and invariant/cost comparison beyond standard concurrency control. |
| 2: path dependence | [RoutePrism](https://arxiv.org/abs/2609.34160); [Useful Memories Become Faulty](https://arxiv.org/abs/2605.12978) | Prospective mitigation under admissible order changes, rather than rediscovering order effects. |
| 3: exploration | [Memory in MLE agents](https://aclanthology.org/2026.findings-acl.525/); [Controllable Memory Usage](https://aclanthology.org/2026.acl-long.670/) | Randomized timing of verified precedent exposure under a fixed search budget. |
| 4: scope | [PersistBench](https://arxiv.org/abs/2602.01146); [TANGLE](https://arxiv.org/abs/2608.13921) | Scope inference versus explicit namespace controls, with genuine ambiguity and clarification cost. |
| 5: private exceptions | [Taming Knowledge Conflicts](https://arxiv.org/abs/2503.10996); [Beyond Black-Box Interventions](https://arxiv.org/abs/2510.12460) | Separate persistent write loss, retrieval loss and answer integration under controlled prior conflict. |
| 6: resumable thought | [Coconut](https://arxiv.org/abs/2412.06769v4); [Recurrent-depth reasoning](https://arxiv.org/abs/2502.05171) | A complete declared inference checkpoint and measured byte/recompute frontier, beyond latent reasoning itself. |
| 7: stopping value | [Learning When to Stop](https://arxiv.org/abs/2511.21581); [Adaptive Depth](https://arxiv.org/abs/2607.20519) | Calibrate marginal improvement and compare it with strong confidence readouts on frozen trajectories. |
| 8: concept refinement | [MindMemOS](https://arxiv.org/abs/2608.12428); [AgentCore schema documentation](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/long-term-memory-metadata.html) | Semantic recoverability and justified unknowns after definition changes, beyond adding metadata fields. |
| 9: late feedback | [FASE](https://arxiv.org/abs/2609.32689); [Skill-Pro](https://arxiv.org/abs/2602.01869) | Feedback attribution to executed procedure versions under subsequent memory revision. |
| 10: poisoning persistence | [MemoryGraft](https://arxiv.org/abs/2512.16962); [MINJA](https://arxiv.org/abs/2503.03704); [Realistic poisoning/defense study](https://arxiv.org/abs/2601.05504) | Longitudinal recovery and recurrence with separate exposure/consolidation interventions, not first discovery of durable poisoning. |

## Distinction from earlier sketches

Concurrency and processing order are different interventions: Topic 1 allows overlapping writes and checks lost updates; Topic 2 is single-writer and changes only admissible construction schedules. Exploration timing uses correct precedents and exact feedback, unlike the earlier endogenous-evidence loop. Scope routing keeps facts true and stored, unlike contributor deletion. Private-exception integration does not edit a fact after writing.

Resumption keeps the same task and model but serializes unfinished computation; host migration changes the reader/writer, and deferred intention memory concerns future workflow actions. Halting asks whether to continue computing, not whether to restore a damaged fact store. Ontology refinement changes category semantics, whereas the earlier skill-contract proposal changes tool interfaces. Delayed feedback concerns learning attribution, not reminders. Defensive poisoning recovery concerns integrity, whereas consent revocation concerns a legitimate contributor's withdrawal.

These distinctions define experimental scope. They do not establish that every nearest predecessor lacks the proposed test; before registration, inspect full methods, appendices, code and citation chains. Negative results or conventional baselines winning would be legitimate outcomes.

## Search scope

Queries covered semantic transactions, consolidation order, memory and discovery diversity, project leakage, contextual/parametric conflicts, latent reasoning and halting, schema evolution, delayed feedback, and persistent memory poisoning. Primary arXiv and ACL entries and official AWS documentation were read at abstract or selected-section depth. No unpublished submissions or exhaustive database exports were searched. Source-entry details and reading depth are recorded in [SOURCES.json](SOURCES.json).
