"""Compact Ziggy's Corner, using the index's prepared task and review records."""
from pathlib import Path
from datetime import date, datetime, timezone
import json
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import streamlit as st

from studio_dependencies import current_module, destination_label, output_kind_label, media_path, mission_pending_requests, mission_storyboard_requests, mission_task_progress, mission_tasks, mission_visible, review_provenance

STATES = {"ready": ("Ready to send", "green"), "needs_input": ("Needs your input", "orange"),
          "in_progress": ("In progress", "blue"), "planned": ("Planned", "gray"), "done": ("Done", "green")}
RANK = {"ready": 0, "needs_input": 1, "in_progress": 2, "planned": 3, "done": 4}
DIRECTIONS = {"inbound": "Incoming", "outbound": "Outgoing", "internal": "Internal"}
WORK_KINDS = {"image_new": "New image", "image_repair": "Image repair", "video": "Video", "planning": "Planning"}
PROVIDER_FAMILIES = {
    "Grok / Chief of Staff": ("Grok",), "Claude (lead writer)": ("Claude",),
    "CFA / Grok / Gemini": ("CFA", "Grok", "Gemini"), "Grok / Gemini": ("Grok", "Gemini"),
}


def provider_families(provider):
    """Known team assignments only; unknown slash labels remain a single provider."""
    return PROVIDER_FAMILIES.get(provider, (provider,))


def provider_matches(provider, selected):
    members = provider_families(provider)
    return selected == "all" or (len(members) > 1 if selected == "Teamwork" else selected in members)


def format_page_updated(value):
    """Display footer dates without changing the source timestamp or shifting date-only values."""
    if not isinstance(value, str):
        return "Time unavailable"
    text = value.strip()
    try:
        if len(text) == 10:
            return date.fromisoformat(text).strftime("%m.%d.%Y")
        moment = datetime.fromisoformat(text.replace("Z", "+00:00"))
    except ValueError:
        return "Time unavailable"
    if moment.tzinfo is not None:
        try:
            display_zone = ZoneInfo("America/New_York")
        except ZoneInfoNotFoundError:
            display_zone = timezone.utc
        moment = moment.astimezone(display_zone)
    clock = f"{moment.hour % 12 or 12}:{moment.minute:02d} {'AM' if moment.hour < 12 else 'PM'}"
    zone = moment.tzname()
    return moment.strftime("%m.%d.%Y") + " · " + clock + (" " + zone if zone else "")


def show_collection(ids, label, mode="references", project=None):
    st.session_state.studio_mission_collection = {"ids": ids, "label": label, "mode": mode, "project": project}
    st.session_state.studio_mission_selected = None
    st.session_state.pop("corner-collection-page", None)


def close_collection():
    st.session_state.pop("studio_mission_collection", None)
    st.session_state.pop("studio_mission_selected", None)
    st.session_state.pop("studio_mission_questionnaire", None)
    st.session_state.pop("studio_mission_task_focus", None)


def _reply_record():
    pilot = current_module("collaborator_review")
    return st.session_state.get("studio_review_provenance", {}).get("collaboratorReviews", {}).get(pilot.TASK_ID)


def _store_reply(record):
    pilot = current_module("collaborator_review")
    provenance = dict(st.session_state.get("studio_review_provenance", {}))
    provenance["collaboratorReviews"] = {**provenance.get("collaboratorReviews", {}), pilot.TASK_ID: record}
    st.session_state.studio_review_provenance = provenance
    if not st.session_state.get("studio_reply_storage_blocked") and st.session_state.get("studio_reply_storage_status") != "unavailable":
        st.session_state.studio_reply_storage_status = "syncing"


def start_return_review(assets):
    pilot = current_module("collaborator_review")
    record = _reply_record() or pilot.empty()
    st.session_state.studio_mission_questionnaire = pilot.TASK_ID
    st.session_state.studio_mission_task_focus = pilot.TASK_ID
    st.session_state.pop("studio_mission_selected", None)
    st.session_state.pop("studio_mission_collection", None)
    st.session_state["return-review-step"] = next((q["id"] for q in pilot.QUESTIONS
        if not pilot.answer_complete(q, record["answers"].get(q["id"]), assets)), "next_action")


