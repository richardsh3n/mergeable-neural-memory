# Three new frontiers for agent memory

**Status:** literature-informed research proposals, not completed experiments, registered studies, or novelty claims. Scan date: 15 October 2026. The scan is targeted and should be refreshed before preregistration.

This second set is intentionally distinct from the first set in `../`: it does not repackage counterfactually sufficient state, decision-value forgetting, or revocable shared memory. It shifts the unit of study from stored representations to the agent's ongoing control loop: carrying intentions into action, learning from selectively observed outcomes, and deciding what evidence to capture for future tasks.

| Priority | Working title | Main question | Why it matters |
|---:|---|---|---|
| 1 | **Prospective memory for interrupted tool agents** | Can an agent carry an intention through interruptions and execute it exactly when external workflow conditions permit? | Connects memory to reliable action, deadlines, cancellation, and duplicate side effects. |
| 2 | **The self-confirming memory loop** | When an agent acts on stored beliefs and then selectively observes outcomes, can its own memory create persistent, unjustified confidence? | Isolates a feedback failure that static recall and static belief calibration do not capture. |
| 3 | **Active evidence capture for lifelong agents** | Which observations should an agent deliberately acquire and preserve now to improve unknown future tasks under a fixed cost? | Moves memory research upstream from retrieval/compression to the agent's choice of what to observe and log. |

Read the [Chinese decision brief](OVERVIEW.zh-CN.md), the [integrated agenda](MASTER_DRAFT.md), the [related-work boundary](RELATED_WORK.md), and the three [individual proposals](01_prospective_tool_memory.md), [02_self_confirming_loop.md](02_self_confirming_loop.md), and [03_active_evidence_capture.md](03_active_evidence_capture.md).

## Claim discipline

Recent 2026 papers already cover text-based prospective memory, memory-induced anchoring, probabilistic belief memory, online memory controllers, and embodied active exploration. These proposals therefore make no “first ever” claim. Each specifies a narrower experimental gap and a direct falsification test. The immediate recommendation is Proposal 1 for a practical, bounded first study; Proposal 2 has the strongest conceptual upside but needs careful simulator validation; Proposal 3 is the most architectural and should begin only after a clean task interface is frozen.

The prior proposal round remains in the parent directory. The v0.2 diagnostic remains a separate, underpowered synthetic study and is not evidence for any proposal here.
