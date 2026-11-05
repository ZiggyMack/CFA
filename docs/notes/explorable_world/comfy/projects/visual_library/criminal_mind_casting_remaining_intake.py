"""Replay twelve remaining speaking-role batches without selecting a character."""
from copy import deepcopy
import hashlib,json,os
from pathlib import Path
from urllib.parse import quote

PROJECT='criminal_mind';STORY='criminal_mind:the-criminal-mind';TASK='tcm-grok-casting-20261030'
HOME=Path('docs/notes/explorable_world/comfy/references/From Grok/GROK-TCM-CASTING_v001/intake')
ROSTER=Path('docs/notes/explorable_world/comfy/projects/the_criminal_mind/handoffs/grok_casting_and_sets_20261030/CASTING_ROSTER_v001.json')
ROSTER_SHA='5a4cb34faff8988c5f934bc316e823c30a7d41120c0cb6fa64b022a0717dbf81'
AGGREGATE=('CFA_CASTING_INTAKE_007-018_v001.json', '4966b311ec5df9d79a09c68038189c4613fe3f13412d38baecd950dd84db6df9')
VISUAL_CHECK=('CFA_CASTING_VISUAL_CHECK_007-018_v001.json', 'e5157a00a0a4ca8dd4773b50a63e918b5f1d88bcfa59171d9a72aeec12463ed8')
# Pinned only after CFA Nova finishes verification and seals all twelve receipts.
BATCHES=(('007', 'OPENING-MAN', "Mother's boyfriend (opening MAN)", '6410036c380a33532234cfd91dd58d0ad53fa6545fdcf6703d3632274b72a1d1'), ('008', 'STEELE', 'Captain Steele', 'fbefa736d889e22b7698f693479a8d7e86849c3c7f2fc9e81045822dd706be82'), ('009', 'FOX', 'Agent Fox', '0bb99e99820cd68c8c3fa98a9b7768f12d5ce5db0936ba566a9de1109db2c0e8'), ('010', 'DANIELS', 'Agent Daniels', '96494403e1cae01bdd06b314a528924f021a3cf3efecba406ce6763127fc89da'), ('011', 'WALLACE', 'Mr Wallace', '274a2fdd8e3294f4bc937e093ee677400b130ce74d15d889d4bd7c7141c32e20'), ('012', 'ALLEY-WOMAN', 'Later alley woman (GIRL)', '82bef91121eaa79fbbee375b7c68f37aed50256f68c23d81fd2f990d78512a77'), ('013', 'DISPATCH', 'Dispatcher', 'a47d6459a7c64d017199da85b182adf244f15a3a3f4e7bcdb19c1b267a258e24'), ('014', 'BRITISH-MAN', 'Street British man', '10a9612d47055b41e9091790d38b335c6d90dc201a9f96e2336e8e3bcca8ac6b'), ('015', 'BAR-WOMAN', 'Woman at the bar', 'a813908a3293bc303752c2b13af118d837aa84d938c5a8d91e7ee9b7a6403783'), ('016', 'NEWS-ANCHOR', 'Television news anchor', '72c0bb1d2c9c2b43bbbeff6c1e40373a34bd34133a9ace6744f4f2444b074230'), ('017', 'HOSTAGE-MAN', 'Hostage man (flashback MAN)', 'bba742bd01c11e1d3c2793d02f160a36dc2ae3a0fb57b96f4ec483a9b2e6a8a6'), ('018', 'PARAMEDIC', 'Flashback paramedic', '5e9373b75e7070ef1432fb5c477a58ba2a85aab28550f234d33f3d194331d9ae'))
SCOPE='Source scene context only: a role may be present, heard or discussed. This is not proof of on-screen presence, a casting choice, a Card D selection or a starting-frame binding.'


def receipt_paths(root):
    return [Path(root)/HOME/f'TCM-INTAKE-BATCH-{number}_{key}_v001'/'CFA_INTAKE_RECEIPT_v001.json' for number,key,_,_ in BATCHES]


