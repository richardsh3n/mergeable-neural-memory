# Not Found Is Not False: Coverage-Aware Negative Memory for Search Agents

**Research sketch — 16 October 2026.** Proposal only; no experiment run, preregistration, or originality claim.

## Question and useful outcome

How should an agent remember an unsuccessful search without converting incomplete retrieval into a false claim that the answer does not exist? A useful memory might record that a particular collection, snapshot, query and access scope was searched, rather than store the universal statement “no such document exists.” This could avoid both repeated pointless searches and persistent false negatives in research or code-search assistants.

The focus is the logical validity and reuse scope of negative observations. Evidence streams are supplied by the environment; this is not the earlier active evidence-acquisition study. It also does not estimate independence between multiple witnesses or model policy-induced confirmation loops.

## Nearest work and proposed contrast

[MERIT](https://arxiv.org/abs/2608.05906v2) already maintains successful corrections and unsuccessful directions. [TANGLE](https://arxiv.org/abs/2608.13921v1) already evaluates genuine uncertainty and conflict-aware action. Negative experience and justified uncertainty are therefore not new themes. The proposed distinction is a scoped, snapshot-bound account of search coverage that separates known absence inside a finite examined domain from an unresolved top-k retrieval miss.

## Hypothesis and small first study

Hypothesis: coverage-aware negative memory reduces redundant searches without increasing false absence claims, compared with naive “not found” notes. Its value should disappear when queries or collections change so much that previous coverage no longer applies.

Use a synthetic finite corpus with known contents and version history. Simulate exhaustive enumeration, top-k retrieval, pagination, stale indexes, changed query predicates, newly added documents, and different visible collection subsets. Store negative observations with a query predicate, examined domain, snapshot identifier, and coverage status. Reuse an absence conclusion only when its scope is logically supported; unknown coverage remains unknown. A simulator can certify complete enumeration, while an ordinary web search cannot certify global nonexistence.

Compare no memory, positive-only memory, naive negative notes, time-decayed negative notes, a structured coverage ledger, and a candidate coverage-conditioned retrieval policy. Give all methods the same search traces and snapshot metadata. Include a full-corpus oracle as a diagnostic reference. Do not let the candidate inspect hidden corpus contents or receive coverage labels unavailable to the baselines.

Primary endpoint: correctly resolved tasks per search cost subject to a preregistered maximum false-absence rate. Report false negatives, repeated equivalent searches, abstention/re-verification, retrieval recall, reuse after corpus updates, and state bytes. Separate true finite-domain absence from unresolved retrieval misses. Hold out corpus seeds, predicate structures and update schedules; pair analyses by corpus snapshot and preserve all failed searches.

## Stop rule and deliverable

Stop if the policy only saves calls by issuing more false absence claims, if benefit disappears against the structured ledger, or if the result assumes an unrealistically complete search API. The first deliverable is an auditable negative-observation schema and controlled benchmark. A useful result might favor simple structured memory rather than a neural method. It would not establish truth or nonexistence across the open web.
