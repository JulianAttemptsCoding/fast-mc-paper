"""Bind the follow-up reader pass to the inspected PDF and source archive."""
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
SERIES = "hep_readability_followup_20261001"
QA = ROOT / "audit/qa_series" / SERIES / "iteration_06.json"
OLD = ROOT / "audit/qa_series/hep_readability_20261001/iteration_15.json"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def twin(root: Path, name: str, data: dict, prose: str) -> None:
    path = root / "audit" / name
    path.with_suffix(".json").write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    path.with_suffix(".md").write_text(prose, encoding="utf-8")


qa = json.loads(QA.read_text(encoding="utf-8"))
old = json.loads(OLD.read_text(encoding="utf-8"))
assert qa["result"] == "pass" and qa["full_suite"] is True
assert len(qa["checks"]) == 20 and qa["pdf"]["pages"] == 14
assert digest(ROOT / "output/fast_mc_zdc_manuscript.pdf") == qa["pdf"]["sha256"]
changed = [a["page"] for a, b in zip(old["page_metrics"], qa["page_metrics"], strict=True)
           if a["sha256"] != b["sha256"]]
assert changed == [1, 2, 8, 9, 10, 11], changed
for number, inspected_iteration in [(1, 3), (2, 3), (8, 4), (9, 6), (10, 6), (11, 3)]:
    inspected = json.loads((QA.parent / f"iteration_{inspected_iteration:02d}.json").read_text(encoding="utf-8"))
    assert inspected["page_metrics"][number - 1]["sha256"] == qa["page_metrics"][number - 1]["sha256"]

notes = {
    "1": "Title, abstract, ePIC motivation and study limits inspected; classifier control is explicit.",
    "2": "Condition vector and nonnegative raw target inspected; three-momentum and geometry caveats clear.",
    "3": "Population provenance and architecture diagram inherited unchanged from reviewed prior PDF.",
    "4": "Response, cap and activity equations inherited unchanged; no lost theta/sigma symbols.",
    "5": "Flow, layer budget, graph and selection equations inherited unchanged; math legible.",
    "6": "Decoder membership cases and loss inherited unchanged; no OCR-alleged typesetting defects.",
    "7": "Evaluation definitions, m>=R bound and C2ST caveat inherited unchanged.",
    "8": "Section-calibration example, results table and longitudinal paragraph inspected; no clipping.",
    "9": "Energy-depth paragraph and both figures inspected; no sentence is interrupted by a float.",
    "10": "Bound starts a complete paragraph; C2ST, numerical checks and physical discussion inspected.",
    "11": "Threshold two-sided sensitivity, timing and reconstruction limitations inspected.",
    "12": "Acknowledgments, disclosure and reproducibility table inherited unchanged.",
    "13": "Energy-bin and classifier tables inherited unchanged; all entries legible.",
    "14": "All references inherited unchanged and remain on the final page.",
}
for page in qa["page_metrics"]:
    image = ROOT / "audit/qa_runs" / SERIES / f"iteration_06/page-{page['page']:02d}.png"
    assert digest(image) == page["sha256"]
visual = {
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "result": "pass",
    "series": SERIES,
    "iteration": 6,
    "pdf_sha256": qa["pdf"]["sha256"],
    "page_sha256": {str(page["page"]): page["sha256"] for page in qa["page_metrics"]},
    "review_method": "All pages reviewed in the predecessor QA15. Current changed pages 1, 2, 11 directly inspected in QA03, page 8 in QA04, pages 9 and 10 in QA06; exact page hashes unchanged thereafter. The eight other pages match inspected QA15 page hashes.",
    "page_notes": notes,
    "scope": "Visual and textual QA, not new physics validation.",
}
twin(ROOT, "visual_review_finalization_20260930", visual,
     "# Current every-page visual review\n\nAll 14 pages are bound by page-image hash. The six pages changed from the fully reviewed predecessor were directly inspected in the indicated QA attempts; unchanged pages match that review exactly. Figures, equations, tables and bibliography are legible; page 8–9 and 9–10 sentence interruptions were repaired. This is layout and language QA, not physics validation.\n")

command = [sys.executable, "-X", "utf8", "scripts/write_build_audit.py"]
run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace")
assert run.returncode == 0, run.stdout + run.stderr
print(run.stdout.strip())

