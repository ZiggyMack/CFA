"""Read existing backup metadata; write only this audit's report artifacts.

No archive creation, extraction, upload, Git operation, move or deletion.
Media inventories are filename/stat based; private source contents are not read.
"""
import collections
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import zipfile

AUDIT = Path(__file__).parent
ROOT = Path('D:/Documents/CFA')
STAGE = Path('D:/CFA_Backup_Staging')
DRIVE = Path('G:/My Drive/CFA_Backups/CFA_Prime_20261011_185936')
MEDIA_EXTS = {'.jpg', '.jpeg', '.png', '.webp', '.gif', '.mp4', '.mov', '.mkv', '.webm', '.mp3', '.wav', '.m4a', '.ogg', '.flac', '.zip', '.7z'}


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def manifest_entries(manifest):
    value = manifest.get('files', manifest.get('entries', manifest.get('sourceFiles')))
    if not isinstance(value, list) or not all(isinstance(x, dict) and isinstance(x.get('path'), str) for x in value):
        raise ValueError('Unknown backup manifest entry schema; no report created.')
    return value


def is_audit_path(path):
    normal = str(path).removeprefix(chr(92) * 2 + '?' + chr(92)).replace(chr(92), '/')
    audit = str(AUDIT).replace(chr(92), '/')
    return normal.casefold() == audit.casefold() or normal.casefold().startswith(audit.casefold() + '/')


def relnorm(value):
    value = str(value).replace('\\', '/')
    prefix = 'D:/Documents/CFA/'
    return (value[len(prefix):] if value.lower().startswith(prefix.lower()) else value).lstrip('./')


