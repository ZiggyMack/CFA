"""Take planning preserves exact history and keeps plans separate from execution."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import unittest

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP))
import storyboard_takes as takes


class StoryboardTakesTests(unittest.TestCase):
    def setUp(self):
        self.scope = ('hon', 'hon:strictly-business', 'S01-1')
        self.shot = {'shotID': 'S01-1', 'revision': 'take 1', 'stage': 'production', 'source': {'path': 'shot.md', 'sha256': 'a' * 64, 'line': 4},
                     'fields': [{'key': 'camera', 'text': 'Locked', 'status': 'accepted', 'evidence': [{'path': 'writer.md'}]},
                                {'key': 'prompt_clip', 'text': 'Hold the grin.', 'status': 'accepted', 'evidence': [{'path': 'prompt.txt'}]},
                                *[{'key': key, 'text': 'OLD ' + key, 'status': 'accepted', 'evidence': [{'path': 'old.mp4'}], 'reviewer': 'Ziggy'} for key in ('settings', 'results', 'acceptance')]],
                     'materials': [{'assetID': 'old-video', 'role': 'result_on_disk'}, {'assetID': 'face', 'role': 'identity_reference'}],
                     'kitchenWritten': True, 'kitchen': [{'key': '11.10', 'text': 'Old prompt', 'status': 'accepted'}]}
        self.foundation = {'state': 'detailed', 'inputs': [{'assetID': 'face'}], 'notes': [], 'dependencyReviewNeeded': False}

    def options(self, take_id='take-2', note='Let the grin arrive later.'):
        return {'project': self.scope[0], 'storyID': self.scope[1], 'shot': self.shot, 'foundation': self.foundation,
                'id': take_id, 'recordedAt': '2026-10-29T20:00:00Z', 'changeNote': note}

    def test_three_generations_preserve_exact_history_and_frozen_parent(self):
        initial = takes.empty()
        before = deepcopy((initial, self.shot, self.foundation))
        self.assertIsNone(takes.current(initial, *self.scope))
        self.assertEqual(takes.for_shot(initial, *self.scope), [])
        second = takes.plan(initial, self.options())
        self.assertEqual((initial, self.shot, self.foundation), before)
        source = next(row for row in second['takes'] if row['state'] == 'written')
        self.assertEqual(source['snapshot'], {'shot': self.shot, 'foundation': self.foundation})
        self.shot['fields'][0]['text'] = 'Later writer revision'
        third = takes.plan(second, self.options('take-3', 'Hold longer.'))
        fourth = takes.plan(third, self.options('take-4', 'Test the framing.'))
        for row in second['takes']:
            self.assertEqual(next(item for item in fourth['takes'] if item['id'] == row['id']), row)
        active = takes.current(fourth, *self.scope)
        self.assertEqual(active['number'], 4)
        self.assertEqual(next(f for f in active['snapshot']['shot']['fields'] if f['key'] == 'camera')['text'], 'Locked')

    def test_planned_take_resets_execution_and_review(self):
        active = takes.current(takes.plan(takes.empty(), self.options()), *self.scope)
        shot = active['snapshot']['shot']
        self.assertEqual(shot['stage'], 'preliminary')
        self.assertFalse(shot['kitchenWritten'])
        self.assertTrue(shot['handoffNeedsReconciliation'])
        self.assertTrue(active['snapshot']['foundation']['dependencyReviewNeeded'])
        for key in ('settings', 'results', 'acceptance'):
            self.assertEqual(next(f for f in shot['fields'] if f['key'] == key),
                             {'key': key, 'text': '', 'status': 'unknown', 'evidence': [], 'note': takes.RESET_NOTE})
        self.assertEqual(next(f for f in shot['fields'] if f['key'] == 'prompt_clip')['status'], 'draft')
        self.assertEqual(shot['kitchen'][0]['status'], 'draft')
        self.assertEqual(next(f for f in shot['fields'] if f['key'] == 'camera')['status'], 'draft')
        self.assertEqual(shot['materials'], [{'assetID': 'face', 'role': 'identity_reference'}])

    def test_round_trip_deduplicates_identical_records_but_rejects_mutation(self):
        ledger = takes.plan(takes.empty(), self.options())
        self.assertEqual(takes.merge(ledger, json.loads(json.dumps(ledger))), ledger)
        changed = deepcopy(ledger)
        changed['takes'][0]['changeNote'] = 'different'
        with self.assertRaisesRegex(ValueError, 'immutable record conflict'):
            takes.merge(ledger, changed)

    def test_planning_preserves_unwritten_placeholders_and_explicit_not_needed(self):
        self.shot['fields'] = [field for field in self.shot['fields'] if field['key'] not in ('prompt_still', 'prompt_clip')]
        self.shot['fields'].extend([{'key': 'prompt_still', 'text': 'Missing start frame', 'status': 'missing'},
                                    {'key': 'prompt_clip', 'text': 'CFA Nova zone', 'status': 'unknown'}])
        self.shot['kitchen'] = [{'key': '11.1', 'text': 'Missing start frame', 'status': 'missing'},
                                {'key': '11.2', 'text': 'CFA Nova zone', 'status': 'unknown'},
                                {'key': '11.3', 'text': 'Not required for this route', 'status': 'not_needed'},
                                {'key': '11.4', 'text': 'Supplied lock text', 'status': 'present'},
                                {'key': '11.5', 'text': ' ', 'status': 'accepted'}]
        original = deepcopy(self.shot)
        planned = takes.current(takes.plan(takes.empty(), self.options()), *self.scope)['snapshot']['shot']
        self.assertEqual([field['status'] for field in planned['kitchen']], ['missing', 'unknown', 'not_needed', 'draft', 'unknown'])
        self.assertEqual(next(f for f in planned['fields'] if f['key'] == 'prompt_still')['status'], 'missing')
        self.assertEqual(next(f for f in planned['fields'] if f['key'] == 'prompt_clip')['status'], 'unknown')
        self.assertEqual(self.shot, original)

    def test_concurrent_branches_are_retained_with_no_silent_winner(self):
        first = takes.plan(takes.empty(), self.options())
        other = takes.plan(takes.empty(), self.options('alternate-2', 'Another choice.'))
        ledger = takes.merge(first, other)
        self.assertEqual(len(ledger['takes']), 3)
        self.assertIsNone(takes.current(ledger, *self.scope))
        with self.assertRaisesRegex(ValueError, 'conflicting branches'):
            takes.plan(ledger, self.options('take-3'))

    def test_invalid_parent_cycle_and_missing_note_rejected(self):
        ledger = takes.plan(takes.empty(), self.options())
        active = takes.current(ledger, *self.scope)
        with self.assertRaisesRegex(ValueError, 'missing or cross-shot'):
            takes.merge({'format': takes.FORMAT, 'takes': [active]})
        changed = deepcopy(ledger)
        next(r for r in changed['takes'] if r['state'] == 'written')['parentID'] = 'take-2'
        with self.assertRaises(ValueError):
            takes.merge(changed)
        with self.assertRaisesRegex(ValueError, 'describe what changes'):
            takes.plan(takes.empty(), self.options('bad', '  '))
        with self.assertRaisesRegex(ValueError, 'already exists'):
            takes.plan(ledger, self.options())

    def test_unknown_shot_survives_import_and_unlabeled_source_starts_at_one(self):
        self.shot.update(shotID='FUTURE-99', revision='posted scene card')
        ledger = takes.plan(takes.empty(), self.options('future-1'))
        active = takes.current(ledger, 'hon', self.scope[1], 'FUTURE-99')
        self.assertEqual(active['number'], 1)
        self.assertEqual(takes.merge(takes.empty(), ledger), ledger)

    def test_browser_python_parity(self):
        root = APP.parents[1]
        script = root / 'docs/notes/explorable_world/comfy/projects/visual_library/test_storyboard_takes.cjs'
        node = Path('D:/Program Files (x86)/node.exe')
        result = subprocess.run([str(node), str(script), '--fixture'], cwd=root, check=True, text=True, encoding='utf-8', capture_output=True)
        fixture = json.loads(result.stdout)
        self.assertEqual(takes.plan(takes.empty(), fixture['options']), fixture['ledger'])


if __name__ == '__main__':
    unittest.main()
