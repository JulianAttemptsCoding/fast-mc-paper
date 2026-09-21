from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
PDF = ROOT / "output" / "fast_mc_zdc_manuscript.pdf"
REPORT = ROOT / "data" / "reports" / "dicos-f-02_epoch90.json"
PROVENANCE = ROOT / "data" / "reports" / "dicos-f-02_epoch90.provenance.json"
HISTORY = ROOT / "data" / "training" / "calibrated_lr3e4_history.csv"
FIGURE_MANIFEST = ROOT / "figures" / "manifest.json"
EXPECTED_FIGURES = {
    "detector_geometry.png",
    "generator_schematic.png",
    "training_history.png",
    "response_energy_bins.png",
    "longitudinal_profile.png",
    "structure_ratio_summary.png",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def run(command: list[str], *, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if result.returncode:
        raise AssertionError(
            f"command failed ({result.returncode}): {' '.join(command)}\n"
            f"STDOUT:\n{result.stdout[-6000:]}\nSTDERR:\n{result.stderr[-6000:]}"
        )
    return result


def close(actual: float, expected: float, *, atol: float = 1e-9) -> None:
    assert math.isclose(float(actual), float(expected), rel_tol=1e-9, abs_tol=atol), (actual, expected)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_evidence(checks: list[str]) -> dict:
    report = load_json(REPORT)
    provenance = load_json(PROVENANCE)
    geometry = load_json(ROOT / "data" / "geometry" / "geometry_summary.json")
    control = load_json(ROOT / "data" / "reports" / "condition_only_control.json")

    assert report["schema_version"] == 3
    assert report["split"] == "validation"
    assert report["test_events_used"] == 0
    assert report["validation_events_used"] == 10_000
    assert report["pairs"] == 10_000
    assert report["identity"]["epoch"] == 90
    assert report["identity"]["generator_seed"] == 20260723
    assert report["identity"]["checkpoint_sha256"] == provenance["checkpoint_sha256"]
    assert report["identity"]["frozen_config_sha256"] == provenance["frozen_config_sha256"]
    assert provenance["report_sha256"] == sha256(REPORT)
    assert provenance["selected_by"] == "lowest validation loss over the complete declared horizon"
    close(provenance["selected_validation_loss"], 4.483767619419238)
    assert control == {
        "kind": "condition-only-pipeline-control",
        "run_tag": "dicos-f-02",
        "epoch": 90,
        "source_split": "validation",
        "condition_only_auroc": 0.5,
        "interpretation": "pairing-pipeline sanity control only; contains no shower information",
        "test_events_used": 0,
    }
    checks.append("Evidence identity, split roles, checkpoint/config hashes, and condition-only control")

    invariants = report["structural_invariants"]
    assert invariants["pass"] is True and invariants["reports"] == 1250
    for key in [
        "count_mismatch_max", "dust_cells", "negative", "nonfinite", "outside_valid_support",
        "requested_realized_mismatch_max", "support_mask_mismatch",
    ]:
        assert invariants[key] == 0, key
    close(invariants["event_closure_max_gev"], 1.1444091796875e-05)
    close(invariants["layer_closure_max_gev"], 3.0517578125e-05)
    close(invariants["closure_tolerance_effective_gev"], 0.0004941688537597657)
    checks.append("All 1,250 invariant reports and numerical closure tolerances")

    split_counts = (612_482, 76_160, 76_298)
    assert sum(split_counts) == 764_940
    assert 551_234 + 30_624 + 30_624 == split_counts[0]
    percentages = [100 * n / sum(split_counts) for n in split_counts]
    for value, expected in zip(percentages, [80.069, 9.956, 9.974], strict=True):
        close(value, expected, atol=5e-4)
    checks.append("Corpus and role arithmetic, including exact 80.069/9.956/9.974 percentages")

    assert geometry["n_nodes"] == 6790
    assert geometry["layer_counts"][0] == 400
    assert sum(geometry["layer_counts"][1:]) == 6390
    assert geometry["n_layers"] == 65
    assert geometry["n_edges"] == 107920
    gang = geometry["physical_position_count_histogram"]
    assert sum(int(v) for v in gang.values()) == 6790
    assert int(gang["1"]) == 4390 and int(gang["2"]) == 1950 and int(gang["3"]) == 444 and int(gang["4"]) == 6
    assert 4390 - 400 == 3990 and 6390 - 3990 == 2400
    checks.append("Readout geometry, ganging arithmetic, layer count, and directed-edge count")

    zero_g = report["visibility_and_zero_response"]["generated"]["zero_fraction"]
    zero_r = report["visibility_and_zero_response"]["truth"]["zero_fraction"]
    ng, nr = 1 - zero_g, 1 - zero_r
    values = {
        "active_layers_g": report["activity"]["generated"]["mean_active_layers"] / ng,
        "active_layers_r": report["activity"]["truth"]["mean_active_layers"] / nr,
        "channels_g": report["counts"]["generated"]["mean_hit_count"] / ng,
        "channels_r": report["counts"]["truth"]["mean_hit_count"] / nr,
        "components_g": report["topology"]["generated"]["connected_components_mean"] / ng,
        "components_r": report["topology"]["truth"]["connected_components_mean"] / nr,
        "largest_g": report["topology"]["generated"]["largest_component_fraction_mean"] / ng,
        "largest_r": report["topology"]["truth"]["largest_component_fraction_mean"] / nr,
    }
    for key, expected in {
        "active_layers_g": 54.83495638060458,
        "active_layers_r": 54.58302210558191,
        "channels_g": 1588.8193345506188,
        "channels_r": 1617.5679822347834,
        "components_g": 59.38953134510042,
        "components_r": 23.419198546482285,
        "largest_g": 0.8887087677677027,
        "largest_r": 0.9490057777215484,
    }.items():
        close(values[key], expected, atol=1e-8)
    assert round(100 * (values["channels_g"] / values["channels_r"] - 1), 1) == -1.8
    close(report["activity"]["generated"]["mean_gaps"], 6.048792858592006)
    close(report["activity"]["truth"]["mean_gaps"], 2.1021499949530633)
    close(report["activity"]["generated"]["gap_fraction"], 0.9352809900588355)
    close(report["activity"]["truth"]["gap_fraction"], 0.5242757646108812)
    close(report["first_layer"]["generated"]["ecal_start_prevalence"], 0.9253398255224183)
    close(report["first_layer"]["truth"]["ecal_start_prevalence"], 0.9381245583930554)
    close(report["first_layer"]["generated"]["mean_first_active_layer"], 0.7351389734226009)
    close(report["first_layer"]["truth"]["mean_first_active_layer"], 0.5099424649237912)
    checks.append("Nonempty-event denominators and every activity/topology table statistic")

    total = report["distribution_metrics"]["total_response_gev"]
    close(total["generated_mean"], 4.36936254901063)
    close(total["truth_mean"], 4.324175614774786)
    bins = report["positive_response"]["response_bins"]
    assert sum(int(row["n"]) for row in bins) == 10_000
    close(sum(row["n"] * row["generated_mean"] for row in bins) / 10_000, total["generated_mean"], atol=3e-7)
    close(sum(row["n"] * row["truth_mean"] for row in bins) / 10_000, total["truth_mean"], atol=3e-7)
    mean_diffs = [100 * row["mean_bias_fraction"] for row in bins]
    width_diffs = [100 * row["resolution_difference_fraction"] for row in bins]
    close(min(mean_diffs), -7.653090357780457, atol=1e-8)
    close(max(mean_diffs), 7.735941559076309, atol=1e-8)
    close(min(width_diffs), -10.88799312710762, atol=1e-8)
    close(max(width_diffs), 9.582071751356125, atol=1e-8)
    close(report["positive_response"]["response_wasserstein_gev"], 0.07272892743995106)
    interval = report["bootstrap"]["intervals"]["response_wasserstein_gev"]
    close(interval["low"], 0.0684143976088688)
    close(interval["high"], 0.19837148981439048)
    close(report["truth_half_floors"]["response_wasserstein_gev"], 0.1474655284291369)
    checks.append("Response moments, energy-bin counts/ranges, bootstrap interval, and reference-half floor")

    profile = report["distribution_metrics"]["mean_longitudinal_profile"]
    g = np.asarray(profile["generated"], dtype=float)
    r = np.asarray(profile["truth"], dtype=float)
    assert g.shape == r.shape == (65,)
    close(g[0] / r[0] - 1, 0.083159, atol=2e-6)
    close(g[1:].sum() / r[1:].sum() - 1, -0.058226, atol=2e-6)
    close(np.abs(g - r).sum() / r.sum(), 0.070965, atol=2e-6)
    checks.append("ECAL/HCAL cancellation and longitudinal-profile discrepancy")

    with HISTORY.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    assert len(rows) == 104
    epochs = [int(row["epoch"]) for row in rows]
    losses = [float(row["validation_loss"]) for row in rows]
    assert (min(epochs), max(epochs)) == (11, 114)
    best = min(zip(losses, epochs, strict=True))
    close(best[0], 4.483767619419238)
    assert best[1] == 90
    assert all(loss > best[0] for loss, epoch in zip(losses, epochs, strict=True) if epoch > 90)
    checks.append("Complete 104-row recorded training lineage and epoch-90 validation selection")
    return report


def validate_tex_and_bib(checks: list[str]) -> None:
    tex = (ROOT / "main.tex").read_text(encoding="utf-8")
    bib = (ROOT / "references.bib").read_text(encoding="utf-8")
    required = [
        "Julian Juan", "Wen-Chen Chang", "Institute of Physics, Academia Sinica",
        "condition-only pipeline control with AUROC 0.500", "single-seed",
        "50\\leq\\Kinc\\leq250\\GeV", "No nominal test event is used",
        "recorded continuation lineage through absolute epoch 114",
        r"V=B\,\mathbb 1[\Kinc>0]\,\mathbb 1[\widetilde T>0]",
        "independently given the condition", "This factorization can match per-layer activation probabilities",
        "unresolved support risk", "physics fidelity", "matched timing",
        "Zero-deposit events (\\%) & 0.93 & 1.42 & 1.53",
        "Mean first active layer & 0.510 & 0.735 & 1.44",
        "Mean weak graph components & 23.42 & 59.39 & 2.54",
        "Mean largest-component fraction (\\%) & 94.90 & 88.87 & 0.94",
    ]
    missing = [phrase for phrase in required if phrase not in tex]
    assert not missing, f"required manuscript text missing: {missing}"
    forbidden = [
        "V3-SUP", "V3-S2", "M0", "B0", "epoch 12", "midpoint Euler",
        "plotted error bars", "promotion criterion",
        "0.4636", "0.7748", "0.7785", "0.9330", "S2",
    ]
    found = [phrase for phrase in forbidden if phrase in tex]
    assert not found, f"stale or excluded manuscript language: {found}"
    assert r'Kr{\"u}ger' in bib and 'Kr{"u}ger' not in bib
    checks.append("Claim language, author/mentor metadata, scope statements, and stale-model exclusion")

    bib_keys = set(re.findall(r"@\w+\{([^,]+),", bib))
    citation_groups = re.findall(r"\\cite\{([^}]+)\}", tex)
    cited = {key.strip() for group in citation_groups for key in group.split(",")}
    missing_bib = sorted(cited - bib_keys)
    assert not missing_bib, f"missing bibliography entries: {missing_bib}"
    assert len(cited) >= 12
    labels = set(re.findall(r"\\label\{([^}]+)\}", tex))
    refs = set(re.findall(r"\\(?:ref|eqref)\{([^}]+)\}", tex))
    assert not (refs - labels), f"undefined source refs: {sorted(refs-labels)}"
    assert len(labels) == len(re.findall(r"\\label\{([^}]+)\}", tex)), "duplicate labels"
    checks.append(f"{len(cited)} citation keys and {len(labels)} LaTeX labels/references")


def validate_figures(checks: list[str]) -> None:
    manifest = load_json(FIGURE_MANIFEST)
    assert set(manifest["figures_sha256"]) == EXPECTED_FIGURES
    assert manifest["test_events_used"] == 0
    for name, digest in manifest["figures_sha256"].items():
        path = ROOT / "figures" / name
        assert path.exists() and sha256(path) == digest
        with Image.open(path) as image:
            assert image.width >= 1200 and image.height >= 500
            gray = np.asarray(ImageOps.grayscale(image), dtype=np.uint8)
            assert float((gray < 245).mean()) > 0.005
    assert manifest["sources_sha256"]["data/reports/dicos-f-02_epoch90.json"] == sha256(REPORT)
    checks.append("Six deterministic figures, source hashes, dimensions, and nonblank raster content")


def validate_repository(checks: list[str]) -> None:
    active_reports = {path.name for path in (ROOT / "data" / "reports").glob("*.json")}
    assert active_reports == {
        "condition_only_control.json",
        "dicos-f-02_epoch90.json",
        "dicos-f-02_epoch90.provenance.json",
    }
    archived_screens = {path.name for path in (ROOT / "archive" / "excluded_screens").glob("*")}
    assert {
        "frozen_v3-sup-portable.yaml", "screening_summary.json", "v3-m0-fresh_epoch19.json",
        "v3-s2-response_epoch19.json", "v3-sup_epoch12.json", "verified_condition_control.json",
    } <= archived_screens
    json_paths = sorted((ROOT / "data").rglob("*.json")) + sorted((ROOT / "figures").glob("*.json"))
    for path in json_paths:
        load_json(path)
    reviews = sorted((ROOT / "reviews").glob("review*.txt"))
    substantive = [path for path in reviews if "headings" not in path.name]
    assert len(substantive) == 9 and all(path.stat().st_size > 500 for path in substantive)
    run([sys.executable, "-m", "py_compile", "scripts/build_figures.py", "scripts/full_manuscript_qa.py", "scripts/write_build_audit.py"])
    diff = run(["git", "diff", "--check"])
    assert not diff.stdout.strip()
    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    status = (ROOT / "STATUS.md").read_text(encoding="utf-8")
    citation = (ROOT / "CITATION.cff").read_text(encoding="utf-8")
    literature = (ROOT / "audit" / "literature_benchmark.md").read_text(encoding="utf-8")
    response = (ROOT / "audit" / "reviewer_response_round3.md").read_text(encoding="utf-8")
    assert "dicos-f-02" in readme and "epoch 90" in readme and "Version 0.3.0" in status
    assert "version: 0.3.0" in citation and "Auditing a Hierarchical Generator" in citation
    assert literature.count("https://") >= 8 and "CaloChallenge" in literature and "Zero Degree" in literature
    assert all(token in response for token in ["reviews/review7.txt", "reviews/review8.txt", "reviews/review9.txt", "Findings resolved by removal"])
    checks.append(f"Active-versus-archived evidence separation, {len(json_paths)} active JSON files, nine supplied audits, synchronized release documentation, Python compilation, and git whitespace check")


def validate_pdf(iteration: int, checks: list[str]) -> tuple[dict, list[dict]]:
    info_text = run(["pdfinfo", str(PDF)]).stdout
    pages = int(re.search(r"^Pages:\s+(\d+)", info_text, re.MULTILINE).group(1))
    assert 8 <= pages <= 16
    render_dir = ROOT / "audit" / "qa_runs" / f"iteration_{iteration:02d}"
    if render_dir.exists():
        shutil.rmtree(render_dir)
    render_dir.mkdir(parents=True)
    run(["pdftoppm", "-png", "-r", "110", str(PDF), str(render_dir / "page")])
    rendered = sorted(render_dir.glob("page-*.png"))
    assert len(rendered) == pages
    page_metrics: list[dict] = []
    thumbs: list[Image.Image] = []
    sizes: set[tuple[int, int]] = set()
    for index, path in enumerate(rendered, start=1):
        with Image.open(path) as source:
            image = source.convert("RGB")
        sizes.add(image.size)
        gray = np.asarray(ImageOps.grayscale(image), dtype=np.uint8)
        ink = gray < 248
        fraction = float(ink.mean())
        assert 0.005 < fraction < 0.45, (index, fraction)
        ys, xs = np.where(ink)
        margins = {
            "left": int(xs.min()), "right": int(image.width - 1 - xs.max()),
            "top": int(ys.min()), "bottom": int(image.height - 1 - ys.max()),
        }
        assert min(margins.values()) >= 8, (index, margins)
        page_text = run(["pdftotext", "-f", str(index), "-l", str(index), str(PDF), "-"]).stdout
        assert len(re.sub(r"\s+", "", page_text)) >= 120, f"page {index} has too little extractable text"
        page_metrics.append({
            "page": index, "sha256": sha256(path), "ink_fraction": fraction,
            "ink_margins_px": margins, "text_characters": len(page_text),
        })
        thumb = image.copy()
        thumb.thumbnail((390, 510))
        thumbs.append(thumb)
    assert len(sizes) == 1
    cols = 3
    rows = math.ceil(len(thumbs) / cols)
    sheet = Image.new("RGB", (cols * 400, rows * 520), "white")
    for i, thumb in enumerate(thumbs):
        sheet.paste(thumb, ((i % cols) * 400, (i // cols) * 520))
    sheet.save(render_dir / "contact.png", optimize=True)

    pdf_text = run(["pdftotext", str(PDF), "-"]).stdout
    forbidden = ["??", "0.4636", "0.7748", "0.7785", "0.9330", "V3-SUP", "V3-S2", "M0", "S2"]
    found = [term for term in forbidden if term in pdf_text]
    assert not found, f"forbidden PDF text: {found}"
    required = ["Auditing a Hierarchical Generator", "Julian Juan", "Wen-Chen Chang", "References"]
    assert all(term in pdf_text for term in required)
    log = (ROOT / "main.log").read_text(encoding="utf-8", errors="replace")
    problems = re.findall(r"LaTeX Warning|Undefined control sequence|Overfull|Underfull|Citation '.+?' undefined", log)
    assert not problems, problems
    checks.append(f"{pages}-page PDF text/log scan plus every-page render, clipping, ink, and extractability checks")
    return {
        "sha256": sha256(PDF), "bytes": PDF.stat().st_size, "pages": pages,
        "page_size": next(line.split(":", 1)[1].strip() for line in info_text.splitlines() if line.startswith("Page size:")),
        "contact_sheet": str((render_dir / "contact.png").relative_to(ROOT)).replace("\\", "/"),
    }, page_metrics


def write_report(iteration: int, focus: str, disposition: str, checks: list[str], pdf: dict, pages: list[dict]) -> None:
    out_dir = ROOT / "audit" / "iterations"
    out_dir.mkdir(parents=True, exist_ok=True)
    created = datetime.now(timezone.utc).isoformat()
    source_files = [ROOT / "main.tex", ROOT / "references.bib", ROOT / "scripts" / "build_figures.py"]
    payload = {
        "schema_version": 1,
        "iteration": iteration,
        "created_utc": created,
        "focus": focus,
        "disposition": disposition,
        "result": "pass",
        "full_suite": True,
        "checks": checks,
        "pdf": pdf,
        "page_metrics": pages,
        "source_sha256": {str(path.relative_to(ROOT)).replace("\\", "/"): sha256(path) for path in source_files},
        "commands": [
            "powershell -NoProfile -ExecutionPolicy Bypass -File build.ps1",
            "python -m py_compile scripts/build_figures.py scripts/full_manuscript_qa.py scripts/write_build_audit.py",
            "git diff --check",
            f"pdftoppm -png -r 110 output/fast_mc_zdc_manuscript.pdf audit/qa_runs/iteration_{iteration:02d}/page",
            "pdftotext output/fast_mc_zdc_manuscript.pdf -",
        ],
    }
    json_path = out_dir / f"iteration_{iteration:02d}.json"
    md_path = out_dir / f"iteration_{iteration:02d}.md"
    json_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    lines = [
        f"# Full manuscript QA iteration {iteration:02d}", "", f"Created: {created}", "",
        f"**Focus:** {focus}", "", f"**Disposition:** {disposition}", "",
        "**Result:** PASS", "", "## Full-suite checks", "",
        *[f"- {item}: pass" for item in checks], "", "## Rendered artifact", "",
        f"- PDF SHA-256: `{pdf['sha256']}`", f"- Size: {pdf['bytes']:,} bytes",
        f"- Layout: {pdf['pages']} pages; {pdf['page_size']}",
        f"- Every page was rasterized at 110 dpi and checked for blank content, edge clipping, and extractable text.",
        f"- Contact sheet: `{pdf['contact_sheet']}` (local QA artifact; excluded from release).", "",
        "This was a complete manuscript-wide pass. The focus names the adversarial reading lens; it does not limit the automated suite.", "",
    ]
    md_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--iteration", type=int, required=True)
    parser.add_argument("--focus", required=True)
    parser.add_argument("--disposition", required=True)
    args = parser.parse_args()
    assert 1 <= args.iteration <= 99

    build = run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "build.ps1"])
    checks: list[str] = ["Clean end-to-end figure, bibliography, and LaTeX rebuild"]
    validate_evidence(checks)
    validate_tex_and_bib(checks)
    validate_figures(checks)
    validate_repository(checks)
    pdf, pages = validate_pdf(args.iteration, checks)
    write_report(args.iteration, args.focus, args.disposition, checks, pdf, pages)
    print(f"FULL QA iteration {args.iteration:02d}: PASS ({pdf['pages']} pages, {pdf['sha256']})")
    if build.stdout.strip():
        print(build.stdout.strip().splitlines()[-1])


if __name__ == "__main__":
    main()
