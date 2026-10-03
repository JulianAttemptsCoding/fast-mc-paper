"""Bind the surgical review and source package to the final QA17 PDF."""
import json
import re
import zipfile
from datetime import datetime, timezone
from session import ROOT, HERE, record, sha

qa_path = ROOT / 'audit/qa_series/mentor_send_20261002/iteration_17.json'
qa16 = json.loads((qa_path.parent / 'iteration_16.json').read_text(encoding='utf-8'))
qa = json.loads(qa_path.read_text(encoding='utf-8'))
assert qa['result'] == 'pass' and qa['full_suite'] is True
assert len(qa['checks']) == 22 and qa['pdf']['pages'] == 14
assert qa['pdf']['sha256'] == sha(ROOT / 'output/fast_mc_zdc_manuscript.pdf')
assert [(p['page'], p['sha256']) for p in qa['page_metrics']] == [
    (p['page'], p['sha256']) for p in qa16['page_metrics']]
now = datetime.now(timezone.utc).isoformat()
findings = {
    '1': 'Displayed title, author, abstract and introduction legible. Abstract identifies the kinetic-energy-only control and uses precise group-count wording.',
    '2': 'Target, geometry, condition equation and Figure 1 checked; no clipping or detached caption.',
    '3': 'Prior separate test-partition inspection is disclosed next to the no-test-events-in-this-analysis statement; Figure 2 checked.',
    '4': 'Response, activity and flow equations 2-6 remain legible and within margins.',
    '5': 'Equations 7-11, generation order and channel-placement account checked.',
    '6': 'Decoder/loss equations 12-13 and training protocol checked.',
    '7': 'Gap equation 14 and classifier control explicitly define incident kinetic energy alone; references and caveats legible.',
    '8': 'Table 1, response text and all Figure 3 labels/captions checked.',
    '9': 'Figure 4(c1) says last active layer, consistent with Table 1, surrounding prose and caption; panels and numbers legible.',
    '10': 'Graph, classifier and closure results and discussion opening checked; screening criterion wording consistent.',
    '11': 'Three independent generator-training seeds are distinguished from classifier seeds; detector/timing and conclusion opening legible.',
    '12': 'Conclusion continuation, availability, acknowledgments, AI disclosure and Table 2 checked.',
    '13': 'Appendix A/B, response bins and classifier-seed Table 4 checked; caption uses screening criterion of 0.65.',
    '14': 'All 25 references legible with complete identifiers and no overflow.'
}
visual = {
    'created_utc': now, 'result': 'pass', 'pdf_sha256': qa['pdf']['sha256'],
    'page_sha256': {str(p['page']): p['sha256'] for p in qa['page_metrics']},
    'method': 'Direct visual inspection of all fourteen QA16 rendered pages, followed by exact pixel-hash comparison of every QA17 page. QA17 differs only in PDF file metadata after a STATUS documentation change.',
    'qa_record': str(qa_path.relative_to(ROOT)).replace('\\', '/'),
    'page_findings': findings,
    'findings': 'No clipping, overlap, missing glyph, figure/caption mismatch, unresolved reference or unreadable label observed. Natural Conclusion continuation across pages 11-12 accepted.'
}
vp = ROOT / 'audit/visual_review_finalization_20260930.json'
vp.write_text(json.dumps(visual, indent=2) + '\n', encoding='utf-8')
vp.with_suffix('.md').write_text(
    '# Current complete visual review\n\n' + now + '\n\nPDF SHA-256: ' + visual['pdf_sha256']
    + '. All 14 pages directly inspected in QA16; every QA17 rendered page has the same pixel hash.\n\n'
    + '\n'.join('- Page ' + n + ': ' + finding for n, finding in findings.items())
    + '\n\n' + visual['findings'] + '\n', encoding='utf-8')
record('Final every-page visual review bound', visual)

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
    + '.\n\nQA17 and all-page visual review passed. arXiv upload and server compilation were not performed.\n',
    encoding='utf-8')
record('Source package synchronized', package)

before = (HERE / 'before/main.tex').read_text(encoding='utf-8')
after = (ROOT / 'main.tex').read_text(encoding='utf-8')
equations = lambda text: re.findall(r'\\begin\{equation\}.*?\\end\{equation\}', text, re.S)
tables = lambda text: re.findall(r'\\begin\{tabular\}.*?\\end\{tabular\}', text, re.S)
assert equations(before) == equations(after) and len(equations(after)) == 14
assert tables(before) == tables(after) and len(tables(after)) == 4
assert (ROOT / 'CITATION.cff').read_bytes() == (HERE / 'before/CITATION.cff').read_bytes()
assert (ROOT / 'README.md').read_text(encoding='utf-8').splitlines()[0][2:] in after.replace('\\\\', ' ')
review = {
    'created_utc': now, 'result': 'pass', 'manuscript_sha256': sha(ROOT / 'main.tex'),
    'pdf_sha256': qa['pdf']['sha256'], 'source_package_sha256': package['sha256'],
    'figure4_sha256': sha(ROOT / 'figures/support_summary.png'),
    'qa': 'QA17: 22 groups passed, 14 pages; all page pixels equal directly inspected QA16 pages',
    'corrections': [
        'Abstract and first methods use define the classifier control as incident kinetic energy alone.',
        'Figure 4(c1) says last active layer.',
        'Sec. 2.3 distinguishes this validation-only analysis from earlier separate inspection of nominal-test events, documented in Appendix A.',
        'Sec. 6.2 specifies three independent generator-training seeds; Appendix B classifier seeds remain distinct.',
        'Sec. 5.4 and Table 4 both say recorded screening criterion of 0.65.',
        'Abstract uses mean group count and similar aggregate means mask a hit-pattern discrepancy.'
    ],
    'metadata': 'Local PDF title, README title and CITATION.cff title/version 0.22.1 match. Public repository synchronization is recorded separately after push.',
    'preserved': 'All 14 numbered equations, four tabular bodies, data, training/checkpoint selection, figures other than the label, and numerical claims unchanged.',
    'failures': 'Three interrupted edit attempts from exact-match or line-ending assumptions and QA15 15-page overflow are retained in events and QA records; concise Sec. 6.2 wording resolved pagination. A failed optional inspection one-liner and console-encoding retry are logged.',
    'boundary': 'Document QC does not establish structural significance, detector reconstruction performance, generator speedup or physics validation.'
}
(HERE / 'review.json').write_text(json.dumps(review, indent=2) + '\n', encoding='utf-8')
(HERE / 'review.md').write_text(
    '# Mentor pre-submission surgical review\n\n' + now + '\n\n'
    + '\n'.join('- ' + item for item in review['corrections'])
    + '\n\n' + review['qa'] + '.\n\n' + review['preserved'] + '\n\n'
    + review['failures'] + '\n\n' + review['boundary'] + '\n\nPDF SHA-256: '
    + review['pdf_sha256'] + '.\n', encoding='utf-8')
record('Mentor surgical review completed', review)
print('QA17 visual binding, seven-member source package and mentor review recorded.')
