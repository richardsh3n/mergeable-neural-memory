# From Memory Store to Memory-Controlled Agent: Three New Research Programs

**Working agenda — 15 October 2026**  
**Status:** proposal set. No benchmark, algorithm, or result is claimed as original or completed.

## Abstract

Long-term memory research is moving quickly beyond retrieval. Recent work has introduced prospective-memory benchmarks, typed intention stores, probabilistic belief memories, memory-use policies, and embodied active exploration. The next proposals should therefore target narrow questions that existing systems do not settle, rather than rename a broad capability. This agenda studies three complementary parts of the agent loop: (1) **prospective memory under interruptions and tool side effects**, where success means executing a deferred intention exactly when permitted; (2) **self-confirming memory loops**, where a memory-conditioned policy changes which evidence the agent sees and can thereby entrench error; and (3) **active evidence capture**, where the agent chooses what to inspect and preserve for unknown future tasks. Each proposal includes close prior work, a falsifiable design, resource-matched comparisons, practical outputs, and explicit stop conditions. The programs are independent; the recommendation is to start with the first because it is the most directly useful and easiest to score exactly.

## Why this is a second set

The first research-direction pack studies the information content of a bounded memory state, how to allocate a fixed memory budget through forgetting, and source-scoped revocation after shared-memory fusion. This second set asks about **control over time**: how intentions become future actions; how actions affect later evidence and memory; and how an agent chooses to gather evidence for future use. They are related to persistent memory but are not substitutions for the earlier three.

## Proposal 1 — Prospective memory for interrupted tool agents

**Question:** Can an agent carry a deferred commitment through interruptions and changing external state, then execute it exactly once and only when its trigger and prerequisites are valid?

PM-Bench (2026) establishes a text-based prospective-memory task, and PIS (2026) demonstrates the value of typed intention storage on that benchmark. The research opportunity is not to invent prospective memory. It is to test its action boundary: cancellation, rescheduling, partial completion, uncertain tool outcomes, duplicate side effects, and current-world verification. A deterministic workflow simulator can make this precise without sending real messages or modifying external accounts.

**Hypothesis:** an explicit intention lifecycle and pre-action state check improve safe fulfillment over free-form notes at equal model and token budgets, while idempotency-aware handling reduces duplicate actions after ambiguous tool outcomes.

**Study:** compare transcript, typed store, and typed store plus trigger verification/idempotency across paired task streams. Score safe completion and report missed, premature, late, duplicate, canceled, and correctly abstained actions separately. Include task success, tool calls, latency, and token cost. Bridge to PM-Bench-style tasks, but do not mix results across different harnesses.

**Stop rule:** no broad novelty claim if the action-oriented extension does not distinguish from existing typed intention stores, or if gains only follow from larger budgets. Fail the safety gate if canceled or duplicate actions rise.

Full draft: [01_prospective_tool_memory.md](01_prospective_tool_memory.md).

## Proposal 2 — The self-confirming memory loop

**Question:** Does a stored belief alter the agent's actions in a way that changes its evidence stream, causing its future memory to reinforce an initially incorrect belief?

BeliefMem models uncertainty in memory under partial observability; experience-following work studies error propagation; ICML 2026 work examines whether self-evolving agents faithfully use past experience. The proposed distinction is a causal one: randomize the evidence-selection mechanism while fixing the world, model, and observation budget, to isolate endogenous sampling from ordinary update errors.

**Hypothesis:** policy-selected evidence can make incorrect beliefs persist longer than randomized evidence exposure; a low-rate randomized audit may lower long-run regret, but its effect should depend on observability and prior strength.

**Study:** use a known-ground-truth partially observable simulator. Compare deterministic and probabilistic memories, policy-selected observations, randomized audits, and an oracle. Measure decision regret, calibration, time to correct, harmful action repetition, observation coverage, and cost.

**Stop rule:** if policy-selected exposure does not cause additional persistence over randomized exposure, the central mechanism is not supported. If only one model exhibits it, keep the claim model-specific. A failed symbolic control invalidates the environment until repaired.

Full draft: [02_self_confirming_loop.md](02_self_confirming_loop.md).

## Proposal 3 — Active evidence capture for lifelong agents

**Question:** Can an agent choose which observations to acquire and preserve now to improve unknown future tasks under a fixed overall resource budget?

MemCtrl already addresses online memory filtering in embodied agents, while MemAct (posted 13 October 2026) combines spatial memory with active exploration. The proposed scope is cross-episode, non-visual tool workflows: an agent chooses among diagnostic or inspection actions, pays for them, and decides which resulting evidence should persist. It separates current-task benefit from downstream transfer and total acquisition, storage, and retrieval cost. It also differs from the earlier decision-value forgetting proposal because its main control is at evidence acquisition, before or during memory formation.

**Hypothesis:** a selective capture policy can improve future-task performance per total cost over full logging and passive writing heuristics when tasks share reusable structure, but may fail under unrelated tasks or distribution shift.

**Study:** use sandbox task sequences with explicit evidence-gathering actions. Compare no memory, full logging, post-hoc summaries, fixed heuristics, active capture, and an oracle. Replay matched-evidence conditions to separate active observation from retention. Report the quality-cost frontier and transfer/negative-transfer outcomes.

**Stop rule:** do not claim active capture if it merely reproduces reflection benefits, depends on future task labels, or loses its advantage when evidence opportunities and costs are matched.

Full draft: [03_active_evidence_capture.md](03_active_evidence_capture.md).

## Cross-study protocol

All three studies should expose the memory write, read, decision, and environment interfaces. Keep a frozen task generator, paired random seeds, and complete action/memory traces. Match backbones and budgets for confirmatory comparisons. Use symbolic or deterministic controls where available to verify the environment independently of language-model behavior. Report component errors and cost curves; avoid a single score that conceals harmful behaviors. Run the smallest diagnostic that can falsify the central mechanism before scaling. Publish negative results and protocol deviations.

The previous v0.2 synthetic diagnostic missed its preregistered progress gate and has a disclosed RNG-protocol deviation. It motivates strict audit practice but does not support these hypotheses or establish an LLM memory capability.

## Ranking and next action

Start with Proposal 1. It has the clearest practical case, a deterministic testbed, and outcomes that can be scored without a generative judge. Advance Proposal 2 after a symbolic simulator verifies the endogenous evidence mechanism. Advance Proposal 3 after a frozen, reproducible task suite defines comparable evidence-action costs and future task distributions. Do not launch all three as one experiment.

## Claims boundary

The literature scan is targeted through 15 October 2026 and is not an exhaustive novelty search. Several direct neighbors are only months old. Before preregistration, verify the newest versions, inspect full methods and code, add any 2026–2027 follow-up work, and conduct a structured search across ACL Anthology, OpenReview, PMLR, arXiv, and relevant systems venues. Any paper must state the difference from its nearest predecessor as an explicit experimental contrast, not a slogan.
