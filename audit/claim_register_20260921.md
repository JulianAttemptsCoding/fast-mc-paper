# Claim register and scientific corrections

The final claim is a detector-specific validation result for one artifact: decoder-level numerical validity and percent-level agreement in selected inclusive response and occupancy observables coexist with substantially more fragmented longitudinal and readout-graph shower support. It does not require full marginal agreement or a causal training explanation.

| ID | Claim | Evidence / disposition |
|---|---|---|
| C01 | Close mean occupancies coexist with more fragmented support for this checkpoint/bank. | Aggregate activity/count/topology fields; all conditional means recomputed with nonempty fractions. No population-general or causal inference. **supported within stated scope** |
| C02 | 26624 training /6656 selection-validation pilot; 764940 canonical corpus with 612482/76158/76300 partitions. | source_evidence pilot_training exact config hash + canonical_preparation; the 551234 role belongs another model. **corrected** |
| C03 | 10000 diagnostic conditions, 50-250 GeV; training/selection/diagnostic roles distinct; historical nominal-test exposure disclosed. | Report identity, source evidence battery contract, source docs/PIPELINES.md and existing terminal-gate evidence. **supported within stated scope** |
| C04 | 6790 readout channels, 65 layers, 400 ECAL +6390 HCAL; physical-position multiplicities 4390/1950/444/6. | geometry_summary.json and readout_geometry.npz; checks verify count/layer/multiplicity arithmetic. **supported within stated scope** |
| C05 | Fixed centroid graph and 107920 directed edges; topology tied to that representation. | Frozen geometry summary and model graph precedent; ganged positions cannot be individually recovered. **supported within stated scope** |
| C06 | Condition order logK,ux,uy,uz,logE; zero-direction denominator convention. | Source features.py exact implementation hash in source_evidence. **corrected** |
| C07 | 2082507 parameters for reported checkpoint alias B0. | Historical v3_parameter_counts_20260816.json; source_evidence records input hash and method. **supported within stated scope** |
| C08 | Gaussian-mixture transformed response, Bernoulli branch, zero projection, cap at frozen constants. | Source response.py and report identity; cap values preserved in archived inherited portable config. No cap-activation claim. **supported within stated scope** |
| C09 | Independent post-first-layer Bernoulli activities, CLR flows, eight first-order time-centered updates. | Source profile.py/system.py + report steps. No convergence or invertibility claim. **supported within stated scope** |
| C10 | Counts satisfy masks, Gumbel draw without replacement, support BCE and ranking, conditional masked share flow. | Source support.py/losses.py and Gumbel Top-k primary paper. **supported within stated scope** |
| C11 | Piecewise decoder including empty supports; exact identities are real-arithmetic statements. | Source decode_exact_support; finite-precision checks distinct. Removed universal strict-positivity guarantee and malformed equation. **corrected** |
| C12 | Nine weights and clipped geometric-mean-over-median calibration. | source_evidence calibration audit + weights.py. Actual normalized numbers recomputed by QA. **corrected** |
| C13 | One declared post-90 continuation and documented scheduler restart; epoch90 objective minimum4.483768. | 104 unique contiguous history rows, provenance hash and terminal gate. Incorrect scheduler variant excluded. **corrected** |
| C14 | Interior missing layers6.04879 vs2.10215, ratio2.87743; NOT separate gap runs. | Source _activity_report at historical commit dce44556; exact mean_span - conditional mean_active_layers identity verified on both sides. **corrected P1 metric definition** |
| C15 | Gap-event prevalence93.53% vs52.43%; means conditional on nonempty. | activity.gap_fraction, first_layer source, explicit n_generated9858 and n_reference9907. **supported within stated scope** |
| C16 | Active channels1588.819 vs1617.568; weak components59.3895 vs23.4192; largest fractions88.8709% vs94.9006%. | counts/topology all-event aggregates divided by nonempty fractions; topology.py zero-event convention checked. **supported within stated scope** |
| C17 | Mean total4.36936 vs4.32418; ECAL+8.3%, HCAL-5.8%; profile L1=0.070965. | distribution_metrics profile and total; weighted bin consistency recomputed. **supported within stated scope** |
| C18 | Bin mean differences-7.7%..+7.7%, width differences-10.9%..+9.6%. | positive_response.response_bins all-event moments; no reconstruction or error-bar interpretation. **supported within stated scope** |
| C19 | W1=0.0727 GeV and exploratory nominal95% bootstrap endpoints; reference-half0.1475 not calibrated floor. | bootstrap fields and correlations.py/v3_battery.py; 5000-vs5000 reference versus10000-vs10000 generator comparison. **corrected** |
| C20 | Recorded all1250 batches pass under batch-maximum-scaled tolerance; layer residual exceeds old absolute-only criterion. | structural_invariants + source invariants.py; old and new rules stated without edits. Aggregate lacks per-batch reports. **corrected** |
| C21 | Raw-mode dust zero is trivial, while support/counters and finite values are actual recorded checks. | invariants.py conditional dust counter; threshold0. **corrected** |
| C22 | Condition-only AUROC0.500 is not shower-fidelity or complete leakage evidence; historical shower-aware outputs excluded. | condition_only_control.json, source contract and C2ST primary paper. **corrected interpretation** |
| C23 | Four-node path example proves accounting/cardinality do not determine support connectivity. | Direct arithmetic: (1,1,0,0) and (1,0,1,0) both sum2 with two active nodes; induced path supports have1 and2 components. **algebraic illustration only** |
| C24 | Architectural and training causes remain hypotheses; no demonstrated repair or all-model claim. | No oracle cascade or controlled alternatives in retained evidence. Limits stated consistently. **supported within stated scope** |
| C25 | Potential EIC ZDC use is motivation, not verified detector equivalence, affiliation or readiness. | User steering; noted in STATUS only. **not a scientific claim** |
| C26 | Source/figures rebuild from aggregates, no independent retraining or event-level tests. | Public-package contents inspected; model checkpoint and raw data absent. **supported within stated scope** |

