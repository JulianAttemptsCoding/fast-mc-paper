"""Check new descriptive statistics and guard against unsupported audit inferences."""
import hashlib
import json
import math
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
def validate_second_audit(checks):
    source=ROOT/'data/reports/dicos-f-02_epoch90.json'
    assert hashlib.sha256(source.read_bytes()).hexdigest()=='0e7cc51d34e36eef68039bec36acc5f05dc06cc509a4ad70fea2f5d35a044bd5'
    r=json.loads(source.read_text(encoding='utf-8'))
    tex=(ROOT/'main.tex').read_text(encoding='utf-8')
    b=r['positive_response']['response_bins']
    moments={}
    for key,expected in [('truth',4.759442787252806),('generated',4.8302628711907625)]:
        n=sum(x['n'] for x in b)
        mean=sum(x['n']*x[key+'_mean'] for x in b)/n
        var=sum(x['n']*(x[key+'_std']**2+(x[key+'_mean']-mean)**2) for x in b)/n
        assert math.isclose(math.sqrt(var),expected,abs_tol=1e-10)
        assert f'{math.sqrt(var):.3f}' in tex
        moments[key]={'n':n,'mean':mean,'population_std':math.sqrt(var),'marginal_iid_mean_se':math.sqrt(var/(n-1))}
    # An independent retained normalization corroborates the reference width.
    p=r['positive_response']
    assert math.isclose(p['response_wasserstein_gev']/p['response_wasserstein_normalized'],moments['truth']['population_std'],rel_tol=1e-6)
    for key,fmt in [('truth','93.81'),('generated','92.53')]:
        assert f"{100*r['first_layer'][key]['ecal_start_prevalence']:.2f}"==fmt
        assert fmt+r'\%' in tex
    assert r['structural_invariants']['support_mask_mismatch']==0
    for text in ['does not establish electronic ganging','aggregate-only','Bounding the difference in occupied-layer run counts','assumes conditional independence','70\\% chance','0.25\\,MeV','provisional $V_0$','zero support-mask mismatch','4.759 and 4.830']:
        assert text in tex,text
    assert 'ganged channel' not in tex
    assert 'A MIP-equivalent threshold cannot be assigned' not in tex
    figs=(ROOT/'scripts/build_figures.py').read_text(encoding='utf-8')
    assert 'Readout ganging' not in figs
    geometry=json.loads((ROOT/'data/geometry/geometry_summary.json').read_text())
    h=geometry['physical_position_count_histogram']
    physical=sum(int(k)*v for k,v in h.items())-400
    assert physical==9246 and sum(h.values())==6790
    payload={'report_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'population_moments_from_bins':moments,'hcal_position_count':physical,'hcal_positions_per_id':physical/6390,'scope':'Aggregate arithmetic only; no paired covariance, electronics mapping or model mechanism inferred.'}
    (ROOT/'audit/second_audit_derived_statistics_20260930.json').write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
    (ROOT/'audit/second_audit_derived_statistics_20260930.md').write_text('# Aggregate statistics\n\nAll-event population standard deviations pooled from eight recorded bins: reference 4.759443 GeV; generated 4.830263 GeV. Marginal iid standard errors do not supply the missing paired covariance. The geometry has 9,246 HCAL position observations grouped into 6,390 IDs; their physical interpretation remains unverified.\n',encoding='utf-8')
    checks.append('Second audit: hash-bound bin widths, pooled moments, ECAL-start fractions, selected/positive support equality and stored-ID scope; no inferred electronics or zero-cause result')
