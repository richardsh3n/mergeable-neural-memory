# Remember Success without Repeating It: Exposure Timing for Discovery Agents

**Research sketch — 16 October 2026.** Proposal only; no new experiment or external registration. Common rules: [README.md](README.md).

## Question and proposed contrast

Can delaying exposure to successful precedent preserve exploration while still allowing later reuse? Prior memories can be entirely correct and the environment stationary; the failure of interest is premature convergence on one solution family, not false beliefs or selectively observed evidence.

[Demystify the Role of Memory in MLE Agents](https://aclanthology.org/2026.findings-acl.525/) already finds a stability/diversity tradeoff. [Controllable Memory Usage](https://aclanthology.org/2026.acl-long.670/) already studies anchoring and control of memory reliance. The proposed question is a narrow intervention on when precedent is revealed during a fixed-budget discovery process, rather than a new claim that memory can suppress creativity.

## Hypothesis and minimal experiment

Hypothesis: a short independent exploration phase followed by retrieval can improve best verified solution quality over immediate retrieval, at the same total search cost, when the task admits several solution families. It may hurt easy tasks where precedent is already optimal.

Use sandbox program-search or algorithm-design tasks with deterministic execution scores and multiple valid approaches. Provide the same verified precedent library. Randomize immediate retrieval, delayed retrieval, no retrieval, repeated reminders, and an adaptive reveal policy. Match generation, evaluation and retrieval costs; delayed arms do not receive extra attempts. Include both strong precedents and merely adequate precedents. Hold tasks stationary and feedback exact.

Primary endpoint: best verified solution utility at the fixed budget. Report solution-family coverage using preregistered behavioral equivalence tests, success rate, time to first success, novelty relative to supplied precedents, and token/tool costs. Textual variety is not meaningful algorithmic novelty. Blind human review can supplement execution scores but cannot replace correctness checks. Split by task family and precedent source.

## Stop rule and value

Stop if diversity increases without useful verified solutions, if gains disappear after matching attempts, or if one fixed prompting control matches the adaptive policy. This would inform research and coding agents deciding when to consult experience. It differs from the earlier self-confirming-loop proposal because neither source correctness nor the evidence-sampling process changes; the manipulated variable is exposure timing during search.
