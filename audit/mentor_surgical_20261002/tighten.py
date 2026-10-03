"""Recover the unchanged page limit while preserving the requested scope."""
import json
from session import ROOT, record, sha


def swap(path, old, new):
    file = ROOT / path
    contents = file.read_bytes()
    old = old.encode('utf-8')
    new = new.encode('utf-8')
    assert contents.count(old) == 1, (path, contents.count(old))
    file.write_bytes(contents.replace(old, new))
    record('QA15 pagination correction', {'file': path, 'sha256_after': sha(file),
                                          'old': old.decode('utf-8'), 'new': new.decode('utf-8')})


swap('main.tex',
     'Paired sampling intervals for the headline structural means are not retained. Large descriptive differences do not establish robustness across training seeds, thresholds or graphs. A study with three independent generator-training seeds and a full-data fit is needed to separate architecture effects from training-population and optimization effects. The failed condition-only classifier control is a separate limitation: the quoted classifier scores cannot supply the missing structural significance. A rerun that keeps each matched pair in one partition is needed on the same validation bank.',
     'Paired sampling intervals for the headline structural means are not retained. Large descriptive differences do not establish robustness across training seeds, thresholds or graphs. Three independent generator-training seeds and a full-data fit are needed to separate architecture effects from training-population and optimization effects. Classifier scores cannot supply the missing structural significance: the condition-only control failed. A same-bank rerun must keep each matched pair in one partition.')
swap('scripts/full_manuscript_qa.py',
     '"A study with three independent generator-training seeds"',
     '"Three independent generator-training seeds"')
pointer = ROOT / 'audit/finalization_20260930.json'
data = json.loads(pointer.read_text(encoding='utf-8'))
data['current_main_tex_sha256'] = sha(ROOT / 'main.tex')
pointer.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
with pointer.with_suffix('.md').open('a', encoding='utf-8') as handle:
    handle.write('\nAfter QA15 page-count failure, the Sec. 6.2 caveat was shortened without removing its generator-seed, classifier-control or same-bank pair-grouped-rerun meaning. Current main source SHA-256: '
                 + data['current_main_tex_sha256'] + '.\n')
record('QA15 correction pointer synchronized', {'main_tex_sha256': data['current_main_tex_sha256'],
                                                 'QA15_failure': '15 pages; unchanged 14-page guard retained',
                                                 'scientific_changes': 'None'})
