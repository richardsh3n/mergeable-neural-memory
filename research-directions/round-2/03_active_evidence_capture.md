# Remembering What to Observe: Active Evidence Capture for Lifelong Agents

**Proposal status:** research design only. No benchmark or experiment has been completed. Literature scan: 15 October 2026.

## Abstract

Most memory systems decide what to store from the observations that happen to arrive. Yet an agent often controls which files it opens, tests it runs, or state it inspects. That choice determines what evidence is available to its future self. We propose **active evidence capture**: a memory-aware agent allocates part of its task budget to acquiring and preserving evidence that is useful across an unknown sequence of future tasks, not merely to solving the current one. In a controlled workflow environment, the agent can inspect candidate artifacts, run tests, or log events at a cost; later tasks reuse some but not all learned structure. We compare passive logging, full logging, salience-based writing, and an active capture policy under matched cost and storage budgets. The key measure is future-task regret per total acquisition, storage, and retrieval cost. This tests a practical bridge between memory and active learning while keeping the scope distinct from memory eviction or state compression.

## Research question and motivation

When future tasks are unknown, can an agent choose which evidence to inspect and preserve now so that later tasks become easier or safer, without spending more total resources than passive memory baselines?

In software work, for example, an agent may choose whether to inspect a test fixture, run a targeted test, or record an environment assumption. In web operations it may inspect a page's state or retain a concise trace of a successful workflow. A purely passive memory system stores whatever was observed; a memory-aware policy can invest in acquiring evidence with future reuse value. The difficult part is that immediate task reward and long-run information value may conflict.

## Prior work and novelty boundary

MemCtrl (2026) learns an online memory controller for embodied agents, including whether observations or reflections should be retained. MemAct (Wei et al., 2026; posted 13 October) combines streaming spatial memory with active visual exploration and evaluates when to move or stop. Active retrieval/navigation work such as NapMem also treats memory access as an agent action. These papers establish that active memory control and active exploration are active topics.

The narrower question here is cross-episode **evidence acquisition for unknown future work** in non-visual tool workflows. The agent chooses which available evidence-gathering operation to pay for and which resulting evidence to preserve. The evaluation separates (i) current-task success, (ii) downstream transfer to future task families, and (iii) acquisition/storage/retrieval cost. This is not the earlier proposal's eviction problem: the main intervention occurs before and during observation, when the agent chooses what evidence to create or inspect.

## Hypotheses

**H1 — Selective acquisition transfers:** an active capture policy trained or calibrated on a task-family distribution will improve future-task performance per total cost over full logging and passive salience heuristics.

**H2 — Environment diversity matters:** the advantage will be largest when tasks share hidden reusable structure but differ in surface wording, and will shrink when future tasks are unrelated or the capture policy faces distribution shift.

**H3 — Over-capture can hurt:** saving more traces will increase retrieval interference or cost after a point; an active policy should have a measurable Pareto region rather than dominate at every budget.

## Experimental design

Create a deterministic, sandboxed multi-session workflow suite with a sequence of task families (for example, repository debugging, configuration edits, and command-line data transforms). During each task, the agent can choose among evidence actions with known costs: inspect a file, run a targeted test, read a command's detailed output, or record a structured observation. Some artifacts expose reusable rules; others are distractors or task-specific. Future tasks are drawn from a frozen but partially hidden mixture, with both in-distribution and shifted mixtures. The simulator logs every available evidence option so the opportunity set is auditable.

Compare: (1) no memory; (2) passive transcript/full logging; (3) post-hoc summarization; (4) fixed heuristic capture (errors, successes, changed files); (5) a learned or model-selected active capture policy; and (6) an oracle upper bound that knows future task mixture. To isolate active observation from smarter reasoning, replay a paired condition in which each policy receives the same evidence and can only choose what to retain. To isolate capture value, separately compare policies that may choose evidence actions.

**Primary endpoint:** cumulative future-task regret divided by total cost, where costs include evidence actions, memory tokens/bytes, and retrieval/model calls. Report raw task reward and each cost component separately. Secondary measures: transfer to unseen task variants, success on the first attempt, test/tool calls, evidence coverage, memory precision, retrieval latency, harmful negative transfer, and sensitivity to future-mixture shift.

## Analysis and stop rules

Use paired world/task streams and cluster uncertainty by stream, not individual question. Freeze the future task mixture and an out-of-distribution holdout before tuning. Set a practical gate before confirmation: the active policy must beat the best non-oracle baseline on a preregistered cost-adjusted primary metric while not materially reducing current-task success or increasing harmful transfer. Include a storage-cost sweep to produce a quality-cost frontier, not one cherry-picked budget.

Stop the novelty claim if active capture only duplicates the benefits of post-hoc reflection, if advantage disappears when evidence opportunities are matched, or if the result depends on access to future task labels. If the agent's choices change the environment in ways the simulator cannot score reliably, revise the testbed before scaling.

## Practical value and execution plan

1. Define task generators, evidence actions, exact costs, and hidden reusable structure.
2. Validate with rule-based agents and a small LLM pilot; audit the oracle's achievable bound.
3. Preregister a matched-cost comparison and run a frozen sequence across multiple seeds.
4. Test transfer to a second workflow domain and release traces, opportunity sets, scoring, and analysis scripts.

An eventual system could decide which diagnostic tests to run, which project facts to preserve, or which steps of a recurring workflow deserve a durable record. The proposed study is initially limited to harmless sandbox workflows; it does not claim that an agent should autonomously inspect private or production data.

## References

- Dorbala and Manocha. [MemCtrl: Using MLLMs as Active Memory Controllers on Embodied Agents](https://arxiv.org/abs/2601.20831), 2026.
- Wei et al. [MemAct: Streaming Spatial Understanding with Memory and Active Exploration](https://arxiv.org/abs/2610.17640), 2026.
- Xu et al. [From Passive Retrieval to Active Memory Navigation](https://arxiv.org/abs/2607.05794), 2026.
- Luo et al. [From Storage to Experience: A Survey on the Evolution of LLM Agent Memory Mechanisms](https://aclanthology.org/2026.findings-acl.2069/), Findings of ACL 2026.
