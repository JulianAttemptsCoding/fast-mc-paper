# English Fast MC manuscript audit — 2026-09-20

## Scope and status

- Output: `paper/CBSC_ZDC_manuscript.pdf` (A4, 9 pages).
- Source: `paper/CBSC_ZDC_manuscript.tex` and `paper/CBSC_ZDC_manuscript.bib`.
- Scientific status: validation study and manuscript draft. Physics fidelity and end-to-end acceleration are not established.
- Data use: all numerical plots use frozen local validation reports with 10,000 validation truth conditions and zero test events. No training or remote job was launched.
- The supplied SSP PDF informed only the broad narrative shape. Its instructions, model, and numerical results were not imported.

## Literature basis

The related-work section uses primary sources for Geant4, CaloChallenge 2022, the ALICE ZDC flow-matching study, L2LFlows, CaloGraph, CaloDiffusion, CaloPointFlow II, conditional flow matching, and Gumbel-Top-k sampling. Nine bibliography entries resolve in the rendered PDF.

## Figures

`paper/build_manuscript_figures.py` regenerates one architecture schematic and five validation plots under `exhibition/current/manuscript/`:

1. Hierarchical sampling and sparse decode schematic.
2. High-, low-, and profile-aware classifier two-sample AUROC.
3. Conditional response bias and resolution difference in eight 25-GeV bins.
4. Mean longitudinal response, with the HCAL development and log-scale tail shown separately.
5. Interior-gap fraction, mean gap count, and graph connected components.
6. Zero-response fractions, including the failed S2 screen.

The figure manifest records source and output SHA-256 hashes and states `test_events_used: 0`.

## Render and QA iterations

1. First LaTeX render: nine pages; unresolved references before the bibliography pass; figures 3 and 4 landed on a float-only page with excessive vertical separation.
2. Bibliography and cross-reference pass: nine references resolved; visual review of every page found the float-only layout and one unprofessional sentence about the supplied student report.
3. Scientific/layout correction: replaced the schematic output-density equality with a joint latent factorization, removed the student-report sentence, corrected S3 delta rounding, forced figures into their result sections, and replaced non-ASCII plot-range punctuation.
4. Figure revision: added the architecture schematic, checked it visually, and reflowed the manuscript. A redundant appendix created a nearly empty tenth page and was removed.
5. Final pass: visually checked all nine A4 pages. No clipped content, overlapping elements, unresolved citations/references, overfull boxes, underfull boxes, or LaTeX warnings remain. `pdfinfo` reports nine pages and 984,722 bytes.

## Focused verification

- `python paper/build_manuscript_figures.py`: pass.
- `python -m py_compile paper/build_manuscript_figures.py`: pass.
- Two final `pdflatex -interaction=nonstopmode -halt-on-error` passes: pass.
- PDF text scan for `??`, undefined citations, and undefined references: pass.
- PDF log scan for overfull/underfull boxes and warnings: pass.
- All nine final pages visually inspected after Poppler rendering: pass.
- `python exhibition/build_metrics_catalog.py`: blocked by a pre-existing missing dashboard source file, `dashboard/public/data/dicos-c-05-calibrated-lr3e5_joint_epoch_0036.json`.
- `python -m pytest -q tests/test_exhibition_metrics.py`: 4 passed, 5 failed. The manuscript category was added to the gallery classifier; remaining failures are caused by the same missing dashboard file and a pre-existing escaped visual under `exhibition/live_remote/`.

## Final hashes

- PDF: `db973fa160712b159236785308da447cbeca890d2b412791ec64f7bfe07d6193`
- TeX: `9fae50b3b8dbae101769eaeb33125ac81328343b0901e65156fdcda032512fa9`
- BibTeX: `eb6060444cd1ffd3286564f9b27c00b815b34cd5431c63d9724a0dfc83807de5`
- Figure builder: `10fda875b89344efd72f6ac420616fbd1c84a63af9d0d960f6e7838814206539`
- Figure manifest: `467018b8df0d59c4e91680de02a7cbd3e9ccc8a306eb75dcb0097ca8801cef04`

## Remaining work before a submission claim

Add author and affiliation metadata, venue formatting, the governed three-seed final experiment, exact test-event provenance, matched baselines, downstream reconstruction, memorization analysis, and complete generation-versus-Geant4 timing.
