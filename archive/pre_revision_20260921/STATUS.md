# Scientific status

Version 0.3.0 is an auditable development-bank manuscript. It is a defensible preprint draft about a specific generator failure pattern, rather than a final Fast MC validation or speed result.

## Supported by the current evidence

- The accepted `dicos-f-02` epoch-90 checkpoint is the minimum-validation-objective state in the recorded single-seed lineage through epoch 114. Two later continuation attempts did not improve the selection quantity.
- The generator used the 551,234-event generator role. The remaining two 30,624-event training roles were reserved for planned critic work and were not used by the reported generator.
- All quantitative results use a repeatedly inspected 10,000-condition validation bank over 50--250 GeV. No nominal-test event appears in the manuscript.
- The decoder realized requested channel counts and generated budgets across 1,250 recorded evaluation batches, with zero nonfinite, negative, dust, support-mask, or count-mismatch findings.
- Close total-deposit and active-count marginals coexist with compensating ECAL/HCAL errors, excessive interior gaps, and substantially more weak readout-graph components.
- The retained condition-only AUROC of 0.500 checks pairing only. All shower-aware classifier outputs from the invalid evaluator are excluded.

## Current claim boundary

The evidence supports this statement: for this checkpoint and development bank, deterministic output constraints and close marginal counts do not ensure the joint longitudinal and spatial structure needed from a calorimeter surrogate.

The evidence does not support final conditional fidelity, architecture superiority, reconstruction equivalence, cross-detector ranking, or acceleration.

## Required before a physics-fidelity or production claim

1. Freeze a new evaluation bank with exact event identifiers and no adaptive inspection.
2. Train at least three independent seeds for every frozen final condition.
3. Generate repeated Geant4 and model showers at fixed conditions.
4. Run pair-grouped shower-only and joint condition-plus-shower C2STs with permutation and same-source controls.
5. Measure response-cap activations, reference cap exceedances, CLR clipping frequency and moved energy, and solver-step convergence.
6. Run the component-wise teacher-forced and oracle-versus-ancestral cascade.
7. Report angle dependence, energy-angle maps, tails, distributions rather than means alone, and threshold-stable topology.
8. Validate topology with an independent physical-neighbor representation that preserves ganged-channel geometry.
9. Add matched simple baselines and relevant published baselines under the same readout semantics.
10. Evaluate reconstructed observables and end-to-end timing, including transfer and decode costs.
11. Archive complete Geant4, detector, material, field, cut, software, and random-seed provenance.
12. Resolve collaboration data ownership, authorship, and an immutable archival release before submission.
