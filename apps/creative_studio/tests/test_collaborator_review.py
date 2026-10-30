"""Bounded Grok reply: exact scope, draft/ready separation and recoverable history."""
import copy
import io
import json
from pathlib import Path
import sys
import unittest
from types import SimpleNamespace
from unittest.mock import patch
import zipfile

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP))
import collaborator_review as pilot
from library_helpers import review_payload, review_provenance


def assets():
    return [{"id": q["assetID"], "kind": "image", "project": "hon", "sha256": q["sha256"]} for q in pilot.QUESTIONS]


def complete():
    record = pilot.empty("2026-10-30T13:00:00Z")
    for i, question in enumerate(pilot.QUESTIONS):
        record = pilot.edit(record, question_id=question["id"], choice="needs_correction", note="Keep the composition; fix this specific detail.",
                            now=f"2026-10-30T13:01:{i:02d}Z")
    return pilot.edit(record, direction={"choice": "bounded_corrections", "note": "One correction per recorded defect; no motion."}, now="2026-10-30T13:02:00Z")


class CollaboratorReviewTest(unittest.TestCase):
    def test_scope_is_seven_exact_original_outputs_and_answers_do_not_change_reviews(self):
        data = json.loads((APP / "library/design_catalog.json").read_text(encoding="utf-8"))
        self.assertEqual(len(pilot.QUESTIONS), 7)
        self.assertEqual(len({q["assetID"] for q in pilot.QUESTIONS}), 7)
        self.assertTrue(all(pilot.available(q, data["assets"]) for q in pilot.QUESTIONS))
        by_id = {a["id"]: a for a in data["assets"]}
        self.assertTrue(all(by_id[e["assetID"]]["sha256"] == e["sha256"] for e in pilot.EVIDENCE))
        self.assertIn("PROP-HD-HIP", [q["id"] for q in pilot.QUESTIONS])
        self.assertIn("CALEB-K_REF", [q["id"] for q in pilot.QUESTIONS])
        reviews = copy.deepcopy(data["reviewDecisions"])
        record = complete()
        provenance = review_provenance({"collaboratorReviews": {pilot.TASK_ID: record}, "reviewDecisions": reviews})
        exported = review_payload(assets(), {}, set(), provenance=provenance)
        self.assertEqual(exported["items"], [])
        self.assertEqual(data["reviewDecisions"], reviews)
        self.assertEqual(exported["collaboratorReviews"][pilot.TASK_ID], record)

    def test_required_answers_and_current_hashes_do_not_silently_pass(self):
        record = pilot.empty()
        with self.assertRaises(ValueError):
            pilot.prepare(record, assets())
        question = pilot.QUESTIONS[0]
        record = pilot.edit(record, question_id=question["id"], choice="needs_correction", note="")
        self.assertEqual(pilot.progress(record, assets())["answered"], 0)
        complete_record = complete()
        missing = assets()[1:]
        self.assertEqual(pilot.progress(complete_record, missing)["answered"], 6)
        with self.assertRaises(ValueError):
            pilot.prepare(complete_record, missing)
        uncertain = pilot.edit(complete_record, question_id=question["id"], choice="cannot_assess", note="Exact image absent from this snapshot.")
        self.assertTrue(pilot.prepare(uncertain, missing)["state"] == "ready")
        wrong = copy.deepcopy(complete_record)
        wrong["answers"][question["id"]]["reference"]["sha256"] = "a" * 64
        self.assertEqual(pilot.progress(wrong, assets())["answered"], 6)

    def test_prepare_edit_reprepare_keeps_prior_snapshot_and_roundtrips(self):
        draft = complete()
        original = copy.deepcopy(draft)
        ready = pilot.prepare(draft, assets(), now="2026-10-30T13:03:00Z", reply_id="first")
        self.assertEqual(draft, original)
        self.assertTrue(pilot.progress(ready, assets())["ready"])
        frozen = copy.deepcopy(ready["replies"][0])
        edited = pilot.edit(ready, question_id=pilot.QUESTIONS[0]["id"], choice="reject", note="Wrong scene entirely.", now="2026-10-30T13:04:00Z")
        self.assertFalse(pilot.progress(edited, assets())["ready"])
        self.assertIsNone(edited["readyReplyID"])
        second = pilot.prepare(edited, assets(), now="2026-10-30T13:05:00Z", reply_id="second")
        self.assertEqual(second["replies"][0], frozen)
        merged = pilot.merge({pilot.TASK_ID: second}, {pilot.TASK_ID: ready})
        self.assertEqual(merged[pilot.TASK_ID], second)
        with zipfile.ZipFile(io.BytesIO(pilot.reply_zip(second))) as archive:
            self.assertEqual(set(archive.namelist()), {"README.txt", "GROK_REPLY.txt", "cfa-visual-review.json"})
            body = archive.read("GROK_REPLY.txt").decode()
            self.assertIn("Not sent", body)
            self.assertIn("Wrong scene entirely.", body)
            for question in pilot.QUESTIONS:
                self.assertIn(question["sha256"], body)
            restored = json.loads(archive.read("cfa-visual-review.json"))
            self.assertEqual(review_provenance(restored)["collaboratorReviews"], merged)

    def test_conflicts_fail_atomically_and_unknown_records_survive(self):
        ready = pilot.prepare(complete(), assets(), now="2026-10-30T13:03:00Z", reply_id="one")
        original = copy.deepcopy(ready)
        conflict = copy.deepcopy(ready)
        conflict["replies"][0]["extra"] = "different immutable receipt"
        with self.assertRaisesRegex(ValueError, "immutable"):
            pilot.merge({pilot.TASK_ID: ready}, {pilot.TASK_ID: conflict})
        draft = complete()
        changed = copy.deepcopy(draft)
        changed["direction"]["note"] = "Different same-time instruction"
        with self.assertRaisesRegex(ValueError, "same timestamp"):
            pilot.merge({pilot.TASK_ID: draft}, {pilot.TASK_ID: changed})
        future = copy.deepcopy(draft)
        future.update(taskID="future-task", questionnaireVersion="future-v2", extra={"preserve": True})
        self.assertEqual(pilot.merge({"future-task": future})["future-task"], future)
        self.assertEqual(ready, original)
        with self.assertRaises(ValueError):
            review_provenance({"collaboratorReviews": []})
        backed_up = review_provenance({"collaboratorReviews": []}, strict_takes=False)
        self.assertEqual(backed_up["collaboratorReviews"], {})
        self.assertEqual(backed_up["collaboratorReviewBackups"][0]["origin"], "source collaboratorReviews")
        for field in ("state", "answer", "direction"):
            malformed = copy.deepcopy(draft)
            if field == "answer":
                malformed["answers"][pilot.QUESTIONS[0]["id"]]["choice"] = []
            elif field == "direction":
                malformed["direction"]["choice"] = []
            else:
                malformed["state"] = []
            with self.assertRaises(ValueError):
                pilot.normalize({pilot.TASK_ID: malformed})

    def test_motion_nomination_is_an_explicit_reviewed_still_and_not_dispatch(self):
        record = complete()
        record = pilot.edit(record, direction={"choice": "nominate_motion", "note": "Later handoff only", "assetID": pilot.QUESTIONS[0]["assetID"]})
        with self.assertRaises(ValueError):
            pilot.prepare(record, assets())
        record = pilot.edit(record, question_id=pilot.QUESTIONS[0]["id"], choice="meets_brief", note="")
        prepared = pilot.prepare(record, assets())
        self.assertIn("separate handoff", pilot.reply_text(prepared))
        self.assertNotIn("sentAt", prepared)
        self.assertEqual(prepared["state"], "ready")


