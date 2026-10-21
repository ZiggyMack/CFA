"""Design parity: visibility, explicit selections and hash-bound review recovery."""

import copy
import itertools
import json
from pathlib import Path
import sys
import unittest

APP_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_DIR))
from library_helpers import (
    EXPORT_FORMAT, FAVORITES_FORMAT, REVIEW_FORMAT, HISTORICAL_TATTOO_IDS,
    approved_multiverse, asset_archived, basket_payload, design_archive_membership,
    effective_design_data, effective_reviews, export_allowed, merge_review_overrides,
    mission_visible, normal_visible, normalize_decision, ordered_assets, read_basket,
    read_favorites, read_review, resolve_asset_reference, review_payload,
    review_provenance, sweep_payload, validated_asset_aliases,
)


def asset(asset_id, **extra):
    return {"id": asset_id, "sha256": "a" * 64, "project": "hon", "kind": "image", **extra}


class DesignStateTest(unittest.TestCase):
    def test_history_membership_matches_each_explicit_source_and_protection(self):
        names = ["cover", "bom-selected", "cast-current", "cast-working", "component", "bom-old",
                 "shared-old", "cast-old", "cast-candidate", "mouth-old", "mouth-wrong-hash",
                 "inspiration", "creature", "HD-LIKENESS-02", *HISTORICAL_TATTOO_IDS]
        assets = [asset(name) for name in names]
        next(a for a in assets if a["id"] == "component")["componentApprovals"] = [
            {"sourceSHA256": "a" * 64, "status": "user_selected_component"}]
        protected = ["cover", "bom-selected", "cast-current", "cast-working", "component"]
        data = {"assets": assets,
                "albums": [{"id": "hon:scene-ideas", "assetIDs": ["inspiration", *protected]},
                           {"id": "hon:creature-boss", "assetIDs": ["creature"]}],
                "characterBOM": {"characters": [{"coverAssetID": "cover", "historyAssetIDs": ["bom-old"],
                                                  "entries": [{"assetID": "bom-selected", "recordedSelection": {"status": "selected"}}]}]},
                "sharedReferenceCollections": [{"sections": [{"history": True, "assetIDs": ["shared-old"]}]}],
                "castCollections": [{"currentIDs": ["cast-current"], "workingReferenceIDs": ["cast-working"],
                                     "historicalReferenceIDs": ["cast-old"],
                                     "sections": [{"history": True, "assetIDs": ["cast-candidate"]}]}],
                "mouthCoverage": {"looks": [{"id": "old", "planStatus": "History only"}], "items": [
                    {"lookID": "old", "assetID": "mouth-old", "sha256": "a" * 64},
                    {"lookID": "old", "assetID": "mouth-wrong-hash", "sha256": "b" * 64}]}}
        before = copy.deepcopy(data)
        historical, retired = design_archive_membership(data)
        self.assertEqual(historical, {"bom-old", "shared-old", "cast-old", "mouth-old", "inspiration",
                                      "HD-LIKENESS-02", *HISTORICAL_TATTOO_IDS})
        self.assertEqual(retired, {"inspiration", *protected})
        self.assertEqual(data, before)

    def test_archive_restore_and_remove_are_independent_and_survive_round_trip(self):
        source = {"assets": [asset("HD-LIKENESS-02"), asset("source-old", archived=True), asset("removed")], "albums": []}
        reviews = {"HD-LIKENESS-02": {"status": "keep", "collectionState": "working"},
                   "source-old": {"status": "needs_fixes", "collectionState": "working"},
                   "removed": {"status": "remove", "collectionState": "working"}}
        before = copy.deepcopy(source)
        data = effective_design_data(source, reviews)
        self.assertEqual([a["id"] for a, _ in ordered_assets(data["assets"], [], "hon")], ["HD-LIKENESS-02", "source-old"])
        self.assertEqual(len(ordered_assets(data["assets"], [], "hon", include_archived=True)), 3)
        self.assertFalse(normal_visible(data["assets"][2], reviews))
        self.assertFalse(export_allowed(data["assets"][2], reviews))
        self.assertFalse(mission_visible(data["assets"][2], reviews))
        self.assertEqual(effective_design_data(data, reviews), data)
        self.assertEqual(source, before)
        restored, _, skipped = read_review(review_payload(source["assets"], reviews, set()), source["assets"])
        self.assertEqual(skipped, 0)
        self.assertEqual(effective_design_data(source, restored), data)
        cleared = {**reviews, "source-old": {"collectionState": None}}
        self.assertTrue(asset_archived(effective_design_data(data, cleared)["assets"][1], cleared))
        explicit = {"HD-LIKENESS-02": {"status": "keep", "collectionState": "archived"}}
        self.assertFalse(normal_visible(effective_design_data(source, explicit)["assets"][0], explicit))

    def test_selected_retired_inspiration_stays_visible_but_explicit_archive_wins(self):
        data = {"assets": [asset("idea")], "albums": [{"id": "hon:outfit-ideas", "assetIDs": ["idea"]}]}
        for decision in ({"workingReference": {"status": "approved", "scope": "outfit"}},
                         {"status": "keep", "storyboardStage": "production"}):
            reviews = {"idea": decision}
            self.assertTrue(normal_visible(effective_design_data(data, reviews)["assets"][0], reviews))
            reviews["idea"] = {**decision, "collectionState": "archived"}
            self.assertFalse(normal_visible(effective_design_data(data, reviews)["assets"][0], reviews))
        for decision in ({"status": "keep"}, {"storyboardStage": "production"}, {"likenessRating": 5}):
            self.assertTrue(effective_design_data(data, {"idea": decision})["assets"][0]["archived"])

    def test_multiverse_requires_explicit_approval_and_character_rating(self):
        image = asset("multi", variant="multiverse")
        for rating in (2, 3, 4, 5):
            self.assertTrue(approved_multiverse(image, {"multi": {"multiverseSelection": "approved", "likenessRating": rating}}))
        for decision in ({"likenessRating": 5, "sceneQualityRating": 5, "status": "keep", "storyboardStage": "production"},
                         {"multiverseSelection": "candidate", "likenessRating": 5},
                         {"multiverseSelection": "approved", "likenessRating": 1},
                         {"multiverseSelection": "approved", "likenessRating": True},
                         {"multiverseSelection": "approved", "sceneQualityRating": 5},
                         {"multiverseSelection": "approved", "likenessRating": 5, "collectionState": "archived"},
                         {"multiverseSelection": "approved", "likenessRating": 5, "status": "remove"},
                         {"multiverseSelection": "approved", "likenessRating": 5, "variant": "prime"}):
            self.assertFalse(approved_multiverse(image, {"multi": decision}), decision)
        self.assertTrue(export_allowed(image, {}, "multiverse_ingredients"))
        self.assertFalse(export_allowed(image, {}, "prime"))
        source = {**image, "workingReference": {"status": "approved", "scope": "identity"}}
        self.assertIsNone(effective_reviews([source], [], {})["multi"]["workingReference"])

    def test_invalid_design_choices_rejected_and_explicit_null_clears_retained(self):
        for key in ("collectionState", "multiverseSelection"):
            with self.assertRaises(ValueError):
                normalize_decision({key: "automatic"})
            self.assertIsNone(normalize_decision({key: None})[key])

    def test_dated_field_only_clear_blocks_older_import_without_dating_other_fields(self):
        assets = [asset("panel")]
        seed = {"id": "panel", "sha256": "a" * 64, "updatedAt": "2026-10-12T12:00:00Z", "note": "Original",
                "shotPlan": None, "shotPlanClearEvidence": {"updatedAt": "2026-10-14T13:18:15.369Z", "exportSHA256": "d" * 64}}
        old_plan = {"destinations": ["Flow"], "idea": "Cleared idea", "prompt": ""}
        imported, _, _ = read_review({"format": REVIEW_FORMAT, "items": [
            {"id": "panel", "sha256": "a" * 64, "updatedAt": "2026-10-13T12:00:00Z", "shotPlan": old_plan, "note": "Still import this note"}]}, assets)
        effective = effective_reviews(assets, [seed], imported)
        self.assertIsNone(effective["panel"]["shotPlan"])
        self.assertEqual(effective["panel"]["note"], "Still import this note")
        self.assertEqual(effective["panel"]["updatedAt"], "2026-10-13T12:00:00Z")
        self.assertEqual(effective["panel"]["shotPlanClearEvidence"], seed["shotPlanClearEvidence"])
        exported = review_payload(assets, effective, set())
        restored = read_review(exported, assets)[0]
        self.assertIsNone(effective_reviews(assets, [seed], restored)["panel"]["shotPlan"])

    def test_newer_explicit_plan_survives_older_clear_import_and_backup(self):
        assets = [asset("panel")]
        seed = {"id": "panel", "sha256": "a" * 64, "updatedAt": "2026-10-12T12:00:00Z", "shotPlan": None,
                "shotPlanClearEvidence": {"updatedAt": "2026-10-14T13:18:15.369Z", "exportSHA256": "d" * 64}}
        plan = {"destinations": ["Flow"], "idea": "New explicit plan", "prompt": ""}
        newer = {"id": "panel", "sha256": "a" * 64, "updatedAt": "2026-10-20T12:00:00Z", "shotPlan": plan}
        for records in itertools.permutations([seed, newer]):
            imported = read_review({"format": REVIEW_FORMAT, "items": list(records)}, assets)[0]
            effective = effective_reviews(assets, [seed], imported)
            self.assertEqual(effective["panel"]["shotPlan"]["idea"], "New explicit plan")
            restored = read_review(review_payload(assets, effective, set()), assets)[0]
            self.assertEqual(effective_reviews(assets, [seed], restored)["panel"]["shotPlan"]["idea"], "New explicit plan")
            self.assertEqual(effective["panel"]["shotPlanClearEvidence"], seed["shotPlanClearEvidence"])


