from pathlib import Path
from datetime import datetime, timezone
import json, hashlib
R=Path('D:/Documents/CFA');P=R/'docs/notes/explorable_world/comfy/projects';L=P/'visual_library';E=Path(__file__).parent
def read(p):return json.loads(p.read_bytes())
def save(p,v):p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def pin(p):
 b=p.read_bytes();return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def doc(project,p,label):return dict(assetID=project+':doc:'+p.relative_to(R).as_posix(),label=label)
now=datetime.now(timezone.utc).isoformat()
assert (E/'baseline.json').exists() and not (E/'source_update.json').exists()
J=P/'lisan_al_gaib/handoffs/james_gun_removal_20261014';j=read(J/'RESULT_INTAKE.json')
assert pin(J/'RESULT_INTAKE.json')['sha256']=='0143813bd5876ff8e6144db2f7fd3f622a549f66fed60bac22bd82545e0dda5b'
for row in [j['source'],j['output'],j['adoptionRecord'],j['technicalReview'],*j['receivedFiles']]:
 assert pin(R/row['path'])=={k:row[k] for k in ['path','bytes','sha256']},row['path']
source=j['source']['assetID'];draft=j['output']['assetID'];boss='HD-RETURN-8421e7cfa1a0'
receipt=P/'hon_dolo_strictly_business/feedback/boss_selection_20261014_46c7936e-274a-4e8e-9a3f-82a92a9c7983/SELECTION_RECEIPT.json'
assert pin(receipt)['sha256']=='8d2814cd33cb4f00a049eb9ea0380c8358b27d8d3673ea73519dfc6c6c8c6bf0'
M=read(P/'collaborators/mission_control.json');tasks={t['id']:t for t in M['tasks']}
t=tasks['comfy-report-decisions-20261013']
t.setdefault('phaseHistory',[]).append({k:t[k] for k in ['title','status','summary','nextAction','missing','project','priority']})
t.update(project='lisan',title='SW-2 prototype received · video review pending',priority='normal',status='needs_input',receiptState='prototype_received_awaiting_video_review',comparisonInHistory=True,previewAssetIDs=[],updatedAtUTC=now,
 summary='The eight-second SW-2 Flow prototype has returned from the selected C13 patch-c image. It is Preliminary and awaits video review. Sampled frames show mouth opening and the audio track is non-silent. Earlier Hon Comfy mask and identity tests remain separate diagnostic work, with corrections scheduled later.',
 nextAction='Watch and listen to the returned clip, then review its movement, action, mouth behavior, camera and worm motion. Record character defects separately from direction feedback. The starting-image choice is already saved.',
 missingLabel='Review to complete',missing=['Video and audio review of the returned prototype; no production acceptance is recorded.'],
 links=[dict(label='Watch SW-2 · The rise · returned prototype',assetID='FLOW-LAG-SW2-001'),
 dict(label='SW-2 result intake and measured limits',href='../lisan_al_gaib/flow/sw2_prototype_20261013/RESULT_INTAKE.json'),
 *[dict(link,label=('Earlier: '+link['label'])) for link in t['links']]])
t=tasks['grok-boss-discovery'];t.setdefault('phaseHistory',[]).append({k:t[k] for k in ['title','status','summary','nextAction','missing','userSelection']})
t.update(title='Crocodile boss selected · golden reference saved',status='done',priority='normal',updatedAtUTC=now,receiptState='user_selected_visible_character_reference',
 summary='BOSS-008, the crocodile, is Ziggy’s first-choice boss. This exact image is the golden reference for visible likeness and proportions. Earlier candidates remain as alternatives; candidate 9 stays the bartender and 6 stays the bouncer.',
 nextAction='Use the selected crocodile as the starting reference for later boss work. Keep the recognizable look and build; proposed refinements and unseen views still need review.',missing=[],previewAssetIDs=[],
 links=[dict(label='Selected crocodile · golden reference',assetID=boss),dict(label='Boss character and earlier alternatives',href='#hon/cast/hon%3Aboss-round01'),doc('hon',receipt,'Recorded crocodile selection')])
