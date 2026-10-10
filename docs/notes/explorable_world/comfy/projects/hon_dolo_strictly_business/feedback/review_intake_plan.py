"""Read-only review intake plan. Writes no files and never deletes media.

Run from any directory with Python: python review_intake_plan.py
An optional first argument selects another exported cfa-visual-review-v1 JSON.
Without an argument, discover docs/notes/cfa-review.json and only immediate
cfa-review*.json files in docs/notes/downloads. Rank by timezone-aware exported
timestamp, or file modification time when that timestamp is absent/invalid.
An invalid newest candidate blocks intake rather than silently using an older
snapshot. Every discovered candidate and its selection evidence is reported.
Review the plan before applying it. A saved snapshot may predate later explicit
user instructions; those instructions must be reconciled separately.
"""
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json
import sys


class SnapshotSelectionError(ValueError):
    def __init__(self, message, selection):
        super().__init__(message)
        self.selection = selection


def _candidate(path):
    info = {'path': str(path), 'valid': False, 'errors': [], 'warnings': []}
    original, review = None, None
    try:
        modified = path.stat().st_mtime
        info['modified_at_utc'] = datetime.fromtimestamp(modified, timezone.utc).isoformat()
        info['timestamp_basis'] = 'file_mtime'
        info['selection_timestamp_utc'] = info['modified_at_utc']
        original = path.read_bytes()
        review = json.loads(original)
        if not isinstance(review, dict):
            raise ValueError('Review must be a JSON object.')
        info['exported'] = review.get('exported')
        exported = review.get('exported')
        try:
            parsed = datetime.fromisoformat(exported) if isinstance(exported, str) else None
            if parsed is None or parsed.tzinfo is None or parsed.utcoffset() is None:
                raise ValueError('Missing or timezone-less exported timestamp.')
            info['selection_timestamp_utc'] = parsed.astimezone(timezone.utc).isoformat()
            info['timestamp_basis'] = 'exported'
        except (ValueError, OverflowError):
            info['warnings'].append('Missing/invalid timezone-aware exported timestamp; using file modification time.')
        if review.get('format') != 'cfa-visual-review-v1':
            raise ValueError('Unsupported review format.')
        for field in ('items', 'favorites'):
            records = review.get(field, [])
            if not isinstance(records, list) or not all(isinstance(rec, dict) for rec in records):
                raise ValueError(f'{field} must be a list of record objects.')
        info['valid'] = True
    except (OSError, ValueError, UnicodeError) as exc:
        info['errors'].append(f'{type(exc).__name__}: {exc}')
    return info, original, review


def select_snapshot(root, explicit=None):
    canonical = root / 'docs/notes/cfa-review.json'
    inbox = root / 'docs/notes/downloads'
    selection = {
        'mode': 'explicit_path' if explicit is not None else 'bounded_auto_discovery',
        'policy': 'Newest timezone-aware exported timestamp; otherwise file mtime. Newest invalid candidate blocks; older invalid candidates are reported, not applied.',
        'search_locations': [] if explicit is not None else [str(canonical), str(inbox / 'cfa-review*.json')],
        'candidates': [],
    }
    if explicit is not None:
        paths = [Path(explicit).resolve()]
    else:
        paths = ([canonical] if canonical.is_file() else [])
        paths += sorted(p for p in inbox.glob('cfa-review*.json') if p.is_file())
    if not paths:
        raise SnapshotSelectionError('No review snapshot found in the canonical path or repo downloads inbox; no changes made.', selection)
    candidates = [_candidate(path) for path in paths]
    # Unknown freshness (e.g. failed stat) cannot safely be treated as an old file.
    candidates.sort(key=lambda c: (c[0].get('selection_timestamp_utc', '9999'), c[0].get('modified_at_utc', ''), c[0]['path']), reverse=True)
    selection['candidates'] = [c[0] for c in candidates]
    chosen, original, review = candidates[0]
    selection['selected_source'] = chosen['path']
    for info, _, _ in candidates:
        info['selected'] = info is chosen
        info['disposition'] = 'selected' if info is chosen else ('older_valid_not_selected' if info['valid'] else 'older_invalid_not_selected')
    if not chosen['valid']:
        raise SnapshotSelectionError('Selected review snapshot is invalid; no fallback to an older file and no changes made. Correct it or pass an explicit valid path.', selection)
    selection['reason'] = 'Explicit CLI path overrides discovery.' if explicit is not None else 'Latest candidate by the reported timestamp policy.'
    return Path(chosen['path']), original, review, selection


def main(argv=None):
    script = Path(__file__).resolve()
    root = next(p for p in script.parents if (p / 'AGENTS.md').is_file())
    argv = sys.argv[1:] if argv is None else argv
    try:
        source, original, review, selection = select_snapshot(root, argv[0] if argv else None)
    except SnapshotSelectionError as exc:
        print(json.dumps({'mode': 'plan_only_no_writes_no_deletions', 'application_allowed': False,
                          'errors': [{'error': str(exc)}], 'source_selection': exc.selection}, indent=2, ensure_ascii=False))
        return 2
    catalog_path = root / 'docs/notes/explorable_world/comfy/projects/visual_library/catalog.js'
    catalog = json.loads(catalog_path.read_text(encoding='utf-8').split('=', 1)[1].strip().rstrip(';'))
    assets = {a['id']: a for a in catalog['assets']}
    errors, verified, cache = [], [], {}
    records = review.get('items', []) + review.get('favorites', [])
    for rec in records:
        aid = rec.get('id')
        a = assets.get(aid)
        if not a or not a.get('sha256') or rec.get('sha256') != a.get('sha256'):
            errors.append({'id': aid, 'error': 'ID not found, catalog SHA256 missing, or export SHA256 differs from catalog'})
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
        'source_selection': selection,
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
