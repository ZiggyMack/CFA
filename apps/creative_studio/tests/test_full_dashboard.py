"""Offline packaging checks for the full HTML mirror; no browser or server."""
import hashlib
import json
import os
import shutil
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

APP_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_DIR))
from build_full_dashboard import build, read_catalog, source_file


class FullDashboardBundleTest(unittest.TestCase):
    def setUp(self):
        cache = APP_DIR.parents[1] / ".cache"
        cache.mkdir(exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(prefix="full-dashboard-test-", dir=cache)
        self.root = Path(self.temp.name).resolve()
        assert self.root.is_relative_to(cache.resolve())
        self.source = self.root / "visual_library"
        self.source.mkdir()
        self.media = self.root / "original.jpg"
        self.media.write_bytes(b"test image bytes; image transforms are deliberately not performed")
        self.sha = hashlib.sha256(self.media.read_bytes()).hexdigest()
        self.doc = self.root / "notes.py"
        self.doc.write_text("# inert source\nprint('never execute this')\n", encoding="utf-8")
        self.catalog = {"projects": [{"id": "hon"}], "categories": [], "albums": [],
                        "assets": [{"id": "one", "project": "hon", "kind": "image", "src": "../original.jpg", "thumb": "../original.jpg", "sha256": self.sha},
                                   {"id": "two", "project": "hon", "kind": "image", "src": "../original.jpg", "sha256": self.sha},
                                   {"id": "doc", "project": "hon", "kind": "document", "src": "../notes.py"}],
                        "reviewDecisions": [{"id": "one", "sha256": self.sha, "workingReferenceScope": "detail", "note": "Keep tattoo only."}],
                        "missionControl": {"tasks": [{"id": "task", "links": [{"label": "Missing", "href": "../../outside.txt"},
                            {"label": "Source evidence", "href": "https://example.com/evidence"},
                            {"label": "Outfits", "href": "../index.html#hon/outfits"}]}]}}
        self.write_catalog()
        for name in ("library.js", "library.css"):
            (self.source / name).write_text("/* exact existing dashboard code */", encoding="utf-8")
        self.output = self.root / "bundle"

    def tearDown(self):
        self.temp.cleanup()

    def write_catalog(self):
        (self.source / "catalog.js").write_text("window.REVIEW_CATALOG=" + json.dumps(self.catalog) + ";", encoding="utf-8")

    def snapshot(self, result):
        return self.output / "snapshots" / result["buildID"]

    def test_hardlink_bundle_preserves_every_asset_review_and_source(self):
        before = self.media.read_bytes()
        result = build(self.source, self.output, self.root)
        snapshot = self.snapshot(result)
        packaged = read_catalog((snapshot / "catalog.js").read_bytes())
        self.assertEqual([a["id"] for a in packaged["assets"]], ["one", "two", "doc"])
        self.assertEqual(packaged["reviewDecisions"], self.catalog["reviewDecisions"])
        self.assertEqual(packaged["assets"][0]["src"], packaged["assets"][1]["src"])
        self.assertTrue(os.path.samefile(self.media, snapshot / packaged["assets"][0]["src"]))
        self.assertEqual(self.media.read_bytes(), before)
        self.assertEqual(result["additionalMediaBytes"], 0)
        self.assertEqual(result["fileCount"], 2)
        self.assertEqual((snapshot / "library.js").read_bytes(), (self.source / "library.js").read_bytes())
        self.assertTrue(packaged["assets"][2]["src"].endswith(".txt"))
        self.assertEqual(len(result["unresolvedPreparedLinks"]), 1)
        self.assertNotIn("href", packaged["missionControl"]["tasks"][0]["links"][0])
        self.assertEqual(packaged["missionControl"]["tasks"][0]["links"][1]["href"], "https://example.com/evidence")
        self.assertEqual(packaged["missionControl"]["tasks"][0]["links"][2]["href"], "index.html#hon/outfits")
        self.assertEqual(build(self.source, self.output, self.root)["buildID"], result["buildID"])

    def test_portable_copy_is_explicit_and_independent(self):
        result = build(self.source, self.output, self.root, copy_media=True)
        snapshot = self.snapshot(result)
        packaged = read_catalog((snapshot / "catalog.js").read_bytes())
        target = snapshot / packaged["assets"][0]["src"]
        self.assertFalse(os.path.samefile(self.media, target))
        self.assertEqual(target.read_bytes(), self.media.read_bytes())
        self.assertGreater(result["additionalMediaBytes"], 0)

    def test_hash_failure_does_not_publish_partial_build(self):
        first = build(self.source, self.output, self.root)
        current_before = (self.output / "current.json").read_bytes()
        self.catalog["assets"][0]["sha256"] = "wrong"
        self.write_catalog()
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            build(self.source, self.output, self.root)
        self.assertEqual((self.output / "current.json").read_bytes(), current_before)

    def test_no_path_escape_remote_url_or_code_evaluation(self):
        for value in ("../../outside.txt", "https://example.com/asset.jpg", "file:///D:/secret.txt", "../original.jpg?query=1"):
            with self.assertRaises(ValueError):
                source_file(value, self.source, self.root)
        with self.assertRaises(ValueError):
            read_catalog(b"alert('not a catalog')")
        with self.assertRaises(ValueError):
            build(self.source, self.root.parent / "escape", self.root)

    def context_pack_fixture(self):
        prefix = "docs/notes/explorable_world/comfy/projects/collaborators/project_context_packs_20261010/"
        values = {"UPLOAD_MAP.txt": b"Choose a recipient and read its loading guide.",
                  "all.zip": b"All prepared pack transport bytes.",
                  "deepseek/00_LOAD_FIRST.txt": b"DeepSeek loading order and dated route.",
                  "deepseek.zip": b"DeepSeek prepared transport bytes."}
        records = []
        for name, data in values.items():
            target = self.root / (prefix + name)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
            records.append({"path": prefix + name, "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
        # A nearby repository file is never added simply because the folder exists.
        (self.root / prefix / "not_opted_in.txt").write_bytes(b"Unlisted private working note.")
        index = {"schemaVersion": 1, "status": "prepared_not_delivered", "releaseID": "test", "files": records,
                 "uploadMapPath": prefix + "UPLOAD_MAP.txt", "allPacksZipPath": prefix + "all.zip",
                 "packs": [{"recipientID": "deepseek", "loadGuidePath": prefix + "deepseek/00_LOAD_FIRST.txt",
                            "zipPath": prefix + "deepseek.zip"}]}
        self.catalog["projectContextPacks"] = index
        self.write_catalog()
        return index

    def test_context_packs_package_only_explicit_hash_verified_links(self):
        index = self.context_pack_fixture()
        result = build(self.source, self.output, self.root)
        snapshot = self.snapshot(result)
        packaged = read_catalog((snapshot / "catalog.js").read_bytes())["projectContextPacks"]
        self.assertEqual(packaged["uploadMapPath"], index["uploadMapPath"])
        for owner, href, path_key in [(packaged, "uploadMapHref", "uploadMapPath"),
                                      (packaged, "allPacksZipHref", "allPacksZipPath"),
                                      (packaged["packs"][0], "loadGuideHref", "loadGuidePath"),
                                      (packaged["packs"][0], "zipHref", "zipPath")]:
            self.assertTrue(owner[href].startswith("media/"))
            self.assertEqual((snapshot / owner[href]).read_bytes(), (self.root / owner[path_key]).read_bytes())
        self.assertEqual(result["fileCount"], 6)
        source_paths = [name for entry in result["files"] for name in entry["sourcePaths"]]
        self.assertFalse(any(name.endswith("not_opted_in.txt") for name in source_paths))
        self.assertEqual(packaged["status"], "prepared_not_delivered")

    def test_context_pack_missing_or_changed_source_does_not_publish(self):
        index = self.context_pack_fixture()
        build(self.source, self.output, self.root)
        current_before = (self.output / "current.json").read_bytes()
        guide = self.root / index["packs"][0]["loadGuidePath"]
        original = guide.read_bytes()
        # Replace atomically: the previous snapshot may hardlink the source.
        temporary = guide.with_suffix(".tmp")
        temporary.write_bytes(b"X" + original[1:])
        temporary.replace(guide)
        with self.assertRaisesRegex(ValueError, "hash mismatch"):
            build(self.source, self.output, self.root)
        self.assertEqual((self.output / "current.json").read_bytes(), current_before)
        guide.unlink()
        with self.assertRaisesRegex(ValueError, "Missing"):
            build(self.source, self.output, self.root)
        self.assertEqual((self.output / "current.json").read_bytes(), current_before)

    def test_context_pack_paths_and_provenance_cannot_expand_served_scope(self):
        index = self.context_pack_fixture()
        index["uploadMapPath"] = "../original.jpg"
        index["files"].append({"path": "../original.jpg", "sha256": self.sha, "bytes": self.media.stat().st_size})
        self.write_catalog()
        with self.assertRaisesRegex(ValueError, "Unsafe project context pack path"):
            build(self.source, self.output, self.root)
        index = self.context_pack_fixture()
        index["files"] = index["files"][1:]
        self.write_catalog()
        with self.assertRaisesRegex(ValueError, "Unverified project context pack link"):
            build(self.source, self.output, self.root)
        index = self.context_pack_fixture()
        index["files"][0]["bytes"] += 1
        self.write_catalog()
        with self.assertRaisesRegex(ValueError, "size mismatch"):
            build(self.source, self.output, self.root)

    def studio_fixture(self):
        studio = self.root / "studio"
        pages = studio / "pages"
        pages.mkdir(parents=True)
        (studio / "app.py").write_text("import streamlit as st\nst.title('Existing compact studio')\n", encoding="utf-8")
        shutil.copyfile(APP_DIR / "pages/01_Full_Visual_Library.py", pages / "01_Full_Visual_Library.py")
        shutil.copyfile(APP_DIR / "full_dashboard_component.py", studio / "full_dashboard_component.py")
        return studio

    def test_multipage_component_registers_without_changing_compact_page(self):
        from streamlit.testing.v1 import AppTest
        from streamlit.runtime.pages_manager import PagesManager
        studio = self.studio_fixture()
        self.assertFalse((studio / "library/design_catalog.json").exists())
        build(self.source, studio / "full_dashboard_bundle", self.root)
        # Streamlit caches pages-directory discovery process-wide. Earlier
        # AppTest.from_string fixtures can set False even though this app has pages.
        with patch.object(PagesManager, "uses_pages_directory", None):
            app = AppTest.from_file(str(studio / "app.py"), default_timeout=20).run()
            self.assertFalse(app.exception)
            self.assertEqual(app.title[0].value, "Existing compact studio")
            app.switch_page("pages/01_Full_Visual_Library.py").run()
            self.assertFalse(app.exception)
            self.assertEqual(app.title[0].value, "Full visual library")
            self.assertEqual(len(app.get("component_instance")), 1)
            self.assertNotIn("studio_view", app.session_state)
            self.assertFalse((studio / "library/design_catalog.json").exists())

    def test_prepared_mirror_takes_priority_over_native_catalog_and_preserves_reviews(self):
        from streamlit.testing.v1 import AppTest
        from streamlit.runtime.pages_manager import PagesManager
        studio = self.studio_fixture()
        (studio / "library").mkdir()
        (studio / "library/design_catalog.json").write_text('{"assets": []}', encoding="utf-8")
        # A design catalog no longer silently redirects the full mirror to native.
        build(self.source, studio / "full_dashboard_bundle", self.root)
        with patch.object(PagesManager, "uses_pages_directory", None):
            app = AppTest.from_file(str(studio / "app.py"), default_timeout=20).run()
            app.session_state.studio_view = "Favorites & notes"
            app.session_state.studio_selected = "one"
            app.session_state.studio_reviews = {"one": {"status": "needs_fixes", "note": "Keep this decision"}}
            app.session_state.studio_favorites = {"one"}
            app.session_state.studio_project = "lisan"
            app.switch_page("pages/01_Full_Visual_Library.py").run()
            self.assertFalse(app.exception)
            self.assertEqual(app.title[0].value, "Full visual library")
            self.assertEqual(app.session_state.studio_view, "Favorites & notes")
            self.assertEqual(app.session_state.studio_selected, "one")
            self.assertEqual(app.session_state.studio_reviews, {"one": {"status": "needs_fixes", "note": "Keep this decision"}})
            self.assertEqual(app.session_state.studio_favorites, {"one"})
            self.assertEqual(app.session_state.studio_project, "lisan")
            self.assertEqual(len(app.get("component_instance")), 1)
            self.assertFalse(app.info)

    def test_absent_native_and_mirror_catalogs_keep_missing_package_message(self):
        from streamlit.testing.v1 import AppTest
        from streamlit.runtime.pages_manager import PagesManager
        studio = self.studio_fixture()
        with patch.object(PagesManager, "uses_pages_directory", None):
            app = AppTest.from_file(str(studio / "app.py"), default_timeout=20).run()
            app.switch_page("pages/01_Full_Visual_Library.py").run()
            self.assertFalse(app.exception)
            self.assertEqual(app.title[0].value, "Full visual library")
            self.assertIn("has not been prepared", app.info[0].value)
            self.assertNotIn("studio_view", app.session_state)
            self.assertEqual(len(app.get("component_instance")), 0)


if __name__ == "__main__":
    unittest.main()
