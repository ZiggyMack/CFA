"""Build the current HTML dashboard from the verified hosted design publication.

No original masters, arbitrary repository files, network calls or deployment.
The generated component serves only manifest-verified browser copies, the exact
local UI, and generated wrappers. Image IDs and original hashes remain unchanged.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
from html import escape
import json
import os
from pathlib import Path
import posixpath
import re
import shutil
from urllib.parse import quote, unquote, urlsplit

from build_full_dashboard import APP, ROOT, VISUAL, DEFAULT_OUTPUT, write_generated

FORMAT = "cfa-portable-dashboard-v1"
ALLOWED_SUFFIXES = {'.jpg', '.jpeg', '.png', '.webp', '.avif', '.gif', '.svg', '.mp4', '.webm', '.mov', '.mp3', '.wav', '.m4a', '.pdf', '.txt', '.json', '.csv', '.tsv', '.md', '.zip'}


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def relative_path(value: str) -> str:
    if not isinstance(value, str) or not value or re.search(r'[\\%?#:\x00-\x1f\x7f]', value):
        raise ValueError('Unsafe publication path')
    if value.startswith('/') or any(p in ('', '.', '..') for p in value.split('/')):
        raise ValueError('Unsafe publication path')
    return value


def verified_files(design: Path, manifest: dict, raw_catalog: bytes) -> dict:
    if manifest.get('schema') != 'cfa-design-manifest-v1' or sha(raw_catalog) != manifest.get('snapshotSHA256'):
        raise ValueError('Design snapshot does not match its publication manifest')
    records = {}
    for record in manifest.get('outputs', []):
        relative = relative_path(record.get('path'))
        if relative in records:
            raise ValueError('Repeated publication path')
        target = (design / relative).resolve()
        if not target.is_relative_to(design) or not target.is_file():
            raise ValueError('Missing or redirected publication file: ' + relative)
        if target.suffix.lower() not in ALLOWED_SUFFIXES:
            raise ValueError('Unsupported active publication file: ' + relative)
        raw = target.read_bytes()
        if len(raw) != record.get('bytes') or sha(raw) != record.get('sha256'):
            raise ValueError('Publication file changed: ' + relative)
        records[relative] = record
    if 'design_catalog.json' not in records:
        raise ValueError('Catalog is absent from the publication allowlist')
    return records


def winners_index(supplement: dict, assets: dict) -> bytes:
    """Recreate the useful visual map using sanitized records and hosted media."""
    groups = [('approved', 'Golden references'), ('validated', 'V-Team scoped passes'), ('preliminary', 'Preliminary mouth picks')]
    content = []
    for group, title in groups:
        items = [i for i in supplement.get('items', []) if i.get('group') == group]
        if not items:
            continue
        cards = []
        for item in items:
            asset = assets.get(item.get('exactAssetID'), {})
            matched = asset.get('sha256') == item.get('sha256') and asset.get('src')
            thumb = item.get('thumbURL') or (asset.get('thumb') if matched else '')
            image = f'<img loading="lazy" src="{escape(thumb, quote=True)}" alt="{escape(item.get("title", "Reference"), quote=True)}">' if thumb else '<p>Preview unavailable</p>'
            fields = [('Version', item.get('version')), ('Team finding', item.get('vVerdict') or item.get('label')), ('Checked scope', item.get('reviewScope')), ('Advisory', item.get('advisories')), ('Source', item.get('sourceEvidence')), ('SHA-256', item.get('sha256'))]
            details = ''.join(f'<dt>{escape(label)}</dt><dd>{escape(str(value))}</dd>' for label, value in fields if value)
            action = ''
            if matched:
                route = '#'+ '/'.join(quote(str(x), safe='') for x in [asset.get('project', 'hon'), 'asset', asset['id']])
                action = f'<a class="action" href="index.html{route}">Review image in the library</a>'
            cards.append(f'<article>{image}<div class="copy"><h3>{escape(item.get("title", "Reference"))}</h3>{action}<dl>{details}</dl></div></article>')
        content.append(f'<section><h2>{escape(title)} · {len(items)}</h2><div class="grid">{"".join(cards)}</div></section>')
    page = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Winners visual index | CFA</title><style>
body{margin:0;padding:24px;background:#11151b;color:#edf0f5;font:15px/1.5 system-ui}a{color:#d8c095}h1{margin:0}h2{padding:15px 0;border-bottom:1px solid #455262}.intro{max-width:900px;color:#b8c8d9}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));gap:16px}article{background:#1b2532;border:1px solid #354657;border-radius:10px;overflow:hidden;min-width:0}img{display:block;width:100%;height:230px;object-fit:contain;background:#080e15}.copy{padding:16px}h3{margin:0 0 12px;font-size:17px}dt{font-weight:650;margin-top:12px}dd{margin:3px 0;overflow-wrap:anywhere;color:#bacbdd}.action{display:inline-block;padding:8px 12px;border:1px solid #ad946b;border-radius:7px}section{margin:30px 0}@media(max-width:600px){body{padding:15px}.grid{grid-template-columns:1fr}}
</style><a href="index.html#hon/intake">← Intake verification</a><h1>Winners visual index</h1><p class="intro">The supplied selections, team findings and review scope, presented with hosted review copies. Open an image in the library to record your decision. Team findings and your decisions remain separate; preliminary picks are not V-Team validations.</p>'''+''.join(content)+'</html>'
    return page.encode('utf-8')


def build(design: Path = APP / 'library', source: Path = VISUAL, output: Path = DEFAULT_OUTPUT,
          root: Path = ROOT, copy_media: bool = False) -> dict:
    root, design, source, output = (p.resolve() for p in (root, design, source, output))
    if any(not p.is_relative_to(root) for p in (design, source, output)):
        raise ValueError('Build paths must stay inside the repository')
    if output in (source, design) or source.is_relative_to(output) or design.is_relative_to(output):
        raise ValueError('Bundle must be separate from its inputs')
    raw_catalog = (design / 'design_catalog.json').read_bytes()
    manifest_raw = (design / 'design_manifest.json').read_bytes()
    manifest = json.loads(manifest_raw)
    records = verified_files(design, manifest, raw_catalog)
    original = json.loads(raw_catalog)
    catalog = deepcopy(original)
    source_catalog = (source / 'catalog.js').read_bytes()
    provenance = manifest.get('snapshot', {}).get('sourceCatalog', {})
    if provenance.get('sha256') != sha(source_catalog):
        raise ValueError('Design publication is stale against the local catalog; rebuild it first')
    inputs = {name: (source / name).read_bytes() for name in ('library.js', 'library.css')}
    inputs.update({name: (APP / name).read_bytes() for name in ('full_dashboard_bridge.js', 'hosted_dashboard.js', 'hosted_dashboard_seed.js', 'hosted_dashboard.css')})
    hashes = {name: sha(raw) for name, raw in inputs.items()}
    hashes.update({'design_catalog.json': sha(raw_catalog), 'design_manifest.json': sha(manifest_raw), 'builder': sha(Path(__file__).read_bytes())})
    mode = 'copy' if copy_media else 'hardlink'
    build_id = sha(json.dumps({'format': FORMAT, 'hashes': hashes, 'mode': mode}, sort_keys=True).encode())[:20]
    snapshot = output / 'snapshots' / build_id
    snapshot.mkdir(parents=True, exist_ok=True)
    if not snapshot.resolve().is_relative_to(output):
        raise ValueError('Bundle destination contains an unexpected path redirect')
    by_id = {a['id']: a for a in catalog['assets']}
    media_records = {k: v for k, v in records.items() if k != 'design_catalog.json'}
    unresolved = []
    referenced = set()
    generated = set()
    source_base = posixpath.dirname(provenance.get('path', ''))
    outputs_by_hash = {}
    for relative, record in media_records.items():
        outputs_by_hash.setdefault(record.get('source_sha256'), []).append((relative, record))
    by_source = {}
    for record in manifest.get('sources', []):
        candidates = outputs_by_hash.get(record.get('sha256'), [])
        candidates.sort(key=lambda pair: pair[1].get('role') == 'thumbnail')
        if candidates:
            by_source[record['path']] = candidates[0][0]

    def package_path(relative):
        referenced.add(relative)
        return 'library/' + relative

    def portable_url(value, owner, key, trail):
        if not value:
            return None
        if value in generated:
            return value
        try:
            parsed = urlsplit(value)
        except ValueError:
            unresolved.append({'field': trail + '.' + key, 'reason': 'Invalid source URL'})
            return None
        if parsed.scheme == 'https' and parsed.hostname and not parsed.username and not parsed.password:
            return value
        if value.startswith('#'):
            return value
        if not parsed.scheme and not parsed.netloc and parsed.fragment and (not parsed.path or parsed.path.endswith('index.html')):
            return '#' + parsed.fragment
        if value in media_records:
            return package_path(value)
        if value.startswith('library/') and value[8:] in media_records:
            return package_path(value[8:])
        if not parsed.scheme and not parsed.netloc and not parsed.query and not parsed.fragment:
            normalized = posixpath.normpath(posixpath.join(source_base, unquote(parsed.path).replace('\\', '/')))
            if normalized in by_source:
                return package_path(by_source[normalized])
        if key in {'fullImageURL', 'thumbURL', 'url'} and owner.get('sha256'):
            asset = by_id.get(owner.get('exactAssetID') or owner.get('assetID'))
            if asset and asset.get('sha256') == owner['sha256']:
                relative = asset.get('thumb' if key == 'thumbURL' else 'src')
                if relative in media_records:
                    return package_path(relative)
                if relative and relative.startswith('library/') and relative[8:] in media_records:
                    return package_path(relative[8:])
        unresolved.append({'field': trail + '.' + key, 'reason': 'Not part of the verified hosted publication'})
        return None

    for number, supplement in enumerate(catalog.get('reviewSupplements', []), 1):
        name = f'winners-index-{number}.html'
        generated.add(name)
        supplement['indexURL'] = name
        supplement['sourceURL'] = name

    def rewrite(value, trail='catalog'):
        if isinstance(value, list):
            return [rewrite(v, f'{trail}[{n}]') for n, v in enumerate(value)]
        if not isinstance(value, dict):
            return value
        result = {}
        for key, item in value.items():
            # User review payloads are evidence, not navigation instructions.
            if key in {'reviewDecisions', 'sceneReviews'}:
                result[key] = item
            elif isinstance(item, str) and (key in {'src', 'thumb', 'href', 'url', 'downloadPath'} or key.endswith(('URL', 'Href'))):
                mapped = portable_url(item, value, key, trail)
                if mapped:
                    result[key] = mapped
            else:
                result[key] = rewrite(item, trail + '.' + key)
        if 'href' not in result and isinstance(result.get('route'), str) and result['route'].startswith('#'):
            result['href'] = result['route']
        elif 'href' not in result and result.get('downloadPath'):
            result['href'] = result['downloadPath']
        elif 'href' not in result and result.get('label') and result.get('assetID') in by_id:
            asset = by_id[result['assetID']]
            if asset.get('src'):
                result['href'] = '#' + '/'.join(quote(str(x), safe='') for x in (asset['project'], 'asset', asset['id']))
        return result

    catalog = rewrite(catalog)
    catalog['hostedMirror'] = {'format': FORMAT, 'buildID': build_id, 'sourceCatalogSHA256': provenance['sha256'], 'reviewStorage': 'Browser backup on this hosted origin; export/import review JSON for another device.', 'media': 'Browser-sized review copies; original asset IDs and SHA-256 values preserved.', 'availablePaths': sorted(['index.html'] + list(generated) + ['library/' + p for p in referenced])}
    by_id = {a['id']: a for a in catalog['assets']}
    generated_content = {}
    for number, supplement in enumerate(catalog.get('reviewSupplements', []), 1):
        generated_content[f'winners-index-{number}.html'] = winners_index(supplement, by_id)
    catalog_bytes = ('window.REVIEW_CATALOG=' + json.dumps(catalog, ensure_ascii=False, separators=(',', ':')) + ';\n').encode('utf-8')
    generated_content.update({'catalog.js': catalog_bytes, 'library.js': inputs['library.js'], 'library.css': inputs['library.css'], 'bridge.js': inputs['full_dashboard_bridge.js'], 'hosted.js': inputs['hosted_dashboard.js'], 'seed.js': inputs['hosted_dashboard_seed.js'], 'hosted.css': inputs['hosted_dashboard.css']})
    generated_content['index.html'] = ('''<!doctype html><html lang="en" data-hosted-mirror="true"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>CFA Full Visual Library</title><link rel="stylesheet" href="library.css"><link rel="stylesheet" href="hosted.css"></head><body><div id="app"></div><script>window.REVIEW_INITIAL={project:'hon',view:'intake'};if(!location.hash)location.hash='hon/intake';window.REVIEW_BUILD=''' + json.dumps(build_id) + ''';</script><script src="bridge.js"></script><script src="catalog.js"></script><script src="seed.js"></script><script src="library.js"></script><script src="hosted.js"></script></body></html>''').encode()
    files = []
    for relative in sorted(referenced):
        origin, target = design / relative, snapshot / 'library' / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if not target.resolve().is_relative_to(snapshot):
            raise ValueError('Packaged media destination escapes the bundle')
        record = media_records[relative]
        if target.exists():
            if sha(target.read_bytes()) != record['sha256']:
                raise ValueError('Existing content-addressed snapshot was modified')
        elif copy_media:
            shutil.copyfile(origin, target)
        else:
            os.link(origin, target)
        files.append({**record, 'path': 'library/' + relative, 'mode': mode})
    for name, raw in generated_content.items():
        write_generated(snapshot / name, raw)
        files.append({'path': name, 'sha256': sha(raw), 'bytes': len(raw), 'role': 'generated_wrapper' if name.endswith('.html') else 'dashboard_source'})
    # Recheck inputs before publishing current.json; a concurrent build cannot
    # silently mix catalogs or local UI revisions.
    if (design / 'design_catalog.json').read_bytes() != raw_catalog or (design / 'design_manifest.json').read_bytes() != manifest_raw or (source / 'catalog.js').read_bytes() != source_catalog:
        raise RuntimeError('Design inputs changed during packaging')
    if any((source / name).read_bytes() != inputs[name] for name in ('library.js', 'library.css')):
        raise RuntimeError('Local UI changed during packaging')
    receipt = {'format': FORMAT, 'buildID': build_id, 'builtAt': datetime.now(timezone.utc).isoformat(), 'sourceHashes': hashes, 'sourceCatalogSHA256': provenance['sha256'], 'assetCount': len(catalog['assets']), 'albumCount': len(catalog['albums']), 'mediaMode': mode, 'logicalMediaBytes': sum(media_records[p]['bytes'] for p in referenced), 'fileCount': len(files), 'unresolvedPreparedLinks': unresolved, 'files': files, 'reviewStorage': catalog['hostedMirror']['reviewStorage']}
    receipt['publicationFiles'] = sorted(['current.json', f'snapshots/{build_id}/bundle_manifest.json'] + [f'snapshots/{build_id}/{f["path"]}' for f in files])
    write_generated(snapshot / 'bundle_manifest.json', (json.dumps(receipt, indent=2) + '\n').encode())
    current = {'format': FORMAT, 'buildID': build_id, 'snapshot': f'snapshots/{build_id}', 'assetCount': receipt['assetCount'], 'mediaMode': mode, 'sourceCatalogSHA256': provenance['sha256']}
    write_generated(output / 'current.json', (json.dumps(current, indent=2) + '\n').encode())
    return receipt


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--design', type=Path, default=APP / 'library')
    parser.add_argument('--source', type=Path, default=VISUAL)
    parser.add_argument('--output', type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument('--copy-media', action='store_true')
    args = parser.parse_args()
    receipt = build(args.design, args.source, args.output, copy_media=args.copy_media)
    print(json.dumps({k: receipt[k] for k in ('buildID', 'assetCount', 'fileCount', 'logicalMediaBytes', 'unresolvedPreparedLinks')}, indent=2))


if __name__ == '__main__':
    main()
