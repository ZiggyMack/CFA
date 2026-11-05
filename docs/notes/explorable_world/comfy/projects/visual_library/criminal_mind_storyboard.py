"""Bind the sealed TCM preliminary coverage to the shared storyboard views.

No media, review, source-frame selection, dispatch or acceptance is inferred.
The function is usable on an already verified catalog and is idempotent.
"""
from copy import deepcopy
import hashlib
import json
import os
from pathlib import Path
from urllib.parse import quote


PROJECT_ID = 'criminal_mind'
STORY_ID = 'criminal_mind:the-criminal-mind'
SEQUENCE_ID = STORY_ID
BASE = Path('docs/notes/explorable_world/comfy/projects')
PACKET_DIR = BASE / 'the_criminal_mind/story/preliminary_pass_20261030'
INTAKE_DIR = BASE / 'the_criminal_mind/source_intake_20261030'
CARDS_ID = 'TCM-PRELIMINARY-SHOT-CARDS-20261030'
STRUCTURE_ID = 'TCM-STORYBOARD-STRUCTURE-20261030'
VERIFICATION_ID = 'TCM-STORYBOARD-VERIFICATION-20261030'
DOCUMENTS = (
    (CARDS_ID, 'TCM_PRELIMINARY_SHOT_CARDS_v001.md',
     '8f79c29dbab12718f25b8a67909af917e576d4398b03f6df6fcef3333bd4cd9b', 1029304,
     'The Criminal Mind · Preliminary shot cards',
     '165 proposed coverage shots across 41 source-scene groups. Read each shot in Panels & writings or Structure & gaps; open the full source for the complete written packet.'),
    (STRUCTURE_ID, 'TCM_STORYBOARD_STRUCTURE_v001.json',
     '12b738e8861d2feff5a1237b2e689876f8bf5593999e8170d0b3cb3dbd481484', 4715895,
     'The Criminal Mind · Preliminary structure source',
     'Machine-readable source for 165 Preliminary shots with the shared 16-field model and exact screenplay excerpts. The structured shot view contains this writing; this document retains the complete inert JSON source.'),
    (VERIFICATION_ID, 'VERIFICATION_v001.json',
     'abeae3f9a0af5186d8ad111a72194d4ae0cac787fad8769ea56a8a9f782b3e1b', 1058,
     'The Criminal Mind · packet verification',
     'Packet integrity and source-line coverage checks. Verification of the supplied files does not approve the proposed adaptation, artwork, timing or any generated result.'),
)
FIELD_KEYS = ('purpose', 'context', 'lineage', 'references', 'start_frame', 'lighting',
              'camera', 'character', 'background', 'beats', 'cue', 'prompt_still',
              'prompt_clip', 'settings', 'results', 'acceptance')


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _require(condition, message):
    if not condition:
        raise ValueError(message)


def _read(root, path, digest, size):
    relative = Path(path)
    _require(not relative.is_absolute() and '..' not in relative.parts, 'Invalid TCM source path')
    target = (root / relative).resolve()
    _require(target.is_relative_to(root), 'TCM source outside repository')
    raw = target.read_bytes()
    _require(len(raw) == size and _sha(raw) == digest, 'TCM source bytes changed: ' + str(path))
    text = raw.decode('utf-8-sig')
    _require('\ufffd' not in text, 'Replacement character in sealed TCM source: ' + str(path))
    return raw, text


def _evidence(asset):
    return dict(path=asset['repoPath'], assetID=asset['id'], sha256=asset['sha256'],
                bytes=asset['bytes'], line=None, endLine=None)


def _document(root, row, text):
    asset_id, filename, digest, size, title, summary = row
    path = PACKET_DIR / filename
    return dict(id=asset_id, project=PROJECT_ID, category='documents', kind='document',
                album=PROJECT_ID + ':preliminary-storyboard', title=title, filename=filename,
                repoPath=path.as_posix(),
                src=quote(os.path.relpath(root / path, root / BASE / 'visual_library').replace('\\', '/'), safe='/'),
                sha256=digest, bytes=size, text=text if asset_id == VERIFICATION_ID else summary,
                textPreviewOnly=asset_id != VERIFICATION_ID, inert=True,
                author='CFA Nova', originalAuthor='Baldadoon', controllerID='baldadoon',
                sourceIntake='TCM-PRELIMINARY-20261030', sourceStatus='Preliminary proposal · specialist review pending',
                note='Authored coverage is not a generated clip, accepted image or measured runtime. Adaptation scope remains a human choice.',
                tags=['Storyboard', 'Preliminary', 'Writer proposal'])


