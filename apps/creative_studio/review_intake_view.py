"""Present frozen handoffs alongside exact-image, independently saved reviews."""
from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlsplit

import streamlit as st

from studio_dependencies import effective_reviews, media_path


REVIEW_LABELS = {"keep": "Keep", "needs_fixes": "Needs fixes", "remove": "Marked for removal"}
DECISION_LABELS = {"pending": "Still to review", "reviewed": "Reviewed", "all": "All families"}
LAYOUT_LABELS = {"evidence": "Detailed evidence", "gallery": "Batch gallery"}
STRUCTURE_LABELS = {"all": "All families", "repairs": "Families with versions",
                    "unavailable": "Unavailable history or originals"}


def intake_families(intake: dict, project: str, dataset: str = "All datasets", query: str = "") -> list[dict]:
    """Keep package/frame identity intact; searching never changes review state."""
    needle = query.strip().casefold()
    return [family for family in intake.get("families", [])
            if family.get("project") == project
            and (dataset == "All datasets" or family.get("dataset") == dataset)
            and (not needle or needle in json.dumps(family, ensure_ascii=False).casefold())]


def family_versions(family: dict, assets: list[dict] | dict[str, dict]) -> list[dict]:
    """An ID alone cannot attach media or a review to a different revision."""
    by_id = assets if isinstance(assets, dict) else {asset["id"]: asset for asset in assets}
    result = []
    for version in family.get("versions", []):
        asset = by_id.get(version.get("assetID"))
        exact = (version.get("availability") == "available" and asset is not None
                 and bool(version.get("sha256")) and asset.get("sha256") == version["sha256"])
        result.append({"version": version, "asset": asset if exact else None})
    return result


def _nominated_versions(items: list[dict], family: dict) -> tuple[dict | None, dict | None]:
    original_sha = (family.get("original") or {}).get("sha256")
    current_sha = (family.get("currentCandidate") or {}).get("sha256")
    original = next((item for item in items if original_sha and item["version"].get("sha256") == original_sha), None)
    if original is None:
        original = next((item for item in items if item["version"].get("role") == "version_only_base"), None)
    current = next((item for item in items if current_sha and item["version"].get("sha256") == current_sha), None)
    return original, current


def intake_review_targets(family: dict, assets: list[dict] | dict[str, dict]) -> list[dict]:
    """Only the exact original/base and nominated current image require decisions.

    History remains inspectable. If neither nominated image is available, the
    first available delivered version is the single fallback review target.
    """
    items = family_versions(family, assets)
    original, current = _nominated_versions(items, family)
    targets = [item["asset"] for item in (original, current) if item and item["asset"]]
    if not targets:
        targets = [item["asset"] for item in items if item["asset"]][:1]
    return list({(asset["id"], asset["sha256"]): asset for asset in targets}.values())


def _decision(asset: dict, reviews: dict) -> dict:
    """Session reviews are prevalidated; reject a conflicting hash if supplied."""
    row = reviews.get(asset["id"], {})
    return row if isinstance(row, dict) and (not row.get("sha256") or row["sha256"] == asset.get("sha256")) else {}


def intake_review_progress(family: dict, assets: list[dict] | dict[str, dict], reviews: dict) -> dict:
    targets = intake_review_targets(family, assets)
    reviewed = [asset for asset in targets if _decision(asset, reviews).get("status") in REVIEW_LABELS]
    pending = [asset for asset in targets if _decision(asset, reviews).get("status") not in REVIEW_LABELS]
    return {"targets": targets, "reviewed": reviewed, "pending": pending,
            "complete": bool(targets) and not pending, "unavailable": not targets}


