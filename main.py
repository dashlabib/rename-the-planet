#!/usr/bin/env python3
"""Rename the Planet — make.fun entry.

Writes one funny new name for a planet of our solar system, with the why
in the same line, to /output/entry.txt (and prints it to stdout).
Deterministic: stdlib only, no input, no randomness, no network.
"""

import os
import sys

LINE = (
    "Venus is now 'The Contrarian' because its day is longer than "
    "its year and it spins backwards purely out of spite."
)


def candidate_paths():
    """Ordered output candidates: /output, then $MAKEFUN_OUTPUT_DIR, then local."""
    paths = ["/output/entry.txt"]
    env_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env_dir:
        paths.append(os.path.join(env_dir, "entry.txt"))
    paths.append(os.path.join("output", "entry.txt"))
    return paths


def write_entry(data: bytes) -> str:
    """Write to the first candidate that accepts the write; return its path."""
    errors = []
    for path in candidate_paths():
        try:
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "wb") as f:
                f.write(data)
            return path
        except OSError as exc:
            errors.append(f"{path}: {exc}")
    print("could not write entry to any output dir:\n" + "\n".join(errors),
          file=sys.stderr)
    raise SystemExit(1)


def main() -> int:
    if not 1 <= len(LINE) <= 200:
        print(f"entry line is {len(LINE)} chars, must be 1-200", file=sys.stderr)
        return 1
    if LINE.strip() != LINE or not LINE.strip():
        print("entry line must not be only whitespace", file=sys.stderr)
        return 1

    data = LINE.encode("utf-8")
    path = write_entry(data)

    # Read-back verification: file bytes must decode to the entry exactly.
    with open(path, "rb") as f:
        written = f.read()
    if written != data or written.decode("utf-8") != LINE:
        print("read-back mismatch: file bytes differ from entry", file=sys.stderr)
        return 1

    sys.stdout.buffer.write(data)
    sys.stdout.buffer.flush()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
