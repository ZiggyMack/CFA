"""Dated, hash-bound publication overlays keep current authority and explicit clears."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from library_helpers import effective_reviews, review_payload
from review_snapshot import overlay_review_snapshot


EARLY = "2026-10-20T10:00:00Z"
MIDDLE = "2026-10-21T10:00:00Z"
LATE = "2026-10-22T10:00:00Z"


class ReviewSnapshotTest(unittest.TestCase):
    def fixture(self):
        asset = {"id": "image", "sha256": "a" * 64, "project": "hon", "filename": "image.jpg"}
        row = {"id": "image", "sha256": asset["sha256"], "status": "keep", "note": "Canonical note",
               "updatedAt": MIDDLE, "origin": "user", "likenessRating": 5,
               "acceptedScope": {"scope": "scene", "source": "direct user"},
               "validationEvidence": {"passed": "only the exact original"}}
        return {"assets": [asset], "reviewDecisions": [row], "referenceValidation": {"assessments": [{"id": "unchanged"}]}}, asset

    def payload(self, asset, **fields):
        return {"format": "cfa-visual-review-v1", "exported": LATE,
                "items": [{"id": asset["id"], "sha256": asset["sha256"], "origin": "user", **fields}]}

    def test_newer_explicit_clear_and_note_preserve_omitted_scores_and_authority(self):
        catalog, asset = self.fixture()
        before = deepcopy(catalog)
        payload = self.payload(asset, updatedAt=LATE, status=None, note="", acceptedScope={"scope": "invented"},
                               validationEvidence={"passed": "must not overwrite"})
        result, report = overlay_review_snapshot(catalog, payload)
        row = result["reviewDecisions"][0]
        self.assertIsNone(row["status"])
        self.assertEqual(row["note"], "")
        self.assertEqual(row["likenessRating"], 5)
        self.assertEqual(row["acceptedScope"], before["reviewDecisions"][0]["acceptedScope"])
        self.assertEqual(row["validationEvidence"], before["reviewDecisions"][0]["validationEvidence"])
        self.assertEqual(result["referenceValidation"], before["referenceValidation"])
        self.assertEqual(catalog, before)
        self.assertEqual(report["changedFields"], 2)

    def test_field_dates_compare_independently_and_survive_review_export(self):
        catalog, asset = self.fixture()
        catalog["reviewDecisions"][0].update(updatedAt=LATE, fieldUpdatedAt={"status": LATE, "note": EARLY})
        result, report = overlay_review_snapshot(catalog, self.payload(asset, updatedAt=MIDDLE, status="remove", note="Newer note"))
        row = result["reviewDecisions"][0]
        self.assertEqual(row["status"], "keep")
        self.assertEqual(row["note"], "Newer note")
        self.assertEqual(report["conflicts"][0]["field"], "status")
        reviews = effective_reviews(result["assets"], result["reviewDecisions"], {})
        exported = review_payload(result["assets"], reviews, set())
        self.assertEqual(exported["items"][0]["fieldUpdatedAt"], row["fieldUpdatedAt"])
        repeated, again = overlay_review_snapshot(result, self.payload(asset, updatedAt=MIDDLE, status="remove", note="Newer note"))
        self.assertEqual(repeated["reviewDecisions"], result["reviewDecisions"])
        self.assertEqual(again["changedFields"], 0)

    def test_older_equal_undated_and_catalog_echo_changes_are_reported_not_applied(self):
        catalog, asset = self.fixture()
        for stamp, reason in ((EARLY, "canonical_newer"), (MIDDLE, "same_time_different_value"), (None, "undated_change")):
            result, report = overlay_review_snapshot(catalog, self.payload(asset, updatedAt=stamp, status="remove"))
            self.assertEqual(result["reviewDecisions"], catalog["reviewDecisions"])
            self.assertEqual(report["conflicts"][0]["reason"], reason)
        payload = self.payload(asset, updatedAt=LATE, status="remove")
        payload["items"][0]["origin"] = "catalog"
        result, report = overlay_review_snapshot(catalog, payload)
        self.assertEqual(result["reviewDecisions"], catalog["reviewDecisions"])
        self.assertEqual(report["skipped"][0]["reason"], "catalog_echo_or_origin_unknown")

    def test_current_exact_alias_can_copy_choice_without_transplanting_validation(self):
        catalog, asset = self.fixture()
        catalog["assetAliases"] = [{"id": "old-image", "sha256": "b" * 64, "canonicalID": asset["id"],
                                     "canonicalSHA256": asset["sha256"], "kind": "visual_duplicate_reencoding"}]
        alias = {"id": "old-image", "sha256": "b" * 64}
        payload = self.payload(alias, updatedAt=LATE, status="needs_fixes", validationEvidence={"oldPixels": "passed"})
        payload["favorites"] = [alias, {"id": asset["id"], "sha256": "incorrect"}]
        payload["exportBasket"] = [{"id": asset["id"], "sha256": asset["sha256"]}]
        result, report = overlay_review_snapshot(catalog, payload)
        self.assertEqual(result["reviewDecisions"][0]["status"], "needs_fixes")
        self.assertEqual(result["reviewDecisions"][0]["validationEvidence"], catalog["reviewDecisions"][0]["validationEvidence"])
        self.assertEqual(result["reviewSessionSeed"]["favorites"][0]["sha256"], asset["sha256"])
        self.assertEqual(len(result["reviewSessionSeed"]["favorites"]), 1)
        self.assertEqual(report["aliases"], [{"sourceID": "old-image", "canonicalID": "image"}])
        bad, _ = overlay_review_snapshot(catalog, self.payload({"id": "old-image", "sha256": "c" * 64}, updatedAt=LATE, status="remove"))
        self.assertEqual(bad["reviewDecisions"], catalog["reviewDecisions"])

    def test_dated_plan_clear_is_not_resurrected_or_erased_by_missing_fields(self):
        catalog, asset = self.fixture()
        catalog["reviewDecisions"][0].update(shotPlan=None, shotPlanClearEvidence={"updatedAt": LATE, "source": "user clear"})
        plan = {"destinations": ["Flow"], "idea": "An older idea", "prompt": ""}
        result, report = overlay_review_snapshot(catalog, self.payload(asset, updatedAt=MIDDLE, shotPlan=plan))
        self.assertIsNone(result["reviewDecisions"][0]["shotPlan"])
        self.assertEqual(report["conflicts"][0]["reason"], "canonical_newer")
        result, _ = overlay_review_snapshot(catalog, self.payload(asset, updatedAt=LATE, note="New note"))
        self.assertEqual(result["reviewDecisions"][0]["shotPlanClearEvidence"], catalog["reviewDecisions"][0]["shotPlanClearEvidence"])
        self.assertIsNone(result["reviewDecisions"][0]["shotPlan"])

    def test_bad_hash_new_user_record_and_optional_selections(self):
        catalog, asset = self.fixture()
        extra = {**asset, "id": "new", "sha256": "d" * 64}
        catalog["assets"].append(extra)
        payload = self.payload(extra, updatedAt=LATE, status="keep", sceneQualityRating=5)
        payload["items"].append({"id": "image", "sha256": "wrong", "origin": "user", "updatedAt": LATE, "status": "remove"})
        result, report = overlay_review_snapshot(catalog, payload, include_selections=False)
        self.assertEqual(len(result["reviewDecisions"]), 2)
        self.assertEqual(result["reviewDecisions"][0], catalog["reviewDecisions"][0])
        self.assertEqual(result["reviewDecisions"][1]["sceneQualityRating"], 5)
        self.assertNotIn("acceptedScope", result["reviewDecisions"][1])
        self.assertNotIn("reviewSessionSeed", result)
        self.assertEqual(report["skipped"][0]["reason"], "unmatched_id_or_hash")


if __name__ == "__main__":
    unittest.main()
