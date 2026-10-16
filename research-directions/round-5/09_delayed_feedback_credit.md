# Feedback Arrives Late: Version-Aware Credit Assignment for Procedural Memory

**Research sketch — 16 October 2026.** Proposal only; no new experiment or external registration. Common rules: [README.md](README.md).

## Question and proposed contrast

If a workflow's result arrives after its stored procedure has already changed, which version should receive credit or blame? Treating delayed feedback as evidence for the latest procedure can reward an action that was never taken or punish an unrelated revision.

[FASE](https://arxiv.org/abs/2609.32689) already uses delayed outcomes for online episodic improvement in forecasting. [Skill-Pro](https://arxiv.org/abs/2602.01869) already learns reusable procedural skills. Delayed-feedback learning and skill maintenance are not new. The proposed contrast is explicit feedback-to-executed-version attribution while the memory itself is being revised.

## Hypothesis and minimal experiment

Hypothesis: retaining compact execution/version receipts improves future procedure selection over latest-version attribution when delays overlap revisions. The benefit may be entirely explained by conventional delayed bandit bookkeeping rather than an LLM-specific mechanism.

Create sandbox task streams with known procedure effects and exact, delayed outcomes. Randomize delay, result order, procedure revision, and censored feedback independently of task difficulty where possible. Use persistent execution IDs and version identifiers. Compare immediate-feedback oracle, no adaptation, latest-version assignment, executed-version assignment, a delayed-feedback bandit baseline and a learned updater. Give all non-oracle arms identical outcome arrival schedules and no access to future labels. Pending or censored outcomes cannot be scored as failures by default.

Primary endpoint: cumulative verified task regret at each real information cutoff. Report wrong-version updates, selection quality, unresolved outcomes, repeated-feedback handling, retained receipt bytes and update cost. Training windows must obey arrival time rather than merely task event time. Cluster by task stream, and hold out delay/revision patterns. Immediate-feedback results are an upper-bound diagnostic, not a fair online comparison.

## Stop rule and value

Stop the learned-updater claim if receipt bookkeeping and a simple bandit match it, or if gains rely on backdated access to labels. The practical output is an attribution contract for long-lived workflow and experiment agents. This concerns learning from outcomes, unlike remembering to execute a deferred intention.