def _validate(root, catalog):
    """Validate all supplied bytes, excerpts and evidence before changing anything."""
    by_id = {a['id']: a for a in catalog['assets']}
    _require(len(by_id) == len(catalog['assets']), 'Duplicate catalog asset identity')
    docs, texts = [], {}
    for row in DOCUMENTS:
        raw, text = _read(root, PACKET_DIR / row[1], row[2], row[3])
        asset = _document(root, row, text)
        docs.append(asset)
        texts[row[0]] = text
    verification = json.loads(texts[VERIFICATION_ID])
    _require(verification.get('format') == 'cfa-preliminary-shot-verification-v1', 'Unexpected TCM verification format')
    pinned = {a['repoPath']: (a['sha256'], a['bytes']) for a in docs[:2]}
    supplied = verification.get('files', [])
    _require(len(supplied) == 2 and {r['path']: (r['sha256'], r['bytes']) for r in supplied} == pinned,
             'TCM verification file set differs')
    packet = json.loads(texts[STRUCTURE_ID])
    _require(packet.get('format') == 'cfa-storyboard-structure-v1' and len(packet.get('stories', [])) == 1,
             'Unexpected TCM structure format')
    _require([f['key'] for f in packet['fields']] == list(FIELD_KEYS), 'TCM shared fields differ')
    structure = deepcopy(packet['stories'][0])
    _require(structure.get('storyID') == STORY_ID and structure.get('project') == PROJECT_ID,
             'TCM story identity differs')
    _require(structure.get('reviewControllerID') == 'baldadoon', 'TCM review owner differs')
    sources = {a['id']: a for a in docs}
    for asset_id in ('TCM-SCRIPT-TEXT', 'TCM-SOURCE-INVENTORY'):
        asset = by_id.get(asset_id)
        _require(asset and asset.get('project') == PROJECT_ID, 'Apply the screenplay intake first')
        raw, text = _read(root, asset['repoPath'], asset['sha256'], asset['bytes'])
        sources[asset_id], texts[asset_id] = asset, text
    _require(packet['sourceScript'] == _evidence(sources['TCM-SCRIPT-TEXT']), 'Script source binding differs')
    script_lines = texts['TCM-SCRIPT-TEXT'].splitlines()
    cards_lines = texts[CARDS_ID].splitlines()
    line_counts = {asset_id: len(text.splitlines()) for asset_id, text in texts.items()}
    card_boundaries = [i + 1 for i, line in enumerate(cards_lines) if line.startswith(('## ', '### '))] + [len(cards_lines) + 1]
    inventory = json.loads(texts['TCM-SOURCE-INVENTORY'])
    blocks = {b['source_block_id']: b for b in inventory}
    _require(len(blocks) == len(inventory) == 41, 'TCM source inventory differs')
    for block in inventory:
        start, end = block['line_start'], block['line_end_inclusive']
        _require(1 <= start <= end <= len(script_lines), 'Invalid TCM source block range')
        excerpt = '\n'.join(script_lines[start - 1:end])
        _require(_sha(excerpt.encode('utf-8')) == block['text_sha256'], 'TCM source block hash differs')
        _require(script_lines[start - 1].strip() == block['source_heading_verbatim'].strip(), 'TCM source heading differs')

    def validate_evidence(value, card_range=None):
        if isinstance(value, list):
            for child in value:
                validate_evidence(child, card_range)
        elif isinstance(value, dict):
            if {'path', 'assetID', 'sha256', 'bytes'} <= value.keys():
                asset = sources.get(value['assetID'])
                _require(asset and all(value[key] == asset[target] for key, target in
                                       [('path', 'repoPath'), ('sha256', 'sha256'), ('bytes', 'bytes')]),
                         'Unbound TCM source evidence')
                start, end = value.get('line'), value.get('endLine')
                if start is not None or end is not None:
                    _require(type(start) is int and type(end) is int and 1 <= start <= end <= line_counts[asset['id']],
                             'Invalid TCM evidence line range')
                if card_range and value['assetID'] == CARDS_ID:
                    _require((start, end) == card_range, 'TCM card evidence physical line range differs')
            for child in value.values():
                validate_evidence(child, card_range)
    validate_evidence(structure['source'])
    shots, sections = structure['shots'], structure['sections']
    shot_ids = [s['shotID'] for s in shots]
    declared = [sid for section in sections for sid in section['shotIDs']]
    _require(len(shots) == len(set(shot_ids)) == 165 and len(sections) == 41, 'TCM shot/section count differs')
    _require(declared == shot_ids and len({s['id'] for s in sections}) == 41, 'TCM section/shot crosswalk differs')
    _require([bid for s in sections for bid in s['sourceBlockIDs']] == list(blocks), 'TCM source-group crosswalk differs')
    section_by_shot = {sid: section for section in sections for sid in section['shotIDs']}
    covered = set()
    for index, shot in enumerate(shots):
        block = blocks.get(shot.get('sourceBlockID'))
        section = section_by_shot[shot['shotID']]
        _require(block and shot['sectionID'] == section['id'] and shot['sourceBlockID'] in section['sourceBlockIDs'],
                 'TCM shot source group differs')
        _require(shot.get('stage') == 'preliminary' and shot.get('reviewControllerID') == 'baldadoon', 'TCM shot stage/owner differs')
        _require([f['key'] for f in shot['fields']] == list(FIELD_KEYS) and
                 all(f.get('status') in {'draft', 'missing', 'unknown'} and isinstance(f.get('text'), str) for f in shot['fields']),
                 'TCM shot fields differ or imply unsupported approval')
        _require(not shot.get('materials') and not shot.get('kitchen') and not shot.get('kitchenWritten') and
                 not shot.get('revisions') and shot.get('videoDispatchReady') is False,
                 'TCM packet unexpectedly declares media, prepared kitchen, revision or dispatch')
        _require(all(shot.get(k) is None for k in ('timing', 'songStartSeconds', 'songEndSeconds')), 'TCM timing must remain unmeasured')
        start, end = shot['sourceLineStart'], shot['sourceLineEnd']
        _require(type(start) is int and type(end) is int and block['line_start'] <= start <= end <= block['line_end_inclusive'],
                 'TCM shot excerpt leaves its source group')
        excerpt = '\n'.join(script_lines[start - 1:end])
        _require(excerpt == shot['sourceExcerpt'] and _sha(excerpt.encode('utf-8')) == shot['sourceExcerptSHA256'],
                 'TCM shot excerpt no longer matches exact screenplay lines')
        _require(shot['coverageEvidence']['line'] == start and shot['coverageEvidence']['endLine'] == end,
                 'TCM excerpt evidence range differs')
        _require(shot['parent']['line'] == block['line_start'] and shot['parent']['endLine'] == block['line_end_inclusive'],
                 'TCM source parent range differs')
        validate_evidence(shot)
        card_start = shot['source']['line']
        _require(cards_lines[card_start - 1].startswith('### ' + shot['shotID'] + ' '),
                 'TCM card line does not identify the shot')
        card_end = next(line for line in card_boundaries if line > card_start) - 1
        while card_end > card_start and not cards_lines[card_end - 1].strip():
            card_end -= 1
        validate_evidence(shot, (card_start, card_end))
        _require(shot.get('previousShotID') == (shot_ids[index - 1] if index else None) and
                 shot.get('nextShotID') == (shot_ids[index + 1] if index + 1 < len(shots) else None),
                 'TCM neighboring-shot links differ')
        covered.update(range(start, end + 1))
    _require(covered == set(range(2, 1922)), 'TCM screenplay line coverage is incomplete')
    _require(verification.get('sourceGroups') == 41 and verification.get('proposedCoverageShots') == 165 and
             verification.get('sourceLineCoverage') == [2, 1921] and
             verification.get('cardEvidencePhysicalLineRangesVerified') is True and
             verification.get('markdownPhysicalLines') == len(cards_lines) == 9705 and
             all(verification.get(k) is True for k in ('allSourceLinesCovered', 'exactExcerptHashesVerified', 'all16FieldsPresent', 'allShotsPreliminary', 'noInventedMediaOrReviews')) and
             all(verification.get(k) == 0 for k in ('kitchenPackagesReady', 'providerRuns', 'claudeRequests')),
             'TCM verification assertions differ from the sealed coverage')
    return docs, structure


