"""Sealed coverage integrity, shared-model integration and preservation checks."""
from copy import deepcopy
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from criminal_mind_intake import apply_criminal_mind_intake, INTAKE
from criminal_mind_storyboard import (
    apply_criminal_mind_storyboard, CARDS_ID, STRUCTURE_ID, VERIFICATION_ID,
    DOCUMENTS, FIELD_KEYS, PACKET_DIR, PROJECT_ID, STORY_ID,
)
from storyboard_structure import FIELDS, KITCHEN_FIELDS

ROOT = Path(__file__).resolve().parents[6]


class CriminalMindStoryboardTests(unittest.TestCase):
    def fixture(self):
        catalog = {
            'projects': [{'id': 'hon'}, {'id': 'lisan'}, {'id': 'unassigned'}],
            'assets': [{'id': 'existing', 'project': 'hon', 'kind': 'image', 'sha256': 'a' * 64}],
            'albums': [], 'reviewDecisions': [{'id': 'existing', 'rating': 1, 'reviewer': 'Ziggy'}],
            'missionControl': {'tasks': [{'id': 'existing-task', 'project': 'hon'}]},
            'shotMaterials': {'shots': [{'id': 'unchanged-shot'}]},
            'storyboardStories': [{'id': 'hon:strictly-business', 'project': 'hon'}],
            'storyboardSequences': [{'id': 'existing-sequence', 'project': 'lisan'}],
            'storyboardStructure': {
                'format': 'cfa-storyboard-structure-v1', 'updated': 'preserve-this-date',
                'fields': [dict(key=k, section=s, label=label, owner=owner, phase=phase, hint=hint)
                           for k, s, label, owner, phase, hint in FIELDS],
                'kitchenFields': [dict(key=k, label=label, hint=hint) for k, label, hint in KITCHEN_FIELDS],
                'stories': [{'storyID': 'hon:strictly-business', 'project': 'hon', 'shots': [{'shotID': 'P-1'}]}],
                'template': {'demonstration': True, 'source': {'path': 'unchanged-template'}},
            },
            'storyboardTakes': {'takes': [{'id': 'unchanged-take'}]},
            'storyboardSourceFoundation': {'bindings': [{'project': 'hon', 'shotID': 'P-1'}]},
        }
        apply_criminal_mind_intake(catalog, ROOT)
        return catalog

    def test_sealed_packet_populates_both_views_and_keeps_source_blocks_distinct(self):
        catalog = self.fixture()
        apply_criminal_mind_storyboard(catalog, ROOT)
        story = next(s for s in catalog['storyboardStories'] if s['id'] == STORY_ID)
        sequence = next(s for s in catalog['storyboardSequences'] if s['id'] == story['sequenceID'])
        structure = next(s for s in catalog['storyboardStructure']['stories'] if s['storyID'] == STORY_ID)
        self.assertEqual(len(sequence['shots']), 165)
        self.assertEqual(len(sequence['sections']), 41)
        self.assertEqual([s['shotID'] for s in sequence['shots']], [s['shotID'] for s in structure['shots']])
        self.assertTrue(all(s['label'] and s['line'] and s['pendingReferences'] and not s['materials'] for s in sequence['shots']))
        self.assertTrue(all([f['key'] for f in s['fields']] == list(FIELD_KEYS) and s['stage'] == 'preliminary' for s in structure['shots']))
        project = next(p for p in catalog['projects'] if p['id'] == PROJECT_ID)
        self.assertEqual(len(project['landing']['sourceBlocks']), 41)
        self.assertEqual(project['landing']['authoredShotCount'], 165)
        self.assertIn('Review the current writer decisions', project['landing']['nextStep'])
        self.assertNotIn('can still choose', project['landing']['nextStep'])
        self.assertEqual(catalog['storyboardMetadata'][PROJECT_ID]['panelCount'], 0)
        self.assertTrue(any(s['timeLayer'] != 'present_day' for s in structure['shots']))

    def test_registered_writer_development_is_reachable_from_the_story(self):
        catalog = self.fixture()
        document_id = 'criminal_mind:doc:technical-lineage.md'
        catalog['assets'].append({'id': document_id, 'project': PROJECT_ID, 'kind': 'document'})
        catalog['writerDevelopment'] = {'projects': [{
            'id': PROJECT_ID,
            'groups': [
                {'id': 'reader', 'storyboard': True, 'documentIDs': [document_id]},
                {'id': 'not-storyboard', 'storyboard': False, 'documentIDs': ['not-linked']},
            ],
        }]}
        apply_criminal_mind_storyboard(catalog, ROOT)
        story = next(s for s in catalog['storyboardStories'] if s['id'] == STORY_ID)
        self.assertIn(document_id, story['documentIDs'])
        self.assertNotIn('not-linked', story['documentIDs'])

    def test_repeat_application_is_exact_and_keeps_existing_records_and_scope_task(self):
        catalog = self.fixture()
        before = deepcopy(catalog)
        apply_criminal_mind_storyboard(catalog, ROOT)
        first = deepcopy(catalog)
        self.assertIs(apply_criminal_mind_storyboard(catalog, ROOT), catalog)
        self.assertEqual(catalog, first)
        for key in ('reviewDecisions', 'missionControl', 'shotMaterials', 'storyboardTakes', 'storyboardSourceFoundation'):
            self.assertEqual(catalog[key], before[key], key)
        for key in ('format', 'updated', 'fields', 'kitchenFields', 'template'):
            self.assertEqual(catalog['storyboardStructure'][key], before['storyboardStructure'][key], key)
        self.assertEqual(catalog['storyboardStructure']['stories'][0], before['storyboardStructure']['stories'][0])
        self.assertEqual(catalog['assets'][:-3], before['assets'])
        self.assertEqual([p for p in catalog['projects'] if p['id'] != PROJECT_ID],
                         [p for p in before['projects'] if p['id'] != PROJECT_ID])

    def test_documents_keep_full_sources_without_embedding_large_json_text(self):
        catalog = self.fixture()
        apply_criminal_mind_storyboard(catalog, ROOT)
        assets = {a['id']: a for a in catalog['assets']}
        for aid in (CARDS_ID, STRUCTURE_ID):
            self.assertLess(len(assets[aid]['text']), 1000)
            self.assertTrue(assets[aid]['textPreviewOnly'])
            self.assertTrue(assets[aid]['inert'])
            self.assertFalse(assets[aid].get('downloadOnly'))
        self.assertEqual(assets[STRUCTURE_ID]['bytes'], (ROOT / PACKET_DIR / DOCUMENTS[1][1]).stat().st_size)
        self.assertEqual(json.loads(assets[VERIFICATION_ID]['text'])['proposedCoverageShots'], 165)
        structure = catalog['storyboardStructure']['stories'][-1]
        for shot in structure['shots']:
            for field in shot['fields']:
                for evidence in field['evidence']:
                    self.assertEqual(assets[evidence['assetID']]['sha256'], evidence['sha256'])
                    self.assertEqual(assets[evidence['assetID']]['repoPath'], evidence['path'])

    def test_changed_sealed_source_fails_before_mutation(self):
        catalog = self.fixture()
        before = deepcopy(catalog)
        with tempfile.TemporaryDirectory(dir=ROOT / '.cache') as directory:
            temp = Path(directory)
            (temp / PACKET_DIR).mkdir(parents=True)
            for row in DOCUMENTS:
                shutil.copyfile(ROOT / PACKET_DIR / row[1], temp / PACKET_DIR / row[1])
            with (temp / PACKET_DIR / DOCUMENTS[0][1]).open('ab') as stream:
                stream.write(b'changed')
            with self.assertRaisesRegex(ValueError, 'source bytes changed'):
                apply_criminal_mind_storyboard(catalog, temp)
        self.assertEqual(catalog, before)

    def test_wrong_script_binding_and_existing_record_conflict_fail_atomically(self):
        catalog = self.fixture()
        script = next(a for a in catalog['assets'] if a['id'] == 'TCM-SCRIPT-TEXT')
        script['sha256'] = '0' * 64
        before = deepcopy(catalog)
        with self.assertRaisesRegex(ValueError, 'source bytes changed'):
            apply_criminal_mind_storyboard(catalog, ROOT)
        self.assertEqual(catalog, before)
        catalog = self.fixture()
        catalog['storyboardStories'].append({'id': STORY_ID, 'project': PROJECT_ID, 'title': 'A later proposal'})
        before = deepcopy(catalog)
        with self.assertRaisesRegex(ValueError, 'reconcile separately'):
            apply_criminal_mind_storyboard(catalog, ROOT)
        self.assertEqual(catalog, before)


if __name__ == '__main__':
    unittest.main()
