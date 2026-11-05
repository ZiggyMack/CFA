import copy
import json
from pathlib import Path
import tempfile
import unittest

from cfa_review_metadata_intake import DROP, IntakeError
from review_winners_supplement import PACKAGE, apply_winners_supplement, load_winners_supplement

ROOT = Path(__file__).resolve().parents[6]


class WinnersSupplementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw = Path(__file__).with_name('catalog.js').read_text(encoding='utf-8')
        cls.catalog = json.loads(raw.split('=', 1)[1].strip().rstrip(';'))
        cls.supplement = load_winners_supplement(cls.catalog, ROOT)

    def test_status_authority_and_counts(self):
        summary = self.supplement['summary']
        self.assertEqual((summary['items'], summary['approved'], summary['validated'], summary['preliminary']), (52,11,28,13))
        validated = [i for i in self.supplement['items'] if i['group']=='validated']
        self.assertEqual(sum(i['vVerdict']=='PASS-ADVISORY' for i in validated),18)
        self.assertTrue(all(i['advisories'] for i in validated if i['vVerdict']=='PASS-ADVISORY'))
        self.assertTrue(all('awaiting Ziggy' in i['label'] for i in validated))

    def test_originals_and_previews_have_separate_identities(self):
        summary = self.supplement['summary']
        self.assertEqual((summary['localOriginals'],summary['previewOnly'],summary['exactAssetMatches']), (50,2,45))
        previews = [i for i in self.supplement['items'] if i['availability']=='preview_only']
        self.assertEqual({i['sha8'] for i in previews}, {'d68287f1','a906752d'})
        for item in self.supplement['items']:
            self.assertNotEqual(item['sha256'],item['thumbnailSHA256'])
            if item['availability']=='preview_only':
                self.assertIsNone(item['fullImageURL'])
                self.assertIsNone(item['exactAssetID'])

    def test_missing_declared_links_recovered_by_full_hash(self):
        for prefix in ('26a91590','104b30b1'):
            item = next(i for i in self.supplement['items'] if i['sha8']==prefix)
            self.assertTrue(item['fullImageURL'])
            self.assertTrue(item['exactAssetID'])

    def test_verified_lineage_replaces_name_only_family_association(self):
        pilot = next(i for i in self.supplement['items'] if i['sha8']=='d68287f1')
        repair = next(i for i in self.supplement['items'] if i['sha8']=='12453ef4')
        self.assertEqual(pilot['familyLinkBasis'],'exact_version_hash')
        self.assertEqual(repair['familyLinkBasis'],'explicit_lineage_root_hash')
        self.assertEqual(repair['familyIDs'],['GROK-HD-FALCON-1000:C04-battle-light-005'])
        self.assertTrue(repair['exactAssetID'])
        roots = {row['sha256'] for row in repair['lineage'] if row['kind']=='ROOT'}
        self.assertIn(repair['familyLinks'][0]['matchedSHA256'], roots)
        self.assertTrue(all(not row['isImmediateParent'] for item in self.supplement['items'] for row in item['lineage']))

    def test_r003_enrichment_joins_exact_versions_and_preserves_provider_labels(self):
        delivery = self.catalog['winnersMediaIntake']
        self.assertEqual(self.supplement['mediaRevision'], delivery['id'])
        self.assertEqual(self.supplement['indexURL'], delivery['indexURL'])
        self.assertEqual(self.supplement['receiptURL'], delivery['receiptURL'])
        self.assertEqual(self.supplement['mediaDelivery'], {
            'fullImages':41, 'versionMatchedReports':29, 'lineageRows':210,
        })
        records = {record['sha256']:record for record in delivery['records']}
        for item in self.supplement['items']:
            record = records[item['sha256']]
            for field in ('label','group','vVerdict','reviewScope','advisories',
                          'fullImageURL','exactAssetID','availability','familyIDs',
                          'familyLinkBasis','familyLinks','lineage','lineageURL',
                          'lineageNote','reportLinks','supportingEvidence'):
                self.assertEqual(item[field], record[field], (item['sha8'],field))
            for report in item['reportLinks']:
                self.assertIn(report, item['sourceLinks'])
                self.assertEqual(report['targetSHA256'], item['sha256'])
                self.assertTrue(report['versionVerified'])
                self.assertTrue(item['sha256'].startswith(report['matchedHash']))
                self.assertTrue(report['matchedLines'])
            if item['group']=='validated':
                self.assertTrue(item['reportLinks'])
                self.assertEqual(item['sourceReportsStatus'],'full_reports_available')
            if item['group']=='preliminary':
                self.assertEqual(item['reportLinks'],[])
                self.assertEqual(item['vVerdict'],'')
                self.assertEqual(item['sourceReportsStatus'],'no_v_validation_recorded')
        repair = next(i for i in self.supplement['items'] if i['sha8']=='12453ef4')
        self.assertEqual(len(repair['reportLinks']),2)

    def test_only_version_matched_human_acceptance_is_exposed(self):
        catalog = copy.deepcopy(self.catalog)
        passed = [i for i in self.supplement['items'] if i['group']=='validated']
        accepted, stale = passed[:2]
        preliminary = next(i for i in self.supplement['items'] if i['group']=='preliminary')
        acceptance = {'sha256':accepted['sha256'], 'scope':'scene_reference'}
        catalog['reviewDecisions'] = [
            {'id':accepted['exactAssetID'], 'acceptedScope':acceptance},
            {'id':stale['exactAssetID'], 'acceptedScope':{
                'sha256':'f'*64, 'scope':'scene_reference',
            }},
            {'id':preliminary['exactAssetID'], 'status':'keep', 'likenessRating':5},
        ]
        before = copy.deepcopy(catalog)
        result = load_winners_supplement(catalog,ROOT)
        self.assertEqual(catalog,before,'Reading a supplement cannot write site review state')
        for item in result['items']:
            self.assertEqual(item['humanAcceptance'], acceptance if item['sha256']==accepted['sha256'] else None)
            provider = next(i for i in self.supplement['items'] if i['sha256']==item['sha256'])
            self.assertEqual(item['label'],provider['label'])
            self.assertEqual(item['group'],provider['group'])

    def test_inferred_gold_references_remain_inferred(self):
        validated = [i for i in self.supplement['items'] if i['group']=='validated']
        self.assertTrue(all('shape = stencil a906752d panel 1 [INFERRED' in i['goldReferences'] for i in validated))
        self.assertTrue(all(i['referenceLinks'] for i in validated))
        for item in validated:
            self.assertEqual(item['sourceReportsStatus'],'full_reports_available')
            for link in item['referenceLinks']:
                self.assertEqual(link['matchBasis'],'unique_hash_prefix_from_provider')

    def test_additive_idempotent_does_not_change_frozen_intake_or_reviews(self):
        catalog = copy.deepcopy(self.catalog)
        original = copy.deepcopy(catalog)
        apply_winners_supplement(catalog,ROOT)
        apply_winners_supplement(catalog,ROOT)
        self.assertEqual(len([s for s in catalog['reviewSupplements'] if s['id']==PACKAGE]),1)
        for key in original:
            if key!='reviewSupplements':self.assertEqual(catalog[key],original[key],key)

    def test_reject_changed_package_before_loading_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            folder=root/DROP/PACKAGE
            folder.mkdir(parents=True)
            (folder/'WINNERS_index.html').write_text('changed')
            with self.assertRaises(IntakeError):load_winners_supplement(self.catalog,root)


if __name__=='__main__':unittest.main()
