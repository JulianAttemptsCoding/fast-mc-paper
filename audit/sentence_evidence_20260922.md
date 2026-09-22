# Sentence-level evidence and clarity review

Created: 2026-09-22T17:42:45Z

Every prose paragraph, equation, table caption, and figure caption in manuscript v0.7.0 was assigned an evidence basis. Sentences were retained only when they define the computation, report a stored result, cite external physics context, state a direct algebraic consequence, or mark an evidence boundary.

| Section | Why each sentence is present | Evidence |
|---|---|---|
| Abstract | Study identity, model order, sample sizes, reported differences, and evidence limits. | `data/reports/dicos-f-02_epoch90.json`, `data/provenance/source_evidence.json`, `audit/model_exposition_20260922.json`, `audit/claim_register_20260922.json` |
| Introduction | Motivation and comparison to prior calorimeter-surrogate practice; each field statement carries a primary citation. The final paragraph states the exact question and evidence boundary. | `references.bib`, `audit/literature_benchmark.md`, `audit/claim_register_20260922.md` |
| Simulation target and evaluation population | Feature semantics, target definition, channel/layer counts, graph construction, split counts, and development-bank role. | `data/provenance/source_evidence.json`, `data/geometry/geometry_summary.json`, `figures/manifest.json`, `audit/model_exposition_20260922.json` |
| Generator and training procedure | Every architectural, sampling, decoder, loss, optimizer, and checkpoint-selection statement is tied to an implementation blob, selected-configuration identity, training history, or source audit. Interpretive sentences only state direct consequences of the equations or declared nonclaims. | `audit/model_exposition_20260922.json`, `data/provenance/source_evidence.json`, `data/training/calibrated_lr3e4_history.csv`, `data/reports/dicos-f-02_epoch90.provenance.json` |
| Diagnostics | Definitions are explicit equations or direct metric semantics; the classifier-control interpretation follows from its condition-only feature set. | `data/reports/dicos-f-02_epoch90.json`, `data/reports/condition_only_control.json`, `data/provenance/source_evidence.json`, `references.bib` |
| Results | Every number is reproduced from the immutable aggregate report. Statements about what the aggregates cannot determine follow from fields that were not retained. | `data/reports/dicos-f-02_epoch90.json`, `audit/claim_register_20260922.json`, `audit/adversarial_revision_20260922.json` |
| Discussion and conclusion | The central interpretation restates measured aggregate differences. Alternative explanations are labeled as untested; proposed studies are linked to the uncertainty or mechanism each would probe. | `audit/claim_register_20260922.md`, `audit/adversarial_revision_20260922.md`, `data/provenance/source_evidence.json` |
| Availability, acknowledgments, contributions, and AI disclosure | Repository contents were checked directly. Authorship, acknowledgment, and tool-use sentences are declarations by the author rather than scientific inferences. | `README.md`, `STATUS.md`, `CITATION.cff` |

## Style pass

The manuscript avoids promotional adjectives, stock contribution language, unsupported causal verbs, and vague claims of robustness or validation. The automated source guard rejects the canned phrases listed in the JSON twin. Model jargon is defined at first use or paired with its operation and inputs.

The scientific claim is unchanged: the source audit improves the explanation of the generator; it does not convert the development-bank discrepancy into a validation result.

## Typeset disposition

Iteration 40 passed the complete automated suite. All nine pages were inspected. The only visual issue found during iteration was an architecture float that could interrupt the flow-matching explanation; the figure is now a fixed block immediately after the model factorization is introduced.
