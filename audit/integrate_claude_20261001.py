"""Adopt verified reader improvements without changing the experiment."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,shutil,re,sys,platform
ROOT=Path(__file__).resolve().parents[1]
WORK=Path('C:/Users/Julia/OneDrive/Desktop/coding/ASIoP/Fast MC CBSC')
REVIEW=Path('C:/Users/Julia/Desktop/coding/ASIoP/Fast MC CBSC/audit/manuscript_fresh_reader_claude_20261001.md')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def edit(name,pairs):
 p=ROOT/name;s=p.read_text(encoding='utf-8')
 for a,b in pairs:
  assert a in s,(name,a[:80]);s=s.replace(a,b)
 p.write_text(s,encoding='utf-8')
snapshot=ROOT/'audit/source_snapshots/claude_integration_20261001'
assert not snapshot.exists()
files=['main.tex','README.md','STATUS.md','CITATION.cff','references.bib','audit/current_qa_series.json','audit/finalization_20260930.json','audit/final_build_audit.json','audit/claim_register_20260922.json','audit/claim_register_20260922.md','audit/visual_review_finalization_20260930.json']
files += [str(p.relative_to(ROOT)) for d in ['scripts','figures','output'] for p in (ROOT/d).glob('*') if p.is_file()]
for n in files:
 d=snapshot/n;d.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(ROOT/n,d)
intake={'created_utc':datetime.now(timezone.utc).isoformat(),'revision':'0.20.0','status':'integration_in_progress','inputs':{'review':sha(REVIEW),'proposal_pdf':sha(ROOT/'proposals/claude_20261001/proposed_revision.pdf'),'proposal_source':sha(ROOT/'proposals/claude_20261001/main.tex')},'baseline_sha256':{n:sha(ROOT/n) for n in files},'environment':{'python':sys.version,'platform':platform.platform()},'commands':['Read entire 18-page proposal via pdftotext; inspect contact sheet and detailed figure pages','Read supplied fresh-reader audit and proposed figure source','Read historical evaluator source, aggregate report, static geometry and training history','git status, branch, remote, log; git fetch origin; HEAD...origin/main = 0 0','python -X utf8 audit/integrate_claude_20261001.py'],'graft':{'tokens_saved_estimate':16736,'legacy_hits':'Ignored; no legacy artifact used'},'external_sources':['https://arxiv.org/html/2406.12877v2'],'scope':'Existing aggregate evidence only; no new training, remote execution, test data or model changes'}
for root,name in [(ROOT,'claude_integration_20261001'),(WORK,'manuscript_claude_integration_20261001')]:
 (root/'audit'/f'{name}.json').write_text(json.dumps(intake,indent=2)+'\n',encoding='utf-8');(root/'audit'/f'{name}.md').write_text('# Claude proposal integration intake\n\n'+json.dumps(intake,indent=2)+'\n',encoding='utf-8')
 with (root/'logs.md').open('a',encoding='utf-8') as f:f.write('\n\n## 2026-10-01: final reader-proposal integration\n\nRead complete 18-page proposal and supplied audit; snapshot v0.19.0. Adopt verified physical exposition, geometry, observable illustration and paired normalized-response statistics. Preserve uncertainty boundaries, numerical guards and prior failures. GitHub update explicitly authorized; origin/main matches local HEAD before integration. See audit/'+name+'.json.\n')
# Reuse the peer's diagram implementations, with stored-coordinate wording and local output binding.
src=(ROOT/'proposals/claude_20261001/build_proposal_figures.py').read_text(encoding='utf-8')
src=src.replace('HERE = Path(__file__).resolve().parent\nROOT = HERE.parents[1]','HERE = Path(__file__).resolve().parent\nROOT = HERE.parent').replace('OUT = HERE / "figures"','OUT = ROOT / "figures"')
src=src.replace('"detector_layout.png"','"detector_geometry.png"').replace('"observable_definitions.png"','"support_summary.png"')
src=src.replace('channel position $z$ (m)','stored centroid $z$ (m)').replace('channel position $x$ (mm)','stored centroid $x$ (mm)').replace('positions per channel','positions per stored ID')
src=src.replace('label="$x=-0.025\\\\,z$"','label="coordinate guide"')
# Keep diagrams only; the proposal training curve is preserved in proposals/.
a=src.index('def plot_training_history()');b=src.index('def _strip(',a);src=src[:a]+src[b:]
src=src[:src.index('def main()')]
src=src.replace('"""Figures added or replaced by the 2026-10-01 proposed revision.\n\nReads only files already in the paper repository (static geometry and the\ntraining-history extract).  Writes into this proposal folder; the manuscript\nfigures under ``figures/`` are not touched.\n"""','"""Reader diagrams adapted from the preserved Claude proposal; static geometry and toy graph only."""')
(ROOT/'scripts/reader_figures.py').write_text(src,encoding='utf-8')
p=ROOT/'scripts/build_figures.py';s=p.read_text();a=s.index('def plot_geometry(') if 'def plot_geometry(' in s else s.index('def plot_detector_geometry(');b=s.index('\ndef ',a+4)
name=s[a:s.index('\n',a)];s=s[:a]+name+'\n    from reader_figures import plot_detector_layout\n    plot_detector_layout()\n\n'+s[b:]
a=s.index('def plot_support_summary(');b=s.index('\ndef ',a+4);s=s[:a]+'def plot_support_summary(report: dict) -> None:\n    from reader_figures import plot_observable_definitions\n    plot_observable_definitions()\n\n'+s[b:];p.write_text(s,encoding='utf-8')
edit('main.tex',[
 (r'\date{September 2026}',r'\date{October 2026}'),
 ('Detailed particle transport provides the reference calorimeter showers but can be computationally costly. Before detector reconstruction is considered, a surrogate can be tested against the spatial organization of its stored simulation deposits. Here, support means the set of stored channels with positive deposit; occupancy counts its members.',
  'At the Electron--Ion Collider, a zero-degree calorimeter (ZDC) measures neutral particles emitted close to the outgoing hadron beam. The cited SiPM-on-tile design uses hit energies and positions to reconstruct neutron energy and angle~\\cite{epiczdc}. A surrogate for detailed particle transport must therefore reproduce spatial organization as well as total energy. Here, support is the set of stored channels with positive deposit; occupancy counts its members.'),
 ('Hit-level graph networks have been used for energy and angular reconstruction in the cited ZDC design~\\cite{epiczdc}, motivating tests of spatial correlations. The present graph components are diagnostics; their effect on reconstruction is not measured.','The graph components below diagnose spatial structure; this study does not measure their effect on reconstruction.'),
 ('The stored ePIC ZDC sample has 400 electromagnetic-calorimeter (ECAL) IDs in layer 0 and 6,390 hadronic-calorimeter (HCAL) IDs in layers 1--64: 100 per layer through 63 and 90 in layer 64.',
  'The stored ePIC ZDC geometry has 400 electromagnetic-calorimeter (ECAL) IDs in layer 0 and 6,390 hadronic-calorimeter (HCAL) IDs in layers 1--64: 100 per layer through 63 and 90 in layer 64. The ECAL centroid grid has 30.3\\,mm horizontal pitch. Mean HCAL layer coordinates have median $z$ spacing 24.9\\,mm and span 1.57\\,m from first to last layer. The ECAL centroid lies at $z=35.73$\\,m in the stored frame (Fig.~\\ref{fig:geometry}); these coordinates alone do not identify its origin with the interaction point.'),
 ('For 2,400 HCAL IDs, two to four stable positions share one ID; their unweighted centroid defines the graph node (Fig.~\\ref{fig:geometry}).','For 2,400 HCAL IDs, two to four distinct positions share one ID; their unweighted centroid defines the graph node.'),
 ('Stored-ID geometry: ECAL layer 0, HCAL layer 1, and position multiplicity over all 6,790 IDs. The first bar contains 400 ECAL and 3,990 HCAL IDs. Centroids define model nodes; multiplicity does not verify physical readout ganging.',
  'Stored-ID centroids. Left: horizontal projection of all 65 layers, with a coordinate guide $x=-0.025z$; axes have different scales. Center and right: ECAL and first HCAL faces, colored by positions per ID. Centroids define graph nodes. The guide does not establish the production beam axis, and multiplicity does not establish electronic ganging.'),
 ('Only aggregate reports and static geometry are available for this reanalysis; the matching event arrays and checkpoint were not recovered locally. Thus exact run counts, paired structural intervals and new generation tests cannot be reconstructed here.',
  'This reanalysis uses the evaluation summary and static geometry. Per-event masks and energies were not included in that summary; exact run counts, paired structural intervals and threshold studies require a new event-level evaluation of the project checkpoint.'),
 ('The response stage separates zero','\\textbf{Stored response.} The response stage separates zero'),
 ('For a visible event, the model draws the first active layer','\\textbf{Layer activity.} For a visible event, the model draws the first active layer'),
 ('Both energy-allocation flows learn a velocity field','\\textbf{Energy allocation by flow matching.} Both energy-allocation flows learn a velocity field'),
 ('Given $(h_c,B_\\ell,A_\\ell)$','\\textbf{Channel counts.} Given $(h_c,B_\\ell,A_\\ell)$'),
 ('The support network uses channel geometry','\\textbf{Channel placement.} The support network uses channel geometry'),
 ('A second flow divides each layer budget','\\textbf{Channel energies.} A second flow divides each layer budget'),
 ('For an empty reference shower, the target and mask are zero. The centering removes a common log offset, leaving the relative layer shares that enter the later softmax. Floors of $10^{-8}$ and $10^{-12}\\GeV$ keep the operations finite; they are numerical conventions, not detector thresholds. Floored shares are altered; their frequency is unrecorded. Centering fixes the softmax offset: targets sum to zero, whereas base noise has an extra common-offset mode. No likelihood on that singular target plane is evaluated.',
  'For an empty reference shower, the target and mask are zero. Subtracting the mean fixes the common log offset that the softmax ignores. Gaussian noise can contain this offset, which final normalization removes. Floors of $10^{-8}$ and $10^{-12}\\GeV$ keep the operations finite; they alter small shares and are numerical conventions, not detector thresholds. Their activation frequency was not measured.'),
 ('Define $Q=m-R$, the component count beyond one per occupied-layer run. Writing',
  'Define $Q=m-R$, the component count beyond one per occupied-layer run (Fig.~\\ref{fig:support}). Writing'),
 ('The 95\\% percentile intervals for $W_1$ and the zero-deposit fraction difference use 1,000 bootstrap resamples, stratified by incident-energy bin and preserving matched pairs.',
  'The 95\\% percentile intervals for $W_1$, the zero-deposit fraction difference and the mean normalized response residual use 1,000 bootstrap resamples, stratified by incident-energy bin and preserving matched pairs.'),
 ('Table~\\ref{tab:energy_bins} gives binwise means, standard deviations and relative differences. Pooling the bin moments gives all-event standard deviations of 4.759 and 4.830\\,GeV for reference and generator. The paired covariance is unavailable, so neither significance of the 0.045\\,GeV mean difference nor a sampling-noise explanation of the binwise fluctuations is established.',
  'Table~\\ref{tab:energy_bins} gives binwise means and widths; the pooled standard deviations are 4.759 and 4.830\\,GeV. The mean paired residual $(T_{\\rm gen}-T_{\\rm ref})/\\Kinc$ is $2.94\\times10^{-5}$, with 95\\% bootstrap interval $[-8.51,9.34]\\times10^{-4}$, which includes zero. This tests a different, energy-normalized quantity from the 0.045\\,GeV mean difference; it does not supply that difference\'s paired covariance.'),
 ('Figure~\\ref{fig:support} bounds the within-run fragmentation.',
  'Mean energy in layers 57--64 is 17.85\\,MeV for the generator and 17.19\\,MeV for Geant4, about 0.4\\% of each total. This fixed-region average does not isolate the energy of the additional occupied layers or disconnected components.'),
 ('The all-event active-channel-count distribution has $W_1=58.68$ channels,',
  'The bound in Sec.~\\ref{sec:diagnostics} places the mean within-run excess between 30.45 and 37.14 components; at least 84.6\\% of the component increase cannot be explained by additional runs. The all-event active-channel-count distribution has $W_1=58.68$ channels,'),
 ('The evaluator timing includes topology and classifier tests; generation latency was not isolated.',
  'The evaluation took 3,442\\,s for 10,000 pairs. Its nonoverlapping timed analysis stages total 1,009\\,s, leaving 2,433\\,s (0.243\\,s per event) for generation, I/O and other untimed work; generation latency was not isolated.'),
 ('OpenAI Codex assisted with software and manuscript drafting, specification review, literature searches, and editing.',
  'OpenAI Codex assisted with software and manuscript drafting, specification review, literature searches, and editing. Anthropic Claude provided an additional manuscript review and revision proposal; selected text and figure designs were incorporated after verification.'),
 ])
# Replace the low-information bound plot by the peer's explicit observable schematic.
p=ROOT/'main.tex';s=p.read_text();s=s.replace('Graph fragmentation conditional on nonempty readout (9,907 Geant4 and 9,858 generated showers). Left: observed mean component counts $m$ (crosses) and allowed ranges of $Q=m-R$ (segments). Right: the allowed difference in mean $Q$ compared with the observed difference in mean $m$. Ranges use $1+\\mathbf 1_{G>0}\\leq R\\leq G+1$; they are algebraic bounds, not uncertainty intervals. All quantities use strictly positive deposits and the model graph.',
 'Definitions on an illustrative graph, not shower data. Left: active layers (filled), interior empty layers (hatched), first and last layers $F,L$, gap count $G$ and occupied runs $R$. Right: all four layers are active ($R=1$), but occupied channels form three components ($m=3$), so $Q=m-R=2$. Pale edges join adjacent nodes of this toy grid; the detector graph is defined in Sec.~\\ref{sec:data}.')
p.write_text(s,encoding='utf-8')
# Keep the current named series and every old attempt immutable.
marker={'series':'claude_integration_20261001','predecessor':'audit/qa_series/physics_exposition_20261001/iteration_08.json','predecessor_sha256':sha(ROOT/'audit/qa_series/physics_exposition_20261001/iteration_08.json'),'reason':'New revision integrating the independently reviewed proposal, with unchanged safety and scientific guards.'}
(ROOT/'audit/current_qa_series.json').write_text(json.dumps(marker,indent=2)+'\n')
for n in ['README.md','STATUS.md','CITATION.cff','scripts/full_manuscript_qa.py','scripts/write_build_audit.py']:
 edit(n,[('0.19.0','0.20.0')])
edit('CITATION.cff',[('date-released: 2026-09-30','date-released: 2026-10-01')])
for n in ['README.md','STATUS.md']:
 p=ROOT/n;s=p.read_text();s=s.replace('The matching event arrays and checkpoint were not recovered locally; exact runs, jointly nonempty statistics and new experiments remain unavailable to this reanalysis.','The present reanalysis uses the evaluation summary; exact runs, jointly nonempty statistics and threshold studies require a new event-level evaluation.');s+='\n\n## Final reader-proposal integration\n\nVersion 0.20.0 incorporates verified improvements from the Claude proposal: detector context and stored-coordinate dimensions, clearer stage labels, an illustration of gaps/runs/components, normalized paired-response intervals and deep-layer energy totals. Proposal claims of independent paired samples, threshold irrelevance and guaranteed classifier lower bounds are not adopted. See `audit/claude_integration_response_20261001.md`.\n';p.write_text(s)
p=ROOT/'audit/finalization_20260930.json';j=json.loads(p.read_text());j['current_revision']='0.20.0';j['current_main_tex_sha256']=sha(ROOT/'main.tex');j['superseding_scientific_review']='audit/claude_integration_response_20261001.md';p.write_text(json.dumps(j,indent=2)+'\n')
p=ROOT/'audit/claim_register_20260922.json';j=json.loads(p.read_text());j['current_revision']='0.20.0';j['current_reader_revision']='audit/claude_integration_response_20261001.md';p.write_text(json.dumps(j,indent=2)+'\n')
print('Reader integration source changes applied; full QA pending')
