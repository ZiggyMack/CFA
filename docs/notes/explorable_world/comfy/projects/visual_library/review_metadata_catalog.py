"""Add the frozen review intake without changing existing asset or review records."""
from pathlib import Path
import hashlib
import os
import shutil
import subprocess
from urllib.parse import quote

from cfa_review_metadata_intake import load_review_metadata_intake


def apply_review_metadata_intake(catalog, repo_root):
    from PIL import Image, ImageOps
    from browser_media_paths import BrowserMediaPaths
    root = Path(repo_root)
    projects = root / 'docs/notes/explorable_world/comfy/projects'
    here = projects / 'visual_library'
    previews = projects / 'review_previews_20261021'
    previews.mkdir(exist_ok=True)
    browser_paths = BrowserMediaPaths(root, projects / 'browser_media')
    ffmpeg = shutil.which('ffmpeg')
    bundled_ffmpeg = root / '.cache/hon_dolo_i2v_20261004/python_packages/imageio_ffmpeg/binaries/ffmpeg-win-x86_64-v7.1.exe'
    if not ffmpeg and bundled_ffmpeg.is_file():
        ffmpeg = str(bundled_ffmpeg)
    # Exclude this adapter's earlier additions so rebuilding keeps its identities
    # and summary stable; pre-existing IDs remain authoritative for exact bytes.
    existing = [a for a in catalog['assets'] if a.get('sourceIntake') != 'CFA-META-20261021-r002']
    intake = load_review_metadata_intake(root, existing)
    current = {a['id']: a for a in catalog['assets']}
    added = []
    for record in intake.pop('newAssets'):
        item = dict(record)
        if item['id'] in current:
            assert current[item['id']]['sha256'] == item['sha256']
            continue
        path = root / item.pop('path', item.get('repoPath', ''))
        item['repoPath'] = path.relative_to(root).as_posix()
        item['src'] = quote(os.path.relpath(browser_paths.resolve(path), here).replace('\\', '/'), safe='/')
        item['sourceIntake'] = 'CFA-META-20261021-r002'
        preview = previews / (item['sha256'] + '.jpg')
        if not preview.exists():
            if item['kind'] == 'image':
                with Image.open(path) as original:
                    im = ImageOps.exif_transpose(original).convert('RGB')
                    im.thumbnail((600, 600))
                    im.save(preview, quality=85)
            elif ffmpeg:
                subprocess.run([ffmpeg, '-v', 'error', '-y', '-i', str(path), '-frames:v', '1',
                                '-vf', 'scale=600:-2', str(preview)], check=True, capture_output=True)
        if preview.exists():
            item['thumb'] = quote(os.path.relpath(preview, here).replace('\\', '/'), safe='/')
        added.append(item)
    catalog['assets'].extend(added)
    if not any(c[0] == 'intake' for c in catalog['categories']):
        catalog['categories'].append(['intake', 'Intake verification'])
    known = {a['id'] for a in catalog['albums']}
    for asset in added:
        if asset['album'] not in known:
            catalog['albums'].append({'id': asset['album'], 'project': asset['project'], 'category': 'intake',
                                      'title': asset['tags'][-1] + ' · received review package',
                                      'description': 'Originals and repairs remain linked by family and exact hash.', 'assetIDs': []})
            known.add(asset['album'])
        album = next(a for a in catalog['albums'] if a['id'] == asset['album'])
        if asset['id'] not in album['assetIDs']:
            album['assetIDs'].append(asset['id'])
    intake['receipt'] = {'id': 'CFA-META-20261021-r002', 'status': 'received_and_hash_verified',
                         'verifiedManifestEntries': 493, 'verifiedManifests': 9,
                         'teamConfirmedReady': '2026-10-21', 'humanArtworkApproval': False,
                         'note': 'Chief, HaL and Z_6 confirmed the frozen handoff. Later repairs require a separate supplement.'}
    catalog['reviewIntake'] = intake
    if browser_paths.entries:
        browser_paths.write_manifest(here / 'review_intake_browser_paths.json')
    ids = [a['id'] for a in catalog['assets']]
    assert len(ids) == len(set(ids)), 'Repeated intake asset ID'
    by_id = {a['id']: a for a in catalog['assets']}
    for family in intake['families']:
        for version in family['versions']:
            if version.get('assetID'):
                assert by_id[version['assetID']]['sha256'] == version['sha256']
        assert family['humanAcceptance'] is None
    from review_winners_media import apply_winners_media
    apply_winners_media(catalog, root)
    from review_winners_supplement import apply_winners_supplement
    apply_winners_supplement(catalog, root)
    return added
