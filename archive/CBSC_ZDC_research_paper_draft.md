# A Geometry-Aware Hierarchical Fast Monte Carlo Generator for Neutron Showers in a Zero Degree Calorimeter

**English research paper draft — 20 September 2026**  
**Authors and affiliations:** [To be supplied by the project owner]  
**Evidence cutoff:** Local project artifacts available through 29 August 2026.  
**Scientific status:** Methods and preliminary validation. Physics fidelity and end-to-end speedup have not been established.

## Abstract

Detailed Geant4 calorimeter simulation can be costly at the event counts needed for high-energy physics studies. We investigate a conditional fast Monte Carlo generator for single-neutron showers in a fixed Zero Degree Calorimeter with 65 longitudinal layers and 6,790 valid readout channels. The model conditions on incident four-momentum and generates raw deposited readout energy through a hierarchy of visible response, total response, longitudinal budgets, layer hit counts, geometry-aware support, and positive cell-energy shares. Conditional flow matching models continuous profiles and shares; one Gumbel-Top-*k* draw selects sparse channel support. The decoder guarantees nonnegative output, exact zeros outside selected support, and closure to its *generated* response total within a declared floating-point tolerance. We converted and audited 764,940 Geant4 events and froze a 612,482/76,158/76,300 train/validation/test assignment. Production-derived pilot training and later validation batteries demonstrate structural execution but reveal a persistent distributional gap: a recent supervised checkpoint had high-level classifier two-sample AUROC 0.779 on a 10,000-condition validation bank, while generated showers had interior layer gaps in 93.6% of events versus 52.4% for Geant4. Controlled v3 screening has not yet promoted a proposed architecture change. We report these negative findings alongside the method and define the remaining multi-seed, baseline, test, reconstruction, and timing studies required for a final physics claim.

**Keywords:** fast simulation; Zero Degree Calorimeter; Geant4; conditional flow matching; sparse generative models; graph neural networks

## 1. Introduction

Geant4 is a standard toolkit for detailed particle-transport simulation [1]. Its calorimeter outputs are valuable reference data, but repeated full simulation can be expensive. The CaloChallenge established that evaluating a learned calorimeter surrogate requires several views of fidelity as well as generation time [2]. A Zero Degree Calorimeter (ZDC) adds an especially sparse, layered response: shower start, longitudinal extent, channel occupancy, and energy sharing fluctuate at fixed incident conditions.

This work asks whether a conditional generator can approximate the distribution of single-neutron ZDC readout given the incident four-vector while preserving the detector's readout semantics. Our detector has 400 ECAL channels and 6,390 HCAL channels across 65 longitudinal layers. Some HCAL readouts combine several physical positions. The authoritative representation is therefore a frozen channel map and geometry graph, rather than a padded regular image.

We use a hierarchical factorization to separate discrete shower structure from continuous energy allocation. This choice gives algebraic guarantees about the *form* of generated events. Whether their distribution matches Geant4 remains an empirical question. The present manuscript reports the design, the audited data contract, and the validation evidence currently available. Related work includes ALICE ZDC flow-matching generators [3], graph-based generation for irregular calorimeters [4], and layer-wise flows [5]. Different detector representations and timing protocols prevent direct numerical comparison with those studies.

## 2. Data and scientific target

### 2.1 Condition and target

The sole raw event condition is the incident neutron four-vector

\[
p^\mu=(E_{\mathrm{tot}},p_x,p_y,p_z),\qquad
K_{\mathrm{inc}}=E_{\mathrm{tot}}-m_n,
\]

where \(E_{\mathrm{tot}}\) is relativistic *total* energy, \(K_{\mathrm{inc}}\) is incident *kinetic* energy, and \(m_n=0.93956542052\,\mathrm{GeV}\). All energy ranges below refer to \(K_{\mathrm{inc}}\). Geometry \(\mathcal G\) is fixed metadata, not an additional fluctuating event condition.

