import streamlit as st
import yaml
import pandas as pd
from pathlib import Path
from datetime import datetime

from utils.profile_loader import list_available_profiles

_BASE = Path(__file__).parent.parent

_SHORT = {
    "vs_classical_theism": "CT",
    "vs_methodological_naturalism": "MdN",
    "vs_process_theology": "PT",
    "vs_gnosticism": "G",
    "vs_buddhism": "B",
}


# ── Shared helpers ─────────────────────────────────────────────────────────────

def _section_card(icon, title, subtitle, color):
    sub = (
        f'<div style="font-size:0.85rem;color:#666;margin-top:0.2rem">{subtitle}</div>'
        if subtitle else ""
    )
    st.markdown(
        f'<div style="border:1.5px solid {color};border-radius:10px;'
        f'padding:0.75rem 1.25rem;background:{color}12;margin-bottom:0.9rem">'
        f'<span style="font-size:0.7rem;color:{color};font-weight:700;'
        f'letter-spacing:0.12em;text-transform:uppercase">{icon}&nbsp;&nbsp;{title}</span>'
        f'{sub}</div>',
        unsafe_allow_html=True,
    )

def _inline_badge(text, color):
    return (
        f'<span style="background:{color}20;color:{color};border-radius:4px;'
        f'padding:0.1rem 0.45rem;font-size:0.72rem;font-weight:700">{text}</span>'
    )

def _row(left, right_text, right_color):
    return (
        f'<div style="display:flex;align-items:center;justify-content:space-between;'
        f'border-bottom:1px solid #eee;padding:0.45rem 0">'
        f'{left}'
        f'<span style="font-size:0.8rem;color:{right_color};font-weight:600;'
        f'white-space:nowrap;margin-left:0.5rem">{right_text}</span></div>'
    )


# ── Page entry ─────────────────────────────────────────────────────────────────

def render():
    hcol, bcol = st.columns([8, 1])
    with hcol:
        st.title("🎛️ Mission Control")
        st.caption("Creator's dashboard — SYNC_IN inbox, data coverage, research status, open loops")
    with bcol:
        if st.button("🏠 Home", key="mc_home"):
            st.session_state.page = 'landing'
            st.rerun()

    st.markdown("---")
    _render_sync_inbox()
    st.markdown("---")
    _render_coverage_matrix()
    st.markdown("---")
    _render_research_status()
    st.markdown("---")
    _render_theoretical_grounding()
    st.markdown("---")
    _render_open_loops()


# ── SYNC_IN Inbox ─────────────────────────────────────────────────────────────

def _render_sync_inbox():
    _section_card("📥", "SYNC_IN Inbox",
                  "Files delivered by Repo Claude awaiting action", "#1a4f68")

    pending_dir   = _BASE / "docs" / "REPO_SYNC" / "SYNC_IN" / "pending"
    processed_dir = _BASE / "docs" / "REPO_SYNC" / "SYNC_IN" / "processed"

    pending = sorted(
        [f for f in pending_dir.glob("*.md")],
        key=lambda p: p.stat().st_mtime, reverse=True,
    )

    if not pending:
        st.markdown(
            '<div style="border:1.5px solid #1a6b50;border-radius:8px;padding:0.7rem 1.1rem;'
            'background:#1a6b5012;color:#1a6b50;font-weight:600">'
            '✅&nbsp;&nbsp;Inbox clear — no files waiting in SYNC_IN/pending/</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div style="border:1.5px solid #c97000;border-radius:8px;padding:0.7rem 1.1rem;'
            f'background:#c9700012;color:#c97000;font-weight:600">'
            f'⚠️&nbsp;&nbsp;{len(pending)} file(s) waiting for action</div>',
            unsafe_allow_html=True,
        )
        st.markdown("")
        for f in pending:
            stat = f.stat()
            modified = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M")
            size_kb = stat.st_size / 1024
            with st.expander(f"📄 {f.name} — {size_kb:.1f} KB — {modified}"):
                st.caption(str(f))

    processed = sorted(
        [f for f in processed_dir.glob("*.md")],
        key=lambda p: p.stat().st_mtime, reverse=True,
    )[:6]

    if processed:
        st.markdown(
            '<div style="margin-top:0.9rem;font-size:0.78rem;color:#888;'
            'font-weight:700;letter-spacing:0.06em;text-transform:uppercase;'
            'margin-bottom:0.4rem">Recently processed</div>',
            unsafe_allow_html=True,
        )
        cols = st.columns(3)
        for i, f in enumerate(processed):
            modified = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d")
            cols[i % 3].markdown(
                f'<div style="background:#f4f5fa;border-radius:6px;padding:0.4rem 0.6rem;'
                f'margin-bottom:0.3rem;font-size:0.75rem;color:#444;line-height:1.4">'
                f'<span style="color:#1a6b50;font-weight:700">✅</span>&nbsp;'
                f'{f.stem[:36]}'
                f'<br><span style="color:#aaa">{modified}</span></div>',
                unsafe_allow_html=True,
            )


