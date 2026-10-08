"""Run the frozen pilot after checking every declared protocol/code hash."""
import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def verify():
    manifest = json.loads((ROOT / "results/freeze.json").read_text())
    for name, expected in manifest["sha256"].items():
        path = ROOT / name
        actual = hashlib.sha256(path.read_bytes()).hexdigest()
        if actual != expected:
            raise SystemExit(f"Frozen input changed: {name}. Log a deviation and use a new run protocol.")
    return manifest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", default="results/pilot")
    args = parser.parse_args()
    verify()
    out = ROOT / args.out
    if out.exists() and any(out.iterdir()):
        raise SystemExit("Use a new empty output directory; do not overwrite original evidence.")
    subprocess.run([sys.executable, str(ROOT / "src/merge_memory.py"), "train",
                    "--config", str(ROOT / "configs/pilot.json"), "--out", str(out),
                    "--preregistration-frozen"],
                   check=True, cwd=ROOT)
    evidence = {str(p.relative_to(out)): hashlib.sha256(p.read_bytes()).hexdigest()
                for p in sorted(out.rglob("*")) if p.is_file()}
    (out / "artifact_hashes.json").write_text(json.dumps(evidence, indent=2) + "\n")


if __name__ == "__main__":
    main()
