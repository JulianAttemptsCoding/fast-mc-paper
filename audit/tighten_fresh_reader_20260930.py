import importlib.util
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('review', ROOT/'audit/fresh_reader_revision_20260930.py')
review=importlib.util.module_from_spec(spec)
spec.loader.exec_module(review)
p=ROOT/'main.tex'
t=p.read_text(encoding='utf-8')
changes=[
('Agreement in mean deposited energy and occupancy can conceal differences in the spatial structure of generated calorimeter showers. We investigate this problem with a hierarchical model of single-neutron showers in a 6,790-channel Zero-Degree Calorimeter readout, using raw deposited energies without a threshold.',
 'Mean deposited energy and occupancy can agree while spatial shower structure differs. We study a hierarchical single-neutron generator for a 6,790-channel Zero-Degree Calorimeter using raw deposited energies without a threshold.'),
('Conditioned on the incident four-vector, the model generates a total readout deposit, distributes it among active layers, and selects and energizes channels within each layer.',
 'Conditioned on the incident four-vector, it samples total deposit, active layers, channel support, and energy shares.'),
('Detailed particle transport provides the reference description of calorimeter showers, but producing large simulated samples can be computationally costly. A useful surrogate must reproduce the aspects of the readout that matter for detector studies, not only its mean deposited energy.',
 'Detailed particle transport provides the reference calorimeter showers but can be computationally costly. A useful surrogate must reproduce readout properties relevant to detector studies beyond mean deposited energy.'),
('The contribution is a concrete diagnostic case: near-agreement in marginal means can coexist with a different organization of occupied layers. The architecture supplies the test case, rather than a demonstrated improvement over competing generators.',
 'This is a diagnostic case study; no architecture-superiority comparison is performed.'),
('The centroid representation defines the spatial information available to both the model and the graph diagnostic.',
 'These centroids define the spatial representation for the model and connectivity diagnostic.'),
('The comparison tests distributions over this bank, not reproduction of a particular Geant4 shower; one draw per condition cannot determine the full conditional shower distribution.',
 'One draw per condition tests bank-level distributions, not the full shower distribution at a fixed condition.'),
('Event-level run counts with paired uncertainty estimates and threshold scans are the next tests needed to establish the robustness and origin of this pattern.',
 'Event-level run counts, paired uncertainty estimates, and threshold scans would clarify its robustness and interpretation.'),
]
for old,new in changes:
    assert t.count(old)==1, old
    t=t.replace(old,new)
p.write_text(t,encoding='utf-8',newline='\n')
f=ROOT/'audit/finalization_20260930.json'
data=json.loads(f.read_text(encoding='utf-8'))
data['current_main_tex_sha256']=review.sha(p)
f.write_text(json.dumps(data,indent=2)+'\n',encoding='utf-8')
state=json.loads(review.AUDIT.read_text(encoding='utf-8'))
state['changes'].extend({'purpose':'Tighten repetition and avoid causal implication in next-step wording','old':a,'new':b} for a,b in changes)
review.save(state,{'summary':'QA88 retained as failed page-count attempt. Tightened seven passages, including abstract and repeated introduction scope; replaced origin with interpretation in conclusion. No guard, equation, result, figure, or scientific threshold changed.', 'command':'python audit/tighten_fresh_reader_20260930.py'})
