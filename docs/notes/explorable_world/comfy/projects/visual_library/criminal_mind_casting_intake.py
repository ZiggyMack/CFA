"""Replay sealed preliminary casting alternatives without selecting a character."""
from copy import deepcopy
import hashlib,json,os
from pathlib import Path
from urllib.parse import quote

PROJECT='criminal_mind';STORY='criminal_mind:the-criminal-mind';TASK='tcm-grok-casting-20261030'
HOME=Path('docs/notes/explorable_world/comfy/references/From Grok/GROK-TCM-CASTING_v001/intake')
ROSTER=Path('docs/notes/explorable_world/comfy/projects/the_criminal_mind/handoffs/grok_casting_and_sets_20261030/CASTING_ROSTER_v001.json')
ROSTER_SHA='5a4cb34faff8988c5f934bc316e823c30a7d41120c0cb6fa64b022a0717dbf81'
AGGREGATE=('CFA_CASTING_INTAKE_002-006_v001.json','7e8a30c222118c68f17af11b21f9f9803eff9747bd67063e5414366c9352cbae')
VISUAL_CHECK=('CFA_CASTING_VISUAL_CHECK_002-006_v001.json','572042e3341fa218708ff9154b63344be159749e6c42a2bc06c5eac8af510958')
# Pinned only after CFA Nova finishes verification and seals all five receipts.
BATCHES=(
    ('002','JOHN','John / Jack / Johnny','fdb5bb26d7baca0b1ef55b05866da71ae475a167c44ce2fbc0d4127f006f91f5'),
    ('003','YOUNG-JOHN','Young John','daceb03483018b0b4f537cade953d6c6e82515a547f50db749172f8af7f59ef0'),
    ('004','JILL','Jill','2072b46576ba329cbb1bec53364d26fbca428a105d56bc72f73538abd7a3dc2a'),
    ('005','DIEGO','Diego','11bdd6d0ab2894ce7a0889fa762d248b72f00b0718ef039a4021465ed711db44'),
    ('006','JEN','Jen','df086ac8e4c5226c20f49140db8cf93d2a22ee0a32121f0a9ea3e8c565ef5acf'),
)
SCOPE='Source scene context only: a role may be present, heard or discussed. This is not proof of on-screen presence, a casting choice, a Card D selection or a starting-frame binding.'


def receipt_paths(root):
    return [Path(root)/HOME/f'TCM-INTAKE-BATCH-{number}_{key}_v001'/'CFA_INTAKE_RECEIPT_v001.json' for number,key,_,_ in BATCHES]


def available(root):
    present=[p.is_file() for p in receipt_paths(root)]
    if any(present) and not all(present):
        raise ValueError('First casting intake is incomplete; wait for all five sealed CFA receipts.')
    return all(present)


def scene_summary(ids):
    numbers=sorted({int(s.rsplit('-',1)[-1]) for s in ids});runs=[]
    for number in numbers:
        if runs and runs[-1][-1]+1==number:runs[-1].append(number)
        else:runs.append([number])
    return ', '.join(str(r[0]) if len(r)==1 else f'{r[0]}–{r[-1]}' for r in runs)


