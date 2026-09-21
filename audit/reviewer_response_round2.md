# Round-two audit disposition

This record covers every issue in `review_4_conditional_method_audit.txt`, `review_5_hard_reproducibility_audit.txt`, and `review_6_hostile_second_pass.txt`. Repeated issues are grouped by scientific dependency. “Deferred” means the requested result cannot be reconstructed from the released aggregates; the manuscript states the gap instead of inventing a result.

## Source corrections found during the audit

- **Training population:** the earlier manuscript incorrectly assigned the 26,624-event pilot size to V3-SUP. The frozen role partition and handoff logs show that V3-SUP used all 551,234 `generator_train` events. The 26,624-event sample applies to B0 and the short M0/S1/S2/S3 screens.
- **Model identity:** V3-SUP is epoch 12 of a planned 24, initialized from the pilot/composite lineage. Its frozen `cbsc-zdc-v3` configuration enables no optional v3 feature blocks and retains v2.2 behavior.
- **Parameter count:** 2,082,507 trainable parameters, reconstructed from the pinned public source and frozen geometry.
- **Evaluation sets:** the 10,000-event battery and 4,096-event loss screen are distinct uses. Their overlap is not proven in the released evidence.
- **Model graph:** 107,920 directed edges are built from eight same-layer centroid neighbors and four adjacent-layer centroid neighbors with reverse longitudinal edges.

## Disposition by issue family