# ── Framework Coverage Matrix ─────────────────────────────────────────────────

def _render_coverage_matrix():
    _section_card("📊", "Framework Coverage Matrix",
                  "Live read from worldview YAMLs — Trinity matchups with per-metric data, "
                  "lever calibration, H2H button status",
                  "#5a3a8a")

    rows = _build_coverage()

    trinity_n = sum(1 for r in rows if r["Trinity"].startswith("✅"))
    lever_n   = sum(1 for r in rows if r["Levers"].startswith("✅"))
    h2h_n     = sum(1 for r in rows if r["H2H"] == "✅")

    s1, s2, s3, s4 = st.columns(4)
    s1.metric("Frameworks",      len(rows))
    s2.metric("Trinity Audited", f"{trinity_n} / {len(rows)}")
    s3.metric("Lever Calibrated", f"{lever_n} / {len(rows)}")
    s4.metric("H2H Ready",       f"{h2h_n} / {len(rows)}")

    st.markdown("")
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


def _build_coverage():
    rows = []
    for wv_name in list_available_profiles():
        yaml_key = wv_name.upper().replace(' ', '_')
        yaml_path = _BASE / "profiles" / "worldviews" / f"{yaml_key}.yaml"

        try:
            with open(yaml_path, encoding='utf-8') as f:
                data = yaml.safe_load(f) or {}
        except FileNotFoundError:
            rows.append({
                "Framework": wv_name,
                "Trinity": "⬜ 0", "Trinity Detail": "—",
                "Levers": "⬜ 0",  "Lever Detail": "—",
                "H2H": "⬜",
            })
            continue

        ts = data.get('trinity_scores_by_matchup', {}) or {}
        trinity_keys = [
            k for k, v in ts.items()
            if isinstance(v, dict) and 'metrics' in v and not k.startswith('control')
        ]

        lm = data.get('levers_by_matchup', {}) or {}
        lever_keys = [
            k for k, v in lm.items()
            if isinstance(v, dict) and 'collective_coherence_impact' in v
            and not k.startswith('control')
        ]

        rows.append({
            "Framework":      wv_name,
            "Trinity":        f"✅ {len(trinity_keys)}" if trinity_keys else "⬜ 0",
            "Trinity Detail": ", ".join(_SHORT.get(k, k) for k in trinity_keys) or "—",
            "Levers":         f"✅ {len(lever_keys)}" if lever_keys else "⬜ 0",
            "Lever Detail":   ", ".join(_SHORT.get(k, k) for k in lever_keys) or "—",
            "H2H":            "✅" if lever_keys else "⬜",
        })

    return rows


# ── Research Program Status ───────────────────────────────────────────────────