def intake_review_totals(families: list[dict], assets: list[dict] | dict[str, dict], reviews: dict) -> dict:
    by_id = assets if isinstance(assets, dict) else {asset["id"]: asset for asset in assets}
    progress = [intake_review_progress(family, by_id, reviews) for family in families]
    targets = {(asset["id"], asset["sha256"]): asset for row in progress for asset in row["targets"]}
    done = sum(_decision(asset, reviews).get("status") in REVIEW_LABELS for asset in targets.values())
    return {"total": len(targets), "done": done, "remaining": len(targets) - done,
            "familiesPending": sum(bool(row["pending"]) for row in progress),
            "familiesReviewed": sum(row["complete"] for row in progress),
            "unavailable": sum(row["unavailable"] for row in progress)}


def intake_batch_key(family: dict) -> str:
    return str(family.get("dataset", "")) + "::" + str(family.get("category") or "")


def intake_rows(intake: dict, project: str, assets: list[dict] | dict[str, dict], reviews: dict,
                dataset: str = "All datasets", query: str = "", batch: str = "all", structure: str = "all",
                decision: str = "pending", focused: str = "") -> tuple[list[dict], dict]:
    """Progress covers the chosen batch/search before the decision filter."""
    by_id = assets if isinstance(assets, dict) else {asset["id"]: asset for asset in assets}
    if focused:
        rows = [family for family in intake.get("families", [])
                if family.get("project") == project and family.get("id") == focused]
    else:
        rows = [family for family in intake_families(intake, project, dataset, query)
                if batch == "all" or intake_batch_key(family) == batch]
        if structure == "repairs":
            rows = [family for family in rows if len(family.get("versions", [])) > 1]
        elif structure == "unavailable":
            rows = [family for family in rows if any(version.get("availability") != "available"
                                                    for version in family.get("versions", []))]
    totals = intake_review_totals(rows, by_id, reviews)
    if not focused and decision != "all":
        key = "complete" if decision == "reviewed" else "pending"
        rows = [family for family in rows if intake_review_progress(family, by_id, reviews)[key]]
    return rows, totals


def gallery_versions(family: dict, assets: list[dict] | dict[str, dict], reviews: dict,
                     decision: str = "pending") -> tuple[dict | None, list[dict]]:
    unique = {}
    for item in family_versions(family, assets):
        version = item["version"]
        unique.setdefault(version.get("sha256") or version.get("assetID") or version.get("filename"), item)
    items = list(unique.values())
    original, _ = _nominated_versions(items, family)
    pending = intake_review_progress(family, assets, reviews)["pending"] if decision == "pending" else []
    cover = next((item for item in items if pending and item["asset"]
                  and (item["asset"]["id"], item["asset"]["sha256"]) == (pending[0]["id"], pending[0]["sha256"])), None)
    cover = cover or (original if original and original["asset"] else None) or next(
        (item for item in items if item["asset"]), None) or original or next(iter(items), None)
    return cover, [item for item in items if item is not cover]


def family_for_asset(intake: dict, asset: dict) -> list[dict]:
    metadata = intake.get("assetMetadata", {}).get(asset["id"], {})
    if not asset.get("sha256") or metadata.get("sha256") != asset["sha256"]:
        return []
    ids = set(metadata.get("familyIDs", []))
    return [family for family in intake.get("families", []) if family.get("id") in ids]


def duplicate_evidence(intake: dict, family: dict) -> list[dict]:
    group = family.get("providerReview", {}).get("duplicateGroup")
    return [record for record in intake.get("duplicateGroups", [])
            if group and record.get("id") == group and record.get("dataset") == family.get("dataset")]


