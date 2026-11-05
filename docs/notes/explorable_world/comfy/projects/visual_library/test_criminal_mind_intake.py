"""Verify source-only project intake, owner isolation, and original DOC preservation."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

from criminal_mind_intake import apply_criminal_mind_intake, INTAKE, ORIGINAL_SHA

ROOT = Path(__file__).resolve().parents[6]
sys.path.insert(0, str(ROOT / 'apps/creative_studio'))
from build_design_library import DesignBundle


class CriminalMindIntakeTests(unittest.TestCase):
    def fixture(self):
        return {'projects': [{'id': 'hon'}, {'id': 'lisan'}, {'id': 'unassigned'}],
                'assets': [{'id': 'existing', 'project': 'hon', 'kind': 'image'}], 'albums': [],
                'reviewDecisions': [{'id': 'existing', 'rating': 1, 'reviewer': 'Ziggy'}],
                'missionControl': {'tasks': [{'id': 'existing-task', 'project': 'hon'}]},
                'shotMaterials': {'shots': []}, 'storyboardStories': []}

    def test_source_blocks_and_no_inherited_media_or_decisions(self):
        catalog = self.fixture()
        before = deepcopy(catalog)
        apply_criminal_mind_intake(catalog, ROOT)
        project = next(p for p in catalog['projects'] if p['id'] == 'criminal_mind')
        self.assertEqual(project['controllerID'], 'baldadoon')
        self.assertEqual(len(project['landing']['sourceBlocks']), 41)
        self.assertTrue(any(b['containsUnheadedFlashback'] for b in project['landing']['sourceBlocks']))
        self.assertEqual(catalog['storyboardMetadata']['criminal_mind']['panelCount'], 0)
        self.assertEqual(catalog['reviewDecisions'], before['reviewDecisions'])
        self.assertEqual(catalog['assets'][0], before['assets'][0])
        self.assertEqual(catalog['missionControl']['tasks'][0], before['missionControl']['tasks'][0])
        self.assertEqual(catalog['shotMaterials'], before['shotMaterials'])
        self.assertEqual(catalog['storyboardStories'], before['storyboardStories'])
        self.assertEqual({a['kind'] for a in catalog['assets'][1:]}, {'document'})
        self.assertEqual(catalog['missionControl']['tasks'][-1]['assigneeControllerID'], 'baldadoon')
        self.assertEqual(catalog['missionControl']['tasks'][-1]['decisionAuthorityControllerID'], 'baldadoon')
        self.assertEqual(catalog['projects'][0]['controllerID'], 'ziggy')

    def test_full_script_and_original_are_separate_and_original_survives_packaging(self):
        catalog = self.fixture()
        apply_criminal_mind_intake(catalog, ROOT)
        assets = {a['id']: a for a in catalog['assets']}
        self.assertGreater(len(assets['TCM-SCRIPT-TEXT']['text']), 40000)
        self.assertEqual(assets['TCM-ORIGINAL-DOC']['text'], '')
        with tempfile.TemporaryDirectory(dir=ROOT / '.cache') as directory:
            bundle = object.__new__(DesignBundle)
            bundle.assets = assets
            bundle.root = ROOT
            bundle.source = ROOT / 'docs/notes/explorable_world/comfy/projects/visual_library/catalog.js'
            bundle.out = Path(directory)
            bundle.media = bundle.out / 'design_media'
            bundle.media.mkdir()
            bundle.sources = {}
            bundle.outputs = {}
            bundle.packaged_assets = {}
            bundle.max_file_bytes = 10_000_000
            item = bundle.package_asset('TCM-ORIGINAL-DOC')
            published = (bundle.out / item['src']).read_bytes()
            self.assertEqual(hashlib.sha256(published).hexdigest(), ORIGINAL_SHA)
            self.assertEqual(published, (ROOT / INTAKE / 'The Criminal Mind (final).doc').read_bytes())
            self.assertTrue(item['downloadOnly'])
            self.assertTrue(item['src'].endswith('.doc'))


if __name__ == '__main__':
    unittest.main()
