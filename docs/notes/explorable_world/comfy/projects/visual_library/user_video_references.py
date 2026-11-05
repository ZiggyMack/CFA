"""Apply explicit, hash-pinned user video reference links after story assembly.

Reference selection adds materials only. It never edits authored direction,
starting frames, timing, stages, ratings, reviews or acceptance.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path


def apply_user_video_references(catalog, repo_root):
    root = Path(repo_root).resolve()
    registry_path = root / 'docs/notes/explorable_world/comfy/projects/visual_library/user_video_intakes.json'
    registry = json.loads(registry_path.read_text(encoding='utf-8'))
    assert registry['format'] == 'cfa-user-video-intakes-v1'
    assets = {asset['id']: asset for asset in catalog['assets']}
    pending = []
    for intake in registry['intakes']:
        path = (root / intake['requestPath']).resolve()
        assert path.is_relative_to(root), intake['requestPath']
        raw = path.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == intake['requestSHA256'], intake['requestPath']
        request = json.loads(raw)
        assert request['id'] == intake['id']
        originals = {item['sha256']: item for item in request['media']}
        registered = {item['id']: item for item in intake['media']}
        evidence = dict(path=intake['requestPath'], sha256=intake['requestSHA256'], bytes=len(raw))
        for link in request.get('storyboardReferences', []):
            item = registered[link['assetID']]
            original = originals[link['sha256']]
            assert item['sha256'] == link['sha256']
            assert item['path'] == original['path'] and item['bytes'] == original['bytes']
            assert item['project'] == link['project']
            assert link['role'] in {'dinner_reference', 'scene_reference', 'costume_reference'}
            assert link.get('shotMaterialIDs') or link.get('shotIDs')
            asset = assets[link['assetID']]
            assert asset['kind'] == 'video' and asset['project'] == link['project']
            assert asset['sha256'] == link['sha256'] and asset['repoPath'] == item['path']
            media_path = (root / item['path']).resolve()
            assert media_path.is_relative_to(root), item['path']
            media_raw = media_path.read_bytes()
            assert len(media_raw) == item['bytes'] and hashlib.sha256(media_raw).hexdigest() == link['sha256']
            pending.append((link, asset, evidence, intake['id']))

    # Validate every target on copies so an invalid receipt leaves the caller intact.
    materials = deepcopy(catalog.get('shotMaterials', {'shots': []}))
    structure = deepcopy(catalog.get('storyboardStructure', {'stories': []}))
    linked = []
    for link, asset, evidence, intake_id in pending:
        common = dict(assetID=asset['id'], role=link['role'], sha256=link['sha256'],
                      note=link['note'], sourceIntake=intake_id, selectionEvidence=evidence)
        source = dict(assetID=asset['id'], path=asset['repoPath'], sha256=asset['sha256'], bytes=asset['bytes'])
        def append_once(target, material):
            existing = [m for m in target['materials'] if m['assetID'] == asset['id']]
            if existing:
                assert len(existing) == 1 and existing[0] == material, asset['id']
            else:
                target['materials'].append(material)

        for sid in link.get('shotMaterialIDs', []):
            targets = [s for s in materials['shots'] if s['id'] == sid and s['project'] == link['project']]
            assert len(targets) == 1 and targets[0]['sectionID'] == link['sectionID'], sid
            append_once(targets[0], dict(**common, status='user_selected_reference'))
        if link.get('shotIDs'):
            stories = [s for s in structure['stories'] if s['storyID'] == link['storyID'] and s['project'] == link['project']]
            assert len(stories) == 1, link['storyID']
            for sid in link['shotIDs']:
                targets = [s for s in stories[0]['shots'] if s['shotID'] == sid]
                assert len(targets) == 1 and targets[0]['sectionID'] == link['sectionID'], sid
                append_once(targets[0], dict(**common, availability='catalogued', source=source))
        linked.append(asset['id'])
    if pending:
        catalog['shotMaterials'] = materials
        catalog['storyboardStructure'] = structure
    return list(dict.fromkeys(linked))