def intake_payload(root):
    root=Path(root).resolve();roster_raw=(root/ROSTER).read_bytes()
    assert hashlib.sha256(roster_raw).hexdigest()==ROSTER_SHA,'Casting roster changed; reconcile first'
    roster=json.loads(roster_raw);groups={g['castingGroupID']:g for g in roster['castingGroups']}
    visual=root/'docs/notes/explorable_world/comfy/projects/visual_library'
    assets,albums,collections,requests,receipts=[],[],[],[],[]
    for name,digest in [AGGREGATE,VISUAL_CHECK]:
        path=root/HOME/name;raw=path.read_bytes();assert hashlib.sha256(raw).hexdigest()==digest,'Changed sealed casting evidence'
        record=json.loads(raw);assert record['project']==PROJECT and record['humanVerdictsCreated']==record['acceptedOriginals']==0
        receipts.append(dict(path=path.relative_to(root).as_posix(),sha256=digest,bytes=len(raw)))
    aggregate=json.loads((root/HOME/AGGREGATE[0]).read_bytes())
    assert aggregate['receivedOriginals']==70 and aggregate['physicalCandidateCount']==50 and aggregate['receivedCastingGroups']==5
    for number,key,label,expected_sha in BATCHES:
        batch=f'TCM-INTAKE-BATCH-{number}_{key}_v001';family='TCM-CAST-'+key
        folder=root/HOME/batch;path=folder/'CFA_INTAKE_RECEIPT_v001.json';raw=path.read_bytes()
        assert hashlib.sha256(raw).hexdigest()==expected_sha,'Changed casting receipt: '+batch
        receipt=json.loads(raw);count=30 if key=='JOHN' else 10
        aggregate_record=next(r for r in aggregate['receipts'] if r['batchID']==batch)
        assert aggregate_record['receiptSHA256']==expected_sha and aggregate_record['receivedOriginals']==count
        assert receipt['format']=='cfa-grok-casting-intake-v1' and receipt['project']==PROJECT and receipt['taskID']==TASK and receipt['batchID']==batch
        assert receipt['receivedOriginals']==count and receipt['physicalCandidateCount']==10
        assert receipt['acceptedOriginals']==receipt['humanVerdictsCreated']==receipt['selectedStartingFrames']==0
        assert receipt['sourceRosterSHA256']==ROSTER_SHA and Path(receipt['sourceRoster']).resolve()==(root/ROSTER).resolve()
        assert all(receipt['verification'][k] is True for k in ['zipCRC','archiveHash','exactCandidateIDs','uniqueImageHashes','indexedBytesAndHashes','screeningHashes','JPEGDecode'])
        assert receipt['verification']['humanLikenessOrPairingValidation'] is False
        expected_ids=[f'{family}-C{i:02}'+suffix for i in range(1,11) for suffix in (['-JOHN','-JACK','-JOHNNY'] if key=='JOHN' else [''])]
        rows={row['candidateID']:row for row in receipt['assets']}
        assert set(rows)==set(expected_ids) and len(rows)==count
        assert len({r['sha256'] for r in rows.values()})==count
        album_id=PROJECT+':casting-'+key.lower()+'-options';group=groups[family]
        role_note='Ten physical candidates, each shown as John, Jack and Johnny. The three portraits share a proposed body identity; provider pairing has not been human-validated.' if key=='JOHN' else 'Ten unselected preliminary casting options.'
        if key=='YOUNG-JOHN':role_note+=' This younger-role pool is not yet matched to an adult John candidate.'
        for aid in expected_ids:
            row=rows[aid];original=Path(row['path']).resolve()
            assert original.parent==folder.resolve() and original.name==aid+'.jpg'
            content=original.read_bytes();assert hashlib.sha256(content).hexdigest()==row['sha256'] and len(content)==row['bytes']
            assert row['project']==PROJECT and row['castingGroupID']==family and row['role']=='casting_option'
            assert row['selected'] is False and row['humanReview'] is None and row['stage']=='preliminary' and row['reviewControllerID']=='baldadoon'
            assert row['providerScreeningIsHumanVerdict'] is False
            assert row['makerOriginalHashPresent'] is (key!='JEN')
            assert row['sourceScenes']==group['sourceScenes'] and row['eligibleShotIDs']==group['linkedShotIDs']
            src=quote(os.path.relpath(original,visual).replace('\\','/'),safe='/')
            state=row.get('performanceState');physical=row['physicalCandidateID']
            title=f'Casting option · {label} · {physical}'+(' · '+state.title() if state else '')
            note=role_note+'\nSource role: '+row['sourceAppearance']+'\nRole context: '+row['roleContext']
            note+='\nGrok look proposal: '+row['providerLookNote']+'\nGrok source/proposal distinction: '+row['providerSourceVsProposal']
            note+='\nGrok screening note (not a human verdict): '+row['providerDefectNote']
            asset=dict(id=aid,project=PROJECT,kind='image',category='cast',album=album_id,title=title,filename=original.name,
                src=src,thumb=src,repoPath=original.relative_to(root).as_posix(),sha256=row['sha256'],bytes=row['bytes'],width=row['width'],height=row['height'],
                stage='preliminary',storyboardStage='preliminary',provider='Grok',model=None,role='casting_option',referenceRole='casting_option',
                characterRole=row['character'],selected=False,reviewControllerID='baldadoon',controllerID='baldadoon',castingGroupID=family,
                physicalCandidateID=physical,performanceState=state,pairingStatus=row.get('pairingStatus'),
                sourceScenes=row['sourceScenes'],sourceIntake=batch,receivedAt=receipt['receivedAtUTC'],
                intakeReceipt={'path':(HOME/batch/path.name).as_posix(),'sha256':expected_sha},note=note)
            for field in ['sourceAppearance','roleContext','providerLookNote','providerSourceVsProposal','providerDefectNote','providerScreening','providerScreeningIsHumanVerdict','makerOriginalHashPresent']:
                asset[field]=deepcopy(row[field])
            assets.append(asset)
            requests.append(dict(id=aid,sha256=row['sha256'],type='missing_decision',requestedBy='CFA Nova',requestedAt=receipt['receivedAtUTC'],
                project=PROJECT,reviewControllerID='baldadoon',taskID=TASK,reason='Review this preliminary casting option. No identity, character role, Card D reference or starting frame is selected.'))
        title=label+(' · 10 matched candidate triples' if key=='JOHN' else ' · 10 casting options')
        description=role_note+' Review with Baldadoon; no option is selected or accepted.'
        albums.append(dict(id=album_id,project=PROJECT,category='cast',title=title,description=description,assetIDs=expected_ids,related=[],castingGroupID=family,sourceIntake=batch))
        sections=[dict(title=f'C{i:02} · matched John / Jack / Johnny portraits',physicalCandidateID=f'C{i:02}',assetIDs=[f'{family}-C{i:02}-{state}' for state in ['JOHN','JACK','JOHNNY']],description='One proposed physical identity, three performance states. Pairing is provider-assigned, not human-validated.') for i in range(1,11)] if key=='JOHN' else [dict(title='Unselected casting options',assetIDs=expected_ids,description=role_note)]
        context=dict(storyID=STORY,sourceScenes=group['sourceScenes'],sourceLinkedShotIDs=group['linkedShotIDs'],scope=SCOPE,sourceRoster={'path':ROSTER.as_posix(),'sha256':ROSTER_SHA})
        collections.append(dict(id=album_id,project=PROJECT,title=title,role='Preliminary casting alternatives',description=description,
            sourceAlbumIDs=[album_id],assetIDs=expected_ids,castingGroupID=family,sourceIntake=batch,sections=sections,sourceContext=context,
            notes=[role_note,'Source scenes '+scene_summary(group['sourceScenes'])+'. '+SCOPE,'No selected character cover, identity or working reference. All portraits retain separate human review records.']))
        receipts.append(dict(path=path.relative_to(root).as_posix(),sha256=expected_sha,bytes=len(raw),batchID=batch,receivedOriginals=count,acceptedOriginals=0,physicalCandidateCount=10))
    assert len(assets)==70 and len({a['sha256'] for a in assets})==70
    return dict(assets=assets,albums=albums,castCollections=collections,requests=requests,receipts=receipts)


