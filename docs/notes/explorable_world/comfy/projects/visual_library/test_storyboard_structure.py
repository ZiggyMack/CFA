from copy import deepcopy
import json
from pathlib import Path
import unittest
import tempfile
import shutil
import storyboard_structure as adapter
from storyboard_structure import apply_storyboard_structure, content_status, numbered, FIELDS, KITCHEN_FIELDS

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[5]
def catalog():
    return json.loads((HERE/'catalog.js').read_text(encoding='utf-8').split('=',1)[1].strip().removesuffix(';'))

class StoryboardStructureTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original=catalog(); cls.data=deepcopy(cls.original)
        apply_storyboard_structure(cls.data,ROOT)
        cls.structure=cls.data['storyboardStructure']; cls.story=cls.structure['stories'][0]
        cls.shots={s['shotID']:s for s in cls.story['shots']}
    def fields(self,sid): return {f['key']:f for f in self.shots[sid]['fields']}
    def test_current_publication_projection_is_unchanged(self):
        self.assertEqual(self.original.get('storyboardStructure'),self.structure)
    def test_authored_order_survives_without_media(self):
        self.assertEqual(len(self.shots),70)
        self.assertEqual(len(self.story['sections']),14)
        self.assertEqual([s['shotID'] for s in self.story['shots']], [sid for section in self.story['sections'] for sid in section['shotIDs']])
        self.assertIn('P-6b',self.shots)
        self.assertEqual(sum(s['kitchenWritten'] for s in self.shots.values()),11)
        self.assertEqual(len(self.fields('P-1')),len(FIELDS))
    def test_ship_shot_missing_prompt_is_not_missing_character_or_camera(self):
        fields=self.fields('S02-9')
        self.assertEqual(fields['character']['status'],'not_needed')
        self.assertEqual(fields['camera']['status'],'draft')
        self.assertEqual(fields['lighting']['status'],'draft')
        self.assertEqual(fields['prompt_clip']['status'],'missing')
        self.assertEqual(fields['start_frame']['status'],'missing')
        kitchen={f['key']:f for f in self.shots['S02-9']['kitchen']}
        self.assertEqual(kitchen['11.10']['status'],'missing')
    def test_still_and_lipsync_prompt_are_independent(self):
        self.assertEqual(self.fields('S02-6')['prompt_still']['status'],'draft')
        self.assertEqual(self.fields('S02-6')['prompt_clip']['status'],'missing')
        self.assertEqual(self.fields('S02-8')['prompt_clip']['status'],'draft')
        self.assertTrue(self.shots['S02-8']['unresolvedReferences'])
    def test_scoped_mouth_correction_does_not_accept_scene(self):
        fields=self.fields('S01-1')
        self.assertIn('dental_mouth_only',fields['references']['note'])
        self.assertEqual(fields['acceptance']['status'],'unknown')
        self.assertEqual(fields['start_frame']['status'],'missing')
        self.assertEqual(self.shots['S01-1']['revisions'][0]['status'],'draft')
    def test_headings_alone_and_explicit_none(self):
        parsed=numbered('2. **LIGHTING.**\n3. **CAMERA.**\n4. **CHARACTER DIRECTION.** None.\n7. **RESULTING PROMPT.** Not yet.\n')
        self.assertEqual(content_status(parsed['2']),'unknown')
        self.assertEqual(content_status(parsed['3']),'unknown')
        self.assertEqual(content_status(parsed['4']),'not_needed')
        self.assertEqual(content_status(parsed['7']),'missing')
    def test_future_planned_slot_without_card_or_media(self):
        with tempfile.TemporaryDirectory(dir=ROOT/'.cache',prefix='structure-fixture-') as folder:
            fixture=Path(folder)
            rows=json.loads(adapter.read(ROOT,adapter.MAP))
            paths={adapter.MAP,adapter.ADDENDUM,adapter.WRITER+'OPENING_PACKET_20261028.md',adapter.KITCHEN+'S02_PACKET_20261029.md',adapter.KITCHEN+'EXAMPLE_S01-1_KITCHEN_BLOCK_20261029.md'}
            paths.update(row['cardRepoPath'] for row in rows['shots'])
            for relative in paths:
                target=fixture/relative;target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/relative,target)
            sid='TEST-UNWRITTEN'
            rows['shots'].append({'shotID':sid,'sectionID':rows['sections'][0]['id'],'title':'Empty fixture slot','cardRepoPath':'absent/card.md'})
            rows['sections'][0]['shotIDs'].append(sid)
            (fixture/adapter.MAP).write_text(json.dumps(rows),encoding='utf-8')
            result=adapter.build_hon(fixture,self.original)
            shot=next(s for s in result['shots'] if s['shotID']==sid)
            self.assertEqual(len(result['shots']),71)
            self.assertEqual(shot['revision'],'unwritten')
            self.assertFalse(shot['materials'])
            self.assertTrue(all(f['status']=='unknown' and not f['text'] for f in shot['fields']))
            self.assertEqual(shot['source']['path'],adapter.MAP)
            self.assertEqual(shot['parent']['path'],adapter.MAP)
    def test_existing_ids_reviews_and_source_bytes_are_untouched(self):
        for key in ['reviewDecisions','sceneReviews','reviewIntake','shotMaterials','storyboardSequences']:
            self.assertEqual(self.original[key],self.data[key],key)
        originals={a['id']:a for a in self.original['assets']}
        self.assertEqual(originals,{a['id']:a for a in self.data['assets'] if a['id'] in originals})
        self.assertEqual(len(KITCHEN_FIELDS),12)
        self.assertTrue(self.structure['template']['demonstration'])
        self.assertNotIn('shotID',self.structure['template'])
    def test_persisted_checkpoint_detects_change_on_fresh_build(self):
        checkpoint=json.loads(json.dumps(self.structure))
        checkpoint['stories'][0]['shots'][0]['dependencies'][0]['sha256']='0'*64
        fresh=deepcopy(self.original); fresh.pop('storyboardStructure',None)
        apply_storyboard_structure(fresh,ROOT,previous_structure=checkpoint)
        changed=fresh['storyboardStructure']['stories'][0]['shots'][0]
        self.assertTrue(changed['dependencyReviewNeeded'])
        self.assertEqual(changed['priorDependencyEvidence'][0]['sha256'],'0'*64)
    def test_only_four_requests_and_latest_delta_are_applied_idempotently(self):
        task=next(t for t in self.data['missionControl']['tasks'] if t['id']=='hon-coverage-review-queue-20261028')
        self.assertEqual(len(task['missing']),17)
        self.assertIn('start state',task['missing'][15])
        self.assertIn('30-panel',task['laterReview'])
        first=deepcopy(self.data); apply_storyboard_structure(first,ROOT)
        self.assertEqual(first,self.data)

if __name__=='__main__': unittest.main()
