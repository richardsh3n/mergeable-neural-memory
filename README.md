# Mergeable Neural Memory

A controlled synthetic pilot asking whether two fixed-size learned memory states can be combined to answer relational questions that neither party can resolve alone, including when their evidence overlaps.

This package contains a small PyTorch neural model, an executable protocol, literature and theory audits, and reproducibility checks. **It is not a pretrained LLM experiment, a validated human-memory model, or an established novel architecture.** The intended retained state is a numerical tensor; its merger and reader do not receive event histories or a fact-table solver at inference.

## Status

This is a local research archive and exploratory pilot. The protocol is locally frozen with file hashes; it is not registration with an external registry, peer review, or a publication. No public release or submission is implied by this package.

**The locked pilot is complete, and its primary superiority hypothesis is unsupported.** At overlap 0.50, the candidate's known two-hop world-macro accuracy is **78.85%**, versus **79.33%** for MAXSET. The paired effect is **−0.47 percentage points**, conditional 95% world-bootstrap interval **[−1.23, +0.32]**. All three final fits are retained; their variability is substantial. This is not evidence of equivalence or a successful new LLM architecture.

The archive contains **396,000 prediction rows**, three final checkpoints, source and a self-contained [English working paper](paper/manuscript.tex). Independent reconstruction passes **173 audit assertions**, with one disclosed reporting omission: generator rejection-attempt counts were not saved. Begin with the [Chinese opening brief](docs/OPENING_BRIEF.zh-CN.md), [full result report](docs/PILOT_REPORT.md), and [audit evidence](results/audit.json). The reporting boundaries are in [CLAIMS.md](CLAIMS.md), and amendments belong in [DEVIATIONS.md](DEVIATIONS.md).

## What is being tested

Each synthetic world has six entities and two directed functional relations. Relation targets are sampled independently, rather than as bijections. Entity names are randomly permuted in every world. Evidence is split between A and B, with overlapping distractors and exclusive facts needed for two-hop questions.

Evaluation uses four distinct queries sharing the same world and evidence: two one-hop and two two-hop queries. For a known two-hop query, an evaluator-only oracle checks that each private party admits at least two possible answers. The neural model never receives that oracle. Missing required evidence produces a dedicated unknown-answer label. A 0.20 per-query deletion opportunity is not a guarantee that exactly 20% of labels are unknown.

The learned encoder maps local event tensors into 12 slots of 24 float32 coordinates. The reader makes two learned attention reads, using its own predicted intermediate distribution for the second read. A merged output retains **288 floats, or 1,152 payload bytes**, with no per-world auxiliary metadata. Two-party merging still needs both input states, the output, model parameters, and temporary computation; the payload bound is not a peak-memory claim.

The candidate merger adds a learned symmetric residual to `A + B`, using `[A+B, abs(A-B), A*B]`. It guarantees input commutativity and an empty-state identity. Associativity and idempotence are measured diagnostics, not guarantees. Neither this residual network nor DeepSets is presented as a novel structure.

| Method | Input representation and operation |
|---|---|
| Learned candidate | Sum-pooled local states; symmetric residual merger |
| DeepSets | Same sum-pooled states; trained `rho(phi(A) + phi(B))` |
| SUM / MEAN | Addition / arithmetic mean of sum-pooled local states |
| MAXSET (`max` in machine-readable outputs) | Max-pooled versions of the same learned event features, followed by coordinatewise max |
| A-only / B-only / zero | Required evidence-dependence controls |
| Swapped B | Candidate receives another world's B state; original query and label remain, and donor IDs are saved |
| Full re-encoding references | Re-encode deduplicated combined raw evidence using sum or max pooling; these have privileged history access |

Every method uses the same fitted encoder weights and frozen reader. MAXSET changes the pooling rule; it is not max applied to the candidate's sum states. The full re-encoding references are not state-only competitors or guaranteed accuracy upper bounds. Under disjoint evidence, additive re-encoding equality is a sanity check rather than a substantive discovery.

