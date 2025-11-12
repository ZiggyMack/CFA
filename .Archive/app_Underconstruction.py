"""
CFA v2.0 - Main Application (Modular Version)
Run with: streamlit run app.py
"""

import streamlit as st
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import page modules
from pages import landing

# Page configuration
st.set_page_config(
    page_title="CFA v2.0 - Epistemic Engineering",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="auto"
)

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

# Main router
def main():
    if st.session_state.page == 'landing':
        landing.render()
    elif st.session_state.page == 'console':
        st.title("🚧 Console Coming Soon")
        if st.button("← Back to Landing"):
            st.session_state.page = 'landing'
            st.rerun()
    elif st.session_state.page == 'manual':
        st.title("🚧 Manual Coming Soon")
        if st.button("← Back to Landing"):
            st.session_state.page = 'landing'
            st.rerun()
    elif st.session_state.page == 'about':
        st.title("🚧 About Coming Soon")
        if st.button("← Back to Landing"):
            st.session_state.page = 'landing'
            st.rerun()

if __name__ == "__main__":
    main()
