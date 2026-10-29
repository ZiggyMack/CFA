"""Grouping and native-control checks for parity with the frozen local index."""
import copy
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP))
from design_view import build_design_model, cast_browse_groups, model_asset_ids
from library_helpers import effective_reviews

CATALOG = APP.parents[1] / "docs/notes/explorable_world/comfy/projects/visual_library/catalog.js"
# Reconciled 2026-10-28: handoff stages and saved reviews refreshed;
# media, scoped BOM, outfit, tattoo, mouth-coverage and archive records unchanged.
CATALOG_HASH = "067f1c621cbf092211cc48f0c78315b7ab3ab17e743655c6f47d7bcd4ed26e4e"


def walk(node):
    yield node
    for child in [*node.get("sections", []), *node.get("groups", [])]:
        yield from walk(child)


def named(node, title):
    return next(n for n in walk(node) if n.get("title") == title)


def fixture():
    ids = ["face", "HD-B-91ef00348229", "mouth-shape", "tattoo", "wrist", "outfit", "alternative", "old", "cast"]
    assets = [{"id": aid, "sha256": str(i + 1) * 64, "project": "hon", "kind": "image", "title": aid,
               "filename": aid + ".jpg", "src": "missing.jpg", "thumb": "missing.jpg", "album": "hon:outfit-vest", "category": "outfits"}
              for i, aid in enumerate(ids)]
    by_id = {a["id"]: a for a in assets}
    by_id["mouth-shape"]["album"] = "hon:mouth-v003-candidates"
    by_id["alternative"]["variant"] = "multiverse"
    fields = [("face", "identity", "identity"), ("HD-B-91ef00348229", "details", "dental_mouth_only"),
              ("mouth-shape", "details", "mouth_detail"), ("tattoo", "artwork", "tattoo_artwork_options"),
              ("wrist", "details", "visible_jewelry_only"), ("outfit", "wardrobe", "outfit")]
    return {"assets": assets, "projects": [{"id": "hon", "name": "Hon Dolo"}], "categories": [["outfits", "Outfits"]],
            "albums": [{"id": "hon:outfit-vest", "project": "hon", "category": "outfits", "title": "Smuggler vest", "assetIDs": ["outfit"]}],
            "reviewDecisions": [{"id": "alternative", "sha256": by_id["alternative"]["sha256"], "likenessRating": 5, "variant": "multiverse", "status": "needs_fixes", "storyboardStage": "production"}],
            "characterBOM": {"characters": [{"id": "hon:character-bom", "project": "hon", "coverAssetID": "face", "historyAssetIDs": ["old"],
                "entries": [{"assetID": aid, "sha256": by_id[aid]["sha256"], "section": sec, "role": role, "recordedSelection": "user_selected_component"} for aid, sec, role in fields]}]},
            "accessoryCollections": [{"id": "hon:accessories", "project": "hon", "title": "Jewelry", "assetIDs": ["wrist"], "coverID": "wrist"}],
            "sharedReferenceCollections": [{"id": "hon:mouths", "project": "hon", "title": "Mouth shapes & teeth details", "assetIDs": ["mouth-shape", "old"],
                "sections": [{"title": "Mouth shapes", "assetIDs": ["mouth-shape"]}, {"title": "Earlier mouths", "assetIDs": ["old"], "history": True}]}],
            "castCollections": [{"id": "hon:cast", "project": "hon", "title": "Supporting character", "coverID": "cast", "currentIDs": ["cast"], "assetIDs": ["cast"]}]}


