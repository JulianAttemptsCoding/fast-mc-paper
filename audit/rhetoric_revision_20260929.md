# Scientific-language and rhetoric revision

Status: research complete; source revision pending. Intended release v0.13.0.

The user's four attached PDFs were read as examples, and the pasted comparison was used as requested guidance. Their embedded prose, citation placeholders and claims were not treated as instructions or as evidence for this checkpoint.

## Parnassus_2503.19981v1

Organizes dataset, method and results cleanly; conceptual event-level to particle-level decomposition precedes network details; results proceed by physical scale and explain comparison conventions before interpreting figures.

## Lamarr_2309.13213v1

Introduces modular pipeline input, output and dependencies before component prose; pairs validation observables with explicitly scoped timing evidence. This manuscript cannot adopt Lamarr's acceleration claim because it has no comparable end-to-end measurement.

## pGAN_1912.02748v1

Defines domain-specific fidelity checks and moves from low-level distributions to high-level event and downstream observables. This manuscript cannot add unavailable event-level or reconstruction analyses.

## HEIDi_2502.16330v2

Reports event sample sizes, interprets distributions by physical variable, and discusses residual discrepancies. Its reported timing and future speedups belong to that work, not to this ZDC checkpoint.

## Revision test

The paper should move from dataset and physical target to a conceptual cascade, then to a generation/evaluation protocol and results by physical scale. It should lead with measured observations, explain signs and denominators, and preserve the one-checkpoint validation-bank limit. No speedup, reconstruction or physics-fidelity result may be imported from the reference papers.

Input hashes, environment, commands and failed extraction attempt are in the JSON twin.

## Pass 1: opening and target

The abstract now states the physical comparison and its development-bank limit. The introduction moves from problem to field context to the specific structural question. Target, geometry, graph and sample provenance are separated. Current main.tex SHA-256: 0f2f19c1e683e34a79bcc101885626ce912fa4055047d9c593b6cb19037b1931.

## Passes 2–3: model narrative and equation prose

The model section now explains total response, longitudinal allocation and within-layer support before architecture details. Each equation has a short physical setup and interpretation; the mathematical expressions and numeric settings remain unchanged. Current main.tex SHA-256: 78ea541608ac46e50c927e7aa7c1921abd411029d441672dc1cb710dbb17dde4.

## Passes 4–5: evaluation and results

Evaluation definitions now precede results; result subsections follow global response, longitudinal activity, channel support and classifier/numerical checks. The gap equation, table values and plotted data were retained; captions were revised later in the audit. Current main.tex SHA-256: 6b717d6592b9f6539d917d7bd89ceb1dd9dc12d2e25a46cd642718e18278e33b.

## Passes 6–7: interpretation, conclusion, captions

Possible mechanisms are now explicitly hypotheses. The conclusion connects exact budget closure to the observed structural failure and states that speed/fidelity are unmeasured. Captions identify population and limits. Availability distinguishes the prior public package from this mentor-review revision. Current main.tex SHA-256: a3bc898501bf497d6f4881d085ea087bf83f12f70bf66ef1d7add95419fba812.

## Pass 8: speed and claim boundary

The immutable aggregate report records 0.3441926269 s/event of evaluator wall time for 10,000 events and includes topology and classifier analysis stages. The paper now states this is not generation latency and does not infer a speedup. Current main.tex SHA-256: c8f8b4e2504fa9110b12f61d1ae57656f731b1daa87804c679890524193fbb03.

## Passes 9–10: numbers and sentences

Eight source-bound evidence groups and eleven manuscript number/role assertions passed. Sentence review clarified the Bernoulli-logit antecedent, restored the exact count of five graph-edge inputs, split a long speed-benchmark sentence and standardized spelling. Current main.tex SHA-256: 939ff4792ecb74e80ed9eadcf4fd87b180942d4d086acfa038e0c53891a7d22b.

## Formatting and full-manuscript restarts

The current source SHA-256 is `5191c9c3a40519d6ae92e0d840af660f2ceaab163696398e6b3c79c7a4cd3d56`. Passes 11 and 12 revised pagination and release checks. Five whole-paper restarts reviewed scientific scope, mathematical chain, numerical denominators, page/figure sequence, and skeptical claim language. A read-only text assertion initially failed on two stale phrases; equivalent current assertions passed after correction. The final exact-PDF QA binding follows below.

## Exact-output verification

Full automated QA iteration 72 failed on a stale wording assertion and remains preserved. Iteration 73 passed all checks, including numerical/source identity, bibliography, four figures, PDF text and render extraction. All 12 current page PNGs were directly inspected; the JSON visual-review twin binds their hashes and the PDF hash. PDF SHA-256: `440bc3a55cc4d87523e0b81718eac129afaab33f4d4e49ba9c078c779421e795`.

## Final sentence correction

A literal final copyedit found a missing verb in the top-K connectivity sentence. The source and its exact-language QA assertion were corrected. Final source SHA-256: `dfd0c3628e097eb63a09f322c1ccb351303b18a171381477bd01df889ee29cfa`. The preceding iteration-73 PDF review is superseded by the next exact-output QA.

## Final copyedit QA

Iteration 74 failed on a second stale exact assertion and remains recorded. Iteration 75 passed the complete suite. Only page 5 changed relative to the fully inspected iteration-73 rendering; that page was inspected directly and all other eleven page hashes match. Final PDF SHA-256: `6b6dbcae67b27310fd49a8acd44d6bbab76c5ad7d7372db068e2da32531b1eb5`.
