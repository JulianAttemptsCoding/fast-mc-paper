"""Bind the mentor-send clarity additions to the released aggregate report."""
import hashlib
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def verify_mentor_send_additions(checks):
    report_path = ROOT / 'data/reports/dicos-f-02_epoch90.json'
    assert hashlib.sha256(report_path.read_bytes()).hexdigest() == '0e7cc51d34e36eef68039bec36acc5f05dc06cc509a4ad70fea2f5d35a044bd5'
    report = json.loads(report_path.read_text(encoding='utf-8'))
    tex = (ROOT / 'main.tex').read_text(encoding='utf-8')

    # Stored total relative to incident kinetic energy: a scale, not a sampling fraction.
    kinetic = report['paired_response']['mean_kinetic_gev']
    total = report['distribution_metrics']['total_response_gev']
    fractions = {key: total[key + '_mean'] / kinetic for key in ['truth', 'generated']}
    assert round(kinetic, 1) == 149.9
    assert all(round(100 * value) == 3 for value in fractions.values()), fractions

    # Binwise widths and the independent-sample error scale already used for the pooled mean.
    rows = []
    for item in report['positive_response']['response_bins']:
        n = item['n']
        scale = math.sqrt((item['truth_std'] ** 2 + item['generated_std'] ** 2) / (n - 1))
        rows.append({
            'low': item['low'], 'n': n,
            'reference_std_over_mean': item['truth_std'] / item['truth_mean'],
            'generated_std_over_mean': item['generated_std'] / item['generated_mean'],
            'reference_mean_relative_se': item['truth_std'] / math.sqrt(n) / item['truth_mean'],
            'difference_over_independent_se': (item['generated_mean'] - item['truth_mean']) / scale,
            'mean_difference_percent': 100 * item['mean_bias_fraction'],
        })
    assert all(0.9 < row[key] < 1.25 for row in rows for key in ['reference_std_over_mean', 'generated_std_over_mean'])
    assert all(round(100 * row['reference_mean_relative_se']) == 3 for row in rows)
    largest = max(rows, key=lambda row: abs(row['difference_over_independent_se']))
    assert largest['low'] == 150.0 and round(abs(largest['difference_over_independent_se']), 1) == 2.0
    assert round(largest['mean_difference_percent'], 2) == -7.65
    # Both of the largest percentage differences are quoted with their error scales.
    by_percent = sorted(rows, key=lambda row: abs(row['mean_difference_percent']), reverse=True)[:2]
    assert [row['low'] for row in by_percent] == [125.0, 150.0]
    assert round(by_percent[0]['mean_difference_percent'], 2) == 7.74
    assert round(by_percent[0]['difference_over_independent_se'], 1) == 1.8
    assert sorted(row['mean_difference_percent'] > 0 for row in rows) == [False] * 3 + [True] * 5

    # Last-active-layer shift expressed with the stored HCAL layer spacing.
    activity = report['activity']
    shift_layers = activity['generated']['mean_last_active_layer'] - activity['truth']['mean_last_active_layer']
    with np.load(ROOT / 'data/geometry/readout_geometry.npz') as geometry:
        xyz = geometry['positions_mm'].astype(float)
        layer = geometry['layer_index']
        z_means = np.array([xyz[layer == index, 2].mean() for index in range(1, 65)])
    z_pitch = float(np.median(np.diff(z_means)))
    assert round(z_pitch, 1) == 24.9 and round(shift_layers * z_pitch / 1000, 2) == 0.11

    # Mean-profile ratio quoted beside the longitudinal figure.
    profile = report['distribution_metrics']['mean_longitudinal_profile']
    ratio = np.asarray(profile['generated'], dtype=float) / np.asarray(profile['truth'], dtype=float)
    assert int(ratio.argmin()) == 51 and round(float(ratio.min()), 2) == 0.84
    assert np.all(ratio[60:] > 1) and np.all(ratio[33:60] < 1)
    assert int(ratio.argmax()) == 64 and round(float(ratio[64]), 2) == 1.23

    # Energy-weighted transverse summaries. Empty showers enter the all-event means as exact zeros.
    nonempty = {key: 1 - report['visibility_and_zero_response'][key]['zero_fraction'] for key in ['truth', 'generated']}
    metrics = report['distribution_metrics']
    transverse = {}
    for name in ['x_centroid_mm', 'y_centroid_mm', 'radial_rms_mm']:
        transverse[name] = {key: metrics[name][key + '_mean'] / nonempty[key] for key in ['truth', 'generated']}
    assert round(abs(transverse['x_centroid_mm']['generated'] - transverse['x_centroid_mm']['truth']), 1) == 0.5
    assert round(abs(transverse['y_centroid_mm']['generated'] - transverse['y_centroid_mm']['truth']), 1) == 1.1
    assert round(transverse['radial_rms_mm']['generated'], 1) == 84.7
    assert round(transverse['radial_rms_mm']['truth'], 1) == 87.1
    radial_change = 100 * (transverse['radial_rms_mm']['generated'] / transverse['radial_rms_mm']['truth'] - 1)
    assert round(radial_change, 1) == -2.8
    radial_w1 = metrics['radial_rms_mm']['wasserstein']
    radial_floor = metrics['truth_half_floor']['radial_rms_mm']['wasserstein']
    assert round(radial_w1, 2) == 3.34 and round(radial_floor, 2) == 0.48

    # Definitions restored for the reader: reference-half scale and abstract context.
    assert report['pairs'] // 2 == 5000
    zero = report['visibility_and_zero_response']
    layers = {key: activity[key]['mean_active_layers'] / (1 - zero[key]['zero_fraction']) for key in ['truth', 'generated']}
    assert f"{layers['generated']:.2f}" == '54.83' and f"{layers['truth']:.2f}" == '54.58'
    counts = {key: report['counts'][key]['mean_hit_count'] / (1 - zero[key]['zero_fraction']) for key in ['truth', 'generated']}
    assert round(100 * (counts['generated'] / counts['truth'] - 1), 1) == -1.8

    for token in [
        'incident-neutron conditions', '54.83 generated versus 54.58 Geant4, of 65 layers',
        '23.42 for Geant4 and 59.39 for the generator', 'rather than the chance value 0.5',
        'the set of active channels', 'no single random vector is shared by all stages of an event',
        'free-running (fully sampled)', 'Wasserstein-1 distance $W_1$',
        'two disjoint 5,000-event halves of the Geant4 sample (the reference-half scale)',
        'about 3\\% of the 149.9\\,GeV mean incident kinetic energy',
        'neither a calibrated energy nor a sampling-fraction measurement',
        'are 1.8 and 2.0 standard errors', 'the mixed signs in', 'do not establish an energy-dependent bias',
        '(the generator is 2.8\\% narrower)', 'section-level cancellation',
        'of the same checkpoint (\\texttt{dicos-f-02}, epoch 90)', 'The bound discounts empty-layer separations',
        'the last deposit lies deeper', 'The zero-threshold hit pattern describes',
        'splits individual showers at random, not matched pairs',
        'Bernoulli-draw ($V_0=0$) and zero-clamp contributions',
        'about 0.11\\,m at the 24.9\\,mm median HCAL layer spacing',
        '0.84 at layer 51', '1.23 at layer 64', '($-1.8\\%$)',
        'differ by 0.5\\,mm in $x$ and 1.1\\,mm in $y$', '84.7\\,mm for the generator and 87.1\\,mm for Geant4',
        '$W_1$ is 3.34\\,mm', '0.48\\,mm reference-half scale', 'neither is a reconstructed position',
        'graph edges whose two end channels are both active', 'Closure residuals compare decoded deposits',
        'builds a null sample from Geant4 itself', 'Dr.~Wen-Chen Chang', 'the activity indicator of layer $\\ell$', 'single-precision (FP32) decoding',
        '0.155-layer reference-half scale', '92.53\\% for the generator versus 93.81\\% for Geant4',
        'active-layer count and active-channel count do not imply',
    ]:
        assert token in tex, token
    for overclaim in ['sampling fraction of', 'statistically consistent', 'centroids agree', 'position resolution is']:
        assert overclaim not in tex, overclaim
    for superseded in ['the largest binwise mean difference', 'alternating signs', 'section-level compensation',
                       'strict $E>0$', 'the last deposit occurs later', 'classifier battery splits rows']:
        assert superseded not in tex, superseded
    figures = (ROOT / 'scripts/reader_figures.py').read_text(encoding='utf-8')
    assert '["Geant4", "generator"]' in figures and '["Geant4", "model"]' not in figures

    payload = {
        'report_sha256': hashlib.sha256(report_path.read_bytes()).hexdigest(),
        'mean_incident_kinetic_gev': kinetic, 'stored_total_over_mean_kinetic': fractions,
        'energy_bins': rows, 'last_active_layer_shift_layers': shift_layers,
        'hcal_median_layer_spacing_mm': z_pitch, 'last_active_layer_shift_m': shift_layers * z_pitch / 1000,
        'mean_profile_ratio': {'minimum_layer': 51, 'minimum': float(ratio.min()), 'layer_64': float(ratio[64]),
                               'layers_above_one_after_33': [int(i) for i in np.flatnonzero(ratio[33:] > 1) + 33]},
        'nonempty_transverse_means_mm': transverse, 'radial_rms_relative_change_percent': radial_change,
        'radial_rms_w1_mm': radial_w1, 'radial_rms_reference_half_w1_mm': radial_floor,
        'scope': 'Arithmetic on the released aggregate report and static geometry. The binwise error scale treats the samples as independent and is not a paired interval; transverse summaries are energy-weighted stored-ID centroids, not reconstructed positions.',
    }
    dest = ROOT / 'audit/mentor_send_derived_20261002.json'
    dest.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
    dest.with_suffix('.md').write_text(
        '# Mentor-send clarity additions\n\n'
        'Every number added in v0.22.1 is recomputed from the released aggregate report and static geometry: '
        'the stored total as a fraction of mean incident kinetic energy, binwise width-to-mean ratios and the '
        'independent-sample error scale, the last-active-layer shift in metres, the mean-profile ratio quoted beside '
        'Figure 3, and nonempty-sample energy-weighted transverse means with the radial-RMS distance and its '
        'reference-half scale. No event-level data, checkpoint or new evaluation was used. Values are in the JSON twin.\n',
        encoding='utf-8')
    checks.append('Mentor-send additions: stored-energy scale, binwise error scale, depth shift in metres, profile ratio, transverse summaries and restored definitions')


if __name__ == '__main__':
    checks = []
    verify_mentor_send_additions(checks)
    print('\n'.join(checks))
