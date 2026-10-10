"""Inspect (default) or safely extract eight already-unpacked Grok500 folders.

Uses the existing bounded ZIP Scanner. Does not recompress outer folders, copy
input ZIPs, delete inputs, change source bytes, edit catalogs or approve designs.
Usage: python intake_grok500_folders.py --input-dir PATH [--extract]
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from datetime import datetime, timezone
import json
import os
from pathlib import Path, PurePosixPath
import stat
import sys

import intake_grok500 as core

HERE = Path(__file__).resolve().parent
PARTS = [f'LAG-500-MASTER-part{i:02}' for i in range(1, 9)]
SHOTS = {f'{p}{i}' for p in ('V', 'S') for i in range(1, 6)}
GUIDE = 'NOVA-GUIDE-500.md'
LEGEND = 'LEGEND-500.csv'


def io_path(path):
    """Extended Windows I/O only; manifests keep ordinary portable paths."""
    text = str(Path(path).absolute())
    if os.name == 'nt' and not text.startswith('\\\\?\\'):
        text = '\\\\?\\UNC\\' + text[2:] if text.startswith('\\\\') else '\\\\?\\' + text
    return Path(text)


def output_path(root, relative):
    root = core.safe_path(root)
    normal = root / core.member_path(str(relative).replace('\\', '/'))
    if not normal.is_relative_to(root):
        raise core.IntakeError('Output escapes the resolved intake root.')
    for candidate in [normal, *normal.parents]:
        p = io_path(candidate)
        if p.exists() or p.is_symlink():
            s = p.lstat()
            if p.is_symlink() or (getattr(s, 'st_file_attributes', 0) & 0x400):
                raise core.IntakeError(f'Symlink/reparse output rejected: {normal}')
    return io_path(normal)


def verify_folder_extracted(plan):
    root = core.safe_path(plan['intake_root'])
    for rec in plan['files']:
        p = output_path(root, rec['relative_path'])
        if not p.is_file() or p.stat().st_size != rec['bytes'] or core.file_hash(p) != rec['sha256']:
            raise core.IntakeError(f'Extracted size/hash mismatch: {rec["relative_path"]}')
        if 'image' in rec and core.decode_image(p.read_bytes(), p.name) != rec['image']:
            raise core.IntakeError(f'Extracted decode differs: {rec["relative_path"]}')
    for rel in plan['directories']:
        if not output_path(root, rel).is_dir():
            raise core.IntakeError(f'Missing extracted directory: {rel}')
    return len(plan['files'])


def source_files(folder):
    """Walk only this explicit part, never following links/reparse points."""
    folder = core.safe_path(folder)
    result = []
    stack = [folder]
    while stack:
        current = stack.pop()
        for child in sorted(current.iterdir(), key=lambda p: p.name):
            checked = core.safe_path(child)
            if not checked.is_relative_to(folder):
                raise core.IntakeError(f'Input escapes the named part: {child}')
            mode = checked.stat().st_mode
            rel = core.member_path(child.relative_to(folder).as_posix())
            if stat.S_ISDIR(mode):
                result.append((checked, rel, True))
                stack.append(checked)
            elif stat.S_ISREG(mode):
                result.append((checked, rel, False))
            else:
                raise core.IntakeError(f'Special filesystem input rejected: {child}')
            if len(result) > core.MAX_FILES:
                raise core.IntakeError('Input member count exceeds configured limit.')
    return sorted(result, key=lambda row: row[1].as_posix())


def read_legend(path):
    with path.open('r', encoding='utf-8-sig', newline='') as f:
        rows = list(csv.DictReader(f))
    needed = {'row', 'look_num', 'look_slug', 'shot', 'filename', 'zip_name',
              'qa_status', 'qa_note', 'hero', 'breather', 'arm_worm'}
    if len(rows) != 500 or not rows or not needed.issubset(rows[0]):
        raise core.IntakeError('LEGEND must have exactly 500 rows and the expected columns.')
    if {r['row'] for r in rows} != {str(i) for i in range(1, 501)}:
        raise core.IntakeError('LEGEND row IDs must be exactly 1 through 500.')
    if {r['look_num'] for r in rows} != {f'L{i:02}' for i in range(1, 51)}:
        raise core.IntakeError('LEGEND must contain exactly looks L01 through L50.')
    for look in {r['look_num'] for r in rows}:
        group = [r for r in rows if r['look_num'] == look]
        if len(group) != 10 or {r['shot'] for r in group} != SHOTS:
            raise core.IntakeError(f'LEGEND requires V1-V5 and S1-S5 once each: {look}')
        if len({r['look_slug'] for r in group}) != 1:
            raise core.IntakeError(f'Conflicting LEGEND look slug: {look}')
    for row in rows:
        for field in ('filename', 'zip_name', 'look_slug'):
            if core.member_path(row[field]).name != row[field]:
                raise core.IntakeError(f'LEGEND {field} must be a safe basename.')
        if row['zip_name'] != row['look_slug'] + '.zip':
            raise core.IntakeError('LEGEND ZIP and look slug disagree.')
    return rows


def reconcile(scan, rows):
    """Reconcile exact CSV ZIP/member pairs, not inferred filename categories."""
    if len(scan.archives) != 50 or any(a['nested_depth'] for a in scan.archives):
        raise core.IntakeError('Exactly 50 per-look ZIPs required; unexpected nested archives.')
    archives = {}
    for a in scan.archives:
        name = Path(a['source_path']).name
        if name in archives:
            raise core.IntakeError(f'Duplicate per-look ZIP basename: {name}')
        archives[name] = a
    if set(archives) != {r['zip_name'] for r in rows}:
        raise core.IntakeError('Received look ZIP names do not exactly match LEGEND.')
    images = [r for r in scan.files if 'image' in r]
    lookup = {(r['source_archive'], r['source_member']): r for r in images}
    if len(lookup) != len(images):
        raise core.IntakeError('Duplicate image source/member mapping.')
    mapped, expected = [], set()
    for row in rows:
        aid = archives[row['zip_name']]['archive_id']
        member = f"{row['look_slug']}/{row['filename']}"
        pair = (aid, member)
        if pair in expected or pair not in lookup:
            raise core.IntakeError(f'CSV image missing/duplicated: {aid}!{member}')
        rec = lookup[pair]
        expected.add(pair)
        mapped.append({'row': int(row['row']), 'look_num': row['look_num'],
                       'look_slug': row['look_slug'], 'shot': row['shot'],
                       'filename': row['filename'], 'zip_name': row['zip_name'],
                       'relative_path': rec['relative_path'], 'sha256': rec['sha256'],
                       'bytes': rec['bytes'], 'image': rec['image']})
    contacts = []
    for slug in sorted({r['look_slug'] for r in rows}):
        aid = archives[slug + '.zip']['archive_id']
        pair = (aid, f'{slug}/CONTACT-{slug}.jpg')
        if pair not in lookup:
            raise core.IntakeError(f'Missing exact per-look contact sheet: {slug}')
        expected.add(pair)
        contacts.append({k: lookup[pair][k] for k in ('relative_path', 'sha256', 'bytes', 'image')})
    index_pair = ('folder:' + PARTS[0], 'CONTACT-INDEX.jpg')
    if index_pair not in lookup:
        raise core.IntakeError('Missing part01 CONTACT-INDEX.jpg.')
    expected.add(index_pair)
    if expected != set(lookup):
        raise core.IntakeError('Unexpected image files outside 500 CSV sources, 50 contacts and index.')
    return {'status': 'exact_500_source_rows_50_contacts_and_index_matched',
            'source_images': sorted(mapped, key=lambda r: r['row']),
            'contact_sheets': contacts,
            'index': {k: lookup[index_pair][k] for k in ('relative_path', 'sha256', 'bytes', 'image')},
            'source_count': 500, 'contact_count': 50, 'index_count': 1,
            'unique_source_image_hashes': len({r['sha256'] for r in mapped}),
            'role_basis': 'Exact CSV ZIP/member mapping and exact contact/index paths; no visual design acceptance.'}


def inspect_folders(input_dir, intake_root, writer=None):
    source = core.safe_path(input_dir)
    root = core.safe_path(intake_root)
    if not source.is_dir():
        raise core.IntakeError('Input directory does not exist.')
    if root.is_relative_to(source) or source.is_relative_to(root):
        raise core.IntakeError('Input and intake roots must be disjoint; no overlapping extraction.')
    parts = [core.safe_path(source / n) for n in PARTS]
    if any(not p.is_dir() for p in parts):
        raise core.IntakeError('Missing expected outer folder; all eight are required.')
    guide = core.safe_path(source / GUIDE)
    legend = core.safe_path(parts[0] / LEGEND)
    embedded_guide = core.safe_path(parts[0] / GUIDE)
    if not guide.is_file() or not legend.is_file() or not embedded_guide.is_file():
        raise core.IntakeError('Loose guide, part01 guide and part01 LEGEND-500.csv are required.')
    if guide.read_bytes() != embedded_guide.read_bytes():
        raise core.IntakeError('Loose and part01 guide differ; resolve versions before intake.')
    rows = read_legend(legend)
    scan = core.Scanner(root, writer)
    inputs, outer = [], []
    for folder in parts:
        prefix = PurePosixPath('content') / folder.name
        scan.reserve(prefix, True)
        inventory = []
        for p, rel, is_dir in source_files(folder):
            if is_dir:
                scan.reserve(prefix / rel, True)
                continue
            if p.stat().st_size > core.MAX_BYTES:
                raise core.IntakeError(f'Input file exceeds configured byte limit: {p}')
            data = p.read_bytes()
            record = {'path': str(p), 'part': folder.name, 'relative_path': rel.as_posix(),
                      'bytes': len(data), 'sha256': core.digest(data)}
            inputs.append(record)
            inventory.append({k: record[k] for k in ('relative_path', 'bytes', 'sha256')})
            if rel.suffix.lower() == '.zip':
                scan.walk(data, folder.name + '/' + rel.as_posix(),
                          prefix / PurePosixPath(rel.as_posix() + '.contents'), p)
            else:
                scan.add_file(prefix / rel, data, 'folder:' + folder.name, rel.as_posix())
        outer.append({'folder': str(folder), 'name': folder.name, 'input_files': len(inventory),
                      'input_bytes': sum(r['bytes'] for r in inventory),
                      'content_manifest_sha256': core.digest(json.dumps(inventory, sort_keys=True).encode()),
                      'outer_archive_present': False, 'outer_archive_crc_verified': None,
                      'outer_crc_reason': 'Received already-unpacked directory; outer ZIP bytes unavailable.'})
    data = guide.read_bytes()
    inputs.append({'path': str(guide), 'part': 'loose_guide', 'relative_path': GUIDE,
                   'bytes': len(data), 'sha256': core.digest(data)})
    scan.add_file(PurePosixPath('guides') / GUIDE, data, 'loose_guide', None)
    mapping = reconcile(scan, rows)
    claims = {'status': 'provider_reported_not_independently_accepted',
              'CSV_QA_counts': dict(Counter(r['qa_status'] for r in rows)),
              'CSV_hero_Y': sum(r['hero'] == 'Y' for r in rows),
              'CSV_breather_Y': sum(r['breather'] == 'Y' for r in rows),
              'CSV_arm_worm_Y': sum(r['arm_worm'] == 'Y' for r in rows),
              'note': 'QA and hero/feature labels are provider reports, not visual verification or promotion.'}
    return {'schema': 'grok500-folder-intake-v1', 'input_root': str(source), 'intake_root': str(root),
            'state': 'inspection_only_no_files_written', 'expected_top_level_parts': 8,
            'verified_top_level_parts': 8, 'outer_folders': outer, 'source_files': inputs,
            'archives': scan.archives, 'files': scan.files, 'directories': sorted(scan.directories),
            'csv_reconciliation': mapping, 'provider_reports': claims,
            'summary': {'outer_folders': 8, 'outer_ZIP_CRC': 'unavailable_no_outer_ZIP_received',
                        'nested_ZIPs_CRC_verified': len(scan.archives), 'source_images': 500,
                        'contact_sheets': 50, 'contact_index_images': 1, 'total_image_files': 551,
                        'extracted_files': len(scan.files), 'extracted_bytes': scan.total,
                        'unique_source_image_hashes': mapping['unique_source_image_hashes'],
                        'ZIP_copies_created': 0},
            'source_guides_unchanged': True, 'new_approvals': [], 'no_catalog_changes': True,
            'zip_deletion_completed': False, 'original_inputs_deleted': False,
            'cleanup': {'performed': False, 'allowed_by_this_wrapper': False,
                        'note': 'Stop at verified receipt; root coordinates any later enumerated ZIP cleanup.'}}


def signature(plan):
    return json.dumps({k: plan[k] for k in ('source_files', 'outer_folders', 'archives', 'files',
                                           'directories', 'csv_reconciliation', 'provider_reports')}, sort_keys=True)


def extract_folders(plan, resume_verified=False):
    root = core.safe_path(plan['intake_root'])
    if (root / 'intake_receipt.json').exists():
        raise core.IntakeError('Existing receipt; refusing overwrite or a second extraction.')
    expected = {r['relative_path']: r for r in plan['files']}
    reused = set()
    if resume_verified and root.exists():
        # Reject extra or changed partial output, including links, before writes.
        allowed_dirs = set(plan['directories'])
        for p in io_path(root).rglob('*'):
            rel = p.relative_to(io_path(root)).as_posix()
            checked = output_path(root, rel)
            if checked.is_dir():
                if rel not in allowed_dirs:
                    raise core.IntakeError(f'Unexpected partial directory: {rel}')
            elif rel not in expected:
                raise core.IntakeError(f'Unexpected partial file: {rel}')
    for rec in plan['files']:
        p = output_path(root, rec['relative_path'])
        if p.exists():
            if not resume_verified:
                raise core.IntakeError(f'Output exists; no overwrite: {p}')
            if not p.is_file() or p.stat().st_size != rec['bytes'] or core.file_hash(p) != rec['sha256']:
                raise core.IntakeError(f'Partial output changed; refusing resume: {rec["relative_path"]}')
            if 'image' in rec and core.decode_image(p.read_bytes(), p.name) != rec['image']:
                raise core.IntakeError(f'Partial image decode differs: {rec["relative_path"]}')
            reused.add(rec['relative_path'])

    def writer(rel, data, rec):
        if rec != expected.get(rel.as_posix()):
            raise core.IntakeError(f'Source changed between inspection and extraction: {rel}')
        p = output_path(root, rel.as_posix())
        if rel.as_posix() in reused:
            if p.stat().st_size != rec['bytes'] or core.file_hash(p) != rec['sha256']:
                raise core.IntakeError(f'Partial file changed during resume: {rel}')
            return
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('xb') as f:
            f.write(data)

    # A fresh complete no-write scan detects source changes before writes begin.
    fresh = inspect_folders(plan['input_root'], root)
    if signature(fresh) != signature(plan):
        raise core.IntakeError('Input changed after inspection; extraction not started.')
    actual = inspect_folders(plan['input_root'], root, writer)
    if signature(actual) != signature(plan):
        raise core.IntakeError('Inputs changed during extraction; preserve ZIPs and inspect partial output.')
    for d in plan['directories']:
        output_path(root, d).mkdir(parents=True, exist_ok=True)
    plan['verified_extracted_files'] = verify_folder_extracted(plan)
    for rec in plan['source_files']:
        p = core.safe_path(rec['path'])
        if p.stat().st_size != rec['bytes'] or core.file_hash(p) != rec['sha256']:
            raise core.IntakeError(f'Original input changed during intake: {p}')
    plan['state'] = 'eight_folders_nested_CRC_csv_hash_size_decode_verified'
    plan['verified_utc'] = datetime.now(timezone.utc).isoformat()
    plan['cleanup']['verification_gate_complete'] = True
    plan['resumed_verified_partial_files'] = len(reused)
    plan['windows_extended_path_io'] = os.name == 'nt'
    core.write_receipt(root, plan)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input-dir', required=True, type=Path)
    ap.add_argument('--intake-root', type=Path, default=HERE / 'received')
    ap.add_argument('--extract', action='store_true')
    ap.add_argument('--resume-verified', action='store_true', help='With --extract only: skip matching partial files; refuse changed or unlisted output.')
    args = ap.parse_args(argv)
    try:
        if args.resume_verified and not args.extract:
            raise core.IntakeError('--resume-verified requires --extract.')
        plan = inspect_folders(args.input_dir, args.intake_root)
        if args.extract:
            extract_folders(plan, args.resume_verified)
        print(json.dumps({k: plan[k] for k in ('state', 'summary', 'provider_reports', 'intake_root', 'cleanup')}, indent=2))
        return 0
    except (core.IntakeError, OSError, csv.Error, ValueError) as exc:
        print(json.dumps({'state': 'blocked_no_cleanup', 'error': str(exc),
                          'note': 'No input deletion or overwrite is performed. Preserve any partial outputs for inspection.'}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