## Registered budget and analysis

[configs/pilot.json](configs/pilot.json) and [docs/PREREGISTRATION.md](docs/PREREGISTRATION.md) define the run. Frozen numerical settings take precedence over this overview.

| Setting | Registered value |
|---|---|
| Training seeds | 11, 23, 37 |
| Execution | CPU, one thread, deterministic settings |
| Shared encoder/reader | 1,500 steps per seed; batch 64; AdamW learning rate 0.003, weight decay 0.0001 |
| Shared training modes | Equal cycle of full-union sum, split SUM, split MEAN, and split MAXSET |
| Candidate merger | 1,000 steps per seed; frozen encoder/reader; batch 64; learning rate 0.002 |
| DeepSets merger | Same 1,000-step budget, frozen backbone, batch stream, and supervision as candidate |
| Objective | Final-answer CE + 0.30 first-hop CE; each trained merger additionally receives 0.10 relative state MSE against full-union sum encoding |
| Algebraic regularization | None; idempotence-loss weight is zero |
| Parameters | Shared encoder/reader 25,623; candidate merger 6,232; DeepSets merger 6,320 |
| Checkpoint selection | Final configured step only; no outcome-driven selection or training extension |
| Evaluation | 1,000 worlds per fit at overlap 0.00, 0.25, and 0.50; four queries per world |
| Evaluation seeds | Training seed + 100003 + 10000 × condition index; independent streams per fitted model |
| Planned total evaluation | 9,000 worlds, 36,000 query instances, and 396,000 prediction rows across 11 methods |

Stage 1 samples one query per training world, with two-hop probability 0.70, distractor overlap probability 0.30, and missing-path probability 0.20. Evaluation instead shares four queries per world. Gold intermediate labels and full-union state targets are privileged training supervision, not inference inputs.

The one primary comparison is **candidate minus MAXSET on known two-hop queries at overlap 0.50**. Average eligible query correctness within each world, then average worlds within each fit, then average the three fitted-model effects equally. A paired world bootstrap uses 5,000 resamples and RNG seed 20261008. Its percentile interval is conditional on these three fitted models; it does not estimate variability over a population of training seeds. H1 is supported only if the interval's lower bound is strictly above zero. All methods, seeds, strata, exclusions, and negative results must still be reported.

## Reproduce

