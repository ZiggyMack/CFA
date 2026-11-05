"""Resolve the exact, verified Grok source relocation without rewriting history.

Historical intake records keep their original Downloads paths. Only an active
map redirects one of the three authorized packages to its verified From Grok
file. A planned map has no effect on reads.
"""
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat

from grok500_catalog import CatalogIntakeError, io_path

SOURCE_PREFIX = 'docs/notes/downloads/'
PACKAGES = ('GROK-HD-FALCON-1000', 'GROK-HD-STORY-SET-02', 'GROK-HD-ENABLERS-03')
SOURCE_ROOTS = tuple(SOURCE_PREFIX + package for package in PACKAGES)
DESTINATION_ROOT = 'docs/notes/explorable_world/comfy/references/From Grok'
MAP_PATH = ('docs/notes/explorable_world/comfy/projects/visual_library/'
            'grok_source_relocation_20261012/relocation_map.json')
_map_cache = {}
_verified_cache = {}


def _portable(value):
    if not isinstance(value, str) or not value:
        raise CatalogIntakeError('Relocation path must be a nonempty repository path.')
    path = PurePosixPath(value)
    if (path.is_absolute() or '..' in path.parts or '.' in path.parts
            or path.as_posix() != value
            or re.search(r'[\\%?#:\x00-\x1f\x7f]', value)):
        raise CatalogIntakeError('Unsafe relocation path: ' + value)
    return path


def _source_package(relative):
    for prefix in SOURCE_ROOTS:
        if relative == prefix or relative.startswith(prefix + '/'):
            return prefix
    return None


def _no_reparse(root, path):
    """Reject junctions and symbolic links before resolving a mapped path."""
    if not path.is_relative_to(root):
        raise CatalogIntakeError('Relocation path escapes the repository.')
    current = root
    for part in path.relative_to(root).parts:
        current /= part
        try:
            metadata = io_path(current).lstat()
        except FileNotFoundError:
            continue
        if (stat.S_ISLNK(metadata.st_mode)
                or getattr(metadata, 'st_file_attributes', 0) & 0x400):
            raise CatalogIntakeError('Relocation crosses a reparse point: ' + str(current))


def _load_map(root):
    map_path = root / MAP_PATH
    try:
        metadata = io_path(map_path).stat()
    except FileNotFoundError:
        return None
    _no_reparse(root, map_path)
    signature = (metadata.st_size, metadata.st_mtime_ns)
    key = str(map_path)
    cached = _map_cache.get(key)
    if cached and cached[0] == signature:
        return cached[1]
    data = json.loads(io_path(map_path).read_text(encoding='utf-8-sig'))
    if (data.get('schemaVersion') != 1
            or data.get('state') not in ('planned', 'active')
            or set(data.get('sourceRoots', [])) != set(SOURCE_ROOTS)
            or data.get('destinationRoot') != DESTINATION_ROOT):
        raise CatalogIntakeError('Unexpected Grok relocation map scope or state.')
    indexed = {}
    destinations = {}
    for entry in data.get('entries', []):
        original = entry.get('originalRepoPath', '')
        physical = entry.get('physicalRepoPath', '')
        _portable(original)
        _portable(physical)
        package = _source_package(original)
        if (not package or original == package
                or not physical.startswith(DESTINATION_ROOT + '/')
                or entry.get('action') not in ('move_unique', 'reuse_verified_preferred')
                or type(entry.get('bytes')) is not int or entry['bytes'] < 0
                or not re.fullmatch(r'[a-f0-9]{64}', entry.get('sha256', ''))
                or original in indexed):
            raise CatalogIntakeError('Unsafe or duplicate Grok relocation entry.')
        if entry['action'] == 'move_unique':
            expected = DESTINATION_ROOT + '/' + original[len(SOURCE_PREFIX):]
            if physical != expected:
                raise CatalogIntakeError('Unique Grok relocation changes the package path.')
        identity = (entry['sha256'], entry['bytes'])
        if physical in destinations and destinations[physical] != identity:
            raise CatalogIntakeError('Conflicting Grok relocation destination identities.')
        destinations[physical] = identity
        indexed[original] = entry
    if not indexed:
        raise CatalogIntakeError('Grok relocation map has no verified files.')
    parsed = (data, indexed)
    _map_cache[key] = (signature, parsed)
    return parsed


def resolve_source(repo_root, historical_path, *, expected_sha256=None, expected_bytes=None):
    """Return a current physical Path, verifying each mapped file's identity.

    Intake callers retain their own original-path scope checks. Unmapped sources
    stay unchanged. A mapped source never falls back to a removed Downloads copy
    if the preferred file is absent or has changed.
    """
    root = Path(repo_root).resolve()
    supplied = Path(historical_path)
    if supplied.is_absolute():
        if not supplied.is_relative_to(root):
            raise CatalogIntakeError('Source path is outside the repository.')
        relative = supplied.relative_to(root).as_posix()
    else:
        relative = str(historical_path)
    portable = _portable(relative)
    original = root / Path(*portable.parts)
    package = _source_package(relative)
    if not package:
        return original
    _no_reparse(root, original)
    loaded = _load_map(root)
    if loaded is None or loaded[0]['state'] != 'active':
        return original
    _, indexed = loaded
    entry = indexed.get(relative)
    if entry is None:
        # A package directory remains useful for browsing. Exact file entries
        # also cover duplicates retained in earlier bare preferred groups.
        if any(name.startswith(relative + '/') for name in indexed):
            directory = root / DESTINATION_ROOT / relative[len(SOURCE_PREFIX):]
            _no_reparse(root, directory)
            if io_path(directory).is_dir():
                return directory
        return original
    if ((expected_sha256 is not None and expected_sha256 != entry['sha256'])
            or (expected_bytes is not None and expected_bytes != entry['bytes'])):
        raise CatalogIntakeError('Relocation differs from recorded source identity: ' + relative)
    physical = root / Path(*_portable(entry['physicalRepoPath']).parts)
    _no_reparse(root, physical)
    destination_root = (root / DESTINATION_ROOT).resolve()
    physical = physical.resolve()
    if not physical.is_relative_to(destination_root):
        raise CatalogIntakeError('Grok relocation escapes From Grok.')
    try:
        metadata = io_path(physical).stat()
    except FileNotFoundError as exc:
        raise CatalogIntakeError('Missing relocated Grok source: ' + relative) from exc
    if not stat.S_ISREG(metadata.st_mode) or metadata.st_size != entry['bytes']:
        raise CatalogIntakeError('Changed relocated Grok source size: ' + relative)
    signature = (str(physical), metadata.st_size, metadata.st_mtime_ns,
                 metadata.st_ctime_ns, entry['sha256'])
    if signature not in _verified_cache:
        actual = hashlib.sha256(io_path(physical).read_bytes()).hexdigest()
        if actual != entry['sha256']:
            raise CatalogIntakeError('Changed relocated Grok source hash: ' + relative)
        _verified_cache[signature] = True
    return physical


resolve_grok_source = resolve_source
