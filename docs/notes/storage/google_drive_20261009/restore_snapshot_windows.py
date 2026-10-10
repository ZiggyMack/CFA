"""Restore CFA archives with Windows extended-length paths and no overwrites."""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import stat
import sys
import zipfile


def digest_file(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        while chunk := stream.read(8 * 1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def extended(path):
    text = str(path)
    if os.name == 'nt' and not text.startswith(chr(92) * 2 + '?' + chr(92)):
        text = chr(92) * 2 + '?' + chr(92) + text
    return Path(text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--archive', required=True)
    parser.add_argument('--destination', required=True)
    parser.add_argument('--sha256')
    parser.add_argument('--member', action='append', help='Repeat for a bounded restore probe; omit for full restore.')
    args = parser.parse_args()
    if sys.version_info < (3, 12):
        raise SystemExit('Use Python 3.12 or newer.')
    archive = Path(args.archive).resolve()
    destination = Path(args.destination).absolute()
    target_root = extended(destination)
    if target_root.exists():
        raise SystemExit('Destination already exists. Choose a new folder; this tool never overwrites.')
    if args.sha256 and digest_file(extended(archive)).lower() != args.sha256.lower():
        raise SystemExit('Archive SHA-256 mismatch; nothing extracted.')
    restored = []
    with zipfile.ZipFile(extended(archive)) as bundle:
        members = [bundle.getinfo(name) for name in args.member] if args.member else bundle.infolist()
        for item in members:
            parts = PurePosixPath(item.filename).parts
            if not parts or PurePosixPath(item.filename).is_absolute() or '..' in parts or chr(92) in item.filename or any(':' in part for part in parts):
                raise SystemExit('Unsafe archive member path: ' + item.filename)
            if stat.S_ISLNK(item.external_attr >> 16):
                raise SystemExit('Symlink entries are not supported: ' + item.filename)
        target_root.mkdir(parents=True)
        for item in members:
            target = target_root.joinpath(*PurePosixPath(item.filename).parts)
            if item.is_dir():
                target.mkdir(parents=True, exist_ok=True)
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            with bundle.open(item) as source, target.open('xb') as output:
                while chunk := source.read(8 * 1024 * 1024):
                    output.write(chunk)
            restored.append({'member': item.filename, 'bytes': item.file_size})
            if len(restored) % 5000 == 0:
                print('Restored ' + str(len(restored)) + ' files', flush=True)
    print(json.dumps({'destination': str(destination), 'filesRestored': len(restored), 'zipCrcVerifiedDuringExtraction': True, 'members': restored if args.member else 'Full archive extracted'}, indent=2), flush=True)


if __name__ == '__main__':
    main()