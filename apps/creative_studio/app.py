"""CFA's portable visual review room. Run from the repository root with Streamlit."""

from __future__ import annotations

import html
import json
import mimetypes
import sys
from pathlib import Path

import streamlit as st

APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))
from library_helpers import (
    DESTINATIONS, EXPORT_FORMAT, MISSION_PROVIDERS, STORYBOARD_STAGES, VISUAL_KINDS, basket_payload, basket_zip,
    collaborator_sections, document_tree, effective_reviews, export_allowed, handoff_payload, handoff_text,
    layout_video_assets, media_path, mission_tasks, mission_review_data, normalize_plan, ordered_assets, production_workflows,
    read_basket, read_review, review_payload, storyboard_stage, storyboard_themes, storyboard_window, sweep_payload,
)

LIBRARY_DIR = APP_DIR / "library"
PAGE_SIZE = 24
CORNER = "Ziggy’s Corner"
VIEWS = (CORNER, "Library", "Storyboard", "Collaborators", "Collaborator briefs", "Review queue", "Shot plans", "Export basket", "Favorites & notes", "Documents")
STATUS_LABELS = {None: "Unmarked", "keep": "Keep", "needs_fixes": "Needs fixes", "remove": "Marked for removal"}

st.set_page_config(page_title="Creative Studio | CFA", page_icon="🎬", layout="wide", initial_sidebar_state="auto")


def apply_theme() -> None:
    st.markdown("""<style>
    :root {--studio-ink:#243936;--studio-accent:#176b62;--studio-line:#d7ddd4;}
    .stApp {background:#fbfaf7;color:var(--studio-ink);}
    .block-container {padding-top:2rem;max-width:1500px;padding-bottom:4rem;}
    h1,h2,h3 {font-family:Georgia,'Times New Roman',serif!important;color:var(--studio-ink);}
    h1 {letter-spacing:-.04em;line-height:1.06!important;}
    [data-testid="stSidebar"] {background:#101a18;border-right:1px solid #38504a;}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] label,[data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3 {color:#e8efea!important;}
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {color:#a6bdb3!important;}
    [data-testid="stSidebarCollapseButton"] span {color:#e8efea!important;}
    [data-testid="stSidebar"] button[kind="secondary"] {background:#213532;color:#e8efea;border-color:#38504a;text-align:left;}
    [data-testid="stSidebar"] button[kind="primary"] {background:#2a9d8f;border-color:#2a9d8f;color:white;}
    [data-testid="stSidebar"] .stButton button {justify-content:flex-start;}
    .studio-hero {padding:1.75rem 2rem;background:#173b3b;border-radius:18px;margin:0 0 1.7rem;color:#fbfaf3;}
    .studio-hero .eyebrow {font-size:.75rem;letter-spacing:.16em;text-transform:uppercase;color:#a7d8cb;margin-bottom:.7rem;}
    .studio-hero h1 {color:#fbfaf3!important;margin:0!important;padding:0!important;font-size:clamp(2rem,5vw,3.7rem)!important;}
    .studio-hero p {margin:.65rem 0 0;color:#d4e5dd;max-width:760px;line-height:1.5;}
    .studio-label {font-size:.74rem;text-transform:uppercase;letter-spacing:.11em;color:#176b62;margin:.7rem 0 .3rem;}
    [data-testid="stImage"] img {border-radius:10px;}
    [data-testid="stVerticalBlockBorderWrapper"]>div {border-color:#d7ddd4!important;border-radius:12px;}
    .stButton button,.stDownloadButton button {border-radius:8px;}
    @media(max-width:760px) {.block-container{padding:4.5rem .8rem 3rem;} .studio-hero{padding:1.35rem;} }
    </style>""", unsafe_allow_html=True)


@st.cache_data(show_spinner=False)
def load_catalog(path: str, modified: int) -> dict:
    del modified  # Changes to the packaged catalog invalidate the cache.
    data = json.loads(Path(path).read_text(encoding="utf-8-sig"))
    if not all(isinstance(data.get(key), list) for key in ("projects", "assets", "albums", "categories")):
        raise ValueError("The library catalog is missing its project or collection lists.")
    return data


def init_state() -> None:
    for key, default in (("studio_view", CORNER), ("studio_selected", None),
                         ("studio_favorites", set()), ("studio_notes", {}), ("studio_pages", {}),
                         ("studio_review_overrides", {}), ("studio_reviews", {}), ("studio_basket", set())):
        if key not in st.session_state:
            st.session_state[key] = default
    if st.session_state.studio_view == "Collaborator kits":
        st.session_state.studio_view = "Collaborator briefs"


def navigate(view: str) -> None:
    if st.session_state.studio_view not in (CORNER, "Collaborators"):
        st.session_state.studio_return_view = st.session_state.studio_view
    st.session_state.studio_view = view
    st.session_state.studio_selected = None
    st.session_state.pop("studio_mission_selected", None)
    st.session_state.pop("studio_mission_collection", None)


def back_to_library() -> None:
    view = st.session_state.get("studio_return_view", "Library")
    navigate(view if view in ("Library", "Storyboard", "Documents", "Review queue", "Shot plans", "Export basket", "Favorites & notes") else "Library")


def clear_selection() -> None:
    st.session_state.studio_selected = None
    st.session_state.pop("studio_mission_selected", None)


def clear_project_selection() -> None:
    clear_selection()
    st.session_state.pop("studio_mission_collection", None)


def select_asset(asset_id: str, project: str | None = None) -> None:
    if project is not None:
        st.session_state.studio_project = project
    st.session_state.studio_selected = asset_id


def toggle_favorite(asset_id: str) -> None:
    favorites = set(st.session_state.studio_favorites)
    favorites.remove(asset_id) if asset_id in favorites else favorites.add(asset_id)
    st.session_state.studio_favorites = favorites


def toggle_basket(asset_id: str) -> None:
    basket = set(st.session_state.studio_basket)
    basket.remove(asset_id) if asset_id in basket else basket.add(asset_id)
    st.session_state.studio_basket = basket
    st.session_state.pop("studio_basket_zip", None)


def clear_basket() -> None:
    st.session_state.studio_basket = set()
    st.session_state.pop("studio_basket_zip", None)


