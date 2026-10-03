"""Evidence log for removing the editorial page cap."""
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
    for output in [HERE / 'events.md', ROOT / 'logs.md']:
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
    record('Content-first pagination correction started', {
        'user_direction': 'There is no need for a hard page cap; content matters.',
        'environment': {'platform': platform.platform(), 'python': sys.version},
        'input_sha256': {name: sha(ROOT / name) for name in
                         ['main.tex', 'scripts/full_manuscript_qa.py', 'STATUS.md',
                          'audit/finalization_20260930.json', 'output/fast_mc_zdc_manuscript.pdf']},
        'baseline': 'QA17 passed 22 groups with 14 pages after a prior paragraph was shortened to satisfy a 14-page assertion. Eight raw/historical text files from the previous publication remain local and untracked; preserve them.',
        'scope': 'Remove only the unjustified upper page limit, restore the fuller structural-limitation explanation, rebuild, inspect every resulting page, synchronize release evidence and GitHub.',
        'scientific_boundary': 'Do not alter numerical results, equations, tables, graph definitions, data or physics claims.'
    })
