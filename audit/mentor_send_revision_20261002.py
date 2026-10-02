"""Apply the mentor-send clarity revision (v0.22.1) by exact, counted byte replacement.

Numbered equations and numerical table bodies are not edited. Run once on v0.22.0.
"""
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = '0.22.1'
BASELINE_MAIN = '19ee0ec31df33e7506f450446ad85f352136b1421797d4573d83e470199e78c3'
BASELINE_COMMIT = 'd540f97'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace(path, old, new, count=1):
    raw = path.read_bytes()
    found = raw.count(old.encode('utf-8'))
    assert found == count, (path.name, old[:70], found)
    path.write_bytes(raw.replace(old.encode('utf-8'), new.encode('utf-8')))


def twin(name, payload, prose):
    dest = ROOT / 'audit' / name
    dest.with_suffix('.json').write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
    dest.with_suffix('.md').write_text(prose.rstrip() + '\n', encoding='utf-8')


tex = ROOT / 'main.tex'
assert sha(tex) == BASELINE_MAIN, 'Run once, on the v0.22.0 source'

EDITS = [
    # Abstract: particle species, direction of each comparison, classifier sentence without jargon.
    ('abstract',
     r"is compared with Geant4 at 10,000 matched incident conditions spanning 50--250\,GeV kinetic energy. Among nonempty showers, the mean active-layer count differs by 0.25, yet the last layer with a deposit lies 4.42 layers farther downstream and the occupied span contains 3.95 more skipped layers. The mean number of connected hit groups on the model graph rises from 23.42 to 59.39.",
     r"is compared with Geant4 at 10,000 matched incident-neutron conditions spanning 50--250\,GeV kinetic energy. Among nonempty showers, the mean active-layer count differs by only 0.25 (54.83 generated versus 54.58 Geant4, of 65 layers), yet the generated last layer with a deposit lies 4.42 layers farther downstream and the occupied span contains 3.95 more skipped layers. The mean number of connected hit groups on the model graph is 23.42 for Geant4 and 59.39 for the generator."),
    ('abstract',
     r"A row-split classifier distinguishes high-level summaries (AUROC 0.775), but its condition-only control fails (0.464); the classifier score is not a calibrated fidelity test.",
     r"A classifier separates generated from Geant4 showers on high-level summaries (AUROC 0.775, where 0.5 is chance), but its control using incident conditions alone gives 0.464 rather than 0.5, so the score is not a calibrated fidelity test."),
    # Sentence continuity after equations that end with a comma.
    ('conditioning',
     r"Here $\mathbf p=(p_x,p_y,p_z)$ is the three-momentum",
     r"where $\mathbf p=(p_x,p_y,p_z)$ is the three-momentum"),
    ('placement',
     r"Rank one denotes the largest noisy score. The sampler uses temperature $\tau=1$ and independent Gumbel perturbations $g_{\ell i}$ obtained",
     r"with temperature $\tau$ and random perturbations $g_{\ell i}$. Rank one denotes the largest noisy score. The sampler uses $\tau=1$ and independent Gumbel perturbations $g_{\ell i}$ obtained"),
    ('decoder',
     r"Consequently, in exact arithmetic, $|S_\ell|=K_\ell$",
     r"so that, in exact arithmetic, $|S_\ell|=K_\ell$"),
    # Terms used before they were defined.
    ('generator overview',
     r"Discrete heads generate visibility, layer activity, channel counts, and support; two conditional",
     r"Discrete heads generate visibility, layer activity, channel counts, and support (the set of active channels); two conditional"),
    ('generator overview',
     r"There is no learned shower encoder or common random event latent.",
     r"There is no learned shower encoder or common random event latent: no single random vector is shared by all stages of an event."),
    ('training',
     r"the free-running support diagnostics were evaluated subsequently",
     r"the free-running (fully sampled) support diagnostics were evaluated subsequently"),
    ('evaluation',
     r"eight 25\,GeV bins show its energy dependence.",
     r"eight 25\,GeV bins of incident kinetic energy show the energy dependence of the response."),
    ('evaluation',
     r"For all-event active-channel counts, $W_1$ is the area between empirical cumulative distributions, in channels~\cite{kansalmetrics}. The 95\% intervals for $W_1$, zero-deposit fraction",
     r"For a scalar observable, the Wasserstein-1 distance $W_1$ is the area between the generated and reference empirical cumulative distributions, in the units of that observable~\cite{kansalmetrics}; all events enter, with empty showers at zero. As a finite-sample scale, we also quote $W_1$ between two disjoint 5,000-event halves of the Geant4 sample (the reference-half scale); it is a descriptive comparison, not a critical value. The 95\% intervals for the active-channel-count $W_1$, zero-deposit fraction"),
    ('evaluation',
     r"has chance benchmark 0.5~\cite{c2st,kansalmetrics}.",
     r"has chance benchmark 0.5 and equals 1 for perfect separation~\cite{c2st,kansalmetrics}."),
    # Table 1 row names tied to the symbols of the evaluation section (table body unchanged).
    ('results table caption',
     r"Differences are generator minus reference, computed before rounding; pp denotes percentage points.}",
     r"Inactive layers in span is the gap count $G$ of Eq.~\eqref{eq:gaps}; weak graph components are the graph-connected hit groups $m$ of Sec.~\ref{sec:diagnostics}. Differences are generator minus reference, computed before rounding; pp denotes percentage points.}"),
    # Deposited energy: physical scale of the stored total, binwise error scale, plain wording.
    ('deposited energy',
     r"a difference of 0.045\,GeV (1.0\%). Opposing section shifts are concealed:",
     r"a difference of 0.045\,GeV (1.0\%). Both are about 3\% of the 149.9\,GeV mean incident kinetic energy: the stored total counts only energy deposited in readout channels and is neither a calibrated energy nor a sampling-fraction measurement. Opposing section shifts are concealed:"),
    ('deposited energy',
     r"without constituting a matched-size significance test.",
     r"without constituting a matched-size significance test. In every energy bin the standard deviation of the stored total is comparable to its mean (Table~\ref{tab:energy_bins}), so each binwise mean has a standard error near 3\%. On the same independent-sample scale, the largest binwise mean difference ($-7.65\%$ at 150--175\,GeV) is 2.0 standard errors; the alternating signs in Table~\ref{tab:energy_bins} therefore do not establish an energy-dependent bias."),
    ('deposited energy',
     r"cannot be split reliably into hurdle and clamp contributions",
     r"cannot be split reliably into Bernoulli-draw ($V_0=0$) and zero-clamp contributions"),
    # Longitudinal activity: figure cross-references and a physical length.
    ('longitudinal activity',
     r"but the last positive deposit is farther downstream.",
     r"but the last positive deposit is farther downstream (Table~\ref{tab:results}; Fig.~\ref{fig:support}, bottom)."),
    ('longitudinal activity',
     r"last active layer by $+4.42$.",
     r"last active layer by $+4.42$, about 0.11\,m at the 24.9\,mm median HCAL layer spacing."),
    ('longitudinal activity',
     r"does not isolate the energy of the additional occupied layers or disconnected components.",
     r"does not isolate the energy of the additional occupied layers or disconnected components. In Fig.~\ref{fig:longitudinal} (right), the generator-to-reference ratio of mean layer deposits is 0.84 at layer 51 and exceeds one from layer 60 onward, reaching 1.23 at layer 64."),
    # Hit pattern: relative size, figure reference, restored co-occupancy definition.
    ('hit pattern',
     r"Generated showers have 28.7 fewer positive-deposit channels but 35.97 more graph-connected hit groups;",
     r"Generated showers have 28.7 fewer positive-deposit channels ($-1.8\%$) but 35.97 more graph-connected hit groups (Fig.~\ref{fig:support}, bottom);"),
    ('hit pattern',
     r"Edge co-occupancy is 0.1375 for the generator and 0.1458 for Geant4. Because this fraction is not occupancy-normalized,",
     r"Edge co-occupancy, the all-event mean fraction of graph edges whose two end channels are both active, is 0.1375 for the generator and 0.1458 for Geant4. Because this fraction is not normalized to the number of active channels,"),
    ('numerical checks',
     r"The evaluator uses a common event/layer residual tolerance: the larger of",
     r"Closure residuals compare decoded deposits with the sampled budgets: $|\sum_{\ell i}Y_{\ell i}-T|$ per event and $|\sum_iY_{\ell i}-B_\ell|$ per layer. The evaluator uses a common tolerance for both: the larger of"),
    # Discussion: the proposed tests in plain terms.
    ('discussion',
     r"A reference activity null controlling energy, direction, $T$ and $F$ would test whether factorization reproduces the depth and gap shifts. An oracle cascade must replace the full activity mask; reference $T$ and $F$ alone leave the factorization intact.",
     r"A direct test builds a null sample from Geant4 itself: redraw each later layer's activity independently, with probabilities matched in energy, direction, $T$ and $F$, and check whether the depth and gap shifts appear. A complementary test runs the generator with the Geant4 activity mask substituted for its own; substituting only the reference $T$ and $F$ would leave the factorization intact."),
    ('conclusion',
     r"similar mean deposited energy and active-channel count do not imply",
     r"similar mean deposited energy, active-layer count and active-channel count do not imply"),
    ('acknowledgments', r"thanks Dr. Wen-Chen Chang", r"thanks Dr.~Wen-Chen Chang"),
    ('disclosure',
     r"Anthropic Claude provided an additional manuscript review and revision proposal; selected text",
     r"Anthropic Claude provided additional manuscript reviews, revision proposals and final clarity edits; selected text"),
]
for _, old, new in EDITS:
    replace(tex, old, new)