def basket_button(asset: dict, context: str = "card") -> None:
    selected = asset["id"] in st.session_state.studio_basket
    st.button("✓ In export basket" if selected else "⇩ Add to export basket", key=f"basket:{context}:{asset['id']}",
              help="Select this reference for export without changing your favorites or review decision.",
              on_click=toggle_basket, args=(asset["id"],), width="stretch", disabled=bool(asset.get("archived")))


def save_note(asset_id: str, key: str) -> None:
    st.session_state.studio_notes[asset_id] = st.session_state[key]
    set_review_field(asset_id, "note", st.session_state[key])


def set_review_field(asset_id: str, field: str, value) -> None:
    st.session_state.studio_review_overrides.setdefault(asset_id, {})[field] = value
    st.session_state.pop("studio_basket_zip", None)


def set_variant(asset_id: str, variant: str) -> None:
    set_review_field(asset_id, "variant", variant)
    set_review_field(asset_id, "variantSource", "user")
    if variant == "multiverse":
        set_review_field(asset_id, "workingReference", None)


def request_working_reference(asset_id: str, scope_key: str) -> None:
    set_review_field(asset_id, "workingReference", {"status": "requested", "scope": st.session_state[scope_key]})


def save_storyboard_stage(asset_id: str, key: str) -> None:
    set_review_field(asset_id, "storyboardStage", st.session_state[key])


def export_intent(key: str) -> str:
    return st.selectbox("Export intent", ("prime", "multiverse_ingredients"),
                        format_func=lambda value: "Prime production references" if value == "prime" else "Multiverse creative ingredients",
                        key=key, on_change=lambda: st.session_state.pop("studio_basket_zip", None))


def save_shot_plan(asset_id: str) -> None:
    plan = normalize_plan({"destinations": st.session_state[f"plan-destinations:{asset_id}"],
                           "idea": st.session_state[f"plan-idea:{asset_id}"],
                           "prompt": st.session_state[f"plan-prompt:{asset_id}"]})
    set_review_field(asset_id, "shotPlan", plan)
    st.session_state[f"plan-destinations:{asset_id}"] = plan["destinations"]
    st.session_state.studio_flash = "Shot plan saved in this session. Export it from Shot plans or Favorites & notes."


def remove_shot_plan(asset_id: str) -> None:
    set_review_field(asset_id, "shotPlan", None)
    for field in ("destinations", "idea", "prompt"):
        st.session_state.pop(f"plan-{field}:{asset_id}", None)


def toggle_collaborator(asset_id: str, provider: str) -> None:
    existing = st.session_state.studio_reviews.get(asset_id, {}).get("shotPlan")
    plan = normalize_plan(existing or {})
    destinations = {destination for destination in plan["destinations"] if destination != "undecided"}
    if provider in destinations:
        destinations.remove(provider)
    else:
        destinations.add(provider)
    plan["destinations"] = list(destinations)
    plan = normalize_plan(plan)
    set_review_field(asset_id, "shotPlan", plan)
    st.session_state[f"plan-destinations:{asset_id}"] = plan["destinations"]


def render_collaborator_controls(asset: dict) -> None:
    plan = st.session_state.studio_reviews.get(asset["id"], {}).get("shotPlan") or {}
    destinations = plan.get("destinations", [])
    st.markdown("**Collaborator**")
    for column, provider in zip(st.columns(3), ("Flow", "Grok", "Gemini")):
        with column:
            selected = provider in destinations
            st.button(("✓ " if selected else "") + provider, key=f"collaborator:{asset['id']}:{provider}",
                      type="primary" if selected else "secondary", width="stretch",
                      on_click=toggle_collaborator, args=(asset["id"], provider), disabled=bool(asset.get("archived")))
    queued = [provider for provider in ("Flow", "Grok", "Gemini") if provider in destinations]
    if queued:
        st.caption(f"Queued for {', '.join(queued)} — draft not sent.")
    else:
        st.caption("Choose a collaborator to queue a draft locally. Add the idea or prompt under Plan a shot.")