t['userSelection']=dict(t['userSelection'],date='2026-10-14',finalBossSelected=True,selectedID='BOSS-008',selectedAssetID=boss,scope='Visible likeness and proportions of this exact image; unseen views and future derivatives are not approved.')
assert 'grok-james-gun-removal-20261014' not in tasks
M['tasks'].append(dict(id='grok-james-gun-removal-20261014',provider='Grok',project='lisan',title='James · gun-removal draft needs repair',status='in_progress',priority='normal',updatedAtUTC=now,
 summary='James is Lisan Al Gaib’s brother, using the character and visible look you selected. The gun-removal draft has returned, but the belt and trousers patch is visibly unfinished, with small metallic remnants. It is not an accepted master.',
 nextAction='The team must resolve the localized repair before presenting a clean result for your review. Keep the original character, tattoos, coat, jewelry, pose and setting. No additional generation is launched by this card.',
 deliverables=['A clean gun-area repair that preserves the selected visible character and scene.'],missing=[],
 links=[dict(label='Open James character',href='#lisan/cast/lisan%3Acast-james'),dict(label='Inspect returned repair draft',assetID=draft),dict(label='Original selected character · Hon source',assetID=source),doc('lisan',J/'RESULT_INTAKE.json','James return and repair findings'),doc('lisan',R/j['adoptionRecord']['path'],'James adoption and scope')],generationAuthorizedByThisCard=False))
save(P/'collaborators/mission_control.json',M)
C=read(L/'cast_collections.json');g=next(g for g in C['collections'] if g['id']=='hon:boss-round01')
g.update(title='Crocodile boss',coverID=boss,representativeID=boss,currentIDs=[boss],workingReferenceIDs=[boss],historyIDs=[i for i in g['assetIDs'] if i!=boss],preferredIDs=[],role='Selected boss · visible golden reference',
 notes=['Ziggy selected BOSS-008 as the first-choice boss. Preserve this exact visible likeness and proportions; avoid an unexplained redesign or heavier build.','Small improvements can be proposed. Unseen body views, new scenes and future derivatives still need review.','The other discovery candidates are retained under earlier studies in Working references. Candidate 9 remains the bartender and candidate 6 the bouncer.'])
for aid in ['HD-RETURN-339cdbe1e03a','HD-RETURN-e18185bdab18','HD-RETURN-9143639db1cf']:
 C['assetOverrides'][aid]['noteAppend']='Earlier boss shortlist alternative; BOSS-008 crocodile is now the selected boss. This alternate image retains its own review.'
C['assetOverrides'][boss]=dict(selectionStatus='user_selected_visible_golden_reference',sourceStatus='Selected boss · visible likeness and proportions',referenceRole='selected_character_reference',note='Ziggy selected this exact crocodile as the first-choice boss and golden visible reference. Preserve its recognizable likeness and proportions. Unseen views and future derivatives remain subject to review.')
for old in C['collections']:
 old['notes']=[n.replace('This collection does not select the final boss from the separate discovery round.','Earlier boss studies; the selected crocodile is in the separate Crocodile boss character hub.') for n in old.get('notes',[])]
C['collections'].append(dict(id='lisan:cast-james',project='lisan',title='James · Lisan’s brother',coverID=source,representativeID=source,assetIDs=[source,draft],currentIDs=[source],workingReferenceIDs=[source],referenceAssetIDs=[draft],relatedAssetIDs=[draft],role='Selected character · repair draft needs fixes',
 sharedReferences=[dict(assetID=source,sha256=j['source']['sha256'],sourceProject='hon',evidencePath=j['adoptionRecord']['path'])],
 description='The selected man and his visible look are James, Lisan Al Gaib’s brother. The original is retained here as the character reference. The returned gun-removal image is a repair draft, not an accepted master.',
 notes=['Keep the visible tattoos, coat, jewelry, pose and setting. Remove the gun only.','The original still carries its Hon-context review; that record is not a James approval or rejection.','The returned draft has repeated belt details, a grey trousers smear, residual metal and a soft patch edge. Age, powers and backstory beyond the brother relationship remain undecided.']))
