"""Bind the completed HEP framing review to the current manuscript artifacts."""
import json
import re
import zipfile
from datetime import datetime, timezone
from session import ROOT, HERE, record, sha

qa_path = ROOT / 'audit/qa_series/mentor_send_20261002/iteration_14.json'
qa = json.loads(qa_path.read_text(encoding='utf-8'))
assert qa['result'] == 'pass' and qa['full_suite'] is True
assert qa['pdf']['sha256'] == sha(ROOT / 'output/fast_mc_zdc_manuscript.pdf')
assert len(qa['page_metrics']) == 14
now = datetime.now(timezone.utc).isoformat()
findings = {
    '1': 'Two-line neutron-shower title, author, self-contained abstract and complete introduction legible; caveats and metric definition present.',
    '2': 'Condition equation, raw-deposit target, detector definitions, Figure 1 axes/legend/caption and graph counts legible within margins.',
    '3': 'Split and population explanation, generator overview and Figure 2 arrows, symbols and training/generation distinction checked.',
    '4': 'Equations 2-6 and response, activity and flow-matching explanations legible; equation numbers and denominators intact.',
    '5': 'Equations 7-11, solver caveat, channel count and placement explanations checked; no clipping.',
    '6': 'Decoder equation 12, loss equation 13, training/selection account and evaluation introduction checked.',
    '7': 'Equation 14, contiguous-segment bound, separate denominators, uncertainty scope and classifier-control caveats checked.',
    '8': 'Table 1 numbers/units/rounding and Figure 3 axes, ratios, legends and caption checked; caption remains with figure.',
    '9': 'Response uncertainty, empty counts and longitudinal results checked; all illustrative and aggregate panels of Figure 4 clearly distinguished.',
    '10': 'Graph results, classifier and closure limitations and opening Discussion interpretation checked; hypotheses are explicitly distinguished from measured effects.',
    '11': 'Proposed activity and placement controls, robustness limits, detector relevance and timing checked; Conclusion heading has two following lines before natural continuation.',
    '12': 'Conclusion continuation, availability, acknowledgment, author-requested AI disclosure, Appendix A identities and Table 2 legible.',
    '13': 'Calibration/split provenance, Appendix B and Tables 3-4 checked; all classifier seeds and failed-control caveats retained.',
    '14': 'All 25 references legible on one page; names, titles, identifiers, hyperlinks and wrapping checked against the unchanged bibliography.'
}
visual = {
    'created_utc': now, 'result': 'pass', 'pdf_sha256': qa['pdf']['sha256'],
    'page_sha256': {str(p['page']): p['sha256'] for p in qa['page_metrics']},
    'method': 'Direct visual inspection of all fourteen final 110-dpi rendered page PNGs, displayed individually in five batches.',
    'qa_record': str(qa_path.relative_to(ROOT)).replace('\\', '/'),
    'page_findings': findings,
    'findings': 'No clipping, overlap, missing glyphs, detached captions or unreadable figure labels observed. Natural paragraph continuations, including Conclusion across pages 11-12, accepted. All equations, four figures, four tables and references inspected.'
}
vp = ROOT / 'audit/visual_review_finalization_20260930.json'
vp.write_text(json.dumps(visual, indent=2) + '\n', encoding='utf-8')
vp.with_suffix('.md').write_text(
    '# Current complete visual review\n\n' + now + '\n\nPDF SHA-256: ' + visual['pdf_sha256']
    + '. All 14 pages of QA14 directly inspected.\n\n'
    + '\n'.join('- Page ' + p + ': ' + x for p, x in findings.items())
    + '\n\n' + visual['findings'] + '\n', encoding='utf-8')
record('Final every-page visual review passed', visual)

members = ['main.tex', 'references.bib', 'main.bbl', 'figures/detector_geometry.png',
           'figures/generator_schematic.png', 'figures/longitudinal_profile.png', 'figures/support_summary.png']