def render_review_controls(asset: dict) -> None:
    asset_id = asset["id"]
    decision = st.session_state.studio_reviews.get(asset_id, {})
    status = decision.get("status")
    st.markdown("**Review decision**")
    st.caption(f"Current: {STATUS_LABELS.get(status, 'Unmarked')}")
    for row in ((("Keep", "keep"), ("Needs fixes", "needs_fixes")), (("Mark for removal", "remove"), ("Clear", None))):
        for column, (label, value) in zip(st.columns(2), row):
            with column:
                st.button(label, key=f"review:{asset_id}:{value}", width="stretch",
                          type="primary" if value is not None and status == value else "secondary",
                          on_click=set_review_field, args=(asset_id, "status", value))
    st.caption("Keep applies to the scope in your note. Mark for removal flags the reference; it does not delete a file. Clear keeps your note and shot plan.")
    note_key = f"asset-note:{asset_id}"
    if note_key not in st.session_state:
        st.session_state[note_key] = decision.get("note", "")
    st.text_area("Your review note", key=note_key, height=130, on_change=save_note, args=(asset_id, note_key),
                 placeholder="What works here? What should change in the next pass?")
    plan = decision.get("shotPlan")
    with st.expander("Plan a shot", expanded=False):
        st.caption("Save a draft for Gemini, Flow, or Grok. This does not send a request or generate media.")
        defaults = plan or {"destinations": ["undecided"], "idea": "", "prompt": ""}
        for field in ("destinations", "idea", "prompt"):
            key = f"plan-{field}:{asset_id}"
            if key not in st.session_state:
                st.session_state[key] = defaults[field]
        with st.form(f"shot-plan:{asset_id}"):
            st.multiselect("Destination", DESTINATIONS, key=f"plan-destinations:{asset_id}")
            st.text_area("Shot idea", key=f"plan-idea:{asset_id}", height=100,
                         placeholder="What should happen in this shot? What must stay the same?")
            st.text_area("Prompt draft", key=f"plan-prompt:{asset_id}", height=150)
            st.form_submit_button("Save shot plan", on_click=save_shot_plan, args=(asset_id,), width="stretch")
        if plan:
            st.caption("Planned for " + ", ".join(plan["destinations"]) + " · not sent")
            st.button("Remove shot plan", key=f"remove-plan:{asset_id}", on_click=remove_shot_plan, args=(asset_id,))
    st.caption("Review choices, notes, plans, and stars stay in this session. Export them before you leave.")
    variant = decision.get("variant", asset.get("variant", "prime"))
    with st.expander("Reference lane & working-reference request"):
        st.caption(f"Current lane: {'Multiverse' if variant == 'multiverse' else 'Prime'}")
        for column, label, value in zip(st.columns(2), ("Prime", "Multiverse"), ("prime", "multiverse")):
            with column:
                st.button(label, key=f"variant:{asset_id}:{value}", on_click=set_variant, args=(asset_id, value),
                          type="primary" if variant == value else "secondary", width="stretch")
        scope_key = f"working-scope:{asset_id}"
        st.selectbox("Working-reference scope", ("complete_look", "identity", "outfit", "scene", "detail"),
                     format_func=lambda value: value.replace("_", " ").title(), key=scope_key)
        blocked = variant == "multiverse" or bool(asset.get("archived")) or decision.get("status") == "remove"
        st.button("Request working reference", key=f"request-working:{asset_id}", on_click=request_working_reference,
                  args=(asset_id, scope_key), disabled=blocked)
        if decision.get("workingReference"):
            reference = decision["workingReference"]
            st.caption(f"{reference['status'].title()} · {reference['scope'].replace('_', ' ')}")
            st.button("Clear working-reference request", key=f"clear-working:{asset_id}",
                      on_click=set_review_field, args=(asset_id, "workingReference", None))
        st.caption("Requests go into the review sweep for Nova. They do not move a file or approve a category automatically. Multiverse references cannot become Prime working references.")
    with st.expander("Workflow & storyboard stage"):
        stage_key = f"asset-stage:{asset_id}"
        if stage_key not in st.session_state:
            st.session_state[stage_key] = decision.get("storyboardStage")
        effective_stage = storyboard_stage(asset, st.session_state.studio_reviews)
        st.caption("Current stage: " + STORYBOARD_STAGES.get(effective_stage, "Unassigned"))
        st.selectbox("Storyboard stage", [None, *STORYBOARD_STAGES], format_func=lambda value: STORYBOARD_STAGES.get(value, "Use source stage"),
                     key=stage_key, on_change=save_storyboard_stage, args=(asset_id, stage_key))
        st.caption("This records the planning stage only. Advancing a stage does not mark technical verification passed or approve a working reference.")


def change_page(signature: str, value: int) -> None:
    st.session_state.studio_pages[signature] = value
    clear_selection()


def hero(project: dict, view: str, assets: list[dict]) -> None:
    visuals = [a for a in assets if a.get("kind") in VISUAL_KINDS and not a.get("archived")]
    videos = sum(a.get("kind") == "video" for a in visuals)
    captions = {
        "Library": "Explore the looks, compare the details, and keep the references you want to return to.",
        "Storyboard": "Follow the story in pictures. Open a panel for its beat, lyric connection, and review notes.",
        "Collaborator briefs": "Instructions, references, and current care packages for Gemini, Flow, and Grok.",
        "Favorites & notes": "Your working shortlist. Export it to keep your choices and carry them between review sessions.",
        "Review queue": "Keep what works, record corrections, and flag unwanted references for review.",
        "Shot plans": "Turn references into draft shots, then export a handoff for Gemini, Flow, or Grok.",
        "Export basket": "Choose references to take with you. The basket is separate from favorites and review decisions.",
        "Documents": "The supporting notes behind the pictures, grouped so the useful details are easy to find.",
    }
    subtitle = project.get("subtitle", "")
    st.markdown(f'<div class="studio-hero"><div class="eyebrow">CFA · Creative Studio · {html.escape(view)}</div>'
                f'<h1>{html.escape(project["name"])}</h1><p>{html.escape(subtitle)} · '
                f'{len(visuals) - videos} pictures · {videos} clips</p><p>{captions[view]}</p></div>', unsafe_allow_html=True)


def favorite_button(asset: dict, context: str = "card") -> None:
    chosen = asset["id"] in st.session_state.studio_favorites
    st.button("★ Saved" if chosen else "☆ Save", key=f"favorite:{context}:{asset['id']}",
              help="Add to your review shortlist. This does not change the source's approval status.",
              on_click=toggle_favorite, args=(asset["id"],), width="stretch", disabled=bool(asset.get("archived")))


def render_selected(asset: dict) -> None:
    st.button("← Back to the collection", on_click=clear_selection)
    st.subheader(asset.get("title", asset["filename"]))
    if asset.get("archived"):
        st.info("Archived from regular browsing and exports. This entry remains available for review bookkeeping.")
    left, right = st.columns([3, 2], gap="large")
    with left:
        source = media_path(LIBRARY_DIR, asset.get("src"))
        preview = media_path(LIBRARY_DIR, asset.get("thumb"))
        if asset.get("kind") == "video" and source:
            st.video(str(source))
        elif source or preview:
            st.image(str(source or preview), width="stretch")
        else:
            st.info("This media file is not included in the current review bundle.")
        if source:
            st.download_button("Download this review copy", data=source.read_bytes(), file_name=source.name,
                               mime=mimetypes.guess_type(source.name)[0] or "application/octet-stream",
                               key=f"media-download:{asset['id']}")
        st.caption(asset.get("filename", ""))
    with right:
        favorite_button(asset, "selected")
        basket_button(asset, "selected")
        render_collaborator_controls(asset)
        if asset.get("beat"):
            st.markdown("**Story beat**")
            st.write(asset["beat"])
        if asset.get("lyric"):
            st.markdown("**Lyric connection**")
            st.write(asset["lyric"])
        if asset.get("motion"):
            st.markdown("**Motion idea**")
            st.write(asset["motion"])
        if asset.get("note"):
            st.markdown("**What to look for**")
            st.write(asset["note"])
        render_review_controls(asset)
        with st.expander("Reference details"):
            st.write(f"Reference: {asset['id']}")
            if asset.get("sceneID"):
                st.write(f"Scene: {asset['sceneID']}")
            if asset.get("duration") is not None:
                st.write(f"Clip length: {asset['duration']:g} seconds")
            if asset.get("tags"):
                st.write(" · ".join(str(tag) for tag in asset["tags"]))
            st.caption("Saved selections are review choices; they do not replace the project's reference instructions.")


