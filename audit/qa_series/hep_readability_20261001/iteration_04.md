# QA attempt 4: FAIL

command failed (2): git diff --check
STDOUT:
railing whitespace.
+"""Check new descriptive statistics and guard against unsupported audit inferences."""
scripts/second_audit_checks.py:2: trailing whitespace.
+import hashlib
scripts/second_audit_checks.py:3: trailing whitespace.
+import json
scripts/second_audit_checks.py:4: trailing whitespace.
+import math
scripts/second_audit_checks.py:5: trailing whitespace.
+from pathlib import Path
scripts/second_audit_checks.py:6: trailing whitespace.
+
scripts/second_audit_checks.py:7: trailing whitespace.
+ROOT=Path(__file__).resolve().parents[1]
scripts/second_audit_checks.py:8: trailing whitespace.
+def validate_second_audit(checks):
scripts/second_audit_checks.py:9: trailing whitespace.
+    source=ROOT/'data/reports/dicos-f-02_epoch90.json'
scripts/second_audit_checks.py:10: trailing whitespace.
+    assert hashlib.sha256(source.read_bytes()).hexdigest()=='0e7cc51d34e36eef68039bec36acc5f05dc06cc509a4ad70fea2f5d35a044bd5'
scripts/second_audit_checks.py:11: trailing whitespace.
+    r=json.loads(source.read_text(encoding='utf-8'))
scripts/second_audit_checks.py:12: trailing whitespace.
+    tex=(ROOT/'main.tex').read_text(encoding='utf-8')
scripts/second_audit_checks.py:13: trailing whitespace.
+    b=r['positive_response']['response_bins']
scripts/second_audit_checks.py:14: trailing whitespace.
+    moments={}
scripts/second_audit_checks.py:15: trailing whitespace.
+    for key,expected in [('truth',4.759442787252806),('generated',4.8302628711907625)]:
scripts/second_audit_checks.py:16: trailing whitespace.
+        n=sum(x['n'] for x in b)
scripts/second_audit_checks.py:17: trailing whitespace.
+        mean=sum(x['n']*x[key+'_mean'] for x in b)/n
scripts/second_audit_checks.py:18: trailing whitespace.
+        var=sum(x['n']*(x[key+'_std']**2+(x[key+'_mean']-mean)**2) for x in b)/n
scripts/second_audit_checks.py:19: trailing whitespace.
+        assert math.isclose(math.sqrt(var),expected,abs_tol=1e-10)
scripts/second_audit_checks.py:20: trailing whitespace.
+        assert f'{math.sqrt(var):.3f}' in tex
scripts/second_audit_checks.py:21: trailing whitespace.
+        moments[key]={'n':n,'mean':mean,'population_std':math.sqrt(var),'marginal_iid_mean_se':math.sqrt(var/(n-1))}
scripts/second_audit_checks.py:22: trailing whitespace.
+    # An independent retained normalization corroborates the reference width.
scripts/second_audit_checks.py:23: trailing whitespace.
+    p=r['positive_response']
scripts/second_audit_checks.py:24: trailing whitespace.
+    assert math.isclose(p['response_wasserstein_gev']/p['response_wasserstein_normalized'],moments['truth']['population_std'],rel_tol=1e-6)
scripts/second_audit_checks.py:25: trailing whitespace.
+    for key,fmt in [('truth','93.81'),('generated','92.53')]:
scripts/second_audit_checks.py:26: trailing whitespace.
+        assert f"{100*r['first_layer'][key]['ecal_start_prevalence']:.2f}"==fmt
scripts/second_audit_checks.py:27: trailing whitespace.
+        assert fmt+r'\%' in tex
scripts/second_audit_checks.py:28: trailing whitespace.
+    assert r['structural_invariants']['support_mask_mismatch']==0
scripts/second_audit_checks.py:29: trailing whitespace.
+    for text in ['does not establish electronic ganging','aggregate-only','at least 30.45 of the 35.97 excess groups','assumes conditional independence','70\\% chance','0.25\\,MeV','provisional $V_0$','zero support-mask mismatch','4.759 and 4.830']:
scripts/second_audit_checks.py:30: trailing whitespace.
+        assert text in tex,text
scripts/second_audit_checks.py:31: trailing whitespace.
+    assert 'ganged channel' not in tex
scripts/second_audit_checks.py:32: trailing whitespace.
+    assert 'A MIP-equivalent threshold cannot be assigned' not in tex
scripts/second_audit_checks.py:33: trailing whitespace.
+    figs=(ROOT/'scripts/build_figures.py').read_text(encoding='utf-8')
scripts/second_audit_checks.py:34: trailing whitespace.
+    assert 'Readout ganging' not in figs
scripts/second_audit_checks.py:35: trailing whitespace.
+    geometry=json.loads((ROOT/'data/geometry/geometry_summary.json').read_text())
scripts/second_audit_checks.py:36: trailing whitespace.
+    h=geometry['physical_position_count_histogram']
scripts/second_audit_checks.py:37: trailing whitespace.
+    physical=sum(int(k)*v for k,v in h.items())-400
scripts/second_audit_checks.py:38: trailing whitespace.
+    assert physical==9246 and sum(h.values())==6790
scripts/second_audit_checks.py:39: trailing whitespace.
+    payload={'report_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'population_moments_from_bins':moments,'hcal_position_count':physical,'hcal_positions_per_id':physical/6390,'scope':'Aggregate arithmetic only; no paired covariance, electronics mapping or model mechanism inferred.'}
scripts/second_audit_checks.py:40: trailing whitespace.
+    (ROOT/'audit/second_audit_derived_statistics_20260930.json').write_text(json.dumps(payload,indent=2)+'\n',encoding='utf-8')
scripts/second_audit_checks.py:41: trailing whitespace.
+    (ROOT/'audit/second_audit_derived_statistics_20260930.md').write_text('# Aggregate statistics\n\nAll-event population standard deviations pooled from eight recorded bins: reference 4.759443 GeV; generated 4.830263 GeV. Marginal iid standard errors do not supply the missing paired covariance. The geometry has 9,246 HCAL position observations grouped into 6,390 IDs; their physical interpretation remains unverified.\n',encoding='utf-8')
scripts/second_audit_checks.py:42: trailing whitespace.
+    checks.append('Second audit: hash-bound bin widths, pooled moments, ECAL-start fractions, selected/positive support equality and stored-ID scope; no inferred electronics or zero-cause result')
scripts/write_build_audit.py:38: trailing whitespace.
+        'release': 'v0.21.0', 'status': 'exploratory HEP/computational-physics case study',
scripts/write_build_audit.py:50: trailing whitespace.
+    text = ('# Final manuscript build audi\n\nVersion 0.21.0; '+payload['created_utc']+'.\n\n'

STDERR:
