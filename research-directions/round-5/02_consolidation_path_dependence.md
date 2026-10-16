# Same Evidence, Different Memory: Controlling Consolidation Path Dependence

**Research sketch — 16 October 2026.** Proposal only; no new experiment or external registration. Common rules: [README.md](README.md).

## Question and proposed contrast

Should equivalent records processed in different batches produce materially different remembered beliefs? Test whether consolidation is stable under changes to batching and processing order while preserving the events' actual timestamps and causal order. A chronology-dependent change can be legitimate; a processing-order artifact is not automatically so.

[RoutePrism](https://arxiv.org/abs/2609.34160) directly diagnoses construction-order effects. [Useful Memories Become Faulty](https://arxiv.org/abs/2605.12978) directly studies consolidation failures and update schedules. Finding order sensitivity is therefore already covered. The proposed extension is a prospective, resource-matched intervention that minimizes avoidable path dependence while retaining valid temporal updates.

## Hypothesis and minimal experiment

Hypothesis: a canonical event representation or replay-checked consolidation reduces answer variance across admissible processing schedules without merely keeping more raw evidence. Requiring full order invariance would be wrong for conflicting dated facts, so admissible schedules are defined before evaluation.

Generate exact event ledgers with corrections, independent records and partial-order constraints. Replay each ledger under fixed batch partitions and topological processing orders. Hold record contents, event dates, reader, total evidence and fitting budget constant. Compare streaming summaries, batch summaries, event-sourced symbolic state, canonical ordering, and a consistency-trained consolidator. Full-history replay is a privileged reference if it exceeds the memory budget. Separate content lost during initial compression from later destructive rewriting.

Primary endpoint: ground-truth query error averaged over preregistered schedules; report between-schedule disagreement, worst-schedule accuracy, valid-update retention, unsupported claims, consolidation calls and retained bytes. A system that always emits the same wrong answer is invariant but unsuccessful. Use paired ledgers and publish all schedules rather than selecting favorable orders.

## Stop rule and value

Stop the learned-method claim if canonical sorting or an ordinary event ledger already solves the problem, if variance falls only by ignoring updates, or if the candidate gains uncounted history access. A useful diagnostic can still identify when a memory pipeline's outputs depend on accidental processing choices. This concerns memory construction, unlike the earlier neural-state merger's algebraic tests or online eviction-value proposal.
