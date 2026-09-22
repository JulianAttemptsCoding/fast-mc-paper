# Scientific status

Version 0.7.0 is an exploratory HEP/computational-physics case study: **for one pilot Zero-Degree Calorimeter checkpoint, similar mean occupancies coexist with a later longitudinal reach and a more disconnected strict-positive support on the model graph.**

The manuscript now explains the implemented generator from input to output: five condition features feed a residual condition encoder; response, longitudinal profile, count, support, and share stages are sampled in sequence; graph message passing and layer attention score channels; and a deterministic softmax decoder closes each layer to its sampled budget. These are implementation statements verified against source blobs, not claims that the architecture is physically adequate or responsible for the measured discrepancy.

## Supported claim

On the recorded 10,000-condition development bank, the generated sample has 0.25 more active layers but reaches 4.42 layers farther downstream, leaving 3.95 more inactive layers inside the occupied span. It has 28.7 fewer active channels but 35.97 more weak graph components and a 6.03-percentage-point lower largest-component fraction. Mean total deposit differs by 0.045 GeV, with opposing ECAL and HCAL shifts. These are descriptive aggregate differences restricted to the selected dicos-f-02 epoch 90 checkpoint trained on 26,624 pilot events.

The batch-relative evaluator reports numerical validity. Its maximum layer residual exceeds the earlier absolute-only tolerance. The revision describes both policies without changing either. Raw-mode dust is a trivial zero-threshold counter. Aggregate records cannot independently reconstruct per-batch checks.

## Corrected provenance

The earlier v0.3.0 draft incorrectly attributed a later model's 551,234-event training role to this pilot checkpoint, misstated canonical split counts, described two later continuations rather than one accepted continuation, and presented a batch-wide closure tolerance as eventwise. Those statements and the previous QA assurances are superseded. Source evidence is bound to the checkpoint's exact configuration hash in `data/provenance/source_evidence.json`.

## Limits of this draft

The bank was repeatedly inspected, its overlap with pilot validation is unresolved, the checkpoint has one training seed, and event arrays are not available for uncertainty estimates, structural distributions, threshold scans, or graph sensitivity tests. The support definition uses energy greater than zero, the readout graph collapses ganged positions, and the graph is shared with the model. The manuscript makes no statistical-significance, post-digitization, physics-fidelity, speed, causal-mechanism, or architecture-superiority claim. Historical shower-aware classifier results remain excluded; condition-only AUROC 0.500 is not evidence of shower fidelity or complete leakage control.

## Work needed for broader claims

A locked bank with exact identities; at least three independent final training seeds; repeated fixed-condition Geant4 and model showers; valid paired/grouped multivariate tests; cap, clipping, solver and threshold diagnostics; an independent physical-neighbor graph; oracle-cascade and matched baseline comparisons; full-training-sample controls; reconstruction and memorization studies; end-to-end timing; and complete production physics provenance.

Before submission, the author must verify authorship/acknowledgments, collaboration data permissions and the immutable release. These are publication decisions; manuscript QA cannot establish them. The user's intended future Stony Brook/New Haven EIC ZDC context is noted as motivation only and is not used to assert detector identity, affiliation or readiness.
