"""Seal the exact reviewed document and seven-file arXiv source package."""
from pathlib import Path
import json,hashlib,zipfile,subprocess,sys,platform
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
WORK=Path('C:/Users/Julia/OneDrive/Desktop/coding/ASIoP/Fast MC CBSC')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def twin(root,name,payload,body):
 p=root/'audit'/name;p.with_suffix('.json').write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8');p.with_suffix('.md').write_text(body,encoding='utf-8')
qa_path=ROOT/'audit/qa_series/physics_exposition_20261001/iteration_08.json'
qa=json.loads(qa_path.read_text());prior=json.loads((qa_path.parent/'iteration_07.json').read_text())
assert qa['result']=='pass' and len(qa['page_metrics'])==14 and len(qa['checks'])==19
changed=[n['page'] for p,n in zip(prior['page_metrics'],qa['page_metrics']) if p['sha256']!=n['sha256']]
assert changed==[3,9]
for page in qa['page_metrics']:
 image=ROOT/f"audit/qa_runs/physics_exposition_20261001/iteration_08/page-{page['page']:02d}.png"
 assert sha(image)==page['sha256']
notes={
 '1':'Abstract, central bound and introduction read; coherent scope and clean title/email without affiliation label.',
 '2':'Conditioning, stored energy, detector representation and Figure 1 read; unresolved physical mapping explicit.',
 '3':'Population and complete physical architecture read; revised caption and training/generation annotation directly reinspected in QA08.',
 '4':'Response, hurdle, cap, first-deposit distinction, activity and flow target/equations fully read.',
 '5':'Solver, longitudinal shares, count, graph and sampling equations read; physical roles and constraints clear.',
 '6':'Energy-sharing flow, decoder conservation scope and training procedure/loss read.',
 '7':'Checkpoint protocol, strengthened inequality, units/populations, uncertainty and classifier controls read.',
 '8':'Primary table and Figure 3 fully read; ECAL point, ratios and peak-deficit explanation legible; entire ratio range visible.',
 '9':'All/nonempty mean depths and Figure 4 directly reinspected in QA08; lower/upper bounds and legends readable.',
 '10':'Classifier failure, FP32 historic failure, activity example and limitations read without causal overclaim.',
 '11':'Limitations, computational scope, conclusion, availability, acknowledgment and AI declaration read; fit cleanly.',
 '12':'Appendix A settings, hashes, weights, calibration and historical test-use disclosure read.',
 '13':'Appendix B all bins, standard deviations, classifier seeds, algorithms and twin-split caveat read.',
 '14':'All 25 bibliography entries visible and legible; numbering/cross-references clean.'}
visual={'created_utc':datetime.now(timezone.utc).isoformat(),'result':'pass','series':'physics_exposition_20261001','iteration':8,'pdf_sha256':qa['pdf']['sha256'],'page_sha256':{str(p['page']):p['sha256'] for p in qa['page_metrics']},'review_method':'Direct full-page visual reading of QA07 pages 1-14; QA08 changed pages 3 and 9 directly reinspected, unchanged pages verified by image SHA-256; additional QA08 pages 10-14 also directly reinspected.','page_notes':notes,'scientific_scope':'Document and numerical evidence review; not physics validation.'}
twin(ROOT,'visual_review_finalization_20260930',visual,'# Current every-page visual review\n\nAll 14 pages read. Final QA08 pages 3 and 9 reinspected; the other page images match the inspected QA07 output. No clipping, illegible plots, orphan headings or unexplained stage semantics found. The exact PDF and per-page hashes are in the JSON twin.\n')
commands=[]
def run(args):
 result=subprocess.run(args,cwd=ROOT,capture_output=True,text=True,encoding='utf-8',errors='replace');commands.append({'argv':args,'returncode':result.returncode,'stdout_sha256':hashlib.sha256(result.stdout.encode()).hexdigest(),'stderr_sha256':hashlib.sha256(result.stderr.encode()).hexdigest()});assert result.returncode==0,result.stdout+result.stderr;print(result.stdout.strip());return result
run([sys.executable,'-X','utf8','scripts/write_build_audit.py'])
files=['main.tex','references.bib','main.bbl']+['figures/'+n for n in ['detector_geometry.png','generator_schematic.png','longitudinal_profile.png','support_summary.png']]
assert 'bbl format version 3.3' in (ROOT/'main.bbl').read_text()
dest=ROOT/'output/fast_mc_zdc_submission_source.zip'
with zipfile.ZipFile(dest,'w',compression=zipfile.ZIP_DEFLATED) as z:
 for name in files:z.write(ROOT/name,name)
