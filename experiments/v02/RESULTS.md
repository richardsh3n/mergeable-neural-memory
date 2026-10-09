# v0.2 writer-supervision diagnostic

## Finding

On the preregistered primary subset (known two-hop questions, 50% overlap), future-union supervision scored **79.8%**, versus **68.0%** after local-only adaptation. The paired difference was **+11.82 percentage points**; a 5,000-resample world bootstrap gave a conditional 95% interval of **[+10.36, +13.29] points** across the 444 held-out worlds with at least one eligible query.

The result does **not** pass the preregistered progress gate. Fit-level effects were +0.00, +9.01, and +26.46 points for inherited fits 11, 23, and 37. The future-supervised group also reached only 79.8% on the primary task, below the required 90%. Its score was essentially the unadapted inherited baseline (79.8% vs. 79.8%), while its private-local accuracy was 90.3% vs. 90.1% for the inherited baseline. The simplest supported interpretation is that local-only adaptation can erase an existing union skill in some fits, and the future-union loss helps preserve it. This experiment does not show that the writer learned a new capability or that the result generalizes to pretrained LLMs.

| Fit | Local-only | Future-union | Difference |
|---:|---:|---:|---:|
| 11 | 100.00% | 100.00% | 0.00 pp |
| 23 | 79.84% | 88.85% | +9.01 pp |
| 37 | 23.31% | 49.77% | +26.46 pp |
| Equal-fit mean | 67.72% | 79.54% | +11.82 pp |

The primary bootstrap resamples the same world identities and averages the three fit effects. It is conditional on these three inherited checkpoints; it is not an interval over a population of training seeds. Fit 11 is ceiling-saturated, while fit 37 is far below the 90% feasibility gate. Those differences are central results, not reasons to discard a fit.

One protocol deviation was found during audit: the preregistration specifies reseeding the data generator at every step, while the runner seeds once per fit and consumes one continuous stream. The two writer arms still received exactly matched streams, as verified by per-step hashes. This limits the result's confirmatory status; see [`DEVIATIONS.md`](DEVIATIONS.md).

## Registered checks

- The two arms used identical initial checkpoints, writer parameter sets, per-step world hashes, and attempt counts. Each fit saw 16,000 accepted training worlds; fit 37 required one rejected attempt, and the other fits required none.
- The three test strata each contain 500 accepted worlds and 2,000 query rows. The source sampler matched the frozen v0.1 sampler on the registered deterministic fixtures.
- The fixed state payload was 1,152 bytes. Reader and shared embeddings remained frozen. On every evaluation world, MAXSET of split states equaled full-union re-encoding; both three-party merge trees also matched.
- The archive contains all per-query class probabilities across nine evidence controls, plus the raw held-out evidence, local and union targets, required paths, generation counters, paired training hashes, and final writer weights.
- Probability rows normalized within 1e-5. Three-party, duplicate-delivery, swapped-source, private-label, unknown-answer, and full-reencode checks were recorded; these algebraic checks do not establish neural-memory novelty.

## Decision

**Do not scale this result directly to an LLM experiment.** The next useful step is a capacity and optimization diagnostic with fresh, separately preregistered fit seeds. It should test whether the two weak inherited fits can reach the minimum accuracy gate, whether local-only forgetting is robust across a wider fit sample, and whether future-union training still helps after controlling for ordinary adaptation/forgetting. If it cannot clear those gates, retain the result as a negative/diagnostic study rather than adding an LLM layer.

## Scope and execution record

This was a synthetic six-entity, two-relation, fixed two-hop task. There was no pretrained language model, natural-language memory, update conflict, or real user data. The protocol was frozen locally and was not externally preregistered. Execution issues are documented in `RUN_NOTES.md` and `DEVIATIONS.md`: one audit-control assembly error stopped the first invocation; the corrected run completed training and inference but stopped during summary serialization; and the per-step RNG reseeding rule was not implemented exactly as written. The saved predictions were summarized deterministically without repeating training or inference. `FREEZE.json`, `POSTHOC.json`, `training-audit.json`, and the retained logs provide the audit trail.
