from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
import hashlib,json,subprocess,sys,urllib.parse,traceback
R=Path('D:/Documents/CFA');P=R/'docs/notes/explorable_world/comfy/projects';L=P/'visual_library';E=P/'collaborators/site_publication_20261013/reference_validation_20261013'
NODE='D:/Program Files (x86)/node.exe'
def now():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):return json.loads(p.read_bytes())
def save(name,value): (E/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=sha(b))
def pinned(row):
 b=(R/row['path']).read_bytes();assert len(b)==row['bytes'] and sha(b)==row['sha256'],row['path']
def catalog(p):return json.loads(p.read_text(encoding='utf-8').split('=',1)[1].strip().removesuffix(';'))
def run(name,args):
 result=subprocess.run(args,cwd=L,capture_output=True,text=True,encoding='utf-8',errors='replace')
 row=dict(name=name,exitCode=result.returncode,stdout=result.stdout,stderr=result.stderr)
 try:row['result']=json.loads(result.stdout)
 except:pass
 return row
assert not (E/'build_result.json').exists(),'Build record exists; inspect it instead of rebuilding'
b=read(E/'preservation.before.json');w=read(L/'writer_development.json');v=read(L/'reference_validation.json');m=read(L/'mouth_coverage.json')
reconciliation=read(E/'WRITER_INTAKE_RECONCILIATION.json')
for row in b['guards']+w['documents']+w['excludedSources']:pinned(row)
assert len(w['documents'])==43 and len(w['excludedSources'])==8
allowed={'library.js','library.css','build_catalog.py','writer_development.json','test_scene_readiness.cjs','test_review_direct_clarification.cjs'}
for row in b['sourceFiles']:
 if Path(row['path']).name not in allowed:pinned(row)
