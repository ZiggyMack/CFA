import copy
import json
import sys
import unittest
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
sys.path.insert(0, str(HERE))

from criminal_mind_review_intake import apply_criminal_mind_review_intake


def read_catalog():
    text = (HERE / 'catalog.js').read_text(encoding='utf-8')
    return json.loads(text.split('=', 1)[1].strip().removesuffix(';'))


class CriminalMindReviewIntakeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.before = read_catalog()
        cls.after = copy.deepcopy(cls.before)
        apply_criminal_mind_review_intake(cls.after, ROOT)

    def test_counts_and_decision_separation(self):
        images = [row for row in self.after['assets']
                  if row.get('project') == 'criminal_mind' and row.get('kind') == 'image']
        self.assertEqual(len(images), 1194)
        self.assertEqual(sum(row.get('category') == 'cast' for row in images), 238)
        self.assertEqual(sum(bool(row.get('locationFamilyID')) for row in images), 956)
        self.assertTrue(all(row.get('selected') is False for row in images))
        self.assertEqual(sum(row.get('role') == 'background_casting_option' for row in images), 48)
        self.assertEqual(sum(row.get('role') in {'set_design_option', 'set_camera_option'} for row in images), 956)
        self.assertEqual(len({row['sha256'] for row in images if row.get('locationFamilyID')}), 954)
        tasks = {row['id']: row for row in self.after['missionControl']['tasks']}
        self.assertEqual(tasks['tcm-grok-casting-20261030']['acceptedOutputs'], 0)
        self.assertEqual(tasks['tcm-grok-sets-20261030']['acceptedOutputs'], 0)
        self.assertEqual(len(tasks['tcm-grok-sets-20261030']['receivedLocationFamilies']), 24)

    def test_provider_mapping_and_set_round_never_auto_binds(self):
        new_sets = [row for row in self.after['assets']
                    if row.get('project') == 'criminal_mind' and row.get('aggregateIntake', {}).get('path', '').endswith('CFA_SET_INTAKE_035-118_SITE_INDEX_v003.json')]
        self.assertEqual(len(new_sets), 946)
        provider_ids = [row['providerCandidateID'] for row in new_sets]
        self.assertEqual(len(provider_ids), len(set(provider_ids)))
        self.assertEqual(sum(row['id'] != row['providerCandidateID'] for row in new_sets), 423)
        later = [row for row in new_sets if row['role'] == 'set_camera_option']
        self.assertEqual(len(later), 756)
        self.assertTrue(all(row['eligibleShotIDs'] == [] for row in later))
        self.assertTrue(all('variant' not in row and 'providerVariant' in row for row in new_sets))
        self.assertTrue(all('variantOf' not in row and 'providerVariantOf' in row for row in new_sets))
        self.assertEqual(sum(bool(row.get('cameraPositionID')) for row in later), 749)
        self.assertEqual(sum(bool(row.get('lightState')) for row in later), 749)
        identity = [row for row in later if row.get('setRoundKind') == 'identity_sheet']
        self.assertEqual(len(identity), 20)
        self.assertTrue(all(row['bindingPolicy'] == 'identity_sheet_never_bound' for row in identity))

    def test_preserves_reviews_story_structure_and_starting_state(self):
        self.assertEqual(self.after.get('reviewDecisions'), self.before.get('reviewDecisions'))
        self.assertEqual(self.after.get('storyboardStructure'), self.before.get('storyboardStructure'))
        self.assertEqual(self.after.get('storyboardSourceFoundation'), self.before.get('storyboardSourceFoundation'))
        before_selected = {row['id']: row.get('selected') for row in self.before['assets']
                           if row.get('project') == 'criminal_mind'}
        after_selected = {row['id']: row.get('selected') for row in self.after['assets']
                          if row['id'] in before_selected}
        self.assertEqual(after_selected, before_selected)
        henderson = next(row for row in self.after['assets'] if row['id'] == 'TCM-SET-HENDERSON-EXTERIOR-L03')
        self.assertFalse(henderson['selected'])
        self.assertEqual(henderson['relayedAuthorChoiceSignal']['reviewEvidenceStatus'],
                         'recovered_favorite_or_basket_only_no_attributed_saved_review')

    def test_replay_is_idempotent(self):
        replay = copy.deepcopy(self.after)
        apply_criminal_mind_review_intake(replay, ROOT)
        self.assertEqual(replay, self.after)


if __name__ == '__main__':
    unittest.main()
