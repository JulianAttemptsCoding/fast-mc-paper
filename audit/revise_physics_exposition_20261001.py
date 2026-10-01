"""Evidence-preserving manuscript revision; no event data or model edits."""
from pathlib import Path
import hashlib,json,shutil,sys,platform
from datetime import datetime,timezone
ROOT=Path(__file__).resolve().parents[1]
WORK=Path('C:/Users/Julia/OneDrive/Desktop/coding/ASIoP/Fast MC CBSC')
AUDIT=Path('C:/Users/Julia/.codex/attachments/f064f65e-cf5c-4b4f-b8b1-a8d62722f8f6/Pasted text.txt')
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def edit(name,pairs):
 p=ROOT/name;s=p.read_text(encoding='utf-8')
 for old,new in pairs:
  assert old in s,(name,old[:90]);s=s.replace(old,new)
 p.write_text(s,encoding='utf-8')
snapshot=ROOT/'audit/source_snapshots/physics_exposition_20261001'
assert not snapshot.exists()
files=['main.tex','README.md','STATUS.md','CITATION.cff','audit/finalization_20260930.json','audit/finalization_20260930.md','audit/claim_register_20260922.json','audit/claim_register_20260922.md','audit/final_build_audit.json','audit/component_bound_20260930.json','audit/component_bound_20260930.md','audit/visual_review_finalization_20260930.json']
files += [str(p.relative_to(ROOT)) for folder in ['scripts','figures','output'] for p in (ROOT/folder).glob('*') if p.is_file()]
for name in files:
 dest=snapshot/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/name,dest)
record={'created_utc':datetime.now(timezone.utc).isoformat(),'revision':'0.19.0','status':'revision_in_progress','input_audit_sha256':sha(AUDIT),'input_sha256':{n:sha(ROOT/n) for n in files},'environment':{'python':sys.version,'platform':platform.platform()},'scope':'Aggregate manuscript revision only; no event/test access, training, frozen-config changes or external submission','navigation':'graft check current; ask contained legacy hits which were excluded from evidence; current source corroborated independently','commands':['Read supplied audit and complete current manuscript; inspect aggregate/model/evaluator sources','python -X utf8 audit/revise_physics_exposition_20261001.py'],'research_sources':['https://arxiv.org/html/2608.12795v1','https://arxiv.org/html/2406.12877v2','https://proceedings.mlr.press/v97/kool19a.html']}
def twin(root,name,payload):
 p=root/'audit'/name;p.parent.mkdir(exist_ok=True,parents=True);p.with_suffix('.json').write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8');p.with_suffix('.md').write_text('# Physical architecture and third external audit\n\n'+json.dumps(payload,indent=2)+'\n',encoding='utf-8')
for root,name in [(ROOT,'physics_exposition_20261001'),(WORK,'manuscript_physics_exposition_20261001')]:
 twin(root,name,record)
 with (root/'logs.md').open('a',encoding='utf-8') as f:f.write('\n\n## 2026-10-01: physical architecture and third audit intake\n\nSnapshot preserves v0.18.0. Strengthen run bound using gap fractions; clarify readout-stage physics; reject unsupported significance/conservatism claims. No new physics validation. See audit/'+name+'.json for commands, hashes, sources and environment.\n')
