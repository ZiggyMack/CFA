"""Read-only check of published foundation data and real scoped references."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
from copy import deepcopy
import hashlib
import importlib.util
import json

ROOT = Path(r'D:\Documents\CFA')
CATALOG = ROOT / 'docs/notes/explorable_world/comfy/projects/visual_library/catalog.js'
def load(path):
    raw = path.read_text(encoding='utf-8-sig')
    return json.loads(raw.split('=', 1)[1].strip().removesuffix(';') if raw.startswith('window.') else raw)

catalog = load(CATALOG)
prior = load(ROOT / '.cache/story_structure_20261029/catalog.candidate.json')
model = catalog['storyboardSourceFoundation']
spec = importlib.util.spec_from_file_location('root_foundation_audit', ROOT / 'apps/creative_studio/source_foundation.py')
helper = importlib.util.module_from_spec(spec)
spec.loader.exec_module(helper)
story = next(s for s in catalog['storyboardStructure']['stories'] if s['storyID'] == 'hon:strictly-business')
reviews = {r['id']: r for r in catalog['reviewDecisions']}
states = Counter(helper.derive(model, s, story['project'], story['storyID'], catalog['assets'], reviews,
                               catalog.get('sceneReviews', []))['state'] for s in story['shots'])
checks = {
    'all70CurrentShotsHaveNoSelectedFrame': states == {'no_frame': 70},
    'noSelectionsManufactured': model['bindings'] == [],
    'allReviewsUnchanged': catalog['reviewDecisions'] == prior['reviewDecisions'],
    'allIntakeUnchanged': catalog['reviewIntake'] == prior['reviewIntake'],
    'allAssetsUnchanged': catalog['assets'] == prior['assets'],
    'storyboardStagesUnchanged': [s['stage'] for s in story['shots']] == [s['stage'] for s in prior['storyboardStructure']['stories'][0]['shots']],
    'blankStillIsolated': catalog['storyboardStructure']['template']['demonstration'] is True,
}
mouth = next(a for a in catalog['assets'] if a['id'] == 'HD-B-91ef00348229')
binding = {'project': 'hon', 'storyID': story['storyID'], 'shotID': 'S01-1', 'mode': 'first_frame',
           'evidence': {'source': 'Root audit simulation only; never a saved selection'},
           'inputs': [{'assetID': mouth['id'], 'sha256': mouth['sha256'], 'bytes': mouth['bytes'],
                       'role': 'start_frame', 'required': True}]}
simulation = deepcopy(model)
simulation.update(bindings=[binding], checkpoints=[])
component = helper.derive(simulation, {'shotID': 'S01-1'}, 'hon', story['storyID'], catalog['assets'], reviews)
checks['realProductionMouthCannotPromoteScene'] = component['state'] == 'unresolved' and component['inputs'][0]['scope'] == 'detail'
assert all(checks.values()), checks
receipt = {'checkedAtUTC': datetime.now(timezone.utc).isoformat(), 'checks': checks,
           'catalogSHA256': hashlib.sha256(CATALOG.read_bytes()).hexdigest(), 'foundationCounts': dict(states),
           'pythonHelperSHA256': hashlib.sha256((ROOT / 'apps/creative_studio/source_foundation.py').read_bytes()).hexdigest(),
           'browserHelperSHA256': hashlib.sha256((CATALOG.parent / 'source_foundation.js').read_bytes()).hexdigest(),
           'reviewCount': len(reviews), 'componentSimulationOnly': True,
           'rootSiteWrites': False, 'newSelectionsSaved': False, 'liveBrowserVerified': False}
Path(__file__).with_name('ROOT_FOUNDATION_VERIFICATION.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
print(json.dumps(receipt, ensure_ascii=True))
