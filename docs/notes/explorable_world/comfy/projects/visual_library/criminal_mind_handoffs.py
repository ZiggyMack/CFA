"""Replay TCM handoff and verified intake states without implying acceptance."""
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
from urllib.parse import quote
from criminal_mind_set_intake import intake_payload, apply_task_intake, apply_set_intake
from criminal_mind_casting_intake import intake_payload as casting_intake_payload, apply_casting_task, apply_casting_intake
from criminal_mind_casting_remaining_intake import intake_payload as remaining_casting_payload, apply_casting_task as apply_remaining_casting_task, apply_casting_intake as apply_remaining_casting_intake

BASE=Path('docs/notes/explorable_world/comfy/projects')
DROP=BASE/'the_criminal_mind/handoffs/grok_casting_and_sets_20261030'
DOCS=(('TCM-GROK-CASTING-BRIEF-20261030','GROK_CASTING_HANDOFF_v001.txt','Grok casting call · prepared brief'),
      ('TCM-GROK-SETS-BRIEF-20261030','GROK_SETS_HANDOFF_v001.txt','Grok set scout · prepared brief'))
TASKS=('tcm-grok-casting-20261030','tcm-grok-sets-20261030')
STORY_ID='criminal_mind:the-criminal-mind'

def apply_criminal_mind_handoffs(catalog,root):
    root=Path(root).resolve()
    manifest=json.loads((root/DROP/'PREPARED_DROP_MANIFEST_v001.json').read_text(encoding='utf-8-sig'))
    assert manifest['project']=='criminal_mind' and manifest['reviewControllerID']=='baldadoon'
    assert manifest['outputsReceived']==manifest['generatedAssetsAccepted']==0
    assert [t['id'] for t in manifest['tasks']]==list(TASKS)
    assert [t['brief'] for t in manifest['tasks']]==[r[1] for r in DOCS]
    assert all(t['status']=='prepared_waiting_storyboard_site_verification' for t in manifest['tasks'])
    assert manifest['castingImages']==238 and manifest['setImages']==200 and manifest['totalImageCap']==438
    files={}
    for item in manifest['files']:
        relative=Path(item['path'])
        assert not relative.is_absolute() and '..' not in relative.parts
        path=(root/DROP/relative).resolve()
        assert path.is_relative_to(root/DROP)
        raw=path.read_bytes()
        assert hashlib.sha256(raw).hexdigest()==item['sha256'] and len(raw)==item['bytes'], item['path']
        files[item['path']]=(raw,item)
    packet=root/manifest['storyboardPacket']['path']
    assert packet.resolve().is_relative_to(root)
    assert hashlib.sha256(packet.read_bytes()).hexdigest()==manifest['storyboardPacket']['sha256']
    assert any(s['storyID']==STORY_ID for s in catalog['storyboardStructure']['stories'])
    assert next(a['sha256'] for a in catalog['assets'] if a['id']=='TCM-SCRIPT-TEXT')==manifest['sourceScriptSHA256']
    album_id='criminal_mind:prepared-grok-handoffs'
    docs=[]; tasks=[]
    for index,(asset_id,filename,title) in enumerate(DOCS):
        raw,item=files[filename]; text=raw.decode('utf-8-sig')
        assert '\ufffd' not in text
        docs.append(dict(id=asset_id,project='criminal_mind',kind='document',category='documents',album=album_id,
                         filename=filename,title=title,repoPath=(DROP/filename).as_posix(),
                         src=quote(os.path.relpath(root/DROP/filename,root/BASE/'visual_library').replace('\\','/'),safe='/'),
                         sha256=item['sha256'],bytes=len(raw),text=text,inert=True,controllerID='baldadoon',
                         author='CFA Nova',sourceStatus='Prepared · not sent',sourceIntake='TCM-GROK-PREPARED-20261030'))
        source=manifest['tasks'][index]
        summary=('19 speaking roles in 17 physical casting groups, plus 16 background groups. Prepared casting cap: 238 candidate images.' if index==0 else
                 '20 set/location families mapped to the proposed storyboard. Prepared set cap: 200 candidate images.')
        tasks.append(dict(id=source['id'],project='criminal_mind',provider='Grok',title=source['title'],priority='normal',
                          status='planned',statusLabel='Source brief delivered · generation held',direction='outbound',workKind='image_new',
                          ownerControllerID='baldadoon',assigneeControllerID='baldadoon',decisionAuthorityControllerID='baldadoon',
                          decisionScope='project_decision',assignee='CFA Nova',executionAssignee='CFA Nova',
                          summary=summary+' CFA Nova handles execution; Baldadoon selects the returned candidates in Casa.',
                          nextAction='CFA Nova delivered the source package for readback only. Generation remains held until Site Nova verifies the published Structure & gaps and CFA Nova sends the separate GO. Source readback is not yet confirmed.',
                          enablers=['Published storyboard Structure & gaps verification is pending.'],
                          laterReview='Review the received candidates in Casa Baldadoon; no winner or production asset has been selected.',
                          links=[{'label':'Read the prepared brief','assetID':asset_id},
                                 {'label':'Read the source screenplay','assetID':'TCM-SCRIPT-TEXT'},
                                 {'label':'Open Storyboard · Structure & gaps','href':'https://algaib.streamlit.app/Full_Visual_Library?project=criminal_mind&view=storyboard&album=structure%3Acriminal_mind%3Athe-criminal-mind'}],
                          storyID=STORY_ID,previewAssetIDs=[],missing=[],sent=False,readbackDelivered=True,generationReleased=False,externalExecution=False,
                          generationAuthorizedByThisCard=False,writtenBy='CFA Nova',authorship='prepared_handoff',requestedBy='Ziggy',
                          preparationState=source['status'],preparedImageCap=manifest['castingImages' if index==0 else 'setImages']))
    album=dict(id=album_id,project='criminal_mind',category='documents',title='Prepared Grok handoffs',
               description='Casting and set proposals awaiting storyboard-site verification; no dispatch or generated result.',
               assetIDs=[d['id'] for d in docs],related=[])
    def appended(rows, additions):
        existing={row['id']:row for row in rows}
        assert len(existing)==len(rows)
        for row in additions:
            assert row['id'] not in existing or existing[row['id']]==row, 'Conflicting prepared handoff '+row['id']
        return rows+[row for row in additions if row['id'] not in existing]
    # Replay supported delivery stages; unknown stages require reconciliation.
    delivery_path=root/DROP/'DELIVERY_STATUS_v001.json'
    received_payload=None
    casting_payload=None
    remaining_payload=None
    if delivery_path.is_file():
        delivery=json.loads(delivery_path.read_text(encoding='utf-8-sig'))
        assert delivery['project']=='criminal_mind' and set(delivery['task_ids'])==set(TASKS)
        stage_updates={'generation_go_acknowledged_team_dispatched': {'status': 'in_progress', 'statusLabel': 'Team dispatched · first image job pending', 'sent': True, 'readbackDelivered': True, 'readbackConfirmed': True, 'generationReleased': True, 'teamDispatched': True, 'generationReported': False, 'generationStartedVerified': False, 'externalExecution': False, 'outputFilesReceived': 0, 'acceptedOutputs': 0, 'preparationState': 'generation_go_acknowledged_team_dispatched', 'enablers': [], 'nextAction': 'Grok acknowledged CFA Nova’s GO and reports team dispatch. Await the first actual maker job receipt and original-image batch; no CFA receipt or acceptance is recorded.'}, 'maker_generation_reported_first_artifact_pending': {'status': 'in_progress', 'statusLabel': 'Team dispatched · first delivered batch pending', 'sent': True, 'readbackDelivered': True, 'readbackConfirmed': True, 'generationReleased': True, 'teamDispatched': True, 'generationReported': True, 'generationStartedVerified': False, 'externalExecution': False, 'outputFilesReceived': 0, 'acceptedOutputs': 0, 'preparationState': 'maker_generation_reported_first_artifact_pending', 'enablers': [], 'nextAction': 'Grok’s team reports image-tool starts and remote originals, but those reports and counts are unverified by CFA. CFA Nova requested the first original-image batch with its index and a contact sheet. No originals have been received or inspected by CFA; received and accepted totals remain zero. The D: delivery bridge is unverified.'}}
        stage=delivery['stage']
        all_speaking_stages = {
            'all_190_speaking_casting_originals_verified_site_intake_in_progress',
            'first_70_casting_published_next_120_integrated_pending_director_casting_room',
        }
        if stage in {'first_original_image_batch_received_verified', 'first_original_image_batch_published_for_human_review', 'seventy_casting_originals_verified_site_intake_requested', *all_speaking_stages}:
            received_payload=intake_payload(root)
            expected_count=200 if stage in all_speaking_stages else (80 if stage=='seventy_casting_originals_verified_site_intake_requested' else 10)
            assert delivery['output_files_received']==expected_count and delivery['accepted_outputs']==0
            assert delivery['generation_started_verified'] is True
            assert Path(delivery['first_batch_receipt']).resolve()==(root/'docs/notes/explorable_world/comfy/references/From Grok/GROK-TCM-SETS_v001/intake/TCM-INTAKE-BATCH-001_HENDERSON-EXTERIOR_v001/CFA_INTAKE_RECEIPT_v001.json').resolve()
            # Retain the casting task's independent pre-receipt state. Only
            # the verified set receipt supplies received assets and counts.
            selected=deepcopy(stage_updates['maker_generation_reported_first_artifact_pending'])
            if stage in {'seventy_casting_originals_verified_site_intake_requested', *all_speaking_stages}:
                casting_payload=casting_intake_payload(root)
            if stage in all_speaking_stages:
                remaining_payload=remaining_casting_payload(root)
                assert delivery['received_by_lane']=={'sets':10,'casting':190,'speakingCasting':190,'backgroundCasting':0}
                additional=delivery['casting_additional_delivery']
                assert additional['receiptSHA256']=='4966b311ec5df9d79a09c68038189c4613fe3f13412d38baecd950dd84db6df9'
                assert additional['receivedOriginals']==120 and additional['castingGroups']==12
                assert additional['cumulativeSpeakingOriginals']==190 and additional['cumulativeSpeakingGroups']==17 and additional['accepted']==0
        elif stage in stage_updates:
            selected=deepcopy(stage_updates[stage])
            assert delivery['generation_started_verified'] is selected['generationStartedVerified']
            assert delivery['output_files_received']==selected['outputFilesReceived']
            assert delivery['accepted_outputs']==selected['acceptedOutputs']
        else:
            raise ValueError('Unsupported TCM delivery stage; reconcile instead of regressing: '+stage)
        assert delivery['execution_released'] is True
        assert bool(delivery.get('generation_started_reported',False)) is selected['generationReported']
        for task in tasks:
            task.update(deepcopy(selected))
            if received_payload:
                apply_task_intake(task,received_payload)
            if casting_payload and task['id']=='tcm-grok-casting-20261030':
                apply_casting_task(task,casting_payload)
            if remaining_payload and task['id']=='tcm-grok-casting-20261030':
                apply_remaining_casting_task(task,remaining_payload)
    assets=appended(catalog['assets'],docs)
    albums=appended(catalog['albums'],[album])
    mission=deepcopy(catalog['missionControl'])
    mission['tasks']=appended(mission['tasks'],tasks)
    result=deepcopy(catalog)
    result.update(assets=assets,albums=albums,missionControl=mission)
    if received_payload:
        apply_set_intake(result,received_payload)
    if casting_payload:
        result=apply_casting_intake(result,casting_payload)
    if remaining_payload:
        result=apply_remaining_casting_intake(result,remaining_payload)
    catalog.clear()
    catalog.update(result)
    return catalog
