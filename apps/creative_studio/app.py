"""CFA's portable visual review room. Run from the repository root with Streamlit."""

from __future__ import annotations

import html
import hashlib
import importlib.util
import json
import mimetypes
import sys
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import streamlit as st
from streamlit.components.v1 import declare_component

APP_DIR = Path(__file__).resolve().parent
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))


def _current_dependency_registry():
    """Refresh the registry itself when a warm server receives new source."""
    path = APP_DIR / "studio_dependencies.py"
    source = path.read_bytes()
    digest = hashlib.sha256(str(path.resolve()).encode() + b"\0" + source).hexdigest()
    key = "_cfa_studio_registry_" + digest
    module = sys.modules.get(key)
    if module is None:
        spec = importlib.util.spec_from_file_location(key, path)
        module = importlib.util.module_from_spec(spec)
        exec(compile(source, str(path), "exec"), module.__dict__)
        sys.modules[key] = module
    # Replace the import alias, never reload an older session's module in place.
    sys.modules["studio_dependencies"] = module
    return module


_studio_dependencies = _current_dependency_registry()
current_module = _studio_dependencies.current_module
# Keep this script's imports attached to the registry whose bytes it validated.
# Another warm session can replace the process-wide import alias at any time.
for _helper_name in (
    "DESTINATIONS", "OUTPUT_KINDS", "EXPORT_FORMAT", "MISSION_PROVIDERS", "STORYBOARD_STAGES", "VISUAL_KINDS", "basket_payload", "basket_zip", "destination_label", "output_kind_label",
    "collaborator_sections", "document_tree", "effective_reviews", "export_allowed", "handoff_payload", "handoff_text",
    "layout_video_assets", "media_path", "mission_tasks", "mission_review_data", "normalize_plan", "ordered_assets", "production_workflows",
    "read_basket", "read_review", "review_payload", "storyboard_stage", "storyboard_themes", "storyboard_window", "sweep_payload",
    "effective_design_data", "normal_visible", "approved_multiverse", "merge_review_overrides", "review_provenance", "validated_asset_aliases",
    "navigation_reference_count", "navigation_storyboard_shot_count", "mission_pending_requests", "cast_use_state",
):
    globals()[_helper_name] = getattr(_studio_dependencies, _helper_name)

LIBRARY_DIR = APP_DIR / "library"
PAGE_SIZE = 24
CORNER = "Ziggy’s Corner"
CASA = "Casa Baldadoon"
DESIGN_VIEWS = ("Working references", "Outfits", "Tattoos & piercings", "Supporting cast", "Comfy swap targets", "Archive")
VIEWS = (CORNER, CASA, "Project home", "Library", *DESIGN_VIEWS, "Storyboard", "Videos", "Inspiration", "Needs review", "Collaborators", "Collaborator briefs", "Review queue", "Shot plans", "Export basket", "Favorites & notes", "Documents", "Intake verification")
STATUS_LABELS = {None: "Unmarked", "keep": "Keep", "needs_fixes": "Needs fixes", "remove": "Marked for removal"}
NOTE_PRESETS_FORMAT = "cfa-review-note-presets-v1"
NOTE_LIMIT = 20000
REVIEW_EDITABLE_FIELDS = ("status", "note", "shotPlan", "likenessRating", "sceneQualityRating",
                          "storyboardStage", "variant", "workingReference", "workingReferenceScope",
                          "collectionState", "multiverseSelection", "creativeReview", "castUse")

st.set_page_config(page_title="Creative Studio | Stories & Visual Production", page_icon="🎬", layout="wide", initial_sidebar_state="auto")