class CollaboratorReviewAppTest(unittest.TestCase):
    def test_portal_answers_back_path_and_task_ready_state(self):
        from streamlit.testing.v1 import AppTest
        source = f'''
import json, sys
from pathlib import Path
sys.path.insert(0, {str(APP)!r})
import streamlit as st
from mission_view import render_corner
from collaborator_review import TASK_ID
catalog = json.loads((Path({str(APP)!r})/'library/design_catalog.json').read_text(encoding='utf-8'))
task = next(t for t in catalog['missionControl']['tasks'] if t['id'] == TASK_ID)
catalog['missionControl']['tasks'] = [task]
st.session_state.setdefault('studio_reviews', {{}})
st.session_state.setdefault('studio_review_provenance', {{}})
st.session_state.studio_project = 'hon'
def open_asset(asset):
 st.session_state.studio_mission_selected = asset['id']
render_corner(catalog, Path({str(APP / 'library')!r}), open_asset,
              lambda a: st.write('OPTIONAL REVIEW '+a['id']), lambda a, **kw: None,
              lambda view: None, lambda: None)
'''
        app = AppTest.from_string(source).run(timeout=30)
        self.assertFalse(app.exception)
        self.assertTrue(any(e.label == "Task map · purpose, sources and next steps" for e in app.expander))
        self.assertFalse(any(e.label == "Briefs and records" for e in app.expander))
        app.button(key="mission-return-review:" + pilot.TASK_ID).click().run(timeout=30)
        self.assertFalse(app.exception)
        self.assertEqual(app.selectbox(key="return-review-step").value, "REV-HD-001")
        app.button(key="return-standard-review:REV-HD-001").click().run(timeout=30)
        self.assertTrue(any("OPTIONAL REVIEW" in e.value for e in app.markdown))
        app.button(key="corner-selected-back").click().run(timeout=30)
        for question in pilot.QUESTIONS:
            app.selectbox(key="return-review-step").select(question["id"]).run(timeout=30)
            app.selectbox(key="return-answer:" + question["id"] + ":choice").select("needs_correction").run(timeout=30)
            app.text_area(key="return-answer:" + question["id"] + ":note").input("Keep the source; repair the recorded defect.").run(timeout=30)
        app.selectbox(key="return-review-step").select("next_action").run(timeout=30)
        app.selectbox(key="return-direction").select("bounded_corrections").run(timeout=30)
        app.button(key="return-prepare").click().run(timeout=30)
        self.assertFalse(app.exception)
        record = app.session_state.studio_review_provenance["collaboratorReviews"][pilot.TASK_ID]
        self.assertEqual(record["state"], "ready")
        self.assertEqual(app.session_state.studio_reviews, {})
        self.assertTrue(any(e.proto.label == "Download reply package for Grok" for e in app.get("download_button")))
        app.button(key="return-task-back").click().run(timeout=30)
        self.assertTrue(any("Ready to send · your reply" in e.label for e in app.expander))
        app.button(key="mission-return-review:" + pilot.TASK_ID).click().run(timeout=30)
        app.selectbox(key="return-review-step").select("REV-HD-001").run(timeout=30)
        app.text_area(key="return-answer:REV-HD-001:note").input("Amended correction").run(timeout=30)
        self.assertEqual(app.session_state.studio_review_provenance["collaboratorReviews"][pilot.TASK_ID]["state"], "draft")
        self.assertEqual(len(app.session_state.studio_review_provenance["collaboratorReviews"][pilot.TASK_ID]["replies"]), 1)


class BrowserBackupTest(unittest.TestCase):
    def test_restored_ready_reply_merges_before_write_and_conflict_is_retained(self):
        import collaborator_review_storage as storage
        class State(dict):
            __getattr__ = dict.__getitem__
            __setattr__ = dict.__setitem__
        class Rerun(Exception):
            pass
        def rerun():
            raise Rerun()
        ready = pilot.prepare(complete(), assets(), now="2026-10-30T13:03:00Z", reply_id="browser-reply")
        state = State(studio_review_provenance={}, studio_reviews={"untouched": {"status": "keep"}})
        fake_st = SimpleNamespace(session_state=state, rerun=rerun)
        event = {"kind": "loaded", "eventID": "first:1", "token": "sha", "raw": json.dumps({pilot.TASK_ID: ready})}
        with patch.object(storage, "st", fake_st), patch.object(storage, "declare_component", return_value=lambda **kw: event):
            with self.assertRaises(Rerun):
                storage.sync()
        self.assertEqual(state.studio_review_provenance["collaboratorReviews"][pilot.TASK_ID], ready)
        self.assertEqual(state.studio_reply_storage_ack, "sha")
        self.assertEqual(state.studio_reviews, {"untouched": {"status": "keep"}})
        broken = {"kind": "loaded", "eventID": "second:1", "token": "bad", "raw": "{broken json"}
        with patch.object(storage, "st", fake_st), patch.object(storage, "declare_component", return_value=lambda **kw: broken):
            with self.assertRaises(Rerun):
                storage.sync()
        self.assertTrue(state.studio_reply_storage_blocked)
        self.assertEqual(state.studio_reply_storage_ack, "sha")
        self.assertEqual(state.studio_review_provenance["collaboratorReviews"][pilot.TASK_ID], ready)
        self.assertEqual(state.studio_review_provenance["collaboratorReviewBackups"][0]["data"], "{broken json")


if __name__ == "__main__":
    unittest.main()
