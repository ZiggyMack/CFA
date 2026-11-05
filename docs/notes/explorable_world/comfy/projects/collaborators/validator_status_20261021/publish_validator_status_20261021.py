"""Publish only the verified native metadata delta; preserve shared checkout/index."""
from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,os,subprocess,uuid
ROOT=Path(r'D:\Documents\CFA');P=ROOT/'docs/notes/explorable_world/comfy/projects'
E=P/'collaborators/validator_status_20261021';A=ROOT/'apps/creative_studio';OUT=A/'library'
BASE='abee028405da867193dba577487a99d34e0f9c7e'
def git(*args,data=None,env=None):
 return subprocess.run(['git',*args],cwd=ROOT,input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True,env=env).stdout
sha=lambda b:hashlib.sha256(b).hexdigest()
def shared():
 idx=Path(git('rev-parse','--path-format=absolute','--git-path','index').decode().strip())
 return {'head':git('rev-parse','HEAD').decode().strip(),'indexSHA256':sha(idx.read_bytes())}
def remote():return git('ls-remote','origin','refs/heads/main').decode().split()[0]
def save(f,x):f.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
state=shared()
assert state=={'head':'e58074d0fe345e8b429ed44b5b938a82f55f1fdd','indexSHA256':'ffad1a7bb11b6a25e6447ec85b9b8565cd36afbacae3f806e008e704913c9a97'}
assert remote()==BASE
rec=json.loads((E/'RECONCILIATION.json').read_text(encoding='utf-8'))
checks=json.loads((E/'CHECKS.json').read_text(encoding='utf-8'));assert checks['nativeAppTest']=='passed'
assert sha((P/'visual_library/catalog.js').read_bytes())==rec['localCatalogSHA256']
assert sha((P/'collaborators/mission_control.json').read_bytes())==rec['sourceAfterSHA256']
for rel,digest in rec['protectedFiles'].items():assert sha((ROOT/rel).read_bytes())==digest,rel
old_raw=git('show',BASE+':apps/creative_studio/library/design_catalog.json')
assert sha(old_raw)==rec['beforeFiles']['apps/creative_studio/library/design_catalog.json']
old_manifest=json.loads(git('show',BASE+':apps/creative_studio/library/design_manifest.json'))
manifest=json.loads((OUT/'design_manifest.json').read_text(encoding='utf-8'))
old_outputs={o['path']:o for o in old_manifest['outputs']}
new_outputs={o['path']:o for o in manifest['outputs']}
for rel,obj in old_outputs.items():
 if rel!='design_catalog.json':assert new_outputs[rel]==obj,rel
assert set(new_outputs)-set(old_outputs)==set(rec['newMediaFiles'])
files=[OUT/'design_catalog.json',OUT/'design_manifest.json',*[OUT/rel for rel in rec['newMediaFiles']]]
pins={f.relative_to(ROOT).as_posix():{'sha256':sha(f.read_bytes()),'bytes':f.stat().st_size} for f in files}
for f in files:
 rel=f.relative_to(OUT).as_posix()
 if rel in new_outputs:
  assert all(pins[f.relative_to(ROOT).as_posix()][k]==new_outputs[rel][k] for k in ('sha256','bytes'))
paths=sorted(pins)
env=dict(os.environ,GIT_INDEX_FILE=str(ROOT/'.cache'/('validator-status-'+uuid.uuid4().hex+'.index')))
git('read-tree',BASE,env=env)
blobs=git('hash-object','-w','--no-filters','--stdin-paths',data=('\n'.join(paths)+'\n').encode('utf-8'),env=env).decode().splitlines()
entries=b''.join(b'100644 '+blob.encode()+b'\t'+path.encode()+b'\0' for path,blob in zip(paths,blobs))
git('update-index','-z','--index-info',data=entries,env=env)
tree=git('write-tree',env=env).decode().strip()
changes=git('diff','--name-only','-z',BASE,tree).decode().strip('\0').split('\0')
assert set(changes)<=set(paths) and not git('diff','--diff-filter=D','--name-only',BASE,tree)
assert shared()==state and remote()==BASE
for rel,pin in pins.items():assert sha((ROOT/rel).read_bytes())==pin['sha256']
message=('Reconcile validator reference card with delivered foundation and current returns\n\n'
 'Retain its identity and prior dispatch; show ongoing reference reconciliation, '
 'actual V1 return and later scoped human decisions. Preserve every other card, '
 'review, validation assessment and prior media record.\n\n'
 'Checks: five Mission progress tests, native AppTest and bounded preservation checks passed.\n')
commit=git('commit-tree',tree,'-p',BASE,data=message.encode('utf-8')).decode().strip()
publication={'parent':BASE,'commit':commit,'tree':tree,'files':pins,'changedFiles':changes,'checks':checks,'sharedStateBefore':state,'liveStatus':'pending'}
save(E/'PUBLICATION.json',publication)
print('Publishing '+commit+' ('+str(len(changes))+' metadata/text files)',flush=True)
result=subprocess.run(['git','push','origin',commit+':refs/heads/main'],cwd=ROOT,check=False)
assert remote()==commit,f'Push not confirmed ({result.returncode})'
assert shared()==state
publication.update(publishedAtUTC=datetime.now(timezone.utc).isoformat(),sharedStateAfter=shared(),remoteMain=commit)
save(E/'PUBLICATION.json',publication)
rec.update(hostedSnapshotStatus='published_not_live_verified',publishedCommit=commit)
save(E/'RECONCILIATION.json',rec)
print(json.dumps({'publishedCommit':commit,'changedFiles':len(changes),'sharedCheckoutAndIndexPreserved':True}))
