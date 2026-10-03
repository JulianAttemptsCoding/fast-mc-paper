import re,shutil
from session import ROOT,HERE,record,sha
backup=HERE/'before'
backup.mkdir(exist_ok=False)
for name in ['main.tex','references.bib','README.md','STATUS.md','audit/final_build_audit.json','audit/visual_review_finalization_20260930.json','audit/visual_review_finalization_20260930.md','audit/arxiv_package_20260930.json','audit/arxiv_package_20260930.md']:
    p=ROOT/name
    if p.exists(): shutil.copy2(p,backup/p.name)
changes={
 'main.tex':[
  ('A proposed ePIC SiPM-on-tile design','A proposed ePIC silicon-photomultiplier (SiPM)-on-tile design'),
  ('no MIP-scale threshold or additional time cut is applied','no minimum-ionizing-particle (MIP) threshold or additional time cut is applied'),
  ('layer 0 as nominally LYSO','layer 0 as nominally lutetium--yttrium oxyorthosilicate (LYSO)'),
  ('its stochastic shower histories are independent.','its stochastic shower histories are independent at that fixed condition.'),
  ('they are statistical comparisons, not particle or energy transport.','they are learned feature transformations, not particle or energy transport.'),
  ("literature searches, and editing. The author takes responsibility", "literature searches, and editing. GPT-6 assisted with the final manuscript review. The author takes responsibility")
 ],
 'references.bib':[
  ('author={Buckley, Matthew R. and Krause, Claudius and Pang, Ian and Shih, David}', 'author={Buckley, Matthew R. and Pang, Ian and Shih, David and Krause, Claudius}'),
  ('@misc{rectifiedflow,','@inproceedings{rectifiedflow,'),
  ('year={2022}, eprint={2209.03003}, archivePrefix={arXiv}', 'booktitle={International Conference on Learning Representations},\n year={2023}, eprint={2209.03003}, archivePrefix={arXiv}'),
  ('title={{CaloPointFlow II}: Generating Calorimeter Showers as Point Clouds}', 'title={{CaloPointFlow II} Generating Calorimeter Showers as Point Clouds}')
 ]}
for name,items in changes.items():
    p=ROOT/name;text=p.read_text(encoding='utf-8')
    for old,new in items:
        assert text.count(old)==1,(name,old,text.count(old))
        text=text.replace(old,new)
    p.write_text(text,encoding='utf-8')
before=(backup/'main.tex').read_text(encoding='utf-8');after=(ROOT/'main.tex').read_text(encoding='utf-8')
for env in ['equation','tabular']:
    pattern=r'\\begin\{'+env+r'\}.*?\\end\{'+env+r'\}'
    assert re.findall(pattern,before,re.S)==re.findall(pattern,after,re.S),env
note='\n## Comprehensive final review, 2 October 2026\n\nThe complete title-to-references review defines SiPM, MIP and LYSO, makes paired-shower independence explicitly conditional, clarifies graph messages, records GPT-6 final-review assistance, and synchronizes three bibliography entries with primary publication records. All 14 numbered equations, four numerical tables, figure definitions and scientific results are preserved. See `audit/final_review_20261002/events.{json,md}` for commands, source hashes, failures and the final full-suite/every-page review. The exact current release remains bound by `audit/final_build_audit.json`.\n'
for name in ['README.md','STATUS.md']:
    with (ROOT/name).open('a',encoding='utf-8') as f:f.write(note)
record('Editorial and bibliography corrections applied',{'changes':changes,'equations_preserved':14,'tables_preserved':4,'hashes':{name:sha(ROOT/name) for name in ['main.tex','references.bib','README.md','STATUS.md']},'reference_sources':['https://journals.aps.org/prd/abstract/10.1103/PhysRevD.109.033006','https://iclr.cc/virtual/2023/papers.html','https://github.com/gnobitab/RectifiedFlow','https://arxiv.org/abs/2403.15782'],'status':'Awaiting complete build, aggregate checks and visual verification.'})
