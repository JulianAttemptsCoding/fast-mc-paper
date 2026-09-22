from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
import platform
import traceback
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
COMMAND_RECORDS: list[dict] = []


def release_source_hashes() -> dict:
    paths = [ROOT / name for name in ["main.tex", "references.bib", "build.ps1", "README.md", "STATUS.md", "CITATION.cff"]]
    paths += [ROOT / p for p in [
        "audit/claim_register_20260922.json", "audit/claim_register_20260922.md",
        "audit/adversarial_revision_20260922.json", "audit/adversarial_revision_20260922.md",
        "audit/literature_benchmark.md",
    ]]
    paths += sorted((ROOT / "scripts").glob("*.py"))
    paths += sorted(p for p in (ROOT / "data").rglob("*") if p.is_file())
    return {str(p.relative_to(ROOT)).replace("\\", "/"): sha256(p) for p in paths}

EXPECTED_FIGURES = {
    "detector_geometry.png",
    "generator_schematic.png",
    "longitudinal_profile.png",
}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def run(command: list[str], *, cwd: Path = ROOT) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    COMMAND_RECORDS.append({"argv": command, "returncode": result.returncode,
                            "stdout_sha256": hashlib.sha256(result.stdout.encode()).hexdigest(),
                            "stderr_sha256": hashlib.sha256(result.stderr.encode()).hexdigest()})
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
    close(invariants["closure_tolerance_absolute_gev"], 2e-5)
    close(invariants["closure_tolerance_relative"], 1e-5)
    close(invariants["closure_tolerance_effective_gev"],
          max(invariants["closure_tolerance_absolute_gev"],
              invariants["closure_tolerance_relative"] * invariants["closure_scale_gev"]))
    assert invariants["layer_closure_max_gev"] > invariants["closure_tolerance_absolute_gev"]
    checks.append("Aggregate invariant counters and historical batch-relative policy; legacy absolute-only countercheck fails as disclosed")

    source = load_json(ROOT / "data/provenance/source_evidence.json")
    split_counts = source["canonical_preparation"]["split_counts"]
    assert split_counts == {"train": 612482, "validation": 76158, "test": 76300}
    assert sum(split_counts.values()) == source["canonical_preparation"]["entries"] == 764940
    pilot = source["pilot_training"]
    assert pilot["events"] == 26624 and pilot["pilot_validation_events"] == 6656
    assert pilot["config_sha256"] == report["identity"]["frozen_config_sha256"]
    assert pilot["splits_sha256"] == source["binding"]["splits_sha256"]
    assert pilot["splits_sha256"] != report["identity"]["splits_sha256"]
    assert source["candidate"]["checkpoint_sha256"] == report["identity"]["checkpoint_sha256"]
    assert source["battery_contract"]["validation_manifest_sha256"] == report["identity"]["validation_manifest_sha256"]
    assert source["battery_contract"]["splits_sha256"] == report["identity"]["splits_sha256"]
    assert abs(100 * pilot["events"] / split_counts["train"] - 4.35) < 0.005
    checks.append("Config-hash-bound pilot population, canonical preparation counts, and distinct training/diagnostic split provenance")

    assert geometry["n_nodes"] == 6790
    assert geometry["layer_counts"][0] == 400
    assert sum(geometry["layer_counts"][1:]) == 6390
    assert geometry["n_layers"] == 65
    assert geometry["n_edges"] == 107920
    assert 8 * 6790 + 2 * 4 * (400 + 63 * 100) == geometry["n_edges"]
    gang = geometry["physical_position_count_histogram"]
    assert sum(int(v) for v in gang.values()) == 6790
    assert int(gang["1"]) == 4390 and int(gang["2"]) == 1950 and int(gang["3"]) == 444 and int(gang["4"]) == 6
    assert 4390 - 400 == 3990 and 6390 - 3990 == 2400
    checks.append("Readout geometry, ganging arithmetic, layer count, and explicitly reproduced directed-edge count")

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
    close(report["activity"]["generated"]["mean_last_active_layer"], 60.61888821261919)
    close(report["activity"]["truth"]["mean_last_active_layer"], 56.195114565458766)
    close(report["activity"]["generated"]["mean_span"], 60.88374923919659)
    close(report["activity"]["truth"]["mean_span"], 56.68517210053498)
    close(report["activity"]["generated"]["gap_fraction"], 0.9352809900588355)
    close(report["activity"]["truth"]["gap_fraction"], 0.5242757646108812)
    close(report["first_layer"]["generated"]["ecal_start_prevalence"], 0.9253398255224183)
    close(report["first_layer"]["truth"]["ecal_start_prevalence"], 0.9381245583930554)
    close(report["first_layer"]["generated"]["mean_first_active_layer"], 0.7351389734226009)
    close(report["first_layer"]["truth"]["mean_first_active_layer"], 0.5099424649237912)
    for side, nonempty in [("generated", ng), ("truth", nr)]:
        activity = report["activity"][side]
        close(activity["mean_span"] - activity["mean_active_layers"] / nonempty,
              activity["mean_gaps"], atol=1e-10)
    close(values["active_layers_g"] - values["active_layers_r"], 0.2519342750226694, atol=1e-8)
    close(report["activity"]["generated"]["mean_last_active_layer"] - report["activity"]["truth"]["mean_last_active_layer"], 4.423773647160425, atol=1e-8)
    close(values["components_g"] - values["components_r"], 35.970332798618135, atol=1e-8)
    close(100 * (values["largest_g"] - values["largest_r"]), -6.029700995384565, atol=1e-8)
    checks.append("Nonempty denominators; absolute table differences; span/gap/last-layer identities; no ratio-only headline")

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
    checks.append("Response moments and energy-bin ranges; legacy Wasserstein/bootstrap fields verified as stored but excluded from the manuscript")

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
    assert len(set(epochs)) == len(epochs)
    assert epochs == list(range(11, 115))
    assert {row["run_tag"] for row in rows if int(row["epoch"]) > 90} == {"dicos-f-03"}
    assert sha256(HISTORY) == load_json(ROOT / "data/training/calibrated_lr3e4_history.provenance.json")["sha256"]
    checks.append("Hash-verified 104-row extract, contiguous unique epochs, one declared post-90 continuation, and epoch-90 objective minimum")
    return report


