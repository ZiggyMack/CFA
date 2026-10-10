"""Verify the eight exact D:/Downloads outer archives; opt-in scoped cleanup."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import zipfile

import intake_grok500 as core
import intake_grok500_folders as folders

HERE = Path(__file__).resolve().parent
FROZEN_SHA = '96069a962794403c9d426150158acff20fd6de66f833e129f006cd70d5ce8db9'
DOWNLOADS = Path('D:/Downloads')


def run(execute=False):
    receipt = HERE / 'received/intake_receipt.json'
    if core.file_hash(receipt) != FROZEN_SHA:
        raise ValueError('Extraction receipt changed; stop.')
    saved = json.loads(receipt.read_text(encoding='utf-8'))
    if saved['state'] != 'eight_folders_nested_CRC_csv_hash_size_decode_verified':
        raise ValueError('Verified extraction required.')
    downloads = core.safe_path(DOWNLOADS)
    target = HERE / 'received/outer_cleanup_summary.json'
    if target.exists():
        raise ValueError('Outer cleanup receipt already exists; inspect before retry.')
    checked = []
    for part in folders.PARTS:
        path = core.safe_path(downloads / (part + '.zip'))
        if path.parent != downloads or not path.is_file():
            raise ValueError('Expected exact archive missing or outside Downloads.')
        expected = {x['relative_path']: x for x in saved['source_files'] if x['part'] == part}
        archive_sha = core.file_hash(path)
        with zipfile.ZipFile(path) as z:
            infos = z.infolist()
            if len(infos) != len(expected) or {i.filename for i in infos} != set(expected):
                raise ValueError('Outer member set differs: ' + part)
            if z.testzip() is not None:
                raise ValueError('Outer CRC failure: ' + part)
            for info in infos:
                core.member_path(info.orig_filename)
                record = expected[info.filename]
                if info.file_size != record['bytes']:
                    raise ValueError('Member size differs: ' + info.filename)
                data = z.read(info)
                if hashlib.sha256(data).hexdigest() != record['sha256']:
                    raise ValueError('Member bytes differ: ' + info.filename)
        checked.append({'path': str(path), 'sha256': archive_sha,
                        'bytes': path.stat().st_size, 'member_count': len(expected),
                        'crc_verified': True, 'all_members_match_extraction_inputs': True})
    output_count = folders.verify_folder_extracted(saved)
    result = {'schema': 'grok500-outer-cleanup-v1',
              'verified_at_utc': datetime.now(timezone.utc).isoformat(),
              'extraction_receipt_sha256': FROZEN_SHA, 'archives': checked,
              'verified_outer_archive_count': 8, 'verified_output_files': output_count,
              'removed': [], 'removed_bytes': 0, 'cleanup_complete': False,
              'note': 'Outer archives discovered later in D:/Downloads. Original extraction receipt remains a frozen earlier observation.'}
    def journal():
        tmp = target.with_suffix('.next.json')
        with tmp.open('x', encoding='utf-8') as f:
            json.dump(result, f, indent=2)
            f.write('\n')
        tmp.replace(target)
    if execute:
        journal()
        for rec in checked:
            path = core.safe_path(rec['path'])
            if path.parent != downloads or path.name not in {p + '.zip' for p in folders.PARTS}:
                raise ValueError('Cleanup target escaped exact eight-archive scope.')
            if path.stat().st_size != rec['bytes'] or core.file_hash(path) != rec['sha256']:
                raise ValueError('Archive changed after verification.')
            path.unlink()
            result['removed'].append(rec['path'])
            result['removed_bytes'] += rec['bytes']
            journal()
        if core.file_hash(receipt) != FROZEN_SHA:
            raise ValueError('Frozen receipt changed.')
        result['verified_output_files_after_cleanup'] = folders.verify_folder_extracted(saved)
        result['cleanup_complete'] = True
        result['completed_at_utc'] = datetime.now(timezone.utc).isoformat()
        journal()
    print(json.dumps({'verified_outer_archive_count': 8, 'verified_output_files': output_count,
                      'outer_archive_bytes': sum(r['bytes'] for r in checked),
                      'removed_count': len(result['removed']), 'cleanup_complete': result['cleanup_complete']}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--execute', action='store_true')
    run(parser.parse_args().execute)
