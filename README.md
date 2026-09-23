# Longitudinal Gaps and Readout Connectivity in a Pilot Generative Model of Zero-Degree Calorimeter Showers

Version 0.10.0 is a case study of one pilot-trained calorimeter model. On a repeatedly inspected validation bank, its showers extend farther downstream and contain more inactive layers within their occupied span than the Geant4 reference, despite similar mean active-layer counts. Mean graph-component counts also differ, but the adjacent-layer graph makes part of that difference inseparable from longitudinal gaps in the retained aggregates. The paper explains the generation path from incident four-vector to 6,790 deposited energies. The recorded high-level classifier AUROC of 0.775 fails its declared 0.65 gate; its row-wise split limits interpretation. The paper does not establish structural statistical significance, performance after digitization or retraining, acceleration, or detector readiness. Paired bootstrap intervals are available for the separate zero-deposit fraction and hit-count distance.

## Fixed case

- Run `dicos-f-02`, epoch 90; training seed 20260723.
- 26,624 pilot training events; 6,656 pilot validation events for the selection objective.
- 10,000-condition diagnostic bank from canonical validation, 50--250 GeV; repeatedly inspected and not an untouched test.
- Checkpoint SHA-256: `491284c7423f365230d34b0443f95aa4888ec770bdc673c4c979897bad8acbce`.
- Configuration SHA-256: `116bc8c220b07ce54ae07196bdd6ed8e835775c8c937182a209a799dc94ae9c5`.
- The 104-row history covers epochs 11--114. One declared post-90 continuation did not improve the minimum. An incorrect scheduler variant remains excluded.

## Build and QA

Requirements: Python with NumPy, Matplotlib and Pillow; pdflatex, biber and Poppler on PATH.

```powershell
.\build.ps1
$Iteration = Read-Host "Unused QA iteration number"
python scripts/full_manuscript_qa.py --iteration $Iteration --focus "scientific revision" --disposition "source-bound checks"
```

Choose an unused iteration number; historical records cannot be overwritten. The build stops on a failed native command before replacing `output/fast_mc_zdc_manuscript.pdf`. The QA checks evidence hashes, source-bound data roles, reported arithmetic, citation/label resolution, every figure and every rendered page. Automated raster checks are not human visual review. A final release audit additionally requires a hash-matched visual-review record and rejects stale source/PDF hashes.

## Evidence and reproducibility

- `main.tex`, `references.bib`: revised manuscript and primary literature.
- `data/reports/`: immutable aggregate diagnostic report and provenance.
- `data/provenance/source_evidence.json`: training-population/config binding, preparation counts, evaluator policy and source-file hashes.
- `data/training/`, `data/geometry/`: recorded history and event-independent geometry.
- `scripts/build_figures.py`, `figures/manifest.json`: reproducible figures and input/output hashes.
- `audit/revision_20260921.*`: corrections, failed attempts, research and decisions.
- `audit/framing_revision_20260921.*`: HEP/computational-physics framing criteria and pre-November-2025 style references.
- `audit/adversarial_revision_20260922.*`: historical disposition of the earlier supplied adversarial audits; its zero-uncertainty statement is superseded.
- `audit/adversarial_revision_round3_20260922.*`: historical disposition of the preceding two audits, including the recovered zero-fraction interval and graph confound.
- `audit/adversarial_revision_round4_20260923.*`: disposition of the subsequent audits, including the restored classifier results and mechanism corrections.
- `audit/claim_register_20260922.*`: current claim-by-claim disposition and sources.
- `audit/model_exposition_20260922.*`: source-hash-bound audit of the model mechanisms described in the manuscript.
- `audit/sentence_evidence_20260922.*`: section-by-section evidence and clarity review for the complete manuscript.
- `audit/iterations/`: historical and current build checks; only a hash-matched current record applies to the current PDF.
- `archive/pre_revision_20260921/`: original v0.3.0 source/PDF/build snapshot.
- `reviews/`: the nine earlier reviews, unchanged; their previous dispositions are historical.
- `STATUS.md`: supported claim and outstanding research for broader claims.

The package rebuilds the paper from aggregate evidence. It does not redistribute the collaboration-owned event file or checkpoint and cannot reproduce training or event-level tests. No source data, frozen model configuration, or scientific threshold was modified by this manuscript revision. Intended future EIC ZDC use is project motivation, not a detector-identity or detector-equivalence claim.
