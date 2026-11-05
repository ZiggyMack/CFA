"""Exact-input maturity, read-only behavior and persisted checkpoint regression."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[5]
sys.path.insert(0,str(ROOT/'apps/creative_studio'))
import source_foundation as f
from storyboard_foundation import apply_source_foundation

class SourceFoundationTest(unittest.TestCase):
    def test_shared_cases(self):
        for case in json.loads((HERE/'test_source_foundation_cases.json').read_text()):
            with self.subTest(case=case['name']):
                a=case['arguments'];before=deepcopy(a)
                out=f.derive(a['model'],a['shot'],a['project'],a['storyID'],a['assets'],a['reviews'],a['sceneReviews'])
                self.assertEqual(out['state'],case['expectedState']);self.assertEqual(a,before)
                if case['name']=='exact current review stage and defects':self.assertIn('Recorded disposition: needs fixes',out['inputs'][0]['notes'])

    def test_two_loaded_catalog_checkpoints(self):
        a=json.loads((HERE/'test_source_foundation_cases.json').read_text())[0]['arguments']
        cache=ROOT/'.cache/source_foundation_20261029';cache.mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=cache) as directory:
            d=Path(directory);registry=d/'bindings.json'
            registry.write_text(json.dumps({'format':'cfa-storyboard-input-bindings-v1','bindings':a['model']['bindings']}))
            c={'assets':a['assets'],'reviewDecisions':[{'id':'fixture:scene','sha256':'a'*64,'status':'keep','note':'Retain prior acceptance.'}],'storyboardStructure':{'stories':[{'project':'hon','storyID':a['storyID'],'shots':[a['shot']]}]}}
            apply_source_foundation(c,ROOT,registry=registry)
            first=d/'catalog-v1.json';first.write_text(json.dumps(c))
            # Reload the earlier checkpoint from disk, then create a separate publication.
            loaded=json.loads(first.read_text());previous=deepcopy(loaded['storyboardSourceFoundation'])
            loaded['assets'][0].update(sha256='b'*64,bytes=105)
            changed_binding=deepcopy(a['model']['bindings']);changed_binding[0]['inputs'][0].update(sha256='b'*64,bytes=105)
            registry.write_text(json.dumps({'format':'cfa-storyboard-input-bindings-v1','bindings':changed_binding}))
            apply_source_foundation(loaded,ROOT,previous=previous,registry=registry)
            second=d/'catalog-v2.json';second.write_text(json.dumps(loaded))
            current=json.loads(second.read_text());original=json.loads(first.read_text())
            out=f.derive(current['storyboardSourceFoundation'],a['shot'],'hon',a['storyID'],current['assets'])
            self.assertEqual(out['state'],'detailed');self.assertTrue(out['dependencyReviewNeeded'])
            self.assertEqual(current['reviewDecisions'],original['reviewDecisions'])
            self.assertEqual(current['storyboardStructure'],original['storyboardStructure'])
            self.assertNotEqual(current['storyboardSourceFoundation']['checkpoints'][0]['signature'],original['storyboardSourceFoundation']['checkpoints'][0]['signature'])

    def test_saved_exact_story_selection_checkpoint(self):
        a=next(c['arguments'] for c in json.loads((HERE/'test_source_foundation_cases.json').read_text()) if c['name']=='saved exact story selection')
        matches=f.selected_binding(a['model'],a['shot'],'hon',a['storyID'],a['sceneReviews'])
        model={'bindings':[],'checkpoints':f.checkpoint(matches,a['assets'])}
        self.assertFalse(f.derive(model,a['shot'],'hon',a['storyID'],a['assets'],scene_reviews=a['sceneReviews'])['dependencyReviewNeeded'])
        a['sceneReviews'][0]['ingredients'][0]['assetID']='different:asset'
        self.assertTrue(f.derive(model,a['shot'],'hon',a['storyID'],a['assets'],scene_reviews=a['sceneReviews'])['dependencyReviewNeeded'])

    def test_registry_and_saved_selection_conflict_is_visible(self):
        a=json.loads((HERE/'test_source_foundation_cases.json').read_text())[0]['arguments']
        saved={'project':'hon','storyID':a['storyID'],'shotID':a['shot']['shotID'],'ingredients':[{'kind':'reference',**a['model']['bindings'][0]['inputs'][0]}]}
        self.assertEqual(f.derive(a['model'],a['shot'],'hon',a['storyID'],a['assets'],scene_reviews=[saved])['state'],'detailed')
        saved['ingredients'][0]['assetID']='another:selected:asset'
        self.assertEqual(f.derive(a['model'],a['shot'],'hon',a['storyID'],a['assets'],scene_reviews=[saved])['state'],'unresolved')

if __name__=='__main__':unittest.main()
