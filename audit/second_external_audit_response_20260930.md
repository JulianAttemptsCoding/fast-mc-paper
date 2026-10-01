# Response to the second external audit

Current revision: v0.18.0. Intended venue: arXiv, as specified by the author. This is an aggregate-only diagnostic note, not a validated detector simulator or certification of journal readiness. The supplied audit is preserved in `audit/source_snapshots/second_external_audit_20260930/supplied_audit.txt`. Original source, PDF and source ZIP are preserved beside it.

## S1.1 — Threshold and timing sensitivity

Accepted the missing context. The [cited detector study](https://arxiv.org/html/2406.12877v2) explicitly defines a 0.5 MeV MIP scale, retains reconstructed hits above 0.5 MIP and before 275 ns, and describes digitization. The manuscript now cites these as concrete motivation for a 0.25 MeV HCAL sensitivity scan. They are not established operating cuts for this production: segmentation, digitization and timing conventions remain unverified. Applying a timing cut only to reference showers would change the compared targets; the generator produces time-integrated deposits and no hit times.

Small fragment energies are plausible, not demonstrated by the mean longitudinal curves. The suggested fragment sizes multiply means of correlated quantities: the mean number outside the largest component is E[N(1-f)], not generally E[N](1-E[f]). Neither the energy fraction outside that component nor the energy in newly occupied late layers is identifiable from the released means. No artificial spectrum or threshold result was added. The frozen raw target is unchanged.

## S1.2 — Stored ID grouping versus electronic ganging

Accepted the terminology correction. The scanner groups by the stored readout key and averages distinct stable positions. Its historical `ganged_channel_count` field is a label, not evidence of electronics. Figure 1 and its caption now describe stored-ID centroids and position multiplicity. The text defines a model channel as a stored ID grouping and explicitly states that electronic ganging is unverified.

The HCAL position arithmetic is 3,990 + 2(1,950) + 3(444) + 4(6) = 9,246, or 1.44695 positions per HCAL ID. Agreement with a nominal tile-area count supports an aliasing hypothesis but does not identify the production segmentation. No production compact XML or exact epoch-90 file was found by the current scoped local search. The author was asked for locations. No frozen geometry was modified or guard relaxed. Physical electronics/neighbor interpretations remain unresolved; stored-ID graph arithmetic remains reproducible and has no demonstrated integrity failure. The [staggered-tessellation paper](https://arxiv.org/abs/2308.06939) is now cited for the spatial information at issue.

## S1.3 — Exact runs versus aggregate bound

Accepted. The data section now explicitly states what is available to this reanalysis: aggregate reports and static geometry; matching event arrays and checkpoint were not recovered locally. The protocol explains that R and Q are exactly computable from event masks, which the aggregate report does not preserve. The bound is useful under this evidence constraint and is not presented as a superior replacement for an exact measurement. Exact runs, lateral-only components and jointly nonempty-pair metrics remain event-level follow-up work. This local access statement does not assert that the events or checkpoint have ceased to exist elsewhere.

## S1.4 — Single fit and failed screening

Accepted the abstract omission: it now states that the checkpoint fails the recorded classifier screen. It already states the 26,624-event training size, one seed and reused validation sample. The limitations now explicitly request three seeds and a full-data fit to separate architecture from training-population and optimization effects. Calling the fit undertrained as an established cause would require the missing comparisons. The separate-bank grouped AUROC cannot replace the original sample's evaluation or quantify its row-split bias.

## S2 — Mechanism and calibration

The activity null, temperature sweep, oracle activity/count swaps and cross-layer centroid correlation tests are sensible follow-ups. Matching two longitudinal mean shifts with a stratified independence null would establish that the null can reproduce those shifts; it would not uniquely prove the trained generator's causal failure mechanism. Stratum sparsity and conditioning sufficiency also require checks.

The categorical claim that a shower axis cannot wander coherently without a common event latent is too strong. The model has shared random upstream states, a joint layer-budget flow, and cross-layer attention. These can induce correlated scores and energy-weighted centroids despite conditionally independent Gumbel perturbations. The manuscript now states that distinction and proposes centroid-correlation measurements.

Raw-total similarity is now explicitly called raw-deposit similarity in the introduction. The design study's 2.1% electron sampling fraction would give about -5.5% using the rounded section means (the exact value depends on rounding), but that is a hypothetical weighting, not this production's reconstructed response. A cap does not establish shower composition. Nor does one weighting establish a -6% bias for every physical weighting: the section differences have opposite signs. No externally borrowed calibration or interaction-length conversion is reported as a measured result.

## S2 — Statistics recovered from the existing report

Table 3 now includes both per-bin population standard deviations. The archived evaluator uses NumPy's default population standard deviation. Pooling within- and between-bin second moments gives reference 4.759443 GeV and generator 4.830263 GeV. The reference value is independently corroborated by the stored normalized Wasserstein metric. These describe variation in this sample; they do not provide the missing covariance for a paired mean-difference interval. The speculative 0.06 GeV independent-sample estimate is not substituted for that interval.

Removed the repeated ±7.7% sentence. The complete table remains, with wording that neither energy-dependent bias nor reference sampling noise is established. The zigzag is not diagnostic of either explanation by itself. Conditional ECAL-start fractions, requested by the audit and already stored, are now reported: 93.81% reference and 92.53% generated among separately nonempty showers.

The report contains fields named `zero_from_visibility_hurdle` and `zero_from_positive_branch`, but their names are insufficient to answer the proposed clamp test. The available response sampler returns the final V after the positive-total requirement; the evaluator decomposition uses the supplied visibility flag. It does not preserve provisional V0. All 142 zeros being labeled invisible therefore does not show that none arose from clamping. The manuscript now states that the decomposition cannot be recovered reliably. The loss-weight ceiling alone does not prove the opposite claim either.

## S2 — Data hygiene and physical observables

The proposed overlap expectation is about 874 only under uniform independent sampling; it is not a recovered overlap count, and energy restriction may affect the relevant population. No test data were opened. A locked test subset requires exact identities and a frozen analysis, not merely the uninspected-event count. A new test result would be a separate result and would not make the existing validation result cease to be repeatedly inspected.

The appendix now states both perspectives on classifier pair leakage: 42% of pairs straddle partitions in expectation, while 70% of scored rows have their twin in the fitting partition (about 4,200 rows). Because this evaluator stratifies by class, the latter is 7,000/10,000 = 0.7; 14,000/19,999 is the corresponding unstratified approximation. Library-internal early-stopping reservation can further change which fitting rows train trees. The failed historical scores remain disclosed; no same-bank grouped rerun was invented.

Generation latency, energy/angle reconstruction, radial and centroid distributions, physical-neighbor sensitivity and thresholded observables remain absent. The 0.344 s number is labeled evaluator time. A 0.55 interaction-length conversion and global-frame assignment require verified production materials and coordinates. Consistency with nominal dimensions/crossing angle alone is not verification.

## S3 — Methods and numerical specification

The two energy features are redundant; the manuscript now says both belong to the analyzed checkpoint, and removing one changes the model. No post hoc architectural alteration was made. Centering fixes the softmax common-offset freedom. The target has zero sum, while base noise has a common-offset mode; no likelihood on that singular plane is evaluated. The share floor modifies small shares; its occurrence rate is unavailable.

The numerical section now explicitly interprets the zero support-mask mismatch: selected channels equal positive FP32 deposits in the evaluated sample. This is evidence from the report, not a universal underflow guarantee. The stricter historical absolute-tolerance failure stays visible; dropping it would conceal negative evidence contrary to the project's operating contract. No claim is made that the historical relative criterion was chosen in advance.

Solver-step, graph, temperature, loss-weight and batch-size studies were not performed. No undocumented memory constraint is invented to justify effective batch size 24. Conditional neighbor occupancy is related to but not identical to Jaccard co-activation: P(B|A)=P(A∩B)/P(A), whereas J(A,B)=P(A∩B)/P(A∪B). Aggregate edge co-occupancy alone lacks the required per-edge marginals. No invented normalized value was added.

## S4 — Presentation, affiliation and references

Abstract bound wording now says that the difference in run counts is bounded, avoiding an implication that exact runs were subtracted. Absolute component means 23.42 and 59.39 are given directly (their ratio is approximately 2.54); the ratio is not promoted over the absolute effect. The discussion says the activity factorization assumes conditional independence. Equation punctuation is grammatical; the numbered equations are unchanged. Repeated availability/discussion prose was trimmed while necessary provenance and failed QA remained. The existing name/email-only author line respects the author's explicit removal of the affiliation label. Academia Sinica mentorship stays acknowledged. The author already confirmed data-owner permission; no further institutional policy is asserted or permission invented.

Updated the detector reference to its published NIM A article and verified DOI; added CaloChallenge and flow-matching ZDC arXiv IDs; added the [ExpertSim proceedings DOI](https://journals.sagepub.com/doi/10.3233/FAIA251042). Added staggered tessellation, [rectified flow](https://arxiv.org/abs/2209.03003) for the actual straight interpolation, and [CaloPointFlow II](https://arxiv.org/html/2403.15782v2) for count-conditioned point generation. Stochastic interpolants was checked but is not required in addition to the directly matching flow references. DD4hep is not claimed as this production's verified runtime, so its citation was not added merely to imply provenance. The detector paper's Geant4/physics-list settings are not assigned to this sample.

## Completion boundary

This revision addresses all findings that can be resolved through the existing aggregate evidence, mathematical checks, source review and primary literature. Exact event-level results, production ID semantics, training replication and detector-performance validation remain research tasks. Repeated document QA cannot remove those limitations. No external submission was performed.

Final document verification: QA98 passed 18 groups at 14 pages; all 14 pages visually reviewed; seven release-guard tests passed; exact seven-file source archive verified.

Final release binding uses QA99 after a README-only historical clarification. All 18 groups pass and all 14 rendered pages are byte-identical to those visually reviewed for QA98.