def _provider_review(review: dict) -> None:
    labels = {"stage": "Provider review stage", "qaGrade": "Provider QA grade", "verdict": "Scoped verdict",
              "scope": "Review scope", "validationLabel": "Validation label", "technicalValidation": "Technical check",
              "qaScoreSuggestion": "Provider score suggestion", "qaBasis": "Score basis",
              "likenessSelfScore": "Provider likeness self-score", "sceneSelfScore": "Provider scene self-score",
              "chestClass": "Chest classification", "classSuggestion": "Class suggestion",
              "multiverseSuggestion": "Multiverse suggestion", "duplicateGroup": "Duplicate group",
              "duplicateRole": "Duplicate role", "duplicateKeeperSuggestion": "Suggested duplicate keeper",
              "reason": "QA reason", "remainingDefects": "Remaining defects", "staleReason": "Stale verdict reason",
              "humanQuestion": "Question for Ziggy", "notes": "Provider notes", "openItemsOwner": "Open items owner"}
    for key, label in labels.items():
        value = review.get(key)
        if value is not None and value != "":
            st.markdown(f"**{label}**")
            st.text(value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, indent=2))
    for key, label in (("components", "Component checks"), ("pending", "Pending work"),
                       ("referenceIDs", "Checked reference IDs"), ("ruleVersions", "Rule versions"),
                       ("scopedChecks", "Scoped checks"), ("checks", "Reviewers & check records")):
        if review.get(key):
            st.markdown("**" + label + "**")
            st.json(review[key], expanded=False)


def _version_preview(item: dict | None, label: str, library_dir: Path, open_asset, key: str,
                     reviews: dict | None = None) -> None:
    st.markdown(f"**{label}**")
    if item is None:
        st.caption("No available version nominated in this handoff.")
        return
    version, asset = item["version"], item["asset"]
    if asset:
        source = media_path(library_dir, asset.get("src"))
        preview = media_path(library_dir, asset.get("thumb"))
        if asset.get("kind") == "video" and source:
            st.video(str(source))
        elif preview or (source and asset.get("kind") == "image"):
            st.image(str(preview or source), width="stretch")
        else:
            st.info("This version is recorded but its review copy is not packaged here.")
        if reviews is not None:
            st.caption("Your decision: " + REVIEW_LABELS.get(_decision(asset, reviews).get("status"), "Not reviewed"))
        st.button("Open review", key=key, on_click=open_asset, args=(asset["id"], asset.get("project")), width="stretch")
    else:
        st.info("Media unavailable · " + str(version.get("availability", "unknown")).replace("_", " "))
    st.caption(version.get("filename", ""))
    if version.get("providerReview", {}).get("stage"):
        st.caption("Provider: " + str(version["providerReview"]["stage"]))


def _progress_caption(family: dict, assets: list[dict] | dict[str, dict], reviews: dict) -> None:
    progress = intake_review_progress(family, assets, reviews)
    st.caption("Waiting for a full image" if progress["unavailable"] else
               f"{len(progress['reviewed'])} of {len(progress['targets'])} review targets decided")


