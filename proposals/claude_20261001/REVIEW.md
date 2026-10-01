# Manuscript review: fresh reader, then in context (2026-10-01)

Subject: `fast-mc-paper/output/fast_mc_zdc_manuscript.pdf`, v0.19.0, 14 pages
(SHA-256 `aae417e8…b278f`; source `main.tex` `d6ecda67…e423`). Neither file was
modified. A proposed revision is in
`fast-mc-paper/proposals/claude_20261001/` (18 pages, `proposed_revision.pdf`).

Question asked of every part, on every pass: does it do its job in the
manuscript, and can an experimental-HEP / computational-physics reader follow it?

## 1. Verdict

**Correct and honest, but not yet doing its job for that reader.**

What is sound: every number, table entry and equation was re-derived from the
evaluation summary, the geometry file and the training history. No arithmetic
or algebra error was found (192 scripted checks plus the bound, the edge count,
the three-layer example, the loss-weight normalisation and the classifier
leakage fractions by hand). The model description matches the source code
(`profile.py`, `response.py`, `counts.py`, `node_fields.py`, `graph.py`,
`support.py`, `system.py`).

What is not working falls into two groups.

**Presentation (fixable by editing; fixed in the proposal).**

- It reads as an audit record. 59 uses of bookkeeping vocabulary in 5,500 words
  ("retained", "recorded", "recovered", "aggregate-only", "development bank",
  "screening maximum", "calibration proposal", "lineage"), and 21 of
  "unavailable / unverified / undocumented / unknown". A physicist cannot tell
  which of these are physics limitations and which are file-management history.
- Disclaimers follow almost every statement, so the findings are hard to locate.
- No physics motivation: nothing says what a ZDC is for or why the spatial
  pattern of hits matters to it.
- The detector is described only by what is not known about it. The stored
  geometry already gives the layer pitch, the cell pitch, the depth and the
  position on the beam line; none of that is stated.
- The architecture is given as fourteen equations in running prose, with no
  table of stages and no statement of which stage controls which observable.
- The central inequality is unnumbered and buried mid-paragraph, although the
  abstract and conclusion rest on it.
- Figures: no longitudinal view of the detector, no training curve, no picture
  explaining gaps, runs and components. Figure 4 plots six numbers.

**Substance (not fixable by editing).**

- The headline observables count any positive deposit as a hit. No threshold.
  The data in hand show the extra depth carries almost no energy (see 3.3), so a
  reader's first question is whether the effect survives a 0.25–0.5 MeV cut.
  The paper cannot answer.
- Only means are reported for the structural observables: no distributions, no
  uncertainties, no event display.
- The central result is a bound on a quantity that is exactly computable from
  per-event masks. The paper says the events "were not recovered locally". A
  referee will not accept that as a reason; see 3.1.
- One checkpoint, one seed, 4% of the training data.

Further rereading of the text will not change the second group. One evaluation
run will.

## 2. Cold read, part by part (v0.19.0)