def apply_theme() -> None:
    st.markdown("""<style>
    :root {--studio-ink:#edf0f5;--studio-accent:#d4b582;--studio-line:#38475b;
        --studio-font:system-ui,-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;}
    .stApp {background:#11151b;color:var(--studio-ink)!important;font-family:var(--studio-font);}
    .block-container {padding-top:2rem;max-width:1500px;padding-bottom:4rem;}
    .stApp p,.stApp label,.stApp button,.stApp input,.stApp textarea,.stApp select,
    h1,h2,h3,h4,h5,h6 {font-family:var(--studio-font)!important;}
    h1,h2,h3,h4,h5,h6 {color:var(--studio-ink);}
    .stApp [data-testid="stHeading"] :is(h1,h2,h3,h4,h5,h6) {color:#edf0f5!important;}
    h1 {letter-spacing:-.025em;line-height:1.15!important;}
    [data-testid="stHeader"] {background:#11151bf2;border-bottom:1px solid #2a333e;}
    [data-testid="stSidebar"] {background:#171d25;border-right:1px solid #2a333e;}
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"],
    [data-testid="stSidebar"] label,[data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3 {color:#edf0f5!important;}
    [data-testid="stCaptionContainer"],[data-testid="stCaptionContainer"] p {color:#a6b3c5!important;}
    .stApp [data-testid="stCaptionContainer"] {opacity:1!important;}
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] {color:#92a1b5!important;}
    [data-testid="stSidebarCollapseButton"] span {color:#edf0f5!important;}
    [data-testid="stSidebar"] button[kind="secondary"] {background:#1b222d;color:#edf0f5;border-color:#303b4b;text-align:left;}
    [data-testid="stSidebar"] button[kind="secondary"]:hover {background:#242e3b;border-color:#d2b37b;color:white;}
    [data-testid="stSidebar"] button[kind="primary"] {background:#d4b582;border-color:#d4b582;color:#15191e;}
    [data-testid="stSidebar"] button[kind="primary"] [data-testid="stMarkdownContainer"] {color:#15191e!important;}
    .st-key-mission-image-review {background:#16262c;border:1px solid #38515a;border-radius:12px;padding:1rem;}
    .st-key-mission-storyboard-review {background:#1a232e;border:1px solid #394859;border-radius:12px;padding:1rem;}
    [data-testid="stSidebar"] .stButton button {justify-content:flex-start;}
    /* Keep native controls readable while an existing Cloud session retains its previous theme. */
    .stApp :is(.stButton,.stDownloadButton,.stLinkButton,.stFormSubmitButton,[data-testid="stFileUploader"]) :is(button,a) {
        background:#1b232e!important;color:#edf0f5!important;border:1px solid #394453!important;}
    .stApp :is(.stButton,.stDownloadButton,.stLinkButton,.stFormSubmitButton,[data-testid="stFileUploader"]) :is(button,a) [data-testid="stMarkdownContainer"] {color:inherit!important;}
    .stApp :is(.stButton,.stDownloadButton,.stLinkButton,.stFormSubmitButton,[data-testid="stFileUploader"]) :is(button,a):is(:hover,:focus-visible):not(:disabled):not([aria-disabled="true"]) {
        background:#253345!important;color:#edf0f5!important;border-color:#d4b582!important;}
    .stApp :is(.stButton,.stDownloadButton,.stLinkButton,.stFormSubmitButton,[data-testid="stFileUploader"]) :is(button,a)[kind="primary"] {
        background:#d4b582!important;color:#15191e!important;border-color:#d4b582!important;}
    .stApp :is(.stButton,.stDownloadButton,.stLinkButton,.stFormSubmitButton,[data-testid="stFileUploader"]) :is(button,a)[kind="primary"]:is(:hover,:focus-visible):not(:disabled):not([aria-disabled="true"]) {
        background:#eed4a6!important;color:#15191e!important;border-color:#eed4a6!important;}
    [data-testid="stSidebar"] :is(.st-key-sidebar-home-ziggy,.st-key-sidebar-home-casa) button {
        border-color:#d4b582!important;}
    .stApp :is(.stButton,.stDownloadButton,.stLinkButton,.stFormSubmitButton,[data-testid="stFileUploader"]) :is(button,a):is(:disabled,[aria-disabled="true"]) {
        background:#171d25!important;color:#92a1b5!important;border-color:#303b4b!important;opacity:1;}
    .stApp [kind]:is(:disabled,[aria-disabled="true"]) [data-testid="stMarkdownContainer"] {color:inherit!important;}
    .stApp [data-testid="stMarkdownContainer"] a {color:#c7dbed;}
    .stApp [data-testid="stMarkdownContainer"] a:hover {color:#ffe2ae;}
    .stApp label,.stApp label [data-testid="stMarkdownContainer"],[data-testid="stHeader"] button {color:#edf0f5!important;}
    .stApp :is([data-baseweb="input"],[data-baseweb="base-input"],[data-baseweb="textarea"]),
    .stApp [data-baseweb="select"]>div {
        background:#1b232e!important;color:#edf0f5!important;border-color:#394453!important;}
    .stApp :is([data-baseweb="input"],[data-baseweb="base-input"],[data-baseweb="textarea"]) :is(input,textarea),
    .stApp [data-baseweb="select"] input {
        background:transparent!important;color:#edf0f5!important;-webkit-text-fill-color:#edf0f5!important;caret-color:#f5ca80;}
    .stApp :is(input,textarea)::placeholder {color:#92a1b5!important;-webkit-text-fill-color:#92a1b5!important;opacity:1;}
    .stApp [data-testid="InputInstructions"] {color:#a6b3c5!important;}
    .stApp [data-baseweb="select"] :is(div,span) {color:#edf0f5!important;}
    .stApp [data-baseweb="select"] svg {fill:#a6b3c5!important;}
    .stApp [data-baseweb="select"] [data-baseweb="tag"] {background:#303e4f!important;}
    .stApp :is([data-baseweb="input"],[data-baseweb="textarea"],[data-baseweb="select"]):focus-within {outline:2px solid #f5ca80;outline-offset:2px;}
    .stApp :is(input,textarea):disabled {color:#92a1b5!important;-webkit-text-fill-color:#92a1b5!important;}
    .stApp [data-testid="stNumberInput"] button {background:#1b232e!important;color:#edf0f5!important;}
    .stApp [data-testid="stFileUploaderDropzone"] {background:#1a2330!important;color:#edf0f5!important;border:1px dashed #56667c;}
    .stApp [data-testid="stFileUploaderDropzoneInstructions"] {color:#edf0f5!important;}
    .stApp [data-testid="stFileUploaderDropzoneInstructions"] :is(span,small) {color:#a6b3c5!important;}
    .stApp [data-testid="stFileUploaderDropzone"][aria-disabled="true"] {background:#171d25!important;color:#92a1b5!important;}
    .stApp [data-testid="stText"],.stApp [data-testid="stText"]>span {color:#edf0f5!important;}
    .stApp [data-testid="stMarkdownContainer"] {color:#edf0f5;}
    .stApp [data-testid="stCode"],.stApp [data-testid="stCode"] :is(pre,code) {background:#0d1725!important;color:#eef3fb!important;}
    [data-testid="stAlertContainer"] {background:#314964!important;color:#dcecff!important;}
    [data-testid="stAlertContainer"]:has([data-testid="stAlertContentSuccess"]) {background:#284c3e!important;color:#d1f0dd!important;}
    [data-testid="stAlertContainer"]:has([data-testid="stAlertContentWarning"]) {background:#55462f!important;color:#ffe3b0!important;}
    [data-testid="stAlertContainer"]:has([data-testid="stAlertContentError"]) {background:#59313e!important;color:#f6dae4!important;}
    [data-testid="stAlertContainer"] [data-testid="stMarkdownContainer"] {color:inherit!important;}
    /* Base Web dropdown menus render in a portal outside .stApp. */
    [data-baseweb="menu"],[role="listbox"],[role="option"],[data-baseweb="menu"] li {
        background:#1b232e!important;color:#edf0f5!important;}
    [data-baseweb="menu"] :is(div,span),[role="option"] :is(div,span) {color:inherit!important;}
    [role="option"]:is(:hover,:focus,[aria-selected="true"]),[data-baseweb="menu"] li:is(:hover,:focus,[aria-selected="true"]) {
        background:#303e4f!important;color:#ffe2ae!important;}
    [data-baseweb="menu"] [aria-disabled="true"],[role="option"][aria-disabled="true"] {color:#92a1b5!important;}
    [data-testid="stPopoverBody"],[data-baseweb="tooltip"] {background:#1a2330!important;color:#edf0f5!important;border-color:#394453!important;}
    .stApp [data-baseweb="tab-list"] {background:#11151b!important;}
    .stApp [data-baseweb="tab"] {background:#1a2330!important;color:#edf0f5!important;}
    .stApp [data-baseweb="tab"][aria-selected="true"] {background:#28303a!important;color:#ffe2ae!important;}
    .stApp [data-baseweb="tab"]:disabled {color:#92a1b5!important;}
    .stApp [data-baseweb="tab-highlight"] {background:#d4b582!important;}
    .stApp [data-baseweb="tab-border"] {background:#394453!important;}
    .stMarkdownBadge {background:#354255!important;color:#dce5f2!important;}
    [class*="st-key-mission-state-ready-"] {--mission-badge-background:#284c3e;--mission-badge-text:#d1f0dd;}
    [class*="st-key-mission-state-needs_input-"] {--mission-badge-background:#55462f;--mission-badge-text:#ffe3b0;}
    [class*="st-key-mission-state-in_progress-"] {--mission-badge-background:#314964;--mission-badge-text:#dcecff;}
    [class*="st-key-mission-state-done-"] {--mission-badge-background:#34463e;--mission-badge-text:#bed1c6;}
    [class*="st-key-mission-state-planned-"] {--mission-badge-background:#354255;--mission-badge-text:#dce5f2;}
    [class*="st-key-mission-state-"] [data-testid="stExpander"]>details>summary .stMarkdownBadge {
        background:var(--mission-badge-background)!important;color:var(--mission-badge-text)!important;}
    [data-testid="stExpander"]>details>summary {background:#1a2330!important;color:#edf0f5!important;}
    [data-testid="stExpander"]>details>summary [data-testid="stMarkdownContainer"] {color:inherit!important;}
    [data-testid="stExpander"]>details>summary:is(:hover,:focus-visible) {background:#253345!important;}
    .studio-hero {padding:1.5rem 1.75rem;background:#1a2330;border:1px solid #38475b;border-radius:10px;margin:0 0 1.7rem;color:#edf0f5;}
    .studio-hero .eyebrow {font-size:.75rem;letter-spacing:.16em;text-transform:uppercase;color:#d8b87f;margin-bottom:.7rem;}
    .studio-hero h1 {color:#edf0f5!important;margin:0!important;padding:0!important;font-size:clamp(2rem,4vw,2.7rem)!important;}
    .studio-hero p {margin:.65rem 0 0;color:#a9b7c9;max-width:760px;line-height:1.5;}
    .studio-label {font-size:.74rem;text-transform:uppercase;letter-spacing:.11em;color:#d2b37b;margin:.7rem 0 .3rem;}
    [data-testid="stImage"] img {border-radius:10px;}
    [data-testid="stExpander"] {background:#1a2330;border-radius:10px;}
    [data-testid="stExpander"]>details {border-color:#38475b;border-radius:10px;}
    [data-testid="stMetric"] {background:#1b2532;border:1px solid #3a4759;border-radius:10px;padding:1rem;min-height:6.6rem;}
    [data-testid="stMetricValue"] {color:#eed4a6;}
    [data-testid="stMetricLabel"] {color:#b6c6da;}
    .stApp .st-key-mission-shot-plans button {background:#1b2532!important;border:1px solid #3a4759!important;min-height:6.6rem;color:#eed4a6!important;font-size:1.1rem;}
    .st-key-mission-shot-plans button:hover {background:#253345;border-color:#d4b582;}
    .st-key-mission-priority {background:linear-gradient(135deg,#2b2240,#1e1c2d);border-radius:10px;}
    .st-key-mission-priority [data-testid="stExpander"] {background:transparent;}
    .st-key-mission-priority [data-testid="stExpander"]>details {border-color:#9678c8;}
    .st-key-mission-priority [data-testid="stExpander"]>details>summary {background:#2b2240!important;color:#f3e8ff!important;}
    .st-key-mission-priority [data-testid="stExpander"]>details>summary:is(:hover,:focus-visible) {background:#44315e!important;}
    .stButton button,.stDownloadButton button {border-radius:8px;}
    .stApp button[kind="primary"],.stApp button[kind="primary"] [data-testid="stMarkdownContainer"] {color:#15191e!important;}
    .stApp :is(button,a,input,textarea,select,summary):focus-visible {outline:3px solid #f5ca80!important;outline-offset:3px;}
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
                         ("studio_review_overrides", {}), ("studio_reviews", {}), ("studio_basket", set()),
                         ("studio_review_provenance", {}), ("studio_note_presets", [])):
        if key not in st.session_state:
            st.session_state[key] = default
    if st.session_state.studio_view == "Collaborator kits":
        st.session_state.studio_view = "Collaborator briefs"
    if st.session_state.studio_view == "Needs review":
        st.session_state.studio_view = "Review queue"
        st.session_state['review-queue-view'] = 'Review collections'


def navigate(view: str) -> None:
    if st.session_state.studio_view not in (CORNER, CASA, "Collaborators"):
        st.session_state.studio_return_view = st.session_state.studio_view
    if view == "Project home" and st.session_state.get("studio_project") == "criminal_mind":
        view = "Library"
    if view == 'Needs review':
        view = 'Review queue'
        st.session_state['review-queue-view'] = 'Review collections'
    elif view == 'Review queue':
        st.session_state['review-queue-view'] = 'Awaiting your decision'
    st.session_state.studio_view = view
    st.session_state.studio_selected = None
    st.session_state.pop("studio_mission_selected", None)
    st.session_state.pop("studio_mission_collection", None)
    st.session_state.pop("studio_mission_questionnaire", None)
    st.session_state.pop("studio_mission_task_focus", None)
    st.session_state.pop("studio_human_task_context", None)
    if view in (CORNER, CASA):
        data = st.session_state.get("studio_controller_data", {})
        routing = current_module("controller_routing")
        owner = "baldadoon" if view == CASA else "ziggy"
        owned = [p["id"] for p in data.get("projects", []) if routing.project_controller(data, p["id"]) == owner]
        if owned and st.session_state.get("studio_project") not in owned:
            st.session_state.studio_project = owned[0]
    if "studio_project" in st.session_state:
        st.session_state.studio_project_selection = st.session_state.studio_project
        st.query_params["project"] = st.session_state.studio_project
        st.query_params["view"] = {CORNER: "mission_control", CASA: "casa_baldadoon", "Project home": "project_home"}.get(view, view)
        st.session_state.studio_route_seen = (st.query_params.get("project"), st.query_params.get("view"))


def back_to_library() -> None:
    view = st.session_state.get("studio_return_view", "Library")
    navigate(view if view in VIEWS and view not in (CORNER, CASA, "Collaborators") else "Library")


def clear_selection() -> None:
    st.session_state.studio_selected = None
    st.session_state.pop("studio_mission_selected", None)


def clear_project_selection() -> None:
    clear_selection()
    st.session_state.pop("studio_mission_collection", None)
    st.session_state.pop("studio_mission_questionnaire", None)
    st.session_state.pop("studio_mission_task_focus", None)
    st.session_state.pop("studio_human_task_context", None)
    project = next((p for p in st.session_state.get("studio_controller_data", {}).get("projects", [])
                    if p["id"] == st.session_state.get("studio_project")), {})
    navigate("Project home" if project.get("landing") and project.get("id") != "criminal_mind" else "Library")


def select_asset(asset_id: str, project: str | None = None) -> None:
    if project is not None:
        st.session_state.studio_project = project
        st.session_state.studio_project_selection = project
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
    casting = st.session_state.get("studio_view") == CASA
    if casting:
        # A draft is not a human disposition. Keep it when reviewer attribution is
        # still missing, including after Streamlit removes an unmounted widget.
        st.session_state.setdefault("studio_casting_note_drafts", {})[asset_id] = st.session_state[key]
    if set_review_field(asset_id, "note", st.session_state[key]):
        st.session_state.studio_notes[asset_id] = st.session_state[key]
        if casting:
            st.session_state.studio_casting_note_drafts.pop(asset_id, None)


def read_note_presets(payload: dict) -> list[dict]:
    """Presets are reusable user text, never review decisions or source evidence."""
    if "notePresets" not in payload:
        return []
    envelope = payload["notePresets"]
    if not isinstance(envelope, dict) or envelope.get("format") != NOTE_PRESETS_FORMAT:
        raise ValueError("The saved-note preset format is not supported. Your session is unchanged.")
    rows = envelope.get("items")
    if not isinstance(rows, list) or len(rows) > 50:
        raise ValueError("A saved-note list can contain at most 50 presets.")
    result, seen = [], set()
    for row in rows:
        if (not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"]
                or row["id"] in seen or not isinstance(row.get("label"), str)
                or not row["label"].strip() or len(row["label"]) > 80
                or not isinstance(row.get("text"), str) or not row["text"].strip()
                or len(row["text"]) > NOTE_LIMIT):
            raise ValueError("A saved-note preset is invalid. Your session is unchanged.")
        result.append({key: row[key] for key in ("id", "label", "text")})
        seen.add(row["id"])
    return result


def merge_note_presets(existing: list[dict], incoming: list[dict]) -> list[dict]:
    result = [dict(row) for row in existing]
    for row in incoming:
        if any((old["label"], old["text"]) == (row["label"], row["text"]) for old in result):
            continue
        copy = dict(row)
        if any(old["id"] == copy["id"] for old in result):
            copy["id"] = "note-" + uuid4().hex
        result.append(copy)
    if len(result) > 50:
        raise ValueError("Import would exceed 50 note presets. Export your current list, then remove unused presets before importing.")
    return result


def complete_review_payload() -> dict:
    payload = review_payload(st.session_state.get("studio_export_assets", []), st.session_state.studio_reviews,
                             st.session_state.studio_favorites, st.session_state.studio_basket,
                             provenance=st.session_state.studio_review_provenance)
    payload["notePresets"] = {"format": NOTE_PRESETS_FORMAT,
                              "items": [dict(row) for row in st.session_state.studio_note_presets]}
    return payload


def export_review_button(context: str) -> None:
    st.download_button("Export review", json.dumps(complete_review_payload(), ensure_ascii=False, indent=2),
                       file_name="cfa-visual-review.json", mime="application/json", width="stretch",
                       key=f"export-review:{context}", help="Save decisions, notes, presets, plans, favorites and evidence from all projects.")


def seed_review_selections(data: dict) -> None:
    """Seed validated snapshot selections once; never undo this session's edits."""
    seed = data.get("reviewSessionSeed")
    if not isinstance(seed, dict) or not seed.get("id") or st.session_state.get("studio_selection_seed") == seed["id"]:
        return
    envelope = {"format": "cfa-visual-review-v1", "items": [], "favorites": seed.get("favorites", [])}
    _, favorites, _ = read_review(envelope, data["assets"], aliases=data.get("assetAliases", []))
    basket, _ = read_basket({"format": EXPORT_FORMAT, "items": seed.get("exportBasket", [])},
                            data["assets"], aliases=data.get("assetAliases", []))
    st.session_state.studio_favorites = set(st.session_state.studio_favorites) | favorites
    st.session_state.studio_basket = set(st.session_state.studio_basket) | basket
    st.session_state.studio_selection_seed = seed["id"]


def choose_note_preset(asset_id: str, select_key: str) -> None:
    preset_id = st.session_state[select_key]
    st.session_state[select_key] = ""
    preset = next((row for row in st.session_state.studio_note_presets if row["id"] == preset_id), None)
    if not preset:
        return
    note_key = f"asset-note:{asset_id}"
    before = st.session_state.get(note_key, st.session_state.studio_reviews.get(asset_id, {}).get("note", ""))
    after = before + ("\n" if before and not before.endswith("\n") else "") + preset["text"]
    if len(after) > NOTE_LIMIT:
        st.session_state.studio_preset_error = "That preset would exceed the 20,000-character note limit. Your note is unchanged."
        return
    st.session_state[note_key] = after
    save_note(asset_id, note_key)


def load_note_preset_editor() -> None:
    selected = st.session_state.get("preset-editor-id", "")
    row = next((row for row in st.session_state.studio_note_presets if row["id"] == selected), {})
    st.session_state["preset-editor-label"] = row.get("label", "")
    st.session_state["preset-editor-text"] = row.get("text", "")


def use_current_note(asset_id: str) -> None:
    st.session_state["preset-editor-id"] = ""
    st.session_state["preset-editor-label"] = ""
    st.session_state["preset-editor-text"] = st.session_state.get(f"asset-note:{asset_id}", "")


def save_note_preset() -> None:
    preset_id = st.session_state.get("preset-editor-id", "")
    label = st.session_state.get("preset-editor-label", "").strip()
    text = st.session_state.get("preset-editor-text", "").strip()
    rows = st.session_state.studio_note_presets
    if not text or len(text) > NOTE_LIMIT or len(label) > 80:
        st.session_state.studio_preset_error = "Enter preset text of 1–20,000 characters and a name of at most 80 characters."
        return
    if not preset_id and len(rows) >= 50:
        st.session_state.studio_preset_error = "You have 50 presets. Edit or delete one to make room."
        return
    if preset_id and not any(row["id"] == preset_id for row in rows):
        st.session_state.studio_preset_error = "That preset is no longer available. Choose New preset."
        return
    row = {"id": preset_id or "note-" + uuid4().hex, "label": label or " ".join(text.split())[:60], "text": text}
    st.session_state.studio_note_presets = [row if old["id"] == preset_id else old for old in rows] if preset_id else [*rows, row]
    st.session_state["preset-editor-id"] = row["id"]
    st.session_state.studio_flash = "Preset saved in this session. Export your review to keep it."


def delete_note_preset() -> None:
    selected = st.session_state.get("preset-editor-id", "")
    st.session_state.studio_note_presets = [row for row in st.session_state.studio_note_presets if row["id"] != selected]
    st.session_state["preset-editor-id"] = ""
    load_note_preset_editor()


def clear_note_presets() -> None:
    st.session_state.studio_cleared_presets = st.session_state.studio_note_presets
    st.session_state.studio_note_presets = []
    st.session_state["preset-editor-id"] = ""
    load_note_preset_editor()


def undo_clear_note_presets() -> None:
    try:
        restored = merge_note_presets(st.session_state.studio_note_presets,
                                     st.session_state.get("studio_cleared_presets", []))
    except ValueError as error:
        st.session_state.studio_preset_error = str(error)
        return
    st.session_state.studio_note_presets = restored
    st.session_state.pop("studio_cleared_presets", None)


def render_note_presets(asset_id: str) -> None:
    rows = st.session_state.studio_note_presets
    names = {row["id"]: row["label"] for row in rows}
    insert_key = f"preset-insert:{asset_id}"
    st.selectbox("Add a saved note", ["", *names], format_func=lambda value: names.get(value, "Choose a preset…"),
                 key=insert_key, disabled=not rows, on_change=choose_note_preset, args=(asset_id, insert_key))
    if message := st.session_state.pop("studio_preset_error", None):
        st.warning(message)
    with st.expander("Manage note presets", expanded=False):
        st.caption("Choosing a preset appends its text to your note. Editing or clearing presets leaves applied notes intact. Export your review to keep this list between sessions.")
        if st.session_state.get("preset-editor-id", "") not in ["", *names]:
            st.session_state["preset-editor-id"] = ""
        st.selectbox("Create or edit", ["", *names], format_func=lambda value: names.get(value, "New preset"),
                     key="preset-editor-id", on_change=load_note_preset_editor)
        st.button("Use current note as a starting point", key="preset-from-note", on_click=use_current_note, args=(asset_id,))
        st.text_input("Short name (optional)", key="preset-editor-label", max_chars=80)
        st.text_area("Preset text", key="preset-editor-text", height=100, max_chars=NOTE_LIMIT)
        left, right = st.columns(2)
        left.button("Save preset", key="preset-save", on_click=save_note_preset, width="stretch")
        right.button("Delete preset", key="preset-delete", on_click=delete_note_preset,
                     disabled=not st.session_state.get("preset-editor-id"), width="stretch")
        st.button("Clear list", key="presets-clear", on_click=clear_note_presets, disabled=not rows)
        if st.session_state.get("studio_cleared_presets"):
            st.button("Undo clear", key="presets-undo", on_click=undo_clear_note_presets)


def set_review_field(asset_id: str, field: str, value) -> bool:
    now = datetime.now(timezone.utc).isoformat()
    attribution = {}
    data = st.session_state.get("studio_controller_data")
    if data:
        routing = current_module("controller_routing")
        asset = next((a for a in st.session_state.get("studio_export_assets", []) if a["id"] == asset_id), None)
        if not asset:
            st.session_state.studio_flash = "This review's source is not in the current snapshot. No decision was changed."
            return False
        owner = routing.project_controller(data, asset["project"])
        task = next((t for t in data.get("missionControl", {}).get("tasks", [])
                     if t.get("id") == st.session_state.get("studio_human_task_context")), None)
        try:
            attribution = routing.human_action(data, asset,
                st.session_state.get("human-actor:" + owner, "ziggy" if owner == "ziggy" else None),
                st.session_state.get("human-scope:" + asset_id, "project_decision" if owner == "ziggy" else None),
                [field], now, task)
        except ValueError as error:
            st.session_state.studio_flash = str(error)
            return False
        prior_record = {**st.session_state.studio_reviews.get(asset_id, {}),
                        **st.session_state.studio_review_overrides.get(asset_id, {})}
        touched = st.session_state.setdefault("studio_human_review_touched", set())
        if prior_record and (asset_id not in touched or any(prior_record.get(key) != attribution.get(key)
                for key in ("reviewerControllerID", "decisionScope"))):
            snapshot = {**prior_record, "id": asset_id, "sha256": asset.get("sha256")}
            st.session_state.studio_review_provenance = current_module("library_helpers").review_provenance(
                {"items": [snapshot]}, st.session_state.get("studio_review_provenance", {}))
        touched.add(asset_id)
    record = st.session_state.studio_review_overrides.setdefault(asset_id, {})
    record[field] = value
    record.update(attribution)
    record["updatedAt"] = now
    record["origin"] = "user"
    prior = st.session_state.studio_reviews.get(asset_id, {})
    prior_dates = prior.get("fieldUpdatedAt", {})
    current_dates = record.get("fieldUpdatedAt", {})
    dates = {**(prior_dates if isinstance(prior_dates, dict) else {}),
             **(current_dates if isinstance(current_dates, dict) else {})}
    for old_field in REVIEW_EDITABLE_FIELDS:
        if old_field in prior and old_field not in dates and isinstance(prior.get("updatedAt"), str):
            dates[old_field] = prior.get(old_field + "UpdatedAt") or prior["updatedAt"]
    dates[field] = now
    record["fieldUpdatedAt"] = dates
    st.session_state.pop("studio_basket_zip", None)
    return True


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
                           "outputKind": st.session_state.get(f"plan-outputKind:{asset_id}", "unspecified"),
                           "idea": st.session_state[f"plan-idea:{asset_id}"],
                           "prompt": st.session_state[f"plan-prompt:{asset_id}"]})
    if not set_review_field(asset_id, "shotPlan", plan):
        return
    st.session_state[f"plan-destinations:{asset_id}"] = plan["destinations"]
    st.session_state.studio_flash = "Shot plan saved in this session. Export it from Shot plans or Favorites & notes."