def render_card(asset: dict) -> None:
    with st.container(border=True):
        preview = media_path(LIBRARY_DIR, asset.get("thumb"))
        if not preview and asset.get("kind") in {"image", "gif"}:
            preview = media_path(LIBRARY_DIR, asset.get("src"))
        if preview:
            st.image(str(preview), width="stretch")
        else:
            st.info("Open to view this clip." if asset.get("kind") == "video" else "Preview not included")
        st.markdown(f"**{asset.get('title', asset['filename'])}**")
        decision = st.session_state.studio_reviews.get(asset["id"], {})
        if asset.get("archived"):
            st.caption("Archived")
        if decision.get("variant", asset.get("variant")) == "multiverse":
            st.caption("Multiverse · creative ingredient")
        if decision.get("status"):
            st.caption(STATUS_LABELS[decision["status"]])
        if decision.get("shotPlan"):
            st.caption("Shot planned · " + ", ".join(decision["shotPlan"]["destinations"]))
        if decision.get("note"):
            st.write(decision["note"])
        if asset.get("kind") == "video":
            duration = asset.get("duration")
            st.caption(f"Video · {duration:g} seconds" if isinstance(duration, (int, float)) else "Video")
        if asset.get("lyric"):
            st.caption(asset["lyric"])
        elif asset.get("note"):
            note = str(asset["note"])
            st.caption(note[:165] + ("…" if len(note) > 165 else ""))
        c1, c2 = st.columns([3, 2])
        with c1:
            st.button("Play & review" if asset.get("kind") == "video" else "Open & review",
                      key=f"open:{asset['id']}", on_click=select_asset, args=(asset["id"], asset["project"]), width="stretch")
        with c2:
            favorite_button(asset)
        basket_button(asset)


def render_grid(results: list[tuple[dict, dict | None]], signature: str) -> None:
    if not results:
        st.info("No pictures match this view. Try another collection or a shorter search.")
        return
    count = len(results)
    last_page = (count - 1) // PAGE_SIZE
    page = min(st.session_state.studio_pages.get(signature, 0), last_page)
    start, stop = page * PAGE_SIZE, min((page + 1) * PAGE_SIZE, count)
    a, b, c = st.columns([2, 5, 2])
    with a:
        st.button("← Previous", key=f"prev:{signature}", disabled=page == 0,
                  on_click=change_page, args=(signature, page - 1), width="stretch")
    with b:
        st.caption(f"Showing {start + 1}–{stop} of {count} · Page {page + 1} of {last_page + 1}")
    with c:
        st.button("Next →", key=f"next:{signature}", disabled=page == last_page,
                  on_click=change_page, args=(signature, page + 1), width="stretch")
    visible = results[start:stop]
    index = 0
    while index < len(visible):
        album = visible[index][1]
        group_id = album.get("id") if album else None
        end = index + 1
        while end < len(visible) and (visible[end][1].get("id") if visible[end][1] else None) == group_id:
            end += 1
        if album:
            st.subheader(album["title"])
            if album.get("description"):
                st.caption(album["description"])
        for row in range(index, end, 3):
            for col, (asset, _) in zip(st.columns(3, gap="medium"), visible[row:min(row + 3, end)]):
                with col:
                    render_card(asset)
        index = end
    if count > PAGE_SIZE:
        st.caption("Use the page controls above to continue through this collection.")


def render_library(data: dict, project: str, storyboard: bool = False) -> None:
    albums = [a for a in data["albums"] if a.get("project") == project]
    if storyboard:
        category = "storyboard"
        matching = [a for a in albums if a.get("category") == category]
        st.caption("Panel sequence and story notes are planning references. No song timing is implied.")
    else:
        available = {a.get("category") for a in albums}
        options = ["all"] + [key for key, _ in data["categories"] if key in available]
        labels = {"all": "All pictures & clips", **dict(data["categories"])}
        category = st.selectbox("Explore", options, format_func=lambda key: labels.get(key, key),
                                key=f"category:{project}", on_change=clear_selection)
        matching = [a for a in albums if category == "all" or a.get("category") == category]
        if category == "details" and data.get("detailProfiles"):
            detail_view = st.radio("Detail view", ("By character", "All references"), horizontal=True, key=f"detail-view:{project}")
            if detail_view == "By character" and render_detail_profiles(data, project):
                return
    c1, c2 = st.columns([3, 2])
    with c1:
        album_ids = ["all"] + [a["id"] for a in matching]
        album_labels = {"all": "All collections", **{a["id"]: a["title"] for a in matching}}
        album_id = st.selectbox("Collection", album_ids, format_func=lambda key: album_labels[key],
                               key=f"album:{project}:{category}:{storyboard}", on_change=clear_selection)
    with c2:
        query = st.text_input("Find a picture or moment", placeholder="Try: neck, coat, cockpit…",
                              key=f"search:{project}:{storyboard}", on_change=clear_selection)
    results = ordered_assets(data["assets"], data["albums"], project, category, album_id, query)
    story_range, themes, stage = (0, 100), [], "all"
    if storyboard:
        metadata = data.get("storyboardMetadata", {}).get(project, {})
        st.caption(metadata.get("timingStatus", "Source panel order only; not aligned to song seconds."))
        stage = st.selectbox("Stage", ["all", *STORYBOARD_STAGES],
                             format_func=lambda value: "All stages" if value == "all" else STORYBOARD_STAGES[value],
                             key=f"story-stage:{project}")
        if stage != "all":
            results = [(asset, album) for asset, album in results if storyboard_stage(asset, st.session_state.studio_reviews) == stage]
        story_range = st.slider("Storyboard position (%)", 0, 100, (0, 100), step=5, key=f"story-position:{project}")
        results = storyboard_window(results, *story_range)
        choices = sorted({theme for asset, album in results for theme in storyboard_themes(asset, album)}, key=str.casefold)
        theme_key = f"story-themes:{project}"
        if theme_key in st.session_state:
            st.session_state[theme_key] = [theme for theme in st.session_state[theme_key] if theme in choices]
        themes = st.multiselect("Story themes", choices, key=theme_key)
        if themes:
            results = [(asset, album) for asset, album in results if any(theme in storyboard_themes(asset, album) for theme in themes)]
    layout, order = "Grouped", "Longest first"
    if category == "videos":
        layout_column, sort_column = st.columns(2)
        with layout_column:
            layout = st.selectbox("Layout", ("Grouped", "All clips"), key=f"video-layout:{project}")
        with sort_column:
            order = st.selectbox("Sort", ("Longest first", "Shortest", "Alphabetical A–Z"), key=f"video-sort:{project}")
        results = layout_video_assets(results, layout, order)
        st.caption("Grouped keeps scene categories and places turnarounds last. All clips sorts across the current collection and search. Unknown durations appear last.")
    signature = json.dumps([project, category, album_id, query, storyboard, layout, order, story_range, themes, stage])
    render_grid(results, signature)


