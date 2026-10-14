# Round 3 related-work boundary

**Targeted primary-source scan: 15 October 2026.** Scope records proximity and the proposed contrast, not proof of absence. See [SOURCES.json](SOURCES.json) for checked versions and reading depth.

| Work | Prior coverage | Required difference |
|---|---|---|
| [Model-upgrade portability study](https://arxiv.org/abs/2609.05339v1) | Migration failures in raw, retrieval, note, and graph memory | Test a writable bounded numerical state and continued updates, not generic upgrade compatibility. |
| [Frozen Memory Is Not Enough](https://arxiv.org/abs/2608.17050v3) | Cross-model frozen learned-memory extraction with an adapted reader | Manipulate post-migration writing and repeated migration; frozen reuse is a baseline. |
| [Memp](https://arxiv.org/abs/2508.06433v4) | Writable procedural memories and cross-model reuse | Do not claim writable or transferable memory broadly; isolate update-compatible numerical episodic state. |
| [MEMORYLLM](https://arxiv.org/abs/2402.04624v2) | Self-updatable latent memory | Self-update alone is established; jointly test model replacement and continued writes. |
| [GovMem](https://arxiv.org/abs/2607.02579v1) | Dependency-aware governance of correlated traces | Study posterior information surviving compressed writes/merges, not a renamed promotion gate. |
| [Sigma-Mem](https://arxiv.org/abs/2607.27958v1) | Peer reliability and relationship memory | Separate coordination policy from dependence-preserving belief compression. |
| [When Latent Agents Lie](https://arxiv.org/abs/2606.28958v1) | KV tampering and authenticated transport | Limit the new claim to accidental faults and selective recall; do not imply security guarantees. |
| [Sparse neural associative memory](https://arxiv.org/abs/1303.7032v2) | Error-correcting associative recall | Noise tolerance is old; test task-level selective reliability at equal total bytes. |
| [Reed–Solomon codes](https://epubs.siam.org/doi/10.1137/0108018) | Conventional code-based recovery | Include a strong standard recovery baseline, with protection overhead counted. |

## Search record and exclusions

Search terms combined agent/latent memory with model upgrade, cross-model transfer, writable state, evidence correlation, source dependence, state corruption, fault tolerance, and error correction. Searches also checked transactional/concurrent memory and multimodal identity memory; direct recent precedents made those broad themes poor candidates for an unqualified new contribution. No secondary summary is used as the sole support for a cited technical claim.

The scan inspected source abstracts, version histories, and selected full text for the frozen-memory-transfer, correlated-trace, and KV-integrity papers. It did not reproduce their systems or establish that every proposed contrast is absent from all appendices, code, submissions, or unpublished work. Before registering, extend citation chasing and inspect the nearest implementations. Before submission, refresh 2026–2027 work and pin the final source versions.

## Separation from earlier rounds

Portability evaluates state across hosts, not counterfactual inference. Dependence preservation evaluates exogenous evidence probabilities, not policy-driven self-confirmation or contributor deletion. Damage-aware recall evaluates unplanned faults, not chosen eviction or consent revocation. The state may be shared or merged, but those operations alone are not a new contribution.
