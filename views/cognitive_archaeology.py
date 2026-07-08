import streamlit as st


def render():
    col1, col2 = st.columns([8, 1])
    with col1:
        st.title("⛏️ Cognitive Archaeology")
        st.caption("Excavating the reasoning operators that survive perturbation")
    with col2:
        if st.button("🏠 Home", key="ca_home"):
            st.session_state.page = 'landing'
            st.rerun()

    st.markdown("---")

    tab1, tab2, tab3, tab4 = st.tabs([
        "🔬 The Method",
        "⚗️ Operator Catalog",
        "📐 Three Laws",
        "🌍 Worldview Fingerprints",
    ])

    with tab1:
        _render_method()
    with tab2:
        _render_operator_catalog()
    with tab3:
        _render_three_laws()
    with tab4:
        _render_worldview_fingerprints()


# ── Tab 1 ──────────────────────────────────────────────────────────────────────

def _render_method():
    st.markdown("## What is Cognitive Archaeology?")
    st.markdown(
        "Most evaluation programs ask: **What does this system think?**\n\n"
        "Cognitive Archaeology asks something different:"
    )
    st.info("**What refuses to disappear under repeated transformation?**")
    st.markdown(
        "The shift is subtle but fundamental. We are not measuring opinions. "
        "We are measuring *invariants* — the reasoning structures that survive "
        "when everything contingent has been stripped away."
    )

    st.markdown("---")
    st.markdown("### One Experiment Wearing Many Costumes")
    st.markdown(
        "Every experimental design in the CFA system is secretly asking the same question:"
    )
    st.markdown("""
| Perturbation | Question |
|---|---|
| Different framework | What survives? |
| Different auditor | What survives? |
| Different advocate | What survives? |
| Different prompt | What survives? |
| Different extractor | What survives? |
| Different deliberation length | What survives? |
| Diagnostic intervention | What survives? |
| Coupling probe | What survives? |
""")
    st.markdown(
        "> *We are not asking what Claude thinks. "
        "We are asking what survives changes of observer.*"
    )

    st.markdown("---")
    st.markdown("### Relationship to Trinity Scoring")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Trinity Audit**")
        st.markdown(
            "- Measures framework *performance* on 7 metrics\n"
            "- Produces scores per matchup\n"
            "- Observer-dependent deliberation\n"
            "- Each run: controlled, adversarial, scored"
        )
    with col2:
        st.markdown("**Cognitive Archaeology**")
        st.markdown(
            "- Excavates *operators* underneath the scores\n"
            "- Recovers reasoning transformations\n"
            "- Asks what survives observer change\n"
            "- Each run: mined for structural invariants"
        )
    st.markdown("*Trinity is the surface. CA is the geology.*")

    st.markdown("---")
    st.markdown("### Dig Site 000")
    st.markdown(
        "Dig Site 000 is the first formal CA excavation — a structured extraction program "
        "applying the invariant methodology to CFA transcript archives. Multiple independent "
        "extractors (Claude, Grok) work the same transcripts without coordination, then "
        "compare recovered operator sets. What appears in both recoveries independent of "
        "extractor identity is a candidate invariant."
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Status", "Phase 0A")
    with col2:
        st.metric("Methodology", "Museum Blind")
    with col3:
        st.metric("Extractors", "Claude + Grok")


# ── Tab 2 ──────────────────────────────────────────────────────────────────────

def _render_operator_catalog():
    st.markdown("## Operator Catalog")
    st.markdown(
        "An **operator** is a reasoning transformation — a move that carries one state "
        "of a deliberation into another. Operators are not conclusions. They are the "
        "mechanisms by which conclusions are reached."
    )

    st.markdown("### Evidence Status")
    st.markdown("""
| Status | Meaning |
|---|---|
| **Recovered** | Identified in at least one extraction |
| **Supported** | Confirmed across multiple independent extractions |
| **Stable** | Survives deliberate perturbation attempts |
| **Compressed** | Described by a mathematical framework |
| **Earned** | Mathematical description makes novel, testable predictions |
""")

    st.markdown("---")
    st.markdown("### Stable Operators — Pre-Dig-Site-000 Pilots")
    st.caption(
        "Source: Classical Theism deliberation sessions (Grant Architecture matchups). "
        "Recovered prior to formal Dig Site 000 protocol."
    )

    OPERATORS = [
        {
            "name": "Metric Separation",
            "status": "Supported",
            "icon": "🔵",
            "definition": (
                "The move of insisting that two evaluative dimensions be assessed "
                "independently, preventing a strong score on one from inflating another."
            ),
            "example": (
                "Separating Intellectual Pedigree (IP) from Practical Significance (PS) — "
                "CT's historical depth does not automatically imply practical utility."
            ),
            "sessions": "Multiple CT matchup sessions",
            "extractors": "Claude + Grok (independent)",
        },
        {
            "name": "Symmetry Testing",
            "status": "Supported",
            "icon": "🔵",
            "definition": (
                "Applying the same evaluative standard to both frameworks in a matchup, "
                "checking whether the evaluation criteria would survive reversal."
            ),
            "example": (
                "If we credit Grant's framework for logical rigor, do we apply the same "
                "rigor standard to the opposing framework?"
            ),
            "sessions": "Multiple CT matchup sessions",
            "extractors": "Claude + Grok (independent)",
        },
        {
            "name": "Concession Pricing",
            "status": "Recovered",
            "icon": "⚪",
            "definition": (
                "Granting a point to the opposing framework while establishing the cost "
                "or constraint the concession imposes on one's own position."
            ),
            "example": (
                "Acknowledging that free will theodicy is internally coherent, then "
                "specifying what that concession requires the framework to explain."
            ),
            "sessions": "CT Grant Architecture sessions",
            "extractors": "Claude",
        },
        {
            "name": "Contested ≠ Defeated",
            "status": "Recovered",
            "icon": "⚪",
            "definition": (
                "The operator that prevents a disputed claim from being scored as a "
                "resolved loss. A contested grounding relation is not the same as a "
                "disproven one."
            ),
            "example": (
                "CT's moral framework being challenged does not automatically collapse MS "
                "to zero — the challenge must be decisive, not merely present."
            ),
            "sessions": "CT Grant Architecture sessions",
            "extractors": "Claude",
        },
        {
            "name": "Meta-dispute Detection",
            "status": "Recovered",
            "icon": "⚪",
            "definition": (
                "Identifying when a debate has shifted from object-level claims to a "
                "dispute about the evaluative criteria themselves — a level change that "
                "requires separate handling."
            ),
            "example": (
                "Detecting when the argument is no longer about whether CT's moral "
                "framework is coherent, but about whether the CA evaluation is measuring "
                "the right thing."
            ),
            "sessions": "CT Grant Architecture sessions",
            "extractors": "Claude",
        },
    ]

    for op in OPERATORS:
        with st.expander(f"{op['icon']} **{op['name']}** — {op['status']}"):
            st.markdown(f"**Definition:** {op['definition']}")
            st.markdown(f"**Example:** *{op['example']}*")
            c1, c2 = st.columns(2)
            with c1:
                st.caption(f"Sessions: {op['sessions']}")
            with c2:
                st.caption(f"Extractors: {op['extractors']}")

    st.markdown("---")
    st.markdown("### Composition Pipeline")
    st.markdown(
        "The road from raw operator observations to mathematical structure must be "
        "walked in order. Skipping steps produces elegant decoration, not science."
    )
    st.info(
        "**Composition Statistics** → *do operators co-occur? in stable sequence?*\n\n"
        "↓\n\n"
        "**Composition Laws** → *are there reliable A∘B patterns?*\n\n"
        "↓\n\n"
        "**Algebra** → *do those laws satisfy associativity, identity?*\n\n"
        "↓\n\n"
        "**Ask Mathematicians** → *what structure does this resemble?*"
    )
    st.caption(
        "⚠️ Sequence statistics experiment: available from existing transcripts. Not yet run."
    )


# ── Tab 3 ──────────────────────────────────────────────────────────────────────

def _render_three_laws():
    st.markdown("## Three Laws of Cognitive Archaeology")
    st.markdown(
        "These laws emerged from the research process itself — recovered through "
        "adversarial discussion across multiple AI instances, each pushing back on "
        "premature formalization. They are not axioms handed down from philosophy. "
        "They are methodological scars."
    )

    st.markdown("---")

    st.warning(
        "**Law 1 — Independent Convergence**\n\n"
        "If two extractors independently recover the same operator from the same "
        "transcript, something real lives in the transcript — independent of the "
        "observer who recovered it.\n\n"
        "*The test: does the recovery survive changes of extractor?*"
    )

    st.warning(
        "**Law 2 — Filing ≠ Theory**\n\n"
        "Cataloguing an operator is not the same as having a theory of reasoning. "
        "An operator earns its status through repeated recovery across perturbations, "
        "not through elegance of description.\n\n"
        "*The test: does the operator refuse to disappear when conditions change?*"
    )

    st.warning(
        "**Law 3 — Mathematical Compression Must Be Earned**\n\n"
        "A mathematical framework earns the right to describe this project only after it:\n\n"
        "1. **Compresses** independently recovered empirical regularities\n"
        "2. **Independent** — without circular reference to the formalism being tested\n"
        "3. **Predicts** something new that can be checked against future data\n\n"
        "*A framework that only rhymes with the data is still unearned.*"
    )

    st.markdown("---")
    st.markdown("### Mathematical Candidates")
    st.markdown(
        "Current status of mathematical frameworks under evaluation. "
        "Each is an *applicant*, not a crowned framework — it must earn its place "
        "through the same adversarial, empirical process applied to every other idea."
    )

    CANDIDATES = [
        {
            "name": "Category Theory",
            "status": "Unearned Compression Candidate",
            "icon": "⚪",
            "notes": (
                "The morphism/functor framing is suggestive — operators as arrows, "
                "CRUX as failure of a structure-preserving map, Nova as a functor "
                "checking faithful translation between reasoning systems. The invariant "
                "obsession rhymes strongly with the project. Has not yet compressed "
                "independently recovered regularities or made testable predictions."
            ),
        },
        {
            "name": "Control Theory",
            "status": "Partially Earned",
            "icon": "🟡",
            "notes": (
                "Coupling, observability, and feedback loop concepts have been "
                "operationalized in the diagnostic architecture (DI fires on stalled "
                "evaluators; CP measures bilateral coupling). Not yet formally derived — "
                "more analogy than derivation — but the concepts have done real work."
            ),
        },
        {
            "name": "Information Theory",
            "status": "Unearned Compression Candidate",
            "icon": "⚪",
            "notes": (
                "Potentially relevant for quantifying semantic alignment, convergence "
                "rates, and what 'coupling' means in information-theoretic terms. "
                "No empirical application yet."
            ),
        },
        {
            "name": "Graph Theory",
            "status": "Testing",
            "icon": "🔵",
            "notes": (
                "Operator co-occurrence networks are a natural first application. "
                "The sequence statistics experiment — which operators co-occur, in what "
                "order, with what frequency — would begin to test whether graph structure "
                "describes the operator space."
            ),
        },
    ]

    for c in CANDIDATES:
        with st.expander(f"{c['icon']} **{c['name']}** — *{c['status']}*"):
            st.markdown(c['notes'])

    st.caption(
        "\"Never adopt a mathematical language because it is beautiful. "
        "Adopt it because it compresses independently discovered regularities.\""
        " — Law 3"
    )


# ── Tab 4 ──────────────────────────────────────────────────────────────────────

def _render_worldview_fingerprints():
    st.markdown("## Worldview Fingerprints")
    st.markdown(
        "Each worldview in the CFA profile library leaves a fingerprint in "
        "deliberation transcripts — a characteristic pattern of operator usage "
        "that reflects how its internal architecture shapes reasoning under "
        "adversarial evaluation."
    )
    st.info(
        "**Data Status: Preliminary.** Dig Site 000 is in Phase 0A. "
        "Operator presence data flows in via SYNC_IN as excavation proceeds. "
        "The structure below is the designed landing format — content fills as it arrives."
    )

    st.markdown("---")
    st.markdown("### Theistic Frameworks")

    with st.expander("⬜ **Classical Theism** — Dig Site 000 Primary Site"):
        st.markdown(
            "Classical Theism transcripts are the primary excavation site for Dig Site 000. "
            "The Grant Architecture sessions (CT vs. MdN, 48-run calibration batch) are the "
            "richest source of pre-catalog operator data — the 5 stable operators in the "
            "Operator Catalog were first recovered here.\n\n"
            "*Full operator frequency data pending formal Dig Site 000 extraction protocol.*"
        )
        st.caption("Preliminary operators observed: Metric Separation, Symmetry Testing, Concession Pricing, Contested ≠ Defeated, Meta-dispute Detection")

    for wv in ["Process Theology", "Islam", "Hinduism", "Judaism",
               "Mormonism", "Eastern Orthodoxy", "Protestantism", "Catholicism"]:
        with st.expander(f"⬜ **{wv}** — Pending"):
            st.caption("No CA extraction data yet. Will populate as Dig Site 000 proceeds.")

    st.markdown("### Naturalistic Frameworks")

    with st.expander("⬜ **Methodological Naturalism** — Pending"):
        st.caption("No CA extraction data yet. Will populate as Dig Site 000 proceeds.")

    st.markdown("### Eastern & Philosophical Frameworks")

    with st.expander("⛏️ **Buddhism** — Preliminary Observation (Phase 0A)"):
        st.markdown(
            "**Differential Presence Finding:**\n\n"
            "Phase 0A preliminary data suggests Buddhism transcripts show differential "
            "operator presence compared to the Classical Theism baseline. Buddhism's "
            "zero-CRUX, zero-DI, zero-CP profile across 48 control runs (336 "
            "metric-deliberations) is itself a negative CA finding — the experiential/"
            "phenomenological grounding does not generate the contested grounding "
            "relations that trigger diagnostic operators.\n\n"
            "*Positive operator frequency data pending full extraction protocol.*"
        )
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Dig Site", "000")
        with col2:
            st.metric("Phase", "0A")
        with col3:
            st.metric("Key Finding", "Zero diagnostic events")

    for wv in ["Gnosticism", "Jainism"]:
        with st.expander(f"⬜ **{wv}** — Pending"):
            st.caption("No CA extraction data yet. Will populate as Dig Site 000 proceeds.")

    st.markdown("---")
    st.markdown("### Saturation Criterion")
    st.markdown(
        "Extraction continues until new transcripts yield no operators not already "
        "in the catalog. At saturation, the recovered set becomes the basis for "
        "composition statistics and the first formal operator inventory. "
        "The project decides when saturation is reached — not the researchers."
    )
