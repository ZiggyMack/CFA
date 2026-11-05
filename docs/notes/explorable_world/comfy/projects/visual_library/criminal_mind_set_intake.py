"""Register verified set alternatives without selecting storyboard inputs."""
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
from urllib.parse import quote

PROJECT = 'criminal_mind'
STORY = 'criminal_mind:the-criminal-mind'
BATCH = 'TCM-INTAKE-BATCH-001_HENDERSON-EXTERIOR_v001'
FAMILY = 'TCM-SET-HENDERSON-EXTERIOR'
ALBUM = 'criminal_mind:henderson-exterior-options'
SHOTS = ('TCM-05-01', 'TCM-10-01')
HOME = Path('docs/notes/explorable_world/comfy/references/From Grok/GROK-TCM-SETS_v001/intake') / BATCH
RECEIPT_SHA = '600d7f5f7fbed6fbe2e192473f9a64296b27dca35bd3298b0a6352e6ff8e8fba'
NOTE = 'Candidate alternative for the Henderson house exterior; Baldadoon has not selected this set, a Card D reference, or a starting frame.'


def intake_payload(root):
    root = Path(root).resolve()
    folder = root / HOME
    receipt_path = folder / 'CFA_INTAKE_RECEIPT_v001.json'
    raw = receipt_path.read_bytes()
    assert hashlib.sha256(raw).hexdigest() == RECEIPT_SHA, 'Reconcile changed TCM intake receipt'
    receipt = json.loads(raw)
    assert receipt['project'] == PROJECT and receipt['batchID'] == BATCH
    assert receipt['receivedOriginals'] == 10 and receipt['acceptedOriginals'] == receipt['humanVerdictsCreated'] == 0
    rows = receipt['assets']
    assert [r['candidateID'] for r in rows] == [FAMILY + f'-L{i:02}' for i in range(1, 11)]
    assert len({r['sha256'] for r in rows}) == 10
    assets, requests, materials = [], [], []
    visual = root / 'docs/notes/explorable_world/comfy/projects/visual_library'
    for row in rows:
        path = Path(row['path']).resolve()
        assert path.parent == folder.resolve() and path.name == row['candidateID'] + '.jpg'
        content = path.read_bytes()
        assert hashlib.sha256(content).hexdigest() == row['sha256'] and len(content) == row['bytes']
        assert row['project'] == PROJECT and row['locationFamilyID'] == FAMILY
        assert row['role'] == 'set_design_option' and row['selected'] is False and row['humanReview'] is None
        assert row['eligibleShotIDs'] == list(SHOTS) and row['stage'] == 'preliminary'
        assert row['reviewControllerID'] == 'baldadoon'
        suffix = row['candidateID'].rsplit('-', 1)[-1]
        src = quote(os.path.relpath(path, visual).replace('\\', '/'), safe='/')
        note = NOTE + '\nProvider look proposal: ' + row['providerLookNote']
        note += '\nProvider source/proposal distinction: ' + row['providerSourceVsProposal']
        note += '\nProvider screening note (not a human verdict): ' + row['providerDefectNote']
        assets.append(dict(id=row['candidateID'], project=PROJECT, kind='image', category='review', album=ALBUM,
            title='Candidate alternative · Henderson exterior · ' + suffix, filename=path.name, src=src, thumb=src,
            repoPath=path.relative_to(root).as_posix(), sha256=row['sha256'], bytes=row['bytes'],
            width=row['width'], height=row['height'], stage='preliminary', storyboardStage='preliminary',
            provider='Grok', model=None, makerReported=row['makerReported'], role='set_design_option',
            referenceRole='set_design_option', selected=False, reviewControllerID='baldadoon',
            controllerID='baldadoon', locationFamilyID=FAMILY, eligibleShotIDs=list(SHOTS),
            sourceScenes=row['sourceScenes'], sourceIntake=BATCH, receivedAt=receipt['receivedAtUTC'],
            intakeReceipt={'path': (HOME / receipt_path.name).as_posix(), 'sha256': RECEIPT_SHA},
            providerLookNote=row['providerLookNote'], providerSourceVsProposal=row['providerSourceVsProposal'],
            providerDefectNote=row['providerDefectNote'], note=note))
        requests.append(dict(id=row['candidateID'], sha256=row['sha256'], type='missing_decision',
            requestedBy='CFA Nova', requestedAt=receipt['receivedAtUTC'], project=PROJECT,
            reviewControllerID='baldadoon', taskID='tcm-grok-sets-20261030',
            reason='Review this Henderson exterior alternative and its source constraints. No set or starting frame has been selected.'))
        materials.append(dict(assetID=row['candidateID'], sha256=row['sha256'], role='set_design_option',
            status='candidate_alternative_unreviewed', selected=False, note=NOTE))
    album = dict(id=ALBUM, project=PROJECT, category='review', title='Henderson house exterior · 10 options',
        description='Ten received Grok set alternatives for TCM-05-01 and TCM-10-01. Review with Baldadoon; none is selected or accepted.',
        assetIDs=[a['id'] for a in assets], related=[], locationFamilyID=FAMILY, sourceIntake=BATCH)
    return dict(assets=assets, requests=requests, materials=materials, album=album, receipt=receipt)


