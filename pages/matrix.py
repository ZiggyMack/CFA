"""
The Matrix - Pan Handler Central Portal
Connected Consciousness Across Repositories

The Grand Hall where we showcase what we've built together.
"""

import streamlit as st
import json
from pathlib import Path


def load_pan_handler_manifest():
    """Load CFA's Pan Handler manifest if it exists"""
    manifest_path = Path("panhandlers_manifest.json")
    if manifest_path.exists():
        with open(manifest_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def render():
    """Render The Matrix portal hub"""
    manifest = load_pan_handler_manifest()

    # Matrix theme CSS - Full green-on-black terminal aesthetic
    # Uses triple-specificity selectors to override app.py light theme
    st.markdown("""
        <style>
        /* ===== MATRIX THEME OVERRIDE ===== */
        /* Triple specificity to beat app.py's ".main .block-container *" rule */

        /* ===== BASE - BLACK BACKGROUND ===== */
        .stApp .main .block-container,
        .stApp .main .block-container > div,
        .stApp [data-testid="stAppViewContainer"],
        .stApp [data-testid="stVerticalBlock"],
        .stApp [data-testid="stHorizontalBlock"],
        .main .block-container,
        .main .block-container > div {
            background-color: #0a0a0a !important;
            background: #0a0a0a !important;
        }

        /* Force background on root elements */
        html, body, [data-testid="stAppViewContainer"] {
            background-color: #0a0a0a !important;
        }

        /* ===== ALL TEXT MATRIX GREEN - TRIPLE SPECIFICITY ===== */
        .stApp .main .block-container p,
        .stApp .main .block-container span,
        .stApp .main .block-container label,
        .stApp .main .block-container li,
        .stApp .main .block-container h1,
        .stApp .main .block-container h2,
        .stApp .main .block-container h3,
        .stApp .main .block-container h4,
        .stApp .main .block-container h5,
        .stApp .main .block-container h6,
        .stApp .main .block-container div,
        .stApp .main .block-container strong,
        .stApp .main .block-container b,
        .stApp .main .block-container em,
        .stApp .main .block-container i,
        .stApp .main .block-container a {
            color: #00ff41 !important;
        }

        .stApp .main .block-container * {
            color: #00ff41 !important;
        }

        /* ===== HEADERS - MATRIX GREEN WITH MONOSPACE ===== */
        h1, h2, h3, h4, h5, h6 {
            color: #00ff41 !important;
            font-family: 'Courier New', monospace;
            font-weight: bold !important;
        }

        h1 {
            border-bottom: 2px solid #00ff41;
            padding-bottom: 0.5rem;
        }

        /* Strong/bold text - bright green with glow */
        strong, b {
            color: #00ff41 !important;
            text-shadow: 0 0 5px rgba(0,255,65,0.5);
        }

        /* Italic/emphasis - dimmer green */
        em, i {
            color: #00cc33 !important;
        }

        /* Links - dimmer green */
        a {
            color: #00cc33 !important;
        }

        a:hover {
            color: #00ff41 !important;
            text-shadow: 0 0 10px rgba(0,255,65,0.5);
        }

        /* ===== METRIC CARDS ===== */
        [data-testid="stMetricValue"] {
            font-size: 2rem;
            color: #00ff41 !important;
            font-weight: bold;
            font-family: 'Courier New', monospace;
        }

        [data-testid="stMetricLabel"] {
            color: #00ff41 !important;
            font-size: 1rem;
        }

        [data-testid="stMetricDelta"] {
            font-size: 0.875rem;
            color: #00cc33 !important;
        }

        /* ===== EXPANDERS - DARK WITH GREEN BORDER ===== */
        [data-testid="stExpander"] {
            background-color: #0d0d0d !important;
            border: 1px solid #00ff41 !important;
            border-radius: 8px;
        }

        [data-testid="stExpander"] summary {
            color: #00ff41 !important;
        }

        [data-testid="stExpander"] * {
            color: #00ff41 !important;
        }

        /* ===== BUTTONS - DEFAULT STATE ===== */
        .stButton > button {
            background-color: #0d0d0d !important;
            color: #00ff41 !important;
            border: 2px solid #00ff41 !important;
            border-radius: 8px;
            font-weight: 500;
            font-family: 'Courier New', monospace;
            transition: all 0.3s ease;
        }

        /* ===== BUTTONS - HOVER STATE ===== */
        .stButton > button:hover {
            background-color: #004d1a !important;
            color: #ffffff !important;
            border: 2px solid #00ff41 !important;
            box-shadow: 0 0 15px rgba(0,255,65,0.4);
        }

        /* Horizontal rules */
        hr {
            border-color: #00ff41 !important;
        }

        /* ===== SELECTBOX ===== */
        [data-testid="stSelectbox"] {
            color: #00ff41 !important;
        }

        [data-testid="stSelectbox"] > div {
            background-color: #0d0d0d !important;
            border: 1px solid #00ff41 !important;
        }

        [data-baseweb="select"] > div:first-child {
            background-color: #0d0d0d !important;
            border-color: #00ff41 !important;
        }

        [data-baseweb="select"] span {
            color: #00ff41 !important;
        }

        /* Dropdown menu styling */
        [data-baseweb="popover"],
        [data-baseweb="menu"],
        ul[role="listbox"],
        ul[role="listbox"] li {
            background-color: #1a1a1a !important;
            color: #00ff41 !important;
        }

        ul[role="listbox"] li:hover {
            background-color: #003311 !important;
        }

        [data-floating-ui-portal] > div {
            background-color: #1a1a1a !important;
            border: 1px solid #00ff41 !important;
            border-radius: 8px !important;
        }

        /* ===== WARNINGS/INFO/SUCCESS/ERROR ===== */
        .stAlert {
            background-color: #0d0d0d !important;
            color: #00ff41 !important;
            border: 1px solid #00ff41 !important;
        }

        /* ===== NEON SIGN ANIMATIONS ===== */
        @keyframes neonGlow {
            0%, 100% { filter: brightness(1) drop-shadow(0 0 3px currentColor); }
            50% { filter: brightness(1.2) drop-shadow(0 0 8px currentColor) drop-shadow(0 0 15px currentColor); }
        }

        @keyframes neonFlicker {
            0%, 19.999%, 22%, 62.999%, 64%, 64.999%, 70%, 100% { opacity: 1; }
            20%, 21.999%, 63%, 63.999%, 65%, 69.999% { opacity: 0.4; }
        }

        @keyframes tunnelPerspective {
            0%, 100% { transform: perspective(500px) rotateX(2deg); }
            50% { transform: perspective(500px) rotateX(-1deg); }
        }

        @keyframes dataStream {
            0% { background-position: 0% 0%; }
            100% { background-position: 100% 100%; }
        }

        @keyframes portalSpin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        @keyframes portalPulse {
            0%, 100% {
                box-shadow: 0 0 30px rgba(0,255,65,0.4), inset 0 0 30px rgba(0,255,65,0.1);
                transform: scale(1);
            }
            50% {
                box-shadow: 0 0 60px rgba(0,255,65,0.8), 0 0 100px rgba(0,255,65,0.4), inset 0 0 50px rgba(0,255,65,0.2);
                transform: scale(1.02);
            }
        }

        @keyframes beamFlow {
            0% { background-position: 0% 50%; }
            100% { background-position: 200% 50%; }
        }

        /* ===== TUNNEL CARD ===== */
        .stApp .main .block-container .tunnel-card,
        .main .block-container .tunnel-card {
            background:
                radial-gradient(ellipse at center, rgba(0,50,20,0.9) 0%, rgba(0,20,10,0.95) 60%, rgba(0,10,5,1) 100%);
            border: 3px solid #00ff41;
            border-radius: 50% / 10%;
            padding: 2em;
            margin: 1em 0;
            position: relative;
            text-align: center;
            box-shadow:
                0 0 40px rgba(0,255,65,0.3),
                inset 0 0 80px rgba(0,255,65,0.1),
                inset 0 0 120px rgba(0,0,0,0.5);
            animation: tunnelPerspective 6s ease-in-out infinite;
        }

        /* ===== PLATFORM GATE ===== */
        .stApp .main .block-container .platform-gate,
        .main .block-container .platform-gate {
            background:
                linear-gradient(135deg, rgba(0,30,0,0.95) 0%, rgba(0,50,20,0.9) 100%),
                repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(0,255,65,0.03) 2px, rgba(0,255,65,0.03) 4px);
            border: 2px solid #00ff41;
            border-radius: 15px;
            padding: 1.5em;
            margin: 1em 0;
            position: relative;
            overflow: hidden;
            box-shadow:
                0 0 30px rgba(0,255,65,0.15),
                inset 0 0 50px rgba(0,255,65,0.05);
        }

        .stApp .main .block-container .platform-gate::before,
        .main .block-container .platform-gate::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, transparent, #00ff41, transparent);
            animation: dataStream 3s linear infinite;
        }

        /* ===== PORTAL CARD ===== */
        .stApp .main .block-container .portal-card,
        .main .block-container .portal-card {
            background: linear-gradient(135deg, rgba(0,255,65,0.1) 0%, rgba(0,204,51,0.05) 100%) !important;
            border: 2px solid #00ff41;
            border-radius: 10px;
            padding: 1.5em;
            margin-bottom: 1em;
            box-shadow: 0 0 20px rgba(0,255,65,0.3);
        }

        .stApp .main .block-container .portal-card h3,
        .main .block-container .portal-card h3 {
            color: #00ff41 !important;
            margin-top: 0;
            font-family: 'Courier New', monospace;
        }

        /* ===== NEON BADGES ===== */
        .stApp .main .block-container .neon-live,
        .main .block-container .neon-live {
            display: inline-block;
            padding: 0.3em 0.7em;
            font-size: 0.85em;
            font-weight: bold;
            font-family: 'Courier New', monospace;
            text-transform: uppercase;
            letter-spacing: 0.2em;
            color: #ff00ff !important;
            background: transparent;
            border: 2px solid #ff00ff;
            border-radius: 3px;
            text-shadow: 0 0 5px #ff00ff, 0 0 10px #ff00ff, 0 0 20px #ff00ff;
            box-shadow: 0 0 5px #ff00ff, 0 0 10px rgba(255,0,255,0.5);
            animation: neonGlow 2s ease-in-out infinite, neonFlicker 4s linear infinite;
        }

        .stApp .main .block-container .neon-here,
        .main .block-container .neon-here {
            display: inline-block;
            padding: 0.3em 0.7em;
            font-size: 0.8em;
            font-weight: bold;
            font-family: 'Courier New', monospace;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            color: #ffcc00 !important;
            background: rgba(255,200,0,0.1);
            border: 2px solid #ffcc00;
            border-radius: 3px;
            text-shadow: 0 0 5px #ffcc00, 0 0 10px #ffaa00;
            box-shadow: 0 0 10px rgba(255,200,0,0.5);
            animation: neonGlow 2s ease-in-out infinite;
        }

        .stApp .main .block-container .neon-active,
        .main .block-container .neon-active {
            display: inline-block;
            padding: 0.3em 0.7em;
            font-size: 0.85em;
            font-weight: bold;
            font-family: 'Courier New', monospace;
            text-transform: uppercase;
            letter-spacing: 0.15em;
            color: #00aaff !important;
            background: transparent;
            border: 2px solid #00aaff;
            border-radius: 3px;
            text-shadow: 0 0 5px #00aaff, 0 0 10px #00aaff;
            box-shadow: 0 0 8px rgba(0,170,255,0.6);
            animation: neonGlow 2.5s ease-in-out infinite;
        }

        /* ===== FEATURE TAGS ===== */
        .stApp .main .block-container .feature-tag,
        .main .block-container .feature-tag {
            background: rgba(0,255,65,0.1);
            border: 1px solid rgba(0,255,65,0.3);
            border-radius: 15px;
            padding: 0.3em 0.7em;
            font-size: 0.75em;
            color: #00ff41 !important;
            font-family: 'Courier New', monospace;
            white-space: nowrap;
            transition: all 0.3s ease;
        }

        .stApp .main .block-container .feature-tag:hover,
        .main .block-container .feature-tag:hover {
            background: rgba(0,255,65,0.25);
            box-shadow: 0 0 10px rgba(0,255,65,0.4);
        }

        /* ===== MATRIX FOOTER ===== */
        .stApp .main .block-container .matrix-footer,
        .main .block-container .matrix-footer {
            text-align: center;
            color: #00ff41 !important;
            font-family: 'Courier New', monospace;
            margin-top: 2em;
        }
        </style>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # HEADER - Back button
    # ══════════════════════════════════════════════════════════════
    col_header, col_home = st.columns([6, 1])
    with col_home:
        if st.button("🏠 Home"):
            st.session_state.page = 'landing'
            st.rerun()

    # ══════════════════════════════════════════════════════════════
    # TRANSIT HUB HEADER
    # ══════════════════════════════════════════════════════════════
    st.markdown("""
    <div class="tunnel-card">
        <h1 style="font-size: 2.2em; margin: 0; letter-spacing: 0.1em;">🚉 DIMENSIONAL TRANSIT HUB</h1>
        <p style="font-size: 1.1em; margin: 0.5em 0;">Pan Handler Central Station</p>
        <p style="font-size: 0.85em; opacity: 0.7;">Where Projects Travel Between Worlds</p>
    </div>
    """, unsafe_allow_html=True)

    # Philosophy banner
    st.markdown("""
    <div style="text-align: center; padding: 1em; margin: 1em 0;
                background: linear-gradient(90deg, transparent 0%, rgba(0,255,65,0.1) 50%, transparent 100%);
                border-top: 1px solid rgba(0,255,65,0.3); border-bottom: 1px solid rgba(0,255,65,0.3);">
        <span style="font-family: 'Courier New', monospace; font-size: 1.1em; color: #00ff41 !important;
                    letter-spacing: 0.05em;">"Where ideas reveal their true weight, and honesty becomes quantifiable."</span>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # SECTION 1: CONNECTED PLATFORMS - Key-Keyhole Design
    # ══════════════════════════════════════════════════════════════
    st.markdown("""
    <div style="background: linear-gradient(180deg, rgba(0,255,65,0.15) 0%, rgba(0,255,65,0.05) 100%);
                border: 2px solid #00ff41; border-radius: 10px 10px 0 0; padding: 0.8em 1.2em; margin-top: 1em;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h2 style="margin: 0; color: #00ff41 !important;">📡 CONNECTED PLATFORMS</h2>
            <span style="background: rgba(0,0,0,0.5); border: 1px solid #00ff41; border-radius: 4px;
                        padding: 0.3em 0.8em; font-family: 'Courier New', monospace; font-size: 0.9em;
                        color: #00ff41 !important; letter-spacing: 0.1em;">GATE A</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Two-panel layout with KEY-KEYHOLE connector
    col1, col_connector, col2 = st.columns([10, 1, 10])

    with col1:
        # CFA is current location (Origin Card)
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(0,30,0,0.95) 0%, rgba(0,50,20,0.9) 100%);
                    border: 3px solid #00ff41; border-right: none; border-radius: 15px 0 0 15px;
                    padding: 1.5em; padding-right: 1em; box-shadow: 0 0 20px #00ff41; height: 420px;">
            <div style="text-align: center; margin-bottom: 0.5em;">
                <span style="display: inline-block; padding: 0.3em 0.8em; font-size: 0.8em; font-weight: bold;
                            font-family: 'Courier New', monospace; text-transform: uppercase; letter-spacing: 0.15em;
                            color: #ffdd44 !important; background: rgba(255,204,0,0.2); border: 3px solid #ffcc00;
                            border-radius: 3px; box-shadow: 0 0 12px #ffcc00;">CURRENT LOCATION</span>
            </div>
            <h2 style="margin: 0.3em 0; font-size: 1.6em; text-align: center; color: #00ff41 !important;">⚙️ CFA Framework</h2>
            <p style="font-size: 0.95em; opacity: 0.8; margin-bottom: 1em; text-align: center; color: #00cc33 !important;">Epistemic Engineering Lab</p>
            <div style="display: flex; justify-content: center; gap: 1em; margin: 1em 0;">
                <div style="background: rgba(0,255,65,0.1); border: 1px solid rgba(0,255,65,0.3);
                            border-radius: 8px; padding: 0.5em 1em; text-align: center; flex: 1;">
                    <span style="display: block; font-size: 1.2em; font-weight: bold; color: #00ff41 !important;">v5.0</span>
                    <span style="display: block; font-size: 0.7em; color: #00cc33 !important; text-transform: uppercase;">Version</span>
                </div>
                <div style="background: rgba(0,255,65,0.1); border: 1px solid rgba(0,255,65,0.3);
                            border-radius: 8px; padding: 0.5em 1em; text-align: center; flex: 1;">
                    <span style="display: block; font-size: 1.2em; font-weight: bold; color: #00ff41 !important;">98%</span>
                    <span style="display: block; font-size: 0.7em; color: #00cc33 !important; text-transform: uppercase;">Health</span>
                </div>
                <div style="background: rgba(0,255,65,0.1); border: 1px solid rgba(0,255,65,0.3);
                            border-radius: 8px; padding: 0.5em 1em; text-align: center; flex: 1;">
                    <span style="display: block; font-size: 1.2em; font-weight: bold; color: #00ff41 !important;">3</span>
                    <span style="display: block; font-size: 0.7em; color: #00cc33 !important; text-transform: uppercase;">Auditors</span>
                </div>
            </div>
            <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 0.5em; margin-top: 1em;">
                <span style="background: rgba(0,255,65,0.15); border: 1px solid #00ff41; border-radius: 12px;
                            padding: 0.3em 0.8em; font-size: 0.75em; color: #00ff41 !important;">Trinity Auditors</span>
                <span style="background: rgba(0,255,65,0.15); border: 1px solid #00ff41; border-radius: 12px;
                            padding: 0.3em 0.8em; font-size: 0.75em; color: #00ff41 !important;">BFI/YPA</span>
                <span style="background: rgba(0,255,65,0.15); border: 1px solid #00ff41; border-radius: 12px;
                            padding: 0.3em 0.8em; font-size: 0.75em; color: #00ff41 !important;">Brute Ledger</span>
                <span style="background: rgba(0,255,65,0.15); border: 1px solid #00ff41; border-radius: 12px;
                            padding: 0.3em 0.8em; font-size: 0.75em; color: #00ff41 !important;">Matrix Portal</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_connector:
        # Key-Keyhole connector
        st.markdown("""
        <div style="display: flex; flex-direction: column; justify-content: center; align-items: center;
                    height: 420px; position: relative;">
            <div style="width: 50px; height: 70px; position: relative; display: flex; align-items: center; justify-content: center;">
                <div style="position: absolute; left: 0; width: 28px; height: 50px;
                            background: linear-gradient(90deg, rgba(0,50,20,0.95) 0%, rgba(0,80,30,0.9) 100%);
                            border: 2px solid #00ff41; border-left: none;
                            border-radius: 0 25px 25px 0;
                            box-shadow: 0 0 15px rgba(0,255,65,0.5);"></div>
                <div style="position: absolute; right: 0; width: 28px; height: 54px;
                            background: linear-gradient(90deg, rgba(60,0,60,0.9) 0%, rgba(40,0,40,0.95) 100%);
                            border: 2px solid #ff00ff; border-right: none;
                            border-radius: 27px 0 0 27px;
                            box-shadow: 0 0 15px rgba(255,0,255,0.5);"></div>
                <span style="position: relative; z-index: 10; font-size: 1.3em;
                            filter: drop-shadow(0 0 8px #00ff41) drop-shadow(0 0 8px #ff00ff);">⚡</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Pan Handler Central (Portal Destination)
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(40,0,40,0.95) 0%, rgba(20,0,30,0.9) 100%);
                    border: 4px solid #ff00ff; border-left: none; border-radius: 0 15px 15px 0;
                    padding: 1.5em; padding-left: 1em; box-shadow: 0 0 25px #ff00ff;
                    height: 420px;">
            <div style="text-align: center; margin-bottom: 0.5em;">
                <span style="display: inline-block; padding: 0.3em 0.8em; font-size: 0.85em; font-weight: bold;
                            font-family: 'Courier New', monospace; text-transform: uppercase; letter-spacing: 0.15em;
                            color: #ff66ff !important; background: rgba(255,0,255,0.25); border: 3px solid #ff00ff;
                            border-radius: 3px; box-shadow: 0 0 15px #ff00ff;">LIVE PORTAL</span>
            </div>
            <h2 style="margin: 0.3em 0; text-align: center; font-size: 1.6em; color: #ff00ff !important;">🏛️ Pan Handler Central</h2>
            <p style="text-align: center; font-size: 0.85em; opacity: 0.7; margin-bottom: 1em; color: #cc66cc !important;">Federation Hub - All Worlds Connect</p>
            <div style="display: flex; justify-content: center; align-items: center; margin: 1.5em 0;">
                <div style="width: 120px; height: 120px; border-radius: 50%; border: 4px solid #ff00ff;
                            box-shadow: 0 0 25px #ff00ff;
                            display: flex; justify-content: center; align-items: center;
                            background: radial-gradient(circle, rgba(255,0,255,0.3) 0%, rgba(40,0,40,0.8) 70%);">
                    <div style="width: 80px; height: 80px; border-radius: 50%; border: 3px solid #ff66ff;
                                display: flex; justify-content: center; align-items: center;
                                box-shadow: 0 0 15px #ff00ff;
                                background: radial-gradient(circle, rgba(255,0,255,0.4) 0%, transparent 70%);">
                        <span style="font-size: 2.5em;">🌀</span>
                    </div>
                </div>
            </div>
            <div style="text-align: center; margin-top: 1em;">
                <a href="https://pan-handlers.streamlit.app/" target="_blank"
                   style="display: inline-block; padding: 0.8em 2em; background: linear-gradient(135deg, #ff00ff 0%, #cc00cc 100%);
                          color: white !important; text-decoration: none; font-weight: bold; font-size: 1.1em;
                          border-radius: 25px; border: 3px solid #ff66ff;
                          box-shadow: 0 0 20px #ff00ff;">
                    🚀 JUMP TO HUB 🚀
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # SECTION 2: LOCAL DASHBOARDS
    # ══════════════════════════════════════════════════════════════
    st.markdown("""
    <div style="background: linear-gradient(180deg, rgba(0,255,65,0.15) 0%, rgba(0,255,65,0.05) 100%);
                border: 2px solid #00ff41; border-radius: 10px 10px 0 0; padding: 0.8em 1.2em; margin-top: 2em;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h2 style="margin: 0; color: #00ff41 !important;">🏠 CFA LOCAL DASHBOARDS</h2>
            <span style="background: rgba(0,0,0,0.5); border: 1px solid #00ff41; border-radius: 4px;
                        padding: 0.3em 0.8em; font-family: 'Courier New', monospace; font-size: 0.9em;
                        color: #00ff41 !important; letter-spacing: 0.1em;">GATE B</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background: rgba(0,0,0,0.3); border: 1px solid rgba(0,255,65,0.3);
                border-top: none; border-radius: 0 0 10px 10px; padding: 1em;">
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="portal-card">
            <h3>📊 Health Dashboard <span class="neon-active">ACTIVE</span></h3>
            <p><strong>Purpose:</strong> Repository health visualization</p>
            <p><strong>Port:</strong> localhost:8504</p>
            <p><strong>Features:</strong></p>
            <ul>
                <li>Overall health score (98/100)</li>
                <li>7-category breakdown</li>
                <li>README directory matrix</li>
                <li>3-month health trends</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Open Health Dashboard", key="open_health", use_container_width=True):
            st.session_state.show_health_embed = True
            st.rerun()

        if 'show_health_embed' in st.session_state and st.session_state.show_health_embed:
            st.markdown("### 📊 Live Health Dashboard")
            st.components.v1.iframe("http://localhost:8504", height=800, scrolling=True)
            if st.button("✖️ Close Dashboard", key="close_health"):
                st.session_state.show_health_embed = False
                st.rerun()

    with col2:
        st.markdown("""
        <div class="portal-card">
            <h3>🔺 SMV Trinity <span class="neon-active">ACTIVE</span></h3>
            <p><strong>Purpose:</strong> Symmetry Matrix Visualizer</p>
            <p><strong>Port:</strong> localhost:3001</p>
            <p><strong>Features:</strong></p>
            <ul>
                <li>Claude ↔ Nova ↔ Grok triangle</li>
                <li>Real-time symmetry tracking</li>
                <li>Calibration drift analysis</li>
                <li>Crux detection alerts</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Open SMV Trinity", key="open_smv", use_container_width=True):
            st.warning("**SMV Trinity Dashboard:**\n\n⚠️ **Note:** SMV Trinity must be running first!\n\n**To launch:**\n```bash\ncd dashboard\nlaunch_smv.bat\n```\n\n**Then visit:** http://localhost:3001")

    st.markdown('</div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # SECTION 3: EXTERNAL REPOSITORIES
    # ══════════════════════════════════════════════════════════════
    st.markdown("""
    <div style="background: linear-gradient(180deg, rgba(0,255,65,0.15) 0%, rgba(0,255,65,0.05) 100%);
                border: 2px solid #00ff41; border-radius: 10px 10px 0 0; padding: 0.8em 1.2em; margin-top: 2em;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h2 style="margin: 0; color: #00ff41 !important;">🌌 EXTERNAL REPOSITORIES</h2>
            <span style="background: rgba(0,0,0,0.5); border: 1px solid #00ff41; border-radius: 4px;
                        padding: 0.3em 0.8em; font-family: 'Courier New', monospace; font-size: 0.9em;
                        color: #00ff41 !important; letter-spacing: 0.1em;">GATE C</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Nyquist card
    col_spacer1, col_center, col_spacer2 = st.columns([1, 2, 1])
    with col_center:
        st.markdown("""
        <div class="portal-card" style="text-align: center;">
            <h3>📡 Nyquist Consciousness <span class="neon-active">LINKED</span></h3>
            <p><strong>Purpose:</strong> Persona testing laboratory / Core Engine</p>
            <p><strong>Integration:</strong> CFA v5.0 (S7-S10 physics)</p>
            <p><strong>Features:</strong></p>
            <div style="display: flex; flex-wrap: wrap; justify-content: center; gap: 0.5em; margin-top: 1em;">
                <span class="feature-tag">S0-S9 Stack</span>
                <span class="feature-tag">AI Armada</span>
                <span class="feature-tag">Omega Nova</span>
                <span class="feature-tag">Pattern Fidelity</span>
                <span class="feature-tag">LITE Seeds</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔗 View Nyquist Repository", key="view_nyquist", use_container_width=True):
            st.info("**Nyquist Consciousness:**\n\ngithub.com/ZiggyZigg/Nyquist_Consciousness\n\n**Local Sync:** `docs/Nyquist-sync/`")

    # ══════════════════════════════════════════════════════════════
    # SECTION 4: STATION METRICS
    # ══════════════════════════════════════════════════════════════
    st.markdown("""
    <div class="platform-gate">
        <div style="display: flex; justify-content: space-between; align-items: center; padding-bottom: 1em;
                    border-bottom: 1px solid rgba(0,255,65,0.3); margin-bottom: 1em;">
            <h2 style="margin: 0;">📊 STATION METRICS</h2>
            <span style="font-family: 'Courier New', monospace; font-size: 0.8em; color: #00cc33 !important;
                        background: rgba(0,255,65,0.1); padding: 0.3em 0.8em; border-radius: 4px;
                        border: 1px solid rgba(0,255,65,0.3);">CONTROL</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("CFA Health", "98/100", delta="A+")
        st.caption("Repository health")

    with col2:
        st.metric("Platforms", "3", delta="Connected")
        st.caption("CFA + Nyquist + Pan Handler")

    with col3:
        st.metric("Auditors", "3", delta="Trinity")
        st.caption("Claude, Grok, Nova")

    with col4:
        st.metric("Frameworks", "2", delta="Audited")
        st.caption("MdN + CT (98% convergence)")

    # ══════════════════════════════════════════════════════════════
    # FOOTER
    # ══════════════════════════════════════════════════════════════
    st.markdown("""
    <div class="matrix-footer">
        <p><strong>🚉 PAN HANDLER TRANSIT HUB</strong></p>
        <p style="font-size: 0.9em; opacity: 0.7;">
            "These are the things we built together that neither could have done alone."
        </p>
        <p style="font-size: 0.8em; opacity: 0.5;">
            The Grand Hall - Where Human-AI Collaboration Becomes Infrastructure
        </p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    render()