def available(root):
    present=[p.is_file() for p in receipt_paths(root)]
    if any(present) and not all(present):
        raise ValueError('Remaining speaking-role casting intake is incomplete; wait for all twelve sealed CFA receipts.')
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
    assert aggregate['receivedOriginals']==120 and aggregate['physicalCandidateCount']==120 and aggregate['receivedCastingGroups']==12
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
            assert row['makerOriginalHashPresent'] is (key not in {'OPENING-MAN','STEELE','FOX','DANIELS'})
            assert row['sourceScenes']==group['sourceScenes'] and row['eligibleShotIDs']==group['linkedShotIDs']
            src=quote(os.path.relpath(original,visual).replace('\\','/'),safe='/')
            state=row.get('performanceState');physical=row['physicalCandidateID']
            title=f'Casting option · {label} · {physical}'+(' · '+state.title() if state else '')
            note=role_note+'\nSource role: '+row['sourceAppearance']+'\nRole context: '+row['roleContext']
            note+='\nGrok look proposal: '+(row['providerLookNote'] or 'Not supplied')+'\nGrok source/proposal distinction: '+(row['providerSourceVsProposal'] or 'Not supplied')
            note+='\nGrok maker defect note: '+(row['providerDefectNote'] or 'Not supplied')
            screening=row.get('providerScreening') or {}
            note+='\nGrok screening opinion (not a human verdict): '+(screening.get('tag') or 'No tag supplied')+' — '+(screening.get('note') or 'No note supplied')
            if not row['makerOriginalHashPresent']:
                note+='\nOriginal maker hash was not supplied. CFA verified the delivered bytes and current file hash; this does not reconstruct an earlier maker hash.'
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
        context=dict(storyID=STORY,sourceScenes=group['sourceScenes'],scope=SCOPE,sourceRoster={'path':ROSTER.as_posix(),'sha256':ROSTER_SHA})
        collections.append(dict(id=album_id,project=PROJECT,title=title,role='Preliminary casting alternatives',description=description,
            sourceAlbumIDs=[album_id],assetIDs=expected_ids,castingGroupID=family,sourceIntake=batch,sections=sections,sourceContext=context,
            notes=[role_note,'Source scenes '+scene_summary(group['sourceScenes'])+'. '+SCOPE,'No selected character cover, identity or working reference. All portraits retain separate human review records.']))
        receipts.append(dict(path=path.relative_to(root).as_posix(),sha256=expected_sha,bytes=len(raw),batchID=batch,receivedOriginals=count,acceptedOriginals=0,physicalCandidateCount=10))
    assert len(assets)==120 and len({a['sha256'] for a in assets})==120
    return dict(assets=assets,albums=albums,castCollections=collections,requests=requests,receipts=receipts)


def apply_casting_task(task,payload):
    assert task['id']==TASK and task['acceptedOutputs']==0
    previous_roles=['JOHN','YOUNG-JOHN','JILL','DIEGO','JEN']
    prior_ids=[f'TCM-CAST-JOHN-C{i:02}-{state}' for i in range(1,11) for state in ['JOHN','JACK','JOHNNY']]
    prior_ids += [f'TCM-CAST-{role}-C{i:02}' for role in previous_roles[1:] for i in range(1,11)]
    all_ids=prior_ids+[a['id'] for a in payload['assets']]
    assert task['previewAssetIDs'] in [prior_ids,all_ids] and task['outputFilesReceived'] in [70,190]
    prior_batches=[f'TCM-INTAKE-BATCH-{n:03}_{role}_v001' for n,role in enumerate(previous_roles,2)]
    all_batches=prior_batches+[r['batchID'] for r in payload['receipts'] if 'batchID' in r]
    all_groups=['TCM-CAST-'+role for role in previous_roles]+[g['castingGroupID'] for g in payload['castCollections']]
    task.update(status='needs_input',statusLabel='190 speaking-role portraits received · 17 groups',direction='inbound',generationStartedVerified=True,externalExecution=True,
        outputFilesReceived=190,acceptedOutputs=0,preparationState='all_speaking_casting_batches_received_verified',previewAssetIDs=all_ids,
        receivedBatchIDs=all_batches,receivedCastingGroups=all_groups,physicalCandidatesReceived=170,
        summary='All 190 requested speaking-role portraits are verified received across 17 casting groups. Adult John retains ten matched John / Jack / Johnny triples. Background casting returns remain separate and pending. No option is selected or accepted.',
        nextAction='Baldadoon reviews the 17 speaking-role casting collections and records scoped decisions or changes. Provider screening remains attributed opinion; matching John performance portraits and young-to-adult resemblance still need human review. These are options, not selected storyboard inputs.',
        laterReview='A casting decision does not accept a shot, starting frame or finished video. Background casting and the remaining set returns remain separate from this completed speaking-role delivery.')
    new_links=[dict(label='Review '+a['title'],href='#criminal_mind/review_queue/'+quote(a['id'],safe=''),albumID=a['id'],assetIDs=a['assetIDs']) for a in payload['albums']]
    known={l.get('albumID'):l for l in task.get('links',[]) if l.get('albumID')}
    for link in new_links:assert link['albumID'] not in known or known[link['albumID']]==link
    task['links'] += [link for link in new_links if link['albumID'] not in known]


def apply_casting_intake(catalog,payload):
    result=deepcopy(catalog)
    for key,rows in [('assets',payload['assets']),('albums',payload['albums']),('castCollections',payload['castCollections']),('reviewRequests',payload['requests'])]:
        prior=result.setdefault(key,[]);existing={r['id']:r for r in prior};assert len(existing)==len(prior)
        for row in rows:assert row['id'] not in existing or existing[row['id']]==row,'Conflicting casting record: '+row['id']
        prior.extend(deepcopy(r) for r in rows if r['id'] not in existing)
    task=next(t for t in result['missionControl']['tasks'] if t['id']==TASK);apply_casting_task(task,payload)
    return result
