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


def load_pan_handler_projects():
    """Load flagship projects from Pan_Handlers/projects.json"""
    projects_file = Path("Pan_Handlers") / "projects.json"
    if projects_file.exists():
        with open(projects_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None


def render():
    """Render The Matrix portal hub"""
    manifest = load_pan_handler_manifest()
    pan_handler_data = load_pan_handler_projects()

    # ==========================================================================
    # MATRIX THEME CSS - ALL STYLES SCOPED TO .matrix-page WRAPPER
    # This prevents CSS from leaking to other pages (Landing, Console, etc.)
    # ==========================================================================
    st.markdown("""
        <style>
        /* ===== MATRIX THEME - SCOPED TO .matrix-page ===== */
        /* All selectors prefixed with .matrix-page to prevent global leaking */

        /* ===== KEYFRAME ANIMATIONS ===== */
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

        @keyframes beamPulse {
            0%, 100% { opacity: 0.3; }
            50% { opacity: 1; }
        }

        @keyframes keyPulse {
            0%, 100% { box-shadow: 0 0 10px rgba(0,255,65,0.3), inset 0 0 10px rgba(0,255,65,0.1); }
            50% { box-shadow: 0 0 25px rgba(0,255,65,0.6), 0 0 40px rgba(0,255,65,0.3), inset 0 0 20px rgba(0,255,65,0.2); }
        }

        @keyframes mirrorShimmer {
            0%, 100% { left: -100%; }
            50% { left: 150%; }
        }

        @keyframes keyholeGlow {
            0%, 100% { opacity: 0.5; }
            50% { opacity: 1; }
        }

        @keyframes hologramScan {
            0% { background-position: 0% 0%; }
            100% { background-position: 0% 100%; }
        }

        /* ===== BASE CONTAINER - BLACK BACKGROUND ===== */
        .matrix-page {
            background-color: #0a0a0a !important;
            color: #00ff41 !important;
            font-family: 'Courier New', monospace;
            padding: 1em;
            min-height: 100vh;
        }

        /* ===== ALL TEXT ELEMENTS - MATRIX GREEN ===== */
        .matrix-page p,
        .matrix-page span,
        .matrix-page label,
        .matrix-page li,
        .matrix-page div,
        .matrix-page strong,
        .matrix-page b,
        .matrix-page em,
        .matrix-page i {
            color: #00ff41 !important;
        }

        .matrix-page a {
            color: #00cc33 !important;
        }

        .matrix-page a:hover {
            color: #00ff41 !important;
            text-shadow: 0 0 10px rgba(0,255,65,0.5);
        }

        /* ===== HEADERS ===== */
        .matrix-page h1,
        .matrix-page h2,
        .matrix-page h3,
        .matrix-page h4,
        .matrix-page h5,
        .matrix-page h6 {
            color: #00ff41 !important;
            font-family: 'Courier New', monospace;
            font-weight: bold !important;
        }

        .matrix-page h1 {
            border-bottom: 2px solid #00ff41;
            padding-bottom: 0.5rem;
        }

        /* Strong/bold text - bright green with glow */
        .matrix-page strong,
        .matrix-page b {
            color: #00ff41 !important;
            text-shadow: 0 0 5px rgba(0,255,65,0.5);
        }

        /* Italic/emphasis - dimmer green */
        .matrix-page em,
        .matrix-page i {
            color: #00cc33 !important;
        }

        /* ===== TUNNEL CARD - Main header element ===== */
        .matrix-page .tunnel-card {
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
        .matrix-page .platform-gate {
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

        .matrix-page .platform-gate::before {
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: linear-gradient(90deg, transparent, #00ff41, transparent);
            animation: dataStream 3s linear infinite;
        }

        .matrix-page .platform-header {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding-bottom: 1em;
            border-bottom: 1px solid rgba(0,255,65,0.3);
            margin-bottom: 1em;
        }

        .matrix-page .platform-id {
            font-family: 'Courier New', monospace;
            font-size: 0.8em;
            color: #00cc33 !important;
            background: rgba(0,255,65,0.1);
            padding: 0.3em 0.8em;
            border-radius: 4px;
            border: 1px solid rgba(0,255,65,0.3);
        }

        /* ===== PORTAL CARD ===== */
        .matrix-page .portal-card {
            background: linear-gradient(135deg, rgba(0,255,65,0.1) 0%, rgba(0,204,51,0.05) 100%) !important;
            border: 2px solid #00ff41;
            border-radius: 10px;
            padding: 1.5em;
            margin-bottom: 1em;
            box-shadow: 0 0 20px rgba(0,255,65,0.3);
        }

        .matrix-page .portal-card h3 {
            color: #00ff41 !important;
            margin-top: 0;
            font-family: 'Courier New', monospace;
        }

        .matrix-page .portal-card p,
        .matrix-page .portal-card li,
        .matrix-page .portal-card strong,
        .matrix-page .portal-card em,
        .matrix-page .portal-card span {
            color: #00ff41 !important;
        }

        /* ===== PORTAL CHAMBER - Hub + Gateway unified ===== */
        .matrix-page .portal-chamber {
            background: linear-gradient(135deg, rgba(0,20,0,0.95) 0%, rgba(0,40,0,0.9) 50%, rgba(0,20,0,0.95) 100%) !important;
            border: 2px solid #00ff41;
            border-radius: 20px;
            padding: 1.5em;
            margin: 1em 0;
            box-shadow: 0 0 40px rgba(0,255,65,0.2), inset 0 0 60px rgba(0,255,65,0.05);
        }

        .matrix-page .chamber-content {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 1em;
            flex-wrap: wrap;
        }

        .matrix-page .chamber-hub {
            flex: 1 1 55%;
            min-width: 280px;
            padding-right: 1em;
        }

        .matrix-page .chamber-hub h3 {
            color: #00ff41 !important;
            font-family: 'Courier New', monospace !important;
            font-size: 1.3em;
            margin-bottom: 0.5em;
            text-shadow: 0 0 10px rgba(0,255,65,0.5);
        }

        .matrix-page .chamber-hub p {
            color: #00cc33 !important;
            font-family: 'Courier New', monospace !important;
            font-size: 0.9em;
            margin: 0.3em 0;
        }

        .matrix-page .portal-beam {
            flex: 0 0 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            height: 120px;
        }

        .matrix-page .beam-line {
            width: 4px;
            height: 100%;
            background: linear-gradient(180deg, transparent, #00ff41, #00ff88, #00ff41, transparent);
            background-size: 100% 200%;
            animation: beamFlow 2s linear infinite;
            border-radius: 2px;
            box-shadow: 0 0 10px rgba(0,255,65,0.5);
        }

        .matrix-page .beam-pulse {
            position: absolute;
            width: 12px;
            height: 12px;
            background: #00ff41;
            border-radius: 50%;
            animation: beamPulse 1.5s ease-in-out infinite;
            box-shadow: 0 0 20px rgba(0,255,65,0.8);
        }

        .matrix-page .chamber-portal {
            flex: 0 0 150px;
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
        }

        .matrix-page .portal-ring {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            border: 3px solid #00ff41;
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
            animation: portalPulse 3s ease-in-out infinite;
            background: radial-gradient(circle, rgba(0,255,65,0.1) 0%, transparent 70%);
        }

        .matrix-page .portal-ring::before {
            content: '';
            position: absolute;
            width: 120%;
            height: 120%;
            border: 2px dashed rgba(0,255,65,0.3);
            border-radius: 50%;
            animation: portalSpin 8s linear infinite;
        }

        .matrix-page .portal-inner {
            width: 70px;
            height: 70px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(0,80,30,0.9) 0%, rgba(0,40,15,0.95) 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            border: 2px solid rgba(0,255,65,0.5);
        }

        .matrix-page .portal-icon {
            font-size: 2em;
            animation: portalSpin 4s linear infinite reverse;
        }

        .matrix-page .portal-btn {
            display: inline-block;
            background: linear-gradient(135deg, #00ff41 0%, #00cc33 100%);
            color: #0a0a0a !important;
            padding: 0.6em 1.2em;
            border-radius: 25px;
            font-weight: bold;
            font-family: 'Courier New', monospace;
            text-decoration: none;
            font-size: 0.9em;
            margin-top: 0.8em;
            transition: all 0.3s ease;
            box-shadow: 0 0 15px rgba(0,255,65,0.5);
        }

        .matrix-page .portal-btn:hover {
            background: linear-gradient(135deg, #00ff88 0%, #00ff41 100%);
            box-shadow: 0 0 30px rgba(0,255,65,0.8), 0 0 50px rgba(0,255,65,0.4);
            transform: scale(1.1);
        }

        .matrix-page .portal-status {
            color: #00ff41 !important;
            font-family: 'Courier New', monospace !important;
            font-size: 0.7em;
            margin-top: 0.5em;
            opacity: 0.8;
        }

        /* ===== NEON BADGES ===== */
        .matrix-page .neon-live {
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

        .matrix-page .neon-here {
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

        .matrix-page .neon-active {
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
        .matrix-page .feature-tag {
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

        .matrix-page .feature-tag:hover {
            background: rgba(0,255,65,0.25);
            box-shadow: 0 0 10px rgba(0,255,65,0.4);
        }

        .matrix-page .feature-grid {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 0.4em;
            margin-top: 0.8em;
        }

        /* ===== STATUS BADGES ===== */
        .matrix-page .status-badge {
            display: inline-block;
            padding: 0.3em 0.8em;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: bold;
            margin-left: 0.5em;
        }

        .matrix-page .badge-active {
            background: rgba(0,255,65,0.2) !important;
            color: #00ff41 !important;
            border: 1px solid #00ff41;
        }

        .matrix-page .badge-here {
            background: rgba(0,255,65,0.3) !important;
            color: #00ff41 !important;
            border: 1px solid #00ff41;
            text-shadow: 0 0 5px rgba(0,255,65,0.5);
        }

        .matrix-page .badge-coming-soon {
            background: rgba(0,204,51,0.2) !important;
            color: #00cc33 !important;
            border: 1px solid #00cc33;
        }

        /* ===== DEPARTURE BOARD ===== */
        .matrix-page .departure-board {
            background: linear-gradient(180deg, #0a0a0a 0%, #151515 100%);
            border: 3px solid #333;
            border-radius: 10px;
            padding: 1em;
            font-family: 'Courier New', monospace;
            box-shadow:
                inset 0 0 20px rgba(0,0,0,0.8),
                0 5px 20px rgba(0,0,0,0.5);
        }

        .matrix-page .departure-row {
            display: flex;
            align-items: center;
            padding: 0.8em;
            border-bottom: 1px solid #222;
            transition: background 0.3s;
        }

        .matrix-page .departure-row:hover {
            background: rgba(0,255,65,0.05);
        }

        .matrix-page .departure-dest {
            flex: 2;
            color: #ffaa00 !important;
            font-weight: bold;
            text-shadow: 0 0 10px rgba(255,170,0,0.5);
        }

        .matrix-page .departure-status {
            flex: 1;
            text-align: center;
        }

        .matrix-page .departure-platform {
            flex: 0.5;
            text-align: right;
            color: #00ff41 !important;
            font-size: 1.2em;
            font-weight: bold;
        }

        /* ===== MATRIX FOOTER ===== */
        .matrix-page .matrix-footer {
            text-align: center;
            color: #00ff41 !important;
            font-family: 'Courier New', monospace;
            margin-top: 2em;
        }

        .matrix-page .matrix-footer p {
            color: #00ff41 !important;
        }

        /* ===== HUB CARD ===== */
        .matrix-page .hub-card {
            background: linear-gradient(135deg, rgba(0,255,65,0.12) 0%, rgba(0,204,51,0.06) 100%) !important;
            border: 2px solid #00ff41;
            border-radius: 12px;
            padding: 2em;
            margin: 1.5em auto;
            max-width: 700px;
            box-shadow: 0 0 30px rgba(0,255,65,0.4);
            text-align: center;
        }

        .matrix-page .hub-card h3 {
            color: #00ff41 !important;
            font-family: 'Courier New', monospace;
            font-size: 1.8em;
            margin-bottom: 0.5em;
            letter-spacing: 0.05em;
        }

        .matrix-page .hub-card p,
        .matrix-page .hub-card strong,
        .matrix-page .hub-card em,
        .matrix-page .hub-card span {
            color: #00cc33 !important;
            font-family: 'Courier New', monospace;
        }

        .matrix-page .hub-card li {
            color: #00ff41 !important;
            font-family: 'Courier New', monospace;
            margin: 0.3em 0;
        }

        /* ===== FLAGSHIP CARD ===== */
        .matrix-page .flagship-card {
            background: linear-gradient(135deg, rgba(0,255,65,0.08) 0%, rgba(0,204,51,0.04) 100%) !important;
            border: 2px solid #00cc33;
            border-radius: 10px;
            padding: 1.2em;
            margin-bottom: 0.8em;
            box-shadow: 0 0 15px rgba(0,255,65,0.2);
        }

        .matrix-page .flagship-card h4 {
            color: #00ff41 !important;
            margin-top: 0;
            margin-bottom: 0.5em;
            font-family: 'Courier New', monospace;
        }

        .matrix-page .flagship-card p,
        .matrix-page .flagship-card strong,
        .matrix-page .flagship-card em,
        .matrix-page .flagship-card span {
            color: #00cc33 !important;
            margin-bottom: 0.3em;
            font-size: 0.95em;
        }

        /* ===== SECTION HEADER ===== */
        .matrix-page .section-header {
            color: #00ff41 !important;
            font-size: 1.5em;
            font-weight: bold;
            margin-top: 1.5em;
            margin-bottom: 0.8em;
            font-family: 'Courier New', monospace;
            border-bottom: 2px solid #00ff41;
            padding-bottom: 0.3em;
        }

        /* ===== PHILOSOPHY QUOTE ===== */
        .matrix-page .philosophy-quote {
            font-size: 1.3em;
            font-weight: bold;
            color: #00ff41 !important;
            text-align: center;
            padding: 1em;
            font-family: 'Courier New', monospace;
            text-shadow: 0 0 10px rgba(0,255,65,0.3);
        }

        /* ===== MOBILE RESPONSIVE ===== */
        @media (max-width: 600px) {
            .matrix-page .chamber-content {
                flex-direction: column;
                text-align: center;
            }
            .matrix-page .chamber-hub {
                padding-right: 0;
            }
            .matrix-page .portal-beam {
                height: 40px;
                width: 100%;
            }
            .matrix-page .beam-line {
                width: 100%;
                height: 4px;
                background: linear-gradient(90deg, transparent, #00ff41, #00ff88, #00ff41, transparent);
            }
        }
        </style>
    """, unsafe_allow_html=True)

    # ==========================================================================
    # START MATRIX PAGE WRAPPER - All content inside this div gets Matrix theme
    # ==========================================================================
    st.markdown('<div class="matrix-page">', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # HEADER - Back button
    # ══════════════════════════════════════════════════════════════
    col_header, col_home = st.columns([6, 1])
    with col_home:
        if st.button("Home"):
            st.session_state.page = 'landing'
            st.experimental_rerun()

    # ══════════════════════════════════════════════════════════════
    # TRANSIT HUB HEADER
    # ══════════════════════════════════════════════════════════════
    st.markdown("""
    <div class="tunnel-card">
        <h1 style="font-size: 2.2em; margin: 0; letter-spacing: 0.1em; color: #00ff41 !important;">DIMENSIONAL TRANSIT HUB</h1>
        <p style="font-size: 1.1em; margin: 0.5em 0; color: #00ff41 !important;">Pan Handler Central Station</p>
        <p style="font-size: 0.85em; opacity: 0.7; color: #00cc33 !important;">Where Projects Travel Between Worlds</p>
    </div>
    """, unsafe_allow_html=True)

    # Philosophy banner
    philosophy = "Where ideas reveal their true weight, and honesty becomes quantifiable."
    if pan_handler_data:
        philosophy = pan_handler_data.get('meta', {}).get('philosophy', philosophy)

    st.markdown(f"""
    <div style="text-align: center; padding: 1em; margin: 1em 0;
                background: linear-gradient(90deg, transparent 0%, rgba(0,255,65,0.1) 50%, transparent 100%);
                border-top: 1px solid rgba(0,255,65,0.3); border-bottom: 1px solid rgba(0,255,65,0.3);">
        <span style="font-family: 'Courier New', monospace; font-size: 1.1em; color: #00ff41 !important;
                    letter-spacing: 0.05em;">"{philosophy}"</span>
    </div>
    """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # SECTION 1: CONNECTED PLATFORMS - Key-Keyhole Design
    # ══════════════════════════════════════════════════════════════
    st.markdown("""
    <div style="background: linear-gradient(180deg, rgba(0,255,65,0.15) 0%, rgba(0,255,65,0.05) 100%);
                border: 2px solid #00ff41; border-radius: 10px 10px 0 0; padding: 0.8em 1.2em; margin-top: 1em;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h2 style="margin: 0; color: #00ff41 !important;">CONNECTED PLATFORMS</h2>
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
            <h2 style="margin: 0.3em 0; font-size: 1.6em; text-align: center; color: #00ff41 !important;">CFA Framework</h2>
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
                <span class="feature-tag">Trinity Auditors</span>
                <span class="feature-tag">BFI/YPA</span>
                <span class="feature-tag">Brute Ledger</span>
                <span class="feature-tag">Matrix Portal</span>
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
                            filter: drop-shadow(0 0 8px #00ff41) drop-shadow(0 0 8px #ff00ff);">*</span>
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
                <span class="neon-live">LIVE PORTAL</span>
            </div>
            <h2 style="margin: 0.3em 0; text-align: center; font-size: 1.6em; color: #ff00ff !important;">Pan Handler Central</h2>
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
                        <span style="font-size: 2.5em;">~</span>
                    </div>
                </div>
            </div>
            <div style="text-align: center; margin-top: 1em;">
                <a href="https://pan-handlers.streamlit.app/" target="_blank"
                   style="display: inline-block; padding: 0.8em 2em; background: linear-gradient(135deg, #ff00ff 0%, #cc00cc 100%);
                          color: white !important; text-decoration: none; font-weight: bold; font-size: 1.1em;
                          border-radius: 25px; border: 3px solid #ff66ff;
                          box-shadow: 0 0 20px #ff00ff;">
                    JUMP TO HUB
                </a>
            </div>
        </div>
        """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # SECTION 2: DEPARTURES - Flagship Projects
    # ══════════════════════════════════════════════════════════════
    st.markdown("""
    <div style="background: linear-gradient(180deg, rgba(0,255,65,0.15) 0%, rgba(0,255,65,0.05) 100%);
                border: 2px solid #00ff41; border-radius: 10px 10px 0 0; padding: 0.8em 1.2em; margin-top: 2em;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h2 style="margin: 0; color: #00ff41 !important;">DEPARTURES - Flagship Projects</h2>
            <span style="background: rgba(0,0,0,0.5); border: 1px solid #00ff41; border-radius: 4px;
                        padding: 0.3em 0.8em; font-family: 'Courier New', monospace; font-size: 0.9em;
                        color: #00ff41 !important; letter-spacing: 0.1em;">GATE B</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if pan_handler_data and 'flagship_projects' in pan_handler_data:
        projects = pan_handler_data['flagship_projects']

        # Departure board style
        st.markdown("""
        <div style="background: rgba(0,0,0,0.3); border: 1px solid rgba(0,255,65,0.3);
                    border-top: none; border-radius: 0 0 10px 10px; padding: 0.5em;">
        """, unsafe_allow_html=True)

        # Header row
        st.markdown("""
        <div style="display: flex; align-items: center; background: rgba(0,255,65,0.08);
                    border-bottom: 2px solid #00ff41; padding: 0.5em 0.8em;">
            <span style="flex: 2; color: #00ff41 !important; font-weight: bold; font-size: 0.9em; text-transform: uppercase; letter-spacing: 0.1em;">DESTINATION</span>
            <span style="flex: 1; text-align: center; color: #00ff41 !important; font-weight: bold; font-size: 0.9em; text-transform: uppercase; letter-spacing: 0.1em;">STATUS</span>
            <span style="flex: 1; color: #00ff41 !important; font-weight: bold; font-size: 0.9em; text-transform: uppercase; letter-spacing: 0.1em;">TRACK</span>
            <span style="flex: 0.5; text-align: right; color: #00ff41 !important; font-weight: bold; font-size: 0.9em; text-transform: uppercase; letter-spacing: 0.1em;">SYNC</span>
        </div>
        """, unsafe_allow_html=True)

        # CFA as first entry - connected repo
        st.markdown("""
        <div style="display: flex; align-items: center; padding: 0.6em 0.8em;
                    background: rgba(0,170,255,0.05); border-left: 3px solid #00aaff;
                    border-bottom: 1px solid rgba(0,255,65,0.15);">
            <span style="flex: 2; color: #00aaff !important; font-weight: bold;">CFA Framework</span>
            <span style="flex: 1; text-align: center;">
                <span style="display: inline-block; padding: 0.2em 0.6em; font-size: 0.75em; font-weight: bold;
                            color: #00aaff !important; background: rgba(0,170,255,0.15); border: 1px solid #00aaff;
                            border-radius: 3px;">LINKED</span>
            </span>
            <span style="flex: 1; color: #888; font-size: 0.85em;">Framework / v5.0</span>
            <span style="flex: 0.5; text-align: right; color: #00aaff !important;">*</span>
        </div>
        """, unsafe_allow_html=True)

        # Sync level tooltips
        sync_tooltips = {
            1: "Solo", 2: "Pair", 3: "Squad", 4: "Squad",
            5: "Coalition", 6: "Coalition", 7: "Movement", 8: "Movement", 9: "Civilization"
        }

        for project in projects[:7]:
            status = project.get('status', 'Concept')
            if status == "In Preparation":
                status_badge = '<span style="display: inline-block; padding: 0.2em 0.6em; font-size: 0.75em; font-weight: bold; color: #00aaff !important; background: rgba(0,170,255,0.15); border: 1px solid #00aaff; border-radius: 3px; text-shadow: 0 0 5px rgba(0,170,255,0.5);">BOARDING</span>'
            elif status == "Complete":
                status_badge = '<span style="display: inline-block; padding: 0.2em 0.6em; font-size: 0.75em; font-weight: bold; color: #ffcc00 !important; background: rgba(255,204,0,0.15); border: 1px solid #ffcc00; border-radius: 3px; text-shadow: 0 0 5px rgba(255,204,0,0.5);">ARRIVED</span>'
            else:
                status_badge = '<span style="color: #666; border: 1px solid #444; padding: 0.2em 0.5em; border-radius: 3px; font-size: 0.8em;">SCHEDULED</span>'

            track = project.get('track', 'TBD')
            sync_level = project.get('sync_level', 5)

            st.markdown(f"""
            <div style="display: flex; align-items: center; padding: 0.6em 0.8em; border-bottom: 1px solid rgba(0,255,65,0.15);">
                <span style="flex: 2; color: #ffaa00 !important; font-weight: bold;">{project.get('title', 'Untitled')[:35]}</span>
                <span style="flex: 1; text-align: center;">{status_badge}</span>
                <span style="flex: 1; color: #888; font-size: 0.85em;">{track}</span>
                <span style="flex: 0.5; text-align: right; color: #00ff41 !important; font-weight: bold;">{sync_level}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)

        # Sync Level Legend
        st.markdown("""
        <div style="margin-top: 1em; padding: 1em; background: rgba(0,255,65,0.05); border: 1px solid rgba(0,255,65,0.2); border-radius: 8px;">
            <div style="display: flex; align-items: center; gap: 0.5em; margin-bottom: 0.8em;">
                <span style="color: #00ff41 !important; font-weight: bold; font-size: 0.9em;">SYNC LEVEL</span>
                <span style="color: #00cc33 !important; font-size: 0.8em; opacity: 0.8;">- Collaborative Resonance Required</span>
            </div>
            <div style="display: flex; flex-wrap: wrap; gap: 0.8em; font-size: 0.75em; font-family: 'Courier New', monospace;">
                <span style="color: #888;"><span style="color: #00ff41; font-weight: bold;">1-2</span> Solo/Pair</span>
                <span style="color: #888;"><span style="color: #00ff41; font-weight: bold;">3-4</span> Squad</span>
                <span style="color: #888;"><span style="color: #00ff41; font-weight: bold;">5-6</span> Coalition</span>
                <span style="color: #888;"><span style="color: #ffd700; font-weight: bold;">7-8</span> Movement</span>
                <span style="color: #888;"><span style="color: #ff00ff; font-weight: bold;">9</span> Civilization</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: rgba(0,0,0,0.3); border: 1px solid rgba(0,255,65,0.3);
                    border-top: none; border-radius: 0 0 10px 10px; padding: 1em; text-align: center;">
            <p style="color: #00cc33 !important;">Loading departures from Pan_Handlers/projects.json...</p>
        </div>
        """, unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # SECTION 3: LOCAL DASHBOARDS
    # ══════════════════════════════════════════════════════════════
    st.markdown("""
    <div style="background: linear-gradient(180deg, rgba(0,255,65,0.15) 0%, rgba(0,255,65,0.05) 100%);
                border: 2px solid #00ff41; border-radius: 10px 10px 0 0; padding: 0.8em 1.2em; margin-top: 2em;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h2 style="margin: 0; color: #00ff41 !important;">CFA LOCAL DASHBOARDS</h2>
            <span style="background: rgba(0,0,0,0.5); border: 1px solid #00ff41; border-radius: 4px;
                        padding: 0.3em 0.8em; font-family: 'Courier New', monospace; font-size: 0.9em;
                        color: #00ff41 !important; letter-spacing: 0.1em;">GATE C</span>
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
            <h3 style="color: #00ff41 !important;">Health Dashboard <span class="neon-active">ACTIVE</span></h3>
            <p style="color: #00cc33 !important;"><strong style="color: #00ff41 !important;">Purpose:</strong> Repository health visualization</p>
            <p style="color: #00cc33 !important;"><strong style="color: #00ff41 !important;">Port:</strong> localhost:8504</p>
            <p style="color: #00cc33 !important;"><strong style="color: #00ff41 !important;">Features:</strong></p>
            <ul style="color: #00cc33 !important;">
                <li style="color: #00cc33 !important;">Overall health score (98/100)</li>
                <li style="color: #00cc33 !important;">7-category breakdown</li>
                <li style="color: #00cc33 !important;">README directory matrix</li>
                <li style="color: #00cc33 !important;">3-month health trends</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Health Dashboard", key="open_health", use_container_width=True):
            st.session_state.show_health_embed = True
            st.experimental_rerun()

        if 'show_health_embed' in st.session_state and st.session_state.show_health_embed:
            st.markdown("<h3 style='color: #00ff41 !important;'>Live Health Dashboard</h3>", unsafe_allow_html=True)
            st.components.v1.iframe("http://localhost:8504", height=800, scrolling=True)
            if st.button("Close Dashboard", key="close_health"):
                st.session_state.show_health_embed = False
                st.experimental_rerun()

    with col2:
        st.markdown("""
        <div class="portal-card">
            <h3 style="color: #00ff41 !important;">SMV Trinity <span class="neon-active">ACTIVE</span></h3>
            <p style="color: #00cc33 !important;"><strong style="color: #00ff41 !important;">Purpose:</strong> Symmetry Matrix Visualizer</p>
            <p style="color: #00cc33 !important;"><strong style="color: #00ff41 !important;">Port:</strong> localhost:3001</p>
            <p style="color: #00cc33 !important;"><strong style="color: #00ff41 !important;">Features:</strong></p>
            <ul style="color: #00cc33 !important;">
                <li style="color: #00cc33 !important;">Claude - Nova - Grok triangle</li>
                <li style="color: #00cc33 !important;">Real-time symmetry tracking</li>
                <li style="color: #00cc33 !important;">Calibration drift analysis</li>
                <li style="color: #00cc33 !important;">Crux detection alerts</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open SMV Trinity", key="open_smv", use_container_width=True):
            st.warning("**SMV Trinity Dashboard:**\n\nNote: SMV Trinity must be running first!\n\n**To launch:**\n```bash\ncd dashboard\nlaunch_smv.bat\n```\n\n**Then visit:** http://localhost:3001")

    st.markdown('</div>', unsafe_allow_html=True)

    # ══════════════════════════════════════════════════════════════
    # SECTION 4: EXTERNAL REPOSITORIES
    # ══════════════════════════════════════════════════════════════
    st.markdown("""
    <div style="background: linear-gradient(180deg, rgba(0,255,65,0.15) 0%, rgba(0,255,65,0.05) 100%);
                border: 2px solid #00ff41; border-radius: 10px 10px 0 0; padding: 0.8em 1.2em; margin-top: 2em;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <h2 style="margin: 0; color: #00ff41 !important;">EXTERNAL REPOSITORIES</h2>
            <span style="background: rgba(0,0,0,0.5); border: 1px solid #00ff41; border-radius: 4px;
                        padding: 0.3em 0.8em; font-family: 'Courier New', monospace; font-size: 0.9em;
                        color: #00ff41 !important; letter-spacing: 0.1em;">GATE D</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Nyquist card
    col_spacer1, col_center, col_spacer2 = st.columns([1, 2, 1])
    with col_center:
        st.markdown("""
        <div class="portal-card" style="text-align: center;">
            <h3 style="color: #00ff41 !important;">Nyquist Consciousness <span class="neon-active">LINKED</span></h3>
            <p style="color: #00cc33 !important;"><strong style="color: #00ff41 !important;">Purpose:</strong> Persona testing laboratory / Core Engine</p>
            <p style="color: #00cc33 !important;"><strong style="color: #00ff41 !important;">Integration:</strong> CFA v5.0 (S7-S10 physics)</p>
            <p style="color: #00cc33 !important;"><strong style="color: #00ff41 !important;">Features:</strong></p>
            <div class="feature-grid">
                <span class="feature-tag">S0-S9 Stack</span>
                <span class="feature-tag">AI Armada</span>
                <span class="feature-tag">Omega Nova</span>
                <span class="feature-tag">Pattern Fidelity</span>
                <span class="feature-tag">LITE Seeds</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        if st.button("View Nyquist Repository", key="view_nyquist", use_container_width=True):
            st.info("**Nyquist Consciousness:**\n\ngithub.com/ZiggyZigg/Nyquist_Consciousness\n\n**Local Sync:** `docs/Nyquist-sync/`")

    # ══════════════════════════════════════════════════════════════
    # SECTION 5: STATION METRICS
    # ══════════════════════════════════════════════════════════════
    st.markdown("""
    <div class="platform-gate">
        <div class="platform-header">
            <h2 style="margin: 0; color: #00ff41 !important;">STATION METRICS</h2>
            <span class="platform-id">CONTROL</span>
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
        <p><strong style="color: #00ff41 !important;">PAN HANDLER TRANSIT HUB</strong></p>
        <p style="font-size: 0.9em; opacity: 0.7; color: #00cc33 !important;">
            "These are the things we built together that neither could have done alone."
        </p>
        <p style="font-size: 0.8em; opacity: 0.5; color: #00cc33 !important;">
            The Grand Hall - Where Human-AI Collaboration Becomes Infrastructure
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ==========================================================================
    # CLOSE MATRIX PAGE WRAPPER
    # ==========================================================================
    st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    render()