edit('main.tex',[
 ('conditional Jaccard error','Jaccard co-activation error'),('they coexist with later deposits','they coexist with deeper deposits'),
 ('The checkpoint fails the recorded classifier screen.','The high-level classifier AUROC of 0.775 exceeds the recorded screening maximum of 0.65.'),
 ('The central question is whether similar raw-deposit and occupancy means also imply similar longitudinal organization.','Hit-level graph networks have been used for energy and angular reconstruction in the cited ZDC design~\\cite{epiczdc}, motivating tests of spatial correlations. The present graph components are diagnostics; their effect on reconstruction is not measured. We ask whether similar raw-deposit and occupancy means also imply similar longitudinal organization.'),
 (' Generating hit counts before locations also has precedents in point-cloud models~\\cite{caloclouds2,calopointflow}.',''),
 ('The generator builds a shower at three physical scales (Fig.~\\ref{fig:architecture}). It first draws whether any readout deposit is visible and how much energy is deposited in total. It next determines which layers are active and allocates that total among them. Finally, within each active layer it draws a channel count, selects those channels, and divides the layer budget among them. A downstream stage uses the sampled outputs of upstream stages, so agreement in a final observable depends on the full cascade rather than on its last network alone.',
  'The generator builds a shower at three levels of stored readout: event response, longitudinal allocation, and channel deposits (Fig.~\\ref{fig:architecture}). It separates how much energy is stored ($T$), where along the detector it appears ($F,\\mathbf A,\\mathbf B$), and how it is distributed transversely ($\\mathbf K,\\mathbf S,\\mathbf Y$). Counts precede positions, as in point-cloud models~\\cite{caloclouds2,calopointflow}. These observables describe a shower outcome; the cascade does not simulate individual interactions or particle trajectories.'),
 ('At inference, the incident four-vector is the only event input.','At inference, the incident four-vector is the only event input. The embedding $h_c$ encodes energy and direction for a fixed geometry; its learned coordinates have no assigned physical observables. Random draws represent conditional shower variability, not added electronics noise.'),
 ('The response stage separates empty readout from the size of a nonempty deposit.','The response stage separates zero from nonzero stored response (a hurdle model), then describes fluctuations in its magnitude. Here visibility means nonzero deposited energy, not optical visibility or the probability of an inelastic interaction.'),
 ('The activity mask may therefore contain empty layers between active ones. The budget flow subsequently distributes $T$ only across active layers.',
  '$F$ marks the first stored deposit, not necessarily the first inelastic interaction. The mask $\\mathbf A$ specifies occupied depth and gaps; its factorization omits residual co-activation at fixed $(h_c,T,F)$. The budget flow then assigns the longitudinal energy profile and ECAL/HCAL partition on that support.'),
 ('This fixes occupancy, not the positions of selected channels or a minimum deposit per channel.','This models readout multiplicity at a given layer energy. It does not specify particle multiplicity, footprint area, channel positions or a minimum deposit.'),
 ('A graph message can make a score sensitive to nearby readouts, but selection remains a separate stochastic step.','Messages let scores depend on nearby readouts; they are statistical comparisons, not particle or energy transport. The support $S_\\ell$ determines transverse placement and therefore graph connectivity. Selection is a separate stochastic step.'),
 ('Selecting the top $K_\\ell$ enforces the requested count exactly, but imposes no adjacency or connectivity constraint.','Gumbel-top-$K$ samples $K_\\ell$ distinct channels without replacement. It enforces the count but imposes no adjacency or connectivity constraint.'),
 ('A second flow divides each layer budget among its selected channels.','A second flow divides each layer budget among its selected channels, describing energy concentration and fluctuations on fixed support. It can change energy-weighted shape and centroids, but cannot relocate deposits or repair disconnected support in exact arithmetic.'),
 ("These are accounting identities for the model's sampled readout budget.","These identities conserve the sampled readout budget, not the incident neutron's full energy. Energy in unrecorded material and leakage are not generated; positivity and closure alone do not establish a physical shower."),
 ('Since $1\\leq R\\leq G+1$, separately averaged nonempty samples obey',
  'Writing $I=\\mathbf 1_{G>0}$ gives $1+I\\leq R\\leq G+1$: any interior gap requires at least two occupied runs. Thus $\\overline m-1-\\overline G\\leq\\overline Q\\leq\\overline m-1-f$, where $f=\\overline I$ is the nonempty gap fraction. Subtracting the separate sample bounds gives'),
 (r'\Delta\overline m-\overline G_{\rm gen}\leq\Delta\overline Q',r'\Delta\overline m-\overline G_{\rm gen}+f_{\rm ref}\leq\Delta\overline Q'),
 (r'\leq\Delta\overline m+\overline G_{\rm ref},',r'\leq\Delta\overline m+\overline G_{\rm ref}-f_{\rm gen},'),
 ('Ranges follow from $1\\leq R\\leq G+1$;','Ranges use $1+\\mathbf 1_{G>0}\\leq R\\leq G+1$;'),
 ('29.92','30.45'),('83.2','84.6'),('22.42','21.89'),
 ('The zero support-mask mismatch records equality of selected channels and positive FP32 deposits in this sample.','The zero support-mask mismatch verifies that FP32 decoding created no selected-but-empty channels in this sample; such losses would bias support metrics.'),
 ('The available 0.344\\,s per event includes topology and classifier tests; generation latency was not isolated.','Generation speed is outside the measured scope: the recorded evaluator timing includes topology and classifier tests.'),
 ('The bound rules out empty-layer separations as a sufficient graph description;','Similar mean energy and occupancy therefore do not imply matched longitudinal or graph structure in this example. The bound rules out empty-layer separations as a sufficient graph description;'),
 ])
