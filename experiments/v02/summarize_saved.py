"""Rebuild v0.2 aggregate metrics from the already-frozen prediction file."""
import gzip
import hashlib
import json
from pathlib import Path

import numpy as np

import run

HERE = Path(__file__).resolve().parent


def json_safe(value):
    if isinstance(value, np.generic):
        return value.item()
    raise TypeError(f"Not JSON serializable: {type(value).__name__}")


cfg = json.loads((HERE / "config.json").read_text())
with gzip.open(HERE / "predictions.jsonl.gz", "rt", encoding="utf-8") as f:
    rows = [json.loads(line) for line in f]
assert len(rows) == 486000

by_seed = {}
for seed in cfg["seeds"]:
    by_seed[seed] = []
    for arm in ("local", "future"):
        picked = [r for r in rows if r["seed"] == seed and r["arm"] == arm and
                  r["method"] == "union" and r["stratum"] == 2 and r["known"] and r["hops"] == 2]
        worlds = {}
        for row in picked:
            worlds.setdefault(row["world_id"], []).append(row["correct"])
        by_seed[seed].append(np.array([np.mean(worlds[k]) for k in sorted(worlds)]))

run.world_effects_by_seed = by_seed
summary = run.summarize(rows, cfg)
summary["config"] = cfg
summary["scope"] = "Synthetic mechanism diagnostic; no pretrained LLM or architectural novelty claim."
summary["prediction_rows"] = len(rows)
summary["prediction_file_sha256"] = hashlib.sha256((HERE / "predictions.jsonl.gz").read_bytes()).hexdigest()
summary["summary_method"] = "Post-hoc deterministic aggregation of frozen per-query predictions; no model training or inference rerun."
(HERE / "results.json").write_text(json.dumps(summary, indent=2, default=json_safe) + "\n")
print(json.dumps(summary["primary"], indent=2, default=json_safe))
