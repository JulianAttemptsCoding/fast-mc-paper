"""Reader diagrams adapted from the preserved Claude proposal; static geometry and toy graph only."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
GEOMETRY = ROOT / "data/geometry/readout_geometry.npz"
HISTORY = ROOT / "data/training/calibrated_lr3e4_history.csv"
OUT = ROOT / "figures"

REF = "#202124"
GEN = "#2f6f9f"
VAL = "#c26b2e"


def style() -> None:
    plt.rcParams.update(
        {
            "font.family": "serif",
            "font.serif": ["DejaVu Serif"],
            "font.size": 10,
            "axes.titlesize": 10.5,
            "axes.labelsize": 10,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.alpha": 0.22,
            "grid.linewidth": 0.6,
            "savefig.dpi": 260,
        }
    )


def save(fig: plt.Figure, name: str) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / name, dpi=260, facecolor="white")
    plt.close(fig)


def plot_detector_layout() -> None:
    geometry = np.load(GEOMETRY)
    pos = geometry["positions_mm"]
    layer = geometry["layer_index"]
    mult = geometry["physical_position_count"]
    if pos.shape != (6790, 3) or int(layer.max()) != 64:
        raise ValueError("Unexpected stored geometry")

    fig = plt.figure(figsize=(8.6, 2.7), layout="constrained")
    grid = fig.add_gridspec(1, 3, width_ratios=[1.75, 1.0, 1.12])

    top = fig.add_subplot(grid[0, 0])
    hcal = layer > 0
    top.scatter(pos[hcal, 2] / 1000, pos[hcal, 0], s=2.4, color=GEN, linewidths=0,
                label="HCAL, layers 1–64", rasterized=True)
    top.scatter(pos[~hcal, 2] / 1000, pos[~hcal, 0], s=2.4, color="#b3412f", linewidths=0,
                label="ECAL, layer 0", rasterized=True)
    z_line = np.array([35.66, 37.44])
    top.plot(z_line, -0.025 * z_line * 1000, color=REF, lw=0.9, ls="--",
             label="coordinate guide")
    top.set_xlabel("stored centroid $z$ (m)")
    top.set_ylabel("stored centroid $x$ (mm)")
    top.set_title("Top view: 65 layers")
    top.set_xlim(35.62, 37.48)
    top.set_ylim(-1260, -330)
    top.legend(frameon=False, fontsize=8, loc="upper left", ncol=2,
               handletextpad=0.3, columnspacing=1.0, markerscale=3.5,
               borderaxespad=0.2)
    top.set_axisbelow(True)

    scatter = None
    for index, (select_layer, title, size) in enumerate(
        [(0, "ECAL face (layer 0)", 9), (1, "HCAL face (layer 1)", 26)]
    ):
        ax = fig.add_subplot(grid[0, index + 1])
        select = layer == select_layer
        scatter = ax.scatter(pos[select, 0], pos[select, 1], c=mult[select], cmap="viridis",
                             vmin=1, vmax=4, s=size, edgecolors="none")
        ax.set_aspect("equal", adjustable="box")
        ax.set_xlabel("$x$ (mm)")
        ax.set_ylabel("$y$ (mm)")
        ax.set_title(title)
        ax.set_xlim(-1230, -570)
        ax.set_ylim(-330, 330)
        ax.set_xticks([-1100, -900, -700])
        ax.set_axisbelow(True)
        if index == 1:
            bar = fig.colorbar(scatter, ax=ax, shrink=0.72, pad=0.03, ticks=[1, 2, 3, 4])
            bar.set_label("positions per stored ID", fontsize=9)
    save(fig, "detector_geometry.png")


def _strip(ax, y: float, active: set[int], n_layers: int, label: str) -> None:
    first, last = min(active), max(active)
    for index in range(n_layers):
        if index in active:
            face, hatch, edge = GEN, None, "#1d2b3c"
        elif first < index < last:
            face, hatch, edge = "white", "////", "#b3412f"
        else:
            face, hatch, edge = "white", None, "#9aa3ad"
        ax.add_patch(Rectangle((index, y), 0.86, 0.62, facecolor=face, edgecolor=edge,
                               hatch=hatch, linewidth=0.9))
    ax.text(n_layers + 0.35, y + 0.31, label, va="center", ha="left", fontsize=9)
    ax.annotate("", xy=(first, y - 0.16), xytext=(last + 0.86, y - 0.16),
                arrowprops={"arrowstyle": "<->", "color": "#344c65", "lw": 0.9})
    ax.text((first + last + 0.86) / 2, y - 0.2, "span $L-F+1$", va="top", ha="center",
            fontsize=8, color="#344c65")
    ax.text(first + 0.43, y + 0.72, "$F$", ha="center", va="bottom", fontsize=9)
    ax.text(last + 0.43, y + 0.72, "$L$", ha="center", va="bottom", fontsize=9)


def plot_observable_definitions() -> None:
    fig = plt.figure(figsize=(8.6, 2.75), layout="constrained")
    grid = fig.add_gridspec(1, 2, width_ratios=[1.9, 1.0])

    ax = fig.add_subplot(grid[0, 0])
    n_layers = 13
    first_pattern = {0, 1, 2, 3, 4, 5, 6, 7, 9}
    second_pattern = {0, 1, 2, 3, 5, 6, 8, 11}
    _strip(ax, 1.75, first_pattern, n_layers, "9 active, span 10\n$G=1$, $R=2$")
    _strip(ax, 0.15, second_pattern, n_layers, "8 active, span 12\n$G=4$, $R=4$")
    ax.set_xlim(-0.4, n_layers + 5.4)
    ax.set_ylim(-0.55, 2.95)
    ax.set_xticks(np.arange(n_layers) + 0.43, [str(i) for i in range(n_layers)], fontsize=8)
    ax.set_yticks([])
    ax.set_xlabel("layer index (illustration)")
    ax.grid(False)
    for side in ("left",):
        ax.spines[side].set_visible(False)
    ax.set_title("(a) active layers (filled), interior empty layers (hatched)")

    bx = fig.add_subplot(grid[0, 1])
    layers, channels = 4, 6
    occupied = {
        (0, 2): 0, (0, 3): 0, (1, 2): 0, (1, 3): 0, (2, 3): 0, (2, 2): 0, (3, 3): 0,
        (1, 0): 1,
        (3, 5): 2,
    }
    palette = [GEN, "#b3412f", "#5a8f3d"]
    for a in range(layers):
        for b in range(channels):
            if b + 1 < channels:
                bx.plot([a, a], [b, b + 1], color="#c9ced6", lw=0.8, zorder=1)
            if a + 1 < layers:
                bx.plot([a, a + 1], [b, b], color="#c9ced6", lw=0.8, zorder=1)
    for (a, b), comp in occupied.items():
        for da, db in ((1, 0), (0, 1)):
            other = (a + da, b + db)
            if other in occupied and occupied[other] == comp:
                bx.plot([a, other[0]], [b, other[1]], color=palette[comp], lw=2.2, zorder=2)
    for a in range(layers):
        for b in range(channels):
            comp = occupied.get((a, b))
            bx.scatter([a], [b], s=62, zorder=3,
                       facecolor=palette[comp] if comp is not None else "white",
                       edgecolor="#1d2b3c" if comp is not None else "#9aa3ad", linewidth=0.9)
    bx.set_xticks(range(layers), [f"$\\ell$+{i}" if i else "$\\ell$" for i in range(layers)], fontsize=8)
    bx.set_yticks([])
    bx.set_xlim(-0.6, layers - 0.4)
    bx.set_ylim(-0.7, channels - 0.3)
    bx.set_xlabel("four consecutive active layers")
    bx.set_ylabel("channels in a layer")
    bx.grid(False)
    bx.set_title("(b) $R=1$, $m=3$, $Q=m-R=2$")
    save(fig, "support_summary.png")


