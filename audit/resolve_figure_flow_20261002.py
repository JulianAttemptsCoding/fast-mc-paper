"""Keep the structural data figure beside its results when earlier placement spills a page."""
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / "main.tex"
raw = path.read_bytes()
before = hashlib.sha256(raw).hexdigest()
tex = raw.decode("utf-8")
pattern = r"\\begin\{figure\}\[!htbp\][\s\S]*?\\end\{figure\}"
matches = [match for match in re.finditer(pattern, tex) if "support_summary.png" in match.group()]
assert len(matches) == 1
block = matches[0].group()
tex = tex[:matches[0].start()] + tex[matches[0].end():]
anchor = "This fixed-region average does not isolate the energy of the additional occupied layers or disconnected components."
assert tex.count(anchor) == 1
index = tex.index(anchor) + len(anchor)
newline = "\r\n" if tex[index:index + 2] == "\r\n" else "\n"
tex = tex[:index] + newline * 2 + block + tex[index:]
path.write_bytes(tex.encode("utf-8"))
after = hashlib.sha256(path.read_bytes()).hexdigest()
record = {"utc": datetime.now(timezone.utc).isoformat(), "command": "python -X utf8 audit/resolve_figure_flow_20261002.py", "before_main_sha256": before, "after_main_sha256": after, "failure": "First local build after placing Figure 4 in evaluation produced 15 pages, exceeding the unchanged 14-page QA cap", "correction": "Keep data-enriched Figure 4 next to longitudinal result while defining its terms and citing it earlier", "environment": "Windows Python 3.13; local pdfLaTeX/Biber"}
(root / "audit/claude_review_figure_flow_20261002.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
(root / "audit/claude_review_figure_flow_20261002.md").write_text("# Figure-flow correction\n\nThe first local build after moving Figure 4 into the evaluation protocol reached 15 pages, exceeding the binding 14-page QA cap. Figure 4 now stays beside the title result in Section 5.2, and its definitions remain in Section 4 with a forward reference. The data panels and caption are retained.\n", encoding="utf-8")
print(json.dumps(record, indent=2))
