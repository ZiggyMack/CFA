"""Register the received screenplay without manufacturing media or accepted shots."""
import hashlib
import json
import os
from pathlib import Path
from urllib.parse import quote


PROJECT_ID = 'criminal_mind'
CONTROLLER_ID = 'baldadoon'
ORIGINAL_SHA = '5aabf6e669b7c0c402fe9b3cd80bfb2d4f65e661fcd16b2b7bd97ad4467f9b81'
INTAKE = Path('docs/notes/explorable_world/comfy/projects/the_criminal_mind/source_intake_20261030')
DOCUMENTS = (
    ('TCM-ORIGINAL-DOC', 'The Criminal Mind (final).doc', 'Original screenplay · Word DOC'),
    ('TCM-SCRIPT-TEXT', 'SCRIPT_TEXT.txt', 'The Criminal Mind · readable screenplay'),
    ('TCM-FIRST-READ', 'FIRST_READ.txt', 'Preliminary adaptation notes · CFA Nova'),
    ('TCM-SOURCE-INVENTORY', 'SOURCE_SCENE_INVENTORY.json', '41 source heading blocks · inventory'),
    ('TCM-SCRIPT-LINE-MAP', 'SCRIPT_LINE_MAP.txt', 'Screenplay line map'),
)


def apply_criminal_mind_intake(catalog, root):
    root = Path(root).resolve()
    source = root / INTAKE
    here = root / 'docs/notes/explorable_world/comfy/projects/visual_library'
    original = (source / DOCUMENTS[0][1]).read_bytes()
    if len(original) != 208896 or hashlib.sha256(original).hexdigest() != ORIGINAL_SHA:
        raise ValueError('The Criminal Mind original no longer matches received bytes')
    script = (source / 'SCRIPT_TEXT.txt').read_text(encoding='utf-8-sig')
    inventory = json.loads((source / 'SOURCE_SCENE_INVENTORY.json').read_text(encoding='utf-8-sig'))
    if len(inventory) != 41 or '\ufffd' in script:
        raise ValueError('Unexpected screenplay source inventory or extraction')
    lines = script.splitlines()
    blocks = []
    for item in inventory:
        start, end = item['line_start'], item['line_end_inclusive']
        if not 1 <= start <= end <= len(lines):
            raise ValueError('Invalid source block line range')
        text = '\n'.join(lines[start - 1:end])
        if hashlib.sha256(text.encode('utf-8')).hexdigest() != item['text_sha256']:
            raise ValueError('Source block text no longer matches its intake hash')
        if lines[start - 1].strip() != item['source_heading_verbatim'].strip():
            raise ValueError('Source heading no longer matches its line range')
        blocks.append({'id': item['source_block_id'], 'heading': item['source_heading_verbatim'],
                       'lineStart': start, 'lineEnd': end, 'text': text,
                       'sourceTextSHA256': item['text_sha256'],
                       'containsUnheadedFlashback': item['contains_unheaded_flashback_and_return']})
    ids = {a['id'] for a in catalog['assets']}
    if ids.intersection(row[0] for row in DOCUMENTS):
        raise ValueError('The Criminal Mind intake must be applied once')
    album_id = PROJECT_ID + ':source-script'
    for asset_id, filename, title in DOCUMENTS:
        path = source / filename
        raw = path.read_bytes()
        binary = filename.endswith('.doc')
        catalog['assets'].append({
            'id': asset_id, 'project': PROJECT_ID, 'title': title, 'filename': filename,
            'kind': 'document', 'category': 'documents', 'album': album_id,
            'src': quote(os.path.relpath(path, here).replace('\\', '/'), safe='/'),
            'repoPath': path.relative_to(root).as_posix(), 'sha256': hashlib.sha256(raw).hexdigest(),
            'bytes': len(raw), 'text': '' if binary else raw.decode('utf-8-sig'),
            'downloadOnly': binary, 'inert': not binary, 'controllerID': CONTROLLER_ID,
            'sourceIntake': 'TCM-SCRIPT-20261030',
            'sourceStatus': 'Preliminary adaptation proposal' if asset_id == 'TCM-FIRST-READ' else 'Received screenplay source',
            'note': 'Original screenplay by Baldadoon. Source intake does not record adaptation or production acceptance.'
        })
    catalog['albums'].append({'id': album_id, 'project': PROJECT_ID, 'category': 'documents',
                              'title': 'The Criminal Mind · script and development',
                              'description': 'Received source and Preliminary adaptation notes.',
                              'assetIDs': [row[0] for row in DOCUMENTS], 'related': []})
    project = {'id': PROJECT_ID, 'name': 'Baldadoon', 'subtitle': 'The Criminal Mind',
               'controllerID': CONTROLLER_ID, 'defaultView': 'all',
               'landing': {
                   'title': 'The Criminal Mind', 'author': 'Baldadoon', 'stage': 'Preliminary',
                   'description': 'The screenplay is received and readable. The full-script, one-film scope is settled; visual development and proof work remain Preliminary.',
                   'scriptAssetID': 'TCM-SCRIPT-TEXT', 'originalAssetID': 'TCM-ORIGINAL-DOC',
                   'notesAssetID': 'TCM-FIRST-READ', 'inventoryAssetID': 'TCM-SOURCE-INVENTORY',
                   'lineMapAssetID': 'TCM-SCRIPT-LINE-MAP', 'sourceBlockCount': len(blocks), 'sourceBlocks': blocks,
                   'nextStep': 'Review the current writer decisions, author interview, casting candidates and set-camera collections. Open author items A and Q wait for their proofs; the unmarked SUV remains a writer assumption under review.',
                   'emptyMedia': 'This source intake records no accepted character, set, shot, starting frame, generated video or take. Verified review candidates are appended separately without changing that acceptance state.',
                   'runtimeSeconds': None,
               }}
    for existing in catalog['projects']:
        if existing['id'] in {'hon', 'lisan'}:
            existing.setdefault('controllerID', 'ziggy')
    index = next((n for n, p in enumerate(catalog['projects']) if p['id'] == 'unassigned'), len(catalog['projects']))
    catalog['projects'].insert(index, project)
    catalog['humanControllers'] = [
        {'id': 'ziggy', 'name': 'Ziggy', 'homeLabel': "Ziggy’s Corner"},
        {'id': CONTROLLER_ID, 'name': 'Baldadoon', 'homeLabel': 'Casa Baldadoon'},
    ]
    catalog.setdefault('storyboardMetadata', {})[PROJECT_ID] = {
        'timingStatus': 'Source screenplay received; no authored storyboard shots or measured runtime yet.',
        'positionBasis': 'source_heading_blocks', 'panelCount': 0, 'independentSequenceCount': 0,
        'sourceBlockCount': len(blocks),
    }
    task = {
        'id': 'tcm-adaptation-scope-20261030', 'project': PROJECT_ID, 'provider': 'CFA Nova',
        'title': 'The Criminal Mind · adaptation decisions and author interview', 'priority': 'normal',
        'status': 'in_progress', 'statusLabel': 'Scope closed · proof-dependent questions remain',
        'direction': 'inbound', 'workKind': 'planning',
        'ownerControllerID': CONTROLLER_ID, 'assigneeControllerID': CONTROLLER_ID,
        'decisionAuthorityControllerID': CONTROLLER_ID, 'decisionScope': 'project_decision',
        'summary': 'Scope is closed: Baldadoon’s whole screenplay is being developed as one film. Relayed decisions establish present day with smartphones, Massachusetts State Police with the FBI agents as written, Johnny firing at 1471, and the ammonia line as deliberate. Ziggy’s production rule is to hold to the source as written and use a labelled placeholder when a provider refuses or a difficult shot is deferred. The writer’s decisions record relays Henderson exterior L03 as the house geometry, while the site evidence recovers only a favorite/basket signal with no attributed saved review. The 165 coverage shots remain Preliminary; no cast member, shot, starting frame or finished output is selected or accepted.',
        'nextAction': 'Expose only verified writer records and verified, ingested candidates. Baldadoon can review the provisional SUV and, when the proofs exist, answer A and Q. This card authorizes no generation.',
        'missingLabel': 'Open author decisions and provisional review',
        'missing': [
            'A · Whether anyone besides John can perceive the phone remains open; it waits for the scene 3 proof.',
            'Q · Whether Jack and Johnny appear through the body or as inner voices remains open; it waits for the relevant state/reflection proof.',
            'S · The present-day unmarked SUV is a writer assumption under author review, not a selected vehicle image.',
        ],
        'laterReview': 'L03 is a provisional house-geometry signal pending an attributed saved review. Car, casting and other set decisions remain separate; none accepts a shot, starting frame or video.',
        'links': [{'label': label, 'assetID': asset_id} for label, asset_id in [
            ('Read the screenplay', 'TCM-SCRIPT-TEXT'), ('Read Preliminary adaptation notes', 'TCM-FIRST-READ'),
            ('Browse source heading blocks', 'TCM-SOURCE-INVENTORY'),
            ('Read current writer decisions', 'criminal_mind:doc:docs/notes/explorable_world/comfy/projects/the_criminal_mind/story/writer_pass_20261031/TCM_DECISIONS_20261031.md'),
            ('Read author interview status', 'criminal_mind:doc:docs/notes/explorable_world/comfy/projects/the_criminal_mind/story/writer_pass_20261031/BALDADOON_AUTHOR_INTERVIEW_20261101.json'),
            ('Open writer-folder index', 'criminal_mind:doc:docs/notes/explorable_world/comfy/projects/the_criminal_mind/story/writer_pass_20261031/START_HERE.txt'),
            ('Read initial writer pass', 'criminal_mind:doc:docs/notes/explorable_world/comfy/projects/the_criminal_mind/story/writer_pass_20261031/TCM_WRITER_PASS_001_20261031.md')]],
        'previewAssetIDs': [], 'externalExecution': False, 'generationAuthorizedByThisCard': False,
        'authorship': 'coordinator_summary', 'writtenBy': 'CFA Nova', 'requestedBy': 'Ziggy',
    }
    catalog.setdefault('missionControl', {}).setdefault('tasks', []).append(task)
    return catalog