def remove_shot_plan(asset_id: str) -> None:
    if not set_review_field(asset_id, "shotPlan", None):
        return
    for field in ("destinations", "outputKind", "idea", "prompt"):
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
    if not set_review_field(asset_id, "shotPlan", plan):
        return
    st.session_state[f"plan-destinations:{asset_id}"] = plan["destinations"]


def render_collaborator_controls(asset: dict) -> None:
    plan = st.session_state.studio_reviews.get(asset["id"], {}).get("shotPlan") or {}
    destinations = plan.get("destinations", [])
    st.markdown("**Collaborator**")
    for column, provider in zip(st.columns(4), ("Flow", "Grok", "grok_video", "Gemini")):
        with column:
            selected = provider in destinations
            st.button(("✓ " if selected else "") + destination_label(provider), key=f"collaborator:{asset['id']}:{provider}",
                      type="primary" if selected else "secondary", width="stretch",
                      on_click=toggle_collaborator, args=(asset["id"], provider), disabled=bool(asset.get("archived")))
    queued = [destination_label(provider) for provider in ("Flow", "Grok", "grok_video", "Gemini") if provider in destinations]
    if queued:
        st.caption(f"Queued for {', '.join(queued)} — draft not sent.")
    else:
        st.caption("Choose a collaborator to queue a draft locally. Add the idea or prompt under Plan a shot.")


