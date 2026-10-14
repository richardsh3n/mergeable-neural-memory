# Repetition Is Not Evidence: Dependency-Preserving Compression of Agent Memory

**Working proposal, 15 October 2026.** No study has been run or externally registered.

## Abstract

Ten memories may describe ten independent observations or ten paraphrases of one report. A compressed state that remembers the claim but loses its evidence dependence can produce unjustified confidence. Existing work already governs false memory promotion from correlated traces and models peer reliability. This proposal asks a narrower representational question: can a bounded state preserve enough dependence information to support calibrated belief updates after streaming compression and state merging? An executable generative model supplies the posterior oracle. The study compares independent-evidence assumptions, exact deduplication, dependency-aware symbolic summaries, and learned states at matched serialized budgets. Proper probability scores and false-certainty rates, rather than recall alone, define success.

## Question and an identifiability boundary

What dependence information must compressed memory retain to distinguish independent corroboration from copied or jointly caused reports, and how does losing that information affect later decisions?

A simple boundary should be stated before proposing a network. Consider two worlds yielding the same visible sequence of claim strings. In one, every report is an independent noisy observation; in the other, all reports copy one noisy observation. Their correct posteriors can differ. Any deterministic writer receiving only those strings produces the same state, so one reader cannot recover both distinct posteriors. This follows from input indistinguishability, not from a new theorem about LLMs. At least some provenance or a prior over dependency structures is needed. When provenance is unavailable, the evaluator's correct target is the posterior marginalized over that uncertainty, not an oracle posterior conditioned on hidden lineage.

This rules out a misleading claim that a latent state can infer missing source independence by itself.

## Prior work and distinct scope

GovMem directly studies false promotion from correlated traces with dependency-aware governance. Sigma-Mem models historical competence and peer relationships for coordination. Both are necessary predecessors; neither “correlation-aware memory” nor “trust weighting” can be claimed as new here. Our proposed contrast is what survives **bounded compression, partitioned writing, and later state fusion**, with calibrated answer probabilities and complete accounting for retained dependence metadata.

Unlike the prior revocation proposal, no source is deleted. Unlike the self-confirming-loop proposal, actions do not choose the evidence stream: reports arrive exogenously. This isolates source dependence and representation loss from governance, consent withdrawal, and policy-induced sampling bias.

## Hypotheses and candidate mechanism

H1: at equal serialized bytes, a dependence-aware state has lower posterior log loss than a content-only state when repeated reports share origins.

H2: exact-string deduplication will remain inadequate when copies are paraphrased, while collapsing every same-valued report will incorrectly discard genuine independent support.

H3: the advantage will shrink when lineage is missing or when a compact symbolic sufficient-statistic store already solves the task more cheaply.

A candidate stores claim beliefs plus compact origin-group summaries and uncertainty about group assignment. Learned writes and merges may approximate this representation, but IDs, sketches, confidence fields, and auxiliary tables count toward the byte budget. Collision handling and unresolved lineage must be explicit. Exact origin labels may be given only in a named controlled arm; they must not silently improve the candidate alone.

## Controlled study

Generate binary and categorical hidden facts with known observation reliabilities. Produce independent reports, copied reports, partial shared causes, contradictory reports, and paraphrased copies. Partition reports across writers and vary merge order, overlap, and source-count. Test both full lineage and uncertain lineage conditions with the same information available to every method. Use hidden origin clusters rather than text duplicates as the causal unit.

Use an exact Bayesian or enumerated oracle for small worlds and publish its generative assumptions. Include matched pairs with identical report count/content but different available dependency metadata. Confirm that the oracle distinguishes independent support from copied support and treats unknown dependencies conservatively under the declared prior.

Baselines: full-evidence posterior; independent-report accumulation; exact deduplication; semantic deduplication; a compact dependency-aware symbolic store; a content-only learned state; and a learned dependence-aware state. Priors and source reliability inputs must be shared. A full evidence graph is a privileged reference when it exceeds the budget. Memory updates are evaluated before and after merges using a frozen query distribution.

Primary endpoint: mean posterior log loss across held-out worlds at preregistered serialized budgets; compare world-paired effects. Secondary outcomes: Brier score, false-certainty rate, confidence change from copied reports, confidence change from genuinely independent reports, decision regret under fixed error costs, factual recall, and metadata/collision cost. Numerical clipping for log loss is fixed in advance and disclosed. Plot results over correlation and storage budgets; do not choose one favorable dependence level.

Hold out source families, paraphrase templates, and dependency graph shapes. Train/test splitting by individual report would leak shared origins. Set sample size, storage sweep, effect threshold and calibration procedure on an excluded pilot. Use world-level intervals and report every fit.

## Stop criteria and value

Reject the learned-state advantage if it requires hidden lineage, extra evidence, or uncounted per-source state. Reject a general robustness claim if gains disappear on unseen dependency structures. If the symbolic statistic store wins, that is an actionable result: use it instead of a neural dependency state. If metadata is absent, report the identifiability limit rather than attributing it to insufficient model size.

Stage the work as oracle validation, representation comparison, frozen confirmatory run, and a small natural-language replication. This would inform research assistants, multi-source reporting, and team agents where repeated summaries can look like multiple witnesses. It does not establish factual truth from consensus or allow memory confidence to stand in for live verification.

## Primary references

- Qi et al. [When Not to Write Memory: Governing False Promotion from Correlated Agent Traces](https://arxiv.org/abs/2607.02579v1), 2026.
- Feng et al. [Sigma-Mem: An Online Reliability Memory for LLM-based Multi-Agent Systems](https://arxiv.org/abs/2607.27958v1), 2026.
