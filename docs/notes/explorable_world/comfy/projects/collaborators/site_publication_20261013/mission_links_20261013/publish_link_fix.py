from pathlib import Path
from datetime import datetime,timezone
from concurrent.futures import ThreadPoolExecutor
import json,hashlib,subprocess,sys,traceback
R=Path('D:/Documents/CFA');P=R/'docs/notes/explorable_world/comfy/projects';L=P/'visual_library';E=P/'collaborators/site_publication_20261013/mission_links_20261013'
def now():return datetime.now(timezone.utc).isoformat()
def read(p):return json.loads(p.read_bytes())
def pin(p):
 raw=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest())
def check(row):assert pin(R/row['path'])=={k:row[k] for k in ['path','bytes','sha256']},row['path']
def save(name,obj):(E/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def cat(p):return json.loads(p.read_text(encoding='utf-8').split('=',1)[1].strip().removesuffix(';'))
def run(name,args):
 result=subprocess.run(args,cwd=L,capture_output=True,text=True,encoding='utf-8',errors='replace')
 return dict(name=name,exitCode=result.returncode,stdout=result.stdout,stderr=result.stderr)
assert not (E/'build_result.json').exists(),'Inspect existing build record instead of repeating'
b=read(E/'preservation.before.json');w=read(L/'writer_development.json');reconcile=read(E/'writer_owner_reconciliation.json');link=read(E/'link_changes.json')
missionPath=link['sourceAfter']['path']
for row in b['guards']:
 if row['path']!=missionPath:check(row)
check(link['sourceAfter'])
for row in w['documents']+w['excludedSources']:check(row)
for row in b['inputs']:
 if not row['path'].endswith(('/build_catalog.py','/writer_development.json')):check(row)
for change in link['changes']:check(change['target'])
check(reconcile['ownerSourceRecord'])
for row in reconcile['ownerFiles']:check(dict(path=row['path'],bytes=row['afterBytes'],sha256=row['afterSHA256']))
before=cat(E/'catalog.before.js');assert (L/'catalog.js').read_bytes()==(E/'catalog.before.js').read_bytes()
inputs=[pin(L/n) for n in ['library.js','library.css','build_catalog.py','reference_validation.json','mouth_coverage.json','writer_development.json','REFERENCE_VALIDATION_GUIDE.txt','reference_provenance.py','reference_provenance_snapshots.json']]
record=dict(assignmentID='mission-link-repair-20261013',status='running',startedAtUTC=now(),owner='cfa_site_index',buildInvocations=1,sourceInputs=inputs,catalogBefore=pin(L/'catalog.js'))
save('build_result.json',record)
try:
 built=run('build_catalog.py',[sys.executable,'-B',str(L/'build_catalog.py')]);record['build']=built;save('build_result.json',record);assert built['exitCode']==0,built['stderr']
 print('Single local build completed; verifying links and preservation.',flush=True)
 after=cat(L/'catalog.js');old={a['id']:a for a in before['assets']};new={a['id']:a for a in after['assets']}
 expected='lisan:doc:'+reconcile['addedDocument']['path'];assert set(new)-set(old)=={expected};assert not set(old)-set(new)
 allowedPaths={r['path'] for r in reconcile['ownerFiles']}|{r['after']['path'] for r in reconcile['revisedWriterSources']}
 changed=[]
 for aid,asset in old.items():
  if asset!=new[aid]:
   fields=[k for k in set(asset)|set(new[aid]) if asset.get(k)!=new[aid].get(k)]
   assert asset['repoPath'] in allowedPaths and set(fields)<={'text','sha256','bytes','note'},(aid,fields)
   changed.append(dict(assetID=aid,fields=fields))
 for key in before:
  if key not in ['assets','missionControl','writerDevelopment']:assert after[key]==before[key],key
 assert after['missionControl']==read(P/'collaborators/mission_control.json')
 assert after['writerDevelopment']['associations']==before['writerDevelopment']['associations']
 assert len(after['reviewDecisions'])==176
 for row in b['guards']:
  if row['path']!=missionPath:check(row)
 for row in inputs+w['documents']+w['excludedSources']:check(row)
 counts=dict(assets=len(after['assets']),albums=len(after['albums']),documents=sum(a['kind'] in ['document','pdf'] for a in after['assets']),media=sum(a['kind'] not in ['document','pdf'] for a in after['assets']))
 assert counts==dict(assets=2435,albums=229,documents=478,media=1957),counts
 tests=[('mission_links',['D:/Program Files (x86)/node.exe',str(E/'verify_mission_links.cjs')])]+[(n,['D:/Program Files (x86)/node.exe',str(L/n)]) for n in ['test_source_comparison_publication.cjs','test_writer_publication.cjs','test_reference_validation.cjs']]
 with ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(lambda row:run(*row),tests))
 save('test_results.json',dict(checkedAtUTC=now(),passed=all(r['exitCode']==0 for r in results),results=results,browserVisualQA=False,provenanceHelperIndependentReview=dict(checks=11,actualProvenanceChecks=32,currentSources=25,historicalSources=7,criteriaDigests=9,passed=True,method='Read-only subagent compiled helper and mocked Path.read_bytes; no builder import or writes.')))
 for r in results:print(json.dumps(r),flush=True)
 assert all(r['exitCode']==0 for r in results),'Verification failed; no automatic rebuild'
 checkpoint=dict(schemaVersion=1,assignmentID=record['assignmentID'],owner='cfa_site_index',completedAtUTC=now(),source=pin(L/'writer_development.json'),catalog=pin(L/'catalog.js'),sourceFolderTextFiles=51,included=w['documents'],excluded=w['excludedSources'],reconciliation=pin(E/'writer_owner_reconciliation.json'),previousCheckpoint='docs/notes/explorable_world/comfy/projects/collaborators/site_publication_20261013/reference_validation_20261013/SOURCE_PLACEMENT_CHECKPOINT.json')
 save('SOURCE_PLACEMENT_CHECKPOINT.json',checkpoint)
 handback=dict(assignmentID=record['assignmentID'],status='local_fix_complete',completedAtUTC=now(),buildInvocations=1,catalog=pin(L/'catalog.js'),counts=counts,links=link['changes'],checks=pin(E/'test_results.json'),writerCheckpoint=pin(E/'SOURCE_PLACEMENT_CHECKPOINT.json'),historicalEvidenceRegistry=pin(L/'reference_provenance_snapshots.json'),preserved=dict(canonicalReviews=176,existingAssets=len(old),existingAlbums=len(before['albums']),guardFiles=539,guardFilesUnchanged=538,oneGuardChangedOnlyThreeHrefs=True,allSourceComparisons=True,allSceneReviewsAndTiming=True,referenceValidationAndMouthCoverage=True,priorWriterAssociations=True,sourceAuthorFilesUnmodified=True),reconciledExistingDocumentPreviews=changed,newWriterDocument=expected,browserVisualQA=False,limits='Browser automation rejects file://; verified actual renderer output and filesystem targets from all five entry shells, plus existing DOM/storage tests. No hosted deployment.',queuedSeparateAssignments=reconcile['queuedSeparateAssignments'])
 save('SITE_PUBLICATION_HANDBACK.json',handback)
 identity=P/'collaborators/identity/cfa_site_index/I_AM.md';text=identity.read_text(encoding='utf-8')
 addition='\n## Mission Control link repair checkpoint\n\nThe three project-relative brief links are corrected by [this handback](../../site_publication_20261013/mission_links_20261013/SITE_PUBLICATION_HANDBACK.json). The [writer checkpoint](../../site_publication_20261013/mission_links_20261013/SOURCE_PLACEMENT_CHECKPOINT.json) now covers 44 included and eight excluded sources. The current owner prose is preserved; original criteria provenance uses a verified historical text snapshot without repinning assessments. Later source-choice and character-board assignments are separate queued work.\n'
 assert '## Mission Control link repair checkpoint' not in text
 identity.write_text(text+addition,encoding='utf-8')
 record.update(status='complete',completedAtUTC=now(),catalogAfter=pin(L/'catalog.js'),handback=pin(E/'SITE_PUBLICATION_HANDBACK.json'));save('build_result.json',record)
 print(json.dumps(dict(status='complete',catalogSHA256=record['catalogAfter']['sha256'],handback=record['handback'],counts=counts)),flush=True)
except Exception as error:
 record.update(status='needs_attention',error=str(error),checkedAtUTC=now());save('build_result.json',record);raise