def _family(family: dict, assets: list[dict] | dict[str, dict], library_dir: Path, open_asset,
            intake: dict, reviews: dict) -> None:
    key = family["id"]
    items = family_versions(family, assets)
    current_sha = (family.get("currentCandidate") or {}).get("sha256")
    original, current = _nominated_versions(items, family)
    source_label = "Delivered base" if original and original["version"].get("role") == "version_only_base" else "Original"
    with st.container(border=True):
        st.subheader(family.get("frameID", key))
        st.caption(" · ".join(str(family.get(field, "")) for field in ("dataset", "category")))
        _progress_caption(family, assets, reviews)
        if original and current_sha == original["version"].get("sha256"):
            _version_preview(original, source_label + " · provider current candidate", library_dir, open_asset, "intake-open:" + key, reviews)
        else:
            left, right = st.columns(2)
            with left:
                _version_preview(original, source_label, library_dir, open_asset, "intake-original:" + key, reviews)
            with right:
                _version_preview(current, "Provider current candidate", library_dir, open_asset, "intake-current:" + key, reviews)
        with st.expander("Provider QA & open questions"):
            st.caption("Provider checks and suggestions retain their scope. They do not set Keep, character scores, Prime/Multiverse choices or human approval.")
            _provider_review(family.get("providerReview", {}))
            if groups := duplicate_evidence(intake, family):
                st.markdown("**Duplicate evidence & keeper suggestions**")
                st.json(groups, expanded=False)
            if current:
                st.markdown("**Current candidate checks**")
                _provider_review(current["version"].get("providerReview", {}))
            if family.get("providerFinalPointer") and not family.get("currentCandidate"):
                st.caption("The provider's final pointer is preserved for investigation; it is not presented as a current passed candidate.")
                st.json(family["providerFinalPointer"], expanded=False)
        with st.expander(f"Version history & paths · {len(items)}"):
            st.caption("Originals, repairs and earlier versions remain one family even when their files live in different drops. Missing history is listed without a broken preview.")
            for item in items:
                version = item["version"]
                st.markdown("**" + str(version.get("filename") or version.get("role", "Version")) + "**")
                st.caption(str(version.get("role", "")) + " · " + str(version.get("availability", "unknown")).replace("_", " "))
                st.text("SHA-256: " + str(version.get("sha256") or "Not recorded"))
                st.text("Source: " + str(version.get("repoPath") or "Not delivered locally"))
                if version.get("lineage"):
                    st.json({"lineage": version["lineage"], "providerReview": version.get("providerReview", {})}, expanded=False)
            choices = [item for item in items if item["asset"]]
            if len(choices) > 1 and st.checkbox("Compare available versions", key="intake-compare:" + key):
                left, right = st.columns(2)
                options = list(range(len(choices)))
                label = lambda i: choices[i]["version"]["filename"] + " · " + choices[i]["version"]["sha256"][:10]
                with left:
                    chosen = st.selectbox("Left version", options, format_func=label, key="intake-left:" + key)
                    _version_preview(choices[chosen], "Left", library_dir, open_asset, "intake-left-open:" + key, reviews)
                with right:
                    chosen = st.selectbox("Right version", options, index=len(options) - 1, format_func=label, key="intake-right:" + key)
                    _version_preview(choices[chosen], "Right", library_dir, open_asset, "intake-right-open:" + key, reviews)
            if family.get("evidence"):
                st.markdown("**Manifest-verified evidence records**")
                st.json(family["evidence"], expanded=False)


def render_asset_evidence(intake: dict, asset: dict) -> None:
    families = family_for_asset(intake, asset)
    if not families:
        return
    with st.expander("Provider handoff evidence"):
        st.caption("This evidence belongs to the exact source hash. Provider QA remains separate from your review choices and the site's validation records.")
        for family in families:
            st.markdown("**" + family["dataset"] + " · " + family["frameID"] + "**")
            _provider_review(family.get("providerReview", {}))
            if groups := duplicate_evidence(intake, family):
                st.markdown("**Duplicate evidence & keeper suggestions**")
                st.json(groups, expanded=False)
            version = next((v for v in family.get("versions", []) if v.get("sha256") == asset.get("sha256")), None)
            if version:
                st.markdown("**This version**")
                st.json({key: version.get(key) for key in ("sha256", "role", "availability", "repoPath", "lineage", "providerReview", "evidence")}, expanded=False)
            st.caption("Use Intake verification to compare this family's original and repairs.")


def _focus_family(project: str, family_id: str) -> None:
    # Streamlit removes widget state when focused evidence hides those widgets.
    # Keep the prior browse controls separately so Back returns to the same batch.
    keys = [f"intake-{name}:{project}" for name in ("layout", "decision", "dataset", "query", "batch", "structure")]
    keys.extend(key for key in st.session_state if key.startswith(f"intake-page:{project}:"))
    st.session_state["intake-browse-state:" + project] = {key: st.session_state[key] for key in keys if key in st.session_state}
    st.session_state["intake-focus:" + project] = family_id
    st.session_state["intake-layout:" + project] = "evidence"


def _leave_family(project: str) -> None:
    st.session_state["intake-focus:" + project] = ""
    for key, value in st.session_state.pop("intake-browse-state:" + project, {}).items():
        st.session_state[key] = value


