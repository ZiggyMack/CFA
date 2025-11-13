"""
CFA v4.0 - Main Application (Modular Version)
Run with: streamlit run app.py
"""

# deps: file_structure

import streamlit as st
import sys
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import page modules
from pages import landing, console, about, manual, brute_ledger

# Page configuration
st.set_page_config(
    page_title="CFA v4.0 - Epistemic Engineering",
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
        console.render()
    elif st.session_state.page == 'manual':
        manual.render()
    elif st.session_state.page == 'about':
        about.render()
    elif st.session_state.page == 'brute_ledger':
        brute_ledger.render()

if __name__ == "__main__":
    main()