def render_detail_profiles(data: dict, project: str) -> bool:
    profiles = [profile for profile in data.get("detailProfiles", []) if isinstance(profile, dict)
                and profile.get("project") == project and isinstance(profile.get("objects"), list)]
    if not profiles:
        return False
    profile_map = {profile["id"]: profile for profile in profiles}
    profile_id = st.selectbox("Character profile", list(profile_map),
                              format_func=lambda key: profile_map[key].get("title", profile_map[key].get("character", key)), key=f"detail-profile:{project}")
    profile = profile_map[profile_id]
    objects = {item["id"]: item for item in profile["objects"] if isinstance(item, dict) and item.get("id")}
    if not objects:
        st.info("This character profile has no detail objects yet.")
        return True
    object_id = st.selectbox("Detail object", list(objects), format_func=lambda key: objects[key].get("title", key), key=f"detail-object:{profile_id}")
    item = objects[object_id]
    st.subheader(item.get("title", object_id))
    st.caption(" · ".join(str(item.get(key, "")) for key in ("kind", "location", "status") if item.get(key)))
    if item.get("summary"):
        st.write(item["summary"])
    evidence = st.radio("Evidence", ("Placement & examples", "Stencils", "All object references"), horizontal=True, key=f"detail-evidence:{profile_id}:{object_id}")
    keys = ("assetIDs", "exampleAssetIDs") if evidence == "Placement & examples" else ("stencilAssetIDs",) if evidence == "Stencils" else ("assetIDs", "exampleAssetIDs", "stencilAssetIDs")
    ids = list(dict.fromkeys(asset_id for key in keys for asset_id in item.get(key, []) if isinstance(asset_id, str)))
    by_id = {asset["id"]: asset for asset in data["assets"] if not asset.get("archived") and asset.get("kind") in VISUAL_KINDS}
    results = [(by_id[asset_id], None) for asset_id in ids if asset_id in by_id]
    render_grid(results, f"detail:{profile_id}:{object_id}:{evidence}")
    return True


def document_download(asset: dict, context: str = "doc") -> None:
    text = asset.get("text", "")
    source = media_path(LIBRARY_DIR, asset.get("src"))
    if text:
        st.download_button("Download text", text, file_name=asset.get("downloadFilename", asset.get("filename", "reference.txt")),
                           mime="text/plain", key=f"{context}-download:{asset['id']}")
    elif source:
        st.download_button("Download document", source.read_bytes(), file_name=source.name,
                           mime=mimetypes.guess_type(source.name)[0] or "application/octet-stream",
                           key=f"{context}-download:{asset['id']}")


def render_documents(assets: list[dict]) -> None:
    documents = [a for a in assets if a.get("kind") in {"document", "pdf"}]
    if not documents:
        st.info("There are no documents for this project in the current bundle.")
        return
    query = st.text_input("Find a supporting note", key="document-search", placeholder="Search titles or contents")
    groups = document_tree(documents, query)
    if not groups:
        st.info("No supporting notes match this search.")
    for parent, children in groups.items():
        count = sum(len(items) for items in children.values())
        with st.expander(f"{parent} ({count})", expanded=bool(query)):
            for child, items in children.items():
                with st.expander(f"{child} ({len(items)})", expanded=bool(query)):
                    choices = {asset["id"]: asset for asset in items}
                    asset_id = st.selectbox("Document", list(choices), format_func=lambda key, group=choices: group[key].get("title", group[key]["filename"]), key=f"doc-choice:{parent}:{child}")
                    asset = choices[asset_id]
                    if asset.get("note"):
                        st.caption(asset["note"])
                    if asset.get("inert"):
                        st.caption("Technical reference supplied as text. Nothing on this page executes it.")
                    if asset.get("text"):
                        st.code(asset["text"], language=None, wrap_lines=True)
                    elif asset.get("kind") == "pdf":
                        st.write("Use the download below to read this PDF.")
                    document_download(asset)


def render_collaborator_briefs(data: dict, assets: list[dict], project: str, provider_filter: str | None = None) -> None:
    if provider_filter is None:
        st.info("Choose the collaborator below. Supply the named reference images with the current brief; this page does not send anything for you.")
    sections = collaborator_sections(assets)
    tasks = mission_tasks(data.get("missionControl", {}))
    for provider, documents in sections.items():
        if provider_filter is not None and provider != provider_filter:
            continue
        st.subheader(provider)
        packages = [(task, index, link) for task in tasks if task["provider"] == provider and task["project"] in (project, "shared")
                    for index, link in enumerate(task["links"]) if link.get("downloadPath")]
        if provider == "Flow":
            st.markdown("**Recommended first pass**")
            st.write("1. After sorting, upload the selected local reference once and use Character creation for the first preservation proof.")
            st.write("2. Use one short prompt from the starter. Add from project reuses a reference already uploaded.")
            st.write("3. Flow Agent is optional for planning. Give it the relevant brief and a specific task together; keep Confirm before generating set to Always.")
            st.caption("Open Start here · Flow below for the full steps and reference guidance.")
        for task, index, link in packages:
            package = media_path(LIBRARY_DIR, link["downloadPath"])
            if package and package.suffix.lower() == ".zip":
                st.download_button(link["label"], package.read_bytes(), file_name=package.name, mime="application/zip",
                                   key=f"brief-package:{project}:{task['id']}:{index}")
        if not documents:
            st.caption("No current brief for this collaborator is included for this project yet.")
        for asset in documents:
            with st.expander(asset.get("title", asset["filename"])):
                if asset.get("note"):
                    st.caption(asset["note"])
                if asset.get("text"):
                    st.code(asset["text"], language=None, wrap_lines=True)
                document_download(asset, context="brief")
    st.caption("Earlier exploration briefs remain in Documents as historical references.")