def _change_layout(project: str) -> None:
    if st.session_state.get("intake-layout:" + project) == "gallery":
        _leave_family(project)
        st.session_state["intake-layout:" + project] = "gallery"


def _gallery_family(family: dict, assets: dict[str, dict], library_dir: Path, open_asset,
                    reviews: dict, decision: str, project: str) -> None:
    cover, related = gallery_versions(family, assets, reviews, decision)
    original, current = _nominated_versions([cover, *related] if cover else related, family)
    label = "Original / delivered base" if cover is original else (
        "Provider current candidate" if cover is current else "Available delivered version")
    with st.container(border=True):
        st.subheader(family.get("frameID", family["id"]))
        _progress_caption(family, assets, reviews)
        _version_preview(cover, label, library_dir, open_asset, "intake-gallery:" + family["id"], reviews)
        if related:
            with st.expander(f"Related versions · {len(related)}"):
                for index, item in enumerate(related):
                    _version_preview(item, str(item["version"].get("role", "Recorded version")).replace("_", " "),
                                     library_dir, open_asset, f"intake-related:{family['id']}:{index}", reviews)
        st.button("View family evidence", key="intake-detail:" + family["id"], on_click=_focus_family,
                  args=(project, family["id"]), width="stretch")


def _source_link(label: str, value: str | None, library_dir: Path, key: str) -> None:
    """Hosted pages expose only packaged downloads or explicit HTTP(S) links."""
    if not value:
        return
    if source := media_path(library_dir, value):
        st.download_button(label, source.read_bytes(), file_name=source.name, key=key, width="stretch")
    elif urlsplit(value).scheme in {"http", "https"}:
        st.link_button(label, value, width="stretch")
    else:
        st.caption(label + " · source file not packaged for this site")


def _supplements(data: dict, project: str, query: str, assets: dict[str, dict], reviews: dict,
                 library_dir: Path, open_asset) -> None:
    groups = {"approved": "Golden references", "validated": "V-Team scoped passes", "preliminary": "Preliminary mouth picks"}
    for index, supplement in enumerate(data.get("reviewSupplements") or []):
        project_items = [item for item in supplement.get("items", []) if item.get("project") == project]
        if not project_items:
            continue
        needle = query.strip().casefold()
        items = [item for item in project_items if not needle or needle in
                 " ".join(str(item.get(field) or "") for field in ("title", "version", "sha256", "label", "notes")).casefold()]
        prefix = f"intake-supplement:{project}:{index}"
        with st.expander(f"{supplement.get('title', 'Winners supplement')} · {len(items)} entries", expanded=False):
            st.caption("Later delivery · separate from the frozen intake. Your saved choices remain separate from scoped team findings.")
            _source_link("Supplied winners index", supplement.get("indexURL") or supplement.get("sourceURL"), library_dir, prefix + ":index")
            with st.expander("Source details · optional"):
                delivery = supplement.get("mediaDelivery") or {}
                st.write(f"{delivery['fullImages']} full images received and file-verified." if delivery.get("fullImages") is not None
                         else "The delivery lists selected references and their source records.")
                st.caption("These files document the delivery; they are not a review checklist.")
                _source_link("Download source manifest", supplement.get("csvURL"), library_dir, prefix + ":manifest")
                _source_link("Original delivery receipt", supplement.get("receiptURL"), library_dir, prefix + ":receipt")
            for group, title in groups.items():
                rows = [item for item in items if item.get("group") == group]
                if not rows:
                    continue
                with st.expander(f"{title} · {len(rows)}"):
                    if group == "preliminary":
                        st.caption("Preliminary team picks; V-Team has not validated them.")
                    for start in range(0, len(rows), 3):
                        columns = st.columns(3)
                        for column, item in zip(columns, rows[start:start + 3]):
                            with column, st.container(border=True):
                                item_key = prefix + ":" + str(item.get("id", start))
                                asset = assets.get(item.get("exactAssetID"))
                                reviewable = (item.get("availability") == "local_original_verified" and asset is not None
                                              and bool(item.get("sha256")) and asset.get("sha256") == item["sha256"]
                                              and asset.get("kind") == "image")
                                st.write(item.get("title", "Delivered reference"))
                                if reviewable:
                                    _version_preview({"version": {"filename": item.get("version", "")}, "asset": asset},
                                                     "Exact image", library_dir, open_asset, item_key + ":open", reviews)
                                else:
                                    preview = media_path(library_dir, item.get("thumbURL"))
                                    if preview:
                                        st.image(str(preview), width="stretch")
                                    st.caption("Preview only · no exact full image available for review here.")
                                st.caption(" · ".join(str(item.get(field)) for field in ("label", "vVerdict", "reviewScope") if item.get(field)))
                                if item.get("advisories"):
                                    st.write("Advisory: " + str(item["advisories"]))
                                with st.expander("Source and version evidence"):
                                    st.json({key: item.get(key) for key in ("sha256", "version", "reviewScope", "sourceEvidence", "notes",
                                             "goldReferences", "humanAcceptance", "lineage", "referenceLinks", "sourceLinks")}, expanded=False)
                                    for section in ("referenceLinks", "sourceLinks", "reportLinks"):
                                        for link_index, link in enumerate(item.get(section) or []):
                                            _source_link(link.get("label", "Source record"), link.get("url"), library_dir,
                                                         f"{item_key}:{section}:{link_index}")
                                for family_id in item.get("familyIDs", []):
                                    if any(f.get("id") == family_id and f.get("project") == project
                                           for f in (data.get("reviewIntake") or {}).get("families", [])):
                                        st.button("Earlier family · " + family_id.split(":", 1)[-1], key=item_key + ":" + family_id,
                                                  on_click=_focus_family, args=(project, family_id))
            if not items:
                st.info("No supplement entries match this search.")


