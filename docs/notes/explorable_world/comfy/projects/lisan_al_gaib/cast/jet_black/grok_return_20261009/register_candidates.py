"""Append verified CUR candidates to the existing Jet Black registry; no build."""
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'AGENTS.md').is_file())
REGISTRY = HERE.parents[1] / 'registry.json'
GROUPS = {
    '01_CHARACTER_REFS': ('references', 'Jet Black · received reference candidates', 'Cosmic-avatar head/reference exploration; source head-shape tags are proposals. Existing user references remain authoritative.'),
    '02_TURNAROUND_MOODS_SETTINGS': ('moods', 'Jet Black · moods and turnarounds', 'Mood and view candidates with known suit drift. Related images include two byte-identical reference/turnaround aliases stored once.'),
    '03_SCENES_50_ORB_HELMET': ('scenes', 'Jet Black · orb and helmet scenes', '25 scene ideas in two head variants; 50 supplied images. Provider head/storybeat labels remain attributed, not approvals.'),
    '04_STORYBOARD_75': ('saga', 'Jet Black · saga storyboard proposals', 'Five proposed arcs, 75 source frames. User watcher role remains authoritative; story, powers, timing and head choices are not approved.'),
    '05_LISAN_SCENES': ('with-lisan', 'Jet Black · received scene with Lisan', 'Scene context; Lisan tattoo/face drift is documented. Neither character identity is replaced.'),
    '90_SUPERSEDED': ('history', 'Jet Black · superseded return history', 'Seven provider-superseded variants retained for lineage and comparison, excluded from current reference selection.'),
}


