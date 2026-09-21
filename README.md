# Sparse conditional generation for a Zero Degree Calorimeter

This repository contains the English LaTeX manuscript, frozen model configuration, aggregate development reports, event-independent geometry, figure builder, review record, and build audit for Julian Juan's Fast MC project.

The manuscript is a development-bank study of a raw deposited-energy surrogate. It reports decoder guarantees and observed discrepancies without claiming final physics fidelity or measured acceleration. The fixed 10,000-condition sample has been inspected repeatedly and is therefore treated as development data. The nominal test set is retired and is not used for the reported figures.

## Build

Requirements:

- Python 3 with `matplotlib` and `numpy`
- `pdflatex`
- `biber`
- Poppler tools for the optional PDF checks

On Windows PowerShell:

```powershell
.\build.ps1
```

The script regenerates every figure from the pinned aggregate reports, compiles the bibliography and manuscript, checks the PDF text, and writes:

```text
output/fast_mc_zdc_manuscript.pdf
```

The equivalent manual sequence is:

```text
python scripts/build_figures.py
pdflatex -interaction=nonstopmode -halt-on-error main.tex
biber main
pdflatex -interaction=nonstopmode -halt-on-error main.tex
pdflatex -interaction=nonstopmode -halt-on-error main.tex
```

## Repository map

- `main.tex`: manuscript source
- `references.bib`: bibliography
- `scripts/build_figures.py`: deterministic figure generator
- `data/configs/`: frozen portable V3-SUP configuration
- `data/reports/`: aggregate source reports used by the figure generator
- `data/geometry/`: event-independent frozen readout geometry
- `figures/`: generated manuscript figures and provenance manifest
- `reviews/`: all six supplied referee and reproducibility audits, preserved verbatim
- `audit/reviewer_response.md`: first-round disposition
- `audit/reviewer_response_round2.md`: second-round consolidated disposition
- `audit/final_build_audit.*`: hashes and final QA record
- `archive/`: earlier paper and specification artifacts retained for provenance
- `STATUS.md`: unresolved experiments and claim boundary

## Scientific status

The current evidence supports a narrow conclusion: exact-size sparse decoding and generated-budget closure can coexist with substantial distributional error. The full-data V3-SUP continuation used 551,234 generator-role events; 26,624 events applies only to the pilot baseline and short component screens. Longitudinal gaps, readout-graph fragmentation, reduced channel occupancy, and the S2 zero-deposit anomaly are development-bank results. The historical shower-only C2ST is excluded because it used random pair splitting and omitted the condition.

Final claims require a locked evaluation bank, pair-grouped condition-aware tests, three independent training seeds per frozen condition, complete Geant4 and detector provenance, fixed-condition repeated showers, matched baselines, reconstruction studies, and end-to-end timing. See `STATUS.md` for the full list.

The underlying collaboration-owned Geant4 event file and model checkpoints are not redistributed here. The aggregate JSON reports are sufficient to rebuild the paper figures, but not to retrain the model or reproduce the original simulation.
