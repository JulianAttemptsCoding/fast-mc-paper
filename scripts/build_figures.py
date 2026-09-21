"""Render manuscript figures from frozen aggregate development artifacts."""

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
GEOMETRY_DATA = ROOT / "data/geometry/readout_geometry.npz"
GEOMETRY_SUMMARY = ROOT / "data/geometry/geometry_summary.json"
OUTPUT_DIR = ROOT / "figures"

REPORT_FILES = {
    "B0": SOURCE_DIR / "dicos-f-02_epoch90.json",
    "M0": SOURCE_DIR / "v3-m0-fresh_epoch19.json",
    "V3-SUP": SOURCE_DIR / "v3-sup_epoch12.json",
    "S2": SOURCE_DIR / "v3-s2-response_epoch19.json",
}
COLORS = {
    "Geant4": "#222222",
    "B0": "#27659c",
    "M0": "#5b8f5a",
    "V3-SUP": "#d17c24",
    "S2": "#9e3e79",
}


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
    fig, ax = plt.subplots(figsize=(10.8, 3.35), layout="constrained")
    ax.set_xlim(0, 12.2)
    ax.set_ylim(0, 3.1)
    ax.axis("off")
    rows = [
        [(0.05, "Incident neutron\nfour-vector"), (2.5, "Condition\nencoder"),
         (4.95, "Hurdle branch B\nand total draw"), (7.4, "Realized V and T"),
         (9.85, "First layer and\nindependent activity")],
        [(9.85, "Layer budgets\nand channel counts"), (7.4, "Graph support\nscores and top-k"),
         (4.95, "Energy-share\nflow logits"), (2.5, "Exact budget\ndecoder"),
         (0.05, "Sparse deposited-\nenergy vector")],
    ]
    widths, height = 2.15, 0.85
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
    for i in range(4):
        arrow((rows[0][i][0] + widths + 0.08, 2.325), (rows[0][i + 1][0] - 0.08, 2.325))
        arrow((rows[1][i][0] - 0.08, 0.775), (rows[1][i + 1][0] + widths + 0.08, 0.775))
    arrow((10.925, 1.82), (10.925, 1.30))
    ax.text(6.1, 1.52, "Teacher-forced component training; ancestral generation", ha="center",
            va="center", fontsize=10, color="#344c65", style="italic")
    save(fig, "generator_schematic.png")


def plot_geometry() -> None:
    geometry = np.load(GEOMETRY_DATA)
    summary = json.loads(GEOMETRY_SUMMARY.read_text(encoding="utf-8"))
    positions = geometry["positions_mm"]
    layers = geometry["layer_index"]
    multiplicity = geometry["physical_position_count"]
    fig, axes = plt.subplots(1, 3, figsize=(10.8, 3.55), layout="constrained")

    for ax, layer, title in [(axes[0], 0, "ECAL readout centroids"), (axes[1], 1, "Representative HCAL layer")]:
        select = layers == layer
        scatter = ax.scatter(
            positions[select, 0], positions[select, 1], c=multiplicity[select],
            cmap="viridis", vmin=1, vmax=4, s=18 if layer == 0 else 34,
            edgecolors="none",
        )
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlabel("x (mm)")
        ax.set_ylabel("y (mm)")
        ax.set_title(title)
        ax.set_axisbelow(True)
    colorbar = fig.colorbar(scatter, ax=axes[:2], shrink=0.82, pad=0.02)
    colorbar.set_label("Physical positions per readout ID")

    histogram = {int(k): int(v) for k, v in summary["physical_position_count_histogram"].items()}
    x = np.array(sorted(histogram))
    y = np.array([histogram[k] for k in x])
    axes[2].bar(x, y, color="#4c78a8", width=0.65)
    for xi, yi in zip(x, y, strict=True):
        axes[2].text(xi, yi + 70, f"{yi:,}", ha="center", fontsize=9)
    axes[2].set_xticks(x)
    axes[2].set_xlabel("Physical positions represented")
    axes[2].set_ylabel("Readout channels")
    axes[2].set_title("Readout ganging")
    axes[2].set_ylim(0, max(y) * 1.14)
    axes[2].set_axisbelow(True)
    fig.suptitle("Frozen 6,790-channel geometry; plotted locations are readout centroids", fontsize=12)
    save(fig, "detector_geometry.png")


def plot_response_bins(reports: dict) -> None:
    fig, axes = plt.subplots(1, 2, figsize=(10.8, 3.75), sharex=True, layout="constrained")
    for name in ["B0", "V3-SUP"]:
        bins = reports[name]["positive_response"]["response_bins"]
        x = [(b["low"] + b["high"]) / 2 for b in bins]
        for ax, field in zip(axes, ["mean_bias_fraction", "resolution_difference_fraction"], strict=True):
            ax.plot(x, [100 * b[field] for b in bins], marker="o", ms=5, lw=0,
                    label=name, color=COLORS[name])
    for ax, title in zip(axes, ["Mean total-deposit bias", "Total-deposit width difference"], strict=True):
        ax.axhline(0, color="#333333", lw=0.9)
        ax.set_title(title)
        ax.set_xlabel("Incident neutron kinetic energy (GeV)")
        ax.set_xticks([62.5, 112.5, 162.5, 212.5], ["50-75", "100-125", "150-175", "200-225"])
        ax.tick_params(axis="x", labelsize=8)
        ax.set_axisbelow(True)
    axes[0].set_ylabel("Difference from Geant4 (%)")
    axes[0].legend(frameon=False, fontsize=9)
    fig.suptitle("Exploratory total-deposit moments across the 50--250 GeV range", fontsize=12)
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
    fig.suptitle("Mean deposited energy by layer on the same development bank", fontsize=12)
    save(fig, "longitudinal_profile.png")


