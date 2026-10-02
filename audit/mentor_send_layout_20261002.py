"""Second mentor-send pass: restore page flow after QA01 and unify three terms.

QA01 passed all groups at 14 pages, but every-page reading found white gaps on
pages 1, 6 and 7: the abstract had grown by one line, which pushed Section 2 to
page 2 and cascaded. Counted byte replacements only; no equation or table body.
"""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
QA01_MAIN = 'f7cd95b92f49c5209b763c622edd4b6ec9cf49ecef49baf0e8f2e7de5f07b54c'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def replace(path, old, new, count=1):
    raw = path.read_bytes()
    found = raw.count(old.encode('utf-8'))
    assert found == count, (path.name, old[:70], found)
    path.write_bytes(raw.replace(old.encode('utf-8'), new.encode('utf-8')))


tex = ROOT / 'main.tex'
assert sha(tex) == QA01_MAIN, 'Run once, on the QA01 source'
EDITS = [
    ('abstract length',
     r"differs by only 0.25 (54.83 generated versus 54.58 Geant4, of 65 layers)",
     r"differs by 0.25 (54.83 generated versus 54.58 Geant4, of 65 layers)"),
    ('abstract length',
     r"(AUROC 0.775, where 0.5 is chance), but its control using incident conditions alone gives 0.464 rather than 0.5, so the score",
     r"(AUROC 0.775), but its control using incident conditions alone gives 0.464 rather than the chance value 0.5, so the score"),
    ('evaluation',
     r"and $A_\ell$ their activity indicator.",
     r"and $A_\ell$ the activity indicator of layer $\ell$."),
    ('numerical checks',
     r"verifies that FP32 decoding created",
     r"verifies that single-precision (FP32) decoding created"),
    ('longitudinal activity',
     r"The nonempty fraction starting in ECAL is 92.53\% versus 93.81\%.",
     r"The nonempty fraction starting in ECAL is 92.53\% for the generator versus 93.81\% for Geant4."),
    ('longitudinal activity',
     r"versus a 0.155-layer Geant4 half-split scale.",
     r"versus a 0.155-layer reference-half scale."),
    ('longitudinal activity',
     r"The half-split is a descriptive scale, not a significance threshold;",
     r"The reference-half scale is descriptive, not a significance threshold;"),
]
for _, old, new in EDITS:
    replace(tex, old, new)
replace(ROOT / 'scripts/mentor_send_checks.py', "'where 0.5 is chance'", "'rather than the chance value 0.5'")
replace(ROOT / 'scripts/mentor_send_checks.py', "'Dr.~Wen-Chen Chang',",
        "'Dr.~Wen-Chen Chang', 'the activity indicator of layer $\\\\ell$', 'single-precision (FP32) decoding',\n        '0.155-layer reference-half scale', '92.53\\\\% for the generator versus 93.81\\\\% for Geant4',")

path = ROOT / 'audit/finalization_20260930.json'
data = json.loads(path.read_text(encoding='utf-8'))
data['current_main_tex_sha256'] = sha(tex)
path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')

response = ROOT / 'audit/mentor_send_response_20261002.json'
payload = json.loads(response.read_text(encoding='utf-8'))
payload['current_main_sha256'] = sha(tex)
payload['second_pass'] = {
    'created_utc': datetime.now(timezone.utc).isoformat(), 'qa01_main_sha256': QA01_MAIN,
    'finding': 'QA01 passed 22 groups at 14 pages. Every-page reading found white gaps on pages 1, 6 and 7 caused by a one-line longer abstract, plus three wording inconsistencies.',
    'layout_probe': 'Scratch-copy pdfLaTeX builds: page fill before 0.82/0.92/0.83/0.90/0.92/0.81/0.77; after 0.92/0.92/0.92/0.92/0.92/0.91/0.88. Relaxing the nine-line reservation before the hit-pattern paragraph made no difference and was not applied.',
    'replacements': [{'section': section, 'old_sha256': hashlib.sha256(old.encode()).hexdigest(), 'new': new} for section, old, new in EDITS],
}
payload['failed_attempts'] = ['QA01 layout: abstract grew to twelve lines and displaced Section 2; corrected by shortening two abstract clauses without removing a number.']
response.write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
with response.with_suffix('.md').open('a', encoding='utf-8', newline='\n') as handle:
    handle.write('\n## Second pass after QA01\n\nQA01 passed at 14 pages, but reading every page showed white gaps on pages 1, 6 and 7. The abstract had grown by one line and displaced Section 2. Two abstract clauses were shortened without removing a number, restoring the page flow. The same pass unified half-split with reference-half scale, named both samples in the ECAL-start sentence, expanded FP32 once, and fixed the activity-indicator wording.\n')
print(json.dumps({'source_sha256': sha(tex), 'replacements': len(EDITS)}, indent=2))
