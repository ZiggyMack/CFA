"""Purpose browsing uses explicit metadata and leaves design/review records intact."""
import copy
import json
import sys
import unittest
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP))
from design_view import ALL_FILES_PURPOSES, all_files_model
import test_casa_casting as casting_tests


class AllFilesModelTests(unittest.TestCase):
    def test_metadata_only_groups_future_outfits_and_preserves_every_record(self):
        data = casting_tests.casting_fixture()
        source = data["assets"][0]
        data["assets"] += [
            {**source, "id": "set", "category": "review", "album": "explicit"},
            {**source, "id": "suggestion", "category": "review", "title": "Location set outfit", "album": "text-only"},
            {**source, "id": "wardrobe", "category": "outfits", "album": "wardrobe"},
            {**source, "id": "removed", "category": "cast"},
            {**source, "id": "other-project", "project": "hon"},
        ]
        data["albums"] += [
            {"id": "explicit", "project": "criminal_mind", "category": "review", "locationFamilyID": "location-one", "assetIDs": ["set"]},
            {"id": "text-only", "project": "criminal_mind", "category": "review", "title": "Location sets outfits", "assetIDs": ["suggestion"]},
            {"id": "wardrobe", "project": "criminal_mind", "category": "outfits", "assetIDs": ["wardrobe"]},
        ]
        reviews = {"removed": {"status": "remove", "note": "Keep the source"}}
        before = copy.deepcopy((data, reviews))
        model = all_files_model(data, "criminal_mind", reviews)
        ids = {s["id"]: [aid for g in s["groups"] for aid in g["assetIDs"]] for s in model["sections"]}
        self.assertEqual(model["sections"][0]["id"], "cast")
        self.assertEqual(ids["sets"], ["set"])
        self.assertEqual(ids["outfits"], ["wardrobe"])
        self.assertEqual(ids["inspiration"], ["suggestion"])
        self.assertEqual(ids["history"], ["removed"])
        self.assertNotIn("other-project", model["assets"])
        self.assertEqual(len([aid for values in ids.values() for aid in values]), len(set(aid for values in ids.values() for aid in values)))
        self.assertEqual((data, reviews), before)
        data["albums"][-3].pop("locationFamilyID")
        self.assertNotIn("sets", dict(all_files_model(data, "criminal_mind", reviews)["choices"]))

    def test_empty_purposes_are_stable_and_search_does_not_infer_costumes(self):
        data = casting_tests.casting_fixture()
        model = all_files_model(data, "criminal_mind", query="C01")
        self.assertEqual(model["choices"], list(ALL_FILES_PURPOSES))
        self.assertEqual(next(s for s in model["sections"] if s["id"] == "outfits")["count"], 0)
        cast = model["sections"][0]
        self.assertEqual(cast["count"], 4)
        self.assertEqual(len(cast["groups"]), 2)


class AllFilesAppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        casting_tests.CastingAppTests.setUpClass.__func__(cls)

    @classmethod
    def tearDownClass(cls):
        casting_tests.CastingAppTests.tearDownClass.__func__(cls)

    def app(self):
        app = self.AppTest.from_file(str(self.app_dir / "app.py"), default_timeout=25)
        app.query_params.update(project="criminal_mind", view="Library")
        app.run(timeout=45)
        self.assertFalse(app.exception)
        return app

    def test_filters_expansion_search_and_review_keep_exact_asset_identity(self):
        app = self.app()
        before = copy.deepcopy(app.session_state.studio_reviews)
        purpose = app.radio(key="all-files-purpose:criminal_mind")
        self.assertEqual(purpose.options, ["All", "Outfits", "Details", "Supporting cast", "Sets & locations", "Storyboards", "Videos", "Comfy", "Inspiration", "History", "Documents"])
        section_buttons = [b for b in app.button if ":section:" in str(b.key) and ":collection:" not in str(b.key)]
        self.assertTrue(section_buttons[0].label.startswith("▾ Supporting cast"))
        self.assertFalse(any(b.label.startswith("▾ Outfits") for b in app.button))
        purpose.set_value("outfits").run()
        self.assertFalse(app.exception)
        self.assertTrue(any(i.value == "No outfit collections have been added yet." for i in app.info))
        app.radio(key="all-files-purpose:criminal_mind").set_value("all").run()
        next(b for b in app.button if b.label == "Collapse sections").click().run()
        self.assertFalse(any(":collection:" in str(b.key) for b in app.button))
        next(b for b in app.button if b.label == "Expand sections").click().run()
        john = next(b for b in app.button if ":collection:criminal_mind:casting-john-options:toggle" in str(b.key))
        key = john.key
        john.click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.button(key=key).label, "Hide references")
        opens = [b for b in app.button if str(b.key).startswith("open:")]
        self.assertEqual(len(opens), 6)
        next(b for b in app.button if b.label == "Collapse sections").click().run()
        next(b for b in app.button if b.label == "Expand sections").click().run()
        self.assertEqual(app.button(key=key).label, "Hide references")
        app.text_input(key="all-files-search:criminal_mind").set_value("JILL-C02").run()
        opens = [b for b in app.button if str(b.key).startswith("open:")]
        self.assertEqual(len(opens), 1)
        aid = "TCM-CAST-JILL-C02"
        self.assertTrue(opens[0].key.endswith(":" + aid))
        self.assertEqual(app.session_state.studio_reviews, before)
        opens[0].click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state.studio_selected, aid)
        app.selectbox(key="human-actor:baldadoon").select("baldadoon").run()
        app.selectbox(key="human-scope:" + aid).select("character").run()
        app.button(key="review:" + aid + ":needs_fixes").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state.studio_reviews[aid]["status"], "needs_fixes")
        self.assertEqual(app.session_state.studio_reviews[aid]["reviewerControllerID"], "baldadoon")
        for saved_id, decision in before.items():
            self.assertEqual(app.session_state.studio_reviews[saved_id], decision)
        self.assertFalse(app.session_state.studio_reviews[aid].get("castUse"))

    def test_future_outfit_album_appears_without_catalog_migration(self):
        path = self.app_dir / "library" / "catalog.json"
        original = path.read_bytes()
        data = json.loads(original)
        aid = "future-outfit"
        asset = {**next(a for a in data["assets"] if a["id"].startswith("TCM-CAST-JILL")),
                 "id": aid, "album": "criminal_mind:wardrobe", "category": "outfits", "title": "Future wardrobe reference", "role": "outfit_reference"}
        data["assets"].append(asset)
        data["albums"].append({"id": asset["album"], "project": "criminal_mind", "category": "outfits", "title": "Wardrobe collection", "assetIDs": [aid]})
        try:
            path.write_text(json.dumps(data), encoding="utf-8")
            app = self.app()
            app.radio(key="all-files-purpose:criminal_mind").set_value("outfits").run()
            self.assertFalse(app.exception)
            next(b for b in app.button if ":collection:criminal_mind:wardrobe:toggle" in str(b.key)).click().run()
            self.assertTrue(any(str(b.key).endswith(":" + aid) for b in app.button if str(b.key).startswith("open:")))
            self.assertNotIn(aid, app.session_state.studio_reviews)
            self.assertEqual(json.loads(path.read_bytes()), data)
        finally:
            path.write_bytes(original)

    def test_other_project_library_keeps_existing_controls(self):
        app = self.app()
        app.selectbox(key="studio_project").select("hon").run()
        self.assertFalse(app.exception)
        self.assertTrue(any(s.label == "Explore" for s in app.selectbox))
        self.assertFalse(any(r.label == "Purpose" for r in app.radio))
        app.selectbox(key="studio_project").select("lisan").run()
        self.assertFalse(app.exception)
        self.assertTrue(any(s.label == "Explore" for s in app.selectbox))
        self.assertFalse(any(r.label == "Purpose" for r in app.radio))


if __name__ == "__main__":
    unittest.main()
