"""Snapshot all reviewable research evidence, including final checkpoints."""
import hashlib
import json
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKIP = {".git", ".pytest_cache", "__pycache__", ".venv", ".DS_Store"}


def files():
    return sorted(p for p in ROOT.rglob("*") if p.is_file()
                  and not any(part in SKIP for part in p.relative_to(ROOT).parts)
                  and p.name != "package_manifest.json")


def main():
    archive = ROOT.parent / "mergeable-neural-memory-pilot-2026-10-09.zip"
    manifest = ROOT / "results/package_manifest.json"
    if archive.exists() or manifest.exists():
        raise SystemExit("Refusing to replace an existing research snapshot.")
    paths = files()
    hashes = {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    manifest.write_text(json.dumps({"created_utc": datetime.now(timezone.utc).isoformat(),
                                    "scope": "post-run package snapshot, distinct from pre-run freeze",
                                    "sha256": hashes}, indent=2) + "\n")
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=6) as handle:
        for path in paths + [manifest]:
            handle.write(path, str(Path(ROOT.name) / path.relative_to(ROOT)))
    with zipfile.ZipFile(archive) as handle:
        damaged = handle.testzip()
        if damaged is not None:
            raise RuntimeError(f"Archive CRC failed: {damaged}")
        for name, expected in hashes.items():
            actual = hashlib.sha256(handle.read(str(Path(ROOT.name) / name))).hexdigest()
            if actual != expected:
                raise RuntimeError(f"Archive content mismatch: {name}")
    print(json.dumps({"archive": str(archive), "files": len(paths)+1,
                      "bytes": archive.stat().st_size,
                      "sha256": hashlib.sha256(archive.read_bytes()).hexdigest()}, indent=2))


if __name__ == "__main__":
    main()
