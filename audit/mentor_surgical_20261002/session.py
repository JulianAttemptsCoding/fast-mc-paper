"""Command and evidence log for the mentor pre-submission corrections."""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def record(event: str, detail: dict) -> None:
    path = HERE / 'events.json'
    rows = json.loads(path.read_text(encoding='utf-8')) if path.exists() else []
    row = {'utc': datetime.now(timezone.utc).isoformat(), 'event': event, 'detail': detail}
    rows.append(row)
    path.write_text(json.dumps(rows, indent=2) + '\n', encoding='utf-8')
    prose = '\n## ' + event + '\n\n' + row['utc'] + '\n\n```json\n' + json.dumps(detail, indent=2) + '\n```\n'
    for output in (HERE / 'events.md', ROOT / 'logs.md'):
        with output.open('a', encoding='utf-8') as handle:
            handle.write(prose)


def run(args: list[str]) -> int:
    record('Command started', {'argv': args})
    result = subprocess.run(args, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    output = HERE / ('command_' + str(len(json.loads((HERE / 'events.json').read_text()))).zfill(3) + '.txt')
    output.write_text(result.stdout + '\nSTDERR\n' + result.stderr, encoding='utf-8')
    record('Command completed', {'argv': args, 'exit_code': result.returncode,
                                 'output': str(output.relative_to(ROOT)), 'output_sha256': sha(output)})
    print(result.stdout[-4500:])
    print(result.stderr[-1500:])
    return result.returncode


if __name__ == '__main__':
    if len(sys.argv) > 1:
        sys.exit(run(sys.argv[1:]))
    record('Mentor surgical edit started', {
        'scope': 'Classifier input, Figure 4 terminology, test-partition scope, generator-seed wording, screening criterion, abstract prose, and live repository metadata.',
        'environment': {'platform': platform.platform(), 'python': sys.version},
        'inputs_sha256': {name: sha(ROOT / name) for name in
                          ['main.tex', 'scripts/reader_figures.py', 'scripts/full_manuscript_qa.py',
                           'README.md', 'CITATION.cff', 'output/fast_mc_zdc_manuscript.pdf']},
        'pre_logger_commands': [
            'Read project implementation guide; graft check reported fresh graph; graft ask located manuscript release workflow (27,339 tokens saved).',
            'Read local working state, exact target sentences, figure-generation source and QA guard; verified archived classifier source uses kinetic.reshape(-1, 1).',
            'Web-opened the live GitHub repository, README and CITATION.cff; git ls-remote main and origin/main both identify 13ae8adc.',
            'gh CLI unavailable; read-only git remote and GitHub pages show live README/CITATION title differs from PDF, while live CITATION version is already 0.22.1.',
        ],
        'scientific_boundary': 'Editorial and figure-label changes only; retain all data, numbers, equations, figure scales, calibration and statistical caveats.'
    })
