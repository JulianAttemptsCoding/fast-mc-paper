"""Record the mentor consistency review and its commands without event-data access."""
import hashlib
import json
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
NAME = 'mentor_consistency_20261002'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(event, details):
    path = ROOT / 'audit' / (NAME + '.json')
    data = json.loads(path.read_text()) if path.exists() else {
        'scope': 'Complete source/PDF consistency review for mentor discussion; aggregate evidence only.',
        'environment': {'python': sys.version, 'platform': platform.platform()},
        'initial_commit': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'new_event_data_access': False, 'new_model_evaluation': False, 'events': [],
    }
    item = {'utc': datetime.now(timezone.utc).isoformat(), 'event': event, 'details': details,
            'hashes': {p: sha(ROOT / p) for p in ['main.tex', 'references.bib', 'output/fast_mc_zdc_manuscript.pdf']}}
    data['events'].append(item)
    path.write_text(json.dumps(data, indent=2) + '\n', encoding='utf-8')
    md = '# Mentor consistency review, 2 October 2026\n\n'
    md += data['scope'] + '\n\n'
    for entry in data['events']:
        md += '## ' + entry['event'] + '\n\n' + entry['utc'] + '\n\n```json\n' + json.dumps(entry['details'], indent=2) + '\n```\n\n'
    path.with_suffix('.md').write_text(md.rstrip() + '\n', encoding='utf-8')
    with (ROOT / 'logs.md').open('a', encoding='utf-8') as stream:
        stream.write('\n### ' + item['utc'] + ' - ' + event + '\n\n' + json.dumps(details, ensure_ascii=True) + '\n\nEvidence: `audit/' + NAME + '.{json,md}`.\n')


if __name__ == '__main__':
    label, *command = sys.argv[1:]
    if command:
        record(label + ' started', {'command': command})
        result = subprocess.run(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
        out = ROOT / 'audit' / (NAME + '_' + label + '.txt')
        out.write_text(result.stdout, encoding='utf-8')
        record(label + ' completed', {'command': command, 'exit_code': result.returncode, 'output': str(out.relative_to(ROOT)), 'output_sha256': sha(out)})
        print(result.stdout[-9000:])
        raise SystemExit(result.returncode)
    record(label, {'status': 'recorded'})
