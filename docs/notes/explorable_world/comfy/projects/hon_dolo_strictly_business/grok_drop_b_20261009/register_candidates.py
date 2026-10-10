"""Register received B candidates through the existing Hon reference registry.

No catalog rebuild, source cleanup, external action or approval. Preserves prior
registry entries and keeps the head-state coverage separate from mouth macros.
"""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
import csv
import hashlib
import io
import json
import re

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'AGENTS.md').is_file())
PROJECTS = HERE.parent.parent
INTAKE = 'GROK-HD-DROP-20261009B'


def read(p):
    return json.loads(p.read_text(encoding='utf-8-sig'))


def write(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def rel(p):
    return p.relative_to(ROOT).as_posix()


def main():
    receipt_path = HERE / 'received/intake_receipt.json'
    receipt = read(receipt_path)
    assert receipt['state'] == 'available_files_verified_outer_package_incomplete'
    reg_path = HERE.parent / 'reference_updates/registry.json'
    reg = read(reg_path)
    if any(a.get('sourceIntake') == INTAKE for a in reg['assets']):
        raise ValueError('B assets already registered; inspect before repeating.')
    catalog_raw = (PROJECTS / 'visual_library/catalog.js').read_text(encoding='utf-8-sig')
    catalog = json.loads(catalog_raw.split('=', 1)[1].strip().rstrip(';'))
    by_sha = {}
    for a in catalog['assets'] + reg['assets']:
        if a.get('sha256'):
            by_sha.setdefault(a['sha256'], []).append(a)
    files = {f['sha256']: f for f in receipt['unique_files']}
    occurrences = receipt['occurrences']
    def data(member):
        o = next(o for o in occurrences if o['member'] == member)
        return (ROOT / o['canonical_path']).read_bytes()
    v3 = json.loads(data('GROK-HD-20261009_VIS-HD_v003/manifest.json'))
    mouth = {r['sha256']: r for r in v3['items']}
    proposed_keys = [1,2,3,4,5,6,7,8,9,10,11,12,13,19,21,25,27,29,34,43]
    sampled_notes = {
        'VIS-HD-01': 'Contact-sheet review: four gold upper caps visible; REST is slightly open with teeth showing.',
        'VIS-HD-02': 'Contact-sheet review: lips closed, so dental pattern is occluded rather than verified.',
        'VIS-HD-03': 'Contact-sheet review: four gold caps flank two natural central incisors; silver lower grill visible. Mouth-only scope.',
        'VIS-HD-06': 'Contact-sheet review: pursed lips hide most teeth; dental geometry is not verified while occluded.',
        'VIS-HD-14': 'Contact-sheet review shows a smoke-like wisp at the opening; confirm whether that is intended for BLOW-KISS.',
        'VIS-HD-16': 'Individual full-image review confirms silver upper caps where four gold should be, with no upper-lip bite achieved. Failed preservation/articulation candidate.',
        'VIS-HD-18': 'Contact-sheet review: lips look closed rather than rolled inward.',
        'VIS-HD-43': 'Contact-sheet review: open pose is substantially symmetric; does not establish mid-word motion.',
        'VIS-HD-46': 'Individual full-image review confirms visible natural side teeth without the expected gold pattern. Hidden lower row cannot be assessed.',
        'VIS-HD-47': 'Contact-sheet review: chain lies across the open mouth; actual tooth contact/bite needs closer inspection.',
        'VIS-HD-48': 'Contact-sheet review: nose hoop on one side lies at the crop edge. Minor nose variation alone does not trigger a reroll under current user tolerance.'}
    defs = [
        ('hon:mouth-v003-candidates', 'comfy', 'Mouth library v003 · 50 candidates', 'Four-gold base, external grill off. Provider shape labels are not approvals; known failed poses remain flagged. These macros do not count as head-library slots.'),
        ('hon:mouth-v003-sheets', 'comfy', 'Mouth library v003 · overview sheets', 'Nine provider contact sheets for navigation. Individual files govern detail review.'),
        ('hon:head-anchor-b-candidates', 'comfy', 'Head anchors · returned drafts', 'One character with optional external iced grill; no new head anchor is accepted and no 130-state head batch has arrived.'),
        ('hon:mouth-b-archive', 'review', 'Mouth and head archive · B drop', 'Superseded mouth sets, rejected attempts and rejected head drafts. Retained as evidence; not production references.'),
        ('hon:outfit-inventory-b', 'review', 'Outfit inventory · contact sheets', 'Provider inventory of existing looks. These sheets do not create duplicate outfits or approve the proposed 35-look regrill.')]
    albums = [{'id': aid, 'project': 'hon', 'category': category, 'title': title, 'description': desc, 'related': []} for aid,category,title,desc in defs]
    new_assets, documents, mappings = [], [], []
    for f in receipt['unique_files']:
        raw = (ROOT / f['canonical_path']).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == f['sha256'] and len(raw) == f['bytes']
        aliases = [occurrences[i] for i in f['occurrence_indices']]
        matched = by_sha.get(f['sha256'], [])
        mapping = {'sha256': f['sha256'], 'canonical_path': f['canonical_path'], 'kind': f['kind'],
                   'assetIDs': list(dict.fromkeys(a['id'] for a in matched)), 'sourceAliases': aliases, 'newCard': False}
        if matched or f['storage'] == 'existing_canonical':
            if not mapping['assetIDs'] and f.get('canonical_media_id'):
                mapping['assetIDs'] = [f['canonical_media_id']]
            mappings.append(mapping)
            continue
        name = f['original_filename']
        members = [a['member'] for a in aliases]
        if f['kind'] != 'image':
            if Path(name).suffix.lower() in {'.csv','.txt','.md','.json','.pdf'}:
                document = {'project': 'hon', 'path': f['canonical_path'], 'title': name + ' · B return source', 'album': 'Grok B drop · source records'}
                documents.append(document)
                mapping.update(assetIDs=['hon:doc:' + f['canonical_path']], newCard=True)
            mappings.append(mapping)
            continue
        aid = 'HD-B-' + f['sha256'][:12]
        category, album = 'review', 'hon:mouth-b-archive'
        title, role = name, 'historical_candidate'
        notes = ['Received file verified by SHA-256, size and complete image decode; not approved.']
        provider = [a['providerIndex'] for a in aliases if a.get('providerIndex')]
        extra = {'characterID': 'HON-DOLO', 'userApproved': False, 'acceptance': 'not_accepted',
                 'workflowStage': 'preliminary', 'candidateState': 'needs_user_review', 'visualReviewScope': 'not_individually_reviewed',
                 'motionPreservationTested': False, 'nativeLipSyncTested': False}
        if f['sha256'] in mouth:
            row = mouth[f['sha256']]
            category, album = 'comfy', 'hon:mouth-v003-candidates'
            title = row['id'] + ' · ' + row['shape'].replace('-', ' ').title() + ' · v003'
            role = 'mouth_macro_candidate'
            provider.append(row)
            notes += ['Provider QA: ' + row['qa_note'], 'Scope is mouth articulation and dental detail only; no face, tattoo, wardrobe or moving-mouth approval.']
            extra.update(visemeID=row['id'], mouthStateID=row['id'], mouthStateLabel=row['shape'], headRevision=None,
                         grillState='external_off', proposedKeyState=int(row['id'].split('-')[-1]) in proposed_keys,
                         keyStateAccepted=False, countedInHeadCoverage=False)
            if row['id'] in sampled_notes:
                notes.append(sampled_notes[row['id']])
                extra['visualReviewScope'] = 'individual_static_image' if row['id'] in {'VIS-HD-16','VIS-HD-46'} else 'provider_contact_sheet_sample'
            if row['id'] in {'VIS-HD-16','VIS-HD-46'}:
                extra['candidateState'] = 'known_defect_needs_correction'
        elif 'v003_SHEET' in name:
            category, album, role = 'comfy', 'hon:mouth-v003-sheets', 'contact_sheet'
            title = 'Mouth v003 · sheet ' + re.search(r'SHEET_(\d+of9)', name).group(1).replace('of',' / ')
        elif any('/04_HEAD_ANCHORS/' in n for n in members):
            role = 'head_anchor_candidate'
            notes += [r['what'] for r in provider]
            if '_REJECTED_' in name:
                extra['candidateState'] = 'provider_rejected'
            else:
                category, album = 'comfy', 'hon:head-anchor-b-candidates'
                extra.update(grillState='external_iced_on', countedInHeadCoverage=False)
            if 'HEAD-r5_' in name:
                extra['visualReviewScope'] = 'individual_static_image'
                notes.append('Viewed image: external upper grill extends beyond the base four-gold pattern; use only as optional iced-direction draft. Not the external_off dental master.')
        elif any('/03_GRILL_REF/' in n for n in members):
            category, album, role = 'comfy', 'hon:mouth-v003-candidates', 'mouth_dental_reference_candidate'
            notes += [r['what'] for r in provider]
            notes.append('Provider acceptance wording is retained as a claim; this intake grants no new image approval.')
            extra['grillState'] = 'external_off'
        elif any('/06_OUTFIT_INVENTORY/' in n for n in members):
            album, role = 'hon:outfit-inventory-b', 'outfit_inventory_contact_sheet'
            title = 'Outfit inventory · ' + Path(name).stem.replace('_',' ')
            notes.append('Navigation sheet only; reuse existing outfit parents and retain old identity/ink defects.')
        else:
            extra['candidateState'] = 'provider_rejected' if any('REJECTED' in n for n in members) else 'superseded'
            notes.append('Superseded/rejected provider material retained for traceability; v003 and current user instructions govern future candidates.')
        asset = {'id': aid, 'project': 'hon', 'path': f['canonical_path'], 'originalFilename': name,
                 'title': title, 'category': category, 'album': album, 'sha256': f['sha256'], 'bytes': f['bytes'],
                 'width': f['image']['width'], 'height': f['image']['height'], 'mode': f['image']['mode'],
                 'sourceIntake': INTAKE, 'sourceStatus': 'Verified received candidate; not approved', 'sourceAliases': aliases,
                 'providerRecords': provider, 'referenceRole': role, 'note': ' '.join(notes),
                 'tags': [INTAKE, name, 'unaccepted'], **extra}
        new_assets.append(asset)
        mapping.update(assetIDs=[aid], newCard=True)
        mappings.append(mapping)
    extras = [('START_HERE.txt','Grok B drop · receipt and missing files'),
              ('asset_ledger.json','Grok B drop · asset and source mapping'),
              ('coverage.json','Hon head library · received mouth coverage'),
              ('visual_review.json','Mouth v003 · bounded static review'),
              ('outfit_inventory_mapping.json','Outfit inventory · existing parent mapping')]
    documents += [{'project':'hon','path':rel(HERE/name),'title':title,'album':'Grok B drop · intake'} for name,title in extras]
    ledger = {'schema_version': 1, 'intakeID': INTAKE, 'receiptPath': rel(receipt_path),
              'receiptSHA256': hashlib.sha256(receipt_path.read_bytes()).hexdigest(),
              'assets': new_assets, 'albums': albums, 'documents': documents, 'mappings': mappings,
              'newApprovals': [], 'sourceCleanupPerformed': False}
    write(HERE/'asset_ledger.json', ledger)
    id_by_sha = {r['sha256']: r['assetIDs'] for r in mappings}
    coverage = {'intakeID': INTAKE, 'verifiedMouthMacros': [dict(r, assetIDs=id_by_sha[r['sha256']], grillState='external_off') for r in v3['items']],
                'proposedKeyStates': ['VIS-HD-'+str(i).zfill(2) for i in proposed_keys], 'keyStateSelectionAccepted': False,
                'receivedHeadLibrarySlots': 0, 'baselineExpectedPerGrillState': 130, 'pitchExpansionAdditionalPerState': 40,
                'receivedHeadAnchorCandidates': [a['id'] for a in new_assets if a['referenceRole']=='head_anchor_candidate'],
                'externalIcedMouthSetReceived': False, 'propMouthBatchReceived': False,
                'note': 'State labels supplied as provider proposals. Fifty mouth macros are not fifty front-view head slots; all 130 head slots remain unfilled.'}
    write(HERE/'coverage.json', coverage)
    write(HERE/'visual_review.json', {'scope':'Three provider contact sheets (1/9, 3/9, 8/9), individual v003 16 and 46, and head draft r5. Not a full 50-shape visual approval.',
          'sourceSHA256s':[f['sha256'] for f in receipt['unique_files'] if f['original_filename'] in [f'GROK-HD-20261009_VIS-HD_v003_SHEET_{i}of9.jpg' for i in [1,3,8]]],
          'sampledObservations':sampled_notes,'newApprovals':[], 'motionTested':False,
          'jewelryTolerance':'Current user tolerance allows minor nose/ear variations per shot; do not trigger a jewelry-only reroll. Mouth, grill, identity, brow and tattoo requirements remain.'})
    looks = list(csv.DictReader(io.StringIO(data(INTAKE+'/06_OUTFIT_INVENTORY/LOOKS.csv').decode('utf-8-sig'))))
    looks_map = []
    for r in looks:
        matches = by_sha.get(r['sha256'], [])
        tier = re.search(r'TIER ([ABC])',r['notes'])
        looks_map.append({**r,'providerTier':tier.group(1) if tier else None,
                          'existingAssetIDs':list(dict.fromkeys(a['id'] for a in matches)),
                          'existingOutfitAlbums':list(dict.fromkeys(a.get('album') for a in matches if a.get('category')=='outfits')),
                          'newOutfitCreated':False,'regrillApproved':False})
    write(HERE/'outfit_inventory_mapping.json',{'rows':looks_map,'counts':dict(Counter(r['providerTier'] for r in looks_map)),
          'note':'Provider inventory mapped by exact hash only. Old images remain wardrobe/context evidence, not new character approvals or new outfits.'})
    expected_path = HERE.parent/'head_library_20261009/expected_intake.json'
    expected = read(expected_path)
    expected['status']='mouth_v003_received_head_batch_not_received'
    expected['providerProgress'].update(verifiedLocalMouthShapes=50,verifiedLocalHeads=0,
        note='B intake verifies 50 external_off v003 macros. Seven anchor drafts/proposals/rejections are not head-state coverage. Four manifest references remain missing from the outer drop.')
    expected['coverage'].update(stateLabelsSupplied=True,keyStateSelectionSupplied=True,keyStateSelectionAccepted=False)
    expected['receivedMouthCoveragePath']=rel(HERE/'coverage.json')
    expected['receivedIntakePath']=rel(receipt_path)
    for slot in expected['plannedSlots']:
        if slot['plannedSlotID'].startswith('HD-HR1-FRONT-'):
            i=int(slot['plannedSlotID'].rsplit('-',1)[1])-1
            slot.update(stateID=v3['items'][i]['id'],stateLabel=v3['items'][i]['shape'],stateLabelAuthority='provider_proposal',status='head_not_received')
    expected['outfits']['providerReportedInventory'].update(verifiedLocally=True,verificationScope='70 inventory rows received; reference matches in outfit_inventory_mapping.json. No new outfit or regrill approval.')
    expected['headAnchorStatus']['receivedDraftAssetIDs']=coverage['receivedHeadAnchorCandidates']
    for state in expected['grillCollections']['states']:
        if state['grillState']=='external_off':
            state.update(status='50_v003_macros_received_heads_not_received',receivedMouthMacroAssetIDs=[id_by_sha[r['sha256']][0] for r in v3['items']])
        else:
            state['receivedAssetIDs']=[a['id'] for a in new_assets if a['referenceRole']=='head_anchor_candidate' and a.get('grillState')=='external_iced_on']
            state['status']='anchor_drafts_received_matched_mouth_and_head_sets_not_received'
    expected['updatedAtUTC']=datetime.now(timezone.utc).isoformat()
    write(expected_path,expected)
    reg['albums'] += albums
    reg['assets'] += new_assets
    reg['documents'] += documents
    reg['updatedAtUTC']=datetime.now(timezone.utc).isoformat()
    write(reg_path,reg)
    print(json.dumps({'newMediaCards':len(new_assets),'newDocuments':len(documents),'macroCandidates':len(mouth),
        'outfitTiers':dict(Counter(r['providerTier'] for r in looks_map)),
        'outfitRowsWithExactCatalogReference':sum(bool(r['existingAssetIDs']) for r in looks_map)},indent=2))


if __name__=='__main__':
    main()