# Compute the sharpened values directly, avoiding rounded-input arithmetic.
r=json.loads((ROOT/'data/reports/dicos-f-02_epoch90.json').read_text())
f=r['activity']['truth']['gap_fraction'];fg=r['activity']['generated']['gap_fraction']
lo=35.97033279861814-r['activity']['generated']['mean_gaps']+f
hi=35.97033279861814+r['activity']['truth']['mean_gaps']-fg
assert round(lo,2)==30.45,(lo,hi)
edit('scripts/component_bounds.py',[
 ("out[short]={'m':m,'G':g,'Q_low':max(0,m-1-g),'Q_high':m-1}","f=report['activity'][name]['gap_fraction']\n        out[short]={'m':m,'G':g,'f':f,'Q_low':max(0,m-1-g),'Q_high':m-1-f}"),
 ("assert math.isclose(b['delta_Q_low'],29.92153994002613,abs_tol=1e-9)",f"assert math.isclose(b['delta_Q_low'],{lo!r},abs_tol=1e-9)\n    assert math.isclose(b['delta_Q_high'],{hi!r},abs_tol=1e-9)\n    assert 29.92153994002613 < b['delta_Q_low'] < b['delta_Q_high'] < 38.0724827935712"),
 ('==83.2','==84.6'),('assert 1<=R<=G+1','assert 1+int(G>0)<=R<=G+1'),('<=Q<=m-1','<=Q<=m-1-int(G>0)'),("r'83.2\\%', '29.92','52.34','22.42'","r'84.6\\%', '30.45','52.34','21.89'"),
 ('1 <= R <= G+1. Q=m-R therefore lies between max(0,m-1-G) and m-1.','1 + I[G>0] <= R <= G+1. Q=m-R therefore lies between max(0,m-1-G) and m-1-I[G>0].'),
 ])
edit('scripts/build_figures.py',[
 ('5 input features','energy + direction'),('encoding", "learned"','embedding", "learned"'),('event response','stored response'),('layer activity','occupied depth'),('layer budgets','depth energy'),('channel counts','hit multiplicity'),('channel set','hit placement'),('share flow','energy sharing'),
 ("'lower bound\\n29.92'","f\"lower bound\\n{b['delta_Q_low']:.2f}\""),("'upper bound\\n38.07'","f\"upper bound\\n{b['delta_Q_high']:.2f}\""),("'Lower bound = 83.2% of Δm'","f\"Lower bound = {100*b['lower_fraction']:.1f}% of Δm\""),
 ('ax.set_xlim(26,42)','ax.set_xlim(27,41)'),
 ])
