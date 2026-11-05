"""Create one frozen intake snapshot; original media are read, never changed."""
from collections import Counter
import csv
from datetime import datetime, timezone
import hashlib
import io
import json
from pathlib import Path
import sys

from PIL import Image

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]
LIBRARY = ROOT / 'docs/notes/explorable_world/comfy/projects/visual_library'
sys.path.insert(0, str(LIBRARY))
from grok500_catalog import io_path
from lisan_mouth_intake import INTAKE_ID, MANIFEST_SHA256, SOURCE_DIRECTORY, SOURCE_MESSAGE_IDS, validate_registry

source = ROOT / SOURCE_DIRECTORY
manifest_bytes = io_path(source / 'MANIFEST.csv').read_bytes()
assert hashlib.sha256(manifest_bytes).hexdigest() == MANIFEST_SHA256, 'Changed approved source manifest'
rows = list(csv.DictReader(io.StringIO(manifest_bytes.decode('utf-8-sig'))))
assert len(rows) == 65
raw_catalog = io_path(LIBRARY / 'catalog.js').read_text(encoding='utf-8')
catalog = json.loads(raw_catalog[raw_catalog.index('=')+1:].strip().rstrip(';'))
by_hash = {}
for a in catalog['assets']:
    if a.get('sha256') and a.get('project') == 'lisan':
        by_hash.setdefault(a['sha256'], a)
recorded = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
provider_folder = HERE / 'provider_documents'
provider_folder.mkdir(parents=True, exist_ok=True)

def write_new(path, raw):
    with io_path(path).open('xb') as stream:
        stream.write(raw)

documents = []
for name in ['MANIFEST.csv', 'README.md', 'NOTES_Z5_20-50.md', 'DECISION-LAG-BREATHER-V3.md']:
    raw = io_path(source / name).read_bytes()
    target = provider_folder / name
    write_new(target, raw)
    documents.append({'project':'lisan', 'path':target.relative_to(ROOT).as_posix(), 'sourcePath':(source/name).relative_to(ROOT).as_posix(),
                      'title':'HaL mouth set - ' + name, 'album':'Lisan complete mouth set - source evidence',
                      'bytes':len(raw), 'sha256':hashlib.sha256(raw).hexdigest()})
