# The Slow Writer Problem: Concurrent Consolidation without Lost Meaning

**Research sketch — 16 October 2026.** Proposal only; no new experiment or external registration. Common evaluation rules are in [README.md](README.md).

## Question and proposed contrast

When two agents read the same memory version, spend time summarizing, and then write back, can a consolidation erase an update that arrived while it was thinking? This is a semantic read–modify–write problem with an ordinary concurrency-control core. It differs from source revocation: nobody asks to delete information, and every input can be legitimate.

[MemTxn](https://arxiv.org/abs/2607.27834) already studies validated writes and recovery. [BEGIN AI TRANSACTION](https://arxiv.org/abs/2608.05412) already studies semantic isolation in durable workflows. Transactions, snapshot validation and optimistic concurrency are not new. The proposed study isolates a slow, lossy consolidation running concurrently with ordinary writes, and asks which semantic invariants survive retries and rebasing.

## Hypothesis and minimal experiment

Hypothesis: version validation plus evidence-scoped recomputation prevents more lost-fact and resurrected-stale-fact errors than blind summary replacement, with a measurable retry cost. A standard serialized writer may remain best when contention is low.

Build a deterministic memory service and scheduler. Generate insert, correction and consolidation operations with controlled overlaps and inference delays. An evaluator-only serial reference gives permissible outcomes; operations on independent entities may commute, while conflicting corrections retain explicit ordering rules. Compare blind replacement, a global lock, compare-and-swap with retry, immutable-event replay, and a dependency-aware rebase candidate. Expose the same evidence and version metadata to equivalent arms. Never call arbitrary LLM summaries serializable without an executable invariant.

Primary endpoint: final-state semantic invariant violations per scheduled workload. Report lost updates, stale resurrection, reader-visible inconsistent states, retries, completion rate, p95 latency, bytes and model calls. Pair by schedule and world. Separate deterministic structured patches from model-extracted patches so storage correctness is not confused with extraction quality.

## Stop rule and value

Stop a new-method claim if ordinary compare-and-swap or locking gives the same correctness/cost frontier, or if rebase requires hidden original evidence. The useful outcome may be a simple engineering contract and reproducible race-condition benchmark. Begin with structured synthetic states before natural-language summaries; no real multi-user memory is modified.
