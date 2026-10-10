"""Register verified return bytes and candidate roles; never approve or execute them."""
from pathlib import Path
import hashlib
import json
import re
import shutil

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'AGENTS.md').is_file())
LIBRARY = HERE.parent.parent / 'visual_library'

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def main():
    receipt = read(HERE / 'received/intake_receipt.json')
    assert receipt['state'] == 'verified_crc_hash_size_decode'
    audit_path = HERE / 'hd_audit.json'
    if not audit_path.exists():
        audit_path = ROOT / '.cache/grok_hd_return_audit_20261009.json'
    audit = read(audit_path)
    catalog = json.loads((LIBRARY / 'catalog.js').read_text(encoding='utf-8').split('=', 1)[1].strip().rstrip(';'))
    old = {a['id']: a for a in catalog['assets']}
    albums = {}
    def album(key, category, title, description):
        albums[key] = dict(id=key, project='hon', category=category, title=title, description=description, related=[])
        return key
    bosses = album('hon:boss-round01', 'cast', 'Boss discovery · Round 1', 'Ten character proofs. Choose a candidate before four-view development; no winner selected.')
    caleb = album('hon:caleb-return', 'cast', 'Caleb · returned candidates', 'Character and meeting-scene candidates; tattoo continuity still needs review.')
    details = album('hon:return-detail-art', 'details', 'Recovered artwork & placement evidence', 'Source drawings, derived artwork and body crops have distinct roles; none are newly approved.')
    bossart = album('hon:boss-round01-art', 'details', 'Boss tattoo drawings · Round 1', 'Companion artwork and matching derivatives for candidates 003, 006 and 009.')
    review = album('hon:return-recovery-review', 'review', 'Grok recovery · unconfirmed sources', 'Recovery candidates and audit crops. An inventory mention does not establish recovered original artwork.')
    rejected = album('hon:return-rejected-attempts', 'review', 'Gun variants · rejected attempts', 'Earlier attempts retained for comparison, separate from the proposed outfit variants.')
    contact = album('hon:return-contact-sheets', 'review', 'Grok return · contact sheets', 'Review summaries for the verified October 9 intake.')
    rollout = {a['sha256']: a for a in audit['rollout_outfit_map']}
    providers = {}
    for m in audit['manifest_images']:
        providers.setdefault(m['measured']['sha256'], []).append(m['provider_record'])
    for f in receipt['unique_files']:
        if f['original_filename'] == 'RETURN_MANIFEST.json':
            source = read(ROOT / f['canonical_path'])
            for row in source.get('files', []):
                if row.get('sha256'):
                    providers.setdefault(row['sha256'], []).append(row)
    entries, documents = [], []
    species = ['Hippo', 'Gecko-frog', 'Slug', 'Pangolin', 'Catfish', 'Rhino', 'Axolotl', 'Crocodilian', 'Toad', 'Walrus']
    for f in receipt['unique_files']:
        path = ROOT / f['canonical_path']
        raw = path.read_bytes()
        assert len(raw) == f['bytes'] and hashlib.sha256(raw).hexdigest() == f['sha256']
        occurrences = [receipt['occurrences'][i] for i in f['occurrence_indices']]
        source_packs = sorted(set(Path(o['archive_path']).name for o in occurrences if o.get('archive_path')))
        name, sha = f['original_filename'], f['sha256']
        if f['kind'] != 'image':
            documents.append(dict(path=f['canonical_path'], title=name+' · '+(source_packs[0].replace('.zip','') if source_packs else 'Master index'), album='Grok returns · October 9', sha256=sha, bytes=f['bytes']))
            continue
        records = providers.get(sha, [])
        row = records[-1] if records else {}
        category, group, title = 'review', review, name
        source_ids = list(dict.fromkeys([r.get('source_asset_id') for r in records if r.get('source_asset_id') in old] + [i for r in records for i in r.get('source_asset_ids', []) if i in old]))
        extra = {}
        notes = ['Verified local file; creative acceptance remains open.']
        match = re.fullmatch(r'BOSS-(\d{3})_v001.png', name)
        if match:
            n = int(match[1]); category, group, title = 'cast', bosses, f'BOSS-{n:03d} · {species[n-1]}'
        elif any('tattoo_designs/' in o['member'] for o in occurrences):
            parent = next(re.search(r'tattoo_designs/(BOSS-\d+)/', o['member']).group(1) for o in occurrences if 'tattoo_designs/' in o['member'])
            category, group, title = 'details', bossart, parent+' · '+Path(name).stem.replace('_',' ')
        elif 'contact' in name.lower():
            category, group, title = 'review', contact, ('Boss round 1 · ' if any('BOSS-DISCOVERY' in p for p in source_packs) else 'Outfit gun variants · ')+name
        elif sha in rollout:
            m = rollout[sha]; group = m['existing_outfit_album']; category = 'outfits'
            title = m['existing_outfit_title']+' · Gun variant'
            source_ids = list(dict.fromkeys(source_ids+[m['source_asset_id']]))
            notes += ['Grok-reported side check: '+m['hip_side_check']+'. '+m['drift_notes']]
            extra.update(outfitAlbumID=group, propState='with_gun', propStateEvidence='Provider return manifest; independent visual review pending.', view='source composition', providerSideCheck=m['hip_side_check'])
        elif name.startswith('HIP-'):
            category, group, title = 'review', rejected, 'Rejected attempt · '+name
            extra['candidateState'] = 'provider_rejected'
        elif name.startswith('REV-HD-'):
            sources = [old[i] for i in source_ids if old[i]['category']=='outfits']
            if sources:
                category, group = 'outfits', sources[0]['album']; extra['outfitAlbumID'] = group
                title = next((a['title'] for a in catalog['albums'] if a['id']==group), group)+' · '+name.split('_')[0]+' revision'
            else:
                title = 'Revision candidate · '+name
        elif name.startswith(('CALEB-', 'CAL-')):
            category, group = 'cast', caleb
            title = 'Caleb · '+('Character proof' if name.startswith('CALEB-') else 'Meeting scene · continuity fixes needed')
        elif name.startswith(('ST-HD-', 'PROP-HD-')) or sha.startswith('c91af37e775d'):
            category, group = 'details', details
            title = 'Blaster · recovered source sheet' if sha.startswith('c91af37e775d') else Path(name).stem.replace('_',' ')
        for r in records:
            defects = r.get('unresolved', []) + r.get('known_differences', [])
            if defects: notes += ['Grok-reported: '+str(d) for d in defects]
        if name.startswith('REV-HD-001'):
            notes += ['Outfit/scene preservation failed; use as a correction candidate, not a replacement master.']
        if name.startswith('PROP-HD-HIP'):
            notes += ['Derived from generated REV-HD-004, which in turn references the older saloon image; it is not a direct crop of that older image.']
        if any('placement_' in o['member'] or '/_review/' in o['member'] for o in occurrences):
            extra['referenceRole'] = 'body_placement_or_audit_crop_not_stencil'
        elif row.get('artwork_origin'):
            extra['referenceRole'] = row['artwork_origin']
        aid = f.get('canonical_media_id') or 'HD-RETURN-'+sha[:12]
        entries.append(dict(id=aid, project='hon', path=f['canonical_path'], originalFilename=name, title=title, category=category, album=group,
                            sha256=sha, bytes=f['bytes'], width=f['image']['width'], height=f['image']['height'], mode=f['image']['mode'],
                            sourceIntake=receipt['intakeID'], sourceStatus='Verified received candidate; not approved', sourceAssetIDs=source_ids,
                            sourceAliases=[dict(archive=o.get('archive_path'), member=o['member']) for o in occurrences],
                            providerRecords=records, note=' '.join(dict.fromkeys(notes)), tags=['Grok return 20261009',name]+source_ids, **extra))
    ledger=dict(schema='grok-return-catalog-v1', intakeID=receipt['intakeID'], receiptSHA256=hashlib.sha256((HERE/'received/intake_receipt.json').read_bytes()).hexdigest(),
                approval='No provider claims are promoted to user approval.', albums=list(albums.values()), assets=entries, documents=documents)
    (HERE/'asset_ledger.json').write_text(json.dumps(ledger,ensure_ascii=False,indent=2),encoding='utf-8')
    for src, dst in [('.cache/grok_hd_return_audit_20261009.json','hd_audit.json'),('.cache/boss_intake_audit_20261009/audit.json','boss_audit.json')]:
        if not (HERE/dst).exists():
            shutil.copyfile(ROOT/src,HERE/dst)
    print(json.dumps({'images':len(entries),'documents':len(documents),'gun_variants':len(rollout),'albums_added':len(albums)}))

if __name__=='__main__':
    main()
