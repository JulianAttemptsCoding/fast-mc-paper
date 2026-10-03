"""Record the verified publication of the content-first paper revision."""
from datetime import datetime, timezone
from pathlib import Path
import json
import subprocess

from session import ROOT, HERE, record, sha


def git(*args: str) -> str:
    return subprocess.check_output(['git', *args], cwd=ROOT, text=True).strip()


head = git('rev-parse', 'HEAD')
tracking = git('rev-parse', 'origin/main')
remote_line = git('ls-remote', 'origin', 'refs/heads/main')
remote = remote_line.split()[0]
assert head == tracking == remote, (head, tracking, remote)

qa = json.loads((ROOT / 'audit/qa_series/mentor_send_20261002/iteration_18.json').read_text(encoding='utf-8'))
review = json.loads((HERE / 'review.json').read_text(encoding='utf-8'))
assert qa['pdf']['pages'] == review['page_count'] == 15
assert review['result'] == 'pass'

data = {
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'repository': 'https://github.com/JulianAttemptsCoding/fast-mc-paper',
    'release_commit': head,
    'remote_main_verified': remote,
    'pdf_pages': qa['pdf']['pages'],
    'qa_groups_passed': len(qa['checks']),
    'guard_tests_passed': 10,
    'final_release_binding': 'PASS: QA18, visual review, source hashes, figure manifest, PDF, build audit and source archive match',
    'output_sha256': {name: sha(ROOT / name) for name in [
        'main.tex', 'scripts/full_manuscript_qa.py',
        'output/fast_mc_zdc_manuscript.pdf',
        'output/fast_mc_zdc_submission_source.zip',
    ]},
    'scientific_scope': 'No numerical results, equations, table bodies, data or physics claim changed.',
    'disposition': 'Removed arbitrary upper page limit; restored the fuller Sec. 6.2 limitation; all 15 actual pages reviewed.',
    'mentor_submission': 'Not sent by this task.',
}
(HERE / 'publication.json').write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
(HERE / 'publication.md').write_text(
    '# Content-first manuscript publication\n\n'
    f"- Release commit: `{head}` (verified on remote `main`).\n"
    f"- PDF: 15 pages; QA18 passed {len(qa['checks'])} groups; 10 guard tests passed.\n"
    '- Final source, PDF, archive, figures and visual review binding: PASS.\n'
    '- The page count has no editorial upper limit; each rendered page is checked.\n'
    '- The fuller Sec. 6.2 limitation is restored; numerical results and equations are unchanged.\n'
    '- Mentor submission was not performed by this task.\n',
    encoding='utf-8',
)
record('Content-first manuscript publication verified', data)
print('PASS', head, qa['pdf']['pages'], len(qa['checks']))
