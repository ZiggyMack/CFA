"""Regression checks for exact-byte inclusion and preserved user authority."""
import copy
import hashlib
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import crocodile_scene_intake as intake


ROOT = Path(__file__).resolve().parents[6]
HERE = Path(__file__).resolve().parent


class CrocodileIntakeTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = intake.load_crocodile_sources(ROOT)
        cls.source_catalog = json.loads((HERE / "catalog.js").read_text(encoding="utf-8").split("=", 1)[1].strip().rstrip(";"))

    def base_catalog(self):
        # Keep tests valid before and after this adapter is added to the build.
        catalog = copy.deepcopy(self.source_catalog)
        catalog["assets"] = [a for a in catalog["assets"] if a.get("sourceIntake") != intake.INTAKE_ID]
        new_ids = {"HD-CROC-" + r["sha256"][:20] for r in self.sources["records"]}
        catalog["albums"] = [a for a in catalog["albums"] if a["id"] not in {g[2] for g in intake.GROUPS}]
        group = next(g for g in catalog["castCollections"] if g["id"] == intake.COLLECTION_ID)
        for key, value in group.items():
            if isinstance(value, list):
                group[key] = [x for x in value if not isinstance(x, str) or x not in new_ids]
        for key in ["characterStudyIDs", "sceneStudyIDs", "revisionStudyIDs"]:
            group.pop(key, None)
        group["sourceAlbumIDs"] = [x for x in group["sourceAlbumIDs"] if x not in {g[2] for g in intake.GROUPS}]
        catalog.pop("crocodileIntake", None)
        return catalog

    def test_all_source_paths_verified_and_aliases_collapsed(self):
        self.assertEqual(self.sources["sourcePathCount"], 35)
        self.assertEqual(len(self.sources["records"]), 33)
        aliases = [r for r in self.sources["records"] if len(r["sourceAliases"]) > 1]
        self.assertEqual({r["filename"] for r in aliases}, {"E19-boss-dais-004-v001.jpg", "E19-boss-dais-015-v001.jpg"})
        self.assertTrue(all(r["humanAcceptance"] is None for r in self.sources["records"]))

    @patch.object(intake, "_preview", return_value=(1280, 720))
    def test_additive_and_idempotent_with_selected_anchor_unchanged(self, preview):
        catalog = self.base_catalog()
        before_assets = copy.deepcopy(catalog["assets"])
        before_groups = copy.deepcopy(catalog["castCollections"])
        group_before = next(g for g in before_groups if g["id"] == intake.COLLECTION_ID)
        added = intake.apply_crocodile_intake(catalog, ROOT)
        self.assertEqual(len(added), 33)
        self.assertEqual(catalog["assets"][:len(before_assets)], before_assets)
        group = next(g for g in catalog["castCollections"] if g["id"] == intake.COLLECTION_ID)
        for key in ["coverID", "representativeID", "currentIDs", "workingReferenceIDs", "historyIDs", "preferredIDs"]:
            self.assertEqual(group[key], group_before[key], key)
        self.assertEqual(len(group["characterStudyIDs"]), 15)
        self.assertEqual(len(group["sceneStudyIDs"]), 15)
        self.assertEqual(len(group["revisionStudyIDs"]), 3)
        self.assertEqual(len(group["sceneAssetIDs"]), 33)
        self.assertEqual([g for g in catalog["castCollections"] if g["id"] != intake.COLLECTION_ID], [g for g in before_groups if g["id"] != intake.COLLECTION_ID])
        after = copy.deepcopy(catalog)
        self.assertEqual(intake.apply_crocodile_intake(catalog, ROOT), [])
        self.assertEqual(catalog, after)

    @patch.object(intake, "_preview", return_value=(1280, 720))
    def test_exact_existing_asset_is_reused_without_review_mutation(self, preview):
        catalog = self.base_catalog()
        record = self.sources["records"][0]
        existing = {"id": "EXISTING-CROCODILE", "sha256": record["sha256"], "project": "hon", "kind": "image", "category": "storyboard", "status": "needs_fixes", "rating": 2, "note": "User's existing note"}
        catalog["assets"].append(existing)
        saved = copy.deepcopy(existing)
        added = intake.apply_crocodile_intake(catalog, ROOT)
        self.assertEqual(len(added), 32)
        self.assertEqual(existing, saved)
        group = next(g for g in catalog["castCollections"] if g["id"] == intake.COLLECTION_ID)
        self.assertIn(existing["id"], group["characterStudyIDs"])
        self.assertEqual(catalog["crocodileIntake"]["records"][existing["id"]]["sha256"], record["sha256"])

    @patch.object(intake, "_preview", return_value=(1280, 720))
    def test_repairs_and_known_defects_remain_distinct(self, preview):
        catalog = self.base_catalog()
        intake.apply_crocodile_intake(catalog, ROOT)
        records = {r["filename"]: r for r in catalog["crocodileIntake"]["records"].values()}
        first = records["E19-boss-dais-004-v001.jpg"]
        second = records["E19-boss-dais-004-v002.jpg"]
        third = records["E19-boss-dais-004-v003.jpg"]
        self.assertEqual(first["supersededByAssetIDs"], [second["assetID"]])
        self.assertEqual(third["replacesAssetIDs"], [second["assetID"]])
        self.assertTrue(first["superseded"])
        self.assertFalse(third["superseded"])
        self.assertIn("eyepiece missing", json.dumps(second["buildAudit"]))
        self.assertIn("toad-like", " ".join(records["N08-counting-room-003.jpg"]["providerObservations"]))

    def test_changed_evidence_fails_before_mutation(self):
        catalog = self.base_catalog()
        before = copy.deepcopy(catalog)
        with patch.dict(intake.SOURCE_PINS, {next(iter(intake.SOURCE_PINS)): "0" * 64}):
            with self.assertRaisesRegex(ValueError, "source evidence changed"):
                intake.apply_crocodile_intake(catalog, ROOT)
        self.assertEqual(catalog, before)

    def test_source_media_hash_mismatch_is_rejected(self):
        real_read = Path.read_bytes

        def corrupt(path):
            data = real_read(path)
            return data + b"changed" if path.name == "E19-boss-dais-009.jpg" else data

        with patch.object(Path, "read_bytes", corrupt):
            with self.assertRaisesRegex(ValueError, "media differs from manifest"):
                intake.load_crocodile_sources(ROOT)


if __name__ == "__main__":
    unittest.main()
