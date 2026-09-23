"""Render manuscript figures from frozen aggregate development artifacts."""

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch


ROOT = Path(__file__).resolve().parents[1]
REPORT = ROOT / "data/reports/dicos-f-02_epoch90.json"
PROVENANCE = ROOT / "data/reports/dicos-f-02_epoch90.provenance.json"
TRAINING_HISTORY = ROOT / "data/training/calibrated_lr3e4_history.csv"
GEOMETRY_DATA = ROOT / "data/geometry/readout_geometry.npz"
GEOMETRY_SUMMARY = ROOT / "data/geometry/geometry_summary.json"
OUTPUT_DIR = ROOT / "figures"

COLORS = {"Reference": "#202124", "Generator": "#2f6f9f", "Validation": "#c26b2e"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_report() -> dict:
    report = json.loads(REPORT.read_text(encoding="utf-8"))
    provenance = json.loads(PROVENANCE.read_text(encoding="utf-8"))
    if report["split"] != "validation" or report["test_events_used"] != 0:
        raise ValueError("The manuscript report must use validation only and no test events")
    if report["data_usage"]["validation_truth_events"] != 10_000:
        raise ValueError("Unexpected development-bank size")
    if report["identity"]["epoch"] != 90 or report["identity"]["run_tag"] != "dicos-f-02":
        raise ValueError("Unexpected checkpoint identity")
    if sha256(REPORT) != provenance["report_sha256"]:
        raise ValueError("Report byte hash disagrees with provenance sidecar")
    if report["identity"]["checkpoint_sha256"] != provenance["checkpoint_sha256"]:
        raise ValueError("Checkpoint hash disagrees with provenance sidecar")
    return report


def style() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["DejaVu Serif"],
            "font.size": 10.5,
            "axes.titlesize": 11,
            "axes.labelsize": 10.5,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.alpha": 0.22,
            "grid.linewidth": 0.6,
            "savefig.dpi": 260,
        }
    )


def save(fig: plt.Figure, filename: str) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUTPUT_DIR / filename, dpi=260, facecolor="white", metadata={"Software": "fast-mc-paper"})
    plt.close(fig)


def plot_architecture() -> None:
    fig, ax = plt.subplots(figsize=(8.6, 3.2), layout="constrained")
    ax.set_xlim(0, 13.4)
    ax.set_ylim(0, 3.35)
    ax.axis("off")
    x_positions = [0.15, 2.85, 5.55, 8.25, 10.95]
    rows = [
        [(x_positions[0], "$c$\n5 input features", "input"),
         (x_positions[1], "$h_c$\nencoding", "learned"),
         (x_positions[2], "$V,\\,T$\nevent response", "learned"),
         (x_positions[3], "$F,\\,A_\\ell$\nlayer activity", "learned"),
         (x_positions[4], "$B_\\ell$\nlayer budgets", "flow")],
        [(x_positions[4], "$K_\\ell$\nchannel counts", "learned"),
         (x_positions[3], "$S_\\ell$\nchannel set", "learned"),
         (x_positions[2], "$r_{\\ell i}$\nenergy logits", "flow"),
         (x_positions[1], "$Y_{\\ell i}$\nchannel deposits", "decode"),
         (x_positions[0], "$\\mathbf{Y}$\n6,790 deposits", "output")],
    ]
    width, height = 2.25, 0.80
    y_positions = [2.1, 0.70]
    face = {
        "input": "#f1f3f5", "output": "#f1f3f5", "learned": "#e6eef5",
        "flow": "#e8f0e7", "decode": "#ece7f2",
    }
    labels_and_boxes = []
    for row_index, row in enumerate(rows):
        for x, label, kind in row:
            box = FancyBboxPatch(
                (x, y_positions[row_index]), width, height,
                boxstyle="round,pad=0.035,rounding_size=0.09",
                linewidth=1.05, edgecolor="#31445b", facecolor=face[kind],
            )
            ax.add_patch(box)
            label_artist = ax.text(
                x + width / 2, y_positions[row_index] + height / 2, label,
                ha="center", va="center", fontsize=11.2, linespacing=1.4,
                color="#1d2b3c",
            )
            labels_and_boxes.append((label_artist, box))

    def arrow(start: tuple[float, float], end: tuple[float, float]) -> None:
        ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=13,
                                     linewidth=1.35, color="#344c65", shrinkA=0, shrinkB=0))

    for i in range(4):
        arrow((rows[0][i][0] + width + 0.065, 2.5), (rows[0][i + 1][0] - 0.065, 2.5))
        arrow((rows[1][i][0] - 0.065, 1.1), (rows[1][i + 1][0] + width + 0.065, 1.1))
    arrow((x_positions[4] + width / 2, 1.98), (x_positions[4] + width / 2, 1.62))
    legend = [("learned", "learned stage"), ("flow", "conditional flow"),
              ("decode", "deterministic decoder")]
    x0 = 2.55
    for kind, label in legend:
        ax.add_patch(FancyBboxPatch((x0, 0.15), 0.35, 0.18, boxstyle="round,pad=0.02",
                                    linewidth=0.8, edgecolor="#526477", facecolor=face[kind]))
        ax.text(x0 + 0.45, 0.24, label, ha="left", va="center", fontsize=10.2,
                color="#344c65")
        x0 += 2.95
    fig.canvas.draw()
    renderer = fig.canvas.get_renderer()
    for label_artist, box in labels_and_boxes:
        label_bbox = label_artist.get_window_extent(renderer)
        box_bbox = box.get_window_extent(renderer)
        if not (box_bbox.x0 + 4 < label_bbox.x0 and label_bbox.x1 < box_bbox.x1 - 4
                and box_bbox.y0 + 4 < label_bbox.y0 and label_bbox.y1 < box_bbox.y1 - 4):
            raise ValueError(f"Architecture label exceeds its box: {label_artist.get_text()}")
    save(fig, "generator_schematic.png")


