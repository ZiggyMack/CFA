"""Read the pinned Story 01 panel map without changing sources or approvals.

Returned assets/documents are additions only. Existing exact path/hash records
are referenced by their canonical IDs and are never modified. No file writes,
copies, provider requests, thumbnail generation, or catalog publication occur.
"""
from collections import defaultdict
from copy import deepcopy
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

from grok500_catalog import CatalogIntakeError, io_path


SEQUENCE_ID = 'LAG-STORY-01-THE-GLOVED-HAND'
ALBUM_ID = 'lisan:story01-frames'
PROJECTS = 'docs/notes/explorable_world/comfy/projects/'
WRITER = PROJECTS + 'lisan_al_gaib/story/writer_pass_20261012/'
MAP_PATH = WRITER + 'STORY_01_PANEL_MAP_20261014.json'
MAP_MD_PATH = WRITER + 'STORY_01_PANEL_MAP_20261014.md'
SKELETON_PATH = WRITER + 'STORY_01_STORYBOARD_SKELETON_20261014.md'
REQUEST_PATH = PROJECTS + 'collaborators/storyboard_page_request_20261014/STORYBOARD_PAGE_REQUEST_20261014.md'
MESSAGE_ID = '8b44dfe3-8265-44cd-b050-0e69165f9644'
MESSAGE_PATH = PROJECTS + 'collaborators/mailbox/messages/' + MESSAGE_ID + '.json'
ATTACHMENT_PINS = {
    REQUEST_PATH: (9443, '425b8b17c8ff3a5b215c412d8e6955034581bcd862aa620438edc16ed29bb7c3'),
    MAP_PATH: (46653, 'c02099102b007ee68887860767fca710123f31cca4958a89b7e5581c69ca9331'),
    MAP_MD_PATH: (14044, 'cf059be5181a43676908fb8ff0c03f381585a1a5952370c8cf0c0b9d516006fe'),
    SKELETON_PATH: (12207, '263edf979a963358641fdae335ea07bd71b00907ca23bbdb4e1c6b6baadbfd38'),
}
CANONICAL_MATERIAL_IDS = {
    '602a9fd4021dc356086728a781aee985741811b3b401a52d9e85869652bb944f': 'LAG-602a9fd4021dc356',
    '23817577d3d32f0df03d57ac1e49c4c85246e86c405b13c492194f7aa2f52bad': 'LAG-C13-PATCH-C-23817577d3d3',
    '7eafd9ac048dc6d6125dc38281c1b664f7ae0cac1159909c34d90a5e3eef93a3': 'LAG-C13-ORIGINAL-7eafd9ac048d',
    '8f0c3d3bb4f7c8ff6fd6c98ec0f5cc4c8a5ae02daad375b4d2b9e63df0edebaf': 'FLOW-LAG-SW2-001',
    '82dfca3f6472b18dd7ca3919c02e7ca84dc229295eb3a1853b0a980c61f35833': 'LAG-82dfca3f6472b18d',
    'c07327fcf456e328a303a227ac4c11edf96352c913206df862d748145c9773bc': 'LAG-CAST-JET-BLACK-REF-02',
}
MATERIAL_ROLES = {'setting_stand_in', 'source_frame', 'result_on_disk',
                  'character_reference', 'storyboard_concept'}
# Manually classified from this exact pinned narrative, not a word-count heuristic.
PENDING_TYPES = {
    'the Keepers': 'character',
    'Angels': 'character',
    'the oldest Keeper': 'character',
    'Jet in the scene (LAG-JET-01)': 'character',
    'Jet in the scene': 'character',
    'the child with the lamp': 'character',
    'Sassy': 'character',
    'James (lettered)': 'character',
    'the thumper rack (a new request)': 'object_design',
    'the lattice (its form a proposal; colour unrecorded)': 'object_design',
    'the lattice': 'object_design',
}


def _safe_path(root: Path, relative: str) -> Path:
    if (not isinstance(relative, str) or not relative or
            re.search(r'[\\%?#:\x00-\x1f\x7f]', relative)):
        raise CatalogIntakeError('Unsafe Story 01 source path: ' + repr(relative))
    posix = PurePosixPath(relative)
    if posix.is_absolute() or any(p in {'.', '..'} for p in relative.split('/')):
        raise CatalogIntakeError('Unsafe Story 01 source path: ' + relative)
    path = (root / Path(*posix.parts)).resolve()
    if not path.is_relative_to(root):
        raise CatalogIntakeError('Story 01 source escapes the repository: ' + relative)
    return path


