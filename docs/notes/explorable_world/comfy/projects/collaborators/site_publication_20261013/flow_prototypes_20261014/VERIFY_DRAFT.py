"""Verify only draft artifacts, with in-memory catalog mutations. No site build."""
from pathlib import Path
import copy
import hashlib
import json
import runpy
import sys
import urllib.parse

E = Path(__file__).resolve().parent
R = E.parents[7]
L = R/'docs/notes/explorable_world/comfy/projects/visual_library'
sys.path.insert(0, str(L))
from source_relocations import resolve_source
from grok500_catalog import io_path

loader = runpy.run_path(str(E/'PROPOSED_LOADER.py'))
published_text = (L/'catalog.js').read_text(encoding='utf-8')
published = json.loads(published_text.split('=', 1)[1].rstrip().rstrip(';'))
draft = json.loads((E/'flow_prototypes.json').read_text(encoding='utf-8'))
fixture_path = E/'registered_manifest_fixture.json'


def run(value):
    fixture_path.write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
    assets = copy.deepcopy(published['assets'])
    albums = []

    def add_album(project, id, category, title, description='', related=None):
        key = project + ':' + id
        assert not any(a['id'] == key for a in published['albums'])
        assert not any(a['id'] == key for a in albums)
        albums.append(dict(id=key, project=project, category=category, title=title,
                           description=description, related=related or []))
        return key

    def url(path):
        import os
        return urllib.parse.quote(os.path.relpath(R/path, L).replace('\\', '/'), safe='/')

    def doc(project, path, title, album):
        assets.append(dict(id=project+':doc:'+path, project=project, src=url(path),
                           filename=Path(path).name, title=title, repoPath=path,
                           historicalRepoPath=path, category='documents', album=album,
                           kind='document', text=(R/path).read_text(encoding='utf-8-sig')[:40000],
                           note='', inert=False))

    registered = loader['add_flow_prototypes'](fixture_path, root=R, assets=assets,
        add_album=add_album, url=url, doc=doc, io_path=io_path, resolve_source=resolve_source)
    shots = copy.deepcopy(published['shotMaterials'])
    loader['append_flow_shots'](shots, registered)
    assert assets[:len(published['assets'])] == published['assets']
    assert shots['shots'][:len(published['shotMaterials']['shots'])] == published['shotMaterials']['shots']
    by_id = {a['id']: a for a in assets}
    for shot in registered['shots']:
        assert all(m['assetID'] in by_id and m.get('sha256') == by_id[m['assetID']].get('sha256') for m in shot['materials'])
        assert all(id in by_id for id in shot['panelAssetIDs'])
    for album in albums:
        primary = [a['id'] for a in assets if a['album'] == album['id']]
        album['assetIDs'] = list(dict.fromkeys(primary + album.pop('related')))
        assert album['assetIDs'] == ['FLOW-LAG-SW2-001', 'FLOW-LAG-SIGNAL-001', 'FLOW-LAG-SIGNAL-002']
    return dict(assets=assets[len(published['assets']):], albums=albums, shots=registered['shots'])


try:
    run(draft)
    raise RuntimeError('Draft-only manifest was incorrectly accepted for publication')
except AssertionError:
    pass
prepared = copy.deepcopy(draft)
prepared['publicationState'] = 'registered_for_site_build'
additions = run(prepared)
assert len(additions['assets']) == 6 and len(additions['albums']) == 2 and len(additions['shots']) == 3

mutations = [
    ('wrong source binding', lambda d: d['intakes'][0].update(sourceAssetID='LAG500-L19-S3')),
    ('incomplete evidence pins', lambda d: d['intakes'][0]['nestedPins'].pop()),
    ('wrong original bytes', lambda d: d['media'][0].update(bytes=1)),
    ('invented production stage', lambda d: d['media'][0].update(storyboardStage='production')),
    ('invented human approval', lambda d: d['media'][0].update(workingReference={'status':'approved'})),
    ('invented song position', lambda d: d['shots'][0].update(timing='00:12')),
    ('wrong take-one baseline', lambda d: d['media'][2].update(predecessorAssetID='FLOW-LAG-SW2-001')),
]
for label, mutate in mutations:
    invalid = copy.deepcopy(prepared)
    mutate(invalid)
    try:
        run(invalid)
    except (AssertionError, KeyError):
        continue
    raise RuntimeError('Invalid fixture accepted: ' + label)
run(prepared)  # Leave the fixture marked registered only for the in-memory test.
(E/'DRAFT_ADDITIONS_FIXTURE.json').write_text(json.dumps(additions, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps({'loaderAcceptedExactIntakes':True, 'draftPublicationRejected':True,
                  'mutationRejections':len(mutations), 'newVideoAssets':3, 'newIntakeDocuments':3,
                  'newAlbums':2, 'newUnplacedShots':3, 'existingAssetsPreserved':True,
                  'existingShotsPreserved':True, 'siteBuilt':False, 'liveSourcesEdited':False}, indent=2))