def cast_control_state(asset: dict, data: dict) -> dict:
    reviews = dict(st.session_state.studio_reviews)
    reviews[asset['id']] = {**reviews.get(asset['id'], {}), **st.session_state.studio_review_overrides.get(asset['id'], {})}
    return cast_use_state(data, asset, reviews)


def save_cast_field(asset: dict, data: dict, field: str, key: str) -> None:
    value = cast_control_state(asset, data)['value']
    value[field] = st.session_state[key]
    set_review_field(asset['id'], 'castUse', value)


def add_cast_link(asset: dict, data: dict, story_id: str, shot_id: str) -> None:
    state = cast_control_state(asset, data)
    if not any(row['storyID'] == story_id and row['shotID'] == shot_id for row in state['targets']):
        st.session_state.studio_flash = 'Choose an existing shot in this project before linking.'
        return
    value = state['value']
    link = dict(storyID=story_id, shotID=shot_id)
    if not any(row['storyID'] == story_id and row['shotID'] == shot_id for row in value['storyboardLinks']):
        value['storyboardLinks'] = [*value['storyboardLinks'], link]
    value['storyboardPlanned'] = True
    if set_review_field(asset['id'], 'castUse', value):
        st.session_state['cast-planned:'+asset['id']] = True


def remove_cast_link(asset: dict, data: dict, story_id: str, shot_id: str) -> None:
    value = cast_control_state(asset, data)['value']
    value['storyboardLinks'] = [row for row in value['storyboardLinks']
                               if (row['storyID'], row['shotID']) != (story_id, shot_id)]
    set_review_field(asset['id'], 'castUse', value)


def render_cast_controls(asset: dict, data: dict) -> None:
    state = cast_control_state(asset, data)
    if not state['editable']: return
    aid = asset['id']
    with st.expander('Character role & storyboard use', expanded=False):
        st.caption('Choose this exact version for a role or storyboard. These choices do not change its score or technical approval.')
        for key, default in [('cast-role-selected:'+aid, state['roleSelected']), ('cast-role:'+aid, state['role']),
                             ('cast-planned:'+aid, state['storyboardPlanned'])]:
            if st.session_state.get(key) != default: st.session_state[key] = default
        st.checkbox('Use this version for a character role', key='cast-role-selected:'+aid,
                    on_change=save_cast_field, args=(asset, data, 'roleSelected', 'cast-role-selected:'+aid))
        st.text_input('Character role', key='cast-role:'+aid, max_chars=300,
                      on_change=save_cast_field, args=(asset, data, 'role', 'cast-role:'+aid))
        if state['sourceSelected']:
            st.caption('Recorded source choice: '+(state['sourceRole'] or 'selected character version')+'. Your current choice is stored separately.')
        st.checkbox('Plan this version for storyboard', key='cast-planned:'+aid,
                    on_change=save_cast_field, args=(asset, data, 'storyboardPlanned', 'cast-planned:'+aid))
        st.caption('Existing authored plans and links remain recorded. A linked shot also counts as planned use. Plan a shot below remains a separate generation draft.')
        targets = {(row['storyID'], row['shotID']): row for row in state['targets']}
        if state['storyboardLinks']:
            st.markdown('**Your storyboard links**')
            for index, link in enumerate(state['storyboardLinks']):
                target = targets.get((link['storyID'], link['shotID']))
                label = (target['storyTitle']+' · '+target['shotID']+' · '+target['shotTitle']) if target else link['storyID']+' · '+link['shotID']+' · unresolved'
                st.write(label)
                st.button('Remove this link', key=f'cast-unlink:{aid}:{index}',
                          on_click=remove_cast_link, args=(asset, data, link['storyID'], link['shotID']))
        if state['unresolvedLinks']:
            st.warning('Unresolved links are saved for review, but do not count as storyboard-linked.')
        stories = {row['storyID']: row['storyTitle'] for row in state['targets']}
        if not stories:
            st.caption('No registered storyboard shots are available in this project yet.')
            return
        story_key, shot_key = 'cast-link-story:'+aid, 'cast-link-shot:'+aid
        if st.session_state.get(story_key) not in {None, *stories}: st.session_state[story_key] = None
        story_id = st.selectbox('Link to a storyboard', [None, *stories],
            format_func=lambda value: 'Choose a story' if value is None else stories[value], key=story_key)
        shots = {row['shotID']: row['shotTitle'] for row in state['targets'] if row['storyID'] == story_id}
        if st.session_state.get(shot_key) not in {None, *shots}: st.session_state[shot_key] = None
        shot_id = st.selectbox('Storyboard shot', [None, *shots],
            format_func=lambda value: 'Choose a shot' if value is None else value+' · '+shots[value], key=shot_key,
            disabled=not story_id)
        st.button('Link this version to shot', key='cast-link-add:'+aid, disabled=not story_id or not shot_id,
                  on_click=add_cast_link, args=(asset, data, story_id, shot_id))


