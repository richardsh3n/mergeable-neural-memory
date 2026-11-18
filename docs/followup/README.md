# Follow-up research

- [Experimental report](REPORT.md)
- [Technical architecture and audit](ARCHITECTURE.md)
- [Next research decision](NEXT_STEPS.md)
- [研究负责人中文说明](BRIEF.zh-CN.md)
- [Bounded run protocol](PROTOCOL.md)
- [Machine-readable report and evidence](../../experiments/followup/evidence)

The historical phase-one manuscript and archive remain intact. The
follow-up uses frozen fits for the encoder and delivery diagnostics and new
small CPU fits for the capacity and ablation matrix.

From a checkout with the archived artifacts present:

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.lock.txt
python -m pytest -q

python scripts/audit_followup.py experiments/followup/evidence
VECLIB_MAXIMUM_THREADS=1 OPENBLAS_NUM_THREADS=1 \
  python -m experiments.followup.run --out ../followup-run-001
python scripts/audit_followup.py ../followup-run-001 --require-checkpoints
```

The first audit uses shipped evidence. The second additionally verifies the
12 generated checkpoint files. Both reconstruct all saved accuracy cells
without rerunning model inference. A full experiment rerun creates its
output exclusively and cannot use the archived `results/` tree. For a
separate reproduction of v0.1, the safer entry point is
`python scripts/reproduce_pilot.py --out ../pilot-reproduction-001`.
