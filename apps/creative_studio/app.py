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
from library_helpers import VISUAL_KINDS, favorite_payload, media_path, ordered_assets, read_favorites

LIBRARY_DIR = APP_DIR / "library"
PAGE_SIZE = 24
VIEWS = ("Library", "Storyboard", "Collaborator kits", "Favorites & notes", "Documents")

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
    for key, default in (("studio_view", "Library"), ("studio_selected", None),
                         ("studio_favorites", set()), ("studio_notes", {}), ("studio_pages", {})):
        if key not in st.session_state:
            st.session_state[key] = default


def navigate(view: str) -> None:
    st.session_state.studio_view = view
    st.session_state.studio_selected = None


def clear_selection() -> None:
    st.session_state.studio_selected = None


def select_asset(asset_id: str) -> None:
    st.session_state.studio_selected = asset_id


def toggle_favorite(asset_id: str) -> None:
    favorites = set(st.session_state.studio_favorites)
    favorites.remove(asset_id) if asset_id in favorites else favorites.add(asset_id)
    st.session_state.studio_favorites = favorites


def save_note(asset_id: str, key: str) -> None:
    st.session_state.studio_notes[asset_id] = st.session_state[key]


def change_page(signature: str, value: int) -> None:
    st.session_state.studio_pages[signature] = value
    clear_selection()


def hero(project: dict, view: str, assets: list[dict]) -> None:
    visuals = [a for a in assets if a.get("kind") in VISUAL_KINDS]
    videos = sum(a.get("kind") == "video" for a in visuals)
    captions = {
        "Library": "Explore the looks, compare the details, and keep the references you want to return to.",
        "Storyboard": "Follow the story in pictures. Open a panel for its beat, lyric connection, and review notes.",
        "Collaborator kits": "Project instructions and reference maps for Gemini, Flow, and the rest of the creative team.",
        "Favorites & notes": "Your working shortlist. Export it to keep your choices and carry them between review sessions.",
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
              on_click=toggle_favorite, args=(asset["id"],), width="stretch")


def render_selected(asset: dict) -> None:
    st.button("← Back to the collection", on_click=clear_selection)
    st.subheader(asset.get("title", asset["filename"]))
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
        note_key = f"asset-note:{asset['id']}"
        if note_key not in st.session_state:
            st.session_state[note_key] = st.session_state.studio_notes.get(asset["id"], "")
        st.text_area("Your review note", key=note_key, height=130, on_change=save_note, args=(asset["id"], note_key),
                     placeholder="What works here? What should change in the next pass?")
        st.caption("Notes and stars stay in this session. Export them from Favorites & notes before you leave.")
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
                      key=f"open:{asset['id']}", on_click=select_asset, args=(asset["id"],), width="stretch")
        with c2:
            favorite_button(asset)


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
    signature = json.dumps([project, category, album_id, query, storyboard])
    render_grid(results, signature)


def document_download(asset: dict) -> None:
    text = asset.get("text", "")
    source = media_path(LIBRARY_DIR, asset.get("src"))
    if text:
        st.download_button("Download text", text, file_name=asset.get("filename", "reference.txt"),
                           mime="text/plain", key=f"doc-download:{asset['id']}")
    elif source:
        st.download_button("Download document", source.read_bytes(), file_name=source.name,
                           mime=mimetypes.guess_type(source.name)[0] or "application/octet-stream",
                           key=f"doc-download:{asset['id']}")


