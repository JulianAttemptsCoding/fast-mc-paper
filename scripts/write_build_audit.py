"""Release only a PDF bound to current source, automated QA and visual review."""
from __future__ import annotations
import json
import platform
import sys
from datetime import datetime, timezone
from full_manuscript_qa import ROOT, PDF, FIGURE_MANIFEST, release_source_hashes, sha256


def validate_binding(qa, visual, sources, pdf_hash, figure_hash):
    if qa.get('result') != 'pass' or qa.get('full_suite') is not True:
        raise ValueError('Latest QA attempt did not pass the complete automated suite')
    if qa.get('source_sha256') != sources:
        raise ValueError('QA source hashes are stale; rerun the complete suite')
    if qa['pdf']['sha256'] != pdf_hash:
        raise ValueError('QA PDF hash is stale')
    if qa.get('figures_manifest_sha256') != figure_hash:
        raise ValueError('QA figure manifest is stale')
    if visual.get('result') != 'pass' or visual.get('pdf_sha256') != pdf_hash:
        raise ValueError('A passing visual review of this exact PDF is required')
    expected = {str(p['page']): p['sha256'] for p in qa['page_metrics']}
    if visual.get('page_sha256') != expected:
        raise ValueError('Visual review must cover every current rendered page')


def main():
    records = sorted((ROOT / 'audit/iterations').glob('iteration_*.json'))
    if not records:
        raise ValueError('No automated QA record')
    latest = records[-1]
    qa = json.loads(latest.read_text(encoding='utf-8'))
    visual_path = ROOT / 'audit/visual_review_20260922.json'
    visual = json.loads(visual_path.read_text(encoding='utf-8'))
    sources = release_source_hashes()
    validate_binding(qa, visual, sources, sha256(PDF), sha256(FIGURE_MANIFEST))
    payload = {
        'schema_version': 4, 'created_utc': datetime.now(timezone.utc).isoformat(),
        'release': 'v0.6.0', 'status': 'exploratory HEP/computational-physics case study',
        'claim': 'On the specified development bank, one pilot checkpoint has similar mean occupancies but a later longitudinal reach and a more disconnected strict-positive support on the model graph.',
        'output': {'path': str(PDF.relative_to(ROOT)), 'sha256': sha256(PDF), 'bytes': PDF.stat().st_size, 'pages': qa['pdf']['pages']},
        'current_qa': {'record': str(latest.relative_to(ROOT)), 'sha256': sha256(latest), 'checks': qa['checks'],
                       'visual_record': str(visual_path.relative_to(ROOT)), 'visual_sha256': sha256(visual_path)},
        'historical_qa': 'Earlier records are preserved; no pass count is used as evidence for this output.',
        'environment': {'platform': platform.platform(), 'python': sys.version},
        'source_sha256': sources, 'figures_manifest_sha256': sha256(FIGURE_MANIFEST),
        'research_boundary': 'No new training, test-data use or model evaluation. Aggregate arithmetic and source provenance were audited; physics fidelity was not established.',
        'remaining_publication_actions': ['Author/collaborator approval of authorship and acknowledgments', 'Confirm data-release permissions and immutable archival version'],
        'broader_claim_requirements': 'See STATUS.md; these do not negate the descriptive case-study observation.'}
    (ROOT / 'audit/final_build_audit.json').write_text(json.dumps(payload, indent=2)+'\n', encoding='utf-8')
    text = ('# Final manuscript build audit\n\nVersion 0.6.0; '+payload['created_utc']+'.\n\n'
            +'PDF: `'+payload['output']['path']+'`; '+str(payload['output']['pages'])+' pages.\n\n'
            +'SHA-256: `'+payload['output']['sha256']+'`.\n\n'
            +'The complete automated suite in `'+str(latest.relative_to(ROOT))+'` and an every-page visual review match the current PDF and source hashes. '
            +'Historical QA records are not counted as validation of this revision.\n\n'
            +'The supported claim is that one pilot checkpoint has similar mean occupancies but a later longitudinal reach and a more disconnected strict-positive support on the model graph. '
            +'This build audit establishes document consistency and rendering checks, not statistical significance, physics fidelity, or submission approval. '
            +'See STATUS.md and the claim register for evidence boundaries.\n')
    (ROOT / 'audit/final_build_audit.md').write_text(text,encoding='utf-8')
    print('Release audit: exact source/PDF/figure and every-page visual binding PASS')


if __name__ == '__main__':
    main()