class DesignModelTest(unittest.TestCase):
    def test_cast_studies_keep_core_selection_and_exact_character_routes(self):
        data = fixture()
        original = data["assets"][-1]
        for aid in ("dais", "counting", "earlier-repair", "bartender", "bouncer"):
            data["assets"].append({**original, "id": aid, "title": aid, "sha256": aid[0] * 64})
        group = data["castCollections"][0]
        group.update(workingReferenceIDs=["cast"], characterStudyIDs=["dais"], sceneStudyIDs=["counting"],
                     revisionStudyIDs=["earlier-repair"], sceneAssetIDs=["dais", "counting", "earlier-repair"],
                     sourceAlbumIDs=["hon:discovery"])
        for aid in ("bartender", "bouncer"):
            data["castCollections"].append({"id": "hon:" + aid, "project": "hon", "title": aid, "coverID": aid,
                                            "currentIDs": [aid], "assetIDs": [aid], "sourceAlbumIDs": ["hon:cast", "hon:discovery"]})
        before = copy.deepcopy(data)
        model = build_design_model(data, "hon", "working", album_id="hon:cast")
        working = model["sections"][0]["groups"][0]
        self.assertEqual(model_asset_ids(working), ["cast", "dais", "counting", "earlier-repair"])
        self.assertEqual(named(working, "Selected design references")["assetIDs"], ["cast"])
        self.assertFalse(any(s["assetIDs"] for s in walk(working) if s.get("title") == "Approved design references"))
        self.assertEqual(named(working, "Boss dais · character and staging candidates")["assetIDs"], ["dais"])
        self.assertEqual(named(working, "Earlier repair versions")["kind"], "disclosure")
        self.assertEqual([g["id"] for g in build_design_model(data, "hon", "cast", album_id="hon:cast")["sections"][0]["groups"]], ["hon:cast"])
        broad = build_design_model(data, "hon", "cast", album_id="hon:discovery")
        self.assertEqual([g["id"] for g in broad["sections"][0]["groups"]], ["hon:cast", "hon:bartender", "hon:bouncer"])
        removed = build_design_model(data, "hon", "working", {"dais": {"status": "remove"}}, album_id="hon:cast")
        self.assertNotIn("dais", model_asset_ids(removed))
        self.assertEqual(data, before, "Browsing studies must not change current IDs, selected references or approvals")

    def test_cast_story_links_require_recorded_membership_and_distinguish_plans(self):
        data = fixture()
        asset = data["assets"][-1]
        asset["roleDecision"] = "user_assigned"
        data["castCollections"][0]["sourceAlbumIDs"] = ["hon:outfit-vest"]
        data["shotMaterials"] = {"shots": [
            {"id": "planned", "project": "hon", "characterCollectionID": "hon:cast", "panelAssetIDs": []},
            {"id": "linked", "project": "hon", "panelAssetIDs": ["cast"]},
            {"id": "exact-material", "project": "hon", "panelAssetIDs": [], "materials": [{"assetID": "cast", "sha256": asset["sha256"]}]},
            {"id": "wrong-material", "project": "hon", "panelAssetIDs": [], "materials": [{"assetID": "cast", "sha256": "wrong"}]},
            {"id": "other-project", "project": "lisan", "characterCollectionID": "hon:cast", "panelAssetIDs": ["cast"]}]}
        before = copy.deepcopy(data)
        groups = build_design_model(data, "hon", "cast")["sections"][0]["groups"]
        facts = groups[0]["browseFacts"]
        self.assertEqual([s["id"] for s in facts["planned"]], ["planned", "exact-material"])
        self.assertEqual([s["id"] for s in facts["linked"]], ["linked"])
        self.assertEqual(len(cast_browse_groups(groups, "hon:outfit-vest", "roles")), 1)
        self.assertEqual(len(cast_browse_groups(groups, "unrelated", "roles")), 0)
        self.assertEqual(data, before)

    def test_explicit_multiverse_no_rating_approval_or_review_mutation(self):
        data = fixture()
        before = copy.deepcopy(data)
        reviews = effective_reviews(data["assets"], data["reviewDecisions"], {})
        before_reviews = copy.deepcopy(reviews)
        model = build_design_model(data, "hon", "working", reviews)
        self.assertEqual(named(model, "Approved Multiverse")["assetIDs"], [])
        self.assertEqual(named(model, "Multiverse candidates")["assetIDs"], ["alternative"])
        reviews["alternative"]["multiverseSelection"] = "approved"
        model = build_design_model(data, "hon", "working", reviews)
        self.assertEqual(named(model, "Approved Multiverse")["assetIDs"], ["alternative"])
        for rating in (None, 1, True):
            reviews["alternative"]["likenessRating"] = rating
            self.assertEqual(named(build_design_model(data, "hon", "working", reviews), "Approved Multiverse")["assetIDs"], [])
            self.assertEqual(reviews["alternative"]["multiverseSelection"], "approved")
        self.assertEqual(data, before)
        for key in ("status", "variant", "storyboardStage"):
            self.assertEqual(reviews["alternative"][key], before_reviews["alternative"][key])

    def test_nested_order_dental_wip_and_archive_restore(self):
        data = fixture()
        model = build_design_model(data, "hon", "Working references")
        groups = model["sections"][0]["groups"]
        self.assertEqual([g["id"] for g in groups], ["hon:character-bom", "hon:cast-working"])
        lead = groups[0]
        titles = [s["title"] for s in lead["sections"]]
        self.assertLess(titles.index("Body art"), titles.index("Bling bling"))
        self.assertLess(titles.index("Bling bling"), titles.index("Wardrobe"))
        self.assertEqual(named(lead, "Approved details and placement")["assetIDs"], ["HD-B-91ef00348229", "wrist"])
        self.assertIn("mouth-shape", model_asset_ids(named(lead, "Verbose BOM")))
        wip = named(lead, "WIP (work in progress)")
        self.assertEqual(wip["kind"], "disclosure")
        self.assertEqual(wip["sections"], [])
        self.assertEqual(wip["assetIDs"], ["alternative"])
        self.assertNotIn("old", model_asset_ids(model))
        archive = build_design_model(data, "hon", "Archive")
        self.assertEqual(model_asset_ids(archive), ["old"])
        review = effective_reviews(data["assets"], data["reviewDecisions"], {})
        review["old"] = {"collectionState": "working", "status": "needs_fixes"}
        self.assertNotIn("old", model_asset_ids(build_design_model(data, "hon", "archive", review)))
        self.assertIn("old", model_asset_ids(build_design_model(data, "hon", "working", review)))
        review["old"]["status"] = "remove"
        self.assertNotIn("old", model_asset_ids(build_design_model(data, "hon", "working", review)))

    def test_character_route_search_and_no_fabricated_approvals(self):
        data = fixture()
        model = build_design_model(data, "hon", "working", album_id="hon:cast")
        self.assertEqual(len(model["sections"][0]["groups"]), 1)
        self.assertEqual(model_asset_ids(model), ["cast"])
        self.assertFalse(any(s["assetIDs"] for s in walk(model) if s.get("title") == "Approved design references"))
        searched = build_design_model(data, "hon", "outfits", query="missing phrase")
        self.assertEqual(model_asset_ids(searched), [])
        self.assertIsNone(build_design_model(data, "hon", "unhandled"))

    def test_mouth_slots_retain_missing_takes_observations_and_search(self):
        data = fixture()
        by_id = {a["id"]: a for a in data["assets"]}
        take = {"assetID": "mouth-shape", "sha256": by_id["mouth-shape"]["sha256"], "lookID": "current",
                "number": 1, "label": "REST", "revision": "v003", "yaw": "unknown", "pitch": "unknown"}
        data["mouthCoverage"] = {"looks": [{"id": "current", "title": "Current mouth", "project": "hon", "plannedNumbers": [1, 2]}],
            "items": [take], "articulationNumbers": [1, 2], "extendedNumbers": [],
            "observations": [{"assetID": "mouth-shape", "observation": "Attributed observation", "reviewer": {"actor": "Provider"}}]}
        model = build_design_model(data, "hon", "working")
        group = named(model, "Core articulation labels · 2")
        self.assertEqual(group["kind"], "disclosure")
        self.assertFalse(group.get("expanded", False))
        slots = group["sections"][0]["slots"]
        self.assertEqual(slots[0]["takes"], [take])
        self.assertEqual(slots[0]["observations"], data["mouthCoverage"]["observations"])
        self.assertEqual(slots[1]["assetIDs"], [])
        self.assertEqual(slots[1]["label"], "Missing candidate")
        searched = build_design_model(data, "hon", "working", query="rest")
        self.assertIn("mouth-shape", model_asset_ids(searched))
        for label in (None, "", "   "):
            data["mouthCoverage"]["items"][0]["label"] = label
            rendered = named(build_design_model(data, "hon", "working"), "Core articulation labels · 2")["sections"][0]["slots"]
            self.assertEqual(rendered[0]["label"], "Unlabeled reference")
            self.assertEqual(rendered[0]["takes"][0]["label"], label)
            self.assertEqual(rendered[1]["label"], "Missing candidate")
        del data["mouthCoverage"]["items"][0]["label"]
        rendered = named(build_design_model(data, "hon", "working"), "Core articulation labels · 2")["sections"][0]["slots"]
        self.assertEqual(rendered[0]["label"], "Unlabeled reference")
        self.assertNotIn("label", rendered[0]["takes"][0])


