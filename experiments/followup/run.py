"""Run the bounded follow-up in a fresh directory with read-only archive inputs."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import gzip
import hashlib
import io
import json
from pathlib import Path
import platform

import numpy as np
import torch

from src.merge_memory import seed_everything
from src.run_io import digest, reserve_output
from .archived import continuation, load_fit, three_party
from .capacity import capacity

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def write_json(path, data):
    with path.open("x", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2, allow_nan=False)
        handle.write("\n")


def verify_archive(root=ROOT):
    manifests = (root / "results/freeze.json", root / "results/pilot/artifact_hashes.json")
    freeze, artifacts = [json.loads(path.read_text(encoding="utf-8")) for path in manifests]
    hashes = freeze["sha256"] | {f"results/pilot/{key}": value for key, value in artifacts.items()}
    checkpoints = [f"results/pilot/checkpoint-seed-{seed}.pt" for seed in freeze["config"]["training"]["seeds"]]
    if not all(name in hashes for name in checkpoints):
        raise ValueError("Archived checkpoint missing from artifact manifest")
    for name, expected in hashes.items():
        if digest(root / name) != expected:
            raise ValueError(f"Archived input hash mismatch: {name}")
    return freeze["config"], hashes | {str(path.relative_to(root)): digest(path) for path in manifests}


def run(config_path, destination):
    config_bytes = config_path.read_bytes()
    config = json.loads(config_bytes)
    if config["schema_version"] != 1:
        raise ValueError("Unsupported follow-up config schema")
    pilot, archived_hashes = verify_archive()
    if config["archive_seeds"] != pilot["training"]["seeds"]:
        raise ValueError("This protocol evaluates all archived fits in order")
    files = sorted(HERE.glob("*.py")) + [ROOT / "docs/followup/PROTOCOL.md", ROOT / "src/run_io.py"]
    provenance = {
        "scope": "local pre-run input record for an exploratory follow-up",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "config_sha256": hashlib.sha256(config_bytes).hexdigest(),
        "versions": {"python": platform.python_version(), "machine": platform.machine(),
                     "system": platform.system(), "numpy": np.__version__, "torch": torch.__version__},
        "input_hashes": archived_hashes | {str(p.relative_to(ROOT)): digest(p) for p in files},
    }
    output = reserve_output(destination, ROOT)
    with (output / "config.json").open("xb") as handle:
        handle.write(config_bytes)
    write_json(output / "inputs.json", provenance)
    config_fixed = json.loads((output / "config.json").read_bytes())
    seed_everything(0, config_fixed["threads"])
    fits = [(seed, load_fit(ROOT, seed)) for seed in config_fixed["archive_seeds"]]

    # Explicit gzip timestamp and empty header filename keep evidence contents
    # comparable across runs with different dates and directory names.
    with (output / "evidence.jsonl.gz").open("xb") as raw, \
            gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as compressed:
        with io.TextIOWrapper(compressed, encoding="utf-8", newline="\n") as handle:
            def emit(row):
                handle.write(json.dumps(row, separators=(",", ":"), allow_nan=False) + "\n")

            findings = {"continuation": continuation(fits, config_fixed["continuation"], emit)}
            print("Completed archived continuation diagnostic", flush=True)
            findings["three_party"] = three_party(fits, config_fixed["three_party"], emit)
            print("Completed archived three-party diagnostic", flush=True)
            findings["capacity"] = capacity(config_fixed["capacity"], pilot, config_fixed["threads"], output, emit)

    write_json(output / "results.json", findings)
    write_json(output / "artifact_hashes.json", {p.name: digest(p) for p in sorted(output.iterdir())})
    print(f"Complete: {output}", flush=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=HERE / "config.json")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    run(args.config, args.out)


if __name__ == "__main__":
    main()
