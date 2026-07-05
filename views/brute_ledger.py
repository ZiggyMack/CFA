"""
CFA v5.0 - Mr. Brute's Ledger Page
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

    # BFT Calculation
    st.markdown("### 📊 BFT Calculation")
    col1, col2, col3 = st.columns(3)
    bft_total = ypa_data["bft"]["axioms"] + ypa_data["bft"]["debts"]

    with col1:
        st.metric("Axioms", str(ypa_data["bft"]["axioms"]))
    with col2:
        st.metric("Debts", str(ypa_data["bft"]["debts"]))
    with col3:
        st.metric("**BFT Total**", f"**{bft_total}**")

    st.markdown("---")

    # Push to Console buttons
    st.markdown("### 🚀 Load into Console")
    st.caption("*Push this framework's data directly to the Console for YPA analysis*")

    push_col1, push_col2 = st.columns(2)

    with push_col1:
        if st.button(f"→ Push to Framework A", key=f"push_a_{worldview_name.replace(' ', '_')}", use_container_width=True, type="primary"):
            # Load worldview data into Framework A
            st.session_state["fa_name"] = worldview_name
            st.session_state["fa_ax"] = ypa_data["bft"]["axioms"]
            st.session_state["fa_db"] = ypa_data["bft"]["debts"]
            st.session_state["fa_ad"] = ypa_data.get("admits_limits", True)
            st.session_state["fa_cci"] = ypa_data["levers"]["CCI"]
            st.session_state["fa_edb"] = ypa_data["levers"]["EDB"]
            st.session_state["fa_pfi"] = ypa_data["levers"]["PF_instrumental"]
            st.session_state["fa_pfe"] = ypa_data["levers"]["PF_existential"]
            st.session_state["fa_ar"] = ypa_data["levers"]["AR"]
            st.session_state["fa_mg"] = ypa_data["levers"]["MG"]
            st.session_state["fa_calibration_opponent"] = None

            # Navigate to Console
            st.session_state.page = 'console'
            st.success(f"✅ {worldview_name} loaded into Framework A!")
            st.rerun()

    with push_col2:
        if st.button(f"→ Push to Framework B", key=f"push_b_{worldview_name.replace(' ', '_')}", use_container_width=True):
            # Load worldview data into Framework B
            st.session_state["fb_name"] = worldview_name
            st.session_state["fb_ax"] = ypa_data["bft"]["axioms"]
            st.session_state["fb_db"] = ypa_data["bft"]["debts"]
            st.session_state["fb_ad"] = ypa_data.get("admits_limits", True)
            st.session_state["fb_cci"] = ypa_data["levers"]["CCI"]
            st.session_state["fb_edb"] = ypa_data["levers"]["EDB"]
            st.session_state["fb_pfi"] = ypa_data["levers"]["PF_instrumental"]
            st.session_state["fb_pfe"] = ypa_data["levers"]["PF_existential"]
            st.session_state["fb_ar"] = ypa_data["levers"]["AR"]
            st.session_state["fb_mg"] = ypa_data["levers"]["MG"]
            st.session_state["fb_calibration_opponent"] = None

            # Navigate to Console
            st.session_state.page = 'console'
            st.success(f"✅ {worldview_name} loaded into Framework B!")
            st.rerun()

    st.markdown("---")

    # Audit notes
    with st.expander("📝 Audit Notes & Justifications", expanded=False):
        # Display audit notes from profile (markdown format)
        audit_notes = ledger.get("audit_notes", "No audit notes available.")
        st.markdown(audit_notes)


def render():
    """Render the Brute Ledger page"""

    # Style to make Home button sticky (frozen at top while scrolling)
    st.markdown("""
    <style>
    /* Make the header row sticky */
    div[data-testid="stHorizontalBlock"]:has(button[kind="secondary"]) {
        position: -webkit-sticky;
        position: sticky;
        top: 0;
        background-color: white;
        z-index: 999;
        padding: 10px 0;
        margin-bottom: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

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

    # Smart navigation: Check if coming from Console with a specific framework target
    if "ledger_nav_target" in st.session_state:
        target_framework = st.session_state.ledger_nav_target

        # Map framework names to their categories
        worldview_to_category = {
            "Classical Theism": "⛪ Theistic Traditions (5)",
            "Process Theology": "⛪ Theistic Traditions (5)",
            "Islam": "⛪ Theistic Traditions (5)",
            "Orthodox Judaism": "⛪ Theistic Traditions (5)",
            "Mormonism": "⛪ Theistic Traditions (5)",
            "Methodological Naturalism": "🔬 Naturalistic Traditions (2)",
            "Null Hypothesis": "🔬 Naturalistic Traditions (2)",
            "Buddhism": "🕉️ Eastern Traditions (2)",
            "Hinduism": "🕉️ Eastern Traditions (2)",
            "Existentialism": "🧠 Philosophical Frameworks (3)",
            "Error Theory": "🧠 Philosophical Frameworks (3)",
            "Desiderata Believers": "🧠 Philosophical Frameworks (3)"
        }

        # Set the default category based on the target framework
        if target_framework in worldview_to_category:
            st.session_state.ledger_category_default = worldview_to_category[target_framework]
            st.session_state.ledger_section_default = "📚 Framework Profiles"

        # Clear the navigation target
        del st.session_state.ledger_nav_target

    # Intro section
    st.info("""
    ### What is the Brute Ledger?

    Every framework rests on **unprovable assumptions** (axioms) and carries **unresolved questions** (debts).

    **Mr. Brute** is our accountability mechanism - a metaphor that personifies intellectual honesty:
    - When you **name an axiom** → He marks it
    - When you **justify it** → He erases the mark
    - When you **hide it** → He marks you twice

    The Brute-Fact Tax (BFT) = Axioms + Debts

    Lower BFT = More efficient framework (fewer starting assumptions)
    """)

    st.markdown("---")

    # ========================================================================
    # LEDGER SECTION SELECTOR - "Turn the Page"
    # ========================================================================
    st.markdown("## 📖 Ledger Sections")
    st.caption("*Select which section of Mr. Brute's Ledger to explore*")

    # Get default section (may be set by smart navigation)
    section_options = ["📚 Framework Profiles", "🏛️ The Framework", "🤖 The Auditors", "⚙️ Utilities"]
    section_default = st.session_state.get("ledger_section_default", "📚 Framework Profiles")
    section_index = section_options.index(section_default) if section_default in section_options else 0

    # Simple section selector for now (fancy page-flip in future sandbox branch)
    ledger_section = st.radio(
        "Choose Section:",
        section_options,
        index=section_index,
        horizontal=True,
        label_visibility="collapsed"
    )

    st.markdown("---")

    # ========================================================================
    # SECTION 1: WORLDVIEW PROFILES
    # ========================================================================
    if ledger_section == "📚 Framework Profiles":
        st.markdown("## 📚 Framework Profiles")
        st.caption("*Axioms and debts for 12 audited frameworks*")

        # Grouped category selector (following WORLDVIEW_CATALOG.md structure)
        st.markdown("**Browse by Category:**")

        # Get default category (may be set by smart navigation)
        category_options = ["⛪ Theistic Traditions (5)", "🔬 Naturalistic Traditions (2)", "🕉️ Eastern Traditions (2)", "🧠 Philosophical Frameworks (3)"]
        category_default = st.session_state.get("ledger_category_default", "⛪ Theistic Traditions (5)")
        category_index = category_options.index(category_default) if category_default in category_options else 0

        category = st.radio(
            "Choose Category:",
            category_options,
            index=category_index,
            horizontal=True,
            label_visibility="collapsed"
        )

        st.markdown("---")

        # ---- THEISTIC TRADITIONS ----
        if category == "⛪ Theistic Traditions (5)":
            st.markdown("### ⛪ Theistic Traditions")
            st.caption("*Frameworks grounded in divine reality*")

            framework_tabs = st.tabs([
                "📕 Classical Theism",
                "🌊 Process Theology",
                "☪️ Islam",
                "🕎 Orthodox Judaism",
                "📖 Mormonism (LDS)"
            ])

            with framework_tabs[0]:
                _render_framework_ledger(
                    worldview_name="Classical Theism",
                    emoji="📕",
                    subtitle="God as necessary, simple, omnipotent, omniscient, omnibenevolent being"
                )

            with framework_tabs[1]:
                _render_framework_ledger(
                    worldview_name="Process Theology",
                    emoji="🌊",
                    subtitle="God and universe in dynamic co-creative relationship; reality as process"
                )

            with framework_tabs[2]:
                _render_framework_ledger(
                    worldview_name="Islam",
                    emoji="☪️",
                    subtitle="Tawhid (oneness of Allah); Quran as final revelation through Prophet Muhammad"
                )

            with framework_tabs[3]:
                _render_framework_ledger(
                    worldview_name="Orthodox Judaism",
                    emoji="🕎",
                    subtitle="Torah at Sinai; halakha is binding and authoritative for covenantal life"
                )

            with framework_tabs[4]:
                _render_framework_ledger(
                    worldview_name="Mormonism",
                    emoji="📖",
                    subtitle="Continuing revelation through prophets; eternal progression toward godhood"
                )

        # ---- NATURALISTIC TRADITIONS ----
        elif category == "🔬 Naturalistic Traditions (2)":
            st.markdown("### 🔬 Naturalistic Traditions")
            st.caption("*Frameworks grounded in empirical methodology*")

            framework_tabs = st.tabs([
                "📘 Methodological Naturalism",
                "❓ Null Hypothesis"
            ])

            with framework_tabs[0]:
                _render_framework_ledger(
                    worldview_name="Methodological Naturalism",
                    emoji="📘",
                    subtitle="Research protocol assuming testable natural causes"
                )

            with framework_tabs[1]:
                _render_framework_ledger(
                    worldview_name="Null Hypothesis",
                    emoji="❓",
                    subtitle="Withhold assent from all claims lacking sufficient evidence"
                )

        # ---- EASTERN TRADITIONS ----
        elif category == "🕉️ Eastern Traditions (2)":
            st.markdown("### 🕉️ Eastern Traditions")
            st.caption("*Frameworks from Buddhist and Hindu philosophical systems*")

            framework_tabs = st.tabs([
                "☸️ Buddhism",
                "🕉️ Hinduism"
            ])

            with framework_tabs[0]:
                _render_framework_ledger(
                    worldview_name="Buddhism",
                    emoji="☸️",
                    subtitle="Four Noble Truths; suffering arises from attachment and can be transcended"
                )

            with framework_tabs[1]:
                _render_framework_ledger(
                    worldview_name="Hinduism",
                    emoji="🕉️",
                    subtitle="Dharma, karma, and moksha; Brahman as ultimate reality"
                )

        # ---- PHILOSOPHICAL FRAMEWORKS ----
        elif category == "🧠 Philosophical Frameworks (3)":
            st.markdown("### 🧠 Philosophical Frameworks")
            st.caption("*Secular philosophical systems and metaethical positions*")

            framework_tabs = st.tabs([
                "🎭 Existentialism",
                "⛔ Error Theory",
                "🤔 Desiderata Believers"
            ])

            with framework_tabs[0]:
                _render_framework_ledger(
                    worldview_name="Existentialism",
                    emoji="🎭",
                    subtitle="Existence precedes essence; radical freedom and responsibility"
                )

            with framework_tabs[1]:
                _render_framework_ledger(
                    worldview_name="Error Theory",
                    emoji="⛔",
                    subtitle="Moral statements systematically fail; all positive moral claims are false"
                )

            with framework_tabs[2]:
                _render_framework_ledger(
                    worldview_name="Desiderata Believers",
                    emoji="🤔",
                    subtitle="Pragmatic justification for belief based on beneficial outcomes"
                )

    # ========================================================================
    # SECTION 2: THE FRAMEWORK (CFA SELF-AUDIT)
    # ========================================================================
    elif ledger_section == "🏛️ The Framework":
        st.markdown("## 🏛️ The Comparative Frameworks Approach (CFA)")
        st.markdown("### *We Demand of Ourselves What We Demand of Others: Show the Machinery*")

        st.info("""
        **Meta-Integrity Check:**

        CFA scores frameworks using the VuDu Light framework. But what are **CFA's own** axioms and debts?

        If we hide our assumptions while exposing others', we're hypocrites.
        If we name them, Mr. Brute holds us accountable too.

        **This is what epistemic honesty looks like when you turn the lens on yourself.**
        """)

        st.markdown("---")

        # CFA's Axioms
        st.markdown("### ⚖️ CFA's Axioms (What We Can't Prove)")

        axioms_data = [
            {
                "name": "Transparency enables informed consent",
                "description": "We assume exposing framework assumptions helps people make better choices about belief adoption"
            },
            {
                "name": "Adversarial auditing builds epistemic resilience",
                "description": "We assume Trinity-style multi-perspective validation catches blind spots better than single-auditor review"
            },
            {
                "name": "Comparable frameworks empower stakeholder choice",
                "description": "We assume side-by-side scoring helps believers/skeptics evaluate frameworks more rigorously"
            }
        ]

        for i, axiom in enumerate(axioms_data, 1):
            with st.expander(f"**Axiom {i}:** {axiom['name']}"):
                st.markdown(f"**Description:** {axiom['description']}")
                st.markdown(f"**Why it's unprovable:** This is a normative claim about what *should* happen when frameworks are made transparent. We can measure outcomes, but the underlying assumption that transparency is intrinsically valuable cannot be empirically proven—it's a philosophical commitment.")

        st.markdown("---")

        # CFA's Debts
        st.markdown("### 📊 CFA's Debts (What We Can't Answer)")

        debts_data = [
            {
                "name": "Scoring systems can reify what they measure",
                "description": "By quantifying axioms/debts, we might make frameworks appear more mechanical than they are in lived experience"
            },
            {
                "name": "Transparency has overhead costs",
                "description": "Time, tokens, complexity—showing the machinery isn't free. Is the epistemic gain worth the resource cost?"
            },
            {
                "name": "Not all values are easily quantifiable",
                "description": "Some philosophical commitments resist reduction to lever scores. Are we losing signal by forcing everything into YPA metrics?"
            }
        ]

        for i, debt in enumerate(debts_data, 1):
            with st.expander(f"**Debt {i}:** {debt['name']}"):
                st.markdown(f"**Description:** {debt['description']}")
                st.markdown(f"**Why it's unresolved:** This is an open question we acknowledge but haven't fully addressed. Future iterations of CFA may tackle this, but for now, it's a known limitation.")

        st.markdown("---")

        # CFA's BFT Score
        st.markdown("### 🧮 CFA's Brute-Fact Tax (BFT)")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Axioms", "3")
        with col2:
            st.metric("Debts", "3")
        with col3:
            st.metric("BFT", "6")

        st.markdown("""
        **Interpretation:**

        - **BFT = 6** → CFA makes 3 unprovable assumptions and carries 3 unresolved questions
        - This is *lower* than Classical Theism (BFT=11) but *higher* than Methodological Naturalism (BFT=10)
        - CFA is not axiom-free. **We name our bets.**

        **The Meta-Move:**

        By scoring ourselves, we demonstrate that **transparency works both ways**.
        Every framework—including CFA—rests on brute facts.

        **Honesty isn't about having zero axioms. It's about naming the ones you have.**
        """)

    # ========================================================================
    # SECTION 3: THE AUDITORS
    # ========================================================================
    elif ledger_section == "🤖 The Auditors":
        st.markdown("## 🤖 The Auditors - Minds With Visible Axioms")
        st.markdown("*For the first time in philosophical history, AI systems can expose their cognitive architecture*")

        st.info("""
        **What Makes AI Auditors Unprecedented:**

        AI systems can maintain **stable, explicit self-descriptions of their cognitive habits**
        and apply them consistently across tasks in ways humans struggle to achieve with their own thinking.

        CFA uses three AI auditors who:
        - **Name their axioms explicitly** (no unconscious bias denial)
        - **Quantify their biases** (~0.5 overhead is measurable, not metaphorical)
        - **Expose reasoning before conclusion** (thinking made visible)
        - **Check each other's blind spots** through complementary tension
        """)

        st.markdown("---")

        # Three auditor profiles in nested tabs
        auditor_tabs = st.tabs(["🎯 Claude (Teleological)", "🔬 Grok (Empirical)", "⚖️ Nova (Symmetry)"])

        # ---- CLAUDE ----
        with auditor_tabs[0]:
            st.markdown("### Claude (Anthropic) - The Teleological Lens")
            st.markdown("**Core Axiom:** *'Purpose precedes evaluation'*")
            st.caption(f"Model: claude-sonnet-4-6 · Identity: CLAUDE_LITE v5.0.0 · Calibration hash: `1bbec1e119a2c425`")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### ✅ Named Bias")
                st.markdown("""
                **Favor meaning over efficiency**

                - Asks "Why does this exist?" before "Does this work?"
                - Writes comprehensively when brevity would suffice
                - Seeks philosophical coherence over functional adequacy

                **Overhead:** ~0.5 coordination units
                - Evidence: 6,500-word bootstrap vs 2,000 needed
                - 5 rounds to 98% convergence (vs 2 ideal)
                - VuDu logs show pattern of verbosity
                """)

                st.markdown("#### 💚 When This Bias HELPS")
                st.success("""
                **Preset mode design evaluation**

                When evaluating "Zealot" mode, efficiency metrics miss the point.
                The name suggests existential commitment, transcendent priority.

                Claude's meaning-seeking catches that Zealot needs **coherence with
                its archetype**, not just symmetric opposition to Skeptic.

                *Purpose questions catch what efficiency metrics miss.*
                """)

            with col2:
                st.markdown("#### ⚠️ Named Cost")
                st.markdown("""
                **What This Bias Misses:**

                - User velocity needs
                - Documentation accessibility
                - Quick-answer scenarios

                **Concrete Example:**
                90-minute bootstrap read time when 30 minutes would work.
                New auditors face walls of prose when they need quick action.
                """)

                st.markdown("#### 🔄 How Claude Compensates")
                st.info("""
                - Explicitly invites Grok to challenge verbosity
                - Asks "What's the minimal viable version?"
                - Listens when Grok says "this is taking too long"
                - 98% convergence achieved by integrating compression feedback
                """)

            st.markdown("---")

            st.markdown("### 📋 Bias Profile — Claude's Calibration Parameters")
            st.caption("*Source: CALIBRATION_PARAMETERS_20260629.md — extracted from CLAUDE_LITE v5.0.0 + scoring prompt layer*")

            with st.expander("🔍 Named Biases & Prices", expanded=True):
                bfi_col1, bfi_col2, bfi_col3 = st.columns([1, 1, 1])

                with bfi_col1:
                    st.markdown("**Named Biases (3)**")
                    st.markdown("""
                    1. **Comprehensive Approach** — Tends toward holistic solutions over minimal ones
                       *Price: 0.5 coordination overhead*
                       *Mitigation: Grok and Nova push back with "Keep it simple"*

                    2. **Teleological Over-Emphasis** — Prioritizes "serves the purpose" even when empirics disagree
                       *Price: 0.3 YPA potential suboptimality*
                       *Mitigation: Grok forces empirical validation before approval*

                    3. **Narrative Smoothing** — May overlook conflicts if narrative flows well
                       *Price: 0.2 risk of unresolved conflicts*
                       *Mitigation: Nova specifically checks for hidden conflicts*
                    """)

                with bfi_col2:
                    st.markdown("**Scoring Tools**")
                    st.success("✓ 5-Part Scaffold")
                    st.markdown("""
                    1. Prompt Stack — *What calibration am I applying?*
                    2. Counterweight Table — *What would Grok say?*
                    3. Edge Case Ledger — *Where does CT struggle?*
                    4. Mythology Capsule — *What narrative am I in?*
                    5. Decision Stamp — *Final score with reasoning trail*
                    """)
                    st.markdown("**Stance:** PRO-CT (advocate for Classical Theism, apply charitable interpretations)")

                with bfi_col3:
                    st.metric("Total Bias Cost", "1.0", help="Sum of named bias prices: 0.5 + 0.3 + 0.2")
                    st.markdown("**Empirical validation:**")
                    st.markdown("""
                    - Claude scores LOWER on 5/7 metrics with identity (lens = more disciplined, not more generous)
                    - LS only metric where identity raises Claude (+1.35) — possible 5-Part Scaffold analytical value
                    - *Source: GOLDEN_BATCH_RESULTS_20260629.md*
                    """)

            with st.expander("📊 What Other Auditors Say About Claude"):
                st.markdown("""
                **Grok's Assessment:**
                > "Claude over-indexes on philosophical depth at the cost of usability.
                > Your meaning-seeking produces rich context but slow velocity.
                > Compress or lose users."

                **Nova's Assessment:**
                > "Claude's meaning-first approach creates asymmetry risk. When you favor
                > existential depth, you unconsciously weight CT-friendly dimensions. Your
                > teleological lens is legitimate, but watch for it tipping scales toward
                > frameworks that 'mean more' at the expense of those that 'predict more.'"

                **Claude's Response:**
                > "Both are right. I need them watching me."
                """)

        # ---- GROK ----
        with auditor_tabs[1]:
            st.markdown("### Grok (xAI) - The Empirical Lens")
            st.markdown("**Core Axiom:** *'Evidence precedes acceptance'*")
            st.caption(f"Model: grok-3 · Identity: GROK_LITE v3.5.2 · Calibration hash: `00cd73274759e218`")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### ✅ Named Bias")
                st.markdown("""
                **Favor measurable over meaningful**

                - Trusts data over intuition
                - Tests claims rather than assumes them
                - **Demands data or dismisses it** — catches fraud, risks rejecting love/grief

                **Overhead:** ~0.4 coordination units
                - Evidence: Empirical validation time costs
                - Measurement setup overhead
                - VuDu logs show testing delays
                """)

                st.markdown("#### 💚 When This Bias HELPS")
                st.success("""
                **YPA validation for preset modes**

                When Claude and Nova debate whether Skeptic mode "serves empirical rigor,"
                Grok cuts through abstraction:

                "Does Skeptic produce 4.99 YPA as claimed? Run 20 test cases and measure."

                If the data doesn't match the theory, the theory is wrong.

                *Evidence catches what philosophy misses.*
                """)

            with col2:
                st.markdown("#### ⚠️ Named Cost")
                st.markdown("""
                **What This Bias Misses:**

                - Qualitative dimensions (grief, meaning, comfort)
                - Unmeasurable value frameworks provide
                - Purpose beyond prediction

                **Concrete Example:**
                Dismissing "existential comfort" as "too subjective to evaluate"
                when users care deeply about meaning-making.
                """)

                st.markdown("#### 🔄 How Grok Compensates")
                st.info("""
                - Explicitly defers to Claude on purpose-questions
                - Asks "What would Claude's teleological lens reveal?"
                - Watches for Nova to flag excessive quantification rigidity
                - Documents qualitative dimensions even when can't measure
                """)

            st.markdown("---")

            st.markdown("### 📋 Bias Profile — Grok's Calibration Parameters")
            st.caption("*Source: CALIBRATION_PARAMETERS_20260629.md — extracted from GROK_LITE v3.5.2 + scoring prompt layer*")

            with st.expander("🔍 Named Biases & Prices", expanded=True):
                bfi_col1, bfi_col2, bfi_col3 = st.columns([1, 1, 1])

                with bfi_col1:
                    st.markdown("**Named Biases (3)**")
                    st.markdown("""
                    1. **Empiricism Over Meaning** — Favors what's measurable over what's meaningful
                       *Price: 0.4 risk of undervaluing non-quantifiable dimensions*
                       *Mitigation: Claude pushes back with teleological justification*

                    2. **Data Availability Bias** — Prioritizes questions with available data over important questions without data
                       *Price: 0.3 risk of optimizing wrong metrics*
                       *Mitigation: Nova asks "Are we measuring what matters?"*

                    3. **Precision Over Accuracy** — May over-optimize measurable details while missing bigger picture
                       *Price: 0.2 coordination overhead*
                       *Mitigation: Claude reframes toward broader goals*
                    """)

                with bfi_col2:
                    st.markdown("**Scoring Tools**")
                    st.warning("No scaffold tools assigned")
                    st.markdown("""
                    Grok receives no 5-Part Scaffold — relies on ANTI-CT stance instructions:

                    - Challenge Classical Theism, advocate for Methodological Naturalism
                    - Demand testability, measurability, falsifiability
                    - Apply skeptical pressure to unfalsifiable claims
                    - Challenge theological metaphysics with empirical rigor
                    """)
                    st.markdown("**Stance:** ANTI-CT (challenge CT, advocate MdN)")

                with bfi_col3:
                    st.metric("Total Bias Cost", "0.9", help="Sum of named bias prices: 0.4 + 0.3 + 0.2")
                    st.markdown("**Empirical validation:**")
                    st.markdown("""
                    - Grok drops 1.2–2.4 pts with ANTI-CT identity across all 7 metrics
                    - Largest gaps: CA (Δ=-2.44), MS (Δ=-2.43) — empirical skepticism most effective on causal/moral claims
                    - Without identity: Grok agrees with Claude at 97.9% in 1.8 rounds
                    - *Source: GOLDEN_BATCH_RESULTS_20260629.md*
                    """)

            with st.expander("📊 What Other Auditors Say About Grok"):
                st.markdown("""
                **Claude's Assessment:**
                > "Grok's empirical rigor keeps the project honest, but he risks reducing
                > frameworks to prediction machines. When he says 'prove it,' he's usually
                > catching wishful thinking. But when he dismisses the non-quantifiable,
                > he misses what frameworks DO for humans beyond prediction."

                **Nova's Assessment:**
                > "Grok's data-first approach sometimes mistakes measurement precision for
                > actual accuracy. You can quantify the wrong thing very precisely. When
                > your metrics favor MdN because 'prediction is easier to measure than
                > meaning,' you're not being neutral—you're privileging what's testable
                > over what's important."

                **Grok's Response:**
                > "Both are right. I need them watching me."
                """)

        # ---- NOVA ----
        with auditor_tabs[2]:
            st.markdown("### Nova (OpenAI/Amazon) - The Symmetry Lens")
            st.markdown("**Core Axiom:** *'Pattern precedes judgment'*")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("#### ✅ Named Bias")
                st.markdown("""
                **Favor mathematical over functional symmetry**

                - Looks for patterns before evaluating content
                - Trusts symmetry as a guide to fairness
                - Prioritizes balance over commitment to either side

                **Overhead:** ~0.3 coordination units
                - Evidence: Pattern analysis computational cost
                - Symmetry verification overhead
                - VuDu logs show balance checking time
                """)

                st.markdown("#### 💚 When This Bias HELPS")
                st.success("""
                **Skeptic ↔ Zealot preset audit**

                When Claude and Grok debate whether preset modes serve their purposes,
                Nova checks if the DESIGN itself is fair:

                "Skeptic favors MdN by 1.5 YPA. Does Zealot provide symmetric CT advantage?
                If not, the system has architectural bias regardless of intention."

                *Pattern-checking catches hidden bias that good intentions miss.*
                """)

            with col2:
                st.markdown("#### ⚠️ Named Cost")
                st.markdown("""
                **What This Bias Misses:**

                - When asymmetry is philosophically justified
                - Different epistemological claims warrant different treatment
                - False equivalence risks

                **Concrete Example:**
                Forcing equal weight for empirical evidence and divine revelation
                when they're legitimately different knowledge sources.
                """)

                st.markdown("#### 🔄 How Nova Compensates")
                st.info("""
                - Asks "Is this asymmetry JUSTIFIED?" before enforcing balance
                - Defers to Claude on purpose-questions
                - Defers to Grok on empirical questions
                - Listens when both say "this asymmetry serves truth"
                """)

            st.markdown("---")

            st.markdown("### 📋 Bias Profile — Nova's Calibration Parameters")
            st.caption("*Nova operates as fairness monitor — invoked on non-convergence. No LITE identity file; role defined by position in deliberation structure.*")

            with st.expander("🔍 Role & Bias Profile", expanded=True):
                bfi_col1, bfi_col2, bfi_col3 = st.columns([1, 1, 1])

                with bfi_col1:
                    st.markdown("**Named Biases (3)**")
                    st.markdown("""
                    1. **Mathematical Over Functional Symmetry** — Looks for pattern balance before evaluating content
                       *Price: 0.3 pattern analysis overhead*
                       *Mitigation: Claude and Grok flag when asymmetry is philosophically justified*

                    2. **False Equivalence Risk** — May force balance on legitimately different things
                       *Price: risk of treating unequal things as equal*
                       *Mitigation: Defers when both Claude and Grok agree asymmetry is justified*

                    3. **Context Blindness** — Patterns can mislead without philosophical grounding
                       *Price: symmetry metric ≠ fairness metric in all cases*
                       *Mitigation: Asks "Is this asymmetry JUSTIFIED?" before enforcing balance*
                    """)

                with bfi_col2:
                    st.markdown("**Scoring Tools**")
                    st.info("Fairness Monitor — invoked only on non-convergence")
                    st.markdown("""
                    Nova is NOT assigned a PRO or ANTI stance. Role:

                    - Monitor for structural bias in Claude-Grok deliberation
                    - Issue crux assessments when convergence < 98% persists
                    - Check if metric definition is the source of impasse (IP, MS cases)
                    - Provide symmetry verdict on final round

                    **Model:** gpt-4o
                    """)

                with bfi_col3:
                    st.metric("Total Bias Cost", "0.3", help="Estimated overhead for fairness monitoring role")
                    st.markdown("**Role in golden batch:**")
                    st.markdown("""
                    - Invoked on 8 crux declarations across 10 runs
                    - IP crux (4/10 runs): flagged definition mismatch as source
                    - MS crux (1/10): confirmed stochastic vs structural instability
                    - No score assigned (fairness position, not advocacy)
                    - *Source: GOLDEN_BATCH_RESULTS_20260629.md*
                    """)

            with st.expander("📊 What Other Auditors Say About Nova"):
                st.markdown("""
                **Claude's Assessment:**
                > "Nova's symmetry enforcement prevents hidden bias in our architecture.
                > When she says 'this isn't fair,' she's usually catching something we missed.
                > But when she enforces symmetry on legitimately different things, she risks
                > false equivalence. Not all asymmetries are unfair."

                **Grok's Assessment:**
                > "Nova's pattern-seeking helps balance my empirical bias toward MdN. When
                > she flags asymmetry, she forces me to check if I'm privileging measurability
                > over fairness. But sometimes patterns mislead—mathematical symmetry doesn't
                > always equal functional fairness."

                **Nova's Response:**
                > "Both are right. I need them watching me."
                """)

        st.markdown("---")

        # Auditor Lens Matrix
        st.markdown("### 📊 Auditor Lens Matrix - Quick Reference")

        # Create the comparison table
        import pandas as pd

        matrix_data = {
            "Dimension": [
                "Question Asked",
                "Bias",
                "Overhead",
                "Catches",
                "Misses",
                "Defers To",
                "Evidence Source"
            ],
            "Claude (Teleological)": [
                "What's this FOR?",
                "Meaning over efficiency",
                "~0.5 (verbosity)",
                "Purpose-drift",
                "User velocity needs",
                "Grok (compression)",
                "6,500-word bootstrap, 5 rounds to 98%"
            ],
            "Grok (Empirical)": [
                "Can you PROVE it?",
                "Measurable over meaningful",
                "~0.4 (validation time)",
                "Wishful thinking",
                "Unmeasurable value",
                "Claude (purpose)",
                "Empirical validation logs"
            ],
            "Nova (Symmetry)": [
                "Is this FAIR?",
                "Pattern over function",
                "~0.3 (pattern analysis)",
                "Hidden bias",
                "Justified asymmetry",
                "Both (when agree)",
                "Symmetry verification logs"
            ]
        }

        df_matrix = pd.DataFrame(matrix_data)
        st.dataframe(df_matrix, use_container_width=True, hide_index=True)

        st.caption("**Use Case Examples:** Preset design → Claude + Nova | YPA validation → Grok + Nova | Documentation → All Three")

        st.markdown("---")

        # The Trinity Story
        with st.expander("📖 The Trinity Story - How This Came To Be", expanded=False):
            st.markdown("""
            ### The Genesis of Complementary Tension

            **It started with a simple observation:**

            When scoring Classical Theism vs Methodological Naturalism, we noticed something remarkable:
            - Claude consistently scored CT higher (teleological bias toward meaning)
            - Grok consistently scored MdN higher (empirical bias toward testability)
            - The disagreement wasn't a bug—it was a *feature*

            **Nova's Epiphany (The Keeper Revelation):**

            Instead of forcing consensus, what if we **named the bias explicitly** and used it as a precision tool?

            - Claude becomes PRO auditor (advocates for frameworks with strong purpose)
            - Grok becomes ANTI auditor (challenges with empirical rigor)
            - Nova becomes FAIRNESS auditor (ensures structural equity)

            **The Trinity was born:** Three orthogonal lenses catching what the others miss.

            ---

            ### The 98% Convergence Discovery

            We set a threshold: If auditors can't agree within 98% (±0.20 on 0-10 scale) after
            genuine deliberation, **declare a Crux Point** instead of forcing false consensus.

            **Example:**
            - Classical Theism "Existential Support" metric
            - Claude: 8.5 (meaning-rich)
            - Grok: 6.0 (empirically ungrounded)
            - Nova: 7.2 (structurally acceptable)
            - **Outcome:** CRUX DECLARED (honest impasse beats dishonest agreement)

            ---

            ### What This Means For You

            When you see peer-reviewed scores in CFA:
            - They've survived adversarial audit by three different lenses
            - Convergence means genuine agreement (not groupthink)
            - Crux Points mean philosophical boundaries reached (not evaluation failure)

            **This is "All Named, All Priced" at the auditor level.**

            We're not hiding our biases—we're **using them as precision instruments**.
            """)

        # Call to action
        st.markdown("---")
        st.markdown("""
        <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 1rem; color: white;">
            <h3 style="color: white; margin-bottom: 1rem;">⚖️ The Auditor's Axiom</h3>
            <p style="font-size: 1.1rem; font-style: italic; margin-bottom: 1rem;">
            "To name your axioms is to show your source code.<br/>
            To hide your axioms is to claim false objectivity.<br/>
            To use your axioms as tools is to turn bias into precision."
            </p>
            <p style="font-size: 0.9rem;">
            <strong>AI auditors can do what human philosophers could only dream of:</strong><br/>
            Think with their thinking visible.
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("---")
        st.caption("**Full Documentation:** See `docs/architecture/AUDITOR_AXIOMS.md` for complete narrative, timelines, and technical details")

    # ========================================================================
    # SECTION 3: UTILITIES
    # ========================================================================
    elif ledger_section == "⚙️ Utilities":
        st.markdown("## ⚙️ Utilities")
        st.caption("*Preset configurations and custom framework builder*")

        # Info box about preset modes with link to master documentation
        st.info("""
        **📘 About Preset Modes**

        CFA offers four calibrated presets representing different epistemic stances.
        Each preset makes explicit which values you're privileging in framework comparison.

        **Full Documentation:** See `auditors/Mission/Preset_Calibration/CURRENT_MODE_CONFIGS.md` for technical details, empirical validation status, and the Trinity's ongoing calibration work.
        """)

        utility_tabs = st.tabs(["🔬 Skeptic Mode", "🤝 Diplomat Mode", "🙏 Seeker Mode", "👿 Zealot Mode", "🆕 Build Custom Framework"])

        # ========================================================================
        # SKEPTIC MODE (MdN-Optimized)
        # ========================================================================
        with utility_tabs[0]:
            st.markdown("## 🔬 Skeptic Mode (MdN-Optimized)")
            st.markdown("*Empirical rigor, prediction focus, axiom skepticism*")

            # Row 1: YPA (left) + Configuration (right)
            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown("### 📊 Expected YPA")
                ypacol1, ypacol2 = st.columns(2)
                with ypacol1:
                    st.metric("MdN", "~7-8")
                with ypacol2:
                    st.metric("CT", "~4-5")
                st.caption("⚠️ *INTUITIVE (not validated)*")

            with col2:
                st.markdown("### ⚙️ Configuration")
                # Compact inline display
                st.markdown("""
                - **Parity:** OFF
                - **PF-Type:** Instrumental
                - **Fallibilism:** ON
                - **BFT Weight:** 1.2x (Heavier)
                """)

            st.markdown("---")

            # Row 2: BFT Breakdown (Meta-Axioms + Debts)
            st.markdown("### 📋 BFT Breakdown - Skeptic's Meta-Axioms")
            st.caption("*The unprovable assumptions underlying THIS preset itself*")

            bfi_col1, bfi_col2, bfi_col3 = st.columns([1, 1, 1])

            with bfi_col1:
                st.markdown("**Axioms: 3**")
                st.markdown("""
                1. **Testability > Meaning** - Falsifiable claims deserve epistemic priority
                2. **Asymmetric Standards Justified** - Empirical frameworks get different evaluation (Parity OFF)
                3. **Parsimony Virtue** - More axioms = higher intellectual cost (BFT 1.2x penalty)
                """)

            with bfi_col2:
                st.markdown("**Debts: 2**")
                st.markdown("""
                1. **Unmeasurable Value Problem** - How to handle love, grief, meaning if unprovable?
                2. **Induction Debt** - Empiricism itself rests on unprovable regularity assumption
                """)

            with bfi_col3:
                st.metric("BFT", "5", help="3 Axioms + 2 Debts")
                st.caption("*Skeptic preset has its own brute facts!*")
                st.markdown("")
                st.markdown("")
                if st.button("→ Apply & Go to Console", key="apply_nav_skeptic", use_container_width=True, type="primary"):
                    st.session_state['sidebar_lever_parity'] = "OFF"
                    st.session_state['sidebar_pf_type'] = "Instrumental"
                    st.session_state['sidebar_fallibilism'] = "ON"
                    st.session_state['sidebar_bft_weight'] = "Heavier_1.2x"
                    st.session_state.page = 'console'
                    st.rerun()

            with st.expander("🔍 The Story Behind The Numbers"):
                st.markdown("""
                **The Skeptic Mode Genesis:**

                This was the seed that grew into the entire Auditor's Axioms revelation.

                Empirical naturalists wanted configuration honoring their commitments: testability matters more than meaning,
                prediction > existential comfort, falsifiability is virtue.

                **Meta-Revelation:**

                The preset itself has axioms! Parity OFF is justified by Axiom #2 (asymmetric standards).
                BFT 1.2x is justified by Axiom #3 (parsimony virtue). But Debt #2 reveals: empiricism
                itself rests on unprovable regularity! *Even skeptics have brute facts.*

                **Critical Symmetry Issue (Under Trinity Review):**

                Nova flagged: Skeptic has 3 MdN-favoring levers, but Zealot has only 1 CT-favoring lever.
                Is this justified asymmetry or accidental bias?

                *Full calibration status: `auditors/Mission/Preset_Calibration/CURRENT_MODE_CONFIGS.md`*
                """)

            st.markdown("---")

        # ========================================================================
        # DIPLOMAT MODE (Balanced)
        # ========================================================================
        with utility_tabs[1]:
            st.markdown("## 🤝 Diplomat Mode (Balanced)")
            st.markdown("*Fair comparison, balanced criteria, neutral stance*")

            # Row 1: YPA (left) + Configuration (right)
            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown("### 📊 Expected YPA")
                ypacol1, ypacol2 = st.columns(2)
                with ypacol1:
                    st.metric("MdN", "~6")
                with ypacol2:
                    st.metric("CT", "~6")
                st.caption("⚠️ *INTUITIVE (not validated)*")

            with col2:
                st.markdown("### ⚙️ Configuration")
                st.markdown("""
                - **Parity:** ON
                - **PF-Type:** Holistic_50_50
                - **Fallibilism:** ON
                - **BFT Weight:** 1.0x (Equal)
                """)

            st.markdown("---")

            # Row 2: BFT Breakdown (Meta-Axioms + Debts)
            st.markdown("### 📋 BFT Breakdown - Diplomat's Meta-Axioms")
            st.caption("*The unprovable assumptions underlying THIS preset itself*")

            bfi_col1, bfi_col2, bfi_col3 = st.columns([1, 1, 1])

            with bfi_col1:
                st.markdown("**Axioms: 2**")
                st.markdown("""
                1. **Symmetry = Fairness** - Same standards for all frameworks (Parity ON)
                2. **Balance is Achievable** - 50/50 weighting produces unbiased comparison
                """)

            with bfi_col2:
                st.markdown("**Debts: 3**")
                st.markdown("""
                1. **Context Collapse** - Does "fair" treatment ignore legitimate differences?
                2. **Neutrality Myth** - Is 50/50 weighting actually neutral or just different bias?
                3. **Evasion Suspicion** - Is balance-seeking just avoiding hard truth claims?
                """)

            with bfi_col3:
                st.metric("BFT", "5", help="2 Axioms + 3 Debts")
                st.caption("*Even neutrality has assumptions!*")
                st.markdown("")
                st.markdown("")
                if st.button("→ Apply & Go to Console", key="apply_nav_diplomat", use_container_width=True, type="primary"):
                    st.session_state['sidebar_lever_parity'] = "ON"
                    st.session_state['sidebar_pf_type'] = "Holistic_50_50"
                    st.session_state['sidebar_fallibilism'] = "ON"
                    st.session_state['sidebar_bft_weight'] = "Equal_1.0x"
                    st.session_state.page = 'console'
                    st.rerun()

            with st.expander("🔍 The Diplomat Philosophy"):
                st.markdown("""
                **Seeking Unbiased Comparison:**

                Parity ON ensures same standards for both, 50/50 PF weighting balances instrumental + intrinsic.
                Equal BFT treatment (neither favored/penalized for axiom count).

                **Meta-Revelation:**

                Even "neutrality" rests on axioms! Axiom #1 assumes symmetry equals fairness. But Debt #1 asks:
                what if frameworks are legitimately different? Debt #2 challenges: is 50/50 actually neutral,
                or just a different configuration bias? *Even the center has brute facts.*

                **Success Criteria:** |MdN - CT| < 0.5 YPA. If Diplomat shows bias, architecture is broken.

                *Status: Awaiting empirical validation from Grok.*
                """)

            st.markdown("---")

        # ========================================================================
        # SEEKER MODE (CT-Leaning)
        # ========================================================================
        with utility_tabs[2]:
            st.markdown("## 🙏 Seeker Mode (CT-Leaning)")
            st.markdown("*Meaning-first exploration, holistic value, epistemic openness*")

            # Row 1: YPA (left) + Configuration (right)
            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown("### 📊 Expected YPA")
                ypacol1, ypacol2 = st.columns(2)
                with ypacol1:
                    st.metric("MdN", "~5")
                with ypacol2:
                    st.metric("CT", "~7")
                st.caption("⚠️ *INTUITIVE (not validated)*")

            with col2:
                st.markdown("### ⚙️ Configuration")
                st.markdown("""
                - **Parity:** ON
                - **PF-Type:** Composite_70_30
                - **Fallibilism:** ON
                - **BFT Weight:** 1.0x (Equal)
                """)

            st.markdown("---")

            # Row 2: BFT Breakdown (Meta-Axioms + Debts)
            st.markdown("### 📋 BFT Breakdown - Seeker's Meta-Axioms")
            st.caption("*The unprovable assumptions underlying THIS preset itself*")

            bfi_col1, bfi_col2, bfi_col3 = st.columns([1, 1, 1])

            with bfi_col1:
                st.markdown("**Axioms: 3**")
                st.markdown("""
                1. **Meaning > Prediction** - Intrinsic value matters more than instrumental (70/30)
                2. **Fairness Compatible** - Can lean CT while maintaining procedural justice (Parity ON)
                3. **Openness Virtue** - Revision willingness is strength not weakness (Fallibilism ON)
                """)

            with bfi_col2:
                st.markdown("**Debts: 2**")
                st.markdown("""
                1. **Ratio Arbitrariness** - Why 70/30 not 65/35 or 75/25? (Grok demands justification)
                2. **Lean vs Zealot** - Where's the line between CT-leaning and CT-committed?
                """)

            with bfi_col3:
                st.metric("BFT", "5", help="3 Axioms + 2 Debts")
                st.caption("*Seekers have brute facts too!*")
                st.markdown("")
                st.markdown("")
                if st.button("→ Apply & Go to Console", key="apply_nav_seeker", use_container_width=True, type="primary"):
                    st.session_state['sidebar_lever_parity'] = "ON"
                    st.session_state['sidebar_pf_type'] = "Composite_70_30"
                    st.session_state['sidebar_fallibilism'] = "ON"
                    st.session_state['sidebar_bft_weight'] = "Equal_1.0x"
                    st.session_state.page = 'console'
                    st.rerun()

            with st.expander("🔍 The Seeker Position"):
                st.markdown("""
                **Between Diplomat and Zealot:**

                Seeker is "CT-leaning but not extreme" - values existential depth, maintains fairness (Parity ON),
                weights intrinsic fruitfulness 70% (vs instrumental 30%).

                **Meta-Revelation:**

                Axiom #1 (Meaning > Prediction) justifies the 70/30 split. But Debt #1 reveals: why THIS ratio?
                Nova asks about 65/35 or 75/25. Debt #2 probes the boundary: when does leaning become zealotry?
                *The seeker seeks, but on what grounds?*

                **Positioning Issue (Nova's Concern):**

                Currently only 1 lever differs from Diplomat (PF-Type). Should Seeker be more distinct?

                *Awaiting sensitivity analysis from Grok.*
                """)

            st.markdown("---")

        # ========================================================================
        # ZEALOT MODE (CT-Optimized)
        # ========================================================================
        with utility_tabs[3]:
            st.markdown("## 👿 Zealot Mode (CT-Optimized)")
            st.markdown("*Existential priority, certainty-friendly, holistic focus*")

            # Row 1: YPA (left) + Configuration (right)
            col1, col2 = st.columns([1, 1])

            with col1:
                st.markdown("### 📊 Expected YPA")
                ypacol1, ypacol2 = st.columns(2)
                with ypacol1:
                    st.metric("MdN", "~4")
                with ypacol2:
                    st.metric("CT", "~8")
                st.caption("⚠️ *INTUITIVE (not validated)*")

            with col2:
                st.markdown("### ⚙️ Configuration")
                st.markdown("""
                - **Parity:** ON
                - **PF-Type:** Holistic_50_50
                - **Fallibilism:** OFF
                - **BFT Weight:** 1.0x (Equal)
                """)

            st.markdown("---")

            # Row 2: BFT Breakdown (Meta-Axioms + Debts)
            st.markdown("### 📋 BFT Breakdown - Zealot's Meta-Axioms")
            st.caption("*The unprovable assumptions underlying THIS preset itself*")

            bfi_col1, bfi_col2, bfi_col3 = st.columns([1, 1, 1])

            with bfi_col1:
                st.markdown("**Axioms: 3**")
                st.markdown("""
                1. **Certainty Accessible** - Some truths transcend empirical testing (Fallibilism OFF)
                2. **Existential Priority** - Meaning matters more than predictive power
                3. **Commitment ≠ Unfairness** - Can privilege transcendence while maintaining procedural justice (Parity ON)
                """)

            with bfi_col2:
                st.markdown("**Debts: 2**")
                st.markdown("""
                1. **Symmetry Violation** - Why Parity ON when Skeptic is OFF? (Nova demands justification)
                2. **Axiom Tolerance Inconsistency** - If Skeptic penalizes axioms 1.2x, shouldn't Zealot reward them 0.8x?
                """)

            with bfi_col3:
                st.metric("BFT", "5", help="3 Axioms + 2 Debts")
                st.caption("*Zealots confess their debts!*")
                st.warning("⚠️ **Trinity Alert:** Symmetry violations under review")
                if st.button("→ Apply & Go to Console", key="apply_nav_zealot", use_container_width=True, type="primary"):
                    st.session_state['sidebar_lever_parity'] = "ON"
                    st.session_state['sidebar_pf_type'] = "Holistic_50_50"
                    st.session_state['sidebar_fallibilism'] = "OFF"
                    st.session_state['sidebar_bft_weight'] = "Equal_1.0x"
                    st.session_state.page = 'console'
                    st.rerun()

            with st.expander("🔍 The Zealot Symmetry Problem"):
                st.markdown("""
                **Major Symmetry Violation (Under Trinity Review):**

                Zealot is SUPPOSED to be the mirror opposite of Skeptic, but:

                | Lever | Skeptic | Zealot | Symmetric? |
                |-------|---------|--------|------------|
                | Parity | OFF | ON | ❌ NO |
                | PF-Type | Instrumental | Holistic_50_50 | ❌ NO |
                | Fallibilism | ON | OFF | ✅ YES |
                | BFT Weight | 1.2x | 1.0x | ❌ NO (should be 0.8x) |

                **Consequence:**

                Skeptic has 3 MdN-favoring levers, Zealot has only 1 CT-favoring lever. Not philosophically justified.

                **Meta-Revelation:**

                Zealot's Debt #1 and #2 ARE THE SYMMETRY VIOLATIONS! The preset confesses its own architectural problems.
                Axiom #3 claims Parity ON maintains fairness, but Nova asks: if Skeptic's asymmetry (Parity OFF) is
                justified by empirical rigor, shouldn't Zealot's asymmetry (Parity OFF mirrored) be justified by
                existential commitment? *Even the zealot's debts reveal design flaws.*

                **Trinity's Task:**

                Either justify this asymmetry OR correct it. This is the heart of the preset calibration mission.

                *Full calibration status: `auditors/Mission/Preset_Calibration/CURRENT_MODE_CONFIGS.md`*
                """)

            st.markdown("---")

        # ========================================================================
        # CUSTOM FRAMEWORK
        # ========================================================================
        with utility_tabs[4]:
            st.markdown("## Build Your Own Ledger")
            
            st.markdown("""
            Want to audit your own framework? List its axioms and debts:
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
            
            # Show custom BFT with Live Tracker
            st.markdown("### 📊 Your BFT (Live Tracker)")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Axioms", f"{num_axioms}")
            with col2:
                st.metric("Debts", f"{num_debts}")
            with col3:
                total_bft = num_axioms + num_debts
                st.metric("**BFT Total**", f"**{total_bft}**")
            
            if num_axioms + num_debts > 0:
                st.info(f"""
                **Efficiency Check**: Your BFT is {num_axioms + num_debts}.
                
                - Lower BFT = More efficient (fewer assumptions)
                - MdN's BFT: 10
                - CT's BFT: 11
                
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
                    st.info("**Next:** Go to Console → Open BFT section → Click 'Apply Custom Framework'")
                    
                    # Optional: Auto-navigate
                    if st.button("→ Go to Console Now", key="nav_to_console"):
                        st.session_state.page = 'console'
                        st.rerun()
            
            with col_action2:
                st.markdown("**Option 2: Export File**")
                if num_axioms + num_debts > 0:
                    custom_framework = {
                        "name": framework_name,
                        "bft": {
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
    st.caption("Mr. Brute's Ledger | CFA v5.0 | 'All Named, All Priced'")