with zipfile.ZipFile(dest) as z:
 assert z.testzip() is None and set(z.namelist())==set(files) and len(z.namelist())==7
 for name in files:assert z.read(name)==(ROOT/name).read_bytes()
package={'created_utc':datetime.now(timezone.utc).isoformat(),'revision':'0.19.0','sha256':sha(dest),'members_sha256':{n:sha(ROOT/n) for n in files},'pdf_sha256':qa['pdf']['sha256'],'status':'Seven-file source archive; CRC and exact bytes verified','arxiv_server_compile':'Not performed','current_qa':str(qa_path.relative_to(ROOT)),'guidance_checked':['https://info.arxiv.org/help/submit_tex.html','https://info.arxiv.org/help/faq/texlive.html']}
twin(ROOT,'arxiv_package_20260930',package,'# Current arXiv source package\n\nVersion 0.19.0; seven required files only, CRC and exact source/figure bytes verified. See JSON twin for all hashes. arXiv server compilation and upload have not been performed.\n')
p=ROOT/'output/arxiv_submission_notes.md';s=p.read_text(encoding='utf-8').replace('v0.18.0','v0.19.0').replace('audit/second_external_audit_response_20260930.md','audit/physics_exposition_response_20261001.md');p.write_text(s,encoding='utf-8')
final={'created_utc':datetime.now(timezone.utc).isoformat(),'revision':'0.19.0','status':'Manuscript revision and local submission-package QA complete; empirical limits remain','main_sha256':sha(ROOT/'main.tex'),'pdf_sha256':qa['pdf']['sha256'],'zip_sha256':sha(dest),'automated_check_groups':19,'visual_pages':14,'guard_tests':10,'current_qa':str(qa_path.relative_to(ROOT)),'failed_attempts':[1,2,3,4,5,6],'failed_attempt_resolution':'Label fit corrected; required semantic wording preserved; whitespace fixed; pagination corrected by layout and repetition edits. All original guards retained. Attempt 7 passed; final changed source passed attempt 8.','native_compile':'Two platform-directory initialization failures; no source diagnostics available from editor','local_build':'pdfLaTeX/Biber, all 19 check groups, exact source/PDF/figure/every-page binding passed','commands':commands,'environment':{'python':sys.version,'platform':platform.platform()},'new_event_or_test_data_access':False,'external_submission':False,'remaining':'Event/checkpoint recovery, production segmentation, paired structural intervals, threshold/graph/timing, solver and repeated-fit studies.','evidence':'physics_exposition_response_20261001.md; physics_exposition_20261001.json; physics_exposition_derived_20261001.json','graft_tokens_saved_estimate':19282}
body='# Physical architecture revision completed\n\nVersion 0.19.0: the physical observable and limitations of each architecture stage are explained. The within-run lower bound is 30.45 components (84.6%). Figure 3 includes ECAL and complete ratios; nonempty/all-event depth centroids are reported separately. Unsupported significance and guaranteed-conservatism claims were rejected.\n\nFinal complete suite: 19 groups passed; 14 pages visually reviewed; 10 synthetic release guards passed. Native editor compilation remains unavailable due to platform initialization; local LaTeX/Biber succeeds. The seven-file source ZIP matches reviewed source and figures. All failed attempts are preserved. No new empirical validation or external submission. See the JSON twin for exact identities.\n'
for root,name in [(ROOT,'physics_exposition_completion_20261001'),(WORK,'manuscript_physics_exposition_completion_20261001')]:
 twin(root,name,final,body)
 with (root/'logs.md').open('a',encoding='utf-8') as f:f.write('\n\n## 2026-10-01: physical-architecture manuscript revision completed\n\nFinal QA series physics_exposition_20261001 attempt 08: 19 groups, 14 pages, exact rendered-page review binding; 10 release guards passed. Packaged v0.19.0 with seven exact-byte source files. Native editor initialization failure remains disclosed. No physics validation or external submission. See audit/'+name+'.json for hashes, commands, failures and remaining work.\n')
print(json.dumps({'pdf_sha256':final['pdf_sha256'],'zip_sha256':final['zip_sha256'],'release':'0.19.0'},indent=2))
