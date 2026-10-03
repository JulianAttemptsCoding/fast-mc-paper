"""Retain the failed pagination artifact before another build replaces it."""
import shutil
import subprocess
from session import ROOT, HERE, record, sha

folder = HERE / 'quarantined_qa15'
folder.mkdir(exist_ok=True)
pdf = ROOT / 'output/fast_mc_zdc_manuscript.pdf'
shutil.copy2(pdf, folder / pdf.name)
shutil.copy2(ROOT / 'main.tex', folder / 'main.tex')
result = subprocess.run(['pdftotext', '-layout', str(pdf), '-'], capture_output=True,
                        text=True, encoding='utf-8', errors='replace', check=True)
(folder / 'extracted.txt').write_text(result.stdout, encoding='utf-8')
parts = [x for x in result.stdout.split('\f') if x.strip()]
for n, part in enumerate(parts, 1):
    print(n, len(part), part.strip()[:110].replace('\n', ' ').encode('ascii', 'replace').decode('ascii'))
record('QA15 page overflow quarantined', {
    'pdf_sha256': sha(pdf), 'source_sha256': sha(ROOT / 'main.tex'),
    'failed_qa': 'audit/qa_series/mentor_send_20261002/iteration_15.json',
    'pages': len(parts), 'quarantine': str(folder.relative_to(ROOT)),
    'failed_inspection_commands': ['A prior python -c inspection command had a PowerShell quoting syntax error; it did not alter files.',
                                   'First quarantine helper copied the failed files but stopped before logging because Windows console could not encode a minus sign in extracted text. This retry records the copies.'],
    'diagnosis': 'Additional explanatory lines shifted the appendix and references past the unchanged 14-page limit.'
})
