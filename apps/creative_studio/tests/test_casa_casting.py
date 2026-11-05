"""Native casting navigation preserves per-portrait reviews and source records."""
import copy
import json
import sys
import unittest
from pathlib import Path

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP))
from mission_view import casting_roles, casting_review_payload, director_stage, location_collections, script_desk_model
from library_helpers import read_review, review_payload
import test_studio as studio_tests


def casting_fixture():
    assets, collections, albums = [], [], []
    for role, states, count in (("JOHN", ("JOHN", "JACK", "JOHNNY"), 2), ("JILL", ("JILL",), 2)):
        group_id = "criminal_mind:casting-" + role.lower() + "-options"
        ids = []
        for number in range(1, count + 1):
            for state in states:
                aid = f"TCM-CAST-{role}-C{number:02d}" + ("-" + state if role == "JOHN" else "")
                ids.append(aid)
                assets.append({"id": aid, "project": "criminal_mind", "kind": "image", "category": "cast",
                    "album": group_id, "title": aid, "filename": aid + ".jpg", "sha256": "hash-" + aid,
                    "src": "review.jpg", "thumb": "review.jpg", "role": "casting_option", "stage": "preliminary",
                    "castingGroupID": "TCM-CAST-" + role, "physicalCandidateID": f"C{number:02d}",
                    "performanceState": state if role == "JOHN" else None, "selected": False, "characterRole": role.title(),
                    "roleContext": role + " source role context", "sourceAppearance": role + " source appearance"})
        collections.append({"id": group_id, "project": "criminal_mind", "title": role.title(),
                            "castingGroupID": "TCM-CAST-" + role, "assetIDs": ids,
                            "sourceContext": {"sourceScenes": ["TCM-SRC-01"]}})
        albums.append({"id": group_id, "project": "criminal_mind", "title": role.title(), "category": "cast", "assetIDs": ids})
    project = {"id": "criminal_mind", "name": "Baldadoon", "controllerID": "baldadoon", "landing": {
        "author": "Baldadoon", "sourceBlocks": [{"id": "TCM-SRC-01", "heading": "An exact source scene",
            "text": "Original screenplay text stays intact.", "lineStart": 1, "lineEnd": 10}]}}
    return {"assets": assets, "castCollections": collections, "albums": albums, "projects": [project]}