def render_workflow_reference(data: dict, asset_id: str, context: str) -> None:
    asset = next((item for item in data["assets"] if item["id"] == asset_id), None)
    if asset is None:
        st.caption(f"Reference {asset_id} is not included in this bundle yet.")
        return
    if asset.get("kind") in VISUAL_KINDS:
        preview = media_path(LIBRARY_DIR, asset.get("thumb"))
        if preview:
            st.image(str(preview), width=320)
        st.caption(asset.get("filename", asset_id))
        st.button("Open " + asset.get("title", asset.get("filename", asset_id)),
                  key=f"workflow-open:{context}:{asset_id}", on_click=open_mission_reference, args=(asset,))
    else:
        with st.expander(asset.get("title", asset.get("filename", asset_id))):
            if asset.get("text"):
                st.code(asset["text"], language=None, wrap_lines=True)
            document_download(asset, context=f"workflow:{context}")


def render_collaborators(data: dict) -> None:
    st.button("← Back to library", key="collaborators-back", on_click=back_to_library)
    st.markdown('<div class="studio-hero"><div class="eyebrow">CFA · Production workspace</div>'
                '<h1>Collaborators</h1><p>Open the working recipe, review its inputs and outputs, or prepare the next collaborator handoff.</p></div>',
                unsafe_allow_html=True)
    provider = st.selectbox("Collaborator workspace", ("ComfyUI", "Flow", "Gemini", "Grok", "Panhandler Nova"), key="workspace-provider")
    projects = {item["id"]: item["name"] for item in data["projects"]}
    if provider == "ComfyUI":
        workflows = production_workflows(data.get("productionWorkflows", []))
        st.caption("Actual workflow records, inputs, and results. Opening a Cloud link does not execute a workflow.")
        if not workflows:
            st.info("No production workflow record is included in this bundle yet. Existing references remain available in the Library.")
        for workflow in workflows:
            with st.container(border=True):
                st.subheader(workflow["title"])
                st.caption(projects.get(workflow["project"], workflow["project"]))
                st.markdown("**Execution status**")
                st.write(workflow["status"])
                st.write(workflow["summary"])
                st.markdown("**Next action**")
                st.write(workflow["nextAction"])
                if workflow.get("cloudURL"):
                    st.link_button("Open saved Cloud workflow", workflow["cloudURL"])
                inputs, outputs = st.columns(2)
                with inputs:
                    st.markdown("**Inputs**")
                    for asset_id in workflow["sourceAssetIDs"]:
                        render_workflow_reference(data, asset_id, f"{workflow['id']}:input")
                with outputs:
                    st.markdown("**Outputs / previews**")
                    for asset_id in workflow["outputAssetIDs"]:
                        render_workflow_reference(data, asset_id, f"{workflow['id']}:output")
                if workflow["documentAssetIDs"]:
                    st.markdown("**Workflow files and instructions**")
                    for asset_id in workflow["documentAssetIDs"]:
                        render_workflow_reference(data, asset_id, f"{workflow['id']}:document")
        return
    st.caption("Tasks cover all projects. Statuses come from the saved handoff; this page does not monitor or send requests to collaborator accounts.")
    tasks = [task for task in mission_tasks(data.get("missionControl", {})) if task["provider"] == provider]
    states = {"ready": "Ready for handoff", "needs_input": "Needs input", "planned": "Planned", "in_progress": "In progress", "done": "Done"}
    for task in tasks:
        with st.container(border=True):
            st.subheader(task["title"])
            st.caption(f"{projects.get(task['project'], 'Shared projects')} · {states[task['status']]}")
            st.write(task["summary"])
            st.markdown("**Next action**")
            st.write(task["nextAction"])
            for requirement in task["missing"]:
                st.write("• " + requirement)
    for project in data["projects"]:
        assets = [asset for asset in data["assets"] if asset.get("project") == project["id"]]
        section = "Shared roles" if provider == "Panhandler Nova" else provider
        documents = collaborator_sections(assets).get(section, [])
        if documents:
            st.subheader(project["name"] + " · briefs")
            render_collaborator_briefs(data, assets, project["id"], provider_filter=section)


def render_favorites(data: dict, project: str) -> None:
    if message := st.session_state.pop("studio_import_message", None):
        st.success(message)
    payload = review_payload(data["assets"], st.session_state.studio_reviews, st.session_state.studio_favorites, st.session_state.studio_basket)
    export_col, import_col = st.columns(2, gap="large")
    with export_col:
        st.markdown("**Keep your review**")
        st.write("Export includes review decisions, notes, shot plans, favorites, and the export basket from all projects. Save it before closing this session.")
        st.download_button("Export complete review", json.dumps(payload, ensure_ascii=False, indent=2),
                           file_name="cfa-visual-review.json", mime="application/json", width="stretch")
        st.caption(f"{len(payload['items'])} review records · {len(payload['favorites'])} favorites across all projects")
    with import_col:
        st.markdown("**Bring a review back**")
        uploaded = st.file_uploader("Review or favorites JSON", type=["json"], key="favorites-upload")
        if uploaded is not None and st.button("Add this review to my session", width="stretch"):
            try:
                if uploaded.size > 5 * 1024 * 1024:
                    raise ValueError("Choose a review file smaller than 5 MB.")
                imported = json.loads(uploaded.getvalue())
                reviews, accepted, skipped = read_review(imported, data["assets"])
                basket, basket_skipped = read_basket({"format": EXPORT_FORMAT, "items": imported["exportBasket"]}, data["assets"]) if "exportBasket" in imported else (set(), 0)
                st.session_state.studio_basket = set(st.session_state.studio_basket) | basket
                st.session_state.pop("studio_basket_zip", None)
                st.session_state.studio_favorites = set(st.session_state.studio_favorites) | accepted
                for asset_id, decision in reviews.items():
                    st.session_state.studio_review_overrides.setdefault(asset_id, {}).update(decision)
                    for prefix in ("asset-note", "plan-destinations", "plan-idea", "plan-prompt", "asset-stage"):
                        st.session_state.pop(f"{prefix}:{asset_id}", None)
                st.session_state.studio_import_message = f"Merged {len(accepted)} favorites and {len(reviews)} review records, plus {len(basket)} basket references. Skipped {skipped + basket_skipped} unmatched or invalid references."
                st.rerun()
            except (ValueError, TypeError, UnicodeDecodeError) as error:
                st.error(str(error))
    st.divider()
    show_notes = st.checkbox("Also show pictures with a note", value=True)
    results = ordered_assets(data["assets"], data["albums"], project)
    results = [(a, group) for a, group in results if a["id"] in st.session_state.studio_favorites
               or (show_notes and st.session_state.studio_notes.get(a["id"], "").strip())]
    if not results:
        st.info("Nothing saved for this project yet. Use ☆ Save on a picture or open one to leave a note.")
    else:
        render_grid(results, f"favorites:{project}:{show_notes}")


