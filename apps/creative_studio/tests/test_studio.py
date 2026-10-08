"""Focused checks for portable review behavior; no generation or network calls."""

import copy
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_DIR))
from library_helpers import FAVORITES_FORMAT, favorite_payload, media_path, ordered_assets, read_favorites


class LibraryHelpersTest(unittest.TestCase):
    def test_media_cannot_escape_bundle_or_be_a_remote_url(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "photo one.jpg").write_bytes(b"fixture")
            self.assertEqual(media_path(root, "photo%20one.jpg"), root / "photo one.jpg")
            for invalid in ("../outside.jpg", "https://example.com/a.jpg", "//server/share.jpg",
                            "D:/private/photo.jpg", r"D:\private\photo.jpg", "missing.jpg"):
                self.assertIsNone(media_path(root, invalid), invalid)

    def test_album_order_and_membership_override_primary_category(self):
        assets = [{"id": key, "project": "lisan", "kind": "image", "category": "inspiration", "title": key}
                  for key in ("stencil", "portrait", "neck")]
        albums = [{"id": "placements", "project": "lisan", "category": "details", "assetIDs": ["portrait", "neck"]},
                  {"id": "stencils", "project": "lisan", "category": "details", "assetIDs": ["stencil", "portrait"]}]
        ordered = ordered_assets(assets, albums, "lisan", "details")
        self.assertEqual([a["id"] for a, _ in ordered], ["portrait", "neck", "stencil"])
        self.assertEqual([a["id"] for a, _ in ordered_assets(assets, albums, "lisan", "details", query="neck")], ["neck"])

    def test_favorites_round_trip_does_not_change_approval(self):
        assets = [{"id": "one", "sha256": "abc", "project": "hon", "sourceStatus": "needs_review"},
                  {"id": "two", "sha256": "def", "project": "lisan"}]
        before = copy.deepcopy(assets)
        payload = favorite_payload(assets, {"one"}, {"two": "Use the neck placement."})
        self.assertEqual(payload["format"], FAVORITES_FORMAT)
        self.assertEqual(read_favorites(payload, assets), ({"one"}, {"two": "Use the neck placement."}, 0))
        self.assertEqual(assets, before)
        payload["items"][0]["sha256"] = "different"
        payload["note_refs"]["two"] = "different"
        self.assertEqual(read_favorites(payload, assets), (set(), {}, 1))

    def test_legacy_export_without_notes_and_unknown_ids(self):
        payload = {"format": FAVORITES_FORMAT, "items": [{"id": "one"}, {"id": "gone"}]}
        self.assertEqual(read_favorites(payload, [{"id": "one", "sha256": "abc"}]), ({"one"}, {}, 1))
        with self.assertRaises(ValueError):
            read_favorites({"items": []}, [])


class StudioAppTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from PIL import Image
        from streamlit.testing.v1 import AppTest
        cls.AppTest = AppTest
        cache = APP_DIR.parents[1] / ".cache"
        cache.mkdir(exist_ok=True)
        cls.temp = tempfile.TemporaryDirectory(prefix="studio-test-", dir=cache)
        cls.app_dir = Path(cls.temp.name)
        for name in ("app.py", "library_helpers.py"):
            shutil.copy2(APP_DIR / name, cls.app_dir / name)
        library = cls.app_dir / "library"
        library.mkdir()
        Image.new("RGB", (20, 12), "#176b62").save(library / "review.jpg")
        images = [{"id": f"hon-{i:02}", "project": "hon", "kind": "image", "category": "outfits",
                   "album": "hon:outfits", "title": f"Look {i:02}", "filename": f"look-{i:02}.jpg",
                   "src": "review.jpg", "thumb": "review.jpg", "sha256": f"hash-{i}"} for i in range(26)]
        images += [{"id": "SB-01", "project": "hon", "kind": "image", "category": "storyboard",
                    "album": "hon:story", "title": "SB-01 · Count it twice", "filename": "sb-01.jpg",
                    "src": "review.jpg", "thumb": "review.jpg", "lyric": "Strictly business. Count it twice.",
                    "beat": "The opening bargain."},
                   {"id": "lisan-neck", "project": "lisan", "kind": "image", "category": "details",
                    "album": "lisan:placement", "title": "Neck placement", "filename": "neck.jpg",
                    "src": "review.jpg", "thumb": "review.jpg"}]
        documents = [{"id": "gemini-doc", "project": "hon", "kind": "document", "category": "documents",
                      "album": "Gemini instructions and image maps", "filename": "gemini_instructions.txt",
                      "title": "Gemini instructions", "text": "Preserve the supplied character references."},
                     {"id": "flow-doc", "project": "hon", "kind": "document", "category": "documents",
                      "album": "Collaborator briefs · Flow", "filename": "flow_brief.txt",
                      "title": "Flow brief", "text": "Keep the selected shot continuous."}]
        catalog = {"projects": [{"id": "hon", "name": "Hon Dolo", "subtitle": "Strictly Business"},
                                 {"id": "lisan", "name": "Lisan Al Gaib", "subtitle": "Meta Mirror"},
                                 {"id": "unassigned", "name": "Unassigned", "subtitle": "To place"}],
                   "assets": images + documents,
                   "categories": [["outfits", "Outfits"], ["details", "Tattoos & piercings"], ["storyboard", "Storyboard"]],
                   "albums": [{"id": "hon:outfits", "project": "hon", "category": "outfits", "title": "Outfits",
                               "assetIDs": [a["id"] for a in images[:26]]},
                              {"id": "hon:story", "project": "hon", "category": "storyboard", "title": "Pay me first", "assetIDs": ["SB-01"]},
                              {"id": "lisan:placement", "project": "lisan", "category": "details", "title": "Placement portraits", "assetIDs": ["lisan-neck"]}]}
        (library / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def app(self):
        app = self.AppTest.from_file(str(self.app_dir / "app.py"), default_timeout=15).run()
        self.assertFalse(app.exception)
        return app

    def test_pagination_selection_and_session_notes(self):
        app = self.app()
        self.assertEqual(len([b for b in app.button if b.key.startswith("open:")]), 24)
        next(b for b in app.button if b.label == "Next →").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(len([b for b in app.button if b.key.startswith("open:")]), 3)
        app.button(key="open:hon-24").click().run()
        self.assertFalse(app.exception)
        app.button(key="favorite:selected:hon-24").click().run()
        app.text_area(key="asset-note:hon-24").input("Keep this coat.").run()
        self.assertIn("hon-24", app.session_state["studio_favorites"])
        self.assertEqual(app.session_state["studio_notes"]["hon-24"], "Keep this coat.")
        app.button(key="nav:Favorites & notes").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(len([b for b in app.button if b.key.startswith("open:")]), 1)

    def test_storyboard_and_collaborator_kits(self):
        app = self.app()
        app.button(key="nav:Storyboard").click().run()
        self.assertFalse(app.exception)
        self.assertTrue(any("Pay me first" in item.value for item in app.subheader))
        self.assertEqual(len([b for b in app.button if b.key.startswith("open:")]), 1)
        app.button(key="nav:Collaborator kits").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.code), 2)
        self.assertTrue(any("Flow" in item.value for item in app.subheader))

    def test_project_switch_and_empty_project(self):
        app = self.app()
        app.selectbox(key="studio_project").select("lisan").run()
        self.assertFalse(app.exception)
        self.assertEqual(len([b for b in app.button if b.key.startswith("open:")]), 1)
        self.assertTrue(any("Placement portraits" in item.value for item in app.subheader))
        app.selectbox(key="studio_project").select("unassigned").run()
        self.assertFalse(app.exception)
        self.assertTrue(app.info)


if __name__ == "__main__":
    unittest.main()
