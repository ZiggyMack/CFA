from pathlib import Path
from datetime import datetime, timezone
import json, hashlib

R=Path('D:/Documents/CFA'); P=R/'docs/notes/explorable_world/comfy/projects'; L=P/'visual_library'; E=Path(__file__).parent
def read(p): return json.loads(p.read_bytes())
def cat(p): return json.loads(p.read_text(encoding='utf-8').split('=',1)[1].strip().removesuffix(';'))
def pin(p):
    b=p.read_bytes(); return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(name,value): (E/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

record=read(E/'build_result.json')
assert record['buildInvocations']==1 and record['build']['exitCode']==0
assert record['reviewedDocumentRevisions'], 'Reviewed existing-document exception was verified before the test stage'
before=cat(E/'catalog.js.before'); after=cat(L/'catalog.js'); intake=read(E/'writer_intake.json'); flow=read(L/'flow_prototypes.json'); writer=read(L/'writer_development.json')
old={a['id']:a for a in before['assets']}; new={a['id']:a for a in after['assets']}
expected={a['id'] for a in flow['media']+flow['documents']}|{'lisan:doc:'+d['path'] for d in intake['added']}
assert set(new)-set(old)==expected and not set(old)-set(new)
revised={d['id']:d for d in intake['revised']}
for aid,a in old.items():
    if aid not in revised: assert a==new[aid],aid
    else:
        allowed=revised[aid]['allowedFields']; assert set(a)==set(new[aid])
        assert all(new[aid][k]==v for k,v in a.items() if k not in allowed)
        assert new[aid]['sha256']==revised[aid]['afterSource']['sha256']
old_albums={a['id']:a for a in before['albums']}; new_albums={a['id']:a for a in after['albums']}
assert all(new_albums[k]==v for k,v in old_albums.items())
assert set(new_albums)-set(old_albums)=={a['id'] for a in flow['albums']}
for key in before:
    if key not in ['assets','albums','writerDevelopment','reviewDecisions','shotMaterials']: assert after[key]==before[key],key
assert after['shotMaterials']['shots']==before['shotMaterials']['shots']+flow['shots']
for key in before['shotMaterials']:
    if key!='shots': assert after['shotMaterials'][key]==before['shotMaterials'][key]
old_reviews={r['id']:r for r in before['reviewDecisions']}; new_reviews={r['id']:r for r in after['reviewDecisions']}
assert all(new_reviews[k]==v for k,v in old_reviews.items())
assert set(new_reviews)-set(old_reviews)=={'LAG-602a9fd4021dc356','LAG-63126392af1ccf8b'}
for row in writer['documents']+writer['excludedSources']:
    assert pin(R/row['path'])=={k:row[k] for k in ['path','bytes','sha256']},row['path']

initial=read(E/'test_results.json')
if not (E/'test_results.initial_failure.json').exists(): save('test_results.initial_failure.json',initial)
results=[r for r in initial['results'] if r['name']!='test_reference_validation.cjs']
results.append(read(E/'reference_validation_rerun.json'))
for filename,test in [('comfy_test_result.json','test_comfy_collections.cjs'),('gun_variants_test_result.json','test_mission_gun_variants.cjs')]:
    evidence=read(E/filename)
    if 'exitCode' in evidence:
        results.append(dict(name=test,exitCode=evidence['exitCode'],stdout=evidence['stdout'],stderr=evidence.get('stderr',''),evidence=pin(E/filename)))
    else:
        assert evidence['result']['passed'] is True
        assert all(r['exitCode']==0 and r['result']['passed'] for r in evidence['relatedTests'])
        results.append(dict(name=test,passed=True,result=evidence['result'],relatedTests=evidence['relatedTests'],evidence=pin(E/filename)))
assert len(results)==13 and all(r.get('exitCode')==0 or r.get('passed') is True for r in results)
save('test_results.json',dict(passed=True,results=results,browserVisualQA=False,repair='The stale mouth-board test now targets Working References; no rebuild was performed. Later user-directed Comfy and mission-count coverage added.'))
save('SOURCE_PLACEMENT_CHECKPOINT.json',dict(catalog=pin(L/'catalog.js'),source=pin(L/'writer_development.json'),sourceFolderTextFiles=intake['sourceFolderTextFiles'],included=writer['documents'],excluded=writer['excludedSources']))
counts=dict(assets=len(after['assets']),albums=len(after['albums']),documents=sum(a['kind'] in ['document','pdf'] for a in after['assets']),reviews=len(after['reviewDecisions']))
completed=datetime.now(timezone.utc).isoformat()
handback=dict(status='local_publication_complete',completedAtUTC=completed,buildInvocations=1,catalog=pin(L/'catalog.js'),counts=counts,addedAssets=sorted(expected),reviewedExistingDocumentUpdates=list(revised),portraitRatings=[new_reviews[k] for k in sorted(set(new_reviews)-set(old_reviews))],board=pin(L/'character_reference_board.json'),flow=pin(L/'flow_prototypes.json'),writerCheckpoint=pin(E/'SOURCE_PLACEMENT_CHECKPOINT.json'),checks=pin(E/'test_results.json'),runtime=[pin(L/'library.js'),pin(L/'library.css')],runtimeChangesAfterBuild=['Piercings and jewelry selected-route heading','Browser-aware outfit gun review count and complete target list'],preserved=dict(priorAssetsExceptReviewedDocumentUpdate=len(old)-len(revised),allOriginalMedia=True,priorReviews=len(old_reviews),priorAlbums=len(old_albums),priorSceneReviewsAndTiming=True,priorSourceChoices=True,referenceValidationAndMouthCoverage=True,authorFiles=True),pendingSeparateReviewRefresh='A later user export (19) is with CFA NOVA for intake; this checkpoint records the 178-review build before that new input.',novaDotBrief=pin(P/'collaborators/mailbox/messages/10537c9f-3d65-4d63-9b90-1b01eba035df.json'),browserVisualQA=False,limits='Local site only. Actual renderer and handlers tested with DOM/storage doubles and exact source pins. No browser visual or video-playback verification, generation or hosted deployment.')
save('SITE_PUBLICATION_HANDBACK.json',handback)
record.update(status='complete',completedAtUTC=completed,catalogAfter=pin(L/'catalog.js'),handback=pin(E/'SITE_PUBLICATION_HANDBACK.json'),verificationRepair='Stale test route corrected; existing build finalized without rebuilding.')
record.pop('error',None);save('build_result.json',record)
print(json.dumps(record['handback']))