class VisualAliasStateTest(unittest.TestCase):
    def setUp(self):
        self.assets = [asset("canonical"), asset("other", sha256="c" * 64)]
        self.aliases = [{"id": "retired", "sha256": "b" * 64, "canonicalID": "canonical",
                         "canonicalSHA256": "a" * 64, "kind": "visual_duplicate_reencoding"}]
        self.old = {"id": "retired", "sha256": "b" * 64, "status": "keep", "note": "latest alias",
                    "updatedAt": "2026-10-14T13:39:00Z", "shotPlan": None}
        self.current = {"id": "canonical", "sha256": "a" * 64, "status": "needs_fixes", "note": "earlier canonical",
                        "updatedAt": "2026-10-14T13:04:00Z", "shotPlan": {"destinations": ["Grok"], "idea": "Fix teeth"}}

    def test_alias_requires_declared_family_and_exact_old_and_current_hashes(self):
        self.assertEqual(resolve_asset_reference(self.old, self.assets, self.aliases)["id"], "canonical")
        for record in ({"id": "retired"}, {"id": "retired", "sha256": "a" * 64}, {"id": "unknown", "sha256": "b" * 64}):
            self.assertIsNone(resolve_asset_reference(record, self.assets, self.aliases))
        for changed in ({"kind": "same_hash"}, {"canonicalSHA256": "d" * 64}, {"sha256": "short"}):
            self.assertEqual(validated_asset_aliases(self.assets, [{**self.aliases[0], **changed}]), {})
        conflicts = [*self.aliases, {**self.aliases[0], "canonicalID": "other", "canonicalSHA256": "c" * 64}]
        self.assertEqual(validated_asset_aliases(self.assets, conflicts), {})
        self.assertEqual(validated_asset_aliases([*self.assets, asset("retired", sha256="b" * 64)], self.aliases), {})

    def test_latest_alias_decision_wins_independent_of_order_and_clears_plan(self):
        before = copy.deepcopy((self.assets, self.old, self.current))
        for records in itertools.permutations([self.old, self.current]):
            reviews = effective_reviews(self.assets, list(records), {}, self.aliases)
            self.assertEqual(reviews["canonical"]["status"], "keep")
            self.assertIsNone(reviews["canonical"]["shotPlan"])
            imported, _, skipped = read_review({"format": REVIEW_FORMAT, "items": list(records)}, self.assets, self.aliases)
            self.assertEqual(skipped, 0)
            self.assertEqual(imported["canonical"]["note"], "latest alias")
            self.assertIsNone(imported["canonical"]["shotPlan"])
        self.assertEqual((self.assets, self.old, self.current), before)

    def test_canonical_wins_ties_and_newer_ui_edit_drops_old_marker(self):
        tied = {**self.current, "updatedAt": self.old["updatedAt"]}
        for records in itertools.permutations([self.old, tied]):
            for reviews in (effective_reviews(self.assets, list(records), {}, self.aliases),
                            read_review({"format": REVIEW_FORMAT, "items": list(records)}, self.assets, self.aliases)[0]):
                self.assertEqual(reviews["canonical"]["note"], "earlier canonical")
                self.assertNotIn("_visualAliasSource", reviews["canonical"])
        reviews = effective_reviews(self.assets, [self.old, self.current], {}, self.aliases)
        current = {"canonical": {"updatedAt": "2026-10-20T12:00:00Z", "note": "new UI choice", "collectionState": "working"}}
        merged = merge_review_overrides(reviews, current, self.assets, self.aliases)
        self.assertEqual(merged["canonical"]["note"], "new UI choice")
        self.assertNotIn("_visualAliasSource", merged["canonical"])
        stale = read_review({"format": REVIEW_FORMAT, "items": [self.old]}, self.assets, self.aliases)[0]
        self.assertEqual(merge_review_overrides(merged, stale, self.assets, self.aliases), merged)
        spoof = {"canonical": {"note": "wrong source", "_visualAliasSource": {"id": "retired", "sha256": "d" * 64}}}
        self.assertEqual(merge_review_overrides(merged, spoof, self.assets, self.aliases), merged)

    def test_favorites_allow_verified_legacy_ids_while_basket_requires_hash(self):
        refs = ["retired", {"id": "retired"}, self.old, {"id": "retired", "sha256": "wrong"}]
        stars, notes, skipped = read_favorites({"format": FAVORITES_FORMAT, "items": refs,
                                              "notes": {"retired": "old note", "canonical": "current note"}}, self.assets, self.aliases)
        self.assertEqual((stars, notes, skipped), ({"canonical"}, {"canonical": "current note"}, 1))
        _, stars, skipped = read_review({"format": REVIEW_FORMAT, "items": [], "favorites": refs}, self.assets, self.aliases)
        self.assertEqual((stars, skipped), ({"canonical"}, 1))
        basket, skipped = read_basket({"format": EXPORT_FORMAT, "items": refs}, self.assets, self.aliases)
        self.assertEqual((basket, skipped), ({"canonical"}, 3))
        record = basket_payload(self.assets, basket)["items"][0]
        self.assertEqual((record["id"], record["sha256"]), ("canonical", "a" * 64))
        self.assertEqual(read_review({"format": REVIEW_FORMAT, "items": [], "favorites": [{"id": "canonical"}]}, self.assets)[2], 1)

    def test_old_validation_stays_in_raw_backup_and_never_becomes_canonical_evidence(self):
        old = {**self.old, "validationEvidence": {"target": {"assetID": "retired", "sha256": "b" * 64}, "status": "pass"},
               "unknownProviderField": {"keep": [1, None, "raw"]}}
        assessment = {"id": "validation-1", "target": {"assetID": "retired", "sha256": "b" * 64}, "status": "pass"}
        payload = {"format": REVIEW_FORMAT, "items": [old, self.current],
                   "validationEvidence": {"format": "cfa-reference-validation-v1", "schemaVersion": 1,
                                          "assessments": [assessment], "legacyReviewArchive": [{"id": "missing", "sha256": "d" * 64}]},
                   "sceneReviews": [{"project": "hon", "shotID": "S01", "status": "needs_fixes", "note": "Motion"}]}
        before = copy.deepcopy(payload)
        imported, _, _ = read_review(payload, self.assets, self.aliases)
        self.assertNotIn("validationEvidence", imported["canonical"])
        provenance = review_provenance(payload)
        exported = review_payload(self.assets, imported, {"canonical"}, {"canonical"}, provenance=provenance)
        self.assertNotIn("validationEvidence", exported["items"][0])
        self.assertNotIn("_visualAliasSource", exported["items"][0])
        self.assertIn(old, exported["validationEvidence"]["legacyReviewArchive"])
        self.assertEqual(exported["validationEvidence"]["assessments"], [assessment])
        self.assertEqual(exported["sceneReviews"], payload["sceneReviews"])
        self.assertEqual(review_provenance(payload, provenance), provenance)
        self.assertEqual(sweep_payload(self.assets, imported, set(), set(), provenance=provenance)["validationEvidence"], provenance["validationEvidence"])
        restored = read_review(exported, self.assets, self.aliases)[0]
        self.assertIsNone(restored["canonical"]["shotPlan"])
        self.assertEqual(payload, before)

    def test_seed_provenance_preserves_retired_reviews_and_catalog_evidence(self):
        data = {"reviewDecisions": [self.current, self.old],
                "referenceValidation": {"assessments": [{"id": "evidence", "target": {"assetID": "retired", "sha256": "b" * 64}}]}}
        provenance = review_provenance(data)
        self.assertEqual(provenance["validationEvidence"]["legacyReviewArchive"], data["reviewDecisions"])
        self.assertEqual(provenance["validationEvidence"]["assessments"], data["referenceValidation"]["assessments"])
        self.assertEqual(review_provenance(data, provenance), provenance)

    def test_evidence_conflicts_are_atomic_and_unknown_envelopes_are_preserved(self):
        source = {"validationEvidence": {"format": "cfa-reference-validation-v1", "schemaVersion": 1,
                                         "assessments": [{"id": "evidence", "status": "fail"}]}}
        existing = review_provenance(source)
        before = copy.deepcopy(existing)
        with self.assertRaisesRegex(ValueError, "Conflicting immutable evidence ID"):
            review_provenance({"validationEvidence": {**source["validationEvidence"], "assessments": [{"id": "evidence", "status": "pass"}]}}, existing)
        self.assertEqual(existing, before)
        unknown = {"format": "future-v10", "complete": ["do not discard"]}
        backup = review_provenance({"validationEvidence": unknown}, existing)
        self.assertEqual(json.loads(backup["validationEvidence"]["unreadBackups"][0]["raw"]), unknown)
        self.assertEqual(backup["validationEvidence"]["assessments"], before["validationEvidence"]["assessments"])
        future_fields = {**source["validationEvidence"], "futureContext": {"hash": "a" * 64}}
        backup = review_provenance({"validationEvidence": future_fields})
        self.assertEqual(json.loads(backup["validationEvidence"]["unreadBackups"][0]["raw"]), future_fields)


if __name__ == "__main__":
    unittest.main()
