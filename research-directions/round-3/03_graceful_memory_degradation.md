# Memory That Knows It Is Damaged: Selective Recall after State Erasure and Corruption

**Working proposal, 15 October 2026.** No study has been run or externally registered. The tested fault model is accidental damage, not an adversarial security guarantee.

## Abstract

A compact numerical memory can be partially erased or corrupted during storage and transfer. Detecting that an object changed is useful, but rejecting the entire memory discards unaffected knowledge. This proposal asks whether an agent can retain useful selective recall while abstaining on queries whose evidence has become unreliable. It compares learned redundancy and localized states against strong conventional error-correcting and chunk-checksum baselines under equal total serialized bytes. The goal is a risk–coverage advantage beyond whole-state rejection, especially when damage exceeds exact-recovery capacity. Classical associative memory already studies noisy recall; modern latent-agent work already studies hidden-state integrity. The intended contribution is a fault-specific selective-recall evaluation and, only if supported, a representation that degrades usefully without manufacturing confidence.

## Question and threat boundary

Can a bounded memory answer queries supported by retained information while recognizing that other queries are no longer reliable after partial state damage?

Study two distinct channels: known-location erasure of serialized chunks, and unknown-location bit corruption. Quantization is a third, separate control channel with a declared codec; it is not treated as interchangeable with damage. Do not infer physical hardware reliability from synthetic fault rates. Damage is applied after the state is formed, using a seeded channel independent of the answers. No malicious writer, adaptive adversary, or forged valid snapshot is in the claim.

Checksums detect specified changes but do not reconstruct content. Conventional error-correcting codes can recover bytes within their operating limits. A neural reconstruction that produces plausible answers is not proof that the original information survived. Ground-truth task answers and calibrated refusal therefore matter more than latent reconstruction distance.

## Prior work and distinct scope

Error-correcting associative memory has a long history, including sparse neural-network memory. Reed–Solomon codes provide a conventional recovery baseline. Brito and Baquero study KV-cache tampering and authenticated transport for latent collaboration. These precedents rule out claims that noise-tolerant memory or latent-state integrity is new.

The proposed target is **selective reliable use of a damaged persistent state**, with all protection bytes counted and strong local recovery/rejection controls. It is distinct from shared-memory revocation: erasures are random faults, not a person's removal request. It also differs from utility-based forgetting: the missing information is unplanned, and the task is to recognize the resulting uncertainty.

## Hypotheses and candidate mechanism

H1: a localized or redundancy-aware state can retain higher answer coverage at a fixed allowable error risk than a dense state with a whole-state rejection policy.

H2: localized checksums plus conventional coding will be strong baselines and may outperform learned redundancy for recoverable damage.

H3: any selective-recall advantage will depend on the channel and on which queries share state components; robustness to one fault type will not imply robustness to others.

A candidate couples a modular memory with query-specific reliability estimates informed by a damage mask or detector. Evaluate both learned redundancy and standard coding over identical clean-state bytes. All masks, parity bytes, checksums, scale parameters, indexes, and model-specific metadata are included in the retained-state budget. Detection quality and recall quality are measured separately; exact fault locations are shared across arms only in the known-erasure condition.

## Controlled study

Use synthetic episodic worlds with exact fact labels, multi-hop queries, and unknown answers. Assign fact dependencies to an evaluator-only graph so affected and unaffected queries can be stratified. The model never receives the oracle dependency labels. Fit clean memories first, then damage their actual serialized form. Handle non-finite float values with a fixed policy and report failures; do not silently exclude difficult faults.

Compare: dense state without protection; whole-state checksum plus refusal; chunked state with per-chunk checksums and refusal; Reed–Solomon protection; simple replicated chunks; learned redundant state; and localized state with calibrated reliability. Include a compact symbolic record store with the same protection budget. A clean-state reference sets the attainable competence level. Match total bytes and report latency and parameter overhead. Code implementation and declared correction capacity must be checked against known recoverable and uncorrectable examples before neural comparisons.

Primary outcome: answer coverage at a preregistered maximum empirical error risk, with held-out calibration and uncertainty intervals. Also publish risk–coverage curves, false-confident errors, unaffected-query utility, affected-query abstention, clean accuracy, NaN/crash rates, decoding latency and bytes. Refusing every query has zero error but zero coverage and does not pass. Select a minimum useful clean accuracy and coverage floor before confirmation. Query strata are diagnostic; they cannot replace the predeclared primary comparison.

Split clean world seeds and fault seeds independently. Freeze the fault rates and channels, with a separate unfamiliar fault-pattern holdout. Estimate uncertainty by world, since multiple queries share a damaged state. A pilot sets sample size and calibration thresholds and is excluded from the confirmatory run. Report results separately below and beyond conventional exact-correction capacity.

## Stop criteria and practical value

Stop the learned-redundancy claim if conventional coding or chunked symbolic storage dominates the cost–risk frontier, if clean accuracy is sacrificed substantially, or if reliability estimates fail on unseen fault patterns. Do not call reduced average error a guarantee of safe use. If no meaningful coverage survives at the required risk, complete rejection or exact recovery remains the appropriate operational strategy.

Deliver a byte-level fault injector, serialization specification, conventional recovery controls, and a frozen selective-recall benchmark before testing LLM hosts. This could inform local assistants, intermittent state synchronization, and resource-limited devices. It does not justify replacing authentication, backups, or hardware error correction.

## Primary references

- Brito and Baquero. [When Latent Agents Lie: KV-Cache Integrity in Multi-Agent LLM Collaboration](https://arxiv.org/abs/2606.28958v1), 2026.
- Yao, Gripon, and Rabbat. [A Massively Parallel Associative Memory Based on Sparse Neural Networks](https://arxiv.org/abs/1303.7032v2), 2013.
- Reed and Solomon. [Polynomial Codes Over Certain Finite Fields](https://epubs.siam.org/doi/10.1137/0108018), 1960.
