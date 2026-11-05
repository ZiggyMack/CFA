"""Pinned, additive chain intake; reference scope never grants image acceptance."""
from collections import Counter
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
from urllib.parse import quote

PACKAGE = 'HD-CHAIN_winners_v002'
LIBRARY = 'docs/notes/explorable_world/comfy/projects/visual_library'
DROP = 'docs/notes/explorable_world/comfy/references/From Grok/' + PACKAGE
ALBUM_ID = 'hon:chain-winners-v002'
STYLES = ('A01', 'A04', 'A06', 'B05')
STALE_NOTE = 'Four interchangeable neck-chain styles: 24 first-round candidates planned; winner angles wait for selection.'
CURRENT_NOTE = 'Four neck-chain styles selected by Ziggy: A01, A04, A06 and B05. Sixteen received product-reference angles retain their individual reviews.'
PINS = {'MANIFEST.json': '5497505c204c347f2302596bc1d3c0b2eeeca9fd7b41c27e88a70f1690b31470', 'NOTES.md': 'cd202e09cfb05df943e771c3e07327b28b1596d9bae82ee94308b0d78404a472'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def intake_payload(repo_root):
    root = Path(repo_root).resolve()
    directory = root / DROP
    assert set(PINS) == {'MANIFEST.json', 'NOTES.md'}, 'Pinned intake evidence is missing'
    for name, expected in PINS.items():
        assert digest(directory / name) == expected, 'Chain intake evidence changed: ' + name
    manifest = json.loads((directory / 'MANIFEST.json').read_text(encoding='utf-8-sig'))
    rows = manifest['items']
    assert len(rows) == manifest['count'] == 16
    assert Counter(row['id'] for row in rows) == {f'HD-CHAIN-{style}': 4 for style in STYLES}
    assert len({row['file'] for row in rows}) == len({row['sha256'] for row in rows}) == 16
    assets, requests = [], []
    for row in rows:
        path = (directory / row['file']).resolve()
        assert path.parent == directory and path.suffix.lower() == '.jpg'
        assert row['needs_review'] is True and row['product_only'] is True
        assert digest(path) == row['sha256'], 'Original bytes changed: ' + row['file']
        angle = row['view'].split('_', 1)[0].upper()
        version = path.stem.rsplit('_', 1)[1]
        aid = row['id'] + '-' + angle + '-' + version
        url = quote(os.path.relpath(path, root / LIBRARY).replace('\\', '/'), safe='/')
        assets.append({'id': aid, 'project': 'hon', 'kind': 'image', 'category': 'details',
            'album': ALBUM_ID, 'title': row['id'] + ' · ' + row['view'].replace('_', ' '),
            'filename': path.name, 'src': url, 'thumb': url, 'repoPath': path.relative_to(root).as_posix(),
            'sha256': row['sha256'], 'bytes': path.stat().st_size,
            'sourceIntake': PACKAGE, 'sourceStatus': 'received_candidate', 'storyboardStage': 'preliminary',
            'chainStyleID': row['id'], 'referenceRole': 'Jewelry product reference',
            'tags': ['jewelry', 'neck chain', row['id'], row['view'], 'product reference'],
            'note': 'One of four chain styles selected by Ziggy. This exact product-reference angle still needs review; style selection does not accept the image or assign it to a shot.',
            'sourceEvidence': {'manifestPath': DROP + '/MANIFEST.json', 'manifestSHA256': PINS['MANIFEST.json'],
                'notesPath': DROP + '/NOTES.md', 'notesSHA256': PINS['NOTES.md'],
                'needsReview': True, 'productOnly': True, 'defects': row['defects']}})
        requests.append({'id': aid, 'sha256': row['sha256'], 'type': 'missing_decision',
            'project': 'hon', 'reviewControllerID': 'ziggy', 'requestedBy': 'Ziggy',
            'requestedAt': '2026-10-30', 'reason': 'Review this received chain-reference angle. The four style choices are preserved; no image acceptance, scene acceptance or shot assignment is implied.'})
    collections = []
    for style in STYLES:
        selected = [a for a in assets if a['chainStyleID'] == 'HD-CHAIN-' + style]
        collections.append({'id': 'hon:chain-' + style.lower(), 'project': 'hon',
            'title': 'Neck chain ' + style, 'coverID': selected[0]['id'],
            'assetIDs': [a['id'] for a in selected], 'sourceAlbumIDs': [ALBUM_ID],
            'sections': [{'title': 'Product reference angles', 'assetIDs': [a['id'] for a in selected]}],
            'description': 'A selected chain style with four received product-reference angles. Each angle retains its own review.',
            'notes': ['Ziggy selected this style on 2026-10-20. The delivered manifest marks all four angles as needing review. No chain-bite proof or on-character result is selected.']})
    album = {'id': ALBUM_ID, 'project': 'hon', 'category': 'details',
        'title': 'Neck chains · four selected styles', 'coverID': assets[0]['id'],
        'assetIDs': [a['id'] for a in assets],
        'description': 'Sixteen product-reference angles for A01, A04, A06 and B05; individual image reviews remain separate.'}
    return {'assets': assets, 'albums': [album], 'accessoryCollections': collections, 'reviewRequests': requests}


def apply_chain_accessories(catalog, repo_root, payload=None):
    payload = payload or intake_payload(repo_root)
    for key in ('assets', 'albums', 'accessoryCollections', 'reviewRequests'):
        by_id = {row['id']: row for row in catalog.setdefault(key, [])}
        for row in payload[key]:
            if row['id'] in by_id:
                # Rebuilds must retain independently saved review data, never replace it.
                if key == 'reviewRequests':
                    assert by_id[row['id']].get('sha256') == row['sha256']
                else:
                    assert by_id[row['id']] == row, 'Conflicting chain record: ' + row['id']
            else:
                if key == 'assets':
                    assert not any(a.get('sha256') == row['sha256'] for a in catalog[key]), 'Existing exact asset must be reused'
                catalog[key].append(deepcopy(row))
    for category in catalog['categories']:
        if category[0] == 'details':
            category[1] = 'Accessories'
    for group in catalog['accessoryCollections']:
        if group['id'] == 'hon:permanent-accessories':
            group['notes'] = [CURRENT_NOTE if note == STALE_NOTE else note for note in group.get('notes', [])]
    hero_by_sha = {row['sha256']: row for row in payload['assets'] if '-ANG1-' in row['id']}
    matched = []
    for supplement in catalog.get('reviewSupplements', []):
        for row in supplement.get('items', []):
            if row.get('sha256') not in hero_by_sha:
                continue
            asset = hero_by_sha[row['sha256']]
            assert row.get('project') == 'hon' and row.get('group') == 'approved'
            assert row.get('availability') == 'local_original_verified'
            assert row.get('exactAssetID') in (None, asset['id'])
            row['exactAssetID'] = asset['id']
            # The original URL and all supplier scope/evidence fields are retained.
            matched.append(asset['id'])
    assert set(matched) == {a['id'] for a in hero_by_sha.values()} and len(matched) == 4
    return catalog
