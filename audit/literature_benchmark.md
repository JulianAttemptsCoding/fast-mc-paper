# Literature benchmark for the manuscript

Reviewed 2026-09-21. This register uses primary publications and preprints. It records how the current manuscript is positioned; it does not claim numerical comparability across detector geometries, preprocessing, conditioning variables, or timing protocols.

| Work | Relevant scope | Consequence for this manuscript |
|---|---|---|
| [CaloChallenge 2022, Reports on Progress in Physics 88 (2025) 116201](https://doi.org/10.1088/1361-6633/ae1304) | Community comparison of calorimeter surrogate models and evaluation axes | Motivates separate reporting of univariate observables, multivariate tests, model size, and end-to-end generation time. The present draft explicitly identifies which of these are missing. |
| [CaloGraph, Physical Review D 110 (2024) 072003](https://doi.org/10.1103/PhysRevD.110.072003) | Graph diffusion for irregular calorimeter geometry | Provides a relevant graph-based precedent. The present graph is a lossy centroid representation of ganged readout IDs and is described as such. |
| [CaloDREAM, SciPost Physics 18 (2025) 088](https://doi.org/10.21468/SciPostPhys.18.3.088) | Attentive conditional flow matching for calorimeter response | Motivates comparison at the method-family level. No direct numerical ranking is attempted because the detector and evaluation protocol differ. |
| [CaloClouds II, Journal of Instrumentation 19 (2024) P04020](https://doi.org/10.1088/1748-0221/19/04/P04020) | Geometry-independent point-cloud calorimeter generation | Shows an alternative to a fixed dense channel graph and motivates the discussion of geometry representation. |
| [CaloClouds3, arXiv:2511.01460](https://arxiv.org/abs/2511.01460) | Recent point-cloud development with emphasis on fast generation | Reinforces that speed claims require a matched timing protocol; this manuscript makes none. |
| [A First Full Physics Benchmark for Highly Granular Calorimeter Surrogates, arXiv:2511.17293](https://arxiv.org/abs/2511.17293) | Detector integration and reconstructed/full-physics evaluation | Sets a stronger validation target than aggregate shower summaries. The missing reconstruction study is an explicit limitation here. |
| [ParaFlow, arXiv:2503.21461](https://arxiv.org/abs/2503.21461) | Calorimeter simulation parameterized by upstream material configuration | Supports treating upstream transport and material configuration as part of the conditional target. The present production metadata cannot fully resolve that state. |
| [Even Faster Simulations with Flow Matching: A Study of Zero Degree Calorimeter Responses, Computer Physics Communications 319 (2026) 109936](https://doi.org/10.1016/j.cpc.2025.109936) | Flow-matching application to ALICE Zero Degree Calorimeters | It is the closest application-level comparator. Different geometry, representation, preprocessing, and metrics make direct fidelity or timing ratios inappropriate. |

## Positioning decision

The defensible contribution is a carefully audited failure analysis: exact decoder constraints and close marginal statistics coexist with incorrect longitudinal and graph dependence. The manuscript does not claim a new state of the art, a validated detector surrogate, or a measured speedup. This scope is narrower than recent benchmark papers, but the evidence supports it directly.

## Evaluation gap relative to recent practice

Before a production or physics-fidelity claim, the project still needs a locked evaluation bank, multiple training seeds, repeated showers at fixed conditions, valid grouped multivariate tests, independent geometry diagnostics, reconstructed observables, controlled baselines, and matched end-to-end timing.
