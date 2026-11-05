"""Publish sealed TCM review candidates without creating a human decision."""
from copy import deepcopy
import hashlib
import json
import os
import re
from collections import defaultdict
from pathlib import Path
from urllib.parse import quote


PROJECT = 'criminal_mind'
CONTROLLER = 'baldadoon'
CAST_TASK = 'tcm-grok-casting-20261030'
SET_TASK = 'tcm-grok-sets-20261030'
BACKGROUND = (Path('docs/notes/explorable_world/comfy/references/From Grok/GROK-TCM-CASTING_v001/intake/CFA_CASTING_INTAKE_019-034_SITE_INDEX_v003.json'),
              '4c63e19347c97abdbec5e009b3a4fb9fa3f6a69543da492a31a1203534498fc2')
SETS = (Path('docs/notes/explorable_world/comfy/references/From Grok/GROK-TCM-SETS_v001/intake/CFA_SET_INTAKE_035-118_SITE_INDEX_v003.json'),
        '17a0c4358c54b5fe0fc3b62e02c5de593e27e2ae91711e6ea9675413a34346bf')
BASELINE_CATALOG_SHA = '20d35893c50ea4f6fab5ffc585fa343d2898cfced09f35901c1f48cbdd5f4de6'


def _read_pinned(root, source):
    path, expected_sha = source
    raw = (root / path).read_bytes()
    assert hashlib.sha256(raw).hexdigest() == expected_sha, 'Changed TCM aggregate intake: ' + path.as_posix()
    return json.loads(raw), {'path': path.as_posix(), 'sha256': expected_sha, 'bytes': len(raw)}


def _slug(value):
    return re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')


def _title(value):
    return value.removeprefix('TCM-SET-').removeprefix('TCM-BG-').replace('-', ' ').title()


def _append(rows, additions, label):
    existing = {row['id']: row for row in rows}
    assert len(existing) == len(rows), 'Repeated existing ' + label
    for row in additions:
        assert row['id'] not in existing or existing[row['id']] == row, 'Conflicting ' + label + ': ' + row['id']
    return rows + [deepcopy(row) for row in additions if row['id'] not in existing]


def _load_assets(root, aggregate, receipt_evidence):
    assets = []
    candidate_ids = []
    for record in aggregate['receipts']:
        receipt_path = root / record['receiptPath']
        raw = receipt_path.read_bytes()
        assert len(raw) == record['receiptBytes'] and hashlib.sha256(raw).hexdigest() == record['receiptSHA256'], record['receiptPath']
        receipt = json.loads(raw)
        assert receipt['project'] == PROJECT and receipt['batchID'] == record['batchID']
        assert receipt['sealStatus'] == 'complete_only_when_pinned_by_required_aggregate'
        assert receipt['requiredAggregatePath'] == receipt_evidence['path']
        expected_task = CAST_TASK if record['lane'] == 'background' else SET_TASK
        expected_format = 'cfa-grok-casting-intake-v1' if record['lane'] == 'background' else 'cfa-grok-image-intake-v1'
        assert receipt['format'] == expected_format and receipt['lane'] == record['lane'] and receipt['taskID'] == expected_task
        assert receipt['archivePath'] == record['archivePath'] and receipt['archiveSHA256'] == record['archiveSHA256']
        assert receipt['archiveBytes'] == record['archiveBytes'] and receipt['archiveMemberCount'] == record['archiveMemberCount']
        assert receipt['receivedOriginals'] == record['receivedOriginals']
        assert receipt['acceptedOriginals'] == receipt['humanVerdictsCreated'] == receipt['selectedStartingFrames'] == 0
        verification = receipt['verification']
        assert all(verification[key] is True for key in ['zipCRC', 'archiveHash', 'safeMemberPaths', 'noSymlinks',
                                                          'noEncryptedMembers', 'uniqueCandidateIDs',
                                                          'indexedBytesAndHashes', 'JPEGDecode'])
        assert verification['humanReviewOrAcceptanceCreated'] is False
        for row in receipt['assets']:
            path = (root / row['repoPath']).resolve()
            assert path.is_relative_to(root.resolve()) and path.is_file(), row['candidateID']
            content = path.read_bytes()
            assert len(content) == row['bytes'] and hashlib.sha256(content).hexdigest() == row['sha256'], row['candidateID']
            assert row['selected'] is False and row['humanReview'] is None and row['reviewControllerID'] == CONTROLLER
            assert row['project'] == PROJECT and row['stage'] == 'preliminary'
            assert row['repoPath'] == path.relative_to(root).as_posix()
            item = deepcopy(row)
            item['receiptEvidence'] = {'path': record['receiptPath'], 'sha256': record['receiptSHA256']}
            item['aggregateEvidence'] = deepcopy(receipt_evidence)
            assets.append(item)
            candidate_ids.append(row['candidateID'])
    assert candidate_ids == aggregate['candidateIDs']
    assert len(candidate_ids) == len(set(candidate_ids)) == aggregate['receivedOriginals']
    return assets


