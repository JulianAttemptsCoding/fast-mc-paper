"""List sentences of the built text that contain a negation (editing aid)."""

from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
name = sys.argv[1] if len(sys.argv) > 1 else "main.txt"
text = (HERE / name).read_text(encoding="utf-8", errors="replace")
end = text.find("References\n")
if end > 0:
    text = text[:end]
text = re.sub(r"\s+", " ", text)
pattern = re.compile(r"\b(not|no|nor|neither|cannot|without)\b", re.I)
count = 0
for sentence in re.split(r"(?<=[.!?])\s+", text):
    hits = len(pattern.findall(sentence))
    if hits:
        count += 1
        print(f"[{hits}] {sentence[:260]}")
print(count, "sentences with a negation")
