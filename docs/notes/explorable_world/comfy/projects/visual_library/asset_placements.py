"""Apply explicit, hash-bound filing decisions without changing media or reviews."""
from pathlib import Path
import copy
import json


def apply_asset_placements(catalog, root):
    path = Path(root) / 'docs/notes/explorable_world/comfy/projects/visual_library/asset_placements.json'
    manifest = json.loads(path.read_text(encoding='utf-8'))
    assets = {a['id']: a for a in catalog['assets']}
    albums = {a['id']: a for a in catalog['albums']}
    groups = {g['id']: g for g in catalog.get('castCollections', [])}
    entries = manifest['assignments']
    assert len({e['assetID'] for e in entries}) == len(entries), 'Duplicate placement'
    # Validate the entire change before touching any catalog object.
    for e in entries:
        a = assets.get(e['assetID'])
        assert a and a.get('sha256') == e['sha256'], 'Placement hash mismatch: ' + e['assetID']
        assert (a['project'], a['album']) in [(e['fromProject'], e['fromAlbum']), (e['project'], e['albumID'])], 'Unexpected prior placement: ' + a['id']
        dest = albums[e['albumID']]
        assert dest['project'] == e['project'] and dest['category'] == a['category']
        assert groups[e['characterCollectionID']]['project'] == e['project']
    for e in entries:
        a = assets[e['assetID']]
        if not a.get('placement'):
            a['placement'] = {
                'decisionID': manifest['decisionID'],
                'date': manifest['date'],
                'source': manifest['source'],
                'scope': 'Character identity and library placement only; saved reviews and reference selection remain unchanged.',
                'original': {k: copy.deepcopy(a.get(k)) for k in ('project', 'album', 'title', 'note')},
            }
        a.update(project=e['project'], album=e['albumID'], title=e['title'], note=e['note'], characterCollectionID=e['characterCollectionID'])
        for album in catalog['albums']:
            if album['id'] != e['albumID']:
                album['assetIDs'] = [i for i in album['assetIDs'] if i != a['id']]
        dest = albums[e['albumID']]
        if a['id'] not in dest['assetIDs']:
            dest['assetIDs'].append(a['id'])
        group = groups[e['characterCollectionID']]
        for key in ('assetIDs', 'videoAssetIDs'):
            if a['id'] not in group.setdefault(key, []):
                group[key].append(a['id'])
    retired = {e['fromAlbum'] for e in entries}
    catalog['albums'] = [a for a in catalog['albums'] if a['id'] not in retired or a['assetIDs']]

