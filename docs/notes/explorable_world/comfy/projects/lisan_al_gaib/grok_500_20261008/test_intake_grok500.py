"""Synthetic fixtures only; these tests make no claims about the provider drop."""
import io
import json
from pathlib import Path
import stat
import tempfile
import unittest
import zipfile

from PIL import Image

import intake_grok500 as intake


NAMES = [f'LAG-500-MASTER-part{n:02d}.zip' for n in range(1, 9)]


def png():
    b = io.BytesIO()
    Image.new('RGB', (8, 6), (40, 90, 120)).save(b, 'PNG')
    return b.getvalue()


def zip_bytes(entries):
    b = io.BytesIO()
    with zipfile.ZipFile(b, 'w', zipfile.ZIP_STORED) as z:
        for name, data in entries:
            z.writestr(name, data)
    return b.getvalue()


class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='grok500-test-')
        self.root = Path(self.tmp.name)
        self.inputs = self.root / 'explicit-downloads'
        self.inputs.mkdir()
        self.output = self.root / 'intake'
        self.guide = self.inputs / 'NOVA-GUIDE-500.md'
        self.guide.write_bytes(b'# Synthetic guide\nClaim is a fixture, not provider evidence.\n')
        self.paths = []
        for i, n in enumerate(NAMES, 1):
            inner = zip_bytes([(f'look-{i:02d}/image.png', png()),
                               (f'look-{i:02d}/CONTACT.jpg', self.jpeg()),
                               (f'look-{i:02d}/QA.json', b'{"provider_label":"hero_candidate_only"}')])
            p = self.inputs / n
            p.write_bytes(zip_bytes([(f'look-{i:02d}.zip', inner), ('README.txt', b'Fixture README\r\n')]))
            self.paths.append(p)

    def tearDown(self):
        self.tmp.cleanup()

    @staticmethod
    def jpeg():
        b = io.BytesIO()
        Image.new('RGB', (10, 5), 'gray').save(b, 'JPEG')
        return b.getvalue()

    def plan(self):
        parts, guide, _ = intake.resolve_inputs(NAMES, input_dir=self.inputs)
        return intake.inspect(parts, guide, self.output, provider_claims={'fixture_only': True})

    def first_archive(self, entries):
        self.paths[0].write_bytes(zip_bytes(entries))

    def test_inspect_has_no_filesystem_writes_and_separates_counts(self):
        before = {p: p.read_bytes() for p in self.paths + [self.guide]}
        plan = self.plan()
        self.assertFalse(self.output.exists())
        self.assertEqual(len(plan['archives']), 16)
        self.assertEqual(plan['summary']['total_image_files'], 16)
        self.assertEqual(plan['summary']['filename_classification']['source_image_filename_candidate'], 8)
        self.assertEqual(plan['summary']['filename_classification']['contact_sheet_filename_candidate'], 8)
        self.assertTrue(all(a['crc_verified'] for a in plan['archives']))
        self.assertEqual(plan['new_approvals'], [])
        self.assertEqual(before, {p: p.read_bytes() for p in before})

    def test_nested_extract_preserves_all_files_and_guide(self):
        plan = self.plan()
        intake.extract(plan, self.paths, self.guide)
        self.assertEqual(intake.verify_extracted(plan), len(plan['files']))
        p = self.output / 'content/LAG-500-MASTER-part01/look-01.zip.contents/look-01/QA.json'
        self.assertEqual(p.read_bytes(), b'{"provider_label":"hero_candidate_only"}')
        self.assertEqual((self.output / 'guides/NOVA-GUIDE-500.md').read_bytes(), self.guide.read_bytes())
        self.assertTrue(all(p.exists() for p in self.paths))

    def test_cleanup_only_after_verified_receipt_and_preserves_nonzip(self):
        plan = self.plan()
        with self.assertRaises(intake.IntakeError):
            intake.delete_verified_zips(plan, self.inputs)
        self.assertTrue(all(p.exists() for p in self.paths))
        intake.extract(plan, self.paths, self.guide)
        fresh = self.plan()
        intake.delete_verified_zips(fresh, self.inputs)
        self.assertTrue(fresh['zip_deletion_completed'])
        self.assertEqual(len(fresh['deleted_zip_copies']), 16)
        self.assertTrue(all(not p.exists() for p in self.paths))
        self.assertEqual(len(list(self.output.rglob('*.png'))), 8)
        self.assertEqual(len(list(self.output.rglob('*.jpg'))), 8)
        self.assertTrue(self.guide.exists())
        self.assertEqual(len(list(self.output.rglob('*.zip'))), 0)

    def test_missing_part_blocks_before_any_output(self):
        self.paths[-1].unlink()
        with self.assertRaisesRegex(intake.IntakeError, 'Missing expected'):
            self.plan()
        self.assertFalse(self.output.exists())

    def test_collision_is_case_insensitive(self):
        self.first_archive([('Face.png', png()), ('face.png', png())])
        with self.assertRaisesRegex(intake.IntakeError, 'collision'):
            self.plan()
        self.assertFalse(self.output.exists())

    def test_traversal_and_windows_special_names_rejected(self):
        for name in ['../escape.txt', '/absolute.txt', 'folder/../../escape.txt',
                     'C:/escape.txt', 'photo.png:stream', 'NUL.txt', 'trailing./face.png']:
            with self.subTest(name=name):
                self.first_archive([(name, b'unsafe')])
                with self.assertRaises(intake.IntakeError):
                    self.plan()
        self.assertFalse(self.output.exists())
        self.assertFalse((self.root / 'escape.txt').exists())

    def test_raw_backslash_name_rejected_before_zipinfo_normalizes_it(self):
        # On Windows ZipInfo normalizes separators while creating a fixture,
        # so replace equal-length local/central name bytes after ZIP creation.
        raw = zip_bytes([('folder/escape.txt', b'fixture')])
        self.paths[0].write_bytes(raw.replace(b'folder/escape.txt', b'folder\\escape.txt'))
        with self.assertRaises(intake.IntakeError):
            self.plan()

    def test_symlink_member_rejected(self):
        link = zipfile.ZipInfo('link.jpg')
        link.create_system = 3
        link.external_attr = (stat.S_IFLNK | 0o777) << 16
        self.first_archive([(link, b'../../elsewhere')])
        with self.assertRaisesRegex(intake.IntakeError, 'Symlink'):
            self.plan()

    def test_nested_output_collision_rejected(self):
        self.first_archive([('look.zip.contents', b'not a directory'),
                            ('look.zip', zip_bytes([('face.png', png())]))])
        with self.assertRaisesRegex(intake.IntakeError, 'collision'):
            self.plan()

    def test_existing_output_refuses_overwrite(self):
        plan = self.plan()
        target = self.output / plan['files'][0]['relative_path']
        target.parent.mkdir(parents=True)
        target.write_bytes(b'keep me')
        with self.assertRaisesRegex(intake.IntakeError, 'no overwrite'):
            intake.extract(plan, self.paths, self.guide)
        self.assertEqual(target.read_bytes(), b'keep me')
        self.assertTrue(all(p.exists() for p in self.paths))

    def test_tampered_extracted_image_blocks_every_zip_deletion(self):
        plan = self.plan()
        intake.extract(plan, self.paths, self.guide)
        image = next(x for x in plan['files'] if 'image' in x)
        (self.output / image['relative_path']).write_bytes(b'changed')
        with self.assertRaisesRegex(intake.IntakeError, 'size/hash mismatch'):
            intake.delete_verified_zips(self.plan(), self.inputs)
        self.assertTrue(all(p.exists() for p in self.paths))
        self.assertEqual(len(list(self.output.rglob('*.zip'))), 8)

    def test_cleanup_refuses_outer_archives_outside_declared_scope(self):
        plan = self.plan()
        intake.extract(plan, self.paths, self.guide)
        with self.assertRaisesRegex(intake.IntakeError, 'outside resolved'):
            intake.delete_verified_zips(self.plan())
        self.assertTrue(all(p.exists() for p in self.paths))

    def test_crc_corruption_and_undecodable_image_rejected(self):
        original = zip_bytes([('payload.txt', b'FIXTURE-CRC-MARKER')])
        bad = bytearray(original)
        idx = bad.index(b'FIXTURE-CRC-MARKER')
        bad[idx] ^= 1
        self.paths[0].write_bytes(bad)
        with self.assertRaises(intake.IntakeError):
            self.plan()
        self.first_archive([('broken.png', b'not an image')])
        with self.assertRaisesRegex(intake.IntakeError, 'Image decode failed'):
            self.plan()
        self.assertFalse(self.output.exists())

    def test_expected_names_require_exact_eight(self):
        cfg = self.root / 'names.json'
        cfg.write_text(json.dumps(NAMES[:-1]))
        with self.assertRaisesRegex(intake.IntakeError, 'Exactly eight'):
            intake.expected_config(cfg)
        with self.assertRaises(intake.IntakeError):
            intake.resolve_inputs(NAMES, archives=self.paths[:-1], guide=self.guide)

    def test_explicit_list_preserves_expected_order_and_guide(self):
        paths, guide, input_root = intake.resolve_inputs(NAMES, archives=list(reversed(self.paths)), guide=self.guide)
        self.assertEqual(paths, self.paths)
        self.assertEqual(guide, self.guide)
        self.assertIsNone(input_root)


if __name__ == '__main__':
    unittest.main()
