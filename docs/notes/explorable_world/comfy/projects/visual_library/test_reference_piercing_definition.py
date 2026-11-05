"""The new active checklist must not reinterpret prior validation evidence."""
import hashlib
import json
from pathlib import Path
import unittest

from reference_provenance import verify_evidence_source

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(',', ':')).encode()).hexdigest()


class PiercingDefinitionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = json.loads((HERE / 'reference_validation.json').read_text(encoding='utf-8'))
        cls.definitions = {row['id']: row for row in cls.source['criteriaSets']}

    def test_prior_definition_and_evidence_are_unchanged(self):
        self.assertEqual(digest(self.definitions['hon-face']),
                         '8982c8e2e3b7e1fe0a4d87bf8b7ebd4b1ba105784bf9363dde84dfffbc69a377')
        self.assertEqual(digest(self.source['assessments']),
                         '1fd99eabeb8268322b804372e428100ca9e495c55953ff0029932b980e34fb2b')
        self.assertEqual(digest(self.source['inventory']),
                         '585acc2d2661bae2fa7c584ed5b0347826688f59c0cb7aee52e6bd4c03481ce3')
        old = self.definitions['hon-face']
        self.assertEqual([row['id'] for row in old['criteria']], ['face', 'no-dice'])
        self.assertEqual(old['version'], '2026-10-13.1')

    def test_new_selection_and_presence_are_explicit_without_assessments(self):
        new = self.definitions['hon-face-piercings']
        self.assertEqual(self.source['inactiveCriteriaSetIDs'], ['hon-face'])
        self.assertNotIn(new['id'], self.source['inactiveCriteriaSetIDs'])
        self.assertEqual(new['supersedesCriteriaID'], 'hon-face')
        self.assertEqual(new['version'], '2026-10-27.1')
        self.assertEqual(new['sha256'], digest({k: v for k, v in new.items() if k != 'sha256'}))
        self.assertEqual([row['id'] for row in new['criteria']],
                         ['face', 'ear-piercings', 'nose-piercings', 'lip-piercings'])
        self.assertEqual(new['criteria'][0], self.definitions['hon-face']['criteria'][0])
        for criterion in new['criteria'][1:]:
            self.assertIs(criterion['required'], True)
            self.assertIs(criterion['presenceRequired'], True)
            self.assertNotIn('outcome', criterion)
            self.assertNotIn('presence', criterion)
        self.assertFalse(any((row.get('criteria') or {}).get('id') == new['id']
                             for row in self.source['assessments']))
        self.assertIs(new['wholeActorApproval'], False)

    def test_existing_reference_and_policy_provenance_remain_exact(self):
        new = self.definitions['hon-face-piercings']
        old = self.definitions['hon-face']
        for field in ('nominationID', 'nominationScope', 'reference', 'provenance'):
            self.assertEqual(new[field], old[field], field)
        nomination = next(row for row in self.source['inventory'] if row['id'] == new['nominationID'])
        self.assertEqual(nomination['reference'], new['reference'])
        self.assertEqual(nomination['scope'], new['nominationScope'])
        snapshots = json.loads((HERE / 'reference_provenance_snapshots.json').read_text(encoding='utf-8'))['snapshots']
        for source in new['provenance']:
            self.assertIn(verify_evidence_source(ROOT, source, snapshots), ('current', 'historical_snapshot'))


if __name__ == '__main__':
    unittest.main()
