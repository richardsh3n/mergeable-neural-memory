# Proposal 01 — Counterfactually Sufficient Memory State

**Short name:** CSM
**Status:** concept proposal; no method or results yet.

## Abstract

Persistent memory should let an agent answer more than “what happened?” It should help answer “why did it happen?” and “what would have happened if a prior choice or condition had differed?” Existing work has already explored causal memory graphs, intervention-based memory selection, and broad causal-reasoning benchmarks. We propose a narrower problem: **causal sufficiency under bounded state compression**. The project will construct executable causal worlds expressed as multi-session natural-language evidence, then compare full-history, retrieval, summaries, causal graphs, and fixed-byte learned state on factual and intervention queries. The primary outcome will be counterfactual answer accuracy under a strict memory budget, with evidence-grounding and calibration controls. The proposal succeeds only if a compact state preserves intervention performance beyond what factual recall predicts, and if the effect survives held-out causal mechanisms and source partitioning.

## Research question and hypothesis

**RQ:** What minimum information must a compressed, possibly merged memory state preserve so that an agent can answer valid interventions over remembered events?

**H1:** A writer trained on future intervention queries will produce more intervention-sufficient states than a writer trained only on factual recall, at equal bytes, model, compute, and evidence access.

**H2:** The intervention advantage will be larger when evidence is split across sources, but will disappear when the state budget falls below the amount needed to preserve the task-relevant causal variables.

## Proposed experiment

Start with synthetic structural causal models (SCMs) whose equations, confounders, interventions, and counterfactual outcomes are executable and auditable. Render each event as natural-language dialogue with controlled omissions and source ownership. Train/test splits should hold out graph structures and mechanisms, not paraphrases. Include factual queries, “why” questions, `do(X=x)` interventions, individual counterfactuals, and unanswerable cases where the evidence does not identify an effect.

Compare: full raw history; retrieval with matched token budget; abstractive summary; explicit causal graph; a fixed-capacity learned state; and an oracle that reads all permitted evidence. Freeze the reader where possible, or evaluate each representation through a shared reader, to separate representation quality from language-model reasoning. Sweep bytes per world and number of independent sources. Score factual exact match, intervention accuracy, counterfactual consistency, calibration on non-identifiable cases, and citations to supporting evidence.

## Novelty boundary

[ActMem](https://arxiv.org/abs/2603.00026) already converts dialogue into causal and semantic graphs and uses counterfactual reasoning. [Causal Memory Intervention](https://arxiv.org/abs/2605.17641) already selects memories by causal effect on answer quality. A broad “causal memory for LLMs” claim would therefore be weak. The distinct thesis here is that **a persistent compressed state should be tested for intervention sufficiency at fixed bytes**, across held-out causal structures and partitioned evidence. [MemFuse](https://arxiv.org/abs/2608.18704) covers multi-source evidence fusion with atomic evidence and causal organization, so source fusion alone is also not a novelty claim.

## Primary endpoint and stop criteria

Primary endpoint: intervention exact-match accuracy at the smallest registered state budget where factual accuracy is at least 80%, compared with a resource-matched summary and retrieval baseline. The exact threshold should be fixed using a pilot set that is excluded from confirmatory evaluation. Require positive paired effects on at least three independent SCM families and at least four fresh training seeds. Stop if (a) full-history and memory-state results are indistinguishable at the selected budget, (b) gains vanish under mechanism holdout, (c) the model answers unidentifiable interventions confidently, or (d) a causal graph solves the same task at materially lower cost.

## Main risks

Synthetic SCMs may be too clean; textual rendering may leak the equations; a shared reader can be unfair to one representation; and gains may reflect task-specific labels rather than a general state abstraction. Counter these with hidden mechanism generators, blinded question templates, explicit ablations, and a real-domain replication only after the synthetic mechanism passes.
