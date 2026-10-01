from pathlib import Path
import json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def edit(n,a,b):
 p=ROOT/n;s=p.read_text(encoding='utf-8');assert a in s,(n,a);p.write_text(s.replace(a,b),encoding='utf-8')
edit('scripts/build_figures.py','    fig.canvas.draw()','    ax.text(5.6, 1.66, "Training: reference upstream states | Generation: sampled upstream states",\n            ha="center", va="center", fontsize=8.5, color="#344c65")\n    fig.canvas.draw()')
p=ROOT/'scripts/build_figures.py';s=p.read_text(encoding='utf-8');a=s.index('def plot_longitudinal(');b=s.index('def plot_support_summary(',a)
s=s[:a]+'''def plot_longitudinal(report: dict) -> None:
    profile = report["distribution_metrics"]["mean_longitudinal_profile"]
    truth, generated = np.asarray(profile["truth"]), np.asarray(profile["generated"])
    if not (np.all(truth > 0) and np.all(np.isfinite(generated))):
        raise ValueError("Mean-profile ratios require finite means and positive reference bins")
    layers = np.arange(len(truth))
    fig = plt.figure(figsize=(8.6, 3.65), layout="constrained")
    grid = fig.add_gridspec(2, 3, width_ratios=[0.8, 1.35, 1.35], height_ratios=[2.2, 1])
    bar = fig.add_subplot(grid[:, 0])
    parts = np.array([[truth[0], truth[1:].sum()], [generated[0], generated[1:].sum()]])
    bar.bar([0,1], parts[:,0], color=[COLORS["Reference"], COLORS["Generator"]], width=.68)
    bar.bar([0,1], parts[:,1], bottom=parts[:,0], color=["#8c8c8c", "#7fa6c2"], width=.68)
    for i, total in enumerate(parts.sum(axis=1)):
        bar.text(i,total+.06,f"{total:.3f}",ha="center",fontsize=9)
    for y,label in [(parts[0,0]/2,"ECAL"),(parts[0,0]+parts[0,1]/2,"HCAL")]:
        bar.text(0,y,label,ha="center",va="center",color="white",fontsize=9)
    bar.set_xticks([0,1],["reference","generator"],fontsize=9)
    bar.set_ylabel("mean deposit / event (GeV)")
    bar.set_title("ECAL + HCAL")
    for col, low, high, logarithmic in [(1,1,30,False),(2,0,64,True)]:
        ax=fig.add_subplot(grid[0,col]); ratio=fig.add_subplot(grid[1,col],sharex=ax)
        use=slice(low,high+1)
        ax.plot(layers[use],truth[use],ls="--",lw=1.6,color=COLORS["Reference"],label="Geant4")
        ax.plot(layers[use],generated[use],lw=1.6,color=COLORS["Generator"],label="generator")
        ax.set_ylabel("mean layer deposit (GeV)",fontsize=9)
        ax.tick_params(labelbottom=False,labelsize=8.5)
        ax.set_xlim(low,high)
        if logarithmic:
            ax.set_yscale("log"); ax.set_title("All layers (0 = ECAL)")
            ax.legend(frameon=False,fontsize=8,loc="upper right")
        else:
            ax.set_ylim(0,.11);ax.set_title("HCAL layers 1–30")
        ratio.plot(layers[use],(generated/truth)[use],lw=1.2,color=COLORS["Generator"])
        ratio.axhline(1,color="#333333",ls=":",lw=.9)
        ratio.set_ylim(.4,1.2);ratio.set_yticks([.5,1.0]);ratio.tick_params(labelsize=8.5)
        ratio.set_xlabel("longitudinal layer",fontsize=9);ratio.set_ylabel("gen. / ref.",fontsize=9)
    fig.suptitle("Mean longitudinal energy deposit; ratios have no uncertainty bands",fontsize=11)
    save(fig,"longitudinal_profile.png")


'''+s[b:];p.write_text(s,encoding='utf-8')
edit('main.tex','generated ECAL deposit is higher by 0.175\\,GeV and HCAL deposit lower by 0.129\\,GeV','generated ECAL deposit is higher by 0.175\\,GeV (8.3\\%) and HCAL deposit lower by 0.129\\,GeV (5.8\\%)')
edit('main.tex',"Its layer profiles average over events and therefore cannot reveal an individual shower's interior gaps.","At the reference HCAL maximum (layer 9), the generated mean is 8.6\\% lower. Mean profiles cannot reveal individual interior gaps.")
edit('main.tex','Right: HCAL layers 1--64 (log scale). Dashed curves denote Geant4, solid curves the generator; ECAL layer 0 enters only the bars. Event averages include empty showers and do not resolve individual interior gaps.','Right: all layers, including ECAL at 0 (log scale). Dashed curves denote Geant4, solid curves the generator. Lower panels show ratios of means; uncertainty bands are unavailable. Empty showers are included.')
edit('main.tex','Figure~\\ref{fig:support} resolves how much graph fragmentation must remain after occupied-layer runs are accounted for.','The all-event mean energy-weighted depth, $\\sum_\\ell\\ell B_\\ell/\\max(T,10^{-9}\\GeV)$, is instead 13.94 for generated showers and 14.02 for Geant4; empty events contribute zero. This distinguishes occupied extent from energy-weighted depth, but does not determine the energy carried by disconnected components. Figure~\\ref{fig:support} bounds the within-run fragmentation.')
edit('main.tex','On its own event bank, it gives condition-only AUROC','It records the same run and epoch (\\texttt{dicos-f-02}, epoch 90) on a different event bank, with condition-only AUROC')
# Source-led provenance permits run/epoch identity, not stronger event-bank comparability.
p=ROOT/'audit/claim_register_20260922.json';j=json.loads(p.read_text());j['values']['within_run_lower_fraction_of_mean_excess']=0.8464146238259613;j['method_boundaries']['graph']='Same/adjacent-layer edges imply 1+I[G>0]<=R<=G+1 and m>=R. Gap fractions sharpen sample bounds; pure lateral or physical-cluster interpretation is not established.';p.write_text(json.dumps(j,indent=2)+'\n')
p=ROOT/'audit/finalization_20260930.json';j=json.loads(p.read_text());j['current_main_tex_sha256']=hashlib.sha256((ROOT/'main.tex').read_bytes()).hexdigest();p.write_text(json.dumps(j,indent=2)+'\n')
print('Applied figure, descriptive-result and exact-source updates')