def apply_task_intake(task, payload):
    """Both tasks retain independent received counts; only the set batch arrived."""
    if task['id'] == 'tcm-grok-casting-20261030':
        task.update(statusLabel='Casting batch awaited · no files received',
            nextAction='The first set-options batch has arrived separately. Await original casting files and their verified index; casting received and accepted totals remain zero.')
        return
    assert task['id'] == 'tcm-grok-sets-20261030'
    ids = [a['id'] for a in payload['assets']]
    task.update(status='needs_input', statusLabel='10 set options received · review with Baldadoon', direction='inbound',
        generationStartedVerified=True, externalExecution=True, outputFilesReceived=10, acceptedOutputs=0,
        preparationState='first_original_image_batch_received_verified', previewAssetIDs=ids,
        receivedBatchIDs=[BATCH], receivedLocationFamilies=[FAMILY],
        summary='Ten Henderson house-exterior alternatives are verified received from Grok. No option is selected or accepted. The remaining set families and casting returns are still pending.',
        nextAction='Review the ten house-exterior alternatives and the provider notes. Choose a set direction or request changes; these alternatives are eligible for TCM-05-01 and TCM-10-01 but are not selected Card D references or starting frames.',
        laterReview='Baldadoon records scoped decisions; a set choice does not accept a shot, starting frame or finished video.')
    task['links'].append(dict(label='Review the 10 Henderson exterior options',
        href='#criminal_mind/review_queue/' + quote(ALBUM, safe=''), albumID=ALBUM, assetIDs=ids))


def apply_set_intake(catalog, payload):
    """Append records atomically and idempotently, without changing reviews."""
    result = deepcopy(catalog)
    def append(rows, additions):
        existing = {r['id']: r for r in rows}
        assert len(existing) == len(rows)
        for row in additions:
            assert row['id'] not in existing or existing[row['id']] == row, 'Conflicting intake record: ' + row['id']
        return rows + [deepcopy(r) for r in additions if r['id'] not in existing]
    result['assets'] = append(result['assets'], payload['assets'])
    result['albums'] = append(result['albums'], [payload['album']])
    result['reviewRequests'] = append(result.get('reviewRequests', []), payload['requests'])
    structure = next(s for s in result['storyboardStructure']['stories'] if s['storyID'] == STORY)
    by_id = {s['shotID']: s for s in structure['shots']}
    assert set(SHOTS) <= by_id.keys()
    for sid in SHOTS:
        shot = by_id[sid]
        assert shot['locationFamilyID'] == FAMILY
        previous = shot.get('materials', [])
        existing = {m['assetID']: m for m in previous}
        for row in payload['materials']:
            assert row['assetID'] not in existing or existing[row['assetID']] == row
        shot['materials'] = previous + [deepcopy(m) for m in payload['materials'] if m['assetID'] not in existing]
    catalog.clear()
    catalog.update(result)
    return catalog