For readout channel \(i\), \(Y_i\geq0\) is the stored raw deposited energy after duplicate hits to that channel are summed. Sentinel hits are excluded. The learning target is the conditional distribution \(p(Y\mid p^\mu,\mathcal G)\) for \(Y\in\mathbb R_{\geq0}^{6790}\). The observed detector response is \(T=\sum_iY_i\). Detector response need not equal incident kinetic energy, so a decoder's energy closure must not be described as full energy containment.

### 2.2 Frozen corpus and split

The production source contains **764,940** events over 0–300 GeV incident kinetic energy, converted to 187 verified sparse shards. Its frozen geometry has 6,790 channels, 65 layers, and 107,920 graph edges. HCAL readout identity is the pair (layer ID, cell ID); a ganged readout receives the unweighted centroid of its distinct stable physical centers. The geometry hash is `e22d4cfb1e9293a33dd13151587910268ba64cd8efbcdb7a835a7442f2edcb4b`.

The canonical assignment contains **612,482 training**, **76,158 validation**, and **76,300 test** events. The optimization lineage discussed below used a 26,624-training/6,656-validation pilot bank, with zero test events. The fixed validation battery uses 10,000 conditions selected from the canonical validation split because the pilot validation bank is below its 10,000-condition minimum. The primary claim domain is 50–250 GeV, in eight fixed 25-GeV bins.

The test history must be disclosed precisely. An isolated external C2ST used 40,000 test events, and a separate 2026-07-30 visual draw contained 200 test events. Their overlap has not been resolved; between 36,100 and 36,300 test events remain unused. Those earlier uses did not inform model choices. A final test plan must identify its exact evaluation subset and prohibit test-informed tuning.

## 3. Generator and training objective

The generator derives five deterministic features from \(p^\mu\) and maps them through a condition encoder. It then samples, in order, a visible-response indicator \(V\), generated response total \(\widehat T\), first positive layer, active-layer mask, longitudinal layer shares, layer hit counts \(\widehat K_\ell\), channel support \(H_\ell\), and selected-cell energy shares. A zero-response event has zero output on every channel.

The response head uses a Bernoulli visibility hurdle and, for positive events in the original model, a conditional mixture density for response size. Conditional flow matching models longitudinal shares and selected-cell shares [6]. The support scorer combines channel geometry, graph message passing, and layer context. It samples exactly \(\widehat K_\ell\) valid channels with one Gumbel-Top-*k* draw [7]. Inactive layers have zero selected cells, while an active raw-deposit layer has at least one.

Given generated layer budget \(\widehat D_\ell\) and selected-cell logits \(r_i\), the raw-deposit decoder is

\[
\widehat Y_i=
\begin{cases}
\widehat D_\ell\dfrac{\exp(r_i)}{\sum_{j\in H_\ell}\exp(r_j)}, & i\in H_\ell,\\[5pt]
0, & i\notin H_\ell.
\end{cases}
\]

The layer budgets sum to \(\widehat T\), so \(\sum_i\widehat Y_i=\widehat T\) in real arithmetic. In implementation, every generated event is checked against the frozen floating-point tolerance. This guarantee concerns accounting of the *generated* response. It cannot ensure that \(\widehat T\), the layer profile, or the selected channels have the correct Geant4 distribution. Deposited energy is not forced to decrease from one layer to the next.

The original joint objective has nine terms: visible-response binary cross-entropy, response mixture negative log-likelihood, first-layer cross-entropy, active-layer binary cross-entropy, profile flow loss, count cross-entropy, support binary cross-entropy, support ranking loss, and share flow loss. Component diagnostics are trained in the order response → profile → count → support → share → joint. The shared condition encoder is trained at the response stage, held fixed for later isolated stages initialized from its checkpoint, and unfrozen for joint training. Loss weights and optimization decisions use training and validation evidence only.

## 4. Architecture screening and evaluation protocol

