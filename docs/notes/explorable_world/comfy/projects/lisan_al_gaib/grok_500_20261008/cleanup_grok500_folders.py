"""Dry-run by default; remove only the 50 verified original per-look ZIPs.

The extraction receipt is immutable. A separate cleanup_summary.json journals
each removal. No outer ZIPs, directories, images, guides or other packs removed.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import sys
import zipfile

import intake_grok500 as core
import intake_grok500_folders as folders

HERE = Path(__file__).resolve().parent
WORKSPACE = HERE.parents[6]
INPUT_REL = Path('docs/notes/explorable_world/comfy/references/From Grok')
RECEIPT = HERE / 'received/intake_receipt.json'


def utc():
    return datetime.now(timezone.utc).isoformat()


def scoped_file(path, workspace):
    p = core.safe_path(path)
    if not p.is_relative_to(workspace) or not p.is_file():
        raise core.IntakeError(f'Expected file outside resolved workspace or missing: {p}')
    return p


def prepare(receipt, expected_sha, input_dir, workspace=WORKSPACE):
    """Read-only fresh validation of all output bytes/decode and deletion targets."""
    workspace = core.safe_path(workspace)
    receipt = scoped_file(receipt, workspace)
    if core.file_hash(receipt) != expected_sha:
        raise core.IntakeError('Frozen extraction receipt SHA-256 does not match.')
    saved = json.loads(receipt.read_text(encoding='utf-8'))
    if (saved.get('schema') != 'grok500-folder-intake-v1' or
        saved.get('state') != 'eight_folders_nested_CRC_csv_hash_size_decode_verified' or
        saved.get('verified_top_level_parts') != 8 or saved.get('verified_extracted_files') != 555):
        raise core.IntakeError('Complete eight-folder extraction receipt is required.')
    root = core.safe_path(saved['intake_root'])
    source = core.safe_path(input_dir)
    if root != receipt.parent or not root.is_relative_to(workspace) or not source.is_relative_to(workspace):
        raise core.IntakeError('Intake/input root is outside the explicit workspace or receipt root.')
    if source != core.safe_path(saved['input_root']) or source.is_relative_to(root) or root.is_relative_to(source):
        raise core.IntakeError('Input root mismatch or overlapping roots.')
    if (root / 'cleanup_summary.json').exists() or (root / 'cleanup_summary.next.json').exists():
        raise core.IntakeError('Cleanup journal already exists; refuse a second or ambiguous cleanup.')
    mapping = saved.get('csv_reconciliation', {})
    if (mapping.get('status') != 'exact_500_source_rows_50_contacts_and_index_matched' or
        mapping.get('source_count') != 500 or mapping.get('contact_count') != 50 or
        mapping.get('index_count') != 1 or len(mapping.get('source_images', [])) != 500 or
        len(mapping.get('contact_sheets', [])) != 50 or len(saved['files']) != 555):
        raise core.IntakeError('Required exact 500/50/index reconciliation is missing.')
    named_parts = {core.safe_path(source / name) for name in folders.PARTS}
    if len(named_parts) != 8 or any(not p.is_dir() for p in named_parts):
        raise core.IntakeError('All eight exact source part directories must still exist.')
    if {a['name'] for a in saved['outer_folders']} != set(folders.PARTS):
        raise core.IntakeError('Outer folder receipt names do not match expected eight parts.')
    archives = saved['archives']
    expected_zips = {r['zip_name'] for r in mapping['source_images']}
    if len(archives) != 50 or len(expected_zips) != 50:
        raise core.IntakeError('Exactly 50 CSV-mapped per-look ZIPs must be enumerated.')
    targets = []
    for a in archives:
        p = scoped_file(a['source_path'], workspace)
        # This strict parent equality excludes outer parts, Processed and every
        # unrelated pack, even when other ZIPs are under the same From Grok root.
        if (p.parent not in named_parts or p.name not in expected_zips or
            p.suffix.lower() != '.zip' or a.get('nested_depth') != 0):
            raise core.IntakeError(f'ZIP is outside the exact permitted source-part scope: {p}')
        if p.stat().st_size != a['bytes'] or core.file_hash(p) != a['sha256']:
            raise core.IntakeError(f'Original ZIP size/hash changed: {p}')
        with zipfile.ZipFile(p) as z:
            if len(z.infolist()) != a['member_count'] or z.testzip() is not None:
                raise core.IntakeError(f'Fresh ZIP CRC/member verification failed: {p}')
        targets.append({'path': str(p), 'repo_path': p.relative_to(workspace).as_posix(),
                        'archive_id': a['archive_id'], 'bytes': a['bytes'], 'sha256': a['sha256'],
                        'fresh_crc_verified': True, 'part_directory': p.parent.name})
    if len({t['path'].casefold() for t in targets}) != 50 or {Path(t['path']).name for t in targets} != expected_zips:
        raise core.IntakeError('Duplicate or incomplete ZIP deletion target list.')
    verified_outputs = folders.verify_folder_extracted(saved)
    # Check every original input too; retain the source docs/index/loose guide.
    preserved = []
    target_paths = {t['path'] for t in targets}
    for rec in saved['source_files']:
        p = scoped_file(rec['path'], workspace)
        if p.stat().st_size != rec['bytes'] or core.file_hash(p) != rec['sha256']:
            raise core.IntakeError(f'Original input changed: {p}')
        if str(p) not in target_paths:
            preserved.append({k: rec[k] for k in ('path', 'bytes', 'sha256')})
    if len(preserved) != 5:
        raise core.IntakeError('Expected five preserved non-ZIP original inputs.')
    return {'schema': 'grok500-folder-cleanup-v1', 'state': 'verified_dry_run_no_files_removed',
            'prepared_at_utc': utc(), 'workspace': str(workspace), 'input_root': str(source),
            'intake_root': str(root), 'extraction_receipt': str(receipt),
            'extraction_receipt_sha256': expected_sha, 'targets': targets,
            'target_count': 50, 'target_bytes': sum(t['bytes'] for t in targets),
            'verified_output_files_before_cleanup': verified_outputs,
            'preserved_original_inputs': preserved, 'removed': [], 'zip_files_removed': 0,
            'bytes_freed': 0, 'outer_ZIPs_removed': 0, 'directories_removed': 0,
            'image_or_document_files_removed': 0, 'no_catalog_changes': True,
            'new_approvals': [], 'source_folder_scope': folders.PARTS,
            'cleanup_complete': False}


def write_journal(plan):
    root = core.safe_path(plan['intake_root'])
    target = core.safe_path(root / 'cleanup_summary.json')
    temporary = core.safe_path(root / 'cleanup_summary.next.json')
    if not target.is_relative_to(root) or not temporary.is_relative_to(root):
        raise core.IntakeError('Cleanup journal escapes intake root.')
    with temporary.open('x', encoding='utf-8') as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)
        f.write('\n')
    os.replace(temporary, target)


def execute(plan):
    # Validate again rather than trusting an earlier dry-run or caller-built plan.
    fresh = prepare(plan['extraction_receipt'], plan['extraction_receipt_sha256'],
                    plan['input_root'], plan['workspace'])
    if fresh['targets'] != plan['targets']:
        raise core.IntakeError('Deletion targets changed after dry-run.')
    plan = fresh
    plan['state'] = 'verified_cleanup_in_progress'
    plan['started_at_utc'] = utc()
    write_journal(plan)
    workspace = core.safe_path(plan['workspace'])
    named_parts = {core.safe_path(Path(plan['input_root']) / n) for n in folders.PARTS}
    try:
        for target in plan['targets']:
            p = scoped_file(target['path'], workspace)
            if (p.parent not in named_parts or p.suffix.lower() != '.zip' or
                p.stat().st_size != target['bytes'] or core.file_hash(p) != target['sha256']):
                raise core.IntakeError(f'ZIP changed or escaped scope immediately before removal: {p}')
            # Exactly one already-enumerated regular file. Never recurse/remove folders.
            p.unlink()
            plan['removed'].append({**target, 'removed_at_utc': utc()})
            plan['zip_files_removed'] = len(plan['removed'])
            plan['bytes_freed'] += target['bytes']
            write_journal(plan)
        receipt = scoped_file(plan['extraction_receipt'], workspace)
        if core.file_hash(receipt) != plan['extraction_receipt_sha256']:
            raise core.IntakeError('Extraction receipt changed during cleanup.')
        saved = json.loads(receipt.read_text(encoding='utf-8'))
        plan['verified_output_files_after_cleanup'] = folders.verify_folder_extracted(saved)
        for rec in plan['preserved_original_inputs']:
            p = scoped_file(rec['path'], workspace)
            if p.stat().st_size != rec['bytes'] or core.file_hash(p) != rec['sha256']:
                raise core.IntakeError(f'Preserved source input changed: {p}')
        if any(core.safe_path(t['path']).exists() for t in plan['targets']) or any(not p.is_dir() for p in named_parts):
            raise core.IntakeError('Final target absence/directory preservation check failed.')
        plan['state'] = 'fifty_verified_nested_ZIPs_removed_outputs_and_sources_preserved'
        plan['cleanup_complete'] = True
        plan['completed_at_utc'] = utc()
        plan['extraction_receipt_unchanged'] = True
        write_journal(plan)
        return plan
    except Exception as exc:
        plan['state'] = 'cleanup_interrupted_review_journal_before_any_retry'
        plan['error'] = str(exc)
        plan['failed_at_utc'] = utc()
        write_journal(plan)
        raise


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--input-dir', required=True, type=Path)
    ap.add_argument('--expected-receipt-sha256', required=True)
    ap.add_argument('--execute', action='store_true')
    args = ap.parse_args(argv)
    try:
        if core.safe_path(args.input_dir) != core.safe_path(WORKSPACE / INPUT_REL):
            raise core.IntakeError('CLI cleanup permits only this CFA From Grok input root.')
        plan = prepare(RECEIPT, args.expected_receipt_sha256, args.input_dir)
        if args.execute:
            plan = execute(plan)
        print(json.dumps({k: plan[k] for k in ('state', 'target_count', 'target_bytes', 'zip_files_removed',
                                               'bytes_freed', 'cleanup_complete', 'extraction_receipt_sha256')}, indent=2))
        return 0
    except (core.IntakeError, OSError, ValueError, zipfile.BadZipFile) as exc:
        print(json.dumps({'error': str(exc), 'note': 'No broad cleanup. Inspect cleanup_summary.json if a partial removal journal exists.'}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
