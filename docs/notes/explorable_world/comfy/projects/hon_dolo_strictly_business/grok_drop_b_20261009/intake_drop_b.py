"""Bounded intake of the four named B folders; never runs provider code.

Reuses the reviewed Grok archive/decode helpers. Does not move or delete inputs,
change approvals, or rebuild the catalog. Missing manifest rows stay missing.
"""
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import unquote
import csv
import importlib.util
import io
import json
import re
import stat
import sys
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = next(p for p in HERE.parents if (p / 'AGENTS.md').is_file())
PROJECTS = HERE.parent.parent
INBOX = PROJECTS.parent / 'references/From Grok'
NAMES = [f'GROK-HD-DROP-20261009B_part{i}of4' for i in range(1, 5)]
PREFIX = 'GROK-HD-DROP-20261009B/'
HELPER = HERE.parent / 'grok_return_20261009/intake_return.py'
spec = importlib.util.spec_from_file_location('reviewed_return_helpers', HELPER)
m = importlib.util.module_from_spec(spec)
sys.dont_write_bytecode = True
spec.loader.exec_module(m)
INERT = {'.py', '.ps1', '.bat', '.cmd', '.exe', '.dll', '.msi', '.com', '.vbs', '.js', '.mjs', '.cjs', '.sh', '.html', '.htm', '.svg', '.jar'}