def apply_casting_task(task,payload):
    assert task['id']==TASK
    task.update(status='needs_input',statusLabel='First 70 casting portraits received · 5 groups',direction='inbound',generationStartedVerified=True,externalExecution=True,
        outputFilesReceived=70,acceptedOutputs=0,preparationState='first_five_casting_batches_received_verified',previewAssetIDs=[a['id'] for a in payload['assets']],
        receivedBatchIDs=[r['batchID'] for r in payload['receipts'] if 'batchID' in r],receivedCastingGroups=[g['castingGroupID'] for g in payload['castCollections']],
        physicalCandidatesReceived=50,summary='The first 70 casting portraits are verified received: ten matched John / Jack / Johnny triples, plus ten each for Young John, Jill, Diego and Jen. The full casting call is not complete. No option is selected or accepted.',
        nextAction='Baldadoon reviews these five casting groups and records scoped decisions or changes. Compare each adult John triple together; Young John is a separate pool awaiting resemblance reconciliation. These are candidate options, not selected storyboard inputs.',
        laterReview='A casting decision does not accept a shot, starting frame or finished video. Remaining casting groups and background returns are still awaited.')
    new_links=[dict(label='Review '+a['title'],href='#criminal_mind/review_queue/'+quote(a['id'],safe=''),albumID=a['id'],assetIDs=a['assetIDs']) for a in payload['albums']]
    known={l.get('albumID'):l for l in task.get('links',[]) if l.get('albumID')}
    for link in new_links:assert link['albumID'] not in known or known[link['albumID']]==link
    task['links']+= [link for link in new_links if link['albumID'] not in known]


def apply_casting_intake(catalog,payload):
    result=deepcopy(catalog)
    for key,rows in [('assets',payload['assets']),('albums',payload['albums']),('castCollections',payload['castCollections']),('reviewRequests',payload['requests'])]:
        prior=result.setdefault(key,[]);existing={r['id']:r for r in prior};assert len(existing)==len(prior)
        for row in rows:assert row['id'] not in existing or existing[row['id']]==row,'Conflicting casting record: '+row['id']
        prior.extend(deepcopy(r) for r in rows if r['id'] not in existing)
    task=next(t for t in result['missionControl']['tasks'] if t['id']==TASK);apply_casting_task(task,payload)
    return result
