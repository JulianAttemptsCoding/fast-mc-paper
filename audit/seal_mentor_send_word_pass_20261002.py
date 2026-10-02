"""Seal the word-by-word mentor-send pass (QA03) without changing source-bound inputs.

Supersedes the QA02 seal of the same uncommitted revision; the QA02 hashes are kept in the record.
"""
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
QA = ROOT / 'audit/qa_series' / SERIES / 'iteration_03.json'
QA02_SEAL = {
    'main_sha256': '52a7b267299a3999e1831a99aad3c95a101a0fab9f4761cbeef6f58dfbd3cc92',
    'pdf_sha256': '3c542932ce8cd519d279ea84a87913c64f892fa913fef779a588e1a6374c1bf6',
    'zip_sha256': 'be3049010dd6db2b2101ea8c42c35b123409edf15f9f72b8db620517f9d3ccb6',
    'qa': 'audit/qa_series/mentor_send_20261002/iteration_02.json',
}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def twin(root, name, data, prose):
    base = root / 'audit' / name
    base.with_suffix('.json').write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    base.with_suffix('.md').write_text(prose.rstrip() + '\n', encoding='utf-8')


qa = json.loads(QA.read_text(encoding='utf-8'))
assert qa['result'] == 'pass' and qa['full_suite'] is True
assert len(qa['checks']) == 22 and qa['pdf']['pages'] == 14
assert digest(ROOT / 'output/fast_mc_zdc_manuscript.pdf') == qa['pdf']['sha256'] != QA02_SEAL['pdf_sha256']
for page in qa['page_metrics']:
    assert digest(ROOT / 'audit/qa_runs' / SERIES / f"iteration_03/page-{page['page']:02d}.png") == page['sha256']
