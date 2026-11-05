"""Grok video discovery must preserve exact media, evidence and human reviews."""
from copy import deepcopy
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import grok_video_home as home


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
IDS = {clip["id"] for clip in home.CLIPS}


class GrokVideoHomeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.catalog = json.loads((HERE / "catalog.js").read_text(encoding="utf-8").split("=", 1)[1].strip().rstrip(";"))

    def base_catalog(self):
        catalog = deepcopy(self.catalog)
        for asset in catalog["assets"]:
            if asset["id"] not in IDS:
                continue
            original = asset.pop("discoveryPlacement", {}).get("original")
            if original:
                asset.update(original)
            for key in ("provider", "sourceProvider", "sourcePackage", "characterCollectionID", "providerEvidence", "provenancePath"):
                asset.pop(key, None)
            asset["tags"] = ["metadata-intake", "GROK-VIDEO-TEST"]
        catalog["albums"] = [album for album in catalog["albums"] if album["id"] != home.VIDEO_ALBUM]
        group = next(group for group in catalog["castCollections"] if group["id"] == home.CHARACTER)
        group["videoAssetIDs"] = [asset_id for asset_id in group["videoAssetIDs"] if asset_id not in IDS]
        group["sourceAlbumIDs"] = [album_id for album_id in group["sourceAlbumIDs"] if album_id != home.VIDEO_ALBUM]
        return catalog

    def test_exact_pair_gets_one_video_home_without_new_assets_or_source_changes(self):
        catalog = self.base_catalog()
        before = {asset["id"]: deepcopy(asset) for asset in catalog["assets"]}
        self.assertEqual(set(home.apply_grok_video_home(catalog, ROOT)), IDS)
        after = {asset["id"]: asset for asset in catalog["assets"]}
        self.assertEqual(len(catalog["assets"]), len(before))
        self.assertEqual({asset_id for asset_id in before if before[asset_id] != after[asset_id]}, IDS)
        for clip in home.CLIPS:
            asset = after[clip["id"]]
            self.assertEqual((asset["category"], asset["album"], asset["sourceProvider"]), ("videos", home.VIDEO_ALBUM, "Grok"))
            self.assertEqual(asset["title"], clip["title"])
            for key in ("id", "sha256", "bytes", "repoPath", "src", "thumb", "filename", "kind", "sourceIntake", "sourceStatus"):
                self.assertEqual(asset.get(key), before[asset["id"]].get(key), key)
            self.assertEqual(sum(item.get("sha256") == clip["sha256"] for item in catalog["assets"]), 1)
        album = next(album for album in catalog["albums"] if album["id"] == home.VIDEO_ALBUM)
        self.assertEqual(set(album["assetIDs"]), IDS)

    def test_human_decisions_and_frozen_intake_stay_byte_equivalent(self):
        catalog = self.base_catalog()
        saved = {key: deepcopy(catalog[key]) for key in ("reviewDecisions", "reviewRequests", "sceneReviews", "shotMaterials", "reviewIntake") if key in catalog}
        original_album = deepcopy(next(album for album in catalog["albums"] if album["id"] == home.SOURCE_ALBUM))
        reviews = {review["id"]: review for review in catalog["reviewDecisions"] if review["id"] in IDS}
        self.assertEqual(set(reviews), IDS)
        for review in reviews.values():
            self.assertEqual((review["status"], review["likenessRating"], review["sceneQualityRating"]), ("keep", 5, 5))
        home.apply_grok_video_home(catalog, ROOT)
        for key, value in saved.items():
            self.assertEqual(catalog[key], value, key)
        self.assertEqual(next(album for album in catalog["albums"] if album["id"] == home.SOURCE_ALBUM), original_album)
        self.assertTrue(all(any(version.get("assetID") == asset_id for family in catalog["reviewIntake"]["families"] for version in family["versions"]) for asset_id in IDS))

    def test_chewy_video_appearances_are_additive_without_promoting_model_references(self):
        catalog = self.base_catalog()
        before = {group["id"]: deepcopy(group) for group in catalog["castCollections"]}
        home.apply_grok_video_home(catalog, ROOT)
        after = {group["id"]: group for group in catalog["castCollections"]}
        group = after[home.CHARACTER]
        self.assertEqual(set(group["videoAssetIDs"]), set(before[home.CHARACTER]["videoAssetIDs"]) | IDS)
        self.assertIn("GEM-24BA1AE7", group["videoAssetIDs"])
        self.assertEqual(len(group["videoAssetIDs"]), 3)
        self.assertEqual(len(group["workingReferenceIDs"]), 7)
        for key, value in before[home.CHARACTER].items():
            if key not in {"videoAssetIDs", "sourceAlbumIDs"}:
                self.assertEqual(group[key], value, key)
        for group_id in before:
            if group_id != home.CHARACTER:
                self.assertEqual(after[group_id], before[group_id])

    def test_provider_evidence_stays_historical_and_adapter_is_idempotent(self):
        catalog = self.base_catalog()
        home.apply_grok_video_home(catalog, ROOT)
        for asset in catalog["assets"]:
            if asset["id"] not in IDS:
                continue
            evidence = asset["providerEvidence"]
            self.assertEqual((evidence["reviewer"], evidence["status"]), ("Chief", "PRELIMINARY"))
            self.assertEqual(evidence["sha256"], home.REVIEW_SHA256)
            self.assertIn("not current provider controls", evidence["capabilityClaims"])
            self.assertEqual(asset["discoveryPlacement"]["original"]["album"], home.SOURCE_ALBUM)
        once = deepcopy(catalog)
        home.apply_grok_video_home(catalog, ROOT)
        self.assertEqual(catalog, once)

    def test_wrong_second_hash_aborts_before_first_asset_changes(self):
        catalog = self.base_catalog()
        next(asset for asset in catalog["assets"] if asset["id"] == home.CLIPS[1]["id"])["sha256"] = "0" * 64
        before = deepcopy(catalog)
        with self.assertRaisesRegex(ValueError, "identity changed"):
            home.apply_grok_video_home(catalog, ROOT)
        self.assertEqual(catalog, before)

    def test_changed_source_bytes_or_provider_evidence_aborts_without_mutation(self):
        original_read = Path.read_bytes
        for relative in (home.REVIEW_PATH, home.SOURCE_BASE + "/" + home.CLIPS[1]["filename"]):
            with self.subTest(relative=relative):
                catalog = self.base_catalog()
                before = deepcopy(catalog)
                target = ROOT / relative
                def read(path):
                    raw = original_read(path)
                    return raw + b"changed" if path == target else raw
                with patch.object(Path, "read_bytes", read), self.assertRaises(ValueError):
                    home.apply_grok_video_home(catalog, ROOT)
                self.assertEqual(catalog, before)


if __name__ == "__main__":
    unittest.main()