save(L/'cast_collections.json',C)
media={k:j['output'][k] for k in ['path','bytes','sha256','width','height','project','characterID']}
media.update(id=draft,kind='image',category='cast',group='cast-james-revisions',groupTitle='James · revision drafts',title='James · gun-removal draft',referenceRole='cast_revision_draft',sourceStatus='Blocking draft · technical fixes required; human review pending',storyboardStage='preliminary',masterApproved=False,productionReady=False,sourceAssetIDs=[source],note='CFA Nova technical review: repeated belt details, grey trousers smear, residual metal and soft patch edge. No human acceptance recorded. The original character remains the selected visible reference.',tags=['James','Lisan’s brother','gun-removal repair','draft'],sourceIntake='JAMES-GUN-REMOVAL-20261014')
save(L/'cast_revisions.json',dict(format='cfa-cast-revisions-v1',sourcePins=[pin(J/'RESULT_INTAKE.json'),j['adoptionRecord'],j['technicalReview'],{k:j['source'][k] for k in ['path','bytes','sha256']}],media=[media]))
W=read(L/'writer_development.json');folder=P/'lisan_al_gaib/story/writer_pass_20261012'
expected={'DECISIONS_20261012.md':'ae9e8203a43fc80f375ff03840cc0658929d9c3b6213e0a5c10a557a9c0f7974','START_HERE.txt':'13aaa651c1253d7ada5711b1596eb052e27b5f6731832d0dc7c13769fd8f949e','CHARACTER_JAMES_20261014.md':'642c4b6d71775989ab9074de98ae6ca0a959ac0eab7ab4474e19ddfcd9b2b530'}
for name,h in expected.items():assert pin(folder/name)['sha256']==h,name
for item in W['documents']:
 if item['path'] in [(folder/n).relative_to(R).as_posix() for n in list(expected)[:2]]:
  item.update(pin(R/item['path']));item['context']+=' Decision 56 records James’s adoption; the writer’s expanded backstory remains proposed. The later technical intake records a returned repair draft that needs fixes.'
new=pin(folder/'CHARACTER_JAMES_20261014.md');new.update(project='lisan',title='James · Brother relationship and proposed continuity',documentGroup='Lisan Al Gaib · Claude writer-development',documentCategory='Standalone stories and series',author='Claude',status='Brother relationship adopted; expanded continuity proposed',fullTextPreview=True,context='The dated note predates the returned gun-removal draft. The current intake records an unfinished repair, with no human acceptance. Only the adoption scope is canon; age, powers and additional backstory remain open.',relatedAssets=[dict(assetID=source,label='James · original selected character',evidence='Exact adoption record; original Hon review preserved'),dict(assetID=draft,label='James · returned repair draft',evidence='Later technical intake; unaccepted blocking draft')])
W['documents'].append(new);W['updatedAtUTC']=now
next(g for p in W['projects'] if p['id']=='lisan' for g in p['groups'] if g['id']=='stories')['documentIDs'].append('lisan:doc:'+new['path'])
save(L/'writer_development.json',W)
save(E/'source_update.json',dict(updatedAtUTC=now,files=[pin(p) for p in [P/'collaborators/mission_control.json',L/'cast_collections.json',L/'cast_revisions.json',L/'writer_development.json']],authority=[pin(receipt),pin(J/'RESULT_INTAKE.json')],newMediaID=draft,unchangedOriginalID=source))
print('Prepared mission, selected boss, James revision and writer sources.')