def back_to_return_task():
    pilot = current_module("collaborator_review")
    st.session_state.studio_mission_task_focus = pilot.TASK_ID
    st.session_state.pop("studio_mission_questionnaire", None)
    st.session_state.pop("studio_mission_selected", None)


def back_to_questionnaire():
    st.session_state.pop("studio_mission_selected", None)


def _save_return_answer(question_id):
    pilot = current_module("collaborator_review")
    key = "return-answer:" + question_id
    _store_reply(pilot.edit(_reply_record(), question_id=question_id,
                           choice=st.session_state[key + ":choice"], note=st.session_state[key + ":note"]))


def _save_return_direction():
    pilot = current_module("collaborator_review")
    choice = st.session_state.get("return-direction", "")
    direction = {"choice": choice, "note": st.session_state.get("return-direction-note", "")}
    if choice == "nominate_motion":
        direction["assetID"] = st.session_state.get("return-direction-asset", "")
    _store_reply(pilot.edit(_reply_record(), direction=direction))


def _prepare_return_reply(assets):
    pilot = current_module("collaborator_review")
    try:
        _store_reply(pilot.prepare(_reply_record() or pilot.empty(), assets))
        st.session_state["return-review-message"] = "Reply prepared. Your part is ready to send; no message or generation has been sent."
        st.session_state.pop("return-review-error", None)
    except ValueError as error:
        st.session_state["return-review-error"] = str(error)


def _return_step(step):
    st.session_state["return-review-step"] = step


def _restore_return_review(payload):
    """Restore task records atomically; ordinary asset decisions use the full importer."""
    pilot = current_module("collaborator_review")
    if (not isinstance(payload, dict) or payload.get("format") != "cfa-visual-review-v1"
            or not isinstance(payload.get("collaboratorReviews"), dict) or pilot.TASK_ID not in payload["collaboratorReviews"]):
        raise ValueError("Choose a review JSON containing this task's saved questionnaire.")
    provenance = review_provenance({"collaboratorReviews": payload["collaboratorReviews"]},
                                  st.session_state.get("studio_review_provenance", {}))
    st.session_state.studio_review_provenance = provenance
    for key in list(st.session_state):
        if key.startswith("return-answer:") or key in {"return-direction", "return-direction-note", "return-direction-asset"}:
            st.session_state.pop(key, None)


def returned_task_progress(task, assets):
    pilot = current_module("collaborator_review")
    if task["id"] != pilot.TASK_ID or task["status"] == "done":
        return task
    state = pilot.progress(_reply_record(), assets)
    task = dict(task)
    task["status"] = "ready" if state["ready"] else "needs_input"
    task["statusLabel"] = "Ready to send · your reply" if state["ready"] else "Your return review · " + str(state["answered"]) + "/7"
    if state["ready"]:
        task["nextAction"] = "Download the prepared reply for manual delivery to Grok. Delivery and follow-up remain open; nothing has been sent from this page."
    return task


