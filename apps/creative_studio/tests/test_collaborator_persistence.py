"""Questionnaire evidence survives publication, exports and source rebuilding."""
from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
import unittest

APP = Path(__file__).resolve().parents[1]
ROOT = APP.parents[1]
VISUAL = ROOT / 'docs/notes/explorable_world/comfy/projects/visual_library'
sys.path.insert(0, str(APP))
sys.path.insert(0, str(VISUAL))
from collaborator_review import merge, normalize, empty, edit, prepare, QUESTIONS, TASK_ID
from collaborator_review_fixture import records, backups
from collaborator_review_intake import apply_collaborator_reviews
from library_helpers import review_payload, review_provenance
from review_snapshot import overlay_review_snapshot


class CollaboratorPersistenceTest(unittest.TestCase):
    def newer(self, mapping):
        result = deepcopy(mapping)
        row = result['grok-proof-package']
        row.update(state='draft', readyReplyID=None, updatedAt='2026-10-30T10:00:02Z')
        row['answers']['fixture-question']['note'] = 'Revised draft; frozen reply stays intact.'
        row['answers']['fixture-question']['updatedAt'] = row['updatedAt']
        return result

    def test_export_overlay_and_source_rebuild_keep_newer_draft_and_frozen_reply(self):
        saved = records(); newer = self.newer(saved)
        base = {'assets': [], 'reviewDecisions': [], 'collaboratorReviews': saved, 'futureConfig': {'unchanged': True}}
        original = deepcopy(base)
        payload = {'format': 'cfa-visual-review-v1', 'items': [], 'collaboratorReviews': newer,
                   'collaboratorReviewBackups': backups()}
        result, report = overlay_review_snapshot(base, payload)
        self.assertEqual(result['collaboratorReviews'], newer)
        self.assertEqual(result['collaboratorReviews']['grok-proof-package']['replies'], saved['grok-proof-package']['replies'])
        self.assertEqual(report['changedCollaboratorTasks'], ['grok-proof-package'])
        rebuilt = {'assets': [], 'reviewDecisions': []}
        apply_collaborator_reviews(rebuilt, ROOT, {'collaboratorReviews': saved}, result)
        self.assertEqual(rebuilt['collaboratorReviews'], newer)
        self.assertEqual(rebuilt['collaboratorReviewBackups'], backups())
        self.assertEqual(base, original)
        self.assertEqual(result['futureConfig'], original['futureConfig'])
        provenance = review_provenance(result)
        exported = review_payload([], {}, set(), provenance=provenance)
        self.assertEqual(exported['collaboratorReviews'], newer)
        self.assertEqual(exported['collaboratorReviewBackups'], backups())
        self.assertEqual(review_provenance(exported)['collaboratorReviews'], newer)

    def test_invalid_snapshot_import_and_rebuild_fail_without_mutation(self):
        saved = records(); incoming = self.newer(saved)
        incoming['grok-proof-package']['replies'][0]['answers']['fixture-question']['note'] = 'Forbidden rewrite'
        base = {'assets': [], 'reviewDecisions': [], 'collaboratorReviews': saved}
        before = deepcopy(base)
        with self.assertRaisesRegex(ValueError, 'immutable'):
            overlay_review_snapshot(base, {'format': 'cfa-visual-review-v1', 'items': [], 'collaboratorReviews': incoming})
        with self.assertRaisesRegex(ValueError, 'immutable'):
            apply_collaborator_reviews(base, ROOT, {'collaboratorReviews': incoming}, before)
        self.assertEqual(base, before)

    def test_absence_does_not_invent_answers_or_drop_saved_records(self):
        base = {'assets': [], 'reviewDecisions': []}
        apply_collaborator_reviews(base, ROOT, {}, {})
        self.assertNotIn('collaboratorReviews', base)
        base['collaboratorReviews'] = records()
        result, _ = overlay_review_snapshot(base, {'format': 'cfa-visual-review-v1', 'items': []})
        self.assertEqual(result['collaboratorReviews'], base['collaboratorReviews'])

    def test_browser_helper_matches_native_preservation_and_conflicts(self):
        saved = records(); newer = self.newer(saved)
        cases = [
            [saved, newer], [newer, saved], [saved, saved],
            [saved, {'future-task': {**saved['future-task'], 'readyReplyID': None}}],
        ]
        micro = deepcopy(saved)
        micro['future-task']['updatedAt'] = '2026-10-30T10:00:00.000001Z'
        micro['future-task']['direction']['note'] = 'One microsecond newer'
        cases.append([saved, micro])
        bad = deepcopy(saved); bad['future-task']['direction']['note'] = 'Same-time conflict'
        cases.append([saved, bad])
        bad = deepcopy(saved); bad['grok-proof-package']['replies'][0]['futureEvidence']['href'] = '../changed.json'
        cases.append([saved, bad])
        known = empty('2026-10-30T10:00:00Z')
        assets = [{'id': q['assetID'], 'sha256': q['sha256'], 'kind': 'image'} for q in QUESTIONS]
        for question in QUESTIONS:
            known = edit(known, question_id=question['id'], choice='meets_brief', note='Synthetic test only', now='2026-10-30T10:00:01Z')
        known = edit(known, direction={'choice': 'bounded_corrections', 'note': 'Synthetic test only'}, now='2026-10-30T10:00:02Z')
        known = prepare(known, assets, now='2026-10-30T10:00:03Z', reply_id='synthetic-known-reply')
        cases.append([{TASK_ID: known}])
        missing_evidence = deepcopy(known); missing_evidence['replies'][0].pop('evidence')
        cases.append([{TASK_ID: missing_evidence}])
        wrong_question = deepcopy(known); wrong_question['replies'][0]['questions'][0]['request'] = 'Changed request'
        cases.append([{TASK_ID: wrong_question}])
        incomplete = deepcopy(known)
        incomplete['answers'][QUESTIONS[0]['id']]['choice'] = ''
        incomplete['replies'][0]['answers'] = deepcopy(incomplete['answers'])
        cases.append([{TASK_ID: incomplete}])
        expectations = []
        for values in cases:
            try:
                expected = {'ok': True, 'value': merge(*values)}
            except ValueError:
                expected = {'ok': False}
            expectations.append(expected)
        script = "const fs=require('node:fs'),helper=require(process.argv[1]);const cases=JSON.parse(fs.readFileSync(0,'utf8'));process.stdout.write(JSON.stringify(cases.map(data=>{try{return {ok:true,value:helper.merge(...data)};}catch(error){return {ok:false};}})));"
        result = subprocess.run(['D:/Program Files (x86)/node.exe', '-e', script, str(VISUAL / 'collaborator_reviews.js')],
                                input=json.dumps(cases), text=True, capture_output=True, cwd=ROOT, check=True)
        self.assertEqual(json.loads(result.stdout), expectations)

    def test_unread_backups_are_deduplicated_losslessly_in_both_helpers(self):
        from collaborator_review import merge_backups
        saved = backups()
        expected = merge_backups(saved, saved)
        self.assertEqual(expected, saved)
        script = "const h=require(process.argv[1]),fs=require('node:fs');const x=JSON.parse(fs.readFileSync(0,'utf8'));process.stdout.write(JSON.stringify(h.mergeBackups(x,x)));"
        result = subprocess.run(['D:/Program Files (x86)/node.exe', '-e', script, str(VISUAL / 'collaborator_reviews.js')],
                                input=json.dumps(saved), text=True, capture_output=True, cwd=ROOT, check=True)
        self.assertEqual(json.loads(result.stdout), expected)
        with self.assertRaises(ValueError):
            merge_backups([{'origin': 'bad', 'reason': 'missing payload'}])


if __name__ == '__main__':
    unittest.main()