def review_payload(root):
    root = Path(root).resolve()
    background, background_evidence = _read_pinned(root, BACKGROUND)
    sets, set_evidence = _read_pinned(root, SETS)
    assert background['format'] == 'cfa-grok-casting-intake-aggregate-v1'
    assert sets['format'] == 'cfa-grok-image-intake-aggregate-v1'
    assert background['project'] == sets['project'] == PROJECT
    for aggregate in [background, sets]:
        assert aggregate['baselineCatalog'] == {
            'path': 'docs/notes/explorable_world/comfy/projects/visual_library/catalog.js',
            'sha256': BASELINE_CATALOG_SHA,
        }
        assert all(value is True for key, value in aggregate['verification'].items()
                   if key not in {'humanReviewOrAcceptanceCreated', 'crossLaneDuplicateHashes'})
        assert aggregate['verification']['crossLaneDuplicateHashes'] is False
        assert aggregate['verification']['humanReviewOrAcceptanceCreated'] is False
    assert background['taskID'] == CAST_TASK and sets['taskID'] == SET_TASK
    assert background['receivedOriginals'] == background['uniqueImageHashes'] == 48
    assert background['receivedGroups'] == 16
    assert sets['receivedOriginals'] == 946 and sets['baseLookOriginals'] == 190 and sets['setRoundOriginals'] == 756
    assert sets['uniqueImageHashes'] == 944
    assert background['acceptedOriginals'] == sets['acceptedOriginals'] == 0
    assert background['humanVerdictsCreated'] == sets['humanVerdictsCreated'] == 0
    background_rows = _load_assets(root, background, background_evidence)
    set_rows = _load_assets(root, sets, set_evidence)
    assert len({row['sha256'] for row in background_rows}) == 48
    assert len({row['sha256'] for row in set_rows}) == 944
    assert not ({row['sha256'] for row in background_rows} & {row['sha256'] for row in set_rows})
    provider_ids = [row['providerCandidateID'] for row in set_rows]
    assert len(provider_ids) == len(set(provider_ids)) == 946
    assert sum(row['candidateID'] != row['providerCandidateID'] for row in set_rows) == 423
    later = [row for row in set_rows if row['lane'] == 'set_round']
    assert len(later) == 756 and all(row['eligibleShotIDs'] == [] for row in later)
    assert sum(bool((row.get('providerMetadata') or {}).get('cameraPositionID')) for row in later) == 749
    assert sum(bool((row.get('providerMetadata') or {}).get('lightState')) for row in later) == 749
    assert sum(bool((row.get('providerMetadata') or {}).get('servesShotsSourcePresent')) for row in later) == 749
    duplicate_map = {row['sha256']: [] for row in set_rows}
    for row in set_rows:
        duplicate_map[row['sha256']].append(row['candidateID'])
    assert {sha: sorted(ids) for sha, ids in duplicate_map.items() if len(ids) > 1} == {
        row['sha256']: sorted(row['candidateIDs']) for row in sets['duplicatePayloadMappings']}
    return {'backgroundRows': background_rows, 'setRows': set_rows,
            'backgroundEvidence': background_evidence, 'setEvidence': set_evidence}


def _note(row):
    parts = [
        'Received preliminary candidate; unreviewed by Baldadoon. No character, set, shot, starting frame or output is accepted.',
        'Exact archive mapping: ' + row['archivePath'] + ' :: ' + row['archiveMember'],
    ]
    if row.get('providerCandidateID'):
        parts.append('Canonical provider candidate ID: ' + row['providerCandidateID'] +
                     ('' if row['providerCandidateID'] == row['candidateID'] else ' (site file ID retained separately)'))
    proposal = row.get('providerProposal') or {}
    screening = row.get('providerScreening') or {}
    if proposal.get('lookNote'):
        parts.append('Provider look proposal: ' + proposal['lookNote'])
    if proposal.get('sourceVsProposal'):
        parts.append('Provider source/proposal distinction: ' + proposal['sourceVsProposal'])
    if proposal.get('defectNote'):
        parts.append('Provider defect note: ' + proposal['defectNote'])
    if screening.get('tag'):
        parts.append('Attributed preliminary screening (not a human verdict): ' + screening['tag'] +
                     (' — ' + screening['note'] if screening.get('note') else ''))
    return '\n'.join(parts)


