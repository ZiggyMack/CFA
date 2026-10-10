"""Bounded intake of the three named October 9 extracted Grok return folders.

Reuses existing reviewed archive/image helpers. Does not execute provider content,
alter prior receipts, register catalog assets, or move/delete incoming material.
"""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote
import csv
import importlib.util
import io
import json
import stat
import sys
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'AGENTS.md').is_file())
INBOX = ROOT / 'docs/notes/explorable_world/comfy/references/From Grok'
NAMES = ['NOVA-IMG-BENCH-20261009_part1of2', 'NOVA-IMG-BENCH-20261009_part2of2', 'GROK-HD-20261009_VIS-HD_v001']
EXPECTED = [(98, 19074265), (16, 13370509), (21, 6014808)]
HELPER = ROOT / 'docs/notes/explorable_world/comfy/projects/hon_dolo_strictly_business/grok_return_20261009/intake_return.py'
spec = importlib.util.spec_from_file_location('reviewed_grok_intake_helpers', HELPER)
m = importlib.util.module_from_spec(spec)
sys.dont_write_bytecode = True
spec.loader.exec_module(m)
INERT_EXTS = {'.py', '.ps1', '.bat', '.cmd', '.exe', '.dll', '.msi', '.com', '.vbs', '.js', '.mjs', '.cjs', '.sh', '.html', '.htm', '.svg', '.jar'}


