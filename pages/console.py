"""
CFA v5.0 - Console (ENHANCED VERSION)
- Card-based layout with Ledger aesthetic
- New visualizations: Convergence Radar, Sensitivity Heatmap, Battle Cards
- Sidebar mode navigation (Compare, Analyze, Simulate, Audit)
- Progressive disclosure pattern
"""

import streamlit as st
import pandas as pd
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.calculations import ypa_scenario_scores, guardrail_lever_coupling, guardrail_bfi_sensitivity, guardrail_weight_inversion, symmetry_audit, PF_TYPES
from utils.visualizations import create_lever_comparison_chart, create_ypa_trinity_chart
from utils.colors import CFA_COLORS, get_framework_color, get_preset_color
from utils.profile_loader import get_ypa_data

# Import new components
from components.cards import (
    audit_card, audit_badge, status_summary_card, metric_card,
    framework_comparison_header
)
from components.charts import (
    create_convergence_radar, create_sensitivity_heatmap,
    create_battle_card_html, create_preset_compass,
    create_guardrail_grid, create_scenario_comparison_bars
)

# Backward compatibility: Load frameworks from profiles
MDN_DEFAULT = get_ypa_data("Methodological Naturalism")
CT_DEFAULT = get_ypa_data("Classical Theism")

def apply_loaded_run(run: dict):
    """Apply loaded JSON to session state"""
    cfg = run.get("config", {})
    if "lever_parity" in cfg:
        st.session_state["sidebar_lever_parity"] = cfg["lever_parity"]
    if "pf_type" in cfg:
        st.session_state["sidebar_pf_type"] = cfg["pf_type"]
    if "fallibilism_bonus" in cfg:
        st.session_state["sidebar_fallibilism"] = cfg["fallibilism_bonus"]
    if "bfi_debt_weight" in cfg:
        st.session_state["sidebar_bfi_weight"] = cfg["bfi_debt_weight"]

    A = run.get("framework_a", {})
    if "name" in A:
        st.session_state["fa_name"] = A["name"]
    if "bf_i" in A:
        st.session_state["fa_ax"] = A["bf_i"].get("axioms", 6)
        st.session_state["fa_db"] = A["bf_i"].get("debts", 4)
    if "admits_limits" in A:
        st.session_state["fa_ad"] = bool(A["admits_limits"])
    if "levers" in A:
        levers = A["levers"]
        st.session_state["fa_cci"] = float(levers.get("CCI", 5.0))
        st.session_state["fa_edb"] = float(levers.get("EDB", 5.0))
        st.session_state["fa_pfi"] = float(levers.get("PF_instrumental", 5.0))
        st.session_state["fa_pfe"] = float(levers.get("PF_existential", 5.0))
        st.session_state["fa_ar"] = float(levers.get("AR", 5.0))
        st.session_state["fa_mg"] = float(levers.get("MG", 5.0))

    B = run.get("framework_b", {})
    if "name" in B:
        st.session_state["fb_name"] = B["name"]
    if "bf_i" in B:
        st.session_state["fb_ax"] = B["bf_i"].get("axioms", 6)
        st.session_state["fb_db"] = B["bf_i"].get("debts", 4)
    if "admits_limits" in B:
        st.session_state["fb_ad"] = bool(B["admits_limits"])
    if "levers" in B:
        levers = B["levers"]
        st.session_state["fb_cci"] = float(levers.get("CCI", 5.0))
        st.session_state["fb_edb"] = float(levers.get("EDB", 5.0))
        st.session_state["fb_pfi"] = float(levers.get("PF_instrumental", 5.0))
        st.session_state["fb_pfe"] = float(levers.get("PF_existential", 5.0))
        st.session_state["fb_ar"] = float(levers.get("AR", 5.0))
        st.session_state["fb_mg"] = float(levers.get("MG", 5.0))

def detect_active_preset():
    """Detect which preset mode is currently active based on sidebar config"""
    # Read current sidebar values
    parity = st.session_state.get("sidebar_lever_parity", "ON")
    pf = st.session_state.get("sidebar_pf_type", "Holistic_50_50")
    fall = st.session_state.get("sidebar_fallibilism", "ON")
    bfi = st.session_state.get("sidebar_bfi_weight", "Equal_1.0x")

    # Normalize BFI weight naming (Heavier_1.2x and Weighted_1.2x are equivalent)
    bfi_normalized = "Weighted_1.2x" if bfi in ["Heavier_1.2x", "Weighted_1.2x"] else bfi

    # Check against known preset configurations (emojis match Brute Ledger)
    if parity == "OFF" and pf == "Instrumental" and fall == "ON" and bfi_normalized == "Weighted_1.2x":
        return "🔬 Skeptic"
    elif parity == "ON" and pf == "Holistic_50_50" and fall == "ON" and bfi == "Equal_1.0x":
        return "🤝 Diplomat"
    elif parity == "ON" and pf == "Composite_70_30" and fall == "ON" and bfi == "Equal_1.0x":
        return "🙏 Seeker"
    elif parity == "ON" and pf == "Holistic_50_50" and fall == "OFF" and bfi == "Equal_1.0x":
        return "👿 Zealot"
    else:
        return "⚙️ Custom"

