"""Full native design snapshots preserve scope, identity, safe documents and files."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build_design_library import DesignBundle, build_bundle, overlay_plan_clears, sha
from collaborator_review_fixture import records as collaborator_records, backups as collaborator_backups


class DesignBundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'projects/visual_library/catalog.js'
        self.source.parent.mkdir(parents=True)
        self.out = self.root / 'app/library'
        self.out.mkdir(parents=True)
        image = self.source.parent / 'source.png'
        Image.new('RGB', (1600, 900), (20, 40, 90)).save(image)
        self.source_image = image.read_bytes()
        self.asset = {'id': 'A', 'project': 'hon', 'kind': 'image', 'src': 'source.png',
                      'sha256': sha(self.source_image), 'category': 'details', 'title': 'Artwork'}
        self.catalog = {'assets': [deepcopy(self.asset)], 'projects': [{'id': 'hon', 'name': 'Dolo'}],
                        'categories': [['details', 'Details']],
                        'albums': [{'id': 'hon:art', 'project': 'hon', 'category': 'details', 'assetIDs': ['A']}],
                        'missionControl': {'tasks': [{'id': 'task', 'project': 'hon', 'links': []}]},
                        'reviewDecisions': [{'id': 'A', 'sha256': self.asset['sha256'], 'status': 'keep',
                                             'note': 'Preserved note', 'updatedAt': '2026-10-12T10:00:00Z',
                                             'shotPlan': {'prompt': 'Prior plan'}}],
                        'characterBOM': {'characters': [{'id': 'hon:bom', 'coverAssetID': 'A'}]},
                        'castCollections': [{'id': 'hon:cast', 'project': 'hon', 'assetIDs': ['A']}],
                        'sharedReferenceCollections': [{'id': 'hon:shared', 'assetIDs': ['A']}],
                        'detailDisplayGroups': [{'id': 'hon:art', 'assetIDs': ['A']}],
                        'mouthCoverage': {'items': [{'assetID': 'A', 'sha256': self.asset['sha256']}]},
                        'storyboardStories': [{'id': 'story', 'documentIDs': []}],
                        'assetAliases': {'oldA': 'A'}, 'futureConfig': {'retained': True}}

    def write_source(self):
        self.source.write_text('window.REVIEW_CATALOG = ' + json.dumps(self.catalog) + ';', encoding='utf-8')

    def run_build(self, **kwargs):
        self.write_source()
        return build_bundle(self.source, self.out, self.root, generated_at='2026-10-14T12:00:00Z', **kwargs)

    def test_complete_catalog_preserves_every_config_and_all_assets(self):
        self.catalog['assets'].append({**self.asset, 'id': 'B', 'archived': True})
        base = b'{"assets":[],"obsolete":true}'
        (self.out / 'catalog.json').write_bytes(base)
        before = deepcopy(self.catalog)
        result = self.run_build()
        self.assertEqual({a['id'] for a in result['assets']}, {'A', 'B'})
        for key in before.keys() - {'assets'}:
            self.assertEqual(result[key], before[key])
        self.assertEqual(base, (self.out / 'catalog.json').read_bytes())
        self.assertEqual(self.source_image, (self.source.parent / 'source.png').read_bytes())
        self.assertEqual(self.catalog, before)
        for asset in result['assets']:
            self.assertEqual(asset['sha256'], self.asset['sha256'])
            for key, edge in [('src', 1280), ('thumb', 480)]:
                with Image.open(self.out / asset[key]) as image:
                    self.assertLessEqual(max(image.size), edge)

    def test_immutable_take_snapshots_and_backups_bypass_link_cleaning(self):
        frozen = {'format': 'cfa-storyboard-takes-v1', 'takes': [{'id': 'same-immutable-id',
                  'snapshot': {'href': '../original.png', 'sourceURL': str(self.root/'source.txt'),
                               'src': 'D:/Documents/CFA/original.png'}}]}
        self.catalog['storyboardTakes'] = deepcopy(frozen)
        self.catalog['storyboardTakeBackups'] = [{'data': {'href': '../unread.json'}}]
        result = self.run_build()
        self.assertEqual(result['storyboardTakes'], frozen)
        self.assertEqual(result['storyboardTakeBackups'], self.catalog['storyboardTakeBackups'])

    def seed_cache(self, catalog_name='mission_control.json', corrupt=False):
        relative = 'mission_media/cached.jpg'
        target = self.out / relative
        target.parent.mkdir()
        Image.new('RGB', (300, 180), (20, 40, 90)).save(target)
        raw = target.read_bytes()
        cached = {'assets': [{**self.asset, 'id': 'renamed', 'src': relative}]}
        data = json.dumps(cached).encode()
        (self.out / catalog_name).write_bytes(data)
        manifest_name = 'mission_manifest.json' if catalog_name == 'mission_control.json' else 'manifest.json'
        (self.out / manifest_name).write_text(json.dumps({'snapshotSHA256': sha(data), 'outputs': [
            {'path': relative, 'bytes': len(raw), 'sha256': sha(raw), 'source_sha256': self.asset['sha256']}]}))
        if corrupt:
            target.write_bytes(b'broken cache')
        return relative

    def test_collaborator_answers_and_frozen_replies_bypass_path_cleaning(self):
        self.catalog['collaboratorReviews'] = collaborator_records()
        self.catalog['collaboratorReviewBackups'] = collaborator_backups()
        before = deepcopy(self.catalog['collaboratorReviews'])
        result = self.run_build()
        self.assertEqual(result['collaboratorReviews'], before)
        self.assertEqual(result['collaboratorReviewBackups'], collaborator_backups())

    def test_reuses_verified_media_by_hash_even_when_id_changed(self):
        relative = self.seed_cache()
        result = self.run_build()
        self.assertEqual(result['assets'][0]['src'], relative)
        manifest = json.loads((self.out / 'design_manifest.json').read_text())
        self.assertTrue(next(r for r in manifest['outputs'] if r['path'] == relative)['reused'])
        self.assertIn(relative, manifest['publicationFiles'])

    def test_supplements_package_registered_previews_and_evidence(self):
        evidence = self.source.parent / 'receipt.txt'
        evidence.write_text('Scoped pass; acceptance remains separate.', encoding='utf-8')
        self.catalog['reviewSupplements'] = [{
            'id': 'winners', 'indexURL': 'supplier.html', 'receiptURL': 'receipt.txt',
            'items': [{'id': 'known', 'sha256': self.asset['sha256'],
                       'fullImageURL': 'source.png', 'thumbURL': 'source.png'},
                      {'id': 'preview', 'thumbURL': 'source.png',
                       'thumbnailSHA256': self.asset['sha256'], 'fullImageURL': None,
                       'sourceLinks': [{'url': 'receipt.txt', 'sha256': sha(evidence.read_bytes())}]}]}]
        result = self.run_build()
        supplement = result['reviewSupplements'][0]
        self.assertIsNone(supplement['indexURL'])
        self.assertEqual(supplement['items'][0]['fullImageURL'], result['assets'][0]['src'])
        self.assertIsNone(supplement['items'][1]['fullImageURL'])
        self.assertTrue((self.out / supplement['items'][1]['thumbURL']).is_file())
        self.assertEqual((self.out / supplement['receiptURL']).read_text(), evidence.read_text())
        self.assertEqual(supplement['items'][1]['sourceLinks'][0]['url'], supplement['receiptURL'])

    def test_supplement_hash_mismatch_never_publishes_wrong_evidence(self):
        (self.source.parent / 'receipt.txt').write_text('changed', encoding='utf-8')
        self.catalog['reviewSupplements'] = [{'items': [{'sourceLinks': [
            {'url': 'receipt.txt', 'sha256': '0' * 64}]}]}]
        with self.assertRaisesRegex(RuntimeError, 'Registered source hash changed'):
            self.run_build()
        self.assertFalse((self.out / 'design_catalog.json').exists())

    def test_bad_cached_bytes_are_not_reused_or_overwritten(self):
        relative = self.seed_cache(corrupt=True)
        result = self.run_build()
        self.assertTrue(result['assets'][0]['src'].startswith('design_media/'))
        self.assertEqual((self.out / relative).read_bytes(), b'broken cache')

    def test_safe_writer_copy_is_read_instead_of_id_or_stale_preview(self):
        private = self.root / 'writer/DECISIONS.md'
        private.parent.mkdir()
        private.write_text('PRIVATE SENTINEL', encoding='utf-8')
        safe = self.root / 'public/DECISIONS.md'
        safe.parent.mkdir()
        safe.write_text('Site excerpt. Public text only.', encoding='utf-8')
        digest = sha(safe.read_bytes())
        self.catalog['assets'].append({'id': 'hon:doc:writer/DECISIONS.md', 'kind': 'document', 'project': 'hon',
                                      'src': '../../public/DECISIONS.md', 'sha256': digest,
                                      'text': 'STALE PRIVATE PREVIEW', 'title': 'Decisions'})
        registry = {'documents': [{'path': 'writer/DECISIONS.md', 'publication': {'path': 'public/DECISIONS.md',
                     'sha256': digest, 'bytes': safe.stat().st_size}}], 'excludedSources': []}
        (self.source.parent / 'writer_development.json').write_text(json.dumps(registry))
        result = self.run_build()
        doc = result['assets'][1]
        self.assertEqual(doc['sha256'], digest)
        self.assertIn('Public text only', doc['text'])
        for filename in ['design_catalog.json', 'design_manifest.json']:
            text = (self.out / filename).read_text(encoding='utf-8')
            self.assertNotIn('PRIVATE SENTINEL', text)
            self.assertNotIn('STALE PRIVATE PREVIEW', text)
        self.assertEqual(private.read_text(), 'PRIVATE SENTINEL')
        self.catalog['assets'][1]['src'] = '../../writer/DECISIONS.md'
        with self.assertRaisesRegex(RuntimeError, 'Writer-only original'):
            self.run_build()

    def test_explicit_large_document_preview_keeps_complete_packaged_source(self):
        complete = ('A complete screenplay coverage line.\n' * 40000).encode('utf-8')
        source = self.source.parent / 'coverage.md'
        source.write_bytes(complete)
        preview = '165 Preliminary coverage shots. Open the complete source.\n' + str(self.root / 'coverage.md')
        self.catalog['assets'].extend([
            {'id': 'preview', 'kind': 'document', 'project': 'hon', 'src': source.name,
             'sha256': sha(complete), 'filename': source.name, 'text': preview, 'textPreviewOnly': True},
            {'id': 'ordinary', 'kind': 'document', 'project': 'hon', 'src': source.name,
             'sha256': sha(complete), 'text': 'Old catalog preview', 'textPreviewOnly': False}])
        result = self.run_build()
        short, ordinary = result['assets'][1:]
        self.assertTrue(short['textPreviewOnly'])
        self.assertTrue(short['inert'])
        self.assertLess(len(short['text']), 200)
        self.assertNotIn(str(self.root), short['text'])
        self.assertEqual((self.out / short['src']).read_bytes(), complete)
        self.assertEqual(short['sha256'], sha(complete))
        self.assertEqual(source.read_bytes(), complete)
        self.assertEqual(ordinary['text'], complete.decode('utf-8'))
        self.assertEqual(ordinary['src'], short['src'])
        outputs = json.loads((self.out / 'design_manifest.json').read_text())['outputs']
        record = next(row for row in outputs if row['path'] == short['src'])
        self.assertEqual(record['sha256'], sha(complete))
        self.assertEqual(record['source_sha256'], sha(complete))
        self.assertEqual(record['bytes'], len(complete))

    def test_unknown_document_link_is_not_copied_from_disk(self):
        unregistered = self.source.parent / 'unregistered.md'
        unregistered.write_text('Not an approved publication source')
        self.catalog['missionControl']['tasks'][0]['links'] = [
            {'label': 'Unknown', 'href': 'unregistered.md'},
            {'label': 'Artwork', 'href': '#hon/details/hon%3Aart'},
            {'label': 'External', 'href': 'https://example.com/safe'}]
        result = self.run_build()
        links = result['missionControl']['tasks'][0]['links']
        self.assertIn('unavailableReason', links[0])
        self.assertNotIn('href', links[0])
        self.assertEqual(links[1]['assetIDs'], ['A'])
        self.assertEqual(links[1]['route'], '#hon/details/hon%3Aart')
        self.assertEqual(links[2]['href'], 'https://example.com/safe')
        self.assertEqual(len(result['assets']), 1)

    def test_plan_clear_requires_newer_exact_hash_and_preserves_other_fields(self):
        before = deepcopy(self.catalog['reviewDecisions'][0])
        export = {'format': 'cfa-visual-review-v1', 'exported': '2026-10-14T10:00:00Z', 'items': [
            {'id': 'A', 'sha256': self.asset['sha256'], 'updatedAt': '2026-10-13T10:00:00Z',
             'shotPlan': None, 'status': 'remove', 'note': 'Must not import unrelated edits'}]}
        receipt = overlay_plan_clears(self.catalog, export, 'e' * 64)
        self.assertEqual(len(receipt['applied']), 1)
        after = self.catalog['reviewDecisions'][0]
        self.assertIsNone(after['shotPlan'])
        for key in ['status', 'note', 'updatedAt']:
            self.assertEqual(after[key], before[key])
        for change in [{'sha256': '0' * 64}, {'updatedAt': '2026-10-11T10:00:00Z'}, {'updatedAt': None}]:
            self.catalog['reviewDecisions'][0] = deepcopy(before)
            incoming = deepcopy(export)
            incoming['items'][0].update(change)
            rejected = overlay_plan_clears(self.catalog, incoming, 'e' * 64)
            self.assertFalse(rejected['applied'])
            self.assertEqual(self.catalog['reviewDecisions'][0], before)

    def test_export_hash_and_frozen_catalog_hash_are_mandatory_when_supplied(self):
        review = self.root / 'review.json'
        review.write_text('{}')
        with self.assertRaisesRegex(RuntimeError, 'export hash'):
            self.run_build(review_export=review, expected_review_sha='0' * 64)
        with self.assertRaisesRegex(RuntimeError, 'Frozen source catalog'):
            self.run_build(expected_source_sha='0' * 64)

    def test_review_bundle_carries_collaborator_records_in_both_overlay_modes(self):
        reviews = collaborator_records()
        payload = {'format': 'cfa-visual-review-v1', 'items': [], 'collaboratorReviews': reviews,
                   'collaboratorReviewBackups': collaborator_backups()}
        review = self.root / 'review.json'
        review.write_text(json.dumps(payload), encoding='utf-8')
        for mode in ['plan_clears', 'latest']:
            with self.subTest(mode=mode):
                result = self.run_build(review_export=review, expected_review_sha=sha(review.read_bytes()), review_mode=mode)
                self.assertEqual(result['collaboratorReviews'], reviews)
                self.assertEqual(result['collaboratorReviewBackups'], collaborator_backups())
                self.assertEqual(result['reviewDecisions'], self.catalog['reviewDecisions'])

    def test_allowlist_covers_every_asset_path_and_all_output_hashes(self):
        result = self.run_build()
        manifest = json.loads((self.out / 'design_manifest.json').read_text(encoding='utf-8'))
        records = {r['path']: r for r in manifest['outputs']}
        self.assertEqual(set(manifest['publicationFiles']), set(records) | {'design_manifest.json'})
        for asset in result['assets']:
            for key in ('src', 'thumb'):
                self.assertIn(asset[key], records)
        for relative, record in records.items():
            raw = (self.out / relative).read_bytes()
            self.assertEqual(sha(raw), record['sha256'])
            self.assertEqual(len(raw), record['bytes'])

    def test_changed_catalog_preserves_previous_usable_snapshot(self):
        self.run_build()
        before = {name: (self.out / name).read_bytes() for name in ['design_catalog.json', 'design_manifest.json']}
        builder = DesignBundle(self.source, self.out, self.root)
        original = builder.package_asset
        def changed(asset_id):
            item = original(asset_id)
            self.source.write_bytes(self.source.read_bytes() + b' ')
            return item
        with patch.object(builder, 'package_asset', side_effect=changed):
            with self.assertRaisesRegex(RuntimeError, 'catalog changed'):
                builder.build()
        for name, raw in before.items():
            self.assertEqual(raw, (self.out / name).read_bytes())

    def test_registered_hash_drift_fails_without_snapshot(self):
        self.catalog['assets'][0]['sha256'] = '0' * 64
        with self.assertRaisesRegex(RuntimeError, 'Registered source hash changed'):
            self.run_build()
        self.assertFalse((self.out / 'design_catalog.json').exists())

    def test_existing_svg_map_is_preserved_and_supported_by_native_image(self):
        raw = b'<svg xmlns="http://www.w3.org/2000/svg" width="900" height="680"><rect width="900" height="680" fill="#112233"/><circle cx="400" cy="300" r="90" fill="#ffaa55"/></svg>'
        (self.source.parent / 'map.svg').write_bytes(raw)
        self.catalog['assets'] = [{**self.asset, 'id': 'MAP', 'src': 'map.svg', 'sha256': sha(raw),
                                  'referenceRole': 'Location guide only', 'accepted': False}]
        result = self.run_build()
        mapped = result['assets'][0]
        self.assertNotIn('unavailableReason', mapped)
        self.assertEqual(mapped['sha256'], sha(raw))
        self.assertEqual(mapped['referenceRole'], 'Location guide only')
        self.assertFalse(mapped['accepted'])
        self.assertEqual(mapped['src'], mapped['thumb'])
        self.assertTrue(mapped['src'].endswith('.svg'))
        self.assertEqual((self.out / mapped['src']).read_bytes(), raw)
        from streamlit.testing.v1 import AppTest
        from streamlit.runtime.pages_manager import PagesManager
        inherited_pages_state = PagesManager.uses_pages_directory
        # Page discovery is process-wide. An earlier real-app test may enable
        # multipage mode, while this small generated fixture has no pages directory.
        with patch.object(PagesManager, 'uses_pages_directory', None):
            app = AppTest.from_string('import streamlit as st\nst.image(' + repr(str(self.out / mapped['src'])) + ')').run(timeout=15)
            self.assertFalse(app.exception)
            self.assertEqual(len(app.get('imgs')), 1)
        self.assertIs(PagesManager.uses_pages_directory, inherited_pages_state)
        for external in [b'<svg xmlns="http://www.w3.org/2000/svg"><image href="https://example.com/remote.png"/></svg>',
                         b'<?xml version="1.0"?><!DOCTYPE svg [<!ENTITY x "secret">]><svg/>']:
            with self.assertRaises(ValueError):
                DesignBundle.validate_svg(external)


if __name__ == '__main__':
    unittest.main()