def plot_geometry() -> None:
    geometry = np.load(GEOMETRY_DATA)
    summary = json.loads(GEOMETRY_SUMMARY.read_text(encoding="utf-8"))
    positions = geometry["positions_mm"]
    layers = geometry["layer_index"]
    multiplicity = geometry["physical_position_count"]
    fig, axes = plt.subplots(1, 3, figsize=(8.6, 3.55), layout="constrained")

    for ax, layer, title in [(axes[0], 0, "ECAL layer 0"), (axes[1], 1, "HCAL layer 1")]:
        select = layers == layer
        scatter = ax.scatter(
            positions[select, 0], positions[select, 1], c=multiplicity[select],
            cmap="viridis", vmin=1, vmax=4, s=18 if layer == 0 else 34, edgecolors="none",
        )
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlabel("readout-centroid x (mm)")
        ax.set_ylabel("readout-centroid y (mm)")
        ax.set_title(title)
        ax.set_axisbelow(True)
    colorbar = fig.colorbar(scatter, ax=axes[:2], shrink=0.82, pad=0.02)
    colorbar.set_label("physical positions / readout ID")

    histogram = {int(k): int(v) for k, v in summary["physical_position_count_histogram"].items()}
    x = np.array(sorted(histogram))
    y = np.array([histogram[k] for k in x])
    axes[2].bar(x, y, color="#4c78a8", width=0.65)
    for xi, yi in zip(x, y, strict=True):
        axes[2].text(xi, yi + 70, f"{yi:,}", ha="center", fontsize=9.5)
    axes[2].set_xticks(x)
    axes[2].set_xlabel("positions per readout ID")
    axes[2].set_ylabel("all-detector readout channels")
    axes[2].set_title("Readout ganging")
    axes[2].set_ylim(0, max(y) * 1.14)
    axes[2].set_axisbelow(True)
    fig.suptitle("Readout centroids and ganging", fontsize=11.5)
    save(fig, "detector_geometry.png")


def plot_training_history() -> None:
    with TRAINING_HISTORY.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    epochs = np.asarray([int(r["epoch"]) for r in rows])
    train = np.asarray([float(r["train_loss"]) for r in rows])
    validation = np.asarray([float(r["validation_loss"]) for r in rows])
    if len(epochs) != 104 or epochs.min() != 11 or epochs.max() != 114:
        raise ValueError("Unexpected accepted-family history")
    best_index = int(np.argmin(validation))
    if int(epochs[best_index]) != 90:
        raise ValueError("Epoch 90 is not the minimum recorded validation loss")
    fig, ax = plt.subplots(figsize=(8.6, 3.7), layout="constrained")
    ax.plot(epochs, train, color="#607d8b", lw=1.3, alpha=0.9, label="training objective")
    ax.plot(epochs, validation, color=COLORS["Validation"], lw=1.25, alpha=0.8,
            label="validation objective")
    ax.scatter([90], [validation[best_index]], s=55, zorder=5, color="#9b2c2c",
               label=f"selected epoch 90 ({validation[best_index]:.4f})")
    ax.axvspan(91, 114, color="#6b7280", alpha=0.1, label="later continuation")
    ax.set_xlabel("absolute epoch across continuation lineage")
    ax.set_ylabel("weighted teacher-forced objective")
    ax.set_xlim(11, 114)
    ax.legend(frameon=False, ncol=2, fontsize=9.5)
    ax.set_axisbelow(True)
    fig.suptitle("Checkpoint selection over recorded joint-training epochs", fontsize=11.5)
    save(fig, "training_history.png")