def render_return_map(task, data, library_dir, open_reference, document_download, context):
    """One overview with purpose-labeled branches; source records stay accessible."""
    pilot = current_module("collaborator_review")
    by_id = {a["id"]: a for a in data["assets"]}
    links = {link["label"]: link for link in task.get("links", [])}
    branches = [
        ("What we asked for", "The October 8 package requested seven correction / Caleb stills. Other held work in that dated cover is not a new assignment.", ["Read the Grok cover"]),
        ("What came back", "The October 9 intake verifies received files and records limits, including REV-HD-001 preservation and CAL-P01 tattoo defects. Technical verification is separate from your creative judgment.", ["Verified intake & next steps"]),
        ("How to judge it", "Use newer living design instructions when they supersede the dated package. The original request still explains the preservation goal; its old detail counts do not override later choices.", ["Current Grok design instructions"]),
        ("What this can lead to", "Panel coverage and the favorite prop sweep describe conditional follow-on work. They do not assign song timecodes, authorize a new batch, or start motion.", ["Panel plan", "Favorite-look prop sweep"]),
        ("Delivery record", "This receipt records the October 8 outgoing care package and acknowledgement. It does not record delivery of your new reply or completion of the returned-image review.", ["Grok delivery and acknowledgement"]),
    ]
    with st.expander("Task map · purpose, sources and next steps", expanded=False):
        st.markdown("**Request → received evidence → your review → reply ready to send → corrections or a later motion handoff**")
        st.write("Assess the seven requested returns, identify remaining fixes, and give Grok one bounded next direction.")
        for branch, purpose, labels in branches:
            st.markdown("**" + branch + "**")
            st.caption(purpose)
            for label in labels:
                link = links.get(label)
                if not link:
                    st.caption(label + " is not included in this task snapshot.")
                    continue
                asset = by_id.get(link.get("assetID"))
                if asset:
                    with st.expander(label, expanded=False):
                        if asset.get("text"):
                            st.text(asset["text"])
                        document_download(asset, context="return-map:" + context + ":" + label)
                elif link.get("href"):
                    st.link_button(label, link["href"])
                else:
                    st.caption(label + ": source record unavailable in this snapshot.")
        with st.expander("Seven returned image records", expanded=False):
            for question in pilot.QUESTIONS:
                if asset := pilot.available(question, data["assets"]):
                    st.button(question["id"] + " · " + question["title"],
                              key="return-map-image:" + context + ":" + question["id"], on_click=open_reference, args=(asset,))
                else:
                    st.caption(question["id"] + ": exact image unavailable; questionnaire retains its source identity.")
    # Keep the original outgoing package last, after the map and new reply records.
    for i, link in enumerate(task.get("links", [])):
        if link.get("downloadPath"):
            package = media_path(library_dir, link["downloadPath"])
            if package and package.suffix.lower() == ".zip":
                st.download_button("Original October 8 care package · " + link["label"], package.read_bytes(),
                                   file_name=package.name, mime="application/zip", key="return-care-package:" + context + ":" + str(i))
            else:
                st.caption("Original October 8 care package is not included in this snapshot.")


