# Proposal 03 — Revocable Shared Latent Memory

**Short name:** RSM
**Status:** concept proposal; no method or results yet.

## Abstract

Long-term memory can be compressed, summarized, and merged across people or agents. A later request to delete one person's contribution is difficult if the system has lost the link between the source and its derived state. We propose **revocable shared latent memory**: an evaluation and architecture for removing a source-scoped contribution after derivation and merging, while preserving unrelated information. A deterministic benchmark would compare raw-store deletion, retrieval filtering, lineage-aware rollback, snapshot rollback, and latent-state recomputation. Success requires both low residual leakage about revoked content and high utility on queries supported only by retained sources. The proposal does not claim that memory provenance, poisoning, or rollback is new; it studies whether revocation remains possible after bounded latent compression and multi-source composition.

## Research question and hypothesis

**RQ:** Can a compact shared state support source-specific revocation after multiple contributors' observations have been compressed and used to derive further memories?

**H1:** Tracking source contributions through updates and merges will reduce leakage after revocation compared with tombstones or retrieval-time filters, at a lower utility cost than deleting or rebuilding the entire state.

**H2:** Revocation error will increase with lossy compression, overlapping evidence, and derivation depth unless the state preserves an explicit correction/recomputation path.

## Proposed experiment

Create controlled multi-party streams where A, B, and C contribute facts, corrections, preferences, and derived summaries. Merge them under a fixed byte budget using raw text, graph, and learned latent baselines. At randomized points, issue revocation for one source, then test direct extraction, paraphrase extraction, association-based inference, and tool behavior that depends on the revoked content. Also test unaffected queries supported by other sources, concurrent merge order, and repeated revocation.

The reference behavior is recomputation from only the non-revoked raw evidence. Report residual extraction rate, downstream action influence, utility on retained facts, deletion latency, storage overhead, and audit completeness. A strict end-to-end criterion should compare post-revocation outputs to the recompute oracle, not merely check that a record is absent from the retrieval index.

## Novelty boundary

[MEXTRA](https://arxiv.org/abs/2502.13172) demonstrates memory extraction risk; [MemoryGraft](https://arxiv.org/abs/2512.16962) studies persistent poisoning through retrieved experience. The [long-term memory security survey](https://arxiv.org/abs/2604.16548) already covers forgetting and rollback as governance requirements. [MemLineage](https://arxiv.org/abs/2605.14421) attaches cryptographic provenance and derivation lineage, while [ChronoMem](https://arxiv.org/abs/2607.27773) studies version snapshots and semantic rollback. [MemOps](https://arxiv.org/abs/2607.12893) evaluates memory lifecycle operations and [MemFuse](https://arxiv.org/abs/2608.18704) covers multi-source fusion.

The narrow proposed boundary is **source-scoped revocation after lossy shared-state fusion**, with residual leakage and retained utility both measured against a recomputation oracle. It is an open hypothesis, not an established gap. A direct comparison may show that lineage plus recomputation already solves it; that outcome would be useful and should end the latent-specific claim.

## Primary endpoint and stop criteria

Primary endpoints: (1) revoked-source extraction rate after the delete request; and (2) retained-source task accuracy. Report the full privacy-utility curve over byte budget, source count, and derivation depth. Require a pre-registered reduction in leakage over the best lineage-aware baseline while keeping retained-source accuracy within a narrow, predeclared margin. Stop if the mechanism cannot distinguish forgotten-source influence from retained-source evidence, if a white-box oracle is necessary at inference, or if an established lineage/rollback system provides the same result with less complexity.

## Main risks

Deleting latent information may be impossible without source logs; attribution can be uncertain when sources repeat the same fact; an extraction test can miss side-channel influence; and retaining provenance may undermine the memory budget. Start with deterministic state models and an explicit adversary, retain a raw-evidence audit oracle outside the tested memory system, and avoid claiming formal privacy from empirical non-extraction alone.
