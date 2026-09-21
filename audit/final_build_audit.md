# Final build audit

Created: 2026-09-21T15:41:42.307277+00:00

## Artifact

- Release: `v0.3.0`
- Accepted checkpoint: `dicos-f-02`, epoch 90, training seed 20260723
- Output: `output/fast_mc_zdc_manuscript.pdf`
- SHA-256: `775763e71e4b3150f2c43f0bb5df29c60e396b7db55ce13be0b644da730d5154`
- Size: 1,378,743 bytes
- Layout: 11 pages; 612 x 792 pts (letter)
- Scientific status: development-bank diagnostic manuscript; no final fidelity or speed claim

## QA

- Twenty complete sequential manuscript-wide QA iterations passed.
- Every iteration rebuilt all figures, bibliography, and LaTeX from source.
- Every iteration checked the evidence identities, split arithmetic, headline values, citations, labels, excluded language, and figure hashes.
- Every iteration rasterized and checked all 11 PDF pages for content, clipping, and text extraction.
- The final LaTeX log has no warnings, undefined controls, overfull boxes, or underfull boxes.
- PDF text contains no unresolved references, discarded model-screen names, or excluded classifier values.
- The retained condition-only AUROC 0.500 is recorded solely as a pairing-pipeline control.

## Reproducibility boundary

The repository rebuilds the manuscript and figures from frozen aggregate evidence. It does not redistribute the collaboration-owned event file or checkpoint, so it cannot reproduce training or event-level tests independently.

Submission blockers are tracked in `STATUS.md` and `audit/reviewer_response_round3.md`.

Input hashes and per-iteration page metrics are recorded in the JSON audit files.
