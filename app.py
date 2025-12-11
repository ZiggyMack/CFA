"""
CFA v5.0 - Main Application (Modular Version)
Run with: streamlit run app.py
"""

# deps: file_structure

import streamlit as st
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import page modules
from pages import landing, console, about, manual, brute_ledger, chat_assistant, verbose_manifesto, matrix

# Page configuration - wrapped to handle session conflicts
try:
    st.set_page_config(
        page_title="CFA v5.0 - Epistemic Engineering",
        page_icon="⚖️",
        layout="wide",
        initial_sidebar_state="collapsed"  # Start collapsed, expand when needed
    )
except st.errors.StreamlitAPIException:
    pass  # Page config already set by another session or rerun

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'landing'

# Custom Sidebar Navigation
def render_sidebar():
    """Render custom sidebar navigation"""

    # Hide Streamlit's default page navigation
    st.markdown("""
        <style>
        /* Hide the default Streamlit page navigation */
        [data-testid="stSidebarNav"] {
            display: none;
        }
        </style>
    """, unsafe_allow_html=True)

    # Pages that have their own sidebar controls (skip navigation buttons)
    pages_with_own_sidebar = ['console']

    # Only render navigation buttons if current page doesn't have its own sidebar
    if st.session_state.page not in pages_with_own_sidebar:
        with st.sidebar:
            st.markdown("### Navigation")
            st.caption("💡 Tip: Collapse sidebar (← arrow) for full-screen workspace")
            st.markdown("---")

            # Create navigation buttons
            if st.button("🏠 Landing", use_container_width=True, key="nav_landing"):
                st.session_state.page = 'landing'
                st.experimental_rerun()

            if st.button("🎮 Console", use_container_width=True, key="nav_console"):
                st.session_state.page = 'console'
                st.experimental_rerun()

            if st.button("ℹ️ About", use_container_width=True, key="nav_about"):
                st.session_state.page = 'about'
                st.experimental_rerun()

            if st.button("📖 Manual", use_container_width=True, key="nav_manual"):
                st.session_state.page = 'manual'
                st.experimental_rerun()

            if st.button("📓 Brute Ledger", use_container_width=True, key="nav_brute"):
                st.session_state.page = 'brute_ledger'
                st.experimental_rerun()

            if st.button("💬 Chat Assistant", use_container_width=True, key="nav_chat"):
                st.session_state.page = 'chat_assistant'
                st.experimental_rerun()

            if st.button("📜 Verbose Manifesto", use_container_width=True, key="nav_manifesto"):
                st.session_state.page = 'verbose_manifesto'
                st.experimental_rerun()

            if st.button("🌐 Matrix", use_container_width=True, key="nav_matrix"):
                st.session_state.page = 'matrix'
                st.experimental_rerun()

# Main router
def main():
    # Render sidebar navigation
    render_sidebar()

    # Route to appropriate page
    if st.session_state.page == 'landing':
        landing.render()
    elif st.session_state.page == 'console':
        console.render()
    elif st.session_state.page == 'manual':
        manual.render()
    elif st.session_state.page == 'about':
        about.render()
    elif st.session_state.page == 'brute_ledger':
        brute_ledger.render()
    elif st.session_state.page == 'chat_assistant':
        chat_assistant.render()
    elif st.session_state.page == 'verbose_manifesto':
        verbose_manifesto.render()
    elif st.session_state.page == 'matrix':
        matrix.render()

if __name__ == "__main__":
    main()
