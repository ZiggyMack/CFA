"""
CFA v4.0 - User Manual (Beautiful Version)
Inspired by the original vibrant design
"""

import streamlit as st

def render():
    """Render the beautiful manual page"""
    
    # Custom CSS for visual appeal
    st.markdown("""
        <style>
        /* Card styling */
        .info-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 1rem;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .lever-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 1.5rem;
            border-radius: 0.8rem;
            margin: 1rem 0;
            border-left: 4px solid #667eea;
        }
        
        .toggle-card {
            background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
            padding: 1.5rem;
            border-radius: 0.8rem;
            margin: 1rem 0;
            border-left: 4px solid #ff6b6b;
        }
        
        .formula-box {
            background: #2d3748;
            color: #48bb78;
            font-family: 'Courier New', monospace;
            padding: 1.5rem;
            border-radius: 0.5rem;
            font-size: 1.2rem;
            text-align: center;
            margin: 1.5rem 0;
            border: 2px solid #48bb78;
        }
        
        .highlight-box {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            padding: 1rem;
            border-radius: 0.5rem;
            margin: 1rem 0;
            font-weight: bold;
        }
        
        .tip-box {
            background: #e6fffa;
            border-left: 4px solid #38b2ac;
            padding: 1rem;
            margin: 1rem 0;
            border-radius: 0.3rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Header with back button
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown("# 📖 CFA v4.0 User Manual")
        st.markdown("*Your guide to epistemic engineering*")
    with col2:
        if st.button("🏠 Home"):
            st.session_state.page = 'landing'
            st.rerun()
    
    st.markdown("---")
    
    # Hero section with download
    st.markdown("""
        <div class="info-card">
            <h2>📥 Complete Manual (PDF)</h2>
            <p style="font-size: 1.1rem;">Access the full CFA v4.0 User Manual with all formulas, examples, and calibration history.</p>
            <p><a href="https://github.com/ZiggyMack/CFA-2.0/raw/main/docs/CFA_v2_Manual.pdf" 
               style="color: white; text-decoration: underline; font-size: 1.2rem;">
               → Download PDF Manual
            </a></p>
            <p style="font-size: 0.9rem; margin-top: 1rem;"><em>Note: Upload the PDF from this repo's outputs folder to your GitHub docs/ directory</em></p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Tabs for navigation
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "🚀 Quick Start",
        "🌍 v4.0 Features (NEW!)",
        "⚖️ The Six Levers",
        "🎛️ Toggles Explained",
        "📊 Reading Results",
        "💡 Pro Tips"
    ])
    
    # ========================================================================
    # TAB 1: QUICK START
    # ========================================================================
    with tab1:
        st.markdown("## 🚀 Quick Start Guide")
        
        st.markdown("""
            <div class="highlight-box">
            ⚡ New to CFA? Start here!
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### What is CFA?")
        st.write("""
        The **Comparative Framework Audit** is a system for comparing worldviews, 
        epistemologies, and philosophical frameworks using transparent, adjustable criteria.
        
        **Core Innovation**: "All Named, All Priced"
        - Every assumption is disclosed
        - Every presupposition is counted
        - Every bias is made toggleable
        """)
        
        st.markdown("### The Formula")
        st.markdown("""
            <div class="formula-box">
            YPA = (CCI + EDB + PF + AR + MG) ÷ BFI
            </div>
        """, unsafe_allow_html=True)
        
        st.write("""
        **YPA** = Yield-Per-Axiom (efficiency metric)
        
        **Higher YPA** = More efficient framework (more explanatory power per assumption)
        """)
        
        st.markdown("### 5-Minute Workflow")
        
        st.markdown("""
            <div class="lever-card">
            <h4>Step 1: Configure Your Values</h4>
            <p>In the sidebar, set 4 toggles based on what you care about:</p>
            <ul>
                <li>Do moral norms matter as much as predictive power? (Parity)</li>
                <li>Do you value meaning or just tech? (PF-Type)</li>
                <li>Should humility be rewarded? (Fallibilism)</li>
                <li>Do unresolved questions cost more? (BFI Weight)</li>
            </ul>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="lever-card">
            <h4>Step 2: Adjust the Levers</h4>
            <p>Use sliders to score each framework on 6 dimensions (0-10 scale)</p>
            <p>Or use preset buttons: MAX, MID, RESET, MIN</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="lever-card">
            <h4>Step 3: Examine the Trinity</h4>
            <p>Check YPA under 3 scenarios:</p>
            <ul>
                <li><b>Neutral</b> - Baseline (all 1×)</li>
                <li><b>Existential</b> - Meaning-focused (2× EDB, 2× MG)</li>
                <li><b>Empirical</b> - Tech-focused (2× PF, 1.5× CCI)</li>
            </ul>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="tip-box">
            💡 <b>Pro Tip:</b> Don't just look at who "wins." Look at the trade-offs. 
            What does each framework give up? Is that acceptable for your purposes?
            </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # TAB 2: v4.0 FEATURES (NEW!)
    # ========================================================================
    with tab2:
        st.markdown("## 🌍 v4.0 Features - Philosophical Laboratory")

        st.markdown("""
            <div class="highlight-box">
            ✨ NEW in v4.0: CFA expands from technical framework to comprehensive philosophical laboratory
            </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🗂️ 12 Worldview Profiles")
        st.markdown("""
            <div class="info-card">
            <h4>Expanded from 2 to 12 fully-audited worldviews</h4>
            <p><b>Major World Religions:</b> Classical Theism, Islam, Orthodox Judaism, Mormonism, Hinduism, Buddhism</p>
            <p><b>Naturalistic Frameworks:</b> Methodological Naturalism, Process Theology</p>
            <p><b>Meta-Ethical Positions:</b> Error Theory, Null Hypothesis, Desiderata Believers, Existentialism</p>
            <p><b>Total:</b> ~240KB philosophical documentation with Steel-Manning sections, academic sources (9+ per worldview), and calibration YAML blocks</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("### 📐 Symmetry Matrix Visualizer (SMV)")
        st.markdown("""
            <div class="lever-card">
            <h4>Interactive visualization of auditor tension/resolution</h4>
            <p><b>What you see:</b></p>
            <ul>
                <li><b>Claude/Nova/Grok alignment triangle</b> - Where do auditors agree/disagree?</li>
                <li><b>Ethical invariant violation overlays</b> - Which principles challenged?</li>
                <li><b>Symmetry health tracking</b> - Is comparison genuinely fair over time?</li>
                <li><b>Tension → Resolution pathways</b> - How did disagreements resolve?</li>
            </ul>
            <p><b>Philosophy (Nova's vision):</b> "Symmetry thrives in dialogue, not dictation. Tools reveal patterns, not police them."</p>
            <p><b>Key insight:</b> Understanding BEFORE enforcement - judge fairness yourself, not via black-box scoring</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("### ⚖️ Crux Architecture - Honest Impasses")
        st.markdown("""
            <div class="toggle-card">
            <h4>Named impasse system for unresolvable philosophical disagreements</h4>
            <p><b>When auditors can't reach 98%+ convergence after genuine deliberation:</b> Declare a <b>Crux Point</b></p>

            <p><b>Three-View System:</b></p>
            <ul>
                <li><b>Self-Reported Tab:</b> What the worldview claims about itself</li>
                <li><b>Peer-Reviewed Tab:</b> What survives adversarial audit (Claude/Nova/Grok)</li>
                <li><b>Delta Tab:</b> The difference (humility metrics - how well does worldview know itself?)</li>
            </ul>

            <p><b>User Control - Crux Handling Lever:</b></p>
            <ul>
                <li><b>NORMALIZE_UNCERTAINTY (Skeptic Mode):</b> Apply penalty based on disagreement width</li>
                <li><b>CARRY_FORWARD (Zealot Mode):</b> Use self-reported scores, acknowledge but don't penalize</li>
            </ul>

            <p><b>Key insight:</b> Crux Points are <i>features, not bugs</i> - they mark boundaries of knowable truth</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("### 🤝 Adversarial Scoring System")
        st.markdown("""
            <div class="info-card">
            <h4>Multi-AI collaboration: Full bias vs. adversarial-adjusted scores</h4>

            <p><b>Three Auditor Roles:</b></p>
            <ul>
                <li><b>PRO (Claude):</b> Teleological lens, advocates FOR worldview with calibration bias adjustment</li>
                <li><b>ANTI (Grok):</b> Empirical lens, challenges claims from naturalistic perspective</li>
                <li><b>FAIRNESS (Nova):</b> Symmetry lens, ensures balance and catches asymmetric treatment</li>
            </ul>

            <p><b>The Process:</b></p>
            <ol>
                <li>Worldview writes <b>self-reported score</b> (what it claims)</li>
                <li>Three auditors deliberate adversarially using Steel-Manning scaffolds</li>
                <li>Target: <b>98%+ convergence</b> (if can't agree → declare Crux Point)</li>
                <li>Output: <b>Peer-reviewed score</b> (survives genuine philosophical scrutiny)</li>
            </ol>

            <p><b>Calibration Hash System:</b> Each auditor uses bias-adjustment YAML values (e.g., <code>1bbec1e119a2c425</code> for PRO-CT stance) to prevent gaming and ensure consistent posture</p>

            <p><b>Key insight:</b> Scores are <i>earned</i> through intellectual combat, not self-reported. Delta between self-report and peer-review = <b>humility metric</b></p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class="tip-box">
            💡 <b>v4.0 Philosophy:</b> CFA now treats worldviews as <i>living philosophical positions</i> worthy of genuine intellectual charity,
            not strawmen to dismiss. Adversarial collaboration + named impasses = epistemic honesty at scale.
            </div>
        """, unsafe_allow_html=True)

    # ========================================================================
    # TAB 3: THE SIX LEVERS
    # ========================================================================
    with tab3:
        st.markdown("## ⚖️ The Six Levers")
        st.markdown("*Each framework is scored on these dimensions (0-10)*")
        
        # BFI
        st.markdown("""
            <div class="lever-card">
            <h3>🔢 BFI - Brute-Fact Index</h3>
            <p><b>What it measures:</b> How many unprovable assumptions does this framework require?</p>
            <p><b>Scoring:</b> Count axioms + debts. Lower = more efficient</p>
            <p><b>Key insight:</b> Every framework starts somewhere. The question is: are you honest about where?</p>
            <p><i>"To name your brute is to pay your fee"</i></p>
            </div>
        """, unsafe_allow_html=True)
        
        # CCI
        st.markdown("""
            <div class="lever-card">
            <h3>🔗 CCI - Coherence & Closure</h3>
            <p><b>What it measures:</b> Are the rules internally consistent?</p>
            <p><b>High scores (8-10):</b> Tight logical structure, minimal contradictions</p>
            <p><b>Low scores (3-5):</b> Unresolved tensions, competing principles</p>
            <p><b>Example:</b> Does the framework claim certainty while denying absolute truth?</p>
            </div>
        """, unsafe_allow_html=True)
        
        # EDB
        st.markdown("""
            <div class="lever-card">
            <h3>🌍 EDB - Explanatory Depth & Breadth</h3>
            <p><b>What it measures:</b> How much can it explain? How deeply?</p>
            <p><b>Breadth:</b> Range of phenomena addressed (physics, meaning, ethics, etc.)</p>
            <p><b>Depth:</b> Level of detail and mechanism provided</p>
            <p><b>Trade-off:</b> Broad but shallow vs narrow but deep</p>
            </div>
        """, unsafe_allow_html=True)
        
        # PF
        st.markdown("""
            <div class="lever-card">
            <h3>🚀 PF - Pragmatic Fertility</h3>
            <p><b>What it measures:</b> Does it generate practical success?</p>
            <p><b>Instrumental:</b> Tech, predictions, material results</p>
            <p><b>Existential:</b> Meaning, purpose, orientation</p>
            <p><b>Composite:</b> Weighted mix (adjustable via PF-Type toggle)</p>
            <p><i>Default: 70% instrumental, 30% existential</i></p>
            </div>
        """, unsafe_allow_html=True)
        
        # AR
        st.markdown("""
            <div class="lever-card">
            <h3>✨ AR - Aesthetic Resonance</h3>
            <p><b>What it measures:</b> Does it exhibit elegance, simplicity, beauty?</p>
            <p><b>High scores:</b> Parsimony, mathematical beauty, pattern-recognition</p>
            <p><b>Low scores:</b> Ad-hoc, cluttered, inelegant</p>
            <p><b>Debate:</b> Is beauty a guide to truth, or just a preference?</p>
            </div>
        """, unsafe_allow_html=True)
        
        # MG
        st.markdown("""
            <div class="lever-card">
            <h3>⚖️ MG - Moral Generativity</h3>
            <p><b>What it measures:</b> Can it ground or generate moral norms without importing them?</p>
            <p><b>High scores (8-10):</b> Internal resources for ethics</p>
            <p><b>Low scores (3-5):</b> Depends on external moral framework</p>
            <p><b>Key question:</b> Does this framework tell you what's true, or also what's good?</p>
            </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # TAB 3: TOGGLES EXPLAINED
    # ========================================================================
    with tab3:
        st.markdown("## 🎛️ The Four Toggles")
        st.markdown("*Configuration options that reveal your values*")
        
        # Toggle 1
        st.markdown("""
            <div class="toggle-card">
            <h3>1️⃣ Lever-Parity Toggle</h3>
            <p><b>The Question:</b> Should moral norms (MG) be weighted equally with epistemic norms (CCI, EDB)?</p>
            
            <p><b>ON (Default):</b> MG counts fully (1.0×)</p>
            <ul>
                <li>Favors comprehensive worldviews</li>
                <li>Values moral grounding as much as predictive power</li>
            </ul>
            
            <p><b>OFF:</b> MG down-weighted (0.5×)</p>
            <ul>
                <li>Favors methodological frameworks</li>
                <li>Emphasizes epistemic norms over ethical claims</li>
            </ul>
            
            <p><b>Impact:</b> CT loses ~0.8 YPA when OFF (reveals structural dependency on normative grounding)</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Toggle 2
        st.markdown("""
            <div class="toggle-card">
            <h3>2️⃣ PF-Type Toggle</h3>
            <p><b>The Question:</b> How should we measure "pragmatic success"?</p>
            
            <p><b>Instrumental (100% tech):</b></p>
            <ul>
                <li>Only predictive/technological yield</li>
                <li>Favors MdN</li>
            </ul>
            
            <p><b>Composite 70:30 (Default):</b></p>
            <ul>
                <li>Balanced mix</li>
                <li>Fair comparison baseline</li>
            </ul>
            
            <p><b>Holistic 50:50 (Equal meaning):</b></p>
            <ul>
                <li>Existential yield weighted equally</li>
                <li>Favors CT</li>
            </ul>
            
            <p><b>Impact:</b> ±0.4 YPA depending on choice</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Toggle 3
        st.markdown("""
            <div class="toggle-card">
            <h3>3️⃣ Fallibilism-Bonus Toggle</h3>
            <p><b>The Question:</b> Should frameworks that admit their limits get a reward?</p>
            
            <p><b>ON (Default):</b> +0.3 CCI bonus</p>
            <ul>
                <li>Rewards intellectual humility</li>
                <li>Favors frameworks checking "Admits Limits"</li>
            </ul>
            
            <p><b>OFF:</b> No bonus</p>
            <ul>
                <li>Confidence not penalized if grounded</li>
                <li>Divine revelation (CT) gets equal treatment</li>
            </ul>
            
            <p><b>Impact:</b> Usually small (±0.1 YPA) - both MdN and CT admit limits</p>
            </div>
        """, unsafe_allow_html=True)
        
        # Toggle 4
        st.markdown("""
            <div class="toggle-card">
            <h3>4️⃣ BFI Debt-Weight Toggle</h3>
            <p><b>The Question:</b> Should unresolved questions cost more than declared axioms?</p>
            
            <p><b>Equal 1.0× (Default):</b></p>
            <ul>
                <li>Axioms and debts count the same</li>
                <li>Neutrality between foundations and mysteries</li>
            </ul>
            
            <p><b>Weighted 1.2×:</b></p>
            <ul>
                <li>Debts cost 20% more</li>
                <li>Promissory notes vs solid foundations</li>
            </ul>
            
            <p><b>Impact:</b> Penalizes frameworks with many unresolved questions</p>
            </div>
        """, unsafe_allow_html=True)
    
    # ========================================================================
    # TAB 4: TOGGLES EXPLAINED
    # ========================================================================
    with tab4:
        st.markdown("## 📊 Understanding Your Results")
        
        st.markdown("### The YPA Trinity")
        st.write("""
        Every audit reports scores under **three weighting scenarios**. 
        This reveals how frameworks are optimized for different purposes.
        """)
        
        st.markdown("""
            <div class="lever-card">
            <h4>🔵 Neutral Scenario</h4>
            <p><b>Weighting:</b> All levers 1×</p>
            <p><b>Purpose:</b> Baseline comparison</p>
            <p><b>What it shows:</b> General-purpose efficiency</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="lever-card">
            <h4>🟣 Existential Scenario</h4>
            <p><b>Weighting:</b> 2× EDB, 2× MG</p>
            <p><b>Purpose:</b> Meaning/purpose focus</p>
            <p><b>What it shows:</b> Which framework better addresses "Why?" questions</p>
            <p><b>Typical winner:</b> Comprehensive worldviews (CT)</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="lever-card">
            <h4>🟢 Empirical Scenario</h4>
            <p><b>Weighting:</b> 2× PF, 1.5× CCI</p>
            <p><b>Purpose:</b> Prediction/tech focus</p>
            <p><b>What it shows:</b> Which framework generates practical success</p>
            <p><b>Typical winner:</b> Scientific methods (MdN)</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### The Guardrails")
        st.write("**Automated checks that flag suspicious patterns:**")
        
        st.markdown("""
            <div class="tip-box">
            <b>1. Lever-Coupling:</b> If PF ≥ 9, requires CCI ≥ 6.5<br/>
            <i>High success must be backed by coherent foundations</i>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="tip-box">
            <b>2. BFI-Sensitivity:</b> Flags if ΔYPA / ΔBFI > 0.4<br/>
            <i>Efficiency shouldn't increase as you add axioms</i>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="tip-box">
            <b>3. Weight-Inversion:</b> Flags if any lever <0.3× or >3×<br/>
            <i>Prevents cherry-picking extreme scenarios</i>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
            <div class="tip-box">
            <b>4. Symmetry Audit:</b> Tests 3 toggle inversions, flags Δ > 0.3<br/>
            <i>Large impacts reveal structural dependencies</i>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Interpreting the Symmetry Tab")
        
        st.markdown("""
        The Symmetry Audit shows how each framework responds to toggle changes:
        
        - **✅ Green (Δ < 0.3)**: Small impact, framework is robust to this config
        - **⚠️ Yellow (Δ > 0.3)**: Large impact, framework depends on this setting
        
        **Important**: Large impacts aren't "bad" - they reveal **structural dependencies**. 
        The key is **disclosure**: you can see exactly how your choices affect results.
        """)
    
    # ========================================================================
    # TAB 5: READING RESULTS
    # ========================================================================
    with tab5:
        st.markdown("## 📊 Reading Results")
        st.markdown("*How to interpret YPA outcomes*")

        st.markdown("""
            <div class="info-card">
            <h3>The Trinity Scores</h3>
            <p>Every comparison shows 3 scenarios:</p>
            <ul>
                <li><b>Neutral:</b> Baseline (all weights 1×)</li>
                <li><b>Existential:</b> Meaning-focused (2× EDB, 2× MG)</li>
                <li><b>Empirical:</b> Tech-focused (2× PF, 1.5× CCI)</li>
            </ul>
            <p><b>Why?</b> Different contexts demand different priorities. See how frameworks perform under various pressures.</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("""
            <div class="tip-box">
            💡 <b>Key Insight:</b> Don't just look at who "wins" - look at the <i>pattern</i> across scenarios.
            A framework that dominates in all 3 scenarios is universally strong. One that only wins in Existential
            reveals its niche.
            </div>
        """, unsafe_allow_html=True)

    # ========================================================================
    # TAB 6: PRO TIPS
    # ========================================================================
    with tab6:
        st.markdown("## 💡 Pro Tips & Best Practices")
        
        st.markdown("""
            <div class="highlight-box">
            🎯 How to get the most out of CFA
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 1. Don't Look for Winners")
        st.markdown("""
            <div class="tip-box">
            CFA is designed to reveal <b>trade-offs</b>, not declare victors.
            
            If one framework dominates across all scenarios, something's probably wrong with your scoring.
            
            <i>Good audits show: "Framework X wins here, Framework Y wins there, here's why"</i>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 2. Use the Preset Buttons")
        st.write("""
        The **MAX/MID/RESET/MIN** buttons under each framework let you:
        - Test extremes quickly
        - Reset to defaults easily
        - Explore the scoring space
        
        Try setting one framework to MAX and the other to MID - what happens?
        """)
        
        st.markdown("### 3. Flip the Toggles")
        st.markdown("""
            <div class="tip-box">
            The real power of CFA is in the toggles.
            
            Try this experiment:
            1. Start with default config (Parity ON, Composite PF, etc.)
            2. Note the YPA scores
            3. Flip Parity OFF
            4. Watch CT's score drop ~0.8 YPA
            
            <b>Question:</b> Is this bias against CT, or honest measurement of structural dependency?
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### 4. Check the Brute Ledger")
        st.write("""
        Visit the **🔍 Brute Ledger** page to see:
        - Full axiom/debt lists for MdN and CT
        - Why each framework requires its starting assumptions
        - Audit notes from Claude + Grok perspectives
        
        Understanding the BFI makes the YPA scores make sense.
        """)
        
        st.markdown("### 5. Export Your Runs")
        st.write("""
        Use the **📥 Export Run (JSON)** button at the bottom of the console to save:
        - Your configuration
        - Your lever scores
        - The calculated YPA Trinity
        
        Share your runs with others! Compare interpretations!
        """)
        
        st.markdown("### 6. Remember the Pointing Rule")
        st.markdown("""
            <div class="info-card">
            <h3>"To name your brute is to pay your fee"</h3>
            <p>Every framework starts with unprovable assumptions.</p>
            <p>The question isn't whether you have them.</p>
            <p>The question is whether you're honest about them.</p>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        st.markdown("### Need More Help?")
        st.write("""
        - **Full Documentation**: Download the PDF manual (link at top)
        - **Brute Ledger**: Visit 🔍 Brute Ledger page for axiom/debt lists
        - **About Page**: Read the complete 4-level audit story
        - **Console Tooltips**: Hover over any toggle or lever for inline help
        """)
    
    # ========================================================================
    # FOOTER
    # ========================================================================
    st.markdown("---")
    st.markdown("""
        <div style="text-align: center; color: #666; padding: 1rem;">
        <p>CFA v4.0 | "All Named, All Priced" | October 2025</p>
        <p><i>Where ideas reveal their true weight, and honesty becomes quantifiable.</i></p>
        </div>
    """, unsafe_allow_html=True)
