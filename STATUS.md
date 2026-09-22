# Scientific status

Version 0.5.0 is a HEP/computational-physics preprint draft: **for one Zero Degree Calorimeter checkpoint, decoder-level numerical validity and percent-level agreement in selected inclusive response and occupancy observables coexist with substantially more fragmented longitudinal and readout-graph shower support.**

## Supported claim

On the recorded 10,000-condition development bank, mean active layers differ by +0.5% and active channels by -1.8%, while interior inactive layers and weak graph components increase by factors of 2.88 and 2.54. Mean total deposit differs by +1.0%, with opposing ECAL and HCAL biases. The detector-level conclusion is that inclusive response and occupancy agreement do not establish correct shower morphology. The computational-physics conclusion is that constraint preservation guarantees admissibility with respect to the decoder, not fidelity to the reference stochastic process. Both conclusions are restricted to the selected dicos-f-02 epoch 90 checkpoint trained on 26,624 pilot events.

The batch-relative evaluator reports numerical validity. Its maximum layer residual exceeds the earlier absolute-only tolerance. The revision describes both policies without changing either. Raw-mode dust is a trivial zero-threshold counter. Aggregate records cannot independently reconstruct per-batch checks.

## Corrected provenance

The earlier v0.3.0 draft incorrectly attributed a later model's 551,234-event training role to this pilot checkpoint, misstated canonical split counts, described two later continuations rather than one accepted continuation, and presented a batch-wide closure tolerance as eventwise. Those statements and the previous QA assurances are superseded. Source evidence is bound to the checkpoint's exact configuration hash in `data/provenance/source_evidence.json`.

## Limits of this draft

The bank was repeatedly inspected, the checkpoint has one training seed, and event arrays are not available in this package for new topology uncertainty estimates. The readout graph collapses ganged positions and is shared with the model. The manuscript makes no physics-fidelity, speed, causal-mechanism or architecture-superiority claim. Historical shower-aware classifier results remain excluded; condition-only AUROC 0.500 is not evidence of shower fidelity or complete leakage control.

## Work needed for broader claims

A locked bank with exact identities; at least three independent final training seeds; repeated fixed-condition Geant4 and model showers; valid paired/grouped multivariate tests; cap, clipping, solver and threshold diagnostics; an independent physical-neighbor graph; oracle-cascade and matched baseline comparisons; full-training-sample controls; reconstruction and memorization studies; end-to-end timing; and complete production physics provenance.

Before submission, the author must verify authorship/acknowledgments, collaboration data permissions and the immutable release. These are publication decisions; manuscript QA cannot establish them. The user's intended future Stony Brook/New Haven EIC ZDC context is noted as motivation only and is not used to assert detector identity, affiliation or readiness.
