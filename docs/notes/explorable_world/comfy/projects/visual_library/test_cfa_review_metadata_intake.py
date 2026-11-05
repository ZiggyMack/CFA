"""Integrity and decision-boundary tests for the frozen r002 handoff adapter."""
import copy
from collections import Counter
import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from cfa_review_metadata_intake import (
    IntakeError, _Intake, _under, load_review_metadata_intake, verify_manifest,
)


class IntakeBoundariesTest(unittest.TestCase):
    def test_manifest_verifies_bytes_and_rejects_changes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            package = root / "package"
            package.mkdir()
            media = package / "image.jpg"
            media.write_bytes(b"first")
            digest = hashlib.sha256(b"first").hexdigest()
            manifest = package / "SHA256SUMS"
            manifest.write_text(f"{digest}  image.jpg\n", encoding="utf-8")
            pinned = hashlib.sha256(manifest.read_bytes()).hexdigest()
            self.assertEqual(verify_manifest(root, package, manifest.name, pinned), {"package/image.jpg": digest})
            media.write_bytes(b"changed")
            with self.assertRaisesRegex(IntakeError, "mismatch"):
                verify_manifest(root, package, manifest.name, pinned)

    def test_paths_cannot_escape_repository_or_manifest_package(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            for path in ["../other.jpg", "C:/Users/name/private.jpg", "/tmp/other.jpg"]:
                with self.subTest(path=path), self.assertRaises(IntakeError):
                    _under(root, path)
            self.assertEqual(_under(root, r"D:\Documents\CFA\a\b.jpg"), root / "a" / "b.jpg")
            package = root / "package"
            package.mkdir()
            (root / "secret").write_bytes(b"outside package")
            sha = hashlib.sha256(b"outside package").hexdigest()
            manifest = package / "SHA256SUMS"
            manifest.write_text(f"{sha}  ../secret\n", encoding="utf-8")
            with self.assertRaisesRegex(IntakeError, "escapes package"):
                verify_manifest(root, package, manifest.name, hashlib.sha256(manifest.read_bytes()).hexdigest())

    def test_exact_hash_reuses_ids_without_mutating_human_reviews(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "image.jpg").write_bytes(b"image")
            sha = hashlib.sha256(b"image").hexdigest()
            existing = [{"id": "USER-KEPT", "project": "hon", "sha256": sha,
                         "userKeep": True, "likenessRating": 2, "workingReference": {"status": "approved"}}]
            before = copy.deepcopy(existing)
            intake = _Intake(root, existing)
            family = intake.family("test", "frame", "hon", "category")
            version = intake.version(family, sha, ["image.jpg"], "image.jpg", "original", {"verdict": "PASS"})
            self.assertEqual(version["assetID"], "USER-KEPT")
            self.assertEqual(existing, before)
            self.assertEqual(intake.new, {})
            self.assertEqual(family["humanAcceptance"], None)
            self.assertEqual(family["siteValidation"], "not_performed")

    def test_history_and_placeholders_do_not_become_gallery_assets(self):
        with tempfile.TemporaryDirectory() as directory:
            intake = _Intake(directory, [])
            family = intake.family("test", "frame", "hon", "category")
            sha = "a" * 64
            intake.version(family, sha, [], "old.jpg", "repair", availability="deferred_history", required=False)
            intake.candidate(family, sha, "provider unresolved pointer")
            self.assertIsNone(family["currentCandidate"])
            self.assertEqual(family["providerFinalPointer"]["availability"], "deferred_history")
            intake.version(family, None, [], "placeholder", "original", availability="declared_not_on_disk", required=False)
            self.assertEqual(intake.new, {})
            self.assertTrue(all(v["assetID"] is None for v in family["versions"]))

    def test_delivered_without_a_path_fails_instead_of_silently_dropping(self):
        with tempfile.TemporaryDirectory() as directory:
            intake = _Intake(directory, [])
            family = intake.family("test", "frame", "hon", "category")
            with self.assertRaisesRegex(IntakeError, "no explicit local path"):
                intake.version(family, "a" * 64, [], "image.jpg", "original")


class FrozenR002IntegrationTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.root = next(parent for parent in Path(__file__).resolve().parents if (parent / "AGENTS.md").is_file())
        library = Path(__file__).parent
        text = (library / "catalog.js").read_text(encoding="utf-8")
        catalog = json.loads(text[text.index("{"):].rstrip().removesuffix(";"))
        cls.assets = catalog["assets"]
        before = copy.deepcopy(cls.assets)
        cls.data = load_review_metadata_intake(cls.root, cls.assets)
        if cls.assets != before:
            raise AssertionError("Adapter mutated existing catalog assets")
        cls.families = {f["id"]: f for f in cls.data["families"]}

    def test_all_authoritative_rows_are_accounted_for(self):
        counts = self.data["summary"]["datasets"]
        self.assertEqual(counts["GROK-HD-FALCON-1000"],
                         {"families": 1229, "versions": 1441, "available": 1297, "deferred_history": 144})
        self.assertEqual(counts["LAG-1K"],
                         {"families": 1000, "versions": 1070, "available": 1067, "declared_not_on_disk": 3})
        self.assertEqual(counts["GROK-VIDEO-TEST"]["available"], 2)
        self.assertEqual(len(self.data["packages"]), 9)
        self.assertEqual(sum(p["verifiedFileCount"] for p in self.data["packages"]), 493)

    def test_preserves_unknown_falcon_edit_bases(self):
        repairs = [v for f in self.data["families"] if f["dataset"] == "GROK-HD-FALCON-1000"
                   for v in f["versions"] if v["role"] == "repair"]
        self.assertEqual(len(repairs), 212)
        self.assertEqual(sum(v["lineage"]["baseSha256"] is None for v in repairs), 91)
        self.assertTrue(all(v["lineage"]["donorSha256s"] is None for v in repairs))

    def test_stale_and_unavailable_final_pointers_do_not_become_current_candidates(self):
        falcon = [f for f in self.data["families"] if f["dataset"] == "GROK-HD-FALCON-1000"]
        unavailable = [f for f in falcon if f.get("providerFinalPointer", {}).get("availability") == "deferred_history"]
        self.assertEqual(len(unavailable), 3)
        self.assertTrue(all(f["currentCandidate"] is None for f in unavailable))
        for family in falcon:
            if family["currentCandidate"]:
                version = next(v for v in family["versions"] if v["sha256"] == family["currentCandidate"]["sha256"])
                self.assertEqual(version["providerReview"]["stage"], "current pass (scoped)")
                self.assertEqual(version["availability"], "available")

    def test_r002_lisan_corrections_override_old_lineage_labels(self):
        family = self.families["LAG-1K:C37-06_Z_4_FAIL"]
        alternate = next(v for v in family["versions"] if v["sha256"].startswith("a07407f4"))
        self.assertTrue(alternate["providerReview"]["stage"].startswith("ALTERNATE_V_PASS_NOT_SHIPPED"))
        self.assertTrue(family["currentCandidate"]["sha256"].startswith("45775acd"))
        self.assertTrue(all(v["lineage"].get("baseSha256") for v in family["versions"] if v["role"] == "repair"))

    def test_lisan_donor_confidence_stays_separate_from_edit_base_confidence(self):
        lineage = [v["lineage"] for f in self.data["families"] if f["dataset"] == "LAG-1K"
                   for v in f["versions"] if v["role"] == "repair"]
        self.assertEqual(Counter(v["donorConfidence"] for v in lineage),
                         {"INFERRED_FROM_METHOD": 12, "UNKNOWN": 35, "NONE_REQUIRED": 23})
        self.assertEqual(Counter(v["parentConfidence"] for v in lineage),
                         {"LOGGED": 62, "UNKNOWN": 5, "INFERRED_FROM_METHOD": 3})
        self.assertTrue(all(v["baseConfidence"] == v["parentConfidence"] == v["confidence"] for v in lineage))

    def test_chin_v006_uses_original_base_not_superseded_v005(self):
        family = self.families["LAG-VIS-NATURAL:VIS-LAG-13_KISS-PUCKER"]
        current = next(v for v in family["versions"] if v["sha256"].startswith("b1a0f3f0"))
        old = next(v for v in family["versions"] if v["sha256"].startswith("dcd76223"))
        self.assertEqual(current["providerReview"]["verdict"], "PASS")
        self.assertEqual(current["lineage"]["baseSha256"], family["original"]["sha256"])
        self.assertNotEqual(current["lineage"]["baseSha256"], old["sha256"])
        self.assertEqual(old["availability"], "deferred_history")

    def test_new_assets_stay_outside_review_queue_and_carry_no_approval_fields(self):
        forbidden = {"userKeep", "likenessRating", "sceneQualityRating", "workingReference", "storyboardStage"}
        for asset in self.data["newAssets"]:
            self.assertFalse(forbidden.intersection(asset))
            self.assertEqual(asset["category"], "intake")
            self.assertTrue((self.root / asset["repoPath"]).is_file())
            self.assertEqual(len(asset["sha256"]), 64)
        for family in self.data["families"]:
            self.assertIsNone(family["humanAcceptance"])
            self.assertEqual(family["siteValidation"], "not_performed")

    def test_existing_content_ids_are_preserved_and_source_metadata_is_bounded(self):
        by_hash = {}
        for asset in self.assets:
            if asset.get("sha256"):
                by_hash.setdefault(asset["sha256"], set()).add(asset["id"])
        for family in self.data["families"]:
            for version in family["versions"]:
                if version["availability"] == "available" and version["sha256"] in by_hash:
                    self.assertIn(version["assetID"], by_hash[version["sha256"]])
        self.assertTrue(all(set(meta) == {"familyIDs", "sha256"} for meta in self.data["assetMetadata"].values()))
        self.assertLess(len(json.dumps(self.data).encode()), 15_000_000)


if __name__ == "__main__":
    unittest.main()
