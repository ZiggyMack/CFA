"""Read-only review intake plan. Writes no files and never deletes media.

Run from any directory with Python: python review_intake_plan.py
An optional first argument selects another exported cfa-visual-review-v1 JSON.
Review the plan before applying it. A saved snapshot may predate later explicit
user instructions; those instructions must be reconciled separately.
"""
from pathlib import Path
import hashlib
import json
import sys


def main():
    script = Path(__file__).resolve()
    root = next(p for p in script.parents if (p / 'AGENTS.md').is_file())
    source = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else root / 'docs/notes/cfa-review.json'
    original = source.read_bytes()
    review = json.loads(original)
    if review.get('format') != 'cfa-visual-review-v1':
        raise ValueError('Unsupported review format; no changes made.')
    catalog_path = root / 'docs/notes/explorable_world/comfy/projects/visual_library/catalog.js'
    catalog = json.loads(catalog_path.read_text(encoding='utf-8').split('=', 1)[1].strip().rstrip(';'))
    assets = {a['id']: a for a in catalog['assets']}
    errors, verified, cache = [], [], {}
    records = review.get('items', []) + review.get('favorites', [])
    for rec in records:
        aid = rec.get('id')
        a = assets.get(aid)
        if not a or rec.get('sha256') != a.get('sha256'):
            errors.append({'id': aid, 'error': 'ID not found or export SHA256 differs from catalog'})
            continue
        path = (root / a['repoPath']).resolve()
        if not path.is_relative_to(root):
            errors.append({'id': aid, 'error': 'Catalog path escapes repository'})
            continue
        if path not in cache:
            cache[path] = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
        if cache[path] != a['sha256']:
            errors.append({'id': aid, 'error': 'Disk bytes missing or hash mismatch'})
            continue
        verified.append(aid)
    plan = {
        'mode': 'plan_only_no_writes_no_deletions',
        'source': str(source),
        'source_exported': review.get('exported'),
        'source_sha256': hashlib.sha256(original).hexdigest(),
        'verified_record_count': len(verified),
        'errors': errors,
        'user_record_candidates': [r for r in review.get('items', []) if r.get('origin') == 'user'],
        'ignored_catalog_origin_ids': [r['id'] for r in review.get('items', []) if r.get('origin') == 'catalog'],
        'unknown_origin_ids': [r.get('id') for r in review.get('items', []) if r.get('origin') not in ('user', 'catalog')],
        'favorite_snapshot': review.get('favorites', []),
        'application_allowed': False,
        'next_step': 'Human/agent reconciliation with later direct user instructions; merge only explicit user records after validation. Do not overwrite newer canonical decisions with stale catalog seeds.'
    }
    if source.read_bytes() != original:
        plan['source_changed_during_read'] = True
        plan['errors'].append({'error': 'Autosave changed; re-read before applying any plan'})
    print(json.dumps(plan, indent=2, ensure_ascii=False))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
