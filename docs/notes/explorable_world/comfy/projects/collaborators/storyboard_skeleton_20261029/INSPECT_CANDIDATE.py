"""Independently inspect generated site data without running the site builder."""
from pathlib import Path
import json
import sys
from datetime import datetime, timezone
import hashlib

root = Path(r'D:\Documents\CFA')
candidate = Path(sys.argv[1]) if len(sys.argv) > 1 else root / '.cache/story_structure_20261029/catalog.candidate.json'
raw = candidate.read_text(encoding='utf-8-sig')
catalog = json.loads(raw.split('=', 1)[1].strip().removesuffix(';') if raw.startswith('window.') else raw)
structure = catalog['storyboardStructure']
hon = next(s for s in structure['stories'] if s['storyID'] == 'hon:strictly-business')
print(json.dumps({'plannedShots': len(hon['shots']), 'sections': len(hon['sections']),
                  'kitchenBlocksDocumented': sum(s['kitchenWritten'] for s in hon['shots']),
                  'emptyTemplateIsDemonstration': structure['template'].get('demonstration'),
                  'emptyTemplateHasShotID': 'shotID' in structure['template'],
                  'fieldCount': len(structure['fields']),
                  'kitchenFieldCount': len(structure['kitchenFields'])}))
for shot_id in ('S01-1', 'S02-6', 'S02-8', 'S02-9', 'S04-1'):
    shot = next(s for s in hon['shots'] if s['shotID'] == shot_id)
    chosen = {field['key']: {'status': field['status'], 'excerpt': field['text'][:100]}
              for field in shot['fields'] if field['key'] in (
                  'camera', 'character', 'background', 'start_frame', 'prompt_still', 'prompt_clip', 'cue')}
    print(json.dumps({'shot': shot_id, 'fields': chosen}, ensure_ascii=True))

if candidate.suffix == '.js':
    before_raw = (root / '.cache/story_structure_20261029/catalog.js.before').read_text(encoding='utf-8-sig')
    before = json.loads(before_raw.split('=', 1)[1].strip().removesuffix(';'))
    coverage = json.loads((root / 'docs/notes/explorable_world/comfy/projects/hon_dolo_strictly_business/story/writer_pass_20261010/HON_COVERAGE_MAP_20261028.json').read_text(encoding='utf-8-sig'))
    by_shot = {shot['shotID']: shot for shot in hon['shots']}
    field_map = lambda shot_id: {field['key']: field for field in by_shot[shot_id]['fields']}
    checks = {
        'allAuthoredShotsRetained': set(by_shot) == {shot['shotID'] for shot in coverage['shots']},
        'allSectionsRetained': len(hon['sections']) == 14,
        'blankExcludedFromAuthoredShots': structure['template'].get('demonstration') is True and 'shotID' not in structure['template'],
        'allBlankFieldsDefined': len(structure['fields']) == 16 and len(structure['kitchenFields']) == 12,
        'existingReviewsUnchanged': catalog['reviewDecisions'] == before['reviewDecisions'],
        'existingIntakeUnchanged': catalog['reviewIntake'] == before['reviewIntake'],
        'existingAssetsUnchanged': catalog['assets'][:len(before['assets'])] == before['assets'],
        'missingClipDistinctFromWrittenStill': field_map('S02-6')['prompt_clip']['status'] == 'missing' and field_map('S02-6')['prompt_still']['status'] == 'draft',
        'missingArtDistinctFromCameraAndActor': field_map('S02-9')['camera']['status'] == 'draft' and field_map('S02-9')['character']['status'] == 'not_needed' and field_map('S02-9')['start_frame']['status'] == 'missing',
        'referencesDoNotInventStartingFrame': field_map('S01-1')['start_frame']['status'] == 'missing',
    }
    assert all(checks.values()), checks
    receipt = {'checkedAtUTC': datetime.now(timezone.utc).isoformat(), 'checks': checks,
               'catalogSHA256': hashlib.sha256(candidate.read_bytes()).hexdigest(),
               'reviewCount': len(catalog['reviewDecisions']), 'shotCount': len(hon['shots']),
               'rootSiteWrites': False, 'rootWriterChanges': False, 'liveBrowserVerified': False}
    Path(__file__).with_name('LOCAL_STRUCTURE_VERIFICATION.json').write_text(json.dumps(receipt, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'allChecksPassed': True, 'checks': len(checks), 'reviewCount': receipt['reviewCount']}))
