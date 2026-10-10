"""Synthetic cleanup gates; never uses production originals."""
import json
from pathlib import Path
import unittest
import zipfile

import cleanup_grok500_folders as cleanup
import intake_grok500 as core
import intake_grok500_folders as folders
import test_intake_grok500_folders as fixtures

jpg = fixtures.jpg


class CleanupTests(unittest.TestCase):
    write_rows = fixtures.FolderIntakeTests.write_rows

    def setUp(self):
        fixtures.FolderIntakeTests.setUp(self)
        plan = folders.inspect_folders(self.inputs, self.output)
        folders.extract_folders(plan)
        self.receipt = self.output / 'intake_receipt.json'
        self.sha = core.file_hash(self.receipt)

    tearDown = fixtures.FolderIntakeTests.tearDown

    def plan(self):
        return cleanup.prepare(self.receipt, self.sha, self.inputs, self.root)

    def rewrite_receipt_for_negative_fixture(self, change):
        doc = json.loads(self.receipt.read_text(encoding='utf-8'))
        change(doc)
        self.receipt.write_text(json.dumps(doc), encoding='utf-8')
        self.sha = core.file_hash(self.receipt)

    def test_dry_run_then_exact_cleanup_preserves_every_other_file(self):
        other = self.inputs / 'Processed'
        other.mkdir()
        unrelated = other / 'old-pack.zip'
        unrelated.write_bytes(self.zips[0].read_bytes())
        plan = self.plan()
        self.assertFalse((self.output / 'cleanup_summary.json').exists())
        self.assertTrue(all(p.is_file() for p in self.zips))
        expected_bytes = sum(p.stat().st_size for p in self.zips)
        result = cleanup.execute(plan)
        self.assertTrue(result['cleanup_complete'])
        self.assertEqual(result['zip_files_removed'], 50)
        self.assertEqual(result['bytes_freed'], expected_bytes)
        self.assertEqual(result['verified_output_files_after_cleanup'], 555)
        self.assertTrue(all(not p.exists() for p in self.zips))
        self.assertTrue(unrelated.is_file())
        self.assertTrue(self.guide.is_file())
        self.assertTrue(self.legend.is_file())
        self.assertTrue(all((self.inputs / n).is_dir() for n in folders.PARTS))
        self.assertEqual(core.file_hash(self.receipt), self.sha)
        with self.assertRaisesRegex(core.IntakeError, 'journal already exists'):
            cleanup.execute(plan)

    def test_changed_extracted_file_blocks_before_any_zip_removal(self):
        doc = json.loads(self.receipt.read_text(encoding='utf-8'))
        target = folders.output_path(self.output, doc['files'][0]['relative_path'])
        target.write_bytes(b'changed extracted bytes')
        with self.assertRaisesRegex(core.IntakeError, 'Extracted size/hash mismatch'):
            self.plan()
        self.assertTrue(all(p.is_file() for p in self.zips))
        self.assertFalse((self.output / 'cleanup_summary.json').exists())

    def test_changed_zip_after_dry_run_blocks_execute_before_deletion(self):
        plan = self.plan()
        self.zips[0].write_bytes(b'changed ZIP')
        with self.assertRaisesRegex(core.IntakeError, 'ZIP size/hash changed'):
            cleanup.execute(plan)
        self.assertTrue(all(p.is_file() for p in self.zips))
        self.assertFalse((self.output / 'cleanup_summary.json').exists())

    def test_frozen_receipt_workspace_and_exact_part_scope_are_required(self):
        with self.assertRaisesRegex(core.IntakeError, 'receipt SHA-256'):
            cleanup.prepare(self.receipt, '0' * 64, self.inputs, self.root)
        with self.assertRaisesRegex(core.IntakeError, 'outside resolved workspace'):
            cleanup.prepare(self.receipt, self.sha, self.inputs, self.inputs)
        excluded = self.inputs / 'Processed'
        excluded.mkdir()
        alternate = excluded / self.zips[0].name
        alternate.write_bytes(self.zips[0].read_bytes())
        self.rewrite_receipt_for_negative_fixture(lambda d: d['archives'][0].update(source_path=str(alternate)))
        with self.assertRaisesRegex(core.IntakeError, 'exact permitted source-part scope'):
            self.plan()
        self.assertTrue(all(p.is_file() for p in self.zips))
        self.assertTrue(alternate.exists())

    def test_fresh_crc_required_even_when_a_bad_fixture_claims_a_good_hash(self):
        zp = self.zips[0]
        data = bytearray(zp.read_bytes())
        data[data.index(jpg()) + 25] ^= 1
        zp.write_bytes(data)
        def mutate(doc):
            for a in doc['archives']:
                if Path(a['source_path']) == zp:
                    a['sha256'] = core.file_hash(zp)
            for r in doc['source_files']:
                if Path(r['path']) == zp:
                    r['sha256'] = core.file_hash(zp)
        self.rewrite_receipt_for_negative_fixture(mutate)
        with self.assertRaises((core.IntakeError, zipfile.BadZipFile)):
            self.plan()
        self.assertTrue(all(p.is_file() for p in self.zips))
        self.assertFalse((self.output / 'cleanup_summary.json').exists())


if __name__ == '__main__':
    unittest.main()
