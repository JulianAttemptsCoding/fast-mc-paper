# Adversarial-audit disposition

The two supplied reviews were treated as scientific review, not as instructions to manufacture missing evidence. Their central assessment is accepted: the retained aggregates support an exploratory case study of one checkpoint, not a general validation result or a causal diagnosis.

## Implemented

- Renamed the paper around **connectivity diagnostics** and removed “topology-sensitive,” “constraint-preserving,” and “validation” from the title.
- Recast the manuscript as a repeatedly inspected development-set case study.
- Replaced the gap and component ratios with absolute differences and foregrounded the $+4.42$-layer shift in mean last active layer.
- Removed the uncertainty-free energy-bin figure, the mixed-unit ratio figure, the training-history figure, the pooled Wasserstein discussion, the reference-half comparison, the four-channel toy example, and the forensic appendix.
- Added the 49-event zero-deposit difference without an unsupported significance calculation.
- Fixed the activity factorization to use $\ell>F$ and stated that the two energy features are deterministically redundant.
- Explained all 107,920 directed edges from the actual construction: 54,320 lateral plus 53,600 bidirectional longitudinal edges.
- Reduced the decoder QA to one paragraph and replaced six-decimal loss-weight narration with the scientifically relevant clipping outcome.
- Added pre-November-2025 primary literature on HEP generative-model metrics, ALICE ZDC surrogates, and thresholded calorimeter connectivity.
- Consolidated the evidence boundary instead of repeating claim disclaimers throughout the paper.

## Not recoverable from the released evidence

The package contains aggregates, not the generated and Geant4 event arrays or an executable checkpoint. It cannot supply paired uncertainties, threshold scans, energy-weighted components, alternative graphs, energy/angle-resolved distributions, matched event displays, cap-activation counts, solver-step scans, neighboring-checkpoint scans, oracle substitutions, new sampling seeds, independent training seeds, data-scaling runs, a locked evaluation bank, a valid shower-aware classifier, reconstruction studies, or end-to-end timing. The manuscript now states these as requirements for broader claims rather than presenting their absence as a minor caveat.

The released metadata also does not contain the complete Geant4 version, physics list, cuts, material and field configuration, production seeds, or the generator-versus-entry status of the four-vector. Those facts must come from the simulation owner before a physics-performance release.

## Criticisms not supported as stated

- **Edge count:** 106,680 follows a different neighbor-counting rule. The implementation selects four nodes in layer $\ell+1$ for every node in layer $\ell$ and stores every selected pair in both directions. The frozen count 107,920 is exactly reproduced.
- **Zero-count significance:** the quoted Poisson estimate ignores the paired design. The joint zero/nonzero table is absent, so no paired significance is reported.
- **Cap activation from the tolerance:** the largest batch-relative tolerance bounds the largest $|T|$ encountered in at least one batch. It does not identify which events hit the energy-dependent cap or how often. Activation and reference-exceedance counts remain unavailable.
- **Energy carried by extra components:** active-channel counts and largest-component fractions do not determine component energies. The manuscript does not call the extra components physically important without a threshold or energy-weighted analysis.

## Resulting claim

On the specified development bank, the generated sample from one pilot checkpoint has similar mean active-layer and active-channel counts but a later longitudinal reach and a more disconnected strict-positive support on the model graph. This is a reproducible aggregate discrepancy in that artifact. Statistical significance, post-digitization relevance, persistence across fits, and causal origin are unestablished.
