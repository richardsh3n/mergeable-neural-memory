# Long-Lived Memory Needs Contracts: Migration, Evidence Dependence, and Damage

**Research agenda — 15 October 2026.** Proposal drafts only; no new experimental results.

## Abstract

Persistent memory is useful only if its meaning survives operations performed over its lifetime. This agenda proposes three operational contracts for bounded memory: update-compatible migration across model hosts; calibrated evidence accumulation despite repeated or dependent reports; and selective reliable recall after accidental state damage. These questions have direct predecessors in model portability, correlated-trace governance, associative memory, and error-correcting codes. Their proposed contribution is therefore a constrained evaluation of what remains usable after transformations, with conventional symbolic and coding baselines that can falsify a neural advantage. Each program can be run independently, beginning with executable synthetic truth before LLM-scale experiments.

## Three contracts

### 1. Meaning after migration

Memory Beyond Its Host asks whether a target host can continue writing to a migrated state. Migration and update should approximately commute in answer space, and their agreement must be checked against truth. Frozen-reader adaptation is a strong baseline, but a single successful read cannot establish long-term writable interoperability. Repeated migrations, corrections, and queries about facts written under each host provide the operational test. Canonical symbolic stores and history-based recovery prevent a representation-only experiment from being mistaken for a new practical architecture.

Full design: [writable state portability](01_writable_state_portability.md).

### 2. Confidence after evidence fusion

Repetition Is Not Evidence asks whether compressed memory preserves the difference between independent reports and copies. The experiment should use a known generative model and exact posterior reference, disclose which lineage information is available, and count all retained dependence metadata. Identical visible content without lineage cannot identify different hidden source structures. The proposed study tests compression and fusion quality when some dependency evidence is available; it cannot bypass that information limit.

Full design: [dependency-preserving memory](02_dependency_preserving_memory.md).

### 3. Reliability after damage

Memory That Knows It Is Damaged asks whether useful recall can survive partial faults while uncertainty expands appropriately. Accuracy alone is insufficient: confident guesses and total refusal can both distort conclusions. Match total protection bytes and compare coverage at a fixed error-risk target with checksums, local refusal, replicated records, and conventional coding. Known erasure, unknown corruption, and quantization are distinct channels and need separate claims.

Full design: [graceful memory degradation](03_graceful_memory_degradation.md).

## Why these are separate from the first six topics

The original round studies counterfactual sufficiency, eviction value, and contributor revocation. The second studies deferred action, endogenous evidence selection, and active evidence acquisition. The third changes neither the decision objective nor the evidence stream to create its main contrasts: it changes the model host, retained evidence-dependence structure, or physical state integrity. There is overlap at the representation level, which is disclosed; the endpoints and manipulated variables are distinct. See the [nine-topic index](../INDEX.zh-CN.md).

## Shared execution rules

Specify the entire retained state and its information access before fitting. Count metadata, indexes, source labels, adapters, and protection separately rather than hiding them. Use exact symbolic truth to test generators and graders; a language-model judge cannot be the only validity check. Pilot data may set thresholds and sample size but cannot be recycled as confirmatory evidence. Freeze seeds, protocols, calibration data, budgets, and analysis before final evaluation. Pair comparisons by world and preserve all fitted seeds and failure logs.

A neural candidate must beat or offer a defensible tradeoff against the strongest applicable conventional representation. Agreement between models, recovery of a plausible vector, or increased confidence is not itself success. If the simple baseline wins, the program still yields a useful conclusion about which contract should be implemented with conventional state.

## Priority and scope

Writable portability has the strongest architectural connection to persistent cognitive state and model replacement. Dependence preservation offers the cleanest initial probabilistic diagnostic. Damage-aware recall offers a useful systems benchmark, but its architecture claim is conditional on surviving conventional coding baselines. None warrants immediate expensive training before its small, falsifiable task is validated.

The targeted scan checked current primary entries and selected full-text sections. It is not a systematic novelty audit or reproducibility review. Source versions are recorded in [SOURCES.json](SOURCES.json); current titles can change, as the cross-model Engram paper did. Do not describe any of these drafts as accepted, validated, or a demonstrated replacement for Transformer memory. Existing project pilot results remain separate evidence.