target = ROOT / 'output/fast_mc_zdc_submission_source.zip'
assert (HERE / 'before' / target.name).exists(), 'Initial source package backup required'
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
    'pdf_sha256': visual['pdf_sha256'], 'status': 'Seven-file archive; CRC and exact current source bytes verified',
    'arxiv_server_compile': 'Not performed', 'current_qa': visual['qa_record']
}
ap = ROOT / 'audit/arxiv_package_20260930.json'
ap.write_text(json.dumps(package, indent=2) + '\n', encoding='utf-8')
ap.with_suffix('.md').write_text(
    '# Current source package\n\n' + now + '\n\n'
    + 'The seven-member source archive matches the reviewed main source, bibliography, BBL and four figures byte for byte; CRC verified.\n\n'
    + 'Archive SHA-256: ' + package['sha256'] + '. PDF SHA-256: ' + package['pdf_sha256']
    + '.\n\nQA14 and all-page visual review passed. arXiv upload and server compilation were not performed.\n', encoding='utf-8')
record('Final source package synchronized', package)

tex = (ROOT / 'main.tex').read_text(encoding='utf-8')
before = (HERE / 'before/main.tex').read_text(encoding='utf-8')
equations = lambda text: re.findall(r'\\begin\{equation\}.*?\\end\{equation\}', text, re.S)
assert equations(tex) == equations(before) and len(equations(tex)) == 14
assert (ROOT / 'references.bib').read_bytes() == (HERE / 'before/references.bib').read_bytes()
abstract = tex.split('\\begin{abstract}')[1].split('\\end{abstract}')[0].strip()
review = {
    'created_utc': now, 'result': 'pass', 'scope': 'Research-informed title, abstract, discussion and conclusion, with whole-paper regression and visual review.',
    'main_tex_sha256': sha(ROOT / 'main.tex'), 'pdf_sha256': visual['pdf_sha256'],
    'source_package_sha256': package['sha256'], 'research_sources': json.loads((HERE / 'research.json').read_text()),
    'abstract_whitespace_word_count': len(abstract.split()),
    'sections': {
        'title': 'Names generated neutron showers and the pilot ZDC scope; synchronized with PDF metadata, CITATION.cff and README.',
        'abstract': 'States target, method, conditions, key numerical differences and their limitations; defines graph groups and the classifier metric without claiming reconstruction performance.',
        'discussion': 'Leads with the observation; separates the algebraic bound, mechanistic hypotheses, distinguishing tests, robustness limitations, detector relevance and timing.',
        'conclusion': 'States the bounded validation lesson and necessary follow-up; retains one-seed reused-bank status and unmeasured reconstruction effects.'
    },
    'preserved': ['All 14 displayed equations unchanged in this HEP framing revision', 'Bibliography unchanged in this revision', 'Numerical evidence, figures, tables, thresholds, model and data unchanged', 'All QA guards unchanged'],
    'QA_history': [
        'QA11 passed all 22 groups before final wording/layout refinement.',
        'QA12 and QA13 failed the existing 14-page maximum. Both failed QA records and command outputs retained. A fitz import failed during optional quarantine inspection; installed pdfinfo used instead.',
        'Original QA12 PDF was overwritten before retention. QA12 source-hash evidence remains. The reconstructed source under quarantined_qa12 does not match its hash and is not exact provenance. Its copied PDF is QA13; README and event log explicitly correct that identity.',
        'QA13 failed PDF/source retained under quarantined_qa13. Concise wording and natural page flow corrected the overflow without changing fonts, figure sizes, numerical evidence or guards.',
        'QA14 passed all 22 groups; all 14 final pages directly inspected.'
    ],
    'scientific_boundary': 'Document QA and literature-informed editing do not establish physics validation or independent HEP peer review. Structural intervals, repeated training seeds, threshold/graph studies, comparable generation timing and reconstructed neutron performance remain unmeasured as disclosed.'
}
(HERE / 'review.json').write_text(json.dumps(review, indent=2) + '\n', encoding='utf-8')
(HERE / 'review.md').write_text(
    '# Final HEP framing review\n\n' + now + '\n\n'
    + 'Title, abstract, discussion and conclusion revised using six primary guidance/research sources listed in [research.md](research.md).\n\n'
    + '\n'.join('- **' + k.title() + ':** ' + v for k, v in review['sections'].items())
    + '\n\nFinal abstract: ' + str(review['abstract_whitespace_word_count']) + ' whitespace-delimited words. '
    + 'All 14 displayed equations and the bibliography are unchanged in this revision.\n\n'
    + '\n'.join('- ' + item for item in review['QA_history'])
    + '\n\n' + review['scientific_boundary']
    + '\n\nPDF SHA-256: ' + review['pdf_sha256'] + '.\n', encoding='utf-8')
record('HEP framing review complete', review)
print('Visual record, exact seven-member source archive and HEP review report synchronized.')
