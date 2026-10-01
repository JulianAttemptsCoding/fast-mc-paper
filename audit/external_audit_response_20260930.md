# Response to supplied external audit

The audit exposed a genuine missing mathematical inference in v0.16.0. Version 0.17.0 corrects the main conclusion rather than treating the audit as a stylistic review. The paper is prepared as an arXiv diagnostic preprint; document QA is not a certification of physics-journal readiness.

## B1 — Accepted, central correction

Q=m-R obeys m-1-G <= Q <= m-1. Exact aggregate means give delta Q >=29.92153994, 83.18394% of delta m. Abstract, protocol, discussion and conclusion now state the within-run discrepancy. Figure 4 displays the algebraic ranges. Within-run is not purely lateral and is not causal attribution: gaps can also alter connections within the remaining runs. The audit's estimated island size multiplies means and divides by a mean count; E[N(1-f)] need not equal E[N](1-E[f]), so that estimate is not added.

## B2 — Plausible conditional mechanism, not established cause

Added an exact two-layer example: after fixed first layer, independent Bernoullis preserve mean activity but create p(1-p) gap probability and last-layer shift relative to a perfectly correlated pair. This verifies a possible signature, not the observed 4.42-layer magnitude. Sampled T/F induce unconditional dependence. The claim that T correlates only weakly with interaction depth is unmeasured. Reference null should control direction as well as energy/T/F. Teacher-forcing T/F does not change factorization; the oracle proposal now explicitly replaces the whole activity mask. L2LFlows and iCaloFlow cited. No matched reference arrays found locally, so no null experiment claimed.

## B3 — Accepted scope correction; new experiment deferred

Explicitly distinguishes stored deposits from electronics readout, states no added time cut and unknown production integration window, and explains sensitivity to soft/late energy. It is not established that the counts are dominated by sub-MIP hits. A numerical MIP threshold and time cut require technology calibration and hit-time metadata. Raw mode remains the frozen target; changing it without a separately specified experiment would mix target semantics. A split energy spectrum cannot be reconstructed from retained means/Wasserstein summaries.

## B4 — Accepted detector-response distinction

Removed the 1% raw-total comparison from the abstract and conclusion. Kept accurately labeled raw-deposit values in results. Explicitly says ECAL/HCAL compensation is only in an unweighted stored-energy sum and implies no calibrated agreement. A training-only calibration fit is appropriate follow-up but requires training event deposits; it is not metadata-free validation of detector response. No validation/test data fitted.

## B5 — Resolved identity/permission by author; geometry tag unresolved

Author confirms ePIC ZDC and that data owner approves publication. Added detector identification and primary design reference. No exact production tag supplied or recovered. Did not infer a historical tag from channel counts or transverse coordinates; no equivalence to current design claimed. No institutional affiliation added, respecting the explicit earlier removal request.

## B6 — Accepted research-readiness boundary

Rendering/arithmetic QA cannot establish journal readiness. The paper remains an arXiv diagnostic preprint with incomplete robustness and reproducibility evidence. An uninspected-event count does not identify a locked bank; exact IDs and historical overlap must first be resolved. No test remainder opened and no new training launched.

## M1 — Accepted wording correction

Binwise differences are now descriptive; no inference of energy-dependent bias without intervals. Archived bootstrap output contains four aggregate metric intervals, not binwise mean/width intervals, so the claim that those intervals are already available is unsupported by the retained report. Apparent zigzag alone does not prove reference noise either.

## M2 — Qualified, uncertainty wording corrected

Abstract now emphasizes untested variation across fits, thresholds and graphs; protocol still accurately states which paired intervals are unavailable. The suggested independent-sample normal approximations are assumption-dependent for matched, separately nonempty samples on a repeatedly inspected bank. A variance bound is not by itself a Gaussian-tail or sigma-significance proof. Strong sample differences remain visible; they do not establish threshold/graph/training robustness. No invented paired CI added.

## M3 — Accepted diagnostic concern; all failures retained

Main text identifies possible opposite-label twin bias and failed condition-only control, and disclaims calibrated fidelity interpretation. Appendix explains 42% pair straddling under 70/30 rows. Replaced unverified predeclared wording with recorded screening maximum; timing of its declaration is not independently established. Did not erase the failed historical battery. The separate-bank 0.893 is not proof of bias size; same-bank grouped C2ST remains undone.

## M4 — Accepted hypothesis with sampler qualification

Added mismatch between BCE logits and fixed-K inclusion probabilities and possible fragmentation from independent perturbations. Empirical occupancy miscalibration is not proved by loss/sampler mismatch alone. Conditional-Poisson conditioning also changes marginal inclusion probabilities; it is not an automatic sigma(s)-calibrated replacement. No sampler changed and no calibration plot invented.

