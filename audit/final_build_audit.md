# Final build audit

Created: 2026-09-21T06:05:59.877701+00:00

## Artifact

- Output: `output/fast_mc_zdc_manuscript.pdf`
- SHA-256: `86d36f62002c68219539d246d8acdd835f8bb7b96a422d45f03e8a788c8a7d82`
- Size: 1,256,081 bytes
- Layout: 11 A4 pages
- Scientific status: development-bank manuscript; no final fidelity or speed claim

## Checks

- Deterministic figure generation and Python bytecode compilation passed.
- 8 JSON evidence files parsed successfully.
- pdfLaTeX, Biber, and two final pdfLaTeX passes completed.
- The final LaTeX log has no warnings, undefined controls, overfull boxes, or underfull boxes.
- PDF text has no unresolved-reference markers or excluded historical C2ST values.
- All 11 pages were rendered and visually inspected.
- The historical random-fold shower-only C2ST is absent from the manuscript and archived as excluded evidence.

## Reproducibility boundary

The repository rebuilds the manuscript and all plotted figures from frozen aggregate evidence. It includes the portable V3-SUP configuration and event-independent geometry. It does not include the collaboration-owned event file or checkpoints and cannot recompute event-level tests or retrain the model.

Submission blockers are tracked in `STATUS.md` and `audit/reviewer_response_round2.md`.

## Environment

- Platform: `Windows-11-10.0.26200-SP0`
- Python: `3.13.1`
- pdfLaTeX: `MiKTeX-pdfTeX 4.23 (MiKTeX 25.12)`
- Biber: `biber version: 2.21`
- pdftoppm: `pdftoppm version 26.07.0`

Input and figure SHA-256 hashes are recorded in `audit/final_build_audit.json`.
