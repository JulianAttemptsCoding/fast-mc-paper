"""Place the source-bound support illustration and aggregate data by its definitions."""
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / "main.tex"
before = hashlib.sha256(path.read_bytes()).hexdigest()
tex = path.read_bytes().decode("utf-8")
pattern = r"\\begin\{figure\}\[!htbp\]\r?\n(?:.|\r|\n)*?support_summary\.png(?:.|\r|\n)*?\\end\{figure\}"
matches = list(re.finditer(pattern, tex))
assert len(matches) == 1, len(matches)
block = matches[0].group()
old_caption = "Definitions on an illustrative graph, not shower data. Left: active layers (filled), interior empty layers (hatched), first and last layers $F,L$, gap count $G$ and contiguous active-layer segments $R$. Right: all four layers are active ($R=1$), but occupied channels form three graph-connected groups ($m=3$), so $Q=m-R=2$. Pale edges join adjacent nodes of this toy grid; the detector graph is defined in Sec.~\\ref{sec:data}."
new_caption = "Top panels are illustrations, not events: (a) active layers (filled), interior empty layers (hatched), span, gap count $G$ and contiguous segments $R$; (b) three graph-connected groups despite four consecutive active layers ($R=1$, $m=3$, $Q=2$). Bottom panels compare source-bound nonempty-sample means for last active layer, skipped layers and graph groups. Bar lengths use separate scales; labels give the absolute values. No uncertainty estimates for these structural means were retained."
assert block.count(old_caption) == 1
block = block.replace(old_caption, new_caption)
tex = tex[:matches[0].start()] + tex[matches[0].end():]
anchor = "These graph-connected groups are not detector-reconstruction clusters~\\cite{atlastopocluster}."
assert tex.count(anchor) == 1
anchor_at = tex.index(anchor) + len(anchor)
newline = "\r\n" if "\r\n" in tex[anchor_at:anchor_at + 4] else "\n"
tex = tex[:anchor_at] + newline * 2 + block + tex[anchor_at:]
path.write_bytes(tex.encode("utf-8"))
after = hashlib.sha256(path.read_bytes()).hexdigest()
payload = {"utc": datetime.now(timezone.utc).isoformat(), "command": "python -X utf8 audit/place_support_figure_20261002.py", "before_main_sha256": before, "after_main_sha256": after, "action": "Move Figure 4 immediately after definitions; caption distinguishes illustrative top panels and aggregate data bottom panels", "environment": "Windows Python 3.13, local paper checkout"}
(root / "audit/claude_review_figure_placement_20261002.json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
(root / "audit/claude_review_figure_placement_20261002.md").write_text("# Support-figure placement\n\nFigure 4 is placed after the gap/group definitions and its bottom panels now plot nonempty aggregate means from the released report. No event-level distributions or structural uncertainty were inferred. Exact source hashes are in the JSON twin.\n", encoding="utf-8")
print(json.dumps(payload, indent=2))
