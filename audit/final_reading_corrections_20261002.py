"""Apply final visual-review fixes and refresh the exact-source review binding."""
import hashlib
import json
import re
from pathlib import Path

root = Path(__file__).resolve().parents[1]
work = Path('C:/Users/Julia/OneDrive/Desktop/coding/ASIoP/Fast MC CBSC')
path = root / 'main.tex'
tex = path.read_bytes().decode('utf-8')
before = hashlib.sha256(path.read_bytes()).hexdigest()
blocks = list(re.finditer(r'\\begin\{figure\}\[!htbp\][\s\S]*?\\end\{figure\}', tex))
assert len(blocks) == 2
for match in reversed(blocks):
    block = match.group()
    assert sum(name in block for name in ['longitudinal_profile.png', 'support_summary.png']) == 1
    block = block.replace(r'\begin{figure}[!htbp]', '\\begin{center}\n\\begin{minipage}{\\linewidth}')
    block = block.replace(r'\caption{', r'\captionof{figure}{')
    block = block.replace(r'\end{figure}', '\\end{minipage}\n\\end{center}')
    tex = tex[:match.start()] + block + tex[match.end():]
tex = tex.replace(r'0.073\,\GeV', r'0.073\GeV')
anchor = r'\setlist{nosep,leftmargin=*}'
assert tex.count(anchor) == 1
tex = tex.replace(anchor, anchor + '\n\\widowpenalty=10000\n\\clubpenalty=10000')
path.write_bytes(tex.encode('utf-8'))
after = hashlib.sha256(path.read_bytes()).hexdigest()
finalization = root / 'audit/finalization_20260930.json'
data = json.loads(finalization.read_text(encoding='utf-8'))
data['current_main_tex_sha256'] = after
finalization.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
response_path = root / 'audit/claude_review_response_20261002.json'
response = json.loads(response_path.read_text(encoding='utf-8'))
response['current_main_sha256'] = after
response['failed_attempts'] += ['Release preparation stopped after a CRLF-specific matcher failure; completed remaining operations without replaying applied edits. First resume invocation lacked __file__; corrected before any resume writes.', 'QA01 passed 21 automated groups; complete page review found Figure 3 inserted between halves of one sentence and a one-line widow. Replaced the two floating figure environments with anchored minipages and suppressed one-line widows/orphans.']
response['status'] = 'Whole-document source and QA01 visual review complete; final source-bound QA pending after layout correction'
response_path.write_text(json.dumps(response, indent=2) + '\n', encoding='utf-8')
(work / 'audit/manuscript_claude_review_response_20261002.json').write_bytes(response_path.read_bytes())
record = {'command': 'python -X utf8 audit/final_reading_corrections_20261002.py', 'before_main_sha256': before, 'after_main_sha256': after, 'review': 'All 13 QA01 pages directly inspected; prose, equations, numbers, figures and citations read in sequence.', 'correction': 'Anchor both result figures at paragraph boundaries; eliminate figure-interrupted sentence and prevent one-line widow/orphan.', 'native_compile': 'Failed at platform initialization: Unable to find standard directories for platform', 'qa01': '21 groups passed; 10 release-guard tests passed', 'scope': 'Document QA, not physics validation'}
for base, name in [(root, 'claude_review_final_reading_20261002'), (work, 'manuscript_claude_review_final_reading_20261002')]:
    dest = base / 'audit' / name
    dest.with_suffix('.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
    dest.with_suffix('.md').write_text('# Final reading corrections\n\nAll 13 QA01 pages were directly inspected. Numeric and source checks passed; visual review found a figure interrupting a sentence and a one-line widow. Both result figures are now anchored at paragraph boundaries, and one-line widows/orphans are suppressed. Native editor compiler failed at platform initialization; local pdfLaTeX/Biber and 10 guard tests passed. Rebuild and repeat visual binding before release.\n', encoding='utf-8')
    with (base / 'logs.md').open('a', encoding='utf-8') as handle:
        handle.write('\n2026-10-02 QA01: 21 full-suite groups and 10 guard tests passed. All 13 pages directly inspected; figure interrupted sentence and one-line widow found. Anchored result figures and set widow/orphan penalties. Source ' + after + '. Native compiler initialization failed; local build works. Release-preparation CRLF matcher and missing __file__ retry failures recorded in response audit. See audit/' + name + '.json.\n')
print(after)