def _render_research_status():
    _section_card("🔬", "Research Program Status",
                  "Cognitive Archaeology phases and Trinity batch inventory", "#1a6b50")

    # Three-stat banner
    st.markdown(
        '<div style="border:1.5px solid #1a6b50;border-radius:10px;'
        'padding:1rem 1.5rem;background:#1a6b5010;margin-bottom:1.2rem">'
        '<div style="font-size:0.68rem;color:#1a6b50;font-weight:700;letter-spacing:0.12em;'
        'text-transform:uppercase;text-align:center;margin-bottom:0.8rem">'
        'Research at a glance</div>'
        '<div style="display:grid;grid-template-columns:repeat(3,1fr);'
        'gap:0.5rem;text-align:center">'
        '<div><div style="font-size:2.2rem;font-weight:700;color:#1a4f68">663</div>'
        '<div style="font-size:0.8rem;color:#666">Worldview Runs</div></div>'
        '<div><div style="font-size:2.2rem;font-weight:700;color:#1a4f68">15</div>'
        '<div style="font-size:0.8rem;color:#666">Museum Operators</div></div>'
        '<div><div style="font-size:2.2rem;font-weight:700;color:#aaaaaa">Full ⬜</div>'
        '<div style="font-size:0.8rem;color:#666">CA Next Phase</div></div>'
        '</div></div>',
        unsafe_allow_html=True,
    )

    col_ca, col_trinity = st.columns(2)

    with col_ca:
        st.markdown(
            '<div style="font-size:0.75rem;color:#1a6b50;font-weight:700;'
            'letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.6rem">'
            'Cognitive Archaeology</div>',
            unsafe_allow_html=True,
        )
        phases = [
            ("0A",   "CFA transcript extraction",              "✅ Complete",   "#1a6b50"),
            ("0B",   "Negative control battery (17 extractors)", "✅ Complete", "#1a6b50"),
            ("0C",   "Positive control (4/4 extractors, 91–100%)", "✅ Complete", "#1a6b50"),
            ("Full", "Systematic worldview excavation",        "⬜ Not started","#aaaaaa"),
        ]
        html = ""
        for pid, focus, status, color in phases:
            badge = _inline_badge(pid, color)
            left  = f'{badge} <span style="font-size:0.83rem;color:#333">{focus}</span>'
            html += _row(left, status, color)
        st.markdown(f'<div style="margin-bottom:0.8rem">{html}</div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Museum", "15 operators")
        c2.metric("Saturation", "0.50")
        c3.metric("Held", "1 candidate")
        st.caption("Pipeline fully calibrated — 0A ✅ 0B ✅ 0C ✅ · Next: systematic worldview excavation")

    with col_trinity:
        st.markdown(
            '<div style="font-size:0.75rem;color:#1a4f68;font-weight:700;'
            'letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.6rem">'
            'Trinity Batch Inventory</div>',
            unsafe_allow_html=True,
        )
        batches = [
            ("Classical Theism",          "136", "Mature",        "#1a6b50"),
            ("Methodological Naturalism", "94",  "Validated",     "#1a6b50"),
            ("Gnosticism",                "212", "Largest set",   "#1a6b50"),
            ("Process Theology",          "131", "Validated",     "#1a6b50"),
            ("Buddhism",                  "41",  "Newest",        "#c97000"),
            ("8 Breadth Worldviews",      "48",  "n=1 complete",  "#5a3a8a"),
        ]
        html = ""
        for framework, runs, note, color in batches:
            runs_bold = f'<span style="font-weight:700;color:#1a4f68;font-size:0.9rem;margin-right:0.4rem">{runs}</span>'
            note_badge = _inline_badge(note, color)
            right_html = f'<span style="white-space:nowrap">{runs_bold}{note_badge}</span>'
            left  = f'<span style="font-size:0.83rem;color:#333">{framework}</span>'
            html += (
                f'<div style="display:flex;align-items:center;justify-content:space-between;'
                f'border-bottom:1px solid #eee;padding:0.45rem 0">'
                f'{left}{right_html}</div>'
            )
        st.markdown(f'<div style="margin-bottom:0.8rem">{html}</div>', unsafe_allow_html=True)
        st.metric("Total Runs", "663")
        st.caption("663 worldview (259 Golden + 355 Control + 49 Breadth) · +88 calib/legacy · Breadth: 8×6 runs + B-control · BREADTH_SCORECARD_20260717")


# ── What's Cooking ────────────────────────────────────────────────────────────

def _render_theoretical_grounding():
    _section_card("🍳🥚", "What's Cooking?",
                  "New theoretical terrain opening up — what the Barandes ISP study unlocked "
                  "and where the research is headed next",
                  "#3a2a6a")

    TG, TGBG = "#3a2a6a", "#f5f0ff"

    insights = [
        (
            "⚛️", "ARMADA = Axiom 2 Estimation",
            "ISP Axiom 2 states the laws of nature are sparse conditional probabilities. "
            "Lever calibration (10+ golden runs per pairing averaged to YAML finals) is the "
            "empirical measurement procedure for exactly this. ARMADA is not building a scoring "
            "system; it is estimating the sparse conditional probability matrix of a cognitive ISP.",
            "Barandes ISP study · Q1–Q22",
        ),
        (
            "🔗", "Per-matchup design is ontologically mandated — now empirically confirmed",
            "A41 confirmed pair-dependency by ISP theory. The 8-worldview breadth pass confirmed "
            "it empirically: holding subject constant and swapping opponent (CT→MdN) produced "
            "structured, predictable Δ scores — secular frameworks rise against MdN, religious ones "
            "fall. The sign of Δ sorts cleanly along the secular↔religious axis. Axiom 2 is "
            "measurable at the individual worldview grain.",
            "ISP A41 · Breadth opponent effect · OPPONENT_EFFECT_CT_VS_MDN_20260717",
        ),
        (
            "🗜️", "Identity compresses the score range — control is the uncompressed signal",
            "New finding from the breadth control grid: Phase-1 spread halves under identity loading "
            "(3.55 control → 1.72 external). The PRO advocate lifts thin/meta frameworks; the ANTI "
            "critic lowers rich comprehensive ones. Mean effect ≈ 0 (not inflation), but variance "
            "collapses. External CFA scores are range-compressed; the external−control delta "
            "is itself an informative measurement — how far the adversarial frame moves each framework.",
            "IDENTITY_EFFECT_CONTROLS_20260717 · all 13 worldviews now have control baseline",
        ),
        (
            "🏛️", "Cognitive Architecture Extraction emerging",
            "The Barandes Q1–Q40 protocol produced a replicable structure: internal mechanics → "
            "cognitive operators → meta-scientific methodology → cross-disciplinary bridges. "
            "This skeleton is extractable as a standalone CAE template for subsequent thinkers. "
            "Barandes is Case Study #1.",
            "Next: formalize Q1–Q40 skeleton as replicable CAE protocol · Repo Claude staging",
        ),
    ]

    row1_l, row1_r = st.columns(2)
    row2_l, row2_r = st.columns(2)
    grid = [row1_l, row1_r, row2_l, row2_r]

    for i, (icon, title, body, footer) in enumerate(insights):
        with grid[i]:
            st.markdown(
                f'<div style="border:1.5px solid {TG};border-radius:10px;'
                f'padding:1rem 1.1rem;background:{TGBG};margin-bottom:0.8rem">'
                f'<div style="font-size:1.25rem;margin-bottom:0.35rem">{icon}</div>'
                f'<div style="font-size:0.87rem;font-weight:700;color:#222;'
                f'margin-bottom:0.4rem">{title}</div>'
                f'<div style="font-size:0.79rem;color:#555;line-height:1.5;'
                f'margin-bottom:0.45rem">{body}</div>'
                f'<div style="font-size:0.73rem;color:{TG};font-weight:600;'
                f'border-top:1px solid {TG}25;padding-top:0.35rem;'
                f'font-style:italic">{footer}</div>'
                f'</div>',
                unsafe_allow_html=True,
            )


# ── Open Loops ────────────────────────────────────────────────────────────────

def _render_open_loops():
    _section_card("🔓", "Open Loops",
                  "Known issues and pending decisions — remove entries as they're resolved",
                  "#8a4a00")

    # Count line
    st.markdown(
        '<div style="font-size:0.8rem;color:#888;margin-bottom:0.6rem">'
        '<span style="color:#c97000;font-weight:700">1 medium</span>'
        '&nbsp;·&nbsp;'
        '<span style="color:#1a4f68;font-weight:700">4 low</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── MEDIUM — CAE Protocol ─────────────────────────────────────────────────
    AM, ABG = "#c97000", "#fffbf0"
    st.markdown(
        f'<div style="border:1.5px solid {AM};border-radius:10px;'
        f'padding:1rem 1.25rem;background:{ABG};margin-bottom:0.8rem">'
        f'<div style="display:flex;align-items:flex-start;gap:0.9rem">'
        f'<div style="font-size:1.6rem;line-height:1;margin-top:0.1rem">🏛️</div>'
        f'<div style="flex:1">'
        f'<div style="display:flex;align-items:center;gap:0.6rem;margin-bottom:0.5rem">'
        f'<span style="background:{AM};color:white;border-radius:4px;padding:0.1rem 0.5rem;'
        f'font-size:0.7rem;font-weight:700;letter-spacing:0.08em">MEDIUM</span>'
        f'<span style="font-size:0.95rem;font-weight:700;color:#222">'
        f'CAE Protocol — formalize the Barandes extraction template</span>'
        f'</div>'
        f'<div style="font-size:0.83rem;color:#555;line-height:1.55;margin-bottom:0.6rem">'
        f'The Barandes Q1–Q40 study produced a replicable multi-pass structure: internal mechanics '
        f'(Q1–15) → cross-disciplinary bridge (Q16–20) → meta-scientific operators (Q21–35) → '
        f'discovery methodology (Q36–40). Extracting that skeleton as a standalone Cognitive '
        f'Architecture Extraction (CAE) template enables the same protocol to run against '
        f'subsequent thinkers without rebuilding from scratch. Barandes is Case Study #1.'
        f'</div>'
        f'<div style="font-size:0.78rem;color:{AM};font-weight:700;border-top:1px solid {AM}30;'
        f'padding-top:0.45rem">→ Strip Barandes-specific content from Q1–Q40 → '
        f'standalone CAE template → Repo Claude for Nyquist staging</div>'
        f'</div></div></div>',
        unsafe_allow_html=True,
    )

    # ── LOW — three across ────────────────────────────────────────────────────
    LC, LBG = "#1a4f68", "#f0f5fa"
    col_l, col_r, col_b = st.columns(3)

    with col_l:
        st.markdown(
            f'<div style="border:1.5px solid {LC};border-radius:10px;'
            f'padding:1rem 1.1rem;background:{LBG}">'
            f'<div style="display:flex;align-items:flex-start;gap:0.7rem">'
            f'<div style="font-size:1.4rem;line-height:1;margin-top:0.1rem">🔧</div>'
            f'<div style="flex:1">'
            f'<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.4rem">'
            f'<span style="background:{LC};color:white;border-radius:4px;padding:0.1rem 0.45rem;'
            f'font-size:0.7rem;font-weight:700;letter-spacing:0.08em">LOW</span>'
            f'<span style="font-size:0.85rem;font-weight:700;color:#222">PT YAML — vs_buddhism misplaced</span>'
            f'</div>'
            f'<div style="font-size:0.8rem;color:#555;line-height:1.5;margin-bottom:0.5rem">'
            f'PROCESS_THEOLOGY.yaml has a levers_by_matchup.vs_buddhism block with Trinity '
            f'score structure — misplaced during the Buddhism batch. No runtime impact '
            f'(coverage matrix correctly ignores it). Structural debt only.'
            f'</div>'
            f'<div style="font-size:0.76rem;color:{LC};font-weight:700;border-top:1px solid {LC}30;'
            f'padding-top:0.4rem">→ Move block to trinity_scores_by_matchup when convenient</div>'
            f'</div></div></div>',
            unsafe_allow_html=True,
        )

    with col_r:
        st.markdown(
            f'<div style="border:1.5px solid {LC};border-radius:10px;'
            f'padding:1rem 1.1rem;background:{LBG}">'
            f'<div style="display:flex;align-items:flex-start;gap:0.7rem">'
            f'<div style="font-size:1.4rem;line-height:1;margin-top:0.1rem">🏛️</div>'
            f'<div style="flex:1">'
            f'<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.4rem">'
            f'<span style="background:{LC};color:white;border-radius:4px;padding:0.1rem 0.45rem;'
            f'font-size:0.7rem;font-weight:700;letter-spacing:0.08em">LOW</span>'
            f'<span style="font-size:0.85rem;font-weight:700;color:#222">Buddhism 2×2 design incomplete</span>'
            f'</div>'
            f'<div style="font-size:0.8rem;color:#555;line-height:1.5;margin-bottom:0.5rem">'
            f'Buddhism has 41 subject runs (b_vs_ct: 10, b_vs_mdn: 11, b_vs_pt: 10, b_vs_g: 10). '
            f'Reverse-stance runs exist in other framework YAMLs but the closed 2×2 design '
            f'is not formally documented.'
            f'</div>'
            f'<div style="font-size:0.76rem;color:{LC};font-weight:700;border-top:1px solid {LC}30;'
            f'padding-top:0.4rem">→ Awareness item — no action required now</div>'
            f'</div></div></div>',
            unsafe_allow_html=True,
        )

    with col_b:
        st.markdown(
            f'<div style="border:1.5px solid {LC};border-radius:10px;'
            f'padding:1rem 1.1rem;background:{LBG}">'
            f'<div style="display:flex;align-items:flex-start;gap:0.7rem">'
            f'<div style="font-size:1.4rem;line-height:1;margin-top:0.1rem">🌀</div>'
            f'<div style="flex:1">'
            f'<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.4rem">'
            f'<span style="background:{LC};color:white;border-radius:4px;padding:0.1rem 0.45rem;'
            f'font-size:0.7rem;font-weight:700;letter-spacing:0.08em">LOW</span>'
            f'<span style="font-size:0.85rem;font-weight:700;color:#222">Opponent-vs-Buddhism blocks pending</span>'
            f'</div>'
            f'<div style="font-size:0.8rem;color:#555;line-height:1.5;margin-bottom:0.5rem">'
            f'MdN, PT, and G each need trinity_scores_by_matchup.vs_buddhism. Control '
            f'scores exist (0 CRUX, 1.6 avg rounds) but the golden (identity) batch '
            f'hasn\'t run. Apply the full package once external-identity batch completes.'
            f'</div>'
            f'<div style="font-size:0.76rem;color:{LC};font-weight:700;border-top:1px solid {LC}30;'
            f'padding-top:0.4rem">→ Hold for Buddhism golden batch, then apply mdn/pt/g vs_buddhism blocks</div>'
            f'</div></div></div>',
            unsafe_allow_html=True,
        )

    # ── 4th LOW — Buddhism golden batch as ISP experiment ─────────────────────
    st.markdown("")
    st.markdown(
        f'<div style="border:1.5px solid {LC};border-radius:10px;'
        f'padding:1rem 1.25rem;background:{LBG}">'
        f'<div style="display:flex;align-items:flex-start;gap:0.7rem">'
        f'<div style="font-size:1.4rem;line-height:1;margin-top:0.1rem">⚛️</div>'
        f'<div style="flex:1">'
        f'<div style="display:flex;align-items:center;gap:0.5rem;margin-bottom:0.4rem">'
        f'<span style="background:{LC};color:white;border-radius:4px;padding:0.1rem 0.45rem;'
        f'font-size:0.7rem;font-weight:700;letter-spacing:0.08em">LOW</span>'
        f'<span style="font-size:0.85rem;font-weight:700;color:#222">'
        f'Buddhism golden batch = ISP crux-rate prediction test</span>'
        f'</div>'
        f'<div style="font-size:0.8rem;color:#555;line-height:1.5;margin-bottom:0.5rem">'
        f'A41 confirmed: division events require classical correlation density (identity loading). '
        f'The control batch zero-CRUX is an ISP prediction, not instrument failure. The golden '
        f'(identity-loaded) batch is now a formal ISP experiment: does identity loading restore '
        f'non-zero crux rates? Record crux rate and crux content, compare against the control baseline (0.0).'
        f'</div>'
        f'<div style="font-size:0.76rem;color:{LC};font-weight:700;border-top:1px solid {LC}30;'
        f'padding-top:0.4rem">→ Design golden batch to explicitly test the ISP prediction; '
        f'include crux-rate comparison in the results briefing</div>'
        f'</div></div></div>',
        unsafe_allow_html=True,
    )

