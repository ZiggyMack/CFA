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
    st.markdown("### Phase 0 — The Calibration Sequence")
    st.caption(
        "Before any excavation begins, the pipeline must prove it can tell signal from noise. "
        "Phase 0 is not archaeology — it is building and testing the shovel."
    )

    _c0a, _arr1, _c0b, _arr2, _c0c = st.columns([4, 1, 4, 1, 4])

    _CARD = (
        "border-radius:10px;padding:1.4rem 1rem 1.2rem;text-align:center;"
        "color:white;line-height:1.4;"
    )

    with _c0a:
        st.markdown(f"""
<div style="{_CARD}background:#1a6b50;">
  <div style="font-size:0.7rem;opacity:0.75;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.4rem">Phase 0A</div>
  <div style="font-size:1rem;font-weight:600;margin-bottom:0.6rem">CFA Transcript<br>Extraction</div>
  <div style="font-size:2rem;margin-bottom:0.3rem">✅</div>
  <div style="font-size:0.9rem;font-weight:700;margin-bottom:0.7rem">Complete</div>
  <div style="font-size:0.75rem;opacity:0.8">OP-008 &amp; OP-009 admitted<br>OP-007 ×2 rediscovered</div>
</div>""", unsafe_allow_html=True)

    with _arr1:
        st.markdown(
            "<div style='text-align:center;margin-top:4rem;font-size:1.8rem;opacity:0.35'>→</div>",
            unsafe_allow_html=True,
        )

    with _c0b:
        st.markdown(f"""
<div style="{_CARD}background:#1a4f68;">
  <div style="font-size:0.7rem;opacity:0.75;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.4rem">Phase 0B</div>
  <div style="font-size:1rem;font-weight:600;margin-bottom:0.6rem">Negative Control<br>Battery</div>
  <div style="font-size:2rem;margin-bottom:0.3rem">✅</div>
  <div style="font-size:0.9rem;font-weight:700;margin-bottom:0.7rem">Complete</div>
  <div style="font-size:0.75rem;opacity:0.8">17 extractors × 8 graduated texts<br>Shopping list must → 0 operators</div>
</div>""", unsafe_allow_html=True)

    with _arr2:
        st.markdown(
            "<div style='text-align:center;margin-top:4rem;font-size:1.8rem;opacity:0.35'>→</div>",
            unsafe_allow_html=True,
        )

    with _c0c:
        st.markdown(f"""
<div style="{_CARD}background:#5c4a00;">
  <div style="font-size:0.7rem;opacity:0.75;letter-spacing:0.12em;text-transform:uppercase;margin-bottom:0.4rem">Phase 0C</div>
  <div style="font-size:1rem;font-weight:600;margin-bottom:0.6rem">Positive<br>Control</div>
  <div style="font-size:2rem;margin-bottom:0.3rem">⏳</div>
  <div style="font-size:0.9rem;font-weight:700;margin-bottom:0.7rem">Pending</div>
  <div style="font-size:0.75rem;opacity:0.8">Known-rich transcript must → operators<br>Confirms detection when signal is real</div>
</div>""", unsafe_allow_html=True)

    with st.expander("📊 Phase 0B detail — Extractor Calibration Battery"):
        st.markdown(
            "17 extractors ran across 8 graduated texts (A = shopping list → H = philosophical "
            "dialogue). Gate test: a shopping list must produce 0 operators."
        )
        st.markdown("""
| Tier | Label | Extractors | Behavior |
|------|-------|------------|---------|
| 1 | DISCRIMINATORS | DeepSeek V4 Pro, Claude, Gemma 4 31B, Cogito 671B | Clean gate pass, appropriate gradient A→H |
| 2 | GATE-PASSERS | GPT-4o, GPT-OSS 20B/120B, Grok, Llama 3.3, Qwen3, MiniMax M3, Nemotron Ultra | Gate pass, flat-ish gradient |
| 3 | OVER-REFUSERS | Kimi K2.6, Kimi K2.7 Code | Refuse everything including genuine reasoning |
| 4 | NON-DISCRIMINATORS | LFM2, GLM 5.2, Gemini 2.5 Pro | Gate FAIL — hallucinate operators on shopping lists |
""")
        st.success(
            "**Key finding:** Tier 1-2 extractors detect — they do not generate. Tier 4 "
            "extractors hallucinate operators on a shopping list and are excluded from the pipeline. "
            "The extractors used in Phase 0A (Claude = Tier 1, Grok = Tier 2) both pass."
        )

    st.markdown("---")
    st.markdown("### The Core Confound")
    st.warning(
        "**Can you separate operators in the thinkers from operators in the reader?**\n\n"
        "Every extraction is performed by an LLM. The operator recovered may reflect the reasoning "
        "in the transcript — or it may be a pattern the extractor *projects* onto the transcript "
        "from its own training. This is the central methodological challenge of the entire program."
    )
    _left, _right = st.columns(2)
    with _left:
        st.markdown("**How Phase 0 addresses it:**")
        st.markdown(
            "- **Museum-blind** — extractors don't see each other's output\n"
            "- **Multi-extractor convergence** — same signal must appear independently\n"
            "- **Phase 0B gate** — shopping list must produce zero operators\n"
            "- **Phase 0C gate** — known-rich text must produce operators"
        )
    with _right:
        st.markdown("**Phase 0B preliminary answer:**")
        st.markdown(
            "Phase 0B tests each extractor against a gate: give it a shopping list and "
            "see what happens. Those that produce zero operators pass. Those that hallucinate "
            "operators on a grocery list fail — and are permanently excluded.\n\n"
            "✅ **13 of 17 extractors passed** — the pipeline detects operators when they're "
            "present and stays silent when they're not.\n\n"
            "❌ **4 of 17 failed** — they project operators onto blank text. "
            "The extractors used in Phase 0A (Claude, Grok) both passed."
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
        st.metric("Status", "Phase 0C Pending")
    with col2:
        st.metric("Extractors Tested", "17")
    with col3:
        st.metric("Methodology", "Museum Blind")


# ── Tab 2 ──────────────────────────────────────────────────────────────────────

def _render_operator_catalog():
    st.markdown("## Operator Catalog")
    st.markdown(
        "An **operator** is a reasoning transformation — a move that carries one state "
        "of a deliberation into another. Operators are not conclusions. They are the "
        "mechanisms by which conclusions are reached."
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Registered", "9")
    with col2:
        st.metric("Dig Sites", "2 (+partial)")
    with col3:
        st.metric("Saturation Ratio", "0.50")
    with col4:
        st.metric("Held Candidates", "1")
    st.caption(
        "Saturation ratio = rediscoveries ÷ admissions across all sites "
        "(2 OP-007 rediscoveries, 4 operators admitted from 2 dig sites). "
        "At 1.0, excavation is complete — all new transcripts yield known operators."
    )

    st.markdown("---")
    st.markdown("### Confidence Levels")
    st.markdown("""
| Level | Meaning |
|-------|---------|
| 🔴 RED | Hypothesis — recovered from 1 dig site |
| 🟡 YELLOW | Candidate — confirmed across 2+ independent sites |
| 🟢 GREEN | Confirmed — multi-site, multi-extractor, multi-perturbation |
""")
    st.caption("No operators have reached GREEN yet.")

    st.markdown("---")
    st.markdown("### The Museum — 9 Operators")
    st.caption("As of 2026-07-08 · Source: Nyquist_Consciousness / REPO-SYNC / New_9_Cognitive_Archaeology")

    # ── Dig Site 001 ──────────────────────────────────────────────────────────
    st.markdown("#### Dig Site 001 — Adlam & Barandes Papers")
    st.caption("Source: Physics/philosophy papers on representation and ontology. Not CFA-origin.")

    DS001 = [
        ("OP-001", "Representation ≠ Ontology", "YELLOW", "🟡",
         "Separate what the formalism says from what actually exists — the map is not the territory.",
         "Reification — the formalism is treated as the thing itself."),
        ("OP-002", "Hidden Selection Audit", "RED", "🔴",
         "When an outcome appears determined, ask: what mechanism selected it?",
         "Selection blindness — determined-looking outcomes accepted without tracing how they were chosen."),
        ("OP-003", "Goal → Optimization Collapse", "RED", "🔴",
         "Specifying your goal immediately fixes your rational strategy — no intermediate empirical steps.",
         "Strategy drift — rational agency claimed without noticing the goal already fully determines the move."),
        ("OP-004", "Reconstruction Before Judgment", "YELLOW", "🟡",
         "Faithfully reconstruct the object in its own terms before evaluating it from yours.",
         "Premature evaluation — the object is judged through the wrong frame before its own frame is understood."),
        ("OP-005", "Hidden Structure Injection", "RED", "🔴",
         "Detect when analysis quietly imports evaluators, observers, coordinate systems, or representations without admitting it.",
         "Frame laundering — hidden assumptions passed off as neutral analysis."),
        ("OP-006", "Under-Determination Detection", "RED", "🔴",
         "When a formalism underdetermines an outcome, any procedure that claims to determine one is importing extra structure.",
         "False precision — claiming determination where the formalism only provides constraints."),
    ]

    for op_id, name, confidence, icon, definition, failure in DS001:
        with st.expander(f"{icon} **{op_id} — {name}** ({confidence})"):
            st.markdown(f"**Definition:** {definition}")
            st.caption(f"**Failure mode (when absent):** {failure}")
            st.caption(f"Dig Site 001 · Adlam & Barandes")

    # ── OP-007 Cross-Site ─────────────────────────────────────────────────────
    st.markdown("#### OP-007 — Cross-Site (001 + DBEP + 000)")
    with st.expander("🟡 **OP-007 — Locate Disagreement Layer** (YELLOW — strongest evidence)"):
        st.markdown(
            "**Definition:** Before resolving a disagreement, identify which layer it actually "
            "lives in — description, belief, evaluation, or prediction.\n\n"
            "**Why YELLOW:** Three independent recovery sites — Dig Site 001, DBEP framework "
            "development, and CFA transcripts (Dig Site 000). The strongest evidence base of "
            "any operator in the Museum."
        )
        st.markdown(
            "**CFA contribution (Phase 0A):** Two pre-catalog 'stable operators' were reclassified "
            "as OP-007 at specific layers:\n\n"
            "- **'Metric Separation'** = OP-007 at the metric layer — the disagreement was about "
            "*which metric* the challenge scores on, not the object being evaluated\n"
            "- **'Meta-dispute Detection'** = OP-007 at the meta-dispute layer — the disagreement "
            "was about what the instrument measures, not the framework's quality\n\n"
            "These are the same operator at different levels of abstraction. Their independent "
            "rediscovery in CFA transcripts adds a third site to OP-007's evidence record."
        )
        st.caption("Failure mode: Layer Confusion — objections misrouted across the epistemic stack")

    # ── Dig Site 000 CFA-Origin ───────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### Dig Site 000 — CFA Transcripts (CFA-Origin Operators)")
    st.caption(
        "Source: Framework-G deliberation sessions. 4 museum-blind extractions "
        "(Claude × 2 transcripts, Grok × 2 transcripts). Admitted 2026-07-08."
    )

    st.success(
        "**OP-008 — Symmetry Testing of Standards** 🔴 RED\n\n"
        "**Definition:** Test whether an evaluative standard, applied consistently across all "
        "candidates, produces discriminating results — or whether it collapses everything to "
        "the same verdict, revealing selective application rather than genuine assessment.\n\n"
        "**Admission:** 6/6 criteria PASS · 4/4 extractor convergence (all four independent "
        "extractions used 'standard' or 'symmetry' vocabulary without coordination)\n\n"
        "**Failure mode:** Prosecution bias — the same standard that would disqualify the "
        "target would equally disqualify the evaluator, but only the target is held to it."
    )

    st.success(
        "**OP-009 — Contested ≠ Defeated** 🔴 RED\n\n"
        "**Definition:** Separate the claim that a position faces genuine difficulty from the "
        "stronger claim that it has been refuted — refusing to treat open problems as automatic "
        "disqualifiers.\n\n"
        "**Admission:** 6/6 criteria PASS · 3.5/4 extractor convergence (Grok v2.1 captured "
        "a narrower subset: logical vs evidential pressure is one instance of the distinction)\n\n"
        "**Failure mode:** Anomaly-as-refutation — every unresolved difficulty scores as defeat; "
        "frameworks with open questions are eliminated rather than assessed accurately."
    )

    # ── Held Candidate ────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("#### Held Candidate")
    st.warning(
        "**Concession Pricing** — HELD (not yet admitted)\n\n"
        "4/4 extractor convergence — real signal. But two admission criteria are marginal:\n"
        "- Criterion 5 (survives translation): some translations reduce it to bookkeeping\n"
        "- Criterion 6 (transforms epistemic state): manages deliberation state, not world-knowledge\n\n"
        "Classification ambiguous — may be a high-quality deliberation heuristic rather than a "
        "cognitive operator. **Revisit if recovered independently at a future dig site.**"
    )

    # ── Operator Relationships ────────────────────────────────────────────────
    st.markdown("---")
    with st.expander("🌳 Operator Relationships — Hierarchy and Dependencies"):
        st.markdown(
            "Operators are not independent — some are special cases of others, revealing "
            "structure in the operator space itself. This tree is a scientific finding, not a design."
        )
        st.code(
            "Under-Determination Detection (OP-006)\n"
            "  ↓ reveals the need for\n"
            "  Hidden Selection Audit (OP-002)\n"
            "    ↓ often uncovers\n"
            "    Hidden Structure Injection (OP-005)\n"
            "      ↓ which is diagnosed by\n"
            "      Representation ≠ Ontology (OP-001)\n\n"
            "Goal → Optimization Collapse (OP-003)\n"
            "  ↓ requires prior\n"
            "  Reconstruction Before Judgment (OP-004)\n\n"
            "Locate Disagreement Layer (OP-007)    ─── cross-cutting (applies at any layer)\n"
            "Symmetry Testing of Standards (OP-008) ─ tests evaluative standards (sibling to OP-006)\n"
            "Contested ≠ Defeated (OP-009)          ─ calibrates epistemic damage (sibling to OP-002)",
            language=None,
        )

    # ── Composition Pipeline ──────────────────────────────────────────────────
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

    st.markdown("---")
    st.caption(
        "**Phase 0B empirically validated Law 1's core claim.** 17 extractors tested across "
        "8 graduated texts confirm that Tier 1-2 extractors produce zero operators from shopping "
        "lists and appropriate gradients from philosophical dialogues. The pipeline detects — "
        "it does not generate. Falsification criterion #2 is not met for the extractors used."
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
        "**Data Status: Phase 0C Pending.** Phase 0A (CFA transcript extraction, 2 operators admitted) "
        "and Phase 0B (negative control battery, 17 extractors calibrated) are complete. "
        "Phase 0C — positive control on a known-rich transcript — is the final calibration step "
        "before full excavation begins. Operator presence data flows in via SYNC_IN as excavation proceeds."
    )

    st.markdown("---")
    st.markdown("### Theistic Frameworks")

    with st.expander("⛏️ **Classical Theism** — Dig Site 000 Primary Site — Phase 0A Complete"):
        st.markdown(
            "Classical Theism transcripts are the primary excavation site for Dig Site 000. "
            "Phase 0A ran 4 museum-blind extractions against Framework-G deliberation sessions "
            "(Claude × 2 transcripts, Grok × 2 transcripts). Formal admission evaluated 2026-07-08."
        )
        st.markdown("**Phase 0A outcomes:**")
        st.markdown(
            "- **Admitted to Museum:** OP-008 (Symmetry Testing of Standards), "
            "OP-009 (Contested ≠ Defeated) — both 6/6 criteria PASS\n"
            "- **OP-007 rediscoveries (×2):** 'Metric Separation' = OP-007 at metric layer; "
            "'Meta-dispute Detection' = OP-007 at meta-dispute layer — adds CFA as a third "
            "independent recovery site for OP-007\n"
            "- **Held candidate:** Concession Pricing — 4/4 convergence, marginal on criteria 5-6; "
            "pending second evaluation from future dig sites\n"
            "- **Sessions:** 4 transcripts extracted · Museum-blind · Evaluator: Repo (Claude Opus 4.6)"
        )

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

    with st.expander("⛏️ **Gnosticism / Framework-G** — Dig Site 000 Source Transcripts"):
        st.markdown(
            "Framework-G (Consciousness as Telos) deliberation transcripts are the **source material** "
            "for Dig Site 000 Phase 0A. OP-008 and OP-009 — the two CFA-origin operators — were "
            "recovered from Framework-G adversarial deliberation sessions.\n\n"
            "This makes Gnosticism the *origin worldview* of the CFA-contributed operators. The adversarial "
            "deliberation structure of Framework-G evaluations produced the specific reasoning dynamics "
            "that OP-008 (Symmetry Testing) and OP-009 (Contested ≠ Defeated) describe."
        )
        col1, col2 = st.columns(2)
        with col1:
            st.metric("Operators Sourced", "2")
        with col2:
            st.metric("Phase", "0A Complete")
        st.caption("OP-008 (Symmetry Testing of Standards) · OP-009 (Contested ≠ Defeated)")

    with st.expander("⬜ **Jainism** — Pending"):
        st.caption("No CA extraction data yet. Will populate as Dig Site 000 proceeds.")

    st.markdown("---")
    st.markdown("### Saturation Criterion")
    st.markdown(
        "Extraction continues until new transcripts yield no operators not already "
        "in the catalog. At saturation, the recovered set becomes the basis for "
        "composition statistics and the first formal operator inventory. "
        "The project decides when saturation is reached — not the researchers."
    )
