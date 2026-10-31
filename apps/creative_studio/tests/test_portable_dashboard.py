"""Focused publication/identity tests for the current UI mirror; no network."""
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
import unittest

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP))
from build_portable_dashboard import build
from build_full_dashboard import read_catalog
from collaborator_review_fixture import records as collaborator_records, backups as collaborator_backups


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


class PortableDashboardTest(unittest.TestCase):
    def setUp(self):
        cache = APP.parents[1] / '.cache'
        cache.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix='portable-dashboard-test-', dir=cache)
        self.root = Path(self.temp.name)
        self.source, self.design, self.output = [self.root / x for x in ('visual', 'library', 'bundle')]
        self.source.mkdir()
        self.design.mkdir()
        for name in ('library.js', 'library.css', 'source_foundation.js', 'storyboard_takes.js', 'collaborator_reviews.js'):
            (self.source / name).write_text('/* exact current local UI */', encoding='utf-8')
        (self.source / 'catalog.js').write_bytes(b'window.REVIEW_CATALOG={"current":true};')
        self.source_sha = 'a' * 64
        self.catalog = {
            'projects': [{'id': 'hon', 'title': 'Hon'}], 'categories': [], 'albums': [],
            'assets': [{'id': 'asset-one', 'project': 'hon', 'kind': 'image', 'title': 'One',
                        'src': 'design_media/review.jpg', 'thumb': 'design_media/thumb.jpg', 'sha256': self.source_sha}],
            'reviewDecisions': [{'id': 'asset-one', 'sha256': self.source_sha, 'status': 'keep', 'note': 'Exact user decision', 'source': {'sourceURL': '[local file]'}}],
            'missionControl': {'tasks': [{'links': [
                {'label': 'Intake', 'route': '#hon/intake'},
                {'label': 'This image', 'assetID': 'asset-one'},
                {'label': 'Receipt', 'downloadPath': 'design_media/receipt.txt'},
                {'label': 'Not published', 'href': '../secrets/private.txt'},
            ]}]},
            'reviewSupplements': [{'id': 'winners', 'indexURL': '../supplier/index.html',
                'csvURL': 'design_media/list.csv', 'receiptURL': 'design_media/receipt.txt',
                'items': [{'id': 'pick', 'title': 'Pick <safe>', 'group': 'validated', 'project': 'hon',
                           'exactAssetID': 'asset-one', 'sha256': self.source_sha, 'vVerdict': 'PASS-ADVISORY',
                           'reviewScope': 'Chest only', 'advisories': 'Nose ring is missing',
                           'fullImageURL': '../original.jpg', 'thumbURL': '../original-thumb.jpg'}]}],
        }
        self.media = {'design_media/review.jpg': b'1280px browser copy, not original bytes',
                      'design_media/thumb.jpg': b'480px thumbnail',
                      'design_media/receipt.txt': b'Allowed inert receipt',
                      'design_media/list.csv': b'ID,scope\nasset-one,chest',
                      'design_media/unreferenced.txt': b'Allowed but not needed for this mirror'}
        for relative, raw in self.media.items():
            path = self.design / relative
            path.parent.mkdir(exist_ok=True)
            path.write_bytes(raw)
        (self.design / 'private.txt').write_bytes(b'Not published')
        self.write_manifest()

    def tearDown(self):
        self.temp.cleanup()

    def write_manifest(self):
        raw = json.dumps(self.catalog).encode()
        (self.design / 'design_catalog.json').write_bytes(raw)
        outputs = [{'path': path, 'sha256': sha(data), 'bytes': len(data), 'source_sha256': self.source_sha if path.endswith('.jpg') else sha(data), 'role': 'thumbnail' if path.endswith('thumb.jpg') else 'image_preview' if path.endswith('.jpg') else 'inert_text'} for path, data in self.media.items()]
        outputs.append({'path': 'design_catalog.json', 'sha256': sha(raw), 'bytes': len(raw)})
        self.manifest = {'schema': 'cfa-design-manifest-v1', 'snapshotSHA256': sha(raw),
                         'snapshot': {'sourceCatalog': {'path': 'visual/catalog.js', 'sha256': sha((self.source / 'catalog.js').read_bytes())}},
                         'outputs': outputs, 'sources': [{'path': 'original.jpg', 'sha256': self.source_sha}]}
        self.save_manifest()

    def save_manifest(self):
        (self.design / 'design_manifest.json').write_text(json.dumps(self.manifest), encoding='utf-8')

    def make(self, **kwargs):
        receipt = build(self.design, self.source, self.output, self.root, **kwargs)
        snapshot = self.output / 'snapshots' / receipt['buildID']
        return receipt, snapshot, read_catalog((snapshot / 'catalog.js').read_bytes())

    def test_exact_ui_and_review_identity_with_only_allowlisted_browser_media(self):
        receipt, snapshot, catalog = self.make()
        self.assertEqual(catalog['reviewDecisions'], self.catalog['reviewDecisions'])
        asset = catalog['assets'][0]
        self.assertEqual(asset['sha256'], self.source_sha)
        self.assertTrue(os.path.samefile(snapshot / asset['src'], self.design / 'design_media/review.jpg'))
        self.assertNotEqual(sha((snapshot / asset['src']).read_bytes()), asset['sha256'])
        self.assertEqual((snapshot / 'library.js').read_bytes(), (self.source / 'library.js').read_bytes())
        self.assertEqual((snapshot / 'library.css').read_bytes(), (self.source / 'library.css').read_bytes())
        self.assertEqual((snapshot / 'storyboard_takes.js').read_bytes(), (self.source / 'storyboard_takes.js').read_bytes())
        self.assertEqual((snapshot / 'collaborator_reviews.js').read_bytes(), (self.source / 'collaborator_reviews.js').read_bytes())
        index = (snapshot / 'index.html').read_text()
        self.assertIn("window.REVIEW_INITIAL={project:'hon',view:'all'}", index)
        self.assertIn("if(!location.hash)location.hash='hon/all'", index)
        self.assertLess(index.index('src="storyboard_takes.js"'), index.index('src="library.js"'))
        self.assertLess(index.index('src="collaborator_reviews.js"'), index.index('src="library.js"'))
        self.assertFalse((snapshot / 'library/private.txt').exists())
        self.assertFalse((snapshot / 'library/design_media/unreferenced.txt').exists())
        self.assertEqual(receipt['logicalMediaBytes'], sum(len(v) for k, v in self.media.items() if not k.endswith('unreferenced.txt')))
        self.assertEqual(self.make()[0]['buildID'], receipt['buildID'])
        self.assertIn('current.json', receipt['publicationFiles'])
        self.assertTrue(all((self.output / p).is_file() for p in receipt['publicationFiles']))

    def test_collaborator_answers_and_snapshot_metadata_are_not_navigation(self):
        self.catalog['collaboratorReviews'] = collaborator_records()
        self.catalog['collaboratorReviewBackups'] = collaborator_backups()
        self.write_manifest()
        _, _, catalog = self.make()
        self.assertEqual(catalog['collaboratorReviews'], self.catalog['collaboratorReviews'])
        self.assertEqual(catalog['collaboratorReviewBackups'], collaborator_backups())

    def test_internal_links_and_visual_winners_map_are_usable_and_scoped(self):
        receipt, snapshot, catalog = self.make()
        links = catalog['missionControl']['tasks'][0]['links']
        self.assertEqual(links[0]['href'], '#hon/intake')
        self.assertEqual(links[1]['href'], '#hon/asset/asset-one')
        self.assertEqual(links[2]['href'], 'library/design_media/receipt.txt')
        self.assertNotIn('href', links[3])
        self.assertEqual(len(receipt['unresolvedPreparedLinks']), 1)
        supplement = catalog['reviewSupplements'][0]
        self.assertEqual(supplement['items'][0]['fullImageURL'], 'library/design_media/review.jpg')
        self.assertEqual(supplement['items'][0]['thumbURL'], 'library/design_media/thumb.jpg')
        page = (snapshot / supplement['indexURL']).read_text(encoding='utf-8')
        for text in ('Pick &lt;safe&gt;', 'Chest only', 'PASS-ADVISORY', 'Nose ring is missing', 'index.html#hon/asset/asset-one'):
            self.assertIn(text, page)

    def test_copy_mode_is_independent(self):
        _, snapshot, catalog = self.make(copy_media=True)
        self.assertFalse(os.path.samefile(snapshot / catalog['assets'][0]['src'], self.design / 'design_media/review.jpg'))

    def test_take_snapshots_and_unread_backups_are_never_rewritten(self):
        from copy import deepcopy
        frozen = {'format': 'cfa-storyboard-takes-v1', 'takes': [{'id': 'same-immutable-id',
                  'snapshot': {'sourceURL': '../source.txt', 'href': '../original.jpg',
                               'src': 'D:/Documents/CFA/source.jpg', 'url': 'https://example.com/source'}}]}
        self.catalog['storyboardTakes'] = deepcopy(frozen)
        self.catalog['storyboardTakeBackups'] = [{'data': {'href': '../unread.json'}}]
        self.write_manifest()
        _, _, catalog = self.make()
        self.assertEqual(catalog['storyboardTakes'], frozen)
        self.assertEqual(catalog['storyboardTakeBackups'], self.catalog['storyboardTakeBackups'])

    def test_changed_media_and_stale_catalog_never_replace_current(self):
        self.make()
        before = (self.output / 'current.json').read_bytes()
        path = self.design / 'design_media/review.jpg'
        replacement = path.with_suffix('.tmp')
        replacement.write_bytes(b'modified publication')
        replacement.replace(path)
        with self.assertRaisesRegex(ValueError, 'Publication file changed'):
            self.make()
        self.assertEqual((self.output / 'current.json').read_bytes(), before)
        path.write_bytes(self.media['design_media/review.jpg'])
        (self.source / 'catalog.js').write_bytes(b'new local catalog')
        with self.assertRaisesRegex(ValueError, 'stale'):
            self.make()
        self.assertEqual((self.output / 'current.json').read_bytes(), before)

    def test_path_escape_and_unverified_catalog_fail_closed(self):
        self.manifest['outputs'].append({'path': '../private.txt'})
        self.save_manifest()
        with self.assertRaisesRegex(ValueError, 'Unsafe publication path'):
            self.make()
        self.write_manifest()
        self.manifest['snapshotSHA256'] = '0' * 64
        self.save_manifest()
        with self.assertRaisesRegex(ValueError, 'does not match'):
            self.make()
        self.assertFalse((self.output / 'current.json').exists())


if __name__ == '__main__':
    unittest.main()
