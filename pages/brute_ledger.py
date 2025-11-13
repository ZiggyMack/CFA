"""
CFA v4.0 - Mr. Brute's Ledger Page
"To name your brute is to pay your fee"
Comprehensive view of axioms and debts for all frameworks

NOTE: As of 2025-11-10, this page now loads axioms/debts dynamically from
profiles/worldviews/*.md via utils/profile_loader.py instead of hardcoded data.
"""

import streamlit as st
from pathlib import Path
import sys

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.profile_loader import get_brute_ledger, get_ypa_data

def _render_framework_ledger(worldview_name: str, emoji: str, subtitle: str):
    """
    Helper function to render a framework's brute ledger section dynamically from profile

    Args:
        worldview_name: Name to pass to profile_loader (e.g., "Classical Theism")
        emoji: Emoji prefix for display
        subtitle: One-line description
    """
    # Load data from profile
    try:
        ledger = get_brute_ledger(worldview_name)
        ypa_data = get_ypa_data(worldview_name)
    except Exception as e:
        st.error(f"Failed to load profile for {worldview_name}: {e}")
        return

    st.markdown(f"## {worldview_name}")
    st.markdown(f"*{subtitle}*")

    col1, col2 = st.columns(2)

    # Axioms column
    with col1:
        axiom_count = ledger["axioms"]["count"]
        st.markdown(f"### ✅ Axioms ({axiom_count})")
        st.markdown("*Unprovable starting assumptions required:*")

        for i, axiom_item in enumerate(ledger["axioms"]["list"], 1):
            name = axiom_item["name"]
            desc = axiom_item["description"]
            st.markdown(f"{i}. **{name}** - {desc}")

    # Debts column
    with col2:
        debt_count = ledger["debts"]["count"]
        st.markdown(f"### ⚠️ Debts ({debt_count})")
        st.markdown("*Unresolved questions acknowledged but not answered:*")

        for i, debt_item in enumerate(ledger["debts"]["list"], 1):
            name = debt_item["name"]
            desc = debt_item["description"]
            st.markdown(f"{i}. **{name}** - {desc}")

    st.markdown("---")

    # BFI Calculation
    st.markdown("### 📊 BFI Calculation")
    col1, col2, col3 = st.columns(3)
    bfi_total = ypa_data["bf_i"]["axioms"] + ypa_data["bf_i"]["debts"]

    with col1:
        st.metric("Axioms", str(ypa_data["bf_i"]["axioms"]))
    with col2:
        st.metric("Debts", str(ypa_data["bf_i"]["debts"]))
    with col3:
        st.metric("**BFI Total**", f"**{bfi_total}**")

    st.markdown("---")

    # Audit notes
    with st.expander("📝 Audit Notes & Justifications", expanded=False):
        # Display audit notes from profile (markdown format)
        audit_notes = ledger.get("audit_notes", "No audit notes available.")
        st.markdown(audit_notes)


