# Mentor manuscript finalization audit

Version 0.12.0. Status: finalized after full QA and exact-output visual review.

Six full rereads are recorded in the JSON twin. Each restart used a different question set: claim/data role; equation/source; literature/expert-reader exposition; figures/tables/pages; every sentence/word; and final exact-output review.

## Restart 1: scientific claim and data-role audit from abstract through declarations

Coverage: Abstract, Introduction, Simulation target and evaluation population, Generator and training procedure, Diagnostics, Results, Discussion, Conclusion, declarations, all four figure captions, results table.

Findings: All quoted primary numbers match the immutable aggregate report and conditional denominators; failed high-level classifier gate remains stated. New support figure correctly uses side-specific nonempty means; original energy figure remains labelled as an average that cannot reveal eventwise gaps. One checkpoint, repeatedly inspected validation bank, missing structural intervals, unresolved pilot-validation overlap, and no test use remain explicit.

Corrections: No further numerical correction in restart 1.

## Restart 2: equation-by-equation, symbol-by-symbol and sampling-path audit against recorded source commit

Coverage: condition Eq.1, response mixture and cap Eqs.2-3, layer activity Eq.4, log-fraction targets Eqs.5 and 11, masked flow loss Eq.6, eight-step update Eq.7, budget Eq.8, graph message Eq.9, Gumbel top-K Eq.10, decoder Eq.12, nine-loss joint objective Eq.13, support/gap Eq.14, all architecture prose and schematic.

Findings: Response head's positive mixture, lower clipping, cap and final visibility agree with source; the mixture NLL includes the target Jacobian. Profile and share flows both use masked straight-path MSE and current-state midpoint-time eight-step updates; no solver-convergence claim appears. Directed message aggregation, one hard Gumbel top-K draw, exact-count mask, and softmax budget closure agree with source. Axis features are opt-in and disabled for the selected v2 path; five derived four-vector features are the event condition. The paper named a fixed top-K temperature without a value; source sampler uses default 1.0.

Corrections: State tau=1 in the top-K explanation. No equation, model, frozen config, result or guard changed.

## Restart 3: experimental-HEP/computational-physics reader and pre-November-2024 literature comparison

Coverage: Abstract, Introduction and prior work, dataset and four-vector semantics, geometry and graph, generator and training, diagnostic definitions, results/figures, discussion and declarations.

Findings: The original direction expression divided by zero at zero momentum, while the implementation clamps the norm and returns a zero vector. Neutron mass, one-dimensional hit-count Wasserstein meaning, AUROC chance benchmark and teacher-forced checkpoint-selection status were underexplained. Earlier literature explicitly defines target representation, preprocessing, graph, observables and quality/time tradeoffs; this paper must state missing timing and production configuration rather than borrow external claims. The manuscript's current scientific citations include later publications, but the requested exposition research is now explicitly limited to pre-2024-11 versions.

Corrections: Corrected Eq.1 at zero momentum and kinetic endpoint; added neutron mass, W1/AUROC explanations and teacher-forced selection statement; updated literature audit with version-specific primary links.

## Restart 4: figure-by-figure, table-by-table and every-page visual/notation audit

Coverage: geometry figure and caption, sampling schematic and caption, support-summary figure and caption, longitudinal-energy figure and caption, results table and denominators, equations 1-14 on pages 2 and 4-7, all 11 PDF pages.

Findings: Four figures and the table are legible with no overlap, clipping, broken glyphs or mismatched labels. Support figure derives exact conditional means and uses separate zero-based scales; its caption forbids uncertainty or eventwise interpretation. The channel-share target equation appeared at the foot of page 5 with S* defined at the start of page 6; symbols should be defined before the equation. Results heading and its complete introduction end page 7 while Table 1 begins page 8; this is readable and keeps the table with its new support figure.

Corrections: Moved S*_ell and K*_ell definitions before Eq.11; retained pagination and scientific content.

## Restart 5: sentence-by-sentence and word-by-word source read for experimental-HEP mentor audience

Coverage: title and abstract, all Introduction paragraphs, condition/target/geometry/population paragraphs, all generator subsections and each displayed equation, training and diagnostics paragraphs, results table, all figures, every results paragraph, all Discussion and Conclusion paragraphs, availability, acknowledgments, contributions, AI declaration and bibliography.

Findings: Abstract used an awkward possessive for uncertainty and a signed difference where direct direction was clearer. Table presents differences from unrounded source values while row entries are rounded; caption needed to say this. AI-use statement identified only the earlier model, omitting this later editing pass. Actual nine frozen weights could not be recovered from source checkout with the exact frozen config hash; retained source-supported description rather than equating calibration proposals with the selected config.

Corrections: Rephrased abstract, stated unrounded-difference convention in Table 1 caption, made AI-use statement model-neutral, updated release metadata and required this audit in QA.

## Restart 6: post-build exact-output reread and final word/figure check

Coverage: final abstract and citations, all equation pages, Table 1 and all four captions/figures, all results and discussion pages, declarations and all 18 references, all 11 rendered pages by direct review or byte-identical prior review.

Findings: Final pagination is legible with no clipped content, undefined symbols, broken references or table/figure mismatch. The abstract, Table 1 and AI statement corrections survive typesetting. The Results introduction finishes on page 7 and Table 1 begins page 8; no sentence or table is split.

Corrections: No further source correction required after full QA iteration 71.

## Final binding

QA iteration 71: PASS; 11 pages; 14 check groups. PDF SHA-256: 6175d57689a087ef216623ab262a79470bd9cf31d98a387a3dec206577086d60. Every page is bound in the 2026-09-29 visual-review twin. Intermediate QA iteration 70 failed a stale literal assertion and was corrected without reducing the underlying uncertainty requirement.

## Scientific boundary

One checkpoint, one training seed, repeatedly inspected canonical-validation bank. Structural uncertainty, threshold robustness, independent graph behavior, end-to-end speed and physics fidelity remain unmeasured. No raw events, nominal test data, frozen configuration or model weights were accessed or changed by this revision.

Main TeX SHA-256: dfd14e1c37a909b953822e54bbd5d2e64128411f4dc525551bcec29e95f91ed4. Full command, failure, input and output hash records are in the JSON twin and logs.md.
