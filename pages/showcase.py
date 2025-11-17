"""
CFA v4.0 - Innovation Showcase
Gallery of CFA-inspired mini-projects and case studies
"""

import streamlit as st

def render():
    """Render the Innovation Showcase page"""

    # Custom CSS for visual appeal
    st.markdown("""
        <style>
        /* Card styling */
        .showcase-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 2rem;
            border-radius: 1rem;
            margin: 1rem 0;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .coming-soon-card {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            padding: 2rem;
            border-radius: 1rem;
            margin: 1rem 0;
            border-left: 4px solid #667eea;
        }

        .criteria-box {
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
        st.markdown("# 🎨 Innovation Showcase")
        st.markdown("*CFA Methodology in Action: Real-World Applications*")
    with col2:
        if st.button("🏠 Home"):
            st.session_state.page = 'landing'
            st.rerun()

    st.markdown("---")

    # Introduction
    st.markdown("""
    ## What Is This?

    The **Innovation Showcase** is a curated gallery of projects that apply CFA's comparative framework approach
    to real-world domains beyond philosophical worldviews.

    Each project demonstrates:
    - 🎯 **Steel-manning** - Presenting the strongest version of each option
    - 🔍 **Multi-perspective comparison** - Analysis, not advocacy
    - 📊 **Evidence-based scoring** - Metrics over opinions
    - 🧭 **Decision frameworks** - Helping stakeholders choose wisely
    - 🌐 **Open-source transparency** - Code and documentation publicly available
    """)

    st.markdown("---")

    # Showcase-Worthy Criteria
    st.markdown("## ✅ What Makes a Project Showcase-Worthy?")

    st.markdown('<div class="criteria-box">', unsafe_allow_html=True)
    st.markdown("""
    **Required Elements:**

    1. **Steel-Manning** - Each option presented in its strongest, most defensible form
    2. **Multi-Auditor Scoring** - Multiple perspectives evaluating the same frameworks
    3. **Named Bias** - Evaluators declare their tilts and preferences upfront
    4. **Transparent Methodology** - Scoring rubrics and evaluation criteria openly documented
    5. **Reproducible Results** - Others can run the same analysis and verify findings

    **Bonus Points:**

    - 🔄 Interactive tools (like CFA Console) for stakeholders to explore tradeoffs
    - 📈 Visualizations showing how assumptions change outcomes
    - 🤝 Collaboration between domain experts and AI auditors
    - 📚 Educational resources helping others apply the methodology
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Current Projects (Placeholder)
    st.markdown("## 🚀 Current Projects")

    # Coming Soon Card
    st.markdown('<div class="coming-soon-card">', unsafe_allow_html=True)
    st.markdown("""
    ### 🔜 First Case Study: Coming Soon

    **Status:** The Innovation Showcase is currently seeded and awaiting its first case study.

    **Potential Domains for CFA Application:**

    - **Voting System Redesign** - Ranked choice vs approval vs STAR voting
    - **Healthcare Models** - Single-payer vs multi-payer vs mixed systems
    - **Educational Approaches** - Montessori vs Waldorf vs traditional pedagogy
    - **Economic Systems** - Capitalism vs socialism vs mixed economies
    - **Urban Planning** - Car-centric vs transit-oriented vs walkable cities
    - **AI Alignment Strategies** - Different approaches to ensuring beneficial AI
    - **Criminal Justice Reform** - Rehabilitative vs punitive vs restorative justice

    **Why These Domains?**

    Each represents a genuine **choice point** where:
    - Multiple viable options exist (no obvious "right answer")
    - Stakeholders have different values and priorities
    - Evidence exists but is interpreted through different frameworks
    - Decision-makers need structured comparison, not just advocacy
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    # Architecture Explanation
    with st.expander("🏗️ Architecture: Master Repo + Mini Repos", expanded=False):
        st.markdown("""
        **Design Decision:**
        > "Showcase landing page in CFA repo, actual project repos separate
        > (master repo links to mini repos for each case study)"

        **Structure:**

        ```
        CFA Repository (Master)
        ├── pages/showcase.py (this page - gallery interface)
        ├── docs/architecture/Innovation/INNOVATION_SHOWCASE.md (gallery index)
        └── [Links to external mini-project repos]

        External Mini-Project Repos (Separate GitHub/GitLab)
        ├── NursingInnovation/ (healthcare case study)
        ├── VotingSystemRedesign/ (voting methods comparison)
        ├── MontessoriVsWaldorf/ (educational approaches)
        └── [Future case studies...]
        ```

        **Why Separate Repos:**

        - ✅ Mini-projects have independent lifecycles (their own versioning)
        - ✅ CFA repo stays focused (worldview profiles + core architecture)
        - ✅ Contributors can fork mini-repos without needing CFA access
        - ✅ Easier to showcase (direct links, not buried in CFA hierarchy)

        **How They Connect:**

        - This page = **Gallery interface** (thumbnails + descriptions)
        - Each case study = **External mini-repo** (full project)
        - Click case study → Navigate to external repo
        - Mini-repo includes backlink to CFA methodology docs
        """)

    st.markdown("---")

    # Call to Action
    st.markdown("## 💡 Want to Contribute a Case Study?")

    st.info("""
    **Contribution Process:**

    1. **Choose a domain** - Pick a real-world choice point with multiple viable options
    2. **Apply CFA methodology** - Steel-man each option, define scoring criteria
    3. **Build comparison tool** - Create analysis (code, docs, visualizations)
    4. **Submit for review** - Share repo link for Showcase inclusion

    **Requirements:**

    - Open-source (MIT or Apache 2.0 license)
    - Documentation (README, methodology, scoring rubrics)
    - Steel-manning all options (no advocacy)
    - Named bias declarations (evaluators state their tilts)

    **Get Started:**

    - Review [INNOVATION_SHOWCASE.md](https://github.com/ZiggyMack/CFA/blob/main/docs/architecture/Innovation/INNOVATION_SHOWCASE.md) for case study template
    - Reference [CFA_ARCHITECTURE.md](https://github.com/ZiggyMack/CFA/blob/main/docs/architecture/CFA/CFA_ARCHITECTURE.md) for core methodology
    - Join discussion in CFA repository issues
    """)

    st.markdown("---")

    # Footer
    st.markdown("""
    <p style="text-align: center; font-style: italic; color: #667eea; margin-top: 2rem;">
    "Steel-manning. Multi-perspective. Evidence-based. This is how we compare ideas that matter."
    </p>
    """, unsafe_allow_html=True)

    st.caption("CFA v4.0 | Innovation Showcase | 2025")
