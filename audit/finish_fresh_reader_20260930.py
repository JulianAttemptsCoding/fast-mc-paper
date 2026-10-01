"""Bind the completed reading to already-built QA91; never compiles a PDF."""
import importlib.util
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('review', ROOT/'audit/fresh_reader_revision_20260930.py')
review=importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)
state=json.loads(review.AUDIT.read_text(encoding='utf-8'))
qa=json.loads((ROOT/'audit/iterations/iteration_91.json').read_text(encoding='utf-8'))
priorqa=json.loads((ROOT/'audit/iterations/iteration_90.json').read_text(encoding='utf-8'))
assert qa['result']=='pass' and qa['full_suite'] and qa['pdf']['pages']==14
assert qa['pdf']['sha256']==review.sha(ROOT/'output/fast_mc_zdc_manuscript.pdf')
old=(ROOT/'audit/source_snapshots/fresh_reader_20260930/main.tex').read_text(encoding='utf-8')
now=(ROOT/'main.tex').read_text(encoding='utf-8')
for pattern,n in [(r'\\begin\{equation\}.*?\\end\{equation\}',14),(r'\\begin\{tabular\}.*?\\end\{tabular\}',4)]:
    blocks=re.findall(pattern,old,re.S)
    assert len(blocks)==n and blocks==re.findall(pattern,now,re.S)
for name in ('scripts/full_manuscript_qa.py','scripts/build_figures.py','references.bib','data/reports/dicos-f-02_epoch90.json','data/provenance/source_evidence.json'):
    assert review.sha(ROOT/name)==state['input_sha256'][name], name
changed=[b['page'] for a,b in zip(priorqa['page_metrics'],qa['page_metrics']) if a['sha256']!=b['sha256']]
assert changed==[6,7], changed
visual={
 'schema_version':1, 'result':'pass', 'reviewed_utc':datetime.now(timezone.utc).isoformat(),
 'pdf_sha256':qa['pdf']['sha256'], 'page_sha256':{str(p['page']):p['sha256'] for p in qa['page_metrics']},
 'method':'Every QA90 page (1-14) directly read and visually inspected. QA91 changed pages 6 and 7 directly read and inspected; the remaining twelve final page PNGs are byte-identical to QA90. All QA91 PDF text reread in page order, including appendices and references.',
 'directly_reviewed_pages_by_iteration':{'87':list(range(1,15)),'90':list(range(1,15)),'91':[6,7]},
 'previous_exact_visual_record':'audit/source_snapshots/fresh_reader_20260930/visual_review_finalization_20260930.json',
 'layout_failures':[],
 'observations':{'figures':'Four figures legible, correct color semantics and retained dimensions; captions state sample/role/limits.',
                 'equations':'Fourteen equations legible and unchanged; flow time, masks, budgets and graph roles interpreted in prose.',
                 'tables':'Four numerical tables unchanged, units and populations explicit.',
                 'pagination':'Concise captions restore 14 pages. Final training paragraph is wholly on page 6; evaluation begins page 7.',
                 'scientific_scope':'Descriptive pilot, failed classifier screening, fixed-tolerance exceedance, and missing evidence all retained.'},
 'scientific_status':'Document review only; no physics validation',
 'native_editor_compilation':{'result':'platform_error','message':'Unable to find standard directories for platform','source_unchanged':True,'editor_kept_open':True}}
for name in ('audit/visual_review_fresh_reader_20260930.json','audit/visual_review_finalization_20260930.json'):
    p=ROOT/name
    p.write_text(json.dumps(visual,indent=2)+'\n',encoding='utf-8')
    p.with_suffix('.md').write_text('# Final every-page visual review\n\nQA91 PDF SHA256: '+qa['pdf']['sha256']+'\n\n'+visual['method']+'\n\nNo clipping, overlap, illegible equations/figures or orphaned headings found. Native editor compilation remains unverified because its compiler returned a platform-directory error. Existing repository build and document QA passed.\n',encoding='utf-8')

