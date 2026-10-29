"""Mobile triage, reusable notes, and portable review backups without source writes."""
import ast
from copy import deepcopy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest
from uuid import uuid4

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP))
sys.path.insert(0, str(Path(__file__).parent))
from library_helpers import EXPORT_FORMAT, read_basket, read_review, review_payload
import test_studio


class State(dict):
    def __getattr__(self, key):
        return self[key]

    def __setattr__(self, key, value):
        self[key] = value


def callbacks(state):
    names = {"read_note_presets", "merge_note_presets", "complete_review_payload", "choose_note_preset",
             "save_note", "set_review_field", "delete_note_preset", "clear_note_presets",
             "undo_clear_note_presets", "load_note_preset_editor", "save_note_preset", "seed_review_selections"}
    tree = ast.parse((APP / "app.py").read_text(encoding="utf-8"))
    definitions = ast.Module(body=[node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name in names], type_ignores=[])
    namespace = {"st": SimpleNamespace(session_state=state), "NOTE_LIMIT": 20000,
                 "NOTE_PRESETS_FORMAT": "cfa-review-note-presets-v1", "review_payload": review_payload,
                 "REVIEW_EDITABLE_FIELDS": ("status", "note", "shotPlan", "likenessRating", "sceneQualityRating"),
                 "read_review": read_review, "read_basket": read_basket, "EXPORT_FORMAT": EXPORT_FORMAT,
                 "datetime": datetime, "timezone": timezone, "uuid4": uuid4}
    exec(compile(definitions, str(APP / "app.py"), "exec"), namespace)
    return namespace


class NotePresetBackupTest(unittest.TestCase):
    def setUp(self):
        self.state = State(studio_note_presets=[{"id": "nose", "label": "Nose", "text": "Check both nose hoops."}],
                           studio_reviews={"image": {"status": "keep", "note": "Original note", "likenessRating": 5}},
                           studio_review_overrides={}, studio_notes={})
        self.fn = callbacks(self.state)

    def test_append_uses_live_text_and_keeps_other_fields_and_overflow_unchanged(self):
        self.state["asset-note:image"] = "Manually edited note"
        self.state["insert"] = "nose"
        original = deepcopy(self.state.studio_reviews)
        self.fn["choose_note_preset"]("image", "insert")
        self.assertEqual(self.state["asset-note:image"], "Manually edited note\nCheck both nose hoops.")
        self.assertEqual(self.state.studio_review_overrides["image"]["note"], self.state["asset-note:image"])
        self.assertEqual(self.state.studio_reviews, original)
        self.assertNotIn("status", self.state.studio_review_overrides["image"])
        self.assertEqual(self.state["insert"], "")
        self.state["asset-note:image"] = "x" * 20000
        self.state["insert"] = "nose"
        overrides = deepcopy(self.state.studio_review_overrides)
        self.fn["choose_note_preset"]("image", "insert")
        self.assertEqual(self.state["asset-note:image"], "x" * 20000)
        self.assertEqual(self.state.studio_review_overrides, overrides)
        self.assertIn("unchanged", self.state.studio_preset_error)

    def test_preset_edits_clear_undo_and_conflicts_do_not_rewrite_review_notes(self):
        original = deepcopy(self.state.studio_reviews)
        self.state.update({"preset-editor-id": "nose", "preset-editor-label": "Revised", "preset-editor-text": "Different text"})
        self.fn["save_note_preset"]()
        self.fn["clear_note_presets"]()
        self.assertEqual(self.state.studio_note_presets, [])
        self.fn["undo_clear_note_presets"]()
        self.assertEqual(self.state.studio_note_presets[0]["text"], "Different text")
        merged = self.fn["merge_note_presets"](self.state.studio_note_presets,
                                             [{"id": "nose", "label": "Other", "text": "Keep this other wording"}])
        self.assertEqual(len(merged), 2)
        self.assertEqual(len({row["id"] for row in merged}), 2)
        self.state["preset-editor-id"] = "nose"
        self.fn["delete_note_preset"]()
        self.assertEqual(self.state.studio_reviews, original)
        self.assertEqual(self.state.studio_review_overrides, {})

    def test_complete_backup_roundtrip_keeps_hashes_evidence_and_presets_separate(self):
        assets = [{"id": "image", "sha256": "original", "project": "hon", "filename": "one.jpg"}]
        assessment = {"id": "original-assessment", "assetID": "image", "sha256": "original", "presence": "unknown"}
        self.state.update(studio_export_assets=assets, studio_favorites={"image"}, studio_basket={"image"},
                          studio_review_provenance={"validationEvidence": {"format": "cfa-reference-validation-v1", "schemaVersion": 1,
                                                                         "assessments": [assessment], "legacyReviewArchive": []},
                                                    "sceneReviews": [{"id": "scene", "scope": "scene-only"}]})
        payload = json.loads(json.dumps(self.fn["complete_review_payload"]()))
        restored, favorites, skipped = read_review(payload, assets)
        self.assertEqual(skipped, 0)
        self.assertEqual(favorites, {"image"})
        self.assertEqual(restored["image"]["status"], "keep")
        self.assertEqual(restored["image"]["note"], "Original note")
        self.assertEqual(payload["items"][0]["sha256"], "original")
        self.assertEqual(payload["validationEvidence"]["assessments"], [assessment])
        self.assertEqual(payload["sceneReviews"], [{"id": "scene", "scope": "scene-only"}])
        self.assertEqual(self.fn["read_note_presets"](payload), self.state.studio_note_presets)
        self.assertNotIn("notePresets", payload["items"][0])
        bad = deepcopy(payload)
        bad["notePresets"]["items"].append(bad["notePresets"]["items"][0])
        with self.assertRaises(ValueError):
            self.fn["read_note_presets"](bad)
        self.assertEqual(self.state.studio_note_presets, [{"id": "nose", "label": "Nose", "text": "Check both nose hoops."}])

    def test_snapshot_selections_seed_once_and_edit_dates_do_not_retime_other_choices(self):
        asset = {"id": "image", "sha256": "original", "project": "hon"}
        data = {"assets": [asset], "reviewSessionSeed": {"id": "snapshot-one", "favorites": [asset], "exportBasket": [asset]}}
        self.state.update(studio_favorites=set(), studio_basket=set())
        self.fn["seed_review_selections"](data)
        self.assertEqual(self.state.studio_favorites, {"image"})
        self.assertEqual(self.state.studio_basket, {"image"})
        self.state.studio_favorites.clear()
        self.state.studio_basket.clear()
        self.fn["seed_review_selections"](data)
        self.assertEqual(self.state.studio_favorites, set())
        self.assertEqual(self.state.studio_basket, set())
        self.state.studio_reviews["image"]["updatedAt"] = "2026-10-20T10:00:00Z"
        self.fn["set_review_field"]("image", "note", "A new note")
        dates = self.state.studio_review_overrides["image"]["fieldUpdatedAt"]
        self.assertEqual(dates["status"], "2026-10-20T10:00:00Z")
        self.assertNotEqual(dates["note"], dates["status"])
        self.assertEqual(self.state.studio_review_overrides["image"]["origin"], "user")


class MobileReviewAppTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.previous_loader = sys.modules.pop("studio_dependencies", None)
        test_studio.StudioAppTest.setUpClass.__func__(cls)

    @classmethod
    def tearDownClass(cls):
        test_studio.StudioAppTest.tearDownClass.__func__(cls)
        sys.modules.pop("studio_dependencies", None)
        if cls.previous_loader is not None:
            sys.modules["studio_dependencies"] = cls.previous_loader

    def app(self):
        return test_studio.StudioAppTest.app(self)

    def test_review_controls_order_collapsed_scores_and_visible_export(self):
        app = self.app()
        self.assertNotIn("Unassigned", app.selectbox(key="studio_project").options)
        sidebar = [button.key for button in app.sidebar.button]
        self.assertEqual(sidebar[-3:], ["nav:Documents", "nav:Export basket", "nav:Favorites & notes"])
        app.button(key="open:hon-00").click().run()
        self.assertFalse(app.exception)
        keys = [button.key for button in app.button]
        self.assertLess(keys.index("basket:selected:hon-00"), keys.index("review:hon-00:keep"))
        self.assertLess(keys.index("review:hon-00:keep"), keys.index("collaborator:hon-00:Flow"))
        self.assertLess(keys.index("collaborator:hon-00:Flow"), keys.index("archive:hon-00"))
        scores = next(expander for expander in app.expander if expander.label == "Scores (optional)")
        self.assertFalse(scores.proto.expanded)
        downloads = app.get("download_button")
        self.assertGreaterEqual(sum(item.proto.label == "Export review" for item in downloads), 2)
        app.button(key="review:hon-00:keep").click().run()
        self.assertEqual(app.session_state["studio_reviews"]["hon-00"]["status"], "keep")
        self.assertEqual(app.session_state["studio_reviews"]["hon-00"]["note"], "Keep this outfit only.")

    def test_preset_apply_edit_delete_preserves_applied_note_and_sources(self):
        library = self.app_dir / "library"
        before = {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in library.iterdir()}
        app = self.app()
        app.button(key="open:hon-00").click().run()
        app.text_area(key="asset-note:hon-00").input("Manual note").run()
        app.text_input(key="preset-editor-label").input("Piercing check")
        app.text_area(key="preset-editor-text").input("Check both nose hoops.")
        app.button(key="preset-save").click().run()
        self.assertFalse(app.exception)
        preset_id = app.session_state["studio_note_presets"][0]["id"]
        app.selectbox(key="preset-insert:hon-00").select(preset_id).run()
        self.assertFalse(app.exception)
        self.assertEqual(app.text_area(key="asset-note:hon-00").value, "Manual note\nCheck both nose hoops.")
        app.text_area(key="preset-editor-text").input("Changed preset only")
        app.button(key="preset-save").click().run()
        app.button(key="preset-delete").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state["studio_note_presets"], [])
        self.assertEqual(app.session_state["studio_reviews"]["hon-00"]["note"], "Manual note\nCheck both nose hoops.")
        self.assertEqual(app.session_state["studio_reviews"]["hon-00"]["status"], "needs_fixes")
        self.assertEqual(before, {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in library.iterdir()})

    def test_selected_intake_sequence_does_not_shift_after_decision(self):
        app = self.app()
        app.session_state["studio_view"] = "Intake verification"
        app.session_state["studio_selected"] = "hon-00"
        app.session_state["studio_intake_sequence"] = ["hon-00", "hon-01", "hon-02"]
        app.run()
        self.assertFalse(app.exception)
        app.button(key="review:hon-00:keep").click().run()
        app.button(key="intake-selected-next").click().run()
        self.assertEqual(app.session_state["studio_selected"], "hon-01")
        app.button(key="review:hon-01:needs_fixes").click().run()
        app.button(key="intake-selected-prev").click().run()
        self.assertEqual(app.session_state["studio_selected"], "hon-00")
        self.assertEqual(app.session_state["studio_intake_sequence"], ["hon-00", "hon-01", "hon-02"])
        self.assertEqual(app.session_state["studio_reviews"]["hon-00"]["status"], "keep")
        self.assertEqual(app.session_state["studio_reviews"]["hon-01"]["status"], "needs_fixes")


if __name__ == "__main__":
    unittest.main()