@unittest.skipUnless(CATALOG.is_file(), "The canonical source catalog is not distributed with the hosted app")
class FrozenCatalogParityTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        raw = CATALOG.read_bytes()
        if hashlib.sha256(raw).hexdigest() != CATALOG_HASH:
            raise AssertionError("Frozen catalog changed; reconcile parity expectations before testing")
        text = raw.decode("utf-8")
        cls.data = json.loads(text[text.index("=") + 1:].strip().removesuffix(";"))

    def test_exact_outfit_membership_and_counts(self):
        model = build_design_model(self.data, "hon", "outfits")
        self.assertEqual([len(s["groups"]) for s in model["sections"]], [6, 8, 8])
        group_ids = [g["id"] for s in model["sections"] for g in s["groups"]]
        self.assertEqual(len(set(group_ids)), 22)
        self.assertIn("hon:outfit-pinstripe", [g["id"] for g in model["sections"][0]["groups"]])
        single = build_design_model(self.data, "hon", "outfits", album_id="hon:outfit-vest")
        group = single["sections"][0]["groups"][0]
        self.assertEqual(len(group["assetIDs"]), 8)
        self.assertFalse(any("mouth" in n.get("title", "").lower() for n in walk(single)))

    def test_crocodile_studies_exact_hub_and_cast_origin_counts(self):
        before = copy.deepcopy(self.data["castCollections"])
        source = next(g for g in self.data["castCollections"] if g["id"] == "hon:boss-round01")
        anchor = "HD-RETURN-8421e7cfa1a0"
        self.assertEqual(source["currentIDs"], [anchor])
        self.assertEqual(source["workingReferenceIDs"], [anchor])
        self.assertEqual([len(source.get(key, [])) for key in ("characterStudyIDs", "sceneStudyIDs", "revisionStudyIDs")], [15, 15, 3])
        working = build_design_model(self.data, "hon", "working", album_id=source["id"])
        group = working["sections"][0]["groups"][0]
        self.assertEqual(len(model_asset_ids(group)), 34)
        self.assertEqual(named(group, "Selected design references")["assetIDs"], [anchor])
        self.assertFalse(any(s["assetIDs"] for s in walk(group) if s.get("title") == "Approved design references"))
        hub = build_design_model(self.data, "hon", "cast", album_id=source["id"])
        self.assertEqual([g["id"] for g in hub["sections"][0]["groups"]], [source["id"]])
        self.assertEqual(len(model_asset_ids(hub)), 34)
        groups = build_design_model(self.data, "hon", "cast")["sections"][0]["groups"]
        self.assertEqual([len(cast_browse_groups(groups, connection=value)) for value in ("all", "roles", "planned", "linked")], [11, 3, 2, 1])
        self.assertEqual([g["id"] for g in cast_browse_groups(groups, "hon:boss-round01")],
                         ["hon:boss-round01", "hon:cast-bartender", "hon:cast-bouncer"])
        self.assertFalse(hub["sections"][0]["groups"][0]["browseFacts"]["linked"], "Crocodile scene-study folders are not storyboard use")
        self.assertEqual(self.data["castCollections"], before)

    def test_real_bom_and_lisan_visible_reference_pins(self):
        model = build_design_model(self.data, "hon", "working")
        detail = named(model, "Approved details and placement")
        self.assertEqual(detail["assetIDs"].count("HD-B-91ef00348229"), 1)
        for aid in ("HD-DROP-b18c4a123579", "HD-RETURN-9ace849985b4", "HD-RETURN-7b156019ddf8", "HD-RETURN-7fe77eadd174"):
            self.assertIn(aid, detail["assetIDs"])
        self.assertNotIn("HD-B-708df0bb5bff", detail["assetIDs"])
        self.assertIn("HD-B-708df0bb5bff", model_asset_ids(named(model, "Verbose BOM")))
        lisan = build_design_model(self.data, "lisan", "working")
        board = next(n for n in walk(lisan) if n.get("kind") == "reference_board")
        self.assertEqual(len(board["rows"]), 5)
        for row in board["rows"]:
            self.assertEqual(lisan["assets"][row["assetID"]]["sha256"], row["asset"]["sha256"])

    def test_mouth_coverage_and_scoped_deep_links(self):
        model = build_design_model(self.data, "hon", "working")
        iced = named(model, "Hon · optional iced r4")
        slots = [slot for node in walk(iced) for slot in node.get("slots", [])]
        self.assertEqual(len(slots), 50)
        self.assertTrue(all(not slot["assetIDs"] for slot in slots))
        self.assertTrue(iced["expanded"])
        self.assertFalse(any("earlier mouth revision" in node.get("title", "") for node in walk(model)))
        natural = named(build_design_model(self.data, "lisan", "working"), "Lisan · natural teeth · v001 + v002")
        numbers = [slot["number"] for node in walk(natural) for slot in node.get("slots", [])]
        self.assertEqual(len(numbers), 49)
        self.assertNotIn(47, numbers)
        original = next(r for r in self.data["characterReferenceBoard"]["rows"] if r["id"] == "natural-face")
        searched = build_design_model(self.data, "lisan", "working", query="No automatic ink-criterion binding")
        board = next(n for n in walk(searched) if n.get("kind") == "reference_board")
        self.assertEqual([row["assetID"] for row in board["rows"]], [original["asset"]["id"]])
        grill = build_design_model(self.data, "hon", "details", album_id="hon:grillz")
        self.assertEqual([g["title"] for s in grill["sections"] for g in s.get("groups", [])], ["Grills"])
        eye = build_design_model(self.data, "hon", "details", album_id="hon:tattoo-eye")
        self.assertEqual([g["id"] for s in eye["sections"] for g in s.get("groups", [])], ["hon:tattoo-eye"])

    def test_tattoo_overview_order_no_duplicate_map_or_acceptance(self):
        model = build_design_model(self.data, "hon", "details")
        eye = next(g for g in model["sections"][0]["groups"] if g["id"] == "hon:tattoo-eye")
        overview = eye["sections"][0]
        self.assertEqual(overview["kind"], "columns")
        self.assertEqual([s["assetIDs"] for s in overview["sections"]], [["HD-TATGUIDE-91d44599bd8c"], ["HD-LOCATION-EYE-20261012"], ["HD-TATGUIDE-b6eb3258a6ae"]])
        occurrences = [aid for node in walk({"sections": eye["sections"]}) for aid in node.get("assetIDs", [])]
        self.assertEqual(occurrences.count("HD-LOCATION-EYE-20261012"), 1)
        self.assertIn("revision needed", overview["sections"][2]["title"])
        self.assertEqual(eye["sections"][2]["title"], "Body appearances")
        self.assertEqual([g["title"] for g in model["sections"][1]["groups"]], ["Grills", "Piercings and jewelry", "Guns"])

    def test_comfy_bosses_archive_and_missing_files(self):
        comfy = build_design_model(self.data, "hon", "comfy")
        self.assertEqual([s["title"] for s in comfy["sections"]], ["Comfy outputs", "Likeness targets", "Workflow recipes",
                                                                    "Source clips & control guides", "Local finishing"])
        self.assertEqual(named(comfy, "Comfy outputs")["assetIDs"], ["HD-COMFY-MOTION-V001", "HD-COMFY-RELIGHT-V001",
                                                                    "HD-COMFY-RELIGHT-V002", "HD-COMFY-IDENTITY-V001"])
        targets = named(comfy, "Likeness targets")["groups"]
        self.assertEqual([g["id"] for g in targets], ["hon:comfy-likeness-HON-DOLO", "hon:comfy-likeness-LEIA", "hon:comfy-likeness-LUKE"])
        self.assertEqual([len(g["assetIDs"]) for g in targets], [5, 1, 1])
        self.assertTrue(all(g["directSingle"] for g in targets))
        self.assertFalse(any(any(term in g["id"].lower() for term in ("mouth", "head", "viseme", "breather")) for g in targets))
        for aid in ("HD-LIKENESS-02", "HD-B-91ef00348229", "HD-B-708df0bb5bff"):
            self.assertNotIn(aid, model_asset_ids(comfy), "Group photograph and repeated mouth libraries stay out of Comfy galleries")
        recipes = named(comfy, "Workflow recipes")
        self.assertEqual(recipes["kind"], "workflow_families")
        self.assertEqual([family["id"] for family in recipes["families"]],
                         ["character-still", "animation", "relighting", "actor-replacement", "lip-sync", "soundtrack"])
        self.assertEqual(model_asset_ids(recipes), [], "Recipe ingredient links do not duplicate image galleries")
        cast = build_design_model(self.data, "hon", "cast")
        boss = named(cast, "Creature boss ideas")
        self.assertEqual(len(boss["assetIDs"]), 12)
        self.assertFalse(set(boss["assetIDs"]) & set(model_asset_ids(cast["sections"][0])))
        archive = build_design_model(self.data, "hon", "archive")
        self.assertIn("HD-LIKENESS-02", model_asset_ids(archive))
        self.assertNotIn("HD-B-91ef00348229", model_asset_ids(archive))
        self.assertNotIn("HD-TATGUIDE-b6eb3258a6ae", model_asset_ids(archive))
        leaves = [aid for n in walk(archive) if not n.get("sections") and not n.get("groups") for aid in n.get("assetIDs", [])]
        self.assertEqual(len(leaves), len(set(leaves)))
        self.assertEqual(set(leaves), set(model_asset_ids(archive)))
        self.assertTrue(all(aid in archive["assets"] for aid in leaves))


