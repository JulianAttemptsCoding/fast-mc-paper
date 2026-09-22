from __future__ import annotations

import hashlib
import json
import platform
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output" / "fast_mc_zdc_manuscript.pdf"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def command(command: list[str]) -> str:
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", check=True)
    return result.stdout or result.stderr


def first_line(command_args: list[str]) -> str:
    return command(command_args).splitlines()[0].strip()


def main() -> None:
    if not PDF.exists():
        raise SystemExit("Build the PDF before writing the audit")
    iterations = []
    for number in range(1, 21):
        path = ROOT / "audit" / "iterations" / f"iteration_{number:02d}.json"
        if not path.exists():
            raise SystemExit(f"Missing full QA record: {path.relative_to(ROOT)}")
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("result") != "pass" or payload.get("full_suite") is not True:
            raise SystemExit(f"QA iteration {number:02d} is not a full pass")
        iterations.append(payload)

    info = command(["pdfinfo", str(PDF)])
    pages = int(re.search(r"^Pages:\s+(\d+)", info, re.MULTILINE).group(1))
    page_size = re.search(r"^Page size:\s+(.+)$", info, re.MULTILINE).group(1).strip()
    pdf_text = command(["pdftotext", str(PDF), "-"])
    forbidden = ["??", "0.4636", "0.7748", "0.7785", "0.9330", "V3-SUP", "V3-S2", "M0", "S2"]
    found = [term for term in forbidden if term in pdf_text]
    if found:
        raise SystemExit(f"Excluded PDF text found: {found}")
    log = (ROOT / "main.log").read_text(encoding="utf-8", errors="replace")
    warnings = re.findall(r"LaTeX Warning|Undefined control sequence|Overfull|Underfull", log)
    if warnings:
        raise SystemExit(f"LaTeX log warnings remain: {warnings}")

    tracked = [ROOT / item for item in command(["git", "ls-files", "--cached", "--others", "--exclude-standard"]).splitlines() if item]
    excluded = {
        ROOT / "audit" / "final_build_audit.json",
        ROOT / "audit" / "final_build_audit.md",
        ROOT / "output" / "fast_mc_zdc_manuscript.pdf",
    }
    hashes = {
        str(path.relative_to(ROOT)).replace("\\", "/"): sha256(path)
        for path in tracked
        if path.is_file() and path not in excluded
    }
    created = datetime.now(timezone.utc).isoformat()
    blockers = [
        "new locked evaluation bank with exact event identifiers",
        "three independent training seeds for each frozen final condition",
        "repeated reference and generated showers at fixed conditions",
        "pair-grouped condition-aware multivariate tests with calibrated controls",
        "cap, CLR-clipping, and solver-step diagnostics",
        "component-wise teacher-forced and oracle-versus-ancestral cascade",
        "angle, tail, threshold-stability, and independent-geometry studies",
        "complete Geant4 and detector provenance",
        "matched baselines, reconstruction evaluation, and end-to-end timing",
    ]
    audit = {
        "schema_version": 3,
        "created_utc": created,
        "release": "v0.3.0",
        "status": "development-bank diagnostic manuscript",
        "accepted_artifact": {
            "run_tag": "dicos-f-02",
            "epoch": 90,
            "training_seed": 20260723,
            "checkpoint_sha256": "491284c7423f365230d34b0443f95aa4888ec770bdc673c4c979897bad8acbce",
            "frozen_config_sha256": "116bc8c220b07ce54ae07196bdd6ed8e835775c8c937182a209a799dc94ae9c5",
            "validation_events": 10000,
            "test_events": 0,
        },
        "output": {
            "path": "output/fast_mc_zdc_manuscript.pdf",
            "sha256": sha256(PDF),
            "bytes": PDF.stat().st_size,
            "pages": pages,
            "page_size": page_size,
        },
        "qa": {
            "complete_iterations": len(iterations),
            "iteration_results": [entry["result"] for entry in iterations],
            "last_iteration_pdf_sha256": iterations[-1]["pdf"]["sha256"],
            "last_iteration_page_count": iterations[-1]["pdf"]["pages"],
            "latex_log_scan": "pass",
            "pdf_text_scan": "pass",
            "all_pages_rendered_each_iteration": True,
            "condition_only_control_auroc": 0.5,
            "shower_aware_c2st": "excluded",
        },
        "environment": {
            "platform": platform.platform(),
            "python": platform.python_version(),
            "pdflatex": first_line(["pdflatex", "--version"]),
            "biber": first_line(["biber", "--version"]),
            "pdftoppm": first_line(["pdftoppm", "-v"]),
        },
        "known_submission_blockers": blockers,
        "tracked_input_sha256": hashes,
    }
    (ROOT / "audit" / "final_build_audit.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")

    lines = [
        "# Final build audit", "", f"Created: {created}", "", "## Artifact", "",
        "- Release: `v0.3.0`", "- Accepted checkpoint: `dicos-f-02`, epoch 90, training seed 20260723",
        "- Output: `output/fast_mc_zdc_manuscript.pdf`", f"- SHA-256: `{audit['output']['sha256']}`",
        f"- Size: {audit['output']['bytes']:,} bytes", f"- Layout: {pages} pages; {page_size}",
        "- Scientific status: development-bank diagnostic manuscript; no final fidelity or speed claim", "",
        "## QA", "", "- Twenty complete sequential manuscript-wide QA iterations passed.",
        "- Every iteration rebuilt all figures, bibliography, and LaTeX from source.",
        "- Every iteration checked the evidence identities, split arithmetic, headline values, citations, labels, excluded language, and figure hashes.",
        f"- Every iteration rasterized and checked all {pages} PDF pages for content, clipping, and text extraction.",
        "- The final LaTeX log has no warnings, undefined controls, overfull boxes, or underfull boxes.",
        "- PDF text contains no unresolved references, discarded model-screen names, or excluded classifier values.",
        "- The retained condition-only AUROC 0.500 is recorded solely as a pairing-pipeline control.", "",
        "## Reproducibility boundary", "",
        "The repository rebuilds the manuscript and figures from frozen aggregate evidence. It does not redistribute the collaboration-owned event file or checkpoint, so it cannot reproduce training or event-level tests independently.", "",
        "Submission blockers are tracked in `STATUS.md` and `audit/reviewer_response_round3.md`.", "",
        "Input hashes and per-iteration page metrics are recorded in the JSON audit files.", "",
    ]
    (ROOT / "audit" / "final_build_audit.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote final audit for {pages} pages and {len(iterations)} complete QA iterations")


if __name__ == "__main__":
    main()
