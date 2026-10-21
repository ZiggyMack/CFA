"""Comfy workspace roles and controls preserve existing assets and decisions."""
import copy
import json
from pathlib import Path
import sys
import unittest

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP))
from design_view import build_design_model, model_asset_ids, workflow_diagram_html


def fixture():
    assets = [
        {"id": aid, "project": project, "kind": kind, "title": title, "album": album,
         "category": "comfy", "sha256": str(i + 1) * 64, "src": "missing.jpg"}
        for i, (aid, project, kind, title, album) in enumerate([
            ("motion", "hon", "video", "Motion result", "hon:results"),
            ("relight", "hon", "video", "Relight preservation failed", "hon:results"),
            ("identity", "hon", "image", "Identity candidate", "hon:stills"),
            ("han-front", "hon", "image", "Han front", "hon:han"),
            ("han-side", "hon", "image", "Han side", "hon:han"),
            ("leia", "hon", "image", "Leia target", "hon:leia"),
            ("source", "hon", "video", "Gemini source", "hon:source"),
            ("control", "hon", "video", "Canny guide", "hon:guides"),
            ("soundtrack", "hon", "video", "Soundtrack preview", "hon:local"),
            ("mouth", "hon", "image", "Mouth reference", "hon:mouths"),
            ("flow", "hon", "video", "Flow result", "hon:flow"),
            ("lisan-mouth", "lisan", "image", "Lisan mouth reference", "lisan:mouths"),
            ("record", "hon", "document", "Motion run record", "hon:records"),
        ])
    ]
    return {
        "assets": assets,
        "albums": [
            {"id": aid, "project": project, "title": title, "category": "comfy", "assetIDs": ids}
            for aid, project, title, ids in [
                ("hon:han", "hon", "Han Solo", ["han-front", "han-side"]),
                ("hon:leia", "hon", "Princess Leia", ["leia"]),
                ("hon:mouths", "hon", "Mouth library", ["mouth"]),
                ("lisan:mouths", "lisan", "Lisan mouth library", ["lisan-mouth"]),
            ]
        ],
        "browseLayout": {"projects": {"hon": {"comfyWorkspace": {
            "outputAssetIDs": ["motion", "relight", "identity"],
            "targetAlbumIDs": ["hon:han", "hon:leia"],
            "inputAssetIDs": ["source", "control"],
            "finishingAssetIDs": ["soundtrack"],
            "workflowFamilies": [
                {"id": "motion-family", "title": "Animate a still", "inputLabel": "Candidate still",
                 "operationLabel": "Image-to-video", "outputLabel": "Motion candidate", "status": "Executed; acceptance pending",
                 "description": "Existing animation tests and a prepared alternative.",
                 "workflowIDs": ["motion-workflow", "seedance-workflow", "foreign-workflow"],
                 "links": [{"label": "Read motion evidence", "assetID": "record"}]},
                {"id": "sync-family", "title": "Match vocals", "inputLabel": "Clip + vocal audio",
                 "operationLabel": "Lip-sync", "outputLabel": "No result yet", "status": "Prepared; not executed",
                 "description": "Exact phrase remains to be selected.", "workflowIDs": [], "links": []},
            ],
        }}}},
        "productionWorkflows": [
            {"id": "motion-workflow", "project": "hon", "title": "LTX motion test", "status": "Executed",
             "summary": "Long blink remains visible.", "sourceAssetIDs": ["identity"], "outputAssetIDs": ["motion"], "documentAssetIDs": ["record"]},
            {"id": "seedance-workflow", "project": "shared", "title": "Seedance alternative", "status": "Prepared",
             "summary": "Cloud preflight pending.", "sourceAssetIDs": [], "outputAssetIDs": [], "documentAssetIDs": []},
            {"id": "foreign-workflow", "project": "lisan", "title": "Different project", "sourceAssetIDs": ["lisan-mouth"]},
        ],
    }