## M5 — Accepted missing-conditioning concern

Added impact-position caveat and proposed direction-to-position residual test. Whether momentum direction fixes impact position requires verified vertex and recording surface. No centroid residual RMS or missing-position causality is claimed.

## M6 — Joint data unavailable; interpretation corrected

Marginal empty rates alone cannot identify acceptance learning. With a both-empty count a in [0,93], the paired table is: both a, reference-only 93-a, generator-only 142-a, neither 9765+a. This non-identifiability is why no unique contingency table or geometric-acceptance explanation is reported.

## M7 — Partly recovered, other new measurements deferred

Recovered two retained reference-half hit-count Wasserstein comparisons: 13.7816 (deterministic event-ID halves) and 15.816 (seeded permutation halves), 5000 per half. Both are reported as finite-sample scales, not critical values or matched-size significance baselines. Reconstruction, full structural distributions, spectra and displays require events. Archived scalar radial summaries cannot replace radial distributions.

## M8 — No speed claim

Retains explicit statement that 0.344 seconds/event includes evaluator work; there is no isolated generation latency or matched Geant4 timing. Generic computational motivation is background, not an asserted speedup. Published ALICE timing uses a different target/model and is not a comparable benchmark.

## M9 — Accepted graph limitation

Shared centroid kNN connectivity is kept as the explicitly defined mathematical diagnostic. Physical adjacency requires tile shape/ganging/overlap metadata and separate evaluation. The new within-run bound holds for the stated same/adjacent-layer graph; it does not validate it as physical adjacency.

## M10 — Novelty scope narrowed and literature expanded

States correlation-sensitive validation is established in prior work; explains complementary conditional Jaccard co-activation and within-run component diagnostics. Adds L2LFlows, iCaloFlow and IAF ZDC reference. A legacy recurrent model cannot be an unverified baseline; user operating contract forbids importing/training from legacy. No comparative superiority claimed.

## Technical — Clarified without altering model

Eq7 identified as first-order explicit update with midpoint-time evaluation, not midpoint Runge-Kutta. Solver study remains unperformed. Cap described as a training-derived tail safeguard, not a sampling fraction. Weight clipping limitations retained. Teacher-forced checkpoint need not minimize free-running discrepancies. Current trainer source averages training minibatches and validates at epoch end; historical runtime identity is still unverified. Edge co-occupancy explicitly not occupancy-normalized. Numerical tolerance discrepancy remains prominently disclosed, not hidden by moving it.

## Presentation — Revised

Figure4 now shows algebraic bounds instead of redundant means; no fabricated distributions. Coordinate convention and lack of X0/lambdaI mapping stated. Geant4 citation no longer attributed as the source of per-ID preprocessing. Version/build-audit details moved from manuscript availability prose to README. Repository was already a live hyperlink; the audit assertion of no URL was incorrect. Internal checkpoint names retained in reproducibility appendix as useful artifact identifiers. Abstract opening replaced; user-requested name/email-only author line retained. Equal training/generation seed integer explicitly noted.

## References — Primary-source research

Earlier turn verified all 18 cited reference identities/relevance through primary pages; this turn checked proposed interlayer/ZDC references and detector design/prototype sources. Added four directly relevant references; did not pad bibliography with scheduled sampling or conditional-Poisson methods that were neither implemented nor needed to support a claim.

## arXiv — Preparation, not submission

Author selects arXiv. Official help currently supports pdfLaTeX and TeX Live 2025 with biblatex bbl format 3.3; local main.bbl uses 3.3. Package will contain only main.tex, references.bib, main.bbl and four used PNGs, excluding old PDFs, audit files, reviews and logs. Server-side compile/moderation cannot be certified locally. No upload or license selection performed.

## Sources

- https://arxiv.org/abs/2302.11594
- https://arxiv.org/abs/2305.11934
- https://arxiv.org/abs/2512.20346
- https://arxiv.org/html/2608.12795v1
- https://arxiv.org/abs/2406.12877
- https://arxiv.org/abs/2603.14167
- https://info.arxiv.org/help/submit_tex.html
- https://info.arxiv.org/help/faq/texlive.html

## Validation record

All 14 original numbered equations and four original numeric tables are preserved. New deterministic bounds and the two-layer example have dedicated algebra checks. Full build attempts and final exact-PDF visual review are recorded separately; failed attempts are retained.

## Final verification

QA96 passed all 17 groups at 14 pages; all pages directly reviewed. Seven release-guard tests passed. The seven-file source ZIP is created and byte/CRC verified. The native editor compiler remains unavailable because of its platform-directory error; the local LaTeX/Biber build succeeded. No new event-level experiment or external submission was performed.
