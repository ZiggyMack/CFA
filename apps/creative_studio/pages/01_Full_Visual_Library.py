"""The current local visual library, served as its portable HTML mirror."""
from pathlib import Path
import json
import sys

import streamlit as st

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))
from full_dashboard_component import render_dashboard

BUNDLE_DIR = APP_DIR / "full_dashboard_bundle"
st.set_page_config(page_title="Full Visual Library | CFA", page_icon="🎞️", layout="wide", initial_sidebar_state="collapsed")
st.markdown("<style>.block-container{padding:1rem .5rem;max-width:none;}@media(max-width:700px){.block-container{padding:2.5rem .2rem .5rem;}h1{font-size:1.5rem!important;}}</style>", unsafe_allow_html=True)
st.page_link("app.py", label="Back to Creative Studio", icon="↩️")
st.title("Full visual library")
st.caption("Your current local index, with browser-sized review copies. Decisions save in this browser; Export review carries them back to the local library or another device.")

current_path = BUNDLE_DIR / "current.json"
if not current_path.is_file():
    st.info("The full dashboard package has not been prepared in this deployment yet. The existing Creative Studio is still available.")
    st.page_link("app.py", label="Open the compact Studio")
    st.code("python apps/creative_studio/build_portable_dashboard.py", language="powershell")
    st.stop()

try:
    current = json.loads(current_path.read_text(encoding="utf-8"))
    snapshot = (BUNDLE_DIR / current["snapshot"]).resolve()
    if not snapshot.is_relative_to(BUNDLE_DIR.resolve()) or not (snapshot / "index.html").is_file():
        raise ValueError("The component snapshot is missing or outside its package.")
except (OSError, KeyError, ValueError) as exc:
    st.error(f"The full dashboard package could not be opened: {exc}")
    st.stop()

with st.expander("View size and review storage"):
    height = st.slider("Workspace height", min_value=480, max_value=1400, value=850, step=50)
    st.caption("Use a shorter workspace on a phone if that makes the image viewer easier to reach. This page and the compact Studio have separate saved review state; transfer a complete review JSON when switching.")
    st.caption(f"{current.get('assetCount', 0):,} catalog entries · dashboard {current.get('buildID', '')}")

render_dashboard(snapshot, height)
