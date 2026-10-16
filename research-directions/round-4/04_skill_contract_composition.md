# Skills That Compose: Contract-Aware Procedural Memory under Tool Changes

**Research sketch — 16 October 2026.** Proposal only; no experiment run, preregistration, or originality claim.

## Question and useful outcome

If two remembered procedures each worked before, when is their combination still valid after a tool's schema or environment changes? The agent should check not only that each skill fits the task, but that one skill's output satisfies the next skill's preconditions. This could reduce brittle reuse in coding and workflow agents.

The focus is cross-skill interfaces under controlled tool-version changes. It differs from prospective intention memory, which determines when to execute a deferred commitment, and from state portability, which changes a model host rather than the tools and stored procedures.

## Nearest work and proposed contrast

[Skill-Pro](https://arxiv.org/abs/2602.01869v3), formerly indexed as ProcMEM, learns reusable skills with activation/execution/termination structure. [SkillComposer](https://arxiv.org/abs/2606.32025v1) predicts skill subsets and order. [BASM](https://arxiv.org/abs/2608.22339v1) adds applicability and avoidance boundaries. Consequently, executable memory, skill composition, and boundary fields are established ideas. The proposed narrow contrast is an executable compatibility check between composed skill contracts under randomized tool changes.

## Hypothesis and small first study

Hypothesis: checking inter-skill pre/postcondition compatibility will reduce invalid transitions and improve completed-task utility beyond independent skill-boundary checks at equal observation and tool-call budgets. Added refusals must be counted; a system that blocks every composition is not useful.

Build a deterministic workflow simulator with typed objects, explicit state predicates, and versioned tools. Create tasks requiring two to five skills. Hold the task intent fixed while changing a tool's return field, unit, available operation, or state side effect. Include harmless renames, genuinely incompatible changes, and cases where a short repair makes composition valid. Freeze the skill library before test-time version changes.

Compare no memory, prose skill retrieval, ordered skill composition, per-skill applicability checks, a contract-aware planner, and a symbolic typed planner. Use the same schemas and state observations for every method. Separate an oracle-contract track from an LLM-extracted-contract track: sound guarantees about supplied formal predicates cannot be transferred automatically to model-generated contracts. Keep actual side effects inside the simulator.

Primary endpoint: successful complete tasks with no invalid transitions, plus the per-task invalid-call rate. Report false blocking, repair cost, steps, latency, contract-extraction errors and performance on unchanged tools. Test unseen combinations and unseen changes, not renamed copies of training plans. Set the change distribution and safe-completion threshold before confirmation; cluster uncertainty by task family.

## Stop rule and deliverable

Stop the learned-composition claim if ordinary typing or per-skill boundary checks solve the same cases, or if gains come from extra schema access. If a symbolic planner wins, the useful result is identifying which procedural-memory layer should be formal rather than generative. The initial deliverable is a small version-change benchmark with inspectable contracts; no general guarantee about arbitrary external tools is claimed.
