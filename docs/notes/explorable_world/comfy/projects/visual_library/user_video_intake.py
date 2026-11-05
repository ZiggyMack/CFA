"""Index exact user-delivered videos; human decisions stay in canonical reviews."""
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
from urllib.parse import quote


def apply_user_video_intakes(catalog, repo_root):
    root = Path(repo_root).resolve()
    here = root / 'docs/notes/explorable_world/comfy/projects/visual_library'
    registry = json.loads((here / 'user_video_intakes.json').read_text(encoding='utf-8'))
    assert registry['format'] == 'cfa-user-video-intakes-v1'

    def verified(path, sha256, size=None):
        source = (root / path).resolve()
        assert source.is_relative_to(root), path
        raw = source.read_bytes()
        assert hashlib.sha256(raw).hexdigest() == sha256, path
        assert size is None or len(raw) == size, path
        return source, raw

    def url(path):
        return quote(os.path.relpath(path, here).replace('\\', '/'), safe='/')

    # Validate the entire small intake before changing the supplied catalog.
    pending = []
    for intake in registry['intakes']:
        _, raw = verified(intake['requestPath'], intake['requestSHA256'])
        request = json.loads(raw)
        assert request['id'] == intake['id']
        originals = {item['sha256']: item for item in request['media']}
        assert len(originals) == len(intake['media'])
        for item in intake['media']:
            original = originals[item['sha256']]
            assert item['path'] == original['path'] and item['bytes'] == original['bytes']
            assert item['project'] in {'hon', 'lisan', 'unassigned'}
            assert item['kind'] == 'video' and item['category'] == 'videos'
            assert not {'storyboardStage', 'workingReference', 'variant', 'status', 'likenessRating', 'sceneQualityRating'} & item.keys()
            source, _ = verified(item['path'], item['sha256'], item['bytes'])
            poster, _ = verified(item['thumbnailPath'], item['thumbnailSHA256'])
            asset = deepcopy(item)
            group, title = asset.pop('group'), asset.pop('groupTitle')
            asset.pop('path'); asset.pop('thumbnailPath')
            asset.update(repoPath=item['path'], filename=source.name, src=url(source), thumb=url(poster),
                         album=item['project'] + ':' + group, sourceIntake=intake['id'],
                         provenancePath=intake['requestPath'])
            pending.append((asset, title))

    working = deepcopy(catalog)
    for asset, title in pending:
        existing = next((a for a in working['assets'] if a['id'] == asset['id']), None)
        if existing is not None:
            assert all(existing[key] == asset[key] for key in ['sha256', 'repoPath', 'project', 'kind', 'category', 'album']), asset['id']
        else:
            assert not any(a.get('sha256') == asset['sha256'] for a in working['assets']), asset['id']
            working['assets'].append(asset)
        album = next((a for a in working['albums'] if a['id'] == asset['album']), None)
        if album is None:
            album = dict(id=asset['album'], project=asset['project'], category='videos', title=title,
                         description='Original Gemini tests downloaded by Ziggy, with his recorded reviews.', assetIDs=[])
            working['albums'].append(album)
        assert album['project'] == asset['project'] and album['category'] == 'videos'
        if asset['id'] not in album['assetIDs']:
            album['assetIDs'].append(asset['id'])
    catalog['assets'] = working['assets']
    catalog['albums'] = working['albums']
    return [asset['id'] for asset, _ in pending]
