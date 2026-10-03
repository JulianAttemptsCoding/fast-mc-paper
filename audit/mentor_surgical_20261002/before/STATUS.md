# Scientific status

Version 0.22.1 is an arXiv preprint candidate describing one pilot ePIC ZDC simulation model on a repeatedly inspected development bank. It is not a validated FastMC or detector-performance result.

## Corrected central result

The supplied external audit identified an inference omitted in v0.16.0. Let m be graph components, R occupied-layer runs, and G interior inactive layers. With Q=m-R, 1 + I[G>0] <= R <= G+1 implies delta mean Q >= delta mean m - mean G_generator + f_reference = 30.4458 components, at least 84.64% of the 35.9703-component excess. Thus empty-layer separations alone are insufficient: a within-run graph discrepancy is established. It is not necessarily lateral fragmentation, a physical-cluster effect, or causal attribution to a model stage. The earlier claim that the aggregates could not establish within-run fragmentation is superseded.

## Scope and remaining research

The results concern one training seed, raw deposits without an added threshold/time cut, an incompletely documented production geometry, separate nonempty samples and a reused validation bank. Headline structural intervals, threshold/graph sensitivity, an activity-independence null, occupancy calibration, same-bank pair-grouped C2ST, reconstructed observables and model-only timing remain unfinished research. The older row-split C2ST values and their failed condition-only control remain disclosed. No new event generation, training, test inspection, calibration or detector threshold was introduced.

The author confirmed ePIC ZDC identity and data-owner approval for publication on 30 September 2026; no geometry tag was supplied. The paper does not claim equivalence to the current ePIC geometry. Name and email appear without an affiliation label at the author's request; Academia Sinica mentorship is acknowledged.

## Evidence

See audit/claude_integration_response_20261001.md for the latest proposal disposition and the earlier response files listed in README.md for historical audit items, audit/component_bound_20260930.json for the derived arithmetic and mathematical checks, and audit/final_build_audit.json for the current exact-source release binding. The current arXiv upload package should contain only main.tex, references.bib, main.bbl and the four included figures. Upload and final inspection on arXiv have not been performed.

## Second audit correction

The historical v0.20.0 revision is an aggregate-only diagnostic note. Stored IDs are model channels, not verified physical electronics channels. Multiplicity alone does not establish ganging; physical interpretation is unresolved pending production segmentation/volume mapping. No integrity failure has been demonstrated for the stored-ID arithmetic, but no detector-level connectivity inference is permitted. The present reanalysis uses the evaluation summary; exact runs, jointly nonempty statistics and threshold studies require a new event-level evaluation. See `audit/second_external_audit_response_20260930.md`. Table 3 now includes retained population standard deviations.


## Physical interpretation and third audit

Version 0.20.0 explains the physical observable represented by each architecture stage, distinguishes stored-energy closure from incident-energy conservation, and uses gap fractions to sharpen the component bound. See `audit/physics_exposition_response_20261001.md`. The active QA series is named in `audit/current_qa_series.json`; historical attempts are immutable.


## Final reader-proposal integration

Version 0.20.0 incorporates verified improvements from the Claude proposal: detector context and stored-coordinate dimensions, clearer stage labels, an illustration of gaps/runs/components, normalized paired-response intervals and deep-layer energy totals. Proposal claims of independent paired samples, threshold irrelevance and guaranteed classifier lower bounds are not adopted. See `audit/claude_integration_response_20261001.md`.

## Experimental HEP readability pass

Version 0.21.0 clarifies the positive-deposit hit definition and connects graph quantities and model stages to detector observables while preserving the algebra and evidence limits. The term graph-connected hit group denotes a zero-threshold component on the model graph, not a reconstructed calorimeter cluster. See `audit/hep_readability_response_20261001.md`.

## Follow-up HEP reader pass

Version 0.21.1 clarifies the ePIC design context, the condition-only C2ST control, section-weighted calibration as an illustrative calculation, and the two possible directions of threshold effects. No reconstruction, threshold, training, or event-level study was performed. See `audit/hep_readability_followup_response_20261001.md`.

## October reader review

Version 0.22.0 adds a structural-data panel beside the definitions, repairs the geometry guide and tick labels, reports the depth-distribution discrepancy, identifies the pooled response widths, and states the fixed gun vertex and nominal materials as documented context with explicit provenance limits. The uncertainty calculation is an independent-sample error scale, not a recovered paired interval. No threshold scan or event-level experiment was performed. See `audit/claude_review_response_20261002.md`.

## Mentor-send clarity revision

Version 0.22.1 restores definitions that earlier condensing had removed (Wasserstein distance, reference-half scale, edge co-occupancy, closure residuals, support), names the incident particle and both samples in the abstract, ties Table 1 row names to the symbols of the evaluation section, cross-references the result figures, and states the stored-energy scale and the depth shift in physical units. It adds one paragraph of energy-weighted transverse summaries and one binwise error-scale statement, both recomputed from the released aggregate report by `scripts/mentor_send_checks.py`. Numbered equations and numerical table bodies are unchanged. The binwise scale treats the samples as independent and is not a paired interval. No event-level data, checkpoint, threshold scan or new evaluation was used. A word-by-word pre-send pass then corrected the binwise statement to quote both of the largest differences (1.8 and 2.0 standard errors) and made nine wording clarifications without changing any number. See `audit/mentor_send_response_20261002.md`.

## Final consistency review

The mentor consistency pass of 2 October 2026 clarifies provisional visibility versus final zero deposits, stored-ID channel semantics, graph-message inputs, calibration-proposal provenance, relative standard errors, the fully specified three-layer example, component-energy limits, the timing denominator and the comparison of transverse observables. All 14 numbered equations, all four numerical table bodies, data and figure definitions are unchanged. See `audit/mentor_consistency_20261002.{json,md}` for the complete review and verification record. This is an editorial finalization of v0.22.1.

## Comprehensive final review, 2 October 2026

The complete title-to-references review defines SiPM, MIP and LYSO, makes paired-shower independence explicitly conditional, clarifies graph messages, preserves the author-requested AI disclosure, and synchronizes three bibliography entries with primary publication records. All 14 numbered equations, four numerical tables, figure definitions and scientific results are preserved. See `audit/final_review_20261002/events.{json,md}` for commands, source hashes, failures and the final full-suite/every-page review. The exact current release remains bound by `audit/final_build_audit.json`.

## HEP framing research and review, 2 October 2026

The title now names generated neutron showers. The abstract states the target, model comparison, principal quantitative finding and evidentiary limits without an unexplained classifier acronym. The discussion distinguishes the observed discrepancy, possible causes, required tests and relevance to neutron reconstruction; the conclusion states the validation lesson and its one-seed scope. APS/IOP guidance and four relevant primary research papers inform the revision. All 14 numbered equations, four numerical tables, figures and evidence remain unchanged. Research, decisions and full QA are recorded in `audit/hep_framing_research_20261002/`. This is an editorial revision of v0.22.1, not new physics validation.
