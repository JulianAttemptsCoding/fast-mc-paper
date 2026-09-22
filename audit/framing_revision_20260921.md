# HEP and computational-physics framing revision

Status: complete. Full automated QA iteration 28 passed, and all 12 final rendered pages passed direct visual review.

The v0.5.0 manuscript package was pushed to GitHub `main` in content commit `757c36817a4185d25752b6211b511606fc39e03f`; `git ls-remote` returned the same branch head.

The manuscript now follows the sequence used in representative detector-simulation papers available before November 2025: establish the detector-simulation problem; define the physical target and readout; describe the numerical surrogate and enforced constraints; report detector observables; then state the broader computational implication.

## Framing hierarchy

1. **Detector observation:** the generated showers have similar mean layer and channel multiplicities but more interior inactive layers and more disconnected regions on the readout graph.
2. **HEP implication:** inclusive response and occupancy agreement do not establish correct shower morphology.
3. **Computational-physics implication:** numerical admissibility, agreement in low-order detector observables, and structural fidelity are distinct properties of a learned stochastic surrogate.

The title, abstract, introduction, section hierarchy, results, interpretation, scope, conclusion, figure title, repository metadata, and release checks use this ordering. The paper retains the single-checkpoint and development-bank scope. It does not promote the artifact to a validated fast-simulation model or infer a causal architectural mechanism.

## Style references

- CaloFlow, arXiv:2106.05285: detector-simulation motivation followed by model and calorimeter-observable validation.
- CaloGraph, arXiv:2402.11575: detector geometry connected explicitly to model representation.
- CaloDREAM, arXiv:2405.09629: simulation motivation, data, method, detector-level results, and outlook.
- CaloChallenge 2022, arXiv:2410.21611: physics evaluation organized across complementary observables and diagnostics.
- ALICE ZDC flow matching, arXiv:2507.18811v1, July 2025: detector-specific target and metric language before broader surrogate-model claims.

These papers were used for organization and disciplinary register, not as a source of copied phrasing or transferable numerical claims. Later papers remain in the scientific bibliography where relevant, but they were not used to set the requested pre-November-2025 writing style.
