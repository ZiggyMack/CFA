"""Load the verified first Falcon return without promoting provider picks.

The dated intake keeps byte-identical copies of provider documents because the
incoming run can continue. Artwork retains its original recorded source path;
a verified relocation map resolves its current physical location. Later
returns require a separate intake; they are never silently included here.
"""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

from grok500_catalog import CatalogIntakeError, io_path
from source_relocations import resolve_source


def load_falcon_group1(repo_root, intake_dir):
    root = Path(repo_root).resolve()
    intake = Path(intake_dir).resolve()
    path = intake / 'registry.json'
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding='utf-8'))
    if (data.get('id') != 'HON-FALCON-GROUP1-20261011'
            or data.get('receiptState') != 'verified_hash_size_decode'
            or data.get('sourceMessageID') != '39ce2274-9c4b-4490-b7c8-96f4937210e3'):
        raise CatalogIntakeError('Unexpected Falcon group 1 intake identity/state.')

    def verify(record, directory):
        relative = record.get('path', '')
        posix = PurePosixPath(relative)
        if (not relative or posix.is_absolute() or '..' in posix.parts
                or re.search(r'[\\%?#:\x00-\x1f\x7f]', relative)):
            raise CatalogIntakeError('Unsafe Falcon intake path: ' + relative)
        original = (root / Path(*posix.parts)).resolve()
        if (not original.is_relative_to(root)
                or not original.is_relative_to(directory.resolve())):
            raise CatalogIntakeError('Falcon intake source escapes its scope.')
        physical = resolve_source(root, original, expected_sha256=record.get('sha256'),
                                  expected_bytes=record.get('bytes'))
        raw = io_path(physical).read_bytes()
        if (len(raw) != record.get('bytes')
                or hashlib.sha256(raw).hexdigest() != record.get('sha256')):
            raise CatalogIntakeError('Changed Falcon intake source: ' + relative)

    media = data.get('assets', [])
    if (len(media) != 50 or len({a.get('id') for a in media}) != 50
            or len({a.get('path') for a in media}) != 50):
        raise CatalogIntakeError('Falcon group 1 must retain its exact 50 drafts.')
    counts = {}
    for asset in media:
        verify(asset, root / 'docs/notes/downloads/GROK-HD-FALCON-1000')
        if (asset.get('category') != 'storyboard'
                or asset.get('project') != 'hon'
                or asset.get('storyboardStage') != 'preliminary'
                or asset.get('acceptance') != 'not_accepted'
                or asset.get('timing') is not None
                or not asset.get('storySequenceID')
                or type(asset.get('width')) is not int
                or type(asset.get('height')) is not int
                or min(asset['width'], asset['height']) <= 0):
            raise CatalogIntakeError('Invalid Falcon draft metadata: ' + asset['id'])
        category = asset['providerCategory']
        counts[category] = counts.get(category, 0) + 1
    if counts != {'C01-pilot-hover': 15, 'C02-captain-portrait': 15,
                  'C03-look-back-softened': 15, 'C04-battle-light': 5}:
        raise CatalogIntakeError('Unexpected first-50 category counts.')
    documents = data.get('documents', [])
    if len(documents) != 6:
        raise CatalogIntakeError('Falcon intake needs manifest, shortlist and four QA notes.')
    for document in documents:
        verify(document, intake / 'provider_documents')
    expected = {'MANIFEST.csv': '0ddff02fd6f20ddd5c28fd4454ad96ad9a90f1058788c47546658d3b0c2ecd89',
                'SHORTLIST.md': 'ed3eccbd97f001cca0cbff59556c5ac1c608dcd79c283909a79ab4f08c66ebc1'}
    for name, sha in expected.items():
        matches = [d for d in documents if Path(d['path']).name == name]
        if len(matches) != 1 or matches[0]['sha256'] != sha:
            raise CatalogIntakeError('Falcon provider attachment differs from incoming message.')
    picks = data.get('shortlistAssetIDs', [])
    if (len(picks) != 13 or len(set(picks)) != 13
            or not set(picks).issubset({a['id'] for a in media})):
        raise CatalogIntakeError('Falcon provider shortlist must bind 13 received images.')
    return data
