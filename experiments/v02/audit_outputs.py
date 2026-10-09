"""Independent structural and provenance checks for the v0.2 archive."""
import gzip
import hashlib
import json
import math
from pathlib import Path

import torch

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
freeze = json.loads((HERE / "FREEZE.json").read_text())
for relative, expected in freeze["files"].items():
    actual = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
    assert actual == expected, f"Frozen input hash mismatch: {relative}"

with gzip.open(HERE / "heldout-corpus.json.gz", "rt", encoding="utf-8") as f:
    heldout = json.load(f)
assert len(heldout) == 6000
worlds = {}
for row in heldout:
    worlds.setdefault((row["stratum"], row["world_id"]), []).append(row)
assert len(worlds) == 1500 and all(len(rows) == 4 for rows in worlds.values())
for rows in worlds.values():
    assert sum(row["query"][2] < 0 for row in rows) == 2
    assert sum(row["query"][2] >= 0 for row in rows) == 2

audit = json.loads((HERE / "training-audit.json").read_text())
for seed in (11, 23, 37):
    assert audit["step_hashes"][f"{seed}-local"] == audit["step_hashes"][f"{seed}-future"]
    assert audit["attempt_counts"][f"{seed}-local"] == audit["attempt_counts"][f"{seed}-future"]

allowed_changed = ("event_key.", "event_value.", "slot_keys")
for seed in (11, 23, 37):
    original = torch.load(ROOT / f"results/pilot/checkpoint-seed-{seed}.pt",
                          map_location="cpu", weights_only=True)["model"]
    for arm in ("local", "future"):
        saved = torch.load(HERE / f"writer-{arm}-seed-{seed}.pt",
                           map_location="cpu", weights_only=True)
        assert saved["state_bytes"] == 1152
        for name, value in saved["model"].items():
            if not (name == "slot_keys" or name.startswith(allowed_changed[:2])):
                assert torch.equal(original[name], value), f"Unexpected changed parameter: {seed}/{arm}/{name}"

count = 0
with gzip.open(HERE / "predictions.jsonl.gz", "rt", encoding="utf-8") as f:
    for line in f:
        row = json.loads(line)
        probs = row["probabilities"]
        assert len(probs) == 7 and all(math.isfinite(p) and p >= 0 for p in probs)
        assert abs(sum(probs) - 1.0) <= 1e-5
        count += 1
assert count == 486000

results = json.loads((HERE / "results.json").read_text())
assert results["prediction_rows"] == count
assert results["primary"]["world_count"] == 444
assert results["primary"]["progress_gate_passed"] is False
assert results["primary"]["supported"] is True

print(json.dumps({"freeze_hashes": len(freeze["files"]), "heldout_queries": len(heldout),
                  "heldout_worlds": len(worlds), "paired_fits": 3,
                  "prediction_rows": count, "probability_rows_normalized": True,
                  "state_bytes": 1152, "primary_interval_positive": True,
                  "progress_gate_passed": False}, indent=2))
