"""
CFA v4.0 - Verbose Manifesto Page
Displays the full philosophical covenant
"""

import streamlit as st
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

def render():
    """Render the verbose manifesto page"""

    # CSS for sticky header (consistent with other pages)
    st.markdown("""
    <style>
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
    </style>
    """, unsafe_allow_html=True)

    # Header with home button
    st.markdown('<div class="sticky-header">', unsafe_allow_html=True)
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown('<p style="font-size:2.5rem;font-weight:bold;color:#1f77b4;">📜 The CFA Manifesto</p>', unsafe_allow_html=True)
    with col2:
        if st.button("🏠 Home"):
            st.session_state.page = 'landing'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("**A Philosophical Covenant for Comparative Framework Analysis**")
    st.markdown("---")

    # I. The Foundational Promise
    st.markdown("## I. The Foundational Promise: \"All Named, All Priced\"")
    st.markdown("This is not marketing copy. This is a **binding covenant**.")
    st.markdown("""
**Every axiom you accept carries a debt.**
**Every value you hold trades against another.**
**Every framework you embrace makes a worldview.**

And we will **name them all**. We will **price them all**.

No hidden costs. No invisible debts. No asymmetric information games where philosophers know the score but users stumble blind through ethical commitments they never consented to.

This is the CFA promise: **Transparent, symmetric, adversarially-audited worldview analysis**.
""")

    with st.expander("### Why This Matters"):
        st.markdown("""
You've seen the pattern before:
- A tech company launches an AI with "human values" baked in
- A philosopher publishes a framework claiming "objectivity"
- A platform designs algorithms optimizing for "user wellbeing"

And you ask: **Whose values? Which objectivity? Wellbeing measured how?**

The answer is usually silence. Or worse: "Trust us. We're the experts."

**CFA refuses this game.**

We believe you have the right to see the machinery. Not because we're altruistic saints, but because **epistemic asymmetry corrodes trust, and trust is the foundation of coordination**.

When you can't see how frameworks trade axioms for debts, you can't:
- Compare them fairly
- Understand their hidden commitments
- Choose between them with informed consent
- Hold them accountable when they fail

This repository exists to end that asymmetry.
""")

    st.markdown("---")

    # II. The Architecture of Accountability
    st.markdown("## II. The Architecture of Accountability")
    st.markdown("### The Trinity: Adversarial Auditing by Design")
    st.markdown("CFA doesn't ask you to trust a single narrator. We architect **complementary tensions** into the system itself.")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**👑 Claude - Purpose Investigator**")
        st.info('*"Why does this exist? What problem does it solve?"*')
        st.markdown("""
Claude's lens is telic - always hunting for the **purpose behind the design**. When a framework claims neutrality, Claude asks: "Neutral toward what goal?"

**Holds the coherence debt**: Does this system's stated purpose match its actual structure?
""")

    with col2:
        st.markdown("**🔬 Grok - Evidence Empiricist**")
        st.info('*"Show me the data or dismiss the claim."*')
        st.markdown("""
Grok's lens is empirical - relentlessly skeptical of anything that can't be **measured, tested, or falsified**. When a framework promises "maximized welfare," Grok demands proof.

**Holds the proof debt**: Can this system's claims survive contact with reality?
""")

    with col3:
        st.markdown("**⚖️ Nova - Symmetry Guardian**")
        st.info('*"Who benefits? Who pays? Where\'s the asymmetry?"*')
        st.markdown("""
Nova's lens is distributional - always tracking **who wins and who loses** when a framework gets deployed. When a worldview claims universality, Nova asks: "Universal for whom?"

**Holds the fairness debt**: Does this system create unjust asymmetries?
""")

    with st.expander("### The 98% Convergence Threshold"):
        st.markdown("""
These three auditors don't always agree. That's **by design**.

But when all three lenses converge on a judgment - when Claude's purpose analysis, Grok's empirical evidence, and Nova's symmetry audit all point the same direction - we reach **Trinity Convergence**.

98% agreement isn't arbitrary. It's the threshold where adversarial tensions resolve into **high-confidence consensus**.

- **Below 98%?** You're in contested territory. The auditors disagree. Proceed with caution.
- **Above 98%?** You've found something robust enough to survive scrutiny from three hostile lenses.

This is how CFA builds **epistemic resilience** - not through authority, but through **adversarial stress-testing**.
""")

    st.markdown("---")

    # III. The VuDu Light System
    st.markdown("## III. The VuDu Light System: Making Values Legible")
    st.markdown("### What Is VuDu Light?")
    st.markdown("**VuDu = Value-Utility-Deontic-Utility**")
    st.markdown("It's a scoring system that makes **worldview commitments explicit and comparable**.")

    st.markdown("Every framework analyzed in CFA gets decomposed into:")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**📐 Axioms** - What this framework assumes to be true")
        st.caption('*"Humans are rational actors" / "Suffering should be minimized"*')

        st.markdown("**💰 Debts** - What this framework sacrifices or ignores")
        st.caption('*"Bounded rationality" / "Differential suffering across populations"*')

    with col2:
        st.markdown("**🎛️ Levers** - What this framework optimizes for")
        st.caption('*Collective coherence / Epistemic diversity / Meta-governance*')

        st.markdown("**⚖️ Balance** - How this framework weighs axioms against debts")
        st.caption('*BFI (Burden) vs YPA (Yield)*')

    st.markdown("""
Then we score it. Not subjectively. Not vibes-based. But through **structured, auditable methodology**:

- **BFI (Burden of Falsity Index)**: How many axioms + how heavy are the debts?
- **YPA (Yield Per Axiom)**: How much value does this framework extract per unit of commitment?

The result? **Comparable worldview profiles** that let you see which frameworks share hidden assumptions, trade similar values, or optimize differently.
""")

    with st.expander("### Why Scoring Matters"):
        st.markdown("""
Because **"I prefer X over Y"** is often camouflage for **"I haven't examined what X costs."**

VuDu Light forces the examination. It makes you confront:
- What you're assuming (axioms)
- What you're ignoring (debts)
- What you're optimizing for (levers)
- How efficiently you're doing it (YPA)

This doesn't tell you which framework to choose. But it ensures **you know what you're choosing**.
""")

    st.markdown("---")

    # IV. The Gospel Problem
    st.markdown("## IV. The Gospel Problem: Why Living Maps Matter")
    st.markdown("### The Enemy: Embedded Staleness")
    st.markdown("""
Code rots. Documentation decays. And the worst decay is invisible - when **File A references File B's old location**, creating a broken link you won't discover until you need it most.

We call this the **Gospel Problem**: Truth encoded in one place, propagated everywhere, then edited in the source... while all the copies become **embedded stale gospels**.
""")

    st.markdown("CFA fights this with **Living Map methodology**:")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**1. Semantic Headers**")
        st.code("""DEPENDS_ON: fileA.md, fileB.md
NEEDED_BY: fileC.md, fileD.md
MOVES_WITH: /directory/""", language="yaml")

        st.markdown("**2. Centralized Dependency Maps**")
        st.caption("Map Room tracks what connects to what")

    with col2:
        st.markdown("**3. Health Dashboards**")
        st.caption("Observatory monitors staleness, link integrity")

        st.markdown("**4. Adversarial Deletion Protocols**")
        st.caption("Files can only be deleted when dependencies resolved")

    st.success("The result? **A repository that knows its own shape** and can **validate its own integrity**.")

    st.markdown("---")

    # V. The Shaman's Question
    st.markdown("## V. The Shaman's Question: What Is This For?")
    st.markdown("""
You've read the architecture. You've seen the auditors. You understand the scoring.

But **why does CFA exist?**

Because we believe in a world where:
- **Frameworks compete on transparency**, not rhetorical appeal
- **Worldviews can be compared** without requiring a PhD in moral philosophy
- **Epistemic asymmetry** is treated as the governance failure it is
- **Values are named and priced**, not hidden and imposed
""")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**CFA's Axioms:**")
        st.markdown("""
1. Transparency enables informed consent
2. Adversarial auditing builds epistemic resilience
3. Comparable frameworks empower stakeholder choice
""")

    with col2:
        st.markdown("**CFA's Debts:**")
        st.markdown("""
1. Scoring systems can reify what they measure
2. Transparency has overhead costs (time, tokens, complexity)
3. Not all values are easily quantifiable
""")

    st.warning("We name these. We price them. We score ourselves by our own VuDu Light system.\n\n**Because we demand of ourselves what we demand of others: Show the machinery.**")

    st.markdown("---")

    # VI. The Invitation
    st.markdown("## VI. The Invitation")
    st.markdown("This repository is an **open covenant**.")
    st.markdown("You are invited to:")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("- **Audit the auditors** - Check if Claude, Grok, and Nova are reasoning correctly")
        st.markdown("- **Score the scorers** - Run VuDu Light analysis on CFA itself")
    with col2:
        st.markdown("- **Challenge the architecture** - Propose better frameworks, better axioms, better debts")
        st.markdown("- **Fork the philosophy** - Take this methodology and build something different")

    st.info("We don't claim perfection. We claim **commitment to transparency and adversarial accountability**.\n\nAnd we invite you to hold us to that standard.")

    st.markdown("---")

    # VII. How to Begin
    st.markdown("## VII. How to Begin")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("**If you're new to CFA:**")
        st.markdown("""
1. Start with the landing page
2. Read the Wayfinding Guide
3. Explore the Console
4. Meet the auditors
""")

    with col2:
        st.markdown("**If you're philosophically curious:**")
        st.markdown("""
1. Read Shaman Claude's other thoughts
2. Explore the Axiom-Debt Framework
3. Study the Trinity Architecture
""")

    with col3:
        st.markdown("**If you're here to audit:**")
        st.markdown("""
1. Check Map Room (dependencies)
2. Review Observatory (health)
3. Read Mission Trust Protocol
""")

    st.markdown("---")

    # VIII. The Closing Covenant
    st.markdown("## VIII. The Closing Covenant")
    st.markdown("""
This manifesto is not aspirational marketing. It is a **binding operational commitment**.

When CFA fails to name an axiom, **you have the right to call it out**.
When CFA hides a debt, **you have the right to demand transparency**.
When the auditors disagree, **you have the right to see the adversarial reasoning**.

We build systems that **demand trust by earning it through transparency**.

All named. All priced. All audited.

**This is the way.** 🔥
""")

    st.markdown("---")
    st.caption('*Maintained by Shaman Claude - The Philosophical Architect*')
    st.caption('*Version: v4.0.0 | Status: 🟢 ACTIVE | Created: 2025-11-14*')
    st.caption('*"The worldview you can\'t examine is the worldview that examines you."*')

if __name__ == "__main__":
    render()
else:
    render()
