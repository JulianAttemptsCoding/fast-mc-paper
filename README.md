# Auditing a hierarchical generator for sparse calorimeter readout deposits

This repository contains Julian Juan's English LaTeX manuscript and its complete public build package. The paper studies a hierarchical Fast MC generator for raw Geant4 neutron energy deposits in a fixed 6,790-channel Zero Degree Calorimeter readout.

The paper is a diagnostic case study. It shows that exact sampled counts and numerical energy-budget closure can coexist with incorrect longitudinal and graph dependence. It does not claim physics fidelity, acceleration, or performance on an untouched test set.

## Accepted artifact

- Run: `dicos-f-02`
- Checkpoint: epoch 90, selected by the minimum teacher-forced validation objective over the recorded lineage through epoch 114
- Generator training seed: `20260723`
- Checkpoint SHA-256: `491284c7423f365230d34b0443f95aa4888ec770bdc673c4c979897bad8acbce`
- Frozen configuration SHA-256: `116bc8c220b07ce54ae07196bdd6ed8e835775c8c937182a209a799dc94ae9c5`
- Evaluation: repeatedly inspected 10,000-condition validation bank over 50--250 GeV; zero nominal-test events

The old epoch-12 snapshot and the B0, M0, and S2 screens are not part of the scientific comparison. Their training states or controls do not support a clean manuscript claim. Shower-aware C2ST outputs from the existing evaluator are also excluded. The retained condition-only AUROC of 0.500 is a pipeline sanity control with no shower information.

## Build

Requirements are Python 3 with `matplotlib`, `numpy`, and Pillow; `pdflatex`; `biber`; and Poppler. On Windows PowerShell:

```powershell
.\build.ps1
```

The command regenerates all six figures, compiles the bibliography and manuscript, scans the LaTeX log and PDF text, and writes:

```text
output/fast_mc_zdc_manuscript.pdf
```

Run one complete adversarial QA pass with:

```powershell
python scripts/full_manuscript_qa.py --iteration 1 --focus "scope and claims" --disposition "reviewed"
```

Each pass rebuilds the full paper, checks all headline values against the epoch-90 aggregate, verifies hashes and split arithmetic, resolves citations and labels, scans excluded terms, validates every generated figure, rasterizes every PDF page, checks page ink and clipping margins, and records JSON and Markdown evidence under `audit/iterations/`.

## Repository map

- `main.tex`: manuscript source
- `references.bib`: primary-source bibliography
- `scripts/build_figures.py`: deterministic generator for all manuscript figures
- `scripts/full_manuscript_qa.py`: full manuscript and rendered-PDF audit
- `data/reports/dicos-f-02_epoch90.json`: aggregate development-bank report
- `data/reports/dicos-f-02_epoch90.provenance.json`: checkpoint and report provenance
- `data/training/`: accepted-family training history and provenance
- `data/geometry/`: event-independent readout geometry
- `figures/`: six generated figures and hash manifest
- `reviews/`: all nine supplied audits, preserved verbatim
- `audit/reviewer_response_round3.md`: consolidated disposition of the latest audits
- `audit/literature_benchmark.md`: comparison with recent HEP calorimeter-surrogate work
- `audit/iterations/`: 20 complete QA records
- `audit/final_build_audit.*`: final release hashes and QA summary
- `STATUS.md`: supported claims and missing experiments

The collaboration-owned Geant4 event file and model checkpoint are not redistributed. The public aggregates reproduce the figures and quoted battery statistics, but cannot retrain the model or reconstruct event-level tests.
