"""Output intent roundtrips and completed task visibility in the native studio."""
import copy
from pathlib import Path
import sys
import unittest

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP))
from library_helpers import (effective_reviews, handoff_payload, handoff_text, mission_tasks,
                             normalize_plan, output_kind_label, read_review, review_payload, review_provenance)


class OutputKindTest(unittest.TestCase):
    def test_page_footer_dates_are_readable_and_date_only_values_do_not_shift(self):
        from mission_view import format_page_updated
        self.assertEqual(format_page_updated("2026-10-30"), "10.30.2026")
        self.assertIn(format_page_updated("2026-10-30T12:05:06.123Z"),
                      {"10.30.2026 · 8:05 AM EDT", "10.30.2026 · 12:05 PM UTC"})
        self.assertIn(format_page_updated("2026-12-30T12:05:06Z"),
                      {"12.30.2026 · 7:05 AM EST", "12.30.2026 · 12:05 PM UTC"})
        self.assertEqual(format_page_updated("not a timestamp"), "Time unavailable")

    def test_provider_filters_merge_instances_and_keep_team_membership(self):
        from mission_view import provider_families, provider_matches
        self.assertEqual(provider_families("Grok / Chief of Staff"), ("Grok",))
        self.assertEqual(provider_families("Claude (lead writer)"), ("Claude",))
        for member in ("CFA", "Grok", "Gemini", "Teamwork"):
            self.assertTrue(provider_matches("CFA / Grok / Gemini", member))
        self.assertFalse(provider_matches("Grok / Chief of Staff", "Teamwork"))
        self.assertFalse(provider_matches("CFA", "CFA Nova"))
        self.assertFalse(provider_matches("Unknown / Helper", "Teamwork"))
        self.assertEqual(provider_families("Unknown / Helper"), ("Unknown / Helper",))

    def test_explicit_output_survives_review_and_handoff_without_inference(self):
        asset = {"id": "reference", "sha256": "a" * 64, "kind": "image", "project": "hon"}
        for kind in ("image", "video", "unspecified"):
            with self.subTest(kind=kind):
                seed = {"id": asset["id"], "sha256": asset["sha256"], "status": "keep",
                        "note": "Preserve this review", "updatedAt": "2026-10-30T12:00:00Z",
                        "shotPlan": {"destinations": ["Grok"], "outputKind": kind, "idea": "A draft"}}
                before = copy.deepcopy(seed)
                reviews = effective_reviews([asset], [seed], {})
                provenance = review_provenance({"reviewDecisions": [seed]})
                exported = review_payload([asset], reviews, set(), provenance=provenance)
                restored, _, skipped = read_review(exported, [asset])
                self.assertEqual(skipped, 0)
                self.assertEqual(restored[asset["id"]]["shotPlan"]["outputKind"], kind)
                self.assertEqual(restored[asset["id"]]["note"], seed["note"])
                handoff = handoff_payload([asset], restored, "hon", "all")
                self.assertEqual(handoff["items"][0]["shotPlan"]["outputKind"], kind)
                self.assertIn("Output kind: " + output_kind_label(kind), handoff_text(handoff))
                self.assertEqual(seed, before)
        self.assertNotIn("outputKind", normalize_plan({"destinations": ["grok_video"]}))
        for bad in (None, "animation", [], True):
            with self.assertRaises(ValueError):
                normalize_plan({"outputKind": bad})

    def test_task_metadata_is_explicit_and_legacy_tasks_remain_internal(self):
        task = {"id": "task", "project": "hon", "provider": "Writer", "title": "Draft",
                "status": "ready", "summary": "Prepared", "nextAction": "Review"}
        for direction in ("inbound", "outbound", "internal"):
            for kind in ("image_new", "image_repair", "video", "planning"):
                parsed = mission_tasks({"tasks": [{**task, "direction": direction, "workKind": kind}]})[0]
                self.assertEqual((parsed["direction"], parsed["workKind"]), (direction, kind))
        parsed = mission_tasks({"tasks": [task]})[0]
        self.assertEqual((parsed["direction"], parsed["workKind"]), ("internal", "planning"))