def main():
    output = HERE / 'intake_receipt.json'
    if output.exists():
        raise ValueError('Aggregate receipt already exists; inspect before retrying.')
    historical_paths = [HERE / 'part1_receipt.json', HERE / 'part1_manifest_review.json']
    historical_hashes = {m.relative(p): m.digest(p.read_bytes()) for p in historical_paths}
    part1 = json.loads(historical_paths[0].read_text(encoding='utf-8'))
    part1_files = {r['member']: r for r in part1['occurrences'] if r['kind'] != 'directory'}
    catalog_path = ROOT / 'docs/notes/explorable_world/comfy/projects/visual_library/catalog.js'
    catalog_raw = catalog_path.read_bytes()
    catalog = json.loads(catalog_raw.decode('utf-8-sig').split('=', 1)[1].strip().rstrip(';'))
    existing = {}

    def add_known(sha, path, asset_id, evidence, preferred=False):
        if sha:
            existing.setdefault(sha, []).append({'path': path, 'id': asset_id, 'evidence': evidence, 'preferred': preferred})

    for row in part1['unique_files']:
        add_known(row['sha256'], row['canonical_path'], row.get('canonical_media_id'), m.relative(historical_paths[0]), True)
    for row in catalog['assets']:
        if row.get('sha256'):
            path = m.checked_path(ROOT / row['repoPath']) if row.get('repoPath') else m.checked_path(catalog_path.parent / unquote(row['src']))
            add_known(row['sha256'], m.relative(path), row['id'], 'catalog_snapshot')
    prior_path = HELPER.parent / 'received/intake_receipt.json'
    prior = json.loads(prior_path.read_text(encoding='utf-8-sig'))
    for row in prior['unique_files']:
        add_known(row['sha256'], row['canonical_path'], row.get('canonical_media_id'), m.relative(prior_path))

    source_folders, source_files = [], []
    for folder_name, expected in zip(NAMES, EXPECTED):
        folder = m.checked_path(INBOX / folder_name)
        if not folder.is_dir():
            raise ValueError('Missing exact incoming folder: ' + str(folder))
        paths = sorted(folder.rglob('*'))
        infos, files = [], []
        for path in paths:
            if path.is_symlink() or getattr(path.lstat(), 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                raise ValueError('Reparse/symlink path in incoming folder: ' + str(path))
            m.checked_path(path)
            if not path.resolve().is_relative_to(folder.resolve()):
                raise ValueError('Incoming path escapes named folder.')
            rel = path.relative_to(folder).as_posix()
            entry = zipfile.ZipInfo(rel + '/' if path.is_dir() else rel)
            entry.file_size = 0 if path.is_dir() else path.stat().st_size
            infos.append(entry)
            if path.is_file():
                if path.suffix.lower() == '.zip':
                    raise ValueError('Unexpected nested ZIP; inspect separately before proceeding.')
                files.append(path)
        m.safe_members(infos)
        measured = (len(files), sum(p.stat().st_size for p in files))
        if measured != expected:
            raise ValueError('Unexpected source inventory: ' + repr((folder_name, measured, expected)))
        source_folders.append({'source_path': m.relative(folder), 'file_count': measured[0], 'bytes': measured[1], 'nested_zip_count': 0})
        source_files.extend((folder_name, p, p.relative_to(folder).as_posix()) for p in files)

    occurrences, unique, payloads = [], {}, {}
    for folder_name, path, member in source_files:
        raw = m.io_path(path).read_bytes()
        sha, ext = m.digest(raw), path.suffix.lower()
        kind = 'image' if ext in m.IMAGE_EXTS else 'helper_text' if ext in INERT_EXTS else 'document'
        image = m.decode_image(raw, path.name) if kind == 'image' else None
        prior_member = part1_files.get(member) if folder_name == NAMES[0] else None
        if folder_name == NAMES[0] and (not prior_member or sha != prior_member['sha256'] or len(raw) != prior_member['bytes']):
            raise ValueError('Extracted first part differs from verified ZIP member: ' + member)
        if sha not in unique:
            matches = []
            for known in existing.get(sha, []):
                p = m.checked_path(ROOT / known['path'])
                data = m.io_path(p).read_bytes()
                if len(data) != len(raw) or m.digest(data) != sha:
                    raise ValueError('Stale existing canonical bytes: ' + known['path'])
                if kind != 'helper_text' or p.suffix.lower() == '.txt':
                    matches.append(known)
            matches.sort(key=lambda r: (not r['preferred'], r['id'] is None, r['path']))
            if matches:
                canonical, asset_id, storage = matches[0]['path'], matches[0]['id'], 'existing_canonical'
            else:
                name = path.name + '.txt' if kind == 'helper_text' else path.name
                canonical = m.relative(m.checked_path(HERE / 'content' / (sha[:12] + '__' + name)))
                asset_id, storage = None, 'new_content'
                payloads[canonical] = raw
            unique[sha] = {'sha256': sha, 'bytes': len(raw), 'kind': kind, 'canonical_path': canonical,
                           'canonical_media_id': asset_id, 'storage': storage, 'original_filename': path.name,
                           'existing_matches': matches, 'image': image, 'retained_inert': kind == 'helper_text',
                           'occurrence_indices': [], 'prior_archive_aliases': []}
        record = unique[sha]
        record['occurrence_indices'].append(len(occurrences))
        archive_aliases = []
        if prior_member:
            archive_aliases.append({k: prior_member[k] for k in ['archive_path', 'archive_sha256', 'member', 'crc32', 'crc_verified']})
            record['prior_archive_aliases'].extend(a for a in archive_aliases if a not in record['prior_archive_aliases'])
        occurrences.append({'source_folder': m.relative(INBOX / folder_name), 'source_path': m.relative(path),
                            'member': member, 'sha256': sha, 'bytes': len(raw), 'kind': kind,
                            'canonical_path': record['canonical_path'], 'canonical_media_id': record['canonical_media_id'],
                            'storage': record['storage'], 'image': image, 'retained_inert': kind == 'helper_text',
                            'verified_archive_aliases': archive_aliases})

    by_member = {}
    for row in occurrences:
        if row['member'] in by_member:
            raise ValueError('Duplicate relative package path across supplied folders.')
        by_member[row['member']] = row

    def raw_for(member):
        row = by_member[member]
        return m.io_path(ROOT / row['source_path']).read_bytes()

    benchmark_prefix = 'NOVA-IMG-BENCH-20261009/'
    kit = list(csv.DictReader(io.StringIO(raw_for(benchmark_prefix + 'KIT_MANIFEST.csv').decode('utf-8-sig'))))
    for row in kit:
        actual = by_member.get(benchmark_prefix + row['kit_path'])
        if not actual or actual['sha256'] != row['sha256'] or actual['bytes'] != int(row['bytes']):
            raise ValueError('KIT_MANIFEST mismatch: ' + row['kit_path'])
    kit_actual = {p.removeprefix(benchmark_prefix) for p in by_member if p.startswith(benchmark_prefix)}
    if kit_actual - {r['kit_path'] for r in kit} != {'KIT_MANIFEST.csv'}:
        raise ValueError('Unexpected benchmark files outside manifest.')
    refs = list(csv.DictReader(io.StringIO(raw_for(benchmark_prefix + 'refs/refs_manifest.csv').decode('utf-8-sig'))))
    for row in refs:
        actual = by_member[benchmark_prefix + row['kit_file']]
        if actual['sha256'] != row['sha256'] or actual['bytes'] != int(row['bytes']):
            raise ValueError('Reference manifest mismatch.')
    vis_prefix = 'GROK-HD-20261009_VIS-HD_v001/'
    vis = json.loads(raw_for(vis_prefix + 'manifest.json'))
    for row in vis['deliverables'] + vis['rejected']:
        actual = by_member.get(vis_prefix + row['file'])
        if not actual or actual['sha256'] != row['sha256']:
            raise ValueError('VIS manifest SHA mismatch.')
        if row.get('bytes') is not None and actual['bytes'] != row['bytes']:
            raise ValueError('VIS manifest byte mismatch.')
        if row.get('width') is not None and [actual['image']['width'], actual['image']['height']] != [row['width'], row['height']]:
            raise ValueError('VIS manifest dimensions mismatch.')

    for rel, raw in payloads.items():
        target = m.checked_path(ROOT / rel)
        m.io_path(target.parent).mkdir(parents=True, exist_ok=True)
        if m.io_path(target).exists():
            if m.io_path(target).read_bytes() != raw:
                raise ValueError('Content-store collision.')
        else:
            with m.io_path(target).open('xb') as stream:
                stream.write(raw)
    for row in unique.values():
        raw = m.io_path(ROOT / row['canonical_path']).read_bytes()
        if len(raw) != row['bytes'] or m.digest(raw) != row['sha256']:
            raise ValueError('Final canonical verification failed.')
        if row['image'] and m.decode_image(raw, row['original_filename']) != row['image']:
            raise ValueError('Final image decode differs.')
    for row in occurrences:
        if m.digest(m.io_path(ROOT / row['source_path']).read_bytes()) != row['sha256']:
            raise ValueError('Incoming source changed during intake.')
    for rel, sha in historical_hashes.items():
        if m.digest((ROOT / rel).read_bytes()) != sha:
            raise ValueError('Historical part-one snapshot changed.')

    unique_rows = list(unique.values())
    summary = {'source_folders': len(source_folders), 'file_occurrences': len(occurrences),
               'source_bytes': sum(r['bytes'] for r in occurrences), 'unique_files': len(unique_rows),
               'unique_kind_counts': dict(Counter(r['kind'] for r in unique_rows)),
               'image_occurrences': sum(r['kind'] == 'image' for r in occurrences),
               'existing_canonical_files_reused': sum(r['storage'] == 'existing_canonical' for r in unique_rows),
               'new_content_files_written': len(payloads), 'duplicate_occurrences_reused': len(occurrences) - len(unique_rows),
               'canonical_unique_bytes': sum(r['bytes'] for r in unique_rows),
               'new_content_bytes': sum(len(r) for r in payloads.values())}
    receipt = {'schema': 'grok-return-intake-v1', 'intakeID': 'NOVA-IMG-BENCH-AND-VIS-20261009',
               'state': 'verified_hash_size_decode_complete_extracted_batch', 'recordedAtUTC': datetime.now(timezone.utc).isoformat(),
               'catalog_snapshot': {'path': m.relative(catalog_path), 'sha256': m.digest(catalog_raw)},
               'historical_snapshots_unchanged': historical_hashes, 'source_folders': source_folders,
               'archives': part1['archives'], 'unique_files': unique_rows, 'occurrences': occurrences, 'summary': summary,
               'package_completeness': {'expected_folders': NAMES, 'received_verified': NAMES, 'pending': [], 'complete': True},
               'manifest_verification': {'benchmark_manifest_rows_verified': len(kit), 'unlisted_benchmark_file': 'KIT_MANIFEST.csv',
                                         'reference_rows_verified': len(refs), 'reference_kind_counts': dict(Counter(r['kind'] for r in refs)),
                                         'vis_deliverables_verified': len(vis['deliverables']), 'vis_rejected_verified': len(vis['rejected']),
                                         'vis_contact_and_documents': 'Integrity/decode verified; not listed in deliverables/rejected manifest arrays'},
               'newApprovals': [], 'providerHelpersExecuted': False, 'providerHTMLExecuted': False,
               'catalogRegistrationPerformed': False, 'sourceCleanupPerformed': False,
               'limitations': ['Technical integrity is not visual review or approval.',
                               'Part one extracted files exactly match the prior verified ZIP member hashes and sizes.',
                               'Parts two and VIS were supplied extracted; no CRC claim is made for absent source archives.',
                               'Provider QA, character locks, capability claims and proposed attempts are attributed source data.']}
    temporary = HERE / 'intake_receipt.next.json'
    temporary.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    temporary.replace(output)
    print(json.dumps({'state': receipt['state'], 'summary': summary, 'manifest_verification': receipt['manifest_verification']}, indent=2))


if __name__ == '__main__':
    main()
