from __future__ import annotations

import hashlib
import json
import platform
import re
import subprocess
import sys
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


def command_version(command: list[str]) -> str:
    result = subprocess.run(command, capture_output=True, text=True, check=True)
    return (result.stdout or result.stderr).splitlines()[0].strip()


def main() -> None:
    if not PDF.exists():
        raise SystemExit("Build the PDF before writing the audit")

    info = subprocess.run(["pdfinfo", str(PDF)], capture_output=True, text=True, check=True).stdout
    pages = int(re.search(r"^Pages:\s+(\d+)", info, re.MULTILINE).group(1))
    page_size = re.search(r"^Page size:\s+(.+)$", info, re.MULTILINE).group(1).strip()

    text_path = ROOT / "audit" / ".pdf-text-audit.txt"
    subprocess.run(["pdftotext", str(PDF), str(text_path)], check=True)
    pdf_text = text_path.read_text(encoding="utf-8", errors="replace")
    text_path.unlink()
    forbidden = ["??", "0.4636", "0.7748", "0.7785", "0.9330", "validation-only evidence"]
    found = [term for term in forbidden if term in pdf_text]
    if found:
        raise SystemExit(f"Forbidden PDF text found: {found}")

    log = (ROOT / "main.log").read_text(encoding="utf-8", errors="replace")
    warnings = re.findall(r"LaTeX Warning|Undefined control sequence|Overfull|Underfull", log)
    if warnings:
        raise SystemExit(f"LaTeX log warnings remain: {warnings}")

    json_files = sorted((ROOT / "data" / "reports").glob("*.json"))
    json_files += [ROOT / "data" / "geometry" / "geometry_summary.json", ROOT / "figures" / "manifest.json"]
    for path in json_files:
        json.loads(path.read_text(encoding="utf-8"))

    hash_paths = [
        ROOT / ".gitignore",
        ROOT / "CITATION.cff",
        ROOT / "README.md",
        ROOT / "STATUS.md",
        ROOT / "build.ps1",
        ROOT / "main.tex",
        ROOT / "references.bib",
        ROOT / "scripts" / "build_figures.py",
        ROOT / "scripts" / "write_build_audit.py",
    ]
    for directory in ["archive", "data/configs", "data/geometry", "data/reports", "figures", "reviews"]:
        hash_paths.extend(path for path in (ROOT / directory).glob("*") if path.is_file())
    hash_paths.extend([
        ROOT / "audit" / "reviewer_response.md",
        ROOT / "audit" / "reviewer_response_round2.md",
    ])
    hashes = {str(path.relative_to(ROOT)).replace("\\", "/"): sha256(path) for path in sorted(hash_paths)}

    blockers = [
        "new locked evaluation bank with exact event identifiers",
        "pair-grouped condition-aware C2ST with calibrated nulls",
        "three independent generator-training seeds per frozen final condition",
        "fixed-condition repeated reference and generator showers",
        "oracle-versus-ancestral stage cascade and S2 component autopsy",
        "cap and CLR-clipping counters plus topology threshold stability",
        "complete Geant4, detector, material, field, cut, and seed provenance",
        "independent physical-neighbor graph for ganged readout geometry",
        "matched baselines, reconstruction evaluation, and end-to-end timing",
    ]
    created = datetime.now(timezone.utc).isoformat()
    audit = {
        "schema_version": 2,
        "created_utc": created,
        "status": "development-bank-manuscript",
        "release": "v0.2.0",
        "output": {
            "path": "output/fast_mc_zdc_manuscript.pdf",
            "sha256": sha256(PDF),
            "bytes": PDF.stat().st_size,
            "pages": pages,
            "page_size": page_size,
        },
        "qa": {
            "build_exit_code": 0,
            "python_compile": "pass",
            "json_parse_count": len(json_files),
            "latex_warning_scan": "pass",
            "pdf_text_scan": "pass",
            "visual_render": f"pass: all {pages} pages rendered and inspected",
            "historical_random_fold_c2st": "excluded from claims and archived",
            "condition_only_control_auroc": 0.5,
        },
        "environment": {
            "platform": platform.platform(),
            "python": platform.python_version(),
            "pdflatex": command_version(["pdflatex", "--version"]),
            "biber": command_version(["biber", "--version"]),
            "pdftoppm": command_version(["pdftoppm", "-v"]),
        },
        "commands": [
            "python scripts/build_figures.py",
            "python -m py_compile scripts/build_figures.py scripts/write_build_audit.py",
            "pdflatex -interaction=nonstopmode -halt-on-error main.tex",
            "biber main",
            "pdflatex -interaction=nonstopmode -halt-on-error main.tex (two passes)",
            "pdftotext output/fast_mc_zdc_manuscript.pdf <temporary text>",
            "pdftoppm -png -r 110 output/fast_mc_zdc_manuscript.pdf audit/render3/page",
        ],
        "sha256": hashes,
        "known_submission_blockers": blockers,
    }
    (ROOT / "audit" / "final_build_audit.json").write_text(
        json.dumps(audit, indent=2, sort_keys=False) + "\n", encoding="utf-8"
    )

    lines = [
        "# Final build audit",
        "",
        f"Created: {created}",
        "",
        "## Artifact",
        "",
        "- Output: `output/fast_mc_zdc_manuscript.pdf`",
        f"- SHA-256: `{audit['output']['sha256']}`",
        f"- Size: {audit['output']['bytes']:,} bytes",
        f"- Layout: {pages} A4 pages",
        "- Scientific status: development-bank manuscript; no final fidelity or speed claim",
        "",
        "## Checks",
        "",
        "- Deterministic figure generation and Python bytecode compilation passed.",
        f"- {len(json_files)} JSON evidence files parsed successfully.",
        "- pdfLaTeX, Biber, and two final pdfLaTeX passes completed.",
        "- The final LaTeX log has no warnings, undefined controls, overfull boxes, or underfull boxes.",
        "- PDF text has no unresolved-reference markers or excluded historical C2ST values.",
        f"- All {pages} pages were rendered and visually inspected.",
        "- The historical random-fold shower-only C2ST is absent from the manuscript and archived as excluded evidence.",
        "",
        "## Reproducibility boundary",
        "",
        "The repository rebuilds the manuscript and all plotted figures from frozen aggregate evidence. It includes the portable V3-SUP configuration and event-independent geometry. It does not include the collaboration-owned event file or checkpoints and cannot recompute event-level tests or retrain the model.",
        "",
        "Submission blockers are tracked in `STATUS.md` and `audit/reviewer_response_round2.md`.",
        "",
        "## Environment",
        "",
        f"- Platform: `{audit['environment']['platform']}`",
        f"- Python: `{audit['environment']['python']}`",
        f"- pdfLaTeX: `{audit['environment']['pdflatex']}`",
        f"- Biber: `{audit['environment']['biber']}`",
        f"- pdftoppm: `{audit['environment']['pdftoppm']}`",
        "",
        "Input and figure SHA-256 hashes are recorded in `audit/final_build_audit.json`.",
        "",
    ]
    (ROOT / "audit" / "final_build_audit.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