def render_review_queue(data: dict, project: str) -> None:
    status = st.selectbox("Review status", ("all", "keep", "needs_fixes", "remove", "notes"),
                          format_func=lambda s: {"all": "All reviewed references", "notes": "Notes without a decision"}.get(s, STATUS_LABELS.get(s, s)))
    query = st.text_input("Find a reviewed reference", key=f"review-search:{project}")
    results = ordered_assets(data["assets"], data["albums"], project, include_archived=True)
    reviews = st.session_state.studio_reviews
    def matches(asset):
        decision = reviews.get(asset["id"], {})
        if status == "notes":
            return not decision.get("status") and bool(decision.get("note", "").strip())
        return bool(asset.get("archived") or decision.get("status") or decision.get("note", "").strip()
                    or decision.get("workingReference") or decision.get("variant") or decision.get("storyboardStage")
                    or decision.get("shotPlan")) if status == "all" else decision.get("status") == status
    terms = query.casefold().split()
    results = [(asset, album) for asset, album in results if matches(asset)
               and all(term in (json.dumps(asset, ensure_ascii=False) + " " + json.dumps(reviews.get(asset["id"], {}), ensure_ascii=False)).casefold() for term in terms)]
    st.caption("Flags stay in your review. Archived items remain here for bookkeeping while ordinary library views omit them. Export the complete review from Favorites & notes.")
    render_grid(results, f"review:{project}:{status}:{query}")


def render_shot_plans(data: dict, project: str) -> None:
    intent = export_intent(f"shot-intent:{project}")
    destination = st.selectbox("Handoff destination", ("all", *DESTINATIONS),
                               format_func=lambda d: "All destinations" if d == "all" else d)
    query = st.text_input("Find a shot plan", key=f"shot-search:{project}")
    reviews = st.session_state.studio_reviews
    payload = handoff_payload(data["assets"], reviews, project, destination, intent)
    terms = query.casefold().split()
    if terms:
        payload["items"] = [item for item in payload["items"]
                            if all(term in json.dumps(item, ensure_ascii=False).casefold() for term in terms)]
    ids = {item["id"] for item in payload["items"]}
    st.caption(f"{len(ids)} draft shot plans · not sent or generated")
    st.info(payload["attachmentReminder"])
    st.caption("Prime exports exclude Multiverse, removal flags, and archived entries. Multiverse creative ingredients includes variants intentionally; removals and archives stay excluded.")
    txt_col, json_col = st.columns(2)
    filename = f"cfa-shot-handoff-{project}-{destination}"
    with txt_col:
        st.download_button("Export handoff TXT", handoff_text(payload), file_name=filename + ".txt", mime="text/plain", disabled=not ids, width="stretch")
    with json_col:
        st.download_button("Export handoff JSON", json.dumps(payload, ensure_ascii=False, indent=2),
                           file_name=filename + ".json", mime="application/json", disabled=not ids, width="stretch")
    st.caption("Exports contain only the project, destination, and search results shown here. Use the complete review export to restore your session later.")
    results = [(asset, album) for asset, album in ordered_assets(data["assets"], data["albums"], project) if asset["id"] in ids]
    render_grid(results, f"shot:{project}:{destination}:{query}")


def open_mission_reference(asset: dict) -> None:
    st.session_state.studio_project = asset["project"]
    if st.session_state.studio_view == CORNER:
        st.session_state.studio_mission_selected = asset["id"]
    else:
        st.session_state.studio_view = "Library"
        select_asset(asset["id"])


def render_mission_control(data: dict, review_data: dict | None = None) -> None:
    from mission_view import render_corner
    st.button("← Back to library", key="mission-back", on_click=back_to_library)
    st.markdown('<div class="studio-hero"><div class="eyebrow">CFA · Ziggy’s Corner</div>'
                '<h1>Mission Control</h1><p>Your next moves, prepared handoffs, and ideas waiting for their next pass.</p></div>',
                unsafe_allow_html=True)

    def sweep():
        st.write("Save your decisions, favorites, stages and reference roles, then pass the review to Nova. This does not start an agent or delete files.")
        payload = sweep_payload((review_data or data)["assets"], st.session_state.studio_reviews, st.session_state.studio_favorites, st.session_state.studio_basket)
        st.download_button("Prepare review sweep JSON", json.dumps(payload, ensure_ascii=False, indent=2),
                           file_name="cfa-review-sweep-for-nova.json", mime="application/json")

    render_corner(data, LIBRARY_DIR, open_mission_reference, render_selected, document_download, navigate, sweep, review_data=review_data or data)


