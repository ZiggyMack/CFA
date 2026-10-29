"""Focused checks for portable review behavior; no generation or network calls."""

import copy
import hashlib
import io
import json
import shutil
import sys
import tempfile
import types
import unittest
import zipfile
from pathlib import Path

APP_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_DIR))
from library_helpers import (
    EXPORT_FORMAT, FAVORITES_FORMAT, REVIEW_FORMAT, basket_payload, basket_zip, collaborator_sections, document_tree, effective_reviews, export_allowed, favorite_payload,
    handoff_payload, handoff_text, layout_video_assets, media_path, mission_tasks, normalize_plan, ordered_assets,
    production_workflows, read_basket, read_favorites, read_review, review_payload, sort_video_assets, storyboard_stage, storyboard_themes, storyboard_window, sweep_payload,
)


class LibraryHelpersTest(unittest.TestCase):
    def test_storyboard_stage_is_independent_and_hash_restorable(self):
        assets = [{"id": "panel", "sha256": "one", "category": "storyboard"},
                  {"id": "clip", "sha256": "two", "category": "videos", "storyboardStage": "detailed_design"},
                  {"id": "photo", "sha256": "three", "category": "working"}]
        self.assertEqual(storyboard_stage(assets[0], {}), "preliminary")
        self.assertEqual(storyboard_stage(assets[1], {}), "detailed_design")
        self.assertIsNone(storyboard_stage(assets[2], {}))
        reviews, _, skipped = read_review({"format": REVIEW_FORMAT, "items": [
            {"id": "clip", "sha256": "two", "storyboardStage": "production"}]}, assets)
        self.assertEqual(skipped, 0)
        self.assertEqual(storyboard_stage(assets[1], reviews), "production")
        self.assertNotIn("status", reviews["clip"])
        self.assertNotIn("workingReference", reviews["clip"])
        restored, _, _ = read_review(review_payload(assets, reviews, set()), assets)
        self.assertEqual(restored["clip"]["storyboardStage"], "production")
        self.assertEqual(storyboard_stage(assets[1], {"clip": {"storyboardStage": None}}), "detailed_design")

    def test_asset_scoped_working_reference_survives_partial_seed_and_explicit_clear(self):
        assets = [{"id": "clip", "sha256": "original", "workingReference": {"status": "approved", "scope": "scene"}}]
        seeds = [{"id": "clip", "sha256": "original", "note": "Creative approval only."}]
        reviews = effective_reviews(assets, seeds, {})
        self.assertEqual(reviews["clip"]["workingReference"], {"status": "approved", "scope": "scene"})
        self.assertEqual(reviews["clip"]["note"], "Creative approval only.")
        self.assertIsNone(effective_reviews(assets, seeds, {"clip": {"workingReference": None}})["clip"]["workingReference"])
    def test_variant_merge_preserves_fresh_canonical_seed_and_user_override(self):
        assets = [{"id": "armor", "sha256": "abc"}]
        seeds = [{"id": "armor", "sha256": "abc", "variant": "multiverse", "status": None}]
        for stale in ({"note": "Still useful"}, {"variant": "prime", "variantSource": "catalog", "note": "Still useful"}):
            imported, _, _ = read_review({"format": REVIEW_FORMAT, "items": [{"id": "armor", "sha256": "abc", **stale}]}, assets)
            self.assertEqual(effective_reviews(assets, seeds, imported)["armor"]["variant"], "multiverse")
        imported, _, _ = read_review({"format": REVIEW_FORMAT, "items": [{"id": "armor", "sha256": "abc", "variant": "prime", "variantSource": "user"}]}, assets)
        self.assertEqual(effective_reviews(assets, seeds, imported)["armor"]["variant"], "prime")

    def test_export_gates_archives_removals_variants_and_sweep_preserves_backup(self):
        assets = [{"id": key, "sha256": key, "project": "hon", "kind": "image", "archived": key == "archived"}
                  for key in ("prime", "multi", "remove", "archived")]
        plan = {"destinations": ["Flow"], "idea": "Scene", "prompt": ""}
        reviews = {key: {"status": "remove" if key == "remove" else None, "variant": "multiverse" if key == "multi" else "prime",
                         "workingReference": {"status": "requested", "scope": "outfit"}, "shotPlan": plan}
                   for key in ("prime", "multi", "remove", "archived")}
        ids = {a["id"] for a in assets}
        self.assertEqual([a["id"] for a in basket_payload(assets, ids, reviews)["items"]], ["prime"])
        self.assertEqual([a["id"] for a in basket_payload(assets, ids, reviews, "multiverse_ingredients")["items"]], ["prime", "multi"])
        self.assertEqual([a["id"] for a in handoff_payload(assets, reviews, "hon", "Flow")["items"]], ["prime"])
        self.assertEqual([a["id"] for a, _ in ordered_assets(assets, [], "hon")], ["prime", "multi", "remove"])
        self.assertEqual(len(ordered_assets(assets, [], "hon", include_archived=True)), 4)
        sweep = sweep_payload(assets, reviews, ids, ids)
        self.assertEqual(len(sweep["items"]), 4)
        self.assertEqual(len(sweep["favorites"]), 4)
        self.assertEqual([r["id"] for r in sweep["sweep"]["promotionQueue"]], ["prime"])

    def test_document_parents_and_story_window_narrow_themes(self):
        docs = [{"id": str(i), "kind": "document", "filename": f"note{i}.txt", "album": f"Design and outfit notes · {name}", "text": "outfit"}
                for i, name in enumerate(("Coat", "Vest", "Coat"))]
        tree = document_tree(docs)
        self.assertEqual(list(tree), ["Design & outfit notes"])
        self.assertEqual({key: len(value) for key, value in tree["Design & outfit notes"].items()}, {"Coat": 2, "Vest": 1})
        self.assertEqual(list(document_tree(docs, "vest")["Design & outfit notes"]), ["Vest"])
        rows = [({"id": "early", "storyboardPosition": 10, "storyboardOrder": 1, "tags": ["money"]}, None),
                ({"id": "late", "storyboardPosition": 80, "storyboardOrder": 2, "tags": ["love"]}, None)]
        window = storyboard_window(rows, 50, 100)
        self.assertEqual([asset["id"] for asset, _ in window], ["late"])
        self.assertEqual({theme for asset, album in window for theme in storyboard_themes(asset, album)}, {"love"})
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

    def test_video_sort_preserves_recommended_order_and_puts_unknowns_last(self):
        rows = [({"id": "short", "title": "Zulu", "duration": 10}, {"id": "performance"}),
                ({"id": "unknown", "title": "Alpha"}, {"id": "misc"}),
                ({"id": "long", "title": "Beta", "duration": 40}, {"id": "action"})]
        self.assertEqual(sort_video_assets(rows, "Recommended"), rows)
        self.assertEqual([r[0]["id"] for r in sort_video_assets(rows, "Longest")], ["long", "short", "unknown"])
        self.assertEqual([r[0]["id"] for r in sort_video_assets(rows, "Shortest")], ["short", "long", "unknown"])
        self.assertEqual([r[0]["id"] for r in sort_video_assets(rows, "Alphabetical")], ["unknown", "long", "short"])

    def test_video_layout_and_duration_sort_are_independent(self):
        turnaround = {"id": "turnaround", "title": "Turnaround videos"}
        action = {"id": "action", "title": "Action videos"}
        rows = [({"id": "turn", "title": "Turn", "duration": 3}, turnaround),
                ({"id": "zulu", "title": "Zulu", "duration": 10}, action),
                ({"id": "alpha", "title": "Alpha", "duration": 10}, action),
                ({"id": "long", "title": "Long", "duration": 40}, action),
                ({"id": "unknown", "title": "Unknown"}, action)]
        grouped = layout_video_assets(rows, "Grouped", "Longest first")
        self.assertEqual([r[0]["id"] for r in grouped], ["long", "alpha", "zulu", "unknown", "turn"])
        self.assertEqual(grouped[0][1], action)
        flat = layout_video_assets(rows, "All clips", "Shortest")
        self.assertEqual([r[0]["id"] for r in flat], ["turn", "alpha", "zulu", "long", "unknown"])
        self.assertTrue(all(album is None for _, album in flat))

    def test_collaborator_sections_keep_roles_shared_and_current_grok_visible(self):
        assets = [{"id": "roles", "kind": "document", "filename": "provider_roles.txt", "album": "Collaborator briefs · Flow"},
                  {"id": "current", "kind": "document", "filename": "START_HERE.txt", "album": "Grok care package · October 8"},
                  {"id": "old", "kind": "document", "filename": "grok_project_instructions.txt", "album": "Historical collaborator briefs"},
                  {"id": "flow", "kind": "document", "filename": "flow_start_here.txt"},
                  {"id": "workflow", "kind": "document", "filename": "workflow_notes.txt"}]
        sections = collaborator_sections(assets)
        self.assertEqual([a["id"] for a in sections["Shared roles"]], ["roles"])
        self.assertEqual([a["id"] for a in sections["Grok"]], ["current"])
        self.assertEqual([a["id"] for a in sections["Flow"]], ["flow"])

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

    def test_seed_merge_clear_and_plan_removal_survive_export_restore(self):
        assets = [{"id": "cash", "sha256": "cash-hash", "project": "hon", "sourceStatus": "needs_review"}]
        seeds = [{"id": "cash", "sha256": "cash-hash", "status": "needs_fixes", "note": "Keep the vest only.",
                  "shotPlan": {"destinations": ["Grok"], "idea": "Fix the tattoos", "prompt": "Keep the vest"}}]
        before = copy.deepcopy((assets, seeds))
        reviews = effective_reviews(assets, seeds, {"cash": {"status": None}})
        self.assertIsNone(reviews["cash"]["status"])
        self.assertEqual(reviews["cash"]["note"], "Keep the vest only.")
        self.assertEqual(reviews["cash"]["shotPlan"]["destinations"], ["Grok"])
        reviews = effective_reviews(assets, seeds, {"cash": {"status": None, "shotPlan": None}})
        restored, favorites, skipped = read_review(review_payload(assets, reviews, {"cash"}), assets)
        self.assertEqual(effective_reviews(assets, seeds, restored), reviews)
        self.assertEqual((favorites, skipped), ({"cash"}, 0))
        self.assertEqual((assets, seeds), before)

    def test_review_import_requires_matching_hash_and_rejects_bad_fields(self):
        assets = [{"id": "one", "sha256": "abc"}, {"id": "two", "sha256": "def"}]
        payload = {"format": REVIEW_FORMAT, "items": [
            {"id": "one", "sha256": "changed", "status": "remove"},
            {"id": "one", "status": "keep"},
            {"id": "two", "sha256": "def", "status": "invalid"},
            {"id": "one", "sha256": "abc", "status": "keep", "note": "Only the coat",
             "shotPlan": {"status": "generated", "destinations": ["Flow"], "idea": "Board ship"}}],
            "favorites": [{"id": "one"}, {"id": "two", "sha256": "def"}]}
        reviews, favorites, skipped = read_review(payload, assets)
        self.assertEqual(skipped, 4)
        self.assertEqual(favorites, {"two"})
        self.assertEqual(reviews["one"]["shotPlan"]["status"], "planned")
        self.assertEqual(effective_reviews(assets, [{"id": "one", "sha256": "wrong", "status": "remove"}], {}), {})

    def test_legacy_note_import_does_not_clear_seed_decision(self):
        assets = [{"id": "one", "sha256": "abc"}]
        favorites = favorite_payload(assets, {"one"}, {"one": "Correct only the teeth"})
        overrides, stars, skipped = read_review(favorites, assets)
        seeded = [{"id": "one", "sha256": "abc", "status": "needs_fixes", "note": "Original"}]
        restored = effective_reviews(assets, seeded, overrides)
        self.assertEqual(restored["one"]["status"], "needs_fixes")
        self.assertEqual(restored["one"]["note"], "Correct only the teeth")
        self.assertEqual((stars, skipped), ({"one"}, 0))

    def test_provider_handoff_preserves_scope_and_filters_project_destination(self):
        assets = [{"id": key, "sha256": key + "hash", "project": project, "filename": key + ".jpg",
                   "category": "outfits", "repoPath": "references/" + key + ".jpg"}
                  for key, project in (("coat", "hon"), ("parka", "hon"), ("neck", "lisan"))]
        reviews = {key: {"status": "needs_fixes", "note": "Keep the outfit; fix tattoos",
                         "shotPlan": {"destinations": destinations, "idea": "Board ship", "prompt": "Preserve identity"}}
                   for key, destinations in (("coat", ["Grok", "Flow"]), ("parka", ["undecided"]), ("neck", ["Flow"]))}
        payload = handoff_payload(assets, reviews, "hon", "Flow")
        self.assertEqual([r["id"] for r in payload["items"]], ["coat"])
        text = handoff_text(payload)
        for needed in ("coat.jpg", "coathash", "outfits", "Keep the outfit; fix tattoos", "Preserve identity", "not an image ZIP", "not sent or generated"):
            self.assertIn(needed, text)
        self.assertEqual(normalize_plan({"destinations": ["undecided", "Flow", "Flow"]})["destinations"], ["Flow"])
        self.assertEqual(normalize_plan({"destinations": []})["destinations"], ["undecided"])

    def test_mission_cards_validate_status_and_exclude_local_href_links(self):
        task = {"id": "task-1", "provider": "Grok", "project": "hon", "title": "Fix coat",
                "status": "ready", "summary": "Preserve coat", "nextAction": "Attach references",
                "missing": [], "links": [{"label": "Brief", "assetID": "brief"},
                                            {"label": "Private", "href": "D:/private/notes.txt"}]}
        valid = mission_tasks({"tasks": [task, task, {**task, "id": "bad", "status": "sent"},
                                         {**task, "id": "other", "provider": None}]})
        self.assertEqual(len(valid), 1)
        self.assertEqual(valid[0]["links"], [{"label": "Brief", "assetID": "brief"}])
        self.assertEqual(task["links"][1]["href"], "D:/private/notes.txt")

    def test_production_workflow_cloud_links_are_scoped_and_refs_remain_data(self):
        workflow = {"id": "wf-1", "provider": "ComfyUI", "project": "hon", "title": "Replace clip audio",
                    "status": "Local preview complete; Cloud saved and validated, not run.", "summary": "Preserve pictures; replace audio",
                    "nextAction": "Choose the song segment", "sourceAssetIDs": ["input"], "outputAssetIDs": ["output"],
                    "documentAssetIDs": ["graph"], "cloudURL": "https://cloud.comfy.org/workflows/test"}
        result = production_workflows([workflow])
        self.assertEqual(result[0]["cloudURL"], workflow["cloudURL"])
        self.assertEqual(result[0]["status"], workflow["status"])
        self.assertEqual(result[0]["sourceAssetIDs"], ["input"])
        for url in ("http://cloud.comfy.org/workflow", "https://cloud.comfy.org.evil.test/workflow", "javascript:alert(1)", "D:/private/workflow.json"):
            self.assertNotIn("cloudURL", production_workflows([{**workflow, "cloudURL": url}])[0])

    def test_export_basket_hashes_and_zip_deduplicate_review_copies_without_writes(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "preview.jpg").write_bytes(b"hosted review copy")
            assets = [{"id": key, "sha256": "original-hash", "src": "preview.jpg", "filename": key + ".png",
                       "project": project, "category": "outfits"} for key, project in (("one", "hon"), ("two", "lisan"))]
            before = {p.name: p.read_bytes() for p in root.iterdir()}
            payload = basket_payload(assets, {"one", "two"})
            self.assertEqual(payload["format"], EXPORT_FORMAT)
            self.assertEqual(read_basket(payload, assets), ({"one", "two"}, 0))
            payload["items"][0]["sha256"] = "changed"
            self.assertEqual(read_basket(payload, assets), ({"two"}, 1))
            with zipfile.ZipFile(io.BytesIO(basket_zip(root, assets, {"one", "two"}))) as archive:
                manifest = json.loads(archive.read("manifest.json"))
                self.assertEqual(manifest["uniqueReviewCopies"], 1)
                self.assertEqual(len(manifest["items"]), 2)
                self.assertEqual(manifest["items"][0]["archivePath"], manifest["items"][1]["archivePath"])
                self.assertTrue(manifest["items"][0]["archivePath"].endswith(".jpg"))
                self.assertEqual(manifest["items"][0]["sha256"], "original-hash")
                self.assertEqual(hashlib.sha256(archive.read(manifest["items"][0]["archivePath"])).hexdigest(), manifest["items"][0]["reviewCopySha256"])
                self.assertEqual(len([name for name in archive.namelist() if name.startswith("review-copies/")]), 1)
            with self.assertRaises(ValueError):
                basket_zip(root, assets, {"one"}, max_bytes=2)
            with self.assertRaises(ValueError):
                basket_zip(root, [{**assets[0], "src": "../private.jpg"}], {"one"})
            self.assertEqual(before, {p.name: p.read_bytes() for p in root.iterdir()})


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
        for name in ("app.py", "library_helpers.py", "mission_view.py", "studio_dependencies.py"):
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
                    "beat": "The opening bargain.", "storyboardPosition": 70, "storyboardOrder": 1, "tags": ["love", "rescue"]},
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
                   "detailProfiles": [{"id": "hon-profile", "project": "hon", "character": "Hon Dolo", "title": "Hon Dolo details", "objects": [
                       {"id": "neck", "title": "Neck tattoo", "kind": "tattoo", "location": "neck", "status": "reference", "summary": "Preserve the selected placement.",
                        "assetIDs": ["hon-00"], "exampleAssetIDs": [], "stencilAssetIDs": ["hon-01"]}]}],
                   "productionWorkflows": [{"id": "audio-replace", "provider": "ComfyUI", "project": "hon", "title": "Clip soundtrack replacement",
                                            "status": "Local FFmpeg preview complete; Cloud saved and validated, not run.",
                                            "summary": "Preserve the picture while replacing its audio.", "nextAction": "Choose the next song segment.",
                                            "sourceAssetIDs": ["hon-00"], "outputAssetIDs": ["hon-01"], "documentAssetIDs": ["flow-doc"],
                                            "cloudURL": "https://cloud.comfy.org/workflows/example"}],
                   "missionControl": {"updated": "2026-10-08", "tasks": [
                       {"id": "fix-look", "provider": "Grok", "project": "hon", "title": "Correct the coat reference", "status": "ready",
                        "summary": "Keep the scene and outfit.", "nextAction": "Attach source and current LOCK-FACE.", "missing": [],
                        "links": [{"label": "Source look", "assetID": "hon-00"}, {"label": "Brief", "assetID": "gemini-doc"}]},
                       {"id": "lisan-shot", "provider": "Flow", "project": "lisan", "title": "Prepare Lisan motion", "status": "needs_input",
                        "summary": "A character motion study.", "nextAction": "Choose the shot action.", "missing": ["Action and camera choice"],
                        "links": [{"label": "Flow brief", "assetID": "flow-doc"}]}]},
                   "reviewDecisions": [{"id": "hon-00", "sha256": "hash-0", "status": "needs_fixes", "note": "Keep this outfit only."},
                                       {"id": "hon-01", "sha256": "hash-1", "status": "remove", "note": "Wrong teeth."},
                                       {"id": "hon-02", "sha256": "hash-2", "status": None, "note": "",
                                        "shotPlan": {"destinations": ["undecided"], "idea": "A winter shot", "prompt": ""}}],
                   "categories": [["outfits", "Outfits"], ["details", "Tattoos & piercings"], ["storyboard", "Storyboard"]],
                   "albums": [{"id": "hon:outfits", "project": "hon", "category": "outfits", "title": "Outfits",
                               "assetIDs": [a["id"] for a in images[:26]]},
                              {"id": "hon:story", "project": "hon", "category": "storyboard", "title": "Pay me first", "assetIDs": ["SB-01"]},
                              {"id": "hon:details", "project": "hon", "category": "details", "title": "Details", "assetIDs": ["hon-00", "hon-01"]},
                              {"id": "lisan:placement", "project": "lisan", "category": "details", "title": "Placement portraits", "assetIDs": ["lisan-neck"]}]}
        (library / "catalog.json").write_text(json.dumps(catalog), encoding="utf-8")

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    def app(self, library=True):
        app = self.AppTest.from_file(str(self.app_dir / "app.py"), default_timeout=15).run()
        self.assertFalse(app.exception)
        if library:
            app.button(key="nav:Library").click().run()
            self.assertFalse(app.exception)
        return app

    def test_corner_supplement_navigation_preserves_base_browsing_and_reviews(self):
        path = self.app_dir / "library" / "mission_control.json"
        base = json.loads((path.parent / "catalog.json").read_text(encoding="utf-8"))
        extra = {**base["assets"][0], "id": "corner-only", "sha256": "exact", "title": "Corner-only image"}
        snapshot = {"projects": base["projects"], "categories": [], "albums": [], "assets": [extra],
                    "reviewDecisions": [{"id": extra["id"], "sha256": "exact", "status": "needs_fixes",
                                         "likenessRating": 2, "sceneQualityRating": 5}],
                    "missionControl": {"tasks": [{"id": "corner", "provider": "CFA Nova", "project": "hon",
                         "status": "ready", "title": "Current Corner task", "summary": "Current", "nextAction": "Review",
                         "links": [{"label": "Open collection", "assetIDs": [extra["id"]]}]}]}}
        path.write_text(json.dumps(snapshot), encoding="utf-8")
        try:
            app = self.app(library=False)
            self.assertFalse(app.exception)
            self.assertTrue(any("Current Corner task" in e.label for e in app.expander))
            app.button(key="mission-collection:corner:0").click().run()
            app.button(key="corner-collection:corner-only").click().run()
            next(b for b in app.button if b.label == "← Back to the collection").click().run()
            self.assertTrue(any(b.key == "corner-collection:corner-only" for b in app.button))
            app.button(key="corner-collection:corner-only").click().run()
            app.button(key="favorite:selected:corner-only").click().run()
            app.button(key="nav:Favorites & notes").click().run()
            app.button(key="open:corner-only").click().run()
            self.assertFalse(app.exception)
            self.assertTrue(any(h.value == "Corner-only image" for h in app.subheader))
            self.assertEqual(app.session_state["studio_reviews"]["corner-only"]["likenessRating"], 2)
            app.button(key="nav:Library").click().run()
            self.assertFalse(any(b.key == "open:corner-only" for b in app.button))
        finally:
            path.unlink(missing_ok=True)

    def test_hot_redeploy_ignores_stale_generic_helper_and_mission_modules(self):
        import library_helpers as helpers
        stale_helpers = types.ModuleType("library_helpers")
        stale_helpers.__dict__.update({key: value for key, value in vars(helpers).items()
                                      if key != "mission_review_data"})
        stale_mission = types.ModuleType("mission_view")
        def stale_render(*args, **kwargs):
            raise AssertionError("The stale mission renderer was called")
        stale_mission.render_corner = stale_render
        missing = object()
        previous = {name: sys.modules.get(name, missing) for name in ("library_helpers", "mission_view")}
        sys.modules.update(library_helpers=stale_helpers, mission_view=stale_mission)
        try:
            with self.assertRaisesRegex(ImportError, "mission_review_data"):
                exec("from library_helpers import mission_review_data", {})
            app = self.app(library=False)
            self.assertFalse(app.exception)
            self.assertEqual(app.button(key="mission-shot-plans").label, "Shot plans · 1 →")
            self.assertTrue(any("Correct the coat reference" in e.label for e in app.expander))
            app.button(key="mission-shot-plans").click().run()
            self.assertFalse(app.exception)
            self.assertTrue(any(h.value == "All shot plans" for h in app.subheader))
        finally:
            for name, module in previous.items():
                if module is missing:
                    sys.modules.pop(name, None)
                else:
                    sys.modules[name] = module

    def test_pagination_selection_and_session_notes(self):
        app = self.app()
        self.assertEqual(len([b for b in app.button if (b.key or "").startswith("open:")]), 24)
        next(b for b in app.button if b.label == "Next →").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(len([b for b in app.button if (b.key or "").startswith("open:")]), 3)
        app.button(key="open:hon-24").click().run()
        self.assertFalse(app.exception)
        app.button(key="favorite:selected:hon-24").click().run()
        app.text_area(key="asset-note:hon-24").input("Keep this coat.").run()
        self.assertIn("hon-24", app.session_state["studio_favorites"])
        self.assertEqual(app.session_state["studio_notes"]["hon-24"], "Keep this coat.")
        app.button(key="nav:Favorites & notes").click().run()
        self.assertFalse(app.exception)
        self.assertTrue(any(b.key == "open:hon-24" for b in app.button))

    def test_storyboard_and_collaborator_briefs(self):
        app = self.app()
        app.button(key="nav:Storyboard").click().run()
        self.assertFalse(app.exception)
        self.assertTrue(any("Pay me first" in item.value for item in app.subheader))
        self.assertEqual(len([b for b in app.button if (b.key or "").startswith("open:")]), 1)
        app.button(key="nav:Collaborator briefs").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.code), 2)
        self.assertEqual([item.value for item in app.subheader], ["Gemini", "Flow", "Grok", "Shared roles"])
        self.assertTrue(any("Character creation" in item.value for item in app.markdown))

    def test_project_switch_and_empty_unassigned_hidden(self):
        app = self.app()
        app.selectbox(key="studio_project").select("lisan").run()
        self.assertFalse(app.exception)
        self.assertEqual(len([b for b in app.button if (b.key or "").startswith("open:")]), 1)
        self.assertTrue(any("Placement portraits" in item.value for item in app.subheader))
        self.assertNotIn("Unassigned", app.selectbox(key="studio_project").options)

    def test_seed_controls_explicit_clear_and_shot_plan_without_file_writes(self):
        library = self.app_dir / "library"
        before = {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in library.iterdir()}
        app = self.app()
        self.assertEqual(app.session_state["studio_reviews"]["hon-00"]["status"], "needs_fixes")
        app.button(key="nav:Review queue").click().run()
        self.assertEqual({b.key for b in app.button if (b.key or "").startswith("open:")},
                         {"open:hon-00", "open:hon-01", "open:hon-02"})  # Includes the plan-only reference.
        app.button(key="open:hon-00").click().run()
        app.button(key="review:hon-00:keep").click().run()
        self.assertEqual(app.session_state["studio_reviews"]["hon-00"]["status"], "keep")
        app.button(key="review:hon-00:None").click().run()
        self.assertIsNone(app.session_state["studio_reviews"]["hon-00"]["status"])
        self.assertEqual(app.text_area(key="asset-note:hon-00").value, "Keep this outfit only.")
        app.multiselect(key="plan-destinations:hon-00").set_value(["Flow", "Grok"])
        app.text_area(key="plan-idea:hon-00").input("Board the ship at night")
        app.text_area(key="plan-prompt:hon-00").input("Keep this coat; fix tattoos using LOCK-FACE")
        next(b for b in app.button if b.label == "Save shot plan").click().run()
        self.assertFalse(app.exception)
        plan = app.session_state["studio_reviews"]["hon-00"]["shotPlan"]
        self.assertEqual(plan["destinations"], ["Flow", "Grok"])
        self.assertEqual(plan["status"], "planned")
        app.button(key="nav:Shot plans").click().run()
        self.assertEqual(len([b for b in app.button if (b.key or "").startswith("open:")]), 2)
        next(s for s in app.selectbox if s.label == "Handoff destination").select("Flow").run()
        self.assertEqual(len([b for b in app.button if (b.key or "").startswith("open:")]), 1)
        app.button(key="open:hon-00").click().run()
        app.button(key="remove-plan:hon-00").click().run()
        self.assertFalse(app.exception)
        self.assertIsNone(app.session_state["studio_reviews"]["hon-00"]["shotPlan"])
        self.assertIsNone(app.session_state["studio_reviews"]["hon-00"]["status"])
        self.assertEqual(before, {p.name: hashlib.sha256(p.read_bytes()).hexdigest() for p in library.iterdir()})

    def test_mission_control_is_default_global_and_opens_packaged_references(self):
        app = self.app(library=False)
        self.assertEqual(app.session_state["studio_view"], "Ziggy’s Corner")
        self.assertTrue(any("Mission Control" in item.value for item in app.markdown))
        self.assertTrue(any("Correct the coat reference" in item.label for item in app.expander))
        self.assertTrue(any("Prepare Lisan motion" in item.label for item in app.expander))
        self.assertTrue(all(not item.proto.expanded for item in app.expander))
        self.assertEqual([metric.value for metric in app.metric], ["1", "1", "0"])
        self.assertEqual(app.button(key="mission-shot-plans").label, "Shot plans · 1 →")
        app.selectbox(key="studio_project").select("lisan").run()
        self.assertTrue(any("Correct the coat reference" in item.label for item in app.expander))
        app.button(key="mission-asset:fix-look:0").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state["studio_project"], "hon")
        self.assertEqual(app.session_state["studio_mission_selected"], "hon-00")
        app.button(key="corner-selected-back").click().run()
        app.selectbox(key="mission-provider").select("Flow").run()
        self.assertFalse(app.exception)
        self.assertFalse(any("Correct the coat reference" in item.label for item in app.expander))
        self.assertTrue(any("Prepare Lisan motion" in item.label for item in app.expander))

    def test_corner_review_strip_has_only_real_unanswered_requests(self):
        path = self.app_dir / "library" / "catalog.json"
        original = path.read_bytes()
        data = json.loads(original)
        data["reviewRequests"] = [
            {"id": "hon-03", "sha256": "hash-3", "type": "missing_decision"},
            {"id": "hon-00", "sha256": "hash-0", "type": "missing_decision"},
            {"id": "hon-01", "sha256": "hash-1", "type": "missing_decision"},
            {"id": "hon-04", "sha256": "stale", "type": "missing_decision"},
            {"id": "hon-05", "sha256": "hash-5", "type": "missing_decision"}]
        next(a for a in data["assets"] if a["id"] == "hon-05")["archived"] = True
        path.write_text(json.dumps(data), encoding="utf-8")
        try:
            app = self.app(library=False)
            self.assertFalse(any(item.value == "Current work" for item in app.subheader))
            self.assertEqual(sum("Correct the coat reference" in e.label for e in app.expander), 1)
            self.assertFalse(any(b.key in {"mission-shots", "mission-library"} for b in app.button))
            self.assertEqual(app.button(key="mission-review").label, "Review images · 1")
            self.assertFalse(next(e for e in app.expander if e.label == "Prepare review sweep").proto.expanded)
            app.button(key="mission-review").click().run()
            self.assertEqual({b.key for b in app.button if (b.key or "").startswith("corner-collection:")},
                             {"corner-collection:hon-03"})
            app.button(key="corner-collection:hon-03").click().run()
            app.button(key="review:hon-03:keep").click().run()
            next(b for b in app.button if b.label == "← Back to the collection").click().run()
            self.assertFalse(app.exception)
            self.assertFalse(any((b.key or "").startswith("corner-collection:") for b in app.button))
            app.button(key="corner-collection-back").click().run()
            self.assertFalse(any(b.key == "mission-review" for b in app.button))
            self.assertTrue(any("No image reviews waiting" in c.value for c in app.caption))
            app.selectbox(key="studio_project").select("lisan").run()
            self.assertFalse(any(b.key == "mission-review" for b in app.button))
        finally:
            path.write_bytes(original)

    def test_corner_shot_plan_counter_opens_all_visible_plans_and_preserves_return(self):
        path = self.app_dir / "library" / "mission_control.json"
        base = json.loads((path.parent / "catalog.json").read_text(encoding="utf-8"))
        extra = {**base["assets"][0], "id": "lisan-plan", "project": "lisan", "sha256": "lisan-exact", "title": "Lisan planned image"}
        archived = {**extra, "id": "archived-plan", "archived": True}
        plan = {"status": "requested_bounded_test", "destinations": ["ComfyUI", "Grok"],
                "idea": "One controlled motion test", "prompt": "Preserve the approved source."}
        snapshot = {"projects": base["projects"], "categories": [], "albums": [],
                    "assets": [extra, archived, base["assets"][1]],
                    "reviewDecisions": [{"id": extra["id"], "sha256": extra["sha256"], "shotPlan": plan},
                                        {"id": archived["id"], "sha256": archived["sha256"], "shotPlan": plan},
                                        {"id": "hon-01", "sha256": "hash-1", "status": "remove", "shotPlan": plan}],
                    "missionControl": {"tasks": []}}
        path.write_text(json.dumps(snapshot), encoding="utf-8")
        try:
            app = self.app()
            app.button(key="nav:Ziggy’s Corner").click().run()
            before = copy.deepcopy(app.session_state["studio_reviews"])
            self.assertEqual(app.button(key="mission-shot-plans").label, "Shot plans · 2 →")
            app.button(key="mission-shot-plans").click().run()
            self.assertFalse(app.exception)
            self.assertTrue(any(h.value == "All shot plans" for h in app.subheader))
            self.assertEqual({b.key for b in app.button if (b.key or "").startswith("corner-collection:")},
                             {"corner-collection:hon-02", "corner-collection:lisan-plan"})
            self.assertTrue(any("ComfyUI" in c.value and "Grok" in c.value for c in app.caption))
            self.assertTrue(any(m.value == plan["idea"] for m in app.markdown))
            self.assertTrue(any(t.value == plan["prompt"] for t in app.text))
            app.button(key="corner-collection:lisan-plan").click().run()
            self.assertEqual(app.session_state["studio_project"], "lisan")
            next(b for b in app.button if b.label == "← Back to the collection").click().run()
            self.assertEqual({b.key for b in app.button if (b.key or "").startswith("corner-collection:")},
                             {"corner-collection:hon-02", "corner-collection:lisan-plan"})
            self.assertEqual(app.session_state["studio_reviews"], before)
            app.button(key="corner-collection-back").click().run()
            app.button(key="mission-back").click().run()
            self.assertEqual(app.session_state["studio_view"], "Library")
            self.assertFalse(app.exception)
        finally:
            path.unlink(missing_ok=True)


    def test_export_basket_is_global_and_independent_of_favorites_and_review(self):
        app = self.app()
        app.button(key="favorite:card:hon-00").click().run()
        app.button(key="basket:card:hon-00").click().run()
        app.selectbox(key="studio_project").select("lisan").run()
        app.button(key="basket:card:lisan-neck").click().run()
        app.button(key="nav:Export basket").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(len([b for b in app.button if (b.key or "").startswith("open:")]), 2)
        app.button(key="open:hon-00").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state["studio_project"], "hon")
        next(b for b in app.button if b.label == "← Back to the collection").click().run()
        next(b for b in app.button if b.label == "Prepare ZIP of review copies").click().run()
        self.assertFalse(app.exception)
        self.assertTrue(app.session_state["studio_basket_zip"])
        next(b for b in app.button if b.label == "Clear export basket").click().run()
        self.assertEqual(app.session_state["studio_basket"], set())
        self.assertEqual(app.session_state["studio_favorites"], {"hon-00"})
        self.assertEqual(app.session_state["studio_reviews"]["hon-00"]["status"], "needs_fixes")
        self.assertEqual(app.session_state["studio_notes"]["hon-00"], "Keep this outfit only.")

    def test_quick_collaborator_assignment_preserves_plan_and_review_scope(self):
        app = self.app()
        app.button(key="open:hon-02").click().run()
        app.button(key="collaborator:hon-02:Flow").click().run()
        self.assertFalse(app.exception)
        plan = app.session_state["studio_reviews"]["hon-02"]["shotPlan"]
        self.assertEqual(plan["destinations"], ["Flow"])
        self.assertEqual(plan["idea"], "A winter shot")
        self.assertEqual(plan["status"], "planned")
        self.assertEqual(app.multiselect(key="plan-destinations:hon-02").value, ["Flow"])
        self.assertTrue(any("Queued for Flow" in caption.value and "not sent" in caption.value for caption in app.caption))
        app.button(key="collaborator:hon-02:Grok").click().run()
        self.assertEqual(app.session_state["studio_reviews"]["hon-02"]["shotPlan"]["destinations"], ["Flow", "Grok"])
        app.button(key="collaborator:hon-02:Flow").click().run()
        app.button(key="collaborator:hon-02:Grok").click().run()
        self.assertEqual(app.session_state["studio_reviews"]["hon-02"]["shotPlan"]["destinations"], ["undecided"])
        self.assertEqual(app.session_state["studio_reviews"]["hon-02"]["shotPlan"]["idea"], "A winter shot")
        self.assertIsNone(app.session_state["studio_reviews"]["hon-02"]["status"])
        self.assertEqual(app.session_state["studio_favorites"], set())
        self.assertEqual(app.session_state["studio_basket"], set())

    def test_collaborators_defaults_to_actual_comfy_workflow_with_references(self):
        app = self.app()
        app.button(key="nav:Collaborators").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.selectbox(key="workspace-provider").value, "ComfyUI")
        self.assertTrue(any("Clip soundtrack replacement" in heading.value for heading in app.subheader))
        self.assertTrue(any("Cloud saved and validated, not run" in text.value for text in app.markdown))
        self.assertEqual(len(app.code), 1)
        app.button(key="workflow-open:audio-replace:output:hon-01").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state["studio_selected"], "hon-01")
        app.button(key="nav:Collaborators").click().run()
        app.selectbox(key="workspace-provider").select("Flow").run()
        self.assertFalse(app.exception)
        self.assertTrue(any("Prepare Lisan motion" in heading.value for heading in app.subheader))
        self.assertTrue(any("Flow" == heading.value for heading in app.subheader))

    def test_detail_explorer_story_filter_nested_docs_and_back_button(self):
        app = self.app()
        app.selectbox(key="category:hon").select("details").run()
        self.assertFalse(app.exception)
        self.assertEqual(app.selectbox(key="detail-profile:hon").value, "hon-profile")
        self.assertTrue(any(button.key == "open:hon-00" for button in app.button))
        app.radio(key="detail-evidence:hon-profile:neck").set_value("Stencils").run()
        self.assertTrue(any(button.key == "open:hon-01" for button in app.button))
        app.button(key="nav:Storyboard").click().run()
        app.selectbox(key="story-stage:hon").select("detailed_design").run()
        self.assertFalse(any(button.key == "open:SB-01" for button in app.button))
        app.selectbox(key="story-stage:hon").select("all").run()
        self.assertEqual(app.multiselect(key="story-themes:hon").options, ["love", "rescue"])
        app.multiselect(key="story-themes:hon").set_value(["love"]).run()
        app.slider(key="story-position:hon").set_value((0, 50)).run()
        self.assertFalse(app.exception)
        self.assertEqual(app.multiselect(key="story-themes:hon").options, [])
        self.assertEqual(app.multiselect(key="story-themes:hon").value, [])
        app.button(key="nav:Documents").click().run()
        self.assertFalse(app.exception)
        self.assertTrue(any(expander.label.startswith("Collaborator briefs (") for expander in app.expander))
        app.button(key="nav:Ziggy’s Corner").click().run()
        app.button(key="mission-back").click().run()
        self.assertEqual(app.session_state["studio_view"], "Documents")

    def test_working_reference_request_and_multiverse_guard(self):
        app = self.app()
        app.button(key="open:hon-00").click().run()
        app.selectbox(key="asset-stage:hon-00").select("detailed_design").run()
        self.assertEqual(app.session_state["studio_reviews"]["hon-00"]["storyboardStage"], "detailed_design")
        self.assertNotIn("workingReference", app.session_state["studio_reviews"]["hon-00"])
        app.selectbox(key="working-scope:hon-00").select("outfit").run()
        app.button(key="request-working:hon-00").click().run()
        self.assertEqual(app.session_state["studio_reviews"]["hon-00"]["workingReference"], {"status": "requested", "scope": "outfit"})
        app.button(key="variant:hon-00:multiverse").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state["studio_reviews"]["hon-00"]["variant"], "multiverse")
        self.assertIsNone(app.session_state["studio_reviews"]["hon-00"]["workingReference"])
        self.assertTrue(app.button(key="request-working:hon-00").disabled)
        app.button(key="nav:Ziggy’s Corner").click().run()
        self.assertFalse(app.exception)
        self.assertTrue(any(expander.label == "Prepare review sweep" for expander in app.expander))


if __name__ == "__main__":
    unittest.main()
