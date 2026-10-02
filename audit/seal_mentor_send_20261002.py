"""Seal the inspected mentor-send revision without changing source-bound inputs."""
import hashlib
import json
import platform
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = Path('C:/Users/Julia/Desktop/coding/ASIoP/Fast MC CBSC')
SERIES = 'mentor_send_20261002'
VERSION = '0.22.1'
QA = ROOT / 'audit/qa_series' / SERIES / 'iteration_02.json'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def twin(root, name, data, prose):
    base = root / 'audit' / name
    base.with_suffix('.json').write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    base.with_suffix('.md').write_text(prose.rstrip() + '\n', encoding='utf-8')


qa = json.loads(QA.read_text(encoding='utf-8'))
assert qa['result'] == 'pass' and qa['full_suite'] is True
assert len(qa['checks']) == 22 and qa['pdf']['pages'] == 14
assert digest(ROOT / 'output/fast_mc_zdc_manuscript.pdf') == qa['pdf']['sha256']
for page in qa['page_metrics']:
    assert digest(ROOT / 'audit/qa_runs' / SERIES / f"iteration_02/page-{page['page']:02d}.png") == page['sha256']
notes = [
    'Title, eleven-line abstract, introduction and condition equation legible; Section 2 starts on this page again.',
    'Target, geometry, gun context, materials, geometry figure, graph and population opening legible.',
    'Population, generator overview with support and latent glosses, architecture diagram and response equation legible.',
    'Response cap, activity factorization, flow target, flow-matching loss and update rule legible.',
    'Channel counts, placement, sampler sentence after Eq. 10, share target and decoder legible; text after Eq. 12 continues the sentence.',
    'Training, checkpoint selection, evaluation definitions, gap count and component bound legible; no white gap.',
    'Wasserstein and reference-half definitions, classifier caveat, Table 1 with symbol mapping and deposited-energy opening legible.',
    'Figure 3, response error scales, empty showers and longitudinal activity with physical length and figure references legible.',
    'Figure 4 with generator labels, hit-pattern results, transverse summaries, co-occupancy definition and classifier results legible.',
    'Closure residuals, discussion with rewritten diagnostic tests, limitations and timing opening legible.',
    'Detector applications, conclusion, availability, acknowledgments, disclosure and Appendix A opening legible.',
    'Calibration table, settings, test-exposure statement, Appendix B and energy-bin table legible.',
    'Classifier-seed table, evaluator details and references 1-16 legible.',
    'References 17-25 legible without clipping.',
]
visual = {
    'created_utc': datetime.now(timezone.utc).isoformat(), 'result': 'pass',
    'series': SERIES, 'iteration': 2, 'pdf_sha256': qa['pdf']['sha256'],
    'page_sha256': {str(p['page']): p['sha256'] for p in qa['page_metrics']},
    'review_method': 'All 14 QA01 pages read, which found the page-flow gaps on pages 1, 6 and 7. All 14 QA02 pages read again in full from the released PDF after the correction.',
    'page_notes': {str(i + 1): note for i, note in enumerate(notes)},
    'scope': 'Document consistency and visual review, not new physics validation.'
}
twin(ROOT, 'visual_review_finalization_20260930', visual,
     '# Current every-page visual review\n\nAll 14 final pages are covered by exact image hashes and were read in full in QA02. Figures, equations, tables and bibliography are legible. The white gaps found on pages 1, 6 and 7 of QA01 are gone; pages 1-6 are full. Remaining short pages (7, 11, 12) end before an unbreakable figure or table. This is document QA, not physics validation.')
command = [sys.executable, '-X', 'utf8', 'scripts/write_build_audit.py']
run = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8')
assert run.returncode == 0, run.stdout + run.stderr
print(run.stdout.strip())

members = ['main.tex', 'references.bib', 'main.bbl'] + ['figures/' + name for name in
    ('detector_geometry.png', 'generator_schematic.png', 'longitudinal_profile.png', 'support_summary.png')]
