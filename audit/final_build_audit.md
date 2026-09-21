# Final build audit

Created: 2026-09-21T04:51:14.827025+00:00

## Artifact

- Output: `output/fast_mc_zdc_manuscript.pdf`
- SHA-256: `109f8a64db3f7bb1f15cbd21f0f7170a49ffa3d22171e60904fa6329e62e7780`
- Size: 961,899 bytes
- Layout: 11 A4 pages
- Scientific status: preliminary development-bank manuscript

## Checks

- Figure generation completed from the pinned aggregate JSON reports.
- Python bytecode compilation passed for `scripts/build_figures.py`.
- Seven JSON files parsed successfully.
- `pdflatex`, `biber`, and two final `pdflatex` passes completed with exit code 0.
- The LaTeX log contains no LaTeX warnings, undefined control sequences, overfull boxes, or underfull boxes.
- Extracted PDF text contains no unresolved-reference markers, the excluded malformed control value, or undefined-reference text.
- All 11 PDF pages were rendered to PNG and inspected for clipping, overlaps, illegible figures, broken references, and encoding errors.
- The verified pair-grouped condition-only control is AUROC 0.500 from `data/reports/verified_condition_control.json`.

## Reproducibility boundary

The repository can rebuild the manuscript and every plotted figure from aggregate reports. It cannot reproduce training or Geant4 production because the collaboration-owned event file, frozen model configurations, checkpoints, and full production metadata are not included. The unresolved submission blockers are listed in `audit/reviewer_response.md` and the machine-readable audit twin.

## Environment

- Platform: `Windows-11-10.0.26200-SP0`
- Python: `3.13.1`
- pdfLaTeX: `MiKTeX-pdfTeX 4.23 (MiKTeX 25.12)`
- Biber: `biber version: 2.21`
- pdftoppm: `pdftoppm version 26.07.0`

Input and figure SHA-256 hashes are recorded in `audit/final_build_audit.json`.