def render_documents(assets: list[dict], kits_only: bool = False) -> None:
    documents = [a for a in assets if a.get("kind") in {"document", "pdf"}]
    if kits_only:
        documents = [a for a in documents if any(word in a.get("album", "").casefold()
                                                for word in ("gemini instructions", "collaborator", "grok instructions"))
                     or ("grok" in a.get("filename", "").casefold() and "instructions" in a.get("filename", "").casefold())]
        st.info("Start with the instructions, then supply the named reference images and the matching map. "
                "These kits are prepared guidance; this page does not upload anything to a generation service.")
    if not documents:
        st.info("There are no documents for this project in the current bundle.")
        return
    if not kits_only:
        query = st.text_input("Find a supporting note", key="document-search", placeholder="Search titles or contents")
        if query:
            terms = query.casefold().split()
            documents = [a for a in documents if all(t in (a.get("title", "") + " " + a.get("text", "")).casefold() for t in terms)]
    groups: dict[str, list[dict]] = {}
    for asset in documents:
        groups.setdefault(asset.get("album", "Supporting notes"), []).append(asset)
    for group, items in groups.items():
        st.subheader(group)
        for asset in items:
            with st.expander(asset.get("title", asset["filename"])):
                if asset.get("note"):
                    st.caption(asset["note"])
                if asset.get("inert"):
                    st.caption("Technical reference supplied as text. Nothing on this page executes it.")
                if asset.get("text"):
                    st.code(asset["text"], language=None, wrap_lines=True)
                elif asset.get("kind") == "pdf":
                    st.write("Use the download below to read this PDF.")
                document_download(asset)


def render_favorites(data: dict, project: str) -> None:
    if message := st.session_state.pop("studio_import_message", None):
        st.success(message)
    payload = favorite_payload(data["assets"], st.session_state.studio_favorites, st.session_state.studio_notes)
    export_col, import_col = st.columns(2, gap="large")
    with export_col:
        st.markdown("**Keep your review**")
        st.write("Export includes favorites and notes from all projects. Save it before closing this session.")
        st.download_button("Export favorites & notes", json.dumps(payload, ensure_ascii=False, indent=2),
                           file_name="cfa-visual-favorites.json", mime="application/json", width="stretch")
        st.caption(f"{len(payload['items'])} saved references · {len(payload['notes'])} notes across all projects")
    with import_col:
        st.markdown("**Bring a review back**")
        uploaded = st.file_uploader("Favorites JSON", type=["json"], key="favorites-upload")
        if uploaded is not None and st.button("Add this review to my session", width="stretch"):
            try:
                if uploaded.size > 5 * 1024 * 1024:
                    raise ValueError("Choose a favorites file smaller than 5 MB.")
                accepted, notes, skipped = read_favorites(json.loads(uploaded.getvalue()), data["assets"])
                st.session_state.studio_favorites = set(st.session_state.studio_favorites) | accepted
                st.session_state.studio_notes.update(notes)
                for asset_id, note in notes.items():
                    st.session_state[f"asset-note:{asset_id}"] = note
                st.session_state.studio_import_message = f"Added {len(accepted)} favorites and {len(notes)} notes. Skipped {skipped} unmatched references."
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
    projects = {p["id"]: p for p in data["projects"]}
    if not projects:
        st.info("No projects are included in this library yet.")
        return
    with st.sidebar:
        st.markdown("## CFA\n### Creative Studio")
        st.caption("A place to look, compare, and create.")
        project = st.selectbox("Project", list(projects), format_func=lambda key: projects[key]["name"],
                               key="studio_project", on_change=clear_selection)
        for label, views in (("BROWSE", ("Library", "Storyboard")), ("CREATE", ("Collaborator kits",)),
                             ("KEEP & REFER", ("Favorites & notes", "Documents"))):
            st.caption(label)
            for view in views:
                st.button(view, key=f"nav:{view}", type="primary" if st.session_state.studio_view == view else "secondary",
                          on_click=navigate, args=(view,), width="stretch")
        st.divider()
        st.caption("Stars are a personal shortlist. Source references keep their existing status.")
        st.caption("Export favorites and notes to keep them between sessions.")
    assets = [a for a in data["assets"] if a.get("project") == project]
    view = st.session_state.studio_view
    hero(projects[project], view, assets)
    selected = next((a for a in assets if a["id"] == st.session_state.studio_selected and a.get("kind") in VISUAL_KINDS), None)
    if selected:
        render_selected(selected)
    elif view == "Library":
        render_library(data, project)
    elif view == "Storyboard":
        render_library(data, project, storyboard=True)
    elif view == "Collaborator kits":
        render_documents(assets, kits_only=True)
    elif view == "Favorites & notes":
        render_favorites(data, project)
    else:
        render_documents(assets)


if __name__ == "__main__":
    main()