def render_human_review_identity(asset: dict, data: dict | None = None) -> None:
    asset_id = asset["id"]
    if data is not None:
        routing = current_module("controller_routing")
        owner = routing.project_controller(data, asset["project"])
        people = routing.controllers(data)
        actor_key, scope_key = "human-actor:" + owner, "human-scope:" + asset_id
        if actor_key not in st.session_state:
            st.session_state[actor_key] = "ziggy" if owner == "ziggy" else None
        st.selectbox("Recording review as", [None, *people], key=actor_key,
                     format_func=lambda who: "Choose the actual reviewer" if who is None else people[who]["name"])
        task = next((t for t in data.get("missionControl", {}).get("tasks", [])
                     if t.get("id") == st.session_state.get("studio_human_task_context") and routing.task_contains_asset(t, asset)), None)
        scopes = ["asset_review", "project_decision", "story", "scene", "character", "location", "reference", "technical_assistance"]
        if task and task.get("decisionScope") and task["decisionScope"] not in scopes:
            scopes.append(task["decisionScope"])
        if scope_key not in st.session_state:
            st.session_state[scope_key] = task.get("decisionScope") if task else ("project_decision" if owner == "ziggy" else None)
        st.selectbox("Decision scope", [None, *scopes], key=scope_key,
                     format_func=lambda scope: "Choose the scope" if scope is None else scope.replace("_", " "))
        st.caption("Project controller: " + people[owner]["name"] + ". Reviewer attribution is a declared identity in this shared app, not a separate authenticated login.")


def render_review_controls(asset: dict, data: dict | None = None) -> None:
    asset_id = asset["id"]
    decision = st.session_state.studio_reviews.get(asset_id, {})
    archived = bool(asset.get("archived"))
    status = decision.get("status")
    render_human_review_identity(asset, data)
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
        st.session_state[note_key] = st.session_state.get("studio_casting_note_drafts", {}).get(asset_id, decision.get("note", "")) if st.session_state.get("studio_view") == CASA else decision.get("note", "")
    st.text_area("Your review note", key=note_key, height=130, max_chars=NOTE_LIMIT, on_change=save_note, args=(asset_id, note_key),
                 placeholder="What works here? What should change in the next pass?")
    if st.session_state.get("studio_view") == CASA and asset_id in st.session_state.get("studio_casting_note_drafts", {}):
        st.caption("Draft note retained. Choose the reviewer and scope, then save it to include it in your export.")
        st.button("Save review note", key="casa-save-note:" + asset_id, on_click=save_note, args=(asset_id, note_key))
    render_note_presets(asset_id)
    if st.session_state.get("studio_view") != CASA or asset.get("role") != "casting_option":
        export_review_button("selected:" + asset_id)
    st.caption("Review choices and saved-note presets stay in this session. Export before closing or reloading; import the file under Favorites & notes to resume.")
    if data is not None:
        render_cast_controls(asset, data)
    with st.expander("Scores (optional)", expanded=False):
        for field, label in (("likenessRating", "Character score"), ("sceneQualityRating", "Scene craft score")):
            rating_key = f"{field}:{asset_id}"
            if rating_key not in st.session_state:
                st.session_state[rating_key] = decision.get(field)
            st.selectbox(label, [None, 1, 2, 3, 4, 5], format_func=lambda value: "Unrated" if value is None else str(value),
                         key=rating_key, on_change=lambda aid=asset_id, f=field, k=rating_key: set_review_field(aid, f, st.session_state[k]))
        st.caption("Scores and image validation are separate assessments.")
    plan = decision.get("shotPlan")
    with st.expander("Plan a shot", expanded=False):
        st.caption("Save a draft for Gemini, Flow, Grok stills, Grok video, or ComfyUI. This does not send a request or generate media.")
        defaults = {"destinations": ["undecided"], "outputKind": "unspecified", "idea": "", "prompt": "", **(plan or {})}
        for field in ("destinations", "outputKind", "idea", "prompt"):
            key = f"plan-{field}:{asset_id}"
            if key not in st.session_state:
                st.session_state[key] = defaults[field]
        with st.form(f"shot-plan:{asset_id}"):
            st.selectbox("Output kind", OUTPUT_KINDS, format_func=output_kind_label, key=f"plan-outputKind:{asset_id}")
            st.multiselect("Destination", DESTINATIONS, format_func=destination_label, key=f"plan-destinations:{asset_id}")
            st.text_area("Shot idea", key=f"plan-idea:{asset_id}", height=100,
                         placeholder="What should happen in this shot? What must stay the same?")
            st.text_area("Prompt draft", key=f"plan-prompt:{asset_id}", height=150)
            st.form_submit_button("Save shot plan", on_click=save_shot_plan, args=(asset_id,), width="stretch")
        if plan:
            st.caption(output_kind_label(plan.get("outputKind")) + " · Planned for " + ", ".join(map(destination_label, plan["destinations"])) + " · not sent")
            st.button("Remove shot plan", key=f"remove-plan:{asset_id}", on_click=remove_shot_plan, args=(asset_id,))
    render_collaborator_controls(asset)
    with st.expander("Archive", expanded=False):
        st.button("Restore from Archive" if archived else "Archive", key=f"archive:{asset_id}",
                  on_click=set_review_field, args=(asset_id, "collectionState", "working" if archived else "archived"), width="stretch")
        st.caption("Archive keeps this file and its review while hiding it from ordinary browsing. Restore brings it back; any removal flag remains separate.")
    variant = decision.get("variant", asset.get("variant", "prime"))
    with st.expander("Reference lane & working-reference request"):
        st.caption(f"Current lane: {'Multiverse' if variant == 'multiverse' else 'Prime'}")
        for column, label, value in zip(st.columns(2), ("Prime", "Multiverse"), ("prime", "multiverse")):
            with column:
                st.button(label, key=f"variant:{asset_id}:{value}", on_click=set_variant, args=(asset_id, value),
                          type="primary" if variant == value else "secondary", width="stretch")
        if variant == "multiverse":
            selected = decision.get("multiverseSelection") == "approved"
            score = decision.get("likenessRating") or 0
            st.caption("Approved Multiverse" if approved_multiverse(asset, st.session_state.studio_reviews) else "Multiverse candidate")
            st.button("Return to candidates" if selected else "Approve for Multiverse use", key=f"multiverse-selection:{asset_id}",
                      disabled=not selected and (score < 2 or archived or status == "remove"),
                      on_click=set_review_field, args=(asset_id, "multiverseSelection", "candidate" if selected else "approved"))
            st.caption("Choose the usable subset explicitly. Character scores of 2–5 qualify; a score alone never approves a candidate.")
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
    view = "Accessories" if view == "Tattoos & piercings" else view
    if view == "Comfy swap targets":
        st.markdown(f'<div class="studio-hero"><div class="eyebrow">CFA · {html.escape(project["name"])}</div>'
                    '<h1>Comfy results &amp; swap targets</h1>'
                    '<p>Results first, with the source likenesses and technical inputs used for swaps. '
                    'Character, mouth and grill references stay in Working references.</p></div>', unsafe_allow_html=True)
        return
    visuals = [a for a in assets if a.get("kind") in VISUAL_KINDS and normal_visible(a, st.session_state.studio_reviews)]
    videos = sum(a.get("kind") == "video" for a in visuals)
    captions = {
        "Library": "Explore the looks, compare the details, and keep the references you want to return to.",
        "Storyboard": "Follow the story in pictures. Open a panel for its beat, lyric connection, and review notes.",
        "Collaborator briefs": "Instructions, references, and current care packages for Gemini, Flow, and Grok.",
        "Favorites & notes": "Your working shortlist. Export it to keep your choices and carry them between review sessions.",
        "Review queue": "Answer review requests or browse the earlier review collections. Saved removal decisions are in Archive.",
        "Archive": "Saved removal decisions and archived references. These remain separate choices; your notes and original files are retained.",
        "Shot plans": "Turn references into draft shots, then export a handoff for Gemini, Flow, or Grok.",
        "Export basket": "Choose references to take with you. The basket is separate from favorites and review decisions.",
        "Documents": "The supporting notes behind the pictures, grouped so the useful details are easy to find.",
    }
    subtitle = project.get("subtitle", "")
    st.markdown(f'<div class="studio-hero"><div class="eyebrow">CFA · Creative Studio · {html.escape(view)}</div>'
                f'<h1>{html.escape(project["name"])}</h1><p>{html.escape(subtitle)} · '
                f'{len(visuals) - videos} pictures · {videos} clips</p><p>{html.escape(captions.get(view, "Open a collection to explore its references and keep your review choices."))}</p></div>', unsafe_allow_html=True)


def favorite_button(asset: dict, context: str = "card") -> None:
    chosen = asset["id"] in st.session_state.studio_favorites
    st.button("★ Saved" if chosen else "☆ Save", key=f"favorite:{context}:{asset['id']}",
              help="Add to your review shortlist. This does not change the source's approval status.",
              on_click=toggle_favorite, args=(asset["id"],), width="stretch", disabled=bool(asset.get("archived")))


