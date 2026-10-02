"""Synchronize the reader revision, evidence response and immutable QA series."""
import hashlib
import json
import platform
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = Path('C:/Users/Julia/OneDrive/Desktop/coding/ASIoP/Fast MC CBSC')
CONTEXT = Path('C:/Users/Julia/Desktop/coding/ASIoP/Fast MC CBSC')
NOW = datetime.now(timezone.utc).isoformat()
VERSION = '0.22.0'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace(path, old, new, count=1):
    raw = path.read_bytes()
    assert raw.count(old.encode()) == count, (path, old, raw.count(old.encode()))
    path.write_bytes(raw.replace(old.encode(), new.encode()))


def twin(root, name, payload, prose):
    dest = root / 'audit' / name
    dest.with_suffix('.json').write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
    dest.with_suffix('.md').write_text(prose.rstrip() + '\n', encoding='utf-8')


tex = ROOT / 'main.tex'
replace(tex, 'this value has not been checked against the released events', 'this reported value is not independently verified by the released aggregates')
replace(tex, 'Their mean first active layer shifts', 'The generated mean first active layer shifts')
replace(tex, 'statistics on separately nonempty showers', 'statistics computed within each sample\'s nonempty showers')
replace(tex, 'This tests a different, energy-normalized quantity from the 0.045', 'This tests a different, energy-normalized quantity from the 0.045')
anchor = "the exact paired standard error needs their unretained covariance."
replace(tex, anchor, anchor + r" The total-deposit distributions have $W_1=0.073\,\GeV$, below the 0.147\,GeV reference-half scale. This supports descriptive agreement of the total response at this sample size, without constituting a matched-size significance test.")
# Disambiguate overloaded symbols locally without altering source-verified model equations.
replace(tex, 'For active set $S$, the largest-group fraction', 'In this diagnostic, $m$ denotes the group count. For active set $S$, the largest-group fraction')
replace(tex, 'source-bound nonempty-sample means', 'nonempty-sample means from the evaluation summary')
replace(tex, '% page reservation removed after visual review', '% Allow natural page flow.', count=3)

for filename in ['README.md', 'STATUS.md']:
    path = ROOT / filename
    raw = path.read_bytes()
    old = b'Version 0.21.1'
    assert old in raw
    path.write_bytes(raw.replace(old, b'Version 0.22.0', 1))
    with path.open('a', encoding='utf-8') as handle:
        handle.write('\n## October reader review\n\nVersion 0.22.0 adds a structural-data panel beside the definitions, repairs the geometry guide and tick labels, reports the depth-distribution discrepancy, identifies the pooled response widths, and states the fixed gun vertex and nominal materials as documented context with explicit provenance limits. The uncertainty calculation is an independent-sample error scale, not a recovered paired interval. No threshold scan or event-level experiment was performed. See `audit/claude_review_response_20261002.md`.\n')
replace(ROOT / 'CITATION.cff', 'version: 0.21.1', 'version: 0.22.0')
replace(ROOT / 'CITATION.cff', 'date-released: 2026-10-01', 'date-released: 2026-10-02')
replace(ROOT / 'scripts/full_manuscript_qa.py', 'Version 0.21.1', 'Version 0.22.0')
replace(ROOT / 'scripts/full_manuscript_qa.py', 'version: 0.21.1', 'version: 0.22.0')
replace(ROOT / 'scripts/write_build_audit.py', 'v0.21.1', 'v0.22.0')
replace(ROOT / 'scripts/write_build_audit.py', 'Version 0.21.1', 'Version 0.22.0')
replace(ROOT / 'scripts/second_audit_checks.py', 'This evaluation study uses one checkpoint and 10,000 validation conditions', 'aggregate reanalysis of one checkpoint on 10,000 repeatedly inspected validation conditions')
replace(ROOT / 'scripts/second_audit_checks.py', "'4.759 and 4.830'", "'4.759\\\\,GeV for Geant4', '4.830\\\\,GeV for the generator'")
qa_path = ROOT / 'scripts/full_manuscript_qa.py'
replace(qa_path, '    paths += [ROOT / "audit/current_qa_series.json"]', '    paths += [ROOT / "audit/claude_review_response_20261002.json", ROOT / "audit/claude_review_response_20261002.md"]\n    paths += [ROOT / "audit/current_qa_series.json"]')
replace(qa_path, '    validate_reader_revision(checks)\n    validate_repository(checks)', '    validate_reader_revision(checks)\n    from review_october_checks import verify_review_additions\n    verify_review_additions(checks)\n    validate_repository(checks)')

