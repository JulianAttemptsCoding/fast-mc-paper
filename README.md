# Sparse conditional generation for a Zero Degree Calorimeter

This repository contains the English LaTeX manuscript, aggregate development reports, figure builder, review record, and build audit for Julian Juan's Fast MC project.

The manuscript is a preliminary development-bank study. It reports structural guarantees and observed failures without claiming final physics fidelity or measured acceleration. The fixed 10,000-condition sample has been inspected repeatedly and is therefore treated as development data. The nominal test set is not used for the reported figures.

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
- `data/reports/`: aggregate source reports used by the figure generator
- `figures/`: generated manuscript figures and provenance manifest
- `reviews/`: the three supplied referee and reproducibility audits, preserved verbatim
- `audit/reviewer_response.md`: issue-by-issue disposition
- `audit/final_build_audit.*`: hashes and final QA record
- `archive/`: earlier paper and specification artifacts retained for provenance

## Scientific status

The current evidence supports a narrower conclusion: exact sparse decoding and generated-budget closure can coexist with substantial distributional error. Classifier separation, longitudinal fragmentation, and the failed S2 response-head screen remain explicit negative results. Final claims require a locked evaluation bank, three independent training seeds per frozen condition, complete Geant4 and detector provenance, fixed-condition repeated showers, matched baselines, reconstruction studies, and end-to-end timing.

The underlying collaboration-owned Geant4 event file and model checkpoints are not redistributed here. The aggregate JSON reports are sufficient to rebuild the paper figures, but not to retrain the model or reproduce the original simulation.
