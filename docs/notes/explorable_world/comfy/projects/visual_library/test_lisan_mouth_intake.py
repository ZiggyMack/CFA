"""Bounded real-source checks; no catalog build, source edit or provider action."""
import copy
import hashlib
import json
from pathlib import Path
import unittest

from grok500_catalog import CatalogIntakeError, io_path
from lisan_mouth_intake import apply_existing_lisan_metadata, load_lisan_mouth_complete, safe_relative, validate_registry

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
INTAKE = ROOT / 'docs/notes/explorable_world/comfy/projects/lisan_al_gaib/grok_mouth_complete_20261012'


class LisanMouthIntakeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.registry = json.loads(io_path(INTAKE/'registry.json').read_text(encoding='utf-8'))
        raw = io_path(HERE/'catalog.js').read_text(encoding='utf-8')
        cls.catalog = json.loads(raw[raw.index('=')+1:].strip().rstrip(';'))
        new_ids = {a['id'] for a in cls.registry['assets'] if a['binding']=='new'}
        cls.existing = [a for a in cls.catalog['assets'] if a['id'] not in new_ids]
        cls.loaded = load_lisan_mouth_complete(ROOT, INTAKE, cls.existing)

    def test_exact_sources_and_dedup(self):
        self.assertEqual(len(self.loaded['assets']), 44)
        self.assertEqual(len(self.loaded['reusedAssets']), 21)
        all_records = self.loaded['assets'] + self.loaded['reusedAssets']
        self.assertEqual(len({a['id'] for a in all_records}), 65)
        self.assertEqual(len({a['sha256'] for a in all_records}), 65)
        overview = next(a for a in self.loaded['albums'] if a['id']=='lisan:mouth-complete-20261012')
        self.assertEqual(set(overview['related']), {a['id'] for a in all_records})
        for doc in self.loaded['documents']:
            self.assertEqual(hashlib.sha256(io_path(ROOT/doc['path']).read_bytes()).hexdigest(), doc['sha256'])
        self.assertEqual(self.loaded['summary']['newUserRatings'], 0)
        self.assertEqual(self.loaded['summary']['newApprovals'], 0)

    def test_provider_scores_are_metadata_only(self):
        for a in self.loaded['assets']:
            for field in ['likenessRating','sceneQualityRating','status','workingReference','variant','componentApprovals','shotPlan']:
                self.assertNotIn(field, a)
            self.assertEqual(a['storyboardStage'], 'preliminary')
            self.assertEqual(a['acceptance'], 'not_accepted')
            self.assertIsNone(a['timing'])
            self.assertIn('not human ratings', a['note'])
            self.assertEqual(a['providerPreliminaryReview']['status'], 'provider_self_score_preliminary')
        broken = copy.deepcopy(self.registry)
        broken['assets'][-1]['likenessRating'] = 5
        with self.assertRaisesRegex(CatalogIntakeError, 'human review'):
            validate_registry(broken)

    def test_existing_reviews_paths_and_breather_scope_survive(self):
        assets = copy.deepcopy(self.existing)
        before = {a['id']: copy.deepcopy(a) for a in assets}
        apply_existing_lisan_metadata(assets, self.loaded['reusedAssets'])
        after = {a['id']: a for a in assets}
        for record in self.loaded['reusedAssets']:
            old, current = before[record['id']], after[record['id']]
            for field in set(old) - {'note','providerPreliminaryReview','intakeSourceAliases'}:
                self.assertEqual(current[field], old[field], field)
            self.assertTrue(current['note'].startswith(old.get('note','')))
            self.assertIn(record['path'], current['intakeSourceAliases'])
            self.assertEqual(current['providerPreliminaryReview'], record['providerPreliminaryReview'])
        standard = after['LAG-PART-1b60815fa2bb']
        self.assertEqual(standard['sourceStatus'], 'user_selected_scoped_combination')
        self.assertEqual(standard['userSelection']['scope'], 'breather + natural teeth + no grill only')
        self.assertFalse(standard['userSelection']['default'])
        self.assertFalse(standard['userSelection']['fullIdentityApproval'])
        once = copy.deepcopy(assets)
        apply_existing_lisan_metadata(assets, self.loaded['reusedAssets'])
        self.assertEqual(assets, once, 'Repeated metadata application does not duplicate notes or aliases')

    def test_failures_and_missing_shapes_remain_explicit(self):
        failed = next(a for a in self.loaded['albums'] if a['id']=='lisan:mouth-failures-20261012')
        self.assertEqual(failed['category'], 'review')
        self.assertEqual(len(failed['related']), 8)
        self.assertEqual(self.loaded['coverage']['missingUsableShapeNumbers'], [7,15,16,18,35])
        self.assertEqual(self.loaded['coverage']['skippedShapeNumbers'], [47])
        self.assertEqual(self.loaded['coverage']['distinctVisemeShapeNumbers'], 44)
        self.assertEqual(self.loaded['coverage']['breatherMissingOrFailed'], ['BR-06'])
        grill = next(a for a in self.loaded['reusedAssets'] if a['providerCollection']=='03_OPTIONAL_GRILL')
        self.assertIn('candidate', grill['providerNoteSuffix'].lower())
        self.assertNotIn('workingReference', grill)

    def test_wrong_manifest_counts_and_paths_rejected(self):
        bad = copy.deepcopy(self.registry)
        bad['sourceManifestSHA256'] = '0'*64
        with self.assertRaises(CatalogIntakeError):
            validate_registry(bad)
        bad = copy.deepcopy(self.registry)
        bad['assets'].pop()
        with self.assertRaises(CatalogIntakeError):
            validate_registry(bad)
        bad = copy.deepcopy(self.registry)
        bad['assets'][0]['path'] = '../outside.jpg'
        with self.assertRaises(CatalogIntakeError):
            validate_registry(bad)
        for path in ['../escape', '/absolute', 'D:/private.jpg', 'safe%2fescape', 'safe\\escape']:
            with self.assertRaises(CatalogIntakeError):
                safe_relative(path)


if __name__ == '__main__':
    unittest.main()