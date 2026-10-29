"""Package the complete, current visual-library design for the native studio.

Only design_catalog.json, design_manifest.json and design_media/ are written.
Existing base and Mission bundles are verified caches, never edited. Documents
come from the current catalog's publication src, or an already packaged Mission
document; source originals and writer-only context are never inferred from IDs.
No network access, generation, canonical edits or deployment occurs.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import re
from urllib.parse import unquote, urlsplit
import xml.etree.ElementTree as ET

from build_mission_control import MissionBundle, ROOT, SOURCE, OUT, MAX_FILE_BYTES, clean_text, load_catalog, safe_https, sha


def timestamp(value):
    try:
        result = datetime.fromisoformat(value.replace('Z', '+00:00'))
        return result if result.tzinfo else None
    except (AttributeError, TypeError, ValueError):
        return None


def overlay_plan_clears(catalog, export, export_sha):
    """Apply only explicit null plans newer than an existing, exact-hash plan."""
    assets = {a['id']: a for a in catalog['assets']}
    records = {r['id']: r for r in catalog.get('reviewDecisions', [])}
    receipt = {'sourceSHA256': export_sha, 'applied': [], 'skipped': []}
    if export.get('format') != 'cfa-visual-review-v1' or not isinstance(export.get('items'), list):
        raise ValueError('Unsupported review export')
    duplicates = Counter(r.get('id') for r in export['items'])
    for incoming in export['items']:
        asset_id = incoming.get('id')
        prior, asset = records.get(asset_id), assets.get(asset_id)
        if not prior or not prior.get('shotPlan') or 'shotPlan' not in incoming or incoming['shotPlan'] is not None:
            continue
        reason = None
        before, after = timestamp(prior.get('updatedAt')), timestamp(incoming.get('updatedAt'))
        exported = timestamp(export.get('exported'))
        if duplicates[asset_id] != 1:
            reason = 'Duplicate export identity'
        elif not asset or not asset.get('sha256') or incoming.get('sha256') != asset['sha256'] or prior.get('sha256') != asset['sha256']:
            reason = 'Exact source hash does not match'
        elif not before or not after or not exported or not before < after <= exported:
            reason = 'Clear is not demonstrably newer than the saved plan'
        if reason:
            receipt['skipped'].append({'assetID': asset_id, 'reason': reason})
            continue
        prior['shotPlan'] = None
        # Preserve the record timestamp: this overlay does not date unrelated fields.
        prior['shotPlanClearEvidence'] = {'updatedAt': incoming['updatedAt'], 'exportSHA256': export_sha}
        receipt['applied'].append({'assetID': asset_id, 'sha256': asset['sha256'],
                                   'previousUpdatedAt': prior['updatedAt'], 'clearUpdatedAt': incoming['updatedAt']})
    return receipt


class DesignBundle(MissionBundle):
    def __init__(self, source=SOURCE, out=OUT, root=ROOT, max_file_bytes=MAX_FILE_BYTES,
                 expected_source_sha=None, review_export=None, expected_review_sha=None,
                 review_mode='plan_clears'):
        super().__init__(Path(source), Path(out), Path(root), max_file_bytes)
        if expected_source_sha and sha(self.source_bytes) != expected_source_sha.lower():
            raise RuntimeError('Frozen source catalog hash does not match')
        self.cache = {}
        self.cache_snapshots = {}
        self.cache_verified = {}
        self.reuse_candidates = {}
        for catalog_name, manifest_name in [('catalog.json', 'manifest.json'),
                                             ('mission_control.json', 'mission_manifest.json'),
                                             ('design_catalog.json', 'design_manifest.json')]:
            cp, mp = self.out / catalog_name, self.out / manifest_name
            if not cp.is_file() or not mp.is_file():
                continue
            snapshot = load_catalog(cp)
            manifest = json.loads(mp.read_text(encoding='utf-8-sig'))
            pinned = manifest.get('catalog_sha256') or manifest.get('snapshotSHA256')
            if pinned and sha(cp.read_bytes()) != pinned:
                continue
            outputs = {r['path']: r for r in manifest.get('outputs', [])}
            self.cache_snapshots[catalog_name] = snapshot
            for asset in snapshot['assets']:
                digest = asset.get('sha256')
                for key in ('src', 'thumb'):
                    relative = asset.get(key)
                    record = outputs.get(relative)
                    if digest and record and record.get('source_sha256') == digest:
                        self.reuse_candidates.setdefault((asset.get('kind'), digest, key), []).append((relative, record))
            for relative, record in outputs.items():
                self.cache.setdefault(relative, []).append(record)
        self.private_sources = set()
        self.publication_bindings = {}
        registry = self.source.parent / 'writer_development.json'
        if registry.is_file():
            writer = json.loads(registry.read_text(encoding='utf-8-sig'))
            for row in writer.get('documents', []):
                publication = row.get('publication')
                if publication:
                    original = (self.root / row['path']).resolve()
                    self.private_sources.add(original)
                    self.publication_bindings[original] = publication
            for row in writer.get('excludedSources', []):
                relative = row.get('path') if isinstance(row, dict) else row
                if relative:
                    self.private_sources.add((self.root / relative).resolve())
        self.review_receipt = None
        self.review_source = None
        publication_registry = Path(__file__).with_name('hosted_publications.json')
        self.task_publications = json.loads(publication_registry.read_text(encoding='utf-8')).get('documents', []) if publication_registry.is_file() else []
        if review_export:
            self.review_source = Path(review_export).resolve()
            raw = self.review_source.read_bytes()
            if not expected_review_sha or sha(raw) != expected_review_sha.lower():
                raise RuntimeError('Explicit review export hash does not match')
            self.review_source_bytes = raw
            payload = json.loads(raw.decode('utf-8-sig'))
            if review_mode == 'latest':
                from review_snapshot import overlay_review_snapshot
                self.catalog, report = overlay_review_snapshot(self.catalog, payload)
                self.review_receipt = {**report, 'sourceSHA256': sha(raw)}
                self.review_receipt['conflicts'] = [{k: v for k, v in row.items()
                                                    if k not in {'canonical', 'incoming'}}
                                                   for row in report['conflicts']]
            elif review_mode == 'plan_clears':
                self.review_receipt = overlay_plan_clears(self.catalog, payload, sha(raw))
            else:
                raise ValueError('Unsupported review overlay mode')

    def verified_cache(self, relative, record):
        if not isinstance(relative, str) or not relative or urlsplit(relative).scheme:
            return False
        if '\\' in relative or relative.startswith('/') or '..' in relative.split('/'):
            return False
        path = (self.out / relative).resolve()
        if not path.is_relative_to(self.out) or not path.is_file() or path.stat().st_size > self.max_file_bytes:
            return False
        key = (relative, record.get('sha256'), record.get('bytes'))
        if key not in self.cache_verified:
            raw = path.read_bytes()
            self.cache_verified[key] = len(raw) == record.get('bytes') and sha(raw) == record.get('sha256')
        return self.cache_verified[key]

    def reuse(self, asset, key, digest):
        for relative, record in self.reuse_candidates.get((asset.get('kind'), digest, key), []):
            if self.verified_cache(relative, record):
                self.outputs[relative] = {**record, 'reused': True}
                return relative
        return None

    @staticmethod
    def validate_svg(raw):
        # Keep existing diagram bytes intact for Streamlit's image context, without
        # permitting active content, external dependencies or entity expansion.
        if re.search(br'<!\s*(DOCTYPE|ENTITY)', raw, re.I):
            raise ValueError('SVG declarations and entities are not portable media')
        root = ET.fromstring(raw)
        if root.tag.rsplit('}', 1)[-1] != 'svg':
            raise ValueError('Expected SVG image')
        for element in root.iter():
            if element.tag.rsplit('}', 1)[-1].lower() in {'script', 'foreignobject'}:
                raise ValueError('Active SVG content is not portable media')
            for name, value in element.attrib.items():
                if name.lower().startswith('on'):
                    raise ValueError('SVG event handlers are not portable media')
                if name.rsplit('}', 1)[-1].lower() in {'href', 'src'} and not value.startswith('#'):
                    raise ValueError('External SVG references are not allowed')
        for target in re.findall(br'url\(\s*([^)]*)\)', raw, re.I):
            if not target.strip(b' \t\r\n\'"').startswith(b'#'):
                raise ValueError('External SVG styles are not allowed')
        if re.search(br'@import', raw, re.I):
            raise ValueError('External SVG styles are not allowed')

    def write_media(self, raw, suffix, source_sha, role):
        if len(raw) > self.max_file_bytes:
            raise ValueError('Packaged file exceeds the hosted file size limit')
        relative = f'design_media/{sha(raw)}{suffix}'
        path = self.out / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if path.is_file() and path.read_bytes() != raw:
            raise RuntimeError('Content-addressed output was modified')
        if not path.is_file():
            path.write_bytes(raw)
        self.outputs[relative] = {'path': relative, 'sha256': sha(raw), 'bytes': len(raw),
                                  'source_sha256': source_sha, 'role': role, 'reused': False}
        return relative

    def local_path(self, href, exists=True):
        path = super().local_path(href, exists)
        if path in getattr(self, 'private_sources', set()):
            raise RuntimeError('Writer-only original is not a publication source')
        return path

    def package_asset(self, asset_id):
        asset = self.assets[asset_id]
        # Canonical writer IDs retain their old names, but src/hash must bind the safe copy.
        for original, binding in self.publication_bindings.items():
            if asset_id.endswith(original.relative_to(self.root).as_posix()):
                actual = self.local_path(asset['src'])
                if actual != (self.root / binding['path']).resolve() or asset.get('sha256') != binding['sha256']:
                    raise RuntimeError('Writer publication identity does not bind the safe copy')
        if asset.get('kind') == 'image' and urlsplit(asset.get('src', '')).path.lower().endswith('.svg'):
            raw, digest = self.source_record(self.local_path(asset['src']), asset.get('sha256'))
            self.validate_svg(raw)
            relative = self.write_media(raw, '.svg', digest, 'unchanged_svg')
            item = self.clean_config({**deepcopy(asset), 'src': relative, 'thumb': relative, 'sha256': digest,
                                      'previewStatus': 'Unchanged local placement diagram; scope and reviews preserved.'})
            self.packaged_assets[asset_id] = item
            return item
        return super().package_asset(asset_id)

    def mission_supplement(self, task_id, link, source_path):
        """Reuse only an existing Mission publication, not an unregistered local document."""
        old = self.cache_snapshots.get('mission_control.json', {})
        task = next((t for t in old.get('missionControl', {}).get('tasks', []) if t.get('id') == task_id), {})
        matches = [x for x in task.get('links', []) if x.get('label') == link.get('label')]
        if len(matches) != 1:
            return None
        old_link = matches[0]
        if old_link.get('downloadPath'):
            relative = old_link['downloadPath']
            _, digest = self.source_record(source_path)
            for record in self.cache.get(relative, []):
                if record.get('source_sha256') == digest and self.verified_cache(relative, record):
                    self.outputs[relative] = {**record, 'reused': True}
                    return {'downloadPath': relative}
        asset = next((a for a in old.get('assets', []) if a['id'] == old_link.get('assetID')), None)
        if not asset or not asset['id'].startswith('mission:'):
            return None
        raw, digest = self.source_record(source_path)
        if asset.get('sha256') != digest:
            return None
        copied = deepcopy(asset)
        required = [(key, copied[key]) for key in ('src', 'thumb') if copied.get(key)]
        if not required or any(not any(r.get('source_sha256') == digest and self.verified_cache(relative, r)
                for r in self.cache.get(relative, [])) for _, relative in required):
            return None
        for key, relative in required:
            record = next(r for r in self.cache[relative] if r.get('source_sha256') == digest and self.verified_cache(relative, r))
            self.outputs[relative] = {**record, 'reused': True}
        self.packaged_assets[copied['id']] = copied
        return {'assetID': copied['id']}

    def portable_link(self, link, task_id=None):
        result = {k: deepcopy(v) for k, v in link.items() if k not in {'href', 'downloadPath'}}
        href = link.get('href')
        if not href:
            return result
        if safe_https(href):
            result['href'] = href
            return result
        try:
            parsed = urlsplit(href)
            if parsed.fragment and (not parsed.path or parsed.path.replace('\\', '/').endswith('index.html')):
                result['route'] = '#' + parsed.fragment
                result.update(self.route(parsed.fragment))
                return result
            path = self.local_path(href)
            if path in self.by_source:
                result['assetID'] = self.by_source[path]
                return result
            supplemental = self.mission_supplement(task_id, link, path) if task_id else None
            if supplemental:
                result.update(supplemental)
                return result
            publication = next((item for item in self.task_publications
                                if item.get('taskID') == task_id and item.get('label') == link.get('label')
                                and item.get('path') == path.relative_to(self.root).as_posix()), None)
            if publication and path.suffix.lower() in {'.txt', '.md', '.json', '.csv', '.tsv'}:
                raw, digest = self.source_record(path, publication['sha256'])
                asset_id = 'mission:document:' + digest
                self.assets[asset_id] = {
                    'id': asset_id, 'project': 'shared', 'kind': 'document',
                    'title': link.get('label', path.name), 'filename': path.name,
                    'src': href, 'sha256': digest, 'category': 'documents'}
                self.package_asset(asset_id)
                result['assetID'] = asset_id
                return result
            raise ValueError('Local link is not a current catalog asset or a verified existing Mission publication')
        except (ValueError, OSError) as error:
            result['unavailableReason'] = str(error)
            self.unavailable.append({'taskID': task_id, 'label': link.get('label', ''), 'reason': str(error)})
            return result

    def clean_config(self, value):
        if isinstance(value, str):
            return clean_text(value, self.root)
        if isinstance(value, list):
            return [self.clean_config(x) for x in value]
        if isinstance(value, dict):
            source = self.portable_link(value) if 'href' in value else value
            return {k: self.clean_config(v) for k, v in source.items()}
        return value

    def package_review_supplements(self, supplements):
        """Carry only registered supplement media/evidence into the portable bundle."""
        by_sha = {a.get('sha256'): a for a in self.packaged_assets.values()
                  if a.get('sha256') and a.get('src')}
        thumbnail_hashes = {item['thumbURL']: item['thumbnailSHA256']
                            for supplement in supplements for item in supplement.get('items', [])
                            if item.get('thumbURL') and item.get('thumbnailSHA256')}

        def evidence(url, expected=None):
            if not url:
                return None
            if safe_https(url):
                return url
            # Reference links can identify an unavailable original while pointing
            # at its separately hash-bound supplied thumbnail.
            expected = thumbnail_hashes.get(url, expected)
            try:
                path = self.local_path(url)
                known = self.packaged_assets.get(self.by_source.get(path), {})
                if known.get('src') and (not expected or known.get('sha256') == expected):
                    return known['src']
                if path.suffix.lower() in {'.jpg', '.jpeg', '.png', '.webp'}:
                    raw, digest = self.source_record(path, expected)
                    return self.write_media(raw, path.suffix.lower(), digest, 'supplement_evidence_image')
                if path.suffix.lower() not in {'.txt', '.md', '.csv', '.tsv', '.json', '.sha256'}:
                    raise ValueError('Evidence is not a portable text source')
                raw, digest = self.source_record(path, expected)
                suffix = path.suffix.lower() if path.suffix.lower() in {'.csv', '.tsv', '.json'} else '.txt'
                clean = clean_text(raw.decode('utf-8-sig', 'replace'), self.root).encode('utf-8')
                return self.write_media(clean, suffix, digest, 'supplement_evidence')
            except (ValueError, OSError) as error:
                self.unavailable.append({'supplementURL': url, 'reason': str(error)})
                return None

        def record(value):
            if isinstance(value, list):
                return [record(item) for item in value]
            if not isinstance(value, dict):
                return value
            result = {key: record(item) for key, item in value.items()}
            asset = by_sha.get(value.get('sha256'))
            if 'fullImageURL' in value:
                result['fullImageURL'] = asset.get('src') if asset else None
            if value.get('thumbURL'):
                if asset and asset.get('thumb'):
                    result['thumbURL'] = asset['thumb']
                else:
                    try:
                        raw, digest = self.source_record(self.local_path(value['thumbURL']), value.get('thumbnailSHA256'))
                        result['thumbURL'] = self.write_media(self.jpeg(raw, 480, 85), '.jpg', digest, 'supplement_thumbnail')
                    except (ValueError, OSError) as error:
                        result['thumbURL'] = None
                        self.unavailable.append({'supplementID': value.get('id'), 'reason': str(error)})
            if 'url' in value:
                result['url'] = evidence(value['url'], value.get('sha256'))
            for key in ('csvURL', 'receiptURL', 'lineageURL'):
                if value.get(key):
                    result[key] = evidence(value[key])
            # The full mirror generates a visual map from these exact records.
            # Supplier HTML is not copied with its machine-local links.
            for key in ('indexURL', 'sourceURL'):
                if key in result and not safe_https(result[key]):
                    result[key] = None
            return result

        return record(supplements)

    def build(self, generated_at=None):
        source_ids = list(self.assets)
        for index, asset_id in enumerate(source_ids, 1):
            self.package_asset(asset_id)
            if index % 250 == 0:
                print(f'Packaged {index}/{len(source_ids)} catalog assets', flush=True)
        result = deepcopy(self.catalog)
        result['reviewSupplements'] = self.package_review_supplements(result.get('reviewSupplements', []))
        mission = deepcopy(result.get('missionControl', {}))
        for task in mission.get('tasks', []):
            if task.get('id') == 'favorites-prop-sweep':
                task['variantAssetIDs'] = [a['id'] for a in self.assets.values() if a.get('project') == 'hon'
                    and a.get('kind') == 'image' and a.get('sourceIntake') == 'HON-GROK-RETURN-20261009'
                    and a.get('propState') == 'with_gun' and a.get('outfitAlbumID')]
            task['links'] = [self.portable_link(link, task.get('id')) for link in task.get('links', [])]
        result['missionControl'] = mission
        result['assets'] = list(self.packaged_assets.values())
        result = self.clean_config(result)
        for path, record in self.sources.items():
            if not path.is_file() or sha(path.read_bytes()) != record['sha256']:
                raise RuntimeError('Source changed during design packaging')
        if self.source.read_bytes() != self.source_bytes:
            raise RuntimeError('Source catalog changed during design packaging')
        if self.review_source and self.review_source.read_bytes() != self.review_source_bytes:
            raise RuntimeError('Review export changed during design packaging')
        # Recheck every reused file as part of the final publication allowlist.
        for relative, record in self.outputs.items():
            raw = (self.out / relative).read_bytes()
            if sha(raw) != record['sha256'] or len(raw) != record['bytes']:
                raise RuntimeError('Packaged media changed during design packaging')
        snapshot = {'schema': 'cfa-design-snapshot-v1',
                    'generatedAtUTC': generated_at or datetime.now(timezone.utc).isoformat(),
                    'sourceCatalog': {'path': self.source.relative_to(self.root).as_posix(), 'sha256': sha(self.source_bytes)},
                    'purpose': 'Complete portable local design snapshot; saved reviews, not live synchronization.',
                    'sourceAssetCount': len(source_ids), 'supplementalAssetCount': len(result['assets']) - len(source_ids),
                    'unavailableLinks': self.unavailable,
                    'reviewOverlay': self.review_receipt}
        result['designSnapshot'] = snapshot
        data = json.dumps(result, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
        outputs = [self.outputs[k] for k in sorted(self.outputs)]
        outputs.append({'path': 'design_catalog.json', 'bytes': len(data), 'sha256': sha(data), 'role': 'design_catalog', 'reused': False})
        manifest = {'schema': 'cfa-design-manifest-v1', 'snapshot': snapshot, 'snapshotSHA256': sha(data),
                    'builderSHA256': sha(Path(__file__).read_bytes()), 'sourcesPreserved': True,
                    'assetKinds': dict(Counter(a['kind'] for a in result['assets'])),
                    'outputBytes': sum(r['bytes'] for r in outputs),
                    'sources': [self.sources[p] for p in sorted(self.sources)], 'outputs': outputs,
                    'publicationFiles': sorted([r['path'] for r in outputs] + ['design_manifest.json'])}
        self.out.mkdir(parents=True, exist_ok=True)
        output, manifest_path = self.out / 'design_catalog.json', self.out / 'design_manifest.json'
        temp = output.with_suffix('.json.tmp')
        temp.write_bytes(data)
        manifest_temp = manifest_path.with_suffix('.json.tmp')
        manifest_temp.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
        manifest_temp.replace(manifest_path)
        temp.replace(output)
        return result


def build_bundle(source=SOURCE, out=OUT, root=ROOT, generated_at=None, **kwargs):
    return DesignBundle(source, out, root, **kwargs).build(generated_at)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=SOURCE)
    parser.add_argument('--out', type=Path, default=OUT)
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--expected-source-sha')
    parser.add_argument('--review-export', type=Path)
    parser.add_argument('--expected-review-sha')
    parser.add_argument('--review-mode', choices=('plan_clears', 'latest'), default='plan_clears')
    args = parser.parse_args()
    result = build_bundle(args.source, args.out, args.root, expected_source_sha=args.expected_source_sha,
                          review_export=args.review_export, expected_review_sha=args.expected_review_sha,
                          review_mode=args.review_mode)
    print(json.dumps({'assets': len(result['assets']), **result['designSnapshot']}, indent=2))


if __name__ == '__main__':
    main()