# One new paragraph: energy-weighted transverse summaries from the same released report.
anchor = b"Edge co-occupancy, the all-event mean fraction"
raw = tex.read_bytes()
assert raw.count(anchor) == 1
index = raw.index(anchor)
newline = b'\r\n' if raw[index - 2:index] == b'\r\n' else b'\n'
assert raw[index - 2 * len(newline):index] == 2 * newline
paragraph = (
    r"Energy-weighted transverse summaries from the same evaluation summary differ less than the hit pattern. "
    r"Among nonempty showers, the mean energy-weighted centroids differ by 0.5\,mm in $x$ and 1.1\,mm in $y$, "
    r"small compared with the 30.3\,mm ECAL pitch. The mean energy-weighted radial RMS about the centroid is "
    r"84.7\,mm for the generator and 87.1\,mm for Geant4 (2.8\% narrower); its all-event $W_1$ is 3.34\,mm, "
    r"against a 0.48\,mm reference-half scale. Energy weighting suppresses isolated low-energy channels, so these "
    r"summaries and the zero-threshold group counts probe different aspects of the shower; neither is a reconstructed position."
).encode('utf-8')
tex.write_bytes(raw[:index] + paragraph + 2 * newline + raw[index:])

# Figure 4 bar labels follow Figure 3 and Table 1.
replace(ROOT / 'scripts/reader_figures.py', '["Geant4", "model"]', '["Geant4", "generator"]')

