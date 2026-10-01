"""Recompute every number quoted in the proposed revision and check it is in main.tex.

Inputs are the files already in the paper repository: the evaluation summary,
the static geometry and the training history.  Nothing is generated or sampled.
Exit status is non-zero if any expected string is missing from main.tex.
"""

from __future__ import annotations

import csv
import json
import math
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
report = json.loads((ROOT / "data/reports/dicos-f-02_epoch90.json").read_text(encoding="utf-8"))
tex = (HERE / "main.tex").read_text(encoding="utf-8")

missing: list[str] = []
checked = 0


def expect(label: str, *strings: str) -> None:
    """Require every string to be present in main.tex."""
    global checked
    for s in strings:
        checked += 1
        if s not in tex:
            missing.append(f"{label}: {s!r}")


def near(label: str, value: float, quoted: float, tolerance: float) -> None:
    global checked
    checked += 1
    if abs(value - quoted) > tolerance:
        missing.append(f"{label}: computed {value!r} vs quoted {quoted!r}")


# ---- populations and deposits -------------------------------------------------
n = report["pairs"]
empty_ref = report["first_layer"]["truth"]["events_with_no_active_layer"]
empty_gen = report["first_layer"]["generated"]["events_with_no_active_layer"]
ne_ref, ne_gen = n - empty_ref, n - empty_gen
expect("populations", "9,907", "9,858", "93 (0.93\\%)", "142 (1.42\\%)")
near("empty ratio", empty_gen / empty_ref, 1.5, 0.05)

profile = report["distribution_metrics"]["mean_longitudinal_profile"]
ref, gen = np.array(profile["truth"]), np.array(profile["generated"])
t_ref, t_gen = ref.sum(), gen.sum()
near("T ref", t_ref, 4.324, 5e-4)
near("T gen", t_gen, 4.369, 5e-4)
near("dT", t_gen - t_ref, 0.045, 5e-4)
near("dT %", 100 * (t_gen / t_ref - 1), 1.0, 0.05)
near("ECAL ref", ref[0], 2.100, 5e-4)
near("ECAL gen", gen[0], 2.275, 5e-4)
near("dECAL", gen[0] - ref[0], 0.175, 5e-4)
near("dECAL %", 100 * (gen[0] / ref[0] - 1), 8.3, 0.05)
near("HCAL ref", ref[1:].sum(), 2.224, 5e-4)
near("HCAL gen", gen[1:].sum(), 2.094, 5e-4)
near("dHCAL", gen[1:].sum() - ref[1:].sum(), -0.129, 6e-4)
near("dHCAL %", 100 * (gen[1:].sum() / ref[1:].sum() - 1), -5.8, 0.05)
near("HCAL max layer", 1 + int(ref[1:].argmax()), 9, 0)
near("layer 9 %", 100 * (gen[9] / ref[9] - 1), -8.6, 0.05)
ratio = gen / ref
low = [i for i in range(1, 31) if ratio[i] < 0.92]
near("low layers first", low[0], 9, 0)
near("low layers last", low[-1], 16, 0)
near("low layers min %", 100 * (1 - ratio[9:17].min()), 12.0, 0.05)
near("layers 10-16 all low", float(ratio[10:17].max() < 0.92), 1.0, 0)
near("profile max deviation", max(abs(ratio - 1)), 0.23, 0.02)
near("deep ref MeV", 1000 * ref[57:].sum(), 17.2, 0.05)
near("deep gen MeV", 1000 * gen[57:].sum(), 17.8, 0.05)
near("deep fraction ref %", 100 * ref[57:].sum() / t_ref, 0.4, 0.05)
near("deep fraction gen %", 100 * gen[57:].sum() / t_gen, 0.4, 0.05)

# ---- paired residual, standard errors -----------------------------------------
paired = report["paired_response"]
boot = report["bootstrap"]["intervals"]
near("paired mean", paired["response_delta_over_kinetic_mean"], 2.9e-5, 5e-7)
near("paired lo", boot["response_delta_over_kinetic_mean"]["low"], -8.5e-4, 5e-6)
near("paired hi", boot["response_delta_over_kinetic_mean"]["high"], 9.3e-4, 5e-6)
near("paired rms", paired["response_delta_over_kinetic_rmse"], 0.046, 5e-4)
near("mean K", paired["mean_kinetic_gev"], 150, 0.5)
bins = report["positive_response"]["response_bins"]
num = 0.0
second_ref = second_gen = 0.0
chi2 = 0.0
max_z = 0.0
se_fraction = []
for b in bins:
    low_edge, high_edge = b["low"], min(b["high"], 250.0)
    num += b["n"] * (b["truth_std"] ** 2 + b["generated_std"] ** 2
                     + (b["generated_mean"] - b["truth_mean"]) ** 2) / (low_edge * high_edge)
    second_ref += b["n"] * (b["truth_std"] ** 2 + b["truth_mean"] ** 2)
    second_gen += b["n"] * (b["generated_std"] ** 2 + b["generated_mean"] ** 2)
    se = math.sqrt((b["truth_std"] ** 2 + b["generated_std"] ** 2) / b["n"])
    z = (b["generated_mean"] - b["truth_mean"]) / se
    chi2 += z * z
    max_z = max(max_z, abs(z))
    se_fraction.append(100 * se / b["truth_mean"])
