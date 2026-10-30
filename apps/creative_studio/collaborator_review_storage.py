"""Browser backup handshake for task questionnaires, independent of image reviews."""
import json
from pathlib import Path

import streamlit as st
from streamlit.components.v1 import declare_component


def sync():
    from studio_dependencies import current_module
    pilot = current_module("collaborator_review")
    component = declare_component("cfa_collaborator_review_storage", path=str(Path(__file__).with_suffix("")))
    provenance = st.session_state.get("studio_review_provenance", {})
    records = provenance.get("collaboratorReviews", {})
    event = component(records=records, ack=st.session_state.get("studio_reply_storage_ack"),
                      enabled=not st.session_state.get("studio_reply_storage_blocked", False),
                      key="cfa-collaborator-review-browser", default=None)
    if not isinstance(event, dict) or event.get("eventID") == st.session_state.get("studio_reply_storage_event"):
        return
    st.session_state.studio_reply_storage_event = event.get("eventID")
    if event.get("kind") == "error":
        st.session_state.studio_reply_storage_status = "unavailable"
        st.session_state.studio_reply_storage_error = str(event.get("message", "Browser storage is unavailable."))
        return
    if event.get("kind") == "loaded":
        raw = event.get("raw")
        try:
            stored = {} if raw is None else json.loads(raw)
            merged = pilot.merge(records, stored)
        except (ValueError, TypeError) as error:
            # Never overwrite a malformed/conflicting browser backup with a seed.
            st.session_state.studio_reply_storage_blocked = True
            st.session_state.studio_reply_storage_status = "conflict"
            st.session_state.studio_reply_storage_error = str(error)
            st.session_state.studio_reply_storage_backup = raw
            st.session_state.studio_review_provenance = {**provenance,
                "collaboratorReviewBackups": pilot.merge_backups(provenance.get("collaboratorReviewBackups", []),
                    [{"origin": "browser collaboratorReviews", "reason": str(error), "data": raw}])}
            st.rerun()
        st.session_state.studio_reply_storage_ack = event.get("token")
        st.session_state.studio_reply_storage_status = "syncing"
        if merged != records:
            st.session_state.studio_review_provenance = {**provenance, "collaboratorReviews": merged}
            for key in list(st.session_state):
                if key.startswith("return-answer:") or key in {"return-direction", "return-direction-note", "return-direction-asset"}:
                    st.session_state.pop(key, None)
        st.rerun()
    if event.get("kind") == "saved":
        st.session_state.studio_reply_storage_ack = event.get("token")
        st.session_state.studio_reply_storage_status = "saved"
        st.session_state.pop("studio_reply_storage_error", None)
        st.rerun()


def caption():
    state = st.session_state.get("studio_reply_storage_status", "connecting")
    if state == "saved":
        st.caption("Task answers are backed up in this browser and restored after refresh. Download a review JSON to move them to another device or protect against cleared browser data.")
    elif state in {"conflict", "unavailable"}:
        st.warning("Browser backup is unavailable. Download your task draft before refreshing or closing. " + st.session_state.get("studio_reply_storage_error", ""))
        if (raw := st.session_state.get("studio_reply_storage_backup")) is not None:
            st.download_button("Save the untouched browser backup", str(raw), file_name="collaborator-review-browser-backup.json",
                               mime="application/json", key="return-save-browser-backup")
    else:
        st.caption("Connecting to this browser’s task backup. Use the draft download until backup is confirmed.")
