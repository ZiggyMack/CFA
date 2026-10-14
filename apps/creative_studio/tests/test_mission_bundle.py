"""Portable Corner snapshots never mutate the base library or source evidence."""
from copy import deepcopy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from build_mission_control import MissionBundle, build_bundle, sha, safe_https


class MissionBundleTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / 'projects' / 'visual_library' / 'catalog.js'
        self.source.parent.mkdir(parents=True)
        self.out = self.root / 'hosted' / 'library'
        self.out.mkdir(parents=True)
        self.image = self.source.parent / 'source.png'
        Image.new('RGB', (1500, 900), (40, 80, 120)).save(self.image)
        self.original = self.image.read_bytes()
        self.asset = {'id': 'A', 'project': 'hon', 'kind': 'image', 'src': 'source.png',
                      'sha256': sha(self.original), 'title': 'A', 'album': 'hon:outfit', 'category': 'outfits'}
        self.catalog = {'projects': [{'id': 'hon', 'name': 'Hon'}, {'id': 'lisan', 'name': 'Lisan'}],
                        'assets': [deepcopy(self.asset)], 'albums': [{'id': 'hon:outfit', 'project': 'hon',
                            'category': 'outfits', 'title': 'Outfit', 'assetIDs': ['A']}],
                        'missionControl': {'tasks': [{'id': 'task', 'project': 'hon', 'links': [{'label': 'A', 'assetID': 'A'}]}]},
                        'reviewDecisions': [{'id': 'A', 'sha256': self.asset['sha256'], 'status': 'needs_fixes', 'note': 'Gun good, likeness wrong.'}],
                        'reviewRequests': [], 'sourceComparisons': []}

    def run_build(self, **kwargs):
        self.source.write_text('window.CFA_CATALOG = ' + json.dumps(self.catalog) + ';', encoding='utf-8')
        return build_bundle(self.source, self.out, self.root, generated_at='2026-10-14T12:00:00+00:00', **kwargs)

    def test_snapshot_is_deterministic_and_leaves_base_and_sources_alone(self):
        base = b'{"assets": [], "base": "untouched"}'
        (self.out / 'catalog.json').write_bytes(base)
        result = self.run_build()
        first = (self.out / 'mission_control.json').read_bytes()
        self.run_build()
        self.assertEqual(first, (self.out / 'mission_control.json').read_bytes())
        self.assertEqual(base, (self.out / 'catalog.json').read_bytes())
        self.assertEqual(self.original, self.image.read_bytes())
        asset = result['assets'][0]
        self.assertEqual(asset['sha256'], self.asset['sha256'])
        self.assertEqual(result['reviewDecisions'], self.catalog['reviewDecisions'])
        for key, limit in [('src', 1280), ('thumb', 480)]:
            with Image.open(self.out / asset[key]) as image:
                self.assertLessEqual(max(image.size), limit)
            self.assertTrue(asset[key].startswith('mission_media/'))

    def test_registered_hash_mismatch_fails_without_publishing(self):
        self.asset['sha256'] = '0' * 64
        self.catalog['assets'] = [self.asset]
        with self.assertRaisesRegex(RuntimeError, 'Registered source hash changed'):
            self.run_build()
        self.assertFalse((self.out / 'mission_control.json').exists())

    def test_changed_source_keeps_previous_snapshot_and_manifest(self):
        self.run_build()
        before = (self.out / 'mission_control.json').read_bytes()
        manifest_before = (self.out / 'mission_manifest.json').read_bytes()
        builder = MissionBundle(self.source, self.out, self.root)
        original_package = builder.package_asset
        def mutate_source_after_packaging(asset_id):
            result = original_package(asset_id)
            self.source.write_bytes(self.source.read_bytes() + b' ')
            return result
        with patch.object(builder, 'package_asset', side_effect=mutate_source_after_packaging):
            with self.assertRaisesRegex(RuntimeError, 'Source catalog changed'):
                builder.build()
        self.assertEqual(before, (self.out / 'mission_control.json').read_bytes())
        self.assertEqual(manifest_before, (self.out / 'mission_manifest.json').read_bytes())

    def test_saved_review_without_task_link_keeps_media_identity_for_export(self):
        self.catalog['assets'].append({**self.asset, 'id': 'REVIEW-ONLY'})
        self.catalog['reviewDecisions'].append({'id': 'REVIEW-ONLY', 'sha256': self.asset['sha256'],
                                               'status': 'remove', 'note': 'Retain in backup'})
        result = self.run_build()
        self.assertIn('REVIEW-ONLY', {a['id'] for a in result['assets']})
        self.assertEqual(result['reviewDecisions'], self.catalog['reviewDecisions'])

    def test_route_resolves_album_and_cross_project_cast_collection(self):
        self.catalog['castCollections'] = [{'id': 'lisan:james', 'project': 'lisan', 'title': 'James',
                                           'coverID': 'A', 'sharedReferences': [{'assetID': 'A', 'sha256': self.asset['sha256']}]}]
        self.catalog['missionControl']['tasks'][0]['links'] = [
            {'label': 'Outfit', 'href': '../index.html#hon/outfits/hon%3Aoutfit'},
            {'label': 'James', 'href': '#lisan/cast/lisan%3Ajames'},
            {'label': 'Unknown', 'href': '#hon/cast/nonexistent'}]
        result = self.run_build()
        links = result['missionControl']['tasks'][0]['links']
        self.assertEqual(links[0]['assetIDs'], ['A'])
        self.assertEqual(links[1]['assetIDs'], ['A'])
        self.assertEqual(links[1]['albumID'], 'lisan:james')
        self.assertTrue(links[2]['unavailableReason'])
        self.assertFalse(any('href' in link for link in links))

    def test_gun_variants_comparison_and_review_requests_are_all_included(self):
        self.catalog['assets'] = [{**self.asset, 'id': 'G1', 'propState': 'with_gun', 'outfitAlbumID': 'hon:outfit',
                                   'sourceIntake': 'HON-GROK-RETURN-20261009'},
                                  {**self.asset, 'id': 'G2', 'propState': 'with_gun', 'outfitAlbumID': 'hon:outfit',
                                   'sourceIntake': 'HON-GROK-RETURN-20261009'},
                                  {**self.asset, 'id': 'R'}, {**self.asset, 'id': 'C'}]
        self.catalog['missionControl']['tasks'] = [{'id': 'favorites-prop-sweep', 'project': 'hon', 'links': []}]
        self.catalog['reviewRequests'] = [{'id': 'R', 'sha256': self.asset['sha256']}]
        self.catalog['reviewDecisions'] = []
        self.catalog['sourceComparisons'] = [{'id': 'compare', 'items': [{'assetID': 'C'}]}]
        result = self.run_build()
        self.assertEqual(result['missionControl']['tasks'][0]['variantAssetIDs'], ['G1', 'G2'])
        self.assertEqual({a['id'] for a in result['assets']}, {'G1', 'G2', 'R', 'C'})

    def test_documents_are_inert_paths_are_clean_and_zip_is_not_extracted(self):
        document = self.source.parent / 'instructions.py'
        document.write_text('print("do not execute")\nC:\\Users\\Alice\\secret.txt\n', encoding='utf-8')
        archive = self.source.parent / 'care.zip'
        archive.write_bytes(b'this is opaque and must never be extracted')
        self.catalog['missionControl']['tasks'][0]['links'] = [
            {'label': 'Script', 'href': 'instructions.py'}, {'label': 'Care', 'href': 'care.zip'},
            {'label': 'Missing', 'href': 'missing.md'}, {'label': 'Outside', 'href': '../../../outside.txt'},
            {'label': 'Web', 'href': 'https://example.com/safe'}, {'label': 'Unsafe', 'href': 'javascript:alert(1)'}]
        result = self.run_build()
        doc = next(asset for asset in result['assets'] if asset['kind'] == 'document')
        self.assertEqual(doc['kind'], 'document')
        self.assertTrue(doc['inert'])
        self.assertNotIn('C:\\Users', doc['text'])
        self.assertIn('print("do not execute")', doc['text'])
        self.assertTrue(doc['src'].endswith('.txt'))
        links = result['missionControl']['tasks'][0]['links']
        self.assertEqual((self.out / links[1]['downloadPath']).read_bytes(), archive.read_bytes())
        self.assertTrue(all(links[i].get('unavailableReason') for i in (2, 3, 5)))
        self.assertEqual(links[4]['href'], 'https://example.com/safe')

    def seed_reuse(self, corrupt=False, wrong_identity=False):
        relative = 'images/old.jpg'
        target = self.out / relative
        target.parent.mkdir()
        Image.new('RGB', (300, 200), (40, 80, 120)).save(target)
        raw = target.read_bytes()
        (self.out / 'catalog.json').write_text(json.dumps({'assets': [{**self.asset, 'src': relative,
            'sha256': '0' * 64 if wrong_identity else self.asset['sha256']}]}), encoding='utf-8')
        (self.out / 'manifest.json').write_text(json.dumps({'outputs': [{'path': relative, 'bytes': len(raw),
            'sha256': sha(raw), 'source_sha256': self.asset['sha256']}]}), encoding='utf-8')
        if corrupt:
            target.write_bytes(b'corrupt')

    def test_reuses_only_hash_verified_existing_identity(self):
        self.seed_reuse()
        result = self.run_build()
        self.assertEqual(result['assets'][0]['src'], 'images/old.jpg')

    def test_corrupt_cached_file_is_not_reused(self):
        self.seed_reuse(corrupt=True)
        result = self.run_build()
        self.assertTrue(result['assets'][0]['src'].startswith('mission_media/'))
        self.assertEqual((self.out / 'images/old.jpg').read_bytes(), b'corrupt')

    def test_wrong_original_identity_is_not_reused(self):
        self.seed_reuse(wrong_identity=True)
        result = self.run_build()
        self.assertTrue(result['assets'][0]['src'].startswith('mission_media/'))

    def test_oversized_source_is_explicitly_unavailable(self):
        result = self.run_build(max_file_bytes=100)
        self.assertIn('size limit', result['assets'][0]['unavailableReason'])
        self.assertNotIn('src', result['assets'][0])
        self.assertIn('unavailableReason', result['missionControl']['tasks'][0]['links'][0])

    def test_rejects_unsafe_external_urls(self):
        for value in ('javascript:alert(1)', 'file:///D:/file.txt', '//example.com', 'http://example.com',
                      'https://user:pass@example.com', 'https://example.com\n'):
            self.assertFalse(safe_https(value))
        self.assertTrue(safe_https('https://example.com/path?q=1'))


if __name__ == '__main__':
    unittest.main()