Run these commands from the project directory. A Python virtual environment keeps dependencies separate from other projects. The lock file records the installed versions used for the archived run; wheel availability can depend on Python version and platform.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.lock.txt
python -m pytest -q
```

For an archive containing `results/freeze.json`, preserve that original manifest. The locked runner verifies every declared input hash, refuses a nonempty destination, and writes hashes for the new run's artifacts:

```bash
python scripts/run_locked.py --out results/reproduction-001
```

If starting a new, unfrozen protocol, finalize the source, configuration, dependency lock, tests, and preregistration first. Create the results directory, then replace `YYYY-MM-DD` with the actual client-provided date. The freeze script records its actual UTC execution timestamp separately.

```bash
mkdir -p results
python scripts/freeze.py --client-date YYYY-MM-DD
python scripts/run_locked.py --out results/pilot
```

Do not regenerate an existing freeze, overwrite original evidence, or alter hashed files to bypass verification. A post-freeze repair requires an amendment and a new protocol/run. The lower-level training command has an explicit freeze affirmation, but the hash-checking wrapper is the reproducibility entry point.

The runner produces final checkpoints for each seed, `metrics.json`, `training-trace.json`, `predictions.csv.gz`, and `artifact_hashes.json`. Predictions include world/query IDs, methods, labels, predicted answers, probabilities, and swapped-B donor IDs.

## File map

| Path | Purpose |
|---|---|
| `src/merge_memory.py` | Generator, learned encoder/reader, mergers, evaluation, bootstrap, and training entry point |
| `src/theory.py` | Small executable examples supporting the stated algebraic constraints |
| `configs/pilot.json` | Exact numerical run settings |
| `tests/test_memory.py` | Information boundaries, ambiguity checks, invariants, gradient paths, and analysis/schema checks |
| `tests/test_theory.py` | Checks for the executable theory examples |
| `scripts/freeze.py` | Non-overwriting pre-run hash manifest |
| `scripts/run_locked.py` | Hash verification, locked execution, and output hashes |
| `scripts/audit_results.py` | Independent reconstruction of saved statistics and artifact checks |
| `scripts/make_report.py` / `scripts/build_manuscript.py` | Descriptive figures/report and self-contained English manuscript |
| `scripts/package.py` | Non-overwriting complete archive snapshot with content verification |
| `requirements.txt` / `requirements.lock.txt` | Dependency ranges / recorded installed versions |
| `docs/PREREGISTRATION.md` | Frozen question, training, evaluation, decision rule, and reporting requirements |
| `docs/PROTOCOL_REVIEW.md` | Protocol risks and controls |
| `docs/THEORY.md` | Mergeability constraints and their limits; no originality claim for standard algebra |
| `docs/LITERATURE_AUDIT.md` | Closest related work and overlap risks |
| `docs/NEXT_STAGE.md` | Follow-up work beyond this pilot |
| `CLAIMS.md` / `DEVIATIONS.md` | Claim ledger / protocol amendments |
| `results/freeze.json` | Original local freeze, including timestamps and input hashes |
| `results/pilot/` | Locked-run artifacts once generated and checked |
| `results/audit.json` | 173-assertion independent artifact audit, including its boundaries and warnings |
| `docs/PILOT_REPORT.md` / `docs/OPENING_BRIEF.zh-CN.md` | Actual results / Chinese direction and decision |
| `paper/manuscript.tex` / `figures/` | Standalone working paper / exportable standard plots |

## Limits

- The shared entity alphabet is tiny; two-hop depth and relation types are fixed. Fresh worlds do not establish generalization to new vocabularies, arbitrary graphs, or natural language.
- An explicit table can represent this tiny task in substantially less memory. Equal neural-state bytes do not demonstrate useful compression or optimal capacity.
- The learned mergers receive extra parameters and optimization beyond SUM, MEAN, and MAXSET. DeepSets controls for an additional trained symmetric merger; total training budgets remain unequal against arithmetic baselines.
- Duplicate identity is exact event-tuple equality. Semantic aliases, source trust, conflicting reports, and independent repeated observations are not tested.
- Revision tags are reserved; all registered evidence has revision zero. Continual updates, exact forgetting, and corrections are follow-up work.
- Numerical associativity probes include states from different worlds and sometimes repeated states. They do not establish useful same-world three-party integration. Within-party duplication robustness is also unperformed follow-up work.
- Independently trained incompatible encoders, communication failures, and LLM-scale deployment are not covered. No end-to-end speed, energy, or storage-efficiency claim is made.

## Audit and render the archived evidence

These commands reconstruct the already defined primary statistic and render descriptive outputs; they do not train or choose a model. The manuscript is standalone and opens in the Codex LaTeX editor with a PDF preview.

```bash
python scripts/audit_results.py --out results/audit-reproduction-001.json
python scripts/make_report.py
python scripts/build_manuscript.py
```

The [result report](docs/PILOT_REPORT.md) preserves all methods and overlap conditions, eligible counts, realized labels, calibration, algebraic defects and resource accounting. Figures are available as PNG, SVG and PDF in `figures/`. The original protocol remains unchanged. Rendering and independent-audit scripts were added after fitting; this is disclosed in [DEVIATIONS.md](DEVIATIONS.md).

The scientific decision is to **stop scale-up of this residual merger on a superiority claim**, preserve the negative result, and design a new representation-sufficiency study. The next protocol must distinguish encoder/reader instability from merge failure and impose a meaningful capacity bottleneck before claiming compression. Natural-language and LLM experiments remain future work.
