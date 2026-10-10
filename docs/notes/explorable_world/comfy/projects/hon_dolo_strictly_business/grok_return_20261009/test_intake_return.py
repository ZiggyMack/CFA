"""In-memory security/type checks; no source archives or catalog are changed."""
from io import BytesIO
import stat
import unittest
import zipfile
from PIL import Image

from intake_return import decode_image, safe_members


class IntakeTests(unittest.TestCase):
    def test_safe_nested_names(self):
        safe_members([zipfile.ZipInfo('proofs/front.png'), zipfile.ZipInfo('proofs/back.png')])

    def test_traversal_absolute_and_windows_names_rejected(self):
        for name in ('../file.png', '/absolute.png', 'C:/drive.png', 'a\\b.png',
                     'a//b.png', './file.png', 'file.png ', 'CON.txt', 'a/NUL.png'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                safe_members([zipfile.ZipInfo(name)])

    def test_duplicates_case_collisions_and_prefix_collisions(self):
        for names in (('a.png', 'a.png'), ('A.png', 'a.png'), ('folder', 'folder/image.png')):
            with self.subTest(names=names), self.assertRaises(ValueError):
                safe_members([zipfile.ZipInfo(x) for x in names])

    def test_symlink_and_encrypted_entry_rejected(self):
        symbolic = zipfile.ZipInfo('link.png')
        symbolic.external_attr = (stat.S_IFLNK | 0o777) << 16
        encrypted = zipfile.ZipInfo('encrypted.png')
        encrypted.flag_bits = 1
        for item in (symbolic, encrypted):
            with self.assertRaises(ValueError):
                safe_members([item])

    def test_actual_alpha_and_full_decode(self):
        image = Image.new('RGBA', (7, 5), (12, 20, 30, 255))
        image.putpixel((0, 0), (12, 20, 30, 0))
        output = BytesIO()
        image.save(output, format='PNG')
        result = decode_image(output.getvalue(), 'test.png')
        self.assertEqual((result['width'], result['height']), (7, 5))
        self.assertEqual(result['alpha_extrema'], [0, 255])
        self.assertTrue(result['decoded'])

    def test_corrupt_image_rejected(self):
        with self.assertRaises(Exception):
            decode_image(b'not an image', 'broken.png')


if __name__ == '__main__':
    unittest.main()
