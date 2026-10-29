"""Compact Ziggy's Corner, using the index's prepared task and review records."""
from pathlib import Path

import streamlit as st

from studio_dependencies import media_path, mission_pending_requests, mission_task_progress, mission_tasks, mission_visible

STATES = {"ready": ("Ready to send", "green"), "needs_input": ("Needs your input", "orange"),
          "in_progress": ("In progress", "blue"), "planned": ("Planned", "gray"), "done": ("Done", "green")}
RANK = {"ready": 0, "needs_input": 1, "in_progress": 2, "planned": 3, "done": 4}


def show_collection(ids, label, mode="references", project=None):
    st.session_state.studio_mission_collection = {"ids": ids, "label": label, "mode": mode, "project": project}
    st.session_state.studio_mission_selected = None
    st.session_state.pop("corner-collection-page", None)


def close_collection():
    st.session_state.pop("studio_mission_collection", None)
    st.session_state.pop("studio_mission_selected", None)


def render_corner(data, library_dir: Path, open_reference, render_selected, document_download, navigate, sweep, review_data=None):
    reviews = st.session_state.studio_reviews
    by_id = {a["id"]: a for a in data["assets"]}
    review_by_id = {a["id"]: a for a in (review_data or data)["assets"]}
    plans = [a for aid, a in review_by_id.items() if reviews.get(aid, {}).get("shotPlan") and mission_visible(a, reviews)]
    projects = {p["id"]: p["name"] for p in data["projects"]}
    if selected := review_by_id.get(st.session_state.get("studio_mission_selected")):
        st.button("← Back to Ziggy’s Corner", on_click=close_collection, key="corner-selected-back")
        render_selected(selected)
        return
    if collection := st.session_state.get("studio_mission_collection"):
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
            for offset in range(page * 24, min((page + 1) * 24, len(items)), 3):
                for col, asset in zip(st.columns(3), items[offset:offset + 3]):
                    with col:
                        picture = media_path(library_dir, asset.get("thumb") or asset.get("src"))
                        if picture and asset.get("kind") == "image":
                            st.image(str(picture), width="stretch")
                        if is_plans:
                            plan = reviews[asset["id"]]["shotPlan"]
                            st.caption(projects.get(asset.get("project"), "Across projects") + " · " + ", ".join(plan.get("destinations", ["undecided"])))
                            if plan.get("idea"):
                                st.write(plan["idea"])
                            if plan.get("prompt"):
                                with st.expander("Prompt", expanded=False):
                                    st.text(plan["prompt"])
                        st.button(asset.get("title", asset["id"]), key="corner-collection:" + asset["id"], on_click=open_reference, args=(asset,))
        return

    control = data.get("missionControl", {})
    tasks = sorted((mission_task_progress(t, data["assets"], reviews) for t in mission_tasks(control)), key=lambda t: RANK[t["status"]])
    columns = st.columns(4)
    counts = [(STATES[s][0], sum(t["status"] == s for t in tasks)) for s in ("ready", "needs_input", "in_progress")]
    for col, (label, number) in zip(columns, counts):
        col.metric(label, number)
    columns[3].button(f"Shot plans · {len(plans)} →", key="mission-shot-plans", width="stretch",
                      on_click=show_collection, args=([], "All shot plans", "shot_plans"))
    priority_slot = st.container(key="mission-priority")
    filter_col, search_col = st.columns([1, 2])
    with filter_col:
        provider = st.selectbox("Collaborator", ["all", *dict.fromkeys(t["provider"] for t in tasks)],
                                format_func=lambda s: "All collaborators" if s == "all" else s, key="mission-provider")
    with search_col:
        query = st.text_input("Find a task", key="mission-search").casefold().strip()
    matching = [t for t in tasks if (provider == "all" or t["provider"] == provider) and
                query in " ".join(str(t.get(k, "")) for k in ("title", "provider", "project", "summary", "nextAction")).casefold()]
    priority = [t for t in matching if t.get("priority") == "top" and t["status"] != "done"]
    regular = [t for t in matching if t not in priority]

    def references(ids, context, history=False):
        for i, aid in enumerate(dict.fromkeys(ids)):
            asset = by_id.get(aid)
            if asset and (history or mission_visible(asset, reviews)):
                st.button(asset.get("title", aid), key=f"corner-reference:{context}:{i}", on_click=open_reference, args=(asset,))

    def card_content(task, context):
        label, color = STATES[task["status"]]
        project = projects.get(task["project"], "Across projects")
        with st.expander(f":{color}-badge[{task.get('statusLabel', label)}] **{task['title']}** · {project}", expanded=False):
            st.caption(task["provider"])
            st.write(task["summary"])
            if task["nextAction"]:
                st.markdown("**Next**")
                st.write(task["nextAction"])
            for field, heading in (("enablers", "Before sending"), ("deliverables", "Deliverables"), ("missing", task.get("missingLabel", "Other open items"))):
                if task.get(field):
                    st.markdown(f"**{heading}**")
                    for value in task[field]:
                        (st.warning if field == "enablers" else st.write)(value)
            if task.get("laterReview"):
                st.markdown("**Your later review**")
                st.write(task["laterReview"])
            if task.get("previewAssetIDs"):
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
        with st.expander(f"Top priority · {len(priority)} items", expanded=False):
            for task in priority:
                card(task, task["id"])
            if not priority:
                st.caption("No top-priority reviews waiting." if not query else "No top-priority items match this search.")
    project = st.session_state.studio_project
    pending = mission_pending_requests(data, reviews, project)
    review_label, review_action = st.columns([3, 1])
    with review_label:
        st.markdown("**Image review · " + projects.get(project, project) + "**")
        st.caption(f"{len(pending)} images await your decision." if pending else "No image reviews waiting for your decision.")
    if pending:
        review_action.button(f"Review images · {len(pending)}", key="mission-review", width="stretch", on_click=show_collection,
                             args=(pending, "Unanswered review requests", "review_requests", project))
    with st.expander("Prepare review sweep", expanded=False):
        sweep()
    st.subheader("Collaborator handoffs")
    providers = list(dict.fromkeys(t["provider"] for t in regular))
    columns = st.columns(2)
    for index, name in enumerate(providers):
        with columns[index % 2]:
            st.subheader(name)
            work = [t for t in regular if t["provider"] == name]
            st.caption(f"{len(work)} prepared tasks")
            for task in work:
                card(task, task["id"])
    if not matching:
        st.info("No tasks match this filter.")
    st.caption("Task status combines saved handoffs with recorded review decisions. This page does not send requests or monitor collaborator accounts.")
    if control.get("updated"):
        st.caption(f"Handoff updated: {control['updated']}")
    snapshot = data.get("snapshot", {})
    if snapshot:
        st.caption("Index snapshot: " + str(snapshot.get("generatedAtUTC", snapshot.get("generatedAt", "prepared"))))
    st.caption("Reviews use this snapshot plus your session choices. Export/import transfers decisions between the hosted studio and the local index.")
