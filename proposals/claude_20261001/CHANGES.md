# Proposed revision of v0.19.0 (2026-10-01)

This folder is a proposal. `main.tex`, `output/`, `figures/`, `scripts/` and
`audit/` are as they were; the only change outside this folder is one appended
entry in `logs.md`
(`main.tex` `d6ecda67…`, `output/fast_mc_zdc_manuscript.pdf` `aae417e8…`).

Read `REVIEW.md` first. It gives the verdict on v0.19.0, part by part, and the
findings that depend on the parent project.

## Files

| File | Purpose |
|---|---|
| `proposed_revision.pdf` | The proposal, 18 pages (same bytes as `main.pdf`) |
| `main.tex` | Proposed source |
| `main_v0.19.0_original.tex` | Copy of the source the proposal started from |
| `REVIEW.md` | The review |
| `build.sh` | Builds figures and PDF in this folder only |
| `build_proposal_figures.py` | Three new figures, from `data/geometry` and `data/training` |
| `verify_numbers.py` | Recomputes 192 quoted numbers from `data/` and fails on any mismatch |
| `edits_02.json` … `edits_07.json` | The edit rounds after the first draft, as exact replacements |
| `apply_edits.py`, `list_negations.py` | Editing aids |
| `figures/` | Three new figures and unmodified copies of three existing ones |

## Rebuild and check

```bash
bash build.sh
```

```bash
python verify_numbers.py
```

## What is the same

Title, the 14 original equations, every value in the four original tables,
acknowledgments, AI statement, `references.bib`.

## What is new

- Figures: `detector_layout.png` (replaces `detector_geometry.png`),
  `training_history.png`, `observable_definitions.png`.
- Tables: generator stages; shower-shape distances with half-split scale.
- Equations 15–18: the bound, numbered and derived in three steps.
- Results taken from the existing evaluation summary but not used in v0.19.0:
  paired response residual and standard errors, deep-layer energy,
  nine-observable distance table, layer-correlation distance, timing limit.

## Before adopting any of it

1. The AI statement names OpenAI Codex only. It must be updated if text from
   this proposal is used.
2. `scripts/full_manuscript_qa.py` expects 14 pages at most, 14 numbered
   equations, four figures, four tables and phrases such as "aggregate-only".
   The proposal has 18 pages, 18 equations, six figures and six tables.
3. Check against the sources: design-paper numbers in Secs. 1 and 2.1
   (arXiv:2406.12877), "RTX 4090, about 13 minutes per epoch" (parent project
   `CLAUDE.md`, 779.6 s per epoch), "8,000 showers" for the pair-grouped
   evaluation (parent project `audit/current_external_metrics.json`).
4. Title-page date is still September 2026.
