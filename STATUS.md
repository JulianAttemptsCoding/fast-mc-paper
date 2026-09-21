# Scientific status

Version 0.2.0 is an auditable development-bank manuscript and aggregate figure package. It is not a final physics validation or speed result.

## Evidence currently supported

- V3-SUP epoch 12 has 2,082,507 trainable parameters and was optimized on the 551,234-event `generator_train` role over 0--300 GeV.
- Every paper figure uses the repeatedly inspected 10,000-event development battery over 50--250 GeV, except the explicitly separated 4,096-event component-loss screen.
- The decoder passed its recorded finite, nonnegative, support, count, and generated-budget checks on the plotted artifacts.
- The development bank shows excessive interior gaps, weak readout-graph fragmentation, reduced channel occupancy, and excess mean ECAL-layer energy.
- S2 improved its matched common-measure scalar loss relative to M0 while producing a 50.41% zero-deposit fraction on the separate battery. The existing evidence does not identify the cause.
- The historical shower-only C2ST is excluded from scientific claims. Its random pair split and omission of the condition do not test conditional fidelity.

## Required before a physics-fidelity claim

1. Create a newly locked evaluation bank and keep a separate repeatedly used development bank.
2. Run a pair-grouped joint C2ST on `(c_raw, shower features)` with condition bootstrap, reference/reference, generated/generated, and label-permutation nulls. Disable sample-level internal early stopping.
3. Generate repeated reference and model showers at fixed conditions and quantify sampling variation separately from training-seed variation.
4. Run three training seeds for every frozen final condition.
5. Run the oracle-versus-ancestral cascade for response, first layer, activity, profile, count, support, and share stages.
6. Audit the S2 state dict, optimizer membership, visibility logits/BCE, and every weighted loss contribution before assigning a causal interpretation.
7. Record response-cap activation, positive-branch zero mass, CLR clipping frequency and moved energy, and all numerical rejection counts.
8. Evaluate angle dependence, energy-angle maps, tails, and the complete stage distributions rather than means alone.
9. Repeat topology observables across stored-energy thresholds, with occupancy normalization and an independent physical-neighbor graph.
10. Replace or formally revise centroid geometry for the 2,400 ganged HCAL channels.
11. Archive complete Geant4, geometry, field, material, cut, source, and random-seed provenance.
12. Compare matched simple and published baselines, add reconstruction observables, and measure end-to-end timing including transfers and decoding.

## Current claim boundary

The paper can support the statement that enforced sparse structure and budget closure did not ensure agreement with the conditional reference distribution in this checkpoint lineage. It cannot support claims of final physics fidelity, conditional correctness, architecture superiority, reconstruction equivalence, or acceleration.
