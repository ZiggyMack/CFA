"""Bounded Story 01 source/lineage checks. No catalog build or source writes."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

from grok500_catalog import CatalogIntakeError
import story01_intake as intake


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]


class Story01IntakeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw = (HERE / 'catalog.js').read_text(encoding='utf-8-sig')
        cls.catalog = json.loads(raw.split('=', 1)[1].strip().rstrip(';'))
        cls.map = json.loads((ROOT / intake.MAP_PATH).read_text(encoding='utf-8-sig'))
        cls.added_document_ids = {'lisan:doc:' + p for p in [intake.MAP_PATH, intake.MAP_MD_PATH, intake.SKELETON_PATH]}
        # Also works after publication: emulate the catalog immediately before this intake.
        cls.existing = [deepcopy(a) for a in cls.catalog['assets']
                        if a.get('storySequenceID') != intake.SEQUENCE_ID and a['id'] not in cls.added_document_ids]
        cls.before = deepcopy(cls.existing)
        cls.loaded = intake.load_story01(ROOT, cls.existing)

    def test_exact_new_and_reused_identity_without_source_mutation(self):
        self.assertEqual(self.existing, self.before)
        self.assertEqual(len(self.loaded['assets']), 50)
        self.assertEqual(len(self.loaded['documents']), 3)
        verification = self.loaded['verification']
        self.assertEqual(verification['reusedAssetCount'], 6)
        self.assertEqual({r['assetID'] for r in verification['reusedAssets']}, set(intake.CANONICAL_MATERIAL_IDS.values()))
        self.assertEqual(verification['materialAssociationCount'], 98)
        self.assertEqual(len(self.loaded['sequence']['assetIDs']), 56)
        self.assertEqual(len(set(self.loaded['sequence']['assetIDs'])), 56)
        self.assertEqual(self.loaded['albums'][0]['related'], self.loaded['sequence']['assetIDs'])
        for asset in self.loaded['assets']:
            self.assertEqual(asset['id'], 'LAG-1K-' + asset['sha256'][:16])
            self.assertEqual(asset['album'], intake.ALBUM_ID)
        for record in verification['materialFiles'] + verification['attachments']:
            raw = (ROOT / record['path']).read_bytes()
            self.assertEqual(len(raw), record['bytes'])
            self.assertEqual(hashlib.sha256(raw).hexdigest(), record['sha256'])

    def test_exact_shot_order_roles_notes_pins_and_pending_references_preserved(self):
        sequence = self.loaded['sequence']
        self.assertEqual(sequence['sections'], self.map['sections'])
        self.assertEqual([s['shotID'] for s in sequence['shots']], [s['shotID'] for s in self.map['shots']])
        self.assertEqual(sequence['sourceAlbumIDs'], [intake.ALBUM_ID])
        first = self.map['shots'][0]['materials'][0]
        self.assertEqual(sequence['coverID'], 'LAG-1K-' + first['sha256'][:16])
        for actual, original in zip(sequence['shots'], self.map['shots']):
            restored = deepcopy(actual)
            restored.pop('pendingReferenceDetails')
            for material in restored['materials']:
                self.assertIn(material.pop('assetID'), sequence['assetIDs'])
            self.assertEqual(restored, original)
        original_documents = list(dict.fromkeys([intake.MAP_PATH, intake.MAP_MD_PATH,
                                                 intake.SKELETON_PATH, *self.map['sourceDocuments']]))
        self.assertEqual(sequence['documentIDs'], ['lisan:doc:' + p for p in original_documents])
        self.assertEqual(len(sequence['documentIDs']), 6)
        for reference in sequence['sourceDocumentReferences']:
            raw = (ROOT / reference['path']).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), reference['sha256'])

    def test_coverage_distinguishes_frame_character_and_object_gaps(self):
        summary = self.loaded['sequence']['summary']
        self.assertEqual(summary, {'shots': 38, 'shotsWithAFrameOnDisk': 33,
            'shotsWithAResultOnDisk': 1, 'shotsWithPendingReferences': 21, 'distinctFiles': 56,
            'shotsWithPendingCharacterReferences': 20, 'shotsWithPendingObjectReferences': 5,
            'shotsWithOnlyPendingObjectReferences': 1})
        coverage = self.loaded['verification']
        self.assertEqual(coverage['objectOnlyPendingShotIDs'], ['S01-5.3'])
        self.assertEqual(coverage['pendingObjectShotIDs'], ['S01-2.2', 'S01-5.2', 'S01-5.3', 'S01-7.10', 'S01-8.1'])
        self.assertNotIn('S01-2.2', coverage['frameShotIDs'], 'Idea-only concepts do not inflate the frame count to 34')
        self.assertEqual(coverage['resultShotIDs'], ['S01-4.1'])
        lattice = next(s for s in self.loaded['sequence']['shots'] if s['shotID'] == 'S01-5.3')
        self.assertEqual(lattice['pendingReferenceDetails'], [{'label': 'the lattice', 'kind': 'object_design'}])

    def test_canonical_source_choice_result_and_human_reviews_are_not_promoted(self):
        sequence = self.loaded['sequence']
        rise = next(s for s in sequence['shots'] if s['shotID'] == 'S01-4.1')
        self.assertEqual([(m['assetID'], m['role']) for m in rise['materials']], [
            ('LAG-C13-PATCH-C-23817577d3d3', 'source_frame'),
            ('LAG-C13-ORIGINAL-7eafd9ac048d', 'storyboard_concept'),
            ('FLOW-LAG-SW2-001', 'result_on_disk')])
        self.assertEqual(sequence['stage'], 'preliminary')
        self.assertIsNone(sequence['timing'])
        for asset in self.loaded['assets']:
            for field in ['likenessRating', 'sceneQualityRating', 'status', 'workingReference',
                          'componentApprovals', 'shotPlan', 'sourceChoice', 'storyboardOrder']:
                self.assertNotIn(field, asset)
            self.assertEqual(asset['storyboardStage'], 'preliminary')
            self.assertEqual(asset['acceptance'], 'not_accepted')
            self.assertFalse(asset['masterApproved'])
            self.assertFalse(asset['productionReady'])
            self.assertIsNone(asset['timing'])
            self.assertIn('not human ratings', asset['note'])
        self.assertEqual(self.existing, self.before, 'All canonical metadata, including Meta Mirror timing, is untouched')
        self.assertEqual(self.loaded['verification']['newApprovals'], 0)

    def test_repeated_load_reuses_exact_records_and_keeps_sequence_stable(self):
        previous = deepcopy(self.existing)
        for asset in self.loaded['assets']:
            previous.append({**deepcopy(asset), 'repoPath': asset['path'], 'kind': 'image'})
        for document in self.loaded['documents']:
            previous.append({**deepcopy(document), 'repoPath': document['path'], 'kind': 'document'})
        before = deepcopy(previous)
        repeated = intake.load_story01(ROOT, previous)
        self.assertEqual(repeated['assets'], [])
        self.assertEqual(repeated['documents'], [])
        self.assertEqual(repeated['sequence'], self.loaded['sequence'])
        self.assertEqual(previous, before)

    def test_bad_map_attachment_material_and_during_read_changes_fail_closed(self):
        original_read = intake._read_bytes
        material_path = self.map['shots'][0]['materials'][0]['repoPath']
        for relative in [intake.MAP_PATH, intake.SKELETON_PATH, material_path]:
            target = (ROOT / relative).resolve()
            def altered(path, target=target):
                raw = original_read(path)
                return bytes([raw[0] ^ 1]) + raw[1:] if path == target else raw
            with self.subTest(relative=relative), patch.object(intake, '_read_bytes', side_effect=altered):
                with self.assertRaisesRegex(CatalogIntakeError, 'pin mismatch'):
                    intake.load_story01(ROOT, self.existing)
        target = (ROOT / material_path).resolve()
        calls = 0
        def changing(path):
            nonlocal calls
            raw = original_read(path)
            if path == target:
                calls += 1
                if calls > 1:
                    return raw + b'changed'
            return raw
        with patch.object(intake, '_read_bytes', side_effect=changing):
            with self.assertRaisesRegex(CatalogIntakeError, 'changed during intake'):
                intake.load_story01(ROOT, self.existing)

    def test_registered_pin_collision_and_missing_canonical_identity_fail_closed(self):
        bad = deepcopy(self.existing)
        canonical = next(a for a in bad if a['id'] == 'LAG-C13-PATCH-C-23817577d3d3')
        canonical['sha256'] = '0' * 64
        with self.assertRaisesRegex(CatalogIntakeError, 'identity differs'):
            intake.load_story01(ROOT, bad)
        missing = [a for a in self.existing if a['id'] != 'FLOW-LAG-SW2-001']
        with self.assertRaisesRegex(CatalogIntakeError, 'Required canonical'):
            intake.load_story01(ROOT, missing)
        incoming = self.loaded['assets'][0]
        collision = [*deepcopy(self.existing), {'id': incoming['id'], 'project': 'lisan',
                     'repoPath': 'docs/notes/unrelated.jpg', 'sha256': '0' * 64}]
        with self.assertRaisesRegex(CatalogIntakeError, 'ID collision'):
            intake.load_story01(ROOT, collision)
        alias = [*deepcopy(self.existing), {'id': 'OTHER-PATH', 'project': 'lisan',
                 'repoPath': 'docs/notes/unrelated.jpg', 'sha256': incoming['sha256']}]
        with self.assertRaisesRegex(CatalogIntakeError, 'different registered path'):
            intake.load_story01(ROOT, alias)


if __name__ == '__main__':
    unittest.main()
