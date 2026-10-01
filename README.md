# Longitudinal Gaps and Spatial Hit Connectivity in a Pilot Generative Model of Zero-Degree Calorimeter Showers

Version 0.21.1 is a case study of one pilot-trained calorimeter model. On a repeatedly inspected validation bank, its showers extend farther downstream and contain more inactive layers within their occupied span than the Geant4 reference, despite similar mean active-layer counts. The component-count excess is at least 84.6% within occupied-layer runs after subtracting one unavoidable component per run; it cannot be accounted for by empty-layer separations alone. The manuscript explains the full generation path from incident four-vector to 6,790 deposited energies and presents response, longitudinal and support results in physical order. The recorded high-level classifier AUROC of 0.775 exceeds its recorded 0.65 screening threshold; the failed condition-only control and row-wise split prevent a calibrated fidelity interpretation. The paper does not establish structural statistical significance, performance after digitization or retraining, acceleration, or detector readiness. Paired bootstrap intervals are available for the separate zero-deposit fraction and hit-count distance.

## Fixed case

The current local working revision includes a fresh-reader review for experimental HEP and computational physics. `audit/fresh_reader_assessment_20260930.md` assesses every section, equation, figure and table; `audit/fresh_reader_review_20260930.{json,md}` records edits, complete readings and failed attempts. The changes clarify exposition without changing the equations, numerical tables, model or data. The PDF is current only when the source and PDF hashes match `audit/final_build_audit.json`. The author line and `CITATION.cff` omit the affiliation label at the author's request. `audit/submission_preflight_20260930.json` records the latest source checks and compilation status.

- Run `dicos-f-02`, epoch 90; training seed 20260723.
- 26,624 pilot training events; 6,656 pilot validation events for the selection objective.
- 10,000-condition diagnostic bank from canonical validation, 50--250 GeV; repeatedly inspected and not an untouched test.
- Checkpoint SHA-256: `491284c7423f365230d34b0443f95aa4888ec770bdc673c4c979897bad8acbce`.
- Configuration SHA-256: `116bc8c220b07ce54ae07196bdd6ed8e835775c8c937182a209a799dc94ae9c5`.
- The 104-row history covers epochs 11--114. One declared post-90 continuation did not improve the minimum. An incorrect scheduler variant remains excluded.

## Build and QA

Requirements: Python with NumPy, Matplotlib and Pillow; pdflatex, biber and Poppler on PATH.

```powershell
.\build.ps1
$Iteration = Read-Host "Unused QA iteration number"
python scripts/full_manuscript_qa.py --iteration $Iteration --focus "scientific revision" --disposition "source-bound checks"
```

Choose an unused iteration number; historical records cannot be overwritten. The build stops on a failed native command before replacing `output/fast_mc_zdc_manuscript.pdf`. The QA checks evidence hashes, source-bound data roles, reported arithmetic, citation/label resolution, every figure and every rendered page. Automated raster checks are not human visual review. A final release audit additionally requires a hash-matched visual-review record and rejects stale source/PDF hashes.

## Evidence and reproducibility