def render():
    """Render the Brute Ledger page"""
    
    # Header
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown("# 🔍 Mr. Brute's Ledger")
        st.markdown("*'To name your brute is to pay your fee. To deny you have one is to summon him twice.'*")
    with col2:
        if st.button("🏠 Home"):
            st.session_state.page = 'landing'
            st.rerun()
    
    st.markdown("---")
    
    # Intro section
    st.info("""
    ### What is the Brute Ledger?
    
    Every framework rests on **unprovable assumptions** (axioms) and carries **unresolved questions** (debts).
    
    **Mr. Brute** is our accountability mechanism - a metaphor that personifies intellectual honesty:
    - When you **name an axiom** → He marks it
    - When you **justify it** → He erases the mark  
    - When you **hide it** → He marks you twice
    
    The Brute-Fact Index (BFI) = Axioms + Debts
    
    Lower BFI = More efficient framework (fewer starting assumptions)
    """)
    
    st.markdown("---")
    
    # Framework selection
    st.markdown("## 🗂️ Framework Audits")
    st.caption("*Click tabs to view complete axiom/debt lists for each audited framework*")
    
    framework_tabs = st.tabs([
        "📘 Methodological Naturalism (MdN)",
        "📕 Classical Theism (CT)",
        "🕎 Orthodox Judaism",
        "📖 Mormonism (LDS)",
        "⛔ Error Theory",
        "❓ Null Hypothesis",
        "🤔 Desiderata Believers",
        "☸️ Buddhism",
        "☪️ Islam",
        "🕉️ Hinduism",
        "🌊 Process Theology",
        "🎭 Existentialism",
        "⚡ Skeptic Mode Preset",
        "🆕 Build Custom Framework"
    ])
    
    # ========================================================================
    # METHODOLOGICAL NATURALISM
    # ========================================================================
    with framework_tabs[0]:
        _render_framework_ledger(
            worldview_name="Methodological Naturalism",
            emoji="📘",
            subtitle="Research protocol assuming testable natural causes"
        )
    
    # ========================================================================
    # CLASSICAL THEISM
    # ========================================================================
    with framework_tabs[1]:
        _render_framework_ledger(
            worldview_name="Classical Theism",
            emoji="📕",
            subtitle="God as necessary, simple, omnipotent, omniscient, omnibenevolent being"
        )

    # ========================================================================
    # ORTHODOX JUDAISM
    # ========================================================================
    with framework_tabs[2]:
        _render_framework_ledger(
            worldview_name="Orthodox Judaism",
            emoji="🕎",
            subtitle="Torah at Sinai; halakha is binding and authoritative for covenantal life"
        )

    # ========================================================================
    # MORMONISM (LDS)
    # ========================================================================
    with framework_tabs[3]:
        _render_framework_ledger(
            worldview_name="Mormonism",
            emoji="📖",
            subtitle="Continuing revelation through prophets; eternal progression toward godhood"
        )

    # ========================================================================
    # ERROR THEORY
    # ========================================================================
    with framework_tabs[4]:
        _render_framework_ledger(
            worldview_name="Error Theory",
            emoji="⛔",
            subtitle="Moral statements systematically fail; all positive moral claims are false"
        )

    # ========================================================================
    # NULL HYPOTHESIS
    # ========================================================================
    with framework_tabs[5]:
        _render_framework_ledger(
            worldview_name="Null Hypothesis",
            emoji="❓",
            subtitle="Withhold assent from all claims lacking sufficient evidence"
        )

    # ========================================================================
    # DESIDERATA BELIEVERS
    # ========================================================================
    with framework_tabs[6]:
        _render_framework_ledger(
            worldview_name="Desiderata Believers",
            emoji="🤔",
            subtitle="Pragmatic justification for belief based on beneficial outcomes"
        )

    # ========================================================================
    # BUDDHISM
    # ========================================================================
    with framework_tabs[7]:
        _render_framework_ledger(
            worldview_name="Buddhism",
            emoji="☸️",
            subtitle="Four Noble Truths; suffering arises from attachment and can be transcended"
        )

    # ========================================================================
    # ISLAM
    # ========================================================================
    with framework_tabs[8]:
        _render_framework_ledger(
            worldview_name="Islam",
            emoji="☪️",
            subtitle="Tawhid (oneness of Allah); Quran as final revelation through Prophet Muhammad"
        )

    # ========================================================================
    # HINDUISM
    # ========================================================================
    with framework_tabs[9]:
        _render_framework_ledger(
            worldview_name="Hinduism",
            emoji="🕉️",
            subtitle="Dharma, karma, and moksha; Brahman as ultimate reality"
        )

    # ========================================================================
    # PROCESS THEOLOGY
    # ========================================================================
    with framework_tabs[10]:
        _render_framework_ledger(
            worldview_name="Process Theology",
            emoji="🌊",
            subtitle="God and universe in dynamic co-creative relationship; reality as process"
        )

    # ========================================================================
    # EXISTENTIALISM
    # ========================================================================
    with framework_tabs[11]:
        _render_framework_ledger(
            worldview_name="Existentialism",
            emoji="🎭",
            subtitle="Existence precedes essence; radical freedom and responsibility"
        )

    # ========================================================================
    # SKEPTIC MODE PRESET (Grok Note #4)
    # ========================================================================
    with framework_tabs[12]:
        st.markdown("## ⚡ Skeptic Mode Preset")
        st.markdown("*Optimized configuration for empirical naturalists*")
        
        st.info("""
        **What is Skeptic Mode?**
        
        A preset configuration designed for users who prioritize:
        - Predictive power over existential meaning
        - Instrumental utility over moral grounding
        - Empirical evidence over metaphysical explanations
        
        **Configuration:**
        - **Lever-Parity:** OFF (reduces moral norm weighting)
        - **PF-Type:** Instrumental (tech/predictive yield only)
        - **Fallibilism-Bonus:** ON (rewards intellectual honesty)
        - **BFI Debt Weight:** Equal 1.0x (standard)
        
        **Result:** MdN dominates with ~4.99 YPA vs CT ~3.65 YPA
        """)
        
        st.markdown("---")
        st.markdown("### 🔬 Why This Mode?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **For Naturalist Skeptics:**
            - Shows MdN's empirical strength clearly
            - Removes existential/moral "noise"
            - Demonstrates predictive fertility advantage
            - Maintains transparency (no hidden weights)
            """)
        
        with col2:
            st.markdown("""
            **Still Fair to CT:**
            - CT's scores accurately reflect its priorities
            - CT excels in existential/moral domains
            - Switching to Holistic mode shows CT's strengths
            - No framework is "cheated" - just measured differently
            """)
        
        st.markdown("---")
        st.markdown("### 🚀 Load Skeptic Mode")
        
        if st.button("⚡ Apply Skeptic Mode to Console", use_container_width=True, type="primary"):
            # Set session state for console to pick up
            st.session_state['sidebar_lever_parity'] = "OFF"
            st.session_state['sidebar_pf_type'] = "Instrumental"
            st.session_state['sidebar_fallibilism'] = "ON"
            st.session_state['sidebar_bfi_weight'] = "Equal_1.0x"
            
            st.success("✅ Skeptic Mode applied! Navigate to Console to see results.")
            st.info("**What changed:** Parity OFF, PF-Instrumental, Fallibilism ON, BFI Weight Equal")
            
            if st.button("→ Go to Console Now"):
                st.session_state.page = 'console'
                st.rerun()
        
        st.markdown("---")
        st.caption("💡 **Tip:** After applying, compare MdN vs CT in Console to see how configuration affects scores.")
    
    # ========================================================================
    # CUSTOM FRAMEWORK
    # ========================================================================
    with framework_tabs[13]:
        st.markdown("## Build Your Own Ledger")
        
        st.markdown("""
        Want to audit your own worldview? List its axioms and debts:
        """)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ✅ Your Axioms")
            st.markdown("*What unprovable assumptions does your framework require?*")
            
            # Initialize session state for custom framework
            if 'custom_framework_name' not in st.session_state:
                st.session_state.custom_framework_name = "My Framework"
            if 'custom_axioms' not in st.session_state:
                st.session_state.custom_axioms = []
            if 'custom_debts' not in st.session_state:
                st.session_state.custom_debts = []
            
            framework_name = st.text_input("Framework Name", st.session_state.custom_framework_name, key="custom_name_input")
            st.session_state.custom_framework_name = framework_name
            
            num_axioms = st.number_input("Number of Axioms", 1, 20, max(1, len(st.session_state.custom_axioms)), key="custom_axiom_count")
            
            custom_axioms = []
            for i in range(num_axioms):
                default_val = st.session_state.custom_axioms[i] if i < len(st.session_state.custom_axioms) else ""
                axiom = st.text_input(f"Axiom {i+1}", default_val, key=f"custom_axiom_{i}", placeholder="E.g., Consciousness is fundamental")
                if axiom:
                    custom_axioms.append(axiom)
            st.session_state.custom_axioms = custom_axioms
        
        with col2:
            st.markdown("### ⚠️ Your Debts")
            st.markdown("*What questions does your framework acknowledge but not answer?*")
            
            num_debts = st.number_input("Number of Debts", 0, 20, max(0, len(st.session_state.custom_debts)), key="custom_debt_count")
            
            custom_debts = []
            for i in range(num_debts):
                default_val = st.session_state.custom_debts[i] if i < len(st.session_state.custom_debts) else ""
                debt = st.text_input(f"Debt {i+1}", default_val, key=f"custom_debt_{i}", placeholder="E.g., Why does experience exist?")
                if debt:
                    custom_debts.append(debt)
            st.session_state.custom_debts = custom_debts
        
        st.markdown("---")
        
        # Show custom BFI with Live Tracker
        st.markdown("### 📊 Your BFI (Live Tracker)")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Axioms", f"{num_axioms}")
        with col2:
            st.metric("Debts", f"{num_debts}")
        with col3:
            total_bfi = num_axioms + num_debts
            st.metric("**BFI Total**", f"**{total_bfi}**")
        
        if num_axioms + num_debts > 0:
            st.info(f"""
            **Efficiency Check**: Your BFI is {num_axioms + num_debts}.
            
            - Lower BFI = More efficient (fewer assumptions)
            - MdN's BFI: 10
            - CT's BFI: 11
            
            How does your framework compare?
            """)
        
        # Export custom framework
        st.markdown("---")
        st.markdown("### 🚀 Use This Framework")
        
        col_action1, col_action2 = st.columns(2)
        
        with col_action1:
            st.markdown("**Option 1: Load Directly**")
            
            # Let user choose which framework slot
            target_framework = st.radio(
                "Load into:",
                ["Framework A (Left)", "Framework B (Right)"],
                horizontal=True,
                key="target_framework_radio"
            )
            target_key = "framework_a" if "A" in target_framework else "framework_b"
            
            if st.button("🔄 Load into Console", key="load_to_console"):
                # Store in session state for Console to pick up
                st.session_state['custom_framework_ready'] = {
                    "name": framework_name,
                    "axioms": num_axioms,
                    "debts": num_debts,
                    "axiom_list": custom_axioms,
                    "debt_list": custom_debts,
                    "target": target_key
                }
                st.success(f"✅ '{framework_name}' ready for {target_framework}!")
                st.info("**Next:** Go to Console → Open BFI section → Click 'Apply Custom Framework'")
                
                # Optional: Auto-navigate
                if st.button("→ Go to Console Now", key="nav_to_console"):
                    st.session_state.page = 'console'
                    st.rerun()
        
        with col_action2:
            st.markdown("**Option 2: Export File**")
            if num_axioms + num_debts > 0:
                custom_framework = {
                    "name": framework_name,
                    "bf_i": {
                        "axioms": num_axioms,
                        "debts": num_debts
                    },
                    "axiom_list": custom_axioms,
                    "debt_list": custom_debts,
                    "levers": {
                        "CCI": 5.0,
                        "EDB": 5.0,
                        "PF_instrumental": 5.0,
                        "PF_existential": 5.0,
                        "AR": 5.0,
                        "MG": 5.0
                    },
                    "admits_limits": True,
                    "note": "Custom framework from Brute Ledger. Lever scores start at 5.0 (neutral)."
                }
                
                import json
                json_str = json.dumps(custom_framework, indent=2)
                st.download_button(
                    label="📥 Download JSON",
                    data=json_str,
                    file_name=f"{framework_name.replace(' ', '_')}_framework.json",
                    mime="application/json"
                )
                st.caption("*For sharing or external use*")

    
    # ========================================================================
    # FOOTER - The Pointing Rule
    # ========================================================================
    st.markdown("---")
    
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); border-radius: 1rem; border-left: 4px solid #667eea;">
        <h3 style="color: #667eea; margin-bottom: 1rem;">The Pointing Rule</h3>
        <p style="font-size: 1.2rem; font-style: italic; color: #764ba2; margin-bottom: 1rem;">
        "To name your brute is to pay your fee.<br/>
        To deny you have one is to summon him twice."
        </p>
        <p style="color: #555;">
        Every framework begins with unprovable assumptions.<br/>
        The question isn't whether you have them—it's whether you're honest about them.<br/><br/>
        <em>Mr. Brute is neither judge nor executioner—just the accountant of your assumptions.</em>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.caption("Mr. Brute's Ledger | CFA v4.0 | 'All Named, All Priced'")
