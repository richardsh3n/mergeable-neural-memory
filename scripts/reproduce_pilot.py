"""Reproduce the archived pilot into an exclusively created directory."""
import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from scripts.run_locked import verify
from src.merge_memory import run_pilot
from src.run_io import digest, reserve_output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    frozen = verify()
    out = reserve_output(args.out, ROOT)
    run_pilot(frozen["config"], out)
    evidence = {p.name: digest(p)
                for p in sorted(out.iterdir()) if p.is_file()}
    with (out / "artifact_hashes.json").open("x", encoding="utf-8") as handle:
        json.dump(evidence, handle, indent=2)
        handle.write("\n")


if __name__ == "__main__":
    main()
