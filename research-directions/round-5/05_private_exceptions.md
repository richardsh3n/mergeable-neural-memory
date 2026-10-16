# Remember the Exception: Episodic Evidence against Strong Model Priors

**Research sketch — 16 October 2026.** Proposal only; no new experiment or external registration. Common rules: [README.md](README.md).

## Question and proposed contrast

When a trusted private episode records an unusual but valid local fact, does the assistant use it or fall back to the more plausible generic answer? This study keeps evidence truth and access fixed while varying how strongly the fact conflicts with the model's prior expectation.

[Taming Knowledge Conflicts](https://arxiv.org/abs/2503.10996) already studies contextual versus parametric knowledge. [Beyond Black-Box Interventions](https://arxiv.org/abs/2510.12460) studies latent conflict signals and faithful RAG. The proposed distinction is a persistent private-exception task with separate write, retrieval and answer tests. It is not a claim to discover knowledge conflict or to trust every retrieved sentence.

## Hypothesis and minimal experiment

Hypothesis: explicitly scoped episodic evidence reduces prior-driven substitution on unusual local facts more than generic retrieved prose, provided the source is legitimate and the scope is clear. The intervention may otherwise cause blind obedience to false context, which must be measured.

Construct a fictional environment with exact labels and randomized private mappings. Use a held-out baseline measurement to stratify generic answer preference before injecting episodes; do not call that measurement ground truth about internal beliefs. Match evidence length and provenance. Include plausible and unusual private facts, no-evidence cases, and clearly untrusted conflicting claims. Avoid presenting disputed real-world facts as true labels.

Compare full episodic text, summaries, retrieval, structured scoped facts and a candidate reader, using the same backbone. Oracle retrieval isolates answer integration; direct post-write tests isolate encoding loss. A no-memory model and a blindly context-following policy expose both sides of the tradeoff.

Primary endpoint: exact private-fact accuracy as a function of preregistered prior-preference strata. Report unsupported generic substitutions, untrusted-context compliance, unknown-case calibration, retention after distractors, and cost. Split by world and semantic template; balance rare answer labels to prevent answer-frequency shortcuts.

## Stop rule and value

Stop if oracle evidence removes the effect entirely, source-trust differences explain the result, or a simple scope prompt matches the method. The practical output is a component-level diagnostic for assistants remembering private exceptions, not a general policy that contextual memory should always override model knowledge. Unlike local correction, no fact is edited after writing.
