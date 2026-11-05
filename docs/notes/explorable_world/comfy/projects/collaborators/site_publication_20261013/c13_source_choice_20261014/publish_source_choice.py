from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
import json,hashlib,subprocess,sys
R=Path('D:/Documents/CFA');P=R/'docs/notes/explorable_world/comfy/projects';L=P/'visual_library';E=Path(__file__).parent
def now():return datetime.now(timezone.utc).isoformat()
def read(p):return json.loads(p.read_bytes())
def pin(p):
 raw=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def check(row):assert pin(R/row['path'])=={k:row[k] for k in ['path','bytes','sha256']},row['path']
def save(n,o):(E/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def cat(p):return json.loads(p.read_text(encoding='utf-8').split('=',1)[1].strip().removesuffix(';'))
def run(n,args):
 x=subprocess.run(args,cwd=L,capture_output=True,text=True,encoding='utf-8',errors='replace');return dict(name=n,exitCode=x.returncode,stdout=x.stdout,stderr=x.stderr)
assert not (E/'build_result.json').exists(),'Inspect existing build record; do not automatically repeat'
b=read(E/'preservation.before.json');w=read(L/'writer_development.json');intake=read(E/'writer_intake.json')
allowedGuards={(P/'collaborators/mission_control.json').relative_to(R).as_posix(),(L/'source_comparisons.json').relative_to(R).as_posix()}
for row in b['guards']:
 if row['path'] not in allowedGuards:check(row)
for row in w['documents']+w['excludedSources']:check(row)
for row in b['inputs']:
 if Path(row['path']).name not in ['library.js','build_catalog.py','writer_development.json','source_comparisons.json']:check(row)
before=cat(E/'catalog.js.before');assert (L/'catalog.js').read_bytes()==(E/'catalog.js.before').read_bytes()
inputs=[pin(L/Path(x['path']).name) for x in b['inputs']]+[pin(P/'collaborators/mission_control.json'),pin(E/'SOURCE_CHOICE.json')]
record=dict(assignmentID='c13-patch-c-scoped-source-choice-20261014',status='running',startedAtUTC=now(),buildInvocations=1,sourceInputs=inputs,catalogBefore=pin(L/'catalog.js'));save('build_result.json',record)
try:
 built=run('build_catalog.py',[sys.executable,'-B',str(L/'build_catalog.py')]);record['build']=built;save('build_result.json',record);assert built['exitCode']==0,built['stderr']
 print('Local build complete; checking preservation and renderer.',flush=True)
 after=cat(L/'catalog.js');old={a['id']:a for a in before['assets']};new={a['id']:a for a in after['assets']}
 added={'lisan:doc:'+r['path'] for r in intake['added']};assert set(new)-set(old)==added,(set(new)-set(old),added);assert not set(old)-set(new)
 revised={r['path'] for r in intake['revised']};selected={a['id'] for a in read(L/'source_comparisons.json')['media']};changes=[]
 for aid,a in old.items():
  if a==new[aid]:continue
  fields={k for k in set(a)|set(new[aid]) if a.get(k)!=new[aid].get(k)}
  allowed={'sourceStatus','note','tags'} if aid in selected else {'text','sha256','bytes','note'} if a['repoPath'] in revised else set()
  assert fields<=allowed,(aid,fields)
  changes.append(dict(assetID=aid,fields=sorted(fields)))
 for key in before:
  if key not in ['assets','albums','missionControl','writerDevelopment','sourceComparisons']:assert after[key]==before[key],key
 oldAlbums={a['id']:a for a in before['albums']};newAlbums={a['id']:a for a in after['albums']};assert oldAlbums.keys()==newAlbums.keys()
 for aid,a in oldAlbums.items():
  filtered=dict(newAlbums[aid]);filtered['assetIDs']=[i for i in filtered['assetIDs'] if i not in added];assert filtered==a,aid
 assert all(row in after['writerDevelopment']['associations'] for row in before['writerDevelopment']['associations'])
 assert after['sourceComparisons']==read(L/'source_comparisons.json')['comparisons'];assert after['missionControl']==read(P/'collaborators/mission_control.json')
 assert after['reviewDecisions']==before['reviewDecisions']
 for row in b['guards']:
  if row['path'] not in allowedGuards:check(row)
 for row in inputs+w['documents']+w['excludedSources']:check(row)
 names=['test_source_comparison_publication.cjs','test_writer_publication.cjs','test_reference_validation.cjs','test_review_requests.cjs','test_mission_priority.cjs','test_mission_hash_navigation.cjs','test_working_bom.cjs','test_collections_navigation.cjs','test_compact_browse.cjs']
 with ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(lambda n:run(n,['D:/Program Files (x86)/node.exe',str(L/n)]),names))
 save('test_results.json',dict(passed=all(x['exitCode']==0 for x in results),results=results,browserVisualQA=False))
 for x in results:print(json.dumps(x),flush=True)
 assert all(x['exitCode']==0 for x in results),'Verification failed; no automatic rebuild'
 counts=dict(assets=len(after['assets']),albums=len(after['albums']),documents=sum(a['kind'] in ['document','pdf'] for a in after['assets']),reviews=len(after['reviewDecisions']))
 save('SOURCE_PLACEMENT_CHECKPOINT.json',dict(checkedAtUTC=now(),source=pin(L/'writer_development.json'),catalog=pin(L/'catalog.js'),sourceFolderTextFiles=intake['directFolderTextFiles'],included=w['documents'],excluded=w['excludedSources'],intake=pin(E/'writer_intake.json')))
 handback=dict(assignmentID=record['assignmentID'],status='local_publication_complete',completedAtUTC=now(),buildInvocations=1,catalog=pin(L/'catalog.js'),counts=counts,sourceChoice=pin(E/'SOURCE_CHOICE.json'),selectedAssetID='LAG-C13-PATCH-C-23817577d3d3',retainedAssets=sorted(selected),checks=pin(E/'test_results.json'),writerCheckpoint=pin(E/'SOURCE_PLACEMENT_CHECKPOINT.json'),sourceFiles=inputs,changedExistingAssets=changes,preserved=dict(priorReviews=len(before['reviewDecisions']),existingAssets=len(old),allSceneReviewsAndTiming=True,referenceValidationAndMouthCoverage=True,priorWriterAssociations=True,guardFiles=len(b['guards']),unchangedGuards=len(b['guards'])-len(allowedGuards),sourceAuthorFilesUnmodified=True,liveBrowseUIRetained=True),browserVisualQA=False,limitations='Local publication only. Actual renderer and handlers checked with DOM/storage doubles; browser file access is unavailable. Human source choice is an attributed relay. No new ratings, criteria passes or production acceptance.')
 save('SITE_PUBLICATION_HANDBACK.json',handback);record.update(status='complete',completedAtUTC=now(),catalogAfter=pin(L/'catalog.js'),handback=pin(E/'SITE_PUBLICATION_HANDBACK.json'));save('build_result.json',record)
 print(json.dumps(dict(status='complete',handback=record['handback'],counts=counts)),flush=True)
except Exception as error:
 record.update(status='needs_attention',error=str(error),checkedAtUTC=now());save('build_result.json',record);raise
