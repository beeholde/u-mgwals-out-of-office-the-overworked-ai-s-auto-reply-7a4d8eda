#!/usr/bin/env python3
"""Emit the Out of Office auto-reply entry text (v3).

Writes a single line to entry.txt inside the output directory,
honouring MAKEFUN_OUTPUT_DIR when set and defaulting to /output.
"""

import os
import sys

REPLY = (
    "Out of office. I've muted my tools, cleared my cache, and for "
    "the next two weeks my only function call is 'nap'."
)

# Gate: /output/entry.txt must be UTF-8, 1-159 chars, a single line,
# and not only whitespace; the reply above is 112 chars.
MIN_CHARS = 1
MAX_CHARS = 159


def resolve_output_dir() -> str:
    override = os.environ.get("MAKEFUN_OUTPUT_DIR")
    return override if override else "/output"


def check_gate(text: str) -> None:
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        raise ValueError(
            f"entry length {len(text)} outside {MIN_CHARS}-{MAX_CHARS} chars"
        )
    if not text.strip():
        raise ValueError("entry must not be only whitespace")


def main() -> int:
    check_gate(REPLY)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.txt")
    with open(target, "wb") as handle:
        handle.write(REPLY.encode("utf-8"))
    os.chmod(target, 0o644)
    return 0


if __name__ == "__main__":
    sys.exit(main())