class NativeDesignControlsTest(unittest.TestCase):
    def test_cast_source_and_story_controls_preserve_reviews(self):
        from streamlit.testing.v1 import AppTest
        data = fixture()
        original = data["assets"][-1]
        original["roleDecision"] = "user_assigned"
        data["castCollections"][0]["sourceAlbumIDs"] = ["hon:outfit-vest"]
        for aid in ("bartender", "bouncer"):
            data["assets"].append({**original, "id": aid, "title": aid, "sha256": aid[0] * 64, "roleDecision": None})
            data["castCollections"].append({"id": "hon:" + aid, "project": "hon", "title": aid,
                                            "assetIDs": [aid], "currentIDs": [aid], "coverID": aid})
        data["shotMaterials"] = {"shots": [
            {"id": "planned", "project": "hon", "title": "Planned bar", "characterCollectionID": "hon:cast", "panelAssetIDs": []},
            {"id": "linked", "project": "hon", "title": "Bouncer panel", "panelAssetIDs": ["bouncer"]}]}
        script = "\n".join([
            "import sys, json", "from pathlib import Path", "import streamlit as st", f"sys.path.insert(0, {str(APP)!r})",
            "from design_view import render_design_view", f"data = json.loads({json.dumps(data)!r})",
            "st.session_state.setdefault('saved_reviews', {'cast': {'status':'needs_fixes','note':'Keep the reference separate'}})",
            f"render_design_view(data, 'hon', 'cast', Path({str(APP / 'library')!r}), lambda rows, context: None, lambda asset: None, reviews=st.session_state.saved_reviews)"])
        app = AppTest.from_string(script, default_timeout=20).run()
        self.assertFalse(app.exception)
        before = copy.deepcopy(app.session_state["saved_reviews"])
        context = "design:hon:cast:root"
        self.assertEqual(app.button(key=context + ":filter:all").label, "All characters · 3")
        app.button(key=context + ":filter:planned").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.button(key=context + ":filter:planned").proto.type, "primary")
        self.assertIn("**Supporting character**", [m.value for m in app.markdown])
        self.assertNotIn("**bouncer**", [m.value for m in app.markdown])
        app.selectbox(key=context + ":source").select("hon:outfit-vest").run()
        self.assertEqual(app.button(key=context + ":filter:linked").label, "Storyboard-linked · 0")
        app.button(key=context + ":filter:linked").click().run()
        self.assertTrue(any("No characters match" in item.value for item in app.info))
        app.button(key=context + ":clear").click().run()
        self.assertEqual(app.selectbox(key=context + ":source").value, "all")
        self.assertEqual(app.button(key=context + ":filter:all").proto.type, "primary")
        app.button(key=context + ":0:expanded:hon:cast:toggle").click().run()
        self.assertFalse(app.exception)
        self.assertTrue(any(e.label == "Origin & story connections" for e in app.expander))
        self.assertTrue(any("no panel linked yet" in c.value for c in app.caption))
        self.assertEqual(app.session_state["saved_reviews"], before)

    def test_outfit_tag_highlight_and_filter_change_together(self):
        from streamlit.testing.v1 import AppTest
        data = fixture()
        names = [("yellow", "Formal sample"), ("rain", "Casual sample"), ("vest", "Scoundrel sample")]
        data["assets"] = [{"id": name, "sha256": str(i + 1) * 64, "project": "hon", "kind": "image", "title": title,
                           "album": "hon:outfit-" + name, "category": "outfits"} for i, (name, title) in enumerate(names)]
        data["albums"] = [{"id": a["album"], "project": "hon", "category": "outfits", "title": a["title"], "assetIDs": [a["id"]]}
                          for a in data["assets"]]
        script = """
import sys
from pathlib import Path
sys.path.insert(0, APP_PATH)
from design_view import render_design_view
render_design_view(FIXTURE, 'hon', 'outfits', Path(APP_PATH)/'library', lambda rows, context: None, lambda asset: None)
""".replace("APP_PATH", repr(str(APP))).replace("FIXTURE", repr(data))
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "outfit_tags_app.py"
            path.write_text(script, encoding="utf-8")
            app = AppTest.from_file(str(path)).run(timeout=25)
            self.assertFalse(app.exception)
            button = lambda label: next(b for b in app.button if b.label == label)
            self.assertEqual(button("All outfits").proto.type, "primary")
            button("Casual").click().run(timeout=25)
            self.assertFalse(app.exception)
            self.assertEqual(button("Casual").proto.type, "primary")
            self.assertEqual(button("All outfits").proto.type, "secondary")
            self.assertEqual([e.label for e in app.expander], ["Casual · 1 outfits"])
            self.assertIn("**Casual sample**", [m.value for m in app.markdown])
            self.assertNotIn("**Formal sample**", [m.value for m in app.markdown])
            button("All outfits").click().run(timeout=25)
            self.assertFalse(app.exception)
            self.assertEqual(button("All outfits").proto.type, "primary")
            self.assertEqual(button("Casual").proto.type, "secondary")
            self.assertEqual(len(app.expander), 3)

    @unittest.skipUnless(CATALOG.is_file(), "The actual nullable Lisan source is not distributed with the hosted app")
    def test_actual_nullable_lisan_slot_renders_without_changing_source(self):
        from streamlit.testing.v1 import AppTest
        raw = CATALOG.read_bytes()
        self.assertEqual(hashlib.sha256(raw).hexdigest(), CATALOG_HASH)
        text = raw.decode("utf-8")
        data = json.loads(text[text.index("=") + 1:].strip().removesuffix(";"))
        source = next(r for r in data["mouthCoverage"]["items"] if r["assetID"] == "LAG-PART-1b60815fa2bb")
        self.assertIsNone(source["label"])
        asset = next(a for a in data["assets"] if a["id"] == source["assetID"])
        look = next(g for g in data["mouthCoverage"]["looks"] if g["id"] == source["lookID"])
        small = {"assets": [asset], "projects": [{"id": "lisan", "name": "Lisan Al Gaib"}],
                 "characterBOM": {"characters": [{"project": "lisan", "coverAssetID": asset["id"], "entries": []}]},
                 "mouthCoverage": {"items": [source], "looks": [look], "articulationNumbers": [], "extendedNumbers": []}}
        before = copy.deepcopy(small)
        slot = next(slot for n in walk(build_design_model(small, "lisan", "working")) for slot in n.get("slots", []))
        self.assertEqual(slot["label"], "Unlabeled reference")
        self.assertEqual(slot["takes"], [source])
        self.assertEqual(small, before)
        script = """
import sys
from pathlib import Path
sys.path.insert(0, APP_PATH)
import streamlit as st
from design_view import render_design_view
def grid(rows, signature):
    for asset, _ in rows:
        st.caption(asset['title'])
render_design_view(FIXTURE, 'lisan', 'working', Path(APP_PATH)/'library', grid, lambda asset: None)
""".replace("APP_PATH", repr(str(APP))).replace("FIXTURE", repr(small))
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "nullable_lisan_app.py"
            path.write_text(script, encoding="utf-8")
            app = AppTest.from_file(str(path)).run(timeout=25)
            self.assertFalse(app.exception)
            next(b for b in app.button if b.label == "Show references").click().run(timeout=25)
            self.assertFalse(app.exception)
            self.assertIn("**Reference · Unlabeled reference**", [m.value for m in app.markdown])
            self.assertTrue(any(b.label == "LAG-PART-1b60815fa2bb · v001" for b in app.button))

    def test_collapsed_character_and_review_callback(self):
        from streamlit.testing.v1 import AppTest
        script = """
import sys
from pathlib import Path
sys.path.insert(0, APP_PATH)
import streamlit as st
from design_view import render_design_view
data = FIXTURE
def open_reference(asset):
    st.session_state['selected'] = asset['id']
def grid(rows, signature):
    for asset, _ in rows:
        st.button(asset['title'], key=signature+':'+asset['id'], on_click=open_reference, args=(asset,))
render_design_view(data, 'hon', 'working', Path(APP_PATH)/'library', grid, open_reference)
""".replace("APP_PATH", repr(str(APP))).replace("FIXTURE", repr(fixture()))
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "design_test_app.py"
            path.write_text(script, encoding="utf-8")
            app = AppTest.from_file(str(path)).run(timeout=25)
            self.assertFalse(app.exception)
            self.assertNotIn("Body art", [n.value for n in app.subheader])
            next(b for b in app.button if b.label == "Show references").click().run(timeout=25)
            self.assertFalse(app.exception)
            self.assertIn("Body art", [n.value for n in app.subheader])
            next(b for b in app.button if b.label == "tattoo").click().run(timeout=25)
            self.assertFalse(app.exception)
            self.assertEqual(app.session_state["selected"], "tattoo")
            self.assertEqual(len([b.key for b in app.button]), len(set(b.key for b in app.button)))


if __name__ == "__main__":
    unittest.main()
