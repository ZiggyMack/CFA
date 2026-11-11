"""Location-only direction survives every review transfer without selecting assets."""
from copy import deepcopy
from pathlib import Path
import sys
import unittest

APP = Path(__file__).resolve().parents[1]
ROOT = APP.parents[1]
sys.path.insert(0, str(APP))
sys.path.insert(0, str(ROOT / "docs/notes/explorable_world/comfy/projects/visual_library"))
from library_helpers import read_review, review_payload, review_provenance
from location_reviews import merge_state
from review_snapshot import overlay_review_snapshot
from location_review_intake import apply_location_reviews


class LocationReviewTest(unittest.TestCase):
    def fixture(self):
        row = {"project": "criminal_mind", "locationFamilyID": "TCM-SET-HENDERSON-EXTERIOR",
               "note": "Make the neighborhood denser.", "updatedAt": "2026-11-06T12:00:00Z",
               "origin": "browser", "attributionStatus": "confirmed", "projectControllerID": "baldadoon",
               "reviewer": "Baldadoon", "reviewerControllerID": "baldadoon",
               "decisionAuthorityControllerID": "baldadoon", "decisionScope": "location",
               "humanReview": {"reviewerControllerID": "baldadoon", "decisionScope": "location",
                               "project": "criminal_mind", "locationFamilyID": "TCM-SET-HENDERSON-EXTERIOR",
                               "updatedAt": "2026-11-06T12:00:00Z", "fields": ["note"]}}
        return {"format": "cfa-visual-review-v1", "items": [], "favorites": [], "locationReviews": [row]}

    def test_full_native_export_publication_roundtrip_preserves_scope_and_attribution(self):
        incoming = self.fixture()
        before = deepcopy(incoming)
        image = {"id": "house-look", "project": "criminal_mind", "sha256": "a" * 64, "selected": False}
        reviews, favorites, skipped = read_review(incoming, [image])
        self.assertEqual((reviews, favorites, skipped), ({}, set(), 0))
        exported = review_payload([image], reviews, favorites, provenance=review_provenance(incoming))
        self.assertEqual(exported["locationReviews"], incoming["locationReviews"])
        catalog = {"assets": [image], "reviewDecisions": []}
        published, report = overlay_review_snapshot(catalog, exported)
        self.assertEqual(published["locationReviews"], incoming["locationReviews"])
        self.assertEqual(published["assets"], catalog["assets"])
        self.assertEqual(published["reviewDecisions"], [])
        self.assertEqual(report["changedFields"], 0)
        self.assertEqual(incoming, before)
        self.assertNotIn("locationReviews", catalog)

    def test_older_equal_and_undated_conflicts_cannot_overwrite_current_direction(self):
        current = self.fixture()
        row = current["locationReviews"][0]
        for stamp in ("2026-11-05T12:00:00Z", row["updatedAt"], None):
            old = {**deepcopy(row), "note": "Older or conflicting suggestion", "updatedAt": stamp}
            merged = merge_state(current, {"locationReviews": [old]})
            self.assertEqual(merged["locationReviews"], [row])
            self.assertEqual(merged["locationReviewBackups"][0]["data"], old)
            self.assertEqual(merge_state(merged, {"locationReviews": [old]}), merged)

    def test_newer_explicit_clear_retains_old_text_in_backup_and_does_not_confirm_draft(self):
        current = self.fixture()
        clear = {"project": "criminal_mind", "locationFamilyID": "TCM-SET-HENDERSON-EXTERIOR",
                 "note": "", "updatedAt": "2026-11-07T12:00:00Z", "origin": "browser",
                 "attributionStatus": "draft", "decisionScope": "location"}
        merged = review_provenance({"locationReviews": [clear]}, review_provenance(current))
        self.assertEqual(merged["locationReviews"], [clear])
        self.assertNotIn("reviewerControllerID", merged["locationReviews"][0])
        self.assertEqual(merged["locationReviewBackups"][0]["data"], current["locationReviews"][0])
        exported = review_payload([], {}, set(), provenance=merged)
        self.assertEqual(exported["locationReviews"], [clear])
        self.assertEqual(exported["locationReviewBackups"], merged["locationReviewBackups"])

    def test_unsupported_data_is_backed_up_not_interpreted_as_asset_approval(self):
        row = {**self.fixture()["locationReviews"][0], "status": "keep", "selected": True}
        merged = merge_state({}, {"locationReviews": [row, {"futureSchema": 99}]})
        self.assertNotIn("status", merged["locationReviews"][0])
        self.assertNotIn("selected", merged["locationReviews"][0])
        self.assertEqual([b["data"] for b in merged["locationReviewBackups"]], [row, {"futureSchema": 99}])
        invalid = {"locationReviews": {"future": "envelope"}, "locationReviewBackups": "future backup"}
        preserved = review_provenance(invalid)
        self.assertEqual(preserved["locationReviews"], [])
        self.assertEqual(len(preserved["locationReviewBackups"]), 2)

    def test_family_identity_is_project_scoped_and_transport_does_not_rebind_it(self):
        first = self.fixture()["locationReviews"][0]
        other = {**deepcopy(first), "project": "hon", "note": "Different project, same family token"}
        merged = merge_state({}, {"locationReviews": [first, other]})
        self.assertEqual(merged["locationReviews"], [first, other])

    def test_native_transport_preserves_exact_nested_provenance_without_confirming_it(self):
        incoming = self.fixture()
        row = incoming["locationReviews"][0]
        row["humanReview"]["sourceReceipt"] = "director-original-export"
        row["reviewer"] = "Director-provided label"
        row["attributionStatus"] = "draft"
        exported = review_payload([], {}, set(), provenance=review_provenance(incoming))
        self.assertEqual(exported["locationReviews"], [row])
        self.assertEqual(exported["locationReviews"][0]["attributionStatus"], "draft")

    def test_local_rebuild_retains_previous_notes_and_merges_dated_canonical_changes(self):
        previous = self.fixture()
        rebuilt = {"assets": [], "reviewDecisions": []}
        apply_location_reviews(rebuilt, ROOT, {}, previous)
        self.assertEqual(rebuilt["locationReviews"], previous["locationReviews"])
        newer = deepcopy(previous)
        newer["locationReviews"][0].update(note="A later direction", updatedAt="2026-11-08T12:00:00Z")
        apply_location_reviews(rebuilt, ROOT, newer, previous)
        self.assertEqual(rebuilt["locationReviews"], newer["locationReviews"])
        self.assertEqual(rebuilt["locationReviewBackups"][0]["data"], previous["locationReviews"][0])
        self.assertEqual(rebuilt["reviewDecisions"], [])
        empty = {"assets": []}
        apply_location_reviews(empty, ROOT, {}, {})
        self.assertEqual(empty, {"assets": []}, "No notes are invented for existing empty catalogs")


if __name__ == "__main__":
    unittest.main()