def render_export_basket(data: dict) -> None:
    basket = st.session_state.studio_basket
    reviews = st.session_state.studio_reviews
    intent = export_intent("basket-intent")
    payload = basket_payload(data["assets"], basket, reviews, intent)
    eligible = {item["id"] for item in payload["items"]}
    st.caption(f"{len(eligible)} eligible references from {len(basket)} selected across all projects. Stars and review decisions are separate.")
    st.caption("Prime excludes Multiverse. Removal flags and archived entries are excluded from every media export. Full review backups retain the marks.")
    left, right = st.columns(2)
    with left:
        st.download_button("Export selection JSON", json.dumps(payload, ensure_ascii=False, indent=2),
                           file_name="cfa-visual-export.json", mime="application/json", disabled=not eligible, width="stretch")
        st.button("Clear export basket", on_click=clear_basket, disabled=not basket, width="stretch")
        st.caption("Clearing the basket does not change favorites, notes, plans, or source files.")
    with right:
        if st.button("Prepare ZIP of review copies", disabled=not eligible, width="stretch"):
            try:
                with st.spinner("Preparing selected review copies…"):
                    st.session_state.studio_basket_zip = basket_zip(LIBRARY_DIR, data["assets"], basket, reviews=reviews, intent=intent)
            except (OSError, ValueError) as error:
                st.error(str(error))
        if zip_bytes := st.session_state.get("studio_basket_zip"):
            st.download_button("Download review-copy ZIP", zip_bytes, file_name="cfa-review-copies.zip",
                               mime="application/zip", width="stretch")
        st.caption("ZIP includes hosted review copies and a source/hash manifest. It does not contain original masters. Duplicate content is included once. Limit: 100 MB of selected files.")
    with st.expander("Import a saved basket"):
        uploaded = st.file_uploader("Export-basket JSON", type=["json"], key="basket-upload")
        if uploaded is not None and st.button("Add selection to basket"):
            try:
                if uploaded.size > 5 * 1024 * 1024:
                    raise ValueError("Choose a selection list smaller than 5 MB.")
                accepted, skipped = read_basket(json.loads(uploaded.getvalue()), data["assets"])
                st.session_state.studio_basket = set(basket) | accepted
                st.session_state.pop("studio_basket_zip", None)
                st.session_state.studio_flash = f"Added {len(accepted)} basket references. Skipped {skipped} unmatched references."
                st.rerun()
            except (ValueError, TypeError, UnicodeDecodeError) as error:
                st.error(str(error))
    for project in data["projects"]:
        results = [(asset, album) for asset, album in ordered_assets(data["assets"], data["albums"], project["id"]) if asset["id"] in basket]
        if results:
            st.subheader(project["name"])
            render_grid(results, f"basket:{project['id']}")
    if not basket:
        st.info("Use ⇩ Add to export basket on any picture or clip to start a selection.")


def main() -> None:
    apply_theme()
    init_state()
    catalog_path = LIBRARY_DIR / "catalog.json"
    if not catalog_path.is_file():
        st.title("CFA Creative Studio")
        st.info("The studio is ready for its library bundle. Add library/catalog.json and its packaged media to load the collections.")
        return
    try:
        data = load_catalog(str(catalog_path), catalog_path.stat().st_mtime_ns)
    except (OSError, ValueError) as error:
        st.error(f"The review library could not be loaded: {error}")
        return
    mission_data = data
    review_data = data
    mission_path = LIBRARY_DIR / "mission_control.json"
    if mission_path.is_file():
        try:
            mission_data = load_catalog(str(mission_path), mission_path.stat().st_mtime_ns)
            review_data = mission_review_data(data, mission_data)
        except (OSError, ValueError) as error:
            st.error(f"The Ziggy’s Corner snapshot could not be loaded: {error}")
            return
    st.session_state.studio_reviews = effective_reviews(review_data["assets"], review_data.get("reviewDecisions", []), st.session_state.studio_review_overrides)
    st.session_state.studio_notes = {key: value.get("note", "") for key, value in st.session_state.studio_reviews.items()}
    if message := st.session_state.pop("studio_flash", None):
        st.success(message)
    projects = {p["id"]: p for p in data["projects"]}
    if not projects:
        st.info("No projects are included in this library yet.")
        return
    with st.sidebar:
        st.markdown("## CFA\n### Creative Studio")
        st.caption("A place to look, compare, and create.")
        project = st.selectbox("Project", list(projects), format_func=lambda key: projects[key]["name"],
                               key="studio_project", on_change=clear_project_selection)
        for label, views in (("START HERE", (CORNER,)), ("BROWSE", ("Library", "Storyboard")), ("CREATE", ("Collaborators", "Shot plans", "Collaborator briefs")),
                             ("KEEP & REFER", ("Review queue", "Export basket", "Favorites & notes", "Documents"))):
            st.caption(label)
            for view in views:
                st.button(f"{view} · {len(st.session_state.studio_basket)}" if view == "Export basket" else view,
                          key=f"nav:{view}", type="primary" if st.session_state.studio_view == view else "secondary",
                          on_click=navigate, args=(view,), width="stretch")
        st.divider()
        st.caption("Stars are a personal shortlist. Source references keep their existing status.")
        st.caption("Export your complete review to keep decisions, notes, plans, and favorites between sessions.")
    assets = [a for a in data["assets"] if a.get("project") == project]
    view = st.session_state.studio_view
    if view == CORNER:
        render_mission_control(mission_data, review_data)
        return
    if view == "Collaborators":
        render_collaborators(data)
        return
    hero(projects[project], view, assets)
    selection_assets = review_data["assets"] if view in ("Favorites & notes", "Shot plans", "Export basket") else assets
    selected = next((a for a in selection_assets if a["id"] == st.session_state.studio_selected and a.get("kind") in VISUAL_KINDS), None)
    if selected:
        render_selected(selected)
    elif view == "Library":
        render_library(data, project)
    elif view == "Storyboard":
        render_library(data, project, storyboard=True)
    elif view == "Collaborator briefs":
        render_collaborator_briefs(data, assets, project)
    elif view == "Favorites & notes":
        render_favorites(review_data, project)
    elif view == "Review queue":
        render_review_queue(data, project)
    elif view == "Shot plans":
        render_shot_plans(review_data, project)
    elif view == "Export basket":
        render_export_basket(review_data)
    else:
        render_documents(assets)


if __name__ == "__main__":
    main()
