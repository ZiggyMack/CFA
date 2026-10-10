"""Verify/extract five received Grok ZIPs into a deduplicated content store.

No network, source moves/deletions, provider code execution or catalog changes.
Run with --extract to write; the default is a read-only inspection.
"""
from collections import Counter
from datetime import datetime, timezone
from io import BytesIO
from pathlib import Path, PurePosixPath
import argparse
import hashlib
import json
import os
import re
import stat
import unicodedata
from urllib.parse import unquote
import warnings
import zipfile
import zlib

from PIL import Image, ImageSequence

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[6]
INPUT = ROOT / 'docs/notes/explorable_world/comfy/references/From Grok'
CATALOG = HERE.parents[1] / 'visual_library/catalog.js'
EXPECTED = {
    'GROK-BOSS-DISCOVERY-20261008_round01_return_v001.zip',
    'GROK-HD-20261008_return_v001.zip',
    'GROK-HD-20261008_return_v002.zip',
    'GROK-HD-20261008_hip_rollout_v001.zip',
    'GROK-HD-20261008_recovery_inventory.zip',
}
IMAGE_EXTS = {'.png', '.jpg', '.jpeg', '.webp', '.gif', '.bmp', '.tif', '.tiff'}
MAX_FILES = 10000
MAX_BYTES = 1024 * 1024 * 1024
MAX_FILE_BYTES = 512 * 1024 * 1024


def io_path(path):
    text = str(Path(path).absolute())
    if os.name == 'nt' and not text.startswith('\\\\?\\'):
        text = '\\\\?\\UNC\\' + text[2:] if text.startswith('\\\\') else '\\\\?\\' + text
    return Path(text)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def checked_path(path):
    path = Path(path).resolve()
    if not path.is_relative_to(ROOT):
        raise ValueError('Filesystem access outside CFA is not allowed.')
    return path


def relative(path):
    return checked_path(path).relative_to(ROOT).as_posix()


def safe_members(infos):
    """Validate names/types before any member is read or written."""
    if len(infos) > MAX_FILES:
        raise ValueError('Archive entry limit exceeded.')
    seen, files = set(), set()
    for info in infos:
        raw = info.orig_filename
        if not raw or '\x00' in raw or '\\' in raw or ':' in raw or raw.startswith('/'):
            raise ValueError('Unsafe ZIP member name: ' + repr(raw))
        path = PurePosixPath(raw)
        if path.is_absolute() or '..' in path.parts or any(x in {'', '.'} for x in raw.rstrip('/').split('/')):
            raise ValueError('Traversal or ambiguous ZIP member: ' + raw)
        for part in path.parts:
            if part.rstrip(' .') != part or re.fullmatch(r'(?i)(con|prn|aux|nul|com[1-9]|lpt[1-9])', part.split('.')[0]):
                raise ValueError('Unsafe Windows filename: ' + raw)
        key = unicodedata.normalize('NFC', path.as_posix()).casefold()
        if key in seen:
            raise ValueError('Duplicate/case-colliding ZIP member: ' + raw)
        seen.add(key)
        mode = info.external_attr >> 16
        if stat.S_ISLNK(mode) or stat.S_IFMT(mode) not in {0, stat.S_IFREG, stat.S_IFDIR}:
            raise ValueError('Symlink or special ZIP member: ' + raw)
        if info.flag_bits & 1:
            raise ValueError('Encrypted ZIP member is unsupported: ' + raw)
        if info.file_size > MAX_FILE_BYTES:
            raise ValueError('Member size limit exceeded.')
        if not info.is_dir():
            files.add(key)
    for key in seen:
        if any(parent.as_posix() in files for parent in PurePosixPath(key).parents if parent.as_posix() != '.'):
            raise ValueError('ZIP file/directory prefix collision: ' + key)


def decode_image(raw, name):
    with warnings.catch_warnings():
        warnings.simplefilter('error', Image.DecompressionBombWarning)
        with Image.open(BytesIO(raw)) as image:
            width, height = image.size
            if width * height > 100_000_000:
                raise ValueError('Image pixel limit exceeded: ' + name)
            fmt, mode = image.format, image.mode
            frames, total_pixels = 0, 0
            alpha_extrema = None
            for frame in ImageSequence.Iterator(image):
                frame.load()
                frames += 1
                total_pixels += frame.width * frame.height
                if frames > 512 or total_pixels > 250_000_000:
                    raise ValueError('Animated image decode limit exceeded: ' + name)
                if frames == 1 and 'A' in frame.getbands():
                    alpha_extrema = list(frame.getchannel('A').getextrema())
            return {'width': width, 'height': height, 'format': fmt, 'mode': mode,
                    'frames': frames, 'decoded': True, 'alpha_extrema': alpha_extrema}