def plot_response_bins(report: dict) -> None:
    bins = report["positive_response"]["response_bins"]
    x = np.asarray([(b["low"] + b["high"]) / 2 for b in bins])
    mean_diff = 100 * np.asarray([b["mean_bias_fraction"] for b in bins])
    width_diff = 100 * np.asarray([b["resolution_difference_fraction"] for b in bins])
    counts = np.asarray([b["n"] for b in bins])
    labels = [f"{int(b['low'])}\u2013{int(round(b['high']))}" for b in bins]
    fig, axes = plt.subplots(1, 2, figsize=(8.6, 3.8), sharex=True, layout="constrained")
    for ax, values, title in [
        (axes[0], mean_diff, r"Mean difference: $100(\mu_g-\mu_r)/\mu_r$"),
        (axes[1], width_diff, r"Width difference: $100(\sigma_g-\sigma_r)/\sigma_r$"),
    ]:
        ax.axhline(0, color="#333333", lw=0.9)
        ax.plot(x, values, marker="o", ms=5.2, lw=1.5, color=COLORS["Generator"])
        for xi, value, n in zip(x, values, counts, strict=True):
            ax.annotate(f"n={n:,}", (xi, value), xytext=(0, 8 if value >= 0 else -13),
                        textcoords="offset points", ha="center", fontsize=9, color="#4b5563")
        ax.margins(y=0.22)
        ax.set_title(title)
        ax.set_xlabel("incident kinetic-energy bin (GeV)")
        ax.set_xticks(x, labels, rotation=35, ha="right", fontsize=9)
        ax.set_ylabel("relative difference (%)")
        ax.set_axisbelow(True)
    fig.suptitle("Total-deposit moments on the 10,000-condition development bank", fontsize=11.5)
    save(fig, "response_energy_bins.png")


def plot_longitudinal(report: dict) -> None:
    profile = report["distribution_metrics"]["mean_longitudinal_profile"]
    truth = np.asarray(profile["truth"])
    generated = np.asarray(profile["generated"])
    layers = np.arange(len(truth))
    truth_total, gen_total = truth.sum(), generated.sum()
    truth_parts = [truth[0], truth[1:].sum()]
    gen_parts = [generated[0], generated[1:].sum()]
    fig, axes = plt.subplots(1, 3, figsize=(8.6, 3.45), width_ratios=[0.8, 1.35, 1.35], layout="constrained")
    x = np.arange(2)
    axes[0].bar(x, [truth_parts[0], gen_parts[0]], color=[COLORS["Reference"], COLORS["Generator"]],
                width=0.68, label="ECAL")
    axes[0].bar(x, [truth_parts[1], gen_parts[1]], bottom=[truth_parts[0], gen_parts[0]],
                color=["#8c8c8c", "#7fa6c2"], width=0.68, label="HCAL")
    axes[0].set_xticks(x, ["reference", "generator"])
    axes[0].set_ylabel("mean deposit / event (GeV)")
    axes[0].set_title("Subsystem cancellation")
    axes[0].text(0, truth_parts[0] / 2, "ECAL", color="white", ha="center", va="center", fontsize=9.5)
    axes[0].text(0, truth_parts[0] + truth_parts[1] / 2, "HCAL", color="white", ha="center", va="center", fontsize=9.5)
    axes[0].text(0, truth_total + 0.06, f"{truth_total:.3f}", ha="center", fontsize=9.5)
    axes[0].text(1, gen_total + 0.06, f"{gen_total:.3f}", ha="center", fontsize=9.5)
    for ax in axes[1:]:
        ax.plot(layers, truth, label="Geant4 reference", color=COLORS["Reference"], lw=1.8, ls="--")
        ax.plot(layers, generated, label="generator", color=COLORS["Generator"], lw=1.7)
        ax.set_xlabel("longitudinal layer")
        ax.set_axisbelow(True)
    axes[1].set_xlim(1, 30)
    axes[1].set_ylim(0, 0.13)
    axes[1].set_title("HCAL development")
    axes[2].set_xlim(1, 64)
    axes[2].set_yscale("log")
    axes[2].set_title("HCAL tail (log scale)")
    axes[2].legend(frameon=False, fontsize=9.5)
    fig.suptitle("Mean longitudinal energy deposit", fontsize=11.5)
    save(fig, "longitudinal_profile.png")


