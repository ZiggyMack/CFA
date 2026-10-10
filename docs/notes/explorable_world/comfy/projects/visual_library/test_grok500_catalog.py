"""Contract tests for the verified-intake adapter; no catalog generation."""
import copy
import csv
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest

from grok500_catalog import CatalogIntakeError, SHOTS, load_grok500


class Grok500CatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory()
        cls.root = Path(cls.temp.name)
        cls.intake = cls.root / 'intake'
        cls.received = cls.intake / 'received'
        cls.received.mkdir(parents=True)
        cls.records, rows = [], []

        def add(relative, data, image=False):
            p = cls.received / relative
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
            rec = {'relative_path': relative, 'bytes': len(data),
                   'sha256': hashlib.sha256(data).hexdigest()}
            if image:
                # This unit boundary consumes a prior decode receipt. It does
                # not reimplement or simulate the extractor's image decoder.
                rec['image'] = {'width': 1280, 'height': 720, 'decoded': True}
            cls.records.append(rec)

        for i in range(1, 51):
            look = f'L{i:02}'
            slug = f'LAG-{look}-test-look'
            part = 1 if i <= 6 else min(8, (i - 7) // 7 + 2)
            folder = f'content/LAG-500-MASTER-part{part:02}/{slug}.zip.contents/{slug}/'
            for j, shot in enumerate(SHOTS):
                n = (i - 1) * 10 + j + 1
                filename = slug + '__' + shot + '-test.jpg'
                add(folder + filename, f'unit-test source {n}'.encode(), True)
                rows.append({'row': str(n), 'look_num': look, 'look_slug': slug,
                             'shot': shot, 'shot_name': shot + ' test scene',
                             'filename': filename, 'zip_name': slug + '.zip',
                             'outfit': 'Test outfit', 'setting': 'Test setting',
                             'breather': 'N', 'arm_worm': 'N',
                             'qa_status': 'FLAG' if n == 4 else 'OK-note' if n == 1 else 'OK',
                             'qa_note': 'Provider only', 'hero': 'Y' if n == 3 else 'N'})
            add(folder + 'CONTACT-' + slug + '.jpg', f'contact {i}'.encode(), True)
        prefix = 'content/LAG-500-MASTER-part01/'
        add(prefix + 'CONTACT-INDEX.jpg', b'index fixture', True)
        cls.rows = rows
        buf = io.StringIO(newline='')
        writer = csv.DictWriter(buf, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
        add(prefix + 'LEGEND-500.csv', buf.getvalue().encode())
        add(prefix + 'NOVA-GUIDE-500.md', b'Provider guide')
        add(prefix + 'QA.txt', b'Provider QA log')
        cls.receipt = {'state': 'all_eight_extracted_crc_hash_size_decode_verified',
                       'verified_top_level_parts': 8, 'files': cls.records}
        cls.receipt_path = cls.received / 'intake_receipt.json'

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def setUp(self):
        self.write_receipt(copy.deepcopy(self.receipt))

    def write_receipt(self, value):
        self.receipt_path.write_text(json.dumps(value), encoding='utf-8')

    def load(self):
        return load_grok500(self.root, self.intake)

    def test_complete_pack_keeps_provider_judgments_separate(self):
        data = self.load()
        self.assertEqual(len(data['assets']), 551)
        self.assertEqual(len([a for a in data['albums'] if a['category'] == 'outfits']), 50)
        self.assertEqual(len(data['documents']), 3)
        self.assertEqual(data['summary']['newUserApprovals'], 0)
        self.assertEqual(data['summary']['providerHeroCandidates'], 1)
        assets = {a['id']: a for a in data['assets']}
        self.assertTrue(assets['LAG500-L01-V3']['providerQA']['heroCandidate'])
        for a in data['assets']:
            for protected in ('workingReference', 'variant', 'review', 'favorite',
                              'storyboardStage', 'storyboardOrder', 'storyboardPosition'):
                self.assertNotIn(protected, a)
        flag_album = next(a for a in data['albums'] if a['category'] == 'review')
        self.assertEqual(flag_album['related'], ['LAG500-L01-V4'])
        self.assertIn('not a timed', assets['LAG500-L01-S1']['role'])
        self.assertEqual(sum('shotCode' in a for a in data['assets']), 500)

    def test_source_views_and_contact_order(self):
        data = self.load()
        first = [a['id'] for a in data['assets'] if a['album'] == 'lisan:grok500-l01']
        self.assertEqual(first, [f'LAG500-L01-{s}' for s in SHOTS] + ['LAG500-L01-CONTACT'])

    def test_missing_receipt_is_optional(self):
        self.receipt_path.unlink()
        self.assertIsNone(self.load())

    def test_incomplete_or_cleanup_in_progress_receipt_rejected(self):
        for state in ('inspection_only_no_files_written', 'verified_cleanup_in_progress'):
            receipt = copy.deepcopy(self.receipt)
            receipt['state'] = state
            self.write_receipt(receipt)
            with self.assertRaises(CatalogIntakeError):
                self.load()
        receipt['state'] = 'all_eight_extracted_crc_hash_size_decode_verified'
        receipt['verified_top_level_parts'] = 7
        self.write_receipt(receipt)
        with self.assertRaises(CatalogIntakeError):
            self.load()

    def test_cleaned_zip_receipt_needs_no_zip_files(self):
        receipt = copy.deepcopy(self.receipt)
        receipt['state'] = 'verified_extracted_zip_copies_removed'
        self.write_receipt(receipt)
        self.assertEqual(len(self.load()['assets']), 551)

    def test_verified_folder_intake_is_supported(self):
        receipt = copy.deepcopy(self.receipt)
        receipt['state'] = 'eight_folders_nested_CRC_csv_hash_size_decode_verified'
        receipt['schema'] = 'grok500-folder-intake-v1'
        self.write_receipt(receipt)
        self.assertEqual(self.load()['summary']['lookCount'], 50)

    def test_source_hash_mismatch_rejected(self):
        receipt = copy.deepcopy(self.receipt)
        receipt['files'][0]['sha256'] = '0' * 64
        self.write_receipt(receipt)
        with self.assertRaisesRegex(CatalogIntakeError, 'differs'):
            self.load()

    def test_missing_decode_evidence_rejected(self):
        receipt = copy.deepcopy(self.receipt)
        receipt['files'][0]['image']['decoded'] = False
        self.write_receipt(receipt)
        with self.assertRaisesRegex(CatalogIntakeError, 'decode'):
            self.load()

    def test_extra_image_cannot_silently_disappear(self):
        receipt = copy.deepcopy(self.receipt)
        extra = copy.deepcopy(receipt['files'][0])
        extra['relative_path'] = 'content/unmapped.jpg'
        receipt['files'].append(extra)
        self.write_receipt(receipt)
        with self.assertRaisesRegex(CatalogIntakeError, 'match 500'):
            self.load()

    def test_duplicate_or_escape_paths_rejected(self):
        for relative in ('../outside.jpg', '/outside.jpg', 'C:/outside.jpg',
                         'content\\outside.jpg', self.records[0]['relative_path']):
            receipt = copy.deepcopy(self.receipt)
            receipt['files'].append({'relative_path': relative})
            self.write_receipt(receipt)
            with self.assertRaisesRegex(CatalogIntakeError, 'Unsafe|duplicate'):
                self.load()

    def test_mismatched_legend_shot_rejected(self):
        receipt = copy.deepcopy(self.receipt)
        rec = next(r for r in receipt['files'] if r['relative_path'].endswith('LEGEND-500.csv'))
        path = self.received / rec['relative_path']
        original = path.read_bytes()
        try:
            text = original.decode().replace(',V1,V1 test scene,', ',S1,V1 test scene,', 1)
            raw = text.encode()
            path.write_bytes(raw)
            rec['bytes'] = len(raw)
            rec['sha256'] = hashlib.sha256(raw).hexdigest()
            self.write_receipt(receipt)
            with self.assertRaisesRegex(CatalogIntakeError, 'Inconsistent look'):
                self.load()
        finally:
            path.write_bytes(original)


if __name__ == '__main__':
    unittest.main()
