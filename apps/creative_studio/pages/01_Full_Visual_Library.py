"""The current local visual library, served as its portable HTML mirror."""
from pathlib import Path
import json
import sys

import streamlit as st

APP_DIR = Path(__file__).resolve().parents[1]
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))
from full_dashboard_component import render_dashboard, route_config, navigation_request

BUNDLE_DIR = APP_DIR / "full_dashboard_bundle"
st.set_page_config(page_title="Full Visual Library | CFA", page_icon="🎞️", layout="wide", initial_sidebar_state="collapsed")
st.markdown("""<style>
[data-testid="stMain"]{overflow:hidden;}
[data-testid="stMainBlockContainer"]{padding:3.5rem .5rem .5rem;max-width:none;height:100dvh;}
[data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"]{gap:0;}
iframe[title="full_dashboard_component.cfa_full_visual_library"]{display:block;height:calc(100dvh - 4rem)!important;}
@media(max-width:700px){[data-testid="stMainBlockContainer"]{padding-inline:.2rem;}}
</style>""", unsafe_allow_html=True)
with st.sidebar:
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

with st.sidebar.expander("Review storage and publication"):
    st.caption("The library fits your window automatically. This page and the compact Studio have separate saved review state; transfer a complete review JSON when switching.")
    st.caption(f"{current.get('assetCount', 0):,} catalog entries · dashboard {current.get('buildID', '')}")

config = route_config(snapshot)
navigation_state_key = '_full_dashboard_navigation'
request = navigation_request(st.query_params, config, st.session_state.get(navigation_state_key))
st.session_state[navigation_state_key] = request
# Community Cloud can remount the entire app when its outer query changes.
# Apply explicit entry links, then let the dashboard own its hash navigation.
# Ordinary clicks must neither update outer query parameters nor rerun Streamlit.
render_dashboard(snapshot, initial_route=request['requestedRoute'], request_id=request['requestID'],
                 report_navigation=False)
