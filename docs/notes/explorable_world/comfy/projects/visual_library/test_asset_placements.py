"""Exact-media placement regressions; fixtures are copies, never real review writes."""
import copy
import json
from pathlib import Path
import unittest

import asset_placements as placements


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
IDS = {"GEM-8B51108E", "GEM-92EF6FD7"}
SOURCE_ALBUM = "unassigned:video-needs_review"
DESTINATION = "hon:video-supporting_cast"
CHARACTER = "hon:cast-hooded"


class AssetPlacementTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((HERE / "catalog.js").read_text(encoding="utf-8").split("=", 1)[1].strip().rstrip(";"))
        inventory = json.loads((HERE.parent / "hon_dolo_strictly_business/gemini_review_20261007/inventory.json").read_text(encoding="utf-8"))
        cls.originals = {a["reference_id"]: a for a in inventory["items"] if a["reference_id"] in IDS}

    def base_catalog(self):
        # The same regression runs against either a pre- or post-placement build.
        catalog = copy.deepcopy(self.catalog)
        for asset in catalog["assets"]:
            if asset["id"] in IDS:
                original = self.originals[asset["id"]]
                recorded = asset.get("placement", {}).get("original")
                asset.update(recorded or {"project": "unassigned", "album": SOURCE_ALBUM,
                                          "title": original["title"], "note": original["review_notes"]})
                asset.pop("placement", None)
        for album in catalog["albums"]:
            album["assetIDs"] = [asset_id for asset_id in album["assetIDs"] if asset_id not in IDS]
        catalog["albums"] = [album for album in catalog["albums"] if album["id"] != SOURCE_ALBUM]
        catalog["albums"].append({"id": SOURCE_ALBUM, "project": "unassigned", "category": "videos",
                                  "title": "Needs Review videos", "description": "", "assetIDs": sorted(IDS)})
        group = next(g for g in catalog["castCollections"] if g["id"] == CHARACTER)
        for field in ["assetIDs", "videoAssetIDs"]:
            group[field] = [asset_id for asset_id in group.get(field, []) if asset_id not in IDS]
        return catalog

    def test_only_two_clips_move_without_changing_exact_media(self):
        catalog = self.base_catalog()
        before = {a["id"]: copy.deepcopy(a) for a in catalog["assets"]}
        placements.apply_asset_placements(catalog, ROOT)
        after = {a["id"]: a for a in catalog["assets"]}
        self.assertEqual(set(after), set(before), "No new or replacement asset IDs")
        self.assertEqual({asset_id for asset_id in after if after[asset_id] != before[asset_id]}, IDS)
        for asset_id in IDS:
            asset = after[asset_id]
            self.assertEqual(asset["project"], "hon")
            self.assertEqual(asset["album"], DESTINATION)
            self.assertEqual(asset["category"], "videos")
            for field in ["id", "sha256", "repoPath", "src", "thumb", "filename", "kind", "duration", "variant"]:
                self.assertEqual(asset.get(field), before[asset_id].get(field), field)
        self.assertFalse(any(a["project"] == "unassigned" for a in catalog["assets"]))

    def test_all_user_reviews_notes_and_the_saved_correction_plan_are_preserved(self):
        catalog = self.base_catalog()
        before = {key: copy.deepcopy(catalog[key]) for key in
                  ["reviewDecisions", "reviewRequests", "sceneReviews", "shotMaterials"] if key in catalog}
        saved = {r["id"]: copy.deepcopy(r) for r in catalog["reviewDecisions"] if r["id"] in IDS}
        self.assertEqual(len(saved), 2)
        self.assertEqual(saved["GEM-92EF6FD7"]["shotPlan"]["destinations"], ["Grok"])
        self.assertIn("comfy", saved["GEM-92EF6FD7"]["shotPlan"]["idea"].lower())
        self.assertTrue(all(r["status"] == "needs_fixes" and r["variant"] == "multiverse" for r in saved.values()))
        placements.apply_asset_placements(catalog, ROOT)
        for key, value in before.items():
            self.assertEqual(catalog[key], value, key)

    def test_destination_membership_is_additive_and_empty_source_album_is_removed(self):
        catalog = self.base_catalog()
        destination = next((a for a in catalog["albums"] if a["id"] == DESTINATION), None)
        if destination is None:
            destination = {"id": DESTINATION, "project": "hon", "category": "videos", "title": "Supporting cast videos",
                           "description": "Existing destination description", "assetIDs": []}
            catalog["albums"].append(destination)
        sentinel = next(a["id"] for a in catalog["assets"] if a["project"] == "hon" and a["kind"] == "video" and a["id"] not in IDS)
        destination["assetIDs"] = list(dict.fromkeys([*destination["assetIDs"], sentinel]))
        members = set(destination["assetIDs"])
        untouched = {a["id"]: copy.deepcopy(a) for a in catalog["albums"] if a["id"] not in {SOURCE_ALBUM, DESTINATION}}
        placements.apply_asset_placements(catalog, ROOT)
        after = {a["id"]: a for a in catalog["albums"]}
        self.assertNotIn(SOURCE_ALBUM, after)
        self.assertEqual(set(after[DESTINATION]["assetIDs"]), members | IDS)
        self.assertEqual(len(after[DESTINATION]["assetIDs"]), len(set(after[DESTINATION]["assetIDs"])))
        for album_id, value in untouched.items():
            self.assertEqual(after[album_id], value)

    def test_hub_gains_video_appearances_without_promoting_character_references(self):
        catalog = self.base_catalog()
        before = {g["id"]: copy.deepcopy(g) for g in catalog["castCollections"]}
        placements.apply_asset_placements(catalog, ROOT)
        after = {g["id"]: g for g in catalog["castCollections"]}
        group = after[CHARACTER]
        self.assertEqual(set(group["assetIDs"]), set(before[CHARACTER]["assetIDs"]) | IDS)
        self.assertEqual(set(group["videoAssetIDs"]), set(before[CHARACTER].get("videoAssetIDs", [])) | IDS)
        for field in ["coverID", "representativeID", "currentIDs", "workingReferenceIDs", "historyIDs", "enhancementRequest"]:
            self.assertEqual(group.get(field), before[CHARACTER].get(field), field)
        for group_id, value in before.items():
            if group_id != CHARACTER:
                self.assertEqual(after[group_id], value)

    def test_original_placement_is_recorded_and_reapplying_is_idempotent(self):
        catalog = self.base_catalog()
        before = {a["id"]: copy.deepcopy(a) for a in catalog["assets"] if a["id"] in IDS}
        placements.apply_asset_placements(catalog, ROOT)
        for asset in catalog["assets"]:
            if asset["id"] not in IDS:
                continue
            self.assertIsInstance(asset.get("placement"), dict)
            self.assertEqual(asset["placement"]["original"],
                             {field: before[asset["id"]][field] for field in ["project", "album", "title", "note"]})
            self.assertEqual(asset["placement"]["decisionID"], "ziggy-hooded-traveler-placement-20261028")
        once = copy.deepcopy(catalog)
        placements.apply_asset_placements(catalog, ROOT)
        self.assertEqual(catalog, once)

    def test_wrong_hash_in_second_assignment_fails_before_any_mutation(self):
        catalog = self.base_catalog()
        next(a for a in catalog["assets"] if a["id"] == "GEM-92EF6FD7")["sha256"] = "0" * 64
        before = copy.deepcopy(catalog)
        with self.assertRaises((ValueError, AssertionError)):
            placements.apply_asset_placements(catalog, ROOT)
        self.assertEqual(catalog, before, "Validate all assignments before changing the first clip")

    def test_unknown_asset_fails_before_any_mutation(self):
        catalog = self.base_catalog()
        catalog["assets"] = [a for a in catalog["assets"] if a["id"] != "GEM-92EF6FD7"]
        before = copy.deepcopy(catalog)
        with self.assertRaises((ValueError, AssertionError, KeyError)):
            placements.apply_asset_placements(catalog, ROOT)
        self.assertEqual(catalog, before)


if __name__ == "__main__":
    unittest.main()
