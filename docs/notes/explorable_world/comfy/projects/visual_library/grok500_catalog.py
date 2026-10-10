"""Read a verified Lisan look-pack intake without changing sources or approvals.

This is an optional catalog adapter, not an extractor. It deliberately does not
turn provider QA, hero picks, or filenames into user decisions or working refs.
"""
from collections import Counter
import csv
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re

VERIFIED_STATES = {
    'all_eight_extracted_crc_hash_size_decode_verified',
    'verified_extracted_zip_copies_removed',
    'eight_folders_nested_CRC_csv_hash_size_decode_verified',
}
SHOTS = ('V1', 'V2', 'V3', 'V4', 'V5', 'S1', 'S2', 'S3', 'S4', 'S5')
QA_LABELS = {'OK': 'clean', 'OK-note': 'drift note', 'FLAG': 'flagged / needs review'}
QA_CAVEAT = (
    'Grok-reported QA and hero picks are not independent visual verification or '
    'user approval. Grok reports that labels for rows 1–362 were inferred from '
    'earlier free-form notes; borderline classifications may differ.'
)


class CatalogIntakeError(ValueError):
    pass


def io_path(path):
    """Use extended Windows I/O; keep ordinary paths in manifests and URLs."""
    text = str(Path(path).absolute())
    if os.name == 'nt' and not text.startswith('\\\\?\\'):
        text = '\\\\?\\UNC\\' + text[2:] if text.startswith('\\\\') else '\\\\?\\' + text
    return Path(text)


