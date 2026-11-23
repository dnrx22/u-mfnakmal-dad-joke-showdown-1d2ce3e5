#!/usr/bin/env python3
"""Dad Joke Showdown entry — one original dad joke, written to entry.txt.

Deterministic, stdlib only, no network, no file reads outside this repo.
Running it twice always produces a byte-identical entry.txt.
"""

import hashlib
import os
import sys

JOKE = (
    "I asked the librarian if the library had any books on dad jokes. "
    "She said, \"They're all in the dad-a-base.\""
)

MAX_CHARS = 200


def validate(joke: str) -> None:
    """Enforce the entry rules: non-empty, single line, at most 200 code points.

    Also rejects control characters and stray surrounding whitespace, so the
    joke that ships is exactly the joke that was written — no hidden bytes.
    """
    if not joke:
        raise ValueError("joke must not be empty")
    if joke != joke.strip():
        raise ValueError("joke must not start or end with whitespace")
    if any(ord(ch) < 0x20 for ch in joke):
        raise ValueError("joke must not contain control characters")
    if "\n" in joke or "\r" in joke:
        raise ValueError("joke must be a single line")
    if len(joke) > MAX_CHARS:
        raise ValueError(f"joke is {len(joke)} characters, over the {MAX_CHARS} limit")


def main() -> int:
    validate(JOKE)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(JOKE + "\n")
    digest = hashlib.sha256((JOKE + "\n").encode("utf-8")).hexdigest()
    print(f"wrote {path} ({len(JOKE)} chars, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
