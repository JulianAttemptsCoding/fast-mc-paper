"""Apply a list of exact, single-occurrence replacements to main.tex.

Usage: python apply_edits.py edits_NN.json
Each entry is [old, new]; an entry whose old text does not occur exactly once
stops the run before anything is written.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> None:
    edits = json.loads((HERE / sys.argv[1]).read_text(encoding="utf-8"))
    path = HERE / "main.tex"
    text = path.read_text(encoding="utf-8")
    for index, (old, new) in enumerate(edits):
        count = text.count(old)
        if count != 1:
            raise SystemExit(f"edit {index}: expected one occurrence, found {count}: {old[:70]!r}")
        text = text.replace(old, new)
    path.write_text(text, encoding="utf-8")
    print(f"applied {len(edits)} edits")


if __name__ == "__main__":
    main()
