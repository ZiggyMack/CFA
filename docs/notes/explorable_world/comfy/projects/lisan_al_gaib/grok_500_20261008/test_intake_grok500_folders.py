"""Tiny synthetic 50-look fixtures; no production inputs modified."""
import csv
import io
from pathlib import Path
import shutil
import tempfile
import unittest
import zipfile

from PIL import Image

import intake_grok500 as core
import intake_grok500_folders as intake


def jpg():
    out = io.BytesIO()
    Image.new('RGB', (8, 8), (36, 78, 90)).save(out, 'JPEG')
    return out.getvalue()


class FolderIntakeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='grok500-folder-test-')
        self.root = Path(self.temp.name).resolve()
        self.inputs = self.root / 'inputs'
        self.output = self.root / 'received'
        self.inputs.mkdir()
        for name in intake.PARTS:
            (self.inputs / name).mkdir()
        self.guide = self.inputs / intake.GUIDE
        self.guide.write_text('Synthetic provider guide only.', encoding='utf-8')
        self.part1 = self.inputs / intake.PARTS[0]
        (self.part1 / intake.GUIDE).write_bytes(self.guide.read_bytes())
        (self.part1 / 'CONTACT-INDEX.jpg').write_bytes(jpg())
        (self.part1 / 'QA.txt').write_text('Synthetic reported QA, not acceptance.', encoding='utf-8')
        self.rows, self.zips = [], []
        for look in range(1, 51):
            slug = f'LAG-L{look:02}-fixture'
            part = self.inputs / intake.PARTS[(look - 1) % 8]
            zp = part / (slug + '.zip')
            self.zips.append(zp)
            with zipfile.ZipFile(zp, 'w', compression=zipfile.ZIP_STORED) as z:
                for shot in [f'{p}{i}' for p in ('V', 'S') for i in range(1, 6)]:
                    name = f'{slug}__{shot}.jpg'
                    z.writestr(f'{slug}/{name}', jpg())
                    self.rows.append({'row': str(len(self.rows) + 1), 'look_num': f'L{look:02}',
                                      'look_slug': slug, 'shot': shot, 'filename': name,
                                      'zip_name': zp.name, 'qa_status': 'OK-note',
                                      'qa_note': 'fixture', 'hero': 'N', 'breather': 'N', 'arm_worm': 'N'})
                z.writestr(f'{slug}/CONTACT-{slug}.jpg', jpg())
        self.legend = self.part1 / intake.LEGEND
        self.write_rows(self.rows)

    def tearDown(self):
        # Python's ordinary tempfile cleanup also hits Windows' legacy limit.
        # Delete only this resolved, uniquely named synthetic fixture root.
        temp_root = Path(tempfile.gettempdir()).resolve()
        self.assertTrue(self.root.is_relative_to(temp_root))
        self.assertTrue(self.root.name.startswith('grok500-folder-test-'))
        if intake.io_path(self.root).exists():
            shutil.rmtree(intake.io_path(self.root))
        self.temp.cleanup()

    def write_rows(self, rows):
        with self.legend.open('w', encoding='utf-8', newline='') as f:
            w = csv.DictWriter(f, fieldnames=list(self.rows[0]))
            w.writeheader()
            w.writerows(rows)

    def plan(self):
        return intake.inspect_folders(self.inputs, self.output)

    def test_inspection_is_no_write_and_reconciles_exact_roles(self):
        plan = self.plan()
        self.assertFalse(self.output.exists())
        self.assertEqual(plan['summary']['total_image_files'], 551)
        self.assertEqual(len(plan['archives']), 50)
        self.assertTrue(all(a['crc_verified'] for a in plan['archives']))
        self.assertTrue(all(a['outer_archive_crc_verified'] is None for a in plan['outer_folders']))
        self.assertEqual(plan['csv_reconciliation']['source_count'], 500)
        self.assertEqual(plan['csv_reconciliation']['contact_count'], 50)
        self.assertEqual(plan['csv_reconciliation']['index_count'], 1)
        self.assertFalse(plan['cleanup']['allowed_by_this_wrapper'])

    def test_extract_preserves_bytes_and_creates_no_zip_copies(self):
        plan = self.plan()
        originals = {p: core.file_hash(p) for p in self.zips + [self.guide, self.legend]}
        intake.extract_folders(plan)
        self.assertEqual(core.verify_extracted(plan), 555)
        self.assertEqual(plan['verified_extracted_files'], 555)
        self.assertTrue((self.output / 'intake_receipt.json').is_file())
        self.assertFalse(list(self.output.rglob('*.zip')))
        self.assertEqual(originals, {p: core.file_hash(p) for p in originals})
        self.assertFalse(plan['original_inputs_deleted'])
        self.assertTrue(plan['cleanup']['verification_gate_complete'])

    def test_missing_part_blocks(self):
        source = self.inputs / intake.PARTS[-1]
        target = self.inputs / 'missing-part-fixture'
        self.assertTrue(source.resolve().is_relative_to(self.root))
        self.assertTrue(target.resolve().is_relative_to(self.root))
        source.rename(target)
        with self.assertRaisesRegex(core.IntakeError, 'Missing expected outer folder'):
            self.plan()
        self.assertFalse(self.output.exists())

    def test_traversal_in_nested_zip_rejected(self):
        with zipfile.ZipFile(self.zips[0], 'a') as z:
            z.writestr('../escape.txt', 'no')
        with self.assertRaises(core.IntakeError):
            self.plan()
        self.assertFalse((self.root / 'escape.txt').exists())

    def test_case_collision_rejected(self):
        with zipfile.ZipFile(self.zips[0], 'a') as z:
            z.writestr(z.namelist()[0].upper(), jpg())
        with self.assertRaisesRegex(core.IntakeError, 'collision'):
            self.plan()

    def test_corrupt_crc_rejected(self):
        data = bytearray(self.zips[0].read_bytes())
        at = data.index(jpg()) + 25
        data[at] ^= 1
        self.zips[0].write_bytes(data)
        with self.assertRaisesRegex(core.IntakeError, 'CRC'):
            self.plan()

    def test_invalid_image_with_valid_crc_rejected(self):
        with zipfile.ZipFile(self.zips[0]) as z:
            records = [(n, z.read(n)) for n in z.namelist()]
        with zipfile.ZipFile(self.zips[0], 'w') as z:
            for i, (name, data) in enumerate(records):
                z.writestr(name, b'not an image' if i == 0 else data)
        with self.assertRaisesRegex(core.IntakeError, 'Image decode'):
            self.plan()

    def test_wrong_csv_count_or_member_blocks(self):
        self.write_rows(self.rows[:-1])
        with self.assertRaisesRegex(core.IntakeError, '500 rows'):
            self.plan()
        self.rows[0]['filename'] = 'missing-original.jpg'
        self.write_rows(self.rows)
        with self.assertRaisesRegex(core.IntakeError, 'CSV image missing'):
            self.plan()

    def test_existing_output_refuses_overwrite(self):
        plan = self.plan()
        target = self.output / plan['files'][0]['relative_path']
        target.parent.mkdir(parents=True)
        target.write_bytes(b'existing original')
        with self.assertRaisesRegex(core.IntakeError, 'no overwrite'):
            intake.extract_folders(plan)
        self.assertEqual(target.read_bytes(), b'existing original')

    def test_changed_inputs_block_before_output(self):
        plan = self.plan()
        (self.part1 / 'QA.txt').write_text('changed after inspect', encoding='utf-8')
        with self.assertRaisesRegex(core.IntakeError, 'Input changed after inspection'):
            intake.extract_folders(plan)
        self.assertFalse(self.output.exists())

    def test_overlapping_roots_and_guide_mismatch_rejected(self):
        with self.assertRaisesRegex(core.IntakeError, 'disjoint'):
            intake.inspect_folders(self.inputs, self.inputs / 'output')
        self.guide.write_text('different version', encoding='utf-8')
        with self.assertRaisesRegex(core.IntakeError, 'guide differ'):
            self.plan()

    def test_extra_image_rejected(self):
        (self.part1 / 'unlisted.jpg').write_bytes(jpg())
        with self.assertRaisesRegex(core.IntakeError, 'Unexpected image'):
            self.plan()

    def test_resume_only_matching_partial_files(self):
        plan = self.plan()
        first = plan['files'][0]
        target = intake.output_path(self.output, first['relative_path'])
        target.parent.mkdir(parents=True)
        target.write_bytes(jpg())
        intake.extract_folders(plan, resume_verified=True)
        self.assertEqual(plan['resumed_verified_partial_files'], 1)
        self.assertEqual(intake.verify_folder_extracted(plan), 555)

    def test_resume_rejects_changed_and_extra_partial_files(self):
        plan = self.plan()
        first = plan['files'][0]
        target = intake.output_path(self.output, first['relative_path'])
        target.parent.mkdir(parents=True)
        target.write_bytes(b'changed')
        with self.assertRaisesRegex(core.IntakeError, 'Partial output changed'):
            intake.extract_folders(plan, resume_verified=True)
        target.write_bytes(jpg())
        extra = self.output / 'unlisted.txt'
        extra.write_text('preserve me', encoding='utf-8')
        with self.assertRaisesRegex(core.IntakeError, 'Unexpected partial file'):
            intake.extract_folders(plan, resume_verified=True)
        self.assertEqual(extra.read_text(encoding='utf-8'), 'preserve me')

    def test_extended_path_io_preserves_long_names(self):
        rel = 'long-' + 'a' * 200 + '/exact-original-name.jpg'
        p = intake.output_path(self.output, rel)
        p.parent.mkdir(parents=True)
        p.write_bytes(jpg())
        plan = {'intake_root': str(self.output), 'files': [{'relative_path': rel,
                'bytes': len(jpg()), 'sha256': core.digest(jpg()),
                'image': core.decode_image(jpg(), 'test.jpg')}],
                'directories': [rel.rsplit('/', 1)[0]]}
        self.assertGreater(len(str(self.output / rel)), 260)
        self.assertEqual(intake.verify_folder_extracted(plan), 1)


if __name__ == '__main__':
    unittest.main()