def render_return_review(data, library_dir, open_reference, document_download):
    """Task-specific brief + return + answer, with a recoverable consolidated reply."""
    pilot = current_module("collaborator_review")
    assets = data["assets"]
    record = _reply_record() or pilot.empty()
    state = pilot.progress(record, assets)
    st.button("← Back to this task", key="return-task-back", on_click=back_to_return_task)
    st.caption("Ziggy’s Corner › Received the bounded Hon still return › Review returned images")
    st.subheader("Review the returned Hon stills")
    st.write("Seven outputs were requested: four corrections, a hip detail, a Caleb reference and a Caleb scene. The old task linked five; the two omitted returns are included here by their exact source identities.")
    st.caption("The checklist reflects the October 8 brief and October 9 receipt. Note any newer direction in your answer. Existing library triage is context; it does not answer these questions for you.")
    st.info("Newer living design instructions take precedence. For example, Hon now has four upper gold caps; the old package’s two-canines-only pattern is superseded. The task map below includes the current rules and source history.")
    st.progress(state["answered"] / state["total"], text=f"{state['answered']} of {state['total']} return questions answered · " + ("Ready to send" if state["ready"] else "Draft"))
    current_module("collaborator_review_storage").caption()
    if record.get("questionnaireVersion") != pilot.VERSION:
        st.warning("This saved questionnaire has a different version. Its answers and reply history are preserved; reconcile them before preparing a new reply.")
        return
    if message := st.session_state.pop("return-review-message", None):
        st.success(message)
    if error := st.session_state.pop("return-review-error", None):
        st.error(error)
    steps = [q["id"] for q in pilot.QUESTIONS] + ["next_action"]
    labels = {q["id"]: f"{i + 1}. {q['id']} · {q['title']}" for i, q in enumerate(pilot.QUESTIONS)}
    labels["next_action"] = "8. Next action and prepare reply"
    if st.session_state.get("return-review-step") not in steps:
        st.session_state["return-review-step"] = steps[0]
    step = st.selectbox("Review step", steps, format_func=labels.get, key="return-review-step")
    if step != "next_action":
        question = next(q for q in pilot.QUESTIONS if q["id"] == step)
        asset = pilot.available(question, assets)
        left, right = st.columns([3, 2])
        with left:
            picture = media_path(library_dir, (asset or {}).get("src") or (asset or {}).get("thumb"))
            if picture:
                st.image(str(picture), width="stretch", caption=question["id"] + " · Returned candidate")
            else:
                st.warning("The exact returned image is unavailable in this snapshot. Choose Cannot assess and describe what is missing.")
            st.caption(question["assetID"] + " · Original SHA256 " + question["sha256"])
            if asset:
                prior = st.session_state.studio_reviews.get(asset["id"], {})
                if prior.get("status") or prior.get("note"):
                    with st.expander("Existing library review · context only", expanded=False):
                        if prior.get("status"):
                            st.write("Triage: " + prior["status"])
                        if prior.get("note"):
                            st.write(prior["note"])
                st.button("Open standard image review · optional", key="return-standard-review:" + step,
                          on_click=open_reference, args=(asset,))
            with st.expander("Original reference and evidence", expanded=False):
                for label, ref in [("Requested source", question.get("source")), ("Design reference supplied with this brief", pilot.STANDARD if step != "CALEB-K_REF" else None)]:
                    if not ref:
                        continue
                    source = pilot.available(ref, assets)
                    if source:
                        thumb = media_path(library_dir, source.get("thumb") or source.get("src"))
                        if thumb:
                            st.image(str(thumb), width="stretch", caption=label)
                        st.button(label, key="return-source:" + step + ":" + ref["assetID"], on_click=open_reference, args=(source,))
                    else:
                        st.caption(label + " is unavailable here; do not assume this comparison was checked.")
                    st.caption(ref["assetID"] + " · SHA256 " + ref["sha256"])
        with right:
            st.markdown("**Requested work**")
            st.write(question["request"])
            if question.get("known"):
                st.info(question["known"])
            if asset and asset.get("note"):
                with st.expander("Received review notes", expanded=False):
                    st.write(asset["note"])
            st.markdown("**" + question["question"] + "**")
            answer = record["answers"].get(step, {})
            key = "return-answer:" + step
            st.session_state.setdefault(key + ":choice", answer.get("choice", ""))
            st.session_state.setdefault(key + ":note", answer.get("note", ""))
            st.selectbox("Your result", list(pilot.CHOICES), format_func=pilot.CHOICES.get, key=key + ":choice",
                         on_change=_save_return_answer, args=(step,))
            st.text_area("What should stay, change or be clarified?", key=key + ":note", max_chars=20000,
                         height=160, on_change=_save_return_answer, args=(step,))
            st.caption("Corrections, rejection and uncertainty need a note. This saves a task answer; it does not change your library rating or acceptance records.")
    else:
        direction = record.get("direction", {})
        st.session_state.setdefault("return-direction", direction.get("choice", ""))
        st.session_state.setdefault("return-direction-note", direction.get("note", ""))
        st.selectbox("What should Grok do next?", list(pilot.DIRECTIONS), format_func=pilot.DIRECTIONS.get,
                     key="return-direction", on_change=_save_return_direction)
        if st.session_state["return-direction"] == "nominate_motion":
            candidates = [q for q in pilot.QUESTIONS if q["id"] != "PROP-HD-HIP" and pilot.available(q, assets)
                          and record["answers"].get(q["id"], {}).get("choice") == "meets_brief"]
            options = ["", *(q["assetID"] for q in candidates)]
            names = {q["assetID"]: q["title"] for q in candidates}
            if st.session_state.get("return-direction-asset", direction.get("assetID", "")) not in options:
                st.session_state["return-direction-asset"] = ""
            st.session_state.setdefault("return-direction-asset", direction.get("assetID", ""))
            st.selectbox("Still to nominate", options, format_func=lambda value: names.get(value, "Choose a reviewed still…"),
                         key="return-direction-asset", on_change=_save_return_direction)
            st.caption("This names a candidate for a separate motion handoff; it does not start or authorize a video run.")
        st.text_area("Reply summary / bounded instructions", key="return-direction-note", max_chars=20000,
                     height=130, on_change=_save_return_direction)
        st.markdown("**Check your answers**")
        for q in pilot.QUESTIONS:
            answer = record["answers"].get(q["id"], {})
            st.write(q["id"] + " — " + pilot.CHOICES.get(answer.get("choice", ""), "Unanswered"))
            if answer.get("note"):
                st.caption(answer["note"])
        st.button("Prepare reply for Grok", key="return-prepare", type="primary", on_click=_prepare_return_reply,
                  args=(assets,), disabled=state["ready"])
        st.caption("Preparing records your finished response as Ready to send. It does not send it, complete the collaborator task, or approve unrelated work. Changing an answer returns the response to Draft.")
    index = steps.index(step)
    previous, following = st.columns(2)
    previous.button("← Previous", key="return-previous", on_click=_return_step,
                    args=(steps[max(0, index - 1)],), disabled=index == 0)
    following.button("Next →", key="return-next", on_click=_return_step,
                     args=(steps[min(len(steps) - 1, index + 1)],), disabled=index == len(steps) - 1)
    st.divider()
    if state["ready"]:
        st.success("Your consolidated reply is ready to send. Delivery is still unrecorded.")
        st.download_button("Download reply package for Grok", pilot.reply_zip(record),
                           file_name="grok-proof-package-reply.zip", mime="application/zip", key="return-reply-zip")
        with st.expander("Read the prepared reply", expanded=False):
            st.text(pilot.reply_text(record))
    snapshot = {"format": "cfa-visual-review-v1", "items": [], "favorites": [], "collaboratorReviews": {pilot.TASK_ID: record}}
    st.download_button("Save task draft / review JSON", json.dumps(snapshot, ensure_ascii=False, indent=2),
                       file_name="grok-proof-package-review.json", mime="application/json", key="return-save-draft")
    with st.expander("Restore a saved task review", expanded=False):
        uploaded = st.file_uploader("Task review JSON (or the JSON inside its reply ZIP)", type=["json"], key="return-restore-file")
        if uploaded and st.button("Restore task review", key="return-restore"):
            try:
                if uploaded.size > 50 * 1024 * 1024:
                    raise ValueError("Choose a review file no larger than 50 MiB.")
                _restore_return_review(json.loads(uploaded.getvalue()))
                st.session_state["return-review-message"] = "Task review restored. Use the normal full-review importer to restore any separate image decisions."
                st.rerun()
            except (ValueError, TypeError, UnicodeDecodeError) as error:
                st.error(str(error))
    if record.get("replies"):
        with st.expander(f"Prepared reply history · {len(record['replies'])}", expanded=False):
            for reply in record["replies"]:
                st.caption(reply["preparedAt"] + " · " + reply["id"] + " · prepared, not a delivery receipt")
                st.json({"answers": reply["answers"], "nextAction": reply["direction"]}, expanded=False)
    task = next((t for t in mission_tasks(data.get("missionControl", {})) if t["id"] == pilot.TASK_ID), None)
    if task:
        render_return_map(task, data, library_dir, open_reference, document_download, "portal")


