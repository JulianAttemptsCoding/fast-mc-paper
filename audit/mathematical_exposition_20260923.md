# Mathematical exposition audit, 2026-09-23

The v0.11.1 model equations were checked against the recorded source commit and checkpoint configuration hash. The JSON twin binds each equation label to source-file SHA-256 digests obtained with git show. The prior model-exposition hashes agree for every overlapping file.

| Equation | Implementation basis |
|---|---|
| eq:response_transform | src/cbsc_zdc/models/response.py |
| eq:cap | src/cbsc_zdc/models/response.py |
| eq:activity | src/cbsc_zdc/models/profile.py |
| eq:profile_target | src/cbsc_zdc/training/truth.py |
| eq:cfm | src/cbsc_zdc/training/flow_matching.py, src/cbsc_zdc/training/trainer.py |
| eq:flow_steps | src/cbsc_zdc/models/profile.py, src/cbsc_zdc/models/system.py |
| eq:layer_budget | src/cbsc_zdc/models/profile.py |
| eq:message | src/cbsc_zdc/models/graph.py, src/cbsc_zdc/models/node_fields.py |
| eq:topk | src/cbsc_zdc/models/support.py |
| eq:share_target | src/cbsc_zdc/training/truth.py |
| eq:decoder | src/cbsc_zdc/models/support.py |
| eq:joint_loss | src/cbsc_zdc/training/trainer.py, src/cbsc_zdc/training/losses.py, src/cbsc_zdc/training/weights.py, src/cbsc_zdc/models/response.py |

The response equation distinguishes provisional from final visibility. The training targets include the actual fraction and denominator floors. The flow equation uses a mask-normalized minibatch MSE, and the update is evaluated at the current state and midpoint time. Graph messages sum incoming directed edges; perturbed top-k fixes cardinality without imposing connectivity. The loss is the weighted sum of nine terms.

The v0.11.1 reader pass kept each displayed model equation only where it identifies a distinct sampling operation, training target, architectural dependence, or exact output constraint. The JSON twin records that purpose for every equation. The Gumbel inverse-transform formula was removed from the displayed mathematics: the support equation now identifies the selected channel indices, while the numerical clipping convention remains in prose. Nearby text defines the readout quantities, reference symbols, flow state and mask, graph functions, rank convention, and loss abbreviations. No extra model operation or physics result was introduced.

These equations specify the implemented computation and its constraints. They do not prove Geant4 fidelity, solver convergence, a causal mechanism for the observed gaps, or exact identity between the inspected source commit and training-time source bytes.
