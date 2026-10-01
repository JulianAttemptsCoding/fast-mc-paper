# Experimental HEP readability audit: disposition

Three independent critiques were read in full against v0.20.0. The v0.21.0 pass edits the existing manuscript in place and preserves the measured population, graph, mathematical equations, tables, and negative controls.

## Adopted in the manuscript

- The title says spatial hit connectivity rather than readout connectivity, avoiding a confusion with electronics links. The abstract now defines a positive stored deposit as active and gives the physical meaning of the $R$/$Q$ bound before the notation.
- The first mention of support translates it as the positive-deposit hit pattern. The prose calls $R$ contiguous active-layer segments and $m$ graph-connected hit groups, with the exact mathematical definitions retained. The graph groups are explicitly distinguished from thresholded reconstruction clusters.
- The data section brings strict-positive threshold sensitivity next to the target definition. Zero total deposit is an observation whose physical cause is unassigned. Geometry now distinguishes stored-coordinate extent from $X_0$ and $\lambda_I$, and explains the 25-mrad slope as comparable to the EIC crossing convention without claiming a verified beam frame.
- The architecture stages now state the observable each samples. Conditional layer independence is connected to the possibility of skipped layers, and Gumbel selection to possible isolated channels. Both are hypotheses for the discrepancy, not demonstrated causes.
- The metric paragraph explains why a zero-deposit layer separates adjacent-layer graph paths, and why $Q=m-R$ counts disconnection left within a contiguous segment. It explicitly allows a failure to bridge adjacent active layers, so the bound is not mislabeled as purely transverse splitting.
- The classifier paragraph explains pair splitting in incident kinematics. The 0.464 control remains a failure compatible with such bias; its cause has not been established. The 0.65 criterion remains recorded development screening, not an independently verified predeclared physics acceptance threshold.
- Results place ECAL/HCAL opposite shifts alongside their possible calibration consequence, while preserving the uncalibrated nature of the evidence. Longitudinal results call the shifted last deposit an extended zero-threshold footprint rather than proven punch-through. The threshold and timing sensitivity requirement appears next to the graph interpretation.

## Rejected or qualified suggestions

- A zero total deposit does not prove a neutron passed through without interaction. Escapes, unrecorded material and other mechanisms remain unresolved.
- The line $x/z=-0.025$ has a 25-mrad slope compatible with the EIC crossing convention; without the production coordinate frame it cannot be asserted to be this sample's hadron beam axis.
- Multiple positions per stored HCAL ID do not establish SiPM ganging. The production volume and electronics map is missing.
- Graph components at $E>0$ are not ATLAS-style or ePIC reconstructed topological clusters. The $Q$ bound does not isolate transverse scattering, assign a causal fraction to layer factorization/Gumbel sampling, or quantify reconstruction harm.
- Tiny deposits may affect the zero-threshold result; the audits' claims of specific sub-eV/sub-keV energies, floating-point noise prevalence, or that a 0.25 MeV cut removes a given fraction are not in the retained data. Applying the cited design's cuts to this sample is a proposed sensitivity analysis, not a validated mapping.
- A later last positive-deposit layer is not measured shower termination, punch-through or leakage. The fixed-region energy mean does not identify the energy of extra occupied layers or isolated groups.
- Section energy shifts may change reconstructed response after section-specific calibration; no coefficients or reconstructed resolutions were measured. No fake-neutral, jet-scale or particle-identification effect is asserted.
- A 2,433-second residual includes generation, I/O and other untimed work. It cannot be described as a 243-ms generation latency, a throughput comparison, or a speed-up.
- The original C2ST condition-only control fails and the pair split permits a bias. Its exact mechanism and numerical contribution to the 0.464 score are not demonstrated. The layer-profile classifier score alone does not rank physical failure modes.

## Primary research and assurance boundary

The cited ePIC SiPM-on-tile design documents neutron energy/angle reconstruction, and its *own* reconstructed-hit requirement of $E>0.5$ MIP with 1 MIP at 0.5 MeV and $t<275$ ns: https://arxiv.org/html/2406.12877v2 . These cuts are not identified as the analyzed sample's production settings. ePIC reconstruction source uses a crossing-angle configuration of $-0.025$: https://eicrecon.epic-eic.org/doxygen/InclusiveKinematicsJB_8h_source.html . That supports a geometric comparison, not a coordinate-frame identity. The current paper's aggregate report and source-bound model audit support the numerical results and implementation claims. No new event-level, training, test, timing or reconstructed-hit evaluation was performed.

## Quality-control trace

All original numbered equations and four numerical tables remain unchanged. The current QA series retains every failed attempt: early checks caught stale wording guards and a current-source hash; the first expanded draft exceeded the 14-page limit. The text was condensed without changing margins, font size, scientific bounds, or the page limit. Attempt 13 passed all 20 groups at 14 pages; visual inspection then corrected one split sentence and the 70% per-row versus 4,200-row expectation in Appendix B. The final source is checked again in the active series.