near("expected independent rms", math.sqrt(num / n), 0.046, 5e-4)
sd_ref = math.sqrt(second_ref / n - t_ref ** 2)
sd_gen = math.sqrt(second_gen / n - t_gen ** 2)
near("sd ref", sd_ref, 4.759, 5e-4)
near("sd gen", sd_gen, 4.830, 5e-4)
se_total = math.sqrt(sd_ref ** 2 + sd_gen ** 2) / math.sqrt(n)
near("se total", se_total, 0.068, 5e-4)
near("dT in se", (t_gen - t_ref) / se_total, 0.7, 0.05)
near("chi2", chi2, 13.0, 0.05)
near("max z", max_z, 2.0, 0.05)
near("se fraction min", min(se_fraction), 4, 0.5)
near("se fraction max", max(se_fraction), 5, 0.5)
near("bin diff min", min(100 * b["mean_bias_fraction"] for b in bins), -7.7, 0.06)
near("bin diff max", max(100 * b["mean_bias_fraction"] for b in bins), 7.7, 0.06)
near("W1 response", report["distribution_metrics"]["total_response_gev"]["wasserstein"], 0.073, 5e-4)
near("W1 response half A", report["distribution_metrics"]["truth_half_floor"]["total_response_gev"]["wasserstein"], 0.135, 5e-4)
near("W1 response half B", report["truth_half_floors"]["response_wasserstein_gev"], 0.147, 5e-4)
near("zero diff lo pp", 100 * boot["zero_fraction_difference"]["low"], 0.19, 5e-3)
near("zero diff hi pp", 100 * boot["zero_fraction_difference"]["high"], 0.76, 5e-3)

# ---- longitudinal activity ----------------------------------------------------
act = report["activity"]
first = report["first_layer"]
near("F ref", first["truth"]["mean_first_active_layer"], 0.510, 5e-4)
near("F gen", first["generated"]["mean_first_active_layer"], 0.735, 5e-4)
near("L ref", act["truth"]["mean_last_active_layer"], 56.20, 5e-3)
near("L gen", act["generated"]["mean_last_active_layer"], 60.62, 5e-3)
near("dL", act["generated"]["mean_last_active_layer"] - act["truth"]["mean_last_active_layer"], 4.42, 5e-3)
active_ref = act["truth"]["mean_active_layers"] * n / ne_ref
active_gen = act["generated"]["mean_active_layers"] * n / ne_gen
near("active ref", active_ref, 54.58, 5e-3)
near("active gen", active_gen, 54.83, 5e-3)
near("d active", active_gen - active_ref, 0.25, 5e-3)
near("span ref", act["truth"]["mean_span"], 56.69, 5e-3)
near("span gen", act["generated"]["mean_span"], 60.88, 5e-3)
near("d span", act["generated"]["mean_span"] - act["truth"]["mean_span"], 4.20, 5e-3)
g_ref, g_gen = act["truth"]["mean_gaps"], act["generated"]["mean_gaps"]
near("G ref", g_ref, 2.10, 5e-3)
near("G gen", g_gen, 6.05, 5e-3)
near("dG", g_gen - g_ref, 3.95, 5e-3)
near("span - active = G (ref)", act["truth"]["mean_span"] - active_ref, g_ref, 1e-6)
near("span - active = G (gen)", act["generated"]["mean_span"] - active_gen, g_gen, 1e-6)
f_ref, f_gen = act["truth"]["gap_fraction"], act["generated"]["gap_fraction"]
near("f ref %", 100 * f_ref, 52.43, 5e-3)
near("f gen %", 100 * f_gen, 93.53, 5e-3)
near("ecal start ref %", 100 * first["truth"]["ecal_start_prevalence"], 93.81, 5e-3)
near("ecal start gen %", 100 * first["generated"]["ecal_start_prevalence"], 92.53, 5e-3)
depth = report["distribution_metrics"]["depth_centroid_layer"]
near("depth ref nonempty", depth["truth_mean"] * n / ne_ref, 14.15, 5e-3)
near("depth gen nonempty", depth["generated_mean"] * n / ne_gen, 14.14, 5e-3)