before=catalog(E/'catalog.before.js');assert (L/'catalog.js').read_bytes()==(E/'catalog.before.js').read_bytes()
inputs=[pin(L/n) for n in ['library.js','library.css','build_catalog.py','reference_validation.json','mouth_coverage.json','writer_development.json','REFERENCE_VALIDATION_GUIDE.txt']]
for row in m['sourcePins']+[m['recipe']['graph']]:pinned(row)
for row in v['criteriaSets']:
 content={k:x for k,x in row.items() if k!='sha256'}
 assert sha(json.dumps(content,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode())==row['sha256']
 for source in row['provenance']:pinned(source)
for row in m['media']:
 raw=(R/row['repoPath']).read_bytes();assert len(raw)==row['bytes'] and sha(raw)==row['sha256']
assert len(m['media'])==41 and len(v['assessments'])==10 and not any(a['status']=='pass' for a in v['assessments'])
compile((L/'build_catalog.py').read_bytes(),str(L/'build_catalog.py'),'exec')
pretests=[run('syntax',[NODE,'--check',str(L/'library.js')]),run('validation-prebuild',[NODE,str(L/'test_reference_validation.cjs')])]
save('preflight_result.json',dict(checkedAtUTC=now(),guards=539,writerPins=51,inputs=inputs,tests=pretests,passed=all(x['exitCode']==0 for x in pretests)))
assert all(x['exitCode']==0 for x in pretests),'Prebuild checks failed'
print('Preflight passed: 539 guards, 51 reconciled writer pins, 19 evidence scenarios.',flush=True)
for row in b['guards']+w['documents']+w['excludedSources']+inputs:pinned(row)
record=dict(assignmentID='reference-validation-evidence-ui-20261013',owner='cfa_site_index',buildInvocations=1,startedAtUTC=now(),status='running',catalogBefore=pin(L/'catalog.js'),sourceInputs=inputs)
with (E/'build_result.json').open('x',encoding='utf-8') as f:json.dump(record,f,indent=2)
try:
 built=run('build_catalog.py',[sys.executable,'-B',str(L/'build_catalog.py')]);record.update(completedAtUTC=now(),build=built,status='built' if built['exitCode']==0 else 'build_failed');save('build_result.json',record);assert built['exitCode']==0,built['stderr']
 print('Local build completed. Verifying catalog preservation and integrated behavior.',flush=True)
 after=catalog(L/'catalog.js');old={a['id']:a for a in before['assets']};new={a['id']:a for a in after['assets']}
 newDoc='lisan:doc:docs/notes/explorable_world/comfy/projects/lisan_al_gaib/story/writer_pass_20261012/DEEPSEEK_RETURNS_REVIEW_20261013.md'
 guideID='hon:doc:docs/notes/explorable_world/comfy/projects/visual_library/REFERENCE_VALIDATION_GUIDE.txt'
 expectedNew={a['id'] for a in m['media']}|{newDoc,guideID};assert set(new)-set(old)==expectedNew;assert not set(old)-set(new)
 changedIDs={'lisan:doc:'+row['path'] for row in reconciliation['revisedSources']}
 changes=[]
 for aid,a in old.items():
  if a!=new[aid]:
   fields=[key for key in set(a)|set(new[aid]) if a.get(key)!=new[aid].get(key)]
   assert aid in changedIDs and set(fields)<={'text','sha256','bytes','note'},(aid,fields)
   changes.append(dict(assetID=aid,fields=fields))
 oldAlbums={a['id']:a for a in before['albums']};newAlbums={a['id']:a for a in after['albums']}
 assert set(newAlbums)-set(oldAlbums)=={'lisan:mouth-natural-r2','lisan:mouth-grill-later-repairs'}
 assert all(newAlbums.get(k)==value for k,value in oldAlbums.items())
 preservedSections=[k for k in before if k not in ['assets','albums','writerDevelopment']]
 for key in preservedSections:assert after[key]==before[key],key
 assert after['writerDevelopment']['associations']==before['writerDevelopment']['associations']
 assert after['referenceValidation']==v and after['mouthCoverage']=={k:x for k,x in m.items() if k!='media'}
 for item in m['media']:
  a=new[item['id']];path=(L/urllib.parse.unquote(a['src'])).resolve();assert sha(path.read_bytes())==item['sha256']
 for row in b['guards']+w['documents']+w['excludedSources']+inputs:pinned(row)
 assert len(after['reviewDecisions'])==176
 assert len(read(P/'lisan_al_gaib/scene_map.json')['scenes'])==50
 counts=dict(assets=len(after['assets']),albums=len(after['albums']),documents=sum(a['kind'] in ['document','pdf'] for a in after['assets']),media=sum(a['kind'] not in ['document','pdf'] for a in after['assets']))
 assert counts==dict(assets=2434,albums=229,documents=477,media=1957),counts
 import re
 assert not re.search(r'C:[\\/]+Users[\\/]+|\\bStephen\\b',json.dumps(after,ensure_ascii=False))
 verification=dict(checkedAtUTC=now(),counts=counts,canonicalReviews=176,guardFilesUnchanged=539,currentWriterPinsVerified=51,legacyAssetsPreserved=len(old)-len(changes),reconciledWriterAssets=changes,newAssetIDs=sorted(expectedNew),existingAlbumsUnchanged=len(oldAlbums),preservedCatalogSections=preservedSections,priorWriterAssociationsUnchanged=True,acceptedLisanSceneRows=50,sourceFiles=inputs,catalog=pin(L/'catalog.js'),browserVisualQA=False)
 save('preservation.after.json',verification)
 tests=['test_reference_validation.cjs','test_scene_readiness.cjs','test_review_direct_clarification.cjs','test_reference_scope.cjs','test_working_bom.cjs','test_creative_review.cjs','test_scene_craft.cjs','test_collections_navigation.cjs','test_compact_browse.cjs','test_source_comparison_publication.cjs','test_tattoo_subject_collections.cjs','test_cast_character_hub.cjs','test_head_anchor_group.cjs','test_collaborator_profiles.cjs','test_review_requests.cjs','test_outfit_navigation.cjs','test_writer_publication.cjs']
 with ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(lambda name:run(name,[NODE,str(L/name)]),tests))
 passed=all(x['exitCode']==0 for x in results)
 testreport=dict(checkedAtUTC=now(),passed=passed,suites=len(results),results=results,browserVisualQA=False,limits='Real renderer and bound handlers with DOM/storage doubles; no native browser layout or screenshot verification.')
 save('test_results.json',testreport)
 for result in results:print(json.dumps({k:result[k] for k in ['name','exitCode']}),flush=True)
 assert passed,'Integrated tests failed; see test_results.json'
 for row in b['guards']+w['documents']+w['excludedSources']+inputs:pinned(row)
 checkpoint=dict(schemaVersion=1,assignmentID=record['assignmentID'],owner='cfa_site_index',completedAtUTC=now(),source=pin(L/'writer_development.json'),catalog=pin(L/'catalog.js'),sourceFolderTextFiles=50,included=w['documents'],excluded=w['excludedSources'],reconciliation=pin(E/'WRITER_INTAKE_RECONCILIATION.json'),previousCheckpoint='docs/notes/explorable_world/comfy/projects/collaborators/site_publication_20261013/writer_visibility_20261013/SOURCE_PLACEMENT_CHECKPOINT.json')
 save('SOURCE_PLACEMENT_CHECKPOINT.json',checkpoint)
 handback=dict(schemaVersion=1,assignmentID=record['assignmentID'],status='local_publication_complete_browser_visual_QA_unverified',owner='cfa_site_index',ownership='standing_owner_retained',completedAtUTC=now(),buildInvocations=1,catalog=pin(L/'catalog.js'),counts=counts,tests=dict(passed=True,suites=len(results),validationScenarios=19,evidence=pin(E/'test_results.json')),preservation=pin(E/'preservation.after.json'),writerCheckpoint=pin(E/'SOURCE_PLACEMENT_CHECKPOINT.json'),referenceInventory=18,explicitReferenceNominations=8,criteriaSets=9,beta=dict(originalsActuallyViewed=7,assessments=10,characterFails=2,characterUncertain=3,sceneNotApplicable=5,overallPasses=0,attributedObservations=21),newReceivedMouthImages=41,guide=pin(L/'REFERENCE_VALIDATION_GUIDE.txt'),storageCorrection=pin(E/'STORAGE_SOURCE_REDIRECTION.json'),remaining=['Browser visual QA remains policy-blocked; DOM/storage verification is distinct.','Scene-use declarations, unselected family/default references and future Lisan articulation criteria require owner reconciliation. No technical readiness inferred from empty declarations.','Owner-routed method/carepack crosslinks and bounded Pan teaching return are prepared in OWNER_METHOD_FOLLOWUPS.json.','Static evidence does not prove motion, lip sync or acceptance. V1 activation/calibration remain held.'],hostedDeployment=False,generation=False,spending=False,creativeAcceptanceChanged=False,originalMediaDeleted=False)
 save('SITE_PUBLICATION_HANDBACK.json',handback)
 identity=P/'collaborators/identity/cfa_site_index/I_AM.md';assert not any(row['path']==identity.relative_to(R).as_posix() for row in b['guards'])
 text=identity.read_text(encoding='utf-8')
 text=text.replace('The reference-validation evidence UI remains a separate pending item.','The reference-validation evidence UI is implemented; the current publication handback below records checks and limits.')
 text=text.replace('The reference-validation evidence UI remains pending under its separately authorized concrete requirements. This ownership acknowledgment does not implement that feature or reopen the C13 source choice.','The reference-validation evidence UI and mouth board are locally published under the existing assignment. C13 source choice remains separate.')
 addition='\n## Reference validation and current coordination checkpoint\n\nLocal implementation and one serialized build are recorded in [the publication handback](../../site_publication_20261013/reference_validation_20261013/SITE_PUBLICATION_HANDBACK.json). The current [writer checkpoint](../../site_publication_20261013/reference_validation_20261013/SOURCE_PLACEMENT_CHECKPOINT.json) supersedes the earlier checkpoint for active intake; its historical record remains intact. Browser visual QA is still unverified. No hosted deployment or creative acceptance follows.\n\nZiggy directly authorized CFA-project messaging with Nova Dot and CFA NOVA, and routine use of site-maintenance scripts without repeated conversational approval. Native sandbox enforcement remains separate. New project outputs remain on D:. The preparation source lookup now uses verified project-owned D: evidence, with frozen original provenance preserved. Existing small C: helper originals may remain; their removal is not a task gate.\n'
 assert '## Reference validation and current coordination checkpoint' not in text
 identity.write_text(text+addition,encoding='utf-8')
 record.update(status='complete',catalogAfter=pin(L/'catalog.js'),verification=pin(E/'preservation.after.json'),tests=pin(E/'test_results.json'),handback=pin(E/'SITE_PUBLICATION_HANDBACK.json'));save('build_result.json',record)
 print(json.dumps({'status':'complete','counts':counts,'testSuites':len(results),'catalogSHA256':record['catalogAfter']['sha256'],'handbackSHA256':record['handback']['sha256']}),flush=True)
except Exception as error:
 record.update(status='needs_attention',error=str(error),checkedAtUTC=now());save('build_result.json',record);traceback.print_exc();raise