commands=[]
def run(cmd,cwd):
    result=subprocess.run(cmd,cwd=cwd,text=True,capture_output=True,encoding='utf-8',errors='replace')
    commands.append({'argv':cmd,'cwd':str(cwd),'returncode':result.returncode,'stdout':result.stdout,'stderr':result.stderr})
    print(result.stdout or result.stderr)
    if result.returncode:
        state['status']='verification_failed'
        state['final_commands']=commands
        review.save(state,{'summary':'Final binding/guard command failed; no delivery declared.', 'command':cmd})
        raise SystemExit(result.returncode)

testnames=['test_current_exact_binding','test_changed_source_rejected','test_changed_pdf_rejected','test_changed_figure_manifest_rejected','test_partial_visual_review_rejected','test_failed_latest_suite_rejected']
run([sys.executable,'-m','unittest',*[f'test_qa_guards.ReleaseBindingTests.{n}' for n in testnames]],ROOT/'scripts')
run([sys.executable,'scripts/write_build_audit.py'],ROOT)
run(['git','diff','--check'],ROOT)

state['full_readings']=[
 {'number':1,'artifact':'Baseline main.tex, all lines 1-486 plus references.bib','focus':'Fresh-reader argument and definitions','result':'Identified missing first-use explanations and provenance certainty mismatch.'},
 {'number':2,'artifact':'Baseline QA87 pages 1-14','focus':'Every-page visual and prose reading','result':'Verified original colors; identified caption-purpose improvements; no baseline visual defect.'},
 {'number':3,'artifact':'First-revision QA88 full PDF text; middle pages 6-9 retrieved separately after output truncation','focus':'End-to-end explanatory logic after edits','result':'Improved definitions; tightened verbosity and next-step causal wording. QA page-count failure retained.'},
 {'number':4,'artifact':'QA90 pages 1-14','focus':'Complete rendered reading after pagination fix','result':'No visual defects; refined nominal effective batch and floored-share language.'},
 {'number':5,'artifact':'Final main.tex lines 1-486; bibliography unchanged from fully read baseline','focus':'Complete source reading against section purposes and inference limits','result':'No new actionable editorial inconsistency.'},
 {'number':6,'artifact':'QA91 PDF text pages 1-14, with final changed pages 6 and 7 inspected','focus':'Complete final reader pass including declarations, appendices and references','result':'No new actionable editorial inconsistency; scientific gaps remain explicitly unresolved.'}
]
state['focused_checks']=[
 {'topic':'Section purpose','evidence':'Every section/subsection mapped in fresh_reader_assessment_20260930.md','result':'Descriptive case study succeeds; full reproducibility and validation incomplete.'},
 {'topic':'First-use terminology','evidence':'Support, occupancy, ganging, component, reference-star definitions','result':'Clarified in source.'},
 {'topic':'Architecture and physical meaning','evidence':'Generation order, conditional context, attention, graph and decoder prose','result':'Distinguished learned dependencies from particle transport.'},
 {'topic':'All fourteen equations','evidence':'Equation-purpose map and exact block comparison','result':'Equations unchanged; floor qualification corrected.'},
 {'topic':'Dimensions and exact/numerical distinctions','evidence':'GeV/mm, sampled-budget identities, midpoint time update, batch-dependent residual criterion','result':'No new numerical/physical claim.'},
 {'topic':'Populations and estimands','evidence':'10,000 conditions; 9,907/9,858 nonempty subsets; pilot/canonical partitions','result':'Nonempty selection and fixed-condition limits explicit.'},
 {'topic':'All four figures','evidence':'Direct baseline/final raster inspection and caption review','result':'Purpose and uncertainty limits clarified; pixels unchanged.'},
 {'topic':'All four tables and reported arithmetic','evidence':'QA90/91 full evidence checks and exact table-block comparison','result':'Preserved and verified against retained aggregates.'},
 {'topic':'Graph confounding','evidence':'G/R example, m>=R, component interpretation','result':'No unsupported independent lateral-fragmentation or causal claim.'},
 {'topic':'Historical provenance','evidence':'Calibration proposal, source/config/checkpoint hashes, runtime caveats and test-use disclosure','result':'Main-text certainty aligned with appendix.'},
 {'topic':'Literature scope','evidence':state['external_checks'],'result':'Primary-source spot checks; no exhaustive new literature audit claimed.'},
 {'topic':'Conclusion and presentation','evidence':'Complete final readings, QA91 renders and unchanged guard checks','result':'Conclusion bounded; layout passes; native editor platform error disclosed.'}
]
state['failed_attempts'].extend(['QA88 compiled 15 pages and failed unchanged maximum-14-page guard.', 'QA89 still compiled 15 pages and failed unchanged maximum-14-page guard.', 'Native compile_latex_document failed before source diagnostics: Unable to find standard directories for platform.'])
state['qa']={'successful_iterations':[90,91],'failed_iterations':[88,89],'check_groups':len(qa['checks']),'pages':14,'binding_guard_tests_passed':6,'exact_release_binding':'pass','native_editor_compilation':visual['native_editor_compilation']}
state['final_commands']=commands
state['operations_index']={
 'initial_reads':['Get-Content docs/IMPLEMENTATION_GUIDE.md (complete, missing output ranges 440..620 and 618..672 recovered)','Get-Content docs/FOCUSED_OPERATING_RULES.md; Get-Content docs/GRAFT_SETUP.md; git status --short','graft check','graft ask "manuscript paper source figures build review scientific results" --source','Read project manuscript_finalization, prefinal_review and mentor_manuscript audit Markdown','Read PDF SKILL.md; Get-Item both candidate paper paths; attempted Get-Content paper AGENTS.md','Get-ChildItem paper root; git status --short; read README and final_build_audit','Read paper build.ps1, STATUS, finalization and visual audits; rg symbol/assertion locations in QA and release scripts','Read full main.tex and references.bib; read mathematical/model exposition audits','Get-Command python,pdflatex,pdftoppm; python runtime/library version probe','rg --files runtime for mark_artifact_operation_started.mjs; read exhibition/visual_layout.json'],
 'render_inspections':visual['directly_reviewed_pages_by_iteration'],
 'authoring':['PDF mark_artifact_operation_started.mjs --operation-kind edit --expected-output-count 1 --output-format pdf (exit 0)','apply_patch and python audit/fresh_reader_revision_20260930.py edit','apply_patch and python audit/tighten_fresh_reader_20260930.py','apply_patch concise figure captions','apply_patch final floor/batch wording; README/STATUS pointers','apply_patch fresh_reader_assessment_20260930.md','Update finalization current-source hash with prior exact record snapshotted'],
 'full_build_commands':'Exact argv, outputs and return codes preserved in audit/iterations/iteration_88.json through iteration_91.json; builds preceded latest editor-only user instruction.',
 'text_reads':['pdftotext -layout output/fast_mc_zdc_manuscript.pdf audit/fresh_reader_first_revision.txt','pdftotext -layout output/fast_mc_zdc_manuscript.pdf audit/fresh_reader_second_revision.txt','pdftotext -layout output/fast_mc_zdc_manuscript.pdf audit/fresh_reader_final_text.txt','Get-Content of full first-revision text plus separately retrieved pages 6-9; final source read 1-242 and 243-486; final PDF text read pages 1-7 then 8-14'],
 'app_tools':['load_workspace_dependencies','open_in_codex existing main.tex (queued)','compile_latex_document existing main.tex (platform error)'],
 'web_tools':'Primary URLs in external_checks; initial search had no matching return for two arXiv queries, corrected by direct open.',
 'logging':'Each meaningful edit, failure, correction and verification appended using audit/fresh_reader_revision_20260930.py event to both logs.md files.'}
