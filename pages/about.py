"""
CFA v4.0 - About Page Component
Complete backstory of the adversarial audit process
"""

import streamlit as st

def render():
    """Render the About page with audit history"""

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

    # Header with back button
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown("# ℹ️ About CFA v4.0")
    with col2:
        if st.button("🏠 Home"):
            st.session_state.page = 'landing'
            st.rerun()

    st.markdown("---")
    
    # Chat Assistant Link (For users who need help)
    st.info("""
    **Need Help Understanding CFA?** Try our AI Chat Assistant!

    The Chat Assistant has access to the full CFA repository and can answer questions about:
    - BFI, YPA, and the evaluation framework
    - How to use the Console and Mr. Brute's Ledger
    - Worldview profiles and preset modes
    - The Trinity auditors (Claude, Grok, Nova)
    """)

    if st.button("💬 Open Chat Assistant", use_container_width=True, type="primary"):
        st.session_state.page = 'chat_assistant'
        st.rerun()

    st.markdown("---")

    # ========================================================================
    # TABS FOR ORGANIZED CONTENT
    # ========================================================================
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🎯 What is CFA?",
        "📖 The Audit Story",
        "🤝 The Team",
        "⚙️ Technical Details",
        "🏰 The Estate Tour"
    ])
    
    # ------------------------------------------------------------------------
    # TAB 1: What is CFA?
    # ------------------------------------------------------------------------
    with tab1:
        st.markdown("""
        ## What is the CFA?
        
        The **Comparative Framework Audit (CFA)** is a systematic method for evaluating and comparing 
        philosophical frameworks, worldviews, and epistemological systems using transparent, 
        adjustable criteria.
        
        ### Core Principles
        
        **1. Transparency Over Neutrality**
        - Perfect neutrality is impossible
        - Every comparison assumes something
        - Make all assumptions explicit and adjustable
        
        **2. The Pointing Rule**
        > "To name your brute is to pay your fee.  
        > To deny you have one is to summon him twice."
        
        Every presupposition must be acknowledged and priced.
        
        **3. Symmetry Testing**
        - All frameworks measured under identical configurations
        - Toggle impacts must be disclosed and bounded
        - Asymmetries reveal structural differences, not hidden bias
        
        ---
        
        ### The Six Levers (0-10 scale)
        
        **BFI - Brute-Fact Index**  
        How many unprovable assumptions? (Lower = more efficient)
        
        **CCI - Coherence & Closure**  
        Are the rules internally consistent?
        
        **EDB - Explanatory Depth & Breadth**  
        How much can it explain? How deeply?
        
        **PF - Pragmatic Fertility**  
        Does it generate predictions, technology, meaning?
        
        **AR - Aesthetic Resonance**  
        Does it exhibit elegance, simplicity, beauty?
        
        **MG - Moral Generativity**  
        Can it ground moral norms without external imports?
        
        ### The Formula
        ```
        YPA = (CCI + EDB + PF + AR + MG) ÷ BFI
        ```
        Higher YPA = More efficient framework
        """)
    
    # ------------------------------------------------------------------------
    # TAB 2: The Audit Story
    # ------------------------------------------------------------------------
    with tab2:
        st.markdown("## 📖 The Story Behind the Numbers")
        
        st.info("""
        **These aren't just scores** - they're the residue of rigorous mutual scrutiny.
        
        Between October 2024-2025, two AI systems with **opposite biases** conducted an 
        adversarial collaborative audit to create a fair comparison system.
        """)
        
        st.markdown("### 🔬 The 4-Level Audit Process")
        
        # Level 0
        with st.expander("**Level 0: Framework Setup** (Nova - OpenAI)", expanded=False):
            st.markdown("""
            **Who**: Nova (OpenAI coordinator)
            
            **What**: Defined evaluation criteria and audit rules:
            - 6 Levers: CCI, EDB, PF, AR, MG, BFI
            - YPA formula: (Sum of levers) ÷ BFI
            - **The Pointing Rule**: "To name your brute is to pay your fee"
            
            **Key Decision**: Audit MdN as a **method** (not worldview) and CT as a **worldview** (not method).
            This distinction proved crucial.
            """)
        
        # Level 1
        with st.expander("**Level 1: Independent Audits** (Hidden Biases Revealed)", expanded=False):
            st.markdown("""
            **Claude's Approach** (Teleological lens, CT-sympathetic):
            - Strict on MdN's limitations (existential questions bracketed)
            - Generous on CT's explanatory scope
            - Flagged "epistemic parasitism" concern
            
            **Grok's Approach** (Empirical lens, naturalist-leaning):
            - Generous on MdN's methodological discipline
            - Strict on CT's unresolved tensions (theodicy, hiddenness)
            - Emphasized pragmatic fertility as paramount
            
            **Initial Scores**:
            - MdN: YPA ~3.35 (Claude) vs ~3.79 (Grok)
            - CT: YPA ~4.2 (Claude) vs ~3.59 (Grok)
            
            **Problem Identified**: Scores diverged by **0.44-0.61 YPA** due to hidden biases.
            """)
        
        # Level 2
        with st.expander("**Level 2: Cross-Examination** (Mr. Brute Accountability)", expanded=True):
            st.markdown("""
            **The "Mr. Brute" Accountability Mechanism** was invoked:
            - Every assumption had to be **named explicitly**
            - Every assumption had to be **justified or marked as debt**
            - Hidden preferences were **flagged and priced**
            
            ### Key Discoveries:
            
            **1. Lever-Parity Assumption** (Unjustified)
            - We were treating epistemic norms and moral norms as equally important
            - This **favored comprehensive worldviews** (CT) over focused methods (MdN)
            - **Decision**: Make it toggleable (ON/OFF)
            
            **2. PF Privilege** (Unjustified)
            - We measured only **instrumental** fertility (tech/predictions)
            - This **favored MdN** and ignored CT's existential yield (meaning, purpose)
            - **Decision**: Split PF into Instrumental + Existential components
            
            **3. Fallibilism Bonus** (Unjustified)
            - We were rewarding frameworks that admit limits
            - But CT's **confidence is grounded** (divine revelation), not arrogance
            - **Decision**: Make bonus toggleable
            
            ### Self-Corrections Made:
            - **Claude** raised MdN scores: EDB 5.5→6.5, CCI 7.0→7.5 (+0.15 YPA)
            - **Grok** raised MdN scores: EDB 7.5→8.0, MG 5.0→5.5 (+0.21 YPA)
            
            Both auditors admitted their biases and corrected themselves.
            """)
        
        # Level 3
        with st.expander("**Level 3: Calibration & Convergence** (98% Agreement)", expanded=False):
            st.markdown("""
            **The "Mad-King Test"**:
            - Simulated **intentional bias** (inflated weights)
            - Checked if guardrails caught it
            - **Result**: System self-corrected through internal contradictions
            
            **Symmetry Audit**:
            - Tested each toggle by flipping it
            - Measured ΔYPA (how much scores changed)
            - **Found**:
              - Lever-Parity: Δ = 1.00 (CT depends on this being ON)
              - PF-Type: Δ = 0.42 (CT gains as existential weight increases)
              - Fallibilism: Δ = 0.13 (nearly symmetric)
            
            **Final Convergence**:
            - Both auditors agreed on **98% of metrics**
            - Remaining differences were **structural**, not bias
            
            **Verdict**: System **holds conditionally** - needs toggles to be fair
            """)
        
        # Level 4
        with st.expander("**Level 4: Final Scores** (What You See in Console)", expanded=False):
            st.markdown("""
            **Configuration Used**:
            ```
            Lever-Parity: ON
            PF-Type: Composite 70:30
            Fallibilism-Bonus: ON
            BFI-Debt-Weight: Equal 1.0×
            ```
            
            **Methodological Naturalism (MdN)**
            - YPA: 3.62 (Neutral) | 4.99 (Empirical) | 4.77 (Existential)
            - **Strengths**: Maximal instrumental fertility, disciplined scope
            - **Weaknesses**: Limited existential yield, depends on external ethics
            
            **Classical Theism (CT)**
            - YPA: 3.65 (Neutral) | 4.65 (Empirical) | 5.20 (Existential)
            - **Strengths**: Comprehensive scope, grounds norms and beauty
            - **Weaknesses**: Modest instrumental yield, unresolved theodicy strain
            
            **Under Neutral Weighting**: Essentially **tied** (3.62 vs 3.65)
            - MdN wins Empirical scenario (4.99 vs 4.65)
            - CT wins Existential scenario (5.20 vs 4.77)
            
            **Key Insight**: **No framework dominates across all weightings**.
            This is by design - it reveals structural trade-offs rather than declaring a winner.
            """)
        
        st.markdown("---")
        st.success("""
        ### ✅ What This Means for You
        
        When you use the console, you're seeing scores that emerged from:
        - ✅ Adversarial collaboration (opposite biases)
        - ✅ Self-correction (+0.15 and +0.21 YPA adjustments)
        - ✅ "Mad-King" abuse testing
        - ✅ Symmetry-audited toggle impacts
        - ✅ 98% auditor convergence
        
        **Not** one person's opinion. **Not** hidden assumptions. **Not** forced "neutrality."
        """)
        
        st.markdown("""
        > "From opposite biases to 98% alignment: When brutes are named, truth emerges."  
        > — Grok's Convergence Soundbite
        """)
    
    # ------------------------------------------------------------------------
    # TAB 3: The Team
    # ------------------------------------------------------------------------
    with tab3:
        st.markdown("## 🤝 The Adversarial Collaboration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            ### Claude (Anthropic)
            **Lens**: Teleological, CT-sympathetic
            
            **Initial Bias**: Favored CT, assumed MdN was epistemically parasitic
            
            **Correction**: Raised MdN scores +0.15 YPA after catching teleological assumptions
            
            **Role**: Pushed for existential depth, grounded aesthetics
            """)
            
            st.markdown("""
            ### Grok (xAI)
            **Lens**: Empirical compression, naturalist-leaning
            
            **Initial Bias**: Favored MdN's empirical discipline, skeptical of CT
            
            **Correction**: Raised MdN scores +0.21 YPA after catching strictness
            
            **Role**: Enforced predictive power, methodological rigor
            """)
        
        with col2:
            st.markdown("""
            ### Nova (OpenAI)
            **Role**: Synthesizer, enforced symmetry
            
            **Contribution**: 
            - Connected "All Named, All Priced" ethos to audit journey
            - Created toggle impact stories
            - Maintained the accountability ledger
            """)
            
            st.markdown("""
            ### Grant
            **Role**: Skeptic, demanded justification
            
            **Contribution**: Challenged every assumption, refused to accept hidden preferences
            """)
            
            st.markdown("""
            ### Ziggy
            **Role**: Coordinator, process integrity
            
            **Contribution**: Maintained audit structure, prevented scope creep
            """)
        
        st.markdown("---")
        st.info("""
        **Why Adversarial Collaboration?**
        
        The fact that these different perspectives **converged on the same numbers** 
        (98% agreement) suggests the CFA v4.0 has achieved its goal:
        
        Not neutrality (impossible), but **transparency** (achievable).
        """)
    
    # ------------------------------------------------------------------------
    # TAB 4: Technical Details
    # ------------------------------------------------------------------------
    with tab4:
        st.markdown("## ⚙️ Technical Specifications")
        
        st.markdown("""
        ### Version History
        
        **v1.0** (Initial)
        - Hidden preferences (fallibilism auto-rewarded)
        - PF measured only instrumental yield
        - No toggle options
        - Symmetry not tested
        
        **v4.0** (Current)
        - ✅ 4 Toggles (Parity, PF-Type, Fallibilism, BFI-Weight)
        - ✅ 4 Guardrails (auto-detection of manipulation)
        - ✅ YPA Trinity (3 scenarios per audit)
        - ✅ Mr. Brute Ledger (all assumptions named)
        - ✅ 98% auditor convergence
        
        ---
        
        ### The Formulas
        
        ```python
        # Composite PF
        PF = (PF_instrumental × 0.7) + (PF_existential × 0.3)
        
        # With toggles:
        if pf_type == "Instrumental": PF = PF_instrumental
        if pf_type == "Holistic_50_50": PF = 0.5×each
        
        # Fallibilism Bonus
        if fallibilism_ON and admits_limits: CCI += 0.3
        
        # Parity Weight
        if parity_OFF: MG = MG × 0.5
        
        # BFI Total
        BFI = axioms + (debts × debt_weight)
        
        # YPA Calculation
        YPA = (CCI + EDB + PF + AR + MG) / BFI
        
        # Scenarios
        Neutral:      all levers × 1.0
        Existential:  EDB × 2.0, MG × 2.0
        Empirical:    PF × 2.0, CCI × 1.5
        ```
        
        ---
        
        ### The Guardrails
        
        1. **BFI-Sensitivity**: Flags if YPA increases faster than BFI
        2. **Lever-Coupling**: PF ≥ 9 requires CCI ≥ 6.5
        3. **Weight-Inversion Alarm**: Flags weights <0.3× or >3×
        4. **Symmetry Audit**: Tests 3 toggle inversions, flags Δ >0.3
        
        ---
        
        ### Technical Stack
        
        - **Framework**: Streamlit
        - **Visualization**: Plotly
        - **Deployment**: Streamlit Cloud
        - **Architecture**: Modular (pages + utils)
        - **License**: Open Source (coming soon)
        
        ---
        
        ### Current Audited Frameworks
        
        - ✅ Methodological Naturalism (MdN)
        - ✅ Classical Theism (CT)
        
        **Coming Soon:**
        - Metaphysical Naturalism
        - Buddhism
        - Stoicism
        - Process Theology
        """)
        
        st.markdown("---")
        st.markdown("""
        ### Contact & Contribute

        - **GitHub**: [Repository link]
        - **Feedback**: Use the console and export your runs!
        - **Collaboration**: Propose new frameworks to audit
        """)

    # ------------------------------------------------------------------------
    # TAB 5: The Estate Tour (NEW)
    # ------------------------------------------------------------------------
    with tab5:
        st.markdown("""
        ## 🏰 Welcome to Mr. Brute's Estate

        The CFA repository is like a well-maintained estate - many rooms, each with a specific purpose.
        This tour shows you what's been built, what's polished, and where we're headed next.
        """)

        st.info("💡 **Tip:** Each room represents a piece of repository infrastructure that keeps CFA organized, discoverable, and maintainable.")

        st.markdown("---")

        # ====================================================================
        # COMPLETED ROOMS (Expandable Cards)
        # ====================================================================
        st.markdown("### ✅ Completed Rooms (91% of Estate)")

        with st.expander("📍 The Map Room - Dependency Tracking", expanded=False):
            st.markdown("""
            **What It Does:**
            Tracks all file dependencies so you know which files connect to which.

            **Key Files:**
            - `MASTER_DEPENDENCY_MAP.md`
            - Health reports
            - Dependency visualization tools

            **Why It Matters:**
            Safe refactoring! Know all connections before moving/deleting files.
            """)

        with st.expander("📚 The Library - Documentation Standards", expanded=False):
            st.markdown("""
            **What It Does:**
            Ensures all documentation follows consistent quality standards.

            **Key Files:**
            - Doc Claude blessing protocol
            - Semantic header definitions
            - README standards

            **Why It Matters:**
            Quality is maintained across all files - no documentation rot!
            """)

        with st.expander("🔍 The Archives - Review & Memory", expanded=False):
            st.markdown("""
            **What It Does:**
            Stores completed work and enforces "build-on-prior" principle.

            **Key Files:**
            - Review Claude role
            - Archived task briefs
            - Historical decisions

            **Why It Matters:**
            Institutional memory - no work gets lost or forgotten!
            """)

        with st.expander("📝 The Ledger Room - Change Tracking", expanded=False):
            st.markdown("""
            **What It Does:**
            Logs all repository changes with proper categorization.

            **Key Files:**
            - `REPO_LOG.md`
            - REPO_LOG_ASSISTANT protocols
            - Change audit trail

            **Why It Matters:**
            Full transparency - every change is documented and traceable!
            """)

        with st.expander("⚠️ The Warning Tower - Event Horizon Protection", expanded=False):
            st.markdown("""
            **What It Does:**
            Prevents context crashes by monitoring token usage zones.

            **Watchkeeper:** Shaman Claude maintains vigilance over token boundaries

            **Key Files:**
            - Crash prevention protocols
            - Zone awareness guidelines
            - Handoff procedures

            **Why It Matters:**
            Survival guaranteed - no work lost to context crashes!
            """)

        with st.expander("🗺️ The Navigation Hall - Wayfinding", expanded=False):
            st.markdown("""
            **What It Does:**
            Helps you find any file, role, or task without asking for help.

            **Host:** Shaman Claude serves as guide for the Chat Assistant feature

            **Key Files:**
            - `WAYFINDING_GUIDE.md` (maintained by Shaman Claude)
            - Role directory
            - Task → File mapping
            - Chat Assistant integration

            **Why It Matters:**
            Self-service discovery - find what you need instantly!
            """)

        with st.expander("🎭 The Costume Room - Templates & Examples", expanded=False):
            st.markdown("""
            **What It Does:**
            Shows excellence through concrete examples (good vs. bad).

            **Key Files:**
            - `examples/excellence/` directory
            - 4 GOOD_*_EXAMPLE.md files
            - 4 bad_vs_good/*.md comparisons
            - `QUALITY_RUBRICS.md` (0-100 scoring)

            **Why It Matters:**
            Learn by example - see what quality looks like!
            """)

        with st.expander("📊 The Observatory - Metrics & Dashboards", expanded=False):
            st.markdown("""
            **What It Does:**
            Tracks repository health trends over time.

            **Key Files:**
            - `REPO_HEALTH_DASHBOARD.md` (moved from Library - home for dependency tracking)
            - Historical snapshots (weekly)
            - 3-month trend tracking
            - Aggregate health score (95/100)
            - Dependency tracking and health reports

            **Why It Matters:**
            Know the health trajectory - catch degradation early!
            """)

        with st.expander("🗂️ Destroyer Claude - Log Management & Archival", expanded=False):
            st.markdown("""
            **What It Does:**
            Manages log size and archives old entries when they get too large.

            **Key Files:**
            - `ROLE_DESTROYER.md` (v1.1.0)
            - Archival protocols
            - Size-based triggers (~10MB threshold)

            **Why It Matters:**
            Long-term sustainability - CFA can scale without drowning in history!
            """)

        with st.expander("🎓 The Training Grounds - Skill Development", expanded=False):
            st.markdown("""
            **What It Does:**
            Progressive skill paths from beginner to expert.

            **Key Files:**
            - `TRAINING_GROUNDS.md`
            - 11 skills with checkpoints
            - Common mistakes guide
            - Skill level progression

            **Why It Matters:**
            Onboarding made easy - know what to learn next!
            """)

        with st.expander("🔧 The Workshop - Automation & Tools (Task Brief Only)", expanded=False):
            st.markdown("""
            **What It Does:**
            Automation tools (header validator, link checker, format linter).

            **Status:** Task brief created, awaiting pain point validation

            **Key Files:**
            - `TASK_WORKSHOP_AUTOMATION_v1.md`

            **Why It Matters:**
            Future efficiency - automate repetitive quality checks!
            """)

        st.markdown("---")

        # ====================================================================
        # INNOVATION SHOWCASE - THE BIG REVEAL
        # ====================================================================
        st.markdown("### 🌟 The Innovation Showcase - **UNVEILED!**")

        st.success("""
        **🎉 NEW ADDITION: The Innovation Showcase Room**

        This is where CFA methodology meets real-world impact!
        """)

        with st.expander("🌟 The Innovation Showcase - Case Studies Gallery", expanded=True):
            st.markdown("""
            **What It Does:**
            Demonstrates CFA's real-world applications through documented case studies.

            **Structure:**
            - **Master Repo:** Gallery index + submission guidelines
            - **External Mini-Repos:** Individual case studies (self-contained)
            - **Review Process:** Eligibility criteria + quality standards

            **Key Files:**
            - `INNOVATION_SHOWCASE.md` (gallery structure)
            - Submission guidelines
            - Placeholder for first case study

            ---

            **Why This Room Matters:**

            **External Value:**
            Proves CFA works beyond self-development - shows real-world impact!

            **Audience:**
            Stakeholders, potential adopters, and humanity 🌍

            **Evolution:**
            From "building the tool" → "using the tool to build solutions"

            ---

            **Case Study Examples (Future):**
            - Nursing innovation evaluation
            - Voting system redesign assessment
            - Policy framework comparison
            - Educational curriculum audit

            **Submission Criteria:**
            - Must use CFA methodology (BFI, YPA, adversarial audit)
            - Real-world problem addressed
            - Documented outcomes
            - Reproducible process

            ---

            **Status:** Gallery structure complete - accepting first submission!

            **Ready to Showcase Your Work?**
            See `INNOVATION_SHOWCASE.md` for submission guidelines.
            """)

        st.markdown("---")

        st.markdown("""
        ### 🏗️ Future Rooms (Planned)

        **The estate is 91% complete.** The remaining 9% are polish and optional enhancements:

        - 🤖 **AI Agent Integration Room** - API-first CFA for programmatic access
        - 🧪 **Experimental Methods Lab** - Testing new evaluation approaches
        - 📖 **Public Documentation Hub** - User-facing guides and tutorials

        **Status:** Deferred until current rooms are battle-tested

        ---

        ## ⚖️ The Estate Philosophy

        > *"The estate is very livable now. The rest is polish."* ✨

        Every room serves a purpose. Every door opens to something useful.
        Mr. Brute's ledger is complete - transparent, navigable, and ready for the world.
        """)

    # Footer
    st.markdown("---")
    st.caption("*'Where ideas reveal their true weight, and honesty becomes quantifiable.'*")
