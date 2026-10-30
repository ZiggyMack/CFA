"""Two declared humans, one canonical task, and honest screenplay intake."""
import ast
from copy import deepcopy
from datetime import datetime, timezone
import json
from pathlib import Path
import sys
from types import SimpleNamespace
import unittest

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP))
from controller_routing import apply_route, controller_tasks, human_action, project_controller
from library_helpers import effective_reviews, mission_tasks, read_review, review_payload

DATA = {"projects": [{"id": "hon", "name": "Hon Dolo", "controllerID": "ziggy"},
    {"id": "lisan", "name": "Lisan Al Gaib", "controllerID": "ziggy"},
    {"id": "criminal_mind", "name": "Baldadoon", "subtitle": "The Criminal Mind", "controllerID": "baldadoon", "landing": {"title": "The Criminal Mind"}}],
    "humanControllers": [{"id": "ziggy", "name": "Ziggy", "homeLabel": "Ziggy’s Corner"},
                         {"id": "baldadoon", "name": "Baldadoon", "homeLabel": "Casa Baldadoon"}]}
ASSET = {"id": "test-source", "project": "criminal_mind", "sha256": "a" * 64, "kind": "document"}
TASK = {"id": "adaptation", "project": "criminal_mind", "title": "Decide adaptation scope", "summary": "Preliminary notes",
        "nextAction": "Read the original", "status": "needs_input", "provider": "CFA Nova", "links": [{"assetID": ASSET["id"], "label": "Source"}]}


class HumanRoutingTest(unittest.TestCase):
    def test_owner_assignment_authority_and_one_canonical_task(self):
        original = deepcopy(TASK)
        parsed = mission_tasks({"tasks": [TASK]})
        aliases = mission_tasks({"tasks": [{**TASK, "direction": "incoming", "workCategory": "writing_planning"}]})
        self.assertEqual((aliases[0]["direction"], aliases[0]["workKind"]), ("inbound", "planning"))
        casa, delegated = controller_tasks(DATA, parsed, "baldadoon")
        self.assertEqual([t["id"] for t in casa], [TASK["id"]])
        self.assertFalse(delegated)
        self.assertEqual(controller_tasks(DATA, parsed, "ziggy"), ([], []))
        help_task = {**TASK, "assigneeControllerID": "ziggy", "decisionScope": "technical_assistance"}
        casa, delegated = controller_tasks(DATA, [help_task], "baldadoon")
        ziggy, _ = controller_tasks(DATA, [help_task], "ziggy")
        self.assertFalse(casa)
        self.assertEqual([t["id"] for t in delegated], [t["id"] for t in ziggy])
        self.assertEqual(ziggy[0]["decisionAuthorityControllerID"], "baldadoon")
        done = {**help_task, "status": "done"}
        self.assertEqual(controller_tasks(DATA, [done], "ziggy")[0][0]["ownerControllerID"], "baldadoon")
        self.assertEqual(TASK, original)
        for project in ("hon", "lisan"):
            self.assertEqual(project_controller(DATA, project), "ziggy")

    def test_actor_scope_and_exact_task_reference_are_required(self):
        stamp = "2026-10-30T18:00:00Z"
        for actor, scope in ((None, "reference"), ("baldadoon", None), ("ziggy", "reference")):
            with self.assertRaises(ValueError):
                human_action(DATA, ASSET, actor, scope, ["status"], stamp)
        help_task = {**TASK, "assigneeControllerID": "ziggy", "decisionScope": "technical_assistance"}
        note = human_action(DATA, ASSET, "ziggy", "technical_assistance", ["note"], stamp, help_task)
        self.assertEqual(note["humanReview"]["taskID"], TASK["id"])
        with self.assertRaises(ValueError):
            human_action(DATA, ASSET, "ziggy", "technical_assistance", ["status"], stamp, help_task)
        with self.assertRaises(ValueError):
            human_action(DATA, {**ASSET, "id": "unlinked"}, "ziggy", "technical_assistance", ["note"], stamp, help_task)
        delegated = {**help_task, "decisionAuthorityControllerID": "ziggy", "decisionScope": "reference"}
        self.assertEqual(human_action(DATA, ASSET, "ziggy", "reference", ["status"], stamp, delegated)["reviewer"], "Ziggy")
        with self.assertRaises(ValueError):
            human_action(DATA, ASSET, "ziggy", "scene", ["status"], stamp, delegated)

    def test_roundtrip_preserves_actor_scope_and_old_records(self):
        old = {"id": "hon-old", "sha256": "b" * 64, "project": "hon", "kind": "image"}
        historical = {"id": old["id"], "sha256": old["sha256"], "note": "Original human review", "status": "keep"}
        original = deepcopy(historical)
        attribution = human_action(DATA, ASSET, "baldadoon", "story", ["note"], "2026-10-30T18:00:00Z")
        attribution["humanReview"]["futureMetadata"] = {"keep": True}
        records = effective_reviews([ASSET, old], [historical], {ASSET["id"]: {"note": "Synthetic fixture", **attribution}})
        payload = review_payload([ASSET, old], records, set())
        read, _, skipped = read_review(payload, [ASSET, old])
        self.assertEqual(skipped, 0)
        self.assertEqual(read[ASSET["id"]]["humanReview"], attribution["humanReview"])
        self.assertEqual(read[ASSET["id"]]["reviewer"], "Baldadoon")
        self.assertNotIn("humanReview", read[old["id"]])
        self.assertEqual(historical, original)

    def test_deep_links_refresh_and_controller_switch_clear_context(self):
        state = {"studio_mission_questionnaire": "grok-proof-package", "studio_human_task_context": "old"}
        apply_route(state, {"project": "criminal_mind", "view": "project_home"}, DATA)
        self.assertEqual((state["studio_project"], state["studio_view"]), ("criminal_mind", "Project home"))
        self.assertNotIn("studio_human_task_context", state)
        apply_route(state, {"project": "criminal_mind", "view": "casa_baldadoon"}, DATA)
        self.assertEqual(state["studio_view"], "Casa Baldadoon")
        state["studio_view"] = "Documents"
        apply_route(state, {"project": "criminal_mind", "view": "casa_baldadoon"}, DATA)
        self.assertEqual(state["studio_view"], "Documents")
        apply_route(state, {"project": "hon", "view": "mission_control"}, DATA)
        self.assertEqual(state["studio_view"], "Ziggy’s Corner")

    def test_ui_callback_refuses_unattributed_action_before_mutating(self):
        class State(dict):
            __getattr__ = dict.__getitem__
            __setattr__ = dict.__setitem__
        state = State(studio_controller_data=DATA, studio_export_assets=[ASSET], studio_review_overrides={}, studio_reviews={})
        tree = ast.parse((APP / "app.py").read_text(encoding="utf8"))
        nodes = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "set_review_field"]
        scope = {"st": SimpleNamespace(session_state=state), "datetime": datetime, "timezone": timezone, "REVIEW_EDITABLE_FIELDS": ("status", "note")}
        from studio_dependencies import current_module
        scope["current_module"] = current_module
        exec(compile(ast.Module(body=nodes, type_ignores=[]), str(APP / "app.py"), "exec"), scope)
        scope["set_review_field"](ASSET["id"], "status", "keep")
        self.assertFalse(state.studio_review_overrides)
        state["human-actor:baldadoon"] = "baldadoon"
        state["human-scope:" + ASSET["id"]] = "reference"
        scope["set_review_field"](ASSET["id"], "status", "keep")
        self.assertEqual(state.studio_review_overrides[ASSET["id"]]["reviewer"], "Baldadoon")
        state.studio_reviews[ASSET["id"]] = deepcopy(state.studio_review_overrides[ASSET["id"]])
        state["human-scope:" + ASSET["id"]] = "story"
        scope["set_review_field"](ASSET["id"], "note", "A later scoped note")
        saved = state.studio_review_provenance["validationEvidence"]["legacyReviewArchive"]
        self.assertEqual(saved[0]["decisionScope"], "reference")
        scope["set_review_field"](ASSET["id"], "note", "Typing another word")
        self.assertEqual(len(state.studio_review_provenance["validationEvidence"]["legacyReviewArchive"]), 1)


