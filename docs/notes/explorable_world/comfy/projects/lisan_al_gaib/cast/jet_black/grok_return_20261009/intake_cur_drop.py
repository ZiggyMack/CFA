"""Bounded CUR-DROP intake using CFA's reviewed Grok integrity helpers.

Default: inspect only. --ingest writes unchanged unique bytes and evidence.
No catalog edits, source moves, provider execution, or design approvals.
"""
from collections import Counter
from datetime import datetime, timezone
from io import BytesIO, StringIO
from pathlib import Path
from urllib.parse import unquote
import argparse
import csv
import importlib.util
import json
import stat
import sys
import zipfile

from PIL import Image, ImageChops, ImageStat

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'AGENTS.md').is_file())
BASE = ROOT / 'docs/notes/explorable_world/comfy'
INBOX = BASE / 'references/From Grok'
NAMES = [f'CUR-DROP-20261009A_part{i}of4' for i in range(1, 5)]
EXPECTED = [(38, 17405265), (53, 19246236), (50, 16426217), (32, 10975453)]
HELPER = BASE / 'projects/hon_dolo_strictly_business/grok_return_20261009/intake_return.py'
spec = importlib.util.spec_from_file_location('reviewed_grok_intake_helpers', HELPER)
m = importlib.util.module_from_spec(spec)
sys.dont_write_bytecode = True
spec.loader.exec_module(m)


def pixel_record(path):
    with Image.open(m.io_path(path)) as im:
        im.load()
        rgb = im.convert('RGB')
        return {'size': list(rgb.size), 'rgb_sha256': m.digest(rgb.tobytes())}


