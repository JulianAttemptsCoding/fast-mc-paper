# Model-exposition source audit

Created: 2026-09-22T17:37:58Z

The model description in manuscript v0.7.0 was checked against commit `e039841404fc442c7496383d20a8566ac589eea3` of the source repository and the selected frozen-configuration hash `116bc8c220b07ce54ae07196bdd6ed8e835775c8c937182a209a799dc94ae9c5`. The JSON twin records a SHA-256 digest for every inspected source blob.

## Sentence-level model claims

| ID | Manuscript statement | Direct implementation evidence |
|---|---|---|
| M01 | Five deterministic condition features are encoded by a residual MLP into 128 components. | `src/cbsc_zdc/features.py`, `src/cbsc_zdc/models/blocks.py`, `src/cbsc_zdc/models/system.py` |
| M02 | Generation uses no reference shower, learned shower encoder, or one latent variable shared by all stages. | `src/cbsc_zdc/models/system.py` |
| M03 | The response stage uses a Bernoulli visibility head and a four-component Gaussian mixture in log1p total deposit, followed by inverse transformation and caps. | `src/cbsc_zdc/models/response.py`, `src/cbsc_zdc/models/system.py` |
| M04 | The profile stage samples first layer and later activity, then maps Gaussian noise to layer-share logits and closes layer budgets to total deposit with a masked softmax. | `src/cbsc_zdc/models/profile.py`, `src/cbsc_zdc/training/flow_matching.py`, `src/cbsc_zdc/training/truth.py` |
| M05 | The count head samples a feasible categorical count per layer, with zero required for inactive layers and a positive count required for active layers. | `src/cbsc_zdc/models/counts.py` |
| M06 | Support and share fields use static geometry, three 96-component edge-message blocks, pooled layer tokens, and a two-layer four-head layer transformer. | `src/cbsc_zdc/data/geometry.py`, `src/cbsc_zdc/models/node_fields.py`, `src/cbsc_zdc/models/graph.py`, `src/cbsc_zdc/models/system.py` |
| M07 | Gumbel-perturbed top-k selection realizes exactly the sampled count but applies no connectivity constraint. | `src/cbsc_zdc/models/support.py`, `src/cbsc_zdc/models/system.py` |
| M08 | A second graph flow produces selected-channel logits; the deterministic decoder uses a within-layer softmax and closes each layer to its sampled budget. | `src/cbsc_zdc/models/node_fields.py`, `src/cbsc_zdc/models/system.py`, `src/cbsc_zdc/models/support.py` |
| M09 | The nine component losses use reference-derived upstream quantities during training, while inference passes sampled outputs downstream. | `src/cbsc_zdc/training/truth.py`, `src/cbsc_zdc/training/losses.py`, `src/cbsc_zdc/training/trainer.py`, `src/cbsc_zdc/models/system.py` |

## Boundary

This audit verifies the implemented sampling and training paths. It does not establish statistical adequacy, solver convergence, physical fidelity, speed, or causal responsibility for the observed discrepancy.
