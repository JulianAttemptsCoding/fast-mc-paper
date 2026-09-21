# Consolidated response to reviews 7--9

This document records the disposition of every class of finding in `reviews/review7.txt`, `reviews/review8.txt`, and `reviews/review9.txt`. The reviews are preserved verbatim. Repeated comments are grouped by scientific issue so that the response remains auditable.

## Central revision

The manuscript is now a diagnostic case study of one accepted checkpoint. Its central result is that deterministic decoder constraints and close marginal counts do not ensure correct longitudinal and graph dependence. Claims about final conditional fidelity, speed, production readiness, and architecture superiority were removed.

## Findings resolved in the manuscript

### Checkpoint and training lineage

- Replaced the incomplete epoch-12 snapshot with `dicos-f-02` epoch 90.
- Epoch 90 is the minimum teacher-forced validation objective in the recorded lineage from absolute epochs 11--114.
- The training-history figure shows later continuation attempts and makes clear that they did not improve the selection quantity.
- The single training seed and lack of deterministic replay remain explicit limitations.

### Data, roles, and arithmetic

- Reports exact split counts: 612,482 training, 76,160 validation, and 76,298 nominal test events.
- Corrected the rounded percentages to 80.069%, 9.956%, and 9.974%.
- Explains the 551,234 generator role and both unused 30,624-event critic roles.
- Uses only the 10,000-event validation development bank and reports zero nominal-test events.
- Retires the nominal test partition from any pristine-test claim because earlier project work inspected it.

### Conditional target and production boundary

- Restores the mathematical target and makes the unknown generator-level versus detector-entry state explicit.
- Treats upstream simulation configuration as part of the operational target.
- States that detector material, field, production cuts, software, and random-seed provenance are incomplete.
- Makes no portability claim beyond the fixed production configuration.

### Response sampler and support atoms

- Documents the zero, continuous positive, and upper-cap support components.
- Gives the exact cap function and its transition near 97.18 GeV.
- States that cap activations and reference exceedances were not logged, so the upper support remains unresolved.
- Calls the positive-branch objective a latent-branch surrogate rather than the likelihood of the final projected sampler.

### Activity, profile, count, support, and share laws

- Gives the independent-Bernoulli activity factorization and identifies its inability to represent residual adjacency directly.
- Clarifies CLR clipping, the additive gauge removed by terminal softmax, and the missing clipping audit.
- Describes eight explicit Euler updates evaluated at interval midpoints without calling them a midpoint integrator.
- Defines count feasibility masks, exact top-k semantics, Gumbel temperature, support BCE weighting, ranking-pair sampling, dense masked share representation, and the `K=1` case.
- Restores the decoder equation and scopes numerical closure to generated budgets.

### Composite objective

- Replaces ambiguous “joint likelihood” language with “weighted teacher-forced objective.”
- Lists all nine weights and their train-only gradient-norm calibration.
- Defines the loss families, masking, inactive-count weight, support positive-weight clipping, and rank reduction.
- Explains the target-only Jacobian correction and why it does not alter the selected checkpoint.

### Geometry and graph semantics

- Corrects the ganging arithmetic: 4,390 single-position IDs across the full detector equal 400 ECAL plus 3,990 HCAL; 2,400 HCAL IDs are ganged.
- Names ECAL layer 0 and representative HCAL layer 1 in the geometry figure.
- States that ganged positions are collapsed to unweighted centroids.
- Gives the directed-edge construction and edge count.
- States that the model graph and topology graph are the same, so the topology result is representation-specific rather than independent validation.

### Metrics, denominators, and figures

- Defines moment-difference formulas and removes “resolution” terminology.
- Adds energy-bin counts and explicitly states that no uncertainty bars are plotted.
- Conditions activity and topology means on nonempty events, defines an interior gap as a maximal run, and defines largest-component fraction.
- Separates ECAL and HCAL contributions, exposing the cancellation behind the close total mean.
- Replaces redundant and overloaded figures with six focused figures: geometry, sampler, training history, energy-bin moments, longitudinal allocation, and structural ratios.
- Reports invariant batch count, tolerance formula, maxima, and every zero-valued failure counter.

### Classifier evidence

- Removes every shower-aware C2ST value from the manuscript because the existing split and feature construction are invalid for the intended conditional claim.
- Retains only the condition-only AUROC 0.500 as a pipeline sanity control and says explicitly that it contains no shower information.

### Authorship, availability, and disclosure

- Julian Juan is the sole named author and has a contribution statement.
- Dr. Wen-Chen Chang of the Institute of Physics, Academia Sinica is acknowledged as mentor.
- The data statement includes the repository URL and checkpoint/config hashes.
- The collaboration-owned raw data and checkpoint are identified as unavailable in the public repository.
- A generative-AI use statement is included.

## Findings resolved by removal

- Removed the B0 versus V3-SUP comparison because it was descriptive rather than a controlled ablation.
- Removed the M0/S2 screen and every causal lesson drawn from it because its bank relationship and implementation state were undercontrolled.
- Removed the half-trained epoch-12 checkpoint from the scientific narrative.
- Removed the historical shower-only classifier outputs.
- Removed figures that mixed bank roles, implied unsupported error bars, or duplicated the main table.

## Findings retained as explicit limitations

- one generator-training seed;
- one reference and one generated event per condition;
- repeated adaptive inspection of the development bank;
- no pristine test result;
- no cap-activation or CLR-clipping counters;
- no solver-step convergence study;
- no component-wise oracle cascade;
- no angular or energy-angle validation;
- no threshold-stability study for topology;
- no independent physical-neighbor graph;
- no detector-material or full Geant4 provenance;
- no matched simple or published baseline;
- no reconstruction study;
- no end-to-end timing measurement.

These omissions prevent a physics-fidelity or production claim. They do not invalidate the narrower descriptive finding for the fixed checkpoint and bank.

## Literature comparison

The related-work section and `audit/literature_benchmark.md` compare the paper's evidence standard with CaloChallenge, CaloGraph, CaloDREAM, CaloClouds II/3, ParaFlow, a full-physics benchmark, and recent ZDC flow matching. Cross-paper numerical rankings are deliberately omitted because detector and evaluation protocols differ.

## QA response

The release uses `scripts/full_manuscript_qa.py` for 20 complete sequential passes. Every pass rebuilds all figures and the PDF; checks evidence identities, split arithmetic, headline values, citations, labels, excluded language, and figure hashes; rasterizes every PDF page; and checks every page for blank content, edge clipping, and text extraction. JSON and Markdown records are stored in `audit/iterations/`.