# A new namespace preserves all 99 historical attempts and the 1..99 guard.
marker={'series':'physics_exposition_20261001','predecessor':'audit/iterations/iteration_99.json','predecessor_sha256':sha(ROOT/'audit/iterations/iteration_99.json'),'reason':'New source revision after the closed historical QA series; all historical attempts retained.'}
(ROOT/'audit/current_qa_series.json').write_text(json.dumps(marker,indent=2)+'\n')
edit('scripts/full_manuscript_qa.py',[
 ('COMMAND_RECORDS: list[dict] = []','COMMAND_RECORDS: list[dict] = []\nfrom qa_series import series_paths\nITERATION_DIR, RENDER_ROOT = series_paths(ROOT)'),
 ('    paths += sorted((ROOT / "scripts").glob("*.py"))','    paths += [ROOT / "audit/current_qa_series.json"] if (ROOT / "audit/current_qa_series.json").exists() else []\n    paths += sorted((ROOT / "scripts").glob("*.py"))'),
 ('ROOT / "audit" / "qa_runs" / f"iteration_{iteration:02d}"','RENDER_ROOT / f"iteration_{iteration:02d}"'),
 ('out_dir = ROOT / "audit" / "iterations"','out_dir = ITERATION_DIR'),
 ('record_path = ROOT / "audit/iterations"','record_path = ITERATION_DIR'),('failed_path = ROOT / "audit/iterations"','failed_path = ITERATION_DIR'),
 ('    assert 1 <= args.iteration <= 99','    assert 1 <= args.iteration <= 99\n    ITERATION_DIR.mkdir(parents=True, exist_ok=True)'),
 ('"iteration": iteration,','"iteration": iteration,\n        "series_directory": str(ITERATION_DIR.relative_to(ROOT)), '),
 ('audit/qa_runs/iteration_{iteration:02d}/page','{(RENDER_ROOT / f"iteration_{iteration:02d}" / "page").relative_to(ROOT).as_posix()}'),
 ('0.18.0','0.19.0')])
edit('scripts/write_build_audit.py',[
 ('release_source_hashes, sha256','release_source_hashes, sha256, ITERATION_DIR'),("(ROOT / 'audit/iterations').glob",'ITERATION_DIR.glob'),('0.18.0','0.19.0'),('83.2%','84.6%'),('29.92','30.45')])
for name in ['README.md','STATUS.md','CITATION.cff']:
 edit(name,[('0.18.0','0.19.0')])
edit('README.md',[('83.2%','84.6%'),('`audit/iterations/`: historical and current build checks;','`audit/iterations/` and `audit/qa_series/`: preserved historical and current build checks;')])
edit('STATUS.md',[('1 <= R <= G+1 implies delta mean Q >= delta mean m - mean G_generator = 29.9215 components, at least 83.18%','1 + I[G>0] <= R <= G+1 implies delta mean Q >= delta mean m - mean G_generator + f_reference = %.4f components, at least %.2f%%'%(lo,100*lo/35.97033279861814))])
for name in ['README.md','STATUS.md']:
 with (ROOT/name).open('a',encoding='utf-8') as h:h.write('\n\n## Physical interpretation and third audit\n\nVersion 0.19.0 explains the physical observable represented by each architecture stage, distinguishes stored-energy closure from incident-energy conservation, and uses gap fractions to sharpen the component bound. See `audit/physics_exposition_response_20261001.md`. The active QA series is named in `audit/current_qa_series.json`; historical attempts are immutable.\n')
p=ROOT/'audit/claim_register_20260922.json';j=json.loads(p.read_text());j['current_revision']='0.19.0';j['claim']=f'On the pilot development bank, the within-run component excess is at least {lo:.8f}, or {100*lo/35.97033279861814:.5f}% of the mean component excess. This is an algebraic sample bound, not an uncertainty or detector-performance claim.'
def update(v):
 if isinstance(v,dict):
  for k,x in v.items():
   if k=='within_run_component_excess_lower_bound':v[k]=lo
   elif isinstance(x,(dict,list)):update(x)
 elif isinstance(v,list):
  for x in v:update(x)
update(j);p.write_text(json.dumps(j,indent=2)+'\n')
edit('audit/claim_register_20260922.md',[('29.92154 (83.18%',f'{lo:.5f} ({100*lo/35.97033279861814:.2f}%'),('Current v0.18.0','Current v0.19.0')])
p=ROOT/'audit/finalization_20260930.json';j=json.loads(p.read_text());j['current_main_tex_sha256']=sha(ROOT/'main.tex');j['current_revision']='0.19.0';j['superseding_scientific_review']='audit/physics_exposition_response_20261001.md';p.write_text(json.dumps(j,indent=2)+'\n')
record['bound']={'lower':lo,'upper':hi,'lower_percent':100*lo/35.97033279861814};record['output_main_sha256']=sha(ROOT/'main.tex')
for root,name in [(ROOT,'physics_exposition_20261001'),(WORK,'manuscript_physics_exposition_20261001')]:twin(root,name,record)
print(json.dumps(record['bound'],indent=2))
