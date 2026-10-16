# Round 5: ten research sketches across memory, reasoning and agent systems

**Date: 16 October 2026. Status: proposals only.** No new experiment has been run or registered. These are ten proposed study designs, not ten established discoveries or ten entirely new fields. Direct prior work is named in each sketch.

| No. | Working title | Manipulated variable | Draft |
|---:|---|---|---|
| 1 | The Slow Writer Problem | Concurrent write/consolidation schedule and commit validation | [01](01_concurrent_consolidation.md) |
| 2 | Same Evidence, Different Memory | Admissible processing order, batching and consolidation mechanism | [02](02_consolidation_path_dependence.md) |
| 3 | Remember Success without Repeating It | Timing of precedent exposure during fixed-budget discovery | [03](03_exploration_preserving_memory.md) |
| 4 | Right Memory, Wrong Project | Project/role scope cues and clarification policy | [04](04_context_scope_switching.md) |
| 5 | Remember the Exception | Strength of model prior conflict with trusted private episodes | [05](05_private_exceptions.md) |
| 6 | Pause the Thought, Keep the Work | Serialized working-state size under inference preemption | [06](06_resumable_latent_reasoning.md) |
| 7 | Is One More Thought Worth It? | Marginal-value stopping versus confidence stopping | [07](07_value_calibrated_halting.md) |
| 8 | When Concepts Split | Semantic ontology changes and retained discriminating attributes | [08](08_ontology_refinement.md) |
| 9 | Feedback Arrives Late | Feedback delay, memory revision and version attribution | [09](09_delayed_feedback_credit.md) |
| 10 | After the Bad Memory | Poison exposure, benign stream length, consolidation and recovery | [10](10_poisoning_persistence.md) |

Read the [Chinese overview](OVERVIEW.zh-CN.md), [related-work boundary](RELATED_WORK.md), [source inventory](SOURCES.json), and [all-topic index](../INDEX.zh-CN.md).

## Priority and claim level

Sketches 6–7 have the closest architectural connection to persistent internal state and adaptive compute, but require open model access and careful cost measurement. Sketches 1 and 9 have direct workflow-engineering value; conventional concurrency and credit bookkeeping are strong likely winners. Sketches 2 and 4 offer relatively clean diagnostics. Sketches 3, 5, 8 and 10 concern discovery behavior, evidence integration, evolving concepts and memory integrity. All have active predecessors. A method paper needs an actual advantage beyond these baselines; a diagnostic paper needs reproducible identification and a useful result.

## Shared minimum protocol

Start with executable ground truth and a small diagnostic. Separate memory construction, routing, answer integration, reasoning trajectory and stopping where relevant. Match model, evidence access, state bytes and measured compute; disclose unavoidable differences. Use an excluded pilot to set sample size, thresholds and schedules, then freeze paired confirmation. Hold out entire worlds/task families rather than paraphrases. Preserve failures and fit-level variation. Use independent verification where possible and report when simple symbolic or systems controls win.

The literature pass checked current primary entries and selected official documentation, not complete implementations or every appendix. Narrow gaps stated here are proposed contrasts, not certified absences. Before any registration or submission, inspect the nearest full texts and code and refresh the search. Existing v0.1/v0.2 results do not validate this new portfolio. Historical checksum snapshots remain versioned separately from navigation updates.
