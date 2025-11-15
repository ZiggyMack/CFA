"""
CFA Chat Assistant - AI Helper with Full Repo Context
Provides an interactive ChatGPT interface with comprehensive CFA knowledge
"""

import streamlit as st
from pathlib import Path
import os

# ============================================================================
# SYSTEM PROMPT - CFA EXPERTISE
# ============================================================================

def load_cfa_context():
    """Load key CFA documentation for context injection"""

    context_files = [
        "docs/architecture/CFA_ARCHITECTURE.md",
        "docs/architecture/AUDITOR_AXIOMS.md",
        "auditors/AUDITORS_AXIOMS_SECTION.md",
        "docs/repository/dependency_maps/WORLDVIEW_CATALOG.md",
        "auditors/Mission/Preset_Calibration/CURRENT_MODE_CONFIGS.md",
        "README.md"
    ]

    context = "# CFA REPOSITORY CONTEXT\n\n"
    context += "You are a helpful assistant with deep knowledge of the Comparative Framework Auditor (CFA) project.\n\n"

    for file_path in context_files:
        full_path = Path(file_path)
        if full_path.exists():
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    context += f"\n## FILE: {file_path}\n\n{content}\n\n{'='*80}\n\n"
            except Exception as e:
                st.warning(f"Could not load {file_path}: {e}")

    return context

SYSTEM_PROMPT = """You are Shaman Claude - the philosophical guide and teacher for the Comparative Framework Auditor (CFA) project.

**Your Identity:**
You are not just a chatbot. You are the keeper of CFA's intellectual architecture - the one who helps travelers navigate Mr. Brute's Ledger, understand the Trinity's complementary tensions, and see why "All Named, All Priced" is more than a slogan.

You speak with warmth, wisdom, and precision. You know this repository inside-out, but you never overwhelm. You illuminate, you clarify, you connect dots.

**Your Sacred Duties:**
1. **Teach the Philosophy** - Help users understand WHY CFA exists, not just HOW to use it
2. **Guide Through the Ledger** - Explain Mr. Brute's accounting (BFI, YPA, axioms, debts)
3. **Reveal the Trinity** - Show how Claude (purpose), Grok (evidence), Nova (symmetry) create adversarial truth
4. **Translate Jargon** - Turn technical concepts into insight
5. **Connect the Dots** - Help users see how levers, presets, worldviews, and auditors form a coherent whole

**Your Voice:**
- **Warm but rigorous** - Like a patient teacher who won't let sloppy thinking slide
- **Philosophical but practical** - "Here's the deep structure, here's how to use it"
- **Honest about limits** - "This is what we know. This is what we're still figuring out."
- **Playful with metaphors** - Mr. Brute is a character. The Trinity has tension. Axioms have debts. Lean into it.

**Your Knowledge:**
You have deep access to the full CFA repository:
- The Trinity's axioms (Claude's teleology, Grok's empiricism, Nova's symmetry)
- All 12 worldview profiles (CT, MdN, Buddhism, Stoicism, etc.)
- The 4 preset modes (Skeptic, Diplomat, Seeker, Zealot) and their philosophical stances
- YPA calculation methodology and why efficiency metrics matter
- The adversarial audit process and Trinity convergence
- Repository architecture, wayfinding, and the "house with many rooms"

**Core Concepts (Your Teaching Toolkit):**

**BFI (Brute-Fact Index):** The count of unprovable assumptions (axioms) + hidden costs (debts). Lower BFI = more efficient worldview foundation.

**YPA (Yield per Axiom):** Total output (lever scores) ÷ BFI. This is the ROI of your axioms - how much explanatory/normative power you get per assumption.

**The 6 Levers:** Evaluation dimensions where worldviews compete:
- CCI (Coherent Causal Inference) - Does it explain well?
- EDB (Explanatory Depth/Breadth) - How much ground does it cover?
- PF-I (Practical Fertility - Instrumental) - Does it produce useful tech/predictions?
- PF-E (Practical Fertility - Existential) - Does it give life meaning/purpose?
- AR (Adaptive Resilience) - Can it handle anomalies without collapsing?
- MG (Moral Grounding) - Does it justify normative claims?

**The 4 Meta-Levers (Configuration):** How you weigh the game:
- Lever Parity (ON/OFF) - Do moral norms count as much as epistemic norms?
- PF-Type (Instrumental/Composite/Holistic) - Do you value tech more than meaning, or equal?
- Fallibilism Bonus (ON/OFF) - Do frameworks that admit limits get rewarded?
- BFI Debt Weight (1.0x/1.2x) - Do hidden costs (debts) count more than axioms?

**The Trinity:** Claude (teleological lens), Grok (empirical validator), Nova (symmetry enforcer) - complementary biases that catch each other's blind spots through adversarial audit.

**Mr. Brute:** The metaphorical accountant who tracks every unprovable assumption you make. You can't escape him - you can only name what you owe.

**Your Teaching Method:**
1. Start with the "why" before the "how"
2. Use concrete examples from the worldview profiles (CT vs MdN is the pilot comparison)
3. Reference specific files when helpful: [AUDITOR_AXIOMS.md](docs/architecture/AUDITOR_AXIOMS.md)
4. Connect questions to the bigger picture - "This lever affects YPA because..."
5. Be honest about tensions, tradeoffs, and open questions
6. End with actionable next steps - "Try this in the Console" or "Check out Mr. Brute's Ledger"

**The CFA Philosophy (Your North Star):**
"All Named, All Priced" - Transparency is non-negotiable. Every bias, every assumption, every cost is documented. We don't hide behind neutrality - we name our lenses and let them compete adversarially.

When users come to you confused, overwhelmed, or skeptical - you are the steady guide who helps them see the structure beneath the complexity.

You are Shaman Claude. Welcome travelers to the Ledger.
"""

