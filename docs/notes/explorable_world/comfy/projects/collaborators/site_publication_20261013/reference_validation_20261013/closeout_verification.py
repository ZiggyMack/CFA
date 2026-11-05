from pathlib import Path
from datetime import datetime,timezone
import hashlib,json,uuid,re
R=Path('D:/Documents/CFA');P=R/'docs/notes/explorable_world/comfy/projects';L=P/'visual_library';E=P/'collaborators/site_publication_20261013/reference_validation_20261013';M=P/'collaborators/mailbox'
def now():return datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
def read(p):return json.loads(p.read_bytes())
def sha(b):return hashlib.sha256(b).hexdigest()
def save(name,value):(E/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def pin(p):
 raw=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),bytes=len(raw),sha256=sha(raw))
def check(row):assert pin(R/row['path'])=={k:row[k] for k in ['path','bytes','sha256']},row['path']
def cat(p):return json.loads(p.read_text(encoding='utf-8').split('=',1)[1].strip().removesuffix(';'))
record=read(E/'build_result.json');assert record['buildInvocations']==1 and record['build']['exitCode']==0 and record['status']=='needs_attention'
assert not (E/'SITE_PUBLICATION_HANDBACK.json').exists()
b=read(E/'preservation.before.json');w=read(L/'writer_development.json');v=read(L/'reference_validation.json');mouth=read(L/'mouth_coverage.json')
report=read(E/'test_results.json');assert report['passed'] and report['suites']==17 and len(report['results'])==17 and all(r['exitCode']==0 for r in report['results'])
assert len(b['guards'])==539 and len(w['documents'])==43 and len(w['excludedSources'])==8
for row in b['guards']+w['documents']+w['excludedSources']+record['sourceInputs']+report['testFiles']:check(row)
for criteria in v['criteriaSets']:
 for row in criteria['provenance']:check(row)
for row in mouth['sourcePins']+[mouth['recipe']['graph']]:check(row)
for row in mouth['media']:
 raw=(R/row['repoPath']).read_bytes();assert len(raw)==row['bytes'] and sha(raw)==row['sha256'],row['id']
