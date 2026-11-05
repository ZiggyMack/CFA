"""Draft-only integration snippets. Importing this file does not build or edit the site.

For build_catalog.py, call add_flow_prototypes after the source-comparison media
loop and before the review-promotion / album assetIDs passes. Call append_flow_shots
immediately after loading catalog['shotMaterials'], before its existing validator.
The site owner should copy the reviewed manifest to visual_library/flow_prototypes.json
and set publicationState to registered_for_site_build before using it in a build.
"""
from pathlib import Path
import hashlib
import json


def add_flow_prototypes(manifest_path, *, root, assets, add_album, url, doc,
                        io_path, resolve_source):
    data = json.loads(Path(manifest_path).read_text(encoding='utf-8'))
    assert data['format'] == 'cfa-flow-prototypes-v1'
    assert data['publicationState'] == 'registered_for_site_build'
    assert data['scope'] == {
        'registerExactOriginals': True,
        'reuseExistingSourceAssetIDs': True,
        'seedHumanReviews': False,
        'seedSceneReviews': False,
        'assignSongTiming': False,
        'assignSourcePanelNumbers': False,
        'promoteWorkingReferences': False,
        'runProviders': False,
        'includeUndownloadedGemini': False,
        'includeUnfinalizedWriterDirection': False,
    }

    def verify(pin):
        physical = resolve_source(root, pin['path'],
                                  expected_sha256=pin['sha256'],
                                  expected_bytes=pin['bytes'])
        raw = io_path(physical).read_bytes()
        assert len(raw) == pin['bytes'], pin['path']
        assert hashlib.sha256(raw).hexdigest() == pin['sha256'], pin['path']
        return raw

    def at(value, field):
        for part in field.split('.'):
            value = value[int(part)] if isinstance(value, list) else value[part]
        return value

    def core(pin):
        return {key: pin[key] for key in ('path', 'bytes', 'sha256')}

    def nested_pins(value, field=''):
        rows = []
        if isinstance(value, dict):
            if {'path', 'bytes', 'sha256'} <= value.keys() and value['bytes'] and value['sha256']:
                rows.append({'field': field, **core(value)})
            for key, child in value.items():
                rows.extend(nested_pins(child, field + '.' + key if field else key))
        elif isinstance(value, list):
            for index, child in enumerate(value):
                rows.extend(nested_pins(child, field + '.' + str(index)))
        return rows

    expected = {
        'sw2': ('FLOW-LAG-SW2-001', 'LAG-C13-PATCH-C-23817577d3d3'),
        'signal': ('FLOW-LAG-SIGNAL-001', 'LAG500-L19-S3'),
        'signal_take2': ('FLOW-LAG-SIGNAL-002', 'LAG500-L19-S3'),
    }
    assert len(data['intakes']) == 3
    assert {row['id'] for row in data['intakes']} == set(expected)
    assert len(data['media']) == 3
    assert len(data['documents']) == 3
    existing = {item['id']: item for item in assets}
    planned_ids = [item['id'] for item in data['media'] + data['documents']]
    assert len(set(planned_ids)) == 6 and not (set(planned_ids) & set(existing))
    sources = {}
    originals = {}
    records = {row['id']: row for row in data['intakes']}
    media_by_id = {item['id']: item for item in data['media']}
    documents_by_id = {item['id']: item for item in data['documents']}

    # Validate every authoritative record and all its nested pins before mutation.
    for key, record in records.items():
        media_id, source_id = expected[key]
        assert record['mediaAssetID'] == media_id
        assert record['sourceAssetID'] == source_id
        receipt = json.loads(verify(record['intake']))
        assert nested_pins(receipt) == record['nestedPins'], key
        for pinned in record['nestedPins']:
            verify(pinned)
        verify(record['poster'])
        source = at(receipt, record['sourceField'])
        original = at(receipt, record['originalField'])
        measured = at(receipt, record['measurementField'])
        sources[key], originals[key] = source, original
        assert source_id in existing
        assert existing[source_id]['sha256'] == source['sha256']
        assert existing[source_id]['repoPath'] == source['path']
        assert receipt.get('providerSceneURL', receipt.get('sceneURL')) == record['providerSceneURL']
        if key == 'sw2':
            assert measured['durationSeconds'] == 8
            assert (measured['width'], measured['height'], measured['fps'], measured['frames']) == (1280, 720, 24, 192)
            assert measured['fullVideoAndAudioDecodeExitCode'] == 0
            assert receipt['evidenceState']['humanAccepted'] is False
            assert receipt['evidenceState']['productionAccepted'] is False
        else:
            assert measured['pictureDurationSeconds'] == 8
            assert measured['dimensions'] == [1280, 720]
            assert measured['frameRate'] == '24/1' and measured['frameCount'] == 192
            assert measured['fullDecodePassed'] is True
            if key == 'signal':
                assert receipt['status']['humanProductionAcceptanceClaimed'] is False
                assert receipt['humanFeedback']['numericCharacterGrade'] is None
                assert receipt['humanFeedback']['numericSceneGrade'] is None
                assert receipt['humanFeedback']['triageKeepDecision'] is None
            else:
                assert receipt['resultID'] == 'FLOW-LAG-SIGNAL-002'
                assert receipt['status']['productionApprovalClaimed'] is False
                assert receipt['status']['humanAcceptancePending'] is True
                assert receipt['prototypeAssessment']['performanceFixedClaimed'] is False
                authority = receipt['baselineAndHumanAuthority']
                assert all(authority[field] is None for field in ['newTakeTwoHumanFeedback', 'numericCharacterGrade', 'numericSceneGrade', 'triageKeepDecision', 'productionAcceptance'])
                assert record['predecessorAssetID'] == 'FLOW-LAG-SIGNAL-001'
                assert core(at(receipt, record['predecessorField'])) == core(media_by_id['FLOW-LAG-SIGNAL-001'])
                assert core(authority['firstTakeFeedbackIntake']) == core(records['signal']['intake'])
                assert core(receipt['frozenWriterCardAtSubmission']) == core(receipt['creativeOwnership']['finishedCardAtThisRun'])
        media = media_by_id[media_id]
        assert core(media) == core(original)
        assert media['parentAssetID'] == source_id and media['sourceSHA256'] == source['sha256']
        assert media['thumbnailPath'] == record['poster']['path']
        assert media['provenancePath'] == record['intake']['path']
        assert media['provenanceSHA256'] == record['intake']['sha256']
        assert media['providerSceneURL'] == record['providerSceneURL']
        assert media['intakeID'] == key
        assert (media['project'], media['kind'], media['category'], media['album']) == ('lisan', 'video', 'videos', 'lisan:video-flow-prototypes')
        assert (media['duration'], media['width'], media['height'], media['fps'], media['frameCount']) == (8, 1280, 720, 24, 192)
        assert media['storyboardStage'] == 'preliminary' and media['defaultReferenceScope'] == 'scene'
        assert media['provider'] == 'Flow'
        if key == 'signal_take2':
            assert media['predecessorAssetID'] == 'FLOW-LAG-SIGNAL-001'
            assert media['takeNumber'] == receipt['takeNumber'] == 2
            assert media['writerShotID'] == receipt['writerShotID'] == 'LAG-SIGNAL-002'
        assert not any(old.get('sha256') == media['sha256'] for old in assets)
        assert not {'workingReference', 'status', 'likenessRating', 'sceneQualityRating', 'componentApprovals', 'archived'} & media.keys()
        document_id = 'lisan:doc:' + record['intake']['path']
        assert record['documentAssetID'] == document_id
        document = documents_by_id[document_id]
        assert document['project'] == 'lisan' and document['intakeID'] == key
        assert core(document) == core(record['intake'])

    assert len(data['albums']) == 2
    assert {row['id'] for row in data['albums']} == {'lisan:video-flow-prototypes', 'lisan:story-flow-prototypes'}
    for album in data['albums']:
        assert album['project'] == 'lisan'
        expected_category = 'videos' if album['id'] == 'lisan:video-flow-prototypes' else 'storyboard'
        assert album['category'] == expected_category
        expected_related = [] if expected_category == 'videos' else list(media_by_id)
        assert album['related'] == expected_related

    assert len(data['shots']) == 3
    expected_shots = {'LAG-FLOW-SW2-001': 'sw2', 'LAG-FLOW-SIGNAL-001': 'signal', 'LAG-FLOW-SIGNAL-002': 'signal_take2'}
    assert {shot['id'] for shot in data['shots']} == set(expected_shots)
    for shot in data['shots']:
        record = records[expected_shots[shot['id']]]
        assert shot['project'] == 'lisan'
        assert shot['panelIDs'] == [] and shot['panelAssetIDs'] == []
        assert shot['sectionID'] is None and shot['timing'] == 'unassigned'
        assert shot['stage'] == 'preliminary' and shot['acceptance'] == 'not_accepted'
        assert shot['sourceIntakePath'] == record['intake']['path']
        assert shot['sourceIntakeSHA256'] == record['intake']['sha256']
        material_ids = [item['assetID'] for item in shot['materials']]
        expected_material_ids = [record['sourceAssetID'], record['mediaAssetID'], record['documentAssetID']]
        if record['id'] == 'signal_take2':
            expected_material_ids.append(record['predecessorAssetID'])
        assert material_ids == expected_material_ids
        assert all(item['role'] != 'storyboard_concept' for item in shot['materials'])
        hashes = [sources[record['id']]['sha256'], originals[record['id']]['sha256'], record['intake']['sha256']]
        if record['id'] == 'signal_take2':
            hashes.append(media_by_id[record['predecessorAssetID']]['sha256'])
        assert [item['sha256'] for item in shot['materials']] == hashes

    for album in data['albums']:
        add_album(album['project'], album['id'].split(':', 1)[1],
                  album['category'], album['title'], album['description'], album['related'])
    for item in data['media']:
        asset = dict(item)
        path = asset.pop('path')
        poster = asset.pop('thumbnailPath')
        asset.update(src=url(path), thumb=url(poster), repoPath=path, filename=Path(path).name)
        assets.append(asset)
    for record in data['documents']:
        doc(record['project'], record['path'], record['title'], record['album'])
        asset = assets[-1]
        assert asset['id'] == record['id']
        asset.update(sha256=record['sha256'], bytes=record['bytes'],
                     sourceStatus=record['sourceStatus'], intakeID=record['intakeID'])
    return data


def append_flow_shots(shot_materials, flow_prototypes):
    existing = {(shot['project'], shot['id']) for shot in shot_materials['shots']}
    assert all((shot['project'], shot['id']) not in existing for shot in flow_prototypes['shots'])
    # This extends only the in-memory catalog. Existing source JSON is not rewritten.
    shot_materials['shots'].extend(flow_prototypes['shots'])


# Exact build_catalog.py invocation A, after source-comparison media registration:
# from flow_prototype_intake import add_flow_prototypes, append_flow_shots
# flow_prototypes = add_flow_prototypes(
#     HERE/'flow_prototypes.json', root=ROOT, assets=assets,
#     add_album=add_album, url=url, doc=doc,
#     io_path=io_path, resolve_source=resolve_source)
#
# Exact invocation B, after reading catalog['shotMaterials'] and before its validator:
# append_flow_shots(catalog['shotMaterials'], flow_prototypes)
