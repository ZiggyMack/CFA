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
            if isinstance(v, dict) and 'metrics' in v and k != 'control_baseline_pooled'
        ]

        lm = data.get('levers_by_matchup', {}) or {}
        lever_keys = [
            k for k, v in lm.items()
            if isinstance(v, dict) and 'collective_coherence_impact' in v
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
        '<div><div style="font-size:2.2rem;font-weight:700;color:#1a4f68">702</div>'
        '<div style="font-size:0.8rem;color:#666">Trinity Runs</div></div>'
        '<div><div style="font-size:2.2rem;font-weight:700;color:#1a4f68">9</div>'
        '<div style="font-size:0.8rem;color:#666">Museum Operators</div></div>'
        '<div><div style="font-size:2.2rem;font-weight:700;color:#c97000">0C ⏳</div>'
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
            ("0C",   "Positive control",                       "⏳ Pending",    "#c97000"),
            ("Full", "Systematic worldview excavation",        "⬜ Not started","#aaaaaa"),
        ]
        html = ""
        for pid, focus, status, color in phases:
            badge = _inline_badge(pid, color)
            left  = f'{badge} <span style="font-size:0.83rem;color:#333">{focus}</span>'
            html += _row(left, status, color)
        st.markdown(f'<div style="margin-bottom:0.8rem">{html}</div>', unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Museum", "9 operators")
        c2.metric("Saturation", "0.50")
        c3.metric("Held", "1 candidate")
        st.caption("Phase 0C blocker: known-rich CFA transcript (Framework-G preferred) → Repo Claude")

    with col_trinity:
        st.markdown(
            '<div style="font-size:0.75rem;color:#1a4f68;font-weight:700;'
            'letter-spacing:0.1em;text-transform:uppercase;margin-bottom:0.6rem">'
            'Trinity Batch Inventory</div>',
            unsafe_allow_html=True,
        )
        batches = [
            ("Classical Theism",          "136", "Mature",      "#1a6b50"),
            ("Methodological Naturalism", "94",  "Validated",   "#1a6b50"),
            ("Gnosticism",                "212", "Largest set", "#1a6b50"),
            ("Process Theology",          "131", "Validated",   "#1a6b50"),
            ("Buddhism",                  "41",  "Newest",      "#c97000"),
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
        st.metric("Total Runs", "702")
        st.caption("Source: BRIEFING_20260709_ARMADA_STATUS · as of 2026-07-09")


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
        '<span style="color:#1a4f68;font-weight:700">2 low</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    LOOPS = [
        {
            "label":    "🟠 MEDIUM · CA Phase 0C — positive control transcript needed",
            "color":    "#c97000",
            "bg":       "#fffbf0",
            "icon":     "📋",
            "priority": "MEDIUM",
            "body": (
                "Repo Claude needs a known-rich CFA deliberation transcript (Framework-G preferred) "
                "to run the positive control extraction battery — confirming the pipeline detects "
                "operators when they are genuinely present. Phase 0C is the last calibration step "
                "before full excavation begins."
            ),
            "action": "→ Action: pass a known-rich Framework-G transcript to Repo Claude via SYNC_OUT",
        },
        {
            "label":    "🔵 LOW · PT YAML — vs_buddhism misplaced in levers_by_matchup",
            "color":    "#1a4f68",
            "bg":       "#f0f5fa",
            "icon":     "🔧",
            "priority": "LOW",
            "body": (
                "PROCESS_THEOLOGY.yaml has a levers_by_matchup.vs_buddhism block with Trinity "
                "score structure (batch_id, metrics, batch_stats) — misplaced during the Buddhism batch. "
                "No runtime impact (coverage matrix correctly ignores it). Structural debt only."
            ),
            "action": "→ Move block to trinity_scores_by_matchup when convenient",
        },
        {
            "label":    "🔵 LOW · Buddhism 2×2 design incomplete",
            "color":    "#1a4f68",
            "bg":       "#f0f5fa",
            "icon":     "🏛️",
            "priority": "LOW",
            "body": (
                "Buddhism has 41 subject runs (b_vs_ct: 10, b_vs_mdn: 11, b_vs_pt: 10, b_vs_g: 10). "
                "Reverse-stance runs exist in other framework YAMLs but the full closed 2×2 design "
                "is not formally documented."
            ),
            "action": "→ Awareness item — no action required now",
        },
    ]

    for loop in LOOPS:
        c, bg = loop["color"], loop["bg"]
        with st.expander(loop["label"]):
            st.markdown(
                f'<div style="border-left:3px solid {c};background:{bg};'
                f'border-radius:0 8px 8px 0;padding:0.8rem 1rem;margin-top:0.2rem">'
                f'<div style="display:flex;align-items:flex-start;gap:0.7rem">'
                f'<div style="font-size:1.3rem;line-height:1">{loop["icon"]}</div>'
                f'<div style="flex:1">'
                f'<div style="font-size:0.83rem;color:#444;line-height:1.55;margin-bottom:0.55rem">'
                f'{loop["body"]}</div>'
                f'<div style="font-size:0.77rem;color:{c};font-weight:700;'
                f'border-top:1px solid {c}28;padding-top:0.4rem">{loop["action"]}</div>'
                f'</div></div></div>',
                unsafe_allow_html=True,
            )
