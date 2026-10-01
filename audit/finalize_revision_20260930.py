"""Apply the evidence-bound v0.16 manuscript revision; no experiment changes."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def replace_once(text, old, new):
    assert text.count(old) == 1, (old, text.count(old))
    return text.replace(old, new)


tex_path = ROOT / 'main.tex'
tex = tex_path.read_text(encoding='utf-8')
tex = replace_once(tex, r'\author{Julian Juan}', r'\author{Julian Juan\\[3pt]\small Independent researcher\\\small\href{mailto:juliansjuan08@gmail.com}{juliansjuan08@gmail.com}}')
tex = replace_once(tex, 'has only 0.25 more active layers', 'has 0.25 more active layers')
tex = replace_once(tex, 'All shower comparisons use 10,000 incident conditions', 'The primary shower comparison uses 10,000 incident conditions')
tex = replace_once(tex, 'Green stages are conditional flows and the purple stage is the deterministic energy decoder.', r'Green stages generate layer budgets $B_\ell$ and channel-energy logits $r_{\ell i}$ through conditional flows; the purple stage converts the latter to deposits $Y_{\ell i}$ with the deterministic decoder.')
tex = replace_once(tex, 'A weight-sensitivity study would test whether these bounds affect shower structure.', r'The bounds apply before normalization of the weights to mean one. Appendix~\ref{app:reproducibility} records the calibration values and their provenance limits. A weight-sensitivity study would test whether these bounds affect shower structure.')
tex = replace_once(tex, 'Its different event sample precludes a direct comparison between the two batteries.', r'Its different event sample precludes a direct comparison between the two batteries. Appendix~\ref{app:additional} gives each classifier seed and the recovered evaluator specification.')
tex = replace_once(tex, 'Agreement after averaging over incident energy therefore does not imply comparable agreement within each energy bin.', r'Agreement after averaging over incident energy therefore does not imply comparable agreement within each energy bin. Table~\ref{tab:energy_bins} provides the bin counts, means, and relative differences.')
tex = replace_once(tex, 'The present revision is being circulated for mentor review.', r'This manuscript is version 0.16.0; the accompanying \texttt{audit/final\_build\_audit.json} binds the PDF, figures, and source files by SHA-256.')
tex = replace_once(tex, 'The author thanks Dr. Wen-Chen Chang (Institute of Physics, Academia Sinica) for mentorship and guidance on the experimental high-energy-physics context of this project.', 'The author is grateful to Dr. Wen-Chen Chang (Institute of Physics, Academia Sinica) for his generous mentorship, patient guidance, and encouragement throughout this project. He also warmly thanks the members of the Institute of Physics laboratory community who welcomed him and supported him throughout the research process. This work is presented in the author\'s capacity as an independent researcher and does not represent an institutional position of Academia Sinica.')

source = json.loads((ROOT/'data/provenance/source_evidence.json').read_text())
report = json.loads((ROOT/'data/reports/dicos-f-02_epoch90.json').read_text())
weights = source['calibration']['proposed_weights']
mapping = [('V','Visibility','visible'),('T','Total deposit','response'),('F','First active layer','first_layer'),('A','Layer activity','active'),('B','Layer-budget flow','profile_flow'),('K','Channel count','count'),('S','Support BCE','support_bce'),('R','Support ranking','support_rank'),('Y','Channel-share flow','share_flow')]
weight_rows = '\n'.join(f'${symbol}$ & {name} & {weights[key]:.6f} \\\\' for symbol,name,key in mapping)
bin_rows=[]
for b in report['positive_response']['response_bins']:
    interval = f"{int(b['low'])}--{round(b['high'])}"
    bin_rows.append(f"{interval} & {b['n']:,} & {b['truth_mean']:.3f} & {b['generated_mean']:.3f} & ${100*b['mean_bias_fraction']:+.2f}$ & ${100*b['resolution_difference_fraction']:+.2f}$ \\\\")
classifier_rows=[]
for label,key in [('Condition only','condition_only'),('High-level','high_level'),('Channel energies','low_level'),('Layer profile','profile_aware')]:
    c=report['c2st'][key]
    classifier_rows.append(label+' & '+' & '.join(f'{v:.4f}' for v in c['auroc_per_seed'])+f" & {c['auroc_mean']:.4f} \\\\")
appendix=r'''
\clearpage
\appendix
\section{Recorded settings and reproducibility limits}
\label{app:reproducibility}

The analyzed checkpoint is \texttt{dicos-f-02}, epoch 90, from the \texttt{calibrated\_lr3e4} family, with training seed 20260723. Its SHA-256 is
\begin{quote}\footnotesize\nolinkurl{491284c7423f365230d34b0443f95aa4888ec770bdc673c4c979897bad8acbce}\end{quote}
and its recorded frozen-configuration SHA-256 is
\begin{quote}\footnotesize\nolinkurl{116bc8c220b07ce54ae07196bdd6ed8e835775c8c937182a209a799dc94ae9c5}\end{quote}
The selected validation objective is 4.4837676194. The recorded lineage includes a declared learning-rate restart between epochs 70 and 71, followed by annealing; it is not one uninterrupted decay. The retained history covers epochs 11--114. The original runtime configuration, complete component-stage durations, optimizer hyperparameters beyond those in Sec.~\ref{sec:model}, and exact training software environment are not included in the paper package. These details cannot be reconstructed reliably from aggregate losses alone.

\begin{center}
\begin{minipage}{0.82\linewidth}
\centering
\captionof{table}{Recorded gradient-calibration proposal, rounded to six decimals and ordered as in Eq.~\eqref{eq:joint_loss}. These values document the retained calibration record; the historical runtime configuration is unavailable for an independent check of the applied weights.}
\label{tab:weights}
\small
\begin{tabular}{@{}clr@{}}
\toprule
Weight & Component & Value \\
\midrule
WEIGHT_ROWS
\bottomrule
\end{tabular}
\end{minipage}
\end{center}

The retained calibration values are reproduced by taking inverse median gradient norms relative to their geometric mean, clipping to $[0.25,4]$, and normalizing the resulting nine weights to mean one. This explains why the final entries in Table~\ref{tab:weights} can fall outside the clipping interval. Gradient norms were measured on training batches with respect to the shared condition encoder. This is a fixed calibration heuristic, not evidence that the weights are optimal.

The diagnostic report records generation seed 20260723, FP32 precision on a CUDA device, batches of eight, and eight updates for each flow. Its validation-manifest identity is
\begin{quote}\footnotesize\nolinkurl{1bc3a6b21f736fc71551580a93207128c043833c6848627fb16f07475931690a}\end{quote}
The appendix tables use the same retained aggregate report as the main text; no new shower generation or test evaluation was performed to produce them.

The canonical split is based on event hashes rather than independently identified simulation jobs. The present study uses validation events only. The broader project previously inspected 40,000 nominal-test events in an isolated classifier study and a further draw containing 200 test events, with unresolved overlap. Those historical studies did not feed model decisions, but the nominal test partition cannot be described as wholly untouched; 36,100--36,300 events remain uninspected according to the retained record.

\clearpage
\section{Energy-bin results and classifier details}
\label{app:additional}

Table~\ref{tab:energy_bins} resolves the aggregate response comparison into the eight incident-energy bins. The relative mean difference is $100(\mu_{\rm gen}/\mu_{\rm ref}-1)$ and the width difference is $100(\sigma_{\rm gen}/\sigma_{\rm ref}-1)$, where $\mu$ and $\sigma$ are the mean and standard deviation of total deposited energy. Both statistics include empty showers.

\begin{center}
\begin{minipage}{\linewidth}
\centering
\captionof{table}{Deposited-energy response by incident kinetic energy. $n$ is the number of matched conditions; the same $n$ applies to each sample. Means are in GeV and relative differences are percentages. Bins are lower-inclusive and upper-exclusive, except that the final bin includes 250\,GeV (implemented upper edge 250.0001\,GeV). Intervals for these differences are unavailable.}
\label{tab:energy_bins}
\small
\begin{tabular}{@{}rrrrrr@{}}
\toprule
$\Kinc$ (GeV) & $n$ & $\mu_{\rm ref}$ & $\mu_{\rm gen}$ & Mean diff. (\%) & Width diff. (\%) \\
\midrule
BIN_ROWS
\bottomrule
\end{tabular}
\end{minipage}
\end{center}

\begin{center}
\begin{minipage}{\linewidth}
\centering
\captionof{table}{All recorded classifier seeds for the original development screening battery. The three seed columns vary the classifier and its row partition; they are not independent generator-training seeds. All three high-level AUROCs exceed the declared maximum of 0.65.}
\label{tab:classifier_seeds}
\small
\begin{tabular}{@{}lrrrr@{}}
\toprule
Feature family & 20260804 & 20260805 & 20260806 & Mean \\
\midrule
CLASSIFIER_ROWS
\bottomrule
\end{tabular}
\end{minipage}
\end{center}

The archived evaluator implementation uses a histogram gradient-boosting classifier with a maximum of 100 boosting iterations, maximum depth four, and learning rate 0.08. Its class-stratified random split assigns 14,000 of the 20,000 rows to the fitting partition and 6,000 to the scoring partition; the library may further reserve fitting rows for early stopping under its defaults. The same seed controls this split and the classifier. The split does not group matched condition pairs. These are classifier partitions within canonical validation, not the canonical training and test partitions.

The high-level inputs are total deposit, active-channel count, energy-weighted depth and transverse centroids, radial RMS, largest-channel energy fraction, ECAL fraction, and the energy fraction in layers 48--64. The channel-energy family uses all 6,790 deposits, the layer-profile family uses the 65 layer sums, and the condition-only control uses incident kinetic energy. The nine high-level features use a $10^{-9}\GeV$ floor in their total-energy denominators. Other classifier options follow the library defaults; its exact historical version is not established by the retained report.

These settings were recovered from archived implementation source and do not establish an exact source match to the historical evaluation environment. Source hashes and the aggregate report identify the evidence available for this appendix. The row-wise split limitation remains, and Table~\ref{tab:classifier_seeds} does not replace a pair-grouped evaluation on the same bank.

'''.replace('WEIGHT_ROWS',weight_rows).replace('BIN_ROWS','\n'.join(bin_rows)).replace('CLASSIFIER_ROWS','\n'.join(classifier_rows))
tex=replace_once(tex,r'\printbibliography',appendix+r'\clearpage'+'\n'+r'\printbibliography')
tex_path.write_text(tex,encoding='utf-8')

figure_path=ROOT/'scripts/build_figures.py'
fig=figure_path.read_text(encoding='utf-8')
fig=replace_once(fig,r'\nenergy logits", "flow"',r'\nshare flow", "flow"')
fig=replace_once(fig,r'\nchannel deposits", "decode"',r'\nsoftmax decoder", "decode"')
figure_path.write_text(fig,encoding='utf-8')

for name in ['README.md','STATUS.md','CITATION.cff','scripts/write_build_audit.py']:
    p=ROOT/name;s=p.read_text(encoding='utf-8');s=s.replace('0.15.0','0.16.0')
    if name=='scripts/write_build_audit.py':s=s.replace('audit/visual_review_overall_20260929.json','audit/visual_review_finalization_20260930.json')
    p.write_text(s,encoding='utf-8')

qa_path=ROOT/'scripts/full_manuscript_qa.py';qa=qa_path.read_text(encoding='utf-8')
qa=qa.replace('Version 0.15.0','Version 0.16.0').replace('version: 0.15.0','version: 0.16.0')
qa=replace_once(qa,'assert overall_audit["current_main_tex_sha256"] == sha256(ROOT / "main.tex")','assert overall_audit["current_main_tex_sha256"] == load_json(ROOT / "audit/iterations/iteration_82.json")["source_sha256"]["main.tex"]\n    finalization = load_json(ROOT / "audit/finalization_20260930.json")\n    assert finalization["current_main_tex_sha256"] == sha256(ROOT / "main.tex")\n    assert finalization["status"] in {"source_review_complete", "finalized"}')
qa=replace_once(qa,'"audit/literature_benchmark.md",','"audit/literature_benchmark.md",\n        "audit/finalization_20260930.json", "audit/finalization_20260930.md",')
qa_path.write_text(qa,encoding='utf-8')

a_path=ROOT/'audit/finalization_20260930.json';a=json.loads(a_path.read_text())
a['current_main_tex_sha256']=hashlib.sha256(tex_path.read_bytes()).hexdigest()
a['status']='source_review_complete'
a['changes']=['Independent researcher/contact metadata and mentor/lab thanks','Precise primary-comparison bank scope','Explicit share-flow and decoder labels; original colors retained','Two evidence-bound appendices: settings, weights, all bins, all classifier seeds and methodology','Historical test-use disclosure and unavailable-runtime limitations','Revision metadata and strict historical/current audit bindings updated']
a_path.write_text(json.dumps(a,indent=2)+'\n',encoding='utf-8')
with (ROOT/'audit/finalization_20260930.md').open('a',encoding='utf-8') as f:
    f.write('\n## First revision\n\n'+'. '.join(a['changes'])+'.\n')
with (ROOT/'logs.md').open('a',encoding='utf-8') as f:
    f.write('\nFinalization v0.16 source revision applied via audit/finalize_revision_20260930.py. Added two appendices from retained aggregates and historical source, author-approved metadata and acknowledgments. Main source SHA256 '+a['current_main_tex_sha256']+'. Fourteen equations and original numerical table remain unchanged; strict audit pointers updated to preserve historical binding and require the new source review.\n')
print('Applied v0.16 source revision',a['current_main_tex_sha256'])