previous = ROOT / 'audit/qa_series/hep_readability_followup_20261001/iteration_06.json'
series = {'series': 'claude_review_20261002', 'predecessor': previous.relative_to(ROOT).as_posix(), 'predecessor_sha256': sha(previous), 'reason': 'Source-checked October reader review; numerical, equation/table preservation, page, split and release guards retained.'}
(ROOT / 'audit/current_qa_series.json').write_text(json.dumps(series, indent=2) + '\n', encoding='utf-8')
for filename in ['audit/claim_register_20260922.json', 'audit/finalization_20260930.json']:
    path = ROOT / filename
    data = json.loads(path.read_text(encoding='utf-8'))
    if 'claim_register' in filename:
        data['current_revision'] = VERSION
        data['current_reader_revision'] = 'audit/claude_review_response_20261002.md'
    else:
        data['current_main_tex_sha256'] = sha(tex)
    path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
with (ROOT / 'audit/claim_register_20260922.md').open('a', encoding='utf-8') as handle:
    handle.write('\nCurrent v0.22.0 adds documented gun/material context and aggregate structural plots. Exact paired response covariance, group-size/energy distributions and threshold robustness remain unmeasured. See `claude_review_response_20261002.md`.\n')

review = CONTEXT / 'audit/manuscript_review_claude_20261002.md'
context = {}
for relative, excerpt in [
    ('docs/V3_FULL_REPORT.md', 'The generator vertex silently defaulted to the origin. True value is [-917.41, -30.0, 35488.91] mm.'),
    ('docs/DATA_CONTRACT.md', 'Historical detector context to verify, not assume: nominal LYSO ECAL and steel/scintillator HCAL; fixed vertex conversion check.'),
]:
    source = CONTEXT / relative
    context[relative] = {'path': str(source), 'sha256': sha(source), 'excerpt_summary': excerpt, 'status': 'Project documentary context; does not independently identify the historical Geant4 production.'}
