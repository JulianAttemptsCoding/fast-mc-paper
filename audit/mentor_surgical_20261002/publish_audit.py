"""Record direct remote verification of the mentor-ready paper revision."""
import json
import subprocess
from datetime import datetime, timezone
from session import ROOT, HERE, record, sha

commit = subprocess.run(['git', 'rev-parse', 'HEAD'], cwd=ROOT, capture_output=True,
                        text=True, check=True).stdout.strip()
remote_line = subprocess.run(['git', 'ls-remote', 'origin', 'refs/heads/main'], cwd=ROOT,
                             capture_output=True, text=True, check=True).stdout.strip()
remote_commit = remote_line.split()[0]
assert commit == remote_commit == '96aca45578ad16a40a00cf31d63ec200326f7bd3'
for name in ['main.tex', 'README.md', 'CITATION.cff', 'figures/support_summary.png',
             'output/fast_mc_zdc_manuscript.pdf', 'output/fast_mc_zdc_submission_source.zip']:
    blob = subprocess.run(['git', 'show', commit + ':' + name], cwd=ROOT,
                          capture_output=True, check=True).stdout
    assert blob == (ROOT / name).read_bytes(), name
qa = json.loads((ROOT / 'audit/qa_series/mentor_send_20261002/iteration_17.json').read_text())
assert qa['result'] == 'pass' and qa['pdf']['sha256'] == sha(ROOT / 'output/fast_mc_zdc_manuscript.pdf')
excluded = [
    'audit/final_review_20261002/command_015.txt',
    'audit/mentor_surgical_20261002/before/scripts/reader_figures.py',
    'audit/mentor_surgical_20261002/command_024.txt',
    'audit/mentor_surgical_20261002/command_027.txt',
    'audit/qa_series/mentor_send_20261002/iteration_09.md',
    'audit/qa_series/mentor_send_20261002/iteration_12.md',
    'audit/qa_series/mentor_send_20261002/iteration_13.md',
    'audit/qa_series/mentor_send_20261002/iteration_15.md'
]
payload = {
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'repository': 'https://github.com/JulianAttemptsCoding/fast-mc-paper',
    'release_commit': commit, 'remote_main_verified': remote_commit,
    'revision': '0.22.1',
    'output_sha256': {name: sha(ROOT / name) for name in
                      ['main.tex', 'figures/support_summary.png', 'output/fast_mc_zdc_manuscript.pdf',
                       'output/fast_mc_zdc_submission_source.zip', 'README.md', 'CITATION.cff']},
    'qa': 'QA17 full suite passed 22 groups, 14 pages; 10 guard regression tests passed; all final page pixels directly reviewed.',
    'web_verification': 'GitHub commit-specific README and CITATION.cff pages displayed the PDF title and version 0.22.1. The earlier fetched 0.5.0 claim was stale.',
    'excluded_raw_local_evidence': {name: sha(ROOT / name) for name in excluded},
    'exclusion_reason': 'Exact raw transcripts, source backup or immutable failed-attempt markdown retained locally because staged whitespace checks flagged their original bytes. QA JSON attempts and current review records were published; no QA assertion or whitespace policy was changed.',
    'mentor_submission': 'Not sent by this task.'
}
(HERE / 'publication.json').write_text(json.dumps(payload, indent=2) + '\n', encoding='utf-8')
(HERE / 'publication.md').write_text(
    '# Mentor-ready GitHub publication\n\n' + payload['created_utc'] + '\n\n'
    + 'Release commit: ' + commit + '. Remote main verified at this commit.\n\n'
    + 'The published README and CITATION.cff title match the PDF; citation version is 0.22.1. '
    + 'The final PDF, source archive, Figure 4, QA17 JSON and audit records are included.\n\n'
    + payload['qa'] + '\n\n' + payload['exclusion_reason'] + '\n\n'
    + 'The eight local-only raw/historical artifacts and their SHA-256 hashes are listed in the JSON twin. '
    + 'The manuscript has not been sent to the mentor.\n', encoding='utf-8')
record('GitHub release commit verified', payload)
print('GitHub release commit and exact published artifact bytes verified:', commit)
