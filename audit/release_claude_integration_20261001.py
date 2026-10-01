"""Seal the exact reviewed document and seven-file arXiv source package."""
from pathlib import Path
import json,hashlib,zipfile,subprocess,sys,platform
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
WORK=Path('C:/Users/Julia/OneDrive/Desktop/coding/ASIoP/Fast MC CBSC')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def twin(root,name,payload,body):
 p=root/'audit'/name;p.with_suffix('.json').write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8');p.with_suffix('.md').write_text(body,encoding='utf-8')
qa_path=ROOT/'audit/qa_series/claude_integration_20261001/iteration_04.json'
qa=json.loads(qa_path.read_text());prior=json.loads((qa_path.parent/'iteration_03.json').read_text())
assert qa['result']=='pass' and len(qa['page_metrics'])==14 and len(qa['checks'])==20
changed=[n['page'] for p,n in zip(prior['page_metrics'],qa['page_metrics']) if p['sha256']!=n['sha256']]
assert changed==[], changed
for page in qa['page_metrics']:
 image=ROOT/f"audit/qa_runs/claude_integration_20261001/iteration_04/page-{page['page']:02d}.png"
 assert sha(image)==page['sha256']
notes={
 '1':'Title, abstract, physics motivation and scope read; clean layout.',
 '2':'Stored-coordinate geometry figure and caveats read; axes, captions and dimensions legible.',
 '3':'Population definitions and architecture diagram read; physical stages and dependencies clear.',
 '4':'Response, activity and centered-log target read; equations and units checked.',
 '5':'Solver, layer allocation, counts, graph and support sampling read; physical limits explicit.',
 '6':'Channel energy, budget closure and teacher-forced training read; no incident-energy conservation claim.',
 '7':'Checkpoint choice, observables, deterministic bound and paired intervals read; controls disclosed.',
 '8':'Primary results table and energy profiles read; ratios and section compensation clear.',
 '9':'Normalized paired interval, fixed-region energy and illustrative support figure read; count definitions accurate.',
 '10':'Classifier and numerical failures, activity null and causal limits read.',
 '11':'Limitations, timing scope, conclusion, availability and acknowledgments read; no affiliation label.',
 '12':'AI declaration, provenance and calibration table read; scientific responsibility and runtime limits explicit.',
 '13':'Energy-bin means/widths, classifier seeds and evaluator details read; tables legible.',
 '14':'Classifier partition caveat and all 25 references read; links, margins and typography clear.'}
visual={'created_utc':datetime.now(timezone.utc).isoformat(),'result':'pass','series':'claude_integration_20261001','iteration':4,'pdf_sha256':qa['pdf']['sha256'],'page_sha256':{str(p['page']):p['sha256'] for p in qa['page_metrics']},'review_method':'Direct full-page visual reading of Claude integration QA03 pages 1-14. All fourteen QA04 rendered pages independently hash-identical to those reviewed images.','page_notes':notes,'scientific_scope':'Document and numerical evidence review; not physics validation.'}
twin(ROOT,'visual_review_finalization_20260930',visual,'# Current every-page visual review\n\nAll 14 QA03 pages read. All QA04 page images match those reviewed images by SHA-256. No clipping, illegible plots, orphan headings or unexplained stage semantics found. The exact PDF and per-page hashes are in the JSON twin.\n')
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
package={'created_utc':datetime.now(timezone.utc).isoformat(),'revision':'0.20.0','sha256':sha(dest),'members_sha256':{n:sha(ROOT/n) for n in files},'pdf_sha256':qa['pdf']['sha256'],'status':'Seven-file source archive; CRC and exact bytes verified','arxiv_server_compile':'Not performed','current_qa':str(qa_path.relative_to(ROOT)),'guidance_checked':['https://info.arxiv.org/help/submit_tex.html','https://info.arxiv.org/help/faq/texlive.html']}
twin(ROOT,'arxiv_package_20260930',package,'# Current arXiv source package\n\nVersion 0.20.0; seven required files only, CRC and exact source/figure bytes verified. See JSON twin for all hashes. arXiv server compilation and upload have not been performed.\n')
p=ROOT/'output/arxiv_submission_notes.md';s=p.read_text(encoding='utf-8').replace('v0.19.0','v0.20.0').replace('audit/physics_exposition_response_20261001.md','audit/claude_integration_response_20261001.md');p.write_text(s,encoding='utf-8')
final={'created_utc':datetime.now(timezone.utc).isoformat(),'revision':'0.20.0','status':'Manuscript revision and local submission-package QA complete; empirical limits remain','main_sha256':sha(ROOT/'main.tex'),'pdf_sha256':qa['pdf']['sha256'],'zip_sha256':sha(dest),'automated_check_groups':20,'visual_pages':14,'guard_tests':10,'current_qa':str(qa_path.relative_to(ROOT)),'failed_attempts':[1],'failed_attempt_resolution':'Attempt 1: semantic wording guard failed and PDF had 15 pages. Restored precise wording, reduced repetition and geometry figure height. Attempts 2, 3 and 4 passed at 14 pages. No guard relaxed.','native_compile':'Two platform-directory initialization failures; no source diagnostics available from editor','local_build':'pdfLaTeX/Biber, all 20 check groups, exact source/PDF/figure/every-page binding passed','commands':commands, 'publication_integrity':'Added .gitattributes * -text because core.autocrlf=true would otherwise change source/evidence bytes on Git publication; verify every staged blob against working bytes.','environment':{'python':sys.version,'platform':platform.platform()},'new_event_or_test_data_access':False,'external_submission':False,'remaining':'New event-level evaluation with verified identities, production segmentation, paired structural intervals, threshold/graph/timing, solver and repeated-fit studies.','evidence':'claude_integration_response_20261001.md; claude_integration_20261001.json; claude_reader_derived_20261001.json','graft_tokens_saved_estimate':16736}
body='# Reader proposal integration completed\n\nVersion 0.20.0: the physical observable and limitations of each architecture stage are explained. The within-run lower bound is 30.45 components (84.6%). Figure 3 includes ECAL and complete ratios; nonempty/all-event depth centroids are reported separately. Unsupported significance and guaranteed-conservatism claims were rejected.\n\nFinal complete suite: 20 groups passed; 14 pages visually reviewed; 10 synthetic release guards passed. Native editor compilation remains unavailable due to platform initialization; local LaTeX/Biber succeeds. The seven-file source ZIP matches reviewed source and figures. All failed attempts are preserved. No new empirical validation or external submission. See the JSON twin for exact identities.\n'
for root,name in [(ROOT,'claude_integration_completion_20261001'),(WORK,'manuscript_claude_integration_completion_20261001')]:
 twin(root,name,final,body)
 with (root/'logs.md').open('a',encoding='utf-8') as f:f.write('\n\n## 2026-10-01: reader-proposal manuscript revision completed\n\nFinal QA series claude_integration_20261001 attempt 04: 20 groups, 14 pages, exact rendered-page review binding; 10 release guards passed. Packaged v0.20.0 with seven exact-byte source files. Native editor initialization failure remains disclosed. No physics validation or external submission. See audit/'+name+'.json for hashes, commands, failures and remaining work.\n')
print(json.dumps({'pdf_sha256':final['pdf_sha256'],'zip_sha256':final['zip_sha256'],'release':'0.20.0'},indent=2))