def load_grok500(repo_root, intake_dir):
    """Return source-only album/asset/doc records, or None before receipt exists.

    Required media and source documents are rehashed against the receipt. ZIP
    copies can already have been cleaned up; they are never opened or required.
    Returned paths are repo-relative. The caller supplies display URLs/previews.
    """
    root = Path(repo_root).resolve()
    intake = Path(intake_dir).resolve()
    received = intake / 'received'
    if not received.resolve().is_relative_to(root):
        raise CatalogIntakeError('Intake must be inside the repository.')
    receipt_path = received / 'intake_receipt.json'
    if not receipt_path.is_file():
        return None
    receipt = json.loads(receipt_path.read_text(encoding='utf-8-sig'))
    if (receipt.get('state') not in VERIFIED_STATES or
            receipt.get('verified_top_level_parts') != 8):
        raise CatalogIntakeError('The complete eight-part intake is not verified.')

    records = {}
    for rec in receipt.get('files', []):
        relative = rec.get('relative_path', '')
        rel = PurePosixPath(relative)
        if (not relative or '\\' in relative or ':' in relative or rel.is_absolute()
                or '..' in rel.parts or relative in records):
            raise CatalogIntakeError('Unsafe or duplicate receipt path: ' + relative)
        path = (received / Path(*rel.parts)).resolve()
        if not path.is_relative_to(received.resolve()):
            raise CatalogIntakeError('Receipt path escapes the received directory.')
        records[relative] = {**rec, '_path': path}

    def one_file(name):
        matches = [r for r in records.values()
                   if r['relative_path'].startswith('content/') and r['_path'].name == name]
        if len(matches) != 1:
            raise CatalogIntakeError(f'Expected one extracted {name}; found {len(matches)}.')
        return matches[0]

    def verified_bytes(rec, image=False):
        path = rec['_path']
        if not io_path(path).is_file():
            raise CatalogIntakeError('Missing extracted source: ' + rec['relative_path'])
        data = io_path(path).read_bytes()
        if (len(data) != rec.get('bytes') or
                hashlib.sha256(data).hexdigest() != rec.get('sha256')):
            raise CatalogIntakeError('Source differs from intake receipt: ' + rec['relative_path'])
        if image and not rec.get('image', {}).get('decoded'):
            raise CatalogIntakeError('Image has no successful intake decode record.')
        return data

    legend = one_file('LEGEND-500.csv')
    rows = list(csv.DictReader(io.StringIO(verified_bytes(legend).decode('utf-8-sig'))))
    required = {'row', 'look_num', 'look_slug', 'shot', 'shot_name', 'filename',
                'zip_name', 'outfit', 'setting', 'breather', 'arm_worm',
                'qa_status', 'qa_note', 'hero'}
    if len(rows) != 500 or not rows or not required.issubset(rows[0]):
        raise CatalogIntakeError('Legend must contain the expected 500-row schema.')
    try:
        if sorted(int(r['row']) for r in rows) != list(range(1, 501)):
            raise CatalogIntakeError('Legend rows must be exactly 1–500, with no duplicates.')
        rows.sort(key=lambda r: int(r['row']))
    except (TypeError, ValueError) as exc:
        raise CatalogIntakeError('Invalid or duplicate ledger row numbers.') from exc

    albums, assets, documents, used_images, flagged = [], [], [], set(), []
    looks = {}

    def asset(rec, identifier, title, album, role, **extra):
        verified_bytes(rec, image=True)
        used_images.add(rec['relative_path'])
        info = rec['image']
        assets.append({
            'id': identifier, 'project': 'lisan', 'path': rec['_path'].relative_to(root).as_posix(),
            'title': title, 'category': 'outfits', 'album': album, 'role': role,
            'sha256': rec['sha256'], 'bytes': rec['bytes'],
            'width': info.get('width'), 'height': info.get('height'),
            'sourceIntake': 'LAG-500-20261008',
            'sourceStatus': 'Verified local file; creative and character accuracy await review.',
            **extra,
        })

    for row in rows:
        n = int(row['row'])
        look = f'L{(n - 1) // 10 + 1:02}'
        shot = SHOTS[(n - 1) % 10]
        slug = row['look_slug']
        if (row['look_num'] != look or row['shot'] != shot or
                not re.fullmatch(r'LAG-' + look + r'-[a-z0-9-]+', slug) or
                row['zip_name'] != slug + '.zip' or
                not row['filename'].startswith(slug + '__' + shot + '-') or
                Path(row['filename']).suffix.lower() not in {'.jpg', '.jpeg'} or
                row['qa_status'] not in QA_LABELS or
                any(row[key] not in {'Y', 'N'} for key in ('hero', 'breather', 'arm_worm'))):
            raise CatalogIntakeError(f'Inconsistent look, shot, filename or metadata at row {n}.')
        if look in looks and looks[look]['slug'] != slug:
            raise CatalogIntakeError('A look has conflicting slugs: ' + look)
        rec = one_file(row['filename'])
        if (rec['_path'].parent.name != slug or
                rec['_path'].parent.parent.name != row['zip_name'] + '.contents'):
            raise CatalogIntakeError('Source is outside its documented look ZIP folder.')
        album = 'lisan:grok500-' + look.lower()
        if look not in looks:
            name = slug.split('-', 2)[2].replace('-', ' ').capitalize()
            looks[look] = {'slug': slug, 'album': album, 'name': name}
            albums.append({
                'id': album, 'project': 'lisan', 'category': 'outfits',
                'title': f'{look} · {name}',
                'description': 'Five reference views and five scene concepts; supplied contact sheet last. '
                               'Grok exploration, awaiting your review. Outfit: ' + row['outfit'],
                'related': [],
            })
        identifier = f'LAG500-{look}-{shot}'
        role = 'Reference view' if shot.startswith('V') else 'Scene concept — not a timed storyboard panel'
        label = re.sub(r'^' + shot + r'\s*', '', row['shot_name']).replace('-', ' ').strip()
        qa = row['qa_status']
        note = f'Grok QA: {qa} ({QA_LABELS[qa]}). ' + (row['qa_note'] or 'No provider note supplied.')
        if row['hero'] == 'Y':
            note += ' Grok hero candidate; not a user favorite or an approved reference.'
        note += ' ' + QA_CAVEAT
        if shot.startswith('S'):
            note += ' This is a scene concept within this look; no song timing or storyboard order is assigned.'
        tags = [look, looks[look]['name'], role, f'Grok QA {qa}', QA_LABELS[qa], row['outfit']]
        if row['hero'] == 'Y':
            tags.append('Grok hero candidate')
        if qa == 'FLAG':
            flagged.append(identifier)
        asset(rec, identifier, f'{look} · {shot} {label}', album, role,
              note=note, beat=row['setting'], tags=tags,
              lookID=look, shotCode=shot, providerLedgerRow=n,
              providerQA={'provider': 'Grok', 'status': qa, 'note': row['qa_note'],
                          'heroCandidate': row['hero'] == 'Y',
                          'assessment': 'provider_report_not_independently_verified', 'caveat': QA_CAVEAT},
              requestedFeatures={'breather': row['breather'] == 'Y',
                                 'leftForearmWorm': row['arm_worm'] == 'Y'})

    # Add contacts after all ten source shots; contacts are not additional shots.
    for look, item in looks.items():
        rec = one_file('CONTACT-' + item['slug'] + '.jpg')
        asset(rec, f'LAG500-{look}-CONTACT', f'{look} · Contact sheet', item['album'],
              'Provider contact sheet',
              note='Grok overview of this look: V1–V5 above, S1–S5 below. Printed HERO/FLAG '
                   'labels are provider annotations, not user approvals. Inspect the individual source images for detail.',
              tags=[look, 'contact sheet', 'provider overview'], lookID=look)
    overview = 'lisan:grok500-overview'
    albums.append({'id': overview, 'project': 'lisan', 'category': 'inspiration',
                   'title': '500-image look pack · Overview',
                   'description': 'One provider thumbnail per look. Open Outfits for all 50 complete look collections.',
                   'related': []})
    asset(one_file('CONTACT-INDEX.jpg'), 'LAG500-CONTACT-INDEX', 'All 50 looks · Contact index',
          overview, 'Provider contact index', category='inspiration',
          note='Overview only. Grok QA and hero labels do not establish user approval.',
          tags=['50 looks', 'contact index', 'Grok 500'])
    if flagged:
        albums.append({'id': 'lisan:grok500-provider-flags', 'project': 'lisan', 'category': 'review',
                       'title': 'Grok-flagged look-pack images',
                       'description': 'Provider-reported concerns for inspection. These are not your triage decisions.',
                       'related': flagged})
    image_paths = {r['relative_path'] for r in records.values() if r.get('image')}
    if image_paths != used_images or len(assets) != 551:
        raise CatalogIntakeError('Receipt images do not match 500 shots plus 51 contact sheets exactly.')

    for name, title in [('NOVA-GUIDE-500.md', 'Grok 500-image pack · Guide'),
                        ('LEGEND-500.csv', 'Grok 500-image pack · Full image ledger'),
                        ('QA.txt', 'Grok 500-image pack · Original QA log')]:
        rec = one_file(name)
        verified_bytes(rec)
        documents.append({'path': rec['_path'].relative_to(root).as_posix(), 'title': title,
                          'album': 'Design and outfit notes · Grok 500-image pack'})
    # The local intake report, when present, is separate from unchanged provider docs.
    for name in ('receipt_summary.txt', 'INTAKE_SUMMARY.txt', 'intake_summary.txt', 'intake_summary.md'):
        path = intake / name
        if path.is_file():
            documents.append({'path': path.relative_to(root).as_posix(),
                              'title': 'Lisan 500-image pack · Local intake summary',
                              'album': 'Reference maps and drop notes'})

    return {'assets': assets, 'albums': albums, 'documents': documents,
            'summary': {'lookCount': len(looks), 'sourceImages': 500, 'contactSheets': 51,
                        'providerQACounts': dict(Counter(r['qa_status'] for r in rows)),
                        'providerHeroCandidates': sum(r['hero'] == 'Y' for r in rows),
                        'newUserApprovals': 0}}