The v3 program tests changes one at a time while keeping the original decoder and structural contracts. Candidate changes include incident-axis features (S1), a bounded positive-response spline (S2), a hierarchical ECAL/HCAL first-layer head (S3), structured or autoregressive layer activity (S4), autoregressive hit counts (S5), a different profile-flow coupling (S7), and conditional critics for share or profile structure (D1/D2). Several are implemented but remain unevaluated or resource constrained. Their existence in code is not evidence of improved physics.

Each screened feature is compared with **M0-fresh**, the matched control that also restarts the optimizer. Historical v2 response-density losses require an audited \(+0.421936354321\) offset to be expressed on the common deposited-energy-GeV density measure. Comparing a v3 row with an unadjusted historical loss would mix probability-density units; comparing it directly with the older B0 checkpoint would also charge the feature for optimizer restart. The matched control has common-measure validation loss **4.935508**. Screening decisions use declared gates and retain the simpler parent when an improvement is unproved.

The validation battery compares 10,000 generated events with 10,000 Geant4 validation events, uses three evaluator seeds for C2ST, and reports bootstrap intervals and truth-half floors. It includes response, hit counts, longitudinal and spatial moments, layer activity, correlations, topology, diversity, and memorization diagnostics. Evaluator seeds measure diagnostic stability; they are **not** three independent generator-training seeds. Model selection remains based on the declared validation rule. Structural failure quarantines the affected checkpoint.

The final experiment calls for three independent training seeds for each frozen condition, an explicit 0–300 versus 50–250 GeV support comparison on the same primary-domain bank, competent empirical, non-graph, point-cloud, and external ZDC baselines, downstream reconstruction, and matched end-to-end timing. Timing must include ODE solving, support selection, decode, and serialization, and must disclose the Geant4 comparison hardware and method. No test split may inform model design, thresholds, loss weights, stopping, or checkpoint choice.

## 5. Preliminary results

### 5.1 Optimization and controlled screens

Production-derived pilot optimization produced an accepted original-model baseline **B0** at epoch 90, with historical validation loss **4.483768** and common-measure value **4.905704**. The M0-fresh control reached **4.935508** on the common measure. S1's matched value was **4.935990**, a difference of 0.000481, below the measured run-to-run reproducibility reference of 0.001259; incident-axis features were not promoted. S2 reached **4.921213**, which improves its matched control's loss, but it was not promoted because its validation battery exposed a severe zero-response regression: 50.4% generated zero-response events against 0.93% Geant4, with high-level C2ST AUROC 0.933. S3 reached **5.466342**, markedly worse than the matched control, and was not promoted. The S4 autoregressive activity row was still in progress in the latest local screening summary and has no completed battery there. These are screening outcomes, not final three-seed performance estimates.

### 5.2 A recent supervised checkpoint

A later V3-SUP checkpoint selected at epoch 12 was evaluated on the fixed 10,000-condition validation bank. Its high-level C2ST AUROC was **0.7785**, low-level C2ST **0.7768**, and profile-aware C2ST **0.8460**; the condition-only sanity control was **0.4636**. The high-level result remains above the frozen 0.65 diagnostic threshold. Generated zero-response fraction was **1.61%**, compared with **0.93%** for Geant4. The paired generated-minus-truth detector-response residual, normalized by incident kinetic energy, had mean **0.000078** and RMSE **0.0462**. This paired response statistic is not downstream reconstruction closure.

The largest visible morphology defect was shower fragmentation. The fraction of events with an interior gap between active layers was **93.56%** for generated showers and **52.43%** for Geant4. Generated events had a mean **6.25** gaps versus **2.10** for Geant4. This gap persisted while other validation observables improved between V3-SUP epochs 7 and 12, indicating that more training alone had not resolved it by the later checkpoint. The finding motivates the structured-activity screen; it does not prove the proposed replacement will work.

The V3-SUP numbers are from one selected generator checkpoint on validation data. No complete final-test result, three-seed model comparison, matched external baseline, memorization conclusion, downstream reconstruction-equivalence result, or production end-to-end speed ratio is available in the evidence reviewed for this draft. **Physics validation is not established.**

## 6. Discussion