| Part | Does its job? | Clear to a HEP reader? | Main problem |
|---|---|---|---|
| Title | Yes | Yes | — |
| Abstract | Partly | No | "6,790-ID representation", "recorded screening maximum", "aggregate-only" are undefined; the bound sentence cannot be parsed cold; no sentence on why it matters |
| 1 Introduction | Partly | Partly | No physics motivation; "support" and "occupancy" defined before the reader knows the detector; no list of contributions; scope given as a one-line disclaimer |
| 2.1 Target and conditioning | Yes | Mostly | States "production integration window is unknown" without saying what is known |
| 2.2 Geometry and graph | Partly | No | A list of nine undocumented items and no positive description; no dimensions; Fig. 1 shows two faces and a histogram, no depth structure |
| 2.3 Populations | Yes | Partly | "development bank D_dev" (symbol used once); "not recovered locally" reads as a missing-file note |
| 3 overview + Fig. 2 | Yes | Yes | Would be faster with a stage table |
| 3.1 Total and longitudinal | Yes | Mostly | `x_1` used in Eq. 5 before flow matching is introduced; "singular target plane" sentence is opaque; the key assumption (Eq. 4) is not flagged as key |
| 3.2 Counts, support, energies | Yes | Mostly | Five consecutive "it is X, not Y" sentences; what each stage can and cannot change is scattered |
| 3.3 Training and selection | Partly | No | "retained calibration proposal", "104 retained rows"; no training curve; overfitting not mentioned |
| 4 Evaluation protocol | Yes | Partly | The bound derivation is one dense paragraph with an unnumbered display; C2ST paragraph gives 0.464, 0.500, 0.893 with no guidance on which to believe |
| 5 Table 1 | Yes | Yes | — |
| 5.1 Energy, empties | Partly | Partly | Says significance "is not established" while the summary holds a paired bootstrap interval and enough to compute standard errors |
| 5.2 Longitudinal activity | Yes | Yes | Best section. Does not say how little energy the extra depth carries |
| 5.3 Support and graph | Partly | Partly | Result of the bound is deferred to the Discussion; Fig. 4 plots six numbers |
| 5.4 Classifier and numerics | Partly | No | Headlines the value from the flawed split; the closure-tolerance history is internal bookkeeping |
| 6.1 Interpretation | Yes | Yes | The three-layer example is the clearest passage in the paper |
| 6.2 Limitations | Yes | Partly | Four paragraphs of mixed physics and provenance; the threshold issue is not ranked first |
| 6.3 Performance | No | — | No number at all, although the summary bounds generation time |
| 7 Conclusion | Yes | Yes | Short; no statement of what a reader should do differently |
| App. A | Yes | Partly | Fine as a record; "proposal" wording |
| App. B | Yes | Yes | — |
| Eq. 1–14 | Yes | Yes | All correct and all used. Purpose of each is clear except 5/11 (centering) |
| Fig. 1 | Partly | Partly | Third panel (multiplicity histogram) duplicates the text |
| Fig. 2 | Yes | Yes | — |
| Fig. 3 | Yes | Yes | — |
| Fig. 4 | Partly | Partly | Low information; no figure explains the observables |
| Tables 1–4 | Yes | Yes | — |
| References | Yes | Yes | — |

## 3. What changes when the project is known

The manuscript was written from an extract of the project (one JSON summary,
one geometry file, one CSV) and describes everything outside that extract as
unavailable. In the parent project much of it exists.

### 3.1 The per-event data and the checkpoint exist

`_runs/calibrated_lr3e4_dicos-f-02/checkpoints/best.pt` and
`_v3/validation_bank_10k.json` are on the DiCOS work directory.
`src/cbsc_zdc/eval/v3_battery.py` holds the full generated and Geant4 arrays in
memory and the bank selection is deterministic. Exact run counts, histograms of
gaps / last layer / components, component sizes and energies, a threshold scan,
an event display, a pair-grouped classifier on the same events and
generation-only timing are one battery extension and one rerun (the last run
took 3,442 s). `decode_exact_support` and `LayerCountHead` already take a
`threshold_gev` argument.

### 3.2 The signature is reproduced by six descendant checkpoints

Same 10,000-event bank, same battery, reports in
`exhibition/data/v3_battery/`:

| Checkpoint | Gap fraction | Mean gaps | Last layer | Active layers | Components | Empty |
|---|---|---|---|---|---|---|
| Geant4 | 52.4% | 2.10 | 56.20 | 54.58 | 23.42 | 93 |
| dicos-f-02 e90 (paper) | 93.5% | 6.05 | 60.62 | 54.83 | 59.39 | 142 |
| v3-m0-fresh e19 | 93.4% | 6.07 | 60.44 | 54.63 | 57.85 | 164 |
| v3-s1-axis e19 | 93.4% | 6.10 | 60.42 | 54.59 | 57.90 | 162 |
| v3-s3-first e19 | 93.4% | 6.10 | 60.45 | 54.66 | 57.71 | 150 |
| v3-sup e12 | 93.6% | 6.25 | 60.44 | 54.41 | 59.96 | 161 |
| v3-sup e7 | 92.8% | 6.06 | 60.81 | 55.01 | 59.80 | 149 |
| v3-s2-response e19 | 96.1% | 7.43 | 59.64 | 51.42 | 54.81 | 5,041 |

These are not independent seeds: all start from the analysed weights. But the
response head, the first-layer head, the input features and the support stage
were each changed and the gap signature did not move. All share the factorised
activity stage. The paper repo holds three of these under
`archive/excluded_screens/` and `build.ps1` blocks two of their numbers from
appearing. That exclusion was reasonable for model comparison; as robustness
evidence for the diagnostic it is the strongest thing the project has.

