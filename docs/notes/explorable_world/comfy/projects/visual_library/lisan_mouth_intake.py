"""Hash-bound Lisan mouth intake; provider estimates never become human review.

The 65-file source is a dated snapshot. Existing SHA identities retain their
original paths, review decisions and scoped approvals; only 44 assets are new.
"""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

from grok500_catalog import CatalogIntakeError, io_path

INTAKE_ID = 'LISAN-MOUTH-COMPLETE-20261012'
MANIFEST_SHA256 = '671784f33bdcf4d6a221c8cdf4ba6762bc665362f2b53219b7087d863f86281e'
SOURCE_MESSAGE_IDS = ['c27902f2-7edb-4290-8182-a8035586137e', 'b4576d9c-baf6-4448-ac45-f8ba59ed0e85']
SOURCE_DIRECTORY = 'docs/notes/explorable_world/comfy/references/From Grok/GROK-LAG-VIS-NATURAL-v001'
COLLECTION_COUNTS = {'01_VISEMES': 51, '02_BREATHER_NATURAL': 5, '03_OPTIONAL_GRILL': 1, '04_FAILS': 8}
PROTECTED = {'likenessRating', 'sceneQualityRating', 'status', 'workingReference', 'workingReferenceScope',
             'componentApprovals', 'variant', 'shotPlan', 'creativeReview', 'favorite'}

def safe_relative(value):
    posix = PurePosixPath(value) if isinstance(value, str) else None
    if (not value or posix is None or posix.is_absolute() or '..' in posix.parts
            or re.search(r'[\\%?#:\x00-\x1f\x7f]', value)):
        raise CatalogIntakeError('Unsafe Lisan mouth path.')
    return posix

def validate_registry(data):
    if (data.get('id') != INTAKE_ID or data.get('receiptState') != 'verified_hash_size_decode'
            or data.get('sourceManifestSHA256') != MANIFEST_SHA256
            or data.get('sourceMessageIDs') != SOURCE_MESSAGE_IDS):
        raise CatalogIntakeError('Unexpected Lisan mouth intake identity/state.')
    media = data.get('assets', [])
    if (len(media) != 65 or len({a.get('id') for a in media}) != 65
            or len({a.get('path') for a in media}) != 65
            or len({a.get('sha256') for a in media}) != 65):
        raise CatalogIntakeError('Lisan mouth intake must retain exactly 65 unique files.')
    counts = {}
    for a in media:
        safe_relative(a.get('path'))
        if (a.get('project') != 'lisan' or a.get('binding') not in {'existing', 'new'}
                or a.get('decoded') is not True or a.get('width') != 1280 or a.get('height') != 720
                or type(a.get('bytes')) is not int or a['bytes'] <= 0
                or not re.fullmatch(r'[0-9a-f]{64}', a.get('sha256', ''))):
            raise CatalogIntakeError('Invalid Lisan mouth source metadata.')
        if any(field in a for field in PROTECTED):
            raise CatalogIntakeError('Provider intake cannot contain a human review/approval field.')
        if a['binding'] == 'new' and (a.get('storyboardStage') != 'preliminary'
                or a.get('acceptance') != 'not_accepted' or a.get('timing') is not None
                or a['id'] != 'LAG-VIS-' + a['sha256'][:16]):
            raise CatalogIntakeError('New Lisan mouth asset must remain a preliminary, untimed candidate.')
        p = a.get('providerPreliminaryReview', {})
        if (p.get('status') != 'provider_self_score_preliminary'
                or any(type(p.get(k)) is not int or not 1 <= p[k] <= 5
                       for k in ['likenessRating', 'sceneQualityRating'])
                or p.get('suggestedLane') not in {'prime', 'multiverse'}
                or p.get('suggestedScope') not in {'detail', 'complete_look'}
                or p.get('sourceManifestSHA256') != MANIFEST_SHA256):
            raise CatalogIntakeError('Invalid provider preliminary score metadata.')
        counts[a['providerCollection']] = counts.get(a['providerCollection'], 0) + 1
    if counts != COLLECTION_COUNTS or sum(a['binding'] == 'existing' for a in media) != 21:
        raise CatalogIntakeError('Unexpected Lisan mouth collection or dedup counts.')
    if data.get('coverage', {}).get('missingUsableShapeNumbers') != [7, 15, 16, 18, 35]:
        raise CatalogIntakeError('Unresolved Lisan shape coverage must remain explicit.')
    if data.get('coverage', {}).get('skippedShapeNumbers') != [47]:
        raise CatalogIntakeError('Skipped Hon-only prop must remain explicit.')
    docs = data.get('documents', [])
    if len(docs) != 6 or not any(Path(d['path']).name == 'MANIFEST.csv' and d['sha256'] == MANIFEST_SHA256 for d in docs):
        raise CatalogIntakeError('Lisan mouth snapshot needs four provider documents and two notices.')
    for d in docs:
        safe_relative(d.get('path'))
    return data

def load_lisan_mouth_complete(repo_root, intake_dir, existing_assets):
    root, intake = Path(repo_root).resolve(), Path(intake_dir).resolve()
    registry = intake / 'registry.json'
    if not io_path(registry).is_file():
        return None
    data = validate_registry(json.loads(io_path(registry).read_text(encoding='utf-8')))

    def verify(record, directory):
        relative = safe_relative(record['path'])
        source = (root / Path(*relative.parts)).resolve()
        if not source.is_relative_to(root) or not source.is_relative_to(directory.resolve()):
            raise CatalogIntakeError('Lisan mouth source escapes its scope.')
        raw = io_path(source).read_bytes()
        if len(raw) != record['bytes'] or hashlib.sha256(raw).hexdigest() != record['sha256']:
            raise CatalogIntakeError('Changed Lisan mouth source: ' + record['path'])

    for document in data['documents']:
        verify(document, intake / 'provider_documents')
    by_id = {a['id']: a for a in existing_assets}
    new, reused = [], []
    for a in data['assets']:
        verify(a, root / SOURCE_DIRECTORY)
        if a['binding'] == 'existing':
            old = by_id.get(a['id'])
            if not old or old.get('sha256') != a['sha256'] or old.get('project') != 'lisan':
                raise CatalogIntakeError('Existing Lisan mouth identity/hash is missing or changed: ' + a['id'])
            reused.append(a)
        else:
            if a['id'] in by_id:
                raise CatalogIntakeError('New Lisan mouth ID collides with an existing asset.')
            new.append(a)
    return {**data, 'assets': new, 'reusedAssets': reused}

def apply_existing_lisan_metadata(existing_assets, reused_records):
    """Add provider provenance only; never reset paths, human reviews or scopes."""
    by_id = {a['id']: a for a in existing_assets}
    for record in reused_records:
        target = by_id.get(record['id'])
        if not target or target.get('sha256') != record['sha256']:
            raise CatalogIntakeError('Reused Lisan mouth source binding changed.')
        target['providerPreliminaryReview'] = json.loads(json.dumps(record['providerPreliminaryReview']))
        suffix = record['providerNoteSuffix']
        prior_note = target.get('note', '')
        if suffix not in prior_note:
            target['note'] = prior_note + ('\n' if prior_note else '') + suffix
        aliases = target.get('intakeSourceAliases', [])
        target['intakeSourceAliases'] = list(dict.fromkeys(aliases + [record['path']]))