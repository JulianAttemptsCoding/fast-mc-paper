"""Recompute the October reader additions from released aggregate evidence."""
import hashlib
import json
import math
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]


def verify_review_additions(checks):
    report_path = ROOT / 'data/reports/dicos-f-02_epoch90.json'
    geometry_path = ROOT / 'data/geometry/readout_geometry.npz'
    assert hashlib.sha256(report_path.read_bytes()).hexdigest() == '0e7cc51d34e36eef68039bec36acc5f05dc06cc509a4ad70fea2f5d35a044bd5'
    assert hashlib.sha256(geometry_path.read_bytes()).hexdigest() == 'f3bf20d992b41e5f7f6b6fb41453359e80851d3c34a70e3175dd0219748afe2e'
    report = json.loads(report_path.read_text(encoding='utf-8'))
    geometry = np.load(geometry_path)
    xyz = geometry['positions_mm'].astype(float)
    layers = geometry['layer_index']
    parent = np.arange(len(xyz))

    def root(index):
        while parent[index] != index:
            parent[index] = parent[parent[index]]
            index = parent[index]
        return index

    def unite(a, b):
        parent[root(a)] = root(b)

    edges = 0
    nearest = []
    for layer in range(65):
        ids = np.flatnonzero(layers == layer)
        distances = np.linalg.norm(xyz[ids, None] - xyz[ids][None, :], axis=2)
        np.fill_diagonal(distances, np.inf)
        neighbors = np.argsort(distances, axis=1, kind='stable')[:, :8]
        if layer > 0:
            nearest.extend(distances.min(axis=1).tolist())
        for row, indices in enumerate(neighbors):
            for index in indices:
                unite(ids[row], ids[index])
        edges += 8 * len(ids)
        assert len({root(index) for index in ids}) == 1, layer
    for layer in range(64):
        left = np.flatnonzero(layers == layer)
        right = np.flatnonzero(layers == layer + 1)
        distances = np.linalg.norm(xyz[left, None] - xyz[right][None, :], axis=2)
        neighbors = np.argsort(distances, axis=1, kind='stable')[:, :4]
        for row, indices in enumerate(neighbors):
            for index in indices:
                unite(left[row], right[index])
        edges += 2 * 4 * len(left)
    components = len({root(index) for index in range(len(xyz))})
    pitch = float(np.median(nearest))
    assert edges == 107920 and components == 1 and round(pitch, 1) == 54.2

    bins = report['positive_response']['response_bins']
    count = sum(item['n'] for item in bins)
    moments = {}
    for sample in ['truth', 'generated']:
        mean = sum(item['n'] * item[sample + '_mean'] for item in bins) / count
        variance = sum(item['n'] * (item[sample + '_std'] ** 2 + (item[sample + '_mean'] - mean) ** 2) for item in bins) / count
        moments[sample] = {'mean': mean, 'variance': variance}
    independent_se = math.sqrt(sum(item['variance'] for item in moments.values()) / (count - 1))
    depth = report['distribution_metrics']['depth_centroid_layer']['wasserstein']
    depth_floor = report['distribution_metrics']['truth_half_floor']['depth_centroid_layer']['wasserstein']
    response = report['distribution_metrics']['total_response_gev']['wasserstein']
    response_floor = report['truth_half_floors']['response_wasserstein_gev']
    assert round(independent_se, 3) == .068
    assert round(depth, 3) == .971 and round(depth_floor, 3) == .155
    assert round(response, 3) == .073 and round(response_floor, 3) == .147
    tex = (ROOT / 'main.tex').read_text(encoding='utf-8')
    for token in ['54.2', 'full graph is connected', '4.759\\,GeV for Geant4', '4.830\\,GeV for the generator', '0.068', '0.971', '0.155', '0.073', '0.147', 'exact paired standard error', 'separate scales', 'No uncertainty estimates for these structural means']:
        assert token in tex, token
    sections = [tex.index('\\subsection{' + title + '}') for title in ['Deposited energy and empty showers', 'Longitudinal activity', 'Channel hit pattern and graph structure', 'Classifier and numerical checks']]
    assert tex.index('\\section{Results}') < min(sections) and sections == sorted(sections)
    assert tex.index('\\section{Results}') < tex.index('longitudinal_profile.png') < tex.index('support_summary.png') < tex.index('\\section{Discussion}')
    payload = {'geometry_sha256': hashlib.sha256(geometry_path.read_bytes()).hexdigest(), 'report_sha256': hashlib.sha256(report_path.read_bytes()).hexdigest(), 'directed_edges': edges, 'weak_components': components, 'every_layer_laterally_connected': True, 'hcal_median_nearest_centroid_mm': pitch, 'independent_sample_se_scale_gev': independent_se, 'depth_w1_layers': depth, 'depth_half_split_layers': depth_floor, 'response_w1_gev': response, 'response_half_split_gev': response_floor, 'scope': 'Arithmetic, static geometry and section order only; independent-sample SE is an approximation, not a recovered paired interval or physics validation.'}
    dest = ROOT / 'audit/claude_review_derived_20261002.json'
    dest.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
    dest.with_suffix('.md').write_text('# October review evidence checks\n\nRebuilt the nearest-centroid graph: 107,920 directed edges, one weak component, every layer laterally connected. HCAL nearest-centroid median is 54.2 mm. Pooled widths imply an independent-sample mean-difference error scale of 0.068 GeV, without recovering the paired covariance. Depth and total-response Wasserstein distances and half-split scales match the source report. Results and figure reading order are checked explicitly.\n', encoding='utf-8')
    checks.append('October review: graph connectivity and pitch, response error scale, depth/response distances, structural figure denominators and Results reading order')


if __name__ == '__main__':
    checks = []
    verify_review_additions(checks)
    print('\n'.join(checks))
