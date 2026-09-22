# Primary literature benchmark, revised 2026-09-21

The study documents one sparse-readout case of close means with different support structure. Existing calorimeter evaluation already goes beyond marginals; no novelty claim is made for that general principle.

The v0.5.0 framing follows the organization common to representative HEP and computational-physics papers available before November 2025: motivate detector simulation, define the physical target and observable representation, describe the surrogate and numerical method, report detector-level observables, and only then state the broader methodological implication. CaloFlow, CaloGraph, CaloDREAM, CaloChallenge, and the July 2025 ALICE ZDC flow-matching preprint were used as style and organization references. Their scientific claims were not imported into this manuscript.

- [Geant4 toolkit](https://www.sciencedirect.com/science/article/pii/S0168900203013688): Particle-transport toolkit and original reference metadata; no validation of this production configuration.
- [CaloFlow](https://arxiv.org/abs/2106.05285): Normalizing-flow calorimeter surrogate; published PRD title retained.
- [CaloDiffusion](https://arxiv.org/abs/2308.03876): Diffusion with geometry adaptation; method-family precedent.
- [CaloGraph](https://arxiv.org/abs/2402.11575): Graph diffusion on irregular calorimeter geometry; no cross-detector ranking.
- [CaloClouds II](https://arxiv.org/abs/2309.05704): Point-cloud generation; published JINST 19 (2024) P04020.
- [CaloDREAM](https://arxiv.org/html/2405.09629v3): Sections 4.4-4.5 explicitly examine different high-/low-level classifier diagnostics and sparse-feature failure modes; supports acknowledgment of prior evaluation work.
- [CaloChallenge 2022](https://arxiv.org/abs/2410.21611): Community comparison includes univariate distributions, multivariate tests, timing and model size. Primary project page confirms publication 88 (2025) 116201.
- [Full physics benchmark](https://arxiv.org/html/2511.17293v1): Post-reconstruction observables and full physics benchmarks; primary class hep-ex corrected.
- [ALICE Zero Degree Calorimeter flow matching](https://www.sciencedirect.com/science/article/pii/S0010465525004370): CPC 319 (2026) 109936 verified. arXiv full text Section 1 describes optical-fiber photon-count images, different from raw deposits here.
- [CaloClouds3](https://arxiv.org/abs/2511.01460): First author Thorsten Buss, ten authors; JINST 21 (2026) 03 P03018. Corrected author/year/DOI. Cited for point clouds, not unsupported multivariate-testing assertion.
- [ParaFlow](https://arxiv.org/abs/2503.21461): Upstream-material-conditioned toy calorimeter; EPJ C 85 (2025) 857. Metadata updated.
- [Flow Matching](https://arxiv.org/abs/2210.02747): Probability-path vector-field regression. Actual straight path, masks and eight time-centered Euler updates verified in local source, not attributed to paper as a universal requirement.
- [Gumbel Top-k](https://proceedings.mlr.press/v97/kool19a.html): Sampling without replacement and exact cardinality; does not establish learned support fidelity.
- [Classifier two-sample tests](https://arxiv.org/abs/1610.06545): Held-out classification; grouping matched conditions is this project-specific extension and no longer overattributed to original IID formulation.

## Pre-November-2025 framing references

- [CaloFlow](https://arxiv.org/abs/2106.05285): establishes the detector-simulation problem before introducing the model and evaluates concrete calorimeter observables.
- [CaloGraph](https://arxiv.org/abs/2402.11575): connects an irregular detector representation to an architecture designed for that geometry.
- [CaloDREAM](https://arxiv.org/abs/2405.09629): orders the paper as simulation motivation, data, method, observable-level results, and outlook.
- [CaloChallenge 2022](https://arxiv.org/abs/2410.21611): treats model evaluation as a physics problem spanning univariate, multivariate, timing, and model-size diagnostics.
- [ALICE ZDC flow matching, July 2025 preprint](https://arxiv.org/abs/2507.18811v1): uses detector-specific target and metric language before broader surrogate-model claims. Its photon-count images and performance numbers are not directly comparable to the raw-deposit readout studied here.

Cross-detector numerical ranking is excluded. Differences in raw deposits versus photon-count images, geometry, conditions, thresholding and timing prevent a fair ratio. No citation proves this project's detector or reference physics configuration.
