# Related-work boundary (targeted scan, 10 October 2026)

This file records the nearest primary sources used to shape the three proposals. It is not an exhaustive literature review or a novelty certificate.

| Work | Already studies | Consequence for our proposal |
|---|---|---|
| [ActMem](https://arxiv.org/abs/2603.00026) | Causal/semantic memory graphs, counterfactual reasoning, ActMemEval | Do not claim causal memory or counterfactual memory reasoning is new. Focus on causal sufficiency after strict state compression and source partitioning. |
| [Causal Memory Intervention](https://arxiv.org/abs/2605.17641) | Controlled intervention to select memories by answer utility and robustness | Do not pitch intervention-based memory selection. Study what causal content the state itself must retain. |
| [Scientifically validated causal benchmark](https://arxiv.org/abs/2510.07231) | Broad causal relationship and identification questions across domains | Separate general model causal reasoning from memory-grounded counterfactual recall. |
| [Memora](https://arxiv.org/abs/2604.20006) | Long-horizon consolidation, changing facts, stale-memory penalty (FAMA) | A new forgetting proposal needs an online eviction mechanism and matched byte/compute budgets, not only a stale-fact score. |
| [PersistBench](https://arxiv.org/abs/2602.01146) | Cross-domain memory leakage and memory-induced sycophancy | Separate utility-aware forgetting from broad memory safety evaluation. |
| [ForgetBench](https://arxiv.org/abs/2607.26455) | Forgetting dynamics under sequential parametric knowledge editing | Explicitly study agent memory stores and online resource allocation; do not conflate with weight editing. |
| [FSFM](https://arxiv.org/abs/2604.20300) | A broad selective-forgetting framework and controlled evaluation | A new contribution must test decision-value-per-byte against adaptive forgetting baselines. |
| [MemOps](https://arxiv.org/abs/2607.12893) | Operation-level traces for remembering, forgetting, updating, reflecting | Reuse lifecycle-style evaluation ideas; target the value policy, not another operation taxonomy. |
| [Long-term memory security survey](https://arxiv.org/abs/2604.16548) | Lifecycle security, including forget and rollback governance | Do not claim the lifecycle/security gap is unexplored. Formulate a specific guarantee for merged compressed state. |
| [MemLineage](https://arxiv.org/abs/2605.14421) | Cryptographic provenance and derivation DAGs for sensitive-action control | The proposed revocation study must compare directly to lineage and test actual removal from compressed/shared state. |
| [ChronoMem](https://arxiv.org/abs/2607.27773) | Versioned snapshots and semantic global rollback | Distinguish source-scoped deletion after fusion from whole-state time rollback. |
| [MEXTRA](https://arxiv.org/abs/2502.13172), [MemoryGraft](https://arxiv.org/abs/2512.16962) | Memory extraction and persistent poisoning through retrieved experience | Treat confidentiality and integrity attacks as existing; the proposed study focuses on revocation after derivation and merging. |
| [MemFuse](https://arxiv.org/abs/2608.18704) | Multi-source fusion with atomic evidence and causal fusion graph | Do not claim multi-source fusion or provenance is new. Test whether equivalent behavior survives a bounded latent representation and later source revocation. |
| [LiveMem](https://arxiv.org/abs/2608.02515) | Fixed-capacity persistent state continuity through context turnover | Persistent state alone is not the contribution; the proposed questions concern causal sufficiency, value-based forgetting, and revocability. |

## Selection rationale

The three selected directions map to distinct scientific questions: what a memory state must **know** to support intervention; what it should **retain** when capacity is scarce; and whether it can **undo** information after that information has propagated. They are related at the systems level, but each has a separate endpoint and can fail independently.

The scan verified the cited titles and abstracts on their primary arXiv pages. Full text and latest versions should be checked again before preregistration or submission because this field is moving quickly.
