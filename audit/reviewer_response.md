# Disposition of the supplied reviews

Date: 2026-09-20

The three supplied reviews are preserved verbatim in `reviews/`. This document records how the current manuscript addresses them. A resolved item means the manuscript now states the available evidence accurately; it does not turn preliminary evidence into final validation.

## Resolved in the manuscript and repository

1. **Scope and title.** Removed an unmeasured speed claim from the title and framed the work as a preliminary development-bank study.
2. **Evaluation governance.** Reclassified the repeatedly inspected 10,000-condition bank as development data and disclosed unresolved historical exposure of the nominal test set.
3. **Pilot scale.** States that the 26,624-event model-development sample is 4.35% of the canonical training split.
4. **Condition-only C2ST.** Excludes the malformed random-fold control and uses the separately verified pair-grouped, energy-stratified condition-only AUROC of exactly 0.500.
5. **C2ST specification.** Defines the classifier family, feature families, folds, evaluator seeds, reported spread, sample size, and limitations of the battery split.
6. **Response distribution.** Explains the Gaussian response mixture, negative draw clamp, and resulting second source of exact zeros.
7. **Flow coordinates.** Defines the centered log-share transform, numerical floor, teacher-forced training, and ancestral inference path.
8. **Support objective.** States that BCE plus ranking is a surrogate and is not the likelihood of Gumbel top-k or Plackett-Luce sampling.
9. **Common-measure comparison.** Derives the logistic-normal Jacobian adjustment and records the empirical offset calculation and finite-event count.
10. **Metric definitions.** Gives equations for unconditional response bias, response-width difference, profile L1, strict-zero activity, and graph fragmentation.
11. **Detector graph.** Documents the same-layer and adjacent-layer neighbor construction, edge count and features, directed edge convention, and ganged-channel limitation.
12. **Negative result.** Promotes the S2 zero-response failure to a central result showing that the scalar development objective can select a physically unusable generator.
13. **Figures.** Adds ECAL explicitly, uses point estimates for energy-bin response panels, limits displayed precision, and labels missing uncertainty.
14. **Literature.** Adds Geant4, AtlFast3, CaloChallenge, CaloFlow, iCaloFlow, CaloScore, CaloDiffusion, CaloGraph, L2LFlows, CaloPointFlow II, flow matching, support sampling, and C2ST references; updates published bibliographic records where available.
15. **Authorship and acknowledgements.** Lists Julian Juan as author and acknowledges Dr. Wen-Chen Chang of the Institute of Physics, Academia Sinica, for mentorship.
16. **Availability.** Adds a public-repository statement and distinguishes figure reproducibility from unavailable training and Geant4-production inputs.

## Evidence gaps retained as limitations

The current artifacts do not support closing the following items, so the manuscript states them as required follow-up work:

- production Geant4 version, physics list, cuts, detector materials, and full generator provenance;
- exact event identifiers and a newly locked validation/test governance scheme;
- three independent generator-training seeds for each frozen final condition;
- repeated Geant4 and generated showers at fixed conditions to test stochasticity;
- uncertainty intervals for every energy-bin and topology observable;
- stability under nonzero hit thresholds and an independent physical-cell graph;
- complete frozen configuration, parameter count, checkpoints, and environment capture;
- matched empirical and learned baselines, downstream reconstruction studies, and end-to-end timing including data movement and decoding;
- a full negative-result report if the longitudinal fragmentation persists.

These gaps are submission blockers for a strong fidelity or acceleration claim. They do not invalidate the narrower documented result that structural constraints alone did not produce distributional fidelity in this pilot.