def main(ingest=False):
    receipt_path = HERE / 'received/intake_receipt.json'
    if ingest and receipt_path.exists():
        raise ValueError('Receipt already exists; do not overwrite an intake.')
    occurrences, by_member, folders = [], {}, []
    for number, (name, expected) in enumerate(zip(NAMES, EXPECTED), 1):
        folder = m.checked_path(INBOX / name)
        if not folder.is_dir():
            raise ValueError('Missing exact part: ' + name)
        paths = sorted(folder.rglob('*'))
        infos, files = [], []
        for path in [folder, *paths]:
            if path.is_symlink() or getattr(path.lstat(), 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                raise ValueError('Reparse point or symlink rejected: ' + str(path))
            if not m.checked_path(path).is_relative_to(folder):
                raise ValueError('Path escaped the named source folder.')
            if path == folder:
                continue
            rel = path.relative_to(folder).as_posix()
            info = zipfile.ZipInfo(rel + '/' if path.is_dir() else rel)
            info.file_size = 0 if path.is_dir() else path.stat().st_size
            infos.append(info)
            if path.is_file():
                files.append(path)
        m.safe_members(infos)
        measured = (len(files), sum(p.stat().st_size for p in files))
        if measured != expected:
            raise ValueError(f'Changed/incomplete part {name}: {measured} != {expected}')
        folders.append({'source_path': m.relative(folder), 'file_count': measured[0], 'bytes': measured[1]})
        for path in files:
            member = path.relative_to(folder / 'CUR-DROP-20261009A').as_posix()
            if member in by_member:
                raise ValueError('Repeated package member: ' + member)
            raw = m.io_path(path).read_bytes()
            ext = path.suffix.lower()
            if ext not in m.IMAGE_EXTS | {'.md', '.pdf', '.csv', '.txt', '.jsonl'}:
                raise ValueError('Unexpected file type requires review: ' + member)
            row = {'source_folder': m.relative(folder), 'source_path': m.relative(path),
                   'member': member, 'part': number, 'sha256': m.digest(raw), 'bytes': len(raw),
                   'kind': 'image' if ext in m.IMAGE_EXTS else 'document',
                   'image': m.decode_image(raw, path.name) if ext in m.IMAGE_EXTS else None}
            occurrences.append(row)
            by_member[member] = row

    def raw_for(member):
        return m.io_path(ROOT / by_member[member]['source_path']).read_bytes()

    index = list(csv.DictReader(StringIO(raw_for('FILE_INDEX.csv').decode('utf-8-sig'))))
    if len(index) != 172 or len({r['path'] for r in index}) != 172:
        raise ValueError('Expected 172 distinct provider index rows.')
    for row in index:
        actual = by_member[row['path']]
        if (row['sha256'], int(row['size_bytes']), int(row['zip_part'])) != (actual['sha256'], actual['bytes'], actual['part']):
            raise ValueError('Provider index mismatch: ' + row['path'])
        actual['provider_index'] = row
    if set(by_member) - {r['path'] for r in index} != {'FILE_INDEX.csv'}:
        raise ValueError('Unexpected files outside the provider index.')
    maps = []
    for member in sorted(by_member):
        if not member.endswith('/manifest.csv'):
            continue
        rows = list(csv.DictReader(StringIO(raw_for(member).decode('utf-8-sig'))))
        for row in rows:
            target = str(Path(member).parent / row['file']).replace('\\', '/')
            actual = by_member[target]
            if row['sha256'] != actual['sha256'] or actual['kind'] != 'image':
                raise ValueError('Collection manifest mismatch: ' + target)
            if 'provider_mapping' in actual:
                raise ValueError('Duplicate collection mapping: ' + target)
            actual['provider_mapping'] = row
        maps.append({'manifest': member, 'rows_verified': len(rows)})
    if sum(r['rows_verified'] for r in maps) != 149:
        raise ValueError('Expected 149 image map rows.')

    catalog_path = BASE / 'projects/visual_library/catalog.js'
    catalog_raw = catalog_path.read_bytes()
    catalog = json.loads(catalog_raw.decode('utf-8-sig').split('=', 1)[1].strip().rstrip(';'))
    existing = {}
    for asset in catalog['assets']:
        if asset.get('sha256'):
            path = m.checked_path(ROOT / asset['repoPath']) if asset.get('repoPath') else m.checked_path(catalog_path.parent / unquote(asset['src']))
            existing.setdefault(asset['sha256'], []).append({'id': asset['id'], 'path': m.relative(path)})
    unique = {}
    for occurrence in occurrences:
        sha = occurrence['sha256']
        if sha not in unique:
            matches = sorted(existing.get(sha, []), key=lambda r: r['id'])
            for match in matches:
                raw = m.io_path(ROOT / match['path']).read_bytes()
                if m.digest(raw) != sha or len(raw) != occurrence['bytes']:
                    raise ValueError('Stale catalog canonical file: ' + match['id'])
            canonical = matches[0]['path'] if matches else m.relative(HERE / 'received/content' / (sha[:12] + '__' + Path(occurrence['member']).name))
            unique[sha] = {'sha256': sha, 'bytes': occurrence['bytes'], 'kind': occurrence['kind'],
                           'canonical_path': canonical, 'canonical_media_id': matches[0]['id'] if matches else None,
                           'storage': 'existing_catalog' if matches else 'new_content', 'existing_matches': matches,
                           'image': occurrence['image'], 'members': []}
        unique[sha]['members'].append(occurrence['member'])
        occurrence['canonical_path'] = unique[sha]['canonical_path']
        occurrence['canonical_media_id'] = unique[sha]['canonical_media_id']

    identity = []
    for local_name, supplied_member in [
        ('Jet_Black_solo_full_body_user_reference.jpg', '01_CHARACTER_REFS/CUR-REF-04_HEAD-ORB.jpg'),
        ('Jet_Black_with_Lisan_user_reference.jpg', '05_LISAN_SCENES/CUR-LAG-01_DESERT-MEETING.jpg'),
    ]:
        local = HERE.parent / 'source' / local_name
        supplied = ROOT / by_member[supplied_member]['source_path']
        before, after = pixel_record(local), pixel_record(supplied)
        with Image.open(local) as a, Image.open(supplied) as b:
            difference = ImageStat.Stat(ImageChops.difference(a.convert('RGB'), b.convert('RGB'))) if a.size == b.size else None
        identity.append({'existing_reference': m.relative(local), 'existing_sha256': m.digest(local.read_bytes()),
                         'received_member': supplied_member, 'received_sha256': by_member[supplied_member]['sha256'],
                         'existing_pixels': before, 'received_pixels': after, 'decoded_rgb_equal': before == after,
                         'per_channel_mean_absolute_difference_0_to_255': difference.mean if difference else None,
                         'per_channel_rms_difference_0_to_255': difference.rms if difference else None,
                         'byte_identical': m.digest(local.read_bytes()) == by_member[supplied_member]['sha256']})
    unique_rows = list(unique.values())
    summary = {'parts': len(folders), 'file_occurrences': len(occurrences),
               'source_bytes': sum(r['bytes'] for r in occurrences), 'unique_files': len(unique_rows),
               'unique_kind_counts': dict(Counter(r['kind'] for r in unique_rows)),
               'image_occurrences': sum(r['kind'] == 'image' for r in occurrences),
               'mapped_image_occurrences': 149,
               'contact_sheet_occurrences': sum(r['kind'] == 'image' and 'provider_mapping' not in r for r in occurrences),
               'duplicate_occurrences': len(occurrences) - len(unique_rows),
               'existing_canonical_files_reused': sum(r['storage'] == 'existing_catalog' for r in unique_rows),
               'new_content_files': sum(r['storage'] == 'new_content' for r in unique_rows),
               'canonical_unique_bytes': sum(r['bytes'] for r in unique_rows),
               'new_content_bytes': sum(r['bytes'] for r in unique_rows if r['storage'] == 'new_content')}
    receipt = {'schema': 'grok-return-intake-v1', 'intakeID': 'CUR-DROP-20261009A',
               'state': 'verified_hash_size_decode_complete_extracted_batch' if ingest else 'inspection_only',
               'recordedAtUTC': datetime.now(timezone.utc).isoformat(), 'characterID': 'LAG-JET-BLACK',
               'authority': 'Existing user-designated Jet Black, watcher working for Lisan. Provider Curator working name and mentor lore remain proposals.',
               'catalog_snapshot': {'path': m.relative(catalog_path), 'sha256': m.digest(catalog_raw)},
               'source_folders': folders, 'occurrences': occurrences, 'unique_files': unique_rows, 'summary': summary,
               'package_completeness': {'expected_folders': NAMES, 'received_verified': NAMES, 'pending': [], 'complete': True},
               'manifest_verification': {'file_index_rows_verified': len(index), 'unlisted_file': 'FILE_INDEX.csv', 'collection_manifests': maps},
               'existing_character_reference_comparison': identity,
               'newApprovals': [], 'providerHelpersExecuted': False, 'catalogRegistrationPerformed': False, 'sourceCleanupPerformed': False,
               'limitations': ['Extracted folders were supplied; no archive CRC claim.',
                               'Hash/size/decode integrity is not visual acceptance.',
                               'Provider storybeat/headtype tags and 50-scene filename associations remain attributed mappings, not independently accepted narrative.',
                               'This package contains cosmic-avatar/Jet Black head variants; it is not the separately claimed Lisan facial headshot delivery.',
                               'Lisan natural teeth and existing identity/cast reference scope remain unchanged. No Hon Dolo dental design transfers.']}
    if ingest:
        for row in unique_rows:
            destination = m.checked_path(ROOT / row['canonical_path'])
            source = ROOT / by_member[row['members'][0]]['source_path']
            raw = m.io_path(source).read_bytes()
            if row['storage'] == 'new_content':
                m.io_path(destination.parent).mkdir(parents=True, exist_ok=True)
                with m.io_path(destination).open('xb') as output:
                    output.write(raw)
            final = m.io_path(destination).read_bytes()
            if m.digest(final) != row['sha256'] or len(final) != row['bytes']:
                raise ValueError('Final canonical verification failed.')
            if row['image'] and m.decode_image(final, destination.name) != row['image']:
                raise ValueError('Final canonical decode differs.')
        for row in occurrences:
            if m.digest(m.io_path(ROOT / row['source_path']).read_bytes()) != row['sha256']:
                raise ValueError('Source changed during intake.')
        receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        ledger = {'schema': 'cfa-character-return-ledger-v1', 'intakeID': receipt['intakeID'], 'characterID': 'LAG-JET-BLACK',
                  'receipt': m.relative(receipt_path), 'assets': [
                      {'id': r.get('canonical_media_id') or 'LAG-JET-BLACK-DROP-' + r['sha256'][:12],
                       'providerID': r.get('provider_mapping', {}).get('id'), 'member': r['member'],
                       'repoPath': r['canonical_path'], 'sha256': r['sha256'], 'bytes': r['bytes'], 'image': r['image'],
                       'provider': r.get('provider_mapping') or r.get('provider_index'),
                       'reviewStatus': 'needs_user_review', 'approval': None,
                       'scope': 'Exploration candidate; provider scope does not supersede existing user references.'}
                      for r in occurrences if r['kind'] == 'image']}
        (HERE / 'asset_ledger.json').write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(json.dumps({'state': receipt['state'], 'summary': summary, 'manifest_verification': receipt['manifest_verification'],
                      'reference_comparison': identity}, indent=2))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--ingest', action='store_true')
    main(parser.parse_args().ingest)