- `main.tex`, `references.bib`: revised manuscript and primary literature.
- `data/reports/`: immutable aggregate diagnostic report and provenance.
- `data/provenance/source_evidence.json`: training-population/config binding, preparation counts, evaluator policy and source-file hashes.
- `data/training/`, `data/geometry/`: recorded history and event-independent geometry.
- `scripts/build_figures.py`, `figures/manifest.json`: reproducible figures and input/output hashes.
- `audit/revision_20260921.*`: corrections, failed attempts, research and decisions.
- `audit/framing_revision_20260921.*`: HEP/computational-physics framing criteria and pre-November-2025 style references.
- `audit/adversarial_revision_20260922.*`: historical disposition of the earlier supplied adversarial audits; its zero-uncertainty statement is superseded.
- `audit/adversarial_revision_round3_20260922.*`: historical disposition of the preceding two audits, including the recovered zero-fraction interval and graph confound.
- `audit/adversarial_revision_round4_20260923.*`: disposition of the subsequent audits, including the restored classifier results and mechanism corrections.
- `audit/claim_register_20260922.*`: current claim-by-claim disposition and sources.
- `audit/model_exposition_20260922.*`: source-hash-bound audit of the model mechanisms described in the manuscript.
- `audit/mathematical_exposition_20260923.*`: equation-by-equation source binding for the response, flows, graph, support, decoder, and training loss.
- `audit/sentence_evidence_20260922.*`: section-by-section evidence and clarity review for the complete manuscript.
- `audit/mentor_finalization_20260929.*`: prior full-manuscript rereads and presentation QA for v0.12.0.
- `audit/rhetoric_revision_20260929.*`: prior scientific-language and formatting audit for v0.13.0.
- `audit/research_voice_20260929.*`: prior v0.14.0 response to the supplied writing critique, limitation-retention review, and exact equation/table preservation.
- `audit/overall_revision_20260929.*`: v0.15.0 overall scientific, rhetorical and presentation review, including disposition of the latest supplied critique.
- `audit/finalization_20260930.*`: v0.20.0 word-level, numerical, visual and whole-document review; historical author metadata (affiliation label subsequently removed at the author's request); recovered appendix details; correction of the prior Figure 2 false positive.
- `audit/source_snapshots/finalization_20260930/`: hash-bound historical evaluator/calibration source used for the appendices.
- `audit/iterations/` and `audit/qa_series/`: preserved historical and current build checks; only a hash-matched current record applies to the current PDF.
- `archive/pre_revision_20260921/`: original v0.3.0 source/PDF/build snapshot.
- `reviews/`: the nine earlier reviews, unchanged; their previous dispositions are historical.
- `STATUS.md`: supported claim and outstanding research for broader claims.

The package rebuilds the paper from aggregate evidence. It does not redistribute the collaboration-owned event file or checkpoint and cannot reproduce training or event-level tests. No source data, frozen model configuration, or scientific threshold was modified by this manuscript revision. The author confirms that the data are an ePIC ZDC simulation and that the data owner approves publication; the production geometry tag and equivalence to the current design remain unverified.

## External audit and arXiv preparation

The v0.17.0 correction is documented in `audit/external_audit_response_20260930.md`. In v0.17.0, Figure 4 displayed algebraic within-run component bounds rather than repeating Table 1 means. Current v0.20.0 replaces that figure with an illustrative definition of gaps, runs and graph components; the bounds remain in the methods and results. That revision preserved the 14 model/observable equations and four numerical tables; v0.18.0 additionally reports the retained standard deviations in Table 3. Derived bounds are not uncertainty intervals. Internal run `dicos-f-02`, epoch 90, and family `calibrated_lr3e4` identify the analyzed artifact; they do not name a new experiment.

## Second audit correction

Current v0.20.0 is an aggregate-only diagnostic note. Stored IDs are model channels, not verified physical electronics channels. Multiplicity alone does not establish ganging; physical interpretation is unresolved pending production segmentation/volume mapping. No integrity failure has been demonstrated for the stored-ID arithmetic, but no detector-level connectivity inference is permitted. The present reanalysis uses the evaluation summary; exact runs, jointly nonempty statistics and threshold studies require a new event-level evaluation. See `audit/second_external_audit_response_20260930.md`. Table 3 now includes retained population standard deviations.


## Physical interpretation and third audit

Version 0.20.0 explains the physical observable represented by each architecture stage, distinguishes stored-energy closure from incident-energy conservation, and uses gap fractions to sharpen the component bound. See `audit/physics_exposition_response_20261001.md`. The active QA series is named in `audit/current_qa_series.json`; historical attempts are immutable.


## Final reader-proposal integration

Version 0.20.0 incorporates verified improvements from the Claude proposal: detector context and stored-coordinate dimensions, clearer stage labels, an illustration of gaps/runs/components, normalized paired-response intervals and deep-layer energy totals. Proposal claims of independent paired samples, threshold irrelevance and guaranteed classifier lower bounds are not adopted. See `audit/claude_integration_response_20261001.md`.

## Experimental HEP readability pass

Version 0.21.0 uses detector-facing terms for the strictly positive stored-deposit hit pattern, contiguous active-layer segments, and connected groups on the model graph. The revised manuscript places threshold sensitivity and physical interpretation beside the main observables. These graph groups are not reconstructed clusters, and the reported differences do not identify their cause. The three supplied audits and the disposition of adopted and unsupported readings are recorded in `audit/hep_readability_response_20261001.md`.

## Follow-up experimental HEP reader pass

Version 0.21.1 introduces the cited ePIC design directly, defines the incident three-momentum, explains the row-split classifier-control caveat in the abstract, illustrates possible section-wise calibration effects, and makes the two-sided threshold sensitivity explicit. The follow-up audit's apparent equation and table defects were checked against the LaTeX source and rendered PDF and are extraction errors. See `audit/hep_readability_followup_response_20261001.md`.
