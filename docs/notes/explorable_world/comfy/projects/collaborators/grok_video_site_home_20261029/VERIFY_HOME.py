"""Independent read-only catalog audit; writes only this task's result receipt."""
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path('D:/Documents/CFA')
HERE = Path(__file__).resolve().parent
PROJECTS = ROOT / 'docs/notes/explorable_world/comfy/projects'
request = json.loads((HERE / 'REQUEST.json').read_text(encoding='utf-8'))
before = json.loads((HERE / 'PRESERVATION_BEFORE.json').read_text(encoding='utf-8-sig'))
cast_before = json.loads((HERE / 'CAST_BEFORE.json').read_text(encoding='utf-8'))
raw = (PROJECTS / 'visual_library/catalog.js').read_text(encoding='utf-8')
catalog = json.loads(raw.split('=', 1)[1].strip().rstrip(';'))
assets = {a['id']: a for a in catalog['assets']}
album = next((a for a in catalog['albums'] if a['id'] == 'hon:video-grok-tests'), None)
if not album or any(assets[m['id']].get('category') != 'videos' for m in request['media']):
    print(json.dumps({'state': 'awaiting_local_build'}))
    raise SystemExit(0)

cast = next(g for g in catalog['castCollections'] if g['id'] == 'hon:cast-dj')
intake_album = next(a for a in catalog['albums'] if a['id'] == 'hon:intake-grok-video-test')
current_reviews = json.loads((PROJECTS / 'hon_dolo_strictly_business/feedback/review_decisions.json').read_text(encoding='utf-8-sig'))
reviews_before = {r['id']: r for r in before['reviews']['items']}
reviews_after = {r['id']: r for r in current_reviews['items']}
built_reviews = {r['id']: r for r in catalog['reviewDecisions']}
checks = []
for media in request['media']:
    a = assets[media['id']]
    original = Path(request['confirmedDirectory']) / media['filename']
    data = original.read_bytes()
    assert len(data) == media['bytes'] and hashlib.sha256(data).hexdigest() == media['sha256']
    assert a['sha256'] == media['sha256'] and a['filename'] == media['filename']
    assert sum(x['id'] == media['id'] for x in catalog['assets']) == 1
    assert a['album'] == album['id'] and a.get('provider') == 'Grok'
    assert 'Grok' in a['tags'] and media['id'] in album['assetIDs']
    assert media['id'] in cast['videoAssetIDs'] and media['id'] in intake_album['assetIDs']
    assert a['provenancePath'].endswith('GROK-VIDEO-TEST_v001/REVIEW_gorilla-clips_v001.md')
    for key in ['status', 'likenessRating', 'sceneQualityRating', 'note', 'favorite']:
        assert reviews_after[media['id']].get(key) == reviews_before[media['id']].get(key), key
        assert built_reviews[media['id']].get(key) == reviews_after[media['id']].get(key), key
    checks.append({'id': a['id'], 'title': a['title'], 'album': a['album'],
                   'originalUnchanged': True, 'intakeLinkRetained': True,
                   'canonicalAndBuiltReviewsPreserved': True})
for key in ['coverID', 'currentIDs', 'workingReferenceIDs', 'historicalReferenceIDs', 'workingSelectionEvidence']:
    assert cast.get(key) == cast_before.get(key), key
assert len(cast['workingReferenceIDs']) == 7
result = {'verifiedAtUTC': datetime.now(timezone.utc).isoformat(),
          'state': 'verified_local_catalog', 'media': checks,
          'chewyReferenceSelectionPreserved': True,
          'referenceCount': 7, 'duplicateCanonicalAssets': False,
          'videoRoute': '#hon/videos/hon%3Avideo-grok-tests',
          'chewyRoute': '#hon/cast/hon%3Acast-dj',
          'hostedVisibilityVerifiedByRoot': False}
(HERE / 'ROOT_VERIFICATION.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=True))
