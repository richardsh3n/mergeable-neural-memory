# Round 3: operational contracts for persistent memory

**Status:** literature-informed proposals dated 15 October 2026. No new experiments have been run, registered, or submitted. These drafts do not certify novelty. They are prepared for the public research branch of Mergeable Neural Memory.

| Priority | Topic | Main experimental difference |
|---:|---|---|
| 1 | [Writable state portability](01_writable_state_portability.md) | Preserve future writes and corrections after repeated model migrations, rather than testing frozen reads alone. |
| 2 | [Dependency-preserving memory](02_dependency_preserving_memory.md) | Preserve calibrated evidence dependence after bounded compression and merging, rather than merely screening new writes. |
| 3 | [Graceful memory degradation](03_graceful_memory_degradation.md) | Preserve useful selective recall after accidental state damage, compared directly with conventional coding and local rejection. |

Read the [Chinese overview](OVERVIEW.zh-CN.md), [integrated agenda](MASTER_DRAFT.md), [related-work boundary](RELATED_WORK.md), and [source-version inventory](SOURCES.json). The [nine-topic index](../INDEX.zh-CN.md) maps all three proposal rounds. File hashes are recorded in [MANIFEST.json](MANIFEST.json), excluding the manifest itself.

Each topic tests a different contract: what a memory means after changing its host; how strongly it should be believed after combining dependent reports; and what can still be trusted after its state is damaged. Existing portability, governance, associative-memory, and coding research are direct predecessors. The claimed opportunities are narrower intersections and require systematic review before submission.

The underlying v0.1/v0.2 synthetic results do not validate these proposals. This round does not modify their frozen inputs, trained models, results, or reporting decisions.
