"""Create a non-overwriting pre-run provenance manifest."""
import argparse
import hashlib
import json
import platform
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--client-date", required=True)
    args = parser.parse_args()
    target = ROOT / "results/freeze.json"
    if target.exists():
        raise SystemExit("Refusing to replace an existing pre-run freeze.")
    required = [ROOT / "configs/pilot.json", ROOT / "docs/PREREGISTRATION.md",
                ROOT / "src/merge_memory.py"]
    for path in required:
        if not path.exists():
            raise SystemExit(f"Missing protocol input: {path.name}")
    paths = sorted({p for folder in ("src", "tests", "configs", "scripts")
                    for p in (ROOT / folder).glob("*.py")}
                   | set((ROOT / "configs").glob("*.json"))
                   | {ROOT / "docs/PREREGISTRATION.md", ROOT / "requirements.lock.txt"})
    manifest = {
        "schema_version": 1,
        "status": "local_pre_run_freeze_not_external_registration",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "client_date": args.client_date,
        "platform": {"machine": platform.machine(), "python": platform.python_version()},
        "sha256": {str(p.relative_to(ROOT)): digest(p) for p in paths},
        "config": json.loads((ROOT / "configs/pilot.json").read_text()),
    }
    target.write_text(json.dumps(manifest, indent=2) + "\n")
    print(json.dumps({"manifest": str(target.relative_to(ROOT)),
                      "created_utc": manifest["created_utc"],
                      "files": len(paths)}, indent=2))


if __name__ == "__main__":
    main()
