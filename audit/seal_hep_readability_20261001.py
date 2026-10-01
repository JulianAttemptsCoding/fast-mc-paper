"""Seal the HEP-readability preprint against the final complete QA record."""
from __future__ import annotations

import hashlib
import json
import platform
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = Path("C:/Users/Julia/OneDrive/Desktop/coding/ASIoP/Fast MC CBSC")
SERIES = "hep_readability_20261001"
QA_PATH = ROOT / "audit/qa_series" / SERIES / "iteration_15.json"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def twin(root: Path, name: str, payload: dict, prose: str) -> None:
    path = root / "audit" / name
    path.with_suffix(".json").write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    path.with_suffix(".md").write_text(prose, encoding="utf-8")


qa = json.loads(QA_PATH.read_text(encoding="utf-8"))
assert qa["result"] == "pass" and qa["full_suite"] is True
assert len(qa["checks"]) == 20 and qa["pdf"]["pages"] == 14
prior = json.loads((QA_PATH.parent / "iteration_14.json").read_text(encoding="utf-8"))
changed = [current["page"] for old, current in zip(prior["page_metrics"], qa["page_metrics"], strict=True)
           if old["sha256"] != current["sha256"]]
assert changed == [9, 10], changed
notes = {
    "1": "Title, abstract, physics motivation and study scope read; no detector-performance overclaim.",
    "2": "Target, zero-threshold definition, stored geometry and Figure 1 read; dimensions and beam-frame caveat clear.",
    "3": "Population provenance and Figure 2 architecture read; every stage has a readable physical role.",
    "4": "Response, activity factorization, energy cap and first flow target read; equations and units legible.",
    "5": "Flow solver, layer budgets, count, graph message and hit selection read; independence and placement limits clear.",
    "6": "Channel-energy flow, decoder closure, teacher forcing and joint loss read; no incident-energy conservation claim.",
    "7": "Training selection, gap/segment/group definitions, bound and paired-classifier control read; no causal attribution.",
    "8": "Primary results table and energy/longitudinal results read; separate populations and intervals explicit.",
    "9": "Energy and illustrative support figures read; toy graph clearly marked, contiguous-segment result legible.",
    "10": "Hit-count distance, classifier, numerical checks and diagnostic mechanisms read; paragraph now starts coherently.",
    "11": "Threshold, time, geometry, timing, reconstruction limitations and conclusion read; fit and hierarchy clear.",
    "12": "Acknowledgment, AI disclosure, checkpoint hashes and calibration table read; no affiliation label.",
    "13": "Energy-bin/classifier tables and pair-split arithmetic read; 70% per row and 4,200 expected rows distinct.",
    "14": "All 25 bibliography entries visible and legible; no clipping or unresolved citations.",
}
for page in qa["page_metrics"]:
    image = ROOT / "audit/qa_runs" / SERIES / f"iteration_15/page-{page['page']:02d}.png"
    assert sha(image) == page["sha256"]
visual = {
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "result": "pass",
    "series": SERIES,
    "iteration": 15,
    "pdf_sha256": qa["pdf"]["sha256"],
    "page_sha256": {str(p["page"]): p["sha256"] for p in qa["page_metrics"]},
    "review_method": "All 14 QA13 pages directly inspected. QA14 changed pages 9, 10, 13 directly reinspected. Final QA15 changed only pages 9 and 10, directly reinspected; all other page-image hashes match inspected QA14 pages.",
    "page_notes": notes,
    "scientific_scope": "Visual and textual review, not physics validation.",
}
twin(ROOT, "visual_review_finalization_20260930", visual,
     "# Current every-page visual review\n\nAll 14 pages were read. Final pages 9 and 10 were reinspected; all other page images match the inspected prior pass by SHA-256. Figures, tables, equations and references are legible. The exact PDF and page hashes are in the JSON twin.\n")

command = [sys.executable, "-X", "utf8", "scripts/write_build_audit.py"]
proc = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
assert proc.returncode == 0, proc.stdout + proc.stderr
print(proc.stdout.strip())

