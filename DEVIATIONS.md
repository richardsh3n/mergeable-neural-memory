# Deviations and status

The protocol is a locally timestamped, pre-run plan, not an externally registered
preregistration. No inferential run may begin before the protocol/config/code
hash manifest is written. Development and shape/unit checks are allowed before
that freeze; outcome-dependent tuning must be disclosed here.

## Executed run

- Local pre-run freeze: **2026-10-08T16:32:32.407124+00:00**; this is 2026-10-09 in Asia/Shanghai. Client date: 2026-10-09. See `results/freeze.json`.
- Meaningful pre-run checks: **19 passed**. Development included shape, gradient and information-boundary checks; the schema test called evaluation on an untrained model. No training loop, fitted-model performance evaluation or outcome-dependent selection was run before this freeze.
- The frozen runner completed all scheduled optimization for seeds **11, 23, 37**, with final-step checkpoints and **396,000** prediction rows. Registered runtime: 137.736 seconds, descriptive only.
- No source/configuration/protocol/test/lock changes, training extensions, early-checkpoint selection, comparator replacements or endpoint changes occurred after freezing.
- Original run artifacts retain SHA-256 hashes in `results/pilot/artifact_hashes.json`; independent verification is in `results/audit.json`.
- H1 is unsupported: **−0.4737 percentage points**, conditional 95% CI **[−1.2296, +0.3211]**. This statement is not an equivalence claim.

## Reporting omission discovered after fitting

The generator rejects candidate worlds until private evidence is ambiguous for
each eligible joint query. The protocol asks for rejection counts, but the
executed source did **not retain attempt/rejection counters**. Accepted-world
and query counts are complete; the run ended normally without a generator
exhaustion exception. The number and distribution of rejected candidates are
unknown. They must not be reported as zero or inferred from the successful run.

This is a reporting omission. It limits analysis of acceptance bias and accepted
task difficulty. The independent audit verifies saved private-ambiguity counts
and coverage, but cannot reconstruct counters from the saved predictions. The
omission does not alter the saved primary labels or its reconstruction. A new
protocol should log accepted and rejected counts and rejection reasons. The
original run was not repaired, extended or repeated after this result.

The saved audit verifies recorded per-query ambiguity counts, not independently
recomputed ambiguity from each original evidence set. Raw facts and per-world
latent states were not retained in the archive. Frozen code and seeded streams
allow future regeneration; that end-to-end independent replication was not
performed. This is an artifact-audit boundary, not proof of independent model
replication. Fit-to-fit variability combines training and distinct test-world
streams; their separate contributions were not isolated.

## Post-result work

`scripts/audit_results.py` independently reimplements the already frozen primary
statistic and verifies saved evidence. `scripts/make_report.py` and
`scripts/build_manuscript.py` render descriptive tables, charts and the working
paper from original artifacts. These scripts were written after fitting began
or ended, so they are **not included in the original pre-run source hash set**.
They introduce no new confirmatory endpoint or training selection. Their final
hashes are recorded in the package manifest separately.

The proposal to study representations sufficient for future unions is a
post-result research decision, not a claim that the failed primary hypothesis
was fulfilled. Three-party semantics, within-party duplication, continued
updates, tight capacity, independent encoders and real LLM experiments remain
unperformed. The numerical one-row associativity probe is retained as disclosed
before fitting; no favorable diagnostic replaced it.
