"""Probe whether conservative page reservations cause a spill without changing content."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / "main.tex"
raw = path.read_bytes()
before = hashlib.sha256(raw).hexdigest()
assert raw.count(b"margin=0.65in") == 1
raw = raw.replace(b"margin=0.65in", b"margin=0.75in")
for suffix in (b"12", b"10"):
    token = b"\\Needspace{" + suffix + b"\\baselineskip}"
    count = raw.count(token)
    assert count == (2 if suffix == b"12" else 1), (suffix, count)
    raw = raw.replace(token, b"% page reservation removed after visual review")
token = b"\\Needspace{8\\baselineskip}"
assert raw.count(token) == 4
raw = raw.replace(token + b"\r\n\\printbibliography", b"\\printbibliography")
path.write_bytes(raw)
after = hashlib.sha256(raw).hexdigest()
record = {"utc": datetime.now(timezone.utc).isoformat(), "command": "python -X utf8 audit/layout_reflow_probe_20261002.py", "before_main_sha256": before, "after_main_sha256": after, "change": "Restore 0.75-inch margin; remove four conservative Needspace reservations while preserving prose, mathematics and data", "environment": "Windows Python 3.13"}
(root / "audit/claude_review_layout_probe_20261002.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
(root / "audit/claude_review_layout_probe_20261002.md").write_text("# Layout reflow probe\n\nThe 0.65-inch margin did not recover the 14-page layout. Restored the original 0.75-inch margin and removed four conservative page-reservation commands; their removal changes no scientific content. Exact source hashes are in the JSON twin.\n", encoding="utf-8")
print(json.dumps(record, indent=2))
