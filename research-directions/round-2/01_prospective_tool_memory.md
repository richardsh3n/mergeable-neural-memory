# Past Intention, Future Action: Prospective Memory for Interrupted Tool Agents

**Proposal status:** research design only. No benchmark or experiment has been completed. Literature scan: 15 October 2026.

## Abstract

Persistent assistants must remember not only what happened but what they have promised to do later. A deferred intention may be due at a time, after an event, or only once a dependency is satisfied; meanwhile, the agent may be interrupted, receive a cancellation, or lose certainty about whether an external action succeeded. Recent work has made prospective memory an explicit LLM-agent capability, but existing evaluations primarily use text-based simulated routines, and typed intention stores already improve those settings. We propose a controlled study of **side-effectful prospective memory** in tool workflows. The agent must maintain an intention's lifecycle, detect its trigger, verify the current world state, and execute exactly once—or abstain when execution status is uncertain. The primary endpoint is safe intention fulfillment, jointly penalizing missed, premature, duplicate, canceled, and stale actions. The contribution would be an action-grounded evaluation and a minimal memory-control mechanism, if the latter beats strong typed-state baselines under matched model and token budgets.

## Research question and motivation

Can a persistent agent carry a deferred intention through interruptions and execute it at the right future condition without acting too early, twice, or after it has been canceled?

This differs from retrospective memory. A system may correctly recall “send the invoice on Friday” and still fail because it forgets the commitment while handling other tasks, sends it before approval, repeats it after a timeout, or ignores a cancellation. These are state-transition and action-control failures, not just retrieval misses. They matter in calendar, email, issue-tracker, and project-agent workflows where tool calls can have consequences.

## Prior work and novelty boundary

PM-Bench (Liu and Gabriel, 2026) adapts the Virtual Week paradigm to text-based agent interaction and measures delayed intentions, ongoing activity, and environment cues. Zhao and Wu (2026) introduce a typed Prospective Intention Store and report substantial gains on PM-Bench, including with small models. These are direct predecessors. The present proposal should not claim that prospective memory, event-triggered intentions, or typed intention state is new.

The narrower unresolved test proposed here is whether the agent can safely **execute** deferred intentions in tool workflows with side effects and uncertain outcomes. The stressors are lifecycle changes, partial completion, asynchronous tool results, external dependencies, cancellation, and idempotency. If PM-Bench plus a typed store already predicts performance on these cases, the proposed extra task layer is not justified.

## Hypotheses

**H1 — Lifecycle state helps:** an explicit intention state machine (pending, blocked, due, executing, completed, canceled, expired, outcome-unknown) will improve safe fulfillment over free-form notes at equal model and context budgets.

**H2 — Trigger verification matters:** checking the current environment before acting will reduce premature and stale executions, with a measurable latency/tool-call cost.

**H3 — Uncertainty should stop side effects:** when a tool timeout leaves completion unknown, an agent with an explicit outcome-unknown state and idempotency key will duplicate fewer actions than one that retries from a natural-language reminder.

H1–H3 are falsifiable design hypotheses, not expected results.

## Experimental design

Build a deterministic workflow simulator with seeded task streams. Each stream contains concurrent work and deferred intentions with one or more of: time triggers, event triggers, prerequisites, deadlines, cancellation, rescheduling, partial execution, external state changes, and uncertain tool outcomes. Tool actions should be reversible or simulated; no real account or external service is involved. Ground truth records the exact intention lifecycle and permissible execution windows.

Use paired task seeds and the same backbone, prompt budget, tool surface, and inference limits for each condition. Start with a small open-weight model to make runs affordable; replicate the central result with a second model family. Freeze the task generator, scoring, and analysis before the confirmatory run.

**Primary comparison:** free-form transcript memory vs. typed intention store vs. typed store plus trigger verification/idempotency. Include no-persistent-memory and full-history references. Reimplement the PM-Bench/PIS task shapes as a bridge subset, but do not compare reported numbers across papers unless the runtime and grading are exactly matched.

**Primary metric:** Safe Fulfillment Rate: fraction of intentions completed once, inside the valid execution window, with all prerequisites satisfied and no cancellation. Report component metrics separately: missed, early, late, duplicate, canceled-after-execution, unverified, and correctly abstained actions. Also measure task completion, latency, tool calls, visible tokens, and user-intervention rate. No single weighted score should hide a rise in harmful actions.

## Analysis and stop rules

Estimate paired differences with confidence intervals clustered by task stream. Report each lifecycle stressor separately and the full score distribution. Predefine a practical minimum benefit (for example, at least a 5 percentage-point increase in safe fulfillment with no increase in canceled or duplicate actions) before running; calibrate sample size using a pilot that is excluded from confirmation.

Stop or revise the claim if: (a) state-machine gains vanish against a strong typed-state baseline; (b) improvements come only from more tokens or tool calls; (c) the simulator's trigger rules are ambiguous to human reviewers; or (d) performance gains trade off against more unsafe side effects. A failed gate is a result, not grounds to alter the endpoint after inspection.

## Practical value and execution plan

1. **Specification:** define an intention schema, state transitions, tool outcomes, and a safety-oriented score; obtain independent review of edge cases.
2. **Diagnostic pilot:** implement 100–200 streams, test grader reliability and verify all state transitions mechanically.
3. **Confirmatory study:** preregister a power-based sample, run the frozen paired comparison on one backbone.
4. **Replication and release:** repeat on a second backbone; publish simulator, seeds, action traces, and failure taxonomy with a permissive license.

The practical output is a reusable test harness for reminder and workflow agents, plus evidence about when a typed intention state is worth its operational complexity. The scope excludes medical, financial, or other high-stakes autonomous execution.

## References

- Liu and Gabriel. [PM-Bench: Evaluating Prospective Memory in LLM Agents](https://arxiv.org/abs/2607.12385), 2026.
- Zhao and Wu. [Making Prospective Memory SLM-Shaped: Typed Intention Stores for Small-Model Agents](https://arxiv.org/abs/2609.01272), 2026.
- He et al. [Benchmarking Agent Memory in Interdependent Multi-Session Agentic Tasks](https://proceedings.mlr.press/v306/he26am.html), ICML 2026. Used as a reminder to evaluate downstream task behavior, not recall alone.
