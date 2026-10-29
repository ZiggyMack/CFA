"""Intake display joins exact revisions and keeps provider findings read-only."""
import copy
import json
from pathlib import Path
import sys
import unittest

APP = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP))
from review_intake_view import (family_for_asset, family_versions, gallery_versions, intake_batch_key,
                               intake_families, intake_review_progress, intake_review_targets,
                               intake_review_totals, intake_rows)
from streamlit.testing.v1 import AppTest


def fixture():
    original, repair, deferred = "a" * 64, "b" * 64, "c" * 64
    assets = [{"id": aid, "sha256": sha, "project": "hon", "filename": aid + ".jpg", "kind": "image",
               "src": "not-packaged.jpg"} for aid, sha in (("original", original), ("repair", repair), ("wrong-copy", "d" * 64))]
    versions = [{"sha256": sha, "assetID": aid, "role": role, "availability": availability,
                 "filename": name, "repoPath": "docs/drop/" + name if availability == "available" else None,
                 "providerReview": {"stage": "scoped pass" if role == "repair" else "source original"},
                 "lineage": {"rootOriginalSha256": original, "baseSha256": original if role == "repair" else None}}
                for aid, sha, role, availability, name in (("original", original, "original", "available", "C04-006.jpg"),
                    ("repair", repair, "repair", "available", "C04-006_v002.jpg"),
                    ("wrong-copy", deferred, "repair", "deferred_history", "C04-006_v001.jpg"))]
    family = {"id": "FALCON:C04-006", "dataset": "FALCON", "frameID": "C04-006", "project": "hon", "category": "Battle light",
              "versions": versions, "original": {"sha256": original, "assetID": "original"},
              "currentCandidate": {"sha256": repair, "assetID": "repair", "accepted": False},
              "providerReview": {"qaGrade": "STRONG", "chestClass": "correct ship", "notes": "Still requires human review"}}
    lisan = dict(copy.deepcopy(family), id="LAG-1K:C04-006", dataset="LAG-1K", project="lisan")
    intake = {"schemaVersion": "cfa-review-metadata-intake-v1", "id": "CFA-META-20261021-r002", "families": [family, lisan],
              "packages": [], "assetMetadata": {"original": {"sha256": original, "familyIDs": [family["id"]]}}}
    return {"assets": assets, "reviewIntake": intake, "reviewDecisions": [{"id": "original", "sha256": original, "status": "needs_fixes", "likenessRating": 2}]}


class IntakeViewTest(unittest.TestCase):
    def test_exact_hash_and_availability_gate_media_without_mutating_reviews(self):
        data = fixture()
        before = copy.deepcopy(data)
        family = data["reviewIntake"]["families"][0]
        items = family_versions(family, data["assets"])
        self.assertEqual([item["asset"]["id"] if item["asset"] else None for item in items], ["original", "repair", None])
        family["versions"][2]["availability"] = "available"
        self.assertIsNone(family_versions(family, data["assets"])[2]["asset"])
        family["versions"][2]["availability"] = "deferred_history"
        self.assertEqual(data, before)
        self.assertEqual(len(family_for_asset(data["reviewIntake"], data["assets"][0])), 1)
        replaced = dict(data["assets"][0], sha256="e" * 64)
        self.assertEqual(family_for_asset(data["reviewIntake"], replaced), [])

    def test_dataset_and_project_scope_do_not_mix_matching_frame_names(self):
        intake = fixture()["reviewIntake"]
        self.assertEqual([f["id"] for f in intake_families(intake, "hon", query="c04-006")], ["FALCON:C04-006"])
        self.assertEqual([f["id"] for f in intake_families(intake, "lisan", "LAG-1K", "correct ship")], ["LAG-1K:C04-006"])
        self.assertEqual(intake_families(intake, "hon", "LAG-1K"), [])

    def test_native_review_compare_and_deferred_history_do_not_promote_provider_pass(self):
        data = fixture()
        script = "\n".join([
            "import sys, json", "from pathlib import Path", "import streamlit as st",
            f"sys.path.insert(0, {str(APP)!r})", "from review_intake_view import render_intake",
            f"data = json.loads({json.dumps(data)!r})", "st.session_state.setdefault('reviews', data['reviewDecisions'])",
            "def open_asset(aid, project): st.session_state.selected = aid",
            f"render_intake(data, 'hon', Path({str(APP / 'library')!r}), open_asset)",
        ])
        app = AppTest.from_string(script, default_timeout=15).run()
        self.assertFalse(app.exception)
        self.assertEqual(app.metric[0].value, "1")
        self.assertEqual(app.metric[1].value, "1")
        self.assertEqual(app.metric[2].value, "1")
        self.assertEqual(app.metric[3].value, "0")
        self.assertTrue(any("Not delivered locally" in t.value for t in app.text))
        self.assertEqual(app.session_state["reviews"], data["reviewDecisions"])
        app.checkbox(key="intake-compare:FALCON:C04-006").check().run()
        self.assertFalse(app.exception)
        self.assertEqual(len(app.selectbox(key="intake-right:FALCON:C04-006").options), 2)
        app.button(key="intake-current:FALCON:C04-006").click().run()
        self.assertEqual(app.session_state["selected"], "repair")
        self.assertEqual(app.session_state["reviews"], data["reviewDecisions"])