def _asset(row, visual):
    path = Path(row['path'])
    src = quote(os.path.relpath(path, visual).replace('\\', '/'), safe='/')
    family = row.get('castingGroupID') or row.get('locationFamilyID')
    if row['lane'] == 'background':
        album = PROJECT + ':casting-bg-' + _slug(family)
        suffix = row['candidateID'].rsplit('-', 1)[-1]
        title = 'Background casting option · ' + row['character'] + ' · ' + suffix
        category = 'cast'
    elif row['lane'] == 'base_set':
        album = PROJECT + ':set-base-' + _slug(family)
        suffix = row['candidateID'].rsplit('-', 1)[-1]
        title = 'Base set look · ' + row['locationTitle'] + ' · ' + suffix
        category = 'review'
    else:
        album = PROJECT + ':set-camera-' + _slug(family)
        title = 'Set camera candidate · ' + row['locationTitle'] + ' · ' + row['candidateID'].split('__', 1)[-1]
        category = 'review'
    asset = dict(id=row['candidateID'], project=PROJECT, kind='image', category=category, album=album,
        title=title, filename=path.name, src=src, thumb=src, repoPath=row['repoPath'], sha256=row['sha256'],
        bytes=row['bytes'], width=row['width'], height=row['height'], stage='preliminary', storyboardStage='preliminary',
        provider='Grok', model=None, role=row['role'], referenceRole=row['role'], selected=False,
        reviewControllerID=CONTROLLER, controllerID=CONTROLLER, sourceIntake=row['receiptEvidence']['path'],
        intakeReceipt=deepcopy(row['receiptEvidence']), aggregateIntake=deepcopy(row['aggregateEvidence']),
        archivePath=row['archivePath'], archiveMember=row['archiveMember'], providerScreening=deepcopy(row.get('providerScreening')),
        providerScreeningIsHumanVerdict=False, providerProposal=deepcopy(row.get('providerProposal')), note=_note(row))
    if row['lane'] == 'background':
        asset.update(castingGroupID=family, physicalCandidateID=row['candidateID'].rsplit('-', 1)[-1],
                     characterRole=row['character'], sourceScenes=row['sourceScenes'], roleContext=row['roleContext'])
    else:
        metadata = row.get('providerMetadata') or {}
        set_kind = 'identity_sheet' if metadata.get('carID') else (
            'extra' if re.search(r'(?:-|_)X\d+', row['candidateID']) else ('base_look' if row['lane'] == 'base_set' else 'camera_coverage'))
        asset.update(locationFamilyID=family, eligibleShotIDs=row.get('eligibleShotIDs', []),
                     sourceScenes=row.get('sourceScenes', []), setRoundKind=set_kind,
                     sourceFileID=Path(row['repoPath']).stem, providerCandidateID=row.get('providerCandidateID'),
                     candidateIDSource=row.get('candidateIDSource'), bindingPolicy=row.get('bindingPolicy'),
                     cameraPositionID=metadata.get('cameraPositionID'), lightState=metadata.get('lightState'),
                     providerVariant=metadata.get('variant'), providerVariantOf=metadata.get('variantOf'),
                     carID=metadata.get('carID'),
                     providerReferenceIDs=metadata.get('referenceIDs', []),
                     providerServesShotIDs=metadata.get('servesShotIDs', []),
                     providerServesShotsRaw=metadata.get('servesShotsRaw'),
                     providerShotsIDsSourceDetail=metadata.get('shotsIDsSourceDetail', []),
                     providerMetadataSource={'member': metadata.get('sourceMember'), 'sha256': metadata.get('sourceSHA256'),
                                             'isMakerSupplied': metadata.get('isMakerSupplied')})
    return asset


