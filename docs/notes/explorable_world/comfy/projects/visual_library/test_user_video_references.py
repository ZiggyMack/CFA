from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from storyboard_structure import apply_storyboard_structure, build_hon
from user_video_intake import apply_user_video_intakes
from user_video_references import apply_user_video_references

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
REGISTRY = HERE.relative_to(ROOT) / 'user_video_intakes.json'
IDS = {'GEM-HON-203A795FBF12', 'GEM-HON-44141C686AA5'}


class UserVideoReferencesTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = json.loads((HERE / 'catalog.js').read_text(encoding='utf-8').split('=', 1)[1].strip().removesuffix(';'))
        cls.data = deepcopy(cls.original)
        apply_user_video_intakes(cls.data, ROOT)
        cls.authored = build_hon(ROOT, cls.data)
        apply_storyboard_structure(cls.data, ROOT)

    def test_exact_two_clips_and_original_paths(self):
        for aid in IDS:
            asset = next(a for a in self.data['assets'] if a['id'] == aid)
            self.assertIn('/00_Unassigned_Gemini/', asset['repoPath'])
            self.assertEqual(hashlib.sha256((ROOT / asset['repoPath']).read_bytes()).hexdigest(), asset['sha256'])
            self.assertEqual(asset['sourceIntake'], '0b4ac66a-1962-4b01-a705-ff8a166ea528')
            self.assertEqual(asset['sourceStatus'], 'Gemini test · inspiration only · reshoot anticipated')
            self.assertIn('The yellow dinner outfit was selected separately', asset['note'])
            self.assertFalse({'status', 'likenessRating', 'sceneQualityRating', 'storyboardStage', 'workingReference'} & asset.keys())

    def test_scoped_links_preserve_authored_fields_and_acceptance(self):
        story = self.data['storyboardStructure']['stories'][0]
        for before, after in zip(self.authored['shots'], story['shots']):
            if after['shotID'] in {'S10-1', 'S10-2'}:
                added = [m for m in after['materials'] if m['assetID'] in IDS]
                self.assertEqual({m['assetID'] for m in added}, IDS)
                self.assertTrue(all(m['role'] == 'dinner_reference' and m['availability'] == 'catalogued' for m in added))
                self.assertTrue(all('Inspiration only.' in m['note'] and 'seating and blocking remain open' in m['note'] for m in added))
            else:
                self.assertFalse(IDS & {m['assetID'] for m in after['materials']})
            for key in ['fields', 'kitchen', 'stage', 'source', 'dependencies']:
                self.assertEqual(before[key], after[key], (after['shotID'], key))
        dinner = next(s for s in self.data['shotMaterials']['shots'] if s['id'] == 'S10A')
        self.assertEqual(dinner['stage'], 'preliminary')
        self.assertEqual(dinner['acceptance'], 'not_accepted')
        self.assertEqual({m['assetID'] for m in dinner['materials'] if m['assetID'] in IDS}, IDS)
        for key in ['reviewDecisions', 'sceneReviews', 'reviewIntake']:
            self.assertEqual(self.original[key], self.data[key], key)

    def test_repeated_adapter_and_reference_application_are_idempotent(self):
        repeated = deepcopy(self.data)
        apply_user_video_references(repeated, ROOT)
        self.assertEqual(self.data, repeated)
        apply_storyboard_structure(repeated, ROOT)
        self.assertEqual(self.data, repeated)

    def fixture(self, folder):
        registry = json.loads((ROOT / REGISTRY).read_text())
        registry['intakes'] = [i for i in registry['intakes'] if i['id'] == '0b4ac66a-1962-4b01-a705-ff8a166ea528']
        intake = registry['intakes'][0]
        for relative in [intake['requestPath'], *(m['path'] for m in intake['media'])]:
            dest = folder / relative
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, dest)
        (folder / REGISTRY).parent.mkdir(parents=True, exist_ok=True)
        (folder / REGISTRY).write_text(json.dumps(registry))
        return registry, intake

    def test_changed_receipt_is_rejected_without_catalog_mutation(self):
        with tempfile.TemporaryDirectory(dir=ROOT / '.cache', prefix='video-reference-test-') as tmp:
            folder = Path(tmp)
            _, intake = self.fixture(folder)
            path = folder / intake['requestPath']
            path.write_bytes(path.read_bytes() + b' ')
            data = deepcopy(self.data)
            with self.assertRaises(AssertionError):
                apply_user_video_references(data, folder)
            self.assertEqual(data, self.data)

    def test_invalid_target_is_rejected_without_partial_links(self):
        with tempfile.TemporaryDirectory(dir=ROOT / '.cache', prefix='video-reference-test-') as tmp:
            folder = Path(tmp)
            registry, intake = self.fixture(folder)
            path = folder / intake['requestPath']
            request = json.loads(path.read_text())
            request['storyboardReferences'][1]['shotIDs'].append('S10-missing')
            path.write_text(json.dumps(request))
            intake['requestSHA256'] = hashlib.sha256(path.read_bytes()).hexdigest()
            (folder / REGISTRY).write_text(json.dumps(registry))
            data = deepcopy(self.data)
            # Simulate a fresh structure before this intake's reference overlay.
            for shot in data['shotMaterials']['shots']:
                shot['materials'] = [m for m in shot['materials'] if m['assetID'] not in IDS]
            for story in data['storyboardStructure']['stories']:
                for shot in story['shots']:
                    shot['materials'] = [m for m in shot['materials'] if m['assetID'] not in IDS]
            before = deepcopy(data)
            with self.assertRaises(AssertionError):
                apply_user_video_references(data, folder)
            self.assertEqual(data, before)


if __name__ == '__main__':
    unittest.main()