def plot_topology(reports: dict) -> None:
    names = ["Geant4", "B0", "V3-SUP"]
    sup_truth = reports["V3-SUP"]
    metrics = [
        ("Interior-gap fraction", lambda p, t: p["activity"][t]["gap_fraction"] * 100, "%", (0, 105)),
        ("Mean interior gaps", lambda p, t: p["activity"][t]["mean_gaps"], "gaps / event", (0, 8)),
        ("Mean active layers", lambda p, t: p["activity"][t]["mean_active_layers"], "layers / event", (0, 65)),
        ("Mean active channels", lambda p, t: p["counts"][t]["mean_hit_count"], "channels / event", (0, 1800)),
        ("Weak components", lambda p, t: p["topology"][t]["connected_components_mean"], "components / event", (0, 67)),
        ("Largest-component fraction", lambda p, t: p["topology"][t]["largest_component_fraction_mean"] * 100, "%", (0, 105)),
    ]
    fig, axes = plt.subplots(2, 3, figsize=(10.8, 6.15), layout="constrained")
    axes = axes.ravel()
    for ax, (title, getter, unit, ylim) in zip(axes, metrics, strict=True):
        values = [getter(sup_truth, "truth"), getter(reports["B0"], "generated"), getter(sup_truth, "generated")]
        ax.bar(range(3), values, color=[COLORS[n] for n in names], width=0.68)
        for i, val in enumerate(values):
            ax.text(i, val + 0.035 * ylim[1], f"{val:.1f}", ha="center", fontsize=9)
        ax.set_xticks(range(3), names)
        ax.set_ylim(*ylim)
        ax.set_title(title)
        ax.set_ylabel(unit)
        ax.set_axisbelow(True)
    fig.suptitle("Occupancy and readout-graph fragmentation on the development bank", fontsize=12)
    save(fig, "topology_validation.png")


def plot_zero_response(reports: dict) -> None:
    fig, ax = plt.subplots(figsize=(10.8, 4.05), layout="constrained")
    names = ["Geant4", "B0", "M0", "V3-SUP", "S2"]
    values = []
    for name in names:
        p = reports["V3-SUP"] if name == "Geant4" else reports[name]
        role = "truth" if name == "Geant4" else "generated"
        values.append(100 * p["visibility_and_zero_response"][role]["zero_fraction"])
    ax.bar(range(len(names)), values, color=[COLORS[n] for n in names], width=0.64)
    for i, val in enumerate(values):
        ax.text(i, val * 1.13, f"{val:.2f}%", ha="center", fontsize=10)
    ax.set_xticks(range(len(names)), ["Geant4", "baseline\n(B0)", "fresh control\n(M0)",
                                        "full-data continuation\n(V3-SUP)", "spline screen\n(S2)"])
    ax.set_yscale("log")
    ax.set_ylim(0.55, 85)
    ax.set_ylabel("Zero-deposit events (%)")
    ax.set_axisbelow(True)
    fig.suptitle("S2's zero-deposit anomaly is carried by the Bernoulli hurdle", fontsize=12)
    save(fig, "zero_response_validation.png")


def write_manifest() -> None:
    def sha(path: Path) -> str:
        return hashlib.sha256(path.read_bytes()).hexdigest()

    manifest = {
        "kind": "zdc-manuscript-development-bank-figures",
        "scientific_status": "development-bank diagnostics only; physics validation not established",
        "test_events_used": 0,
        "excluded_from_claims": {
            "legacy_random_fold_c2st": "not plotted or quoted; pair-grouped joint condition+shower evaluation is required",
        },
        "verified_condition_control_auroc": json.loads(CONDITION_CONTROL.read_text(encoding="utf-8"))["current"]["condition_only_auroc"],
        "sources_sha256": {str(p.relative_to(ROOT)).replace("\\", "/"): sha(p) for p in [*REPORT_FILES.values(), SCREENING, CONDITION_CONTROL, GEOMETRY_DATA, GEOMETRY_SUMMARY]},
        "figures_sha256": {p.name: sha(p) for p in sorted(OUTPUT_DIR.glob("*.png"))},
    }
    (OUTPUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    reports, _screening = load()
    style()
    plot_architecture()
    plot_geometry()
    plot_response_bins(reports)
    plot_longitudinal(reports)
    plot_topology(reports)
    plot_zero_response(reports)
    write_manifest()
    print(f"Wrote one model schematic and five development-bank figures to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