def build_thumbnails(repo_root, data, output_dir, manifest_path):
    """Create small display derivatives; never modify the received originals."""
    from io import BytesIO
    from PIL import Image, ImageOps

    root = Path(repo_root).resolve()
    output = Path(output_dir).resolve()
    manifest = Path(manifest_path).resolve()
    if not output.is_relative_to(root) or not manifest.is_relative_to(root):
        raise CatalogIntakeError('Thumbnail outputs must remain inside the repository.')
    output.mkdir(parents=True, exist_ok=True)
    old = json.loads(manifest.read_text(encoding='utf-8'))['by_path'] if manifest.is_file() else {}
    mapping = {}
    for asset in data['assets']:
        source = root / asset['path']
        target = output / (asset['sha256'] + '.jpg')
        previous = old.get(asset['path'], {})
        cached = (target.is_file() and previous.get('sha256') == asset['sha256'] and
                  hashlib.sha256(target.read_bytes()).hexdigest() == previous.get('thumbnail_sha256'))
        if not cached:
            raw = io_path(source).read_bytes()
            if hashlib.sha256(raw).hexdigest() != asset['sha256']:
                raise CatalogIntakeError('Source changed while preparing display thumbnails.')
            with Image.open(BytesIO(raw)) as im:
                im.load()
                im = ImageOps.exif_transpose(im)
                if 'A' in im.getbands():
                    backdrop = Image.new('RGBA', im.size, 'white')
                    backdrop.alpha_composite(im.convert('RGBA'))
                    im = backdrop
                im = im.convert('RGB')
                im.thumbnail((480, 480), Image.Resampling.LANCZOS)
                im.save(target, format='JPEG', quality=85, optimize=True)
        with Image.open(target) as im:
            im.load()
            width, height = im.size
            if max(width, height) > 480:
                raise CatalogIntakeError('Display thumbnail exceeds 480 pixels.')
        raw = target.read_bytes()
        mapping[asset['path']] = {
            'thumbnail_path': target.relative_to(root).as_posix(), 'width': width, 'height': height,
            'source_width': asset['width'], 'source_height': asset['height'], 'kind': 'image',
            'sha256': asset['sha256'], 'thumbnail_sha256': hashlib.sha256(raw).hexdigest(),
            'thumbnail_bytes': len(raw), 'poster_seconds': None,
        }
    result = {'schema_version': 1, 'source_intake': data.get('intakeID','LAG-500-20261008'),
              'purpose': 'Display thumbnails only; original artwork and approval state unchanged.',
              'source_images': sum('contact' not in a.get('originalFilename','').lower() for a in data['assets']) if data.get('intakeID') else 500,
              'contact_sheets': sum('contact' in a.get('originalFilename','').lower() for a in data['assets']) if data.get('intakeID') else 51, 'originals_changed': False,
              'thumbnail_total_bytes': sum(x['thumbnail_bytes'] for x in mapping.values()),
              'by_path': mapping}
    manifest.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    return mapping
