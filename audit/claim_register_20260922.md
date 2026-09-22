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
