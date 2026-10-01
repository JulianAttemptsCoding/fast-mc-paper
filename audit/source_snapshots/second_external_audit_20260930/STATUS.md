# Scientific status

Version 0.17.0 is an arXiv preprint candidate describing one pilot ePIC ZDC simulation model on a repeatedly inspected development bank. It is not a validated FastMC or detector-performance result.

## Corrected central result

The supplied external audit identified an inference omitted in v0.16.0. Let m be graph components, R occupied-layer runs, and G interior inactive layers. With Q=m-R, 1 <= R <= G+1 implies delta mean Q >= delta mean m - mean G_generator = 29.9215 components, at least 83.18% of the 35.9703-component excess. Thus empty-layer separations alone are insufficient: a within-run graph discrepancy is established. It is not necessarily lateral fragmentation, a physical-cluster effect, or causal attribution to a model stage. The earlier claim that the aggregates could not establish within-run fragmentation is superseded.

## Scope and remaining research

The results concern one training seed, raw deposits without an added threshold/time cut, an incompletely documented production geometry, separate nonempty samples and a reused validation bank. Headline structural intervals, threshold/graph sensitivity, an activity-independence null, occupancy calibration, same-bank pair-grouped C2ST, reconstructed observables and model-only timing remain unfinished research. The older row-split C2ST values and their failed condition-only control remain disclosed. No new event generation, training, test inspection, calibration or detector threshold was introduced.

The author confirmed ePIC ZDC identity and data-owner approval for publication on 30 September 2026; no geometry tag was supplied. The paper does not claim equivalence to the current ePIC geometry. Name and email appear without an affiliation label at the author's request; Academia Sinica mentorship is acknowledged.

## Evidence

See audit/external_audit_response_20260930.md for every audit item, audit/component_bound_20260930.json for the derived arithmetic and mathematical checks, and audit/final_build_audit.json for the current exact-source release binding. The current arXiv upload package should contain only main.tex, references.bib, main.bbl and the four included figures. Upload and final inspection on arXiv have not been performed.