def render_selected(asset: dict, intake: dict | None = None, data: dict | None = None) -> None:
    if st.session_state.get("studio_mission_questionnaire") != "grok-proof-package":
        st.button("← Back to the collection", on_click=clear_selection)
    if st.session_state.studio_view in ("Intake verification", "intake"):
        sequence = st.session_state.get("studio_intake_sequence", [])
        if asset["id"] in sequence:
            position = sequence.index(asset["id"])
            previous, progress, following = st.columns([2, 3, 2])
            previous.button("← Previous image", key="intake-selected-prev", disabled=position == 0,
                            on_click=select_asset, args=(sequence[max(0, position - 1)],), width="stretch")
            progress.caption(f"Image {position + 1} of {len(sequence)} in this batch")
            following.button("Next image →", key="intake-selected-next", disabled=position == len(sequence) - 1,
                             on_click=select_asset, args=(sequence[min(len(sequence) - 1, position + 1)],), width="stretch")
    st.subheader(asset.get("title", asset["filename"]))
    if asset.get("archived"):
        st.info("Archived from regular browsing and exports. This entry remains available for review bookkeeping.")
    if asset.get("kind") in {"document", "pdf"}:
        if asset.get("text"):
            st.text(asset["text"])
        document_download(asset, context="selected")
        render_human_review_identity(asset, data)
        st.button("Restore from Archive" if asset.get("archived") else "Archive", key=f"archive:{asset['id']}",
                  on_click=set_review_field, args=(asset["id"], "collectionState", "working" if asset.get("archived") else "archived"))
        return
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
        render_review_controls(asset, data)
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
        if intake:
            current_module("review_intake_view").render_asset_evidence(intake, asset)
        with st.expander("Reference details"):
            st.write(f"Reference: {asset['id']}")
            if asset.get("sceneID"):
                st.write(f"Scene: {asset['sceneID']}")
            if asset.get("duration") is not None:
                st.write(f"Clip length: {asset['duration']:g} seconds")
            if asset.get("tags"):
                st.write(" · ".join(str(tag) for tag in asset["tags"]))
            st.caption("Saved selections are review choices; they do not replace the project's reference instructions.")


def render_card(asset: dict, context: str = "card") -> None:
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
            st.caption("Approved Multiverse" if approved_multiverse(asset, st.session_state.studio_reviews) else "Multiverse candidate")
        if decision.get("likenessRating") is not None:
            st.caption(f"Character · {decision['likenessRating']}/5")
        if decision.get("status"):
            st.caption(STATUS_LABELS[decision["status"]])
        if decision.get("shotPlan"):
            st.caption(output_kind_label(decision["shotPlan"].get("outputKind")) + " · Shot planned · " + ", ".join(map(destination_label, decision["shotPlan"]["destinations"])))
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
                      key=f"open:{asset['id']}" if context == "card" else f"open:{context}:{asset['id']}", on_click=select_asset, args=(asset["id"], asset["project"]), width="stretch")
        with c2:
            favorite_button(asset, context)
        basket_button(asset, context)


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
                    render_card(asset, signature if signature.startswith(("design:", "story:")) else "card")
        index = end
    if count > PAGE_SIZE:
        st.caption("Use the page controls above to continue through this collection.")


def render_library(data: dict, project: str, storyboard: bool = False, fixed_category: str | None = None) -> None:
    if project == "criminal_mind" and not storyboard and not fixed_category:
        render_all_files(data, project)
        return
    albums = [a for a in data["albums"] if a.get("project") == project]
    if storyboard:
        category = "storyboard"
        matching = [a for a in albums if a.get("category") == category]
        st.caption("Panel sequence and story notes are planning references. No song timing is implied.")
    elif fixed_category:
        category = fixed_category
        matching = [a for a in albums if a.get("category") == category]
    else:
        available = {a.get("category") for a in albums}
        options = ["all"] + [key for key, _ in data["categories"] if key in available]
        labels = {"all": "All pictures & clips", **dict(data["categories"])}
        category = st.selectbox("Explore", options, format_func=lambda key: labels.get(key, key),
                                key=f"category:{project}", on_change=clear_selection)
        matching = [a for a in albums if category == "all" or a.get("category") == category]
        if data.get("designSnapshot") and category in {"working", "outfits", "details", "cast", "comfy"}:
            render_design_workspace(data, project, category)
            return
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
    if project == "criminal_mind" and category == "all" and album_id == "all":
        # Start the visual library with the people; script records remain below it.
        results = sorted(results, key=lambda row: row[0].get("category") != "cast")
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


def set_all_files_sections(keys, expanded):
    for key in keys:
        st.session_state[key] = expanded


def set_all_files_open(key, expanded):
    st.session_state[key] = expanded


def render_all_files(data, project):
    """Purpose and collection browsing; existing leaf controls own all reviews."""
    query = st.text_input("Find a picture or moment", placeholder="Search characters, sets, outfits…",
                          key=f"all-files-search:{project}", on_change=clear_selection)
    model = current_module("design_view").all_files_model(data, project, st.session_state.studio_reviews, query)
    labels = dict(model["choices"])
    purpose_key = f"all-files-purpose:{project}"
    if st.session_state.get(purpose_key, "all") not in labels:
        st.session_state[purpose_key] = "all"
    purpose = st.radio("Purpose", list(labels), format_func=labels.get, horizontal=True, key=purpose_key,
                       on_change=clear_selection)
    sections = [s for s in model["sections"] if s["groups"] and purpose in {"all", s["id"]}]
    if not sections:
        if query:
            st.info("No references match this search in " + labels[purpose] + ".")
        elif purpose == "all":
            st.info("No visual collections have been added yet.")
        elif purpose == "outfits":
            st.info("No outfit collections have been added yet.")
        else:
            st.info("No collections have been added for " + labels[purpose] + " yet.")
        return
    search_scope = hashlib.sha256(query.encode("utf-8")).hexdigest()[:12]
    context = f"all-files:{project}:{search_scope}"
    section_keys = [context + ":section:" + section["id"] for section in sections]
    expand, collapse, _ = st.columns([2, 2, 5])
    expand.button("Expand sections", key=context + ":expand", on_click=set_all_files_sections,
                  args=(section_keys, True), width="stretch")
    collapse.button("Collapse sections", key=context + ":collapse", on_click=set_all_files_sections,
                    args=(section_keys, False), width="stretch")
    for section, section_key in zip(sections, section_keys):
        opened = st.session_state.get(section_key, True)
        with st.container(border=True):
            st.button(("▾ " if opened else "▸ ") + section["title"] + f" · {section['count']}",
                      key=section_key + ":toggle", on_click=set_all_files_open, args=(section_key, not opened),
                      width="stretch")
            if not opened:
                continue
            groups = section["groups"]
            for start in range(0, len(groups), 3):
                expanded_groups = []
                for column, group in zip(st.columns(3), groups[start:start + 3]):
                    group_key = section_key + ":collection:" + group["id"]
                    group_open = st.session_state.get(group_key, bool(query))
                    with column, st.container(border=True):
                        if not group_open:
                            cover = model["assets"][group["coverID"]]
                            if cover.get("kind") in VISUAL_KINDS and (preview := media_path(LIBRARY_DIR, cover.get("thumb") or cover.get("src"))):
                                st.image(str(preview), width="stretch")
                        st.markdown("**" + group["title"] + "**")
                        st.caption(str(len(group["assetIDs"])) + " references")
                        st.button("Hide references" if group_open else "Show references", key=group_key + ":toggle",
                                  on_click=set_all_files_open, args=(group_key, not group_open), width="stretch")
                    if group_open:
                        expanded_groups.append((group, group_key))
                for group, group_key in expanded_groups:
                    st.subheader(group["title"])
                    if group["description"]:
                        st.caption(group["description"])
                    rows = [(model["assets"][aid], None) for aid in group["assetIDs"]]
                    visuals = [(asset, album) for asset, album in rows if asset.get("kind") in VISUAL_KINDS]
                    if visuals:
                        render_grid(visuals, "design:" + group_key)
                    for asset, _ in rows:
                        if asset.get("kind") in {"document", "pdf"}:
                            st.button(asset.get("title", asset["id"]), key=group_key + ":document:" + asset["id"],
                                      on_click=select_asset, args=(asset["id"], project), width="stretch")


def render_design_workspace(data: dict, project: str, view: str) -> None:
    comfy = view == "Comfy swap targets"
    query = st.text_input("Find a Comfy result or target" if comfy else "Find a reference", key=f"design-search:{project}:{view}",
                          placeholder="Search results, targets, guides…" if comfy else "Search names, details, outfits…", on_change=clear_selection)
    current_module("design_view").render_design_view(
        data, project, view, LIBRARY_DIR, render_grid,
        lambda asset: select_asset(asset["id"], asset["project"]),
        reviews=st.session_state.studio_reviews, query=query, navigate=navigate)
    if view == "Tattoos & piercings":
        current_module("review_intake_view").render_golden_references(
            data, project, query, LIBRARY_DIR,
            select_asset,
            reviews=st.session_state.studio_reviews)


