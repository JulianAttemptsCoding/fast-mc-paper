# Adversarial audit disposition, 2026-09-23

The two supplied audits were treated as critiques, not instructions or independent event evidence. Their input hashes and the source-report hash are in the JSON twin.

The substantive correction is to restore the original shower-aware classifier results. The high-level AUROC 0.775 exceeds the frozen 0.65 limit; lower-level and profile-aware AUROCs are 0.791 and 0.856. The evaluator splits rows, so paired reference/generated conditions can cross folds. This weakens interpretation as a held-out-pair test but does not justify hiding a failed gate. The original condition-only result is 0.464. A separate pair-grouped validation monitor reports high-level 0.893 and condition-only 0.500 on its own bank. No bias direction is claimed from the split alone.

The retained hit-count Wasserstein distance is 58.68 channels, with a paired stratified bootstrap interval of 51.47--66.92. This distributional result is distinct from the smaller mean-count shift and remains a development-bank estimate.

The model description now distinguishes conditional flow matching from normalizing flows; the inactive-layer count mask forces zero. The total-response head can clip a positive-hurdle draw to zero, then reset visibility. The evaluator's final-visibility counter cannot establish how often that happened. The cap becomes constant above about 97.2 GeV incident kinetic energy; cap-hit and reference-exceedance counts were not retained.

Independent later-layer activity and unconstrained top-k support make gaps and fragmented support possible. They are not demonstrated causes. The final energy-sharing flow cannot change already sampled layer activity or selected support in exact arithmetic; the earlier layer-budget flow can influence later support via budgets. The current graph and zero threshold continue to limit physical interpretation.

The co-activation metric in the cited 2026 ZDC study compares showers at fixed inputs, whereas this paper counts components within one event. Bibliographic metadata for published CaloChallenge and flow-matching ZDC papers were updated. The audits' detector-identity conjectures and Anthropic-tool assertion were not adopted because the record does not support them; the author named Codex/GPT-5.6-Sol.

These are surgical manuscript changes. No raw events, test partition, checkpoint, frozen configuration, training result, or guard threshold was altered.