# ---- connectivity and the bound -----------------------------------------------
topo = report["topology"]
hits_ref = topo["truth"]["hit_count_mean"] * n / ne_ref
hits_gen = topo["generated"]["hit_count_mean"] * n / ne_gen
near("hits ref", hits_ref, 1617.6, 0.05)
near("hits gen", hits_gen, 1588.8, 0.05)
near("d hits", hits_gen - hits_ref, -28.7, 0.06)
near("d hits %", 100 * (hits_gen / hits_ref - 1), -1.8, 0.05)
m_ref = topo["truth"]["connected_components_mean"] * n / ne_ref
m_gen = topo["generated"]["connected_components_mean"] * n / ne_gen
near("m ref", m_ref, 23.42, 5e-3)
near("m gen", m_gen, 59.39, 5e-3)
dm = m_gen - m_ref
near("dm", dm, 35.97, 5e-3)
near("m ratio", m_gen / m_ref, 2.5, 0.06)
near("largest ref %", 100 * topo["truth"]["largest_component_fraction_mean"] * n / ne_ref, 94.90, 5e-3)
near("largest gen %", 100 * topo["generated"]["largest_component_fraction_mean"] * n / ne_gen, 88.87, 5e-3)
near("Q ref lo", m_ref - 1 - g_ref, 20.32, 5e-3)
near("Q ref hi", m_ref - 1 - f_ref, 21.89, 6e-3)
near("Q gen lo", m_gen - 1 - g_gen, 52.34, 5e-3)
near("Q gen hi", m_gen - 1 - f_gen, 57.45, 5e-3)
dq_lo = dm - g_gen + f_ref
dq_hi = dm + g_ref - f_gen
near("dQ lo", dq_lo, 30.45, 5e-3)
near("dQ hi", dq_hi, 37.14, 5e-3)
near("dQ lo share %", 100 * dq_lo / dm, 84.6, 0.05)
near("dR hi", dm - dq_lo, 5.52, 5e-3)
near("dR hi share %", 100 * (dm - dq_lo) / dm, 15.4, 0.05)
near("dR lo", dm - dq_hi, -1.17, 5e-3)
near("W1 hits", report["counts"]["hit_count_wasserstein"], 58.68, 5e-3)
near("W1 hits lo", boot["hit_count_wasserstein"]["low"], 51.47, 5e-3)
near("W1 hits hi", boot["hit_count_wasserstein"]["high"], 66.92, 5e-3)
near("W1 hits half A", report["truth_half_floors"]["hit_count_wasserstein"], 13.78, 5e-3)
near("W1 hits half B", report["distribution_metrics"]["truth_half_floor"]["hit_count"]["wasserstein"], 15.82, 5e-3)
near("edge ref", topo["truth"]["edge_cooccupancy_mean"], 0.1458, 5e-5)
near("edge gen", topo["generated"]["edge_cooccupancy_mean"], 0.1375, 5e-5)
cell = report["distribution_metrics"]["positive_cell_energy_gev"]
near("MeV per channel ref", 1000 * cell["truth_mean"], 2.7, 0.05)
near("MeV per channel gen", 1000 * cell["generated_mean"], 2.8, 0.05)

# ---- distribution table -------------------------------------------------------
dm_all = report["distribution_metrics"]
table = {
    "total_response_gev": (4.324, 4.369, 0.073, 0.135, 0.5),
    "x_centroid_mm": (-906.8, -902.8, 4.50, 5.69, 0.8),
    "y_centroid_mm": (-33.2, -31.9, 1.71, 2.15, 0.8),
    "hit_count": (1602.5, 1566.3, 58.7, 15.8, 3.7),
    "depth_centroid_layer": (14.02, 13.94, 0.971, 0.155, 6.3),
    "top1_fraction": (0.1549, 0.1659, 0.0130, 0.0021, 6.3),
    "late_fraction": (0.0221, 0.0252, 0.0083, 0.0013, 6.5),
    "radial_rms_mm": (86.34, 83.48, 3.34, 0.49, 6.9),
    "ecal_fraction": (0.2354, 0.2626, 0.0280, 0.0029, 9.5),
}
for key, (a, b, w, h, r) in table.items():
    entry = dm_all[key]
    half = dm_all["truth_half_floor"][key]["wasserstein"]
    near(f"{key} ref", entry["truth_mean"], a, 0.6 * 10 ** -len(str(abs(a)).split(".")[-1]))
    near(f"{key} gen", entry["generated_mean"], b, 0.6 * 10 ** -len(str(abs(b)).split(".")[-1]))
    near(f"{key} W1", entry["wasserstein"], w, 0.6 * 10 ** -len(str(w).split(".")[-1]))
    near(f"{key} half", half, h, 0.6 * 10 ** -len(str(h).split(".")[-1]))
    near(f"{key} ratio", entry["wasserstein"] / half, r, 0.06)
