"""Evidence-preserving fresh-reader copyedit; no experiment/data modifications."""
import hashlib
import json
import platform
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = Path('C:/Users/Julia/OneDrive/Desktop/coding/ASIoP/Fast MC CBSC')
AUDIT = ROOT / 'audit/fresh_reader_review_20260930.json'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def save(state, event):
    state['updated_utc'] = datetime.now(timezone.utc).isoformat()
    state.setdefault('events', []).append({'utc': state['updated_utc'], **event})
    state['current_source_sha256'] = sha(ROOT / 'main.tex')
    AUDIT.write_text(json.dumps(state, indent=2) + '\n', encoding='utf-8')
    note = '\n[' + state['updated_utc'] + '] Fresh-reader manuscript review: ' + event['summary'] + ' Source SHA256 ' + state['current_source_sha256'] + '.\n'
    for directory in (ROOT, PROJECT):
        with (directory / 'logs.md').open('a', encoding='utf-8') as stream:
            stream.write(note)
    lines = ['# Fresh-reader manuscript review', '', 'Status: ' + state['status'], '',
             'Scientific scope: descriptive one-checkpoint validation-bank case study. Document QA does not establish physics validation.', '',
             '## Findings and changes', '']
    for row in state.get('changes', []):
        lines.append('- ' + row['purpose'])
    lines += ['', '## Events', '']
    for row in state['events']:
        lines.append('- ' + row['utc'] + ': ' + row['summary'])
    lines += ['', 'Detailed section, equation and figure assessments: `audit/fresh_reader_assessment_20260930.md`.', '']
    AUDIT.with_suffix('.md').write_text('\n'.join(lines), encoding='utf-8')

