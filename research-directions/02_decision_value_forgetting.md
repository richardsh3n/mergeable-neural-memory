# Proposal 02 — Decision-Value Forgetting

**Short name:** DVF
**Status:** concept proposal; no method or results yet.

## Abstract

An agent with finite memory must discard information. Current work increasingly evaluates stale beliefs and forgetting, but the central operational choice remains: which item should be removed now, given uncertainty about future tasks? We propose **decision-value forgetting**: estimate each memory's expected marginal reduction in future decision regret per byte and evict the least valuable items subject to privacy and validity constraints. A streaming benchmark would vary task recurrence, concept drift, conflicting updates, and expiration. At equal storage and inference budgets, the learned eviction policy would be compared with recency, frequency, decay, semantic salience, and oracle policies. The central claim is falsifiable: decision-value retention should improve long-horizon utility without increasing stale-memory use or violating explicit expiration rules.

## Research question and hypothesis

**RQ:** Can an agent learn an online memory-eviction policy that preserves future task value better than age-, frequency-, or similarity-based heuristics under a fixed memory budget?

**H1:** A value-per-byte policy will reduce cumulative decision regret at equal storage and inference cost.

**H2:** Its advantage will be largest after task-distribution shifts where old high-frequency memories become misleading, provided the value estimator can detect uncertainty and validity changes.

## Proposed experiment

Construct a sequential stream of user/agent episodes with explicit facts, decisions, outcomes, validity intervals, and source. Each item has a byte cost and may affect one or more future task families. The policy sees only the past and current write event. Evaluation streams contain unannounced recurrence schedules and change points. Include stable preferences, superseded preferences, rare high-impact constraints, irrelevant personal details, and memories whose utility decays independently of their age.

Compare LRU, time decay, frequency, semantic similarity, static salience, learned task-value, and an oracle policy that sees the future. All methods use the same storage limit and retrieval model. Measure cumulative reward/regret, current-fact accuracy, stale-use rate, protected/expired fact recall, latency, and bytes. Use Memora/MemOps-style operation traces to distinguish write, update, expiration, and eviction failures rather than relying only on final answer accuracy.

## Novelty boundary

[Memora](https://arxiv.org/abs/2604.20006) introduces long-duration personalization streams and FAMA, which penalizes reliance on obsolete memories. [PersistBench](https://arxiv.org/abs/2602.01146) studies cross-domain leakage and sycophancy tied to persistent memory. [ForgetBench](https://arxiv.org/abs/2607.26455) studies retention dynamics under sequential parametric editing; [FSFM](https://arxiv.org/abs/2604.20300) lays out selective-forgetting mechanisms; and [MemOps](https://arxiv.org/abs/2607.12893) evaluates lifecycle operations. Therefore, another benchmark or recency-decay method would not be enough. The proposed distinction is a prospective **decision-regret objective under matched byte/compute budgets**, including explicit policy deletion separate from ordinary capacity eviction.

## Primary endpoint and stop criteria

Primary endpoint: normalized cumulative decision regret over a held-out stream, with identical memory bytes and LLM calls. Require the policy to beat the strongest non-oracle heuristic across multiple shift schedules and keep stale-memory use no worse than that baseline. Report the oracle gap but do not treat it as an achievable target. Stop if performance depends on access to future test tasks, if gains disappear after matching inference compute, or if the value estimator cannot distinguish stale high-frequency memories from still-valid rare constraints.

## Main risks

Expected future value can be difficult to estimate without leakage; reward design can privilege one task family; privacy expiration may conflict with task utility; and policy complexity may cost more than it saves. Predefine task distributions, reserve hidden shift schedules, separate immutable deletion rules from learned ranking, and count the estimator's compute and memory overhead.
