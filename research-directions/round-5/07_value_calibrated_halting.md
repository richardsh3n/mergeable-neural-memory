# Is One More Thought Worth It? Value-Calibrated Halting for Latent Reasoning

**Research sketch — 16 October 2026.** Proposal only; no new experiment or external registration. Common rules: [README.md](README.md).

## Question and proposed contrast

Can a reasoning model estimate the marginal benefit of another internal iteration, rather than stop merely because its current answer is confident? Confidence in the current answer and expected improvement from further work are different quantities. A confident answer can be wrong, and an uncertain answer may not improve with more loops.

[Learning When to Stop](https://arxiv.org/abs/2511.21581) already optimizes adaptive latent reasoning length. [Adaptive Depth in Looped Transformers](https://arxiv.org/abs/2607.20519) already separates trajectory formation from stopping readout and finds strong simple confidence controls. This proposal is a narrow value-calibration study, not the invention of adaptive depth.

## Hypothesis and minimal experiment

Hypothesis: a marginal-improvement predictor trained on frozen trajectories can lower decision loss across changing compute prices better than confidence thresholds at the same underlying model competence. The predictor must beat simple post-hoc readouts and include its own cost.

Collect full trajectories only on training/calibration tasks with an exact answer verifier. At each depth, label whether specified extra loops improve, leave unchanged, or worsen the verified answer. Fit a small readout estimating expected improvement, with no answer labels available at test time. Freeze the reasoning model to separate trajectory learning from gate quality. Compare fixed depth, confidence, entropy, learned stopping, marginal-value stopping and an oracle gate. Evaluate fresh task families and unseen compute prices; the oracle sees future outcomes and is explicitly privileged.

Primary endpoint: verified answer loss plus a preregistered measured compute cost, also reported as an accuracy/latency frontier. Report expected-improvement calibration, early-stop mistakes, harmful extra computation, and gate overhead. Average loop count is insufficient when batching or hardware latency is nonlinear. Use paired tasks and exclude calibration tasks from the final comparison.

## Stop rule and value

Stop if confidence-only gates match the frontier, extra trajectory access leaks final labels, or the predictor costs more than it saves. The first deliverable is a stopping diagnostic and value predictor for one frozen model, with replication required. It concerns when to stop healthy computation, unlike pause/resume checkpoints or damage-aware factual recall.