# Version metadata and QA binding.
for filename in ['README.md', 'STATUS.md']:
    path = ROOT / filename
    data = path.read_bytes()
    assert b'Version 0.22.0' in data
    path.write_bytes(data.replace(b'Version 0.22.0', b'Version 0.22.1', 1))
    with path.open('a', encoding='utf-8', newline='\n') as handle:
        handle.write('\n## Mentor-send clarity revision\n\nVersion 0.22.1 restores definitions that earlier condensing had removed (Wasserstein distance, reference-half scale, edge co-occupancy, closure residuals, support), names the incident particle and both samples in the abstract, ties Table 1 row names to the symbols of the evaluation section, cross-references the result figures, and states the stored-energy scale and the depth shift in physical units. It adds one paragraph of energy-weighted transverse summaries and one binwise error-scale statement, both recomputed from the released aggregate report by `scripts/mentor_send_checks.py`. Numbered equations and numerical table bodies are unchanged. The binwise scale treats the samples as independent and is not a paired interval. No event-level data, checkpoint, threshold scan or new evaluation was used. See `audit/mentor_send_response_20261002.md`.\n')
replace(ROOT / 'CITATION.cff', 'version: 0.22.0', 'version: 0.22.1')
qa_path = ROOT / 'scripts/full_manuscript_qa.py'
replace(qa_path, 'Version 0.22.0', 'Version 0.22.1')
replace(qa_path, 'version: 0.22.0', 'version: 0.22.1')
replace(qa_path, '    paths += [ROOT / "audit/current_qa_series.json"]',
        '    paths += [ROOT / "audit/mentor_send_response_20261002.json", ROOT / "audit/mentor_send_response_20261002.md"]\n    paths += [ROOT / "audit/current_qa_series.json"]')
replace(qa_path, '    verify_review_additions(checks)\n    validate_repository(checks)',
        '    verify_review_additions(checks)\n    from mentor_send_checks import verify_mentor_send_additions\n    verify_mentor_send_additions(checks)\n    validate_repository(checks)')
replace(ROOT / 'scripts/write_build_audit.py', 'v0.22.0', 'v0.22.1')
replace(ROOT / 'scripts/write_build_audit.py', 'Version 0.22.0', 'Version 0.22.1')

previous = ROOT / 'audit/qa_series/claude_review_20261002/iteration_02.json'
series = {'series': 'mentor_send_20261002', 'predecessor': previous.relative_to(ROOT).as_posix(),
          'predecessor_sha256': sha(previous),
          'reason': 'Mentor-send clarity revision; numerical, equation/table preservation, page, split and release guards retained and one check module added.'}
(ROOT / 'audit/current_qa_series.json').write_text(json.dumps(series, indent=2) + '\n', encoding='utf-8')

for filename in ['audit/claim_register_20260922.json', 'audit/finalization_20260930.json']:
    path = ROOT / filename
    data = json.loads(path.read_text(encoding='utf-8'))
    if 'claim_register' in filename:
        data['current_revision'] = VERSION
        data['current_reader_revision'] = 'audit/mentor_send_response_20261002.md'
    else:
        data['current_main_tex_sha256'] = sha(tex)
    path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
