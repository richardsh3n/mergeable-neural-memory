"""Non-overwriting research run output and file hashing."""
import hashlib


def digest(path):
    with path.open("rb") as handle:
        result = hashlib.sha256()
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            result.update(block)
        return result.hexdigest()


def reserve_output(destination, root):
    if destination.is_symlink():
        raise ValueError("Use a new output directory, not a symbolic link")
    output = destination.resolve()
    if output.is_relative_to((root / "results").resolve()):
        raise ValueError("Choose a fresh directory outside the archived results tree")
    # Exclusive directory creation reserves the output across concurrent runs.
    output.mkdir(parents=True, exist_ok=False)
    return output
