# Updated nearby-work audit (2026-10-10)

This is a targeted primary-source audit, not an exhaustive novelty certificate.

| Work | Already covered | Boundary for this project |
|---|---|---|
| [Cache Merging, v2](https://arxiv.org/abs/2607.01308v2), Baquero & Brito, revised Oct 2, 2026 | KV fragment set union, deterministic rendering, duplicate absorption, split-evidence latent reasoning | Content-addressed fragment storage grows; bounded compressed learned state remains a different constraint. v2 explicitly limits k>2 composition; do not use v1's corrected HotpotQA interpretation. |
| [LiveMem](https://arxiv.org/abs/2608.02515), Liu et al. | Fixed-capacity intrinsic state, context turnover, memory post-training, actual pretrained LLM | Persistent neural state alone is not our novelty; our prototype has no language backbone. |
| [MemFuse](https://arxiv.org/abs/2608.18704), Li et al. | Fragmented multi-source observations, source provenance, causal memory organization and evaluation | Event-layer raw evidence plus cluster/graph retrieval differs from state-only fixed-capacity merging; multi-source fusion alone is occupied. |
| [MEMAUDIT](https://arxiv.org/abs/2605.02199), Bhargava & Barrento | Budgeted memory writing, future-query requirements, certified finite selection oracle, reader/writer separation | Future-query-aware memory writing and audit separation alone are not new. Our trial is continuous neural writer adaptation, without their certified optimum. |

The candidate future-union objective below is an ordinary supervised intervention.
MAXSET split/centralized equivalence prevents describing it as a new distributed
learning method. A publishable contribution would require a distinct constraint,
nontrivial method, strong resource-matched comparison and replicated evidence.
Read together with the original docs/LITERATURE_AUDIT.md and THEORY.md.