def edit():
    if AUDIT.exists():
        raise FileExistsError('Refusing to overwrite an existing review')
    source = ROOT / 'main.tex'
    original = source.read_text(encoding='utf-8')
    before = {name: sha(ROOT / name) for name in ('main.tex', 'output/fast_mc_zdc_manuscript.pdf', 'references.bib', 'scripts/full_manuscript_qa.py', 'scripts/build_figures.py', 'audit/finalization_20260930.json', 'audit/final_build_audit.json', 'data/reports/dicos-f-02_epoch90.json', 'data/provenance/source_evidence.json')}
    snapshot = ROOT / 'audit/source_snapshots/fresh_reader_20260930'
    snapshot.mkdir(exist_ok=False)
    for name in ('main.tex', 'audit/finalization_20260930.json', 'audit/finalization_20260930.md', 'audit/final_build_audit.json', 'audit/final_build_audit.md', 'audit/visual_review_finalization_20260930.json'):
        (snapshot / Path(name).name).write_bytes((ROOT / name).read_bytes())
    state = {'status': 'review_in_progress', 'environment': {'platform': platform.platform(), 'python': sys.version}, 'input_sha256': before,
             'scope': 'Full manuscript, appendices, all four figures, all four tables and all fourteen equations; fresh-reader judgment with evidence checks, not independent human peer review.',
             'data_access': 'Local aggregate reports and source/provenance only; no raw, remote, or new test data access.',
             'initial_checks': ['Complete source read in order, lines 1-486', 'All fourteen QA87 rendered pages directly read and visually inspected', 'Existing dirty state preserved', 'Guide and focused operating rules read', 'Graft advertised legacy results despite freshness pass; not trusted or used as scientific evidence'],
             'failed_attempts': ['Initial path-discovery command exit 1: absent alternate OneDrive paper path and absent paper AGENTS.md; active paper discovered successfully.', 'Search queries did not return the two requested arXiv pages; direct URL opens verified them.'],
             'external_checks': ['https://arxiv.org/abs/2210.02747', 'https://proceedings.mlr.press/v97/kool19a.html', 'https://arxiv.org/abs/2410.21611', 'https://arxiv.org/abs/2608.12795'],
             'changes': []}
    save(state, {'summary': 'Baseline source and all 14 rendered pages read completely; input hashes and historical release/visual records snapshotted. Editorial corrections planned; no equations, results, data or guards changed.'})
    replacements = [
      ('Scope at first contact', 'a 6,790-channel Zero-Degree Calorimeter readout.', 'a 6,790-channel Zero-Degree Calorimeter readout, using raw deposited energies without a threshold.'),
      ('Define support before relying on it', 'For sparse showers, the occupied layers and channels, their correlations, and their spatial organization are part of that target.', 'For sparse showers, the occupied layers and channels, their correlations, and their spatial organization are part of that target. Here, support means the set of channels with positive deposit; occupancy counts its members.'),
      ('State the study contribution without a novelty or superiority claim', 'It provides a pilot case study of the generator and its diagnostics.', 'The contribution is a concrete diagnostic case: near-agreement in marginal means can coexist with a different organization of occupied layers. The architecture supplies the test case, rather than a demonstrated improvement over competing generators.'),
      ('Explain ganging in detector language', 'Of the HCAL IDs, 2,400 each gang two to four stable physical positions.', 'Of the HCAL IDs, 2,400 combine deposits from two to four stable physical positions into one readout channel (ganging).'),
      ('Give geometry figure a stated purpose', 'its first bar contains 400 ECAL and 3,990 HCAL channels.}', 'its first bar contains 400 ECAL and 3,990 HCAL channels. The centroid representation defines the spatial information available to both the model and the graph diagnostic.}'),
      ('Place estimand limitation beside the sampling design', 'No nominal test event is used here.', 'No nominal test event is used here. The comparison tests distributions over this bank, not reproduction of a particular Geant4 shower; one draw per condition cannot determine the full conditional shower distribution.'),
      ('Distinguish data dependencies from particle transport in architecture figure', 'Training uses reference-derived upstream quantities; sampling uses generated upstream quantities.}', 'Arrows show generation order, not every conditioning connection or particle transport. Training uses reference-derived upstream quantities; sampling uses generated upstream quantities.}'),
      ('Introduce starred reference notation explicitly', 'For a reference shower, let $B_\\ell^\\star=', 'A star denotes a reference-derived quantity. For a reference shower, let $B_\\ell^\\star='),
      ('Qualify fraction floors mathematically', 'they are numerical conventions, not detector thresholds.', 'they are numerical conventions, not detector thresholds. Fractions below the floor are modified before centering, so these targets do not preserve arbitrarily small shares exactly.'),
      ('Explain why attention is used without a causal claim', 'Its context includes $h_c$, the total $T$, layer identity, the activity mask, and a sinusoidal flow-time encoding.', 'Its context includes $h_c$, the total $T$, layer identity, the activity mask, and a sinusoidal flow-time encoding. Bidirectional attention lets each layer use information from all other layers; it is a statistical dependency, not backward particle transport.'),
      ('Disambiguate shared design versus shared parameters', "The channel-flow velocity network shares the support network's graph and layer-context design", "The channel-flow velocity network follows the support network's graph and layer-context design"),
      ('Calibrate main-text certainty to available provenance', 'Training-data gradient norms set the weights $w_j$. Response, layer-profile, and count weights hit the lower clipping bound; the visibility weight hit the upper bound.', 'The retained calibration proposal uses training-data gradient norms to set $w_j$. In that proposal, response, layer-profile, and count weights hit the lower clipping bound; the visibility weight hit the upper bound.'),
      ('Explain why frozen intermediate encoder matters', 'Each stage inherited the preceding checkpoint.', 'Each stage inherited the preceding checkpoint; freezing the encoder kept the inputs to previously trained heads fixed during intermediate stages.'),
      ('Translate gradient accumulation', 'batches of six accumulated over four steps,', 'batches of six accumulated over four steps (24 events per optimizer update),'),
      ('Make connected-component observable accessible', 'These support metrics condition on nonempty readout, leaving 9,907 reference and 9,858 generated showers.', 'A component is a group of occupied channels joined by paths using only occupied channels. These support metrics condition on nonempty readout, leaving 9,907 reference and 9,858 generated showers. The two nonempty subsets need not contain the same incident conditions.'),
      ('Explain graph confounding with a small algebraic example', 'Consecutive empty layers constitute one separation, so $G$ alone specifies neither $R$ nor lateral fragmentation.', 'Consecutive empty layers constitute one separation, so $G$ alone specifies neither $R$ nor lateral fragmentation. For example, occupied layers $1,2,5$ have span five, $G=2$, and $R=2$, whereas $1,3,5$ has the same span and $G$ but $R=3$.'),
      ('Explain C2ST failure scale rather than treating AUROC as percent fidelity', 'Its high-level score exceeds the predeclared maximum of 0.65.', 'Its high-level score exceeds the predeclared maximum of 0.65. This is a classifier discrimination score, not a percentage of physically incorrect showers.'),
      ('Make the support figure self-contained about uncertainty', "components use the same readout graph as the generator.}", "components use the same readout graph as the generator. Uncertainty intervals for these means are unavailable.}"),
      ('Limit interpretation of a mean energy profile', "These event averages do not resolve individual interior gaps.}", "These event averages expose section-level compensation but do not resolve individual interior gaps.}"),
      ('Avoid implying independence between gaps and graph effects', 'The larger component count can therefore include both longitudinal separations and fragmentation within occupied layers.', 'The larger component count can therefore include both longitudinal separations and disconnected regions within an occupied run.'),
      ('Prioritize a specific evidence-resolving next step', 'Within that scope, it demonstrates the value of resolving longitudinal support when assessing a generator whose mean response and occupancy appear similar to the reference.', 'Within that scope, it demonstrates the value of resolving longitudinal support when assessing a generator whose mean response and occupancy appear similar to the reference. Event-level run counts with paired uncertainty estimates and threshold scans are the next tests needed to establish the robustness and origin of this pattern.'),
    ]
    revised = original
    for purpose, old, new in replacements:
        if revised.count(old) != 1:
            raise ValueError((purpose, 'replacement not unique', revised.count(old)))
        revised = revised.replace(old, new)
        state['changes'].append({'purpose': purpose, 'old': old, 'new': new})
    assert re.findall(r'\\begin\{equation\}.*?\\end\{equation\}', original, re.S) == re.findall(r'\\begin\{equation\}.*?\\end\{equation\}', revised, re.S)
    assert re.findall(r'\\begin\{tabular\}.*?\\end\{tabular\}', original, re.S) == re.findall(r'\\begin\{tabular\}.*?\\end\{tabular\}', revised, re.S)
    source.write_text(revised, encoding='utf-8', newline='\n')
    # Keep the existing current-source guard active, preserving its previous exact record.
    finalpath = ROOT / 'audit/finalization_20260930.json'
    final = json.loads(finalpath.read_text(encoding='utf-8'))
    final.setdefault('subsequent_source_revisions', []).append({'audit': str(AUDIT.relative_to(ROOT)), 'previous_source_sha256': before['main.tex'], 'new_source_sha256': sha(source), 'reason': 'Fresh-reader clarification; all equations and all numerical tables unchanged; rebuild pending.'})
    final['current_main_tex_sha256'] = sha(source)
    finalpath.write_text(json.dumps(final, indent=2) + '\n', encoding='utf-8')
    with finalpath.with_suffix('.md').open('a', encoding='utf-8') as stream:
        stream.write('\nFresh-reader follow-up: current source pointer updated; historical exact release preserved under audit/source_snapshots/fresh_reader_20260930. See fresh_reader_review_20260930 twin. Rebuild pending.\n')
    save(state, {'summary': f'Applied {len(replacements)} reader-oriented prose/caption corrections. All 14 equation blocks and all four numerical tables remain identical. Current-source provenance pointer updated with preserved historical snapshot. Full build pending.', 'command': 'python audit/fresh_reader_revision_20260930.py edit', 'output_sha256': {name: sha(ROOT / name) for name in ('main.tex', 'audit/finalization_20260930.json')}})
    print('Applied', len(replacements), 'clarifications; mathematical and numerical blocks unchanged.')

if __name__ == '__main__':
    if sys.argv[1] == 'edit':
        edit()
    elif sys.argv[1] == 'event':
        state = json.loads(AUDIT.read_text(encoding='utf-8'))
        save(state, {'summary': sys.argv[2], 'command': sys.argv[3] if len(sys.argv) > 3 else None})
