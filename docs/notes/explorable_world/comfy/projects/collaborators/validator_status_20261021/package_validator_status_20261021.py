"""Bounded text-only snapshot refresh using the existing DesignBundle packager.

The local catalog is first rebuilt by its existing owner builder. All unrelated
catalog fields, prior native assets, reviews and media remain frozen.
"""
from pathlib import Path
from copy import deepcopy
from collections import Counter
from datetime import datetime, timezone
import json, hashlib, sys

ROOT=Path(r'D:\Documents\CFA'); P=ROOT/'docs/notes/explorable_world/comfy/projects'
V=P/'visual_library'; E=P/'collaborators/validator_status_20261021'
CACHE=ROOT/'.cache/validator_status_20261021'; A=ROOT/'apps/creative_studio'; OUT=A/'library'
TARGET='reference-validation-evidence-ui-20261013'
sha=lambda b:hashlib.sha256(b).hexdigest()
def read(f): return json.loads(f.read_text(encoding='utf-8-sig'))
def load_local(f):return json.loads(f.read_text(encoding='utf-8').split('=',1)[1].strip().rstrip(';'))
def backup(f):return CACHE/f.relative_to(ROOT)
def save(f,x):f.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
receipt=read(E/'RECONCILIATION.json')
before=load_local(backup(V/'catalog.js')); after=load_local(V/'catalog.js')
mission=read(P/'collaborators/mission_control.json')
assert after['missionControl']==mission
strip=lambda m:[t for t in m['tasks'] if t['id']!=TARGET]
assert strip(before['missionControl'])==strip(mission),'Unrelated mission task changed'
for key in before:
 if key not in {'assets','missionControl'}:assert after[key]==before[key],f'Unrelated local field changed: {key}'
old_assets={x['id']:x for x in before['assets']}
new_assets={x['id']:x for x in after['assets']}
assert len(new_assets)==len(after['assets'])
changed=[k for k,x in old_assets.items() if new_assets.get(k)!=x]
assert not changed, f'Unrelated local assets changed: {changed}'
assert [x for x in after['assets'] if x['id'] in old_assets]==before['assets'],'Prior ordering changed'
added=[x for x in after['assets'] if x['id'] not in old_assets]
task=next(t for t in mission['tasks'] if t['id']==TARGET)
allowed={l['assetID'] for l in task['links']}
assert {x['id'] for x in added}<=allowed
assert all(x['kind']=='document' for x in added)
for path,digest in receipt['protectedFiles'].items():assert sha((ROOT/path).read_bytes())==digest,path

native_path=OUT/'design_catalog.json'; manifest_path=OUT/'design_manifest.json'
native_before=native_path.read_bytes();manifest_before=manifest_path.read_bytes()
assert sha(native_before)==receipt['beforeFiles'][native_path.relative_to(ROOT).as_posix()]
assert sha(manifest_before)==receipt['beforeFiles'][manifest_path.relative_to(ROOT).as_posix()]
native=json.loads(native_before); manifest=json.loads(manifest_before)
prior_native=deepcopy(native); prior_manifest=deepcopy(manifest)
sys.path.insert(0,str(A))
from build_design_library import DesignBundle
pack=DesignBundle(V/'catalog.js',OUT,ROOT,expected_source_sha=sha((V/'catalog.js').read_bytes()))
existing={a['id'] for a in native['assets']}
for asset in added:
 assert asset['id'] not in existing
 packaged=pack.package_asset(asset['id'])
 assert not packaged.get('unavailableReason')
 native['assets'].append(packaged)
portable=deepcopy(task)
portable['links']=[pack.portable_link(link,TARGET) for link in task['links']]
portable=pack.clean_config(portable)
assert not pack.unavailable,pack.unavailable
assert all(l.get('assetID') in {a['id'] for a in native['assets']} for l in portable['links'])
pos=next(i for i,t in enumerate(native['missionControl']['tasks']) if t['id']==TARGET)
native['missionControl']['tasks'][pos]=portable
for key in ('updated','updatedAtUTC'):native['missionControl'][key]=mission[key]
snapshot=native['designSnapshot']
snapshot['generatedAtUTC']=datetime.now(timezone.utc).isoformat()
snapshot['sourceCatalog']['sha256']=sha((V/'catalog.js').read_bytes())
snapshot['sourceAssetCount']=len(after['assets'])
snapshot['supplementalAssetCount']=len(native['assets'])-len(after['assets'])
snapshot['metadataRefresh']={'taskID':TARGET,'scope':'One task and linked documents; all prior assets and reviews preserved',
 'priorSnapshotSHA256':sha(native_before),'packagerSHA256':sha(Path(__file__).read_bytes())}
data=json.dumps(native,ensure_ascii=False,separators=(',',':')).encode('utf-8')
outputs={o['path']:o for o in manifest['outputs']}
outputs.update(pack.outputs)
outputs['design_catalog.json']={'path':'design_catalog.json','bytes':len(data),'sha256':sha(data),'role':'design_catalog','reused':False}
manifest.update(snapshot=snapshot,snapshotSHA256=sha(data),assetKinds=dict(Counter(a['kind'] for a in native['assets'])),
 outputs=[outputs[k] for k in sorted(outputs)],outputBytes=sum(o['bytes'] for o in outputs.values()),
 publicationFiles=sorted([*outputs,'design_manifest.json']))
sources={s['path']:s for s in manifest['sources']}
for f,record in pack.sources.items():sources[record['path']]=record
manifest['sources']=[sources[k] for k in sorted(sources)]
assert native['assets'][:len(prior_native['assets'])]==prior_native['assets']
assert strip(native['missionControl'])==strip(prior_native['missionControl'])
for key in prior_native:
 if key not in {'assets','missionControl','designSnapshot'}:assert native[key]==prior_native[key],key
assert snapshot['reviewOverlay']==prior_native['designSnapshot']['reviewOverlay']
for o in prior_manifest['outputs']:
 if o['path']!='design_catalog.json':assert outputs[o['path']]==o,'Prior media record changed'
for o in pack.outputs.values():assert sha((OUT/o['path']).read_bytes())==o['sha256']
assert native_path.read_bytes()==native_before and manifest_path.read_bytes()==manifest_before,'Concurrent snapshot change'
native_path.write_bytes(data);save(manifest_path,manifest)
receipt.update(localCatalogStatus='rebuilt_and_verified',hostedSnapshotStatus='saved_and_verified_not_published',
 localBuildInvocations=1,addedDocumentIDs=[a['id'] for a in added],
 newMediaFiles=list(pack.outputs),localCatalogSHA256=sha((V/'catalog.js').read_bytes()),
 nativeSnapshotSHA256=sha(data),allOtherCardsPreserved=True,priorAssetsPreserved=True,
 reviewDecisionsAndValidationPreserved=True,allExistingMediaRecordsPreserved=True,
 sourceAfterSHA256=sha((P/'collaborators/mission_control.json').read_bytes()))
save(E/'RECONCILIATION.json',receipt)
print(json.dumps({k:receipt[k] for k in ['localCatalogStatus','hostedSnapshotStatus','allOtherCardsPreserved','reviewDecisionsAndValidationPreserved']}))
print('Added documents:',len(added),'new packaged text files:',len(pack.outputs))
