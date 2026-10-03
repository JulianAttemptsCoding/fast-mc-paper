# Manuscript finalization - in progress

Word-level, mathematical, provenance, visual and whole-manuscript passes. No new model evaluation. Evidence and original source snapshots retained.

## Pass 1 - Word-level abstract and introduction

Read every sentence; remove evaluative only from occupancy statement; retain pilot and uncertainty boundaries.

## Pass 2 - Study populations and quantifiers

The phrase All shower comparisons overstates bank uniformity because a separate monitor uses its own bank; change to primary shower comparison.

## Pass 3 - All 14 equations and definitions

Checked conditions, masks, dimensions, cap, flow updates, decoder, graph and gap identity; preserve equations exactly.

## Pass 4 - Figure-to-prose correspondence

Source and high-resolution architecture agree; previous F1 withdrawn. Plan clearer flow/decoder stage labels.

## Pass 5 - Historical provenance and calibration

Calibration source hash matches retained evidence; weights are a proposal and runtime YAML absent, so do not assert independent applied-weight verification.

## Pass 6 - Classifier methodology

Recovered exact historical classifier source: 70/30 class-stratified rows, max_iter=100,max_depth=4,learning_rate=.08; source identity distinct from historical runtime verification.

## Pass 7 - Numerical results and denominators

Per-bin counts and four families of per-seed AUROC recovered; preserve separate nonempty support denominators and all-event response population.

## Pass 8 - Author declarations

User confirms independent researcher affiliation/contact and mentor/lab acknowledgment; no institutional representation.

## First revision

Independent researcher/contact metadata and mentor/lab thanks. Precise primary-comparison bank scope. Explicit share-flow and decoder labels; original colors retained. Two evidence-bound appendices: settings, weights, all bins, all classifier seeds and methodology. Historical test-use disclosure and unavailable-runtime limitations. Revision metadata and strict historical/current audit bindings updated.

## Pass 9 - Rendered title and affiliation

Name, independent-researcher role and mailto email fit on page 1; title remains explicitly pilot-scoped.

## Pass 10 - Abstract-to-conclusion numerical agreement

1.0%, 0.25 layers, 4.42 last-layer shift and 3.95 gaps agree throughout; no precision or causal claim added.

## Pass 11 - Response density wording

Clarified that the Jacobian multiplies the density, avoiding an ambiguous statement about multiplying a negative log likelihood.

## Pass 12 - Appendix symbol alignment

Changed V/T/etc labels to w_V/w_T/etc to match the weights in Eq. 13.

## Pass 13 - Feature-definition exactness

Corrected denominator-floor prose so it applies only to normalized features, not unnormalized total/count inputs.

## Pass 14 - Acknowledgment tone

Retained warm mentor/lab thanks; removed unnecessary institutional-position disclaimer because title metadata already states independent researcher.

## Pass 15 - Graph and longitudinal argument

Verified m>=R uses adjacent-layer edges; no conversion of gap-layer count into run count or independent lateral-fragmentation claim.

## Pass 16 - Metric populations and arithmetic

Checked all-event response, independent nonempty support denominators, paired W1 bootstrap and per-bin counts; numerical table unchanged.

## Pass 17 - Classifier split and seed roles

All 12 family/seed AUROCs retained; condition control, classifier seeds and generator seed clearly distinguished; internal early-stopping defaults caveat retained.

## Pass 18 - Visual pagination and figures

Directly inspected all 14 QA84 pages, four figures, four tables and references; no clipping, overlaps, orphan headings or unreadable labels.

## Pass 19 - Whole-manuscript reread: skeptical scientific reader

Read full rendered manuscript from abstract through appendices/references; central result remains one-bank descriptive support mismatch with limitations disclosed.

## Pass 20 - Reproducibility and historical provenance

Frozen config hash is recorded but runtime file absent; calibration proposal labeled honestly; source snapshots saved rather than treating defaults as exact environment evidence.

## Pass 21 - Whole-manuscript reread: final prose and logical flow

Reread all 14 pages in extracted final PDF order. Checked every paragraph against adjoining claims, definitions and conclusion; no further substantive issue found.

## Pass 22 - Changed-page visual reinspection

Directly inspected QA85 pages 6,11,12,13; all other pages match the individually inspected QA84 renders. Corrected Jacobian prose, acknowledgments, weight labels and feature-floor sentence fit cleanly.

## Pass 23 - Links, fonts and document identity

Verified email and repository annotations, title/author PDF metadata, all fonts embedded with Unicode maps, no TODO/TBD, no whitespace errors and all 14 equations identical to baseline.

## Pass 24 - Release metadata and audit continuity

Synchronized CFF email/independent affiliation; corrected historical v0.15 audit label in README; current-source audit and old QA82 remain separate. Seven stale-binding/build-failure guards passed.

## Review outcome

24 documented review passes; three whole-manuscript readings. QA84 and QA85 passed 16 check groups each. Seven release-binding/native-failure guard tests passed. QA83 failed on the bundled Python missing Matplotlib; the existing project runtime corrected the environment without guard changes. Final source-bound QA and render identity are recorded separately in the final build audit.

Unperformed research remains explicitly identified: headline structural uncertainty, threshold/graph robustness, independent generator fits, governed final testing, complete training environment and end-to-end timing. No evidence was invented.

### Author-requested AI disclosure wording

Replaced "analysis and model-design proposals" with "reviewing the model specifications" only. Source reviewed; full QA iteration 87 pending.

Input main.tex SHA256: 95fa603d553a331fa4f3797615cbf20193b7444b7231463314c9fee723d0541d
Output main.tex SHA256: 844c00be0f102bf527aa75cc252c1906de6dac90bc70b15ff4da540af2ad2c5b

Fresh-reader follow-up: current source pointer updated; historical exact release preserved under audit/source_snapshots/fresh_reader_20260930. See fresh_reader_review_20260930 twin. Rebuild pending.


The current source pointer was refreshed for the 2 October mentor consistency pass. See `audit/mentor_consistency_20261002.json`; the preceding source is preserved in `audit/source_snapshots/mentor_consistency_20261002_main.tex`.

Current AI acknowledgment updated at the author's request to OpenAI's GPT-5.6-Sol only; see `audit/ai_ack_20261002.json`.

Current use-of-generative-AI wording was updated at the author's request to state Julian Juan's lead role and main work; see `audit/author_lead_20261002.json`.

The author requested a concise AI-use disclosure and responsibility for all paper content; current wording is recorded in `audit/ai_usage_only_20261002.json`.