def discover():
    folders = [INPUT / f'GROK-HD-MASTER-20261009_part{i}of2' for i in (1, 2)]
    files = [checked_path(p) for folder in folders for p in folder.rglob('*') if p.is_file()]
    archives = sorted(p for p in files if p.suffix.lower() == '.zip')
    if len(archives) != 5 or {p.name for p in archives} != EXPECTED:
        raise ValueError('Expected the exact five named Grok return ZIPs.')
    extras = sorted(p for p in files if p.suffix.lower() != '.zip')
    if len(extras) != 2 or any(p.name != 'INDEX.txt' for p in extras):
        raise ValueError('Expected only the two loose INDEX.txt source files.')
    return archives, extras


def inspect_and_extract(extract=False):
    archives, loose_files = discover()
    received = checked_path(HERE / 'received')
    content = checked_path(received / 'content')
    catalog_raw = CATALOG.read_bytes()
    catalog = json.loads(catalog_raw.decode('utf-8-sig').split('=', 1)[1].strip().rstrip(';'))
    catalog_by_sha = {}
    for asset in catalog['assets']:
        if asset.get('sha256'):
            catalog_by_sha.setdefault(asset['sha256'], []).append(asset)
    occurrence_rows, unique, archive_rows = [], {}, []
    total_bytes = 0

    def register(raw, name, occurrence):
        nonlocal total_bytes
        total_bytes += len(raw)
        if total_bytes > MAX_BYTES or len(occurrence_rows) >= MAX_FILES:
            raise ValueError('Total intake budget exceeded.')
        sha = digest(raw)
        ext = PurePosixPath(name).suffix.lower()
        kind = 'image' if ext in IMAGE_EXTS else 'helper_text' if ext == '.py' else 'document'
        image = decode_image(raw, name) if kind == 'image' else None
        if sha not in unique:
            matches = []
            for a in catalog_by_sha.get(sha, []):
                path = checked_path(ROOT / a['repoPath']) if a.get('repoPath') else checked_path(CATALOG.parent / unquote(a['src']))
                if not io_path(path).is_file():
                    raise ValueError('Catalog source is missing for a potential reuse: ' + a['id'])
                existing = io_path(path).read_bytes()
                if digest(existing) != sha or len(existing) != len(raw):
                    raise ValueError('Catalog file changed; refusing claimed hash reuse: ' + a['id'])
                matches.append({'id': a['id'], 'path': relative(path)})
            if matches:
                matches.sort(key=lambda x: (not x['id'].startswith('HD-DROP-'), x['id']))
                canonical_path, media_id = matches[0]['path'], matches[0]['id']
                storage = 'existing_catalog'
            else:
                target = checked_path(content / (sha[:12] + '__' + PurePosixPath(name).name))
                canonical_path, media_id = relative(target), None
                storage = 'new_content'
                if extract:
                    io_path(target.parent).mkdir(parents=True, exist_ok=True)
                    output = io_path(target)
                    if output.exists():
                        saved = output.read_bytes()
                        if len(saved) != len(raw) or digest(saved) != sha:
                            raise ValueError('Existing content-store path contains different bytes.')
                    else:
                        with output.open('xb') as stream:
                            stream.write(raw)
            unique[sha] = {'sha256': sha, 'bytes': len(raw), 'kind': kind,
                           'canonical_path': canonical_path, 'canonical_media_id': media_id,
                           'storage': storage, 'original_filename': PurePosixPath(name).name,
                           'catalog_matches': matches, 'image': image, 'occurrence_indices': []}
        rec = unique[sha]
        if rec['bytes'] != len(raw):
            raise ValueError('Unexpected hash/size conflict.')
        rec['occurrence_indices'].append(len(occurrence_rows))
        occurrence_rows.append({**occurrence, 'original_filename': PurePosixPath(name).name,
                                'sha256': sha, 'bytes': len(raw), 'kind': kind,
                                'canonical_path': rec['canonical_path'],
                                'canonical_media_id': rec['canonical_media_id'],
                                'storage': rec['storage'], 'image': image})

    # Check every archive's member set before writing any payload.
    for source in archives:
        with zipfile.ZipFile(io_path(source)) as z:
            safe_members(z.infolist())
    for source in archives:
        original = io_path(source).read_bytes()
        archive_sha = digest(original)
        with zipfile.ZipFile(BytesIO(original)) as z:
            infos = z.infolist()
            expanded = 0
            for info in infos:
                if info.is_dir():
                    continue
                raw = z.read(info)  # ZipFile also validates the stored CRC.
                if len(raw) != info.file_size or zlib.crc32(raw) & 0xffffffff != info.CRC:
                    raise ValueError('ZIP member CRC/size mismatch.')
                expanded += len(raw)
                register(raw, info.filename, {'archive_path': relative(source),
                         'archive_sha256': archive_sha, 'member': info.filename,
                         'source_path': None, 'crc32': f'{info.CRC:08x}', 'crc_verified': True})
        archive_rows.append({'source_path': relative(source), 'current_archive_path': relative(source), 'sha256': archive_sha,
                             'bytes': len(original), 'member_count': len(infos),
                             'file_count': sum(not i.is_dir() for i in infos),
                             'expanded_bytes': expanded, 'crc_verified': True,
                             'source_retained': True})
        if digest(io_path(source).read_bytes()) != archive_sha:
            raise ValueError('Input archive changed during intake.')
    for source in loose_files:
        register(io_path(source).read_bytes(), source.name,
                 {'archive_path': None, 'archive_sha256': None, 'member': None,
                  'source_path': relative(source), 'crc32': None, 'crc_verified': None})

    if extract:
        for rec in unique.values():
            saved = io_path(ROOT / rec['canonical_path']).read_bytes()
            if digest(saved) != rec['sha256'] or len(saved) != rec['bytes']:
                raise ValueError('Final canonical file hash/size verification failed.')
            if rec['image'] and decode_image(saved, rec['original_filename']) != rec['image']:
                raise ValueError('Final canonical image decode differs.')
    unique_rows = list(unique.values())
    images = [r for r in unique_rows if r['kind'] == 'image']
    summary = {'archives': len(archives), 'archive_file_occurrences': sum(x['file_count'] for x in archive_rows),
               'loose_file_occurrences': len(loose_files), 'all_file_occurrences': len(occurrence_rows),
               'unique_files': len(unique_rows), 'unique_images': len(images),
               'unique_kind_counts': dict(Counter(r['kind'] for r in unique_rows)),
               'image_occurrences': sum(r['kind'] == 'image' for r in occurrence_rows),
               'existing_catalog_files_reused': sum(r['storage'] == 'existing_catalog' for r in unique_rows),
               'new_files_written': sum(r['storage'] == 'new_content' for r in unique_rows) if extract else 0,
               'duplicate_occurrences_reused': len(occurrence_rows) - len(unique_rows),
               'canonical_unique_bytes': sum(r['bytes'] for r in unique_rows),
               'new_content_bytes': sum(r['bytes'] for r in unique_rows if r['storage'] == 'new_content'),
               'archive_source_bytes': sum(r['bytes'] for r in archive_rows)}
    receipt = {'schema': 'grok-return-intake-v1', 'intakeID': 'HON-GROK-RETURN-20261009',
               'state': 'verified_crc_hash_size_decode' if extract else 'inspection_only_no_writes',
               'recordedAtUTC': datetime.now(timezone.utc).isoformat(),
               'catalog_snapshot': {'path': relative(CATALOG), 'sha256': digest(catalog_raw)},
               'archives': archive_rows, 'unique_files': unique_rows, 'occurrences': occurrence_rows,
               'summary': summary, 'newApprovals': [], 'sourceZIPDeletion': 'not_performed_hold_for_root_final_verification',
               'providerHelpersExecuted': False, 'providerClaimsVerified': False,
               'limitations': ['Integrity/decode verification is not visual design review or approval.',
                              'Provider source-original, QA, selection and transparency descriptions remain separate claims.']}
    if extract:
        received.mkdir(parents=True, exist_ok=True)
        destination = received / 'intake_receipt.json'
        temporary = received / 'intake_receipt.next.json'
        temporary.write_text(json.dumps(receipt, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
        temporary.replace(destination)
    return receipt


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--extract', action='store_true', help='Write only verified canonical payloads and a final receipt; retain all ZIPs.')
    args = parser.parse_args()
    receipt = inspect_and_extract(args.extract)
    print(json.dumps({'state': receipt['state'], 'summary': receipt['summary']}, indent=2))
