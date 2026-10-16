# Targeted literature boundary — 16 October 2026

The table records existing coverage and the proposed experimental distinction. It is not a systematic review, proof of novelty, or reproduction audit. Primary entries and selected passages were checked; no code or benchmark scores were independently reproduced. Source versions are recorded in [SOURCES.json](SOURCES.json).

| Primary work | Already covered | Consequence |
|---|---|---|
| [M3-Embedding](https://arxiv.org/abs/2402.03216v5) | Multilingual and cross-lingual retrieval | Topic 1 must isolate correction/update consistency, not claim multilingual search as new. |
| [Hindsight](https://aclanthology.org/2026.acl-demo.27/) | Structured persistent memory and multilingual processing; see paper section 4.4 | Test language-triple update failures and decomposition against an existing multilingual system. |
| [Larimar](https://proceedings.mlr.press/v235/das24a.html) | Dynamic episodic editing and sequential updates | Topic 2 cannot claim editable episodic memory broadly. |
| [MQuAKE](https://arxiv.org/abs/2305.14795v3) | Propagation of edits through related knowledge | Evaluate intended dependent changes separately from unrelated collateral changes. |
| [ICM-Bench](https://arxiv.org/abs/2609.04438v3) | Long-term identity reasoning across multimodal person cues | Topic 3 needs explicit paired cue interventions and perception controls. |
| [M3Exam](https://arxiv.org/abs/2606.07402v1) | Multimodal conversational memory and grounding | Do not pitch multimodal memory alone as a new benchmark category. |
| [Skill-Pro](https://arxiv.org/abs/2602.01869v3) | Reusable procedural skills and structured execution conditions | Topic 4 must go beyond adding skill boundaries; the current verified title supersedes older ProcMEM search records. |
| [SkillComposer](https://arxiv.org/abs/2606.32025v1) | Joint selection and ordering of skills | Composition alone is covered; manipulate tool-version changes and compatibility checks. |
| [BASM](https://arxiv.org/abs/2608.22339v1) | Applicability conditions, avoidance boundaries and repair cues | Compare inter-skill verification directly with per-skill boundary checks. |
| [MERIT](https://arxiv.org/abs/2608.05906v2) | Verified correction and unsuccessful-direction memory in agent repair | Topic 5 concerns scoped search coverage, not the invention of negative experience memory. |
| [TANGLE](https://arxiv.org/abs/2608.13921v1) | Unresolvable memory conflicts and uncertainty-aware action | Separate absence inside a fully examined finite domain from unresolved retrieval misses. |

## Search scope

Queries combined agent/LLM memory with multilingual updates, latent correction and locality, multimodal identity, procedural composition, clarification, and negative knowledge. Search results included several direct predecessors, which led to narrower proposals. Primary arXiv, ACL Anthology and PMLR sources support the table. Before registration, inspect full methods, appendices and implementations, and expand citation chasing; a missing search result is not evidence that a contribution is original.

## Separation from the first nine proposals

1. Cross-lingual updates keep the model fixed, unlike model-host migration.
2. Local correction replaces a specific fact, unlike contributor-scoped revocation.
3. Cue binding changes observed cues while stored state remains intact, unlike byte-level damage.
4. Skill contracts concern tool/skill interfaces, unlike deferred-intention triggers or model-state migration.
5. Negative-search memory concerns examined scope and snapshot validity; it does not select observations, infer independent support, or model endogenous evidence feedback.

These boundaries are proposed research choices, not claims that neighboring work cannot address them.