def pin(path):
    data = path.read_bytes()
    return {'path': str(path).replace('\\', '/'), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def xlong(path):
    raw = os.path.abspath(str(path))
    return '\\\\?\\' + raw if os.name == 'nt' and not raw.startswith('\\\\?\\') else raw


base_manifest_path = STAGE / 'CFA_20261009_233600/source_manifest.json'
base_archive = STAGE / 'CFA_20261009_233600/CFA_20261009_233600.zip'
coord_manifest_path = STAGE / 'CFA_20261010_coordination_supplement/supplement_manifest.json'
prime_manifest_path = DRIVE / 'prime_coordination_snapshot_20261011T185936Z_b293e4.manifest.json'
post_manifest_path = DRIVE / 'prime_post_checkpoint_20261011T191749Z_b1c65e.manifest.json'
writer_manifest_path = DRIVE / 'writer_followup_e58074d.manifest.json'
base = load(base_manifest_path)
coord = load(coord_manifest_path)
prime = load(prime_manifest_path)
post = load(post_manifest_path)
writer = load(writer_manifest_path)

paths_in_archives = set()
for entry in base['sourceFiles']:
    paths_in_archives.add(relnorm(entry['path']).casefold())
for manifest in [coord, prime, post, writer]:
    for entry in manifest_entries(manifest):
        paths_in_archives.add(relnorm(entry['path']).casefold())

targets = [
    'docs/notes/explorable_world/comfy/projects/visual_library/library.js',
    'docs/notes/explorable_world/comfy/projects/hon_dolo_strictly_business/feedback/review_decisions.json',
    'docs/notes/explorable_world/comfy/projects/collaborators/provider_roles.txt',
]
coord_files = {relnorm(x['path']): x for x in coord['files']}
versions = []
with zipfile.ZipFile(base_archive) as archive:
    names = archive.namelist()
    for relative in targets:
        path = ROOT / relative
        old_matches = [name for name in names if name.replace('\\', '/').endswith('/' + relative) or name.replace('\\', '/') == relative]
        current = path.read_bytes()
        item = {'path': relative, 'currentBytes': len(current), 'currentSHA256': hashlib.sha256(current).hexdigest(), 'baseEntryMatches': len(old_matches)}
        if len(old_matches) == 1:
            old = archive.read(old_matches[0])
            item.update(baseBytes=len(old), baseSHA256=hashlib.sha256(old).hexdigest())
            item['baseDiffersFromCurrent'] = item['baseSHA256'] != item['currentSHA256']
        if relative in coord_files:
            previous = coord_files[relative]
            item.update(coordinationBytes=previous['bytes'], coordinationSHA256=previous['sha256'])
            item['coordinationDiffersFromCurrent'] = item['coordinationSHA256'] != item['currentSHA256']
        versions.append(item)

comfy = ROOT / 'docs/notes/explorable_world/comfy'
media = []
stat_errors = []
private_name_exclusions = 0
for directory, subdirs, filenames in os.walk(xlong(comfy), followlinks=False):
    subdirs[:] = [x for x in subdirs if x not in {'.git', '.tmp.driveupload', '.tmp.drivedownload'} and not is_audit_path(os.path.join(directory, x))]
    for filename in filenames:
        if Path(filename).suffix.lower() not in MEDIA_EXTS:
            continue
        absolute = os.path.join(directory, filename)
        normal = absolute.removeprefix('\\\\?\\').replace('\\', '/')
        relative = relnorm(normal)
        if any(word in relative.lower() for word in ['answer_key', 'answer-key', 'private_calibration', 'private-calibration']):
            private_name_exclusions += 1
            continue
        try:
            stat = os.stat(absolute, follow_symlinks=False)
        except OSError as exc:
            stat_errors.append({'path': relative, 'errorClass': type(exc).__name__})
            continue
        media.append({'path': relative, 'bytes': stat.st_size, 'mtimeUTC': dt.datetime.fromtimestamp(stat.st_mtime, dt.timezone.utc).isoformat(), 'samePathInOlderManifest': relative.casefold() in paths_in_archives})

same = [x for x in media if x['samePathInOlderManifest']]
not_same = [x for x in media if not x['samePathInOlderManifest']]
not_same_groups = collections.defaultdict(lambda: {'paths': 0, 'bytes': 0})
for item in not_same:
    relative = item['path'].removeprefix('docs/notes/explorable_world/comfy/')
    parts = relative.split('/')
    group = '/'.join(parts[:2])
    not_same_groups[group]['paths'] += 1
    not_same_groups[group]['bytes'] += item['bytes']

archive_metadata = []
archive_locations = [
    (STAGE / 'CFA_20261009_233600/CFA_20261009_233600.zip', 'full CFA base', base.get('completedUtc'), base['sourceFileCount']),
    (STAGE / 'CFA_20261010_coordination_supplement/CFA_20261010_coordination_supplement.zip', 'delta against base', coord.get('completedUtc'), len(coord['files'])),
    (DRIVE / 'prime_coordination_snapshot_20261011T185936Z_b293e4.zip', 'selected Prime source/audio/writer/analysis', prime.get('snapshot_cutoff_utc'), len(manifest_entries(prime))),
    (DRIVE / 'prime_post_checkpoint_20261011T191749Z_b1c65e.zip', 'selected post-Prime working records', post['snapshot_cutoff_utc'], len(post['files'])),
    (DRIVE / 'writer_followup_e58074d.zip', 'five writer followup files', writer['captured_at_utc'], len(writer['files'])),
]
for path, scope, cutoff, count in archive_locations:
    archive_metadata.append({'path': str(path).replace('\\', '/'), 'scope': scope, 'cutoffFromManifest': cutoff, 'selectedSourceCount': count, 'existsNow': path.is_file(), 'observedFileBytes': path.stat().st_size if path.is_file() else None, 'freshWholeArchiveChecksumComputed': False})

result = {
    'schemaVersion': 1,
    'recordedAtUTC': dt.datetime.now(dt.timezone.utc).isoformat(),
    'sourceManifests': [pin(p) for p in [base_manifest_path, coord_manifest_path, prime_manifest_path, post_manifest_path, writer_manifest_path]],
    'archives': archive_metadata,
    'fullSnapshotScope': {'baseCount': base['sourceFileCount'], 'coordinationCount': coord['sourceFileCount'], 'baseManifestDeclaresEntireCFARegardlessOfGitIgnore': True, 'baseDeclaredScope': base.get('scope'), 'coordinationSelectedDeltaFiles': len(coord['files']), 'siblingRepositoriesIncluded': False},
    'historicalVersions': versions,
    'currentComfyMediaFilenameStatComparison': {
        'paths': len(media), 'logicalBytes': sum(x['bytes'] for x in media),
        'samePathInAnyListedOlderManifest': len(same),
        'notSamePathInAnyListedOlderManifest': len(not_same),
        'notSamePathLogicalBytes': sum(x['bytes'] for x in not_same),
        'groupsWithoutSamePath': dict(sorted(not_same_groups.items())),
        'selectedRecentExamples': sorted(not_same, key=lambda x: x['mtimeUTC'], reverse=True)[:20],
        'statErrors': stat_errors, 'privateNameExclusions': private_name_exclusions,
        'limits': [
            'Path occurrence counts/logical bytes include hardlinks and alternate named copies; not unique physical storage.',
            'Same path does not verify the current version; absent path does not rule out identical bytes archived under another name.',
            'This compares named older dated archives, not the new live computer sync or every unrelated backup.',
            'Media bytes were not read for this inventory. Current Drive coverage was separately checked through web metadata and one independent matching retrieval.',
        ],
    },
    'preservation': {'existingArchivesModified': False, 'extractionPerformed': False, 'newBackupCreated': False, 'uploadsStarted': False, 'movesOrDeletes': False},
}
destination = AUDIT / 'OLDER_BACKUP_SCOPE_AND_CURRENT_MEDIA.json'
with destination.open('x', encoding='utf-8') as stream:
    json.dump(result, stream, indent=2)
    stream.write('\n')
print(json.dumps({'report': str(destination), 'bytes': destination.stat().st_size, 'sha256': hashlib.sha256(destination.read_bytes()).hexdigest(), 'media': {k: result['currentComfyMediaFilenameStatComparison'][k] for k in ['paths', 'logicalBytes', 'samePathInAnyListedOlderManifest', 'notSamePathInAnyListedOlderManifest', 'notSamePathLogicalBytes', 'statErrors']}, 'oldVersionsDiffer': all(x.get('baseDiffersFromCurrent') and x.get('coordinationDiffersFromCurrent') for x in versions)}))