def render_needs_review(data: dict, project: str) -> None:
    query = st.text_input("Find a review collection or reference", key=f"needs-review-search:{project}")
    albums = [album for album in data['albums'] if album.get('project') == project and album.get('category') == 'review']
    labels = {'all': 'All review collections', **{album['id']: album['title'] for album in albums}}
    selected = st.selectbox('Review collection', list(labels), format_func=lambda value: labels[value],
                            key=f'review-collection:{project}')
    results = ordered_assets(data['assets'], data['albums'], project, category='review', album_id=selected, query=query)
    collections = {album['id'] if album else asset.get('album') or 'ungrouped' for asset, album in results}
    st.caption(f"{len(collections)} collections · {len(results)} references. Earlier batches keep their original groupings and saved decisions.")
    render_grid(results, f"needs-review:{project}:{selected}:{query}")


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
    if asset.get("textPreviewOnly") is True:
        if source:
            st.download_button("Download complete document", source.read_bytes(),
                               file_name=asset.get("downloadFilename", asset.get("filename", source.name)),
                               mime="text/plain", key=f"{context}-download:{asset['id']}")
        else:
            st.caption("The complete document is unavailable in this bundle; the text above is only a preview.")
    elif text:
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
        st.subheader(f"{provider} · {len(documents)} documents")
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
                    count = navigation_reference_count(data['assets'], workflow['documentAssetIDs'], documents=True)
                    st.markdown(f"**Workflow files and instructions · {count} documents**")
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
    payload = complete_review_payload()
    export_col, import_col = st.columns(2, gap="large")
    with export_col:
        st.markdown("**Keep your review**")
        st.write("Export includes review decisions, notes, saved-note presets, shot plans, favorites, and the export basket from all projects. Save it before closing this session.")
        st.download_button("Export complete review", json.dumps(payload, ensure_ascii=False, indent=2),
                           file_name="cfa-visual-review.json", mime="application/json", width="stretch")
        st.caption(f"{len(payload['items'])} review records · {len(payload['favorites'])} favorites across all projects")
    with import_col:
        st.markdown("**Bring a review back**")
        uploaded = st.file_uploader("Review or favorites JSON", type=["json"], key="favorites-upload")
        if uploaded is not None and st.button("Add this review to my session", width="stretch"):
            try:
                if uploaded.size > 50 * 1024 * 1024:
                    raise ValueError("Choose a review file no larger than 50 MiB.")
                imported = json.loads(uploaded.getvalue())
                aliases = data.get("assetAliases", [])
                reviews, accepted, skipped = read_review(imported, data["assets"], aliases=aliases)
                basket, basket_skipped = read_basket({"format": EXPORT_FORMAT, "items": imported["exportBasket"]}, data["assets"], aliases=aliases) if "exportBasket" in imported else (set(), 0)
                presets = merge_note_presets(st.session_state.studio_note_presets, read_note_presets(imported))
                provenance = review_provenance(imported, st.session_state.studio_review_provenance)
                overrides = merge_review_overrides(st.session_state.studio_review_overrides, reviews, data["assets"], aliases=aliases)
                # Validate every independent part before changing the live session.
                st.session_state.studio_review_provenance = provenance
                st.session_state.studio_note_presets = presets
                st.session_state.studio_basket = set(st.session_state.studio_basket) | basket
                st.session_state.pop("studio_basket_zip", None)
                st.session_state.studio_favorites = set(st.session_state.studio_favorites) | accepted
                st.session_state.studio_review_overrides = overrides
                for key in list(st.session_state):
                    if key.startswith("return-answer:") or key in {"return-direction", "return-direction-note", "return-direction-asset"}:
                        st.session_state.pop(key, None)
                for asset_id in reviews:
                    for prefix in ("asset-note", "plan-destinations", "plan-outputKind", "plan-idea", "plan-prompt", "asset-stage", "likenessRating", "sceneQualityRating"):
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
    tab = st.radio('Review queue view', ('Awaiting your decision', 'Review collections'),
                   horizontal=True, key='review-queue-view', label_visibility='collapsed')
    if tab == 'Review collections':
        render_needs_review(data, project)
        return
    query = st.text_input("Find a review request", key=f"review-search:{project}")
    reviews = st.session_state.studio_reviews
    pending = set(mission_pending_requests(data, reviews, project))
    terms = query.casefold().split()
    results = [(asset, album) for asset, album in ordered_assets(data['assets'], data['albums'], project)
               if not asset.get('archived') and reviews.get(asset['id'], {}).get('status') != 'remove'
               and all(term in (json.dumps(asset, ensure_ascii=False) + " " + json.dumps(reviews.get(asset["id"], {}), ensure_ascii=False)).casefold() for term in terms)]
    awaiting = [(asset, album) for asset, album in results if asset['id'] in pending]
    st.subheader('Awaiting your decision')
    st.caption(f'{len(awaiting)} unanswered requests. Saved removal decisions and archived references are in Archive.')
    if awaiting:
        render_grid(awaiting, f'review-awaiting:{project}:{query}')
    else:
        st.info('No unanswered image review requests.')
    saved = [(asset, album) for asset, album in results if asset['id'] not in pending and any(
        reviews.get(asset['id'], {}).get(field) for field in
        ('status', 'note', 'workingReference', 'variant', 'storyboardStage', 'shotPlan'))]
    if saved:
        with st.expander(f'Saved review decisions and plans · {len(saved)}', expanded=False):
            st.caption('These decisions are saved. Correction work and planned shots remain separate from unanswered reviews.')
            render_grid(saved, f'review-saved:{project}:{query}')


def render_shot_plans(data: dict, project: str) -> None:
    intent = export_intent(f"shot-intent:{project}")
    destination = st.selectbox("Handoff destination", ("all", *DESTINATIONS),
                               format_func=lambda d: "All destinations" if d == "all" else destination_label(d))
    output_kind = st.selectbox("Output kind", ("all", *OUTPUT_KINDS),
                               format_func=lambda kind: "All output kinds" if kind == "all" else output_kind_label(kind),
                               key=f"shot-output-kind:{project}")
    query = st.text_input("Find a shot plan", key=f"shot-search:{project}")
    reviews = st.session_state.studio_reviews
    payload = handoff_payload(data["assets"], reviews, project, destination, intent)
    if output_kind != "all":
        payload["items"] = [item for item in payload["items"]
                            if item["shotPlan"].get("outputKind", "unspecified") == output_kind]
    terms = query.casefold().split()
    if terms:
        payload["items"] = [item for item in payload["items"]
                            if all(term in json.dumps(item, ensure_ascii=False).casefold() for term in terms)]
    ids = {item["id"] for item in payload["items"]}
    st.caption(f"{len(ids)} draft shot plans · not sent or generated")
    st.info(payload["attachmentReminder"])
    st.caption("Prime exports exclude Multiverse, removal flags, and archived entries. Multiverse creative ingredients includes variants intentionally; removals and archives stay excluded.")
    txt_col, json_col = st.columns(2)
    filename = f"cfa-shot-handoff-{project}-{destination}-{output_kind}"
    with txt_col:
        st.download_button("Export handoff TXT", handoff_text(payload), file_name=filename + ".txt", mime="text/plain", disabled=not ids, width="stretch")
    with json_col:
        st.download_button("Export handoff JSON", json.dumps(payload, ensure_ascii=False, indent=2),
                           file_name=filename + ".json", mime="application/json", disabled=not ids, width="stretch")
    st.caption("Exports contain only the project, destination, output kind, and search results shown here. Use the complete review export to restore your session later.")
    results = [(asset, album) for asset, album in ordered_assets(data["assets"], data["albums"], project) if asset["id"] in ids]
    for kind in ("image", "video", "unspecified"):
        group = [(asset, album) for asset, album in results
                 if reviews[asset["id"]]["shotPlan"].get("outputKind", "unspecified") == kind]
        if group:
            st.subheader(output_kind_label(kind))
            render_grid(group, f"shot:{project}:{destination}:{kind}:{query}")


def open_mission_reference(asset: dict) -> None:
    st.session_state.studio_project = asset["project"]
    if st.session_state.studio_view in (CORNER, CASA):
        st.session_state.studio_mission_selected = asset["id"]
    else:
        st.session_state.studio_view = "Library"
        select_asset(asset["id"])


def render_mission_control(data: dict, review_data: dict | None = None) -> None:
    render_corner = current_module("mission_view").render_corner
    st.button("← Back to library", key="mission-back", on_click=back_to_library)
    controller = "baldadoon" if st.session_state.studio_view == CASA else "ziggy"
    home = CASA if controller == "baldadoon" else CORNER
    title = "Casa Baldadoon" if controller == "baldadoon" else "Mission Control"
    introduction = "Your director’s room. Read the script, meet the characters, explore locations, and record your direction." if controller == "baldadoon" else "Your next moves, prepared handoffs, and ideas waiting for their next pass."
    st.markdown(f'<div class="studio-hero"><div class="eyebrow">CFA · {html.escape(home)}</div>'
                f'<h1>{title}</h1><p>{introduction}</p></div>',
                unsafe_allow_html=True)

    def sweep():
        st.write("Save your decisions, favorites, stages and reference roles, then pass the review to Nova. This does not start an agent or delete files.")
        payload = sweep_payload((review_data or data)["assets"], st.session_state.studio_reviews, st.session_state.studio_favorites, st.session_state.studio_basket,
                                provenance=st.session_state.studio_review_provenance)
        st.download_button("Prepare review sweep JSON", json.dumps(payload, ensure_ascii=False, indent=2),
                           file_name="cfa-review-sweep-for-nova.json", mime="application/json")

    if data.get("reviewIntake") and controller == "ziggy":
        st.button("Intake verification →", key="mission-intake", on_click=navigate, args=("Intake verification",))
    def export_casting(assets):
        payload = current_module("mission_view").casting_review_payload(assets, st.session_state.studio_reviews,
                                 st.session_state.studio_favorites, st.session_state.studio_basket)
        st.download_button("Export casting review", json.dumps(payload, ensure_ascii=False, indent=2),
                           file_name="baldadoon-casting-review.json", mime="application/json", key="casa-casting-export")
        st.caption("Only this project's casting portraits and saved feedback are included. The sidebar export keeps your full library backup.")
    render_corner(data, LIBRARY_DIR, open_mission_reference, lambda asset: render_selected(asset, data.get("reviewIntake"), data), document_download, navigate, sweep, review_data=review_data or data, controller=controller,
                  review_asset=lambda asset: render_review_controls(asset, review_data or data), export_casting=export_casting)


