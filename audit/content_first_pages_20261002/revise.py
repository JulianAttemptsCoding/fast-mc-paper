"""Apply the user's content-first page policy and restore the fuller caveat."""
import json
import shutil
from session import ROOT, HERE, record, sha

before = HERE / 'before'
before.mkdir(exist_ok=False)
paths = ['main.tex', 'scripts/full_manuscript_qa.py', 'README.md', 'STATUS.md',
         'audit/finalization_20260930.json', 'audit/finalization_20260930.md',
         'output/fast_mc_zdc_manuscript.pdf', 'output/fast_mc_zdc_submission_source.zip']
for name in paths:
    destination = before / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(ROOT / name, destination)
record('Pre-correction snapshot', {'paths_sha256': {name: sha(before / name) for name in paths},
                                   'directory': str(before.relative_to(ROOT))})


def swap(path: str, old: str, new: str) -> None:
    file = ROOT / path
    contents = file.read_bytes()
    old_bytes, new_bytes = old.encode('utf-8'), new.encode('utf-8')
    assert contents.count(old_bytes) == 1, (path, old)
    file.write_bytes(contents.replace(old_bytes, new_bytes))
    record('Content-first correction', {'path': path, 'input_sha256': sha(before / path),
                                        'output_sha256': sha(file), 'old': old, 'new': new})


swap('scripts/full_manuscript_qa.py',
     'assert 6 <= pages <= 14',
     'assert pages >= 1, "PDF must contain at least one page"')
swap('scripts/full_manuscript_qa.py',
     '"Three independent generator-training seeds", "Similar aggregate means mask a hit-pattern discrepancy",',
     '"A study with three independent generator-training seeds", "Similar aggregate means mask a hit-pattern discrepancy",')
swap('main.tex',
     'Paired sampling intervals for the headline structural means are not retained. Large descriptive differences do not establish robustness across training seeds, thresholds or graphs. Three independent generator-training seeds and a full-data fit are needed to separate architecture effects from training-population and optimization effects. Classifier scores cannot supply the missing structural significance: the condition-only control failed. A same-bank rerun must keep each matched pair in one partition.',
     'Paired sampling intervals for the headline structural means are not retained. Large descriptive differences do not establish robustness across training seeds, thresholds or graphs. A study with three independent generator-training seeds and a full-data fit is needed to separate architecture effects from training-population and optimization effects. The failed condition-only classifier control is a separate limitation: the quoted classifier scores cannot supply the missing structural significance. A rerun that keeps each matched pair in one partition is needed on the same validation bank.')
swap('README.md',
     'A final release audit additionally requires a hash-matched visual-review record and rejects stale source/PDF hashes.',
     'A final release audit additionally requires a hash-matched visual-review record and rejects stale source/PDF hashes. Page count has no upper or editorial target; the QA renders and checks every page, and the final visual review assesses content and layout directly.')
with (ROOT / 'STATUS.md').open('a', encoding='utf-8') as handle:
    handle.write('\n## Content-first pagination policy, 2 October 2026\n\n'
                 'The author clarified that there is no hard page cap. The previous 14-page upper assertion was removed, and the fuller Sec. 6.2 explanation was restored. The earlier 15-page QA failure remains historical evidence of the superseded rule, not a defect in manuscript content. Current QA still requires a valid nonempty PDF and checks every rendered page for text extraction, margins, ink, clipping and unresolved LaTeX issues. The current release hash binding and all-page review are recorded in `audit/content_first_pages_20261002/`.\n')
record('Current-status pagination rule documented', {'status_sha256': sha(ROOT / 'STATUS.md'),
                                                     'historical_record': 'Prior QA15 page-count failure retained unchanged.'})
pointer = ROOT / 'audit/finalization_20260930.json'
data = json.loads(pointer.read_text(encoding='utf-8'))
data['current_main_tex_sha256'] = sha(ROOT / 'main.tex')
data['content_first_pages_20261002'] = 'audit/content_first_pages_20261002/events.json'
pointer.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
with pointer.with_suffix('.md').open('a', encoding='utf-8') as handle:
    handle.write('\nThe author removed the arbitrary upper page cap and restored the fuller Sec. 6.2 caveat. Current main source SHA-256: '
                 + data['current_main_tex_sha256'] + '. See `audit/content_first_pages_20261002/`.\n')
record('Review pointer synchronized', {'main_tex_sha256': data['current_main_tex_sha256'],
                                       'pointer_sha256': sha(pointer),
                                       'pointer_twin_sha256': sha(pointer.with_suffix('.md'))})
print('Removed upper page assertion; restored fuller structural limitation; current documentation and pointer updated.')