The hierarchy enforces exact sparse output semantics, but its principal scientific risk is a gap between optimization loss and shower fidelity. A classifier can still separate generated from Geant4 events, and longitudinal activity has the wrong connected structure. The S2 response-spline experiment illustrates why improving one scalar loss is insufficient: despite a lower aggregate validation loss than M0-fresh, its zero-response distribution deteriorated sharply. The S1 experiment shows why matched optimizer state and common probability-density units matter when interpreting architecture screens.

The supplied SSP report uses a VAE, latent diffusion, and post-hoc energy correction. It is a useful brief model of paper organization and candid limitations, but its architecture and numerical findings belong to that study. In this work, total response is sampled explicitly and allocated through a sparse exact decoder. No result from the SSP report is transferred into the evidence table above.

The path to a publishable final result is empirical: complete the remaining declared screens, freeze the selected model and all diagnostics, evaluate three training seeds on the governed test subset, compare fair baselines, and report failure modes alongside any improvements. A negative result can still establish which component of the hierarchy limits fidelity and whether the geometry-aware cost is justified.

## 7. Conclusion

We describe a four-momentum-conditioned, geometry-aware Fast MC generator for raw single-neutron ZDC readout. Its decoder guarantees nonnegative sparse output and accounting closure to generated response, and production-data preparation and validation pipelines are audited. Current validation results reveal material Geant4-versus-model differences, especially classifier separability and fragmented longitudinal activity. The proposed model is therefore a tested research candidate, not yet a validated replacement for Geant4.

## References

1. S. Agostinelli *et al.*, “Geant4—a simulation toolkit,” *Nuclear Instruments and Methods in Physics Research A* **506**, 250–303 (2003). [doi:10.1016/S0168-9002(03)01368-8](https://doi.org/10.1016/S0168-9002(03)01368-8).
2. C. Krause *et al.*, “CaloChallenge 2022: A Community Challenge for Fast Calorimeter Simulation” (2024). [arXiv:2410.21611](https://arxiv.org/abs/2410.21611).
3. M. Wojnar, “Even Faster Simulations with Flow Matching: A Study of Zero Degree Calorimeter Responses” (2025). [arXiv:2507.18811](https://arxiv.org/abs/2507.18811).
4. D. Kobylianskii *et al.*, “CaloGraph: Graph-Based Diffusion Model for Fast Shower Generation in Calorimeters with Irregular Geometry” (2024). [arXiv:2402.11575](https://arxiv.org/abs/2402.11575).
5. S. Diefenbacher *et al.*, “L2LFlows: Generating High-Fidelity 3D Calorimeter Images,” *Journal of Instrumentation* **18**, P10017 (2023). [doi:10.1088/1748-0221/18/10/P10017](https://doi.org/10.1088/1748-0221/18/10/P10017).
6. Y. Lipman *et al.*, “Flow Matching for Generative Modeling,” *ICLR* (2023). [arXiv:2210.02747](https://arxiv.org/abs/2210.02747).
7. W. Kool, H. van Hoof, and M. Welling, “Stochastic Beams and Where to Find Them: The Gumbel-Top-k Trick for Sampling Sequences Without Replacement,” *Proceedings of Machine Learning Research* **97**, 3499–3508 (2019). [PMLR](https://proceedings.mlr.press/v97/kool19a.html).

## Internal provenance for manuscript revision

The scientific figures and assertions above trace to `docs/DATA_CONTRACT.md`, `docs/IMPLEMENTATION_GUIDE.md`, `docs/FOCUSED_OPERATING_RULES.md`, `docs/V3_FULL_REPORT.md`, `docs/HANDOFF.md`, `exhibition/current/v3_screening/screening_summary.json`, and `exhibition/data/v3_battery/v3-sup_epoch12.json`. The project's existing `paper/CBSC_ZDC_Auditor_Specification_v2_2.tex` is an implementation and audit specification, not this article. Refresh the manuscript from verified artifacts before submission; add author metadata, venue formatting, final figures, all training seeds, exact test-set disposition, and timing only when those results exist.