class ControllerAppTest(unittest.TestCase):
    def test_casa_actionable_delegated_and_corner_are_distinct(self):
        from streamlit.testing.v1 import AppTest
        data = {**DATA, "assets": [], "missionControl": {"tasks": [TASK,
            {**TASK, "id": "help", "title": "Ziggy technical help", "assigneeControllerID": "ziggy", "decisionScope": "technical_assistance"},
            {**TASK, "id": "hon", "project": "hon", "title": "Hon only"}]}}
        source = f'''import sys
from pathlib import Path
sys.path.insert(0, {str(APP)!r})
import streamlit as st
from mission_view import render_corner
st.session_state.studio_reviews = {{}}
st.session_state.studio_project = "criminal_mind"
controller = st.radio("Controller", ["baldadoon", "ziggy"])
render_corner({data!r}, Path({str(APP)!r}), lambda a: None, lambda a: None,
lambda a, **kw: None, lambda v: None, lambda: None, controller=controller)
'''
        app = AppTest.from_string(source.encode("ascii", "backslashreplace").decode()).run()
        self.assertFalse(app.exception)
        self.assertTrue(any(TASK["title"] in e.label for e in app.expander))
        self.assertTrue(any(e.label == "Delegated work · 1" for e in app.expander))
        self.assertFalse(any("Hon only" in e.label for e in app.expander))
        app.radio[0].set_value("ziggy").run()
        self.assertFalse(app.exception)
        self.assertFalse(any(TASK["title"] in e.label for e in app.expander))
        self.assertTrue(any("Ziggy technical help" in e.label for e in app.expander))

    def test_source_blocks_remain_text_not_shots(self):
        from streamlit.testing.v1 import AppTest
        data = deepcopy(DATA)
        project = data["projects"][2]
        project["landing"].update(author="Baldadoon", sourceBlocks=[{"id": str(i), "heading": "Source heading", "text": "Script excerpt", "lineStart": i, "lineEnd": i+1} for i in range(41)])
        source = f'''import sys
sys.path.insert(0, {str(APP)!r})
from project_intake_view import render_project_home
render_project_home({data!r}, {project!r}, lambda a, **kw: None, lambda v: None)
'''
        app = AppTest.from_string(source.encode("ascii", "backslashreplace").decode()).run()
        self.assertFalse(app.exception)
        self.assertEqual(len([e for e in app.expander if "Source heading" in e.label]), 41)
        self.assertTrue(any("not finished scenes or storyboard shots" in c.value for c in app.caption))
        self.assertTrue(any("No character designs" in i.value for i in app.info))


if __name__ == "__main__":
    unittest.main()
