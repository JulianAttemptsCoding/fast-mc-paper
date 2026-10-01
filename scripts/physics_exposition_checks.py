"""Verify new aggregate statements and provenance, not physics fidelity."""
from pathlib import Path
import json,math,hashlib
import numpy as np
ROOT=Path(__file__).resolve().parents[1]

def validate_physics_exposition(checks):
    source=ROOT/'data/reports/dicos-f-02_epoch90.json'
    r=json.loads(source.read_text(encoding='utf-8'))
    p=r['distribution_metrics']['mean_longitudinal_profile']
    ref,gen=np.array(p['truth']),np.array(p['generated'])
    peak=int(np.argmax(ref[1:])+1)
    deficit=100*(gen[peak]/ref[peak]-1)
    assert peak==9 and math.isclose(deficit,-8.644442934169938,abs_tol=1e-10)
    ratios=gen/ref
    assert np.all(np.isfinite(ratios)) and .75<ratios.min()<=ratios.max()<1.3
    centroid=r['distribution_metrics']['depth_centroid_layer']
    assert math.isclose(centroid['truth_mean'],14.021207176895183,abs_tol=1e-10)
    assert math.isclose(centroid['generated_mean'],13.93749794081637,abs_tol=1e-10)
    nonempty_centroid={k:centroid[k+'_mean']/(1-r['visibility_and_zero_response'][k]['zero_fraction']) for k in ['truth','generated']}
    assert round(nonempty_centroid['truth'],2)==14.15 and round(nonempty_centroid['generated'],2)==14.14
    geom=ROOT/'data/geometry/readout_geometry.npz'
    with np.load(geom) as g:
        hist={}
        for layer in range(1,65):
            values,counts=np.unique(g['physical_position_count'][g['layer_index']==layer],return_counts=True)
            hist[str(layer)]={str(int(k)):int(v) for k,v in zip(values,counts)}
    assert all(hist[str(i)]==hist[str(i+4)] for i in range(5,23))
    assert hist['1']!=hist['5'] and hist['23']!=hist['27']
    tex=(ROOT/'main.tex').read_text(encoding='utf-8')
    for token in ['84.6\\%','30.45','13.94','14.02','8.6\\%','not added electronics noise',
                  'not particle or energy transport',"not conservation of the incident neutron's full energy",
                  'first stored deposit','uncertainty bands are unavailable']:
        assert token in tex,token
    claims=json.loads((ROOT/'audit/claim_register_20260922.json').read_text())
    from component_bounds import bounds
    b=bounds(r)
    assert math.isclose(claims['values']['within_run_lower_fraction_of_mean_excess'],b['lower_fraction'],abs_tol=1e-12)
    out={'report_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
         'geometry_sha256':hashlib.sha256(geom.read_bytes()).hexdigest(),
         'reference_hcal_peak_layer':peak,'generator_difference_percent_at_reference_peak':deficit,
         'depth_centroid_layer':centroid,'nonempty_mean_depth_centroid_layer':nonempty_centroid,'mean_profile_ratio_min_max':[float(ratios.min()),float(ratios.max())],
         'multiplicity_histograms_by_layer':hist,'interpretation':'No global mod-4 multiplicity pattern; some blocks repeat. Centroids/multiplicities cannot establish tile contiguity or design equivalence.'}
    dest=ROOT/'audit/physics_exposition_derived_20261001.json'
    dest.write_text(json.dumps(out,indent=2)+'\n',encoding='utf-8')
    dest.with_suffix('.md').write_text('# New aggregate checks\n\nHCAL peak: layer 9, generator mean deficit 8.64444%. All-event mean energy-weighted depths: reference 14.02120718, generator 13.93749794. Ratios finite and entirely inside plotted range. Geometry multiplicity is not globally periodic over four layers; individual tile positions are unavailable. See JSON twin for inputs and all layer histograms. No event-level or detector-performance validation.\n',encoding='utf-8')
    checks.append('Third audit: profile peak/ratios, energy-weighted depth, stored-ID periodicity check, physical-stage scope and synchronized sharper bound')