def _albums(background_assets, set_assets):
    albums, collections = [], []
    background_groups, base_groups, round_groups = defaultdict(list), defaultdict(list), defaultdict(list)
    for asset in background_assets:
        background_groups[asset['castingGroupID']].append(asset)
    for asset in set_assets:
        target = base_groups if asset['setRoundKind'] == 'base_look' else round_groups
        target[asset['locationFamilyID']].append(asset)
    for family, items in background_groups.items():
        album_id = items[0]['album']
        title = items[0]['characterRole'] + ' · 3 background casting options'
        description = 'Received preliminary background candidates. Provider screening is attributed evidence; Baldadoon has not selected or accepted an option.'
        albums.append(dict(id=album_id, project=PROJECT, category='cast', title=title, description=description,
                           assetIDs=[row['id'] for row in items], related=[], castingGroupID=family,
                           sourceIntake=items[0]['aggregateIntake']['path']))
        collections.append(dict(id=album_id, project=PROJECT, title=title, role='Preliminary background casting alternatives',
            description=description, sourceAlbumIDs=[album_id], assetIDs=[row['id'] for row in items],
            castingGroupID=family, sourceIntake=items[0]['aggregateIntake']['path'],
            sections=[dict(title='Unselected background options', assetIDs=[row['id'] for row in items], description=description)],
            sourceContext=dict(sourceScenes=items[0].get('sourceScenes', []), scope='Background role context only; not proof of shot presence or a casting choice.'),
            notes=['Three locally verified options; no human verdict, rank, identity choice or starting-frame binding.']))
    for family, items in base_groups.items():
        albums.append(dict(id=items[0]['album'], project=PROJECT, category='review', title=_title(family) + ' · 10 base looks',
            description='Original ten-look scouting collection. Received and locally verified; no look is selected or accepted.',
            assetIDs=[row['id'] for row in items], related=[], locationFamilyID=family,
            sourceIntake=items[0]['aggregateIntake']['path']))
    for family, items in round_groups.items():
        albums.append(dict(id=items[0]['album'], project=PROJECT, category='review', title=_title(family) + ' · set-camera round',
            description=f'{len(items)} received set-camera still entries. Screening tags are preliminary; no still, row or vehicle identity is selected or accepted.',
            assetIDs=[row['id'] for row in items], related=[], locationFamilyID=family,
            sourceIntake=items[0]['aggregateIntake']['path']))
    return albums, collections


