# Round 4: five focused research sketches

**Dated 16 October 2026.** These are candidate studies, not completed experiments, accepted papers, or verified originality claims. The literature check is targeted and primary-source based; refresh and expand it before preregistration.

| Topic | Proposed narrow contrast | Draft |
|---|---|---|
| One Memory, Many Languages | Cross-language correction consistency, with a fixed host and oracle-retrieval decomposition | [01](01_crosslingual_updates.md) |
| Correct One Fact, Preserve the Rest | Local state edits with valid dependent updates and minimal unrelated damage | [02](02_local_latent_correction.md) |
| Who Goes with What? | Paired cue-swap tests separating cross-modal binding from perception and caption shortcuts | [03](03_crossmodal_binding.md) |
| Skills That Compose | Inter-skill contracts under controlled tool-version changes | [04](04_skill_contract_composition.md) |
| Not Found Is Not False | Reuse of scoped negative search observations under corpus and coverage changes | [05](05_coverage_aware_negative_memory.md) |

Read the [Chinese overview](OVERVIEW.zh-CN.md), [nearest-work boundary](RELATED_WORK.md), [source inventory](SOURCES.json), and [fourteen-topic index](../INDEX.zh-CN.md). Every individual sketch states the question, hypothesis, minimal experiment, strong controls, metrics, and stop rule. No new experiment was executed to prepare this pack.

## Suggested priority

Local latent correction offers a direct architectural question but must outperform editable symbolic state. Coverage-aware negative memory offers the cleanest inexpensive first diagnostic. Skill-contract composition has immediate agent-engineering relevance but especially close recent predecessors. Cross-lingual consistency is practically useful, and cross-modal binding needs careful perception controls before a memory claim is warranted.

## Minimum execution discipline

Validate the executable task truth first; use a separate pilot to set budgets, thresholds, calibration and sample size; freeze a paired confirmatory comparison; release all seeds, traces and failed conditions. Keep training/test groups at world, character, corpus, or task-family level as appropriate. Count metadata and side channels, compare with strong conventional stores, and report negative results. A proposal merits a method claim only if its candidate survives these controls.

Historical manifests in earlier rounds describe earlier snapshots. Navigation and publication-status edits are versioned separately; earlier checksums are preserved rather than silently replaced. The current per-round manifests identify the files in the current publication snapshot. The frozen v0.1/v0.2 experimental artifacts remain separate evidence.
