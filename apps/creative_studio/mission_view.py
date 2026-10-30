"""Compact Ziggy's Corner, using the index's prepared task and review records."""
from pathlib import Path
from datetime import date, datetime, timezone
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import streamlit as st

from studio_dependencies import destination_label, output_kind_label, media_path, mission_pending_requests, mission_storyboard_requests, mission_task_progress, mission_tasks, mission_visible

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
        st.button("← Back to Ziggy’s Corner", on_click=close_collection, key="corner-selected-back")
        render_selected(selected)
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
    tasks = sorted((mission_task_progress(t, data["assets"], reviews) for t in mission_tasks(control)
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
        with st.expander(f":{color}-badge[{task.get('statusLabel', label)}] **{task['title']}** · {project}", expanded=False):
            st.caption(task["provider"] + " · " + DIRECTIONS[task["direction"]] + " · " + WORK_KINDS[task["workKind"]])
            st.write(task["summary"])
            if task["nextAction"]:
                st.markdown("**Next**")
                st.write(task["nextAction"])
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
                        with st.expander(f"Image generation · {len(image_work)}", expanded=False):
                            image_groups = [(label, [task for task in image_work if task["workKind"] == kind])
                                            for kind, label in (("image_new", "New"), ("image_repair", "Repairs"))]
                            image_groups = [(label, group) for label, group in image_groups if group]
                            for column, (label, group) in zip(st.columns(len(image_groups)), image_groups):
                                with column:
                                    st.markdown(f"**{label} · {len(group)}**")
                                    task_group(group)
                with video_column:
                    if video_work:
                        with st.expander(f"Video generation · {len(video_work)}", expanded=False):
                            task_group(video_work)
            if planning_work:
                with st.columns(2)[0]:
                    with st.expander(f"Writing & planning · {len(planning_work)}", expanded=False):
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