class ComfyModelTest(unittest.TestCase):
    def test_explicit_roles_and_no_reference_or_provider_duplicates(self):
        data = fixture()
        before = copy.deepcopy(data)
        reviews = {"relight": {"status": "needs_fixes", "note": "Keep this evidence", "likenessRating": 2},
                   "mouth": {"status": "keep", "likenessRating": 5, "shotPlan": {"title": "Preserved"}}}
        saved = copy.deepcopy(reviews)
        model = build_design_model(data, "hon", "Comfy swap targets", reviews)
        self.assertEqual(model["title"], "Comfy results & swap targets")
        sections = model["sections"]
        self.assertEqual([s["title"] for s in sections], ["Comfy outputs", "Likeness targets", "Workflow recipes", "Source clips & control guides", "Local finishing"])
        self.assertEqual(sections[0]["assetIDs"], ["motion", "relight", "identity"])
        self.assertEqual([g["id"] for g in sections[1]["groups"]], ["hon:han", "hon:leia"])
        self.assertTrue(all(g["directSingle"] and g["unit"] == "targets" for g in sections[1]["groups"]))
        self.assertEqual(sections[3]["assetIDs"], ["source", "control"])
        self.assertEqual(sections[4]["assetIDs"], ["soundtrack"])
        self.assertTrue(all(s["kind"] == "disclosure" and not s.get("expanded", False) for s in sections[3:]))
        self.assertIn("locally", sections[4]["description"])
        self.assertIn("has not executed", sections[4]["description"])
        self.assertEqual(len(model_asset_ids(model)), 9)
        self.assertNotIn("mouth", model_asset_ids(model))
        self.assertNotIn("flow", model_asset_ids(model))
        self.assertEqual(data, before)
        self.assertEqual(reviews, saved)

    def test_archive_removal_query_and_project_filters(self):
        data = fixture()
        data["browseLayout"]["projects"]["hon"]["comfyWorkspace"]["outputAssetIDs"] += ["missing", "lisan-mouth", "motion"]
        reviews = {"motion": {"collectionState": "archived", "status": "keep"}, "identity": {"status": "remove"},
                   "han-side": {"collectionState": "archived"}, "relight": {"status": "needs_fixes", "note": "gold drift"}}
        model = build_design_model(data, "hon", "comfy", reviews)
        self.assertEqual(model["sections"][0]["assetIDs"], ["relight"])
        self.assertEqual(model["sections"][1]["groups"][0]["assetIDs"], ["han-front"])
        self.assertNotIn("lisan-mouth", model_asset_ids(model))
        searched = build_design_model(data, "hon", "comfy", reviews, query="gold drift")
        self.assertEqual(model_asset_ids(searched), ["relight"])
        empty = build_design_model(data, "hon", "comfy", reviews, query="unmatched phrase")
        self.assertEqual(model_asset_ids(empty), [])
        self.assertEqual(empty["sections"][0]["emptyMessage"], "No Comfy outputs match this view.")

    def test_album_routes_remain_scoped(self):
        data = fixture()
        target = build_design_model(data, "hon", "comfy", album_id="hon:leia")
        self.assertEqual(model_asset_ids(target), ["leia"])
        results = build_design_model(data, "hon", "comfy", album_id="hon:results")
        self.assertEqual(model_asset_ids(results), ["motion", "relight"])
        mouth = build_design_model(data, "hon", "comfy", album_id="hon:mouths")
        self.assertEqual(model_asset_ids(mouth), [])

    def test_missing_workspace_is_empty_without_category_inference(self):
        data = fixture()
        for project in ("lisan", "unknown"):
            model = build_design_model(data, project, "comfy")
            self.assertEqual(model_asset_ids(model), [])
            self.assertEqual(model["sections"][0]["emptyMessage"], "No Comfy outputs have been catalogued for this project.")

    def test_recipe_links_are_scoped_separate_and_do_not_change_gallery_counts(self):
        data = fixture()
        before = copy.deepcopy(data)
        reviews = {"motion": {"status": "needs_fixes", "note": "Visible drift"}, "identity": {"collectionState": "archived"},
                   "record": {"status": "remove"}}
        saved_reviews = copy.deepcopy(reviews)
        model = build_design_model(data, "hon", "comfy", reviews)
        recipes = model["sections"][2]
        self.assertEqual(recipes["kind"], "workflow_families")
        self.assertEqual(model_asset_ids(recipes), [])
        motion, prepared = recipes["families"]
        self.assertEqual([w["id"] for w in motion["workflows"]], ["motion-workflow", "seedance-workflow"])
        self.assertEqual(motion["workflows"][0]["sourceAssetIDs"], [])
        self.assertEqual(motion["workflows"][0]["outputAssetIDs"], ["motion"])
        self.assertEqual(motion["workflows"][0]["documentAssetIDs"], [])
        self.assertEqual(motion["links"], [])
        self.assertEqual(prepared["outputLabel"], "No result yet")
        self.assertEqual(prepared["workflows"], [])
        self.assertEqual(data, before)
        self.assertEqual(reviews, saved_reviews)

    def test_recipe_search_and_escaped_accessible_diagram(self):
        data = fixture()
        for query in ("animate", "long blink", "preflight"):
            model = build_design_model(data, "hon", "comfy", query=query)
            families = model["sections"][2]["families"]
            self.assertEqual([f["id"] for f in families], ["motion-family"])
            self.assertEqual(families[0]["workflows"][0]["sourceAssetIDs"], ["identity"])
            self.assertEqual(families[0]["links"], [{"label": "Read motion evidence", "assetID": "record"}])
        html = workflow_diagram_html({"inputLabel": "<script>bad</script>", "operationLabel": "Edit & preserve", "outputLabel": "Candidate"})
        self.assertIn('role="group"', html)
        self.assertIn('aria-label="Input to operation to result"', html)
        self.assertIn("&lt;script&gt;bad&lt;/script&gt;", html)
        self.assertIn("Edit &amp; preserve", html)
        self.assertNotIn("<script>", html)
        self.assertNotIn("<img", html)


