"""Verify the Falcon current-90 snapshot; catalog only its additional 40.

The first-50 registry and asset IDs remain authoritative for that earlier
snapshot. Provider picks never become saved user decisions in this adapter.
"""
import csv
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re

from grok500_catalog import CatalogIntakeError, io_path
from source_relocations import resolve_source


def load_falcon_group1_extension(repo_root, intake_dir, base):
    root = Path(repo_root).resolve()
    intake = Path(intake_dir).resolve()
    registry_path = intake / 'registry.json'
    if not registry_path.is_file():
        return None
    data = json.loads(registry_path.read_text(encoding='utf-8'))
    if (not base or base.get('id') != 'HON-FALCON-GROUP1-20261011'
            or data.get('id') != 'HON-FALCON-GROUP1-EXTENSION-20261012'
            or data.get('receiptState') != 'verified_hash_size_decode'
            or data.get('sourceMessageID') != '8cf62e48-51fd-4206-b8e6-6a461a11a683'):
        raise CatalogIntakeError('Unexpected Falcon extension identity/state.')

    def verified_bytes(record, directory):
        relative = record.get('path', '')
        posix = PurePosixPath(relative)
        if (not relative or posix.is_absolute() or '..' in posix.parts
                or re.search(r'[\\%?#:\x00-\x1f\x7f]', relative)):
            raise CatalogIntakeError('Unsafe Falcon extension path: ' + relative)
        path = (root / Path(*posix.parts)).resolve()
        if (not path.is_relative_to(root)
                or not path.is_relative_to(directory.resolve())):
            raise CatalogIntakeError('Falcon extension path escapes its scope.')
        physical = resolve_source(root, path, expected_sha256=record.get('sha256'),
                                  expected_bytes=record.get('bytes'))
        raw = io_path(physical).read_bytes()
        if (len(raw) != record.get('bytes')
                or hashlib.sha256(raw).hexdigest() != record.get('sha256')):
            raise CatalogIntakeError('Changed Falcon extension source: ' + relative)
        return raw

    base_registry = root / data['baseRegistryPath']
    if (not base_registry.resolve().is_relative_to(root)
            or hashlib.sha256(io_path(base_registry).read_bytes()).hexdigest()
            != data.get('baseRegistrySHA256')):
        raise CatalogIntakeError('The first-50 registry changed since extension intake.')
    base_assets = {a['id']: a for a in base['assets']}
    files = data.get('sourceFiles', [])
    if (len(files) != 90 or len({a.get('id') for a in files}) != 90
            or len({a.get('path') for a in files}) != 90):
        raise CatalogIntakeError('Falcon extension must verify the exact current 90.')
    counts = {}
    incoming = root / 'docs/notes/downloads/GROK-HD-FALCON-1000'
    by_id = {}
    for record in files:
        verified_bytes(record, incoming)
        if (record['id'] != 'HD-FALCON-' + record['sha256'][:16]
                or record.get('decoded') is not True
                or (record.get('width'), record.get('height')) != (1280, 720)):
            raise CatalogIntakeError('Invalid Falcon original metadata: ' + record['id'])
        counts[record['providerCategory']] = counts.get(record['providerCategory'], 0) + 1
        by_id[record['id']] = record
        if record['id'] in base_assets:
            earlier = base_assets[record['id']]
            if any(record[k] != earlier[k] for k in ['path', 'sha256', 'bytes']):
                raise CatalogIntakeError('A first-50 source identity changed.')
    if counts != {'C01-pilot-hover': 15, 'C02-captain-portrait': 15,
                  'C03-look-back-softened': 15, 'C04-battle-light': 15,
                  'C05-lurch-grin': 15, 'C06-lurch-no-grin': 15}:
        raise CatalogIntakeError('Unexpected Falcon current-90 category counts.')
    if (set(data.get('baseAssetIDs', [])) != set(base_assets)
            or not set(base_assets).issubset(by_id)
            or set(data.get('allAssetIDs', [])) != set(by_id)):
        raise CatalogIntakeError('Falcon extension must preserve all first-50 IDs.')
    new_media = data.get('assets', [])
    new_ids = {a['id'] for a in new_media}
    if (len(new_media) != 40 or len(new_ids) != 40
            or new_ids != set(by_id) - set(base_assets)):
        raise CatalogIntakeError('Falcon extension must add exactly 40 new assets.')
    additional_counts = {}
    for asset in new_media:
        source = by_id[asset['id']]
        if any(asset[k] != source[k] for k in ['path', 'sha256', 'bytes', 'width', 'height']):
            raise CatalogIntakeError('Extension card does not match its original.')
        if (asset.get('project') != 'hon' or asset.get('category') != 'storyboard'
                or asset.get('storyboardStage') != 'preliminary'
                or asset.get('acceptance') != 'not_accepted'
                or asset.get('timing') is not None
                or asset.get('storySequenceID') != data['id']):
            raise CatalogIntakeError('Unexpected Falcon extension draft state.')
        category = asset['providerCategory']
        additional_counts[category] = additional_counts.get(category, 0) + 1
    if additional_counts != {'C04-battle-light': 10, 'C05-lurch-grin': 15, 'C06-lurch-no-grin': 15}:
        raise CatalogIntakeError('Unexpected Falcon additional-40 counts.')

    documents = data.get('documents', [])
    if len(documents) != 9 or sum(d.get('sourceSnapshot') is True for d in documents) != 8:
        raise CatalogIntakeError('Falcon extension needs eight provider snapshots and a README.')
    document_bytes = {Path(d['path']).name: verified_bytes(d, intake) for d in documents
                      if Path(d['path']).name != 'NOTES.md'}
    for d in documents:
        if Path(d['path']).name == 'NOTES.md':
            verified_bytes(d, intake / 'provider_documents')
    expected = {'MANIFEST.csv': 'f41bf1f7c3edc22216486d0c1c4689c732a6928b45b91dd28ab2d35dd956c891',
                'SHORTLIST.md': '2998a99ee1b5200cc573cdf63fadb66e76030b6f1e7b6a97e778a3e9f41eccc0'}
    for name, sha in expected.items():
        if hashlib.sha256(document_bytes[name]).hexdigest() != sha:
            raise CatalogIntakeError('Falcon extension attachment differs from Chief message.')
    manifest = list(csv.DictReader(io.StringIO(document_bytes['MANIFEST.csv'].decode('utf-8-sig'))))
    by_name = {a['filename']: a for a in files}
    if len(manifest) != 90 or {r['file'] for r in manifest} != set(by_name):
        raise CatalogIntakeError('Falcon extension source ledger coverage differs.')
    for row in manifest:
        record = by_name[row['file']]
        if (row['category'] != record['providerCategory']
                or row['sha256'].lower() != record['sha256']
                or int(row['bytes']) != record['bytes']):
            raise CatalogIntakeError('Falcon original differs from provider manifest.')
    shortlist = []
    for line in document_bytes['SHORTLIST.md'].decode('utf-8-sig').splitlines():
        if line.startswith('- '):
            category, names = line[2:].split(': ', 1)
            for name in names.split(', '):
                record = by_name[name]
                if record['providerCategory'] != category:
                    raise CatalogIntakeError('Falcon shortlist category mismatch.')
                shortlist.append(record['id'])
    if (len(shortlist) != 28 or len(set(shortlist)) != 28
            or shortlist != data.get('shortlistAssetIDs')
            or data.get('preservedShortlistAssetIDs') != base['shortlistAssetIDs']
            or not set(base['shortlistAssetIDs']).issubset(shortlist)
            or data.get('newShortlistAssetIDs') != [i for i in shortlist if i in new_ids]
            or len(data['newShortlistAssetIDs']) != 15):
        raise CatalogIntakeError('Falcon shortlist must preserve the original 13 plus 15 new picks.')
    for album in data.get('albums', []):
        if not set(album.get('related', [])).issubset(by_id):
            raise CatalogIntakeError('Falcon extension album refers to unknown media.')
    return data
