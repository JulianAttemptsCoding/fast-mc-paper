"""Apply exact, auditable pre-mentor wording and Figure 4 label corrections."""
import json
import shutil
from session import ROOT, HERE, record, sha

before = HERE / 'before'
before.mkdir(exist_ok=True)
paths = ['main.tex', 'scripts/reader_figures.py', 'scripts/full_manuscript_qa.py',
         'README.md', 'STATUS.md', 'CITATION.cff', 'figures/support_summary.png',
         'output/fast_mc_zdc_manuscript.pdf', 'output/fast_mc_zdc_submission_source.zip',
         'audit/finalization_20260930.json', 'audit/finalization_20260930.md']
if not (before / 'main.tex').exists():
    for name in paths:
        dest = before / name
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / name, dest)
    record('Pre-edit source and deliverable snapshot', {'input_sha256': {name: sha(before / name) for name in paths},
                                                       'snapshot': str(before.relative_to(ROOT))})


def replace(path: str, changes: list[tuple[str, str]]) -> None:
    file = ROOT / path
    contents = file.read_bytes()
    crlf = b'\r\n' in contents
    for old, new in changes:
        old_bytes = old.encode('utf-8').replace(b'\n', b'\r\n') if crlf else old.encode('utf-8')
        new_bytes = new.encode('utf-8').replace(b'\n', b'\r\n') if crlf else new.encode('utf-8')
        if contents.count(old_bytes) == 0 and contents.count(new_bytes) >= 1:
            continue  # Already applied before an interrupted revision.
        assert contents.count(old_bytes) == 1, (path, old, contents.count(old_bytes))
        contents = contents.replace(old_bytes, new_bytes)
    if contents != file.read_bytes():
        file.write_bytes(contents)
    record('Surgical edit', {'file': path, 'sha256_before': sha(before / path),
                             'sha256_after': sha(file), 'replacements': changes})


replace('main.tex', [
    ('Their mean number is 23.42 for Geant4 and 59.39 for the generator.',
     'The mean group count is 23.42 for Geant4 and 59.39 for the generator.'),
    ('but its control using incident conditions alone gives 0.464',
     'but a control using incident kinetic energy alone gives 0.464'),
    ('These means miss a hit-pattern discrepancy.',
     'Similar aggregate means mask a hit-pattern discrepancy.'),
    ('No nominal test event is used here.',
     'No nominal-test event enters the analyses reported here; Appendix~\\ref{app:reproducibility} documents prior separate inspection of parts of that partition.'),
    ('Its condition-only AUROC of 0.464 is a failed control consistent with such bias, though the cause is unverified.',
     'The condition-only control uses incident kinetic energy alone; its AUROC of 0.464 is a failed control consistent with such bias, though the cause is unverified.'),
    ('recorded development-screening criterion of 0.65',
     'recorded screening criterion of 0.65'),
    ('A three-seed study and full-data fit are needed',
     'A study with three independent generator-training seeds and a full-data fit is needed'),
    ('All three high-level AUROCs exceed the recorded screening maximum of 0.65.',
     'All three high-level AUROCs exceed the recorded screening criterion of 0.65.'),
])
replace('scripts/reader_figures.py', [
    ('("last hit layer", report["activity"]["truth"]["mean_last_active_layer"]',
     '("last active layer", report["activity"]["truth"]["mean_last_active_layer"]'),
])
replace('scripts/full_manuscript_qa.py', [
    ('"high-level score exceeds the recorded development-screening criterion of 0.65"',
     '"high-level score exceeds the recorded screening criterion of 0.65"'),
    ('"No nominal test event is used"',
     '"No nominal-test event enters the analyses reported here"'),
    ('"104 retained rows spanning epochs 11--114", "defines the checkpoint analyzed below",',
     '"104 retained rows spanning epochs 11--114", "defines the checkpoint analyzed below",\n'
     '        "a control using incident kinetic energy alone gives 0.464", "The condition-only control uses incident kinetic energy alone",\n'
     '        "A study with three independent generator-training seeds", "Similar aggregate means mask a hit-pattern discrepancy",\n'
     '        "All three high-level AUROCs exceed the recorded screening criterion of 0.65",'),
    ('def validate_figures(checks: list[str]) -> None:\n    manifest = load_json(FIGURE_MANIFEST)',
     'def validate_figures(checks: list[str]) -> None:\n'
     '    figure_source = (ROOT / "scripts/reader_figures.py").read_text(encoding="utf-8")\n'
     '    assert \x27("last active layer", report["activity"]["truth"]["mean_last_active_layer"]\x27 in figure_source\n'
     '    assert "last hit layer" not in figure_source\n'
     '    manifest = load_json(FIGURE_MANIFEST)'),
])
replace('README.md', [
    ('the failed condition-only control and row-wise split prevent a calibrated fidelity interpretation.',
     'the failed classifier control using incident kinetic energy alone and the row-wise split prevent a calibrated fidelity interpretation.'),
])
with (ROOT / 'README.md').open('a', encoding='utf-8') as handle:
    handle.write('\n## Mentor pre-submission corrections, 2 October 2026\n\n'
                 'The manuscript now identifies the classifier control as incident kinetic energy alone, labels Figure 4(c1) as last active layer, distinguishes these analyses from earlier separate test-partition inspection, names generator-training seeds in the proposed replication, and uses one screening-criterion term. The repository title and citation metadata match the displayed manuscript title and version 0.22.1. See `audit/mentor_surgical_20261002/` for QA and publication evidence.\n')
record('README pre-submission note added', {'sha256_before': sha(before / 'README.md'), 'sha256_after': sha(ROOT / 'README.md')})
with (ROOT / 'STATUS.md').open('a', encoding='utf-8') as handle:
    handle.write('\n## Mentor pre-submission corrections, 2 October 2026\n\n'
                 'The classifier control uses incident kinetic energy alone. Figure 4(c1), test-partition scope, proposed independent generator-training seeds, and screening-criterion wording are synchronized across the paper. Numerical evidence, equations, tables, figure scales and scientific claims are unchanged. The current PDF and source package require a new hash-bound full QA and visual review after these edits; see `audit/mentor_surgical_20261002/`.\n')
record('STATUS pre-submission note added', {'sha256_before': sha(before / 'STATUS.md'), 'sha256_after': sha(ROOT / 'STATUS.md')})

pointer = ROOT / 'audit/finalization_20260930.json'
data = json.loads(pointer.read_text(encoding='utf-8'))
data['current_main_tex_sha256'] = sha(ROOT / 'main.tex')
data['mentor_surgical_20261002'] = 'audit/mentor_surgical_20261002/events.json'
pointer.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
with pointer.with_suffix('.md').open('a', encoding='utf-8') as handle:
    handle.write('\nThe 2 October mentor pre-submission wording corrections update the current main source pointer to '
                 + data['current_main_tex_sha256'] + '. See `audit/mentor_surgical_20261002/events.json`.\n')
record('Source-review pointer synchronized', {'current_main_tex_sha256': data['current_main_tex_sha256'],
                                              'pointer_sha256': sha(pointer),
                                              'pointer_twin_sha256': sha(pointer.with_suffix('.md'))})
print('Eight manuscript edits, Figure 4 source label, exact QA requirements and release documentation revised.')
