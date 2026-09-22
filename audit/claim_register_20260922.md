# Current claim register

| ID | Claim | Evidence and boundary |
|---|---|---|
| C01 | Mean active-layer counts differ by $+0.25$, while mean last active layer differs by $+4.42$ and mean inactive layers inside the span by $+3.95$. | Recomputed from the aggregate activity fields with nonempty denominators. Descriptive for one bank. |
| C02 | Mean active-channel counts differ by $-28.7$, while weak graph components differ by $+35.97$ and largest-component fraction by $-6.03$ percentage points. | Recomputed from topology/count aggregates with nonempty denominators. Applies only to the shared model graph and energy $>0$ support. |
| C03 | Mean total deposit differs by $+0.045$ GeV; ECAL and HCAL shifts have opposite signs. | Aggregate longitudinal profile and total-response fields. No calibrated equivalence claim. |
| C04 | Energy-bin mean differences span $-7.7\%$ to $+7.7\%$. | Stored all-event bin means. No binwise uncertainty, significance, or smoothness claim. |
| C05 | There are 142 generated and 93 reference zero-deposit events. | Marginal counts only. Paired significance is unavailable. |
| C06 | The graph has 107,920 directed edges. | Frozen geometry plus exact construction arithmetic: $8(6790)+2(4)(400+63\cdot100)$. |
| C07 | Decoder counters and budget checks pass on the stored generated bank. | Aggregate invariant report. Establishes internal numerical consistency under its batch-wide tolerance, not physics fidelity. |
| C08 | The checkpoint used 26,624 training and 6,656 validation events; the diagnostic bank contains 10,000 validation conditions at 50--250 GeV. | Configuration-hash-bound source evidence and report identity. The bank was repeatedly inspected and is not an untouched test. |
| C09 | The activity factorization, top-$k$ support, teacher forcing, pilot size, and eight-step solver are possible explanations. | Model implementation. No ablation, oracle, scaling, or convergence experiment supports causal attribution. |
| C10 | Public files reproduce the manuscript, figures, and aggregate arithmetic. | Build scripts, hashes, and QA. They do not reproduce training or event-level analysis. |
| C11 | Connectivity has physical motivation but the present metric is representation dependent. | ATLAS thresholded topological clustering motivates neighborhood structure; this paper uses a different zero-threshold model graph. No cross-detector equivalence is claimed. |
| C12 | Intended future EIC ZDC use is motivation only. | User context. No detector identity, affiliation, collaboration endorsement, or readiness claim. |
| C13 | The generator maps five condition features to a shared 128-component condition representation and then samples response, longitudinal profile, counts, support, and channel shares in sequence. | Source-level audit of the frozen v2 path. This describes computation, not fidelity. |
| C14 | The response head is a Bernoulli hurdle plus a four-component Gaussian mixture in transformed total deposit. | `response.py` and `system.py` at the source commit recorded in `model_exposition_20260922.json`. |
| C15 | Layer and channel shares are produced by separate conditional flows starting from separate Gaussian source states, each evaluated with eight fixed updates. | `profile.py`, `node_fields.py`, `flow_matching.py`, and the immutable evaluation contract. No solver-convergence claim. |
| C16 | Channel scores use three graph-message blocks and two transformer layers before exact top-$K_\ell$ selection. | `node_fields.py`, `graph.py`, `support.py`, and selected model dimensions. Exact cardinality does not imply connectivity. |
| C17 | The deterministic decoder gives nonnegative deposits and closes each layer to its sampled budget in exact arithmetic. | `support.py` plus aggregate decoder QA. This is closure to sampled readout energy, not conservation of incident energy. |
| C18 | Training uses nine teacher-forced component losses. | `trainer.py`, `truth.py`, and `losses.py`. Teacher forcing is a training procedure, not evidence that exposure bias caused the observed discrepancy. |
