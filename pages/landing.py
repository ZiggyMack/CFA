"""
CFA v4.0 - Landing Page Component (Updated)
With navigation at top, minimal spacing, reordered content
"""

import streamlit as st

def render():
    """Render the landing page"""
    
    # CSS Styling - Minimal spacing, prevents cutoff
    st.markdown("""
        <style>
        /* Minimal padding - adjusted for missing header bar */
        .block-container {
            padding-top: 3rem;
            padding-bottom: 1rem;
        }
        
        /* Header section styling */
        .nav-container {
            display: flex;
            justify-content: center;
            gap: 1rem;
            margin-bottom: 2rem;
        }
        
        .main-title {
            font-size: 3.5rem;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin: 1.5rem 0 0.5rem 0;
        }
        
        .tagline {
            text-align: center;
            font-size: 1.3rem;
            font-style: italic;
            color: #764ba2;
            margin: 0 0 2rem 0;
        }
        
        /* Mr. Brute Easter Egg - Hidden in corner */
        .brute-doodle {
            position: fixed;
            bottom: 20px;
            right: 20px;
            font-size: 2.5rem;
            cursor: pointer;
            opacity: 0.3;
            transition: opacity 0.3s, transform 0.3s;
            z-index: 1000;
            text-decoration: none;
        }
        
        .brute-doodle:hover {
            opacity: 1;
            transform: scale(1.2);
        }
        
        .brute-tooltip {
            position: fixed;
            bottom: 80px;
            right: 30px;
            background: rgba(102, 126, 234, 0.95);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 0.5rem;
            font-size: 0.9rem;
            opacity: 0;
            transition: opacity 0.3s;
            pointer-events: none;
            z-index: 999;
        }
        
        .brute-doodle:hover + .brute-tooltip {
            opacity: 1;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # NAVIGATION - 3 Buttons (evenly spaced across top)
    # ========================================================================
    nav_col1, nav_col2, nav_col3 = st.columns([1, 1, 1])
    
    with nav_col1:
        if st.button("🚀 LAUNCH CONSOLE", use_container_width=True, type="primary"):
            st.session_state.page = 'console'
            st.rerun()
    
    with nav_col2:
        if st.button("📖 USER MANUAL", use_container_width=True):
            st.session_state.page = 'manual'
            st.rerun()
    
    with nav_col3:
        if st.button("ℹ️ ABOUT v4.0", use_container_width=True):
            st.session_state.page = 'about'
            st.rerun()
    
    st.markdown('<div style="height: 1.5rem;"></div>', unsafe_allow_html=True)
    
    # ========================================================================
    # LOGO & TAGLINE (centered)
    # ========================================================================
    st.markdown('<h1 class="main-title">⚖️ CFA-VOODOO</h1>', unsafe_allow_html=True)
    st.markdown('<p class="tagline">"All Named. All Priced."</p>', unsafe_allow_html=True)

    # Secondary navigation - Mr. Brute's Ledger (centered)
    col_spacer1, col_brute, col_spacer2 = st.columns([1.5, 1, 1.5])
    with col_brute:
        if st.button("📓✍️ Mr. Brute's Ledger", use_container_width=True, key="brute_main"):
            st.session_state.page = 'brute_ledger'
            st.rerun()

    # Showcase button - same size as Manifesto button for symmetry
    col_spacer3, col_showcase, col_spacer4 = st.columns([1.5, 1, 1.5])
    with col_showcase:
        if st.button("🎨 Innovation Showcase", use_container_width=True, key="showcase_main"):
            st.session_state.page = 'showcase'
            st.rerun()

    st.markdown("---")
    
    # ========================================================================
    # MAIN MANIFESTO CONTENT
    # ========================================================================
    st.markdown("## ⚡ Launch Manifesto")

    # Link to full philosophical covenant
    if st.button("📜 **Read the Full CFA Manifesto**", use_container_width=True):
        st.session_state.page = 'verbose_manifesto'
        st.rerun()
    st.caption("Why CFA exists, the Trinity architecture, and our binding commitment to transparency.")

    st.write("""
    **Welcome to the Comparative Framework Analysis (CFA) Console,**
    the first interactive epistemic laboratory built to measure how worldviews hold their ground under pressure.
    """)
    
    st.write("""
    Here, philosophy meets engineering.  
    Every assumption is declared, every bias tagged, every outcome earned.
    """)
    
    # What You're Touching
    st.markdown("---")
    st.markdown("## 🧩 What You're Touching")
    
    st.write("The CFA-Voodoo Console is not a game of opinions. It's an instrument—a system that:")
    
    st.markdown("""
    - Quantifies coherence, depth, fertility, beauty, and morality
    - Tests bias symmetry using live toggles and guardrails
    - Displays truth-seeking as a transparent, reproducible process
    """)
    
    # Inline button for Mr. Brute Ledger
    col_text, col_btn = st.columns([1, 5])
    with col_text:
        st.markdown("- Audits hidden axioms through")
    with col_btn:
        if st.button("📓 **Mr. Brute Ledger**", key="manifesto_brute_link"):
            st.session_state.page = 'brute_ledger'
            st.rerun()
    
    st.write("You can watch, in real time, how changing your assumptions reshapes your philosophical landscape.")
    
    # The Field We Just Opened
    st.markdown("---")
    st.markdown("## 🧠 The Field We Just Opened")
    
    st.write("CFA-Voodoo inaugurates a new discipline: **Epistemic Engineering**.")
    
    st.write("""
    A field where frameworks are not argued—they are measured.  
    Where neutrality isn't assumed—it's configured.  
    Where "truth" is not decreed but disclosed by toggle position.
    """)
    
    st.markdown("*Metaphysics with metrics. Ethics with sliders. Philosophy with feedback.*")
    
    # Audit Journey (Grok Enhancement)
    with st.expander("🔍 **The Audit Journey: Level 0-4**", expanded=False):
        st.markdown("""
        **How did we achieve 98% convergence?**
        
        **Level 0: Independent Audits**  
        Claude (Anthropic) and Grok (xAI) each audited MdN and CT independently, bringing different philosophical lenses.
        
        **Level 1: Discrepancy Detection**  
        Scores diverged due to undetected bias:
        - Claude favored CT's comprehensive scope (teleological sympathy)
        - Grok favored MdN's predictive power (empirical favoritism)
        
        **Level 2: Adversarial Correction**  
        Each auditor challenged the other with rationale:
        - Grok to Claude: "CT's CCI should be 7.5, not 8.0 - theodicy tension reduces closure"
        - Claude to Grok: "MdN's PF-Instrumental can stay 10.0 - predictive success is undeniable"
        - Both adjusted scores with documented reasoning
        
        **Level 3: Convergence Achieved**  
        Final scores: MdN 3.62, CT 3.65 (only 0.03 YPA difference = 98% agreement)  
        Convergence proves rigor - mutual checking eliminates solo bias.
        
        **Level 4: Tool Building**  
        The console you see embodies this audit journey:
        - 4 toggles reflect bias discoveries (Parity, PF-Type, Fallibilism, BFI-Weight)
        - Guardrails implement lessons from Level 2 corrections
        - Profile library showcases convergence with badges
        
        **Level 5: DaVinci Pass** *(You are here)*  
        Injecting accountability narrative while maintaining symmetry and usability.
        """)
    
    # Operate with Impeccability
    st.markdown("---")
    st.markdown("## ⚙️ Operate with Impeccability")
    
    st.write("""
    Every visitor is an operator.  
    Every operation leaves a trace.  
    Move the dials with intent.  
    Record your runs.  
    Remember: the one who cares walks the path with the most heart.
    """)
    
    # ========================================================================
    # CREDIBILITY MARKERS (moved from top for better flow)
    # ========================================================================
    st.markdown("---")
    
    # Transparency callout
    st.info("⚖️ **Transparency > Neutrality:** Fairness through disclosure, not false balance.")
    
    # Convergence badge
    st.success("✅ 98% Auditor Convergence | Symmetry Verified by Nova & Grok")
    
    # ========================================================================
    # JOIN THE EXPERIMENT (moved to bottom)
    # ========================================================================
    st.markdown("---")
    st.markdown("## 💡 Join the Experiment")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        1. **Adjust the knobs** - Configure your comparison criteria
        2. **Run the analysis** - See frameworks measured transparently
        """)
    with col2:
        st.markdown("""
        3. **Export your ledger** - Save and share your results
        4. **Debate the data** - Discuss what the numbers reveal
        """)
    
    # Closing Statement
    st.markdown("---")
    st.markdown("""
    <p style="text-align: center; font-size: 1.2rem; font-weight: bold; color: #764ba2; margin-top: 1rem;">
    Welcome to the CFA-Voodoo Console.<br/>
    Where ideas reveal their true weight, and honesty becomes quantifiable.
    </p>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <p style="text-align: center; font-style: italic; color: #667eea; margin-top: 1rem;">
    "All named. All priced. This is the way."
    </p>
    """, unsafe_allow_html=True)
    
    # ========================================================================
    # FOOTER - Every number earned under "All Named, All Priced"
    # ========================================================================
    st.markdown("---")
    st.caption("CFA v4.0 | Epistemic Engineering | October 2025")
    st.caption("*Every number you see was earned under the rule: All Named, All Priced.*")