members = ["main.tex", "references.bib", "main.bbl"] + [
    "figures/" + name for name in
    ("detector_geometry.png", "generator_schematic.png", "longitudinal_profile.png", "support_summary.png")
]
assert "bbl format version 3.3" in (ROOT / "main.bbl").read_text(encoding="utf-8")
dest = ROOT / "output/fast_mc_zdc_submission_source.zip"
with zipfile.ZipFile(dest, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for name in members:
        archive.write(ROOT / name, name)
with zipfile.ZipFile(dest) as archive:
    assert archive.testzip() is None and archive.namelist() == members
    for name in members:
        assert archive.read(name) == (ROOT / name).read_bytes()

package = {
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "revision": "0.21.0",
    "sha256": sha(dest),
    "members_sha256": {name: sha(ROOT / name) for name in members},
    "pdf_sha256": qa["pdf"]["sha256"],
    "status": "Seven-file source archive; CRC and exact bytes verified",
    "arxiv_server_compile": "Not performed",
    "current_qa": str(QA_PATH.relative_to(ROOT)).replace("\\", "/"),
    "guidance_checked": ["https://info.arxiv.org/help/submit_tex.html", "https://info.arxiv.org/help/faq/texlive.html"],
}
twin(ROOT, "arxiv_package_20260930", package,
     "# Current arXiv source package\n\nVersion 0.21.0; seven required files only. CRC and source/figure bytes verified; hashes in the JSON twin. arXiv server compilation and upload have not been performed.\n")
notes_path = ROOT / "output/arxiv_submission_notes.md"
notes_source = notes_path.read_text(encoding="utf-8")
notes_source = notes_source.replace("v0.20.0", "v0.21.0").replace(
    "audit/claude_integration_response_20261001.md", "audit/hep_readability_response_20261001.md")
notes_path.write_text(notes_source, encoding="utf-8")

final = {
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "revision": "0.21.0",
    "status": "Local preprint revision and arXiv source-package QA complete",
    "main_sha256": sha(ROOT / "main.tex"),
    "pdf_sha256": qa["pdf"]["sha256"],
    "zip_sha256": sha(dest),
    "checks": 20,
    "visual_pages": 14,
    "guard_tests": 10,
    "current_qa": package["current_qa"],
    "failed_attempts": list(range(1, 13)),
    "failure_resolution": "Exact-phrase guards followed scientifically equivalent revised wording; current-source hash synchronized; CRLF recognized as an EOL in local Git configuration; prose condensed to satisfy the unchanged 14-page maximum. Every failed attempt preserved.",
    "native_editor_compile": "Platform initialization failed: Unable to find standard directories for platform",
    "local_build": "pdfLaTeX/Biber and all 20 QA groups passed",
    "commands": [command, [sys.executable, "-X", "utf8", "-m", "unittest", "discover", "-s", "scripts", "-p", "test_qa_guards.py", "-v"]],
    "environment": {"python": sys.version, "platform": platform.platform()},
    "source_research": ["https://arxiv.org/html/2406.12877v2", "https://eicrecon.epic-eic.org/doxygen/InclusiveKinematicsJB_8h_source.html"],
    "new_event_or_test_data_access": False,
    "new_training_or_model_changes": False,
    "arxiv_uploaded": False,
    "remaining_empirical_studies": "Event-level threshold, time, graph and reconstruction sensitivity; paired structural intervals; independent generator fits.",
}
body = ("# HEP readability revision completed\n\nVersion 0.21.0: detector-facing definitions of positive-deposit hit patterns, contiguous active-layer segments and graph-connected groups, with physical architecture interpretations and measured limits. All original numbered equations and numerical tables remain.\n\nFinal QA15: 20 groups, 14 visually reviewed pages and 10 release-guard tests passed. The local LaTeX/Biber build and seven-file source archive are verified. Native editor compilation failed at platform initialization; arXiv server compilation and upload remain unperformed. No new physics validation. Exact hashes, failures and environment are in the JSON twin.\n")
for base, name in [(ROOT, "hep_readability_completion_20261001"),
                   (WORK, "manuscript_hep_readability_completion_20261001")]:
    twin(base, name, final, body)
    with (base / "logs.md").open("a", encoding="utf-8") as handle:
        handle.write("\n\n## 2026-10-01: HEP readability release sealed\n\nQA15 passed 20 groups on a 14-page PDF; 14 pages visually reviewed by exact rendered-page hash, 10 release-guard tests passed. Seven-file arXiv source ZIP bytes and CRC verified. Native editor compile failed at platform initialization; local pdfLaTeX/Biber succeeded. See audit/" + name + ".json for hashes, commands and all failed attempts. No new empirical validation or arXiv upload.\n")
print(json.dumps({"revision": final["revision"], "pdf_sha256": final["pdf_sha256"],
                  "zip_sha256": final["zip_sha256"]}, indent=2))