with (ROOT / 'audit/claim_register_20260922.md').open('a', encoding='utf-8', newline='\n') as handle:
    handle.write('\nCurrent v0.22.1 restores reader definitions and adds released energy-weighted transverse means and a binwise independent-sample error scale. Paired covariance, structural intervals, group sizes and energies, and threshold robustness remain unmeasured. See `mentor_send_response_20261002.md`.\n')

decisions = [
    {'item': 'Abstract', 'disposition': 'Named the incident neutron, gave both sample values for the active-layer and group counts, and replaced row-split and condition-only jargon with the plain statement that the control gives 0.464 rather than 0.5.'},
    {'item': 'Definitions removed by earlier condensing', 'disposition': 'Restored: Wasserstein-1 distance for any scalar observable, the reference-half scale (two disjoint 5,000-event Geant4 halves), edge co-occupancy, closure residuals, support, free-running, and the Bernoulli-draw versus zero-clamp origin of empty showers. Each was used in Results without a prior definition.'},
    {'item': 'Naming', 'disposition': 'Table 1 body is byte-locked, so its caption now maps inactive layers in span to G and weak graph components to the graph-connected hit groups m. Figure 4 bars are labelled generator, as in Figure 3 and Table 1.'},
    {'item': 'Figures in Results', 'disposition': 'Sections 5.2 and 5.3 now cite Figure 4, which was referenced only from the evaluation section, and quote the Figure 3 mean-profile ratio at layers 51, 60 and 64.'},
    {'item': 'Physical scale', 'disposition': 'Stated that the stored total is about 3 percent of the 149.9 GeV mean incident kinetic energy and is neither a calibrated energy nor a sampling-fraction measurement; converted the 4.42-layer shift to about 0.11 m with the stored 24.9 mm HCAL layer spacing.'},
    {'item': 'Energy-bin table', 'disposition': 'Added the independent-sample error scale already adopted for the pooled mean: width comparable to mean in every bin, standard error near 3 percent, largest binwise difference 2.0 standard errors. No paired interval or chi-square is claimed.'},
    {'item': 'Transverse summaries', 'disposition': 'Added nonempty-sample energy-weighted centroid differences (0.5 mm, 1.1 mm) and radial RMS (84.7 versus 87.1 mm; W1 3.34 mm against a 0.48 mm reference-half scale) from the released report. Centroid W1 values are not quoted because the zero-deposit mass at the origin dominates them.'},
    {'item': 'Discussion tests', 'disposition': 'Rewrote the reference-activity-null and oracle-cascade sentences as concrete procedures; content unchanged.'},
    {'item': 'Equation punctuation', 'disposition': 'Numbered equations are byte-locked. The sentences following Eqs. 1, 10 and 12, which end with commas, now continue grammatically.'},
    {'item': 'Not changed', 'disposition': 'No numbered equation, numerical table body, figure data, model statement or evidence limit was altered. The title result still has no distribution, interval or threshold scan; that requires an event-level evaluation and is not a prose matter.'},
]
payload = {
    'created_utc': datetime.now(timezone.utc).isoformat(), 'revision': VERSION,
    'baseline_commit': BASELINE_COMMIT, 'baseline_main_sha256': BASELINE_MAIN, 'current_main_sha256': sha(tex),
    'replacements': [{'section': section, 'old_sha256': hashlib.sha256(old.encode()).hexdigest(), 'new': new} for section, old, new in EDITS],
    'inserted_paragraph': paragraph.decode('utf-8'),
    'decisions': decisions,
    'primary_research': ['https://arxiv.org/abs/2406.12877', 'https://arxiv.org/html/2406.12877v2', 'https://arxiv.org/abs/2512.20346', 'https://arxiv.org/abs/2608.12795'],
    'source_definitions_checked': ['src/cbsc_zdc/eval/metrics.py', 'src/cbsc_zdc/eval/topology.py', 'src/cbsc_zdc/eval/invariants.py'],
    'environment': {'python': sys.version, 'platform': platform.platform()},
    'new_event_or_test_data_access': False, 'new_model_evaluation': False,
    'status': 'Source revision complete; final QA and every-page review pending',
}
prose = ('# Mentor-send clarity revision\n\nVersion ' + VERSION + ' is a reader-facing revision of the one-checkpoint aggregate diagnostic note. It is not detector-performance validation.\n\n'
         + '\n\n'.join('## ' + item['item'] + '\n\n' + item['disposition'] for item in decisions)
         + '\n\n## Evidence\n\nThe JSON twin records every replaced string by hash with its replacement, the inserted paragraph, the checked evaluator source files and the primary references reread. Added numbers are recomputed in `scripts/mentor_send_checks.py`.\n')
twin('mentor_send_response_20261002', payload, prose)
print(json.dumps({'revision': VERSION, 'source_sha256': sha(tex), 'series': series['series'], 'replacements': len(EDITS)}, indent=2))
