"""Take history survives exported review publication and local rebuilding."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

APP = Path(__file__).resolve().parents[1]
ROOT = APP.parents[1]
sys.path.insert(0, str(APP))
sys.path.insert(0, str(ROOT / 'docs/notes/explorable_world/comfy/projects/visual_library'))
import storyboard_takes as takes
from review_snapshot import overlay_review_snapshot
from storyboard_take_intake import apply_take_history


class TakePublicationTest(unittest.TestCase):
    def fixture(self):
        shot = {'shotID': 'S01-1', 'title': 'Test shot', 'revision': 'take 1', 'stage': 'preliminary',
                'fields': [{'key': 'camera', 'text': 'Static camera', 'status': 'draft', 'evidence': []},
                           {'key': 'results', 'text': 'Prior take evidence', 'status': 'present', 'evidence': []}],
                'kitchen': [], 'materials': []}
        options = dict(project='hon', storyID='hon:story', shot=shot, foundation=None,
                       changeNote='Change the framing', id='take2', recordedAt='2026-10-29T20:00:00Z')
        ledger = takes.plan(takes.empty(), options)
        return shot, options, ledger

    def test_review_overlay_and_local_rebuild_preserve_complete_history(self):
        shot, options, ledger = self.fixture()
        newer = takes.plan(ledger, {**options, 'id': 'take3', 'changeNote': 'Quieter performance'})
        catalog = {'assets': [], 'reviewDecisions': [], 'storyboardTakes': ledger}
        before = deepcopy(catalog)
        export = {'format': 'cfa-visual-review-v1', 'items': [], 'storyboardTakes': newer,
                  'storyboardTakeBackups': [{'origin': 'older client', 'reason': 'Unsupported version', 'data': {'format': 'future'}}]}
        result, report = overlay_review_snapshot(catalog, export)
        self.assertEqual(result['storyboardTakes'], newer)
        self.assertEqual(catalog, before)
        self.assertEqual(report['changedFields'], 0)
        rebuilt = {'assets': [], 'reviewDecisions': []}
        apply_take_history(rebuilt, ROOT, {'storyboardTakes': ledger}, result)
        self.assertEqual(rebuilt['storyboardTakes'], newer)
        self.assertEqual(rebuilt['storyboardTakeBackups'], export['storyboardTakeBackups'])
        source = next(row for row in newer['takes'] if row['state'] == 'written')
        self.assertEqual(source['snapshot']['shot'], shot)

    def test_conflict_does_not_change_input_catalog(self):
        _, _, ledger = self.fixture()
        catalog = {'assets': [], 'reviewDecisions': [], 'storyboardTakes': ledger}
        before = deepcopy(catalog)
        bad = deepcopy(ledger)
        bad['takes'][-1]['changeNote'] = 'Conflicting rewrite'
        with self.assertRaisesRegex(ValueError, 'immutable record conflict'):
            overlay_review_snapshot(catalog, {'format': 'cfa-visual-review-v1', 'items': [], 'storyboardTakes': bad})
        self.assertEqual(catalog, before)

    def test_no_take_records_are_invented_for_existing_catalogs(self):
        rebuilt = {'assets': [], 'reviewDecisions': []}
        before = deepcopy(rebuilt)
        apply_take_history(rebuilt, ROOT, {}, {})
        self.assertEqual(rebuilt, before)


if __name__ == '__main__':
    unittest.main()
