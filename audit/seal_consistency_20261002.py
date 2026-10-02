"""Bind the final mentor PDF to the completed page review and unchanged QA guards."""
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path
from datetime import datetime, timezone
from consistency_session_20261002 import ROOT, record, sha

qa_path = ROOT / 'audit/qa_series/mentor_send_20261002/iteration_05.json'
qa = json.loads(qa_path.read_text())
prior = json.loads((qa_path.parent / 'iteration_04.json').read_text())
assert qa['result'] == 'pass' and qa['full_suite'] and len(qa['checks']) == 22
assert qa['pdf']['pages'] == 14
assert sha(ROOT / 'output/fast_mc_zdc_manuscript.pdf') == qa['pdf']['sha256']
assert [b['page'] for a, b in zip(prior['page_metrics'], qa['page_metrics']) if a['sha256'] != b['sha256']] == [9]
for page in qa['page_metrics']:
    p = ROOT / 'audit/qa_runs/mentor_send_20261002/iteration_05' / f"page-{page['page']:02d}.png"
    assert sha(p) == page['sha256']

old = (ROOT / 'audit/source_snapshots/mentor_consistency_20261002_main.tex').read_text()
new = (ROOT / 'main.tex').read_text()
for kind, count in [('equation', 14), ('tabular', 4)]:
    pattern = rf'\\begin\{{{kind}\}}.*?\\end\{{{kind}\}}'
    a, b = re.findall(pattern, old, re.S), re.findall(pattern, new, re.S)
    assert len(a) == count and a == b

snapshot = ROOT / 'audit/source_snapshots/mentor_consistency_20261002'
snapshot.mkdir(exist_ok=False)
for name in ['final_build_audit', 'visual_review_finalization_20260930', 'arxiv_package_20260930']:
    for suffix in ['.json', '.md']:
        shutil.copy2(ROOT / 'audit' / (name + suffix), snapshot / (name + suffix))

def twin(name, data, text):
    p = ROOT / 'audit' / (name + '.json')
    p.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    p.with_suffix('.md').write_text(text + '\n', encoding='utf-8')

visual = {
    'created_utc': datetime.now(timezone.utc).isoformat(), 'result': 'pass',
    'pdf_sha256': qa['pdf']['sha256'],
    'page_sha256': {str(p['page']): p['sha256'] for p in qa['page_metrics']},
    'method': 'All fourteen QA04 page images read and visually inspected. QA05 pages 1-8 and 10-14 have identical image hashes; changed page 9 was reopened and read. All current rendered pages are covered.',
    'findings': 'No clipping, overlap, broken equation/citation, illegible figure or table, or unexplained page transition found. Last page contains the remaining bibliography.',
    'qa_record': str(qa_path.relative_to(ROOT)),
    'limits': 'Visual and consistency review only; not physics validation.'
}
twin('visual_review_finalization_20260930', visual,
     '# Current final visual review\n\nAll 14 current pages inspected, including every figure and table. QA05 changed only page 9 from the fully inspected QA04 render; that page was inspected again. No layout defect found. Exact page and PDF hashes are in the JSON twin. Previous review preserved in the consistency snapshot.')

members = ['main.tex', 'references.bib', 'main.bbl'] + ['figures/' + n for n in
    ['detector_geometry.png', 'generator_schematic.png', 'longitudinal_profile.png', 'support_summary.png']]
dest = ROOT / 'output/fast_mc_zdc_submission_source.zip'
with zipfile.ZipFile(dest, 'w', compression=zipfile.ZIP_DEFLATED) as archive:
    for member in members:
        archive.write(ROOT / member, member)
with zipfile.ZipFile(dest) as archive:
    assert archive.testzip() is None and archive.namelist() == members
    assert all(archive.read(m) == (ROOT / m).read_bytes() for m in members)
twin('arxiv_package_20260930', {
    'created_utc': visual['created_utc'], 'revision': '0.22.1', 'sha256': sha(dest),
    'members_sha256': {m: sha(ROOT / m) for m in members},
    'pdf_sha256': qa['pdf']['sha256'], 'status': 'Seven-file archive; CRC and exact bytes verified',
    'arxiv_server_compile': 'Not performed', 'current_qa': qa_path.relative_to(ROOT).as_posix(),
}, '# Current source package\n\nThe seven-file source archive matches the mentor consistency revision of v0.22.1. CRC and all member bytes were verified. No arXiv upload or server compilation was performed.')

record('Final visual and package verification', {
    'qa_record': qa_path.relative_to(ROOT).as_posix(), 'automated_groups': 22,
    'guard_tests': '10 passed; intentional negative native-build test preserved the PDF',
    'pages_visually_reviewed': 14, 'changed_page_reinspected': 9,
    'numbered_equations_unchanged': 14, 'table_bodies_unchanged': 4,
    'source_zip_sha256': sha(dest), 'status': 'Ready for exact-source release binding and Git commit.',
    'bibliography_scope': 'All 25 cited bibliography entries read; primary-source rechecks targeted the detector and recent related studies listed in the assessment.'
})
print('Final visual, equation/table preservation and source archive checks PASS')