def render_intake(data: dict, project: str, library_dir: Path, open_asset, *, reviews: dict | None = None) -> None:
    intake = data.get("reviewIntake") or {}
    st.title("Intake verification")
    st.write("Review the frozen handoff by image family. Originals, current provider candidates and earlier repairs stay together.")
    if not intake.get("families"):
        st.info("No frozen handoff is included in this publication yet.")
        return
    assets = {asset["id"]: asset for asset in data.get("assets", [])}
    if reviews is None:
        reviews = effective_reviews(data.get("assets", []), data.get("reviewDecisions", []), {}, aliases=data.get("assetAliases", []))
    families = intake_families(intake, project)
    focus_key = "intake-focus:" + project
    focused = st.session_state.get(focus_key, "")
    if focused and not any(family.get("id") == focused for family in families):
        focused = st.session_state[focus_key] = ""
    layout_key = "intake-layout:" + project
    if layout_key not in st.session_state:
        st.session_state[layout_key] = 'gallery'
    if focused:
        st.session_state[layout_key] = "evidence"
    layout = st.selectbox("View", list(LAYOUT_LABELS), format_func=LAYOUT_LABELS.get, key=layout_key,
                          on_change=_change_layout, args=(project,))
    datasets = sorted({family["dataset"] for family in families})
    decision, dataset, query, batch, structure = "pending", "All datasets", "", "all", "all"
    if focused:
        st.button("Back to intake families", on_click=_leave_family, args=(project,), key="intake-back:" + project)
    else:
        left, middle, right = st.columns(3)
        with left:
            decision = st.selectbox("Review", list(DECISION_LABELS), format_func=DECISION_LABELS.get, key="intake-decision:" + project)
        with middle:
            dataset = st.selectbox("Dataset", ["All datasets", *datasets], key="intake-dataset:" + project)
        with right:
            structure = st.selectbox("Show", list(STRUCTURE_LABELS), format_func=STRUCTURE_LABELS.get, key="intake-structure:" + project)
        query = st.text_input("Find a frame, category, filename or QA note", key="intake-query:" + project)
        batch_rows = intake_families(intake, project, dataset)
        batches = {}
        for family in batch_rows:
            entry = batches.setdefault(intake_batch_key(family), {"family": family, "count": 0})
            entry["count"] += 1
        batch_key = "intake-batch:" + project
        if st.session_state.get(batch_key, "all") not in {"all", *batches}:
            st.session_state[batch_key] = "all"
        with st.expander(f"Batch / run · {len(batches)} available"):
            batch = st.selectbox("Batch / run", ["all", *batches], key=batch_key,
                                  format_func=lambda key: "All batches" if key == "all" else
                                  f"{batches[key]['family'].get('category') or 'Unlabeled batch'} · {batches[key]['family']['dataset']} · {batches[key]['count']}")
        _supplements(data, project, query, assets, reviews, library_dir, open_asset)
    matched, progress = intake_rows(intake, project, assets, reviews, dataset, query, batch, structure, decision, focused)
    metrics = st.columns(4)
    metrics[0].metric("Images left", progress["remaining"])
    metrics[1].metric("Reviewed images", progress["done"])
    metrics[2].metric("Families still to review", progress["familiesPending"])
    metrics[3].metric("Families awaiting files", progress["unavailable"])
    st.caption("Keep, Needs fixes or Mark for removal completes this pass for that image. Notes and ratings are optional. "
               "Each original and nominated current version has its own decision; earlier attempts stay in the evidence.")
    # The selected-image view does not rerun this renderer. Preserve this list
    # while triage removes families from Still to review behind that view.
    st.session_state["studio_intake_sequence"] = []
    if not matched:
        st.info("No families match these filters. Choose All families to revisit saved decisions or unavailable files.")
    else:
        page_size = 36 if layout == "gallery" else 12
        page_count = max(1, (len(matched) + page_size - 1) // page_size)
        page_key = f"intake-page:{project}:{dataset}:{query}:{batch}:{structure}:{decision}:{layout}:{focused}"
        if page_key in st.session_state:
            st.session_state[page_key] = max(1, min(int(st.session_state[page_key]), page_count))
        page = int(st.number_input("Page", min_value=1, max_value=page_count, value=1, key=page_key))
        st.caption(f"Showing {(page - 1) * page_size + 1}–{min(page * page_size, len(matched))} of {len(matched)} families · {page_count} pages")
        rows = matched[(page - 1) * page_size:page * page_size]
        sequence = []
        for family in rows:
            if layout == "gallery":
                cover, _ = gallery_versions(family, assets, reviews, decision)
                sequence.extend([cover["asset"]["id"]] if cover and cover["asset"] else [])
            else:
                sequence.extend(asset["id"] for asset in intake_review_targets(family, assets))
        st.session_state["studio_intake_sequence"] = list(dict.fromkeys(sequence))
        if layout == "gallery":
            groups = {}
            for family in rows:
                groups.setdefault(intake_batch_key(family), []).append(family)
            for group in groups.values():
                st.subheader(group[0].get("category") or "Unlabeled batch")
                st.caption(group[0]["dataset"])
                for start in range(0, len(group), 3):
                    columns = st.columns(3)
                    for column, family in zip(columns, group[start:start + 3]):
                        with column:
                            _gallery_family(family, assets, library_dir, open_asset, reviews, decision, project)
        else:
            for family in rows:
                _family(family, assets, library_dir, open_asset, intake, reviews)
    with st.expander("Handoff coverage and receipts · optional", expanded=False):
        st.caption("Provider QA remains separate from your choices. Both views use the same images and saved reviews.")
        st.caption(str(intake.get("id", "Frozen intake")) + " · " + str(len(intake.get("packages", []))) + " verified package manifests")
        st.caption("Unavailable versions stay linked here. Nothing is inferred from a matching filename.")
        st.json({key: intake.get(key) for key in ("id", "schemaVersion", "receipt", "sourceIndex", "packages", "summary")}, expanded=False)