### 3.3 The test proposed in Sec. 6.1 has already been trained

`src/cbsc_zdc/models/activity.py` contains a span-and-gap head and an
autoregressive head. `v3-s4-activity-ar` finished its 24 epochs on 2026-08-21
and `v3-s4-activity-span` was trained after it. Neither has a battery report.
Running the existing battery on them answers "does modelling inter-layer
dependence remove the gap excess, and does the fragmentation excess remain?"

### 3.4 Evidence in the paper's own summary file that the paper does not use

- Mean energy in layers 57–64: 17.2 MeV (Geant4), 17.8 MeV (generator), 0.4% of
  the total. The last active layer moves 4.4 layers deeper while the energy
  there changes by under 1 MeV per event. This is the most direct available
  statement on physical relevance.
- Paired response residual `(T_gen − T_ref)/K_inc`: mean 2.9e-5, bootstrap
  interval [−8.5e-4, 9.3e-4], RMS 0.046.
- `W1` and Geant4 half-split `W1` for nine shower summaries. Total deposit and
  transverse centroid agree within the half-split scale; hit count, depth,
  ECAL fraction, late fraction, transverse RMS and largest-channel fraction
  differ by 3.7–9.5 times it.
- Layer-energy correlation-matrix distance 3.52 against 1.98 for Geant4 halves.
- Timing: 3,442 s total, 1,009 s of it in timed analysis steps, so generation
  plus I/O is at most 0.24 s per shower.

### 3.5 A statistical point earlier audits left open

v0.19.0 says the significance of the 0.045 GeV mean difference cannot be
established because the paired covariance is unavailable, and the third audit's
standard-error argument was rejected as only an upper bound. The summary
settles it: the RMS expected for `(T_gen − T_ref)/K_inc` from two uncorrelated
samples with the per-bin standard deviations of Table 3 is 0.0461; the observed
paired RMS is 0.0460. The pairing carries no measurable correlation, so the
independent-sample standard error is the right one, not just a bound. Then:
mean difference 0.045 ± 0.068 GeV (0.7σ); binned differences at most 2.0σ,
χ² = 13.0 for 8 bins. The ±7.7% zig-zag is consistent with sampling noise.

### 3.6 Other project evidence on this checkpoint

- Pair-grouped evaluation, 8,000 events (`audit/current_external_metrics.json`,
  labelled FOLLOW-UP QA, below the 10,000-event minimum): shower-shape AUROC
  0.893, control 0.500; reconstruction proxy energy bias −4.0%, relative RMSE
  0.210, angular 68% containment 12.40 mrad against 10.70 mrad for Geant4. The
  paper says the effect on reconstruction "is not measured".
- Overfitting is established in `docs/V3_FULL_REPORT.md` section 5.
- Hardware and cost are recorded (RTX 4090, 779.6 s per epoch).
- `docs/DATA_CONTRACT.md` records the nominal detector (LYSO ECAL 20×20,
  3×3×7 cm cells; 64-layer steel/scintillator HCAL).

## 4. Proposed revision

`fast-mc-paper/proposals/claude_20261001/`. Built with `bash build.sh`; numbers
checked with `python verify_numbers.py` (192 checks pass). Seven edit rounds
(`edits_02.json` to `edits_07.json` after the first draft), each followed by a
reading of the rendered PDF.

Kept exactly: title, the 14 original equations, every value in the four
original tables, acknowledgments, AI statement, bibliography.

Changed:

1. Abstract rewritten around question, test case, agreement, disagreement,
   bound, scope.
2. Introduction: physics motivation from the design paper, three numbered
   contributions, one Scope paragraph replacing scattered disclaimers.
3. Detector section: positive description measured from the stored geometry
   (30.3 mm ECAL pitch, 24.9 mm layer pitch, 1.57 m HCAL depth, 54 mm cell
   spacing, 35.7 m and −25.0 mrad), compared with the cited design, then what
   is undocumented, once.
4. New Fig. 1 with a top view of all 65 layers.
5. New Table 1: stage, output, conditioning, model, loss.
6. Generator text split into labelled paragraphs; one paragraph states which
   stage owns which observable. Eq. 4 flagged as the assumption that matters.
