"""Aggregate graph-run bounds. Synthetic checks establish algebra, not physics."""
from pathlib import Path
import hashlib, itertools, json, math
ROOT=Path(__file__).resolve().parents[1]

def bounds(report):
    out={}
    for short,name in [('r','truth'),('g','generated')]:
        nonempty=1-report['visibility_and_zero_response'][name]['zero_fraction']
        m=report['topology'][name]['connected_components_mean']/nonempty
        g=report['activity'][name]['mean_gaps']
        f=report['activity'][name]['gap_fraction']
        out[short]={'m':m,'G':g,'f':f,'Q_low':max(0,m-1-g),'Q_high':m-1-f}
    out['delta_m']=out['g']['m']-out['r']['m']
    out['delta_Q_low']=out['g']['Q_low']-out['r']['Q_high']
    out['delta_Q_high']=out['g']['Q_high']-out['r']['Q_low']
    out['lower_fraction']=out['delta_Q_low']/out['delta_m']
    return out

def validate_component_bounds(checks):
    path=ROOT/'data/reports/dicos-f-02_epoch90.json'
    b=bounds(json.loads(path.read_text(encoding='utf-8')))
    assert math.isclose(b['delta_m'],35.97033279861813,abs_tol=1e-9)
    assert math.isclose(b['delta_Q_low'],30.445815704637013,abs_tol=1e-9)
    assert math.isclose(b['delta_Q_high'],37.13720180351237,abs_tol=1e-9)
    assert 29.92153994002613 < b['delta_Q_low'] < b['delta_Q_high'] < 38.0724827935712
    assert round(100*b['lower_fraction'],1)==84.6
    # Exhaust every nonempty layer mask over ten layers. Q=m-R can be
    # any nonnegative graph fragmentation beyond those forced separations.
    cases=0
    for mask in itertools.product([0,1],repeat=10):
        active=[i for i,x in enumerate(mask) if x]
        if not active: continue
        G=active[-1]-active[0]+1-len(active)
        R=sum(x and (i==0 or not mask[i-1]) for i,x in enumerate(mask))
        assert 1+int(G>0)<=R<=G+1
        for Q in [0,1,17]:
            m=R+Q
            assert max(0,m-1-G)<=Q<=m-1-int(G>0)
        cases+=1
    # Exact two-layer conditional-independence illustration (no random draws).
    for p in [0.01,0.2,0.5,0.8,0.99]:
        eg=el=ea=0
        for a,c in itertools.product([0,1],repeat=2):
            weight=(p if a else 1-p)*(p if c else 1-p)
            L=2 if c else (1 if a else 0)
            eg+=weight*(L+1-(1+a+c));el+=weight*L;ea+=weight*(1+a+c)
        assert math.isclose(eg,p*(1-p),abs_tol=1e-12)
        assert math.isclose(el-2*p,p*(1-p),abs_tol=1e-12)
        assert math.isclose(ea,1+2*p,abs_tol=1e-12)
    tex=(ROOT/'main.tex').read_text(encoding='utf-8')
    for token in [r'\Delta\overline m-\overline G_{\rm gen}',r'\Delta\overline Q',
                  r'84.6\%', '30.45','52.34','21.89','not a confidence interval or causal decomposition']:
        assert token in tex,token
    artifact={'source_report_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
              'bounds':b,'layer_masks_checked':cases,'toy_probabilities_checked':5,
              'interpretation':'Deterministic sample-mean bounds. Enumerations test algebra only; no model/data-generation experiment or significance claim.'}
    output=ROOT/'audit/component_bound_20260930.json'
    output.write_text(json.dumps(artifact,indent=2)+'\n',encoding='utf-8')
    output.with_suffix('.md').write_text('# Component-bound derivation\n\nFor a nonempty event, m >= R and 1 + I[G>0] <= R <= G+1. Q=m-R therefore lies between max(0,m-1-G) and m-1-I[G>0]. Averaging separately and subtracting gives the retained-sample bounds in the JSON twin.\n\nThe minimum excess is %.8f components, or %.5f percent of the observed mean excess. This is not a confidence interval or a causal fraction.\n\nAll 1,023 nonempty ten-layer masks and five exact two-layer independence examples passed algebra checks. No synthetic check is physics validation.\n'%(b['delta_Q_low'],100*b['lower_fraction']),encoding='utf-8')
    checks.append('Within-run component bounds from exact aggregate means; 1,023 masks and five analytic independence examples (algebra only)')
    return b

if __name__=='__main__':
    checks=[];print(json.dumps(validate_component_bounds(checks),indent=2));print(checks[0])