notes = [
    'Title, eleven-line abstract, introduction with the deeper-deposit wording and condition equation legible; Section 2 starts on this page.',
    'Target, geometry, gun context, materials, geometry figure, graph and population opening legible.',
    'Population, generator overview, architecture diagram and response equation legible.',
    'Response cap, activity factorization, flow target, flow-matching loss and update rule legible.',
    'Channel counts, placement, sampler, share target and decoder legible.',
    'Training, checkpoint selection, evaluation definitions with the reworded edge sentence, gap count and component bound legible; page full.',
    'Bound caveats with the explicit subject, Wasserstein and reference-half definitions, classifier paragraph one line longer with the checkpoint named, Table 1 and deposited-energy opening legible.',
    'Figure 3 with the cancellation caption, response error scales quoting both largest binwise differences, empty showers and longitudinal activity legible; page ends on the same line as before.',
    'Figure 4, hit-pattern results, transverse paragraph naming the narrower sample, co-occupancy and classifier results legible.',
    'Closure residuals, discussion, limitations opening with the zero-threshold wording and timing opening legible.',
    'Detector applications, conclusion, availability, acknowledgments, disclosure and Appendix A opening legible.',
    'Calibration table, settings, test-exposure statement, Appendix B and energy-bin table legible; Table 3 rows match the two values now quoted in Sec. 5.1.',
    'Classifier-seed table, evaluator details and references 1-16 legible.',
    'References 17-25 legible without clipping.',
]
visual = {
    'created_utc': datetime.now(timezone.utc).isoformat(), 'result': 'pass',
    'series': SERIES, 'iteration': 3, 'pdf_sha256': qa['pdf']['sha256'],
    'page_sha256': {str(p['page']): p['sha256'] for p in qa['page_metrics']},
    'review_method': 'All 14 QA02 pages were read, then the source word by word, which produced ten replacements. All 14 QA03 pages were read again in full from the released PDF; each replacement was located on its page and the page breaks were compared with QA02.',
    'page_notes': {str(i + 1): note for i, note in enumerate(notes)},
    'scope': 'Document consistency and visual review, not new physics validation.'
}
twin(ROOT, 'visual_review_finalization_20260930', visual,
     '# Current every-page visual review\n\nAll 14 final pages are covered by exact image hashes and were read in full in QA03 after the word-by-word pass. Figures, equations, tables and bibliography are legible, the ten replacements appear as intended and the page breaks match QA02; page 7 is one line longer inside its existing white space. Remaining short pages (7, 11, 12) end before an unbreakable figure or table. This is document QA, not physics validation.')
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
notes_text = (ROOT / 'output/arxiv_submission_notes.md').read_text(encoding='utf-8')
assert 'v0.22.1' in notes_text and 'audit/mentor_send_completion_20261002.md' in notes_text
response = json.loads((ROOT / 'audit/mentor_send_response_20261002.json').read_text(encoding='utf-8'))
assert response['current_main_sha256'] == digest(ROOT / 'main.tex') and len(response['third_pass']['replacements']) == 10
git = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True, text=True).stdout.strip()
final = {
    'created_utc': datetime.now(timezone.utc).isoformat(), 'revision': VERSION,
    'status': 'Local manuscript and submission-package QA complete after the word-by-word pass; sealed before commit; supersedes the QA02 seal of this revision',
    'baseline_commit': git, 'committed': False, 'pushed': False,
    'main_sha256': digest(ROOT / 'main.tex'), 'pdf_sha256': qa['pdf']['sha256'],
    'zip_sha256': digest(archive_path), 'checks': 22, 'visual_pages': 14, 'guard_tests': 10,
    'current_qa': package['current_qa'], 'full_qa_attempts': [1, 2, 3],
    'superseded_qa02_seal': QA02_SEAL,
    'word_pass': {'replacements': 10, 'numbers_changed': 0, 'equations_or_table_bodies_changed': 0,
                  'page_breaks_changed': 0, 'record': 'audit/mentor_send_response_20261002.json#third_pass'},
    'failed_attempts': response['failed_attempts'],
    'local_build': 'Clean pdfLaTeX/Biber build and all 22 QA groups passed',
    'environment': {'python': sys.version, 'platform': platform.platform()},
    'commands': ['python -X utf8 audit/mentor_send_revision_20261002.py',
                 'python -X utf8 scripts/full_manuscript_qa.py --iteration 1 ...',
                 'python -X utf8 audit/mentor_send_layout_20261002.py',
                 'python -X utf8 scripts/full_manuscript_qa.py --iteration 2 ...',
                 'python -X utf8 audit/seal_mentor_send_20261002.py',
                 'python -X utf8 audit/mentor_send_word_pass_20261002.py',
                 'python -X utf8 scripts/full_manuscript_qa.py --iteration 3 ...',
                 'python -X utf8 -m unittest discover -s scripts -p test_qa_guards.py',
                 'python -X utf8 audit/seal_mentor_send_word_pass_20261002.py', command],
    'inputs': {'qa_sha256': digest(QA), 'seal_script_sha256': digest(Path(__file__)),
               'response_sha256': digest(ROOT / 'audit/mentor_send_response_20261002.json')},
    'new_event_or_test_data_access': False, 'new_training_or_model_changes': False,
    'arxiv_uploaded': False,
    'remaining_empirical_work': 'Event-level uncertainties and paired covariance, a channel-energy threshold scan, same-bank pair-grouped classifier, repeated seeds, production configuration verification and detector-level validation remain unperformed.'
}
body = ('# Mentor-send clarity revision completed\n\nVersion ' + VERSION + ' restores definitions that earlier condensing had removed, names the incident particle and both samples in the abstract, ties Table 1 to the symbols of the evaluation section, cross-references the result figures from Results, and gives the stored-energy scale and depth shift in physical units. It adds one paragraph of energy-weighted transverse summaries and one binwise error-scale statement, both recomputed from the released aggregate report. Every numbered equation and numerical table body is unchanged.\n\n'
        'A word-by-word pass over the QA02 seal then made ten replacements. Section 5.1 had called -7.65% the largest binwise mean difference although Table 3 lists +7.74%; it now quotes both with their error scales (1.8 and 2.0 standard errors). Nine wordings were clarified. No number, equation, table body, figure or page break changed.\n\n'
        'QA03 passed all 22 groups at 14 pages; all 14 pages were read again and 10 release-guard tests passed. The seven-file source archive passes CRC and byte-identity checks. This record is written before the commit; the publication record carries the commit identity.\n\n'
        'The manuscript remains an aggregate diagnostic case study. Event-level uncertainties, a threshold scan, a same-bank pair-grouped classifier, repeated seeds and production configuration verification remain research limitations. No new physics validation or arXiv upload occurred. Exact hashes, environment, commands, the superseded QA02 seal and the failed first layout are in the JSON twin.')
for root, name in [(ROOT, 'mentor_send_completion_20261002'), (WORK, 'manuscript_mentor_send_completion_20261002')]:
    twin(root, name, final, body)
    with (root / 'logs.md').open('a', encoding='utf-8') as handle:
        handle.write('\n\n2026-10-02 mentor-send manuscript v' + VERSION + ' word-by-word pass sealed: the QA02 seal (main.tex ' + QA02_SEAL['main_sha256'] + ') was read in full and ten counted replacements were made. Sec. 5.1 called -7.65% the largest binwise mean difference while Table 3 lists +7.74%; it now quotes both with 1.8 and 2.0 standard errors. Nine wording clarifications; no number, numbered equation, table body, figure or page break changed. Every quoted number was recomputed from the released report and the recent references and cited design cuts were rechecked at arXiv and Crossref. QA03 passed 22 groups at 14 pages; all 14 pages read; 10 guard tests passed. main.tex ' + final['main_sha256'] + '; PDF ' + final['pdf_sha256'] + '; ZIP ' + final['zip_sha256'] + '. No raw/test data, DiCOS session or new model evaluation. Sealed before commit. See audit/' + name + '.json.\n')
print(json.dumps({'revision': VERSION, 'pdf_sha256': final['pdf_sha256'], 'zip_sha256': final['zip_sha256']}, indent=2))