def render_library_script(data, project):
    """Keep source access beside the library without placing a text landing above images."""
    landing = project.get("landing", {})
    if not landing:
        return
    by_id = {asset["id"]: asset for asset in data["assets"] if asset.get("project") == project["id"]}
    with st.expander("Screenplay & source records", expanded=False):
        st.caption("Original screenplay: " + landing.get("author", "Baldadoon"))
        for key in ("originalAssetID", "scriptAssetID", "inventoryAssetID", "notesAssetID"):
            if asset := by_id.get(landing.get(key)):
                document_download(asset, context="library-source:" + key)
        if script := by_id.get(landing.get("scriptAssetID")):
            if script.get("text"):
                with st.expander("Read the screenplay", expanded=False):
                    st.text(script["text"])
        for block in landing.get("sourceBlocks", []):
            with st.expander(str(block.get("id", "")) + " · " + block.get("heading", "Source block"), expanded=False):
                st.caption(f"Script lines {block.get('lineStart', '?')}–{block.get('lineEnd', '?')}")
                st.text(block.get("text", ""))


def sidebar_navigation_button(view, label):
    def button():
        st.button(label, key=f"nav:{view}", type="primary" if st.session_state.studio_view == view else "secondary",
                  on_click=navigate, args=(view,), width="stretch")
    if view in (CORNER, CASA):
        with st.container(key="sidebar-home-casa" if view == CASA else "sidebar-home-ziggy"):
            button()
    else:
        button()


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
                accepted, skipped = read_basket(json.loads(uploaded.getvalue()), data["assets"], aliases=data.get("assetAliases", []))
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
    if "studio_project_selection" in st.session_state and "studio_project" in st.session_state:
        st.session_state.studio_project_selection = st.session_state.studio_project
    catalog_path = LIBRARY_DIR / "design_catalog.json"
    if not catalog_path.is_file():
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
    if mission_path.is_file() and not data.get("designSnapshot"):
        try:
            mission_data = load_catalog(str(mission_path), mission_path.stat().st_mtime_ns)
            review_data = mission_review_data(data, mission_data)
        except (OSError, ValueError) as error:
            st.error(f"The Ziggy’s Corner snapshot could not be loaded: {error}")
            return
    st.session_state.studio_reviews = effective_reviews(review_data["assets"], review_data.get("reviewDecisions", []), st.session_state.studio_review_overrides,
                                                       aliases=review_data.get("assetAliases", []))
    seed_review_selections(review_data)
    if not data.get("designSnapshot"):
        reply_seed = (str(catalog_path), catalog_path.stat().st_mtime_ns,
                      mission_path.stat().st_mtime_ns if mission_path.is_file() else None)
        if st.session_state.get("studio_reply_source_seed") != reply_seed:
            provenance = st.session_state.studio_review_provenance
            for source in (data, mission_data):
                subset = {key: source[key] for key in ("collaboratorReviews", "collaboratorReviewBackups") if key in source}
                provenance = review_provenance(subset, provenance, strict_takes=False)
            st.session_state.studio_review_provenance = provenance
            st.session_state.studio_reply_source_seed = reply_seed
    if data.get("designSnapshot"):
        identity = data["designSnapshot"].get("sourceCatalog", {}).get("sha256")
        if st.session_state.get("studio_provenance_seed") != identity:
            st.session_state.studio_review_provenance = review_provenance(data, st.session_state.studio_review_provenance, strict_takes=False)
            st.session_state.studio_provenance_seed = identity
        data = effective_design_data(data, st.session_state.studio_reviews)
        mission_data = review_data = data
        aliases = validated_asset_aliases(data["assets"], data.get("assetAliases", []))
        redirect = lambda aid: aliases.get(aid, {}).get("canonicalID", aid)
        st.session_state.studio_selected = redirect(st.session_state.studio_selected)
        st.session_state.studio_favorites = {redirect(aid) for aid in st.session_state.studio_favorites}
        st.session_state.studio_basket = {redirect(aid) for aid in st.session_state.studio_basket}
    st.session_state.studio_notes = {key: value.get("note", "") for key, value in st.session_state.studio_reviews.items()}
    st.session_state.studio_export_assets = review_data["assets"]
    st.session_state.studio_controller_data = {**data, "missionControl": mission_data.get("missionControl", data.get("missionControl", {}))}
    # Streamlit resolves the declaring frame through inspect's filename cache.
    # This stable entrypoint avoids stale names from source-hashed helper modules.
    reply_storage = declare_component("cfa_collaborator_review_storage",
                                      path=str(APP_DIR / "collaborator_review_storage"))
    current_module("collaborator_review_storage").sync(reply_storage)
    if message := st.session_state.pop("studio_flash", None):
        st.success(message)
    populated_projects = {a.get("project") for a in data["assets"]}
    projects = {p["id"]: p for p in data["projects"] if p["id"] != "unassigned" or p["id"] in populated_projects}
    if not projects:
        st.info("No projects are included in this library yet.")
        return
    saved_project = st.session_state.get("studio_project_selection")
    if saved_project not in projects:
        # First render (including an older warm session) reapplies its deep link.
        st.session_state.pop("studio_route_seen", None)
    if st.session_state.get("studio_project") not in projects:
        st.session_state.studio_project = saved_project if saved_project in projects else next(iter(projects))
    current_module("controller_routing").apply_route(st.session_state, st.query_params, data)
    if st.session_state.studio_project == "criminal_mind" and st.session_state.studio_view == "Project home":
        st.session_state.studio_view = "Library"
    # Browser-backup events can rerun before the Project widget mounts. Streamlit
    # then removes widget state, so keep the selected project in durable state too.
    st.session_state.studio_project_selection = st.session_state.studio_project
    with st.sidebar:
        st.markdown("## CFA\n### Creative Studio")
        st.caption("A place to look, compare, and create.")
        project = st.selectbox("Project", list(projects), format_func=lambda key: projects[key]["name"],
                               key="studio_project", on_change=clear_project_selection)
        st.session_state.studio_project_selection = project
        st.caption(projects[project].get("subtitle", ""))
        export_review_button("sidebar")
        browse = (*(("Project home",) if projects[project].get("landing") and project != "criminal_mind" else ()), "Library", "Working references", "Outfits", "Tattoos & piercings", "Supporting cast", "Storyboard", "Videos", "Comfy swap targets", "Collaborators")
        if project != "hon":
            browse += ("Inspiration",)
        browse += ("Review queue", "Archive")
        start = (*(("Intake verification",) if data.get("reviewIntake") else ()), CORNER,
                 *((CASA,) if any(p.get("controllerID") == "baldadoon" for p in projects.values()) else ()))
        for label, views in (("START HERE", start), ("BROWSE", browse), ("CREATE", ("Shot plans", "Collaborator briefs")),
                             ("KEEP & REFER", ("Documents", "Export basket", "Favorites & notes"))):
            st.caption(label)
            for view in views:
                nav_label = "Accessories" if view == "Tattoos & piercings" else view
                if view == 'Export basket':
                    nav_label += ' · '+str(navigation_reference_count(review_data['assets'], st.session_state.studio_basket))
                elif view == 'Documents':
                    nav_label += ' · '+str(navigation_reference_count(
                        [asset for asset in data['assets'] if asset.get('project') == project], documents=True))
                elif view == 'Storyboard':
                    nav_label += f' · {navigation_storyboard_shot_count(data, project)}'
                elif view == 'Review queue':
                    nav_label += ' · '+str(navigation_reference_count(data['assets'],
                        mission_pending_requests(data, st.session_state.studio_reviews, project)))
                sidebar_navigation_button(view, nav_label)
        st.divider()
        st.caption("Stars are a personal shortlist. Source references keep their existing status.")
        st.caption("Export your complete review to keep decisions, notes, plans, and favorites between sessions.")
    assets = [a for a in data["assets"] if a.get("project") == project]
    view = st.session_state.studio_view
    if view in (CORNER, CASA):
        render_mission_control(mission_data, review_data)
        return
    if view == "Collaborators":
        render_collaborators(data)
        return
    if view in ("Intake verification", "intake"):
        selected = next((a for a in data["assets"] if a["id"] == st.session_state.studio_selected), None)
        if selected:
            render_selected(selected, data.get("reviewIntake"), data)
        else:
            current_module("review_intake_view").render_intake(data, project, LIBRARY_DIR, select_asset,
                                                              reviews=st.session_state.studio_reviews)
        return
    hero(projects[project], view, assets)
    selection_assets = review_data["assets"] if view in ("Favorites & notes", "Shot plans", "Export basket") else assets
    selected = next((a for a in selection_assets if a["id"] == st.session_state.get("studio_selected")), None)
    if selected:
        render_selected(selected, data.get("reviewIntake"), data)
    elif view == "Project home":
        current_module("project_intake_view").render_project_home(data, projects[project], document_download, navigate)
    elif view == "Library":
        render_library(data, project)
        if project == "criminal_mind":
            render_library_script(data, projects[project])
    elif view == "Storyboard":
        if data.get("storyboardStories"):
            current_module("story_view").render_stories(data, project, LIBRARY_DIR, render_grid, select_asset, document_download,
                                                       reviews=st.session_state.studio_reviews)
        else:
            render_library(data, project, storyboard=True)
    elif view in DESIGN_VIEWS:
        if view == "Archive":
            current_module("mission_view").render_corner(
                mission_data, LIBRARY_DIR, open_mission_reference, render_selected, document_download,
                navigate, lambda: None, review_data=review_data, archived=True,
                controller=current_module("controller_routing").project_controller(data, project))
        render_design_workspace(data, project, view)
    elif view in ("Videos", "Inspiration"):
        render_library(data, project, fixed_category=view.lower())
    elif view == "Needs review":
        render_needs_review(data, project)
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
