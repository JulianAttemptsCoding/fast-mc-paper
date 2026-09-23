# Sentence-level evidence and clarity review

Created: 2026-09-22T17:42:45Z

Every prose paragraph, equation, table caption, and figure caption in manuscript v0.9.0 was reviewed for purpose and evidence. The revision corrects the zero-fraction uncertainty statement, centers the measured longitudinal discrepancy, and separates it from the graph-component statistic. Sentences were retained when they define the computation, report a stored result, cite physics context, state a direct consequence of the graph or decoder, or explain a material boundary of the result.

| Section | Why each sentence is present | Evidence |
|---|---|---|
| Abstract | Study identity, model order, sample sizes, longitudinal result, component confound, and evidence limits. | `data/reports/dicos-f-02_epoch90.json`, `data/provenance/source_evidence.json`, `audit/model_exposition_20260922.json`, `audit/claim_register_20260922.json` |
| Introduction | Motivation and comparison to prior calorimeter-surrogate work; field claims carry primary citations. The final paragraph names the quantities compared. | `references.bib`, `audit/literature_benchmark.md`, `audit/claim_register_20260922.md` |
| Simulation target and evaluation population | Feature semantics, target definition, channel/layer counts, graph construction, split counts, and development-bank role. | `data/provenance/source_evidence.json`, `data/geometry/geometry_summary.json`, `figures/manifest.json`, `audit/model_exposition_20260922.json` |
| Generator and training procedure | Every architectural, sampling, decoder, loss, optimizer, and checkpoint-selection statement is tied to an implementation blob, selected-configuration identity, training history, or source audit. Interpretive sentences only state direct consequences of the equations or declared nonclaims. | `audit/model_exposition_20260922.json`, `data/provenance/source_evidence.json`, `data/training/calibrated_lr3e4_history.csv`, `data/reports/dicos-f-02_epoch90.provenance.json` |
| Diagnostics | Definitions follow metric semantics. Adjacent-layer splitting follows the stated graph. The paired zero-fraction bootstrap and row-wise classifier split are checked against the report and evaluator source. | `data/reports/dicos-f-02_epoch90.json`, `data/reports/condition_only_control.json`, `audit/adversarial_revision_round3_20260922.json`, `references.bib` |
| Results | Every number, including the zero-fraction interval and all-event edge co-occupancy, comes from the immutable report. Missing gap-run, component-energy, and structural-uncertainty claims follow from absent fields. | `data/reports/dicos-f-02_epoch90.json`, `audit/claim_register_20260922.json`, `audit/adversarial_revision_round3_20260922.json` |
| Discussion and conclusion | The interpretation leads with longitudinal reach and identifies the graph confound. Possible mechanisms are labeled untested and tied to the experiments that would distinguish them. | `audit/claim_register_20260922.md`, `audit/adversarial_revision_round3_20260922.md`, `data/provenance/source_evidence.json` |
| Availability, acknowledgments, contributions, and AI disclosure | Repository contents were checked directly. The author confirmed substantial Codex/GPT-5.6-Sol drafting and proposal roles, personal ownership of the main ideas, and verification of the work. | `README.md`, `STATUS.md`, `CITATION.cff`, author declaration in conversation |

## Style pass

The manuscript avoids promotional adjectives, stock contribution language, unsupported causal verbs, and vague claims of robustness or validation. The automated source guard rejects the canned phrases listed in the JSON twin. Model jargon is defined at first use or paired with its operation and inputs.

The v0.9.0 scientific claim is narrower than v0.8.0: a longitudinal discrepancy is observed, while graph components cannot be interpreted as independent lateral fragmentation from the stored aggregates. The CaloChallenge entry is pinned to arXiv v1, submitted in October 2024, for the requested prose baseline. A 2026 ZDC paper is cited only as current scientific context.

## Typeset disposition

Iteration 50 passed the complete automated suite. Its nine pages were inspected at original render resolution, using byte-identical earlier renders for unchanged pages. The diagram retains its programmatic label-containment check. A subsequent exact-PDF visual review is recorded separately in `audit/visual_review_20260922.json`.
