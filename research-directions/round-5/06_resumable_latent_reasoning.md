# Pause the Thought, Keep the Work: Resumable Latent Reasoning

**Research sketch — 16 October 2026.** Proposal only; no new experiment or external registration. Common rules: [README.md](README.md).

## Question and proposed contrast

Can an ongoing latent reasoning process be paused, stored compactly, and resumed without replaying all prior computation? This targets inference-time working state within one unfinished task. It differs from long-term factual memory, deferred tool intentions and migration between model hosts.

[Coconut](https://arxiv.org/abs/2412.06769v4) already reasons through continuous hidden states. [Recurrent-depth reasoning](https://arxiv.org/abs/2502.05171) already scales internal computation. Neither latent thought nor serial recurrent compute is new. The proposed contrast is a state-size versus restart-cost frontier under scheduled preemption.

## Hypothesis and minimal experiment

Hypothesis: a learned compact checkpoint can retain more useful continuation behavior per byte than a generic textual summary, but full exact-state serialization should remain the correctness reference. Simply pausing a complete process and restoring it is an implementation check, not a scientific contribution.

Use a small open recurrent/latent model on executable planning or constraint tasks. Interrupt at randomized valid inference boundaries, serialize the declared state, evict all other per-task state, then resume on the same frozen model and task. Compare restart, text thought summary, last-hidden-vector only, learned compact checkpoint, and full required-state preservation. A last vector may be insufficient if the model also needs its KV cache; count all cache tensors, positions, input context, RNG state and metadata. Any retained prompt or transcript is shared and charged to every arm.

Primary endpoint: verified solve rate at a fixed total compute budget including pre-interruption work, restart, encoding and decoding. Also report checkpoint bytes, restore latency, recomputed steps, repeated-preemption drift and answer agreement with uninterrupted execution. An exact restore should pass deterministic checks before compressed states are evaluated. Hold out task structures and interruption schedules.

## Stop rule and value

Stop if the compact method silently retains a full cache, wins only because replay compute is uncounted, or loses its frontier advantage against a short symbolic search-state representation. A small synthetic result would establish only resumable computation in that model/task, not a general persistent mind. The practical application is compute scheduling and resuming long-running inference on limited hardware.
