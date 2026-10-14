"""Current Mission decisions remain scoped, reversible and exportable."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from library_helpers import (effective_reviews, mission_pending_requests, mission_review_data,
                             mission_task_progress, mission_tasks, read_review, review_payload)


class MissionProgressTest(unittest.TestCase):
    def test_shortlist_answers_are_not_reassigned_and_explicit_clear_reopens(self):
        assets = [{"id": n, "sha256": n, "project": "lisan", "kind": "image"} for n in ("a", "b", "c", "extra")]
        assets[2]["archived"] = True
        task = {"id": "grok-lisan-mouth65-available", "previewAssetIDs": ["a", "b", "b", "c", "missing"], "priority": "top"}
        before = copy.deepcopy(task)
        reviews = {"a": {"status": "keep"}, "b": {"status": "remove"}, "c": {"status": "needs_fixes"}}
        shown = mission_task_progress(task, assets, reviews)
        self.assertEqual(shown["previewAssetIDs"], [])
        self.assertEqual(shown["reviewedPreviewAssetIDs"], ["a", "b", "c"])
        self.assertIn("1 references are unavailable", shown["summary"])
        self.assertEqual(shown["status"], "in_progress")
        self.assertEqual(task, before)
        reviews["a"]["status"] = None
        reopened = mission_task_progress(task, assets, reviews)
        self.assertEqual(reopened["previewAssetIDs"], ["a"])
        self.assertEqual(reopened["status"], "needs_input")
        self.assertNotIn("extra", reopened["previewAssetIDs"])

    def test_queue_only_counts_hash_bound_unanswered_requests(self):
        data = {"assets": [{"id": n, "project": "hon", "sha256": n} for n in ("a", "b", "c")],
                "reviewRequests": [{"id": n, "sha256": n, "type": "missing_decision"} for n in ("a", "b", "c")]}
        data["reviewRequests"][2]["sha256"] = "stale"
        self.assertEqual(mission_pending_requests(data, {"a": {"status": "needs_fixes"}}, "hon"), ["b"])
        self.assertEqual(mission_pending_requests(data, {"a": {"status": None}}, "lisan"), [])

    def test_rich_reviews_roundtrip_and_field_clears(self):
        asset = {"id": "new", "sha256": "exact", "kind": "image", "project": "hon"}
        seed = {"id": "new", "sha256": "exact", "status": "needs_fixes", "note": "Gun good; wrong character",
                "likenessRating": 2, "sceneQualityRating": 5, "workingReferenceScope": "detail",
                "workingReference": {"status": "approved", "scope": "detail", "scopeCorrection": "Wrist only"},
                "creativeReview": {"status": "queued", "recipients": ["grok_chief"]},
                "componentSelection": {"scope": "gun", "approved": True}}
        base = {"assets": [], "reviewDecisions": [], "albums": []}
        data = mission_review_data(base, {"assets": [asset], "reviewDecisions": [seed]})
        reviews = effective_reviews(data["assets"], data["reviewDecisions"], {"new": {"status": None, "sceneQualityRating": None}})
        exported = review_payload(data["assets"], reviews, {"new"})
        restored, stars, skipped = read_review(exported, data["assets"])
        self.assertEqual((stars, skipped), ({"new"}, 0))
        for key in ("status", "sceneQualityRating"):
            self.assertIsNone(restored["new"][key])
        for key in ("likenessRating", "workingReferenceScope", "workingReference", "creativeReview", "componentSelection"):
            self.assertEqual(restored["new"][key], seed[key])
        self.assertEqual(base, {"assets": [], "reviewDecisions": [], "albums": []})
        with self.assertRaises(ValueError):
            mission_review_data(data, {"assets": [{**asset, "sha256": "different"}]})

    def test_extended_providers_and_deliverables_survive(self):
        task = {"id": "cfa", "provider": "CFA Nova", "project": "shared", "title": "References",
                "status": "ready", "summary": "Ready", "nextAction": "Send", "priority": "top",
                "enablers": [], "deliverables": ["Returned designs"], "laterReview": "Choose later",
                "links": [{"label": "Gallery", "assetIDs": ["a", "b"]}]}
        actual = mission_tasks({"tasks": [task]})[0]
        for key in ("provider", "priority", "enablers", "deliverables", "laterReview", "links"):
            self.assertEqual(actual[key], task[key])

    def test_mutable_brief_refresh_does_not_relax_media_identity(self):
        old = {"id": "brief", "kind": "document", "sha256": "older", "text": "Old"}
        current = {**old, "sha256": "current", "text": "Current"}
        merged = mission_review_data({"assets": [old]}, {"assets": [current]})
        self.assertEqual(merged["assets"], [current])
        self.assertEqual(old["text"], "Old")


if __name__ == "__main__":
    unittest.main()