def main():
    receipt_path = HERE / 'received/intake_receipt.json'
    if receipt_path.exists():
        raise ValueError('Receipt exists; inspect it rather than repeat intake.')
    catalog_path = PROJECTS / 'visual_library/catalog.js'
    catalog_raw = catalog_path.read_bytes()
    catalog = json.loads(catalog_raw.decode('utf-8-sig').split('=', 1)[1].strip().rstrip(';'))
    known = {}
    for a in catalog['assets']:
        if a.get('sha256'):
            p = ROOT / a['repoPath'] if a.get('repoPath') else catalog_path.parent / unquote(a['src'])
            known.setdefault(a['sha256'], []).append({'path': m.relative(p), 'assetID': a['id'], 'evidence': 'catalog_snapshot'})
    for p in [HERE.parent / 'grok_return_20261009/received/intake_receipt.json',
              PROJECTS / 'collaborators/grok_image_benchmark_20261009/received/intake_receipt.json']:
        prior = json.loads(p.read_text(encoding='utf-8-sig'))
        for f in prior['unique_files']:
            known.setdefault(f['sha256'], []).append({'path': f['canonical_path'], 'assetID': f.get('canonical_media_id'), 'evidence': m.relative(p)})

    loose, folders = {}, []
    for name in NAMES:
        folder = m.checked_path(INBOX / name)
        if not folder.is_dir() or folder.is_symlink():
            raise ValueError('Missing/unsafe folder: ' + str(folder))
        files = []
        for p in sorted(folder.rglob('*')):
            if p.is_symlink() or getattr(p.lstat(), 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                raise ValueError('Reparse point: ' + str(p))
            if not p.resolve().is_relative_to(folder.resolve()):
                raise ValueError('Source escapes exact incoming folder.')
            if p.is_file():
                member = p.relative_to(folder).as_posix()
                if not member.startswith(PREFIX) or member in loose:
                    raise ValueError('Unexpected/duplicate outer member: ' + member)
                loose[member] = p
                files.append(p)
        infos = []
        for p in files:
            zi = zipfile.ZipInfo(p.relative_to(folder).as_posix())
            zi.file_size = p.stat().st_size
            infos.append(zi)
        m.safe_members(infos)
        folders.append({'path': m.relative(folder), 'files': len(files), 'bytes': sum(p.stat().st_size for p in files)})

    index_raw = loose[PREFIX + 'FILE_INDEX.csv'].read_bytes()
    index = list(csv.DictReader(io.StringIO(index_raw.decode('utf-8-sig'))))
    missing, verified_rows, self_index = [], [], []
    for row in index:
        p = loose.get(PREFIX + row['path'])
        if p is None:
            matches = [r for r in known.get(row['sha256'], []) if m.io_path(ROOT / r['path']).is_file()
                       and m.digest(m.io_path(ROOT / r['path']).read_bytes()) == row['sha256']]
            missing.append({**row, 'exactExistingMatches': matches, 'presentInThisDrop': False})
            continue
        raw = m.io_path(p).read_bytes()
        if row['path'] == 'FILE_INDEX.csv' and not re.fullmatch('[0-9a-f]{64}', row['sha256']):
            self_index.append({'path': row['path'], 'providerSHAField': row['sha256'], 'actualSHA256': m.digest(raw), 'actualBytes': len(raw)})
            continue
        assert len(raw) == int(row['size_bytes']) and m.digest(raw) == row['sha256'], row['path']
        assert p.is_relative_to(INBOX / NAMES[int(row['zip_part']) - 1]), row['path']
        verified_rows.append(row['path'])
    extras = sorted(set(loose) - {PREFIX + r['path'] for r in index})
    assert not extras, extras
    index_by_path = {PREFIX + r['path']: r for r in index}

    unique, occurrences, archives, payloads = {}, [], [], {}
    member_raw = {}
    total_bytes = 0

    def register(raw, name, source):
        nonlocal total_bytes
        total_bytes += len(raw)
        assert total_bytes < m.MAX_BYTES and len(occurrences) < m.MAX_FILES
        sha = m.digest(raw)
        ext = Path(name).suffix.lower()
        kind = 'image' if ext in m.IMAGE_EXTS else 'helper_text' if ext in INERT else 'document'
        img = m.decode_image(raw, name) if kind == 'image' else None
        if sha not in unique:
            matches = []
            for k in known.get(sha, []):
                p = m.io_path(m.checked_path(ROOT / k['path']))
                if p.is_file() and m.digest(p.read_bytes()) == sha and p.stat().st_size == len(raw):
                    if kind != 'helper_text' or p.suffix.lower() == '.txt':
                        matches.append(k)
            matches.sort(key=lambda k: (k['assetID'] is None, k['path']))
            if matches:
                path, aid, storage = matches[0]['path'], matches[0]['assetID'], 'existing_canonical'
            else:
                basename = Path(name).name + ('.txt' if kind == 'helper_text' else '')
                path = m.relative(HERE / 'received/content' / (sha[:12] + '__' + basename))
                aid, storage = None, 'new_content'
                payloads[path] = raw
            unique[sha] = {'sha256': sha, 'bytes': len(raw), 'kind': kind, 'image': img,
                           'original_filename': Path(name).name, 'canonical_path': path,
                           'canonical_media_id': aid, 'storage': storage, 'existing_matches': matches,
                           'occurrence_indices': [], 'retained_inert': kind == 'helper_text'}
        f = unique[sha]
        f['occurrence_indices'].append(len(occurrences))
        occurrences.append({**source, 'sha256': sha, 'bytes': len(raw), 'kind': kind,
                            'canonical_path': f['canonical_path'], 'canonical_media_id': f['canonical_media_id']})
        return f

    for member, p in loose.items():
        raw = m.io_path(p).read_bytes()
        if p.suffix.lower() != '.zip':
            register(raw, member, {'source_path': m.relative(p), 'member': member, 'providerIndex': index_by_path.get(member)})
            member_raw[member] = raw
            continue
        sha = m.digest(raw)
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            m.safe_members(z.infolist())
            assert sum(i.file_size for i in z.infolist()) < m.MAX_BYTES
            assert z.testzip() is None, str(p)
            arc = {'path': m.relative(p), 'outerMember': member, 'sha256': sha, 'bytes': len(raw), 'crc_verified': True, 'members': []}
            for info in z.infolist():
                if info.is_dir():
                    continue
                if info.filename.endswith('.zip'):
                    raise ValueError('Unexpected deeper nested archive.')
                data = z.read(info)
                assert len(data) == info.file_size
                row = register(data, info.filename, {'source_path': m.relative(p), 'archive_path': m.relative(p),
                    'archive_sha256': sha, 'member': info.filename, 'crc32': f'{info.CRC:08x}', 'crc_verified': True})
                arc['members'].append({'member': info.filename, 'sha256': row['sha256'], 'bytes': row['bytes'], 'canonical_path': row['canonical_path']})
                if info.filename in member_raw:
                    assert member_raw[info.filename] == data
                member_raw[info.filename] = data
            archives.append(arc)

    checks = {}
    for version in ['v001', 'v002', 'v003']:
        prefix = f'GROK-HD-20261009_VIS-HD_{version}/'
        data = json.loads(member_raw[prefix + 'manifest.json'])
        rows = data if isinstance(data, list) else data.get('items', data.get('deliverables', []) + data.get('rejected', []))
        for row in rows:
            key = row['file'] if row['file'].startswith(prefix) else prefix + row['file']
            raw = member_raw[key]
            assert m.digest(raw) == row['sha256'], key
            if 'bytes' in row:
                assert len(raw) == row['bytes']
        checks[version + '_manifest_rows_verified'] = len(rows)
    v3 = json.loads(member_raw['GROK-HD-20261009_VIS-HD_v003/manifest.json'])['items']
    updates = list(csv.DictReader(io.StringIO(member_raw[PREFIX + '01_BENCHMARK_KIT/UPDATE_refs_MOUTH-LOCK-VIS-HD_v003/manifest.csv'].decode('utf-8-sig'))))
    for row in updates:
        loose_key = PREFIX + '01_BENCHMARK_KIT/UPDATE_refs_MOUTH-LOCK-VIS-HD_v003/' + Path(row['file']).name
        assert m.digest(member_raw[loose_key]) == row['sha256'] == m.digest(member_raw[row['file']])
    checks['update_copies_match_v003_shapes'] = len(updates)
    kit = list(csv.DictReader(io.StringIO(member_raw['NOVA-IMG-BENCH-20261009/KIT_MANIFEST.csv'].decode('utf-8-sig'))))
    for row in kit:
        raw = member_raw['NOVA-IMG-BENCH-20261009/' + row['kit_path']]
        assert m.digest(raw) == row['sha256'] and len(raw) == int(row['bytes'])
    checks['benchmark_manifest_rows_verified'] = len(kit)
    looks = list(csv.DictReader(io.StringIO(member_raw[PREFIX + '06_OUTFIT_INVENTORY/LOOKS.csv'].decode('utf-8-sig'))))
    checks['outfit_inventory_rows'] = len(looks)
    checks['outfit_inventory_columns'] = list(looks[0])

    for path, raw in payloads.items():
        out = m.io_path(m.checked_path(ROOT / path))
        out.parent.mkdir(parents=True, exist_ok=True)
        if out.exists():
            assert out.read_bytes() == raw
        else:
            with out.open('xb') as stream:
                stream.write(raw)
    for f in unique.values():
        raw = m.io_path(ROOT / f['canonical_path']).read_bytes()
        assert len(raw) == f['bytes'] and m.digest(raw) == f['sha256']
    # Recheck all original paths after storing, including original ZIP byte hashes.
    for member, p in loose.items():
        if p.suffix.lower() == '.zip':
            expected = next(a['sha256'] for a in archives if a['outerMember'] == member)
        else:
            expected = m.digest(member_raw[member])
        assert m.digest(m.io_path(p).read_bytes()) == expected

    summary = {'source_folders': len(folders), 'outer_files_received': len(loose), 'outer_manifest_rows': len(index),
               'missing_outer_files': len(missing), 'nested_archives_verified': len(archives),
               'file_occurrences': len(occurrences), 'unique_files': len(unique),
               'unique_kind_counts': dict(Counter(f['kind'] for f in unique.values())),
               'existing_canonical_files_reused': sum(f['storage'] == 'existing_canonical' for f in unique.values()),
               'new_content_files_written': len(payloads), 'new_content_bytes': sum(len(v) for v in payloads.values()),
               'duplicate_occurrences_reused': len(occurrences) - len(unique),
               'mouth_macros_v003': len(v3), 'head_library_slots_received': 0, 'head_anchor_drafts_proposals_rejections': 7}
    receipt = {'schema': 'grok-return-intake-v1', 'intakeID': 'GROK-HD-DROP-20261009B',
               'recordedAtUTC': datetime.now(timezone.utc).isoformat(), 'state': 'available_files_verified_outer_package_incomplete',
               'catalog_snapshot': {'path': m.relative(catalog_path), 'sha256': m.digest(catalog_raw)},
               'source_folders': folders, 'archives': archives, 'unique_files': list(unique.values()),
               'occurrences': occurrences, 'summary': summary,
               'package_completeness': {'complete': False, 'missing': missing, 'unexpected': extras},
               'manifest_verification': {'outer_rows_hash_size_part_verified': len(verified_rows), 'self_index': self_index, **checks},
               'newApprovals': [], 'providerHelpersExecuted': False, 'sourceCleanupPerformed': False,
               'limitations': ['All received bytes verified; four files listed by the provider are absent from this drop.',
                   'Provider QA and acceptance wording are attributed claims, not local image approval.',
                   '50 mouth macros are separate from the 130-head baseline, which has not been delivered.',
                   'Provider README explicitly excludes cosmic-avatar; this B package does not contain Jet Black.',
                   'Incoming folders and ZIPs retained pending missing-file reconciliation.']}
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'summary': summary, 'checks': checks, 'missing': [r['path'] for r in missing]}, indent=2))


if __name__ == '__main__':
    main()
