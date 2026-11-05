"""Read-only checks of Claude's proposed shot bundle; writes its own receipt only."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

root = Path(r'D:\Documents\CFA')
projects = root / 'docs/notes/explorable_world/comfy/projects'
writer = projects / 'hon_dolo_strictly_business/story/writer_pass_20261010'
example = writer / 'kitchen_block_20261029/EXAMPLE_S01-1_KITCHEN_BLOCK_20261029.md'
catalog_text = (projects / 'visual_library/catalog.js').read_text(encoding='utf-8-sig')
catalog = json.loads(catalog_text.split('=', 1)[1].strip().removesuffix(';'))
assets = catalog.get('assets', [])
if isinstance(assets, dict):
    assets = list(assets.values())
ids = {'HD-B-91ef00348229', 'HD-RETURN-6c8900223ee9', 'HD-DROP-725c38458fd8'}
selected = [{k: a[k] for k in ('id', 'title', 'path', 'src', 'sha256', 'sourceStatus', 'referenceStatus') if k in a}
            for a in assets if a.get('id') in ids]
files = []
for line in example.read_text(encoding='utf-8-sig').splitlines():
    if not line.startswith('| HD-'):
        continue
    cells = [v.strip() for v in line.split('|')[1:-1]]
    rel = cells[1].split(' (')[0]
    path = projects / 'hon_dolo_strictly_business' / rel
    item = {'id': cells[0], 'path': str(path), 'exists': path.is_file(), 'expectedHash': cells[2]}
    if path.is_file():
        item.update(sha256=hashlib.sha256(path.read_bytes()).hexdigest(), bytes=path.stat().st_size)
        item['hashMatches'] = item['sha256'] == item['expectedHash']
    files.append(item)
reviews = json.loads((projects / 'hon_dolo_strictly_business/feedback/review_decisions.json').read_text(encoding='utf-8-sig'))
review_rows = [x for x in reviews.get('items', []) if x.get('id') in ids or x.get('assetID') in ids]
bom = json.loads((projects / 'visual_library/working_reference_bom.json').read_text(encoding='utf-8-sig'))
scoped_rows = [entry for char in bom.get('characters', []) for entry in char.get('entries', [])
               if entry.get('assetID') in ids]
graph = json.loads((projects.parent / 'workflows/hon_dolo_motion_v001.executed.api.json').read_text())
image_nodes = [{'id': nid, 'class': node.get('class_type'), 'title': node.get('_meta', {}).get('title'), 'inputs': node.get('inputs')}
               for nid, node in graph.items() if node.get('class_type') == 'LoadImage']
report = {'checkedAt': datetime.now(timezone.utc).isoformat(), 'bundleFiles': files,
          'catalogTopLevelKeys': list(catalog), 'selectedCatalogRows': selected,
          'reviewItemCount': len(reviews.get('items', [])), 'selectedReviews': review_rows,
          'currentScopedReferenceSelections': scoped_rows,
          'executedMotionGraphLoadImages': image_nodes,
          'currentCloudPreflight': False, 'newGeneration': False,
          'writerFilesChanged': False, 'siteFilesChanged': False}
out = Path(__file__).with_name('KITCHEN_SOURCE_VERIFICATION_20261029.json')
out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(report, ensure_ascii=False, indent=2))
