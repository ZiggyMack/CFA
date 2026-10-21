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
from design_view import build_design_model, model_asset_ids
from library_helpers import effective_reviews

CATALOG = APP.parents[1] / "docs/notes/explorable_world/comfy/projects/visual_library/catalog.js"
CATALOG_HASH = "16db6f5f69d6444e093acfe42bf96e81fc37079f88c30c5df42be9a9235479b9"


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
        self.assertFalse(any(any(term in g["id"].lower() for term in ("mouth", "head", "viseme", "breather")) for g in comfy["sections"][0]["groups"]))
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
