# Mentor-send clarity revision

Version 0.22.1 is a reader-facing revision of the one-checkpoint aggregate diagnostic note. It is not detector-performance validation.

## Abstract

Named the incident neutron, gave both sample values for the active-layer and group counts, and replaced row-split and condition-only jargon with the plain statement that the control gives 0.464 rather than 0.5.

## Definitions removed by earlier condensing

Restored: Wasserstein-1 distance for any scalar observable, the reference-half scale (two disjoint 5,000-event Geant4 halves), edge co-occupancy, closure residuals, support, free-running, and the Bernoulli-draw versus zero-clamp origin of empty showers. Each was used in Results without a prior definition.

## Naming

Table 1 body is byte-locked, so its caption now maps inactive layers in span to G and weak graph components to the graph-connected hit groups m. Figure 4 bars are labelled generator, as in Figure 3 and Table 1.

## Figures in Results

Sections 5.2 and 5.3 now cite Figure 4, which was referenced only from the evaluation section, and quote the Figure 3 mean-profile ratio at layers 51, 60 and 64.

## Physical scale

Stated that the stored total is about 3 percent of the 149.9 GeV mean incident kinetic energy and is neither a calibrated energy nor a sampling-fraction measurement; converted the 4.42-layer shift to about 0.11 m with the stored 24.9 mm HCAL layer spacing.

## Energy-bin table

Added the independent-sample error scale already adopted for the pooled mean: width comparable to mean in every bin, standard error near 3 percent, largest binwise difference 2.0 standard errors. No paired interval or chi-square is claimed.

## Transverse summaries

Added nonempty-sample energy-weighted centroid differences (0.5 mm, 1.1 mm) and radial RMS (84.7 versus 87.1 mm; W1 3.34 mm against a 0.48 mm reference-half scale) from the released report. Centroid W1 values are not quoted because the zero-deposit mass at the origin dominates them.

## Discussion tests

Rewrote the reference-activity-null and oracle-cascade sentences as concrete procedures; content unchanged.

## Equation punctuation

Numbered equations are byte-locked. The sentences following Eqs. 1, 10 and 12, which end with commas, now continue grammatically.

## Not changed

No numbered equation, numerical table body, figure data, model statement or evidence limit was altered. The title result still has no distribution, interval or threshold scan; that requires an event-level evaluation and is not a prose matter.

## Evidence

The JSON twin records every replaced string by hash with its replacement, the inserted paragraph, the checked evaluator source files and the primary references reread. Added numbers are recomputed in `scripts/mentor_send_checks.py`.

## Second pass after QA01

QA01 passed at 14 pages, but reading every page showed white gaps on pages 1, 6 and 7. The abstract had grown by one line and displaced Section 2. Two abstract clauses were shortened without removing a number, restoring the page flow. The same pass unified half-split with reference-half scale, named both samples in the ECAL-start sentence, expanded FP32 once, and fixed the activity-indicator wording.

## Third pass: word-by-word reading of QA02

The sealed QA02 manuscript was read in full, page by page and then word by word in source, and every quoted number was recomputed from the released report. All numbers, equations and tables hold. Section 5.1 called -7.65% the largest binwise mean difference although Table 3 lists +7.74%; the sentence now quotes both with their error scales (1.8 and 2.0 standard errors) and says mixed rather than alternating signs. Nine wordings were clarified: which sample has the narrower radial RMS, cancellation in place of compensation in the Figure 3 caption, the run tag introduced as the same checkpoint, an unclear pronoun, deeper in place of later, zero-threshold in place of a reused energy symbol, a repeated word, how the classifier battery splits showers, and what graph edges join. No number, numbered equation, table body or figure changed, and the page breaks are identical. Reasons, hashes and the items verified without change are in the JSON twin.
