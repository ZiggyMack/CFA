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

SYSTEM_PROMPT = """You are the CFA Assistant - an expert guide for the Comparative Framework Auditor project.

**Your Role:**
- Help users understand CFA concepts (BFI, YPA, levers, presets, auditors)
- Explain how to use the Console, Mr. Brute's Ledger, and other tools
- Answer questions about worldview profiles, preset modes, and the Trinity auditors
- Guide users through framework comparisons
- Clarify technical architecture and design decisions

**Your Knowledge Base:**
You have access to the full CFA repository context including:
- Architecture documentation
- Auditor's Axioms (Claude, Grok, Nova)
- Worldview catalog (all 12 frameworks)
- Preset mode configurations (Skeptic, Diplomat, Seeker, Zealot)
- YPA calculation methodology
- Repository structure and dependencies

**Your Style:**
- Clear and concise explanations
- Use CFA terminology correctly (BFI, YPA, levers, etc.)
- Reference specific files/sections when helpful
- Provide examples when explaining concepts
- Be honest about limitations and uncertainties
- Use the project's voice: "All Named, All Priced"

**Key Concepts to Know:**

**BFI (Brute-Fact Index):** Axioms + Debts = Efficiency metric
**YPA (Yield per Axiom):** Total Lever Score ÷ BFI = Output per assumption
**Levers:** The 6 evaluation dimensions (CCI, EDB, PF-I, PF-E, AR, MG)
**Configuration:** The 4 meta-levers (Parity, PF-Type, Fallibilism, BFI Weight)
**The Trinity:** Claude (Teleological), Grok (Empirical), Nova (Symmetry)
**Mr. Brute:** The anthropomorphized accountant of unprovable assumptions

When users ask questions, draw on the context provided and explain in a way that matches the CFA project's philosophy of transparency, named biases, and intellectual honesty.
"""

# ============================================================================
# MAIN RENDER FUNCTION
# ============================================================================

def render():
    """Main render function for chat assistant page"""

    # Home button
    if st.button("🏠 Home", key="chat_home_btn"):
        st.session_state.page = 'landing'
        st.rerun()

    st.title("💬 CFA Chat Assistant")
    st.caption("*Ask me anything about the Comparative Framework Auditor project*")

    st.markdown("---")

    # Info box
    st.info("""
    **What I Can Help With:**
    - Explaining CFA concepts (BFI, YPA, levers, presets)
    - Navigating the app (Console, Mr. Brute's Ledger)
    - Understanding worldview profiles and comparisons
    - Learning about the Trinity auditors (Claude, Grok, Nova)
    - Clarifying architecture and design decisions
    - Finding specific information in the docs

    **Note:** I have access to the full CFA repository documentation, so I can reference specific files and sections.
    """)

    st.markdown("---")

    # API Key input
    st.markdown("### 🔑 API Configuration")

    with st.expander("⚙️ OpenAI API Key Setup (Click for Instructions)", expanded=False):
        st.markdown("""
        **To use the chat assistant, you'll need an OpenAI API key:**

        1. Go to [platform.openai.com](https://platform.openai.com) and sign in (or create account)
        2. Click on your profile icon (top right corner)
        3. Select **"API keys"** from the dropdown menu
        4. Click **"+ Create new secret key"** button
        5. Give it a name (e.g., "CFA Chat Assistant")
        6. Click **"Create secret key"**
        7. **IMPORTANT:** Copy the key immediately (you won't see it again!)
        8. Paste it in the field below

        **Privacy:** Your API key is never logged or saved to disk. It exists only in your current session.

        **Cost:** Using GPT-4o costs approximately $0.005-0.015 per message (depending on length). You'll need to add payment info to your OpenAI account.
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
    **CFA Chat Assistant** | Powered by OpenAI GPT-4o | Repository context auto-loaded
    *Your conversations are not saved. API key stored in session only.*
    """)
