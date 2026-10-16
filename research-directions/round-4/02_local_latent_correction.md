# Correct One Fact, Preserve the Rest: Local Editing of Episodic Latent State

**Research sketch — 16 October 2026.** Proposal only; no experiment run, preregistration, or originality claim.

## Question and useful outcome

Can a user correct one remembered fact in a compact numerical memory while preserving unrelated facts and updating only the consequences that genuinely depend on the correction? A usable latent-memory assistant needs inspectable correction behavior, not merely an opaque state that responds differently after feedback.

The target is instance-specific episodic state, with the base model frozen. It differs from source revocation, which removes a contributor, and host migration, which changes the model. Here the information is deliberately replaced and its legitimate downstream consequences should change.

## Nearest work and proposed contrast

[Larimar](https://proceedings.mlr.press/v235/das24a.html) already supports episodic-memory editing and sequential updates. [MQuAKE](https://arxiv.org/abs/2305.14795v3) already evaluates whether edits propagate to related multi-hop beliefs. Neither memory editing nor locality is new. The proposed narrow contrast is a fixed-byte, state-only correction contract with positive dependency propagation, unrelated-fact preservation, and repeated edit/undo tests when the raw episode is unavailable.

## Hypothesis and small first study

Hypothesis: an editor trained with explicit affected/unaffected query supervision can improve the edit-success/locality frontier relative to appending corrections or unconstrained state optimization. It must also compete with ordinary symbolic records; numerical-state editing is not justified by novelty of representation alone.

Use small worlds with an executable fact ledger and evaluator-only dependency graph. Insert facts, issue a natural-language correction identifying entity, relation, scope, and time, and then test direct, dependent, unrelated, and deliberately ambiguous queries. Include legitimate contextual exceptions so a local correction is not mistaken for a global replacement. Run repeated corrections and reversions. The editor sees the state and correction, not the oracle graph or original episode at inference.

Compare native writer updates, append-only correction notes, query-time overrides, direct state optimization, a learned editor, and a compact symbolic patch store. Full-history reconstruction is a privileged recovery reference. Match access to correction labels, retained metadata, bytes and fitting examples, and disclose optimizer/parameter costs. An undo mechanism requiring a saved delta must count those bytes; lossless reversal cannot be assumed after lossy replacement.

Primary outcome: the edit-success versus collateral-error frontier on a preregistered mixed query set. Report dependent-fact accuracy separately from unrelated-answer retention; preserving every old answer would incorrectly penalize valid propagation. Also report ambiguity abstention, repeated-edit drift, latency and storage. Pair by world and hold out correction types, not only paraphrases.

## Stop rule and deliverable

Stop if edits work only when the target answer is placed in the current prompt, collateral harm rises substantially, or the symbolic patch store is better at comparable resources. The first deliverable is a reproducible edit/locality benchmark and a minimal state editor. A toy-state result would not establish reliable editing of general LLM memory or a new biological memory principle.
