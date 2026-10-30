"""Compact document previews never replace the complete download payload."""
import ast
import mimetypes
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest


APP = Path(__file__).resolve().parents[1]


class DocumentDownloadTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'complete.txt'
        self.complete = b'Complete source line.\n' * 60000
        self.source.write_bytes(self.complete)
        self.downloads, self.captions = [], []
        scope = {'LIBRARY_DIR': self.root, 'mimetypes': mimetypes,
                 'media_path': lambda root, path: (root / path) if path and (root / path).is_file() else None,
                 'st': SimpleNamespace(download_button=lambda *a, **kw: self.downloads.append((a, kw)),
                                       caption=self.captions.append)}
        tree = ast.parse((APP / 'app.py').read_text(encoding='utf-8'))
        method = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'document_download')
        exec(compile(ast.Module(body=[method], type_ignores=[]), str(APP / 'app.py'), 'exec'), scope)
        self.download = scope['document_download']

    def test_preview_download_uses_complete_source_bytes(self):
        self.download({'id': 'packet', 'src': self.source.name, 'filename': 'coverage.md',
                       'text': 'Short preview.', 'textPreviewOnly': True})
        args, kwargs = self.downloads[0]
        self.assertEqual(args, ('Download complete document', self.complete))
        self.assertEqual(kwargs['file_name'], 'coverage.md')

    def test_missing_complete_source_does_not_offer_preview_as_complete_document(self):
        self.download({'id': 'missing', 'src': 'missing.txt', 'text': 'Short preview.', 'textPreviewOnly': True})
        self.assertEqual(self.downloads, [])
        self.assertIn('only a preview', self.captions[0])

    def test_ordinary_text_and_original_document_downloads_are_unchanged(self):
        self.download({'id': 'note', 'src': self.source.name, 'text': 'Full ordinary note.'})
        self.assertEqual(self.downloads[-1][0], ('Download text', 'Full ordinary note.'))
        original = self.root / 'original.doc'
        original.write_bytes(b'\xd0\xcf\x11\xe0Original binary document')
        self.download({'id': 'original', 'src': original.name, 'text': '', 'downloadOnly': True})
        self.assertEqual(self.downloads[-1][0], ('Download document', original.read_bytes()))


if __name__ == '__main__':
    unittest.main()
