"""Render validation-only manuscript figures from frozen local battery reports."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIR = ROOT / "data/reports"
SCREENING = SOURCE_DIR / "screening_summary.json"
CONDITION_CONTROL = SOURCE_DIR / "verified_condition_control.json"
OUTPUT_DIR = ROOT / "figures"

REPORT_FILES = {
    "B0": SOURCE_DIR / "dicos-f-02_epoch90.json",
    "V3-SUP": SOURCE_DIR / "v3-sup_epoch12.json",
    "S2": SOURCE_DIR / "v3-s2-response_epoch19.json",
}
COLORS = {"Geant4": "#222222", "B0": "#27659c", "V3-SUP": "#d17c24", "S2": "#9e3e79"}


def load() -> tuple[dict, dict]:
    reports = {name: json.loads(path.read_text(encoding="utf-8")) for name, path in REPORT_FILES.items()}
    for name, report in reports.items():
        if report["split"] != "validation" or report["test_events_used"] != 0:
            raise ValueError(f"{name}: non-validation or test-use report")
        if report["data_usage"]["validation_truth_events"] != 10_000:
            raise ValueError(f"{name}: wrong validation bank")
    hashes = {report["identity"]["validation_manifest_sha256"] for report in reports.values()}
    if len(hashes) != 1:
        raise ValueError("Reports do not share the frozen validation bank")
    screening = json.loads(SCREENING.read_text(encoding="utf-8"))
    if screening["test_events_used"] != 0:
        raise ValueError("Screening has test use")
    return reports, screening


def style() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["DejaVu Serif"],
            "font.size": 10,
            "axes.titlesize": 11,
            "axes.labelsize": 10,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.alpha": 0.22,
            "grid.linewidth": 0.6,
            "savefig.dpi": 240,
        }
    )


def save(fig: plt.Figure, filename: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_DIR / filename, dpi=240, facecolor="white", metadata={"Software": "CBSC-ZDC"})
    plt.close(fig)


def plot_architecture() -> None:
    fig, ax = plt.subplots(figsize=(10.8, 3.05), layout="constrained")
    ax.set_xlim(0, 11.1)
    ax.set_ylim(0, 3.1)
    ax.axis("off")
    rows = [
        [(0.15, "Incident neutron\nfour-vector"), (2.9, "Shared condition\nencoder"),
         (5.65, "Visibility and\nresponse total"), (8.4, "Start layer and\nactivity mask")],
        [(8.4, "Layer budgets\nand hit counts"), (5.65, "Graph-based\nchannel support"),
         (2.9, "Positive energy\nshares"), (0.15, "Sparse calorimeter\nreadout")],
    ]
    widths, height = 2.35, 0.85
    y_positions = [1.9, 0.35]
    for row_index, row in enumerate(rows):
        y = y_positions[row_index]
        for node_index, (x, label) in enumerate(row):
            color = "#e7eef5" if row_index == 0 else "#e9f0e8"
            if row_index == 1 and node_index == 3:
                color = "#e9e4f0"
            ax.add_patch(FancyBboxPatch((x, y), widths, height, boxstyle="round,pad=0.06,rounding_size=0.1",
                                        linewidth=1.1, edgecolor="#31445b", facecolor=color))
            ax.text(x + widths / 2, y + height / 2, label, ha="center", va="center", fontsize=10,
                    color="#1d2b3c")
    def arrow(start: tuple[float, float], end: tuple[float, float]) -> None:
        ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=13,
                                     linewidth=1.4, color="#344c65"))
    for i in range(3):
        arrow((rows[0][i][0] + widths + 0.08, 2.325), (rows[0][i + 1][0] - 0.08, 2.325))
        arrow((rows[1][i][0] - 0.08, 0.775), (rows[1][i + 1][0] + widths + 0.08, 0.775))
    arrow((9.575, 1.82), (9.575, 1.30))
    ax.text(5.55, 1.52, "Conditional generation with exact sparse decoding", ha="center",
            va="center", fontsize=10, color="#344c65", style="italic")
    save(fig, "generator_schematic.png")


def plot_c2st(reports: dict) -> None:
    families = [("high_level", "High-level"), ("low_level", "Low-level"), ("profile_aware", "Profile-aware")]
    names = list(reports)
    fig, axes = plt.subplots(1, 3, figsize=(10.8, 3.15), sharey=True, layout="constrained")
    for ax, (key, label) in zip(axes, families, strict=True):
        for i, name in enumerate(names):
            data = reports[name]["c2st"][key]
            val = data["auroc_mean"]
            ax.errorbar(i, val, yerr=data["auroc_std"], color=COLORS[name], marker="o",
                        markersize=7, capsize=3, lw=1.5)
            ax.text(i, val + 0.016, f"{val:.3f}", ha="center", va="bottom", fontsize=8)
        ax.axhline(0.5, color="#777777", ls=":", lw=1)
        if key == "high_level":
            ax.axhline(0.65, color="#a23b3b", ls="--", lw=1.1)
        ax.set_title(label)
        ax.set_xticks(range(len(names)), names)
        ax.set_ylim(0.48, 1.015)
        ax.set_axisbelow(True)
    axes[0].set_ylabel("Classifier two-sample AUROC")
    control = json.loads(CONDITION_CONTROL.read_text(encoding="utf-8"))["current"]["condition_only_auroc"]
    if control != 0.5:
        raise ValueError("verified condition-only control is not exactly chance")
    fig.suptitle("Development-bank classifier separation; condition-only control = 0.500", fontsize=12)
    save(fig, "c2st_validation.png")


def plot_response_bins(reports: dict) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 3.1), sharex=True, layout="constrained")
    for name in ["B0", "V3-SUP"]:
        bins = reports[name]["positive_response"]["response_bins"]
        x = [(b["low"] + b["high"]) / 2 for b in bins]
        for ax, field in zip(axes, ["mean_bias_fraction", "resolution_difference_fraction"], strict=True):
            ax.plot(x, [100 * b[field] for b in bins], marker="o", ms=5, lw=0,
                    label=name, color=COLORS[name])
    for ax, title in zip(axes, ["Mean response bias", "Response-width difference"], strict=True):
        ax.axhline(0, color="#333333", lw=0.9)
        ax.set_title(title)
        ax.set_xlabel("Incident neutron kinetic energy (GeV)")
        ax.set_xticks([62.5, 112.5, 162.5, 212.5], ["50-75", "100-125", "150-175", "200-225"])
        ax.tick_params(axis="x", labelsize=8)
        ax.set_axisbelow(True)
    axes[0].set_ylabel("Difference from Geant4 (%)")
    axes[0].legend(frameon=False, fontsize=9)
    fig.suptitle("Deposited-response moments vary across the primary range", fontsize=12)
    save(fig, "response_energy_bins.png")


def plot_longitudinal(reports: dict) -> None:
    b0 = reports["B0"]["distribution_metrics"]["mean_longitudinal_profile"]
    sup = reports["V3-SUP"]["distribution_metrics"]["mean_longitudinal_profile"]
    truth = np.asarray(sup["truth"])
    if not np.allclose(truth, b0["truth"], rtol=0, atol=1e-10):
        raise ValueError("Truth longitudinal profiles differ across reports")
    layers = np.arange(len(truth))
    fig, axes = plt.subplots(1, 3, figsize=(10.8, 3.25), width_ratios=[0.75, 1.35, 1.35], layout="constrained")
    ecal_values = [truth[0], b0["generated"][0], sup["generated"][0]]
    axes[0].bar(range(3), ecal_values, color=[COLORS[n] for n in ["Geant4", "B0", "V3-SUP"]], width=0.68)
    axes[0].set_xticks(range(3), ["Geant4", "B0", "V3-SUP"], rotation=25)
    axes[0].set_title("ECAL layer 0")
    axes[0].set_ylabel("Mean deposited energy / event (GeV)")
    axes[0].set_axisbelow(True)
    for ax in axes[1:]:
        for name, vals in [("Geant4", truth), ("B0", b0["generated"]), ("V3-SUP", sup["generated"])]:
            ax.plot(layers, vals, label=name, color=COLORS[name], lw=2 if name == "Geant4" else 1.65,
                    ls="--" if name == "Geant4" else "-")
        ax.set_xlabel("Longitudinal layer")
        ax.set_axisbelow(True)
    axes[1].set_xlim(1, 30)
    axes[1].set_ylim(0, 0.12)
    axes[1].set_title("HCAL development (layers 1-30)")
    axes[2].set_xlim(1, 64)
    axes[2].set_yscale("log")
    axes[2].set_title("HCAL tail (log scale)")
    axes[2].legend(frameon=False, fontsize=8)
    fig.suptitle("Mean longitudinal response on the same validation bank", fontsize=12)
    save(fig, "longitudinal_profile.png")


def plot_topology(reports: dict) -> None:
    names = ["Geant4", "B0", "V3-SUP"]
    sup_truth = reports["V3-SUP"]
    metrics = [
        ("Interior-gap fraction", lambda p, t: p["activity"][t]["gap_fraction"] * 100, "%", (0, 105)),
        ("Mean interior gaps", lambda p, t: p["activity"][t]["mean_gaps"], "gaps / event", (0, 8)),
        ("Connected components", lambda p, t: p["topology"][t]["connected_components_mean"], "components / event", (0, 67)),
    ]
    fig, axes = plt.subplots(1, 3, figsize=(10.8, 3.2), layout="constrained")
    for ax, (title, getter, unit, ylim) in zip(axes, metrics, strict=True):
        values = [getter(sup_truth, "truth"), getter(reports["B0"], "generated"), getter(sup_truth, "generated")]
        ax.bar(range(3), values, color=[COLORS[n] for n in names], width=0.68)
        for i, val in enumerate(values):
            ax.text(i, val + 0.035 * ylim[1], f"{val:.1f}", ha="center", fontsize=8)
        ax.set_xticks(range(3), names)
        ax.set_ylim(*ylim)
        ax.set_title(title)
        ax.set_ylabel(unit)
        ax.set_axisbelow(True)
    fig.suptitle("Longitudinal gaps and spatial fragmentation persist", fontsize=12)
    save(fig, "topology_validation.png")


def plot_zero_response(reports: dict) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 3.05), layout="constrained")
    panels = [["Geant4", "B0", "V3-SUP"], ["Geant4", "S2"]]
    for ax, panel, ylim in zip(axes, panels, [(0, 2.1), (0, 55)], strict=True):
        values = []
        for name in panel:
            p = reports["V3-SUP"] if name == "Geant4" else reports[name]
            role = "truth" if name == "Geant4" else "generated"
            values.append(100 * p["visibility_and_zero_response"][role]["zero_fraction"])
        ax.bar(range(len(panel)), values, color=[COLORS[n] for n in panel], width=0.62)
        for i, val in enumerate(values):
            ax.text(i, val + 0.04 * ylim[1], f"{val:.2f}%", ha="center", fontsize=9)
        ax.set_xticks(range(len(panel)), panel)
        ax.set_ylim(*ylim)
        ax.set_ylabel("Zero-response events (%)")
        ax.set_axisbelow(True)
    axes[0].set_title("Baseline and supervised continuation")
    axes[1].set_title("S2 response-spline regression")
    fig.suptitle("The visible-response hurdle remains a separate fidelity problem", fontsize=12)
    save(fig, "zero_response_validation.png")


def write_manifest() -> None:
    def sha(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    manifest = {
        "kind": "zdc-manuscript-development-bank-figures",
        "scientific_status": "development-bank diagnostics only; physics validation not established",
        "test_events_used": 0,
        "sources_sha256": {str(p.relative_to(ROOT)).replace("\\", "/"): sha(p) for p in [*REPORT_FILES.values(), SCREENING, CONDITION_CONTROL]},
        "figures_sha256": {p.name: sha(p) for p in sorted(OUTPUT_DIR.glob("*.png"))},
    }
    (OUTPUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    reports, _screening = load()
    style()
    plot_architecture()
    plot_c2st(reports)
    plot_response_bins(reports)
    plot_longitudinal(reports)
    plot_topology(reports)
    plot_zero_response(reports)
    write_manifest()
    print(f"Wrote one model schematic and five development-bank figures to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