class CastingModelTests(unittest.TestCase):
    def test_director_stage_default_and_locations_use_only_recorded_metadata(self):
        self.assertEqual(director_stage({}), "casting")
        self.assertEqual(director_stage({"directorDefaultStage": "script"}), "script")
        self.assertEqual(director_stage({"directorDefaultStage": "locations"}), "locations")
        self.assertEqual(director_stage({"directorDefaultStage": "locations"}, "casting"), "casting")
        self.assertEqual(director_stage({"directorDefaultStage": "finished"}), "casting")
        data = casting_fixture()
        data["albums"][0]["title"] = "Sets and locations mentioned in a title"
        self.assertEqual(location_collections(data), [])
        data["albums"][0]["locationFamilyID"] = "recorded-family"
        before = copy.deepcopy(data)
        self.assertEqual(len(location_collections(data)[0]["assets"]), 6)
        self.assertEqual(data, before)

    def test_script_desk_uses_exact_source_links_and_preserves_text(self):
        data = casting_fixture()
        data["projects"][0]["landing"]["sourceBlocks"].append({"id": "TCM-SRC-02", "heading": "Same heading", "text": "Another exact excerpt"})
        data["storyboardStructure"] = {"stories": [{"project": "criminal_mind", "storyID": "story",
            "sections": [{"id": "section", "title": "Same heading", "sourceBlockIDs": ["TCM-SRC-02"], "shotIDs": ["shot", "missing"]}],
            "shots": [{"shotID": "shot", "sectionID": "section", "title": "Proposed shot", "stage": "preliminary"}]}]}
        before = copy.deepcopy(data)
        model = script_desk_model(data)
        self.assertEqual(model["scenes"][0]["coverage"], [])
        self.assertEqual([s["shotID"] for s in model["scenes"][1]["coverage"][0]["shots"]], ["shot"])
        self.assertEqual(model["scenes"][1]["block"]["text"], "Another exact excerpt")
        self.assertEqual(data, before)

    def test_casting_export_is_scoped_and_import_compatible(self):
        data = casting_fixture()
        aid = data["assets"][0]["id"]
        extra = {**data["assets"][0], "id": "other", "project": "hon"}
        assets = [*data["assets"], extra]
        payload = casting_review_payload(assets, {aid: {"note": "Casting note"}, "other": {"note": "Private other project"}}, {aid, "other"}, {aid, "other"})
        self.assertEqual(payload["format"], "cfa-visual-review-v1")
        self.assertEqual(payload["project"], "criminal_mind")
        self.assertEqual(payload["controllerID"], "baldadoon")
        for field in ("items", "favorites", "exportBasket"):
            self.assertEqual([row["id"] for row in payload[field]], [aid])
        self.assertNotIn("Private other project", json.dumps(payload))
        restored, _, skipped = read_review(payload, assets)
        self.assertEqual(skipped, 0)
        self.assertEqual(restored[aid]["note"], "Casting note")

    def test_physical_candidates_keep_separate_portraits_and_exact_context(self):
        data = casting_fixture()
        data["assets"].append({**data["assets"][0], "id": "other-project", "project": "hon"})
        data["assets"].append({**data["assets"][0], "id": "not-casting", "role": "set_design_option"})
        data["castCollections"][0]["assetIDs"].extend(["other-project", "not-casting", "missing"])
        before = copy.deepcopy(data)
        roles = casting_roles(data)
        self.assertEqual([len(r["candidates"]) for r in roles], [2, 2])
        self.assertEqual([a["performanceState"] for a in roles[0]["candidates"][0]["assets"]], ["JOHN", "JACK", "JOHNNY"])
        self.assertEqual(roles[0]["sourceBlocks"][0]["text"], "Original screenplay text stays intact.")
        self.assertEqual(data, before)

    def test_missing_physical_id_does_not_invent_pairing(self):
        data = casting_fixture()
        for asset in data["assets"][:3]:
            del asset["physicalCandidateID"]
        roles = casting_roles(data)
        self.assertEqual(len(roles[0]["candidates"]), 4)
        self.assertEqual(len(roles[0]["candidates"][0]["assets"]), 1)

    def test_working_collection_opens_every_tile_before_collapsed_context(self):
        from streamlit.testing.v1 import AppTest
        ids = ["reference-" + str(i) for i in range(30)]
        data = {"projects": [{"id": "hon", "name": "Hon"}], "albums": [],
                "assets": [{"id": aid, "project": "hon", "kind": "image", "title": aid, "sha256": aid} for aid in ids],
                "castCollections": [{"id": "hon:sample", "project": "hon", "title": "Character references",
                    "assetIDs": ids, "referenceAssetIDs": ids, "coverID": ids[0], "notes": ["Existing scope note"]}]}
        script = f'''import sys
from pathlib import Path
import streamlit as st
sys.path.insert(0, {str(APP)!r})
from design_view import render_design_view
data = {data!r}
st.session_state.setdefault("reviews", {{"reference-0": {{"status": "needs_fixes", "note": "Old note"}}}})
st.session_state["displayed"] = []
st.session_state["grid_sizes"] = []
def grid(rows, context):
    st.session_state["displayed"].extend(a["id"] for a, album in rows)
    st.session_state["grid_sizes"].append(len(rows))
    for a, album in rows:
        st.write(a["title"])
render_design_view(data, "hon", "working", Path({str(APP)!r}), grid, lambda asset: None, reviews=st.session_state.reviews)
'''
        app = AppTest.from_string(script, default_timeout=25).run()
        self.assertFalse(app.exception)
        toggle = next(b for b in app.button if b.key.endswith(":expanded:hon:sample-working:toggle"))
        toggle.click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state["displayed"], ids)
        self.assertEqual(app.session_state["grid_sizes"], [24, 6])
        self.assertTrue(any(e.label == "Reference context & notes" for e in app.expander))
        self.assertFalse(any(e.label == "Design reference candidates" for e in app.expander))
        self.assertFalse(any(b.label == "Review character / collection cover" for b in app.button))
        self.assertEqual(app.session_state["reviews"], {"reference-0": {"status": "needs_fixes", "note": "Old note"}})

    def test_character_hub_pairs_recorded_lanes_and_preserves_actions(self):
        from streamlit.testing.v1 import AppTest
        ids = ["person", "scene", "clip", "design"]
        data = {"projects": [{"id": "hon", "name": "Hon"}], "albums": [],
                "assets": [{"id": aid, "project": "hon", "kind": "video" if aid == "clip" else "image", "title": aid, "sha256": aid} for aid in ids],
                "castCollections": [{"id": "hon:person", "project": "hon", "title": "Character hub", "assetIDs": ["person"],
                    "currentIDs": ["person"], "coverID": "person", "sceneAssetIDs": ["scene"], "videoAssetIDs": ["clip"],
                    "referenceAssetIDs": ["design"], "notes": ["Original character note"]}],
                "shotMaterials": {"shots": [{"id": "planned", "project": "hon", "characterCollectionID": "hon:person", "title": "Recorded scene plan", "panelAssetIDs": []}]}}
        script = f'''import sys
from pathlib import Path
import streamlit as st
sys.path.insert(0, {str(APP)!r})
from design_view import render_design_view
data = {data!r}
st.session_state.setdefault("reviews", {{"clip": {{"note": "Old feedback", "shotPlan": {{"idea": "Recorded motion", "destinations": ["Flow"], "prompt": ""}}}}}})
def open_asset(asset):
    st.session_state["opened"] = asset["id"]
def navigate(view):
    st.session_state["destination"] = view
def grid(rows, context):
    for asset, album in rows:
        st.button(asset["title"], key=context + ":asset:" + asset["id"], on_click=open_asset, args=(asset,))
render_design_view(data, "hon", "cast", Path({str(APP)!r}), grid, open_asset, reviews=st.session_state.reviews, navigate=navigate)
'''
        app = AppTest.from_string(script, default_timeout=25).run()
        self.assertFalse(app.exception)
        next(b for b in app.button if b.label == "Show references").click().run()
        self.assertFalse(app.exception)
        titles = [m.value for m in app.markdown]
        self.assertIn("**Scenes & planned work**", titles)
        self.assertIn("**Videos**", titles)
        self.assertIn("**Planned scenes**", titles)
        self.assertIn("**Saved generation plans**", titles)
        refs = next(e for e in app.expander if e.label.startswith("Reference candidates ·"))
        self.assertTrue(refs.proto.expanded)
        self.assertEqual(len([b for b in app.button if b.label == "design"]), 1)
        self.assertTrue(any(e.label == "Origin & story connections" for e in app.expander))
        next(b for b in app.button if b.label == "Open saved plan · clip").click().run()
        self.assertEqual(app.session_state["opened"], "clip")
        next(b for b in app.button if b.label == "Browse storyboards").click().run()
        self.assertEqual(app.session_state["destination"], "Storyboard")
        self.assertEqual(app.session_state["reviews"], {"clip": {"note": "Old feedback", "shotPlan": {"idea": "Recorded motion", "destinations": ["Flow"], "prompt": ""}}})

    def test_twelve_reference_candidates_start_collapsed_without_nested_drawers(self):
        from streamlit.testing.v1 import AppTest
        ids = ["candidate-" + str(i) for i in range(12)]
        data = {"projects": [{"id": "hon", "name": "Hon"}], "albums": [],
                "assets": [{"id": aid, "project": "hon", "kind": "image", "title": aid} for aid in ids],
                "castCollections": [{"id": "hon:pool", "project": "hon", "title": "Pool", "assetIDs": ids, "coverID": ids[0],
                    "sections": [{"title": "Received candidates", "assetIDs": ids}]}]}
        script = f'''import sys
from pathlib import Path
import streamlit as st
sys.path.insert(0, {str(APP)!r})
from design_view import render_design_view
def grid(rows, context):
    for asset, album in rows:
        st.write(asset["id"])
render_design_view({data!r}, "hon", "cast", Path({str(APP)!r}), grid, lambda asset: None)
'''
        app = AppTest.from_string(script, default_timeout=25).run()
        next(b for b in app.button if b.label == "Show references").click().run()
        self.assertFalse(app.exception)
        refs = next(e for e in app.expander if e.label == "Reference candidates · 12")
        self.assertFalse(refs.proto.expanded)
        self.assertEqual(len(refs.expander), 1)  # AppTest includes this expander itself.
        self.assertEqual([m.value for m in refs.markdown], ids)
        self.assertFalse(any(b.label == "Review character / collection cover" for b in app.button))


class CastingAppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        studio_tests.StudioAppTest.setUpClass.__func__(cls)
        path = cls.app_dir / "library" / "catalog.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        fixture = casting_fixture()
        for project in data["projects"]:
            project["controllerID"] = "ziggy"
        data["projects"] += fixture["projects"]
        # A location before the portraits proves the default library sort, not input order.
        location = {**fixture["assets"][0], "id": "location", "title": "Location first in source", "category": "review", "role": "set_design_option", "album": "criminal_mind:sets"}
        data["assets"] += [location, *fixture["assets"]]
        data["albums"] += [{"id": "criminal_mind:sets", "project": "criminal_mind", "title": "Sets", "category": "review", "setFamilyID": "test-set", "assetIDs": ["location"]}, *fixture["albums"]]
        data["castCollections"] = fixture["castCollections"]
        data["categories"] += [["cast", "Characters"], ["review", "Review"]]
        data["missionControl"]["tasks"].append({"id": "tcm-grok-casting-20261030", "project": "criminal_mind",
            "provider": "Grok", "status": "needs_input", "title": "Casting handoff", "summary": "Received portraits",
            "nextAction": "Review candidates", "direction": "inbound", "workKind": "image_new", "links": [],
            "previewAssetIDs": [a["id"] for a in fixture["assets"]], "decisionScope": "character"})
        path.write_text(json.dumps(data), encoding="utf-8")
        cls.data = data

    @classmethod
    def tearDownClass(cls):
        studio_tests.StudioAppTest.tearDownClass.__func__(cls)

    def app(self):
        app = self.AppTest.from_file(str(self.app_dir / "app.py"), default_timeout=20)
        app.query_params.update(project="criminal_mind", view="casa_baldadoon")
        app.run(timeout=45)
        self.assertFalse(app.exception)
        return app

    def test_navigation_exact_portrait_review_and_roundtrip(self):
        app = self.app()
        self.assertEqual([s.value for s in app.subheader][:2], ["Casting session", "Collaborator handoffs"])
        self.assertFalse(app.metric)
        self.assertEqual(app.selectbox(key="casa-casting-role").options, ["John", "Jill"])
        before = copy.deepcopy(app.session_state.studio_reviews)
        app.button(key="casa-casting-next").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state["casa-casting-index:criminal_mind:casting-john-options"], 1)
        self.assertEqual(app.session_state.studio_reviews, before)
        app.selectbox(key="casa-casting-role").select("criminal_mind:casting-jill-options").run()
        self.assertFalse(app.exception)
        app.button(key="casa-casting-next").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state["casa-casting-index:criminal_mind:casting-jill-options"], 1)
        app.button(key="casa-casting-prev").click().run()
        self.assertFalse(app.exception)
        app.selectbox(key="casa-casting-role").select("criminal_mind:casting-john-options").run()
        aid = "TCM-CAST-JOHN-C02-JACK"
        app.selectbox(key="casa-casting-portrait:criminal_mind:casting-john-options").select(aid).run()
        app.selectbox(key="human-actor:baldadoon").select("baldadoon").run()
        app.selectbox(key="human-scope:" + aid).select("character").run()
        app.button(key="review:" + aid + ":keep").click().run()
        self.assertFalse(app.exception)
        reviews = app.session_state.studio_reviews
        self.assertEqual(reviews[aid]["status"], "keep")
        self.assertEqual(reviews[aid]["reviewerControllerID"], "baldadoon")
        self.assertEqual(reviews[aid]["decisionScope"], "character")
        self.assertNotIn("TCM-CAST-JOHN-C02-JOHN", reviews)
        self.assertNotIn("TCM-CAST-JOHN-C02-JOHNNY", reviews)
        for key, value in before.items():
            self.assertEqual(reviews[key], value)
        payload = review_payload(self.data["assets"], reviews, set())
        restored, _, skipped = read_review(payload, self.data["assets"])
        self.assertEqual(skipped, 0)
        self.assertEqual(restored[aid]["status"], "keep")
        self.assertEqual(restored[aid]["reviewerControllerID"], "baldadoon")
        self.assertFalse(restored[aid].get("castUse"))
        self.assertFalse(restored[aid].get("shotPlan"))
        app.button(key="nav:Ziggy’s Corner").click().run()
        self.assertFalse(app.exception)
        self.assertFalse(any(s.value == "Casting session" for s in app.subheader))

    def test_sidebar_order_and_library_put_people_before_script(self):
        app = self.app()
        keys = [b.key for b in app.sidebar.button]
        self.assertEqual(keys[keys.index("nav:Comfy swap targets") + 1], "nav:Collaborators")
        self.assertLess(keys.index("nav:Collaborators"), keys.index("nav:Archive"))
        self.assertEqual(keys.count("nav:Collaborators"), 1)
        app.button(key="nav:Library").click().run()
        self.assertFalse(app.exception)
        for key in [b.key for b in app.button if ":collection:" in str(b.key) and str(b.key).endswith(":toggle")]:
            app.button(key=key).click().run()
        opens = [b.key for b in app.button if str(b.key).startswith("open:")]
        self.assertTrue(opens[0].endswith(":TCM-CAST-JOHN-C01-JOHN"))
        self.assertTrue(opens[-1].endswith(":location"))
        self.assertFalse(any(s.value == "Project overview" for s in app.subheader))
        self.assertTrue(any(e.label == "Screenplay & source records" for e in app.expander))
        self.assertTrue(any(t.value == "Original screenplay text stays intact." for t in app.text))
        self.assertFalse(any("No character designs" in i.value for i in app.info))

    def test_unattributed_note_draft_survives_navigation_and_requires_save(self):
        app = self.app()
        aid = "TCM-CAST-JOHN-C01-JOHN"
        self.assertIsNone(app.selectbox(key="human-actor:baldadoon").value)
        app.text_area(key="asset-note:" + aid).set_value("Draft direction before reviewer selection").run()
        self.assertFalse(app.exception)
        self.assertNotIn(aid, app.session_state.studio_reviews)
        app.button(key="casa-casting-next").click().run()
        app.button(key="casa-casting-prev").click().run()
        self.assertEqual(app.text_area(key="asset-note:" + aid).value, "Draft direction before reviewer selection")
        self.assertNotIn(aid, app.session_state.studio_reviews)
        app.selectbox(key="human-actor:baldadoon").select("baldadoon").run()
        app.selectbox(key="human-scope:" + aid).select("character").run()
        app.button(key="casa-save-note:" + aid).click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state.studio_reviews[aid]["note"], "Draft direction before reviewer selection")
        self.assertEqual(app.session_state.studio_reviews[aid]["reviewerControllerID"], "baldadoon")
        self.assertNotIn(aid, app.session_state.studio_casting_note_drafts)
        self.assertFalse(app.session_state.studio_reviews[aid].get("status"))
        self.assertFalse(app.session_state.studio_reviews[aid].get("castUse"))

    def test_director_stage_arrows_revisit_without_completing_or_reviewing(self):
        app = self.app()
        before = copy.deepcopy(app.session_state.studio_reviews)
        self.assertEqual(app.session_state["casa-director-stage:criminal_mind"], "casting")
        self.assertFalse(app.button(key="casa-stage-prev").disabled)
        app.button(key="casa-stage-next").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state["casa-director-stage:criminal_mind"], "locations")
        self.assertEqual([s.value for s in app.subheader][:2], ["Locations", "Collaborator handoffs"])
        self.assertTrue(app.button(key="casa-stage-next").disabled)
        self.assertTrue(any(b.key == "casa-location-review:location" for b in app.button))
        self.assertEqual(app.session_state.studio_reviews, before)
        app.button(key="casa-location-review:location").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state.studio_mission_selected, "location")
        self.assertEqual(app.session_state.studio_reviews, before)
        app.button(key="corner-selected-back").click().run()
        app.button(key="casa-stage-prev").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state["casa-director-stage:criminal_mind"], "casting")
        self.assertTrue(any(s.value == "Casting session" for s in app.subheader))
        self.assertEqual(app.session_state.studio_reviews, before)
        app.button(key="casa-stage-prev").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state["casa-director-stage:criminal_mind"], "script")
        self.assertEqual([s.value for s in app.subheader][:2], ["Script desk", "Collaborator handoffs"])
        self.assertTrue(app.button(key="casa-stage-prev").disabled)
        self.assertTrue(any(code.value == "Original screenplay text stays intact." for code in app.code))
        self.assertEqual(app.session_state.studio_reviews, before)
        app.button(key="casa-stage-next").click().run()
        self.assertEqual(app.session_state["casa-director-stage:criminal_mind"], "casting")

    def test_script_reader_scene_selection_coverage_and_real_notes_route(self):
        path = self.app_dir / "library" / "catalog.json"
        original = path.read_bytes()
        data = json.loads(original)
        project = next(p for p in data["projects"] if p["id"] == "criminal_mind")
        project["directorDefaultStage"] = "script"
        project["landing"].update(scriptAssetID="script-doc", notesAssetID="notes-doc")
        project["landing"]["sourceBlocks"].append({"id": "TCM-SRC-02", "heading": "Second source scene", "text": "Second exact source scene.", "lineStart": 11, "lineEnd": 20})
        data["assets"] += [{"id": "script-doc", "project": "criminal_mind", "kind": "document", "filename": "script.txt", "title": "Original script", "text": "Complete original script."},
                           {"id": "notes-doc", "project": "criminal_mind", "kind": "document", "filename": "notes.txt", "title": "Recorded notes", "text": "Real source notes."}]
        data["storyboardStructure"] = {"stories": [{"project": "criminal_mind", "storyID": "story",
            "sections": [{"id": "section", "title": "Proposed sequence", "sourceBlockIDs": ["TCM-SRC-02"], "shotIDs": ["shot"]}],
            "shots": [{"shotID": "shot", "sectionID": "section", "title": "Proposed shot", "stage": "preliminary", "fields": [{"key": "purpose", "text": "Existing purpose text"}]}]}]}
        try:
            path.write_text(json.dumps(data), encoding="utf-8")
            app = self.app()
            before = copy.deepcopy(app.session_state.studio_reviews)
            app.selectbox(key="casa-script-scene:criminal_mind").select("TCM-SRC-02").run()
            self.assertFalse(app.exception)
            self.assertTrue(any(code.value == "Second exact source scene." for code in app.code))
            self.assertTrue(any(e.label == "shot · Proposed shot" for e in app.expander))
            self.assertTrue(any(b.key == "casa-script-shot:story:shot" for b in app.button))
            self.assertTrue(any(code.value == "Complete original script." for code in app.code))
            self.assertEqual(app.session_state.studio_reviews, before)
            app.button(key="casa-script-notes-review").click().run()
            self.assertFalse(app.exception)
            self.assertEqual(app.session_state.studio_mission_selected, "notes-doc")
            self.assertTrue(any(text.value == "Real source notes." for text in app.text))
            self.assertEqual(app.session_state.studio_reviews, before)
            self.assertEqual(json.loads(path.read_bytes()), data)
        finally:
            path.write_bytes(original)

    def test_future_default_stage_starts_locations_and_keeps_casting_available(self):
        path = self.app_dir / "library" / "catalog.json"
        original = path.read_bytes()
        data = json.loads(original)
        next(p for p in data["projects"] if p["id"] == "criminal_mind")["directorDefaultStage"] = "locations"
        try:
            path.write_text(json.dumps(data), encoding="utf-8")
            app = self.app()
            self.assertEqual(app.session_state["casa-director-stage:criminal_mind"], "locations")
            self.assertTrue(any(s.value == "Locations" for s in app.subheader))
            app.button(key="casa-stage-prev").click().run()
            self.assertEqual(app.session_state["casa-director-stage:criminal_mind"], "casting")
            self.assertEqual(json.loads(path.read_bytes()), data)
        finally:
            path.write_bytes(original)


if __name__ == "__main__":
    unittest.main()