state['graft']={'freshness':'reported OK but graph advertised legacy matches; not relied upon','query_count':1,'reported_tokens_saved':26664}
state['unchanged']={'equations':14,'numerical_tables':4,'guard_script':state['input_sha256']['scripts/full_manuscript_qa.py'],'experiment_data_and_settings':True,'figure_builder':state['input_sha256']['scripts/build_figures.py']}
state['output_sha256']={name:review.sha(ROOT/name) for name in ['main.tex','output/fast_mc_zdc_manuscript.pdf','README.md','STATUS.md','audit/fresh_reader_assessment_20260930.md','audit/final_build_audit.json','audit/visual_review_fresh_reader_20260930.json','audit/iterations/iteration_88.json','audit/iterations/iteration_89.json','audit/iterations/iteration_90.json','audit/iterations/iteration_91.json','audit/fresh_reader_revision_20260930.py','audit/tighten_fresh_reader_20260930.py','audit/finish_fresh_reader_20260930.py']}
state['operating_rule_sha256']={name:review.sha(review.PROJECT/name) for name in ['AGENTS.md','docs/IMPLEMENTATION_GUIDE.md','docs/FOCUSED_OPERATING_RULES.md','docs/GRAFT_SETUP.md']}
state['status']='review_complete; repository_build_verified; native_editor_preview_unverified'
review.save(state,{'summary':'Six complete readings and twelve focused checks finished. QA90/91 PASS (16 groups); final 14-page PDF and source/figures visually bound; six existing binding guard tests PASS. All equations/tables, data and guards unchanged. Native editor compiler platform error remains. No new raw/test access, training, publication or separate build after latest user instruction.', 'command':'python audit/finish_fresh_reader_20260930.py'})