for mid in SOURCE_MESSAGE_IDS:
    original = ROOT / 'docs/notes/explorable_world/comfy/projects/collaborators/mailbox/messages' / (mid + '.json')
    raw = io_path(original).read_bytes()
    msg = json.loads(raw)
    assert msg['id'] == mid and msg['sender'] == 'hal' and msg['recipient'] == 'nova'
    if mid == SOURCE_MESSAGE_IDS[1]:
        assert msg['attachments'][0]['sha256'] == MANIFEST_SHA256
    target = provider_folder / ('NOTICE-' + mid + '.json')
    write_new(target, raw)
    documents.append({'project':'lisan','path':target.relative_to(ROOT).as_posix(),'sourcePath':original.relative_to(ROOT).as_posix(),
                      'title':'HaL mouth intake notice - ' + mid[:8], 'album':'Lisan complete mouth set - source evidence',
                      'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()})

album_ids = {'01_VISEMES':'lisan:mouth-visemes-20261012', '02_BREATHER_NATURAL':'lisan:mouth-breather-20261012',
             '03_OPTIONAL_GRILL':'lisan:mouth-optional-grill-20261012', '04_FAILS':'lisan:mouth-failures-20261012'}
assets = []
for row in rows:
    path = source / row['file']
    assert path.resolve().is_relative_to(source.resolve()) and path.is_file(), row['file']
    raw = io_path(path).read_bytes()
    sha = hashlib.sha256(raw).hexdigest()
    assert sha == row['sha256'], row['file']
    with Image.open(io.BytesIO(raw)) as im:
        im.load()
        width, height = im.size
        assert (width,height) == (1280,720)
    old = by_hash.get(sha)
    aid = old['id'] if old else 'LAG-VIS-' + sha[:16]
    provider = {'status':'provider_self_score_preliminary','reportedBy':'hal','contributors':['hal','Z_5'] if 'Z_5' in row['file'] else ['hal'],
                'likenessRating':int(row['prelim_likeness']), 'sceneQualityRating':int(row['prelim_scene']),
                'suggestedLane':row['suggested_lane'], 'suggestedScope':row['suggested_scope'], 'stage':'preliminary',
                'defects':row['defects'], 'sourceMessageID':SOURCE_MESSAGE_IDS[1], 'sourceManifestSHA256':MANIFEST_SHA256}
    note = ('Provider draft likeness: ' + row['prelim_likeness'] + '/5; scene craft: ' + row['prelim_scene'] +
            '/5 (HaL/Z_5 self-scores; not human ratings or approval). Suggested lane: ' + row['suggested_lane'] +
            '; scope: ' + row['suggested_scope'] + '. Provider defects: ' + (row['defects'] or 'none recorded') +
            '. Static preliminary mouth reference; no song timing, motion validation or new identity lock.')
    if row['collection'] == '03_OPTIONAL_GRILL':
        note += ' Optional grill MASTER candidate only; existing decisions and natural-teeth default stay in force.'
    if row['collection'] == '04_FAILS':
        note += ' Reported failure retained visibly for comparison; provider Multiverse suggestion is not a user lane decision.'
    asset = {'id':aid,'project':'lisan','path':path.relative_to(ROOT).as_posix(),'sha256':sha,'bytes':len(raw),
             'width':width,'height':height,'decoded':True,'binding':'existing' if old else 'new',
             'title':('HaL - ' + path.stem.replace('_', ' ')), 'category':'review' if row['collection']=='04_FAILS' else 'details',
             'album':album_ids[row['collection']], 'providerCollection':row['collection'],'providerShapeNumber':int(row['shape_no']) if row['shape_no'] else None,
             'providerPreliminaryReview':provider,'providerNoteSuffix':note,'sourceMessageID':SOURCE_MESSAGE_IDS[1],
             'sourceManifestSHA256':MANIFEST_SHA256,'intakeID':INTAKE_ID}
    if old:
        asset['existingSourcePath'] = old['repoPath']
    else:
        asset.update(storyboardStage='preliminary',acceptance='not_accepted',timing=None,sceneID=None,motionValidated=False,
                     sourceStatus='provider_reported_failure' if row['collection']=='04_FAILS' else 'received_preliminary_candidate',
                     note=note,tags=['Lisan Al Gaib','mouth library','HaL complete return',row['collection']])
    assets.append(asset)
assert len({a['sha256'] for a in assets}) == 65
counts = Counter(a['providerCollection'] for a in assets)
reused = [a for a in assets if a['binding']=='existing']
assert len(reused)==21 and len(assets)-len(reused)==44
descriptions = {
    '01_VISEMES':('Natural-teeth mouth shapes - 51 files','44 distinct numbered shapes. Missing usable 07, 15, 16, 18, 35; 47 skipped as a Hon Dolo prop. Provider draft scores stay separate from your review.'),
    '02_BREATHER_NATURAL':('Breather plus natural teeth - 5 proofs','BR-01 v3 keeps its existing selected scope: breather + natural teeth + no grill only. BR-06 remains failed; this combination is not a universal default.'),
    '03_OPTIONAL_GRILL':('Optional grill - master candidate','One r2 candidate with GAIIB defect; not a new lock. Preserve existing approval scopes and the natural-teeth default.'),
    '04_FAILS':('Mouth experiments - retained failures','Eight failures remain visible as reported failures. No file deletion, user removal decision or forced Multiverse lane.')}
albums = [{'id':'lisan:mouth-complete-20261012','project':'lisan','category':'details','title':'HaL complete mouth set - 65 images',
           'description':'51 viseme files, five breather proofs, one optional grill candidate and eight failures. Reused references keep their existing reviews and scoped selections.',
           'related':[a['id'] for a in assets]}]
for collection,(title,description) in descriptions.items():
    albums.append({'id':album_ids[collection],'project':'lisan','category':'review' if collection=='04_FAILS' else 'details',
                   'title':title,'description':description,'related':[a['id'] for a in assets if a['providerCollection']==collection]})
data = {'schemaVersion':1,'id':INTAKE_ID,'recordedAtUTC':recorded,'receiptState':'verified_hash_size_decode',
        'sourceDirectory':SOURCE_DIRECTORY,'sourceManifestSHA256':MANIFEST_SHA256,'sourceMessageIDs':SOURCE_MESSAGE_IDS,
        'assets':assets,'albums':albums,'documents':documents,
        'coverage':{'visemeFileCount':51,'distinctVisemeShapeNumbers':44,'missingUsableShapeNumbers':[7,15,16,18,35],
                    'skippedShapeNumbers':[47],'breatherProofCount':5,'breatherRequestedCount':6,'breatherMissingOrFailed':['BR-06'],
                    'optionalGrillCandidateCount':1,'failureCount':8,'status':'provider_reported_unresolved'},
        'summary':{'receivedImageCount':65,'existingAssetCount':21,'newAssetCount':44,'newUserRatings':0,'newApprovals':0,'imagesChanged':0}}
validate_registry(data)
write_new(HERE/'registry.json',(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode())
receipt = {'schemaVersion':1,'intakeID':INTAKE_ID,'recordedAtUTC':recorded,'state':'verified_hash_size_decode',
           'sourceManifestSHA256':MANIFEST_SHA256,'sourceMessageIDs':SOURCE_MESSAGE_IDS,'collectionCounts':dict(counts),
           'imageCount':65,'existingAssetsReused':21,'newAssets':44,'allOriginalsUnchanged':True,
           'originalImageByteCount':sum(a['bytes'] for a in assets),'providerDocumentsSnapshotCount':6,
           'humanRatingsWritten':0,'newApprovals':0,'providerMessagesSent':0,'generationRuns':0,
           'images':[{'id':a['id'],'path':a['path'],'sha256':a['sha256'],'bytes':a['bytes'],'decoded':a['decoded'],'binding':a['binding']} for a in assets]}
for a in assets:
    assert hashlib.sha256(io_path(ROOT/a['path']).read_bytes()).hexdigest()==a['sha256']
write_new(HERE/'intake_receipt.json',(json.dumps(receipt,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps({'images':65,'reused':21,'new':44,'collections':dict(counts),'manifestSHA256':MANIFEST_SHA256,'registry':(HERE/'registry.json').relative_to(ROOT).as_posix()}))