def validate_tex_and_bib(checks: list[str]) -> None:
    tex = (ROOT / "main.tex").read_text(encoding="utf-8")
    bib = (ROOT / "references.bib").read_text(encoding="utf-8")
    required = [
        "Julian Juan", "Wen-Chen Chang", "Institute of Physics, Academia Sinica",
        "exploratory case study", "strict-positive support", "condition-only pipeline control has AUROC 0.500",
        "50\\leq\\Kinc\\leq250\\GeV", "No nominal test event is used",
        "104 rows spanning epochs 11--114", "single checkpoint",
        "four nearest centroids are selected", "stored in both directions", "107,920 in total",
        r"\prod_{\ell>F}^{64}", "The two energy features are deterministically related",
        "event-level arrays needed for uncertainty estimates", "end-to-end timing",
        "This counts inactive layers, not contiguous runs.", "26,624 training events", "6,656 validation events", "76,158 validation", "76,300 nominal test",
        "batch-wide absolute-plus-relative tolerance", "0.25 more active layers", "4.42 layers farther downstream",
        "35.97 more weak components", "6.03-percentage-point reduction",
        "Zero-deposit events & 93 (0.93\\%) & 142 (1.42\\%)",
        "Mean last active layer & 56.20 & 60.62 & $+4.42$",
        "Mean weak graph components & 23.42 & 59.39 & $+35.97$",
        "Mean largest-component fraction & 94.90\\% & 88.87\\% & $-6.03$ pp",
    ]
    missing = [phrase for phrase in required if phrase not in tex]
    assert not missing, f"required manuscript text missing: {missing}"
    forbidden = [
        "V3-SUP", "V3-S2", "M0", "B0", "epoch 12", "midpoint Euler",
        "plotted error bars", "promotion criterion",
        "0.4636", "0.7748", "0.7785", "0.9330", "S2",
        "551,234-event", "76,160", "76,298", "Two declared continuations",
        "gap runs", "gap-run", "inactive runs increase", "interior-gap runs",
        "Topology-Sensitive Validation", "The contribution is threefold", "Artifact identity and audit boundary",
        "response_energy_bins.png", "structure_ratio_summary.png", "training_history.png",
        "0.0727", "0.1475", "0.0684", "0.1984", "2.88", "2.54",
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
    checks.append("Three deterministic manuscript figures, source hashes, dimensions, and nonblank raster content")


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
    assert "dicos-f-02" in readme and "epoch 90" in readme and "Version 0.6.0" in status
    assert "version: 0.6.0" in citation and "Connectivity Diagnostics" in citation
    assert literature.count("https://") >= 8 and "CaloChallenge" in literature and "ZDC" in literature
    assert all(token in response for token in ["reviews/review7.txt", "reviews/review8.txt", "reviews/review9.txt", "Findings resolved by removal"])
    checks.append(f"Active-versus-archived evidence separation, {len(json_paths)} active JSON files, nine supplied audits, synchronized release documentation, Python compilation, and git whitespace check")


def validate_pdf(iteration: int, checks: list[str]) -> tuple[dict, list[dict]]:
    info_text = run(["pdfinfo", str(PDF)]).stdout
    pages = int(re.search(r"^Pages:\s+(\d+)", info_text, re.MULTILINE).group(1))
    assert 6 <= pages <= 14
    render_dir = ROOT / "audit" / "qa_runs" / f"iteration_{iteration:02d}"
    render_dir.mkdir(parents=True, exist_ok=False)
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
    required = ["Connectivity Diagnostics", "Julian Juan", "Wen-Chen Chang", "References"]
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
        "source_sha256": release_source_hashes(),
        "figures_manifest_sha256": sha256(FIGURE_MANIFEST),
        "environment": {"platform": platform.platform(), "python": sys.version},
        "executed_commands": COMMAND_RECORDS,
        "human_visual_review": "pending; render statistics are not visual inspection",
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

    record_path = ROOT / "audit/iterations" / f"iteration_{args.iteration:02d}.json"
    if record_path.exists():
        raise FileExistsError(f"Refusing to overwrite historical QA: {record_path}")
    build = run(["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", "build.ps1", "-Python", sys.executable])
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
    try:
        main()
    except Exception as error:
        if "--iteration" in sys.argv:
            number = int(sys.argv[sys.argv.index("--iteration") + 1])
            failed_path = ROOT / "audit/iterations" / f"iteration_{number:02d}.json"
            if not failed_path.exists():
                payload = {"iteration": number, "created_utc": datetime.now(timezone.utc).isoformat(),
                           "result": "fail", "full_suite": False, "error": str(error),
                           "traceback": traceback.format_exc(), "source_sha256": release_source_hashes(),
                           "executed_commands": COMMAND_RECORDS}
                failed_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
                failed_path.with_suffix(".md").write_text(f"# QA attempt {number}: FAIL\n\n{error}\n", encoding="utf-8")
        raise
