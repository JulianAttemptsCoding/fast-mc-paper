import json, re, shutil, zipfile
from datetime import datetime, timezone
from session import ROOT,HERE,record,sha
qa_path=ROOT/'audit/qa_series/mentor_send_20261002/iteration_10.json'
qa=json.loads(qa_path.read_text(encoding='utf-8'))
assert qa['result']=='pass' and qa['full_suite'] is True
assert qa['pdf']['sha256']==sha(ROOT/'output/fast_mc_zdc_manuscript.pdf')
assert len(qa['page_metrics'])==14
now=datetime.now(timezone.utc).isoformat()
page_findings={
 '1':'Title, author/contact, date, abstract, introduction and condition equation: legible, pilot scope explicit, no clipping.',
 '2':'Target, detector definitions, channel semantics, geometry dimensions, Figure 1 axes/legend and graph counts checked.',
 '3':'Population continuation, conditional independence, model overview and Figure 2 generation/conditioning labels checked.',
 '4':'Response mixture, caps, layer activity, log-share target and masked flow objective checked; equation numbers 2-6 clear.',
 '5':'Solver, layer budgets, counts, messages, Gumbel selection and share target checked; equations 7-11 within margins.',
 '6':'Decoder identities, losses, calibration provenance, stage order and selection protocol checked; equations 12-13 legible.',
 '7':'Gap identity, segment/component bounds, denominators, bootstrap scope, W1 definition and classifier caveats checked.',
 '8':'Table 1 numbers/units/rounding, response text and Figure 3 scales/ratios/legend/caption checked.',
 '9':'Response uncertainty, empty counts, longitudinal observations and all Figure 4 illustrative/data panels checked.',
 '10':'Component bounds, transverse summaries, edge co-occupancy, failed classifier screen, closure tolerances and discussion checked.',
 '11':'Activity/support hypotheses, robustness limits, threshold timing scope, cost accounting, conclusion and availability checked.',
 '12':'Acknowledgment, exact author-requested AI disclosure, source/checkpoint identities, Table 2 and test-history accounting checked.',
 '13':'Appendix B, Tables 3-4, all classifier seeds and split caveats checked; references 1-5 legible.',
 '14':'References 6-25 checked for titles, names, dates, venues, identifiers and line wrapping; corrected references 18,20,25 present.'}
visual={'created_utc':now,'result':'pass','pdf_sha256':qa['pdf']['sha256'],
 'page_sha256':{str(p['page']):p['sha256'] for p in qa['page_metrics']},
 'method':'Direct visual inspection of all fourteen current 110-dpi page PNGs, individually displayed in four batches. All prose, numbered equations, table bodies/captions and figure panels reviewed.',
 'qa_record':str(qa_path.relative_to(ROOT)).replace('\\','/'),'page_findings':page_findings,
 'findings':'No clipping, overlap, missing glyphs, broken labels/citations, unreadable figure text or detached captions observed. Natural paragraph continuations and page breaks accepted.'}
vp=ROOT/'audit/visual_review_finalization_20260930.json'
vp.write_text(json.dumps(visual,indent=2)+'\n',encoding='utf-8')
md='# Current complete visual review\n\n'+now+'\n\nPDF SHA-256: `'+visual['pdf_sha256']+'`. All 14 pages of QA10 directly inspected.\n\n'+'\n'.join('- Page '+p+': '+x for p,x in page_findings.items())+'\n\n'+visual['findings']+'\n'
vp.with_suffix('.md').write_text(md,encoding='utf-8')
record('Complete final PDF visual review passed',visual)
members=['main.tex','references.bib','main.bbl','figures/detector_geometry.png','figures/generator_schematic.png','figures/longitudinal_profile.png','figures/support_summary.png']
target=ROOT/'output/fast_mc_zdc_submission_source.zip'
shutil.copy2(target,HERE/'before'/target.name)
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
    for name in members:z.write(ROOT/name,name)
with zipfile.ZipFile(target) as z:
    assert z.testzip() is None
    assert z.namelist()==members
    for name in members:assert z.read(name)==(ROOT/name).read_bytes()
archive={'created_utc':now,'revision':'0.22.1','sha256':sha(target),
 'members_sha256':{name:sha(ROOT/name) for name in members},'pdf_sha256':visual['pdf_sha256'],
 'status':'Seven-file archive; CRC and exact current source bytes verified','arxiv_server_compile':'Not performed',
 'current_qa':visual['qa_record']}
ap=ROOT/'audit/arxiv_package_20260930.json'
ap.write_text(json.dumps(archive,indent=2)+'\n',encoding='utf-8')
ap.with_suffix('.md').write_text('# Current source package\n\n'+now+'\n\n`output/fast_mc_zdc_submission_source.zip` contains the seven required files with current reviewed source, bibliography, BBL and figures. CRC and member bytes verified; all member hashes are in the JSON twin.\n\nArchive SHA-256: `'+archive['sha256']+'`. PDF SHA-256: `'+visual['pdf_sha256']+'`.\n\nLocal QA10 and all-page visual review passed. arXiv upload and server compilation were not performed.\n',encoding='utf-8')
record('Current source archive synchronized',archive)
tex=(ROOT/'main.tex').read_text(encoding='utf-8')
blocks=[]
for m in re.finditer(r'\S[\s\S]*?(?=\n\s*\n|\Z)',tex):
    text=m.group().strip()
    if not text:continue
    import hashlib
    blocks.append({'start_line':tex.count('\n',0,m.start())+1,'sha256':hashlib.sha256(text.encode()).hexdigest(),'opening':text[:110],'disposition':'Reviewed in complete source reading and corresponding final rendered page.'})
coverage={'created_utc':now,'source_sha256':sha(ROOT/'main.tex'),'pdf_sha256':visual['pdf_sha256'],'blocks':blocks,
 'sections':['Title and abstract','Introduction','Simulation target and study population','Generator and training procedure','Evaluation protocol','Results','Discussion','Conclusion','Availability, acknowledgments and AI use','Appendix A','Appendix B','References'],
 'equations':re.findall(r'\\label\{(eq:[^}]+)\}',tex),
 'figure_labels':re.findall(r'\\label\{(fig:[^}]+)\}',tex),
 'table_labels':re.findall(r'\\label\{(tab:[^}]+)\}',tex),
 'claims':'Descriptive one-seed pilot, reused validation; separate nonempty samples; algebraic bounds not intervals; no physics validation, speedup or reconstructed-performance claim.',
 'remaining_research':'Structural paired intervals, repeated model seeds, threshold/graph scans, event-level reconstruction and comparable generation timing remain disclosed research limits, not silently completed by this editorial review.'}
(HERE/'coverage.json').write_text(json.dumps(coverage,indent=2)+'\n',encoding='utf-8')
(HERE/'coverage.md').write_text('# Complete review coverage\n\nAll twelve manuscript areas, '+str(len(blocks))+' source blocks, 14 equations, four figures, four tables and 25 cited references reviewed. Primary metadata for all 26 bibliography entries was checked, including the uncited retained entry. Three bibliography entries corrected.\n\nThe initial full QA09 correctly failed on a stale current-source audit pointer. After review-pointer correction, QA10 passed all 22 groups and all 14 pages were inspected directly. No assertion or threshold was weakened.\n\n'+coverage['claims']+'\n\n'+coverage['remaining_research']+'\n',encoding='utf-8')
print('All-page visual record and seven-member source archive synchronized; coverage saved.')