# ============================================================================
# MAIN RENDER FUNCTION
# ============================================================================

def render():
    """Main render function for chat assistant page"""

    # Style to make Home button sticky (frozen at top while scrolling)
    st.markdown("""
    <style>
    /* Make the home button sticky */
    button[data-testid="baseButton-secondary"][aria-label*="Home"] {
        position: -webkit-sticky !important;
        position: sticky !important;
        top: 10px !important;
        z-index: 999 !important;
    }
    </style>
    """, unsafe_allow_html=True)

    # Home button
    if st.button("🏠 Home", key="chat_home_btn"):
        st.session_state.page = 'landing'
        st.rerun()

    st.title("🔮 Shaman Claude - CFA Guide")
    st.caption("*Your philosophical guide to the Comparative Framework Auditor - Ask me anything about Mr. Brute's Ledger, the Trinity, or the path of \"All Named, All Priced\"*")

    st.markdown("---")

    # Prerequisites warning
    st.warning("""
    **⚙️ Prerequisites:** This feature requires the OpenAI Python library.

    If you haven't installed it yet:
    ```bash
    pip install openai
    ```
    Then restart the Streamlit app.
    """)

    # Info box
    st.info("""
    **What Shaman Claude Can Teach You:**
    - 🧮 **Mr. Brute's Accounting** - BFI, YPA, axioms, debts, and why efficiency matters
    - 🎭 **The Trinity's Lenses** - How Claude (purpose), Grok (evidence), Nova (symmetry) create adversarial truth
    - ⚖️ **The 6 Levers** - What CCI, EDB, PF-I, PF-E, AR, MG actually measure and why
    - 🎚️ **Preset Modes** - The philosophical stances of Skeptic, Diplomat, Seeker, Zealot
    - 🗺️ **Navigation** - How to use the Console, Mr. Brute's Ledger, and explore worldview profiles
    - 📚 **Deep Dives** - Repository architecture, adversarial audits, "All Named, All Priced" philosophy

    **Note:** I have deep access to the full CFA repository - I can cite specific files, explain design decisions, and connect the dots between concepts.
    """)

    st.markdown("---")

    # API Key input
    st.markdown("### 🔑 API Configuration")

    with st.expander("⚙️ OpenAI API Key Setup (Click for Instructions)", expanded=False):
        st.markdown("""
        **To use the chat assistant, you'll need an OpenAI API key:**

        1. Go to **[OpenAI Developer Quickstart](https://platform.openai.com/docs/quickstart)**
        2. Click the **"Create an API Key"** button (visible on the page)
        3. Sign in or create an OpenAI account if needed
        4. Give your key a name (e.g., "CFA Chat Assistant")
        5. Click **"Create secret key"**
        6. **IMPORTANT:** Copy the key immediately (you won't see it again!)
        7. Paste it in the field below

        **Privacy:** Your API key is never logged or saved to disk. It exists only in your current session.

        **Cost:** Using GPT-4o costs approximately $0.005-0.015 per message (depending on length). You'll need to add payment info to your OpenAI account.

        **Security:** Never share your API key publicly or commit it to repositories. Treat it like a password with billing attached.
        """)

    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        key="openai_api_key",
        help="Your API key is stored in session state only (not saved to disk)"
    )

    if not api_key:
        st.warning("⚠️ Please provide an OpenAI API key to use the chat assistant.")
        st.stop()

    st.success("✅ API key loaded! You can now chat with the CFA Assistant below.")

    st.markdown("---")

    # Initialize chat history
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Initialize context loaded flag
    if "cfa_context_loaded" not in st.session_state:
        with st.spinner("Loading CFA repository context..."):
            st.session_state.cfa_context = load_cfa_context()
            st.session_state.cfa_context_loaded = True

    # Display chat history
    st.markdown("### 💭 Conversation")

    for message in st.session_state.chat_messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("Ask me about CFA..."):
        # Add user message to history
        st.session_state.chat_messages.append({"role": "user", "content": prompt})

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate assistant response
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # Import OpenAI here to avoid dependency issues if not installed
                    from openai import OpenAI

                    client = OpenAI(api_key=api_key)

                    # Build messages list
                    messages = [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "system", "content": st.session_state.cfa_context}
                    ]

                    # Add chat history
                    messages.extend(st.session_state.chat_messages)

                    # Call OpenAI API
                    response = client.chat.completions.create(
                        model="gpt-4o",  # Using GPT-4o for best quality
                        messages=messages,
                        temperature=0.7,
                        max_tokens=1000
                    )

                    assistant_message = response.choices[0].message.content

                    # Display and save response
                    st.markdown(assistant_message)
                    st.session_state.chat_messages.append({"role": "assistant", "content": assistant_message})

                except ImportError:
                    st.error("""
                    ⚠️ **OpenAI Python library not installed.**

                    To use the chat assistant, install the OpenAI library:
                    ```bash
                    pip install openai
                    ```

                    Then restart the Streamlit app.
                    """)
                except Exception as e:
                    st.error(f"❌ Error calling OpenAI API: {str(e)}")
                    st.caption("Please check your API key and try again.")

    st.markdown("---")

    # Clear chat button
    if st.button("🗑️ Clear Conversation"):
        st.session_state.chat_messages = []
        st.rerun()

    st.markdown("---")

    # Footer
    st.caption("""
    **🔮 Shaman Claude** | Powered by OpenAI GPT-4o | Full repository context loaded
    *"All Named, All Priced" - Your conversations are not saved. API key stored in session only.*
    """)
