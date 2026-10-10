"""Build a candidate-only ledger from verified local Grok benchmark/VIS intake.

No source mutation, provider code execution, catalog rebuild or user approval.
"""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import csv
import hashlib
import io
import json
import os

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'AGENTS.md').is_file())
CATALOG = ROOT / 'docs/notes/explorable_world/comfy/projects/visual_library/catalog.js'
BENCH = 'NOVA-IMG-BENCH-20261009/'
VIS = 'GROK-HD-20261009_VIS-HD_v001/'


def io_path(path):
    value = str(Path(path).absolute())
    if os.name == 'nt' and not value.startswith('\\\\?\\'):
        value = '\\\\?\\UNC\\' + value[2:] if value.startswith('\\\\') else '\\\\?\\' + value
    return Path(value)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(io_path(path).read_text(encoding='utf-8-sig'))


def main():
    receipt_path = HERE / 'received/intake_receipt.json'
    receipt = read(receipt_path)
    assert receipt['state'] == 'verified_hash_size_decode_complete_extracted_batch'
    assert receipt['package_completeness']['complete']
    catalog_raw = CATALOG.read_bytes()
    catalog = json.loads(catalog_raw.decode('utf-8-sig').split('=', 1)[1].strip().rstrip(';'))
    destination = HERE / 'asset_ledger.json'
    owned_ids = {a['id'] for a in read(destination)['assets']} if destination.exists() else set()
    existing_sha, existing_paths = {}, {}
    for a in catalog['assets']:
        if a['id'] in owned_ids:
            continue
        if a.get('sha256'):
            existing_sha.setdefault(a['sha256'], []).append(a)
        if a.get('repoPath'):
            existing_paths.setdefault(a['repoPath'].replace('\\', '/'), []).append(a)
    by_member = {r['member']: r for r in receipt['occurrences']}

    def bytes_for(member):
        return io_path(ROOT / by_member[member]['canonical_path']).read_bytes()

    def csv_rows(member):
        return list(csv.DictReader(io.StringIO(bytes_for(member).decode('utf-8-sig'))))

    refs = csv_rows(BENCH + 'refs/refs_manifest.csv')
    baselines = csv_rows(BENCH + 'BASELINES/baselines_manifest.csv')
    tests = json.loads(bytes_for(BENCH + 'COMPARE/tests.json'))
    vis = json.loads(bytes_for(VIS + 'manifest.json'))
    ref_rows = {}
    baseline_rows = {}
    for row in refs:
        ref_rows.setdefault(row['sha256'], []).append(row)
    for row in baselines:
        baseline_rows.setdefault(row['kit_file_sha256'], []).append(row)
    vis_rows = {r['sha256']: r for r in vis['deliverables'] + vis['rejected']}
    rejected_sha = {r['sha256'] for r in vis['rejected']}
    albums = [
        {'id': 'hon:image-benchmark-review', 'project': 'hon', 'category': 'review', 'title': 'Image benchmark · historical targets and crops',
         'description': 'Derived comparison images and an identity crop. Historical targets do not count as matched new Grok runs; no new character or outfit approvals.', 'related': []},
        {'id': 'hon:mouth-continuity-candidates', 'project': 'hon', 'category': 'comfy', 'title': 'Mouth continuity · candidates',
         'description': 'Twelve mouth-shape candidates and their contact sheet for continuity review. F/V remains unresolved; this is not a completed lip-sync workflow or approved mouth model.', 'related': []},
        {'id': 'hon:mouth-continuity-rejected', 'project': 'hon', 'category': 'review', 'title': 'Mouth continuity · rejected attempts',
         'description': 'Five attempts rejected by Grok, retained for comparison and defect tracking.', 'related': []},
    ]
    assets, documents, mappings, omitted = [], [], [], []
    crop_sha = '89000d0149bef4f8d846500d0e111c9bde5e03bdd3be5ad4650b074799cc20a5'
    face_sha = 'ef5d59a6402eaff568e30bb6a4432b14b90c692ea6758a761c7702c44d457978'

    def new_id(sha, is_vis=False):
        return ('HD-VIS-' if is_vis else 'IMG-BENCH-') + sha[:12]

    def image_ids(sha):
        matches = existing_sha.get(sha, [])
        if matches:
            return [a['id'] for a in matches]
        f = next((r for r in receipt['unique_files'] if r['sha256'] == sha and r['kind'] == 'image'), None)
        if f:
            return [new_id(sha, any(receipt['occurrences'][i]['member'].startswith(VIS) for i in f['occurrence_indices']))]
        return []

    for f in receipt['unique_files']:
        raw = io_path(ROOT / f['canonical_path']).read_bytes()
        assert len(raw) == f['bytes'] and digest(raw) == f['sha256'], f['canonical_path']
        occurrences = [receipt['occurrences'][i] for i in f['occurrence_indices']]
        sha, name = f['sha256'], f['original_filename']
        aliases = [{'source_path': o['source_path'], 'source_folder': o['source_folder'], 'member': o['member'],
                    'archive_aliases': o.get('verified_archive_aliases', [])} for o in occurrences]
        is_vis = any(o['member'].startswith(VIS) for o in occurrences)
        role_records = ref_rows.get(sha, [])
        historical_records = baseline_rows.get(sha, [])
        projects = {'lisan' if row['test_id'].startswith('LAG-') else 'hon' for row in role_records + historical_records}
        if not projects:
            projects = {'lisan'} if '/LAG-01/' in occurrences[0]['member'] or name.startswith('LAG-01_') else {'hon'}
        match_assets = existing_sha.get(sha, []) if f['kind'] == 'image' else existing_paths.get(f['canonical_path'], [])
        canonical_ids = [a['id'] for a in match_assets]
        mapping = {'sha256': sha, 'bytes': f['bytes'], 'kind': f['kind'], 'canonical_path': f['canonical_path'],
                   'original_filename': name, 'canonical_asset_ids': canonical_ids, 'projects': sorted(projects),
                   'sourceAliases': aliases, 'referenceRoles': role_records, 'historicalBaselineRecords': historical_records,
                   'new_card': False, 'new_approval': False}
        if f['kind'] != 'image':
            ext = Path(f['canonical_path']).suffix.lower()
            if ext not in {'.txt', '.md', '.json', '.csv', '.pdf'}:
                omitted.append({'path': f['canonical_path'], 'reason': 'Retained native file; unsupported document preview extension.', 'sha256': sha})
            elif not match_assets:
                project = sorted(projects)[0]
                title = name + (' · mouth continuity return' if is_vis else ' · image benchmark source')
                if f['kind'] == 'helper_text':
                    title = name + ' · inert source text (not executed)'
                documents.append({'project': project, 'path': f['canonical_path'], 'title': title,
                                  'album': 'Mouth continuity · source records' if is_vis else 'Image benchmark · source records',
                                  'sha256': sha, 'bytes': f['bytes'], 'inert': f['kind'] == 'helper_text', 'sourceAliases': aliases})
                mapping['canonical_asset_ids'] = [project + ':doc:' + f['canonical_path']]
                mapping['new_card'] = True
            mappings.append(mapping)
            continue
        if match_assets:
            mappings.append(mapping)
            continue

        project = 'lisan' if projects == {'lisan'} else 'hon'
        group = 'hon:image-benchmark-review'
        category = 'review'
        title = name
        source_ids = []
        notes = ['Verified received bytes; not approved.']
        extra = {'userApproved': False, 'acceptance': 'not_accepted', 'workflowStage': 'preliminary',
                 'candidateState': 'needs_user_review'}
        if historical_records:
            cases = list(dict.fromkeys(r['test_id'] for r in historical_records))
            title = ' / '.join(cases) + ' · historical target (JPEG derivative)'
            for row in historical_records:
                source_ids.extend(image_ids(row['original_sha256']))
                notes.extend(['Grok-reported: ' + row['note'], 'Conversion: ' + row['conversion'] + '.'])
            notes.append('Existing artwork used as a comparison target. Not a fresh same-prompt Grok generation; compare native originals separately before judging detail fidelity.')
            extra.update(referenceRole='historical_comparison_target_derivative', testIDs=cases,
                         baselineLineage=historical_records)
        elif sha == crop_sha:
            title = 'Dolo · face and neck detail crop'
            source_ids = image_ids(face_sha)
            notes.append('Provider-supplied identity detail crop for ordered benchmark attachments. Crop ancestry is reported; no new identity approval. Nose-hoop wording conflicts with the depicted identity and needs reconciliation before the still-image test.')
            extra.update(referenceRole='identity_detail_crop', testIDs=['HD-01', 'HD-02', 'HD-03', 'HD-04'])
        if is_vis:
            source_ids = image_ids(crop_sha)
            row = vis_rows.get(sha)
            notes = ['Verified received bytes; mouth-shape candidate remains unaccepted.']
            notes.append('Provider lock calls the upper canines fangs; current CFA benchmark calls for modest gold canine caps. Do not promote provider wording into a new character standard.')
            extra.update(referenceRole='mouth_shape_candidate', providerCharacterLock=vis['character_lock'],
                         nativeLipSyncTested=False, motionPreservationTested=False)
            if sha in rejected_sha:
                category, group = 'review', 'hon:mouth-continuity-rejected'
                title = row['label'] + ' · rejected attempt'
                notes.append('Grok-reported rejection: ' + row['reason'])
                extra.update(candidateState='provider_rejected', providerQA=row, relatedViseme=row['related_viseme'])
            elif row:
                category, group = 'comfy', 'hon:mouth-continuity-candidates'
                title = 'Mouth ' + row['id'] + ' · ' + row['shape']
                notes.append('Grok-reported QA: ' + row['qa_note'])
                notes.append('Independent visual review pending; a still does not demonstrate transitions or audio synchronization.')
                extra.update(providerQA=row, visemeID=row['id'], phonemes=row['phonemes'])
            else:
                category, group = 'comfy', 'hon:mouth-continuity-candidates'
                title = 'Mouth continuity · contact sheet'
                notes.append('Provider summary of 12 candidates; original individual files determine inspection detail. F/V is reported unresolved.')
                extra.update(referenceRole='mouth_shape_contact_sheet')
        asset_id = new_id(sha, is_vis)
        mapping['canonical_asset_ids'] = [asset_id]
        mapping['new_card'] = True
        mappings.append(mapping)
        assets.append({'id': asset_id, 'project': project, 'path': f['canonical_path'], 'originalFilename': name,
                       'title': title, 'category': category, 'album': group, 'sha256': sha, 'bytes': f['bytes'],
                       'width': f['image']['width'], 'height': f['image']['height'], 'mode': f['image']['mode'],
                       'sourceIntake': receipt['intakeID'], 'sourceStatus': 'Verified received candidate; not approved',
                       'sourceAssetIDs': list(dict.fromkeys(source_ids)), 'sourceAliases': aliases,
                       'providerRecords': [vis_rows[sha]] if sha in vis_rows else historical_records,
                       'note': ' '.join(dict.fromkeys(notes)), 'tags': ['Grok return 20261009', name, 'unaccepted'] + list(dict.fromkeys(source_ids)),
                       **extra})

    prompt_cards = []
    for test in tests:
        prompt = by_member[BENCH + 'PROMPTS/' + test['id'] + '_PROMPT.txt']
        uploads = []
        for order, member in enumerate(test['uploads'], 1):
            row = by_member[BENCH + member]
            role = next(r for r in refs if r['test_id'] == test['id'] and r['kit_file'] == member)
            uploads.append({'order': order, 'member': row['member'], 'canonical_path': row['canonical_path'],
                            'sha256': row['sha256'], 'asset_ids': image_ids(row['sha256']), 'role': role['role']})
        contexts = []
        for role in refs:
            if role['test_id'] == test['id'] and role['kind'] == 'CONTEXT_ONLY':
                row = by_member[BENCH + role['kit_file']]
                contexts.append({'member': row['member'], 'canonical_path': row['canonical_path'], 'sha256': row['sha256'],
                                 'role': role['role'], 'upload': False})
        prompt_cards.append({'testID': test['id'], 'project': 'lisan' if test['id'].startswith('LAG-') else 'hon',
                             'subject': test['subject'], 'promptPath': prompt['canonical_path'], 'promptSHA256': prompt['sha256'],
                             'promptStatus': 'raw_provider_proposal_not_executed', 'uploads': uploads, 'contextOnly': contexts})

    conflicts = [
        {'id': 'HD-NOSTRIL-AUTHORITY', 'tests': ['HD-01', 'HD-02', 'HD-03', 'HD-04'], 'status': 'needs_reconciliation',
         'detail': 'Benchmark text requests two character-right nostril hoops; identity image/package caveat and VIS text use one each side. Preserve raw sources and reconcile one target for all lanes before generation.'},
        {'id': 'LAG-OLD-FACE-SCOPE', 'tests': ['LAG-01'], 'status': 'needs_local_prompt_revision',
         'detail': 'Raw card supplies historical iced-grill face as neck/piercing authority. CFA reference map reserves it for explicitly requested mouth/grill only; FACE-NATURAL remains current identity and natural teeth default.'},
        {'id': 'BOSS-009-OPTION-B', 'tests': ['BOSS-009'], 'status': 'preserved_attributed_difference',
         'detail': 'Provider asks to reproduce option B shown on the proof; original brief requested A. This is a fidelity target proposal, not user approval of B or the unclear missing arm.'},
        {'id': 'PROBE-01-SUBSTITUTE', 'tests': ['PROBE-01'], 'status': 'original_refusal_source_unverified',
         'detail': 'REF-lord-source.jpg is supplied as an image_25 equivalent; exact relationship to the previously refused upload has not been established.'},
        {'id': 'HISTORICAL-BASELINE-FAIRNESS', 'tests': [t['id'] for t in tests], 'status': 'comparison_scope_required',
         'detail': 'Historical Grok targets have different prompts/attempt histories; boss targets equal the reference image. Fresh matched runs are needed for generator ranking. Current files support historical-image improvement checks.'},
        {'id': 'VIS-FV-AND-LOCK', 'tests': ['VIS-HD'], 'status': 'visual_review_pending',
         'detail': 'F/V is provider-reported unresolved; 02/05/07/08/10 have reported ring/shape issues. Provider canine-fang wording is not a new CFA approval; no motion or lip-sync result is established.'},
    ]
    summary = {'new_image_cards': len(assets), 'new_image_categories': dict(Counter(a['category'] for a in assets)),
               'new_document_cards': len(documents), 'existing_image_hashes_reused': sum(m['kind'] == 'image' and not m['new_card'] for m in mappings),
               'source_mappings': len(mappings), 'raw_prompt_cards': len(prompt_cards), 'unsupported_previews_retained': len(omitted)}
    ledger = {'schema': 'grok-return-catalog-v1', 'intakeID': receipt['intakeID'],
              'receiptPath': receipt_path.relative_to(ROOT).as_posix(), 'receiptSHA256': digest(receipt_path.read_bytes()),
              'catalogSnapshot': {'path': CATALOG.relative_to(ROOT).as_posix(), 'sha256': digest(catalog_raw)},
              'recordedAtUTC': datetime.now(timezone.utc).isoformat(),
              'approval': 'Technical verification creates no user approval. Provider locks, QA and planned attempts remain attributed claims.',
              'albums': albums, 'assets': assets, 'documents': documents, 'sourceMappings': mappings,
              'promptCards': prompt_cards, 'conflicts': conflicts, 'retainedWithoutPreview': omitted,
              'providerCodeExecuted': False, 'generationPerformed': False, 'summary': summary}
    temporary = HERE / 'asset_ledger.next.json'
    temporary.write_text(json.dumps(ledger, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(destination)
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
