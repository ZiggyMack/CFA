"""Bounded, byte-preserving ZIP intake; inspect by default. No provider execution.

Requires Python 3.10+ and Pillow. Extraction creates new paths only. ZIP cleanup
requires a complete eight-part inspection, a verified extraction receipt and a
fresh byte/decode verification. No catalog, acceptance or hero-selection edits.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import unicodedata
import warnings
import zipfile

from PIL import Image, ImageSequence

HERE = Path(__file__).resolve().parent
IMAGE_EXTS = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.bmp', '.tif', '.tiff', '.avif'}
DOC_EXTS = {'.txt', '.md', '.csv', '.json', '.tsv', '.pdf', '.html'}
MAX_DEPTH = 8
MAX_FILES = 20000
MAX_BYTES = 2 * 1024 ** 3
MAX_RATIO = 2000
MAX_PIXELS = 100_000_000


class IntakeError(ValueError):
    pass


def digest(data):
    return hashlib.sha256(data).hexdigest()


def file_hash(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def safe_path(path):
    """Reject existing symlinks/reparse points before resolving a local path."""
    raw = Path(os.path.abspath(os.fspath(path)))
    for p in [raw, *raw.parents]:
        if p.exists() or p.is_symlink():
            s = p.lstat()
            if p.is_symlink() or (getattr(s, 'st_file_attributes', 0) & 0x400):
                raise IntakeError(f'Symlink/reparse path rejected: {p}')
    return raw.resolve()


def member_path(name):
    if not name or '\\' in name or '\x00' in name or name.startswith('/'):
        raise IntakeError(f'Unsafe ZIP name: {name!r}')
    trimmed = name[:-1] if name.endswith('/') else name
    parts = trimmed.split('/')
    for p in parts:
        if not p or p in ('.', '..') or p.endswith((' ', '.')) or re.search(r'[<>:"|?*\x00-\x1f]', p):
            raise IntakeError(f'Unsafe ZIP path component: {name!r}')
        device = p.split('.')[0].upper()
        if device in {'CON', 'PRN', 'AUX', 'NUL', 'CLOCK$'} or re.fullmatch(r'(COM|LPT)[1-9¹²³]', device):
            raise IntakeError(f'Reserved Windows filename: {name!r}')
    return PurePosixPath(*parts)


def key(path):
    return unicodedata.normalize('NFC', path.as_posix()).casefold()


def decode_image(data, filename):
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('error', Image.DecompressionBombWarning)
            with Image.open(io.BytesIO(data)) as im:
                im.verify()
            with Image.open(io.BytesIO(data)) as im:
                pixels = 0
                frames = 0
                width, height = im.size
                mode = im.mode
                for frame in ImageSequence.Iterator(im):
                    pixels += frame.width * frame.height
                    frames += 1
                    if pixels > MAX_PIXELS or frames > 1000:
                        raise IntakeError(f'Image decode budget exceeded: {filename}')
                    frame.load()
                return {'width': width, 'height': height, 'mode': mode, 'frames': frames, 'decoded': True}
    except Exception as exc:
        raise IntakeError(f'Image decode failed for {filename}: {exc}') from exc


def expected_config(path):
    obj = json.loads(Path(path).read_text(encoding='utf-8-sig'))
    names = obj if isinstance(obj, list) else obj.get('expected_archives', [])
    if len(names) != 8 or len({n.casefold() for n in names}) != 8:
        raise IntakeError('Exactly eight distinct expected archive filenames are required.')
    for n in names:
        if member_path(n).name != n or not n.lower().endswith('.zip'):
            raise IntakeError(f'Expected name must be one ZIP basename: {n}')
    return names, (obj if isinstance(obj, dict) else {})


def resolve_inputs(names, input_dir=None, archives=None, guide=None, guide_name='NOVA-GUIDE-500.md'):
    if bool(input_dir) == bool(archives):
        raise IntakeError('Choose --input-dir OR an explicit list using --archive.')
    input_root = safe_path(input_dir) if input_dir else None
    if input_root and not input_root.is_dir():
        raise IntakeError(f'Input directory not found: {input_root}')
    paths = [input_root / n for n in names] if input_root else [safe_path(p) for p in archives]
    actual = [p.name for p in paths]
    if len(paths) != 8 or len(set(actual)) != 8 or set(actual) != set(names):
        raise IntakeError('Input list must match all eight expected basenames exactly; no duplicates or substitutes.')
    ordered = {p.name: p for p in paths}
    paths = [safe_path(ordered[n]) for n in names]
    missing = [str(p) for p in paths if not p.is_file()]
    if missing:
        raise IntakeError('Missing expected archive(s): ' + ', '.join(missing))
    gp = safe_path(guide) if guide else (safe_path(input_root / guide_name) if input_root else None)
    if not gp or not gp.is_file() or gp.name != guide_name:
        raise IntakeError(f'The exact loose guide {guide_name} is required (--guide for explicit archive lists).')
    return paths, gp, input_root


class Scanner:
    def __init__(self, root, writer=None):
        self.root = safe_path(root)
        self.writer = writer
        self.files = []
        self.archives = []
        self.directories = set()
        self.occupied = {}
        self.total = 0
        self.entries = 0

    def reserve(self, rel, is_dir=False):
        k = key(rel)
        if k in self.occupied:
            # An explicit directory may follow an implicitly created parent once.
            if is_dir and self.occupied[k] == 'implicit_dir':
                self.occupied[k] = 'dir'
                self.directories.add(rel.as_posix())
                return
            raise IntakeError(f'Case-insensitive or duplicate output collision: {rel}')
        for parent in rel.parents:
            if str(parent) == '.':
                continue
            pk = key(parent)
            if self.occupied.get(pk) == 'file':
                raise IntakeError(f'File/directory path collision: {rel}')
            self.occupied.setdefault(pk, 'implicit_dir')
            self.directories.add(parent.as_posix())
        self.occupied[k] = 'dir' if is_dir else 'file'
        if is_dir:
            self.directories.add(rel.as_posix())

    def add_file(self, rel, data, source, member=None):
        self.reserve(rel)
        self.entries += 1
        self.total += len(data)
        if self.entries > MAX_FILES or self.total > MAX_BYTES:
            raise IntakeError('Total extraction budget exceeded; no ZIP cleanup allowed.')
        suffix = rel.suffix.lower()
        category = 'archive_copy' if suffix == '.zip' else 'provider_document' if suffix in DOC_EXTS else 'other'
        rec = {'relative_path': rel.as_posix(), 'bytes': len(data), 'sha256': digest(data), 'kind': category,
               'source_archive': source, 'source_member': member}
        if suffix in IMAGE_EXTS:
            rec['image'] = decode_image(data, rel)
            if re.search(r'contact', rel.name, re.I):
                rec['kind'] = 'contact_sheet_filename_candidate'
            elif re.search(r'(^|[-_ ])(index|overview)([-_. ]|$)', rel.name, re.I):
                rec['kind'] = 'index_image_filename_candidate'
            else:
                rec['kind'] = 'source_image_filename_candidate'
        self.files.append(rec)
        if self.writer:
            self.writer(rel, data, rec)

    def walk(self, data, archive_id, prefix, source_path, depth=0):
        if depth > MAX_DEPTH:
            raise IntakeError(f'Nested ZIP depth exceeds {MAX_DEPTH}: {archive_id}')
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as z:
                infos = z.infolist()
                # Budget/header/path checks happen before the CRC test decompresses data.
                if self.entries + len(infos) > MAX_FILES:
                    raise IntakeError('ZIP member count exceeds configured limit.')
                claimed = sum(i.file_size for i in infos)
                if claimed + self.total > MAX_BYTES:
                    raise IntakeError('ZIP uncompressed size exceeds configured limit.')
                for info in infos:
                    # ZipInfo can normalize Windows separators or truncate NULs;
                    # reject the original name before trusting that conversion.
                    member_path(info.orig_filename)
                    member_path(info.filename)
                    typ = stat.S_IFMT(info.external_attr >> 16)
                    if typ not in (0, stat.S_IFREG, stat.S_IFDIR) or info.external_attr & 0x400:
                        raise IntakeError(f'Symlink/special/reparse ZIP member rejected: {info.filename}')
                    if info.flag_bits & 1:
                        raise IntakeError(f'Encrypted ZIP member not supported: {info.filename}')
                    if info.file_size > max(1, info.compress_size) * MAX_RATIO:
                        raise IntakeError(f'ZIP compression ratio exceeds limit: {info.filename}')
                bad = z.testzip()
                if bad is not None:
                    raise IntakeError(f'CRC failed: {archive_id}!{bad}')
                self.archives.append({'archive_id': archive_id, 'source_path': str(source_path),
                                      'bytes': len(data), 'sha256': digest(data), 'member_count': len(infos),
                                      'crc_verified': True, 'nested_depth': depth})
                for info in infos:
                    rel = prefix / member_path(info.filename)
                    if info.is_dir():
                        self.reserve(rel, True)
                        continue
                    payload = z.read(info)
                    if len(payload) != info.file_size:
                        raise IntakeError(f'ZIP size mismatch: {archive_id}!{info.filename}')
                    self.add_file(rel, payload, archive_id, info.filename)
                    if rel.suffix.lower() == '.zip':
                        self.walk(payload, archive_id + '!' + info.filename,
                                  PurePosixPath(rel.as_posix() + '.contents'), self.root / rel.as_posix(), depth + 1)
        except (zipfile.BadZipFile, RuntimeError, NotImplementedError, OSError) as exc:
            raise IntakeError(f'Cannot verify archive {archive_id}: {exc}') from exc


def inspect(archives, guide, intake_root, writer=None, provider_claims=None):
    scan = Scanner(intake_root, writer)
    for p in archives:
        p = safe_path(p)
        scan.walk(p.read_bytes(), p.name, PurePosixPath('content') / p.stem, p)
    scan.add_file(PurePosixPath('guides') / guide.name, guide.read_bytes(), 'loose_guide', None)
    images = [x for x in scan.files if 'image' in x]
    counts = Counter(x['kind'] for x in scan.files)
    return {'schema': 'grok500-intake-v1', 'intake_root': str(scan.root),
            'expected_top_level_parts': 8, 'verified_top_level_parts': len(archives),
            'archives': scan.archives, 'files': scan.files, 'directories': sorted(scan.directories),
            'summary': {'total_files_including_nested_zip_copies': len(scan.files), 'archive_count_outer_and_nested': len(scan.archives),
                        'total_image_files': len(images), 'unique_image_hashes': len({x['sha256'] for x in images}),
                        'filename_classification': dict(counts), 'classification_note': 'Filename-based buckets are candidates, not visual or provider-role verification.'},
            'provider_claims': {'status': 'unverified_provider_report', 'values': provider_claims or {},
                                'note': 'Provider QA, clean/drift/flagged and hero labels are not independent verification or acceptance. Source guides/maps are preserved unchanged.'},
            'no_catalog_changes': True, 'new_approvals': [], 'zip_deletion_completed': False}


def stable_manifest(plan):
    return json.dumps({'files': plan['files'], 'archives': plan['archives'], 'directories': plan['directories']}, sort_keys=True)


def write_receipt(root, plan):
    root = safe_path(root)
    root.mkdir(parents=True, exist_ok=True)
    target = root / 'intake_receipt.json'
    safe_path(target)
    tmp = root / 'intake_receipt.next.json'
    with tmp.open('x', encoding='utf-8') as f:
        json.dump(plan, f, indent=2, ensure_ascii=False)
        f.write('\n')
    os.replace(tmp, target)


def verify_extracted(plan, skip_deleted=False):
    root = safe_path(plan['intake_root'])
    deleted = {r['path'] for r in plan.get('deleted_zip_copies', [])} if skip_deleted else set()
    count = 0
    for rec in plan['files']:
        p = safe_path(root / rec['relative_path'])
        if not p.is_relative_to(root):
            raise IntakeError('Manifest output escapes intake root.')
        if str(p) in deleted and rec['kind'] == 'archive_copy':
            if p.exists():
                raise IntakeError(f'Removed ZIP unexpectedly exists: {p}')
            continue
        if not p.is_file() or p.stat().st_size != rec['bytes'] or file_hash(p) != rec['sha256']:
            raise IntakeError(f'Extracted size/hash mismatch: {p}')
        if 'image' in rec:
            actual = decode_image(p.read_bytes(), p.name)
            if actual != rec['image']:
                raise IntakeError(f'Extracted image metadata differs: {p}')
        count += 1
    for d in plan['directories']:
        p = safe_path(root / d)
        if not p.is_relative_to(root) or not p.is_dir():
            raise IntakeError(f'Missing or unsafe extracted directory: {p}')
    return count


def extract(plan, archives, guide):
    root = safe_path(plan['intake_root'])
    if (root / 'intake_receipt.json').exists():
        raise IntakeError('Existing receipt found; refusing a second extraction/overwrite. Use a new intake root or verify cleanup only.')
    for rec in plan['files']:
        p = safe_path(root / rec['relative_path'])
        if not p.is_relative_to(root) or p.exists():
            raise IntakeError(f'Output exists or escapes intake root; no overwrite: {p}')
    expected = {x['relative_path']: x for x in plan['files']}
    def writer(rel, data, rec):
        if rec != expected.get(rel.as_posix()):
            raise IntakeError(f'Source changed between inspection and extraction: {rel}')
        p = safe_path(root / rel.as_posix())
        if not p.is_relative_to(root):
            raise IntakeError('Unsafe extraction path.')
        p.parent.mkdir(parents=True, exist_ok=True)
        with p.open('xb') as f:
            f.write(data)
    actual = inspect(archives, guide, root, writer, plan['provider_claims']['values'])
    if stable_manifest(actual) != stable_manifest(plan):
        raise IntakeError('Sources changed during extraction. Keep all ZIPs; inspect partial outputs manually.')
    for d in plan['directories']:
        p = safe_path(root / d)
        p.mkdir(parents=True, exist_ok=True)
    plan['verified_extracted_files'] = verify_extracted(plan)
    plan['state'] = 'all_eight_extracted_crc_hash_size_decode_verified'
    plan['verified_utc'] = datetime.now(timezone.utc).isoformat()
    write_receipt(root, plan)


def delete_verified_zips(plan, input_root=None):
    root = safe_path(plan['intake_root'])
    receipt = root / 'intake_receipt.json'
    if not receipt.is_file():
        raise IntakeError('ZIP cleanup needs a completed verified extraction receipt.')
    saved = json.loads(receipt.read_text(encoding='utf-8'))
    if saved.get('state') != 'all_eight_extracted_crc_hash_size_decode_verified' or stable_manifest(saved) != stable_manifest(plan):
        raise IntakeError('Receipt is not complete or does not match freshly inspected archives.')
    if plan['verified_top_level_parts'] != 8:
        raise IntakeError('All eight parts are required before any ZIP removal.')
    verify_extracted(plan)
    allowed = [root]
    if input_root:
        allowed.append(safe_path(input_root))
    targets = []
    for archive in plan['archives']:
        p = safe_path(archive['source_path'])
        if p.suffix.lower() != '.zip' or not any(p.is_relative_to(a) for a in allowed):
            raise IntakeError(f'ZIP is outside resolved intake root/explicit input directory: {p}')
        if not p.is_file() or p.stat().st_size != archive['bytes'] or file_hash(p) != archive['sha256']:
            raise IntakeError(f'ZIP changed before cleanup: {p}')
        targets.append((p, archive))
    if len({str(p).casefold() for p, _ in targets}) != len(targets):
        raise IntakeError('Duplicate ZIP deletion targets; refusing cleanup.')
    plan['deleted_zip_copies'] = []
    plan['state'] = 'verified_cleanup_in_progress'
    write_receipt(root, plan)
    # Only the individually verified files above are removed. Never enumerate a
    # directory for deletion, recurse, remove folders, or follow a symlink.
    for p, archive in targets:
        checked = safe_path(p)
        if checked != p or file_hash(p) != archive['sha256']:
            raise IntakeError(f'ZIP changed during cleanup; partial state recorded: {p}')
        p.unlink()
        plan['deleted_zip_copies'].append({'path': str(p), 'sha256': archive['sha256'], 'bytes': archive['bytes']})
        write_receipt(root, plan)
    plan['verified_remaining_files'] = verify_extracted(plan, skip_deleted=True)
    plan['state'] = 'verified_extracted_zip_copies_removed'
    plan['zip_deletion_completed'] = True
    plan['deletion_completed_utc'] = datetime.now(timezone.utc).isoformat()
    write_receipt(root, plan)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    choice = ap.add_mutually_exclusive_group(required=True)
    choice.add_argument('--input-dir', type=Path)
    choice.add_argument('--archive', type=Path, action='append', help='Repeat for each exact archive; requires --guide.')
    ap.add_argument('--guide', type=Path)
    ap.add_argument('--expected-names-file', type=Path, default=HERE / 'expected_archives.json')
    ap.add_argument('--intake-root', type=Path, default=HERE / 'received')
    ap.add_argument('--delete-input-dir', type=Path, help='Explicit allowable archive directory for --archive cleanup; does not widen extraction scope.')
    ap.add_argument('--extract', action='store_true')
    ap.add_argument('--delete-verified-zips', action='store_true')
    args = ap.parse_args(argv)
    try:
        names, cfg = expected_config(args.expected_names_file)
        archives, guide, input_root = resolve_inputs(names, args.input_dir, args.archive, args.guide, cfg.get('expected_loose_guide', 'NOVA-GUIDE-500.md'))
        claims = cfg.copy()
        pending = HERE / 'intake_status.json'
        if pending.is_file():
            claims['pending_receipt_sha256'] = file_hash(pending)
            claims['reported_qa'] = json.loads(pending.read_text(encoding='utf-8')).get('provider_reported', {})
        plan = inspect(archives, guide, args.intake_root, provider_claims=claims)
        plan['state'] = 'inspection_only_no_files_written'
        if args.extract:
            extract(plan, archives, guide)
        if args.delete_verified_zips:
            delete_verified_zips(plan, args.delete_input_dir or input_root)
        print(json.dumps({'state': plan['state'], 'summary': plan['summary'], 'provider_claims': plan['provider_claims'],
                          'intake_root': plan['intake_root'], 'zip_deletion_completed': plan['zip_deletion_completed']}, indent=2))
        return 0
    except (IntakeError, OSError, json.JSONDecodeError) as exc:
        print(json.dumps({'state': 'blocked_no_cleanup_completion_claim', 'error': str(exc),
                          'note': 'No blanket deletion is performed. If extraction/cleanup was interrupted, inspect the receipt and partial outputs; do not rerun extraction over them.'}), file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