def _append_record(rows, value, key='id'):
    matches = [row for row in rows if row.get(key) == value[key]]
    _require(len(matches) <= 1, 'Duplicate TCM catalog record: ' + value[key])
    if matches:
        _require(matches[0] == value, 'Existing TCM record changed; reconcile separately: ' + value[key])
        return rows
    return [*rows, value]


def apply_criminal_mind_storyboard(catalog, root):
    """Add verified Preliminary coverage in place; return the same catalog.

    Existing TCM records must match exactly on repeat application. All other
    projects, shared definitions, task decisions and review records stay intact.
    Validation and conflict checks finish before the first mutation.
    """
    root = Path(root).resolve()
    docs, structure = _validate(root, catalog)
    model = catalog.get('storyboardStructure')
    _require(model and [f['key'] for f in model.get('fields', [])] == list(FIELD_KEYS),
             'The shared storyboard definitions must already be registered')
    project = next((p for p in catalog['projects'] if p['id'] == PROJECT_ID), None)
    _require(project and project.get('controllerID') == 'baldadoon', 'Apply the Baldadoon project intake first')
    assets = catalog['assets']
    for doc in docs:
        assets = _append_record(assets, doc)
    writer_project = next((p for p in catalog.get('writerDevelopment', {}).get('projects', [])
                           if p.get('id') == PROJECT_ID), None)
    writer_document_ids = list(dict.fromkeys(
        document_id
        for group in (writer_project or {}).get('groups', []) if group.get('storyboard')
        for document_id in group.get('documentIDs', [])
    ))
    available_ids = {asset['id'] for asset in assets}
    _require(all(document_id in available_ids for document_id in writer_document_ids),
             'The Criminal Mind writer-development documents must be registered before storyboard linking')
    album = dict(id=PROJECT_ID + ':preliminary-storyboard', project=PROJECT_ID, category='documents',
                 title='The Criminal Mind · Preliminary storyboard writing',
                 description='165 proposed coverage shots; source integrity checks are separate from human acceptance.',
                 assetIDs=[a['id'] for a in docs], related=[])
    story = dict(id=STORY_ID, project=PROJECT_ID, title='The Criminal Mind', kind='sequence',
                 sequenceID=SEQUENCE_ID, stage='preliminary', group='Stories',
                 author='CFA Nova', originalAuthor='Baldadoon', reviewControllerID='baldadoon',
                 documentIDs=['TCM-SCRIPT-TEXT', 'TCM-FIRST-READ', *album['assetIDs'], *writer_document_ids],
                 description=structure['note'])
    sequence = dict(id=SEQUENCE_ID, project=PROJECT_ID, title='The Criminal Mind', stage='preliminary',
                    author='CFA Nova', originalAuthor='Baldadoon', reviewControllerID='baldadoon',
                    description=structure['note'], assetIDs=[], sourceAlbumIDs=[],
                    sections=deepcopy(structure['sections']), sourceDocuments=[structure['source'], _evidence(docs[1])],
                    shots=[dict(shotID=s['shotID'], sectionID=s['sectionID'], label=s['label'], title=s['title'],
                                line=s['summary'], stage='preliminary', materials=[],
                                pendingReferences=list(dict.fromkeys(s.get('missingArtReported', []) + s.get('unresolvedReferences', []))),
                                sourceBlockID=s['sourceBlockID'], source=s['source'],
                                sourceLineStart=s['sourceLineStart'], sourceLineEnd=s['sourceLineEnd'])
                           for s in structure['shots']])
    updates = {
        'assets': assets,
        'albums': _append_record(catalog['albums'], album),
        'storyboardStories': _append_record(catalog.get('storyboardStories', []), story),
        'storyboardSequences': _append_record(catalog.get('storyboardSequences', []), sequence),
        'storyboardStructure': {**model, 'stories': _append_record(model.get('stories', []), structure, 'storyID')},
    }
    metadata = deepcopy(catalog.get('storyboardMetadata', {}))
    _require(isinstance(metadata, dict), 'Unexpected storyboard metadata shape')
    metadata.setdefault(PROJECT_ID, {}).update(
        timingStatus='165 Preliminary coverage shots are proposed across 41 source groups. Dialogue timing, clip segmentation and runtime remain unmeasured.',
        positionBasis='authored_coverage_order', panelCount=0, independentSequenceCount=1,
        sourceBlockCount=41, authoredShotCount=165, stage='preliminary')
    projects = list(catalog['projects'])
    projects[projects.index(project)] = {**project, 'landing': {**project.get('landing', {}),
        'authoredShotCount': 165, 'storyID': STORY_ID,
    }}
    updates.update(projects=projects, storyboardMetadata=metadata)
    catalog.update(updates)
    return catalog
