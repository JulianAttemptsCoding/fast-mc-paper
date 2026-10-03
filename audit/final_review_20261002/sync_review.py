import json,re,shutil
from session import ROOT,HERE,record,sha
# Preserve the author's previously requested exact AI-disclosure wording.
p=ROOT/'main.tex';s=p.read_text(encoding='utf-8')
s=s.replace(' GPT-6 assisted with the final manuscript review.','')
p.write_text(s,encoding='utf-8')
for name in ['README.md','STATUS.md']:
    p=ROOT/name;s=p.read_text(encoding='utf-8').replace('records GPT-6 final-review assistance, and synchronizes','preserves the author-requested AI disclosure, and synchronizes')
    p.write_text(s,encoding='utf-8')
pointer=ROOT/'audit/finalization_20260930.json'
for name in ['finalization_20260930.json','finalization_20260930.md']:
    shutil.copy2(ROOT/'audit'/name,HERE/'before'/name)
d=json.loads(pointer.read_text(encoding='utf-8'))
previous=d['current_main_tex_sha256']
d['current_main_tex_sha256']=sha(ROOT/'main.tex')
d['followup_final_review_20261002']={'record':'audit/final_review_20261002/events.json','previous_source_sha256':previous,'scope':'Complete current source read; conditional independence and detector definitions clarified; equations and tables preserved. Exact author-requested AI disclosure retained.','status':'source_review_complete; final PDF QA pending'}
pointer.write_text(json.dumps(d,indent=2)+'\n',encoding='utf-8')
with (ROOT/'audit/finalization_20260930.md').open('a',encoding='utf-8') as f:
    f.write('\nThe current source pointer was refreshed after the full 2 October final review; prior pointer preserved in `audit/final_review_20261002/before/`. See that review\'s events twin for the preserved failed QA09 and correction. All equations/tables and author-requested AI disclosure are preserved.\n')
record('Stale review binding diagnosed and corrected',{'failed_qa':'audit/qa_series/mentor_send_20261002/iteration_09.json','failure':'Current-source review pointer remained at prior source hash; build and preceding scientific checks completed but full suite correctly rejected stale evidence.','correction':'Updated current review pointer after completing source review; preserved historical pointer and failed attempt. No guard changed.','disclosure':'Reverted unsolicited GPT-6 sentence to preserve documented author-requested GPT-5.6-Sol-only attribution. This session assistance is recorded here.','reference_fallbacks':{'calograph':'https://journals.aps.org/prd/abstract/10.1103/PhysRevD.110.072003','epiczdc':'https://www.sciencedirect.com/science/article/pii/S0168900225004140','fasterzdc':'https://www.sciencedirect.com/science/article/abs/pii/S0010465525004370'},'reference_outcome':'All 26 stored entries checked against primary bibliographic records (25 cited). Three initial Crossref 429s and invalid-query retry 400s preserved; publisher records resolve metadata.','prior_candidate_status':'Not released: stale evidence binding; superseded by corrected build.','source_sha256':sha(ROOT/'main.tex')})