def apply_criminal_mind_review_intake(catalog, root):
    payload = review_payload(root)
    visual = Path(root).resolve() / 'docs/notes/explorable_world/comfy/projects/visual_library'
    background_assets = [_asset(row, visual) for row in payload['backgroundRows']]
    set_assets = [_asset(row, visual) for row in payload['setRows']]
    albums, collections = _albums(background_assets, set_assets)
    all_assets = background_assets + set_assets
    background_ids = {row['id'] for row in background_assets}
    requests = [dict(id=row['id'], sha256=row['sha256'], type='missing_decision', requestedBy='CFA Site Index',
        requestedAt='2026-11-04T13:41:07Z', project=PROJECT, reviewControllerID=CONTROLLER,
        taskID=CAST_TASK if row['id'] in background_ids else SET_TASK,
        reason=('Review this preliminary background casting option.' if row['id'] in background_ids else
                'Review this preliminary set candidate in its recorded family/position context.') +
               ' No identity, set, shot, starting frame or output is selected or accepted.') for row in all_assets]
    result = deepcopy(catalog)
    existing_tcm_images = [row for row in result['assets'] if row.get('project') == PROJECT and row.get('kind') == 'image']
    existing_ids = {row['id'] for row in existing_tcm_images}
    incoming_ids = {row['id'] for row in all_assets}
    assert len(existing_tcm_images) in {200, 1194}
    if len(existing_tcm_images) == 200:
        assert not (existing_ids & incoming_ids)
        assert not ({row['sha256'] for row in existing_tcm_images} & {row['sha256'] for row in all_assets})
    else:
        assert incoming_ids <= existing_ids
    result['assets'] = _append(result['assets'], all_assets, 'TCM review asset')
    result['albums'] = _append(result['albums'], albums, 'TCM review album')
    result['castCollections'] = _append(result.get('castCollections', []), collections, 'TCM cast collection')
    result['reviewRequests'] = _append(result.get('reviewRequests', []), requests, 'TCM review request')
    tasks = {task['id']: task for task in result['missionControl']['tasks']}
    casting = tasks[CAST_TASK]
    cast_ids = [row['id'] for row in result['assets'] if row.get('project') == PROJECT and row.get('category') == 'cast']
    assert len(cast_ids) == 238 and casting.get('acceptedOutputs', 0) == 0
    casting.update(status='needs_input', statusLabel='238 casting portraits received · 33 groups', direction='inbound',
        outputFilesReceived=238, acceptedOutputs=0, previewAssetIDs=cast_ids,
        preparationState='all_speaking_and_background_casting_received_verified', physicalCandidatesReceived=170,
        backgroundCandidatesReceived=48, receivedBackgroundGroups=16,
        summary='All 190 speaking-role portraits and 48 background candidates are verified received. Provider/V-team screening remains preliminary evidence. No character identity, role, shot or starting frame is selected or accepted.',
        nextAction='Baldadoon reviews the 17 speaking-role and 16 background collections and records scoped decisions or changes. Adult John keeps ten matched three-state triples; background options remain separate, unselected candidates.',
        laterReview='A casting choice does not accept a shot, starting frame or finished video.')
    background_link = dict(label='Review 48 background casting candidates', href='#criminal_mind/review_queue',
                           assetIDs=[row['id'] for row in background_assets])
    prior_background_links = [link for link in casting['links'] if link.get('label') == background_link['label']]
    assert not prior_background_links or prior_background_links == [background_link]
    if not prior_background_links:
        casting['links'].append(background_link)
    set_task = tasks[SET_TASK]
    set_ids = [row['id'] for row in result['assets'] if row.get('project') == PROJECT and row.get('locationFamilyID')]
    assert len(set_ids) == 956 and set_task.get('acceptedOutputs', 0) == 0
    set_task.update(status='needs_input', statusLabel='956 set still entries received · 24 families', direction='inbound',
        outputFilesReceived=956, acceptedOutputs=0, previewAssetIDs=set_ids,
        preparationState='base_looks_and_set_camera_round_received_verified',
        receivedLocationFamilies=sorted({row['locationFamilyID'] for row in set_assets} | {'TCM-SET-HENDERSON-EXTERIOR'}),
        receivedLocationFamilyCount=24,
        baseLookOriginalsReceived=200, setCameraOriginalsReceived=756, uniqueSetImageHashes=954,
        summary='Two hundred base set looks and 756 later set-camera still entries are locally verified across 24 families. Two car identity-sheet frames intentionally reuse their take-2 bytes, preserving both mappings. Screening is preliminary; no still or car identity is selected or accepted.',
        nextAction='Baldadoon reviews the base-look and set-camera collections. Henderson exterior L03 is a provisional favorite/basket signal relayed as the house geometry, but no attributed saved review exists; the unmarked SUV remains a writer assumption and ID01 is not a director pick.',
        laterReview='A set choice remains scoped: it does not accept a shot, starting frame, performance, vehicle identity or finished video.')
    set_link = dict(label='Review 946 newly indexed set originals', href='#criminal_mind/review_queue',
                    assetIDs=[row['id'] for row in set_assets])
    prior_set_links = [link for link in set_task['links'] if link.get('label') == set_link['label']]
    assert not prior_set_links or prior_set_links == [set_link]
    if not prior_set_links:
        set_task['links'].append(set_link)
    project = next(row for row in result['projects'] if row['id'] == PROJECT)
    project['landing'].update(
        emptyMedia='1,194 review images are received: 238 casting portraits and 956 set still entries. None is accepted as a character, set image, shot, starting frame or output. Henderson exterior L03 is a provisional favorite/basket signal with no attributed saved review; the SUV and every cast identity remain unselected.',
        receivedReviewImages=1194, receivedCastingPortraits=238, receivedSetStillEntries=956,
        acceptedReviewImages=0)
    henderson = next(row for row in result['assets'] if row['id'] == 'TCM-SET-HENDERSON-EXTERIOR-L03')
    assert henderson['selected'] is False
    henderson['relayedAuthorChoiceSignal'] = {
        'scope': 'house_geometry',
        'decisionMaker': 'Baldadoon',
        'relayedBy': 'Ziggy',
        'recordedIn': 'TCM_DECISIONS_20261031.md section 1',
        'reviewEvidenceStatus': 'recovered_favorite_or_basket_only_no_attributed_saved_review',
        'note': 'Provisional scoped house-geometry signal only. No formal image review, shot, starting frame or production output acceptance is inferred.',
    }
    receipt_rows = result.setdefault('intakeReceipts', [])
    receipt_by_path = {row['path']: row for row in receipt_rows}
    for evidence in [payload['backgroundEvidence'], payload['setEvidence']]:
        assert evidence['path'] not in receipt_by_path or receipt_by_path[evidence['path']] == evidence
        if evidence['path'] not in receipt_by_path:
            receipt_rows.append(deepcopy(evidence))
    catalog.clear()
    catalog.update(result)
    return catalog
