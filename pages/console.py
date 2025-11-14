"""
CFA v4.0 - Console (FIXED VERSION)
- Per-framework preset buttons ABOVE sliders
- Global preset buttons removed (they break when below)
- Sidebar simplified (just Import at bottom)
- Bottom page has Import + Export side-by-side
"""

import streamlit as st
import pandas as pd
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.calculations import ypa_scenario_scores, guardrail_lever_coupling, guardrail_bfi_sensitivity, guardrail_weight_inversion, symmetry_audit, PF_TYPES
from utils.visualizations import create_lever_comparison_chart, create_ypa_trinity_chart
# Deprecated: from utils.frameworks import MDN_DEFAULT, CT_DEFAULT
# Now loading from profiles via profile_loader
from utils.profile_loader import get_ypa_data

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

def render():
    """Render console"""
    
    # Initialize session state
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
    
    # Header
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown('<p style="font-size:2.5rem;font-weight:bold;color:#1f77b4;">⚖️ CFA v4.0 Console</p>', unsafe_allow_html=True)
    with col2:
        if st.button("🏠 Home"):
            st.session_state.page = 'landing'
            st.rerun()
    
    st.markdown('**"All Named, All Priced" — Interactive Comparison Tool**')
    st.markdown("---")

    # SIDEBAR
    st.sidebar.header("🎛️ Configuration")
    
    # Preset Profile Library
    with st.sidebar.expander("📚 Load Preset Profile", expanded=False):
        st.markdown("**Pre-Audited Frameworks:**")
        
        preset_options = {
            "-- Select Framework --": None,
            "✅ Methodological Naturalism (MdN)": "mdn",
            "✅ Classical Theism (CT)": "ct",
            "🔜 Buddhism": "coming",
            "🔜 Stoicism": "coming",
            "🔜 Pragmatism": "coming",
            "🔜 Process Theology": "coming",
            "🔜 Secular Humanism": "coming",
            "🔜 Metaphysical Naturalism": "coming"
        }
        
        selected_preset = st.selectbox(
            "Choose Framework:",
            list(preset_options.keys()),
            key="preset_selector"
        )
        
        preset_key = preset_options[selected_preset]
        
        if preset_key == "mdn":
            st.info("**Methodological Naturalism**\n\nResearch protocol assuming testable natural causes. Audited by Claude + Grok with 98% convergence.")
            
            if st.button("Load MdN Profile", use_container_width=True):
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
                st.success("✅ MdN loaded into Framework A!")
                st.rerun()
        
        elif preset_key == "ct":
            st.info("**Classical Theism**\n\nTraditional monotheistic worldview. Audited by Claude + Grok with 98% convergence.")
            
            if st.button("Load CT Profile", use_container_width=True):
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
                st.success("✅ CT loaded into Framework B!")
                st.rerun()
        
        elif preset_key == "coming":
            st.warning(f"**{selected_preset.replace('🔜 ', '')}**\n\nAudit in progress. Check back soon!")
        
        if selected_preset != "-- Select Framework --":
            st.markdown("---")
            st.caption("💡 **Tip:** Load two presets to compare!")
    
    st.sidebar.markdown("---")

    # deps: preset_modes
    # NEW v4.0: Preset Mode Spectrum
    with st.sidebar.expander("🎚️ Preset Mode Spectrum", expanded=False):
        st.markdown("**Quick Configuration Profiles:**")
        st.caption("Set all toggles to match your starting epistemology")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔬 Skeptic Mode", use_container_width=True):
                st.session_state["lever_parity"] = "OFF"
                st.session_state["pf_type"] = "Instrumental"
                st.session_state["fallibilism_bonus"] = "ON"
                st.session_state["bfi_debt_weight"] = "Heavier_1.2x"
                st.success("✅ Skeptic Mode loaded! (MdN-optimized)")
                st.rerun()
            st.caption("MdN-optimized\nPredictive power focus")
            
            if st.button("🌉 Seeker Mode", use_container_width=True):
                st.session_state["lever_parity"] = "ON"
                st.session_state["pf_type"] = "Composite_70_30"
                st.session_state["fallibilism_bonus"] = "ON"
                st.session_state["bfi_debt_weight"] = "Equal_1.0x"
                st.success("✅ Seeker Mode loaded! (CT-leaning)")
                st.rerun()
            st.caption("CT-leaning\nMeaning-first")
        
        with col2:
            if st.button("🤝 Diplomat Mode", use_container_width=True):
                st.session_state["lever_parity"] = "ON"
                st.session_state["pf_type"] = "Holistic_50_50"
                st.session_state["fallibilism_bonus"] = "ON"
                st.session_state["bfi_debt_weight"] = "Equal_1.0x"
                st.success("✅ Diplomat Mode loaded! (Balanced)")
                st.rerun()
            st.caption("Balanced bridge\nEqual weighting")
            
            if st.button("⛪ Zealot Mode", use_container_width=True):
                st.session_state["lever_parity"] = "ON"
                st.session_state["pf_type"] = "Holistic_50_50"
                st.session_state["fallibilism_bonus"] = "OFF"
                st.session_state["bfi_debt_weight"] = "Equal_1.0x"
                st.success("✅ Zealot Mode loaded! (CT-optimized)")
                st.rerun()
            st.caption("CT-optimized\nExistential-first")
        
        st.markdown("---")
        st.caption("💡 **Tip:** Start with a mode, then adjust toggles manually!")
    
    st.sidebar.markdown("---")
    
    lever_parity = st.sidebar.selectbox(
        "Lever-Parity", 
        ["ON", "OFF"], 
        index=0,
        key="sidebar_lever_parity",
        help="**Parity ON:** Moral norms (MG) count equally with epistemic norms. **OFF:** Focus on predictive power. [ΔYPA: OFF typically boosts MdN ~+0.2-0.3] Because CT includes moral realism, Parity ON increases MG weighting for both frameworks."
    )
    
    pf_type = st.sidebar.selectbox(
        "PF-Type", 
        PF_TYPES, 
        index=1,
        key="sidebar_pf_type",
        help="**Instrumental:** Tech/predictive yield only. **Composite (70/30):** 70% instrumental, 30% existential. **Holistic (50/50):** Equal weight. [ΔYPA: Holistic favors CT ~+0.15-0.25] CT scores higher on existential fertility, so holistic weighting benefits CT."
    )
    
    fall_bonus = st.sidebar.selectbox(
        "Fallibilism-Bonus", 
        ["ON", "OFF"], 
        index=0,
        key="sidebar_fallibilism",
        help="**Bonus ON:** Frameworks that admit limits get +0.3 CCI boost. **OFF:** No bonus. [ΔYPA: ON benefits both MdN and CT equally ~+0.03] Both frameworks acknowledge limitations, so both receive the fallibilism bonus when enabled."
    )
    
    bfi_weight = st.sidebar.selectbox(
        "BFI Debt Weight", 
        ["Equal_1.0x", "Weighted_1.2x"], 
        index=0,
        key="sidebar_bfi_weight",
        help="**Equal (1.0x):** Debts count same as axioms. **Weighted (1.2x):** Debts cost 20% more. [ΔYPA: Weighted slightly lowers both scores ~-0.05-0.10] Higher BFI denominator reduces YPA. Both frameworks have 4 debts, so weighted impacts both similarly."
    )

    cfg = {
        "lever_parity": lever_parity,
        "pf_type": pf_type,
        "fallibilism_bonus": fall_bonus,
        "bfi_debt_weight": bfi_weight
    }

    st.sidebar.markdown("---")
    st.sidebar.markdown("**Current Config:**")
    st.sidebar.json(cfg)
    
    # Sidebar Import only
    st.sidebar.markdown("---")
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

    # FRAMEWORK EDITORS
    col1, col2 = st.columns(2)

    # FRAMEWORK A
    with col1:
        st.markdown("### 📘 Framework A")
        st.caption("✅ 98% Convergence | Adversarially Audited")
        fa_name = st.text_input("Name", MDN_DEFAULT["name"], key="fa_name")
        
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
            
            fa_axioms = st.number_input("Axioms", 1, 30, MDN_DEFAULT["bf_i"]["axioms"], key="fa_ax")
            fa_debts = st.number_input("Debts", 0, 30, MDN_DEFAULT["bf_i"]["debts"], key="fa_db")
            fa_admits = st.checkbox("Admits Limits", True, key="fa_ad")
            
            if st.button("🔍 Go to Brute Ledger", key="goto_ledger_a"):
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
        fb_name = st.text_input("Name", CT_DEFAULT["name"], key="fb_name")
        
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
            
            fb_axioms = st.number_input("Axioms", 1, 30, CT_DEFAULT["bf_i"]["axioms"], key="fb_ax")
            fb_debts = st.number_input("Debts", 0, 30, CT_DEFAULT["bf_i"]["debts"], key="fb_db")
            fb_admits = st.checkbox("Admits Limits", True, key="fb_ad")
            
            if st.button("🔍 Go to Brute Ledger", key="goto_ledger_b"):
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

    # TABS
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Visual", "📋 Details", "🛡️ Guardrails", "🔄 Symmetry"])

    with tab1:
        st.plotly_chart(create_lever_comparison_chart(ya_levers, yb_levers, fa["name"], fb["name"]), use_container_width=True)
        st.plotly_chart(create_ypa_trinity_chart(ya_results, yb_results, fa["name"], fb["name"]), use_container_width=True)

    with tab2:
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

    with tab3:
        st.caption("✨ Each guardrail tests integrity—of method and of meaning alike.")
        c1, c2 = st.columns(2)
        
        with c1:
            st.markdown(f"**{fa['name']}**")
            
            # Guardrail 1: Lever-Coupling
            ok1, msg1 = guardrail_lever_coupling(ya_levers["PF"], ya_levers["CCI"])
            st.markdown(f"**1. Lever-Coupling:** {msg1}")
            
            # Guardrail 2: BFI-Sensitivity
            ok2, msg2 = guardrail_bfi_sensitivity(
                ya_results["Neutral"]["YPA"], 
                ya_bfi,
                ya_results["Empirical"]["YPA"],
                ya_results["Existential"]["YPA"]
            )
            st.markdown(f"**2. BFI-Sensitivity:** {msg2}")
            
            # Guardrail 3: Weight-Inversion
            ok3, msg3 = guardrail_weight_inversion(ya_results, ya_results["Neutral"]["YPA"])
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
            ok1, msg1 = guardrail_lever_coupling(yb_levers["PF"], yb_levers["CCI"])
            st.markdown(f"**1. Lever-Coupling:** {msg1}")
            
            # Guardrail 2: BFI-Sensitivity
            ok2, msg2 = guardrail_bfi_sensitivity(
                yb_results["Neutral"]["YPA"], 
                yb_bfi,
                yb_results["Empirical"]["YPA"],
                yb_results["Existential"]["YPA"]
            )
            st.markdown(f"**2. BFI-Sensitivity:** {msg2}")
            
            # Guardrail 3: Weight-Inversion
            ok3, msg3 = guardrail_weight_inversion(yb_results, yb_results["Neutral"]["YPA"])
            st.markdown(f"**3. Weight-Inversion:** {msg3}")
            
            # Guardrail 4: Symmetry Audit Summary
            audit_b = symmetry_audit(fb, cfg)
            max_delta_b = max(abs(row[3]) for row in audit_b)
            if max_delta_b > 0.3:
                st.markdown(f"**4. Symmetry:** ⚠️ Max toggle sensitivity = {max_delta_b:.2f} (see Symmetry tab)")
            else:
                st.markdown(f"**4. Symmetry:** ✅ All toggles stable (max Δ = {max_delta_b:.2f})")

    with tab4:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**{fa['name']}**")
            audit = symmetry_audit(fa, cfg)
            df = pd.DataFrame(audit, columns=["Toggle", "Base", "Flip", "Delta"])
            df["Flag"] = df["Delta"].apply(lambda x: "⚠️" if abs(x) > 0.3 else "✅")
            st.dataframe(df)
        with c2:
            st.markdown(f"**{fb['name']}**")
            audit = symmetry_audit(fb, cfg)
            df = pd.DataFrame(audit, columns=["Toggle", "Base", "Flip", "Delta"])
            df["Flag"] = df["Delta"].apply(lambda x: "⚠️" if abs(x) > 0.3 else "✅")
            st.dataframe(df)
    
    # deps: preset_modes
    # NEW v4.0: EPISTEMIC QUIZ SYSTEM
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
