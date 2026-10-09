# Beyond Recall: Three Testable Frontiers for Persistent LLM Memory

**Working research agenda — 10 October 2026**
**Status:** proposal draft; no study in this document has been run or externally registered.

## Abstract

Persistent memory for language-model agents is usually assessed by whether the system can retrieve a past fact. That is necessary, but it does not tell us whether a memory can support counterfactual reasoning, decide what should be forgotten under a fixed budget, or honor a person's request to revoke information after it has been transformed and shared. This agenda proposes three connected but independently testable directions. First, **counterfactually sufficient memory** asks whether a compact, mergeable state can preserve the causal structure needed to answer intervention questions, rather than storing only evidence useful for factual recall. Second, **decision-value forgetting** treats eviction as a prospective resource-allocation problem: retain the memories that reduce expected future decision regret per byte, while measuring stale-memory harm and distribution shift. Third, **revocable shared latent memory** asks whether a source's contribution can be removed after multi-source fusion and compression, with both a privacy test and a utility-preservation test. Each proposal names nearby work, avoids first-ever claims, and defines a falsifiable evaluation. Together they frame memory as a maintained, governable state that supports future computation—not just a searchable transcript.

## 1. Motivation

An agent can retrieve a sentence accurately and still fail at memory. It may not know why an earlier choice worked, may keep a preference after the user changes it, or may continue to expose a fact after the person who supplied it asks for deletion. These failures become more serious when memory is compressed or shared, because the system may no longer have a simple record that can be edited in place.

Recent work makes clear that each of these problems already has active research. ActMem builds causal and semantic graphs for memory-dependent reasoning, while Causal Memory Intervention selects memories based on their measured effect on an answer. Memora and MemOps move evaluation toward stale-memory and operation-level failures. PersistBench studies cross-domain leakage and memory-induced sycophancy. MemLineage attaches provenance and derivation lineage to memories, and ChronoMem studies semantic rollback. MemFuse evaluates evidence fusion across fragmented sources, while LiveMem develops persistent state across context turnover. The opportunity is therefore not to announce “causal memory,” “forgetting,” “security,” or “state” as new categories. It is to isolate the missing constraint that these systems do not jointly settle: **what future behavior must a bounded internal state preserve, and how can that state change safely?**

## 2. Three proposals

### 2.1 Counterfactually sufficient memory state

**Question.** Under a strict storage budget, what representation of experience is sufficient for an agent to answer both factual queries and interventions such as “what would have happened if we had chosen the other supplier?”

**Hypothesis.** A writer trained on a distribution of future intervention queries will preserve more decision-relevant causal structure than one trained only on local factual recall, at the same bytes, compute, and reader. The expected benefit should grow when evidence is split across sources and shrink when the learned state cannot preserve the relevant causal variables.

The study would use executable structural causal models as an oracle and render selected models as multi-session narratives. Each example would separate observations, actions, outcomes, and latent confounders. Training and test splits would hold out causal mechanisms, not merely sentences. Evaluation would include factual recall, intervention accuracy, counterfactual consistency, calibration, and source-grounding. Baselines would include full-history reasoning, retrieval, text summaries, a causal graph, and fixed-capacity learned states. A full-evidence oracle would expose whether failures come from compression or from the reader. Storage would be measured in bytes, and all methods would share the same underlying language model where applicable.

This proposal is distinct from claiming that graphs or counterfactual prompts are new. ActMem already brings causal reasoning into memory, Causal Memory Intervention tests the causal usefulness of retrieved entries, and causal-reasoning benchmarks test broader model abilities. The proposed contribution would be a **resource-matched test of causal sufficiency under state compression and evidence partitioning**. The proposal fails if its advantage disappears against a well-engineered causal-graph baseline, if factual accuracy alone explains the gain, or if the model cannot demonstrate calibrated answers when the causal evidence is absent.

### 2.2 Decision-value forgetting

**Question.** Under a fixed memory budget, which past items should the agent retain when future tasks and user needs can change?

**Hypothesis.** Evicting memory according to its estimated marginal reduction in future decision regret will outperform time decay, recency, frequency, and static salience at equal storage and inference budgets—especially under concept drift and conflicting updates.

The writer would estimate an item's value from held-out or simulated future task families, not from the current query alone. The policy must operate online: it cannot inspect future test questions. A sequential benchmark would vary task recurrence, change points, privacy expiration, and updates. Each memory event would carry a write time, validity interval, source, and cost. Outcomes would include task reward or decision regret, stale-memory use, valid-fact retention, privacy-expired recall, and compute/storage cost. Baselines would include LRU, recency decay, frequency, similarity-based pruning, salience scoring, Memora-style forgetting-aware evaluation, and an oracle eviction policy that sets an upper bound.

The novelty boundary is important. Memora already penalizes use of invalidated memories, PersistBench studies when long-term memories should be forgotten for safety, ForgetBench studies retention under sequential model edits, and FSFM presents a broad selective-forgetting framework. A new paper cannot stop at a new decay curve or another benchmark. It must show that prospective **decision value per byte** gives a robust Pareto improvement over resource-matched retention policies, and it must report where the estimator fails under task-distribution shift. The work should not equate deletion with low retrieval probability; policy-driven erasure and passive eviction need separate measures.

### 2.3 Revocable shared latent memory

**Question.** Can a contributor revoke an observation after it has been compressed into a shared state and used to derive other memories, while preserving unrelated contributors' knowledge?

**Hypothesis.** A memory architecture that tracks source contribution through writes, derivations, and merges can remove the target contribution more completely than tombstones or retrieval filters, while keeping more unaffected utility than deleting the entire merged state.

