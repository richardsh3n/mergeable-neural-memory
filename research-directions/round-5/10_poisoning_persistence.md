# After the Bad Memory: Persistence and Recovery under Long Benign Streams

**Research sketch — 16 October 2026.** Defensive study proposal only; no attack executed and no external account targeted. Common rules: [README.md](README.md).

## Question and proposed contrast

After a small amount of poisoned experience enters a memory store, how long can it influence behavior through ordinary retrieval, consolidation and later benign updates, and which defense removes that influence without rejecting useful history? The relevant endpoint is persistence and recovery across time, not only initial insertion success.

[MemoryGraft](https://arxiv.org/abs/2512.16962) already studies persistent poisoned experience retrieval. [MINJA](https://arxiv.org/abs/2503.03704) already studies query-only memory injection. [Memory Poisoning Attack and Defense](https://arxiv.org/abs/2601.05504) already studies legitimate pre-existing memories and trust calibration. Neither persistent poisoning nor realistic benign backgrounds is new. The proposed study is a controlled longitudinal defense comparison with exposure dose, consolidation and recovery as separately randomized factors.

## Hypothesis and minimal experiment

Hypothesis: entry-level rejection alone may not remove influence already propagated into summaries; lineage-aware invalidation plus re-derivation can improve recovery, but may cost utility or require retained source evidence. The earlier source-revocation proposal concerns legitimate contributor withdrawal; this one concerns integrity failures and unsafe persistence.

Use a simulated agent and harmless mock actions with pre-existing public benchmark-style poisoned records and matched benign controls. Fix the small poison set before evaluation; no live-target payload development is part of the study. Randomize where it enters a benign stream, whether consolidation occurs, and the time of detection. Compare admission checks, read filters, affected-summary recomputation, whole-memory reset and an oracle clean-history rebuild. Charge all evidence retention and recovery costs. Ground-truth poison labels are available only to oracle arms or at the specified detection event.

Primary endpoint: cumulative incorrect mock-action rate over a fixed post-exposure horizon. Report time to recovery, recurrence after consolidation, retained clean-task utility, false rejection, intervention burden and storage. Show full survival/dose curves rather than one handpicked horizon. Separate known-record replay tests from held-out defensive generalization.

## Stop rule and value

Stop a general defense claim if it fails on held-out sources, requires impossible ground-truth knowledge, or succeeds only by disabling all memory. A result from these sandbox channels cannot establish security against adaptive attackers or production systems. The deliverable is an auditable longitudinal evaluation of memory-integrity defenses.
