"""Bounded r003 intake: identity, provenance, version joins and no-review writes."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from cfa_review_metadata_intake import DROP, IntakeError
from review_winners_media import (ALBUMS, PACKAGE, PARENT, PINS, _hash_matches,
                                  apply_winners_media, load_winners_media)

ROOT = Path(__file__).resolve().parents[6]


class WinnersMediaTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        text = Path(__file__).with_name('catalog.js').read_text(encoding='utf-8')
        cls.catalog = json.loads(text.split('=', 1)[1].strip().rstrip(';'))
        cls.catalog['assets'] = [a for a in cls.catalog['assets'] if a.get('sourceIntake') != PACKAGE]
        cls.catalog['albums'] = [a for a in cls.catalog['albums'] if a.get('sourceIntake') != PACKAGE]
        cls.catalog.pop('winnersMediaIntake', None)
        cls.loaded = load_winners_media(cls.catalog, ROOT)

    def test_bounded_package_media_counts_and_missing_originals(self):
        summary = self.loaded['summary']
        self.assertEqual((summary['manifestEntriesVerified'], summary['winnerRecords'],
                          summary['deliveredFullImages'], summary['localOriginals'], summary['previewOnly']),
                         (319, 52, 41, 50, 2))
        self.assertEqual({r['sha256'][:8] for r in self.loaded['missingFullOriginals']}, {'d68287f1', 'a906752d'})
        self.assertEqual(len({a['id'] for a in self.loaded['newAssets']}), 41)
        for asset in self.loaded['newAssets']:
            self.assertEqual(hashlib.sha256((ROOT / asset['repoPath']).read_bytes()).hexdigest(), asset['sha256'])
            self.assertEqual(asset['id'], 'HD-WINNERS-' + asset['sha256'][:20])
        for record in self.loaded['records']:
            self.assertNotEqual(record['sha256'], record['thumbnailSHA256'])
            self.assertEqual(bool(record['fullImageURL']), record['availability'] == 'local_original_verified')

    def test_scoped_v_reports_and_preliminary_picks_do_not_approve_images(self):
        passed = [r for r in self.loaded['records'] if r['group'] == 'validated']
        preliminary = [r for r in self.loaded['records'] if r['group'] == 'preliminary']
        self.assertEqual((len(passed), len(preliminary)), (28, 13))
        self.assertEqual(sum(r['vVerdict'] == 'PASS-ADVISORY' for r in passed), 18)
        for record in passed:
            self.assertTrue(record['reviewScope'])
            self.assertTrue(record['reportLinks'])
            self.assertEqual(record['sourceReportsStatus'], 'full_reports_available')
            for link in record['reportLinks']:
                self.assertTrue(link['versionVerified'])
                self.assertTrue(record['sha256'].startswith(link['matchedHash']))
                self.assertEqual(link['targetSHA256'], record['sha256'])
                self.assertTrue(link['matchedLines'])
            if record['vVerdict'] == 'PASS-ADVISORY':
                self.assertTrue(record['advisories'])
        c04005 = next(r for r in passed if r['sha8'] == '12453ef4')
        self.assertEqual(len(c04005['reportLinks']), 2, 'Full-chest and ink-only checks stay attached to v005')
        for record in preliminary:
            self.assertEqual(record['vVerdict'], '')
            self.assertEqual(record['reportLinks'], [])
            self.assertEqual(record['sourceReportsStatus'], 'no_v_validation_recorded')
        for record in self.loaded['records']:
            self.assertIsNone(record['humanAcceptance'])
            self.assertEqual(record['siteValidation'], 'not_performed')
        for asset in self.loaded['newAssets']:
            for key in ('status', 'likenessRating', 'sceneQualityRating', 'validation', 'workingReference', 'componentApprovals'):
                self.assertNotIn(key, asset)
        target = passed[0]['sha256']
        self.assertEqual(_hash_matches(target[:8], target, {target, target[:8] + 'f' * 56}), [], 'Ambiguous short hashes cannot bind a report')

    def test_explicit_root_hashes_link_families_without_inventing_parents(self):
        linked = [r for r in self.loaded['mediaRecords'] if r['familyIDs']]
        self.assertEqual(len(linked), 17)
        record = next(r for r in linked if r['sha8'] == '12453ef4')
        family_id = 'GROK-HD-FALCON-1000:C04-battle-light-005'
        self.assertEqual(record['familyIDs'], [family_id])
        self.assertEqual(record['familyLinkBasis'], 'explicit_lineage_root_hash')
        roots = {r['sha256'] for r in record['lineage'] if r['kind'] == 'ROOT'}
        self.assertIn(record['familyLinks'][0]['matchedSHA256'], roots)
        self.assertTrue(all(not row['isImmediateParent'] for r in self.loaded['records'] for row in r['lineage']))
        inferred = [row for r in self.loaded['records'] for row in r['lineage'] if row['statusBasis'] == 'provider_inferred']
        self.assertTrue(inferred)
        self.assertTrue(all('inferred' in row['sourceEvidence'].lower() for row in inferred))
        candidate = copy.deepcopy(self.catalog)
        family = next(f for f in candidate['reviewIntake']['families'] if f['id'] == family_id)
        family['original']['sha256'] = 'f' * 64
        result = load_winners_media(candidate, ROOT)
        changed = next(r for r in result['records'] if r['sha8'] == '12453ef4')
        self.assertNotIn(family_id, changed['familyIDs'], 'Matching frame name alone does not recreate a family join')

    def test_reuses_verified_existing_identity_and_keeps_album_scope(self):
        candidate = copy.deepcopy(self.catalog)
        reused = copy.deepcopy(self.loaded['newAssets'][0])
        reused['id'] = 'EXISTING-EXACT-WINNER'
        reused['sourceIntake'] = 'older-local-intake'
        reused['note'] = 'Preserve this original catalog note.'
        candidate['assets'].append(reused)
        result = apply_winners_media(candidate, ROOT)
        self.assertEqual(result['summary']['newAssets'], 40)
        self.assertEqual(result['summary']['matchedExistingAssets'], 1)
        record = next(r for r in result['mediaRecords'] if r['sha256'] == reused['sha256'])
        self.assertEqual(record['exactAssetID'], reused['id'])
        self.assertEqual([a for a in candidate['assets'] if a.get('sha256') == reused['sha256']], [reused])
        self.assertEqual({a['category'] for a in self.loaded['newAssets']}, {'working', 'storyboard'})
        for classification, (album_id, category, _) in ALBUMS.items():
            album = next(a for a in candidate['albums'] if a['id'] == album_id)
            expected = [r['exactAssetID'] for r in result['mediaRecords'] if r['classification'] == classification]
            self.assertEqual(album['assetIDs'], expected)
            self.assertEqual(album['category'], category)
            self.assertEqual(album['project'], 'hon')

    def test_idempotent_addition_preserves_reviews_and_frozen_families(self):
        candidate = copy.deepcopy(self.catalog)
        before = copy.deepcopy(candidate)
        apply_winners_media(candidate, ROOT)
        once = copy.deepcopy(candidate)
        apply_winners_media(candidate, ROOT)
        self.assertEqual(candidate, once)
        self.assertEqual(candidate['assets'][:len(before['assets'])], before['assets'])
        self.assertEqual(candidate['albums'][:len(before['albums'])], before['albums'])
        for key in before:
            if key not in ('assets', 'albums', 'winnersMediaIntake'):
                self.assertEqual(candidate[key], before[key], key)
        self.assertEqual(candidate['reviewIntake'], before['reviewIntake'])

    def test_changed_manifest_media_or_carryover_fails_before_mutation(self):
        # Use copied bytes, never hardlinks: tamper tests must not touch the drop.
        with tempfile.TemporaryDirectory(prefix='winners_test_', dir=ROOT.anchor) as directory:
            root = Path(directory)
            folder = root / DROP / PACKAGE
            shutil.copytree(ROOT / DROP / PACKAGE, folder)
            parent = root / DROP / PARENT
            parent.mkdir()
            shutil.copy2(ROOT / DROP / PARENT / 'WINNERS_list.csv', parent / 'WINNERS_list.csv')
            media = next((folder / 'media').iterdir())
            targets = [folder / 'SHA256SUMS.txt', media, parent / 'WINNERS_list.csv']
            for target in targets:
                with self.subTest(target=target.name):
                    saved = target.read_bytes()
                    target.write_bytes(saved + b'\nchanged')
                    candidate = copy.deepcopy(self.catalog)
                    before = copy.deepcopy(candidate)
                    with self.assertRaises(IntakeError):
                        apply_winners_media(candidate, root)
                    self.assertEqual(candidate, before)
                    target.write_bytes(saved)
            self.assertEqual(hashlib.sha256((folder / 'SHA256SUMS.txt').read_bytes()).hexdigest(), PINS['SHA256SUMS.txt'])


if __name__ == '__main__':
    unittest.main()