## Primary literature

- [Geant4 toolkit](https://www.sciencedirect.com/science/article/pii/S0168900203013688): Particle-transport toolkit and original reference metadata; no validation of this production configuration.
- [CaloFlow](https://arxiv.org/abs/2106.05285): Normalizing-flow calorimeter surrogate; published PRD title retained.
- [CaloDiffusion](https://arxiv.org/abs/2308.03876): Diffusion with geometry adaptation; method-family precedent.
- [CaloGraph](https://arxiv.org/abs/2402.11575): Graph diffusion on irregular calorimeter geometry; no cross-detector ranking.
- [CaloClouds II](https://arxiv.org/abs/2309.05704): Point-cloud generation; published JINST 19 (2024) P04020.
- [CaloDREAM](https://arxiv.org/html/2405.09629v3): Sections 4.4-4.5 explicitly examine different high-/low-level classifier diagnostics and sparse-feature failure modes; supports acknowledgment of prior evaluation work.
- [CaloChallenge 2022](https://arxiv.org/abs/2410.21611): Community comparison includes univariate distributions, multivariate tests, timing and model size. Primary project page confirms publication 88 (2025) 116201.
- [Full physics benchmark](https://arxiv.org/html/2511.17293v1): Post-reconstruction observables and full physics benchmarks; primary class hep-ex corrected.
- [ALICE flow matching](https://www.sciencedirect.com/science/article/pii/S0010465525004370): CPC 319 (2026) 109936 verified. arXiv full text Section 1 describes optical-fiber photon-count images, different from raw deposits here.
- [CaloClouds3](https://arxiv.org/abs/2511.01460): First author Thorsten Buss, ten authors; JINST 21 (2026) 03 P03018. Corrected author/year/DOI. Cited for point clouds, not unsupported multivariate-testing assertion.
- [ParaFlow](https://arxiv.org/abs/2503.21461): Upstream-material-conditioned toy calorimeter; EPJ C 85 (2025) 857. Metadata updated.
- [Flow Matching](https://arxiv.org/abs/2210.02747): Probability-path vector-field regression. Actual straight path, masks and eight time-centered Euler updates verified in local source, not attributed to paper as a universal requirement.
- [Gumbel Top-k](https://proceedings.mlr.press/v97/kool19a.html): Sampling without replacement and exact cardinality; does not establish learned support fidelity.
- [Classifier two-sample tests](https://arxiv.org/abs/1610.06545): Held-out classification; grouping matched conditions is this project-specific extension and no longer overattributed to original IID formulation.

## Research access and limitations

Every cited source has a primary-source record. Where an HTML/DOI route failed, the author preprint or publisher search record was used. The CaloChallenge HTML endpoints and guessed CERN publication route failed; these are retrieval failures, not missing scientific evidence. The exact runtime configuration and per-event arrays are not released here. All aggregate values remain unchanged.
