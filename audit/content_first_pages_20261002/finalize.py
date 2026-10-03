"""Bind the content-first 15-page paper, visual review and source package."""
import json
import re
import zipfile
from datetime import datetime, timezone
from session import ROOT, HERE, record, sha

qa_path = ROOT / 'audit/qa_series/mentor_send_20261002/iteration_18.json'
prior = json.loads((qa_path.parent / 'iteration_17.json').read_text(encoding='utf-8'))
qa = json.loads(qa_path.read_text(encoding='utf-8'))
assert qa['result'] == 'pass' and qa['full_suite'] is True
assert len(qa['checks']) == 22 and qa['pdf']['pages'] == 15
assert qa['pdf']['sha256'] == sha(ROOT / 'output/fast_mc_zdc_manuscript.pdf')
assert all(qa['page_metrics'][i]['sha256'] == prior['page_metrics'][i]['sha256'] for i in range(10))
now = datetime.now(timezone.utc).isoformat()
findings = {
    '1-10': 'Every page has the exact rendered pixel SHA-256 of the prior directly inspected QA17 release. Title, abstract, methods, equations 1-14, four figures and Table 1 remain legible; Figure 4(c1) still reads last active layer.',
    '11': 'The complete fuller structural-limitation paragraph, threshold caveats and detector/timing discussion are readable; the page ends naturally before Conclusion.',
    '12': 'Conclusion is together on one page, followed by availability, acknowledgments, AI disclosure and Appendix A identity; no crowding or clipping.',
    '13': 'Table 2, calibration/split provenance, Appendix B, and all eight response-bin rows of Table 3 legible.',
    '14': 'Table 4 and classifier explanation legible; references 1-16 start below the appendix without detached labels.',
    '15': 'References 17-25 continue with intact titles, identifiers and links. Deliberate white space after the final entry is preferable to compressing text to an arbitrary page target.'
}
visual = {
    'created_utc': now, 'result': 'pass', 'pdf_sha256': qa['pdf']['sha256'],
    'page_sha256': {str(p['page']): p['sha256'] for p in qa['page_metrics']},
    'method': 'Direct visual inspection of QA18 pages 11-15; exact rendered pixel comparison of QA18 pages 1-10 against the prior all-page QA17 direct visual review. All 15 current pages therefore covered.',
    'qa_record': str(qa_path.relative_to(ROOT)).replace('\\', '/'),
    'page_findings': findings,
    'findings': 'No clipping, overlap, missing glyph, unreadable figure/table text, detached caption or unresolved citation observed. The Conclusion starts at the top of page 12 and all 25 references are legible across pages 14-15.'
}
vp = ROOT / 'audit/visual_review_finalization_20260930.json'
vp.write_text(json.dumps(visual, indent=2) + '\n', encoding='utf-8')
vp.with_suffix('.md').write_text(
    '# Current complete visual review\n\n' + now + '\n\nPDF SHA-256: ' + visual['pdf_sha256']
    + '. All 15 pages covered by direct inspection or identical-pixel comparison.\n\n'
    + '\n'.join('- Page ' + n + ': ' + finding for n, finding in findings.items())
    + '\n\n' + visual['findings'] + '\n', encoding='utf-8')
record('Content-first all-page visual review passed', visual)

members = ['main.tex', 'references.bib', 'main.bbl', 'figures/detector_geometry.png',
           'figures/generator_schematic.png', 'figures/longitudinal_profile.png', 'figures/support_summary.png']
target = ROOT / 'output/fast_mc_zdc_submission_source.zip'
with zipfile.ZipFile(target, 'w', zipfile.ZIP_DEFLATED) as archive:
    for name in members:
        archive.write(ROOT / name, name)
with zipfile.ZipFile(target) as archive:
    assert archive.testzip() is None and archive.namelist() == members
    for name in members:
        assert archive.read(name) == (ROOT / name).read_bytes()
package = {
    'created_utc': now, 'revision': '0.22.1', 'sha256': sha(target),
    'members_sha256': {name: sha(ROOT / name) for name in members},
    'pdf_sha256': qa['pdf']['sha256'],
    'status': 'Seven-file archive; CRC and exact current member bytes verified',
    'arxiv_server_compile': 'Not performed', 'current_qa': visual['qa_record']
}
ap = ROOT / 'audit/arxiv_package_20260930.json'
ap.write_text(json.dumps(package, indent=2) + '\n', encoding='utf-8')
ap.with_suffix('.md').write_text(
    '# Current source package\n\n' + now + '\n\nThe seven-member source archive matches the reviewed manuscript source, bibliography, BBL and four figures byte for byte; CRC verified.\n\n'
    + 'Archive SHA-256: ' + package['sha256'] + '. PDF SHA-256: ' + package['pdf_sha256']
    + '.\n\nQA18 and all-page visual review passed. No arbitrary page cap applies. arXiv upload and server compilation were not performed.\n', encoding='utf-8')
record('Content-first source package synchronized', package)

before = (HERE / 'before/main.tex').read_text(encoding='utf-8')
after = (ROOT / 'main.tex').read_text(encoding='utf-8')
equations = lambda text: re.findall(r'\\begin\{equation\}.*?\\end\{equation\}', text, re.S)
tables = lambda text: re.findall(r'\\begin\{tabular\}.*?\\end\{tabular\}', text, re.S)
assert equations(before) == equations(after) and len(equations(after)) == 14
assert tables(before) == tables(after) and len(tables(after)) == 4
qa_source = (ROOT / 'scripts/full_manuscript_qa.py').read_text(encoding='utf-8')
assert '6 <= pages <= 14' not in qa_source
assert 'assert pages >= 1' in qa_source
assert 'assert len(rendered) == pages' in qa_source
review = {
    'created_utc': now, 'result': 'pass', 'decision': 'No upper page count or target; preserve clear scientific explanation and verify every actual page.',
    'user_direction': 'There is no need for a hard page cap; what matters is the content.',
    'main_tex_sha256': sha(ROOT / 'main.tex'), 'qa_script_sha256': sha(ROOT / 'scripts/full_manuscript_qa.py'),
    'pdf_sha256': qa['pdf']['sha256'], 'source_package_sha256': package['sha256'],
    'page_count': qa['pdf']['pages'], 'full_qa_groups': len(qa['checks']),
    'content_restored': 'Sec. 6.2 again explicitly separates the failed classifier control from structural significance and specifies a pair-grouped rerun on the same validation bank, plus three independent generator-training seeds.',
    'quality_checks_retained': 'Every-page render count, nonblank ink range, minimum visible margins, extractable text, complete citations, equations and LaTeX log checks remain in the full suite.',
    'preserved': 'All 14 numbered equations, four tabular bodies, figures, numerical results, data and scientific scope remain unchanged.',
    'historical_failure': 'QA15 failed solely under the superseded 14-page maximum; the original failed record remains intact as historical evidence.',
    'visual': visual['method'] + ' ' + visual['findings']
}
(HERE / 'review.json').write_text(json.dumps(review, indent=2) + '\n', encoding='utf-8')
(HERE / 'review.md').write_text(
    '# Content-first pagination review\n\n' + now + '\n\n'
    + review['decision'] + '\n\n' + review['content_restored'] + '\n\n'
    + review['quality_checks_retained'] + '\n\n' + review['visual'] + '\n\n'
    + review['preserved'] + '\n\n' + review['historical_failure']
    + '\n\nPDF SHA-256: ' + review['pdf_sha256'] + '.\n', encoding='utf-8')
record('Content-first manuscript review completed', review)
print('15-page visual record, exact source package and content-first review synchronized.')
