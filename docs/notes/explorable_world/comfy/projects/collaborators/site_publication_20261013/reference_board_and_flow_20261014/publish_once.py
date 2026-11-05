from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
import json,hashlib,subprocess,sys
R=Path('D:/Documents/CFA');P=R/'docs/notes/explorable_world/comfy/projects';L=P/'visual_library';E=Path(__file__).parent
def read(p):return json.loads(p.read_bytes())
def cat(p):return json.loads(p.read_text(encoding='utf-8').split('=',1)[1].strip().removesuffix(';'))
def pin(p):
 raw=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def check(row):assert pin(R/row['path'])=={k:row[k] for k in ['path','bytes','sha256']},row['path']
def save(n,o):(E/n).write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def run(n,args):
 x=subprocess.run(args,cwd=L,capture_output=True,text=True,encoding='utf-8',errors='replace');return dict(name=n,exitCode=x.returncode,stdout=x.stdout,stderr=x.stderr)
def now():return datetime.now(timezone.utc).isoformat()
assert not (E/'build_result.json').exists(),'Inspect the recorded build instead of repeating it'
before=cat(E/'catalog.js.before');assert cat(L/'catalog.js')==before
w=read(L/'writer_development.json');intake=read(E/'writer_intake.json');f=read(L/'flow_prototypes.json');review=read(P/'hon_dolo_strictly_business/feedback/review_decisions.json')['items']
oldReviews=before['reviewDecisions'];newReviews=[x for x in review if x['id'] not in {v['id'] for v in oldReviews}]
assert [x for x in review if x not in newReviews]==oldReviews
assert {x['id'] for x in newReviews}=={'LAG-602a9fd4021dc356','LAG-63126392af1ccf8b'}
for x in newReviews:
 assert x['likenessRating']==5 and x['humanRatingConfirmation']['field']=='likenessRating'
 assert x['humanRatingConfirmation'].get('decisionAtUTC')
 assert not {'status','sceneQualityRating','storyboardStage','workingReference','workingReferenceScope'}&x.keys()
for row in w['documents']+w['excludedSources']:check(row)
prior=read(P/'collaborators/site_publication_20261013/c13_source_choice_20261014/preservation.before.json')
allowed={'docs/notes/explorable_world/comfy/projects/collaborators/mission_control.json','docs/notes/explorable_world/comfy/projects/visual_library/source_comparisons.json','docs/notes/explorable_world/comfy/projects/hon_dolo_strictly_business/feedback/review_decisions.json'}
for row in prior['guards']:
 if row['path'] not in allowed:check(row)