assert 'bbl format version 3.3' in (ROOT / 'main.bbl').read_text(encoding='utf-8')
archive_path = ROOT / 'output/fast_mc_zdc_submission_source.zip'
with zipfile.ZipFile(archive_path, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
    for name in members:
        archive.write(ROOT / name, name)
with zipfile.ZipFile(archive_path) as archive:
    assert archive.testzip() is None and archive.namelist() == members
    for name in members:
        assert archive.read(name) == (ROOT / name).read_bytes()
package = {
    'created_utc': datetime.now(timezone.utc).isoformat(), 'revision': VERSION,
    'sha256': digest(archive_path), 'members_sha256': {n: digest(ROOT / n) for n in members},
    'pdf_sha256': qa['pdf']['sha256'], 'status': 'Seven-file archive; CRC and exact bytes verified',
    'arxiv_server_compile': 'Not performed', 'current_qa': QA.relative_to(ROOT).as_posix(),
    'guidance_checked': ['https://info.arxiv.org/help/submit_tex.html', 'https://info.arxiv.org/help/faq/texlive.html']
}
twin(ROOT, 'arxiv_package_20260930', package,
     '# Current arXiv source package\n\nVersion ' + VERSION + '; seven required files only. CRC and exact source/figure bytes verified; hashes in the JSON twin. arXiv upload and server compilation remain unperformed.')
notes_path = ROOT / 'output/arxiv_submission_notes.md'
raw = notes_path.read_bytes()
for old, new in [(b'v0.22.0', b'v0.22.1'), (b'audit/claude_review_completion_20261002.md', b'audit/mentor_send_completion_20261002.md')]:
    assert raw.count(old) == 1, old
    raw = raw.replace(old, new)
notes_path.write_bytes(raw)
response = json.loads((ROOT / 'audit/mentor_send_response_20261002.json').read_text(encoding='utf-8'))
git = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
final = {
    'created_utc': datetime.now(timezone.utc).isoformat(), 'revision': VERSION,
    'status': 'Local manuscript and submission-package QA complete; not committed or pushed; supersedes the response audit pending-QA status',
    'baseline_commit': git, 'committed': False, 'pushed': False,
    'main_sha256': digest(ROOT / 'main.tex'), 'pdf_sha256': qa['pdf']['sha256'],
    'zip_sha256': digest(archive_path), 'checks': 22, 'visual_pages': 14, 'guard_tests': 10,
    'current_qa': package['current_qa'], 'full_qa_attempts': [1, 2],
    'failed_attempts': response['failed_attempts'],
    'local_build': 'Clean pdfLaTeX/Biber build and all 22 QA groups passed',
    'environment': {'python': sys.version, 'platform': platform.platform()},
    'commands': ['python -X utf8 audit/mentor_send_revision_20261002.py',
                 'python -X utf8 scripts/full_manuscript_qa.py --iteration 1 ...',
                 'python -X utf8 audit/mentor_send_layout_20261002.py',
                 'python -X utf8 scripts/full_manuscript_qa.py --iteration 2 ...',
                 'python -X utf8 -m unittest discover -s scripts -p test_qa_guards.py',
                 'python -X utf8 audit/seal_mentor_send_20261002.py', command],
    'inputs': {'qa_sha256': digest(QA), 'seal_script_sha256': digest(Path(__file__)),
               'response_sha256': digest(ROOT / 'audit/mentor_send_response_20261002.json')},
    'new_event_or_test_data_access': False, 'new_training_or_model_changes': False,
    'arxiv_uploaded': False,
    'remaining_empirical_work': 'Event-level uncertainties and paired covariance, a channel-energy threshold scan, same-bank pair-grouped classifier, repeated seeds, production configuration verification and detector-level validation remain unperformed.'
}
body = ('# Mentor-send clarity revision completed\n\nVersion ' + VERSION + ' restores definitions that earlier condensing had removed, names the incident particle and both samples in the abstract, ties Table 1 to the symbols of the evaluation section, cross-references the result figures from Results, and gives the stored-energy scale and depth shift in physical units. It adds one paragraph of energy-weighted transverse summaries and one binwise error-scale statement, both recomputed from the released aggregate report. Every numbered equation and numerical table body is unchanged.\n\n'
        'QA02 passed all 22 groups at 14 pages; all 14 pages were read and 10 release-guard tests passed. The seven-file source archive passes CRC and byte-identity checks. The working tree is not committed or pushed.\n\n'
        'The manuscript remains an aggregate diagnostic case study. Event-level uncertainties, a threshold scan, a same-bank pair-grouped classifier, repeated seeds and production configuration verification remain research limitations. No new physics validation or arXiv upload occurred. Exact hashes, environment, commands and the failed first layout are in the JSON twin.')
for root, name in [(ROOT, 'mentor_send_completion_20261002'), (WORK, 'manuscript_mentor_send_completion_20261002')]:
    twin(root, name, final, body)
    with (root / 'logs.md').open('a', encoding='utf-8') as handle:
        handle.write('\n\n2026-10-02 mentor-send manuscript v' + VERSION + ' sealed: QA02 passed 22 groups at 14 pages; all 14 pages read; 10 guard tests passed. main.tex ' + final['main_sha256'] + '; PDF ' + final['pdf_sha256'] + '; ZIP ' + final['zip_sha256'] + '. QA01 passed but its page flow had white gaps on pages 1, 6 and 7, corrected by shortening two abstract clauses. Numbered equations and numerical table bodies unchanged. No raw/test data, DiCOS session or new model evaluation. Not committed or pushed. See audit/' + name + '.json.\n')
print(json.dumps({'revision': VERSION, 'pdf_sha256': final['pdf_sha256'], 'zip_sha256': final['zip_sha256']}, indent=2))
