"""Package the local index's Ziggy's Corner without replacing the hosted library.

Run from any directory: python apps/creative_studio/build_mission_control.py
The only published outputs are mission_control.json, mission_manifest.json and
mission_media/. Existing catalog.json and its media are read-only cache inputs.
No network access, archive extraction, source changes or deployment occurs.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
from io import BytesIO
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[2]
SOURCE = ROOT / 'docs/notes/explorable_world/comfy/projects/visual_library/catalog.js'
OUT = Path(__file__).resolve().parent / 'library'
MAX_FILE_BYTES = 100 * 1024 * 1024  # Existing hosted basket limit; also bound each new file.
TEXT_SUFFIXES = {'.txt', '.md', '.json', '.csv', '.tsv', '.yaml', '.yml', '.py', '.js', '.html', '.css', '.log'}
IMAGE_SUFFIXES = {'.jpg', '.jpeg', '.png', '.webp', '.bmp'}


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_catalog(path: Path) -> dict:
    text = path.read_text(encoding='utf-8-sig').strip()
    if path.suffix.lower() == '.js':
        text = text.split('=', 1)[1].strip().rstrip(';')
    result = json.loads(text)
    if not isinstance(result, dict) or not isinstance(result.get('assets'), list):
        raise ValueError('Invalid catalog')
    return result


def safe_https(value: str) -> bool:
    if not isinstance(value, str) or any(ord(char) < 32 for char in value):
        return False
    try:
        parsed = urlsplit(value)
        return parsed.scheme == 'https' and bool(parsed.hostname) and not parsed.username and not parsed.password
    except ValueError:
        return False


def clean_text(value: str, root: Path) -> str:
    for prefix in (str(root), root.as_posix()):
        value = re.sub(re.escape(prefix) + r'[\\/]*', '', value, flags=re.I)
    value = re.sub(r'(?i)file://[^\s"<>]+', '[local file]', value)
    return re.sub(r'(?i)\b[A-Z]:[\\/][^\s"<>|]+', '[local path]', value)


def clean_values(value, root: Path):
    if isinstance(value, str):
        return clean_text(value, root)
    if isinstance(value, list):
        return [clean_values(item, root) for item in value]
    if isinstance(value, dict):
        return {key: clean_values(item, root) for key, item in value.items()
                if key != 'href' or safe_https(item)}
    return value


def referenced_ids(value):
    """Collect explicit media references, without interpreting prose as IDs."""
    if isinstance(value, list):
        for item in value:
            yield from referenced_ids(item)
    elif isinstance(value, dict):
        for key, item in value.items():
            if (key.endswith('AssetID') or key == 'assetID' or key == 'coverID') and isinstance(item, str):
                yield item
            elif (key.endswith('AssetIDs') or key in {'assetIDs', 'currentIDs', 'historyIDs', 'relatedIDs'}) and isinstance(item, list):
                yield from (asset_id for asset_id in item if isinstance(asset_id, str))
            elif isinstance(item, (dict, list)):
                yield from referenced_ids(item)


class MissionBundle:
    def __init__(self, source: Path, out: Path, root: Path, max_file_bytes=MAX_FILE_BYTES):
        self.source, self.out, self.root = source.resolve(), out.resolve(), root.resolve()
        if not self.source.is_relative_to(self.root):
            raise ValueError('Source catalog must be inside the source root')
        self.max_file_bytes = max_file_bytes
        self.source_bytes = self.source.read_bytes()
        self.catalog = load_catalog(self.source)
        self.assets = {asset['id']: asset for asset in self.catalog['assets']}
        self.albums = {album['id']: album for album in self.catalog.get('albums', [])}
        self.collections = {item['id']: item for item in self.catalog.get('castCollections', [])}
        self.selected, self.selected_albums = set(), {}
        self.outputs, self.sources, self.unavailable = {}, {}, []
        self.packaged_assets = {}
        self.old_assets, self.old_outputs = {}, {}
        if (self.out / 'catalog.json').is_file() and (self.out / 'manifest.json').is_file():
            self.old_assets = {a['id']: a for a in load_catalog(self.out / 'catalog.json')['assets']}
            old = json.loads((self.out / 'manifest.json').read_text(encoding='utf-8'))
            self.old_outputs = {item['path']: item for item in old.get('outputs', [])}
        self.by_source = {}
        for asset in self.assets.values():
            try:
                self.by_source.setdefault(self.local_path(asset.get('src', ''), exists=False), asset['id'])
            except ValueError:
                pass

    def local_path(self, href: str, exists=True) -> Path:
        if not isinstance(href, str) or not href or '\x00' in href:
            raise ValueError('Missing local reference')
        parsed = urlsplit(href)
        if parsed.scheme or parsed.netloc or href.startswith(('\\', '/')):
            raise ValueError('External or absolute local reference')
        path = (self.source.parent / unquote(parsed.path).replace('\\', '/')).resolve()
        if not path.is_relative_to(self.root) or (exists and not path.is_file()):
            raise ValueError('Missing or out-of-root reference')
        return path

    def source_record(self, path: Path, registered_hash=None) -> tuple[bytes, str]:
        if path.stat().st_size > self.max_file_bytes:
            raise ValueError('Reference exceeds the hosted file size limit')
        raw = path.read_bytes()
        digest = sha(raw)
        if registered_hash and digest.lower() != registered_hash.lower():
            raise RuntimeError(f'Registered source hash changed: {path.relative_to(self.root)}')
        self.sources[path] = {'path': path.relative_to(self.root).as_posix(), 'sha256': digest, 'bytes': len(raw)}
        return raw, digest

    def write_media(self, raw: bytes, suffix: str, source_sha: str, role: str) -> str:
        if len(raw) > self.max_file_bytes:
            raise ValueError('Packaged file exceeds the hosted file size limit')
        relative = f'mission_media/{sha(raw)}{suffix}'
        path = self.out / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.is_file() or path.read_bytes() != raw:
            path.write_bytes(raw)
        self.outputs[relative] = {'path': relative, 'sha256': sha(raw), 'bytes': len(raw),
                                  'source_sha256': source_sha, 'role': role, 'reused': False}
        return relative

    def reuse(self, asset: dict, key: str, digest: str) -> str | None:
        old = self.old_assets.get(asset['id'], {})
        if old.get('sha256') != digest or not isinstance(old.get(key), str):
            return None
        relative = old[key]
        path = (self.out / relative).resolve()
        record = self.old_outputs.get(relative, {})
        if not path.is_relative_to(self.out) or not path.is_file() or record.get('source_sha256') != digest:
            return None
        if path.stat().st_size > self.max_file_bytes:
            return None
        raw = path.read_bytes()
        if record.get('bytes') != len(raw) or record.get('sha256') != sha(raw):
            return None
        self.outputs[relative] = {**record, 'reused': True}
        return relative

    @staticmethod
    def jpeg(raw: bytes, edge: int, quality: int) -> bytes:
        with Image.open(BytesIO(raw)) as image:
            image = ImageOps.exif_transpose(image).convert('RGB')
            image.thumbnail((edge, edge), Image.Resampling.LANCZOS)
            stream = BytesIO()
            image.save(stream, format='JPEG', quality=quality, optimize=True)
            return stream.getvalue()

    def package_asset(self, asset_id: str) -> dict | None:
        if asset_id in self.packaged_assets:
            return self.packaged_assets[asset_id]
        original = self.assets.get(asset_id)
        if not original:
            self.unavailable.append({'assetID': asset_id, 'reason': 'Reference is absent from the source catalog'})
            return None
        item = deepcopy(original)
        try:
            path = self.local_path(item.get('src', ''))
            raw, digest = self.source_record(path, item.get('sha256'))
            kind = item.get('kind', 'document')
            item.pop('thumb', None)
            if kind == 'image':
                item['src'] = self.reuse(original, 'src', digest) or self.write_media(self.jpeg(raw, 1280, 82), '.jpg', digest, 'image_preview')
                item['thumb'] = self.reuse(original, 'thumb', digest) or self.write_media(self.jpeg(raw, 480, 85), '.jpg', digest, 'thumbnail')
            elif kind in {'video', 'gif', 'pdf'}:
                permitted = {'video': {'.mp4', '.webm', '.mov'}, 'gif': {'.gif'}, 'pdf': {'.pdf'}}[kind]
                if path.suffix.lower() not in permitted:
                    raise ValueError('Unsupported media extension')
                item['src'] = self.reuse(original, 'src', digest) or self.write_media(raw, path.suffix.lower(), digest, 'unchanged_' + kind)
                if original.get('thumb'):
                    item['thumb'] = self.reuse(original, 'thumb', digest)
                    if not item['thumb']:
                        thumb_path = self.local_path(original['thumb'])
                        thumb_raw, _ = self.source_record(thumb_path)
                        item['thumb'] = self.write_media(self.jpeg(thumb_raw, 480, 85), '.jpg', digest, 'thumbnail')
            else:
                if path.suffix.lower() not in TEXT_SUFFIXES:
                    raise ValueError('Unsupported document extension')
                item['kind'] = 'document'
                item['text'] = clean_text(raw.decode('utf-8-sig', 'replace'), self.root).rstrip('\r\n') + '\n'
                item['src'] = self.write_media(item['text'].encode('utf-8'), '.txt', digest, 'inert_text')
                item['inert'] = True
            item['sha256'] = digest
            item['previewStatus'] = 'Hosted review copy; original source and review identity preserved.'
        except (ValueError, OSError) as error:
            self.unavailable.append({'assetID': asset_id, 'reason': str(error)})
            item.pop('src', None)
            item.pop('thumb', None)
            item['unavailableReason'] = str(error)
        self.packaged_assets[asset_id] = clean_values(item, self.root)
        return self.packaged_assets[asset_id]

    def route(self, fragment: str) -> dict:
        parts = unquote(fragment).split('/')
        if len(parts) < 2 or parts[0] not in {p['id'] for p in self.catalog.get('projects', [])}:
            return {'unavailableReason': 'This index route is not available in the hosted snapshot'}
        project, category = parts[:2]
        route_id = parts[2] if len(parts) > 2 else None
        if route_id:
            collection = self.collections.get(route_id)
            album = self.albums.get(route_id)
            if collection:
                ids = list(dict.fromkeys(referenced_ids(collection)))
                album = {'id': route_id, 'project': project, 'category': category,
                         'title': collection.get('title', route_id), 'assetIDs': ids}
            elif album:
                ids = list(album.get('assetIDs', []))
            else:
                return {'unavailableReason': 'This index collection is absent from the snapshot'}
            self.selected_albums[route_id] = deepcopy(album)
            result = {'albumID': route_id, 'assetIDs': ids}
        elif category == 'shot_plans':
            ids = [r['id'] for r in self.catalog.get('reviewDecisions', [])
                   if r.get('shotPlan') and self.assets.get(r['id'], {}).get('project') == project]
            result = {'assetIDs': ids}
        elif category in {'all', 'review'} or any(a.get('category') == category for a in self.assets.values()):
            ids = [a['id'] for a in self.assets.values() if a.get('project') == project and
                   (category == 'all' or a.get('category') == category)]
            result = {'assetIDs': ids}
        else:
            return {'unavailableReason': 'This index view is not a hosted reference collection'}
        self.selected.update(ids)
        if not ids:
            result['unavailableReason'] = 'No saved references are available for this index route'
        return result

    def normalize_link(self, link: dict, task_project: str) -> dict:
        result = {k: deepcopy(v) for k, v in link.items() if k not in {'href', 'downloadPath'}}
        if link.get('assetID'):
            self.selected.add(link['assetID'])
            if link['assetID'] not in self.assets:
                result['unavailableReason'] = 'Reference is absent from the source catalog'
            return result
        if link.get('assetIDs'):
            self.selected.update(link['assetIDs'])
            return result
        href = link.get('href', '')
        if safe_https(href):
            result['href'] = href
            return result
        try:
            parsed = urlsplit(href)
            if parsed.fragment and (not parsed.path or parsed.path.replace('\\', '/').endswith('index.html')):
                result.update(self.route(parsed.fragment))
                return result
            path = self.local_path(href)
            known_id = self.by_source.get(path)
            if known_id:
                result['assetID'] = known_id
                self.selected.add(known_id)
                return result
            raw, digest = self.source_record(path)
            if path.suffix.lower() == '.zip':
                result['downloadPath'] = self.write_media(raw, '.zip', digest, 'unchanged_care_package')
                return result
            kind = 'image' if path.suffix.lower() in IMAGE_SUFFIXES else 'document'
            if kind == 'document' and path.suffix.lower() not in TEXT_SUFFIXES:
                raise ValueError('This local link has an unsupported file type')
            asset_id = 'mission:' + kind + ':' + digest
            self.assets[asset_id] = {'id': asset_id, 'project': task_project, 'kind': kind,
                                     'title': link.get('label', path.name), 'filename': path.name,
                                     'src': href, 'sha256': digest, 'category': 'documents' if kind == 'document' else 'review'}
            self.by_source[path] = asset_id
            result['assetID'] = asset_id
            self.selected.add(asset_id)
        except (ValueError, OSError) as error:
            result['unavailableReason'] = str(error)
        return result

    def build(self, generated_at=None) -> dict:
        mission = deepcopy(self.catalog.get('missionControl', {}))
        for task in mission.get('tasks', []):
            self.selected.update(referenced_ids(task))
            if task.get('id') == 'favorites-prop-sweep':
                task['variantAssetIDs'] = [a['id'] for a in self.assets.values() if a.get('project') == 'hon'
                    and a.get('kind') == 'image' and a.get('sourceIntake') == 'HON-GROK-RETURN-20261009'
                    and a.get('propState') == 'with_gun' and a.get('outfitAlbumID')]
                self.selected.update(task['variantAssetIDs'])
            task['links'] = [self.normalize_link(link, task.get('project', 'unassigned')) for link in task.get('links', [])]
        comparisons = deepcopy(self.catalog.get('sourceComparisons', []))
        self.selected.update(referenced_ids(comparisons))
        requests = deepcopy(self.catalog.get('reviewRequests', []))
        self.selected.update(r['id'] for r in requests if r.get('id'))
        # Review/export helpers require identity records as well as decisions.
        # Retain all saved reviews without broadening the ordinary hosted library.
        decisions = deepcopy(self.catalog.get('reviewDecisions', []))
        self.selected.update(r['id'] for r in decisions if r.get('id'))
        for asset_id in sorted(self.selected):
            self.package_asset(asset_id)
        for task in mission.get('tasks', []):
            for link in task.get('links', []):
                item = self.packaged_assets.get(link.get('assetID'), {})
                if item.get('unavailableReason'):
                    link['unavailableReason'] = item['unavailableReason']
                if link.get('unavailableReason'):
                    self.unavailable.append({'taskID': task.get('id'), 'label': link.get('label', ''),
                                             'reason': link['unavailableReason']})
        for album in self.catalog.get('albums', []):
            members = [asset_id for asset_id in album.get('assetIDs', []) if asset_id in self.selected]
            if members and album['id'] not in self.selected_albums:
                self.selected_albums[album['id']] = {**album, 'assetIDs': members}
        snapshot = {'schema': 'cfa-mission-control-snapshot-v1',
                    'generatedAtUTC': generated_at or datetime.now(timezone.utc).isoformat(),
                    'sourceCatalog': {'path': self.source.relative_to(self.root).as_posix(), 'sha256': sha(self.source_bytes)},
                    'purpose': 'Saved local index state for Ziggy\u2019s Corner; not a live or two-way review sync.',
                    'unavailableLinks': self.unavailable}
        result = clean_values({'snapshot': snapshot, 'projects': self.catalog.get('projects', []),
                               'categories': self.catalog.get('categories', []), 'assets': list(self.packaged_assets.values()),
                               'albums': list(self.selected_albums.values()), 'missionControl': mission,
                               'sourceComparisons': comparisons, 'reviewRequests': requests, 'reviewDecisions': decisions}, self.root)
        for path, record in self.sources.items():
            if not path.is_file() or sha(path.read_bytes()) != record['sha256']:
                raise RuntimeError('Source file changed during packaging; retry with a stable snapshot')
        if self.source.read_bytes() != self.source_bytes:
            raise RuntimeError('Source catalog changed during packaging; retry with the new snapshot')
        self.out.mkdir(parents=True, exist_ok=True)
        output = self.out / 'mission_control.json'
        data = json.dumps(result, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
        manifest = {'schema': 'cfa-mission-control-manifest-v1', 'snapshot': snapshot,
                    'snapshotSHA256': sha(data), 'sourcesPreserved': True,
                    'sources': [self.sources[p] for p in sorted(self.sources)],
                    'outputs': [self.outputs[p] for p in sorted(self.outputs)]}
        # Promote only complete validated snapshots; failed builds leave the
        # previous usable snapshot intact. Content-addressed media may coexist.
        temporary = output.with_suffix('.json.tmp')
        temporary.write_bytes(data)
        manifest_path = self.out / 'mission_manifest.json'
        manifest_temporary = manifest_path.with_suffix('.json.tmp')
        manifest_temporary.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
        manifest_temporary.replace(manifest_path)
        temporary.replace(output)
        return result


def build_bundle(source=SOURCE, out=OUT, root=ROOT, generated_at=None, max_file_bytes=MAX_FILE_BYTES):
    return MissionBundle(Path(source), Path(out), Path(root), max_file_bytes).build(generated_at)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=SOURCE)
    parser.add_argument('--out', type=Path, default=OUT)
    parser.add_argument('--root', type=Path, default=ROOT)
    args = parser.parse_args()
    bundle = build_bundle(args.source, args.out, args.root)
    print(json.dumps({'assets': len(bundle['assets']), 'tasks': len(bundle['missionControl'].get('tasks', [])),
                      'unavailableAssets': len(bundle['snapshot']['unavailableLinks']),
                      'sourceCatalog': bundle['snapshot']['sourceCatalog']}, indent=2))


if __name__ == '__main__':
    main()