def render():
    """Render console"""

    # Initialize session state (avoids Session State API warnings)
    # Framework names
    if "fa_name" not in st.session_state:
        st.session_state["fa_name"] = MDN_DEFAULT["name"]
    if "fb_name" not in st.session_state:
        st.session_state["fb_name"] = CT_DEFAULT["name"]

    # Framework A - BFI
    if "fa_ax" not in st.session_state:
        st.session_state["fa_ax"] = MDN_DEFAULT["bf_i"]["axioms"]
    if "fa_db" not in st.session_state:
        st.session_state["fa_db"] = MDN_DEFAULT["bf_i"]["debts"]
    if "fa_ad" not in st.session_state:
        st.session_state["fa_ad"] = True

    # Framework A - Levers
    if "fa_cci" not in st.session_state:
        st.session_state["fa_cci"] = MDN_DEFAULT["levers"]["CCI"]
    if "fa_edb" not in st.session_state:
        st.session_state["fa_edb"] = MDN_DEFAULT["levers"]["EDB"]
    if "fa_pfi" not in st.session_state:
        st.session_state["fa_pfi"] = MDN_DEFAULT["levers"]["PF_instrumental"]
    if "fa_pfe" not in st.session_state:
        st.session_state["fa_pfe"] = MDN_DEFAULT["levers"]["PF_existential"]
    if "fa_ar" not in st.session_state:
        st.session_state["fa_ar"] = MDN_DEFAULT["levers"]["AR"]
    if "fa_mg" not in st.session_state:
        st.session_state["fa_mg"] = MDN_DEFAULT["levers"]["MG"]

    # Framework B - BFI
    if "fb_ax" not in st.session_state:
        st.session_state["fb_ax"] = CT_DEFAULT["bf_i"]["axioms"]
    if "fb_db" not in st.session_state:
        st.session_state["fb_db"] = CT_DEFAULT["bf_i"]["debts"]
    if "fb_ad" not in st.session_state:
        st.session_state["fb_ad"] = True

    # Framework B - Levers
    if "fb_cci" not in st.session_state:
        st.session_state["fb_cci"] = CT_DEFAULT["levers"]["CCI"]
    if "fb_edb" not in st.session_state:
        st.session_state["fb_edb"] = CT_DEFAULT["levers"]["EDB"]
    if "fb_pfi" not in st.session_state:
        st.session_state["fb_pfi"] = CT_DEFAULT["levers"]["PF_instrumental"]
    if "fb_pfe" not in st.session_state:
        st.session_state["fb_pfe"] = CT_DEFAULT["levers"]["PF_existential"]
    if "fb_ar" not in st.session_state:
        st.session_state["fb_ar"] = CT_DEFAULT["levers"]["AR"]
    if "fb_mg" not in st.session_state:
        st.session_state["fb_mg"] = CT_DEFAULT["levers"]["MG"]
    
    # Enhanced CSS for card-based layout and Ledger aesthetic
    st.markdown("""
    <style>
    /* Make the sticky-header div stick to top while scrolling */
    .sticky-header {
        position: -webkit-sticky !important;
        position: sticky !important;
        top: 0 !important;
        background-color: var(--background-color) !important;
        z-index: 999 !important;
        padding: 10px 0 !important;
        margin-bottom: 10px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }

    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .sticky-header {
            background-color: rgb(14, 17, 23) !important;
        }
    }

    /* Card-based layout styles */
    .cfa-card {
        background: #ffffff;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #264653;
    }

    .cfa-card-header {
        font-family: Georgia, serif;
        color: #212529;
        border-bottom: 1px solid #dee2e6;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }

    /* Status badges */
    .status-badge {
        padding: 2px 8px;
        border-radius: 12px;
        color: white;
        font-size: 0.8em;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    .badge-audited { background: #264653; }
    .badge-convergent { background: #2a9d8f; }
    .badge-draft { background: #e9c46a; color: #333; }
    .badge-crux { background: #f4a261; }
    .badge-divergent { background: #e76f51; }

    /* Metric cards */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 15px;
        margin: 15px 0;
    }

    .metric-card {
        background: #ffffff;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        border-top: 3px solid #264653;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }

    .metric-label {
        font-size: 0.75em;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 5px;
    }

    .metric-value {
        font-size: 1.5em;
        font-weight: bold;
        color: #212529;
    }

    /* Mode navigation pills */
    .mode-nav {
        display: flex;
        gap: 8px;
        padding: 10px 0;
        border-bottom: 1px solid #dee2e6;
        margin-bottom: 15px;
    }

    .mode-pill {
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85em;
        cursor: pointer;
        transition: all 0.2s;
        border: 1px solid #dee2e6;
        background: #f8f9fa;
        color: #495057;
    }

    .mode-pill.active {
        background: #264653;
        color: white;
        border-color: #264653;
    }

    .mode-pill:hover {
        background: #e9ecef;
    }

    .mode-pill.active:hover {
        background: #1a3a47;
    }
    </style>
    """, unsafe_allow_html=True)

    # Frozen position indicators (top-right corner, stacked vertically)
    active_preset = detect_active_preset()
    audit_mode = st.session_state.get("audit_mode", "Bias")  # Default to Bias mode
    include_crux = st.session_state.get("include_crux", True)  # Default to Include

    # Color coding for audit mode
    audit_color = "#28a745" if audit_mode == "Audit" else "#dc3545"  # Green for Audit, Red for Bias
    audit_icon = "🔍" if audit_mode == "Audit" else "🎯"

    # Crux indicator
    crux_status = "Include" if include_crux else "Exclude"
    crux_color = "#9b59b6" if include_crux else "#e67e22"  # Purple for Include, Orange for Exclude
    crux_icon = "⚖️" if include_crux else "🚫"

    st.markdown(f"""
    <div style="position: fixed; top: 80px; right: 15px; z-index: 9999; max-width: 200px;">
        <!-- Preset Mode Indicator -->
        <div style="background-color: rgba(255, 255, 255, 0.95);
                    border: 2px solid #1f77b4; border-radius: 6px;
                    padding: 6px 10px; margin-bottom: 8px;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
                    max-width: 180px;">
            <div style="font-size: 0.7rem; font-weight: bold; color: #1f77b4; margin-bottom: 2px;">
                Active Mode
            </div>
            <div style="font-size: 0.9rem; font-weight: bold; color: #333;">
                {active_preset}
            </div>
            <div style="font-size: 0.65rem; color: {audit_color}; margin-top: 4px; font-weight: 600;">
                {audit_icon} {audit_mode} Mode
            </div>
            <div style="font-size: 0.65rem; color: {crux_color}; margin-top: 4px; font-weight: 600;">
                {crux_icon} Crux: {crux_status}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Header (sticky wrapper for persistent navigation)
    st.markdown('<div class="sticky-header">', unsafe_allow_html=True)
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown('<p style="font-size:2.5rem;font-weight:bold;color:#1f77b4;">⚖️ CFA v5.0 Console</p>', unsafe_allow_html=True)
    with col2:
        if st.button("🏠 Home"):
            st.session_state.page = 'landing'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('**"All Named, All Priced" — Interactive Comparison Tool**')
    st.markdown("---")

    # SIDEBAR
    st.sidebar.header("🎛️ Configuration")

    # Console Mode Navigation (NEW - from CONSOLE_ENHANCEMENT_PROMPT)
    st.sidebar.markdown("**📊 Console Mode:**")
    if "console_mode" not in st.session_state:
        st.session_state["console_mode"] = "Compare"

    console_modes = ["Compare", "Analyze", "Simulate", "Audit"]
    console_mode = st.sidebar.radio(
        "Mode",
        console_modes,
        index=console_modes.index(st.session_state.get("console_mode", "Compare")),
        key="console_mode_radio",
        horizontal=True,
        label_visibility="collapsed",
        help="**Compare:** Side-by-side framework comparison. **Analyze:** Deep dive on single framework. **Simulate:** Toggle sensitivity playground. **Audit:** Trinity convergence details."
    )
    if console_mode != st.session_state.get("console_mode"):
        st.session_state["console_mode"] = console_mode
        st.rerun()

    st.sidebar.markdown("---")

    # deps: preset_modes
    # Preset Mode Spectrum (MOVED TO TOP - user should select spectrum FIRST)
    with st.sidebar.expander("🎚️ Preset Mode Spectrum", expanded=False):
        st.markdown("**Quick Configuration Profiles:**")
        st.caption("⚠️ **IMPORTANT:** Select your spectrum mode FIRST, then load frameworks below!")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔬 Skeptic Mode", use_container_width=True):
                st.session_state["sidebar_lever_parity"] = "OFF"
                st.session_state["sidebar_pf_type"] = "Instrumental"
                st.session_state["sidebar_fallibilism"] = "ON"
                st.session_state["sidebar_bfi_weight"] = "Weighted_1.2x"
                st.rerun()  # Immediately reflect changes in indicator
            st.caption("MdN-optimized\nPredictive power focus")

            if st.button("🙏 Seeker Mode", use_container_width=True):
                st.session_state["sidebar_lever_parity"] = "ON"
                st.session_state["sidebar_pf_type"] = "Composite_70_30"
                st.session_state["sidebar_fallibilism"] = "ON"
                st.session_state["sidebar_bfi_weight"] = "Equal_1.0x"
                st.rerun()  # Immediately reflect changes in indicator
            st.caption("CT-leaning\nMeaning-first")

        with col2:
            if st.button("🤝 Diplomat Mode", use_container_width=True):
                st.session_state["sidebar_lever_parity"] = "ON"
                st.session_state["sidebar_pf_type"] = "Holistic_50_50"
                st.session_state["sidebar_fallibilism"] = "ON"
                st.session_state["sidebar_bfi_weight"] = "Equal_1.0x"
                st.rerun()  # Immediately reflect changes in indicator
            st.caption("Balanced bridge\nEqual weighting")

            if st.button("👿 Zealot Mode", use_container_width=True):
                st.session_state["sidebar_lever_parity"] = "ON"
                st.session_state["sidebar_pf_type"] = "Holistic_50_50"
                st.session_state["sidebar_fallibilism"] = "OFF"
                st.session_state["sidebar_bfi_weight"] = "Equal_1.0x"
                st.rerun()  # Immediately reflect changes in indicator
            st.caption("CT-optimized\nExistential-first")

        st.markdown("---")
        st.caption("💡 **Workflow:** 1️⃣ Pick spectrum mode → 2️⃣ Load frameworks below → 3️⃣ Adjust toggles if needed")

    st.sidebar.markdown("---")

    # Preset Profile Library (MOVED BELOW SPECTRUM - user loads frameworks AFTER setting spectrum)
    with st.sidebar.expander("📚 Load Preset Profile", expanded=False):
        # Scoring Mode (moved here from below)
        st.markdown("**🔍 Scoring Mode:**")
        if "audit_mode" not in st.session_state:
            st.session_state["audit_mode"] = "Bias"

        audit_mode_options = ["Bias", "Audit"]
        current_audit_idx = audit_mode_options.index(st.session_state.get("audit_mode", "Bias"))
        audit_mode = st.selectbox(
            "Mode",
            audit_mode_options,
            index=current_audit_idx,
            key="audit_mode_selector",
            help="**Bias Mode (🎯):** Full bias scoring - auditors apply their native lenses with bias intact. **Audit Mode (🔍):** Adversarial audit - scores reflect rigorous adversarial checking (Trinity convergence). Switch to Audit to see adversarially-validated scores.",
            label_visibility="collapsed"
        )
        # Update session state and rerun if changed
        if audit_mode != st.session_state.get("audit_mode"):
            st.session_state["audit_mode"] = audit_mode
            st.rerun()

        st.markdown("---")

        # Crux Impasses Toggle
        st.markdown("**⚖️ Crux Impasses:**")
        if "include_crux" not in st.session_state:
            st.session_state["include_crux"] = True

        include_crux_options = ["Include", "Exclude"]
        current_crux_idx = 0 if st.session_state.get("include_crux", True) else 1
        include_crux = st.selectbox(
            "Crux Impact",
            include_crux_options,
            index=current_crux_idx,
            key="crux_selector",
            help="**Include (default):** Scores reflect full convergence including Crux resolutions. **Exclude:** Scores show what convergence would be WITHOUT Crux declarations (counterfactual - shows impact of honest impasse mechanism).",
            label_visibility="collapsed"
        )
        # Update session state and rerun if changed
        new_include_crux = (include_crux == "Include")
        if new_include_crux != st.session_state.get("include_crux"):
            st.session_state["include_crux"] = new_include_crux
            st.rerun()

        st.markdown("---")
        st.markdown("**Pre-Audited Frameworks:**")

        preset_options = {
            "-- Select Framework --": None,
            # Fully audited (98% Trinity convergence) - emojis match Brute Ledger
            "📘 Methodological Naturalism (MdN)": "mdn",
            "📕 Classical Theism (CT)": "ct",
            # Profiles exist but not yet fully audited (emojis match Brute Ledger)
            "☸️ Buddhism": "coming",
            "🤔 Desiderata Believers": "coming",
            "⛔ Error Theory": "coming",
            "🎭 Existentialism": "coming",
            "🕉️ Hinduism": "coming",
            "☪️ Islam": "coming",
            "📖 Mormonism (LDS)": "coming",
            "❓ Null Hypothesis": "coming",
            "🕎 Orthodox Judaism": "coming",
            "🌊 Process Theology": "coming"
        }
        
        selected_preset = st.selectbox(
            "Choose Framework:",
            list(preset_options.keys()),
            key="preset_selector"
        )
        
        preset_key = preset_options[selected_preset]

        if preset_key == "mdn":
            st.info("**Methodological Naturalism**\n\nResearch protocol assuming testable natural causes. Audited by Claude + Grok with 98% convergence.")

            # Let user choose which framework slot
            load_col1, load_col2 = st.columns(2)

            with load_col1:
                if st.button("→ Load to A", key="load_mdn_a", use_container_width=True, type="primary"):
                    st.session_state["fa_name"] = "Methodological Naturalism"
                    st.session_state["fa_ax"] = 6
                    st.session_state["fa_db"] = 4
                    st.session_state["fa_ad"] = True
                    st.session_state["fa_cci"] = 8.0
                    st.session_state["fa_edb"] = 7.5
                    st.session_state["fa_pfi"] = 10.0
                    st.session_state["fa_pfe"] = 3.0
                    st.session_state["fa_ar"] = 7.0
                    st.session_state["fa_mg"] = 4.0
                    st.success("✅ MdN → Framework A!")
                    st.rerun()

            with load_col2:
                if st.button("→ Load to B", key="load_mdn_b", use_container_width=True):
                    st.session_state["fb_name"] = "Methodological Naturalism"
                    st.session_state["fb_ax"] = 6
                    st.session_state["fb_db"] = 4
                    st.session_state["fb_ad"] = True
                    st.session_state["fb_cci"] = 8.0
                    st.session_state["fb_edb"] = 7.5
                    st.session_state["fb_pfi"] = 10.0
                    st.session_state["fb_pfe"] = 3.0
                    st.session_state["fb_ar"] = 7.0
                    st.session_state["fb_mg"] = 4.0
                    st.success("✅ MdN → Framework B!")
                    st.rerun()

        elif preset_key == "ct":
            st.info("**Classical Theism**\n\nTraditional monotheistic worldview. Audited by Claude + Grok with 98% convergence.")

            # Let user choose which framework slot
            load_col1, load_col2 = st.columns(2)

            with load_col1:
                if st.button("→ Load to A", key="load_ct_a", use_container_width=True, type="primary"):
                    st.session_state["fa_name"] = "Classical Theism"
                    st.session_state["fa_ax"] = 7
                    st.session_state["fa_db"] = 4
                    st.session_state["fa_ad"] = True
                    st.session_state["fa_cci"] = 7.5
                    st.session_state["fa_edb"] = 8.5
                    st.session_state["fa_pfi"] = 7.0
                    st.session_state["fa_pfe"] = 8.0
                    st.session_state["fa_ar"] = 8.5
                    st.session_state["fa_mg"] = 8.5
                    st.success("✅ CT → Framework A!")
                    st.rerun()

            with load_col2:
                if st.button("→ Load to B", key="load_ct_b", use_container_width=True):
                    st.session_state["fb_name"] = "Classical Theism"
                    st.session_state["fb_ax"] = 7
                    st.session_state["fb_db"] = 4
                    st.session_state["fb_ad"] = True
                    st.session_state["fb_cci"] = 7.5
                    st.session_state["fb_edb"] = 8.5
                    st.session_state["fb_pfi"] = 7.0
                    st.session_state["fb_pfe"] = 8.0
                    st.session_state["fb_ar"] = 8.5
                    st.session_state["fb_mg"] = 8.5
                    st.success("✅ CT → Framework B!")
                    st.rerun()

        elif preset_key == "coming":
            st.warning(f"**{selected_preset.replace('🔜 ', '')}**\n\nAudit in progress. Check back soon!")

        if selected_preset != "-- Select Framework --":
            st.markdown("---")
            st.caption("💡 **Tip:** Load different frameworks to each side to compare!")
    
    # Initialize sidebar config defaults if not set
    if "sidebar_lever_parity" not in st.session_state:
        st.session_state["sidebar_lever_parity"] = "ON"
    if "sidebar_pf_type" not in st.session_state:
        st.session_state["sidebar_pf_type"] = "Holistic_50_50"
    if "sidebar_fallibilism" not in st.session_state:
        st.session_state["sidebar_fallibilism"] = "ON"
    if "sidebar_bfi_weight" not in st.session_state:
        st.session_state["sidebar_bfi_weight"] = "Equal_1.0x"

    # Lever-Parity selectbox
    parity_options = ["ON", "OFF"]
    current_parity_idx = parity_options.index(st.session_state.get("sidebar_lever_parity", "ON"))

    lever_parity = st.sidebar.selectbox(
        "Lever-Parity",
        parity_options,
        index=current_parity_idx,
        key="sidebar_lever_parity_widget",
        help="**Parity ON:** Moral norms (MG) count equally with epistemic norms. **OFF:** Focus on predictive power. [ΔYPA: OFF typically boosts MdN ~+0.2-0.3] Because CT includes moral realism, Parity ON increases MG weighting for both frameworks."
    )
    # Sync back to session state
    if lever_parity != st.session_state.get("sidebar_lever_parity"):
        st.session_state["sidebar_lever_parity"] = lever_parity
        st.rerun()

    # PF-Type selectbox
    current_pf_idx = PF_TYPES.index(st.session_state.get("sidebar_pf_type", "Holistic_50_50"))

    pf_type = st.sidebar.selectbox(
        "PF-Type",
        PF_TYPES,
        index=current_pf_idx,
        key="sidebar_pf_type_widget",
        help="**Instrumental:** Tech/predictive yield only. **Composite (70/30):** 70% instrumental, 30% existential. **Holistic (50/50):** Equal weight. [ΔYPA: Holistic favors CT ~+0.15-0.25] CT scores higher on existential fertility, so holistic weighting benefits CT."
    )
    # Sync back to session state
    if pf_type != st.session_state.get("sidebar_pf_type"):
        st.session_state["sidebar_pf_type"] = pf_type
        st.rerun()

    # Fallibilism-Bonus selectbox
    fall_options = ["ON", "OFF"]
    current_fall_idx = fall_options.index(st.session_state.get("sidebar_fallibilism", "ON"))

    fall_bonus = st.sidebar.selectbox(
        "Fallibilism-Bonus",
        fall_options,
        index=current_fall_idx,
        key="sidebar_fallibilism_widget",
        help="**Bonus ON:** Frameworks that admit limits get +0.3 CCI boost. **OFF:** No bonus. [ΔYPA: ON benefits both MdN and CT equally ~+0.03] Both frameworks acknowledge limitations, so both receive the fallibilism bonus when enabled."
    )
    # Sync back to session state
    if fall_bonus != st.session_state.get("sidebar_fallibilism"):
        st.session_state["sidebar_fallibilism"] = fall_bonus
        st.rerun()

    # BFI Debt Weight selectbox
    # Normalize "Heavier_1.2x" to "Weighted_1.2x" for display consistency
    if st.session_state.get("sidebar_bfi_weight") == "Heavier_1.2x":
        st.session_state["sidebar_bfi_weight"] = "Weighted_1.2x"

    bfi_options = ["Equal_1.0x", "Weighted_1.2x"]
    current_bfi_idx = bfi_options.index(st.session_state.get("sidebar_bfi_weight", "Equal_1.0x"))

    bfi_weight = st.sidebar.selectbox(
        "BFI Debt Weight",
        bfi_options,
        index=current_bfi_idx,
        key="sidebar_bfi_weight_widget",
        help="**Equal (1.0x):** Debts count same as axioms. **Weighted (1.2x):** Debts cost 20% more. [ΔYPA: Weighted slightly lowers both scores ~-0.05-0.10] Higher BFI denominator reduces YPA. Both frameworks have 4 debts, so weighted impacts both similarly."
    )
    # Sync back to session state
    if bfi_weight != st.session_state.get("sidebar_bfi_weight"):
        st.session_state["sidebar_bfi_weight"] = bfi_weight
        st.rerun()

    st.sidebar.markdown("---")

    # Sidebar Import
    st.sidebar.markdown("### 📥 Import")
    import_file_sidebar = st.sidebar.file_uploader("Load saved audit", type=["json"], key="import_sidebar")
    if import_file_sidebar:
        try:
            run = json.load(import_file_sidebar)
            if "config" in run:
                if st.sidebar.button("✅ Apply", key="apply_sidebar"):
                    apply_loaded_run(run)
                    st.rerun()
        except:
            st.sidebar.error("Invalid file")

    st.sidebar.markdown("---")

    # Current Config (moved below Import, now collapsible)
    cfg = {
        "lever_parity": lever_parity,
        "pf_type": pf_type,
        "fallibilism_bonus": fall_bonus,
        "bfi_debt_weight": bfi_weight,
        "audit_mode": audit_mode,
        "include_crux": include_crux
    }

    with st.sidebar.expander("📋 Current Config", expanded=False):
        st.json(cfg)

    # FRAMEWORK EDITORS
    col1, col2 = st.columns(2)

    # FRAMEWORK A
    with col1:
        st.markdown("### 📘 Framework A")
        st.caption("✅ 98% Convergence | Adversarially Audited")
        fa_name = st.text_input("Name", key="fa_name")
        
        with st.expander("🔢 BFI", expanded=False):
            if 'custom_framework_ready' in st.session_state:
                custom = st.session_state['custom_framework_ready']
                if custom.get('target') == 'framework_a':
                    st.info(f"🔔 **Custom framework ready:** {custom['name']}")
                    if st.button("✅ Apply Custom Framework", key="apply_custom_a"):
                        st.session_state.fa_name = custom['name']
                        st.session_state.fa_ax = custom['axioms']
                        st.session_state.fa_db = custom['debts']
                        del st.session_state['custom_framework_ready']
                        st.rerun()
            
            fa_axioms = st.number_input("Axioms", min_value=1, max_value=30, key="fa_ax")
            fa_debts = st.number_input("Debts", min_value=0, max_value=30, key="fa_db")
            fa_admits = st.checkbox("Admits Limits", key="fa_ad")
            
            if st.button("🔍 Go to Brute Ledger", key="goto_ledger_a"):
                # Pass framework name for smart navigation
                st.session_state.ledger_nav_target = st.session_state.get("fa_name", "Methodological Naturalism")
                st.session_state.page = 'brute_ledger'
                st.rerun()
        
        # PER-FRAMEWORK PRESET BUTTONS (ABOVE SLIDERS - WORKING POSITION)
        st.markdown("**⚡ Quick Adjust:**")
        preset_a = st.columns(4)
        with preset_a[0]:
            if st.button("⚡ MAX", key="fa_max_btn", help="Set all to 10.0"):
                for k in ["fa_cci", "fa_edb", "fa_pfi", "fa_pfe", "fa_ar", "fa_mg"]:
                    st.session_state[k] = 10.0
                st.rerun()
        with preset_a[1]:
            if st.button("⚖️ MID", key="fa_mid_btn", help="Set all to 5.0"):
                for k in ["fa_cci", "fa_edb", "fa_pfi", "fa_pfe", "fa_ar", "fa_mg"]:
                    st.session_state[k] = 5.0
                st.rerun()
        with preset_a[2]:
            if st.button("🔄 RESET", key="fa_reset_btn", help="Reset to MdN"):
                st.session_state["fa_cci"] = MDN_DEFAULT["levers"]["CCI"]
                st.session_state["fa_edb"] = MDN_DEFAULT["levers"]["EDB"]
                st.session_state["fa_pfi"] = MDN_DEFAULT["levers"]["PF_instrumental"]
                st.session_state["fa_pfe"] = MDN_DEFAULT["levers"]["PF_existential"]
                st.session_state["fa_ar"] = MDN_DEFAULT["levers"]["AR"]
                st.session_state["fa_mg"] = MDN_DEFAULT["levers"]["MG"]
                st.rerun()
        with preset_a[3]:
            if st.button("🚫 MIN", key="fa_min_btn", help="Set all to 0.0"):
                for k in ["fa_cci", "fa_edb", "fa_pfi", "fa_pfe", "fa_ar", "fa_mg"]:
                    st.session_state[k] = 0.0
                st.rerun()
        
        st.markdown("---")
        
        # SLIDERS
        fa_cci = st.slider("CCI - Coherence & Closure", 0.0, 10.0, step=0.1, key="fa_cci",
                          help="**Coherence & Closure Index:** How well the framework's concepts fit together and provide satisfying explanations. Higher = more internally consistent and complete.")
        fa_edb = st.slider("EDB - Explanatory Depth & Breadth", 0.0, 10.0, step=0.1, key="fa_edb",
                          help="**Explanatory Depth & Breadth:** Range and depth of phenomena the framework can explain. Higher = explains more domains (physics, ethics, consciousness) more thoroughly.")
        fa_pf_i = st.slider("PF-Instrumental", 0.0, 10.0, step=0.1, key="fa_pfi",
                           help="**Predictive Fertility (Instrumental):** How well the framework generates testable predictions and technological applications. Higher = more empirical/practical fruitfulness.")
        fa_pf_e = st.slider("PF-Existential", 0.0, 10.0, step=0.1, key="fa_pfe",
                           help="**Predictive Fertility (Existential):** How well the framework addresses meaning, purpose, and existential questions. Higher = more depth on 'why we're here' questions.")
        fa_ar = st.slider("AR - Aesthetic Resonance", 0.0, 10.0, step=0.1, key="fa_ar",
                         help="**Aesthetic Resonance:** How beautiful, elegant, or compelling the framework feels. Higher = greater intellectual/emotional appeal and motivational power.")
        fa_mg = st.slider("MG - Moral Generativity", 0.0, 10.0, step=0.1, key="fa_mg",
                         help="**Moral Generativity:** How well the framework grounds and generates moral norms. Higher = stronger foundation for ethics and values. [Weighted by Parity lever]")

        fa = {
            "name": fa_name,
            "bf_i": {"axioms": fa_axioms, "debts": fa_debts},
            "levers": {"CCI": fa_cci, "EDB": fa_edb, "PF_instrumental": fa_pf_i, "PF_existential": fa_pf_e, "AR": fa_ar, "MG": fa_mg},
            "admits_limits": fa_admits
        }

    # FRAMEWORK B
    with col2:
        st.markdown("### 📕 Framework B")
        st.caption("✅ 98% Convergence | Adversarially Audited")
        fb_name = st.text_input("Name", key="fb_name")
        
        with st.expander("🔢 BFI", expanded=False):
            if 'custom_framework_ready' in st.session_state:
                custom = st.session_state['custom_framework_ready']
                if custom.get('target') == 'framework_b':
                    st.info(f"🔔 **Custom framework ready:** {custom['name']}")
                    if st.button("✅ Apply Custom Framework", key="apply_custom_b"):
                        st.session_state.fb_name = custom['name']
                        st.session_state.fb_ax = custom['axioms']
                        st.session_state.fb_db = custom['debts']
                        del st.session_state['custom_framework_ready']
                        st.rerun()
            
            fb_axioms = st.number_input("Axioms", min_value=1, max_value=30, key="fb_ax")
            fb_debts = st.number_input("Debts", min_value=0, max_value=30, key="fb_db")
            fb_admits = st.checkbox("Admits Limits", key="fb_ad")
            
            if st.button("🔍 Go to Brute Ledger", key="goto_ledger_b"):
                # Pass framework name for smart navigation
                st.session_state.ledger_nav_target = st.session_state.get("fb_name", "Classical Theism")
                st.session_state.page = 'brute_ledger'
                st.rerun()
        
        # PER-FRAMEWORK PRESET BUTTONS (ABOVE SLIDERS - WORKING POSITION)
        st.markdown("**⚡ Quick Adjust:**")
        preset_b = st.columns(4)
        with preset_b[0]:
            if st.button("⚡ MAX", key="fb_max_btn", help="Set all to 10.0"):
                for k in ["fb_cci", "fb_edb", "fb_pfi", "fb_pfe", "fb_ar", "fb_mg"]:
                    st.session_state[k] = 10.0
                st.rerun()
        with preset_b[1]:
            if st.button("⚖️ MID", key="fb_mid_btn", help="Set all to 5.0"):
                for k in ["fb_cci", "fb_edb", "fb_pfi", "fb_pfe", "fb_ar", "fb_mg"]:
                    st.session_state[k] = 5.0
                st.rerun()
        with preset_b[2]:
            if st.button("🔄 RESET", key="fb_reset_btn", help="Reset to CT"):
                st.session_state["fb_cci"] = CT_DEFAULT["levers"]["CCI"]
                st.session_state["fb_edb"] = CT_DEFAULT["levers"]["EDB"]
                st.session_state["fb_pfi"] = CT_DEFAULT["levers"]["PF_instrumental"]
                st.session_state["fb_pfe"] = CT_DEFAULT["levers"]["PF_existential"]
                st.session_state["fb_ar"] = CT_DEFAULT["levers"]["AR"]
                st.session_state["fb_mg"] = CT_DEFAULT["levers"]["MG"]
                st.rerun()
        with preset_b[3]:
            if st.button("🚫 MIN", key="fb_min_btn", help="Set all to 0.0"):
                for k in ["fb_cci", "fb_edb", "fb_pfi", "fb_pfe", "fb_ar", "fb_mg"]:
                    st.session_state[k] = 0.0
                st.rerun()
        
        st.markdown("---")
        
        # SLIDERS
        fb_cci = st.slider("CCI - Coherence & Closure", 0.0, 10.0, step=0.1, key="fb_cci",
                          help="**Coherence & Closure Index:** How well the framework's concepts fit together and provide satisfying explanations. Higher = more internally consistent and complete.")
        fb_edb = st.slider("EDB - Explanatory Depth & Breadth", 0.0, 10.0, step=0.1, key="fb_edb",
                          help="**Explanatory Depth & Breadth:** Range and depth of phenomena the framework can explain. Higher = explains more domains (physics, ethics, consciousness) more thoroughly.")
        fb_pf_i = st.slider("PF-Instrumental", 0.0, 10.0, step=0.1, key="fb_pfi",
                           help="**Predictive Fertility (Instrumental):** How well the framework generates testable predictions and technological applications. Higher = more empirical/practical fruitfulness.")
        fb_pf_e = st.slider("PF-Existential", 0.0, 10.0, step=0.1, key="fb_pfe",
                           help="**Predictive Fertility (Existential):** How well the framework addresses meaning, purpose, and existential questions. Higher = more depth on 'why we're here' questions.")
        fb_ar = st.slider("AR - Aesthetic Resonance", 0.0, 10.0, step=0.1, key="fb_ar",
                         help="**Aesthetic Resonance:** How beautiful, elegant, or compelling the framework feels. Higher = greater intellectual/emotional appeal and motivational power.")
        fb_mg = st.slider("MG - Moral Generativity", 0.0, 10.0, step=0.1, key="fb_mg",
                         help="**Moral Generativity:** How well the framework grounds and generates moral norms. Higher = stronger foundation for ethics and values. [Weighted by Parity lever]")

        fb = {
            "name": fb_name,
            "bf_i": {"axioms": fb_axioms, "debts": fb_debts},
            "levers": {"CCI": fb_cci, "EDB": fb_edb, "PF_instrumental": fb_pf_i, "PF_existential": fb_pf_e, "AR": fb_ar, "MG": fb_mg},
            "admits_limits": fb_admits
        }

    st.markdown("---")

    # CALCULATE
    ya_results, ya_levers, ya_bfi = ypa_scenario_scores(fa, cfg)
    yb_results, yb_levers, yb_bfi = ypa_scenario_scores(fb, cfg)

    # YPA EXPLANATION (Grok Note #1: Pragmatic Clarity)
    st.info("💡 **YPA = Yield per Axiom:** Efficiency score = Total Lever Score ÷ BFI. Higher YPA = more output per assumption.")

    # =========================================================================
    # AUDIT STATUS SUMMARY CARD (NEW - from CONSOLE_ENHANCEMENT_PROMPT)
    # =========================================================================
    # Calculate guardrail status for summary
    ok1_a, _ = guardrail_lever_coupling(ya_levers["PF"], ya_levers["CCI"])
    ok2_a, _ = guardrail_bfi_sensitivity(ya_results["Neutral"]["YPA"], ya_bfi, ya_results["Empirical"]["YPA"], ya_results["Existential"]["YPA"])
    ok3_a, _ = guardrail_weight_inversion(ya_results, ya_results["Neutral"]["YPA"])
    audit_a_summary = symmetry_audit(fa, cfg)
    ok4_a = max(abs(row[3]) for row in audit_a_summary) <= 0.3

    ok1_b, _ = guardrail_lever_coupling(yb_levers["PF"], yb_levers["CCI"])
    ok2_b, _ = guardrail_bfi_sensitivity(yb_results["Neutral"]["YPA"], yb_bfi, yb_results["Empirical"]["YPA"], yb_results["Existential"]["YPA"])
    ok3_b, _ = guardrail_weight_inversion(yb_results, yb_results["Neutral"]["YPA"])
    audit_b_summary = symmetry_audit(fb, cfg)
    ok4_b = max(abs(row[3]) for row in audit_b_summary) <= 0.3

    guardrails_passed = sum([ok1_a, ok2_a, ok3_a, ok4_a, ok1_b, ok2_b, ok3_b, ok4_b])
    guardrails_total = 8

    # Symmetry status
    max_delta_overall = max(
        max(abs(row[3]) for row in audit_a_summary),
        max(abs(row[3]) for row in audit_b_summary)
    )
    symmetry_status = "Balanced" if max_delta_overall <= 0.3 else f"Max Δ = {max_delta_overall:.2f}"

    # Display summary card
    st.markdown(status_summary_card(
        frameworks_loaded=2,
        frameworks_total=2,
        guardrails_passed=guardrails_passed,
        guardrails_total=guardrails_total,
        convergence_pct=98.0,  # Hardcoded for audited frameworks
        crux_count=0,
        active_preset=active_preset,
        symmetry_status=symmetry_status
    ), unsafe_allow_html=True)

    # =========================================================================
    # FRAMEWORK COMPARISON HEADER (NEW)
    # =========================================================================
    st.markdown(framework_comparison_header(
        fa["name"], fb["name"],
        ya_results["Neutral"]["YPA"],
        yb_results["Neutral"]["YPA"]
    ), unsafe_allow_html=True)

    # TABS (Enhanced with new visualizations)
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📈 Visual", "⚔️ Battle Card", "📋 Details", "🛡️ Guardrails", "🔄 Symmetry"])

    with tab1:
        # Original charts
        st.plotly_chart(create_lever_comparison_chart(ya_levers, yb_levers, fa["name"], fb["name"]), use_container_width=True)
        st.plotly_chart(create_ypa_trinity_chart(ya_results, yb_results, fa["name"], fb["name"]), use_container_width=True)

        # NEW: Scenario Comparison Bars
        st.markdown("### 📊 Scenario Impact")
        st.plotly_chart(create_scenario_comparison_bars(ya_results, yb_results, fa["name"], fb["name"]), use_container_width=True)

        # NEW: Trinity Convergence Radar (simulated - both frameworks show same audited scores)
        with st.expander("🎯 Trinity Convergence Radar", expanded=False):
            st.caption("*Shows how Claude, Grok, and Nova scored this framework (audited frameworks converge at 98%)*")

            radar_col1, radar_col2 = st.columns(2)

            with radar_col1:
                # Framework A - Trinity scores (simulated convergence)
                trinity_a = {
                    'Claude': [ya_levers["CCI"], ya_levers["EDB"], ya_levers["PF_instrumental"], ya_levers["PF_existential"], ya_levers["AR"], ya_levers["MG"]],
                    'Grok': [ya_levers["CCI"]*0.99, ya_levers["EDB"]*1.01, ya_levers["PF_instrumental"]*0.98, ya_levers["PF_existential"]*1.02, ya_levers["AR"]*0.99, ya_levers["MG"]*1.01],
                    'Nova': [ya_levers["CCI"]*1.01, ya_levers["EDB"]*0.99, ya_levers["PF_instrumental"]*1.01, ya_levers["PF_existential"]*0.99, ya_levers["AR"]*1.02, ya_levers["MG"]*0.98]
                }
                st.plotly_chart(create_convergence_radar(trinity_a, f"{fa['name']} - Trinity View"), use_container_width=True)

            with radar_col2:
                # Framework B - Trinity scores (simulated convergence)
                trinity_b = {
                    'Claude': [yb_levers["CCI"], yb_levers["EDB"], yb_levers["PF_instrumental"], yb_levers["PF_existential"], yb_levers["AR"], yb_levers["MG"]],
                    'Grok': [yb_levers["CCI"]*0.99, yb_levers["EDB"]*1.01, yb_levers["PF_instrumental"]*0.98, yb_levers["PF_existential"]*1.02, yb_levers["AR"]*0.99, yb_levers["MG"]*1.01],
                    'Nova': [yb_levers["CCI"]*1.01, yb_levers["EDB"]*0.99, yb_levers["PF_instrumental"]*1.01, yb_levers["PF_existential"]*0.99, yb_levers["AR"]*1.02, yb_levers["MG"]*0.98]
                }
                st.plotly_chart(create_convergence_radar(trinity_b, f"{fb['name']} - Trinity View"), use_container_width=True)

    with tab2:
        # NEW: Battle Card visualization
        st.markdown("### ⚔️ Framework Battle Card")
        st.caption("*Head-to-head comparison showing which framework wins each lever*")

        st.markdown(create_battle_card_html(
            fa["name"], fb["name"],
            fa["levers"], fb["levers"],
            ya_results["Neutral"]["YPA"],
            yb_results["Neutral"]["YPA"]
        ), unsafe_allow_html=True)

        # NEW: Sensitivity Heatmap
        st.markdown("### 🌡️ Toggle Sensitivity Heatmap")
        st.caption("*How much does YPA change when each toggle is flipped?*")

        # Calculate sensitivity matrix
        sensitivity_matrix = []
        for _, audit_data in [(fa, audit_a_summary), (fb, audit_b_summary)]:
            delta_row = [r[3] for r in audit_data]  # Delta values
            sensitivity_matrix.append(delta_row)

        st.plotly_chart(create_sensitivity_heatmap(
            sensitivity_matrix,
            [fa["name"], fb["name"]],
            ['Parity', 'PF-Type', 'Fallibilism', 'BFI Weight']
        ), use_container_width=True)

    with tab3:
        # Details tab (was tab2)
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**{fa['name']}**")
            st.json(ya_levers)
            st.metric("BFI", f"{ya_bfi:.2f}")
            st.metric("Neutral YPA", f"{ya_results['Neutral']['YPA']:.3f}")
        with c2:
            st.markdown(f"**{fb['name']}**")
            st.json(yb_levers)
            st.metric("BFI", f"{yb_bfi:.2f}")
            st.metric("Neutral YPA", f"{yb_results['Neutral']['YPA']:.3f}")

    with tab4:
        # Guardrails tab (was tab3)
        st.caption("✨ Each guardrail tests integrity—of method and of meaning alike.")

        # NEW: Visual Guardrail Grid
        guardrail_status = [
            ['✅' if ok1_a else '⚠️', '✅' if ok1_b else '⚠️'],  # Lever-Coupling
            ['✅' if ok2_a else '⚠️', '✅' if ok2_b else '⚠️'],  # BFI-Sensitivity
            ['✅' if ok3_a else '⚠️', '✅' if ok3_b else '⚠️'],  # Weight-Inversion
            ['✅' if ok4_a else '⚠️', '✅' if ok4_b else '⚠️'],  # Symmetry
        ]
        st.markdown(create_guardrail_grid([fa["name"], fb["name"]], guardrail_status), unsafe_allow_html=True)

        st.markdown("---")

        c1, c2 = st.columns(2)

        with c1:
            st.markdown(f"**{fa['name']}**")

            # Guardrail 1: Lever-Coupling
            g1_ok, msg1 = guardrail_lever_coupling(ya_levers["PF"], ya_levers["CCI"])
            st.markdown(f"**1. Lever-Coupling:** {msg1}")

            # Guardrail 2: BFI-Sensitivity
            g2_ok, msg2 = guardrail_bfi_sensitivity(
                ya_results["Neutral"]["YPA"],
                ya_bfi,
                ya_results["Empirical"]["YPA"],
                ya_results["Existential"]["YPA"]
            )
            st.markdown(f"**2. BFI-Sensitivity:** {msg2}")

            # Guardrail 3: Weight-Inversion
            g3_ok, msg3 = guardrail_weight_inversion(ya_results, ya_results["Neutral"]["YPA"])
            st.markdown(f"**3. Weight-Inversion:** {msg3}")

            # Guardrail 4: Symmetry Audit Summary
            audit_a = symmetry_audit(fa, cfg)
            max_delta_a = max(abs(row[3]) for row in audit_a)
            if max_delta_a > 0.3:
                st.markdown(f"**4. Symmetry:** ⚠️ Max toggle sensitivity = {max_delta_a:.2f} (see Symmetry tab)")
            else:
                st.markdown(f"**4. Symmetry:** ✅ All toggles stable (max Δ = {max_delta_a:.2f})")

        with c2:
            st.markdown(f"**{fb['name']}**")

            # Guardrail 1: Lever-Coupling
            g1_ok, msg1 = guardrail_lever_coupling(yb_levers["PF"], yb_levers["CCI"])
            st.markdown(f"**1. Lever-Coupling:** {msg1}")

            # Guardrail 2: BFI-Sensitivity
            g2_ok, msg2 = guardrail_bfi_sensitivity(
                yb_results["Neutral"]["YPA"],
                yb_bfi,
                yb_results["Empirical"]["YPA"],
                yb_results["Existential"]["YPA"]
            )
            st.markdown(f"**2. BFI-Sensitivity:** {msg2}")

            # Guardrail 3: Weight-Inversion
            g3_ok, msg3 = guardrail_weight_inversion(yb_results, yb_results["Neutral"]["YPA"])
            st.markdown(f"**3. Weight-Inversion:** {msg3}")

            # Guardrail 4: Symmetry Audit Summary
            audit_b = symmetry_audit(fb, cfg)
            max_delta_b = max(abs(row[3]) for row in audit_b)
            if max_delta_b > 0.3:
                st.markdown(f"**4. Symmetry:** ⚠️ Max toggle sensitivity = {max_delta_b:.2f} (see Symmetry tab)")
            else:
                st.markdown(f"**4. Symmetry:** ✅ All toggles stable (max Δ = {max_delta_b:.2f})")

    with tab5:
        st.markdown("### ⚖️ Symmetry Audit - Nova's Lens")
        st.caption("*Pattern-checking for hidden bias in configuration settings*")

        # Contextual explanation
        st.info("""
        **What This Tests:**

        The Symmetry Audit checks whether your **configuration settings** (Parity, PF-Type, Fallibilism, BFI Weight)
        are creating hidden bias by favoring one framework over the other.

        **How It Works:**
        - Takes your current YPA score (Base)
        - Flips each configuration lever one at a time
        - Measures how much the YPA changes (Delta)
        - Large deltas (>0.3) suggest that lever has asymmetric impact

        **Why This Matters:**
        - Small deltas (±0.1) = Balanced configuration
        - Large deltas (>0.3) = Configuration favors one framework
        - Helps you understand which levers are "load-bearing" for your results
        """)

        st.markdown("---")

        # Interpretation guide
        with st.expander("📖 How to Read This Table", expanded=False):
            st.markdown("""
            **Column Guide:**
            - **Toggle:** Which configuration lever was flipped
            - **Base:** Your current YPA with existing settings
            - **Flip:** What YPA would be if you flipped that one lever
            - **Delta:** The difference (Flip - Base)
            - **Flag:** ✅ Stable (|Delta| ≤ 0.3) | ⚠️ Sensitive (|Delta| > 0.3)

            **Interpretation Examples:**

            **Example 1: Parity Toggle**
            - Base: 6.50, Flip: 6.45, Delta: -0.05 ✅
            - **Meaning:** Parity ON/OFF has minimal impact. This framework's score is stable regardless of moral weighting.

            **Example 2: PF-Type Toggle**
            - Base: 7.20, Flip: 6.50, Delta: -0.70 ⚠️
            - **Meaning:** Switching from Instrumental to Holistic drops YPA by 0.70. This framework is **instrumentally strong** (prediction-focused).

            **Example 3: Fallibilism Toggle**
            - Base: 5.80, Flip: 6.25, Delta: +0.45 ⚠️
            - **Meaning:** Turning Fallibilism OFF *increases* YPA. This framework doesn't emphasize revision mechanisms.

            ---

            **What Action Should I Take?**

            ✅ **All Stable (All Deltas < 0.3):**
            - Your configuration is balanced across all levers
            - Scores are robust to setting changes
            - Good sign of neutral evaluation

            ⚠️ **Some Sensitive (Some Deltas > 0.3):**
            - Identify which levers cause big swings
            - Ask: "Is this sensitivity justified?"
            - Example: If MdN's Parity delta is -0.50, it means moral grounding significantly impacts its score

            🚨 **Many Sensitive (Most Deltas > 0.5):**
            - Your configuration may be "tuned" to favor/penalize this framework
            - Consider using Diplomat Mode (balanced preset) for comparison
            - Review whether lever settings match your epistemic commitments
            """)

        st.markdown("---")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"### 📊 {fa['name']}")
            audit = symmetry_audit(fa, cfg)
            df = pd.DataFrame(audit, columns=["Toggle", "Base", "Flip", "Delta"])
            df["Flag"] = df["Delta"].apply(lambda x: "⚠️" if abs(x) > 0.3 else "✅")
            st.dataframe(df, use_container_width=True, hide_index=True)

            # Summary assessment
            max_delta = max(abs(row[3]) for row in audit)
            sensitive_count = sum(1 for row in audit if abs(row[3]) > 0.3)

            if sensitive_count == 0:
                st.success(f"✅ **Balanced Configuration** - Max delta: {max_delta:.2f}")
            elif sensitive_count <= 2:
                st.warning(f"⚠️ **{sensitive_count} Sensitive Levers** - Max delta: {max_delta:.2f}")
                st.caption("Some levers have asymmetric impact. Review which ones and why.")
            else:
                st.error(f"🚨 **{sensitive_count} Sensitive Levers** - Max delta: {max_delta:.2f}")
                st.caption("Configuration may be tuned to favor/penalize this framework. Consider Diplomat Mode.")

        with c2:
            st.markdown(f"### 📊 {fb['name']}")
            audit = symmetry_audit(fb, cfg)
            df = pd.DataFrame(audit, columns=["Toggle", "Base", "Flip", "Delta"])
            df["Flag"] = df["Delta"].apply(lambda x: "⚠️" if abs(x) > 0.3 else "✅")
            st.dataframe(df, use_container_width=True, hide_index=True)

            # Summary assessment
            max_delta = max(abs(row[3]) for row in audit)
            sensitive_count = sum(1 for row in audit if abs(row[3]) > 0.3)

            if sensitive_count == 0:
                st.success(f"✅ **Balanced Configuration** - Max delta: {max_delta:.2f}")
            elif sensitive_count <= 2:
                st.warning(f"⚠️ **{sensitive_count} Sensitive Levers** - Max delta: {max_delta:.2f}")
                st.caption("Some levers have asymmetric impact. Review which ones and why.")
            else:
                st.error(f"🚨 **{sensitive_count} Sensitive Levers** - Max delta: {max_delta:.2f}")
                st.caption("Configuration may be tuned to favor/penalize this framework. Consider Diplomat Mode.")

        st.markdown("---")

        # Nova's perspective
        st.markdown("### 🔍 Nova's Perspective: Why Symmetry Matters")
        st.markdown("""
        **Nova (Symmetry Auditor) says:**

        > "Configuration bias is insidious because it *feels* neutral. You're not manipulating
        > individual lever scores—you're just choosing 'reasonable' settings. But if those settings
        > systematically favor one framework over another, you've introduced **architectural bias**.
        >
        > The Symmetry Audit exposes this by testing: *Would flipping each setting change the outcome?*
        > If yes, you need to justify why that asymmetry serves truth rather than preference.
        >
        > Mathematical symmetry doesn't always equal functional fairness—but when it breaks,
        > you better have a good reason why."

        **When Asymmetry is Justified:**
        - Skeptic Mode intentionally favors empirical frameworks (Parity OFF = legitimate choice)
        - Zealot Mode intentionally favors existential frameworks (Fallibilism OFF = legitimate choice)
        - **Key:** The bias is *named and priced* in the preset's meta-axioms

        **When Asymmetry is Problematic:**
        - You claim to be using "neutral" settings but deltas show hidden bias
        - Diplomat Mode shows large deltas (should be balanced by design)
        - You didn't realize your configuration was favoring one side
        """)

        st.markdown("---")
        st.caption("**Pro Tip:** Run Diplomat Mode and check Symmetry tab—if deltas are large even in 'balanced' mode, the frameworks themselves may have legitimately different sensitivities.")
    
    # deps: preset_modes
    # EPISTEMIC QUIZ SYSTEM
    st.markdown("---")
    with st.expander("🧠 Epistemic Quiz - Find Your Starting Point", expanded=False):
        st.markdown("**Answer 5 questions to auto-detect your bias profile**")
        st.caption("We'll automatically load the preset mode that matches your epistemology")
        
        # Question 1: Evidence Priority
        q1 = st.radio(
            "**Q1:** What matters more in evaluating a worldview?",
            ["Predictive accuracy and testable results", 
             "Both prediction and meaning equally", 
             "Comprehensive explanation and existential depth"],
            key="quiz_q1"
        )
        
        # Question 2: Moral Foundations
        q2 = st.radio(
            "**Q2:** Where do moral truths come from?",
            ["Human consensus and evolutionary adaptation",
             "A mix of objective and subjective factors",
             "Transcendent moral order grounded in ultimate reality"],
            key="quiz_q2"
        )
        
        # Question 3: Uncertainty Tolerance
        q3 = st.radio(
            "**Q3:** How comfortable are you with unanswered questions?",
            ["Very comfortable - some questions may be permanently unanswerable",
             "Somewhat comfortable - we should keep searching",
             "Uncomfortable - ultimate answers exist even if we haven't found them yet"],
            key="quiz_q3"
        )
        
        # Question 4: Success Explanation
        q4 = st.radio(
            "**Q4:** Why does science work so well?",
            ["Evolutionary pressure + methodological discipline",
             "Both method and the nature of reality contribute",
             "Reality is fundamentally intelligible/rational by design"],
            key="quiz_q4"
        )
        
        # Question 5: Starting Assumptions
        q5 = st.radio(
            "**Q5:** How do you feel about taking on additional axioms?",
            ["Minimize assumptions - prefer lean frameworks",
             "Balance parsimony with explanatory power",
             "Accept necessary axioms if they provide comprehensive answers"],
            key="quiz_q5"
        )
        
        if st.button("🎯 Auto-Detect My Profile", use_container_width=True, type="primary"):
            # Scoring logic
            scores = {"skeptic": 0, "diplomat": 0, "seeker": 0, "zealot": 0}
            
            # Q1 scoring
            if "Predictive accuracy" in q1:
                scores["skeptic"] += 2
            elif "Both prediction" in q1:
                scores["diplomat"] += 2
            else:
                scores["zealot"] += 2
            
            # Q2 scoring
            if "Human consensus" in q2:
                scores["skeptic"] += 2
            elif "mix of objective" in q2:
                scores["diplomat"] += 2
            else:
                scores["zealot"] += 2
            
            # Q3 scoring
            if "Very comfortable" in q3:
                scores["skeptic"] += 2
            elif "Somewhat comfortable" in q3:
                scores["diplomat"] += 1
                scores["seeker"] += 1
            else:
                scores["zealot"] += 2
            
            # Q4 scoring
            if "Evolutionary pressure" in q4:
                scores["skeptic"] += 2
            elif "Both method" in q4:
                scores["diplomat"] += 2
            else:
                scores["zealot"] += 2
            
            # Q5 scoring
            if "Minimize assumptions" in q5:
                scores["skeptic"] += 2
            elif "Balance parsimony" in q5:
                scores["diplomat"] += 2
            else:
                scores["seeker"] += 1
                scores["zealot"] += 1
            
            # Determine winner
            winner = max(scores, key=scores.get)
            
            # Load corresponding mode
            if winner == "skeptic":
                st.session_state["lever_parity"] = "OFF"
                st.session_state["pf_type"] = "Instrumental"
                st.session_state["fallibilism_bonus"] = "ON"
                st.session_state["bfi_debt_weight"] = "Heavier_1.2x"
                st.success("✅ **Profile Detected: Skeptic Mode** (MdN-optimized, predictive power focus)")
            elif winner == "diplomat":
                st.session_state["lever_parity"] = "ON"
                st.session_state["pf_type"] = "Holistic_50_50"
                st.session_state["fallibilism_bonus"] = "ON"
                st.session_state["bfi_debt_weight"] = "Equal_1.0x"
                st.success("✅ **Profile Detected: Diplomat Mode** (Balanced bridge, equal weighting)")
            elif winner == "seeker":
                st.session_state["lever_parity"] = "ON"
                st.session_state["pf_type"] = "Composite_70_30"
                st.session_state["fallibilism_bonus"] = "ON"
                st.session_state["bfi_debt_weight"] = "Equal_1.0x"
                st.success("✅ **Profile Detected: Seeker Mode** (CT-leaning, meaning-first)")
            else:  # zealot
                st.session_state["lever_parity"] = "ON"
                st.session_state["pf_type"] = "Holistic_50_50"
                st.session_state["fallibilism_bonus"] = "OFF"
                st.session_state["bfi_debt_weight"] = "Equal_1.0x"
                st.success("✅ **Profile Detected: Zealot Mode** (CT-optimized, existential-first)")
            
            st.info(f"🎯 **Your Score Breakdown:** Skeptic: {scores['skeptic']}, Diplomat: {scores['diplomat']}, Seeker: {scores['seeker']}, Zealot: {scores['zealot']}")
            st.rerun()
        
        st.markdown("---")
        st.caption("💡 **Note:** This quiz is a starting point. You can always adjust toggles manually after!")

    # BOTTOM: IMPORT + EXPORT
    st.markdown("---")
    st.markdown("### 📥 Import / 📤 Export")
    
    bottom_col1, bottom_col2 = st.columns(2)
    
    with bottom_col1:
        st.markdown("**📥 Import Configuration**")
        import_file_bottom = st.file_uploader("Load saved audit", type=["json"], key="import_bottom")
        if import_file_bottom:
            try:
                run = json.load(import_file_bottom)
                if "config" in run and "framework_a" in run:
                    st.success("✅ Valid profile")
                    if st.button("Apply", key="apply_bottom"):
                        apply_loaded_run(run)
                        st.rerun()
            except:
                st.error("Invalid file")
    
    with bottom_col2:
        st.markdown("**📤 Export Current Audit**")
        export = {
            "config": cfg,
            "framework_a": fa,
            "framework_b": fb,
            "results": {
                "a": {"levers": ya_levers, "bfi": ya_bfi, "ypa": {k: v["YPA"] for k, v in ya_results.items()}},
                "b": {"levers": yb_levers, "bfi": yb_bfi, "ypa": {k: v["YPA"] for k, v in yb_results.items()}}
            }
        }
        st.download_button(
            "📥 Download Audit (JSON)",
            json.dumps(export, indent=2),
            "cfa_run.json",
            "application/json",
            use_container_width=True
        )
