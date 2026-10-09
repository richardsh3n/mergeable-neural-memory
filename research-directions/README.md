# Three research directions for persistent LLM memory

**Status:** local working proposals for review. These are not completed papers, registered studies, or claims of novelty. Literature scan updated 10 October 2026; it is targeted, not exhaustive. Nothing in this folder has been pushed to GitHub.

## Selection

| Rank | Direction | Central question | Why it is promising |
|---:|---|---|---|
| 1 | **Counterfactually sufficient memory state** | What causal information must a bounded, mergeable state retain so an agent can answer “what if?” questions about past decisions and events? | It pushes the current state-memory project past recall and asks whether compressed memory can support intervention and transfer. The boundary is narrow enough to test against causal graphs, retrieval systems, and full-history oracles. |
| 2 | **Decision-value forgetting** | Which memory should be evicted when its predicted contribution to future decisions is smaller than the value of the space it occupies? | Long-term memory already has stale-fact and forgetting benchmarks; a prospective, resource-matched eviction policy could move the field from “forgetting as decay” toward measurable decision utility. |
| 3 | **Revocable shared latent memory** | Can one contributor revoke an observation after it has been compressed, derived, and merged, without losing other contributors’ useful information? | This joins practical privacy and governance with the project's fixed-size, mergeable-state constraint. It is hard, measurable, and has direct multi-user and team-agent value. |

The three drafts are in [the master agenda](MASTER_DRAFT.md) and individual proposals [01](01_counterfactual_state.md), [02](02_decision_value_forgetting.md), and [03](03_revocable_shared_memory.md). The short [Chinese overview](OVERVIEW.zh-CN.md) explains the ranking. [Related work and scope](RELATED_WORK.md) records what is already covered and where each proposal would have to be different.

The v0.2 synthetic diagnostic is a separate result. Its future-union objective improved the pooled primary score but failed the preregistered progress gate; it does not validate any of these three directions. See [`../experiments/v02/RESULTS.md`](../experiments/v02/RESULTS.md).

## Local handoff

The files are prepared for GitHub review, but publication is deferred because account 2FA is unavailable on the user's replacement phone. No authentication bypass or push was attempted. The directory can be added to the public repository after the account owner can complete sign-in.
