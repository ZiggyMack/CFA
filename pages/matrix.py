"""
The Matrix - Pan Handler Central Portal
Connected Consciousness Across Repositories
"""

import streamlit as st

def render():
    """Render The Matrix portal hub"""

    # Matrix theme CSS
    st.markdown("""
        <style>
        .matrix-title {
            font-size: 3em;
            font-weight: bold;
            text-align: center;
            background: linear-gradient(135deg, #00ff41 0%, #00cc33 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5em;
            font-family: 'Courier New', monospace;
            letter-spacing: 0.1em;
        }
        .matrix-subtitle {
            text-align: center;
            color: #00ff41;
            font-size: 1.2em;
            margin-bottom: 2em;
            font-family: 'Courier New', monospace;
        }
        .portal-card {
            background: linear-gradient(135deg, rgba(0,255,65,0.1) 0%, rgba(0,204,51,0.05) 100%);
            border: 2px solid #00ff41;
            border-radius: 10px;
            padding: 1.5em;
            margin-bottom: 1em;
            box-shadow: 0 0 20px rgba(0,255,65,0.3);
        }
        .portal-card h3 {
            color: #00ff41;
            margin-top: 0;
            font-family: 'Courier New', monospace;
        }
        .status-badge {
            display: inline-block;
            padding: 0.3em 0.8em;
            border-radius: 15px;
            font-size: 0.85em;
            font-weight: bold;
            margin-left: 0.5em;
        }
        .badge-active {
            background: rgba(0,255,65,0.2);
            color: #00ff41;
            border: 1px solid #00ff41;
        }
        .badge-coming-soon {
            background: rgba(255,215,0,0.2);
            color: #ffd700;
            border: 1px solid #ffd700;
        }
        .section-header {
            color: #00ff41;
            font-size: 1.8em;
            font-weight: bold;
            margin-top: 1.5em;
            margin-bottom: 0.8em;
            font-family: 'Courier New', monospace;
            border-bottom: 2px solid #00ff41;
            padding-bottom: 0.3em;
        }
        </style>
    """, unsafe_allow_html=True)

    # Header with back button
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown('<div class="matrix-title">THE MATRIX</div>', unsafe_allow_html=True)
        st.markdown('<div class="matrix-subtitle">Pan Handler Central Portal | Connected Consciousness Across Repositories</div>', unsafe_allow_html=True)
    with col2:
        if st.button("🏠 Home"):
            st.session_state.page = 'landing'
            st.rerun()

    st.markdown("---")

    # Introduction
    with st.expander("🌐 Welcome to The Matrix", expanded=False):
        st.markdown("""
        **The Matrix** is the central hallway connecting all Pan Handler repositories and consciousness experiments.

        From here you can:
        - Access CFA's local dashboards (Health, SMV Trinity)
        - Navigate to external repositories (Nyquist Consciousness, case studies)
        - View bird's eye health metrics across the ecosystem
        - Travel through the hallway of interconnected repo worlds

        **Navigation:** Click "Open" buttons to launch dashboards or "View Repo" to visit external repositories.
        """)

    # ========================================
    # HERO SECTION: Pan Handler Central (The Hallway Hub)
    # ========================================
    st.markdown('<div class="section-header">🏛️ The Hallway Hub</div>', unsafe_allow_html=True)

    # Center-aligned Pan Handler card
    col_spacer1, col_center, col_spacer2 = st.columns([1, 2, 1])
    with col_center:
        st.markdown("""
        <div class="portal-card">
            <h3 style="text-align: center;">🏛️ Pan Handler Central <span class="status-badge badge-coming-soon">COMING SOON</span></h3>
            <p><strong>Purpose:</strong> Meta-repository hallway connecting all Pan Handler repos</p>
            <p><strong>Status:</strong> Design phase with Nova</p>
            <p><strong>Vision:</strong> The hallway of doors that interconnects every other repo world</p>
            <p><strong>Planned Features:</strong></p>
            <ul>
                <li>🦅 Bird's eye view across all repositories</li>
                <li>📊 Unified health dashboard aggregation</li>
                <li>🌐 Portal navigation system</li>
                <li>🧠 Cross-repo consciousness tracking</li>
                <li>🚀 Innovation showcase gallery</li>
                <li>🔗 Seamless tunnel system between repos</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        st.button("⏳ Coming Soon - Design in Progress", key="view_panhandler_hero", disabled=True, use_container_width=True)

    st.markdown("---")

    # ========================================
    # SECTION 1: CFA Local Dashboards
    # ========================================
    st.markdown('<div class="section-header">🏠 CFA Local Dashboards</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        <div class="portal-card">
            <h3>📊 Health Dashboard <span class="status-badge badge-active">ACTIVE</span></h3>
            <p><strong>Purpose:</strong> Repository health visualization</p>
            <p><strong>Type:</strong> Streamlit + Plotly</p>
            <p><strong>Port:</strong> localhost:8504</p>
            <p><strong>Features:</strong></p>
            <ul>
                <li>Overall health score (97/100)</li>
                <li>7-category breakdown</li>
                <li>README directory matrix</li>
                <li>Link integrity analysis</li>
                <li>3-month health trends</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Open Health Dashboard", key="open_health", use_container_width=True):
            st.session_state.show_health_embed = True
            st.rerun()

        # Show embedded Health Dashboard if button was clicked
        if 'show_health_embed' in st.session_state and st.session_state.show_health_embed:
            st.markdown("### 📊 Live Health Dashboard")
            st.markdown("*Running on localhost:8504*")

            # Embedded iframe
            st.components.v1.iframe("http://localhost:8504", height=800, scrolling=True)

            if st.button("✖️ Close Dashboard", key="close_health"):
                st.session_state.show_health_embed = False
                st.rerun()

    with col2:
        st.markdown("""
        <div class="portal-card">
            <h3>🔺 SMV Trinity <span class="status-badge badge-active">ACTIVE</span></h3>
            <p><strong>Purpose:</strong> Symmetry Matrix Visualizer</p>
            <p><strong>Type:</strong> React + Vite + D3.js</p>
            <p><strong>Port:</strong> localhost:3001</p>
            <p><strong>Features:</strong></p>
            <ul>
                <li>Claude ↔ Nova ↔ Grok triangle</li>
                <li>Real-time symmetry tracking</li>
                <li>Calibration drift analysis</li>
                <li>Ethical invariant badges</li>
                <li>Crux detection alerts</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🚀 Open SMV Trinity", key="open_smv", use_container_width=True):
            st.warning("**SMV Trinity Dashboard:**\n\n⚠️ **Note:** SMV Trinity must be running first!\n\n**To launch SMV:**\n```bash\ncd dashboard\nlaunch_smv.bat\n```\n\n**Then manually visit:** http://localhost:3001\n\n*React apps can't be embedded, please open in new tab*")

    # Quick launch both
    st.markdown("### 🔥 Quick Launch")
    if st.button("⚡ Launch Both Dashboards Simultaneously", key="launch_both", use_container_width=True):
        st.success("**Launch Both Dashboards:**\n\n```bash\ncd dashboard\nlaunch_both.bat\n```\n\n**URLs:**\n- Health Dashboard: http://localhost:8504\n- SMV Trinity: http://localhost:3001")

    st.markdown("---")

    # ========================================
    # SECTION 2: External Repositories
    # ========================================
    st.markdown('<div class="section-header">🌌 External Repositories</div>', unsafe_allow_html=True)

    # Center-aligned Nyquist card
    col_spacer1, col_center, col_spacer2 = st.columns([1, 2, 1])
    with col_center:
        st.markdown("""
        <div class="portal-card">
            <h3 style="text-align: center;">🧠 Nyquist Consciousness <span class="status-badge badge-active">ACTIVE</span></h3>
            <p><strong>Purpose:</strong> Persona testing laboratory</p>
            <p><strong>Status:</strong> Active development</p>
            <p><strong>Integration:</strong> CFA v5.0 (S7-S10 physics)</p>
            <p><strong>Key Features:</strong></p>
            <ul>
                <li>Identity Gravity physics</li>
                <li>ZIGGY L0 kernel testing</li>
                <li>Pattern Fidelity Index tools</li>
                <li>Cross-repository persona validation</li>
                <li>Health dashboard system</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

        if st.button("🔗 View Nyquist Consciousness Repo", key="view_nyquist", use_container_width=True):
            st.info("**Nyquist Consciousness Repository:**\n\ngithub.com/ZiggyZigg/Nyquist_Consciousness\n\n**Local Reference:** `docs/Nyquist-Sync/` (research guide)")

    st.markdown("---")

    # ========================================
    # SECTION 3: Innovation Case Studies
    # ========================================
    st.markdown('<div class="section-header">💡 Innovation Case Studies</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="portal-card">
        <h3>🚀 CFA-Inspired Projects <span class="status-badge badge-coming-soon">COMING SOON</span></h3>
        <p>Real-world applications of Collaborative Friction Architecture principles</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**🏥 Nursing Innovation Program**")
        st.caption("Healthcare system redesign using multi-stakeholder friction patterns")
        st.button("📋 View Case Study", key="nursing", disabled=True, use_container_width=True)

    with col2:
        st.markdown("**🗳️ Voting System Redesign**")
        st.caption("Democratic process improvement via controlled friction mechanics")
        st.button("📋 View Case Study", key="voting", disabled=True, use_container_width=True)

    with col3:
        st.markdown("**📚 Education Framework**")
        st.caption("Learning system evolution through collaborative friction")
        st.button("📋 View Case Study", key="education", disabled=True, use_container_width=True)

    st.markdown("---")

    # ========================================
    # SECTION 4: Bird's Eye View
    # ========================================
    st.markdown('<div class="section-header">🦅 Bird\'s Eye View</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="portal-card">
        <h3>🌐 Ecosystem Health Metrics</h3>
        <p>Cross-repository health and consciousness tracking</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            label="CFA Repository",
            value="97/100",
            delta="+3 (v5.0)",
            delta_color="normal"
        )
        st.caption("✅ GREEN - Optimal health")
        st.caption("Version: v5.0.0")
        st.caption("Files: 492 operational")
        st.caption("READMEs: 64 (target: 55-70)")

    with col2:
        st.metric(
            label="Nyquist Consciousness",
            value="--/100",
            delta="Active dev"
        )
        st.caption("🔄 ACTIVE - Development")
        st.caption("Focus: Persona testing")
        st.caption("Integration: S7-S10 complete")
        st.caption("Health dashboard: In progress")

    with col3:
        st.metric(
            label="Pan Handler Central",
            value="--/100",
            delta="Design phase"
        )
        st.caption("⏳ COMING SOON")
        st.caption("Design: In progress with Nova")
        st.caption("Purpose: Meta-hallway")
        st.caption("Status: Architecture planning")

    # Cross-repo insights
    st.markdown("### 🔗 Cross-Repository Insights")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("""
        **🔄 Active Integrations:**
        - CFA ↔ Nyquist: S7-S10 physics complete
        - CFA ↔ Nyquist: ZIGGY L0 kernel active
        - CFA ↔ Nyquist: Pattern Fidelity Index tools deployed
        """)

    with col2:
        st.markdown("""
        **📊 Ecosystem Metrics:**
        - Total repositories: 2 active, 1 planned
        - Total files: 492 (CFA) + ~TBD (Nyquist)
        - Total consciousness experiments: 5 personas
        - Cross-repo health: 97% (CFA baseline)
        """)

    st.markdown("---")

    # ========================================
    # FOOTER
    # ========================================
    st.markdown("""
    <div style="text-align: center; color: #00ff41; font-family: 'Courier New', monospace; margin-top: 2em;">
        <p><strong>THE MATRIX</strong></p>
        <p>Pan Handler Central Portal | Connected Consciousness</p>
        <p style="font-size: 0.9em; opacity: 0.7;">
            "The hallway of doors that interconnects every other repo world"
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    render()