class ComfyControlsTest(unittest.TestCase):
    def launch(self, project="hon"):
        from streamlit.testing.v1 import AppTest
        source = f'''
import json, sys
from pathlib import Path
import streamlit as st
sys.path.insert(0, {str(APP)!r})
from design_view import render_design_view
data = json.loads({json.dumps(fixture())!r})
def open_reference(asset):
    st.session_state['opened'] = asset['id']
def navigate(view):
    st.session_state['destination'] = view
def grid(rows, context):
    for asset, _ in rows:
        st.write(asset['id'])
render_design_view(data, {project!r}, 'Comfy swap targets', Path({str(APP)!r}), grid, open_reference, navigate=navigate)
'''
        app = AppTest.from_string(source, default_timeout=20).run()
        self.assertFalse(app.exception)
        return app

    def test_singleton_opens_target_and_multiple_targets_expand(self):
        app = self.launch()
        self.assertEqual([b.label for b in app.button].count("Open target"), 1)
        self.assertEqual([b.label for b in app.button].count("Show references"), 1)
        next(b for b in app.button if b.label == "Open target").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state["opened"], "leia")
        next(b for b in app.button if b.label == "Show references").click().run()
        self.assertFalse(app.exception)
        self.assertTrue(any(b.label == "Hide references" for b in app.button))
        next(b for b in app.button if b.label == "Open Working references").click().run()
        self.assertEqual(app.session_state["destination"], "Working references")

    def test_empty_project_has_working_reference_link(self):
        app = self.launch("lisan")
        self.assertTrue(any(c.value == "No Comfy outputs have been catalogued for this project." for c in app.caption))
        self.assertEqual([b.label for b in app.button], ["Open Working references"])

    def test_diagrams_and_record_links_do_not_render_media_galleries(self):
        app = self.launch()
        diagrams = [m.value for m in app.markdown if 'class="cfa-workflow-diagram"' in m.value]
        self.assertEqual(len(diagrams), 2)
        self.assertTrue(all("<img" not in html for html in diagrams))
        self.assertTrue(any("No result yet" in html for html in diagrams))
        self.assertEqual([e.label for e in app.expander].count("Ingredients and records"), 2)
        next(b for b in app.button if b.label == "Read motion evidence").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state["opened"], "record")


@unittest.skipUnless((APP / "library/design_catalog.json").is_file(), "Portable snapshot unavailable")
class ComfySnapshotTest(unittest.TestCase):
    def test_real_app_video_target_and_reference_navigation_keep_reviews(self):
        from streamlit.testing.v1 import AppTest
        app = AppTest.from_file(str(APP / "app.py"), default_timeout=45).run()
        app.button(key="nav:Comfy swap targets").click().run()
        self.assertFalse(app.exception)
        saved = copy.deepcopy(app.session_state["studio_reviews"])
        next(b for b in app.button if (b.key or "").startswith("open:design:") and b.key.endswith(":HD-COMFY-MOTION-V001")).click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state["studio_selected"], "HD-COMFY-MOTION-V001")
        self.assertTrue(app.get("video"), "Existing player opens for saved Comfy video")
        app.button(key="nav:Comfy swap targets").click().run()
        next(b for b in app.button if b.label == "Open target").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state["studio_selected"], "LEIA-LIKENESS-01")
        app.button(key="nav:Comfy swap targets").click().run()
        next(b for b in app.button if b.label == "Open Working references").click().run()
        self.assertEqual(app.session_state["studio_view"], "Working references")
        self.assertEqual(app.session_state["studio_reviews"], saved)

    def test_actual_snapshot_uses_existing_outputs_and_targets(self):
        data = json.loads((APP / "library/design_catalog.json").read_text(encoding="utf-8"))
        self.assertIn("comfyWorkspace", data.get("browseLayout", {}).get("projects", {}).get("hon", {}))
        model = build_design_model(data, "hon", "comfy")
        families = model["sections"][2]["families"]
        self.assertEqual([f["id"] for f in families], ["character-still", "animation", "relighting", "actor-replacement", "lip-sync", "soundtrack"])
        self.assertTrue(all("<img" not in workflow_diagram_html(f) for f in families))
        self.assertTrue(any(link["assetID"].endswith("MEASURED_RETURN_20261012.txt") for link in families[3]["links"]))
        self.assertEqual(model["sections"][0]["assetIDs"], ["HD-COMFY-MOTION-V001", "HD-COMFY-RELIGHT-V001", "HD-COMFY-RELIGHT-V002", "HD-COMFY-IDENTITY-V001"])
        self.assertEqual([g["id"] for g in model["sections"][1]["groups"]], ["hon:comfy-likeness-HON-DOLO", "hon:comfy-likeness-LEIA", "hon:comfy-likeness-LUKE"])
        self.assertEqual([len(g["assetIDs"]) for g in model["sections"][1]["groups"]], [5, 1, 1])
        self.assertEqual(model["sections"][3]["assetIDs"], ["GEM-C0823C60", "HD-COMFY-RELIGHT-V002-CONTROL"])
        self.assertEqual(model["sections"][4]["assetIDs"], ["HD-AUDIO-REPLACE-V001"])
        self.assertEqual(len(model_asset_ids(model)), 14)
        self.assertNotIn("HD-B-91ef00348229", model_asset_ids(model))
        self.assertEqual(model_asset_ids(build_design_model(data, "lisan", "comfy")), [])


if __name__ == "__main__":
    unittest.main()
