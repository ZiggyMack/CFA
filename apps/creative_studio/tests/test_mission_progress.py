"""Current Mission decisions remain scoped, reversible and exportable."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from library_helpers import (effective_reviews, mission_pending_requests, mission_review_data,
                             mission_task_progress, mission_tasks, read_review, review_payload)


class MissionProgressTest(unittest.TestCase):
    def gated_task(self):
        return {"id": "returned-repairs", "provider": "Grok", "project": "hon", "status": "needs_input",
                "title": "Returned repairs need review", "summary": "Waiting for your decision", "nextAction": "Review both returns",
                "priority": "top", "missing": ["Review the returned candidates"],
                "sourceMessageID": "original-dispatch", "receiptState": "received_unaccepted",
                "reviewGate": {"label": "Returned repairs", "targets": [
                    {"assetID": "a", "sha256": "a" * 64}, {"assetID": "b", "sha256": "b" * 64},
                    {"assetID": "c", "sha256": "c" * 64}],
                    "completed": {"title": "Returned repairs · review recorded", "statusLabel": "Review recorded · follow-up not sent",
                                  "summary": "User decisions are separate from approval and dispatch.",
                                  "nextAction": "Prepare the recorded correction for the team.",
                                  "missing": ["A replacement decision is separate."]}}}

    def gated_assets(self):
        return [{"id": n, "sha256": n * 64, "project": "hon", "kind": "video" if n == "c" else "image"}
                for n in ("a", "b", "c")]

    def test_gate_counts_mixed_answers_including_hidden_history_without_approval_or_dispatch(self):
        task, assets = self.gated_task(), self.gated_assets()
        assets[1]["archived"] = True
        reviews = {"a": {"status": "keep"}, "b": {"status": "remove", "archived": True},
                   "c": {"status": "needs_fixes", "note": "Remove extra lettering"}}
        before = copy.deepcopy((task, assets, reviews))
        shown = mission_task_progress(task, assets, reviews)
        self.assertEqual(shown["previewAssetIDs"], [])
        self.assertEqual(shown["reviewedPreviewAssetIDs"], ["a", "b", "c"])
        self.assertEqual(shown["reviewProgress"]["answered"], 3)
        self.assertEqual(shown["status"], "in_progress")
        self.assertEqual(shown["statusLabel"], "Review recorded · follow-up not sent")
        self.assertEqual(shown["title"], task["reviewGate"]["completed"]["title"])
        self.assertEqual(shown["missing"], ["A replacement decision is separate."])
        self.assertEqual(shown["priority"], "normal")
        self.assertEqual(shown["receiptState"], "received_unaccepted")
        self.assertEqual(shown["sourceMessageID"], "original-dispatch")
        self.assertNotIn("approval", shown)
        self.assertNotIn("feedbackSent", shown)
        self.assertEqual((task, assets, reviews), before)

    def test_gate_requires_triage_and_explicit_clear_reopens(self):
        task, assets = self.gated_task(), self.gated_assets()
        assets[0].update(providerQA="PASS", acceptance="approved")
        reviews = {"a": {"note": "Looks great", "likenessRating": 5}, "b": {"status": "keep"},
                   "c": {"status": "needs_fixes"}}
        pending = mission_task_progress(task, assets, reviews)
        self.assertEqual(pending["previewAssetIDs"], ["a"])
        self.assertEqual(pending["status"], "needs_input")
        self.assertEqual(pending["statusLabel"], "Needs your input")
        self.assertEqual(pending["title"], "Returned repairs · 1 awaiting review")
        self.assertEqual(pending["missing"], ["1 requested versions have no recorded decision."])
        reviews["a"]["status"] = "keep"
        self.assertEqual(mission_task_progress(task, assets, reviews)["previewAssetIDs"], [])
        reviews["b"]["status"] = None
        reopened = mission_task_progress(task, assets, reviews)
        self.assertEqual(reopened["previewAssetIDs"], ["b"])
        self.assertEqual(reopened["reviewedPreviewAssetIDs"], ["a", "c"])

    def test_gate_wrong_or_absent_version_never_completes_from_same_id_review(self):
        task, assets = self.gated_task(), self.gated_assets()
        assets[0]["sha256"] = "d" * 64
        assets[1]["kind"] = "document"
        reviews = {n: {"status": "keep"} for n in ("a", "b", "c")}
        shown = mission_task_progress(task, assets[:2], reviews)
        self.assertEqual(shown["status"], "in_progress")
        self.assertEqual(shown["statusLabel"], "Reference check needed")
        self.assertEqual(shown["reviewProgress"]["unavailableIDs"], ["a", "b", "c"])
        self.assertEqual(shown["reviewedPreviewAssetIDs"], [])
        self.assertIn("exact missing or mismatched versions", shown["nextAction"])
        mixed = mission_task_progress(task, [*assets[:2], self.gated_assets()[2]], {})
        self.assertEqual(mixed["status"], "needs_input")
        self.assertEqual(mixed["previewAssetIDs"], ["c"])
        self.assertEqual(mixed["reviewProgress"]["unavailableIDs"], ["a", "b"])

    def test_gate_checks_review_hash_and_does_not_treat_archive_as_a_review(self):
        task, assets = self.gated_task(), self.gated_assets()
        reviews = {n: {"status": "keep", "sha256": n.upper() * 64} for n in ("a", "b", "c")}
        self.assertEqual(mission_task_progress(task, assets, reviews)["reviewProgress"]["answered"], 3)
        reviews["a"]["sha256"] = "f" * 64
        shown = mission_task_progress(task, assets, reviews)
        self.assertEqual(shown["reviewProgress"]["unavailableIDs"], ["a"])
        self.assertEqual(shown["statusLabel"], "Reference check needed")
        reviews["a"] = {"status": None, "collectionState": "archived", "sha256": "a" * 64}
        shown = mission_task_progress(task, assets, reviews)
        self.assertEqual(shown["reviewProgress"]["unavailableIDs"], ["a"])
        self.assertEqual(shown["reviewProgress"]["answered"], 2)
        self.assertEqual(shown["statusLabel"], "Reference check needed")

    def test_gate_parser_preserves_scope_deduplicates_and_rejects_invalid_whole_gate(self):
        task = self.gated_task()
        task["reviewGate"]["targets"].append({"assetID": "a", "sha256": "A" * 64})
        task["reviewGate"]["completed"]["approval"] = True
        parsed = mission_tasks({"tasks": [task]})[0]
        self.assertEqual(len(parsed["reviewGate"]["targets"]), 3)
        self.assertNotIn("approval", parsed["reviewGate"]["completed"])
        parsed["reviewGate"]["targets"][0]["sha256"] = "f" * 64
        self.assertEqual(task["reviewGate"]["targets"][0]["sha256"], "a" * 64)
        for bad in ([], [{"assetID": "a", "sha256": "wrong"}],
                    [{"assetID": "a", "sha256": "a" * 64}, {"assetID": "a", "sha256": "b" * 64}]):
            task["reviewGate"]["targets"] = bad
            parsed = mission_tasks({"tasks": [task]})[0]
            self.assertNotIn("reviewGate", parsed)
            self.assertEqual(mission_task_progress(parsed, self.gated_assets(), {}), parsed)

    def test_gate_does_not_reopen_done_tasks_or_change_ungated_tasks(self):
        task, assets = self.gated_task(), self.gated_assets()
        task["status"] = "done"
        self.assertEqual(mission_task_progress(task, assets, {}), task)
        task["status"] = "needs_input"
        del task["reviewGate"]
        self.assertEqual(mission_task_progress(task, assets, {n: {"status": "keep"} for n in ("a", "b", "c")}), task)

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
