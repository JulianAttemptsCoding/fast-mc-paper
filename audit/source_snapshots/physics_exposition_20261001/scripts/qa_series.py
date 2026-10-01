"""Resolve immutable, separately numbered QA series without legacy fallback."""
from pathlib import Path
import hashlib
import json
import re

def series_paths(root: Path):
    marker = root / 'audit/current_qa_series.json'
    if not marker.exists():
        return root / 'audit/iterations', root / 'audit/qa_runs'
    spec = json.loads(marker.read_text(encoding='utf-8'))
    name = spec['series']
    if not isinstance(name, str) or not re.fullmatch(r'[a-z][a-z0-9_]{0,79}', name):
        raise ValueError('Invalid QA series name')
    predecessor = (root / spec['predecessor']).resolve()
    if not predecessor.is_relative_to((root / 'audit').resolve()):
        raise ValueError('QA predecessor must be inside audit')
    if hashlib.sha256(predecessor.read_bytes()).hexdigest() != spec['predecessor_sha256']:
        raise ValueError('QA predecessor hash mismatch')
    return root / 'audit/qa_series' / name, root / 'audit/qa_runs' / name