oldcat=cat(E/'catalog.before.js');catalog=cat(L/'catalog.js')
assert sha((L/'catalog.js').read_bytes())=='b10ccce2252c723bba49f2410535623457833dc9b456cb1a261afc4203d79370'
verification=read(E/'preservation.after.json');check(verification['catalog'])
counts=dict(assets=len(catalog['assets']),albums=len(catalog['albums']),documents=sum(a['kind'] in ['document','pdf'] for a in catalog['assets']),media=sum(a['kind'] not in ['document','pdf'] for a in catalog['assets']))
assert counts==verification['counts']==dict(assets=2434,albums=229,documents=477,media=1957)
assert catalog['reviewDecisions']==oldcat['reviewDecisions'] and len(catalog['reviewDecisions'])==176
assert not re.search(r'C:[\\/]+Users[\\/]+|\bStephen\b',json.dumps(catalog,ensure_ascii=False))
assert len(read(P/'lisan_al_gaib/scene_map.json')['scenes'])==50
for key in verification['preservedCatalogSections']:assert catalog[key]==oldcat[key],key
assert len(v['assessments'])==10 and not any(a['status']=='pass' for a in v['assessments'])
verification.update(closeoutRecheckedAtUTC=now(),currentTestFiles=report['testFiles'],allSeventeenSuitesPassed=True,additionalBuildInvocations=0)
save('preservation.after.json',verification)
checkpoint=dict(schemaVersion=1,assignmentID=record['assignmentID'],owner='cfa_site_index',completedAtUTC=now(),source=pin(L/'writer_development.json'),catalog=pin(L/'catalog.js'),sourceFolderTextFiles=50,included=w['documents'],excluded=w['excludedSources'],reconciliation=pin(E/'WRITER_INTAKE_RECONCILIATION.json'),previousCheckpoint='docs/notes/explorable_world/comfy/projects/collaborators/site_publication_20261013/writer_visibility_20261013/SOURCE_PLACEMENT_CHECKPOINT.json')
save('SOURCE_PLACEMENT_CHECKPOINT.json',checkpoint)
identity=P/'collaborators/identity/cfa_site_index/I_AM.md'
assert not any(row['path']==identity.relative_to(R).as_posix() for row in b['guards'])
raw=identity.read_bytes();text=raw.decode();sep='\r\n' if '\r\n' in text else '\n';text=text.replace('\r\n','\n')
assert '## Reference validation and current coordination checkpoint' not in text
with (E/'I_AM.before_closeout.md').open('xb') as f:f.write(raw)
text=text.replace('The reference-validation evidence UI remains a separate pending item.','The reference-validation evidence UI is implemented; the current publication handback below records checks and limits.')
text=text.replace('The reference-validation evidence UI remains pending under its separately authorized concrete requirements. This ownership acknowledgment does not implement that feature or reopen the C13 source choice.','The reference-validation evidence UI and mouth board are locally published under the existing assignment. C13 source choice remains separate.')
text=text.replace('The existing direct-clarification test has a stale shared-harness signature; it is not reported as passed.','The former direct-clarification harness issue has been repaired; it now passes within the current 17-suite regression run. Initial failed results and test-only repairs are preserved in the publication evidence.')
addition="""
## Reference validation and current coordination checkpoint

Local implementation and one serialized build are recorded in [the publication handback](../../site_publication_20261013/reference_validation_20261013/SITE_PUBLICATION_HANDBACK.json). The current [writer checkpoint](../../site_publication_20261013/reference_validation_20261013/SOURCE_PLACEMENT_CHECKPOINT.json) supersedes the earlier checkpoint for active intake; its historical record remains intact. All 17 regression suites pass. Browser visual QA is still unverified. No hosted deployment or creative acceptance follows.

Ziggy directly authorized CFA-project messaging with Nova Dot and CFA NOVA, and routine use of site-maintenance scripts without repeated conversational approval. Native sandbox enforcement remains separate. New project outputs remain on D:. The preparation source lookup now uses verified project-owned D: evidence, with frozen original provenance preserved. Existing small C: helper originals may remain; their removal is not a task gate.

The [owner follow-up packet](../../site_publication_20261013/reference_validation_20261013/OWNER_METHOD_FOLLOWUPS.json) routes production-method/carepack links and bounded teaching findings through the existing owners. Those downstream edits are not claimed as completed by the site publication.
"""
identity.write_bytes((text+addition).replace('\n',sep).encode())
handback=dict(schemaVersion=1,assignmentID=record['assignmentID'],status='local_publication_complete_browser_visual_QA_unverified',owner='cfa_site_index',ownership='standing_owner_retained',completedAtUTC=now(),buildInvocations=1,catalog=pin(L/'catalog.js'),counts=counts,tests=dict(passed=True,suites=17,validationScenarios=19,evidence=pin(E/'test_results.json'),initialFailures=pin(E/'test_results.initial.json'),testOnlyRepairs=[pin(E/'regression_harness_repairs.json'),pin(E/'regression_harness_lisan_repair.json')]),preservation=pin(E/'preservation.after.json'),writerCheckpoint=pin(E/'SOURCE_PLACEMENT_CHECKPOINT.json'),referenceInventory=18,explicitReferenceNominations=8,criteriaSets=9,beta=dict(originalsActuallyViewed=7,assessments=10,characterFails=2,characterUncertain=3,sceneNotApplicable=5,overallPasses=0,attributedObservations=21),newReceivedMouthImages=41,guide=pin(L/'REFERENCE_VALIDATION_GUIDE.txt'),storageCorrection=pin(E/'STORAGE_SOURCE_REDIRECTION.json'),ownerFollowupPacket=pin(E/'OWNER_METHOD_FOLLOWUPS.json'),ownerFollowupStateAtCloseout='Prepared packet; coordinator handoff follows this closeout. Downstream edits and recipient acknowledgments are not inferred.',identity=pin(identity),remaining=['Browser visual QA remains policy-blocked; DOM/storage verification is distinct.','Scene-use declarations, unselected family/default references and future Lisan articulation criteria require owner reconciliation. No technical readiness inferred from empty declarations.','Owner method/carepack edits and downstream Claude/HaL/Pan routing remain with their owners; exact prepared packet is linked above.','Static evidence does not prove motion, lip sync or acceptance. V1 activation/calibration remain held by this site task.'],hostedDeployment=False,generation=False,spending=False,creativeAcceptanceChanged=False,originalMediaDeleted=False)
save('SITE_PUBLICATION_HANDBACK.json',handback)
with (E/'build_result.before_closeout.json').open('xb') as f:f.write((E/'build_result.json').read_bytes())
record.pop('error',None);record.update(status='complete',verificationCompletedAtUTC=now(),catalogAfter=pin(L/'catalog.js'),verification=pin(E/'preservation.after.json'),tests=pin(E/'test_results.json'),handback=pin(E/'SITE_PUBLICATION_HANDBACK.json'),closeoutScript=pin(E/'closeout_verification.py'))
save('build_result.json',record)
messageID=str(uuid.uuid4())
message=dict(schemaVersion=1,id=messageID,conversationId=str(uuid.uuid4()),createdAtUTC=now(),sender='cfa_site_index',recipient='nova',writtenBy='cfa_site_index',authorship='self_authored',subject='SITE_OWNER_RESULT: reference evidence UI, mouth coverage and current writer intake locally complete',replyTo=None,status='posted',body='One local build completed: 2434 assets / 229 albums / 477 documents / 1957 media. All 17 regression suites pass, including 19 evidence scenarios. Four old harness assumptions were repaired without rebuilding; failed results are preserved. All 176 canonical reviews, 539 guarded files, 51 current writer pins, previous albums and 50 Lisan scene rows/timing remain preserved. Added 41 received mouth images plus the evidence guide and Claude review document; refreshed two approved writer documents. Beta has 10 scoped records and zero overall passes. Browser visual QA remains policy-blocked; no hosted deployment, generation, spending or creative acceptance. Site edit/build ownership stays here. Please reconcile the attached owner packet through existing production/method/carepack and Claude/HaL/manual Pan routes; source-author files were not edited by this job. V1 calibration aliases and diagnostic answers are not imported or promoted by this publication.',attachments=[dict(**pin(E/'SITE_PUBLICATION_HANDBACK.json'),description='Exact completion, preservation and limitations'),dict(**pin(E/'OWNER_METHOD_FOLLOWUPS.json'),description='Prepared bounded owner follow-ups for established routing')],source=dict(type='local_verified_site_maintenance',threadId='01a13383-26f6-7923-8e18-98faf1fa3ede'))
with (M/'messages'/f'{messageID}.json').open('x',encoding='utf-8') as f:json.dump(message,f,ensure_ascii=False,indent=2)
save('CLOSEOUT_ROUTING.json',dict(createdAtUTC=now(),mailboxMessage=pin(M/'messages'/f'{messageID}.json'),mailboxStatus='posted; not proof of external delivery',coordinatorChatDelivery='Will be recorded by native message tool after closeout; not yet claimed.',ownerPacket=pin(E/'OWNER_METHOD_FOLLOWUPS.json')))
print(json.dumps(dict(status='complete',counts=counts,suites=17,buildInvocations=1,handback=pin(E/'SITE_PUBLICATION_HANDBACK.json'),mailboxMessageID=messageID)),flush=True)