assert read(P/'collaborators/mission_control.json')==before['missionControl']
assert read(L/'source_comparisons.json')['comparisons']==before['sourceComparisons']
guards=[pin(R/x['path']) for x in prior['guards']]
inputs=[pin(L/n) for n in ['library.js','library.css','build_catalog.py','writer_development.json','source_comparisons.json','flow_prototypes.json','flow_prototype_intake.py','character_reference_board.json','reference_validation.json','mouth_coverage.json','reference_provenance.py','reference_provenance_snapshots.json','shot_materials.json','working_reference_bom.json']]
save('preservation.before.json',dict(guards=guards,inputs=inputs))
record=dict(status='running',startedAtUTC=now(),buildInvocations=1,sourceInputs=inputs,catalogBefore=pin(L/'catalog.js'));save('build_result.json',record)
try:
 built=run('build_catalog.py',[sys.executable,'-B',str(L/'build_catalog.py')]);record['build']=built;save('build_result.json',record);assert built['exitCode']==0,built['stderr']
 print('Combined local build complete; verifying preservation and rendering.',flush=True)
 after=cat(L/'catalog.js');old={a['id']:a for a in before['assets']};new={a['id']:a for a in after['assets']}
 expected={a['id'] for a in f['media']+f['documents']}|{'lisan:doc:'+x['path'] for x in intake['added']}
 assert set(new)-set(old)==expected and not set(old)-set(new)
 revised={x['id']:x for x in intake.get('revised',[])}
 for aid,a in old.items():
  if aid not in revised:assert new[aid]==a,aid;continue
  change=revised[aid];check(change['afterSource'])
  assert a['kind']=='document' and a['sha256']==change['beforeSource']['sha256'] and a['bytes']==change['beforeSource']['bytes']
  assert set(a)==set(new[aid]) and all(new[aid][k]==v for k,v in a.items() if k not in change['allowedFields']),aid
  assert new[aid]['sha256']==change['afterSource']['sha256'] and new[aid]['bytes']==change['afterSource']['bytes']
  assert new[aid]['text']==(R/change['afterSource']['path']).read_text(encoding='utf-8-sig')
 record['reviewedDocumentRevisions']=list(revised);save('build_result.json',record)
 oldAlbums={a['id']:a for a in before['albums']};newAlbums={a['id']:a for a in after['albums']};assert set(newAlbums)-set(oldAlbums)=={a['id'] for a in f['albums']}
 assert all(newAlbums[k]==v for k,v in oldAlbums.items())
 for key in before:
  if key not in ['assets','albums','writerDevelopment','reviewDecisions','shotMaterials']:assert after[key]==before[key],key
 assert after['reviewDecisions']==review
 assert after['shotMaterials']['shots']==before['shotMaterials']['shots']+f['shots']
 for key in before['shotMaterials']:
  if key!='shots':assert after['shotMaterials'][key]==before['shotMaterials'][key]
 assert all(x in after['writerDevelopment']['associations'] for x in before['writerDevelopment']['associations'])
 for row in guards+inputs+w['documents']+w['excludedSources']:check(row)
 names=['test_flow_prototypes.cjs','test_source_comparison_publication.cjs','test_writer_publication.cjs','test_review_direct_clarification.cjs','test_reference_validation.cjs','test_working_bom.cjs','test_collections_navigation.cjs','test_outfit_navigation.cjs','test_tattoo_subject_collections.cjs','test_compact_browse.cjs','test_scene_readiness.cjs']
 with ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(lambda n:run(n,['D:/Program Files (x86)/node.exe',str(L/n)]),names))
 save('test_results.json',dict(passed=all(x['exitCode']==0 for x in results),results=results,browserVisualQA=False))
 for x in results:print(json.dumps(x),flush=True)
 assert all(x['exitCode']==0 for x in results),'Verification failure; no automatic rebuild'
 counts=dict(assets=len(after['assets']),albums=len(after['albums']),documents=sum(a['kind'] in ['document','pdf'] for a in after['assets']),reviews=len(review))
 save('SOURCE_PLACEMENT_CHECKPOINT.json',dict(checkedAtUTC=now(),catalog=pin(L/'catalog.js'),source=pin(L/'writer_development.json'),sourceFolderTextFiles=intake['sourceFolderTextFiles'],included=w['documents'],excluded=w['excludedSources']))
 handback=dict(status='local_publication_complete',completedAtUTC=now(),buildInvocations=1,catalog=pin(L/'catalog.js'),counts=counts,addedAssets=sorted(expected),newPortraitRatings=newReviews,board=pin(L/'character_reference_board.json'),flow=pin(L/'flow_prototypes.json'),writerCheckpoint=pin(E/'SOURCE_PLACEMENT_CHECKPOINT.json'),checks=pin(E/'test_results.json'),sourceFiles=inputs,preserved=dict(priorAssets=len(old),priorReviews=len(oldReviews),priorAlbums=len(oldAlbums),priorSceneReviewsAndTiming=True,priorSourceChoices=True,referenceValidationAndMouthCoverage=True,guardFiles=len(guards),originalMedia=True,authorFiles=True),browserVisualQA=False,limits='Local publication; renderer/handler/storage doubles and exact filesystem pins verified. No browser layout/playback verification or hosted deployment. Returned clips remain preliminary. No new provider run or scene acceptance by Site Index.')
 save('SITE_PUBLICATION_HANDBACK.json',handback);record.update(status='complete',completedAtUTC=now(),catalogAfter=pin(L/'catalog.js'),handback=pin(E/'SITE_PUBLICATION_HANDBACK.json'));save('build_result.json',record);print(json.dumps(record['handback']),flush=True)
except Exception as err:
 record.update(status='needs_attention',error=str(err),checkedAtUTC=now());save('build_result.json',record);raise
