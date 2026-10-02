"""Seal the inspected October revision without changing source-bound inputs."""
import hashlib
import json
import platform
import subprocess
import sys
import zipfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORK = Path('C:/Users/Julia/OneDrive/Desktop/coding/ASIoP/Fast MC CBSC')
SERIES = 'claude_review_20261002'
QA = ROOT / 'audit/qa_series' / SERIES / 'iteration_02.json'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def twin(root, name, data, prose):
    base = root / 'audit' / name
    base.with_suffix('.json').write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    base.with_suffix('.md').write_text(prose.rstrip() + '\n', encoding='utf-8')

qa = json.loads(QA.read_text(encoding='utf-8'))
old = json.loads((QA.parent / 'iteration_01.json').read_text(encoding='utf-8'))
assert qa['result'] == 'pass' and qa['full_suite'] is True
assert len(qa['checks']) == 21 and qa['pdf']['pages'] == 13
assert digest(ROOT / 'output/fast_mc_zdc_manuscript.pdf') == qa['pdf']['sha256']
changed = [a['page'] for a, b in zip(old['page_metrics'], qa['page_metrics'], strict=True)
           if a['sha256'] != b['sha256']]
assert changed == list(range(7, 14)), changed
for page in qa['page_metrics']:
    assert digest(ROOT / 'audit/qa_runs' / SERIES / f"iteration_02/page-{page['page']:02d}.png") == page['sha256']
notes = [
    'Title, abstract, introduction and condition equation legible.',
    'Target, geometry, gun context, materials and geometry figure legible.',
    'Population, architecture diagram and response exposition legible.',
    'Response, activity and flow equations legible.',
    'Channel placement, energy shares and decoder legible.',
    'Training, evaluation definitions and component bound legible.',
    'Evaluation, classifier caveat, main results table and energy opening legible.',
    'Anchored Figure 3, response uncertainty, empty events and depth results legible.',
    'Anchored Figure 4 including all three aggregate comparisons and classifier discussion legible.',
    'Discussion, limitations and timing legible; no one-line widow.',
    'Conclusion, availability, acknowledgments, disclosure and Appendix A table legible.',
    'Appendices and all calibration/classifier tables legible.',
    'Complete references legible without clipping.'
]
visual = {
    'created_utc': datetime.now(timezone.utc).isoformat(), 'result': 'pass',
    'series': SERIES, 'iteration': 2, 'pdf_sha256': qa['pdf']['sha256'],
    'page_sha256': {str(p['page']): p['sha256'] for p in qa['page_metrics']},
    'review_method': 'All 13 QA01 pages directly inspected. QA02 pages 1-6 have identical rendered hashes; all changed QA02 pages 7-13 directly inspected at original resolution.',
    'page_notes': {str(i + 1): note for i, note in enumerate(notes)},
    'scope': 'Document consistency and visual review, not new physics validation.'
}
twin(ROOT, 'visual_review_finalization_20260930', visual,
     '# Current every-page visual review\n\nAll 13 final pages are covered by exact image hashes. Pages 1-6 match the fully inspected QA01 rendering; every changed page 7-13 was directly inspected in QA02. Figures, equations, tables and bibliography are legible. The figure/sentence interruption and widow were repaired. This is document QA, not physics validation.')
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
    'created_utc': datetime.now(timezone.utc).isoformat(), 'revision': '0.22.0',
    'sha256': digest(archive_path), 'members_sha256': {n: digest(ROOT / n) for n in members},
    'pdf_sha256': qa['pdf']['sha256'], 'status': 'Seven-file archive; CRC and exact bytes verified',
    'arxiv_server_compile': 'Not performed', 'current_qa': QA.relative_to(ROOT).as_posix(),
    'guidance_checked': ['https://info.arxiv.org/help/submit_tex.html', 'https://info.arxiv.org/help/faq/texlive.html']
}
twin(ROOT, 'arxiv_package_20260930', package,
     '# Current arXiv source package\n\nVersion 0.22.0; seven required files only. CRC and exact source/figure bytes verified; hashes in the JSON twin. arXiv upload and server compilation remain unperformed.')