members = ["main.tex", "references.bib", "main.bbl"] + [
    "figures/" + name for name in
    ("detector_geometry.png", "generator_schematic.png", "longitudinal_profile.png", "support_summary.png")
]
assert "bbl format version 3.3" in (ROOT / "main.bbl").read_text(encoding="utf-8")
archive_path = ROOT / "output/fast_mc_zdc_submission_source.zip"
with zipfile.ZipFile(archive_path, "w", compression=zipfile.ZIP_DEFLATED) as archive:
    for name in members:
        archive.write(ROOT / name, name)
with zipfile.ZipFile(archive_path) as archive:
    assert archive.testzip() is None and archive.namelist() == members
    for name in members:
        assert archive.read(name) == (ROOT / name).read_bytes()

package = {
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "revision": "0.21.1",
    "sha256": digest(archive_path),
    "members_sha256": {name: digest(ROOT / name) for name in members},
    "pdf_sha256": qa["pdf"]["sha256"],
    "status": "Seven-file source archive; CRC and exact bytes verified",
    "arxiv_server_compile": "Not performed",
    "current_qa": str(QA.relative_to(ROOT)).replace("\\", "/"),
    "guidance_checked": ["https://info.arxiv.org/help/submit_tex.html", "https://info.arxiv.org/help/faq/texlive.html"],
}
twin(ROOT, "arxiv_package_20260930", package,
     "# Current arXiv source package\n\nVersion 0.21.1; seven required files only. CRC and exact source/figure bytes verified; hashes in the JSON twin. arXiv server compilation and upload remain unperformed.\n")

final = {
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "revision": "0.21.1",
    "status": "Local preprint revision and arXiv source-package QA complete",
    "main_sha256": digest(ROOT / "main.tex"),
    "pdf_sha256": qa["pdf"]["sha256"],
    "zip_sha256": digest(archive_path),
    "checks": 20,
    "visual_pages": 14,
    "guard_tests": 10,
    "current_qa": package["current_qa"],
    "failed_attempts": [1, 2, 5],
    "failure_resolution": "Replaced a stale scope-wording guard with explicit equivalent assertions; condensed prose to retain the unchanged 14-page maximum; repaired two figure/page sentence interruptions. Every failed attempt is retained.",
    "native_editor_compile": "Platform initialization failed: Unable to find standard directories for platform",
    "local_build": "pdfLaTeX/Biber and all 20 QA groups passed",
    "environment": {"python": sys.version, "platform": platform.platform()},
    "source_research": ["https://arxiv.org/html/2406.12877v2", "https://pdg.lbl.gov/2024/reviews/rpp2024-rev-particle-detectors-accel.pdf", "https://info.arxiv.org/help/submit_tex.html", "https://info.arxiv.org/help/faq/texlive.html"],
    "new_event_or_test_data_access": False,
    "new_training_or_model_changes": False,
    "arxiv_uploaded": False,
}
body = ("# Follow-up HEP reader revision completed\n\nVersion 0.21.1 clarifies ePIC design context, the paired-row classifier caveat, illustrative section calibration and two-sided threshold sensitivity. Apparent formula and table faults in the supplied audit were verified as extraction artifacts. No numbered equation or numerical table changed.\n\nQA06 passed 20 groups at 14 visually reviewed pages; 10 release-guard tests passed. Local LaTeX/Biber and the seven-file source archive are verified. Native editor compilation failed at platform initialization. No arXiv upload or new physics validation occurred. Hashes and all failed attempts are in the JSON twin.\n")
for root, name in [(ROOT, "hep_readability_followup_completion_20261001"),
                   (WORK, "manuscript_hep_readability_followup_completion_20261001")]:
    twin(root, name, final, body)
    with (root / "logs.md").open("a", encoding="utf-8") as handle:
        handle.write("\n\nFollow-up HEP reader revision v0.21.1 sealed: QA06 passed 20 groups at 14 pages; all pages visually bound by hash; 10 guard tests passed. Seven-file source ZIP CRC and bytes verified. Native editor compiler failed at platform initialization; local LaTeX/Biber passed. See audit/" + name + ".json for exact hashes, environment and failed attempts. No new physics validation or arXiv upload.\n")
print(json.dumps({"revision": final["revision"], "pdf_sha256": final["pdf_sha256"],
                  "zip_sha256": final["zip_sha256"]}, indent=2))
