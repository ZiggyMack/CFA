"""Readable, source-bound project landing without manufacturing storyboard shots."""
import streamlit as st
from studio_dependencies import current_module


def render_project_home(data, project, document_download, navigate):
    landing = project.get("landing", {})
    if not landing:
        st.info("Open the library to browse this project's material.")
        return
    routing = current_module("controller_routing")
    person = routing.controllers(data)[routing.project_controller(data, project["id"])]
    st.subheader(landing.get("title") or project.get("subtitle") or project["name"])
    st.caption("Original screenplay: " + landing.get("author", person["name"]) + " · Adaptation and visual development: " + landing.get("stage", "Preliminary"))
    st.write(landing.get("description", ""))
    st.caption("Human controller: " + person["name"] + ". Controller routing identifies responsibility; this shared app does not authenticate the selected reviewer.")
    if st.button("Open " + person["homeLabel"], key="project-controller-home:" + project["id"]):
        navigate(person["homeLabel"])
        st.rerun()
    assets = {a["id"]: a for a in data.get("assets", []) if a.get("project") == project["id"]}
    script, blocks, notes = st.tabs(["Screenplay", "Source scenes / blocks", "Initial notes"])
    with script:
        for key in ("originalAssetID", "scriptAssetID"):
            asset = assets.get(landing.get(key))
            if asset:
                document_download(asset, context="project-home:" + key)
        asset = assets.get(landing.get("scriptAssetID"))
        if asset and asset.get("text"):
            with st.expander("Read the screenplay", expanded=False):
                st.text(asset["text"])
        else:
            st.info("The readable screenplay is not included in this snapshot.")
    with blocks:
        rows = landing.get("sourceBlocks", [])
        st.caption(f"{len(rows)} source heading blocks · not finished scenes or storyboard shots")
        for row in rows:
            with st.expander(str(row.get("id", "")) + " · " + row.get("heading", "Source block"), expanded=False):
                st.caption(f"Script lines {row.get('lineStart', '?')}–{row.get('lineEnd', '?')}")
                if row.get("containsUnheadedFlashback"):
                    st.caption("This source block includes an unheaded flashback and return.")
                st.text(row.get("text", ""))
        if not rows:
            st.info("Source block text is not included in this snapshot.")
        asset = assets.get(landing.get("inventoryAssetID"))
        if asset:
            document_download(asset, context="project-home:inventory")
    with notes:
        asset = assets.get(landing.get("notesAssetID"))
        if asset:
            st.text(asset.get("text", ""))
            document_download(asset, context="project-home:notes")
        st.caption("Initial observations are Preliminary proposals, not an accepted storyboard or generation request.")
    st.info("No character designs, accepted starting images, generated videos, accepted takes, song master or measured runtime are recorded for this intake. A screenplay can begin storyboarding without a song.")
    st.markdown("**Next step**")
    st.write(landing.get("nextStep", "Review the initial adaptation notes and establish the storyboard scope and required character/location references."))