notes_path = ROOT / 'output/arxiv_submission_notes.md'
text = notes_path.read_text(encoding='utf-8').replace('v0.21.1', 'v0.22.0').replace(
    'audit/hep_readability_followup_response_20261001.md', 'audit/claude_review_completion_20261002.md')
notes_path.write_text(text, encoding='utf-8')
response = json.loads((ROOT / 'audit/claude_review_response_20261002.json').read_text(encoding='utf-8'))
final = {
    'created_utc': datetime.now(timezone.utc).isoformat(), 'revision': '0.22.0',
    'status': 'Local manuscript and submission-package QA complete; supersedes the response audit pending-QA status',
    'main_sha256': digest(ROOT / 'main.tex'), 'pdf_sha256': qa['pdf']['sha256'],
    'zip_sha256': digest(archive_path), 'checks': 21, 'visual_pages': 13, 'guard_tests': 10,
    'current_qa': package['current_qa'], 'full_qa_attempts': [1, 2],
    'failed_attempts': response['failed_attempts'],
    'native_editor_compile': 'Two attempts failed before TeX: Unable to find standard directories for platform',
    'local_build': 'Clean pdfLaTeX/Biber build and all 21 QA groups passed',
    'environment': {'python': sys.version, 'platform': platform.platform()},
    'commands': ['C:/Python313/python.exe -X utf8 -m unittest discover -s scripts -p test_qa_guards.py -v',
                 'C:/Python313/python.exe -X utf8 audit/seal_claude_review_20261002.py', command],
    'inputs': {'review': response['input_review'], 'qa_sha256': digest(QA), 'seal_script_sha256': digest(Path(__file__))},
    'new_event_or_test_data_access': False, 'new_training_or_model_changes': False,
    'arxiv_uploaded': False,
    'remaining_empirical_work': 'Event-level uncertainties and paired covariance, threshold sensitivity, same-bank pair-grouped classifier, repeated seeds, production configuration verification and detector-level validation remain unperformed.'
}
body = '# October review revision completed\n\nVersion 0.22.0 incorporates supported review findings, strengthens physical interpretation and shows the measured structural means. It preserves every numbered equation and numerical table. The proposed exact paired error and product-of-means interpretation were not adopted because the available aggregates do not establish them.\n\nQA02 passed all 21 groups; all 13 pages were visually verified and 10 release-guard tests passed. The seven-file source archive passes CRC and byte-identity checks. Native editor compilation failed before TeX initialization; the local pdfLaTeX/Biber build passed. This completed record supersedes the response audit pending-QA status.\n\nThe manuscript is finalized as an aggregate diagnostic case study. Event-level uncertainties, threshold scans, same-bank pair-grouped classifier checks, repeated seeds and production configuration verification remain research limitations. No new physics validation or arXiv upload occurred. Exact hashes, environment, commands and failed attempts are preserved in the JSON twin.'
for root, name in [(ROOT, 'claude_review_completion_20261002'), (WORK, 'manuscript_claude_review_completion_20261002')]:
    twin(root, name, final, body)
    with (root / 'logs.md').open('a', encoding='utf-8') as handle:
        handle.write('\n\nOctober manuscript v0.22.0 sealed: QA02 passed 21 groups; all 13 pages visually verified; 10 guard tests passed. Seven-file ZIP CRC and byte identities verified. Native compiler initialization failed; local pdfLaTeX/Biber passed. No raw/test data or new model evaluation. See audit/' + name + '.json for commands, hashes, environment, failures and remaining empirical work.\n')
print(json.dumps({'revision': '0.22.0', 'pdf_sha256': final['pdf_sha256'], 'zip_sha256': final['zip_sha256']}, indent=2))