class TaskGroupsAppTest(unittest.TestCase):
    def test_corner_groups_active_work_and_archive_keeps_completed_records(self):
        from streamlit.testing.v1 import AppTest
        base = {"project": "hon", "provider": "Writer", "status": "ready", "summary": "Prepared",
                "nextAction": "Review", "links": [], "workKind": "planning"}
        tasks = [{**base, "id": direction, "title": direction + " active", "direction": direction}
                 for direction in ("inbound", "outbound", "internal")]
        tasks.extend({**base, "id": kind, "title": kind + " active", "direction": "outbound", "workKind": kind}
                     for kind in ("image_new", "image_repair", "video"))
        tasks.extend({**base, "id": "provider-"+str(index), "title": name + " active", "direction": "inbound", "provider": name}
                     for index, name in enumerate(("Grok", "Grok / Chief of Staff", "Grok / Gemini")))
        tasks.append({**base, "id": "completed", "title": "Completed handoff", "direction": "outbound",
                      "status": "done", "links": [{"label": "Completed record", "href": "https://example.com/record"}]})
        source = f'''
import sys
from pathlib import Path
sys.path.insert(0, {str(APP)!r})
import streamlit as st
from mission_view import render_corner
st.session_state.studio_reviews = {{}}
st.session_state.studio_project = "hon"
archived = st.toggle("Archive", key="archive-tasks")
data = {{"assets": [], "projects": [{{"id": "hon", "name": "Hon"}}], "missionControl": {{"tasks": {tasks!r}}}}}
render_corner(data, Path({str(APP)!r}), lambda a: None, lambda a: None,
              lambda a, **kw: None, lambda v: None, lambda: None, archived=archived)
'''
        app = AppTest.from_string(source).run()
        self.assertFalse(app.exception)
        self.assertTrue({"Incoming", "Outgoing", "Internal"}.issubset({h.value for h in app.subheader}))
        self.assertTrue(any(e.label == "Writing & planning · 1" for e in app.expander))
        image_group = next(e for e in app.expander if e.label == "Image generation · 2")
        video_group = next(e for e in app.expander if e.label == "Video generation · 1")
        self.assertTrue(any("image_new active" in e.label for e in image_group.expander))
        self.assertTrue(any("image_repair active" in e.label for e in image_group.expander))
        self.assertFalse(any("video active" in e.label for e in image_group.expander))
        self.assertTrue(any("video active" in e.label for e in video_group.expander))
        self.assertFalse(any("Completed handoff" in e.label for e in app.expander))
        self.assertEqual(app.selectbox(key="mission-provider").options.count("Grok"), 1)
        self.assertNotIn("Grok / Chief of Staff", app.selectbox(key="mission-provider").options)
        app.selectbox(key="mission-provider").select("Grok").run()
        self.assertTrue(any("Grok / Chief of Staff active" in e.label for e in app.expander))
        self.assertTrue(any("Grok / Gemini active" in e.label for e in app.expander))
        app.selectbox(key="mission-provider").select("Teamwork").run()
        self.assertTrue(any("Grok / Gemini active" in e.label for e in app.expander))
        self.assertFalse(any("Grok / Chief of Staff active" in e.label for e in app.expander))
        app.selectbox(key="mission-provider").select("all").run()
        app.toggle(key="archive-tasks").set_value(True).run()
        self.assertFalse(app.exception)
        self.assertTrue(any("Completed handoff" in e.label for e in app.expander))
        self.assertFalse(any(" active" in e.label for e in app.expander))
        self.assertTrue(any("Completed record" in str(e.proto) for e in app.get("link_button")))
        legacy_source = source.replace('archived = st.toggle',
            'if "mission-provider" not in st.session_state:\n    st.session_state["mission-provider"] = "Grok / Chief of Staff"\narchived = st.toggle')
        legacy = AppTest.from_string(legacy_source).run()
        self.assertFalse(legacy.exception)
        self.assertEqual(legacy.selectbox(key="mission-provider").value, "Grok")


if __name__ == "__main__":
    unittest.main()
