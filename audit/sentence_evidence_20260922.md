# Sentence-level evidence and clarity review

Revised: 2026-09-23; manuscript v0.11.1.

Every prose paragraph, equation, table caption, and figure caption was reviewed for purpose and evidence. The reader pass retained model equations with a distinct explanatory role, defined symbols near use, and removed the unnecessary displayed Gumbel inverse transform. The scientific result is unchanged.

| Section | Review basis | Evidence |
|---|---|---|
| Abstract | Checkpoint, population, observables, failed classifier gate, and limits are stated at their supported scope. | Aggregate report; provenance; claim register. |
| Introduction | Detector-simulation motivation and prior work use primary citations; different detector representations are not numerically equated. | References; literature benchmark. |
| Simulation target | Condition features, readout target, geometry, graph, and split roles are source bound. | Source evidence; geometry summary. |
| Generator and training | Provisional and final visibility, centered log targets, masked flow loss, current-state eight-step updates, graph aggregation, perturbed top-k, deterministic closure, and nine loss terms match source at the recorded commit. The reader-facing notation identifies readout quantities, masks, context, graph functions, ranks, and loss terms near use. | Mathematical-exposition and model-exposition audits; training history. |
| Diagnostics and results | Equations define observables, and reported numbers come from the immutable aggregate report. The classifier split and development-bank limits are explicit. | Report; claim register; evaluator review. |
| Discussion and conclusion | Structural observations are separated from untested mechanisms; graph and zero-threshold dependence remain visible. | Claim register; model audit. |
| Declarations | Repository contents and author declarations are represented without implying collaboration approval. | README; STATUS; author declaration. |

The paper does not equate energy-budget closure with conservation of incident neutron energy or Geant4 fidelity. The flow equations describe the implemented objective and numerical update, not an exact likelihood or solver-convergence result. The mathematical audit records source hashes and per-equation bindings.

Typeset QA and visual review of the exact final PDF are recorded separately in the latest iteration and visual-review records.
