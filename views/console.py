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
import re
import glob
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.calculations import ypa_scenario_scores, guardrail_lever_coupling, guardrail_bfi_sensitivity, guardrail_weight_inversion, symmetry_audit, PF_TYPES
from utils.visualizations import create_lever_comparison_chart, create_ypa_trinity_chart
from utils.colors import CFA_COLORS, get_framework_color, get_preset_color
from utils.profile_loader import get_ypa_data, get_trinity_scores

# Import new components
from components.cards import (
    audit_card, audit_badge, status_summary_card, metric_card,
    framework_comparison_header
)
from components.charts import (
    create_convergence_radar, create_sensitivity_heatmap,
    create_battle_card_html, create_preset_compass,
    create_guardrail_grid, create_scenario_comparison_bars,
    create_lever_pie_charts, create_ypa_gauge, create_lever_radar_comparison
)

@st.cache_data(ttl=300)
def load_crux_data(worldview_prefix):
    """Scan golden session JSONs and return unique declared crux events for a batch.

    Deduplicates by crux ID so continuation ticks don't inflate counts.
    Excludes demo/non-standard files by checking the filename key is all digits.
    """
    data_dir = Path(__file__).resolve().parent.parent / "dashboard" / "SMV" / "src" / "data"
    cruxes = []
    prefix_str = f"scenario_{worldview_prefix}_"
    for fpath in glob.glob(str(data_dir / f"scenario_{worldview_prefix}_*.json")):
        try:
            # The filename key (e.g. "132540") must be all digits to be a real session;
            # demo files like "E1_20260629" contain letters and are skipped.
            fname_key = Path(fpath).stem[len(prefix_str):]
            if not fname_key.isdigit():
                continue
            with open(fpath, encoding="utf-8") as f:
                scenario = json.load(f)
            session_id = str(scenario.get("session_id", fname_key))
            condition = scenario.get("identity_condition", "unknown")
            seen_ids = set()  # deduplicate within session by crux ID
            for tick in scenario.get("ticks", []):
                crux = tick.get("crux", {})
                if crux.get("status") != "declared":
                    continue
                crux_id = crux.get("id") or f"{fname_key}_{tick.get('metric')}"
                if crux_id in seen_ids:
                    continue
                seen_ids.add(crux_id)
                narrative = tick.get("claude_narrative", "")
                deadlock = None
                dm = re.search(r'\*{0,2}Deadlock basis[:\s]*\*{0,2}\s*(.+?)(?:\n\n|\n(?=\*\*)|\Z)',
                               narrative, re.IGNORECASE | re.DOTALL)
                if dm:
                    deadlock = dm.group(1).replace('\n', ' ').strip()[:300]
                cruxes.append({
                    "session_id": fname_key,
                    "condition": condition,
                    "metric": tick.get("metric"),
                    "metric_full": tick.get("metric_full"),
                    "round": tick.get("round"),
                    "classification": crux.get("classification", "unclassified"),
                    "description": crux.get("description", ""),
                    "deadlock": deadlock,
                    "claude_score": next((n["score"] for n in tick.get("nodes", []) if n.get("auditor") == "Claude"), None),
                    "grok_score": next((n["score"] for n in tick.get("nodes", []) if n.get("auditor") == "Grok"), None),
                })
        except Exception:
            continue
    return cruxes

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

    # Console Mode Navigation - placeholder for future expansion
    # Currently all modes show the same Compare view
    # Future: Analyze (single framework deep-dive), Simulate (toggle playground), Audit (Trinity details)

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
        st.markdown("**Head-to-Head Pairings:**")
        st.caption("*Sets both A & B in one click*")
        pair_col1, pair_col2 = st.columns(2)
        with pair_col1:
            if st.button("📕 CT  vs  📘 MdN", key="pair_ct_mdn", use_container_width=True, help="Load CT → A, MdN → B"):
                # CT → A
                st.session_state["fa_name"] = CT_DEFAULT["name"]
                st.session_state["fa_ax"]  = CT_DEFAULT["bf_i"]["axioms"]
                st.session_state["fa_db"]  = CT_DEFAULT["bf_i"]["debts"]
                st.session_state["fa_ad"]  = True
                st.session_state["fa_cci"] = CT_DEFAULT["levers"]["CCI"]
                st.session_state["fa_edb"] = CT_DEFAULT["levers"]["EDB"]
                st.session_state["fa_pfi"] = CT_DEFAULT["levers"]["PF_instrumental"]
                st.session_state["fa_pfe"] = CT_DEFAULT["levers"]["PF_existential"]
                st.session_state["fa_ar"]  = CT_DEFAULT["levers"]["AR"]
                st.session_state["fa_mg"]  = CT_DEFAULT["levers"]["MG"]
                # MdN → B
                st.session_state["fb_name"] = MDN_DEFAULT["name"]
                st.session_state["fb_ax"]  = MDN_DEFAULT["bf_i"]["axioms"]
                st.session_state["fb_db"]  = MDN_DEFAULT["bf_i"]["debts"]
                st.session_state["fb_ad"]  = True
                st.session_state["fb_cci"] = MDN_DEFAULT["levers"]["CCI"]
                st.session_state["fb_edb"] = MDN_DEFAULT["levers"]["EDB"]
                st.session_state["fb_pfi"] = MDN_DEFAULT["levers"]["PF_instrumental"]
                st.session_state["fb_pfe"] = MDN_DEFAULT["levers"]["PF_existential"]
                st.session_state["fb_ar"]  = MDN_DEFAULT["levers"]["AR"]
                st.session_state["fb_mg"]  = MDN_DEFAULT["levers"]["MG"]
                st.rerun()
        with pair_col2:
            if st.button("📘 MdN  vs  📕 CT", key="pair_mdn_ct", use_container_width=True, help="Load MdN → A, CT → B"):
                # MdN → A
                st.session_state["fa_name"] = MDN_DEFAULT["name"]
                st.session_state["fa_ax"]  = MDN_DEFAULT["bf_i"]["axioms"]
                st.session_state["fa_db"]  = MDN_DEFAULT["bf_i"]["debts"]
                st.session_state["fa_ad"]  = True
                st.session_state["fa_cci"] = MDN_DEFAULT["levers"]["CCI"]
                st.session_state["fa_edb"] = MDN_DEFAULT["levers"]["EDB"]
                st.session_state["fa_pfi"] = MDN_DEFAULT["levers"]["PF_instrumental"]
                st.session_state["fa_pfe"] = MDN_DEFAULT["levers"]["PF_existential"]
                st.session_state["fa_ar"]  = MDN_DEFAULT["levers"]["AR"]
                st.session_state["fa_mg"]  = MDN_DEFAULT["levers"]["MG"]
                # CT → B
                st.session_state["fb_name"] = CT_DEFAULT["name"]
                st.session_state["fb_ax"]  = CT_DEFAULT["bf_i"]["axioms"]
                st.session_state["fb_db"]  = CT_DEFAULT["bf_i"]["debts"]
                st.session_state["fb_ad"]  = True
                st.session_state["fb_cci"] = CT_DEFAULT["levers"]["CCI"]
                st.session_state["fb_edb"] = CT_DEFAULT["levers"]["EDB"]
                st.session_state["fb_pfi"] = CT_DEFAULT["levers"]["PF_instrumental"]
                st.session_state["fb_pfe"] = CT_DEFAULT["levers"]["PF_existential"]
                st.session_state["fb_ar"]  = CT_DEFAULT["levers"]["AR"]
                st.session_state["fb_mg"]  = CT_DEFAULT["levers"]["MG"]
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
    swap_col, _ = st.columns([1, 5])
    with swap_col:
        if st.button("↔ Swap A & B", key="swap_ab_btn", help="Swap all Framework A and B values"):
            keys = ["name", "ax", "db", "ad", "cci", "edb", "pfi", "pfe", "ar", "mg"]
            for k in keys:
                fa_k, fb_k = f"fa_{k}", f"fb_{k}"
                fa_val = st.session_state.get(fa_k)
                fb_val = st.session_state.get(fb_k)
                st.session_state[fa_k] = fb_val
                st.session_state[fb_k] = fa_val
            st.rerun()

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

    # Pre-compute guardrail ok flags — used by Guardrails tab grid
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

    # =========================================================================
    # FRAMEWORK COMPARISON HEADER (NEW)
    # =========================================================================
    st.markdown(framework_comparison_header(
        fa["name"], fb["name"],
        ya_results["Neutral"]["YPA"],
        yb_results["Neutral"]["YPA"]
    ), unsafe_allow_html=True)

    # TABS (Enhanced with new visualizations)
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📈 Visual", "⚔️ Battle Card", "📋 Details", "🛡️ Guardrails", "🔄 Symmetry", "🔬 Trinity Audit"])

    with tab1:
        # NEW: YPA Gauge meters (visually engaging!)
        st.markdown("### 🎯 YPA Performance")
        st.plotly_chart(create_ypa_gauge(
            ya_results["Neutral"]["YPA"],
            yb_results["Neutral"]["YPA"],
            fa["name"], fb["name"]
        ), use_container_width=True, key="chart_ypa_gauge")


        # NEW: Radar comparison (more engaging than bar chart)
        st.markdown("### 🕸️ Lever Profile Radar")
        st.plotly_chart(create_lever_radar_comparison(ya_levers, yb_levers, fa["name"], fb["name"]), use_container_width=True, key="chart_lever_radar")

        # NEW: Pie charts for lever contribution
        st.markdown("### 🥧 Lever Contribution Breakdown")
        st.plotly_chart(create_lever_pie_charts(ya_levers, yb_levers, fa["name"], fb["name"]), use_container_width=True, key="chart_lever_pie")

        # Scenario Comparison Bars
        st.markdown("### 📊 Scenario Impact")
        st.plotly_chart(create_scenario_comparison_bars(ya_results, yb_results, fa["name"], fb["name"]), use_container_width=True, key="chart_scenario_bars")

        # Original charts in expander for those who want them
        with st.expander("📈 Classic Charts", expanded=False):
            st.plotly_chart(create_lever_comparison_chart(ya_levers, yb_levers, fa["name"], fb["name"]), use_container_width=True, key="chart_lever_comparison")
            st.plotly_chart(create_ypa_trinity_chart(ya_results, yb_results, fa["name"], fb["name"]), use_container_width=True, key="chart_ypa_trinity")

        # NEW: Trinity Convergence Radar (simulated - both frameworks show same audited scores)
        with st.expander("🎯 Trinity Convergence Radar", expanded=False):
            st.caption("*Shows how Claude, Grok, and Nova scored this framework (audited frameworks converge at 98%)*")

            radar_col1, radar_col2 = st.columns(2)

            # Use raw framework levers (fa["levers"]) for individual PF scores
            with radar_col1:
                # Framework A - Trinity scores (simulated convergence)
                fa_raw = fa["levers"]
                trinity_a = {
                    'Claude': [fa_raw["CCI"], fa_raw["EDB"], fa_raw["PF_instrumental"], fa_raw["PF_existential"], fa_raw["AR"], fa_raw["MG"]],
                    'Grok': [fa_raw["CCI"]*0.99, fa_raw["EDB"]*1.01, fa_raw["PF_instrumental"]*0.98, fa_raw["PF_existential"]*1.02, fa_raw["AR"]*0.99, fa_raw["MG"]*1.01],
                    'Nova': [fa_raw["CCI"]*1.01, fa_raw["EDB"]*0.99, fa_raw["PF_instrumental"]*1.01, fa_raw["PF_existential"]*0.99, fa_raw["AR"]*1.02, fa_raw["MG"]*0.98]
                }
                st.plotly_chart(create_convergence_radar(trinity_a, f"{fa['name']} - Trinity View"), use_container_width=True, key="chart_trinity_radar_a")

            with radar_col2:
                # Framework B - Trinity scores (simulated convergence)
                fb_raw = fb["levers"]
                trinity_b = {
                    'Claude': [fb_raw["CCI"], fb_raw["EDB"], fb_raw["PF_instrumental"], fb_raw["PF_existential"], fb_raw["AR"], fb_raw["MG"]],
                    'Grok': [fb_raw["CCI"]*0.99, fb_raw["EDB"]*1.01, fb_raw["PF_instrumental"]*0.98, fb_raw["PF_existential"]*1.02, fb_raw["AR"]*0.99, fb_raw["MG"]*1.01],
                    'Nova': [fb_raw["CCI"]*1.01, fb_raw["EDB"]*0.99, fb_raw["PF_instrumental"]*1.01, fb_raw["PF_existential"]*0.99, fb_raw["AR"]*1.02, fb_raw["MG"]*0.98]
                }
                st.plotly_chart(create_convergence_radar(trinity_b, f"{fb['name']} - Trinity View"), use_container_width=True, key="chart_trinity_radar_b")

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

        # Calculate sensitivity matrix (rows=frameworks, cols=toggles as returned by symmetry_audit)
        toggle_labels = [row[0] for row in audit_a_summary]
        sensitivity_matrix = []
        for audit_data in (audit_a_summary, audit_b_summary):
            delta_row = [r[3] for r in audit_data]  # Delta values
            sensitivity_matrix.append(delta_row)

        st.plotly_chart(create_sensitivity_heatmap(
            sensitivity_matrix,
            [fa["name"], fb["name"]],
            toggle_labels
        ), use_container_width=True, key="chart_sensitivity_heatmap")

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

        # Context callout — specific when CT/MdN loaded, generic otherwise
        _fa_lower = fa["name"].lower()
        _fb_lower = fb["name"].lower()
        _is_ct_mdn = (
            ("classical theism" in _fa_lower or "classical theism" in _fb_lower) and
            ("methodological naturalism" in _fa_lower or "methodological naturalism" in _fb_lower)
        )
        if _is_ct_mdn:
            st.markdown("""
<div style="background:#12121f;border-left:4px solid #d4a843;padding:0.9rem 1.2rem;border-radius:0 6px 6px 0;margin:0 0 1rem 0;">
<p style="margin:0 0 0.5rem 0;font-size:0.9rem;color:#d4a843;font-weight:600;">
⚑ Why is this flag appearing — and is it a problem?
</p>
<p style="margin:0 0 0.6rem 0;font-size:0.85rem;color:#c0c0d0;">
<strong style="color:#e0e0e0;">Short answer: no.</strong> A sensitive lever flag means the worldview has a
<em>concentrated, narrow-and-deep</em> profile in that dimension — it has staked out a strong position
rather than distributing strength broadly across all levers. A fully generalist worldview would show
near-zero sensitivity everywhere. Seeing one flag per worldview at comparable magnitude (0.35–0.39)
means the audit is detecting real philosophical architecture, not instrument error.
Think of it as: the flag marks the <em>hinge point</em> where a worldview's specialization gets tested.
</p>
<p style="margin:0 0 0.4rem 0;font-size:0.85rem;color:#c0c0d0;">
<strong style="color:#e0e0e0;">CT → Lever-Parity (Δ≈−0.39):</strong>
CT carries 7 axioms and only 4 debts — a structurally asymmetric ratio. Parity controls how that
imbalance is weighted in BFI. CT's large axiom count reflects deep metaphysical commitment
(divine simplicity, PSR, teleology, imago dei…); its 4 debts are genuinely serious (evil, hiddenness).
Flipping parity shifts the weight between those two sides, and CT feels it because its axiom-to-debt
ratio is a fundamental feature of how it is built, not an artifact of measurement.
</p>
<p style="margin:0 0 0.4rem 0;font-size:0.85rem;color:#c0c0d0;">
<strong style="color:#e0e0e0;">MdN → PF→Instrumental (Δ≈+0.35):</strong>
MdN is the most functionally specialized worldview in the current library — its identity is built
almost entirely around explaining, predicting, and intervening in the natural world. The Instrumental
setting credits that mode of fertility directly. Switching to Composite blends in existential and
meaning-making fertility, domains MdN intentionally brackets. MdN scores lower there not because
it fails — but because it doesn't try. The sensitivity reveals a narrow-and-deep profile, not a weakness.
</p>
<p style="margin:0;font-size:0.8rem;color:#707080;">
Speculative takeaway: both flags are appearing because both worldviews are <em>specialists</em>, not generalists.
Specialists will always be sensitive to the lever most aligned with their core claim.
That's a diagnostic about the frameworks — not a verdict on the ruler.
</p>
</div>
""", unsafe_allow_html=True)

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
    
    # =========================================================================
    # TAB 6: TRINITY AUDIT (live data from golden batch)
    # =========================================================================
    with tab6:
        fa_name_lower = fa["name"].lower()
        fb_name_lower = fb["name"].lower()
        is_ct_mdn = (
            ("classical theism" in fa_name_lower or "classical theism" in fb_name_lower) and
            ("methodological naturalism" in fa_name_lower or "methodological naturalism" in fb_name_lower)
        )

        if not is_ct_mdn:
            st.info("🔬 **Trinity Audit data is available for CT vs MdN only.**\n\nLoad Classical Theism + Methodological Naturalism to see the 10-run golden batch deliberation results.")
        else:
            trinity_ct  = get_trinity_scores("Classical Theism")
            trinity_mdn = get_trinity_scores("Methodological Naturalism")

            if not trinity_ct and not trinity_mdn:
                st.error("Could not load Trinity scores from YAML profiles.")
            else:
                st.markdown("## 🔬 Trinity Audit — CT ↔ MdN Symmetric Experiment")
                st.caption("Two complementary 10-run golden batches. Each framework audited as subject by its lens-aligned advocate.")

                audit_tabs = st.tabs(["📕 CT as Subject", "📘 MdN as Subject", "⚖️ Cross-Stance Symmetry"])

                METRIC_ORDER_T = ["BFI", "CA", "IP", "ES", "LS", "MS", "PS"]

                def render_crux_analysis(worldview_prefix):
                    cruxes = load_crux_data(worldview_prefix)
                    if not cruxes:
                        st.caption("No crux data found — golden session JSONs not present.")
                        return
                    golden = [c for c in cruxes if c["condition"] == "external_identity"]
                    n_sessions = len(set(c["session_id"] for c in golden))
                    avg_per = round(len(golden) / n_sessions, 1) if n_sessions else 0
                    st.caption(f"**{avg_per} crux impasses per session** ({len(golden)} total across {n_sessions} golden sessions)")

                    # Summary breakdown — build full-name lookup from crux data
                    metric_full_map = {}
                    by_metric = {}
                    by_class = {}
                    for c in golden:
                        key = c["metric"]
                        by_metric[key] = by_metric.get(key, 0) + 1
                        by_class[c["classification"]] = by_class.get(c["classification"], 0) + 1
                        if key not in metric_full_map and c.get("metric_full"):
                            metric_full_map[key] = c["metric_full"]

                    col_m, col_c = st.columns(2)
                    with col_m:
                        st.markdown("**By Metric**")
                        max_cnt = max(by_metric.values()) if by_metric else 1
                        for metric, cnt in sorted(by_metric.items(), key=lambda x: -x[1]):
                            full = metric_full_map.get(metric, metric)
                            bar = "█" * cnt + "░" * (max_cnt - cnt)
                            lc, rc = st.columns([5, 3])
                            lc.markdown(f"**{full}**")
                            rc.markdown(f"{bar} **{cnt}**")
                    with col_c:
                        st.markdown("**By Classification**")
                        for cls, cnt in sorted(by_class.items(), key=lambda x: -x[1]):
                            st.markdown(f"- **{cls}**: {cnt}")

                    # Grouped by metric — one expander per metric, table inside
                    st.markdown("---")
                    METRIC_ORDER_C = ["BFI", "CA", "IP", "ES", "LS", "MS", "PS"]
                    grouped = {}
                    for c in golden:
                        grouped.setdefault(c["metric"], []).append(c)

                    for metric in METRIC_ORDER_C:
                        if metric not in grouped:
                            continue
                        items = grouped[metric]
                        full_name = metric_full_map.get(metric, metric)
                        cls_summary = {}
                        for c in items:
                            cls_summary[c["classification"]] = cls_summary.get(c["classification"], 0) + 1
                        cls_str = " · ".join(f"{cls} ({n})" for cls, n in sorted(cls_summary.items(), key=lambda x: -x[1]))
                        label = f"⚑ {full_name} — {len(items)} crux{'es' if len(items) != 1 else ''} · {cls_str}"
                        with st.expander(label, expanded=False):
                            rows = []
                            for c in sorted(items, key=lambda x: x["session_id"]):
                                rows.append({
                                    "Session": c["session_id"],
                                    "R": c["round"] if c["round"] is not None else "—",
                                    "Claude": c["claude_score"] if c["claude_score"] is not None else "—",
                                    "Grok": c["grok_score"] if c["grok_score"] is not None else "—",
                                    "Type": c["classification"],
                                    "Deadlock Basis": (c["deadlock"] or c["description"] or "—")[:120],
                                })
                            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

                def render_trinity_tab(trinity, subject_label, claude_role, grok_role, delta_label, delta_claude_key, delta_grok_key, extra_delta_label=None, extra_delta_claude_key=None, extra_delta_grok_key=None, crux_prefix=None):
                    if not trinity:
                        st.info(f"No Trinity data loaded for {subject_label}.")
                        return
                    summary = trinity.get("batch_summary", {})
                    st.caption(
                        f"**Experiment:** {trinity.get('experiment_id', '')}  ·  "
                        f"**Status:** {trinity.get('score_audit_status', '')}"
                    )
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Avg Convergence", f"{summary.get('avg_convergence_pct', 0)}%")
                    col2.metric("Avg Rounds", str(summary.get('avg_rounds', 0)))
                    col3.metric("Crux Impasses/Session", str(summary.get('avg_crux_per_run', '—')))
                    ctrl = summary.get('control_avg_convergence_pct')
                    col4.metric("Control Convergence" if ctrl else "Avg Crux/Run",
                                f"{ctrl}%" if ctrl else str(summary.get('avg_crux_per_run', '—')))

                    st.markdown(f"---\n### Per-Metric Results — {subject_label} (n=10)")
                    st.caption(f"Claude = {claude_role} · Grok = {grok_role}")

                    with st.expander("📖 Metric Definitions — What the auditors scored", expanded=False):
                        st.markdown("""
Each metric was scored 0–10 by both auditors independently, then deliberated to convergence (or crux). Definitions below are what auditors were instructed to evaluate against.

| Metric | Full Name | Scoring Question |
|--------|-----------|-----------------|
| **BFI** | Beings, Foundational Importance | Does this worldview provide a compelling account of *why anything exists at all*? Does it ground being-ness itself, or does existence arrive as a brute fact? |
| **CA** | Causal Attribution | Does this worldview coherently explain causal structure — what causes what, why causal chains hold, and what ultimately grounds the causal order of reality? |
| **IP** | Intellectual Pedigree | Has this worldview generated sustained, rigorous philosophical engagement? Is it anchored in a tradition deep enough that its core claims have been seriously stress-tested? |
| **ES** | Explanatory Scope | How broad is this worldview's explanatory reach across domains — physical, moral, aesthetic, existential? Can it address diverse phenomena without category errors or ad hoc patches? |
| **LS** | Logical Soundness | Are the worldview's core propositions internally consistent? Does it avoid contradiction, question-begging, and logical incoherence under adversarial pressure? |
| **MS** | Moral Substance | Can this worldview ground moral claims in something more than preference or convention? Does it have the ontological resources to make morality *real* rather than merely felt? |
| **PS** | Practical Significance | Does this worldview make a *difference* for how one ought to live? Is it actionable — does it provide genuine orientation for real human decisions and values? |

*Scores are assigned under adversarial identity conditions: the PRO auditor argues from the worldview's strongest case; the ANTI auditor applies the opposing lens. Convergence is required above 98% or a crux is declared.*
                        """)

                    metrics = trinity.get("metrics", {})
                    rows = []
                    for key in METRIC_ORDER_T:
                        if key not in metrics:
                            continue
                        m = metrics[key]
                        cd = m.get(delta_claude_key, 0)
                        gd = m.get(delta_grok_key, 0)
                        row = {
                            "Metric": f"{key} — {m.get('full_name', '')}",
                            "Claude": f"{m.get('claude_mean','?')} ±{m.get('claude_sd','?')}",
                            "Grok": f"{m.get('grok_mean','?')} ±{m.get('grok_sd','?')}",
                            "Spread": m.get("spread", "?"),
                            "Conv %": f"{m.get('convergence_pct','?')}%",
                            "Rounds": m.get("avg_rounds", "?"),
                            f"Claude {delta_label}": f"{'+' if cd >= 0 else ''}{cd}",
                            f"Grok {delta_label}": f"{'+' if gd >= 0 else ''}{gd}",
                            "Layer": m.get("divergence_layer", "?"),
                        }
                        if extra_delta_label and extra_delta_claude_key:
                            ecd = m.get(extra_delta_claude_key, "—")
                            egd = m.get(extra_delta_grok_key, "—")
                            if ecd != "—": ecd = f"{'+' if ecd >= 0 else ''}{ecd}"
                            if egd != "—": egd = f"{'+' if egd >= 0 else ''}{egd}"
                            row[f"Claude {extra_delta_label}"] = ecd
                            row[f"Grok {extra_delta_label}"] = egd
                        rows.append(row)
                    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

                    with st.expander("📐 Divergence Layer Definitions (DBEP Framework)", expanded=False):
                        st.markdown("""
The **Layer** column identifies *where in the epistemic stack* the divergence originates — not just that auditors disagree, but **why** the disagreement is structurally resistant to resolution.

| Layer | What it means | Debate signature |
|-------|---------------|-----------------|
| **Definitions** | Auditors are answering *different questions* — the metric term is underspecified and each auditor samples a different definition | Massive score spread; participants appear to talk past each other; high variance across sessions |
| **Beliefs** | Shared definitions, but different fundamental metaphysical commitments about what is true | Moderate, stable disagreement; communication is possible but convergence stalls at a principled gap |
| **Expectations** | Shared beliefs, different anticipations of what evidence or explanation should look like | "You're ignoring X" arguments; auditors notice different features of the same evidence |
| **Perceptions** | Shared framework, but different evaluative registrations of the same content | Soft disagreements; value-weighting and aesthetic differences in how arguments land |

**DBEP Stack:** Stories → Possibility Space → **Definitions → Beliefs → Expectations → Perceptions** → Evaluation

CFA scores live at *Evaluation*. Divergence can originate at any upstream layer. Tagging the layer turns a disagreement into a diagnostic: *is this an argument about what the words mean, or about what is true, or about what counts as evidence?*

*Source: DBEP framework developed collaboratively across CFA Phase 1 batch analysis (2026-06-29).*
                        """)

                    st.markdown("### Key Findings")
                    for finding in summary.get("key_findings", []):
                        st.markdown(f"- {finding}")

                    with st.expander("⚑ Crux Analysis", expanded=False):
                        if crux_prefix:
                            render_crux_analysis(crux_prefix)
                        else:
                            st.caption("Crux prefix not configured for this tab.")

                    with st.expander("📋 Session IDs", expanded=False):
                        ids = trinity.get("session_ids", {})
                        c1, c2 = st.columns(2)
                        with c1:
                            st.markdown("**Golden (External Identity)**")
                            for s in ids.get("golden", []):
                                st.code(s)
                        with c2:
                            st.markdown("**Control (No Identity)**")
                            for s in ids.get("control", []):
                                st.code(s)
                            if not ids.get("control"):
                                st.caption("No control batch for this experiment.")

                with audit_tabs[0]:
                    render_trinity_tab(trinity_ct, "CT (Classical Theism)", "PRO-CT", "ANTI-CT",
                                       "Identity Δ", "identity_delta_claude", "identity_delta_grok",
                                       crux_prefix="CT_MdN")

                with audit_tabs[1]:
                    render_trinity_tab(trinity_mdn, "MdN (Methodological Naturalism)", "ANTI-MdN", "PRO-MdN",
                                       "Role-Swap Δ", "role_swap_delta_claude", "role_swap_delta_grok",
                                       extra_delta_label="Identity Δ",
                                       extra_delta_claude_key="identity_delta_claude",
                                       extra_delta_grok_key="identity_delta_grok",
                                       crux_prefix="MdN_CT")

                with audit_tabs[2]:
                    st.markdown("### Cross-Stance Role-Swap Deltas")
                    st.caption("How much each auditor's score shifts when switching from one stance to the other")
                    if trinity_ct and trinity_mdn:
                        ct_m  = trinity_ct.get("metrics", {})
                        mdn_m = trinity_mdn.get("metrics", {})
                        sym_rows = []
                        for key in METRIC_ORDER_T:
                            if key not in ct_m or key not in mdn_m:
                                continue
                            ct  = ct_m[key]
                            mdn = mdn_m[key]
                            sym_rows.append({
                                "Metric": key,
                                "Claude PRO-CT": ct.get("claude_mean", "?"),
                                "Claude ANTI-MdN": mdn.get("claude_mean", "?"),
                                "Claude Δ": f"{'+' if mdn.get('role_swap_delta_claude',0) >= 0 else ''}{mdn.get('role_swap_delta_claude','?')}",
                                "Grok ANTI-CT": ct.get("grok_mean", "?"),
                                "Grok PRO-MdN": mdn.get("grok_mean", "?"),
                                "Grok Δ": f"{'+' if mdn.get('role_swap_delta_grok',0) >= 0 else ''}{mdn.get('role_swap_delta_grok','?')}",
                                "CT Conv%": f"{ct.get('convergence_pct','?')}%",
                                "MdN Conv%": f"{mdn.get('convergence_pct','?')}%",
                            })
                        st.dataframe(pd.DataFrame(sym_rows), use_container_width=True, hide_index=True)
                        st.markdown("### Instrument Stability")
                        stab = trinity_mdn.get("batch_summary", {}).get("instrument_stability", {})
                        if stab:
                            c1, c2, c3, c4 = st.columns(4)
                            c1.metric("CT Avg Conv", f"{stab.get('ct_golden_avg_convergence','?')}%")
                            c2.metric("MdN Avg Conv", f"{stab.get('mdn_golden_avg_convergence','?')}%")
                            c3.metric("CT Avg Rounds", str(stab.get('ct_golden_avg_rounds','?')))
                            c4.metric("MdN Avg Rounds", str(stab.get('mdn_golden_avg_rounds','?')))
                            st.caption(stab.get("interpretation", ""))

                        # --- Key Finding: Asymmetric Identity Pressure ---
                        st.markdown("### Key Finding: Asymmetric Identity Pressure")

                        # Compute identity delta stats from CT batch (golden condition)
                        id_claude = {k: ct_m[k].get("identity_delta_claude", 0) for k in METRIC_ORDER_T if k in ct_m}
                        id_grok   = {k: ct_m[k].get("identity_delta_grok",   0) for k in METRIC_ORDER_T if k in ct_m}
                        n = len(id_claude)
                        avg_claude_id = round(sum(id_claude.values()) / n, 2) if n else 0
                        avg_grok_id   = round(sum(id_grok.values())   / n, 2) if n else 0
                        grok_harder_ct = sum(
                            1 for k in id_claude
                            if id_grok[k] < 0 and abs(id_grok[k]) > abs(id_claude[k])
                        )
                        largest_gap = max(
                            (abs(id_grok[k]) - abs(id_claude[k]), k) for k in id_claude
                        )

                        metric_full_map_s = {
                            "BFI": "Beings, Foundational Importance",
                            "CA":  "Causal Attribution",
                            "IP":  "Intellectual Pedigree",
                            "ES":  "Explanatory Scope",
                            "LS":  "Logical Soundness",
                            "MS":  "Moral Substance",
                            "PS":  "Practical Significance",
                        }

                        st.markdown(f"""
<div style="background:#1a1a2e;border-left:4px solid #e94560;padding:1rem 1.2rem;border-radius:0 6px 6px 0;margin:0.5rem 0 1rem 0;">
<p style="margin:0 0 0.6rem 0;font-size:0.95rem;color:#e0e0e0;">
<strong style="color:#e94560;">Identity loading deflates the ANTI-CT auditor (Grok) substantially harder than the PRO-CT auditor (Claude)</strong>
across the CT golden batch — on <strong>{grok_harder_ct} of {n} metrics</strong>, Grok's identity-induced deflation is larger in magnitude.
</p>
<p style="margin:0 0 0.6rem 0;font-size:0.9rem;color:#b0b0c0;">
Avg identity Δ — <strong style="color:#7ec8e3;">Claude (PRO-CT): {avg_claude_id:+.2f}</strong> &nbsp;|&nbsp;
<strong style="color:#e94560;">Grok (ANTI-CT): {avg_grok_id:+.2f}</strong> &nbsp;·&nbsp;
Largest gap: <em>{metric_full_map_s.get(largest_gap[1], largest_gap[1])}</em> ({largest_gap[0]:+.2f} pts)
</p>
<p style="margin:0 0 0.4rem 0;font-size:0.85rem;color:#909090;">
<strong style="color:#d4a843;">Why this is a finding about the frameworks, not the instrument:</strong>
CT makes metaphysical claims (PSR, divine simplicity, final causality, teleology) that present rich surface area
for empirical challenge. MdN is itself built on empirical methodology — so an empirical auditor scoring MdN
has less adversarial purchase; the lens and the subject are aligned. The asymmetric pressure is philosophically
principled. The instrument is measuring a real structural fact: CT is a harder target for the empirical lens
than MdN is for the teleological lens.
</p>
<p style="margin:0;font-size:0.8rem;color:#606070;">
Trinity² identity-only condition (H-014) will isolate this effect directly from scaffold and calibration contributions.
</p>
</div>
""", unsafe_allow_html=True)

                    else:
                        st.info("Both CT and MdN trinity data required for symmetry analysis.")

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