def plot_structure_ratios(report: dict) -> None:
    zero_t = report["visibility_and_zero_response"]["truth"]["zero_fraction"]
    zero_g = report["visibility_and_zero_response"]["generated"]["zero_fraction"]
    nonempty_t, nonempty_g = 1 - zero_t, 1 - zero_g
    truth_profile = np.asarray(report["distribution_metrics"]["mean_longitudinal_profile"]["truth"])
    gen_profile = np.asarray(report["distribution_metrics"]["mean_longitudinal_profile"]["generated"])
    metrics = [
        ("total deposit", gen_profile.sum() / truth_profile.sum()),
        ("ECAL mean", gen_profile[0] / truth_profile[0]),
        ("HCAL mean", gen_profile[1:].sum() / truth_profile[1:].sum()),
        ("active layers | nonempty", (report["activity"]["generated"]["mean_active_layers"] / nonempty_g) /
                                      (report["activity"]["truth"]["mean_active_layers"] / nonempty_t)),
        ("active channels | nonempty", (report["counts"]["generated"]["mean_hit_count"] / nonempty_g) /
                                        (report["counts"]["truth"]["mean_hit_count"] / nonempty_t)),
        ("events with interior gaps | nonempty", report["activity"]["generated"]["gap_fraction"] /
                                      report["activity"]["truth"]["gap_fraction"]),
        ("interior inactive layers | nonempty", report["activity"]["generated"]["mean_gaps"] /
                                         report["activity"]["truth"]["mean_gaps"]),
        ("weak components | nonempty", (report["topology"]["generated"]["connected_components_mean"] / nonempty_g) /
                                       (report["topology"]["truth"]["connected_components_mean"] / nonempty_t)),
        ("largest-component fraction | nonempty", (report["topology"]["generated"]["largest_component_fraction_mean"] / nonempty_g) /
                                                    (report["topology"]["truth"]["largest_component_fraction_mean"] / nonempty_t)),
    ]
    labels = [m[0] for m in metrics][::-1]
    values = np.asarray([m[1] for m in metrics][::-1])
    fig, ax = plt.subplots(figsize=(8.6, 4.8), layout="constrained")
    y = np.arange(len(labels))
    ax.axvline(1, color="#222222", lw=1.0, ls="--")
    ax.hlines(y, np.minimum(values, 1), np.maximum(values, 1), color="#9ab5c7", lw=2)
    ax.scatter(values, y, color=COLORS["Generator"], s=48, zorder=3)
    for yi, value in zip(y, values, strict=True):
        ax.annotate(f"{value:.3f}\u00d7", (value, yi), xytext=(7, 0),
                    textcoords="offset points", ha="left", va="center", fontsize=9.5,
                    bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.85, "pad": 0.4})
    ax.set_yticks(y, labels)
    ax.set_xlabel("generator / reference ratio")
    ax.set_xlim(0.85, 3.3)
    ax.set_axisbelow(True)
    fig.suptitle("Topology-sensitive shower observables reveal fragmented generated support", fontsize=11.5)
    save(fig, "structure_ratio_summary.png")


def write_manifest() -> None:
    inputs = [REPORT, PROVENANCE, GEOMETRY_DATA, GEOMETRY_SUMMARY]
    manifest = {
        "kind": "fast-mc-paper-development-figures",
        "scientific_status": "development-bank diagnostics; physics validation not established",
        "test_events_used": 0,
        "excluded_from_claims": {
            "all_shower_aware_c2st_results": "reported as development-bank screening scores with the row-wise matched-pair split limitation",
            "condition_only_c2st": "sanity control only; not plotted because it contains no shower information",
            "short_v3_screens": "removed from the main narrative because they are undercontrolled and use different analysis roles",
        },
        "sources_sha256": {str(p.relative_to(ROOT)).replace("\\", "/"): sha256(p) for p in inputs},
        "figures_sha256": {
            name: sha256(OUTPUT_DIR / name)
            for name in [
                "detector_geometry.png",
                "generator_schematic.png",
                "longitudinal_profile.png",
            ]
        },
    }
    (OUTPUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> None:
    report = load_report()
    style()
    plot_architecture()
    plot_geometry()
    plot_longitudinal(report)
    for stale_name in [
        "zero_response_validation.png", "topology_validation.png",
        "training_history.png", "response_energy_bins.png", "structure_ratio_summary.png",
    ]:
        stale = OUTPUT_DIR / stale_name
        if stale.exists():
            stale.unlink()
    write_manifest()
    print(f"Wrote three manuscript figures to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