def _read_bytes(path: Path) -> bytes:
    return io_path(path).read_bytes()


def _json(raw: bytes, label: str) -> dict:
    try:
        data = json.loads(raw.decode('utf-8-sig'))
    except (ValueError, UnicodeError) as error:
        raise CatalogIntakeError('Invalid Story 01 JSON: ' + label) from error
    if not isinstance(data, dict):
        raise CatalogIntakeError('Story 01 JSON must be an object: ' + label)
    return data


def _pin(relative: str, raw: bytes) -> dict:
    return {'path': relative, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def load_story01(root: Path, existing_assets: list) -> dict:
    """Verify and resolve the dated map, returning additions and one sequence."""
    root = Path(root).resolve()
    checked = {}

    def verify(relative, size=None, digest=None):
        path = _safe_path(root, relative)
        try:
            raw = checked.get(relative)
            if raw is None:
                raw = _read_bytes(path)
                checked[relative] = raw
        except OSError as error:
            raise CatalogIntakeError('Missing Story 01 source: ' + relative) from error
        actual = _pin(relative, raw)
        if ((size is not None and (type(size) is not int or size != actual['bytes'])) or
                (digest is not None and digest != actual['sha256'])):
            raise CatalogIntakeError('Story 01 source pin mismatch: ' + relative)
        return raw

    message = _json(verify(MESSAGE_PATH), MESSAGE_PATH)
    attachment_rows = message.get('attachments', [])
    if (message.get('id') != MESSAGE_ID or not isinstance(attachment_rows, list) or
            len(attachment_rows) != len(ATTACHMENT_PINS) or
            {a.get('path'): (a.get('bytes'), a.get('sha256')) for a in attachment_rows
             if isinstance(a, dict)} != ATTACHMENT_PINS):
        raise CatalogIntakeError('Story 01 handoff identity/attachment pins differ.')
    for relative, (size, digest) in ATTACHMENT_PINS.items():
        verify(relative, size, digest)
    source = _json(checked[MAP_PATH], MAP_PATH)
    if (source.get('schemaVersion') != 1 or source.get('id') != SEQUENCE_ID or
            source.get('project') != 'lisan' or source.get('stage') != 'preliminary' or
            source.get('timing') is not None or source.get('positionBasis') != 'shot_order'):
        raise CatalogIntakeError('Unexpected Story 01 sequence identity/stage/timing.')
    sections, shots = source.get('sections', []), source.get('shots', [])
    shot_ids = [s.get('shotID') for s in shots]
    if (len(shots) != 38 or len(set(shot_ids)) != 38 or len(sections) != 9 or
            [s.get('scene') for s in sections] != list(range(1, 10)) or
            [sid for section in sections for sid in section.get('shotIDs', [])] != shot_ids or
            any(shot.get('scene') != section['scene'] for section in sections
                for shot in shots if shot['shotID'] in section['shotIDs'])):
        raise CatalogIntakeError('Story 01 scene/shot order or binding differs.')

    by_id, by_path, by_hash = {}, defaultdict(list), defaultdict(list)
    for asset in existing_assets:
        aid = asset.get('id')
        if not isinstance(aid, str) or aid in by_id:
            raise CatalogIntakeError('Duplicate or invalid existing asset ID: ' + repr(aid))
        by_id[aid] = asset
        relative = asset.get('repoPath', asset.get('path'))
        if relative:
            by_path[relative.casefold()].append(asset)
        if asset.get('sha256'):
            by_hash[asset['sha256']].append(asset)

    unique, uses = {}, defaultdict(list)
    for shot in shots:
        for material in shot.get('materials', []):
            relative, digest, size = material.get('repoPath'), material.get('sha256'), material.get('bytes')
            if (material.get('role') not in MATERIAL_ROLES or
                    not isinstance(digest, str) or not re.fullmatch('[a-f0-9]{64}', digest) or
                    type(size) is not int or size <= 0):
                raise CatalogIntakeError('Invalid Story 01 material binding: ' + shot['shotID'])
            verify(relative, size, digest)
            if relative in unique and any(unique[relative][key] != material[key] for key in ['sha256', 'bytes']):
                raise CatalogIntakeError('Conflicting Story 01 material pins: ' + relative)
            unique.setdefault(relative, material)
            uses[relative].append({'shotID': shot['shotID'], 'role': material['role'],
                                   **({'note': material['note']} if 'note' in material else {})})
        if any(label not in PENDING_TYPES for label in shot.get('pendingReferences', [])):
            raise CatalogIntakeError('Unclassified Story 01 pending reference: ' + shot['shotID'])
    if len(unique) != 56 or sum(map(len, uses.values())) != 98 or len({m['sha256'] for m in unique.values()}) != 56:
        raise CatalogIntakeError('Story 01 must retain 56 unique files and 98 material associations.')

    new_assets, resolved, reused = [], {}, []
    for relative, material in unique.items():
        digest = material['sha256']
        matches = by_path.get(relative.casefold(), [])
        required_id = CANONICAL_MATERIAL_IDS.get(digest)
        if matches:
            if len(matches) != 1:
                raise CatalogIntakeError('Ambiguous registered Story 01 material path: ' + relative)
            asset = matches[0]
            expected_kind = 'video' if any(u['role'] == 'result_on_disk' for u in uses[relative]) else 'image'
            if (asset.get('sha256') != digest or asset.get('project') != 'lisan' or
                    asset.get('kind', 'image') != expected_kind or
                    asset.get('bytes') not in (None, material['bytes']) or
                    (required_id and asset['id'] != required_id)):
                raise CatalogIntakeError('Registered Story 01 material identity differs: ' + relative)
            aid = asset['id']
            reused.append({'assetID': aid, **_pin(relative, checked[relative])})
        else:
            if required_id:
                raise CatalogIntakeError('Required canonical Story 01 asset is missing: ' + required_id)
            if by_hash.get(digest):
                raise CatalogIntakeError('Story 01 hash exists at a different registered path: ' + relative)
            aid = 'LAG-1K-' + digest[:16]
            if aid in by_id or aid in resolved.values():
                raise CatalogIntakeError('Story 01 asset ID collision: ' + aid)
            if not relative.startswith('docs/notes/explorable_world/comfy/references/From Grok/GROK-LAG-1K-') or Path(relative).suffix.lower() != '.jpg':
                raise CatalogIntakeError('Unregistered Story 01 material is outside the bounded frame intake.')
            mapped_notes = list(dict.fromkeys(u['note'] for u in uses[relative] if u.get('note')))
            note = ('Story 01 setting stand-in from the LAG-1K archive; the figure is Lisan. '
                    'Only its mapped material role applies in each shot. Folder NOTES/self-scores '
                    'are attributed preliminary provider observations, not human ratings, approval, '
                    'or production readiness.')
            if mapped_notes:
                note += ' Writer-map observations: ' + ' | '.join(mapped_notes)
            new_assets.append({'id': aid, 'project': 'lisan', 'path': relative,
                'category': 'storyboard', 'album': ALBUM_ID,
                'title': Path(relative).stem + ' · Story 01 stand-in',
                'stage': 'preliminary', 'storyboardStage': 'preliminary', 'timing': None,
                'sha256': digest, 'bytes': material['bytes'], 'note': note,
                'storySequenceID': SEQUENCE_ID, 'sourceIntake': SEQUENCE_ID,
                'sourceMessageID': MESSAGE_ID, 'sourceStatus': 'preliminary_setting_stand_in',
                'acceptance': 'not_accepted', 'approvalScope': None,
                'masterApproved': False, 'productionReady': False,
                'materialRoles': list(dict.fromkeys(u['role'] for u in uses[relative])),
                'story01MaterialUses': deepcopy(uses[relative]),
                'tags': ['Story 01', 'The Gloved Hand', 'LAG-1K', 'setting stand-in', 'preliminary']})
        resolved[relative] = aid
    if not set(CANONICAL_MATERIAL_IDS.values()).issubset(resolved.values()):
        raise CatalogIntakeError('Story 01 lost a canonical material binding.')

    document_paths = list(dict.fromkeys([MAP_PATH, MAP_MD_PATH, SKELETON_PATH, *source['sourceDocuments']]))
    documents, document_ids, document_refs = [], [], []
    for relative in document_paths:
        if not relative.startswith(WRITER) or Path(relative).suffix.lower() not in {'.json', '.md'}:
            raise CatalogIntakeError('Story 01 document outside its writer scope.')
        raw = verify(relative)
        pin = _pin(relative, raw)
        aid = 'lisan:doc:' + relative
        matches = by_path.get(relative.casefold(), [])
        if matches:
            if (len(matches) != 1 or matches[0]['id'] != aid or
                    matches[0].get('project') != 'lisan' or matches[0].get('kind') != 'document' or
                    matches[0].get('sha256') not in (None, pin['sha256']) or
                    matches[0].get('bytes') not in (None, pin['bytes'])):
                raise CatalogIntakeError('Registered Story 01 document changed: ' + relative)
        elif aid in by_id:
            raise CatalogIntakeError('Story 01 document ID collision: ' + aid)
        else:
            documents.append({'id': aid, 'project': 'lisan', **pin,
                              'title': Path(relative).stem.replace('_', ' '),
                              'album': 'Story 01 · The Gloved Hand writings'})
        document_ids.append(aid)
        document_refs.append({'assetID': aid, **pin})

    sequence = deepcopy(source)
    sequence['assetIDs'] = list(resolved.values())
    sequence['sourceAlbumIDs'] = [ALBUM_ID]
    sequence['coverID'] = resolved[source['shots'][0]['materials'][0]['repoPath']]
    sequence['documentIDs'] = document_ids
    sequence['sourceDocumentReferences'] = document_refs
    sequence['sourceMap'] = _pin(MAP_PATH, checked[MAP_PATH])
    sequence['sourceMessageID'] = MESSAGE_ID
    sequence['acceptance'] = 'not_accepted'
    for shot in sequence['shots']:
        for material in shot['materials']:
            material['assetID'] = resolved[material['repoPath']]
        shot['pendingReferenceDetails'] = [{'label': label, 'kind': PENDING_TYPES[label]}
                                           for label in shot.get('pendingReferences', [])]
    frame_shots = [s['shotID'] for s in shots if any(m['role'] in {'setting_stand_in', 'source_frame'} for m in s['materials'])]
    result_shots = [s['shotID'] for s in shots if any(m['role'] == 'result_on_disk' for m in s['materials'])]
    pending_shots = [s['shotID'] for s in shots if s['pendingReferences']]
    character_shots = [s['shotID'] for s in shots if any(PENDING_TYPES[p] == 'character' for p in s['pendingReferences'])]
    object_shots = [s['shotID'] for s in shots if any(PENDING_TYPES[p] == 'object_design' for p in s['pendingReferences'])]
    object_only = [sid for sid in object_shots if sid not in character_shots]
    summary = {'shots': len(shots), 'shotsWithAFrameOnDisk': len(frame_shots),
               'shotsWithAResultOnDisk': len(result_shots), 'shotsWithPendingReferences': len(pending_shots),
               'distinctFiles': len(unique)}
    if summary != source['summary'] or (len(character_shots), len(object_shots), object_only, result_shots) != (20, 5, ['S01-5.3'], ['S01-4.1']):
        raise CatalogIntakeError('Story 01 coverage differs from its verified narrative.')
    sequence['summary'] = {**summary, 'shotsWithPendingCharacterReferences': len(character_shots),
                           'shotsWithPendingObjectReferences': len(object_shots),
                           'shotsWithOnlyPendingObjectReferences': len(object_only)}
    verification = {'sourceMessage': _pin(MESSAGE_PATH, checked[MESSAGE_PATH]),
        'attachments': [_pin(p, checked[p]) for p in ATTACHMENT_PINS],
        'materialFiles': [{**_pin(p, checked[p]), 'assetID': resolved[p]} for p in unique],
        'reusedAssets': reused, 'newAssetCount': len(new_assets), 'reusedAssetCount': len(reused),
        'materialAssociationCount': 98, 'newDocumentCount': len(documents),
        'frameShotIDs': frame_shots, 'resultShotIDs': result_shots,
        'pendingReferenceShotIDs': pending_shots, 'pendingCharacterShotIDs': character_shots,
        'pendingObjectShotIDs': object_shots, 'objectOnlyPendingShotIDs': object_only,
        'newHumanRatings': 0, 'newApprovals': 0, 'sourceMutation': False}
    # A build must not publish an intake assembled across changing source versions.
    for relative, raw in checked.items():
        if _read_bytes(_safe_path(root, relative)) != raw:
            raise CatalogIntakeError('Story 01 source changed during intake: ' + relative)
    return {'albums': [{'id': ALBUM_ID, 'project': 'lisan', 'category': 'storyboard',
                        'title': 'Story 01 · The Gloved Hand frames',
                        'description': 'Preliminary setting stand-ins with separately scoped character references, source frames and the unaccepted Flow result.',
                        'related': list(resolved.values())}],
            'assets': new_assets, 'documents': documents,
            'sequence': sequence, 'verification': verification}
