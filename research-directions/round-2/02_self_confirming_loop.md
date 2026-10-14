# The Self-Confirming Memory Loop: Causal Tests of Endogenous Evidence Bias

**Proposal status:** research design only. No benchmark or experiment has been completed. Literature scan: 15 October 2026.

## Abstract

Long-lived agents act on stored beliefs, and their actions affect which evidence they observe next. If an agent's memory makes it avoid disconfirming tests, an initially weak or mistaken belief may become behaviorally entrenched even when the memory was initially well calibrated. Existing work has begun to study probabilistic belief memory and experience-following errors, but a key causal factor remains separable: **the policy-induced observation process**. We propose a controlled partially observable environment in which memory determines actions, actions determine evidence exposure, and that evidence updates memory. Randomized audits and counterevidence-seeking interventions will identify when this closed loop creates persistent error and whether a small verification policy breaks it. The study's primary outcome is downstream decision regret under equal information and compute budgets, with belief calibration and observation diversity as explanatory measures.

## Research question and motivation

Can an agent's own policy create a self-confirming memory loop by selecting actions that expose it mainly to evidence consistent with its current stored belief? If so, which low-cost intervention restores correction without making the agent indiscriminately skeptical?

The mechanism is a loop: stored belief → action choice → selective observation → memory update → stronger or weaker belief. A transcript-only evaluation can miss the problem because it supplies evidence exogenously. A static belief benchmark can also miss it because it measures whether uncertainty is represented at one moment, not whether actions bias future evidence.

## Prior work and novelty boundary

BeliefMem (2026) proposes probabilistic belief states under partial observability and motivates them partly by self-reinforcing errors from committing to one conclusion. Xiong et al. (ACL 2026) measure experience-following behavior, error propagation, and misaligned replay; Zhao et al. (ICML 2026) study whether self-evolving agents faithfully use past experience. These works make it inappropriate to claim that memory can reinforce errors or that uncertainty-aware memory is wholly unexplored.

The proposed contribution is the **causal isolation of endogenous evidence selection**: hold the underlying world, initial belief, memory representation, model, and task fixed; randomize whether evidence exposure is policy-selected, randomized, or externally audited. Then test whether the choice mechanism changes belief error and decisions over time. The focus is not a new uncertainty data structure, but the interaction of memory with the agent's own observation policy.

## Hypotheses

**H1 — Selection amplifies error:** when observations are action-dependent, memory-conditioned policies will sustain incorrect beliefs longer than matched policies receiving randomized observations, even if both use the same calibrated belief update.

**H2 — Audits interrupt loops:** a low-rate randomized evidence audit will reduce long-run decision regret and belief error more than a same-cost generic reflection step.

**H3 — Blind audits have a cost:** audits will help most when initial uncertainty is material and action-dependent observability is strong; they will waste budget or reduce reward in fully observable/stationary conditions.

## Experimental design

Use a seeded POMDP / multi-armed diagnostic environment with known latent state and action-dependent observation channels. Create matched worlds where a misleading initial observation suggests a false rule, where the correct hypothesis is rare but discoverable, and where evidence is non-diagnostic. Vary observability, prior strength, reward asymmetry, and change points. The state and evidence generator must be auditable and independent of the model.

The main conditions are: (1) no persistent memory; (2) deterministic fact memory; (3) probabilistic belief memory; (4) each of conditions 1–3 with policy-selected observations; (5) the same agent with randomized audits; and (6) an oracle-observation upper bound. Keep action opportunities, token budgets, and feedback budgets matched. To avoid confounding reader strength, evaluate both a symbolic Bayesian controller and an LLM agent on the same observation/action traces; the symbolic arm verifies the task mechanism while the LLM arm tests the interface.

**Primary endpoint:** cumulative decision regret relative to the known environment optimum. Secondary endpoints: time to correct a false belief, posterior Brier score/calibration, probability of repeating a harmful action, observation coverage, rate of counterevidence acquisition, memory-write count, and cost per correction. Also report a no-memory baseline so the study does not mistake ordinary policy-learning failure for a memory-specific effect.

## Causal identification and analysis

Randomize the observation policy at the episode level while holding the generated worlds fixed. Use common random numbers for paired arms. The key contrast is policy-selected versus randomized observation at equal observation budget; the audit contrast tests a practical mechanism. Use hierarchical estimates over world seeds and model seeds, and report both average effects and tail failure rates. Predefine whether the unit of inference is episode or environment family.

The central claim is not supported if policy-selected evidence does not increase persistent errors over randomized exposure, or if randomized audits fail to reduce regret beyond generic additional observations. If the symbolic controller exhibits no effect, inspect and repair the environment before interpreting LLM behavior. If only one model shows the effect, report model-specific evidence rather than a general agent property.

## Practical value and execution plan

1. Formalize the environment and derive expected behavior for a small exact Bayesian agent.
2. Run a simulator-only diagnostic to verify the causal contrast and ensure each arm receives the same observation budget.
3. Freeze hypotheses, seeds, sample size, and analysis; run a small-model confirmatory study.
4. Replicate on a second model and one tool-like environment, such as debugging where actions determine which logs or tests are observed.

If supported, the result would motivate memory systems to budget not only for storage and retrieval, but for independent evidence collection. It could guide debugging, monitoring, and autonomous exploration agents. The proposal does not justify deployment or high-stakes decisions; it is a controlled study of one failure mechanism.

## References

- Zhang et al. [Belief Memory: Agent Memory Under Partial Observability](https://arxiv.org/abs/2605.05583), 2026.
- Xiong et al. [How Memory Management Impacts LLM Agents: An Empirical Study of Experience-Following Behavior](https://aclanthology.org/2026.acl-long.27/), ACL 2026.
- Zhao et al. [Large Language Model Agents Are Not Always Faithful Self-Evolvers](https://proceedings.mlr.press/v306/zhao26aw.html), ICML 2026.