The benchmark would create multi-party evidence streams, merge them through text, graph, and latent-state systems, then issue deletion or consent-revocation requests at different points in the lifecycle. The privacy criterion would test direct extraction, paraphrase extraction, and behavior that depends on the revoked source. The utility criterion would test answers supported only by non-revoked sources. A recompute-from-retained-raw-evidence oracle would define the desired post-deletion behavior. Stressors would include lossy compression, overlapping facts, derived summaries, concurrent updates, and merge-order changes. Systems would report deletion latency, residual leakage, retained utility, storage overhead, and whether an audit can identify what was removed.

This direction must distinguish itself from active work. The long-term memory security survey already frames forgetting and rollback as lifecycle governance; MemLineage tracks cryptographic provenance and derivation ancestry; ChronoMem studies semantic memory rollback; and MemOps evaluates explicit lifecycle operations. The proposed boundary is narrower: **source-scoped revocation after multi-source compression or latent merging**, measured by both residual leakage and unaffected utility. If ordinary provenance DAGs can reconstruct the same guarantees with comparable cost, the latent-state angle is not justified. The work should begin with a formal threat model and deterministic synthetic states, then move to LLM agents only if exact deletion behavior is demonstrated.

## 3. Shared experimental discipline

All three projects should separate the memory writer, memory state, retrieval/reader, and final language model. Results should identify which component failed. Comparisons should match state bytes, inference budget, model backbone, and access to raw evidence. Test streams must be frozen before tuning, with source-level seeds and complete evidence archives. A positive result should be replicated across fresh model initializations and at least two task families. A failed feasibility gate should be reported as a stop signal, not converted into a success claim by changing the endpoint.

The first work package should stay synthetic and deterministic. This keeps causal truth, update history, source ownership, and deletion targets auditable. Only after a mechanism clears a stated gate should the project use natural-language conversations or a pretrained LLM. This staged approach is consistent with the current v0.2 diagnostic: it found a sizeable difference between two training objectives but failed the registered absolute-accuracy and fit-consistency gate. A mismatch between the written per-step RNG reseeding rule and the implemented continuous per-fit stream is disclosed in the result archive, further limiting confirmatory interpretation. That result motivates better diagnostics; it does not establish any of the three proposals.

## 4. Priority and sequence

The strongest immediate fit is **counterfactually sufficient memory state**, because it extends the current thesis from “store a persistent latent state” to “preserve the causal variables needed for future decisions.” The most immediately useful product-facing direction is **decision-value forgetting**, because memory budgets, stale preferences, and privacy expiry occur in practical assistants. **Revocable shared latent memory** has the highest governance value and a clear systems challenge, but it requires a precise adversary model and stronger deletion tests before claiming an advantage over lineage and rollback systems.

These are candidate research programs, not three simultaneous implementation commitments. The proposed first next study is a low-cost causal-state benchmark and method comparison; the other tracks should remain independent until that first result demonstrates a reliable state representation.

## 5. Claims boundary

This document is a proposal, not a completed paper. No algorithm, benchmark, or result is claimed as original here. The literature scan is targeted and current to 10 October 2026; it does not certify novelty. Before any submission, each proposal needs an exhaustive search, precise related-work table, power-aware study design, artifact license review, and a fresh preregistration. The v0.1 negative result and v0.2 feasibility failure must remain visible alongside future positive results.

## References

- Zhang et al. [ActMem: Bridging the Gap Between Memory Retrieval and Reasoning in LLM Agents](https://arxiv.org/abs/2603.00026), 2026.
- Srivastava. [Causal Intervention-Based Memory Selection for Long-Horizon LLM Agents](https://arxiv.org/abs/2605.17641), 2026.
- Lee et al. [Benchmarking LLM Causal Reasoning with Scientifically Validated Relationships](https://arxiv.org/abs/2510.07231), 2025.
- Uddin et al. [From Recall to Forgetting: Benchmarking Long-Term Memory for Personalized Agents](https://arxiv.org/abs/2604.20006), 2026.
- Pulipaka et al. [PersistBench: When Should Long-Term Memories Be Forgotten by LLMs?](https://arxiv.org/abs/2602.01146), 2026.
- Gu et al. [ForgetBench: Benchmarking Forgetting Dynamics of Long-Term Parametric Memory in Language Models](https://arxiv.org/abs/2607.26455), 2026.
- Hao et al. [MemOps: Benchmarking Lifecycle Memory Operations in Long-Horizon Conversations](https://arxiv.org/abs/2607.12893), 2026.
- Lin et al. [A Survey on Long-Term Memory Security in LLM Agents](https://arxiv.org/abs/2604.16548), 2026.
- Ouyang and Hou. [MemLineage: Lineage-Guided Enforcement for LLM Agent Memory](https://arxiv.org/abs/2605.14421), 2026.
- Su et al. [ChronoMem: Version Control and Semantic Rollback for Large Language Model Agent Memory](https://arxiv.org/abs/2607.27773), 2026.
- Wang et al. [Unveiling Privacy Risks in LLM Agent Memory](https://arxiv.org/abs/2502.13172), 2025.
- Srivastava and He. [MemoryGraft: Persistent Compromise of LLM Agents via Poisoned Experience Retrieval](https://arxiv.org/abs/2512.16962), 2025.
- Li et al. [MemFuse: Multi-Source Memory Fusion from Fragmented Observations](https://arxiv.org/abs/2608.18704), 2026.
- Liu et al. [LiveMem: Maintaining Memory State Continuity in Long-Running LLM Inference](https://arxiv.org/abs/2608.02515), 2026.