class IntakeProgressTest(unittest.TestCase):
    def setUp(self):
        self.data = fixture()
        self.family = self.data["reviewIntake"]["families"][0]
        self.assets = self.data["assets"]
        self.reviews = {"original": {"status": "needs_fixes", "note": "Keep this note"}}

    def test_targets_exclude_older_repairs_and_require_exact_available_media(self):
        older = dict(self.assets[0], id="older", sha256="e" * 64)
        self.assets.append(older)
        self.family["versions"].append({"assetID": "older", "sha256": older["sha256"], "availability": "available", "role": "repair"})
        before = copy.deepcopy(self.data)
        ids = lambda: [asset["id"] for asset in intake_review_targets(self.family, self.assets)]
        self.assertEqual(ids(), ["original", "repair"])
        self.assertEqual(self.data, before)
        self.family["currentCandidate"] = dict(self.family["original"])
        self.assertEqual(ids(), ["original"])
        self.family["versions"][0]["availability"] = "not_delivered"
        self.assertEqual(ids(), ["repair"], "First available is used only when both nominated targets are unavailable")
        self.family["versions"][1]["sha256"] = "f" * 64
        self.assertEqual(ids(), ["older"], "An ID with a wrong hash is never reviewable")
        self.family["versions"][-1]["availability"] = "deferred_history"
        self.assertEqual(ids(), [])
        self.assertTrue(intake_review_progress(self.family, self.assets, self.reviews)["unavailable"])
        self.assertFalse(intake_review_progress(self.family, self.assets, self.reviews)["complete"])

    def test_version_only_base_and_explicit_decisions_have_independent_completion(self):
        family = copy.deepcopy(self.family)
        family.pop("original")
        family.pop("currentCandidate")
        family["versions"][0]["role"] = "version_only_base"
        self.assertEqual([a["id"] for a in intake_review_targets(family, self.assets)], ["original"])
        for choice in ({"note": "Looks good"}, {"likenessRating": 5}, {"variant": "prime"},
                       {"status": "pass"}, {"status": "keep", "sha256": "z" * 64}):
            progress = intake_review_progress(self.family, self.assets, {**self.reviews, "repair": choice})
            self.assertEqual([a["id"] for a in progress["pending"]], ["repair"])
            self.assertFalse(progress["complete"])
        for status in ("keep", "needs_fixes", "remove"):
            progress = intake_review_progress(self.family, self.assets, {**self.reviews, "repair": {"status": status}})
            self.assertTrue(progress["complete"])
        self.assertEqual(self.family["providerReview"]["qaGrade"], "STRONG")
        self.assertFalse(self.family["currentCandidate"]["accepted"])

    def test_unique_target_counts_and_family_filters_after_batch_search(self):
        shared = dict(copy.deepcopy(self.family), id="SECOND:C04-006", dataset="SECOND")
        missing = dict(copy.deepcopy(self.family), id="FALCON:missing", frameID="missing")
        for version in missing["versions"]:
            version["availability"] = "not_delivered"
        intake = {"families": [self.family, shared, missing]}
        before = copy.deepcopy((intake, self.assets, self.reviews))
        totals = intake_review_totals(intake["families"], self.assets, self.reviews)
        self.assertEqual(totals, {"total": 2, "done": 1, "remaining": 1, "familiesPending": 2,
                                  "familiesReviewed": 0, "unavailable": 1})
        rows, totals = intake_rows(intake, "hon", self.assets, self.reviews, batch=intake_batch_key(shared), query="correct ship")
        self.assertEqual([f["id"] for f in rows], [shared["id"]])
        self.assertEqual(totals["remaining"], 1)
        self.assertEqual(intake_rows(intake, "hon", self.assets, self.reviews, decision="reviewed")[0], [])
        finished = {**self.reviews, "repair": {"status": "keep"}}
        self.assertEqual(len(intake_rows(intake, "hon", self.assets, finished, decision="reviewed")[0]), 2)
        self.assertEqual(len(intake_rows(intake, "hon", self.assets, finished, decision="all")[0]), 3)
        rows, totals = intake_rows(intake, "hon", self.assets, finished, dataset="wrong", query="no match",
                                   batch="wrong", decision="pending", focused=missing["id"])
        self.assertEqual(rows, [missing])
        self.assertEqual(totals["unavailable"], 1)
        self.assertEqual((intake, self.assets, self.reviews), before)

    def test_pending_gallery_promotes_repair_and_keeps_original_and_history(self):
        pending, related = gallery_versions(self.family, self.assets, self.reviews)
        self.assertEqual(pending["asset"]["id"], "repair")
        self.assertEqual([item["version"]["assetID"] for item in related], ["original", "wrong-copy"])
        all_cover, all_related = gallery_versions(self.family, self.assets, self.reviews, "all")
        self.assertEqual(all_cover["asset"]["id"], "original")
        self.assertEqual(len(all_related), 2)
        self.family["versions"].append(copy.deepcopy(self.family["versions"][0]))
        self.assertEqual(len(gallery_versions(self.family, self.assets, self.reviews)[1]), 2)


