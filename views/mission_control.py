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


def render():
    col1, col2 = st.columns([8, 1])
    with col1:
        st.title("🎛️ Mission Control")
        st.caption("Creator's dashboard — SYNC_IN inbox, data coverage, research status, open loops")
    with col2:
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
    st.markdown("## 📥 SYNC_IN Inbox")

    pending_dir  = _BASE / "docs" / "REPO_SYNC" / "SYNC_IN" / "pending"
    processed_dir = _BASE / "docs" / "REPO_SYNC" / "SYNC_IN" / "processed"

    pending = sorted(
        [f for f in pending_dir.glob("*.md")],
        key=lambda p: p.stat().st_mtime, reverse=True,
    )

    if not pending:
        st.success("**Inbox clear** — no files waiting in SYNC_IN/pending/")
    else:
        st.warning(f"**{len(pending)} file(s) waiting for action**")
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
        st.markdown("**Recently processed:**")
        cols = st.columns(3)
        for i, f in enumerate(processed):
            modified = datetime.fromtimestamp(f.stat().st_mtime).strftime("%Y-%m-%d")
            cols[i % 3].caption(f"✅ {f.stem[:40]}  \n{modified}")


# ── Framework Coverage Matrix ─────────────────────────────────────────────────

def _render_coverage_matrix():
    st.markdown("## 📊 Framework Coverage Matrix")
    st.caption("Live read from worldview YAMLs. Trinity = matchups with full per-metric data. "
               "Levers = matchups with Phase 2 calibration. H2H = lever data present (both sides needed for button).")

    rows = _build_coverage()
    df = pd.DataFrame(rows)
    st.dataframe(df, use_container_width=True, hide_index=True)


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
                "Levers": "⬜ 0", "Lever Detail": "—",
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

        t_short = ", ".join(_SHORT.get(k, k) for k in trinity_keys) or "—"
        l_short = ", ".join(_SHORT.get(k, k) for k in lever_keys) or "—"

        rows.append({
            "Framework": wv_name,
            "Trinity": f"✅ {len(trinity_keys)}" if trinity_keys else "⬜ 0",
            "Trinity Detail": t_short,
            "Levers": f"✅ {len(lever_keys)}" if lever_keys else "⬜ 0",
            "Lever Detail": l_short,
            "H2H": "✅" if lever_keys else "⬜",
        })

    return rows


# ── Research Program Status ───────────────────────────────────────────────────

def _render_research_status():
    st.markdown("## 🔬 Research Program Status")

    col_ca, col_trinity = st.columns(2)

    with col_ca:
        st.markdown("### Cognitive Archaeology")
        st.markdown("""
| Phase | Focus | Status |
|-------|-------|--------|
| 0A | CFA transcript extraction | ✅ Complete |
| 0B | Negative control battery (17 extractors) | ✅ Complete |
| 0C | Positive control | ⏳ Pending |
| Full | Systematic worldview excavation | ⬜ Not started |
""")
        c1, c2, c3 = st.columns(3)
        c1.metric("Museum", "9 operators")
        c2.metric("Saturation", "0.50")
        c3.metric("Held", "1 candidate")
        st.caption("Phase 0C blocker: known-rich CFA transcript (Framework-G preferred) → Repo Claude")

    with col_trinity:
        st.markdown("### Trinity Batch Inventory")
        st.markdown("""
| Framework | Runs | Note |
|-----------|------|------|
| Classical Theism | 136 | ✅ Mature |
| Methodological Naturalism | 94 | ✅ Validated |
| Gnosticism | 212 | ✅ Largest set |
| Process Theology | 131 | ✅ Validated |
| Buddhism | 41 | 🟡 Newest |
| **Total** | **702** | |
""")
        st.caption("Source: BRIEFING_20260709_ARMADA_STATUS · as of 2026-07-09")


# ── Open Loops ────────────────────────────────────────────────────────────────

def _render_open_loops():
    st.markdown("## 🔓 Open Loops")
    st.caption("Known issues and pending decisions. Remove entries here as they're resolved.")

    LOOPS = [
        {
            "icon": "🟡",
            "title": "CA Phase 0C — positive control transcript needed",
            "body": (
                "Repo Claude needs a known-rich CFA deliberation transcript (Framework-G preferred) "
                "to run the positive control extraction battery — confirming the pipeline detects "
                "operators when they are genuinely present. Phase 0C is the last calibration step "
                "before full excavation begins. Pass the transcript to Repo Claude via SYNC_OUT request."
            ),
        },
        {
            "icon": "🔵",
            "title": "PT YAML — vs_buddhism misplaced in levers_by_matchup",
            "body": (
                "`PROCESS_THEOLOGY.yaml` has a `levers_by_matchup.vs_buddhism` block with Trinity "
                "score structure (batch_id, metrics, batch_stats) — misplaced during the Buddhism batch. "
                "It should live in `trinity_scores_by_matchup`. The coverage matrix correctly ignores "
                "it (no `collective_coherence_impact` field), so it causes no runtime issues. "
                "Fix when convenient — move the block to the right section."
            ),
        },
        {
            "icon": "🔵",
            "title": "Buddhism 2x2 design incomplete",
            "body": (
                "Buddhism has 41 subject runs (b_vs_ct: 10, b_vs_mdn: 11, b_vs_pt: 10, b_vs_g: 10). "
                "The reverse-stance runs (CT/MdN/PT/G as subject vs Buddhism as opponent) exist in "
                "those frameworks' folders and their YAMLs reference b_vs results, but the full "
                "closed 2x2 design (each framework both as subject and opponent vs Buddhism) isn't "
                "formally documented. Low urgency — awareness item."
            ),
        },
    ]

    for loop in LOOPS:
        with st.expander(f"{loop['icon']} {loop['title']}"):
            st.markdown(loop["body"])