rms_ref = dm_all["radial_rms_mm"]["truth_mean"] * n / ne_ref
rms_gen = dm_all["radial_rms_mm"]["generated_mean"] * n / ne_gen
near("rms narrower %", 100 * (1 - rms_gen / rms_ref), 3, 0.5)
corr = report["correlations"]
near("corr frobenius", corr["correlation_frobenius"], 3.52, 5e-3)
near("corr half", corr["truth_half_floor_correlation_frobenius"], 1.98, 5e-3)

# ---- classifier, closure, timing ----------------------------------------------
c2st = report["c2st"]
near("auroc high", c2st["high_level"]["auroc_mean"], 0.775, 5e-4)
near("auroc low", c2st["low_level"]["auroc_mean"], 0.791, 5e-4)
near("auroc profile", c2st["profile_aware"]["auroc_mean"], 0.856, 5e-4)
near("auroc control", c2st["condition_only"]["auroc_mean"], 0.464, 5e-4)
near("gate", c2st["high_level"]["gate_value"], 0.65, 0)
inv = report["structural_invariants"]
near("layer residual", inv["layer_closure_max_gev"], 3.05e-5, 5e-8)
near("event residual", inv["event_closure_max_gev"], 1.14e-5, 5e-8)
timing = report["timing"]
analysis = sum(timing["stage_seconds"].values())
near("total s", timing["total_seconds"], 3442, 0.5)
near("analysis s", analysis, 1009, 0.5)
near("generation upper s", (timing["total_seconds"] - analysis) / n, 0.24, 5e-3)

# ---- training history ---------------------------------------------------------
with (ROOT / "data/training/calibrated_lr3e4_history.csv").open(newline="", encoding="utf-8") as handle:
    rows = list(csv.DictReader(handle))
val = np.array([float(r["validation_loss"]) for r in rows])
epochs = np.array([int(r["epoch"]) for r in rows])
near("best epoch", epochs[val.argmin()], 90, 0)
near("improvement", val[0] - val.min(), 0.20, 5e-3)
near("improvement %", 100 * (val[0] - val.min()) / val[0], 4, 0.5)
near("mean epoch change", np.abs(np.diff(val)).mean(), 0.04, 5e-3)
order = np.argsort(val)
near("next best margin", val[order[1]] - val[order[0]], 0.008, 5e-4)
near("next best epochs", sorted(int(e) for e in epochs[order[1:3]]) == [100, 111], True, 0)

# ---- geometry -----------------------------------------------------------------
geometry = np.load(ROOT / "data/geometry/readout_geometry.npz")
pos, layer, mult = geometry["positions_mm"], geometry["layer_index"], geometry["physical_position_count"]
zc = np.array([pos[layer == i, 2].mean() for i in range(65)])
xc = np.array([pos[layer == i, 0].mean() for i in range(65)])
pitch = math.hypot(np.diff(xc)[1:].mean(), np.diff(zc)[1:].mean())
near("layer pitch", pitch, 24.9, 0.05)
near("hcal depth m", math.hypot(zc[-1] - zc[1], xc[-1] - xc[1]) / 1000, 1.57, 5e-3)
near("ecal distance m", math.hypot(zc[0], xc[0]) / 1000, 35.7, 0.05)
near("axis mrad", 1000 * math.atan2(xc[0], zc[0]), -25.0, 0.05)


def nearest(points: np.ndarray) -> np.ndarray:
    d = np.sqrt(((points[:, None] - points[None]) ** 2).sum(-1))
    np.fill_diagonal(d, np.inf)
    return d.min(axis=1)


near("ecal pitch", float(np.median(nearest(pos[layer == 0]))), 30.3, 0.05)
near("hcal spacing", float(np.median(nearest(pos[layer == 1]))), 54, 0.5)
hcal = layer > 0
near("multi ids", int((mult[hcal] > 1).sum()), 2400, 0)
near("mult 2", int((mult == 2).sum()), 1950, 0)
near("mult 3", int((mult == 3).sum()), 444, 0)
near("mult 4", int((mult == 4).sum()), 6, 0)

# ---- strings that must appear verbatim ----------------------------------------
expect("abstract", "23.42 to 59.39", "at most 5.52 of these 35.97", "at least 30.45 (84.6\\%)", "AUROC of 0.775")
expect("bound", "30.45\\;\\leq\\;\\Delta\\overline Q\\;\\leq\\;37.14",
       "$20.32\\leq\\overline Q_{\\rm ref}\\leq21.89$", "$52.34\\leq\\overline Q_{\\rm gen}\\leq57.45$")
expect("classifier", "0.500 for the control and 0.893")
expect("graph", "54{,}320", "53{,}600", "107,920")
expect("samples", "764,940", "612,482", "76,158", "76,300", "26,624", "6,656", "4.35\\%")

print(f"checked {checked} items")
if missing:
    print("FAILED:")
    for item in missing:
        print("  ", item)
    sys.exit(1)
print("all quoted numbers reproduce from the repository data")