| Issue family | Disposition in v0.2.0 |
|---|---|
| Page-one governance language | Replaced “validation-only” with “development-bank evidence”; nominal test set is retired. |
| Conditional C2ST | Removed every historical shower-only AUROC and the old figure from claims. The manuscript specifies the required joint `(c_raw, Y)` grouped evaluator and nulls. The old plot is archived as excluded evidence. |
| Pair leakage and evaluator internals | Requires grouped matched pairs, condition bootstrap, and no sample-level classifier-internal validation. Deferred because event-level arrays are absent from this paper repository. |
| Condition-only AUROC 0.500 | Retained only as a tautological pipeline sanity check; explicitly denied evidentiary value for shower fidelity. |
| Bernoulli hurdle versus realized visibility | Introduced distinct variables `B` and `V`; wrote the implemented zero-mass decomposition. |
| Positive-branch support mismatch | Described the unconstrained Gaussian negative tail and clamp-created zero atom as a model limitation. Positive-branch zero counts are reported as zero on the available battery, without claiming the defect is absent. |
| Safety cap | Reported the exact ratio and absolute cap, deterministic clipping rule, lack of rejection/resampling, and missing cap-activation counter. |
| Runtime “quarantine” | Removed ambiguous terminology. A failed invariant excludes the entire artifact; individual events are not dropped or resampled. Recorded plotted-artifact failure counts are zero. |
| Full objective | Added the nine-term equation and all frozen weights. Defined BCE, categorical CE, common-measure GMM NLL, ranking, and masked CFM terms. |
| S2 component autopsy | Compared S2 with M0 and reported the zero-cause decomposition. Causal diagnosis is withheld because per-component loss trajectories, state-dict checks, and visibility-logit audits are unavailable. |
| Teacher forcing and exposure mismatch | Elevated teacher forcing into the model description and interpretation. The oracle-versus-ancestral cascade is a required experiment. |
| CLR gauge | States that the source is independent Gaussian while the target is zero-sum, that softmax removes the gauge for sampling, and that no full-dimensional density claim is made. Centering the source remains required work. |
| CLR clipping | Reports the `1e-8` floor and the absence of clipping-frequency and moved-energy counters. No exact-invertibility claim is made. |
| Activity model | Defines independent Bernoulli activity conditioned on condition, total deposit, and first layer; links this assumption cautiously to the gap discrepancy without causal attribution. |
| Count head | Defines the categorical head, per-layer physical masks, inactive-zero weighting, and exact realized count semantics. |
| Support loss and Gumbel sampler | Defines balanced BCE, the 256-pair ranking loss, exact-size Gumbel-top-k sampling, and the mismatch between surrogate scores and sampler likelihood. Conditional calibration is listed as missing. |
| Fragmentation mechanism | Reports stage-level occupancy and weak-component discrepancies. Does not claim that support sampling alone caused them. |
| Directed connectivity | Defines the published metric as weak connectivity obtained by unioning directed-edge endpoints. Strong connectivity is not claimed. |
| Zero-event topology conventions | Defines inclusion or exclusion for active counts, gaps, components, and largest-component fraction. |
| Threshold dependence | States that activity is strict stored energy `>0` and that no threshold sweep exists. Physics interpretation is limited accordingly. |
| Ganged geometry | Quantifies 2,400/6,390 HCAL channels (37.56%) and the 1/2/3/4-position multiplicity distribution. Explains that centroiding affects the model and metrics. |
| Geometry figure and edge construction | Added a detector/readout figure, layer cardinalities, edge construction, and the centroid contract. |
| Fixed vertex and upstream transport | Reframed the target as generator-level conditioning under an incompletely documented fixed simulation setup. No entry-state claim is made. |
| Encoder singularity and redundancy | Reports the audited positive minimum kinetic energy and states that exact zero inputs are outside the verified domain. Describes the five inputs as a deterministic embedding rather than independent variables. |
| Angular conditioning | Explicitly says angular fidelity is unvalidated and requires angle-stratified metrics. |
| 0--300 versus 50--250 GeV | States that training covers 0--300 GeV and every paper diagnostic covers the 50--250 GeV claim domain. |
| Development-set overlap | Names `D_bat` and `D_loss` separately and states that overlap is unknown. No statistics are combined across them. |
| Response-bin definitions | Defines eight 25 GeV bins, unconditional inclusion of zero events, and standard deviations as distribution widths rather than uncertainty bars. |
| Wasserstein interpretation | Defines empirical one-dimensional W1 and labels it exploratory; no significance or uncertainty interpretation is assigned. |
| Longitudinal profile | Added a dedicated ECAL panel and discussed the 11.1% ECAL mean excess together with lower ECAL-start prevalence. |
| First-layer, activity, occupancy, sparsity | Added a stage table with zero rate, ECAL start, mean first layer, gaps, active layers, active channels, active fraction, components, and largest-component fraction. |
| Distribution-versus-mean limitation | States that plotted topology bars are means and that event-level distributions and occupancy-normalized components are unavailable from the aggregates. |
| One shower per condition | States the design exactly and rejects fixed-condition spread claims. Repeated draws are required work. |
| Training and sampling uncertainty | States that one generator training seed and one draw per condition cannot establish robustness. Requires three training seeds and repeated sampling. |
| Architecture reproducibility | Added parameter count, exact head widths, embeddings, graph/context depth, flow solver, optimizer, batching, precision, seed, stopping, cap, closure tolerances, frozen config, and source commit. |
| Internal project jargon | B0, M0, V3-SUP, and S2 are defined by role on first use and limited to comparisons where their provenance is needed. S1/S3 and arbitrary promotion gates were removed. |
| Scalar-loss tables and 0.0013 reference | Removed the old summary table and the undefined run-to-run reference. Retained only the matched M0/S2 comparison with its base measure. |
| Dimensional logarithm | Rewrote the Jacobian with `t=T/(1 GeV)` and dimensionless scale `s=10`. |
| “Truth,” “hit,” and “detector simulator” terminology | Uses “Geant4 reference,” “active channel,” and “raw deposited-energy surrogate.” Internal JSON field names are not presented as scientific terminology. |
| Sparse-computation implication | States that sparsity refers to output support; no sparse-compute or speed advantage is claimed. |
| Related work | Added CaloDREAM and CaloClouds; upgraded CaloGraph to its published PRD citation. The directly relevant ZDC flow-matching paper remains cited without treating it as a matched baseline. |
| Figures | Removed the C2ST figure and arbitrary 0.65 line, enlarged response/topology plots, changed the zero plot to one logarithmic axis, added M0 to the zero comparison, and added the geometry figure. |
| Manuscript voice | Removed reviewer-response language, the title-defense sentence, submission TODOs, and unsupported novelty phrasing. |
| Acknowledgments | Thanks only Dr. Wen-Chen Chang for mentorship and guidance; no authorship or endorsement is implied. |
| Versioning | Manuscript and repository identify release v0.2.0 and the exact public implementation commit. |

## Deferred experiments

The following requests require event-level samples, checkpoints, new Geant4 production, or new training and are therefore not fabricated in this revision: corrected condition-aware C2ST; evaluator null distributions; angular maps; cap and CLR clipping counters; S2 state/optimizer/component-loss autopsy; oracle cascade; threshold sweep; occupancy-normalized component distributions; independent physical adjacency; repeated fixed-condition reference showers; repeated model draws; multiple training seeds; training-scale curve; matched baselines; reconstruction observables; and end-to-end timing.

These items are also tracked in `STATUS.md` and are stated as limitations in the manuscript.
