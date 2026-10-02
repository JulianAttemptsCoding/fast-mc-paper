"""Apply source-checked HEP-reader corrections to the existing main.tex."""
from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / "main.tex"
raw = path.read_bytes()
assert b"\r\n" in raw  # Historical source contains both CRLF and LF paragraphs.
before = hashlib.sha256(raw).hexdigest()
assert before == "9d0510a62d243db574d42b7d3640d6c639878cf49fcf675578c44e0bd728e645"
tex = raw.decode("utf-8")
edits = []


def change(old: str, new: str, label: str) -> None:
    global tex
    variants = [(old.replace("\n", "\r\n"), new.replace("\n", "\r\n")), (old, new)]
    matches = [(a, b) for a, b in variants if tex.count(a) == 1]
    assert matches, (label, [tex.count(a) for a, _ in variants])
    a, b = matches[0]
    tex = tex.replace(a, b)
    edits.append(label)


change(
    "for a hierarchical neutron generator in an ePIC Zero-Degree Calorimeter simulation.",
    "for a hierarchical flow-matching shower generator in an ePIC Zero-Degree Calorimeter simulation.",
    "abstract model type",
)
change(
    "High-level classifier AUROC is 0.775, above the recorded 0.65 screen; a condition-only control gives 0.464 with row splits that can separate matched pairs.",
    "A row-split classifier distinguishes high-level summaries (AUROC 0.775), but its condition-only control fails (0.464); the classifier score is not a calibrated fidelity test.",
    "abstract classifier meaning",
)
change(
    "At the Electron--Ion Collider, a zero-degree calorimeter (ZDC) measures neutral particles near the outgoing hadron beam. A proposed ePIC SiPM-on-tile design reconstructs neutron energy and angle from hit energies and positions~\\cite{epiczdc}. A surrogate's spatial pattern could therefore affect reconstruction, which this study does not test. Here the hit pattern (mathematical support) comprises stored channels with positive deposit. Its size is the active-channel count, not digitized occupancy.",
    "At the Electron--Ion Collider, a zero-degree calorimeter (ZDC) measures neutral particles near the outgoing hadron beam. Detailed Geant4 transport is useful for detector studies but costly to repeat at scale; a fast generator must reproduce more than a mean energy response. A proposed ePIC SiPM-on-tile design reconstructs neutron energy and angle from hit energies and positions~\\cite{epiczdc}, so spatial discrepancies may matter for reconstruction. We test that possibility at the level of stored deposits, without claiming a reconstructed performance effect. A hit here means any stored channel with positive energy; it is not a digitized hit.",
    "intro motivation and hit definition",
)
change(
    "We study a generator that samples total deposit, active layers and deposited-energy hit patterns in sequence. We ask whether similar mean deposits and hit counts imply similar depth and graph structure. They do not here: the last deposit occurs later, more layers are skipped, and many extra graph-connected groups remain after accounting for empty-layer separations. Their reconstruction effect is unmeasured; the diagnostic complements established co-activation tests.\n\nThis evaluation study uses one checkpoint and 10,000 validation conditions; it tests neither architecture superiority nor detector performance.",
    "We study a generator that samples total deposit, active layers and deposited-energy hit patterns in sequence. The question is whether similar mean deposits and hit counts imply similar shower depth and graph structure. They do not in this case: the last deposit occurs later, more layers are skipped, and many extra graph-connected groups remain after accounting for empty-layer separations. We describe the target and sample, trace the physical meaning of each generation stage, and compare response with longitudinal and graph observables. This is an aggregate reanalysis of one checkpoint on 10,000 repeatedly inspected validation conditions. It tests neither architecture superiority nor detector performance; its graph diagnostic complements established co-activation tests.",
    "intro contributions and study status",
)
change(
    "ECAL centroids have 30.3\\,mm horizontal pitch; HCAL mean layer coordinates have median $z$ spacing 24.9\\,mm and first-to-last span 1.57\\,m.",
    "ECAL centroids have 30.3\\,mm horizontal pitch; HCAL nearest-centroid spacing within a layer has median 54.2\\,mm. HCAL mean layer coordinates have median $z$ spacing 24.9\\,mm and first-to-last span 1.57\\,m.",
    "HCAL lateral scale",
)
change(
    "The ECAL lies at $z=35.73$\\,m in the stored frame (Fig.~\\ref{fig:geometry}).",
    "The ECAL lies at $z=35.73$\\,m in the stored frame (Fig.~\\ref{fig:geometry}). The project production record reports a fixed neutron-gun vertex at $(-917.41,-30.0,35488.91)$\\,mm, about 0.24\\,m upstream of that plane; this value has not been checked against the released events. With a fixed vertex, direction constrains the nominal impact trajectory, although the actual entry-point distribution was not retained.",
    "fixed vertex and impact scope",
)
change(
    "Production materials and coordinate origin are undocumented, so layer index cannot be converted to radiation lengths $X_0$ or nuclear interaction lengths $\\lambda_I$.",
    "Project documents describe layer 0 as nominally LYSO and the HCAL as nominally steel/scintillator, but the production material map is not in the released evidence. The cited SiPM-on-tile study models an iron/scintillator sampling calorimeter without this layer-0 section~\\cite{epiczdc}; its material scales and reconstruction cuts cannot be assigned to this production. Layer index therefore cannot be converted reliably to radiation lengths $X_0$ or interaction lengths $\\lambda_I$.",
    "nominal material versus cited design",
)
change(
    "Left: horizontal projection of 65 layers, with a guide of $x/z=-0.025$, a 25-mrad slope comparable to the nominal EIC crossing angle (unequal axis scales). Center/right: ECAL/HCAL faces, colored by positions per ID. The stored coordinate frame does not establish beam-axis alignment; ID multiplicity does not establish electronic ganging.",
    "Left: horizontal projection of 65 stored layers; the nearly flat rows in this coordinate frame should not be read as a beam-axis direction. Center/right: ECAL/HCAL faces, colored by positions per ID. ID multiplicity does not establish electronic ganging.",
    "geometry figure caption",
)
change(
    "The same three-dimensional nearest-centroid graph supplies model messages and connects positive-deposit channels for diagnostics; its links are not verified physical tile neighbors.",
    "The full graph is connected, including lateral connectivity within every layer. The same three-dimensional nearest-centroid graph supplies model messages and connects positive-deposit channels for diagnostics; its links are not verified physical tile neighbors. Consequently, extra components arise from the occupied hit pattern on this graph, not disconnected pieces of the full graph.",
    "full graph connectivity",
)
change("builds a stored shower readout in physical order", "builds a stored shower readout from coarse to fine", "architecture order wording")
change(
    "Response includes empty showers and eight 25\\,GeV energy bins.",
    "Response metrics include empty showers; eight 25\\,GeV bins show its energy dependence.",
    "evaluation scope sentence",
)
change(
    "The pooled standard deviations are 4.759 and 4.830\\,GeV.",
    "The pooled standard deviations are 4.759 and 4.830\\,GeV.",
    "noop guard",
) if False else None
change(
    "Table~\\ref{tab:energy_bins} gives binwise means and widths; the pooled standard deviations are 4.759 and 4.830\\,GeV.",
    "Table~\\ref{tab:energy_bins} gives binwise means and widths; the pooled standard deviations are 4.759\\,GeV for Geant4 and 4.830\\,GeV for the generator.",
    "pooled width order",
)
change(
    "This tests a different, energy-normalized quantity from the 0.045\\,GeV mean difference; it does not supply that difference's paired covariance.",
    "This tests a different, energy-normalized quantity from the 0.045\\,GeV mean difference. The latter is smaller than the 0.068\\,GeV standard-error scale obtained by treating the two samples as independent; the exact paired standard error needs their unretained covariance.",
    "response sampling scale",
)
change(
    "For nonempty showers, mean energy-weighted depth, $\\sum_\\ell\\ell B_\\ell/\\max(T,10^{-9}\\GeV)$, is instead 14.14 for the generator and 14.15 for Geant4. Including empty events as zeros gives 13.94 and 14.02, respectively. This distinguishes occupied extent from energy-weighted depth, but does not determine the energy carried by disconnected components.",
    "For nonempty showers, mean energy-weighted depth, $\\sum_\\ell\\ell B_\\ell/\\max(T,10^{-9}\\GeV)$, is 14.14 for the generator and 14.15 for Geant4. Including empty events as zeros gives 13.94 and 14.02, respectively. Yet the all-event depth distributions have $W_1=0.971$ layers, versus a 0.155-layer Geant4 half-split scale. Thus similar means hide a depth-distribution difference, as they do for occupied extent. The half-split is a descriptive scale, not a significance threshold; component energies remain unmeasured.",
    "depth distribution versus mean",
)
change(
    "The bound leaves 30.45--37.14 excess groups within contiguous active-layer segments (at least 84.6\\% of the total).",
    "The aggregate bounds give $\\overline Q_{\\rm gen}\\geq52.34$ and $\\overline Q_{\\rm ref}\\leq21.89$. Hence 30.45--37.14 of the 35.97 excess groups remain within contiguous active-layer segments (at least 84.6\\%). The upper bound can exceed the total excess because the generator may have fewer segments than the reference. Both samples retain a dominant connected group (88.87\\% and 94.90\\% of active channels on average); the extra groups lie outside it, but their sizes and energies are unmeasured.",
    "main result explanation",
)
change(
    "The fraction of directed graph edges whose endpoints are both occupied averages 0.1375 for the generator and 0.1458 for Geant4 over all 10,000 events. This measures local co-occupancy on the same graph, but is not normalized for occupancy and does not isolate a correlation discrepancy.",
    "Edge co-occupancy is 0.1375 for the generator and 0.1458 for Geant4. Because this fraction is not occupancy-normalized, we do not interpret its difference as a correlation effect.",
    "edge measure scope",
)
change(
    "The incident four-vector omits an explicit impact position. Whether direction determines that position depends on the production vertex and recording surface, which need verification. Position-conditioned residuals and the joint empty-shower contingency table would test whether conditioning and geometric acceptance are learned; marginal empty fractions alone cannot answer this.",
    "The model has no explicit impact-position input. The recorded fixed gun vertex makes direction informative about the nominal entry point, but the production surface and event-level positions are not available here. Position-conditioned residuals and the joint empty-shower contingency table would test geometric acceptance; marginal empty fractions alone cannot answer this.",
    "impact limitation corrected",
)
change(
    "Training loss averages updating minibatches, whereas validation uses the epoch-end model in the available implementation; historical runtime identity is unverified. Response-tail studies require counts of generated draws clipped by the cap and reference deposits above it. Numerical sensitivity requires a solver-step study. A locked bank with verified identities and repeated generation at fixed conditions is also needed.",
    "Response-tail studies require counts of generated draws clipped by the cap and reference deposits above it. Numerical sensitivity requires a solver-step study. A locked bank with verified identities and repeated generation at fixed conditions is also needed.",
    "remove irrelevant train validation averaging",
)
change(
    "\\subsection{Computational performance and detector applications}",
    "\\subsection{Timing and detector applications}",
    "avoid unsupported performance heading",
)
change(
    "Intervals for these differences are unavailable.",
    "Exact paired intervals for these differences are unavailable from the aggregate summary.",
    "bin uncertainty wording",
)
change(
    "Definitions on an illustrative graph, not shower data. Left: active layers (filled), interior empty layers (hatched), first and last layers $F,L$, gap count $G$ and contiguous active-layer segments $R$. Right: all four layers are active ($R=1$), but occupied channels form three graph-connected groups ($m=3$), so $Q=m-R=2$. Pale edges join adjacent nodes of this toy grid; the detector graph is defined in Sec.~\\ref{sec:data}.",
    "Top panels are illustrations, not events: (a) active layers (filled), interior empty layers (hatched), span, gap count $G$ and contiguous segments $R$; (b) three graph-connected groups despite four consecutive active layers ($R=1$, $m=3$, $Q=2$). Bottom panels compare source-bound nonempty-sample means for last active layer, skipped layers and graph groups. Bar lengths use separate scales; labels give the absolute values. No uncertainty estimates for these structural means were retained.",
    "data-plus-definition figure caption",
)

path.write_bytes(tex.encode("utf-8"))
after = hashlib.sha256(path.read_bytes()).hexdigest()
record = {"utc": datetime.now(timezone.utc).isoformat(), "command": "python -X utf8 audit/revise_claude_review_20261002.py", "before_main_sha256": before, "after_main_sha256": after, "edits": edits, "equations_and_numeric_tables": "not intentionally changed", "environment": "Windows Python 3.13, local paper checkout"}
(root / "audit/claude_review_source_edits_20261002.json").write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
(root / "audit/claude_review_source_edits_20261002.md").write_text("# Source edits from 2 October review\n\n" + "\n".join("- " + item for item in edits) + "\n\nNo new event-level or threshold result was inferred. Exact hashes are in the JSON twin.\n", encoding="utf-8")
print(json.dumps({"before": before, "after": after, "edits": len(edits)}, indent=2))