def open_storyboard_review(project, story_id, structure, navigate):
    st.session_state.studio_project = project
    st.session_state[f'story-select:{project}'] = story_id
    st.session_state[f'story-view:{project}'] = 'Structure & gaps' if structure else 'Panels & writings'
    navigate('Storyboard')


def render_corner(data, library_dir: Path, open_reference, render_selected, document_download, navigate, sweep, review_data=None, archived=False):
    reviews = st.session_state.studio_reviews
    by_id = {a["id"]: a for a in data["assets"]}
    review_by_id = {a["id"]: a for a in (review_data or data)["assets"]}
    plans = [a for aid, a in review_by_id.items() if reviews.get(aid, {}).get("shotPlan") and mission_visible(a, reviews)]
    projects = {p["id"]: p["name"] for p in data["projects"]}
    if not archived and (selected := review_by_id.get(st.session_state.get("studio_mission_selected"))):
        if st.session_state.get("studio_mission_questionnaire") == "grok-proof-package":
            st.button("← Back to the return questionnaire", on_click=back_to_questionnaire, key="corner-selected-back")
            st.caption("Ziggy’s Corner › Bounded Hon still return › Optional library image review")
        else:
            st.button("← Back to Ziggy’s Corner", on_click=close_collection, key="corner-selected-back")
        render_selected(selected)
        return
    if not archived and st.session_state.get("studio_mission_questionnaire") == "grok-proof-package":
        render_return_review({**data, "assets": list(review_by_id.values())}, library_dir, open_reference, document_download)
        return
    if not archived and (collection := st.session_state.get("studio_mission_collection")):
        st.button("← Back to Ziggy’s Corner", on_click=close_collection, key="corner-collection-back")
        st.subheader(collection["label"])
        is_plans = collection.get("mode") == "shot_plans"
        if is_plans:
            items = plans
            st.caption(f"{len(items)} saved shot plans across all projects.")
        else:
            ids = mission_pending_requests(data, reviews, collection["project"]) if collection.get("mode") == "review_requests" else collection["ids"]
            items = [by_id[aid] for aid in dict.fromkeys(ids) if aid in by_id and mission_visible(by_id[aid], reviews)]
        if not items:
            st.info("No visible shot plans saved." if is_plans else "No unanswered image reviews remain." if collection.get("mode") == "review_requests" else
                    "No visible references in this collection. Recorded removal and archive decisions remain saved.")
        else:
            page = st.selectbox("Page", range((len(items) + 23) // 24), format_func=lambda n: str(n + 1), key="corner-collection-page")
            for offset in range(page * 24, min((page + 1) * 24, len(items)), 4):
                for col, asset in zip(st.columns(4), items[offset:offset + 4]):
                    with col:
                        picture = media_path(library_dir, asset.get("thumb") or asset.get("src"))
                        if picture and asset.get("kind") == "image":
                            st.image(str(picture), width="stretch")
                        if is_plans:
                            plan = reviews[asset["id"]]["shotPlan"]
                            st.caption(projects.get(asset.get("project"), "Across projects") + " · " + output_kind_label(plan.get("outputKind")) + " · " + ", ".join(map(destination_label, plan.get("destinations", ["undecided"]))))
                            if plan.get("idea"):
                                st.write(plan["idea"])
                            if plan.get("prompt"):
                                with st.expander("Prompt", expanded=False):
                                    st.text(plan["prompt"])
                        st.button(asset.get("title", asset["id"]), key="corner-collection:" + asset["id"], on_click=open_reference, args=(asset,))
        return

    control = data.get("missionControl", {})
    tasks = sorted((returned_task_progress(mission_task_progress(t, data["assets"], reviews), (review_data or data)["assets"]) for t in mission_tasks(control)
                    if (t["status"] == "done") == archived), key=lambda t: RANK[t["status"]])
    if archived:
        st.subheader("Completed tasks")
        st.caption("Completed handoffs and their records remain available here.")
    else:
        columns = st.columns(4)
        counts = [(STATES[s][0], sum(t["status"] == s for t in tasks)) for s in ("ready", "needs_input", "in_progress")]
        for col, (label, number) in zip(columns, counts):
            col.metric(label, number)
        columns[3].button(f"Shot plans · {len(plans)} →", key="mission-shot-plans", width="stretch",
                          on_click=show_collection, args=([], "All shot plans", "shot_plans"))
    priority_slot = st.container(key="mission-priority")
    filter_col, search_col = st.columns([1, 2])
    with filter_col:
        families = list(dict.fromkeys(family for task in tasks for family in provider_families(task["provider"])))
        provider_options = ["all", *families, *(["Teamwork"] if any(len(provider_families(task["provider"])) > 1 for task in tasks) else [])]
        selected_provider = st.session_state.get("mission-provider", "all")
        if selected_provider not in provider_options:
            members = provider_families(selected_provider)
            replacement = members[0] if len(members) == 1 else "Teamwork"
            st.session_state["mission-provider"] = replacement if replacement in provider_options else "all"
        provider = st.selectbox("Collaborator", provider_options,
                                format_func=lambda s: "All collaborators" if s == "all" else s, key="mission-provider")
    with search_col:
        query = st.text_input("Find a task", key="mission-search").casefold().strip()
    matching = [t for t in tasks if provider_matches(t["provider"], provider) and
                query in " ".join(str(t.get(k, "")) for k in ("title", "provider", "project", "summary", "nextAction")).casefold()]
    focused = None if archived else st.session_state.get("studio_mission_task_focus")
    if focused:
        matching = [t for t in tasks if t["id"] == focused]
        st.button("← All Corner tasks", key="corner-all-tasks", on_click=close_collection)

    def references(ids, context, history=False, limit=None):
        items = [(i, by_id[aid]) for i, aid in enumerate(dict.fromkeys(ids))
                 if aid in by_id and (history or mission_visible(by_id[aid], reviews))]
        if limit is not None:
            items = items[:limit]
        for offset in range(0, len(items), 4):
            for column, (i, asset) in zip(st.columns(4), items[offset:offset + 4]):
                with column:
                    picture = media_path(library_dir, asset.get("thumb") or (asset.get("src") if asset.get("kind") == "image" else None))
                    if picture:
                        st.image(str(picture), width="stretch")
                    st.button(asset.get("title", asset["id"]), key=f"corner-reference:{context}:{i}",
                              on_click=open_reference, args=(asset,), width="stretch")

    def card_content(task, context):
        label, color = STATES[task["status"]]
        project = projects.get(task["project"], "Across projects")
        with st.expander(f":{color}-badge[{task.get('statusLabel', label)}] **{task['title']}** · {project}", expanded=task["id"] == focused):
            st.caption(task["provider"] + " · " + DIRECTIONS[task["direction"]] + " · " + WORK_KINDS[task["workKind"]])
            st.write(task["summary"])
            if task["nextAction"]:
                st.markdown("**Next**")
                st.write(task["nextAction"])
            if task["id"] == "grok-proof-package" and not archived:
                st.button("Review returned images →", key="mission-return-review:" + context,
                          on_click=start_return_review, args=((review_data or data)["assets"],), type="primary")
                st.caption("Seven exact outputs · requested fixes beside each image · save a single reply for Grok.")
            writing_requests = mission_storyboard_requests(data, [task], task['project'])
            if writing_requests:
                request = writing_requests[0]
                st.markdown('**For you now**')
                st.caption('Open the written shots to inspect their context. Discuss your choices in chat.')
                st.button('Storyboard · Structure & gaps' if request['structure'] else 'Storyboard · Panels & writings',
                          key='mission-writing-workspace:'+context, on_click=open_storyboard_review,
                          args=(request['project'], request['storyID'], request['structure'], navigate))
            for field, heading in (("enablers", "Before sending"), ("deliverables", "Deliverables"), ("missing", task.get("missingLabel", "Other open items"))):
                if task.get(field):
                    if field == 'missing' and writing_requests:
                        heading = 'Author choices · discuss in chat'
                    st.markdown(f"**{heading}**")
                    for value in task[field]:
                        (st.warning if field == "enablers" else st.write)(value)
            if task.get("laterReview"):
                st.markdown("**Your later review**")
                st.write(task["laterReview"])
            if task.get("previewAssetIDs"):
                if writing_requests:
                    with st.expander('Reference images · optional', expanded=False):
                        references(task["previewAssetIDs"], context + ":preview")
                else:
                    st.markdown("**Start with these images**")
                    references(task["previewAssetIDs"], context + ":preview")
            if task.get("reviewedPreviewAssetIDs"):
                with st.expander(f"Recorded review decisions · {len(task['reviewedPreviewAssetIDs'])}", expanded=False):
                    references(task["reviewedPreviewAssetIDs"], context + ":history", history=True)
            for comparison in data.get("sourceComparisons", []):
                if comparison.get("missionTaskID") == task["id"]:
                    with st.expander("Selected starting image and earlier comparison", expanded=False):
                        st.write(comparison.get("summary", ""))
                        references([r["assetID"] for r in comparison.get("items", [])], context + ":comparison")
            if task["id"] == "grok-proof-package":
                render_return_map(task, data, library_dir, open_reference, document_download, context)
                return
            with st.expander('Briefs and records', expanded=False):
                for i, link in enumerate(task["links"]):
                    key = f"{context}:{i}"
                    if link.get("downloadPath"):
                        package = media_path(library_dir, link["downloadPath"])
                        if package and package.suffix.lower() == ".zip":
                            st.download_button(link["label"], package.read_bytes(), file_name=package.name, mime="application/zip", key="mission-package:" + key)
                        else:
                            st.caption(link["label"] + ": package is not included in this snapshot.")
                    elif link.get("assetIDs") is not None:
                        st.button(link["label"], key="mission-collection:" + key, on_click=show_collection, args=(link["assetIDs"], link["label"]))
                        references(link["assetIDs"], context + ":linked:" + str(i), limit=8)
                    elif asset := by_id.get(link.get("assetID")):
                        if asset.get("kind") in {"document", "pdf"}:
                            with st.expander(link["label"], expanded=False):
                                if asset.get("text"):
                                    st.text(asset["text"])
                                document_download(asset, context="mission:" + key)
                        else:
                            st.button(link["label"], key="mission-asset:" + key, on_click=open_reference, args=(asset,))
                    elif link.get("href"):
                        st.link_button(link["label"], link["href"])
                    else:
                        st.caption(link["label"] + ": " + link.get("unavailableReason", "reference is not included in this snapshot."))

    def card(task, context):
        with st.container(key=f"mission-state-{task['status']}-{context}"):
            card_content(task, context)

    with priority_slot:
        for direction, heading in DIRECTIONS.items():
            work = [task for task in matching if task["direction"] == direction]
            if not work:
                continue
            st.subheader(heading)
            image_work = [task for task in work if task["workKind"] in {"image_new", "image_repair"}]
            video_work = [task for task in work if task["workKind"] == "video"]
            planning_work = [task for task in work if task["workKind"] == "planning"]

            def task_group(group):
                for task in sorted(group, key=lambda task: task.get("priority") != "top"):
                    card(task, task["id"])

            if image_work or video_work:
                image_column, video_column = st.columns(2)
                with image_column:
                    if image_work:
                        with st.expander(f"Image generation · {len(image_work)}", expanded=bool(focused)):
                            image_groups = [(label, [task for task in image_work if task["workKind"] == kind])
                                            for kind, label in (("image_new", "New"), ("image_repair", "Repairs"))]
                            image_groups = [(label, group) for label, group in image_groups if group]
                            for column, (label, group) in zip(st.columns(len(image_groups)), image_groups):
                                with column:
                                    st.markdown(f"**{label} · {len(group)}**")
                                    task_group(group)
                with video_column:
                    if video_work:
                        with st.expander(f"Video generation · {len(video_work)}", expanded=bool(focused)):
                            task_group(video_work)
            if planning_work:
                with st.columns(2)[0]:
                    with st.expander(f"Writing & planning · {len(planning_work)}", expanded=bool(focused)):
                        task_group(planning_work)
        if not matching:
            st.info("No completed tasks match this filter." if archived else "No tasks match this filter.")
    if archived:
        return
    project = st.session_state.studio_project
    pending = [aid for aid in mission_pending_requests(data, reviews, project)
               if by_id.get(aid, {}).get('kind') not in {'document', 'pdf'}]
    with st.container(key='mission-image-review'):
        review_label, review_action = st.columns([3, 1])
        with review_label:
            st.markdown("**Image review · " + projects.get(project, project) + "**")
            st.caption(f"{len(pending)} images await your decision." if pending else "No image reviews waiting for your decision.")
        if pending:
            review_action.button(f"Review images · {len(pending)}", key="mission-review", width="stretch", on_click=navigate,
                                 args=('Review queue',))
        with st.expander("Prepare review sweep", expanded=False):
            sweep()
    storyboard_requests = mission_storyboard_requests(data, tasks, project)
    if storyboard_requests:
        with st.container(key='mission-storyboard-review'):
            st.markdown('**Storyboard review · '+projects.get(project, project)+'**')
            st.caption(f'{len(storyboard_requests)} writing '+('package awaits' if len(storyboard_requests) == 1 else 'packages await')+' your choices.')
            for request in storyboard_requests:
                st.write(request['title'])
                st.button('Review storyboard', key='mission-storyboard-review:'+request['id'],
                          on_click=open_storyboard_review,
                          args=(project, request['storyID'], request['structure'], navigate))
    st.caption("Task status combines saved handoffs with recorded review decisions. This page does not send requests or monitor collaborator accounts.")
    st.caption("Reviews use this snapshot plus your session choices. Export/import transfers decisions between the hosted studio and the local index.")
    if control.get("updated"):
        st.caption("Handoff updated: " + format_page_updated(control["updated"]))
    snapshot = data.get("snapshot", {})
    if snapshot:
        st.caption("Index snapshot: " + format_page_updated(snapshot.get("generatedAtUTC", snapshot.get("generatedAt"))))
