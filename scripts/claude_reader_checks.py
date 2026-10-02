"""Check newly reported aggregates and the illustrative graph independently."""
from pathlib import Path
import hashlib,json,math
import numpy as np
ROOT=Path(__file__).resolve().parents[1]

def validate_reader_revision(checks):
    source=ROOT/'data/reports/dicos-f-02_epoch90.json'
    assert hashlib.sha256(source.read_bytes()).hexdigest()=='0e7cc51d34e36eef68039bec36acc5f05dc06cc509a4ad70fea2f5d35a044bd5'
    r=json.loads(source.read_text())
    p=r['distribution_metrics']['mean_longitudinal_profile']
    late={k:1000*sum(p[k][57:]) for k in ['truth','generated']}
    assert round(late['truth'],2)==17.19 and round(late['generated'],2)==17.85
    paired=r['paired_response'];ci=r['bootstrap']['intervals']['response_delta_over_kinetic_mean']
    assert math.isclose(paired['response_delta_over_kinetic_mean'],2.935218067806149e-5)
    assert ci['low']<0<ci['high'] and ci['replicates']==1000 and r['bootstrap']['paired']
    assert round(ci['low']*1e4,2)==-8.51 and round(ci['high']*1e4,2)==9.34
    seconds=r['timing'];analysis=sum(seconds['stage_seconds'].values());residual=seconds['total_seconds']-analysis
    assert round(analysis)==1009 and round(residual)==2433 and round(residual/10000,3)==.243
    with np.load(ROOT/'data/geometry/readout_geometry.npz') as g:
        xyz=g['positions_mm'].astype(float);layer=g['layer_index']
        means=np.array([xyz[layer==i].mean(axis=0) for i in range(65)])
        pitch=float(np.median(np.diff(np.unique(np.round(xyz[layer==0,0],3)))))
        z_pitch=float(np.median(np.diff(means[1:,2])))
        span=float(means[64,2]-means[1,2])
        assert round(pitch,1)==30.3 and round(z_pitch,1)==24.9 and round(span/1000,2)==1.57
        assert round(means[0,2]/1000,2)==35.73
    patterns=[({0,1,2,3,4,5,6,7,9},1,2),({0,1,2,3,5,6,8,11},4,4)]
    for active,gaps,runs in patterns:
        assert max(active)-min(active)+1-len(active)==gaps
        assert sum(i-1 not in active for i in active)==runs
    occupied={(0,2),(0,3),(1,2),(1,3),(2,3),(2,2),(3,3),(1,0),(3,5)}
    todo=set(occupied);components=0
    while todo:
        components+=1;stack=[todo.pop()]
        while stack:
            x,y=stack.pop()
            for q in [(x+1,y),(x-1,y),(x,y+1),(x,y-1)]:
                if q in todo:todo.remove(q);stack.append(q)
    assert components==3 and {x for x,y in occupied}=={0,1,2,3}
    tex=(ROOT/'main.tex').read_text()
    # Author-requested attribution; historical review records remain unchanged.
    assert "Anthropic" not in tex and "Claude" not in tex
    for token in ['30.3','24.9','1.57','35.73','17.85','17.19','2.94','8.51','9.34','0.243',"OpenAI's GPT-5.6-Sol",'does not isolate the energy']:
        assert token in tex,token
    for overclaim in ['no measurable correlation','This difference is not statistically significant','acceptance is likely to matter','the quoted values are lower bounds']:
        assert overclaim not in tex,overclaim
    payload={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'late_energy_mev':late,
             'paired_normalized_response':paired,'paired_normalized_mean_interval':ci,
             'timed_analysis_seconds':analysis,'remaining_evaluation_seconds':residual,
             'geometry':{'ecal_x_pitch_mm':pitch,'hcal_median_z_pitch_mm':z_pitch,'hcal_z_span_mm':span,'ecal_mean_z_mm':float(means[0,2])},
             'toy_graph_components':components,'toy_layer_runs':1,
             'scope':'Aggregate arithmetic and schematic validation only; no new event-level physics evaluation.'}
    dest=ROOT/'audit/claude_reader_derived_20261001.json';dest.write_text(json.dumps(payload,indent=2)+'\n')
    dest.with_suffix('.md').write_text('# Verified reader additions\n\nStatic geometry, normalized paired-response interval, fixed-region energy and evaluation timing arithmetic reproduce the reported values. The two schematic activity masks and three-component toy graph were independently counted. These checks validate arithmetic and exposition, not physics fidelity. Exact inputs and values are in the JSON twin.\n')
    checks.append('Reader proposal: physical coordinate dimensions, paired normalized interval, deep-layer totals, timing accounting and independently counted schematic')