decisions = [
    {'item': 'Headline data figure', 'disposition': 'Added three aggregate mean comparisons to Figure 4 while retaining the definition illustration. Structural distributions and intervals cannot be reconstructed from means.'},
    {'item': 'Response uncertainty', 'disposition': 'Report 0.068 GeV independent-sample SE scale; do not adopt exact 0.065 GeV paired SE or chi-square. Conditional independence does not determine covariance of the conditional means within each energy bin; the review requires additional assumptions.'},
    {'item': 'Depth and response distributions', 'disposition': 'Report depth W1=0.971 layers versus half-split 0.155, and response W1=0.073 GeV versus half-split 0.147. These unequal-size empirical scales do not establish a calibrated significance test.'},
    {'item': 'Geometry and gun', 'disposition': 'Verify graph connectivity and median nearest-centroid spacing from static geometry. Report gun vertex and nominal materials as documentary context with an explicit production-evidence caveat. Remove misleading beam guide and crowded tick.'},
    {'item': 'Product-of-means satellite estimate', 'disposition': 'Do not turn products of marginal means into mean group size or energy. State only that both samples retain a dominant connected group and sizes/energies remain unmeasured.'},
    {'item': 'Prose and architecture', 'disposition': 'Name flow-matching shower generator; clarify motivation and aggregate scope, coarse-to-fine generation, pooled-width ordering, depth distribution, bound range, and timing heading. Model equations and numerical table bodies remain unchanged.'},
    {'item': 'Form guards', 'disposition': 'AGENTS rule 23 forbids weakening assertions to pass. Retained the 14-page maximum, equation/table preservation and exact figure set. Equivalent source-wording checks now require explicit width ordering. Natural page flow and standard 10-point article typography fit without removing scientific content; bibliography remains 8 point.'},
    {'item': 'Event-level experiments and frozen runtime weights', 'disposition': 'Not represented as completed. The paper package lacks events/checkpoint/runtime config; no DiCOS session, raw/test data access, retraining, metadata request or new model experiment was performed. The manuscript remains an aggregate diagnostic case study.'},
]
failures = [
    'Initial PowerShell audit writer parser error; corrected before any write.',
    'V3_FULL_REPORT absent in OneDrive checkout; found and hashed in the reviewer-named Desktop checkout.',
    'First source-edit script assumed uniform CRLF; assertion rejected mixed line endings; matcher corrected before source write.',
    'Figure relocation regex moved the intervening result prose. Visual check caught it; restored exact HEAD source and replayed only supported edits. Earlier placement/flow records are superseded.',
    'Several 11-point layout probes remained 15 pages. 0.70/0.65-inch margin probes were rejected and original 0.75-inch margins restored.',
    'Layout helper count assertions and one apply_patch context failed before writes; corrected. Removing conservative page reservations alone still gave 15 pages.',
    '10-point build reached 13 pages but failed an overfull bibliography box; 8-point bibliography with flexible line breaking corrected it.',
]
payload = {'created_utc': NOW, 'revision': VERSION, 'input_review': {'path': str(review), 'sha256': sha(review)}, 'baseline_commit': '7d14229b914aa1f519d17bc37504c0c93620212a', 'current_main_sha256': sha(tex), 'context_sources': context, 'primary_research': ['https://arxiv.org/html/2406.12877v2'], 'decisions': decisions, 'failed_attempts': failures, 'environment': {'python': sys.version, 'platform': platform.platform()}, 'new_event_or_test_data_access': False, 'new_model_evaluation': False, 'status': 'Source revision complete; final QA and every-page review pending'}
prose = '# Response to the 2 October manuscript review\n\nVersion 0.22.0 retains the one-checkpoint, aggregate-only diagnostic scope. It is not detector-performance validation.\n\n' + '\n\n'.join('## ' + x['item'] + '\n\n' + x['disposition'] for x in decisions) + '\n\n## Evidence and failed attempts\n\nThe JSON twin binds the input review, documentary context, source revision, primary design reference, environment and all failed attempts. The diagram relocation error was detected in the rendered reading order and fully reversed. Historical probe/placement records do not apply to the final source. Final QA and PDF hashes are recorded separately in the release audit.\n'
for root, name in [(ROOT, 'claude_review_response_20261002'), (WORK, 'manuscript_claude_review_response_20261002')]:
    twin(root, name, payload, prose)
    with (root / 'logs.md').open('a', encoding='utf-8') as handle:
        handle.write('\n2026-10-02 October review source revision v0.22.0: main.tex ' + sha(tex) + '. See audit/' + name + '.json for adopted/rejected inferences, documentary hashes, primary research, all layout/editor failures and corrections. No event/test access or new experiment. Version metadata and source-binding QA synchronized; final checks pending.\n')
# Preserve failed render probes as clearly labelled historical evidence.
probe_root = ROOT / 'audit/qa_runs/claude_review_20261002/probes_superseded'
probe_root.mkdir(parents=True, exist_ok=True)
for path in (ROOT / 'audit').glob('probe_*.png'):
    target = probe_root / path.name
    assert path.resolve().is_relative_to(ROOT.resolve()) and target.resolve().is_relative_to(ROOT.resolve())
    assert not target.exists()
    path.rename(target)
print(json.dumps({'revision': VERSION, 'source_sha256': sha(tex), 'series': series['series']}, indent=2))