def app_script(data, with_decision_buttons=False):
    lines = ["import sys, json", "from pathlib import Path", "import streamlit as st",
             f"sys.path.insert(0, {str(APP)!r})", "from review_intake_view import render_intake",
             "from studio_dependencies import effective_reviews", f"data = json.loads({json.dumps(data)!r})",
             "st.session_state.setdefault('studio_reviews', effective_reviews(data['assets'], data.get('reviewDecisions', []), {}))",
             "def open_asset(aid, project): st.session_state.selected = aid"]
    if with_decision_buttons:
        lines.extend(["def choose(status): st.session_state.studio_reviews['repair'] = {'status': status, 'note':'Preserved review'}",
                      "st.button('Test Keep', on_click=choose, args=('keep',), key='test-keep')",
                      "st.button('Test Clear', on_click=choose, args=(None,), key='test-clear')"])
    lines.append(f"render_intake(data, 'hon', Path({str(APP / 'library')!r}), open_asset, reviews=st.session_state.studio_reviews)")
    return "\n".join(lines)


class IntakeParityAppTest(unittest.TestCase):
    def test_live_progress_and_review_filters_use_saved_choices_without_mutating_them(self):
        data = fixture()
        app = AppTest.from_string(app_script(data, True), default_timeout=20).run()
        self.assertFalse(app.exception)
        self.assertEqual(app.selectbox(key="intake-decision:hon").value, "pending")
        self.assertEqual(app.metric[0].value, "1")
        self.assertEqual(app.session_state["studio_intake_sequence"], ["original", "repair"])
        app.button(key="test-keep").click().run()
        self.assertFalse(app.exception)
        self.assertEqual([m.value for m in app.metric[:3]], ["0", "2", "0"])
        self.assertTrue(any("No families match" in item.value for item in app.info))
        app.selectbox(key="intake-decision:hon").select("reviewed").run()
        self.assertTrue(any(item.value == "C04-006" for item in app.subheader))
        app.selectbox(key="intake-decision:hon").select("all").run()
        self.assertEqual(app.session_state["studio_reviews"]["repair"], {"status": "keep", "note": "Preserved review"})
        app.button(key="test-clear").click().run()
        app.selectbox(key="intake-decision:hon").select("pending").run()
        self.assertEqual(app.metric[0].value, "1")
        self.assertFalse(app.exception)

    def test_gallery_batch_focus_and_evidence_share_membership_and_keep_review_data(self):
        data = fixture()
        second = dict(copy.deepcopy(data["reviewIntake"]["families"][0]), id="SECOND:C04-006", dataset="SECOND")
        data["reviewIntake"]["families"].append(second)
        app = AppTest.from_string(app_script(data), default_timeout=20).run()
        before = copy.deepcopy(app.session_state["studio_reviews"])
        app.selectbox(key="intake-layout:hon").select("gallery").run()
        app.selectbox(key="intake-batch:hon").select("SECOND::Battle light").run()
        self.assertFalse(app.exception)
        self.assertEqual(app.session_state["studio_intake_sequence"], ["repair"])
        self.assertEqual(len([b for b in app.button if b.label == "View family evidence"]), 1)
        app.button(key="intake-gallery:SECOND:C04-006").click().run()
        self.assertEqual(app.session_state["selected"], "repair")
        app.button(key="intake-detail:SECOND:C04-006").click().run()
        self.assertFalse(app.exception)
        self.assertEqual(app.selectbox(key="intake-layout:hon").value, "evidence")
        self.assertEqual(len([s for s in app.subheader if s.value == "C04-006"]), 1)
        self.assertEqual(app.session_state["studio_intake_sequence"], ["original", "repair"])
        app.button(key="intake-back:hon").click().run()
        self.assertEqual(app.session_state["studio_reviews"], before)
        self.assertEqual(app.selectbox(key="intake-layout:hon").value, "gallery")
        self.assertEqual(app.selectbox(key="intake-batch:hon").value, "SECOND::Battle light")
        app.selectbox(key="intake-dataset:hon").select("FALCON").run()
        self.assertEqual(app.selectbox(key="intake-batch:hon").value, "all")

    def test_pagination_switches_page_size_and_clamps_after_review(self):
        data = fixture()
        family = data["reviewIntake"]["families"][0]
        data["reviewIntake"]["families"] = [dict(copy.deepcopy(family), id=f"FALCON:{i}", frameID=str(i)) for i in range(40)]
        app = AppTest.from_string(app_script(data), default_timeout=30).run()
        self.assertFalse(app.exception)
        self.assertEqual(len([s for s in app.subheader if s.value.isdigit()]), 12)
        app.number_input[0].set_value(4).run()
        self.assertEqual(len([s for s in app.subheader if s.value.isdigit()]), 4)
        app.selectbox(key="intake-layout:hon").select("gallery").run()
        self.assertFalse(app.exception)
        self.assertEqual(len([b for b in app.button if b.label == "View family evidence"]), 36)
        self.assertEqual(app.number_input[0].value, 1)
        self.assertEqual(app.session_state["studio_intake_sequence"], ["repair"])

    def test_supplement_is_collapsed_exact_hash_only_and_receipts_are_last(self):
        data = fixture()
        data["reviewSupplements"] = [{"id": "supp", "title": "Winners supplement", "indexURL": "https://example.org/index.html",
                                      "csvURL": "../../outside.csv", "mediaDelivery": {"fullImages": 1}, "items": [
            {"id": "exact", "project": "hon", "title": "Scoped chest pass", "group": "validated", "availability": "local_original_verified",
             "exactAssetID": "repair", "sha256": "b" * 64, "reviewScope": "Chest only", "familyIDs": ["FALCON:C04-006"]},
            {"id": "wrong", "project": "hon", "title": "Wrong hash", "group": "preliminary", "availability": "local_original_verified",
             "exactAssetID": "repair", "sha256": "f" * 64}]}]
        app = AppTest.from_string(app_script(data), default_timeout=20).run()
        self.assertFalse(app.exception)
        outer = next(e for e in app.expander if e.label.startswith("Winners supplement"))
        self.assertFalse(outer.proto.expanded)
        self.assertEqual(app.expander[-1].label, "Handoff coverage and receipts · optional")
        self.assertFalse(app.expander[-1].proto.expanded)
        self.assertEqual(len([b for b in app.button if b.key and b.key.startswith("intake-supplement:") and b.key.endswith(":open")]), 1)
        self.assertTrue(any("source file not packaged" in c.value for c in app.caption))
        self.assertTrue(any("Preview only" in c.value for c in app.caption))
        self.assertNotIn("repair", app.session_state["studio_reviews"])
        app.button(key="intake-supplement:hon:0:exact:open").click().run()
        self.assertEqual(app.session_state["selected"], "repair")


if __name__ == "__main__":
    unittest.main()