def main():
    raw = REGISTRY.read_bytes()
    registry = json.loads(raw)
    receipt = json.loads((HERE / 'received/intake_receipt.json').read_text(encoding='utf-8'))
    cleanup = json.loads((HERE / 'cleanup_receipt.json').read_text(encoding='utf-8-sig'))
    assert receipt['state'] == 'verified_hash_size_decode_complete_extracted_batch'
    assert cleanup['state'] == 'complete'
    marker = HERE / 'registration_receipt.json'
    if marker.exists():
        raise ValueError('Registration receipt exists; inspect rather than duplicate.')
    original_refs = list(registry['characters'][0]['referenceAssetIDs'])
    original_assets = [dict(a) for a in registry['assets']]
    by_sha = defaultdict(list)
    for row in receipt['occurrences']:
        if row['kind'] == 'image':
            by_sha[row['sha256']].append(row)
    new_assets, related = [], defaultdict(list)
    for sha, rows in by_sha.items():
        first = rows[0]
        path = ROOT / first['canonical_path']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == sha
        assert not any(a['sha256'] == sha for a in registry['assets'])
        aid = 'LAG-JET-BLACK-DROP-' + sha[:12]
        assert not any(a['id'] == aid for a in registry['assets'])
        collection = first['member'].split('/')[0]
        key, _, _ = GROUPS[collection]
        provider = first.get('provider_mapping', {})
        contact = not bool(provider)
        title = ('Contact sheet · ' + Path(first['member']).stem.removeprefix('_CONTACT_').replace('_', ' ')) if contact else provider['id'] + ' · ' + provider['label'].replace('-', ' ').title()
        aliases = [{'member': r['member'], 'providerID': r.get('provider_mapping', {}).get('id'),
                    'providerStatus': (r.get('provider_mapping') or r.get('provider_index') or {}).get('status'),
                    'providerRecord': r.get('provider_mapping') or r.get('provider_index'),
                    'originalSourcePath': r['source_path'],
                    'currentSourcePath': r['source_path'].replace('references/From Grok/CUR-', 'references/From Grok/Processed/CUR-', 1)} for r in rows]
        note = ('Provider contact-sheet overview; cannot establish full-resolution or temporal fidelity. ' if contact else '')
        note += 'Unapproved received candidate. Jet Black remains the user-named watcher working for Lisan; provider Curator name/lore/head-default claims are proposals. '
        if provider.get('qa_note'):
            note += 'Provider QA: ' + provider['qa_note'] + '. '
        if collection == '90_SUPERSEDED':
            note += 'Superseded history; do not use as a current identity or outfit reference. '
        if provider.get('id') == 'CUR-REF-05':
            note += 'Head-shape proposal only; armoured jacket does not establish the suit. '
        if provider.get('id') == 'CUR-LAG-01':
            note += 'Lisan chin AL differs from current GAIB; scene context only. '
        if len(rows) > 1:
            note += 'Multiple provider filenames share these exact bytes; one canonical media record retains every alias. '
        a = {'id': aid, 'project': 'lisan', 'path': first['canonical_path'], 'title': title,
             'category': 'cast', 'album': 'lisan:cast-jet-black-cur-' + key,
             'characterID': 'LAG-JET-BLACK', 'sha256': sha, 'bytes': first['bytes'],
             'width': first['image']['width'], 'height': first['image']['height'],
             'tags': ['Jet Black', 'CUR-DROP-20261009A', 'needs user review', key] + ([provider['head']] if provider.get('head') else []) + (['contact sheet'] if contact else []),
             'sourceStatus': 'Received candidate, integrity verified; ' + (provider.get('status') or 'contact overview; unapproved'),
             'reviewStatus': 'needs_user_review', 'approval': None, 'note': note.strip(),
             'intakeID': receipt['intakeID'], 'sourceProvenance': {'provider': 'Grok', 'intakeReceipt': str((HERE / 'received/intake_receipt.json').relative_to(ROOT)).replace('\\', '/'), 'sourceAliases': aliases},
             'providerWorkingName': 'the Curator', 'isContactSheet': contact}
        new_assets.append(a)
        for alias in rows[1:]:
            other = GROUPS[alias['member'].split('/')[0]][0]
            if other != key:
                related[other].append(aid)
    assert len(new_assets) == 158
    new_albums = []
    for key, title, description in GROUPS.values():
        album_id = 'lisan:cast-jet-black-cur-' + key
        assert not any(a['id'] == album_id for a in registry['albums'])
        new_albums.append({'id': album_id, 'project': 'lisan', 'category': 'cast', 'title': title,
                           'description': description, 'related': related[key]})
    registry['assets'].extend(new_assets)
    registry['albums'].extend(new_albums)
    new_docs = []
    for row in receipt['unique_files']:
        if row['kind'] != 'document' or Path(row['canonical_path']).suffix.lower() == '.jsonl':
            continue
        member = row['members'][0]
        title = 'Grok CUR source · ' + member
        if member.endswith('DESIGN-LOCK.txt'):
            title += ' (historical provider text)'
        new_docs.append({'project': 'lisan', 'path': row['canonical_path'], 'title': title, 'album': 'Jet Black · raw provider return'})
    registry['documents'].extend(new_docs)
    registry['updatedAtUTC'] = datetime.now(timezone.utc).isoformat()
    assert registry['characters'][0]['referenceAssetIDs'] == original_refs
    assert registry['assets'][:len(original_assets)] == original_assets
    assert REGISTRY.read_bytes() == raw, 'Registry changed concurrently; retry after review.'
    encoded = (json.dumps(registry, indent=2, ensure_ascii=False) + '\n').encode('utf-8')
    REGISTRY.write_bytes(encoded)
    output = {'schema': 'cfa-cast-registration-receipt-v1', 'intakeID': receipt['intakeID'],
              'registeredAtUTC': registry['updatedAtUTC'], 'registry': str(REGISTRY.relative_to(ROOT)).replace('\\', '/'),
              'beforeSHA256': hashlib.sha256(raw).hexdigest(), 'afterSHA256': hashlib.sha256(encoded).hexdigest(),
              'newImageRecords': len(new_assets), 'newAlbums': len(new_albums), 'newRawDocumentLinks': len(new_docs),
              'sourceImageOccurrences': 160, 'uniqueSourceImages': 158, 'exactDuplicateOccurrences': 2,
              'originalReferenceAssetIDsPreserved': original_refs, 'originalTwoAssetRecordsUnchanged': True,
              'newApprovals': [], 'catalogRebuilt': False}
    marker.write_text(json.dumps(output, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