handoff={'schema_version':1,'created_utc':datetime.now(timezone.utc).isoformat(),'status':state['status'],'version':'0.16.0 local working revision','paper_root':str(ROOT),'purpose':'Repeated fresh-reader assessment and clarity revision for experimental HEP/computational physics', 'pdf':{'path':str(ROOT/'output/fast_mc_zdc_manuscript.pdf'),'sha256':qa['pdf']['sha256'],'pages':14},'source':{'path':str(ROOT/'main.tex'),'sha256':review.sha(ROOT/'main.tex')},'whole_manuscript_readings':6,'focused_checks':12,'qa':state['qa'],'scientific_scope':'Descriptive one-seed development-bank case study. Structural uncertainty, robustness, exact historical runtime and isolated timing remain unavailable.','records':{name:{'path':str(ROOT/name),'sha256':review.sha(ROOT/name)} for name in ['audit/fresh_reader_review_20260930.json','audit/fresh_reader_review_20260930.md','audit/fresh_reader_assessment_20260930.md','audit/final_build_audit.json','audit/visual_review_fresh_reader_20260930.json','audit/iterations/iteration_91.json']},'dashboard_refresh':'Not applicable: manuscript copyedit only; no changed run, metric or accepted-best checkpoint.'}
target=review.PROJECT/'audit/manuscript_fresh_reader_20260930.json'
target.write_text(json.dumps(handoff,indent=2)+'\n',encoding='utf-8')
summary='# Current manuscript fresh-reader handoff\n\n'+handoff['status']+'\n\nSource: '+handoff['source']['path']+'\n\nPDF SHA256: '+qa['pdf']['sha256']+'\n\nSix complete readings, twelve focused checks, full QA90/91 and six binding tests passed. All fourteen final pages visually covered. Equations and four numerical tables unchanged. QA88/89 page-limit failures preserved.\n\nNative editor compiler failed with: Unable to find standard directories for platform. The editor remains open. No alternate build/export after the latest editor-only instruction.\n\nFull section/equation/figure/table assessment: '+str(ROOT/'audit/fresh_reader_assessment_20260930.md')+'\n\nScientific status remains a descriptive pilot; missing uncertainty/robustness/runtime/timing evidence remains missing. No physics validation or publication.\n'
target.with_suffix('.md').write_text(summary,encoding='utf-8')
oldpointer=review.PROJECT/'audit/manuscript_finalization_20260930.json'
previous=json.loads(oldpointer.read_text(encoding='utf-8'))
updated={**handoff,'previous_handoff':previous,'superseded_by_current_review':'audit/manuscript_fresh_reader_20260930.json'}
oldpointer.write_text(json.dumps(updated,indent=2)+'\n',encoding='utf-8')
oldpointer.with_suffix('.md').write_text(summary+'\nPrevious finalization and disclosure handoffs are preserved in the JSON previous_handoff object.\n',encoding='utf-8')
with (review.PROJECT/'logs.md').open('a',encoding='utf-8') as stream:
    stream.write('\nCurrent manuscript handoff synchronized: audit/manuscript_fresh_reader_20260930.json SHA256 '+review.sha(target)+'; main finalization pointer now references QA91 while preserving prior handoff.\n')
print('Fresh-reader review finalized; existing source/PDF binding verified. Native editor platform error disclosed.')
