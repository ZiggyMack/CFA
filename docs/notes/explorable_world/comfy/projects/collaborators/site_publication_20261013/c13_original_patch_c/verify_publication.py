"""Preservation proof for the C13 display publication; never restores source files."""
from pathlib import Path
import hashlib, json, sys
from datetime import datetime, timezone
from urllib.parse import unquote
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[7]
PROJECTS = ROOT / 'docs/notes/explorable_world/comfy/projects'
LIB = PROJECTS / 'visual_library'
def read(path): return json.loads(path.read_text(encoding='utf-8'))
def digest(path):
    raw = path.read_bytes()
    return dict(path=path.relative_to(ROOT).as_posix(), bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
def cat():
    raw = (LIB/'catalog.js').read_text(encoding='utf-8')
    return json.loads(raw.removeprefix('window.REVIEW_CATALOG = ').strip().removesuffix(';'))
def save(name, value):
    with (HERE/name).open('x', encoding='utf-8') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
assignment = read(HERE.parent/'SITE_OWNER_ASSIGNMENT_fb34beae-9485-407b-9e3d-189d094fcdd6.json')
guard_paths = [x['path'] for x in assignment['preservation_guard_at_handoff']]
guard_paths += ['docs/notes/explorable_world/comfy/projects/'+x for x in [
    'visual_library/working_reference_bom.json',
    'visual_library/assistant_likeness_assessments.json',
    'visual_library/shared_reference_collections.json',
    'collaborators/mailbox/registry.json']]
guards = [digest(ROOT/name) for name in guard_paths]
sources = []
for src in assignment['sources']:
    actual = digest(ROOT/src['path'])
    assert all(actual[k] == src[k] for k in ['bytes','sha256']), src['path']
    sources.append(actual)
if sys.argv[1] == 'before':
    data = cat()
    save('catalog.before.json', data)
    backup = HERE/'source_before'
    backup.mkdir(exist_ok=False)
    for name in ['build_catalog.py','library.js','library.css']:
        (backup/name).write_bytes((LIB/name).read_bytes())
    save('preservation.before.json', dict(capturedAtUTC=datetime.now(timezone.utc).isoformat(),
        assignmentID=assignment['assignment_id'], sources=sources, guards=guards,
        catalog=digest(LIB/'catalog.js'),
        counts=dict(assets=len(data['assets']), tasks=len(data['missionControl']['tasks'])),
        handoffGuardMatches=[dict(path=x['path'], matches=digest(ROOT/x['path']) == x)
            for x in assignment['preservation_guard_at_handoff']]))
    print(json.dumps(dict(snapshot='preservation.before.json', guards=len(guards),
        assets=len(data['assets']), sourcesVerified=len(sources))))
elif sys.argv[1] == 'after':
    initial = read(HERE/'preservation.before.json')
    assert guards == initial['guards'], 'Canonical change detected: inspect concurrent edits, never restore.'
    before, after = read(HERE/'catalog.before.json'), cat()
    old = {a['id']:a for a in before['assets']}
    new = {a['id']:a for a in after['assets']}
    expected = {'LAG-C13-ORIGINAL-7eafd9ac048d','LAG-C13-PATCH-C-23817577d3d3'}
    assert set(new)-set(old) == expected, 'Unexpected additions'
    assert set(old).issubset(new), 'Existing ID lost'
    changes = [key for key in old if old[key] != new[key]]
    assert not [key for key in changes if old[key]['kind'] not in ['document','pdf']], changes
    fields = [key for key in before if key not in ['assets','albums']]
    old_albums = {a['id']:a for a in before['albums']}
    new_albums = {a['id']:a for a in after['albums']}
    assert set(new_albums)-set(old_albums) == {'lisan:c13-original-patch-c'}
    assert all(new_albums.get(key) == value for key,value in old_albums.items()), 'Existing album changed'
    for key in fields:
        assert before.get(key) == after.get(key), 'Catalog changed: '+key
    assert after['missionControl'] == read(PROJECTS/'collaborators/mission_control.json')
    assert len(after['missionControl']['tasks']) == len(before['missionControl']['tasks'])
    pair = after['sourceComparisons']
    assert len(pair) == 1 and pair[0]['status'] == 'pending_comparison'
    links = []
    for item, src in zip(pair[0]['items'], assignment['sources']):
        asset = new[item['assetID']]
        assert asset['repoPath'] == src['path']
        assert all(asset[k] == src[k] for k in ['bytes','sha256'])
        for key in ['workingReference','componentApprovals','likenessRating','sceneQualityRating','storyboardStage','variant']:
            assert key not in asset, 'Seeded review state: '+key
        for field in ['src','thumb']:
            target = (LIB/unquote(asset[field])).resolve()
            proof = digest(target)
            assert all(proof[k] == src[k] for k in ['bytes','sha256'])
            links.append(dict(assetID=asset['id'], field=field, url=asset[field], **proof))
    result = dict(verifiedAtUTC=datetime.now(timezone.utc).isoformat(), assignmentID=assignment['assignment_id'],
        sources=sources, guardsBefore=initial['guards'], guardsAfter=guards,
        allCanonicalGuardsUnchanged=True, existingAssetIDsPreserved=len(old),
        existingMediaRecordsUnchanged=True, refreshedDocumentIDs=changes,
        catalogReviewAndTimingFieldsUnchanged=True, preservedCatalogFields=fields,
        sourceLinks=links, counts=dict(assets=len(after['assets']), tasks=len(after['missionControl']['tasks'])),
        comparison=pair[0], catalog=digest(LIB/'catalog.js'),
        verificationScope='Source bytes, generated data and local link targets. Browser visual preview blocked; not attempted.')
    save('preservation.after.json', result)
    print(json.dumps({k:result[k] for k in ['allCanonicalGuardsUnchanged','existingAssetIDsPreserved',
        'existingMediaRecordsUnchanged','refreshedDocumentIDs','catalogReviewAndTimingFieldsUnchanged','counts']}))
else:
    raise SystemExit('Expected before or after')