7. New Fig. 3: training curve with run boundaries and the selected epoch; text
   notes that epoch 90 beats the next-best epochs by 0.008 against a typical
   epoch-to-epoch change of 0.04, and that overfitting sets in after it.
8. New Fig. 4: schematic of span, gaps, runs and components.
9. Bound promoted to numbered equations 15–18 with a three-step derivation;
   result stated in Results, not deferred.
10. Results use the evidence of 3.4 and 3.5: significance of the response
    difference, deep-layer energy, new Table 3 of shower-shape distances,
    correlation distance.
11. Classifier section explains the below-chance control in two sentences,
    gives both evaluations, and notes that channel-level AUROC below layer-level
    AUROC means the classifier is not using channel information.
12. Limitations as seven labelled items, threshold first.
13. Computing cost gives the 0.24 s upper limit.
14. Conclusion adds the practical lesson for validating surrogates.
15. Internal bookkeeping (tolerance history, hash narrative) moved to App. A.
16. Limitations note that the Geant4 empty fraction (0.93%) is about ten times
    the punch-through probability of a seven-interaction-length detector, so
    acceptance, which the condition cannot express, is likely to matter.

Measured effect on the prose: bookkeeping vocabulary 59 → 8 occurrences;
"unavailable/unverified/…" 21 → 0. Negations stay near 15 per 1,000 words
because the result itself is a disagreement.

Not included, by choice: the descendant-checkpoint table (3.2) and the
reconstruction proxy (3.6). Both were excluded from the paper on purpose
earlier; re-admitting them is the author's decision.

## 5. Decisions for the author

1. **AI statement.** It names OpenAI Codex only. If any text from the proposal
   is adopted, the statement must be updated.
2. **QA guards.** Adopting the proposal trips the 14-page cap (18 pages), the
   14-equation and 4-table/4-figure expectations, and required phrases such as
   "aggregate-only" in `scripts/full_manuscript_qa.py`.
3. **Check against sources** before use: design-paper numbers (25 cm² tiles,
   3 mm, 60×60×162 cm³, 7 λ, z ≈ 35 m, 50%/√E, 3 mrad/√E) were read from the
   arXiv HTML through an automated summary; "RTX 4090, about 13 minutes per
   epoch" and "8,000 showers" come from project documents, not from the paper
   repository.
4. **Date** on the title page is September 2026.
5. Whether to re-admit the evidence in 3.2 and 3.6.

## 6. Work that would change the verdict, in order

1. Rerun the battery on the same bank with per-event output: exact runs and
   `Q`, histograms, component size and energy, a channel-threshold scan
   (0, 0.1, 0.25, 0.5 MeV), an event display, pair-grouped classifier,
   generation-only timing. About one GPU-hour.
2. Run the same battery on `v3-s4-activity-ar` and `v3-s4-activity-span`.
3. Ask the data owner for the geometry tag, Geant4 version, physics list and
   identifier map.
4. Three seeds and a fit on the full training partition.

Items 1 and 2 are new declared experiments on DiCOS and were not started.

## 7. Passes performed

1. Cold read of the 14-page PDF, all pages as images; every equation and table
   re-derived by hand.
2. Context: `main.tex`, README, STATUS, logs, the fresh-reader assessment of
   2026-09-30 and the three external-audit responses.
3. Context: evaluation summary, provenance, geometry, training history; every
   reported number recomputed.
4. Context: model source and project documents (HANDOFF, V3 report, data
   contract, GPU benchmarks, screening summary, all battery reports).
5. Proposal draft 1: full read of 18 rendered pages.
6. Draft 2 (16 edits): accuracy pass; three numeric mismatches found by script
   and fixed.
7. Draft 3–4: full text read as a referee; layout pass on rendered pages.
8. Draft 5–6: jargon and negation count against the original; full read.
9. Draft 7: experimentalist-sceptic pass (energy spectrum of the sample,
   acceptance versus punch-through for empty showers); final layout check.

Test events used: 0. No training, generation or DiCOS command was run. In the
paper repository the only change outside `proposals/claude_20261001/` is one
appended entry in `logs.md`, which the release binding does not hash.
