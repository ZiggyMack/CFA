"""Dated, hash-bound publication overlays keep current authority and explicit clears."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from library_helpers import effective_reviews, review_payload, review_provenance
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

    def attributed(self, asset, fields, stamp=LATE, reviewer="baldadoon", **changes):
        human = {"reviewerControllerID": reviewer, "reviewer": reviewer.title(),
                 "projectControllerID": reviewer, "decisionAuthorityControllerID": reviewer,
                 "decisionScope": "location", "project": asset.get("project"),
                 "assetID": asset["id"], "sha256": asset["sha256"], "updatedAt": stamp,
                 "fields": fields}
        return {"id": asset["id"], "sha256": asset["sha256"], "origin": "user", "updatedAt": stamp,
                **{key: human[key] for key in ("reviewerControllerID", "reviewer", "projectControllerID",
                                               "decisionAuthorityControllerID", "decisionScope")},
                "humanReview": human, **changes}

    def test_mixed_new_note_stale_status_only_attributes_applied_note_and_archives_originals(self):
        asset = {"id": "house", "sha256": "a" * 64, "project": "criminal_mind"}
        prior = self.attributed(asset, ["note", "status"], MIDDLE, reviewer="ziggy", note="Earlier note", status="keep")
        incoming = self.attributed(asset, ["note", "status"], note="Denser neighborhood", status="remove",
                                  fieldUpdatedAt={"note": LATE, "status": EARLY})
        result, report = overlay_review_snapshot({"assets": [asset], "reviewDecisions": [prior]},
                                                 {"format": "cfa-visual-review-v1", "items": [incoming]})
        row = result["reviewDecisions"][0]
        self.assertEqual(row["note"], "Denser neighborhood")
        self.assertEqual(row["status"], "keep")
        self.assertEqual(row["reviewerControllerID"], "baldadoon")
        self.assertEqual(row["humanReview"]["fields"], ["note"])
        self.assertEqual(report["attributionConflicts"], [])
        archive = result["validationEvidence"]["legacyReviewArchive"]
        self.assertIn(prior, archive)
        self.assertIn(incoming, archive)
        exported = review_payload([asset], effective_reviews([asset], result["reviewDecisions"], {}), set(),
                                  provenance=review_provenance(result))
        self.assertEqual(exported["items"][0]["humanReview"]["fields"], ["note"])
        self.assertIn(incoming, exported["validationEvidence"]["legacyReviewArchive"])

    def test_no_change_echo_keeps_prior_attribution_but_preserves_incoming_receipt(self):
        asset = {"id": "house", "sha256": "a" * 64, "project": "criminal_mind"}
        prior = self.attributed(asset, ["note"], MIDDLE, reviewer="ziggy", note="Same note")
        incoming = self.attributed(asset, ["note"], note="Same note")
        result, report = overlay_review_snapshot({"assets": [asset], "reviewDecisions": [prior]},
                                                 {"format": "cfa-visual-review-v1", "items": [incoming]})
        self.assertEqual(result["reviewDecisions"], [prior])
        self.assertEqual(report["changedFields"], 0)
        self.assertIn(incoming, result["validationEvidence"]["legacyReviewArchive"])

    def test_alias_observation_is_archived_without_transplanting_reviewer_to_new_pixels(self):
        asset = {"id": "house", "sha256": "a" * 64, "project": "criminal_mind"}
        old = {**asset, "id": "old-house", "sha256": "b" * 64}
        incoming = self.attributed(old, ["note"], note="Alias-bound original observation")
        catalog = {"assets": [asset], "reviewDecisions": [], "assetAliases": [
            {"id": old["id"], "sha256": old["sha256"], "canonicalID": asset["id"],
             "canonicalSHA256": asset["sha256"], "kind": "visual_duplicate_reencoding"}]}
        result, report = overlay_review_snapshot(catalog, {"format": "cfa-visual-review-v1", "items": [incoming]})
        self.assertEqual(result["reviewDecisions"][0]["note"], incoming["note"])
        self.assertNotIn("humanReview", result["reviewDecisions"][0])
        self.assertNotIn("reviewerControllerID", result["reviewDecisions"][0])
        self.assertEqual(report["attributionConflicts"][0]["reason"], "human_receipt_target_mismatch_or_alias")
        self.assertIn(incoming, result["validationEvidence"]["legacyReviewArchive"])

    def test_unscoped_incoming_attribution_is_not_guessed_and_explicit_clear_evidence_survives(self):
        asset = {"id": "house", "sha256": "a" * 64, "project": "criminal_mind"}
        prior = self.attributed(asset, ["note", "shotPlan"], MIDDLE, reviewer="ziggy", note="Earlier",
                                shotPlan={"status": "planned", "destinations": ["Flow"], "idea": "Old", "prompt": ""})
        clear = {"updatedAt": LATE, "source": "Explicit director clear", "sourceReceipt": "original receipt"}
        incoming = {"id": asset["id"], "sha256": asset["sha256"], "origin": "user", "updatedAt": LATE,
                    "note": "New note", "shotPlan": None, "shotPlanClearEvidence": clear, "reviewerControllerID": "baldadoon"}
        result, report = overlay_review_snapshot({"assets": [asset], "reviewDecisions": [prior]},
                                                 {"format": "cfa-visual-review-v1", "items": [incoming]})
        row = result["reviewDecisions"][0]
        self.assertEqual(row["note"], incoming["note"])
        self.assertIsNone(row["shotPlan"])
        self.assertEqual(row["shotPlanClearEvidence"], clear)
        self.assertNotIn("humanReview", row)
        self.assertNotIn("reviewerControllerID", row)
        self.assertEqual(report["attributionConflicts"][0]["reason"], "missing_scoped_human_receipt")
        self.assertIn(prior, result["validationEvidence"]["legacyReviewArchive"])
        exported = review_payload([asset], effective_reviews([asset], [row], {}), set(), provenance=review_provenance(result))
        again, _ = overlay_review_snapshot({"assets": [asset], "reviewDecisions": []}, exported)
        self.assertIn(incoming, again["validationEvidence"]["legacyReviewArchive"])

    def test_cast_choices_survive_publication_and_review_export(self):
        catalog, asset = self.fixture()
        choice = {"roleSelected": True, "role": "Dolo's wife", "storyboardPlanned": True,
                  "storyboardLinks": [{"storyID": "strictly-business", "shotID": "S07-4"}]}
        result, report = overlay_review_snapshot(catalog, self.payload(asset, updatedAt=LATE, castUse=choice))
        self.assertEqual(result["reviewDecisions"][0]["castUse"], choice)
        self.assertEqual(report["changedFields"], 1)
        reviews = effective_reviews(result["assets"], result["reviewDecisions"], {})
        exported = review_payload(result["assets"], reviews, set())
        self.assertEqual(exported["items"][0]["castUse"], choice)
        self.assertEqual(result["reviewDecisions"][0]["acceptedScope"], catalog["reviewDecisions"][0]["acceptedScope"])
        self.assertNotIn("castUse", catalog["reviewDecisions"][0])

    def test_cast_clear_is_dated_and_unrelated_note_does_not_restore_it(self):
        catalog, asset = self.fixture()
        cleared = {"roleSelected": False, "role": "Dolo's wife", "storyboardPlanned": False, "storyboardLinks": []}
        catalog["reviewDecisions"][0].update(castUse=cleared, fieldUpdatedAt={"castUse": LATE})
        old_choice = {**cleared, "roleSelected": True, "storyboardPlanned": True}
        result, report = overlay_review_snapshot(catalog, self.payload(asset, updatedAt=MIDDLE, castUse=old_choice))
        self.assertEqual(result["reviewDecisions"][0]["castUse"], cleared)
        self.assertEqual(report["conflicts"][0]["field"], "castUse")
        result, _ = overlay_review_snapshot(catalog, self.payload(asset, updatedAt=LATE, note="Reconsider the scene"))
        self.assertEqual(result["reviewDecisions"][0]["castUse"], cleared)


if __name__ == "__main__":
    unittest.main()
