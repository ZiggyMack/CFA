"""
CFA v5.0 - Console (ENHANCED VERSION)
- Card-based layout with Ledger aesthetic
- New visualizations: Convergence Radar, Sensitivity Heatmap, Battle Cards
- Sidebar mode navigation (Compare, Analyze, Simulate, Audit)
- Progressive disclosure pattern
"""

import streamlit as st
import pandas as pd
import json
import re
import glob
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from utils.calculations import ypa_scenario_scores, guardrail_lever_coupling, guardrail_bfi_sensitivity, guardrail_weight_inversion, symmetry_audit, PF_TYPES
from utils.visualizations import create_lever_comparison_chart, create_ypa_trinity_chart
from utils.colors import CFA_COLORS, get_framework_color, get_preset_color
from utils.profile_loader import get_ypa_data, get_trinity_scores, get_framework_templates

# Import new components
from components.cards import (
    audit_card, audit_badge, status_summary_card, metric_card,
    framework_comparison_header
)
from components.charts import (
    create_convergence_radar, create_sensitivity_heatmap,
    create_battle_card_html, create_preset_compass,
    create_guardrail_grid, create_scenario_comparison_bars,
    create_lever_pie_charts, create_ypa_gauge, create_lever_radar_comparison
)

_PREFIX_TO_SUBJECT = {
    "CT":  "Classical Theism",
    "MdN": "Methodological Naturalism",
    "PT":  "Process Theology",
}

@st.cache_data(ttl=300)
def load_crux_data(worldview_prefix):
    """Scan golden session JSONs and return unique declared crux events for a batch.

    Handles two session schemas:
    - V1 (CT/MdN): scenario_{SUBJECT}_{OPPONENT}_{HHMMSS}.json in dashboard/SMV/src/data/
      Uses 'ticks' list with crux.status == 'declared'
    - V2 (PT/ARMADA): S7_cfa_trinity_{date}_{time}.json in SYNC_IN/pending/{5,6,7,8}/
      Uses 'component1_results' dict with crux_declared bool per metric
    """
    root = Path(__file__).resolve().parent.parent
    cruxes = []

    # --- V1 schema: dashboard/SMV/src/data/ ---
    data_dir = root / "dashboard" / "SMV" / "src" / "data"
    prefix_str = f"scenario_{worldview_prefix}_"
    for fpath in glob.glob(str(data_dir / f"scenario_{worldview_prefix}_*.json")):
        try:
            # Files are scenario_{SUBJECT}_{OPPONENT}_{HHMMSS}.json.
            # Real sessions end with a 6-digit HHMMSS timestamp; demo/example files
            # end with an 8-digit YYYYMMDD date (e.g. "E1_20260629") and are skipped.
            stem = Path(fpath).stem
            fname_key = stem[len(prefix_str):]          # e.g. "MdN_132540"
            last_part = fname_key.rsplit("_", 1)[-1]    # e.g. "132540"
            if not (last_part.isdigit() and len(last_part) == 6):
                continue
            with open(fpath, encoding="utf-8") as f:
                scenario = json.load(f)
            session_id = str(scenario.get("session_id", fname_key))
            condition = scenario.get("identity_condition", "unknown")
            seen_ids = set()
            for tick in scenario.get("ticks", []):
                crux = tick.get("crux", {})
                if crux.get("status") != "declared":
                    continue
                crux_id = crux.get("id") or f"{fname_key}_{tick.get('metric')}"
                if crux_id in seen_ids:
                    continue
                seen_ids.add(crux_id)
                narrative = tick.get("claude_narrative", "")
                deadlock = None
                dm = re.search(r'\*{0,2}Deadlock basis[:\s]*\*{0,2}\s*(.+?)(?:\n\n|\n(?=\*\*)|\Z)',
                               narrative, re.IGNORECASE | re.DOTALL)
                if dm:
                    deadlock = dm.group(1).replace('\n', ' ').strip()[:300]
                cruxes.append({
                    "session_id": session_id,
                    "condition": condition,
                    "metric": tick.get("metric"),
                    "metric_full": tick.get("metric_full"),
                    "round": tick.get("round"),
                    "classification": crux.get("classification", "unclassified"),
                    "description": crux.get("description", ""),
                    "deadlock": deadlock,
                    "claude_score": next((n["score"] for n in tick.get("nodes", []) if n.get("auditor") == "Claude"), None),
                    "grok_score": next((n["score"] for n in tick.get("nodes", []) if n.get("auditor") == "Grok"), None),
                })
        except Exception:
            continue

    # --- V2 schema: SYNC_IN/pending/5-8/ (ARMADA format) ---
    expected_subject = _PREFIX_TO_SUBJECT.get(worldview_prefix)
    if expected_subject:
        sync_pending = root / "docs" / "REPO_SYNC" / "SYNC_IN" / "pending"
        for folder in ["5", "6", "7", "8"]:
            folder_path = sync_pending / folder
            if not folder_path.exists():
                continue
            for fpath in glob.glob(str(folder_path / "S7_cfa_trinity_*.json")):
                try:
                    with open(fpath, encoding="utf-8") as f:
                        scenario = json.load(f)
                    if scenario.get("subject_framework") != expected_subject:
                        continue
                    session_id = str(scenario.get("session_id", Path(fpath).stem))
                    # "external" = golden (maps to identity_condition naming); "control" = control
                    raw_cond = scenario.get("condition", "unknown")
                    condition = "external_identity" if raw_cond == "external" else raw_cond
                    for metric, data in scenario.get("component1_results", {}).items():
                        if not isinstance(data, dict) or not data.get("crux_declared"):
                            continue
                        crux_info = data.get("crux_point") or {}
                        crux_id = crux_info.get("id") or f"{session_id}_{metric}"
                        cruxes.append({
                            "session_id": session_id,
                            "condition": condition,
                            "metric": metric,
                            "metric_full": data.get("metric_full", metric),
                            "round": data.get("rounds_taken"),
                            "classification": crux_info.get("type", "unclassified"),
                            "description": crux_info.get("description", ""),
                            "deadlock": None,
                            "claude_score": data.get("claude_score"),
                            "grok_score": data.get("grok_score"),
                        })
                except Exception:
                    continue

    return cruxes

# Backward compatibility: Load frameworks from profiles
MDN_DEFAULT = get_ypa_data("Methodological Naturalism")
CT_DEFAULT = get_ypa_data("Classical Theism")

def apply_loaded_run(run: dict):
    """Apply loaded JSON to session state"""
    cfg = run.get("config", {})
    if "lever_parity" in cfg:
        st.session_state["sidebar_lever_parity"] = cfg["lever_parity"]
    if "pf_type" in cfg:
        st.session_state["sidebar_pf_type"] = cfg["pf_type"]
    if "fallibilism_bonus" in cfg:
        st.session_state["sidebar_fallibilism"] = cfg["fallibilism_bonus"]
    if "bfi_debt_weight" in cfg:
        st.session_state["sidebar_bfi_weight"] = cfg["bfi_debt_weight"]

    A = run.get("framework_a", {})
    if "name" in A:
        st.session_state["fa_name"] = A["name"]
    if "bf_i" in A:
        st.session_state["fa_ax"] = A["bf_i"].get("axioms", 6)
        st.session_state["fa_db"] = A["bf_i"].get("debts", 4)
    if "admits_limits" in A:
        st.session_state["fa_ad"] = bool(A["admits_limits"])
    if "levers" in A:
        levers = A["levers"]
        st.session_state["fa_cci"] = float(levers.get("CCI", 5.0))
        st.session_state["fa_edb"] = float(levers.get("EDB", 5.0))
        st.session_state["fa_pfi"] = float(levers.get("PF_instrumental", 5.0))
        st.session_state["fa_pfe"] = float(levers.get("PF_existential", 5.0))
        st.session_state["fa_ar"] = float(levers.get("AR", 5.0))
        st.session_state["fa_mg"] = float(levers.get("MG", 5.0))

    B = run.get("framework_b", {})
    if "name" in B:
        st.session_state["fb_name"] = B["name"]
    if "bf_i" in B:
        st.session_state["fb_ax"] = B["bf_i"].get("axioms", 6)
        st.session_state["fb_db"] = B["bf_i"].get("debts", 4)
    if "admits_limits" in B:
        st.session_state["fb_ad"] = bool(B["admits_limits"])
    if "levers" in B:
        levers = B["levers"]
        st.session_state["fb_cci"] = float(levers.get("CCI", 5.0))
        st.session_state["fb_edb"] = float(levers.get("EDB", 5.0))
        st.session_state["fb_pfi"] = float(levers.get("PF_instrumental", 5.0))
        st.session_state["fb_pfe"] = float(levers.get("PF_existential", 5.0))
        st.session_state["fb_ar"] = float(levers.get("AR", 5.0))
        st.session_state["fb_mg"] = float(levers.get("MG", 5.0))

def detect_active_preset():
    """Detect which preset mode is currently active based on sidebar config"""
    # Read current sidebar values
    parity = st.session_state.get("sidebar_lever_parity", "ON")
    pf = st.session_state.get("sidebar_pf_type", "Holistic_50_50")
    fall = st.session_state.get("sidebar_fallibilism", "ON")
    bfi = st.session_state.get("sidebar_bfi_weight", "Equal_1.0x")

    # Normalize BFI weight naming (Heavier_1.2x and Weighted_1.2x are equivalent)
    bfi_normalized = "Weighted_1.2x" if bfi in ["Heavier_1.2x", "Weighted_1.2x"] else bfi

    # Check against known preset configurations (emojis match Brute Ledger)
    if parity == "OFF" and pf == "Instrumental" and fall == "ON" and bfi_normalized == "Weighted_1.2x":
        return "🔬 Skeptic"
    elif parity == "ON" and pf == "Holistic_50_50" and fall == "ON" and bfi == "Equal_1.0x":
        return "🤝 Diplomat"
    elif parity == "ON" and pf == "Composite_70_30" and fall == "ON" and bfi == "Equal_1.0x":
        return "🙏 Seeker"
    elif parity == "ON" and pf == "Holistic_50_50" and fall == "OFF" and bfi == "Equal_1.0x":
        return "👿 Zealot"
    else:
        return "⚙️ Custom"

@st.cache_data(ttl=300)
def _worldview_options():
    """Return sorted list of worldviews that have canonical YAML score files."""
    try:
        return sorted(get_framework_templates().keys())
    except Exception:
        return ["Classical Theism", "Methodological Naturalism", "Process Theology"]


_WV_EMOJI = {
    "Buddhism":                  "☸️",
    "Classical Theism":          "📕",
    "Desiderata Believers":      "🤔",
    "Error Theory":              "⛔",
    "Existentialism":            "🎭",
    "Hinduism":                  "🕉️",
    "Islam":                     "☪️",
    "Methodological Naturalism": "📘",
    "Mormonism":                 "📖",
    "Mormonism (LDS)":           "📖",
    "Null Hypothesis":           "❓",
    "Orthodox Judaism":          "🕎",
    "Process Theology":          "🌊",
}

def _wv_label(name: str) -> str:
    return f"{_WV_EMOJI.get(name, '🌐')} {name}"


def _get_crux_rates(wv_name: str, opponent_name: str) -> dict:
    """Return per-metric crux rates (0.0–1.0) from Trinity YAML for a given matchup pair.
    Handles both float and 'N/M' fraction string formats stored in the YAML.
    """
    trinity = get_trinity_scores(wv_name, opponent=opponent_name)
    if not trinity:
        return {}
    result = {}
    for metric, data in trinity.get("metrics", {}).items():
        if not isinstance(data, dict):
            continue
        raw = data.get("crux_rate")
        if raw is None:
            continue
        if isinstance(raw, str) and "/" in raw:
            try:
                num, den = raw.split("/")
                result[metric] = float(num) / float(den) if float(den) else 0.0
            except (ValueError, ZeroDivisionError):
                result[metric] = 0.0
        else:
            try:
                result[metric] = float(raw)
            except (TypeError, ValueError):
                result[metric] = 0.0
    return result


# Maps YAML lever keys → session-state suffix (fa_cci, fb_edb, etc.)
_LEVER_SS_KEYS = {
    "CCI": "cci", "EDB": "edb",
    "PF_instrumental": "pfi", "PF_existential": "pfe",
    "AR": "ar", "MG": "mg",
}


def _is_drifted(prefix: str) -> bool:
    """True if any lever slider has moved away from the loaded audit baseline."""
    baseline = st.session_state.get(f"{prefix}_audit_baseline", {})
    if not baseline:
        return False
    return any(
        abs(st.session_state.get(f"{prefix}_{_LEVER_SS_KEYS[k]}", 0.0) - v) > 0.005
        for k, v in baseline.items()
        if k in _LEVER_SS_KEYS
    )


def _store_audit_baseline(prefix: str, levers: dict, calibration_opponent) -> None:
    """Snapshot the loaded lever values as the audit baseline (or clear if unaudited)."""
    if calibration_opponent:
        st.session_state[f"{prefix}_audit_baseline"] = dict(levers)
    else:
        st.session_state.pop(f"{prefix}_audit_baseline", None)


def _get_audit_status(prefix: str, wv_name: str, opp_name: str) -> str:
    """Compute the 4-state audit caption by comparing current sliders against YAML live.

    No cached calibration_opponent state required — reads YAML fresh each render.
    This makes it immune to the Streamlit widget-reconciliation worldview reset bug.
    """
    if st.session_state.get("audit_mode", "Audit") == "Bias":
        if not wv_name:
            return "🎯 Prior (canonical, pre-experiment)"
        try:
            _canonical = get_ypa_data(wv_name)["levers"]  # no opponent → canonical values
        except Exception:
            return "🎯 Prior (canonical, pre-experiment)"
        _bias_match = all(
            abs(st.session_state.get(f"{prefix}_{_LEVER_SS_KEYS[k]}", 0.0) - v) <= 0.005
            for k, v in _canonical.items()
            if k in _LEVER_SS_KEYS
        )
        return "🎯 Prior (canonical, pre-experiment)" if _bias_match else "✏️ Customized"
    if not wv_name or not opp_name:
        return "📋 Unaudited"
    try:
        ypa = get_ypa_data(wv_name, opponent=opp_name)
    except Exception:
        return "📋 Unaudited"
    if not ypa.get("calibration_opponent"):
        return "📊 Audit TBD (bias data used)" if ypa.get("has_audit_data") else "📋 New profile"
    calibrated = ypa["levers"]
    sliders_match = all(
        abs(st.session_state.get(f"{prefix}_{_LEVER_SS_KEYS[k]}", 0.0) - v) <= 0.005
        for k, v in calibrated.items()
        if k in _LEVER_SS_KEYS
    )
    return "✅ Adversarially Audited" if sliders_match else "✏️ Customized"


def _on_fa_worldview_change():
    name = st.session_state.get("fa_name", "")
    opponent = st.session_state.get("fb_name", "")
    audit_mode = st.session_state.get("audit_mode", "Bias")
    if not name:
        return
    try:
        use_matchup = audit_mode == "Audit" and bool(opponent)
        ypa = get_ypa_data(name, opponent=opponent) if use_matchup else get_ypa_data(name)
        st.session_state["fa_ax"]  = ypa["bf_i"]["axioms"]
        st.session_state["fa_db"]  = ypa["bf_i"]["debts"]
        st.session_state["fa_ad"]  = ypa["admits_limits"]
        st.session_state["fa_cci"] = ypa["levers"]["CCI"]
        st.session_state["fa_edb"] = ypa["levers"]["EDB"]
        st.session_state["fa_pfi"] = ypa["levers"]["PF_instrumental"]
        st.session_state["fa_pfe"] = ypa["levers"]["PF_existential"]
        st.session_state["fa_ar"]  = ypa["levers"]["AR"]
        st.session_state["fa_mg"]  = ypa["levers"]["MG"]
        cal_opp = ypa.get("calibration_opponent")
        st.session_state["fa_calibration_opponent"] = cal_opp
        st.session_state["fa_has_audit_data"] = ypa.get("has_audit_data", False)
        _store_audit_baseline("fa", ypa["levers"], cal_opp)
    except Exception:
        pass
    # Refresh B's calibration status since its opponent just changed
    if opponent and audit_mode == "Audit":
        try:
            ypa_b = get_ypa_data(opponent, opponent=name)
            cal_opp_b = ypa_b.get("calibration_opponent")
            st.session_state["fb_calibration_opponent"] = cal_opp_b
            st.session_state["fb_has_audit_data"] = ypa_b.get("has_audit_data", False)
            _store_audit_baseline("fb", ypa_b["levers"], cal_opp_b)
        except Exception:
            pass


def _on_fb_worldview_change():
    name = st.session_state.get("fb_name", "")
    opponent = st.session_state.get("fa_name", "")
    audit_mode = st.session_state.get("audit_mode", "Bias")
    if not name:
        return
    try:
        use_matchup = audit_mode == "Audit" and bool(opponent)
        ypa = get_ypa_data(name, opponent=opponent) if use_matchup else get_ypa_data(name)
        st.session_state["fb_ax"]  = ypa["bf_i"]["axioms"]
        st.session_state["fb_db"]  = ypa["bf_i"]["debts"]
        st.session_state["fb_ad"]  = ypa["admits_limits"]
        st.session_state["fb_cci"] = ypa["levers"]["CCI"]
        st.session_state["fb_edb"] = ypa["levers"]["EDB"]
        st.session_state["fb_pfi"] = ypa["levers"]["PF_instrumental"]
        st.session_state["fb_pfe"] = ypa["levers"]["PF_existential"]
        st.session_state["fb_ar"]  = ypa["levers"]["AR"]
        st.session_state["fb_mg"]  = ypa["levers"]["MG"]
        cal_opp = ypa.get("calibration_opponent")
        st.session_state["fb_calibration_opponent"] = cal_opp
        st.session_state["fb_has_audit_data"] = ypa.get("has_audit_data", False)
        _store_audit_baseline("fb", ypa["levers"], cal_opp)
    except Exception:
        pass
    # Refresh A's calibration status since its opponent just changed
    if opponent and audit_mode == "Audit":
        try:
            ypa_a = get_ypa_data(opponent, opponent=name)
            cal_opp_a = ypa_a.get("calibration_opponent")
            st.session_state["fa_calibration_opponent"] = cal_opp_a
            st.session_state["fa_has_audit_data"] = ypa_a.get("has_audit_data", False)
            _store_audit_baseline("fa", ypa_a["levers"], cal_opp_a)
        except Exception:
            pass


def render():
    """Render console"""

    # audit_mode must be initialized first — lever init below is mode-aware
    if "audit_mode" not in st.session_state:
        st.session_state["audit_mode"] = "Audit"

    # Initialize session state (avoids Session State API warnings)
    if "fa_name" not in st.session_state:
        st.session_state["fa_name"] = MDN_DEFAULT["name"]
    if "fb_name" not in st.session_state:
        st.session_state["fb_name"] = CT_DEFAULT["name"]

    # On first load, initialize levers mode-aware so Audit mode shows ✅ immediately
    # without requiring an H2H click or dropdown re-select.
    if "fa_cci" not in st.session_state:
        _init_fa   = st.session_state["fa_name"]
        _init_fb   = st.session_state["fb_name"]
        _use_match = st.session_state["audit_mode"] == "Audit"
        try:
            _ypa_a = get_ypa_data(_init_fa, opponent=_init_fb) if _use_match else get_ypa_data(_init_fa)
            _ypa_b = get_ypa_data(_init_fb, opponent=_init_fa) if _use_match else get_ypa_data(_init_fb)
        except Exception:
            _ypa_a = MDN_DEFAULT
            _ypa_b = CT_DEFAULT
        for _pfx, _ypa in [("fa", _ypa_a), ("fb", _ypa_b)]:
            st.session_state[f"{_pfx}_ax"]  = _ypa["bf_i"]["axioms"]
            st.session_state[f"{_pfx}_db"]  = _ypa["bf_i"]["debts"]
            st.session_state[f"{_pfx}_ad"]  = _ypa["admits_limits"]
            st.session_state[f"{_pfx}_cci"] = _ypa["levers"]["CCI"]
            st.session_state[f"{_pfx}_edb"] = _ypa["levers"]["EDB"]
            st.session_state[f"{_pfx}_pfi"] = _ypa["levers"]["PF_instrumental"]
            st.session_state[f"{_pfx}_pfe"] = _ypa["levers"]["PF_existential"]
            st.session_state[f"{_pfx}_ar"]  = _ypa["levers"]["AR"]
            st.session_state[f"{_pfx}_mg"]  = _ypa["levers"]["MG"]
    
    # Enhanced CSS for card-based layout and Ledger aesthetic
    st.markdown("""
    <style>
    /* Make the sticky-header div stick to top while scrolling */
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

    /* Dark mode support */
    @media (prefers-color-scheme: dark) {
        .sticky-header {
            background-color: rgb(14, 17, 23) !important;
        }
    }

    /* Card-based layout styles */
    .cfa-card {
        background: #ffffff;
        border-radius: 8px;
        padding: 20px;
        margin: 10px 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #264653;
    }

    .cfa-card-header {
        font-family: Georgia, serif;
        color: #212529;
        border-bottom: 1px solid #dee2e6;
        padding-bottom: 10px;
        margin-bottom: 15px;
    }

    /* Status badges */
    .status-badge {
        padding: 2px 8px;
        border-radius: 12px;
        color: white;
        font-size: 0.8em;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    .badge-audited { background: #264653; }
    .badge-convergent { background: #2a9d8f; }
    .badge-draft { background: #e9c46a; color: #333; }
    .badge-crux { background: #f4a261; }
    .badge-divergent { background: #e76f51; }

    /* Metric cards */
    .metric-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
        gap: 15px;
        margin: 15px 0;
    }

    .metric-card {
        background: #ffffff;
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        border-top: 3px solid #264653;
        box-shadow: 0 2px 4px rgba(0,0,0,0.08);
    }

    .metric-label {
        font-size: 0.75em;
        color: #6c757d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 5px;
    }

    .metric-value {
        font-size: 1.5em;
        font-weight: bold;
        color: #212529;
    }

    /* Mode navigation pills */
    .mode-nav {
        display: flex;
        gap: 8px;
        padding: 10px 0;
        border-bottom: 1px solid #dee2e6;
        margin-bottom: 15px;
    }

    .mode-pill {
        padding: 6px 16px;
        border-radius: 20px;
        font-size: 0.85em;
        cursor: pointer;
        transition: all 0.2s;
        border: 1px solid #dee2e6;
        background: #f8f9fa;
        color: #495057;
    }

    .mode-pill.active {
        background: #264653;
        color: white;
        border-color: #264653;
    }

    .mode-pill:hover {
        background: #e9ecef;
    }

    .mode-pill.active:hover {
        background: #1a3a47;
    }
    </style>
    """, unsafe_allow_html=True)

    # Frozen position indicators (top-right corner, stacked vertically)
    active_preset = detect_active_preset()
    audit_mode = st.session_state.get("audit_mode", "Bias")  # Default to Bias mode
    include_crux = st.session_state.get("include_crux", True)  # Default to Include

    # Color coding for audit mode
    audit_color = "#28a745" if audit_mode == "Audit" else "#dc3545"  # Green for Audit, Red for Bias
    audit_icon = "🔍" if audit_mode == "Audit" else "🎯"

    # Crux indicator
    crux_status = "Include" if include_crux else "Exclude"
    crux_color = "#9b59b6" if include_crux else "#e67e22"  # Purple for Include, Orange for Exclude
    crux_icon = "⚖️" if include_crux else "🚫"

    st.markdown(f"""
    <div style="position: fixed; top: 80px; right: 15px; z-index: 9999; max-width: 200px;">
        <!-- Preset Mode Indicator -->
        <div style="background-color: rgba(255, 255, 255, 0.95);
                    border: 2px solid #1f77b4; border-radius: 6px;
                    padding: 6px 10px; margin-bottom: 8px;
                    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
                    max-width: 180px;">
            <div style="font-size: 0.7rem; font-weight: bold; color: #1f77b4; margin-bottom: 2px;">
                Active Mode
            </div>
            <div style="font-size: 0.9rem; font-weight: bold; color: #333;">
                {active_preset}
            </div>
            <div style="font-size: 0.65rem; color: {audit_color}; margin-top: 4px; font-weight: 600;">
                {audit_icon} {audit_mode} Mode
            </div>
            <div style="font-size: 0.65rem; color: {crux_color}; margin-top: 4px; font-weight: 600;">
                {crux_icon} Crux: {crux_status}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Header (sticky wrapper for persistent navigation)
    st.markdown('<div class="sticky-header">', unsafe_allow_html=True)
    col1, col2 = st.columns([6, 1])
    with col1:
        st.markdown('<p style="font-size:2.5rem;font-weight:bold;color:#1f77b4;">⚖️ CFA v5.0 Console</p>', unsafe_allow_html=True)
    with col2:
        if st.button("🏠 Home"):
            st.session_state.page = 'landing'
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('**"All Named, All Priced" — Interactive Comparison Tool**')
    st.markdown("---")

    # SIDEBAR
    st.sidebar.header("🎛️ Configuration")

    # Console Mode Navigation - placeholder for future expansion
    # Currently all modes show the same Compare view
    # Future: Analyze (single framework deep-dive), Simulate (toggle playground), Audit (Trinity details)

    # deps: preset_modes
    # Preset Mode Spectrum (MOVED TO TOP - user should select spectrum FIRST)
    with st.sidebar.expander("🎚️ Preset Mode Spectrum", expanded=False):
        st.markdown("**Quick Configuration Profiles:**")
        st.caption("⚠️ **IMPORTANT:** Select your spectrum mode FIRST, then load frameworks below!")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("🔬 Skeptic Mode", use_container_width=True):
                st.session_state["sidebar_lever_parity"] = "OFF"
                st.session_state["sidebar_pf_type"] = "Instrumental"
                st.session_state["sidebar_fallibilism"] = "ON"
                st.session_state["sidebar_bfi_weight"] = "Weighted_1.2x"
                st.session_state["include_crux"] = False  # skeptic distrusts contested scores
                st.rerun()  # Immediately reflect changes in indicator
            st.caption("MdN-optimized\nPredictive power focus")

            if st.button("🙏 Seeker Mode", use_container_width=True):
                st.session_state["sidebar_lever_parity"] = "ON"
                st.session_state["sidebar_pf_type"] = "Composite_70_30"
                st.session_state["sidebar_fallibilism"] = "ON"
                st.session_state["sidebar_bfi_weight"] = "Equal_1.0x"
                st.rerun()  # Immediately reflect changes in indicator
            st.caption("CT-leaning\nMeaning-first")

        with col2:
            if st.button("🤝 Diplomat Mode", use_container_width=True):
                st.session_state["sidebar_lever_parity"] = "ON"
                st.session_state["sidebar_pf_type"] = "Holistic_50_50"
                st.session_state["sidebar_fallibilism"] = "ON"
                st.session_state["sidebar_bfi_weight"] = "Equal_1.0x"
                st.rerun()  # Immediately reflect changes in indicator
            st.caption("Balanced bridge\nEqual weighting")

            if st.button("👿 Zealot Mode", use_container_width=True):
                st.session_state["sidebar_lever_parity"] = "ON"
                st.session_state["sidebar_pf_type"] = "Holistic_50_50"
                st.session_state["sidebar_fallibilism"] = "OFF"
                st.session_state["sidebar_bfi_weight"] = "Equal_1.0x"
                st.rerun()  # Immediately reflect changes in indicator
            st.caption("CT-optimized\nExistential-first")

        st.markdown("---")
        st.caption("💡 **Workflow:** 1️⃣ Pick spectrum mode → 2️⃣ Load frameworks below → 3️⃣ Adjust toggles if needed")

    st.sidebar.markdown("---")

    # Head-to-Head Pairings — button only appears when BOTH directions have
    # matchup-calibrated lever data (levers_by_matchup.vs_{opponent} in each YAML).
    # Add future pairings to _HH_PAIRS; readiness is auto-detected, no other changes needed.
    _HH_PAIRS = [
        ("Classical Theism",          "Methodological Naturalism", "📕 CT  vs  📘 MdN", "pair_ct_mdn"),
        ("Classical Theism",          "Process Theology",          "📕 CT  vs  🌊 PT",  "pair_ct_pt"),
        ("Process Theology",          "Methodological Naturalism", "🌊 PT  vs  📘 MdN", "pair_pt_mdn"),
        ("Classical Theism",          "Gnosticism",                "📕 CT  vs  🌀 GN",  "pair_ct_gn"),
        ("Methodological Naturalism", "Gnosticism",                "📘 MdN vs  🌀 GN",  "pair_mdn_gn"),
        ("Process Theology",          "Gnosticism",                "🌊 PT  vs  🌀 GN",  "pair_pt_gn"),
    ]

    _ready_pairs = []
    for _wv_a, _wv_b, _lbl, _key in _HH_PAIRS:
        try:
            _chk_a = get_ypa_data(_wv_a, opponent=_wv_b)
            _chk_b = get_ypa_data(_wv_b, opponent=_wv_a)
            if _chk_a.get("calibration_opponent") and _chk_b.get("calibration_opponent"):
                _ready_pairs.append((_wv_a, _wv_b, _lbl, _key))
        except Exception:
            pass

    with st.sidebar.expander("🎯 Head-to-Head Pairings", expanded=True):
        st.markdown("**Head-to-Head Pairings:**")
        st.caption("*Sets both A & B in one click*")
        if not _ready_pairs:
            st.caption("*No fully calibrated pairings yet.*")
        else:
            _pair_cols = st.columns(len(_ready_pairs))
            for _i, (_wv_a, _wv_b, _lbl, _key) in enumerate(_ready_pairs):
                with _pair_cols[_i]:
                    if st.button(_lbl, key=_key, use_container_width=True,
                                 help="Both directions calibrated — sets A & B with matchup-specific levers"):
                        _data_a = get_ypa_data(_wv_a, opponent=_wv_b)
                        _data_b = get_ypa_data(_wv_b, opponent=_wv_a)
                        for _ss, _d in [("fa", _data_a), ("fb", _data_b)]:
                            st.session_state[f"{_ss}_name"] = _d["name"]
                            st.session_state[f"{_ss}_ax"]   = _d["bf_i"]["axioms"]
                            st.session_state[f"{_ss}_db"]   = _d["bf_i"]["debts"]
                            st.session_state[f"{_ss}_ad"]   = _d["admits_limits"]
                            st.session_state[f"{_ss}_cci"]  = _d["levers"]["CCI"]
                            st.session_state[f"{_ss}_edb"]  = _d["levers"]["EDB"]
                            st.session_state[f"{_ss}_pfi"]  = _d["levers"]["PF_instrumental"]
                            st.session_state[f"{_ss}_pfe"]  = _d["levers"]["PF_existential"]
                            st.session_state[f"{_ss}_ar"]   = _d["levers"]["AR"]
                            st.session_state[f"{_ss}_mg"]   = _d["levers"]["MG"]
                            _cal_opp = _d.get("calibration_opponent")
                            st.session_state[f"{_ss}_calibration_opponent"] = _cal_opp
                            st.session_state[f"{_ss}_has_audit_data"] = _d.get("has_audit_data", False)
                            _store_audit_baseline(_ss, _d["levers"], _cal_opp)
                        st.rerun()


    st.sidebar.markdown("---")
    st.sidebar.markdown("### ⚙️ YPA Tuning")

    # Scoring Mode
    if "audit_mode" not in st.session_state:
        st.session_state["audit_mode"] = "Audit"
    audit_mode_options = ["Bias", "Audit"]
    audit_mode = st.sidebar.selectbox(
        "Scoring Mode",
        audit_mode_options,
        index=audit_mode_options.index(st.session_state.get("audit_mode", "Audit")),
        key="audit_mode_selector",
        help="**Bias Mode (🎯):** Full bias scoring — auditors apply their native lenses. **Audit Mode (🔍):** Adversarial audit — scores reflect Trinity convergence (display only for now; YPA wiring coming).",
    )
    if audit_mode != st.session_state.get("audit_mode"):
        st.session_state["audit_mode"] = audit_mode
        st.rerun()

    with st.sidebar.expander("🏷️ Badge guide"):
        st.markdown("""
**✅ Adversarially Audited**
Calibrated for this specific matchup via Trinity experiment.

**✏️ Customized**
You've moved a slider from the loaded baseline.

**📊 Audit TBD (bias data used)**
Worldview has audit history but not for this pairing yet — canonical priors shown.

**📋 New profile**
Pre-audit pipeline. Values are preliminary.
""")

    # Crux Impasses
    if "include_crux" not in st.session_state:
        st.session_state["include_crux"] = True
    include_crux_options = ["Include", "Exclude"]
    include_crux_sel = st.sidebar.selectbox(
        "Crux Impasses",
        include_crux_options,
        index=0 if st.session_state.get("include_crux", True) else 1,
        key="crux_selector",
        help="**Include:** Trust Trinity golden means as-is for all metrics. **Exclude (pessimistic):** Apply a proportional confidence dampening — lever × (1 − crux_rate × 0.15). Assumes disagreement signals overstatement. Note: direction is a stance, not a fact — the crux tells us *that* auditors disagreed, not *who was right*.",
    )
    new_include_crux = (include_crux_sel == "Include")
    include_crux = new_include_crux
    if new_include_crux != st.session_state.get("include_crux"):
        st.session_state["include_crux"] = new_include_crux
        st.rerun()

    # Initialize sidebar config defaults if not set
    if "sidebar_lever_parity" not in st.session_state:
        st.session_state["sidebar_lever_parity"] = "ON"
    if "sidebar_pf_type" not in st.session_state:
        st.session_state["sidebar_pf_type"] = "Holistic_50_50"
    if "sidebar_fallibilism" not in st.session_state:
        st.session_state["sidebar_fallibilism"] = "ON"
    if "sidebar_bfi_weight" not in st.session_state:
        st.session_state["sidebar_bfi_weight"] = "Equal_1.0x"

    # Lever-Parity selectbox
    parity_options = ["ON", "OFF"]
    current_parity_idx = parity_options.index(st.session_state.get("sidebar_lever_parity", "ON"))

    lever_parity = st.sidebar.selectbox(
        "Lever-Parity",
        parity_options,
        index=current_parity_idx,
        key="sidebar_lever_parity_widget",
        help="**Parity ON:** Moral norms (MG) count equally with epistemic norms. **OFF:** Focus on predictive power. [ΔYPA: OFF typically boosts MdN ~+0.2-0.3] Because CT includes moral realism, Parity ON increases MG weighting for both frameworks."
    )
    # Sync back to session state
    if lever_parity != st.session_state.get("sidebar_lever_parity"):
        st.session_state["sidebar_lever_parity"] = lever_parity
        st.rerun()

    # PF-Type selectbox
    current_pf_idx = PF_TYPES.index(st.session_state.get("sidebar_pf_type", "Holistic_50_50"))

    pf_type = st.sidebar.selectbox(
        "PF-Type",
        PF_TYPES,
        index=current_pf_idx,
        key="sidebar_pf_type_widget",
        help="**Instrumental:** Tech/predictive yield only. **Composite (70/30):** 70% instrumental, 30% existential. **Holistic (50/50):** Equal weight. [ΔYPA: Holistic favors CT ~+0.15-0.25] CT scores higher on existential fertility, so holistic weighting benefits CT."
    )
    # Sync back to session state
    if pf_type != st.session_state.get("sidebar_pf_type"):
        st.session_state["sidebar_pf_type"] = pf_type
        st.rerun()

    # Fallibilism-Bonus selectbox
    fall_options = ["ON", "OFF"]
    current_fall_idx = fall_options.index(st.session_state.get("sidebar_fallibilism", "ON"))

    fall_bonus = st.sidebar.selectbox(
        "Fallibilism-Bonus",
        fall_options,
        index=current_fall_idx,
        key="sidebar_fallibilism_widget",
        help="**Bonus ON:** Frameworks that admit limits get +0.3 CCI boost. **OFF:** No bonus. [ΔYPA: ON benefits both MdN and CT equally ~+0.03] Both frameworks acknowledge limitations, so both receive the fallibilism bonus when enabled."
    )
    # Sync back to session state
    if fall_bonus != st.session_state.get("sidebar_fallibilism"):
        st.session_state["sidebar_fallibilism"] = fall_bonus
        st.rerun()

    # BFI Debt Weight selectbox
    # Normalize "Heavier_1.2x" to "Weighted_1.2x" for display consistency
    if st.session_state.get("sidebar_bfi_weight") == "Heavier_1.2x":
        st.session_state["sidebar_bfi_weight"] = "Weighted_1.2x"

    bfi_options = ["Equal_1.0x", "Weighted_1.2x"]
    current_bfi_idx = bfi_options.index(st.session_state.get("sidebar_bfi_weight", "Equal_1.0x"))

    bfi_weight = st.sidebar.selectbox(
        "BFI Debt Weight",
        bfi_options,
        index=current_bfi_idx,
        key="sidebar_bfi_weight_widget",
        help="**Equal (1.0x):** Debts count same as axioms. **Weighted (1.2x):** Debts cost 20% more. [ΔYPA: Weighted slightly lowers both scores ~-0.05-0.10] Higher BFI denominator reduces YPA. Both frameworks have 4 debts, so weighted impacts both similarly."
    )
    # Sync back to session state
    if bfi_weight != st.session_state.get("sidebar_bfi_weight"):
        st.session_state["sidebar_bfi_weight"] = bfi_weight
        st.rerun()

    st.sidebar.markdown("---")

    # Sidebar Import
    st.sidebar.markdown("### 📥 Import")
    import_file_sidebar = st.sidebar.file_uploader("Load saved audit", type=["json"], key="import_sidebar")
    if import_file_sidebar:
        try:
            run = json.load(import_file_sidebar)
            if "config" in run:
                if st.sidebar.button("✅ Apply", key="apply_sidebar"):
                    apply_loaded_run(run)
                    st.rerun()
        except:
            st.sidebar.error("Invalid file")

    st.sidebar.markdown("---")

    # Current Config (moved below Import, now collapsible)
    cfg = {
        "lever_parity": lever_parity,
        "pf_type": pf_type,
        "fallibilism_bonus": fall_bonus,
        "bfi_debt_weight": bfi_weight,
        "audit_mode": audit_mode,
        "include_crux": include_crux
    }

    with st.sidebar.expander("📋 Current Config", expanded=False):
        st.json(cfg)

    # FRAMEWORK EDITORS
    swap_col, _ = st.columns([1, 5])
    with swap_col:
        if st.button("↔ Swap A & B", key="swap_ab_btn", help="Swap all Framework A and B values"):
            keys = ["name", "ax", "db", "ad", "cci", "edb", "pfi", "pfe", "ar", "mg", "calibration_opponent", "has_audit_data", "audit_baseline"]
            for k in keys:
                fa_k, fb_k = f"fa_{k}", f"fb_{k}"
                fa_val = st.session_state.get(fa_k)
                fb_val = st.session_state.get(fb_k)
                st.session_state[fa_k] = fb_val
                st.session_state[fb_k] = fa_val
            st.rerun()

    col1, col2 = st.columns(2)

    # FRAMEWORK A
    with col1:
        st.markdown("### 📘 Framework A")
        st.caption(_get_audit_status("fa", st.session_state.get("fa_name", ""), st.session_state.get("fb_name", "")))
        fa_name = st.selectbox("Worldview", options=_worldview_options(), key="fa_name", on_change=_on_fa_worldview_change, format_func=_wv_label)
        
        with st.expander("🔢 BFI", expanded=False):
            if 'custom_framework_ready' in st.session_state:
                custom = st.session_state['custom_framework_ready']
                if custom.get('target') == 'framework_a':
                    st.info(f"🔔 **Custom framework ready:** {custom['name']}")
                    if st.button("✅ Apply Custom Framework", key="apply_custom_a"):
                        st.session_state.fa_name = custom['name']
                        st.session_state.fa_ax = custom['axioms']
                        st.session_state.fa_db = custom['debts']
                        del st.session_state['custom_framework_ready']
                        st.rerun()
            
            fa_axioms = st.number_input("Axioms", min_value=1, max_value=30, key="fa_ax")
            fa_debts = st.number_input("Debts", min_value=0, max_value=30, key="fa_db")
            fa_admits = st.checkbox("Admits Limits", key="fa_ad")
            
            if st.button("🔍 Go to Brute Ledger", key="goto_ledger_a"):
                # Pass framework name for smart navigation
                st.session_state.ledger_nav_target = st.session_state.get("fa_name", "Methodological Naturalism")
                st.session_state.page = 'brute_ledger'
                st.rerun()
        
        # PER-FRAMEWORK PRESET BUTTONS (ABOVE SLIDERS - WORKING POSITION)
        st.markdown("**⚡ Quick Adjust:**")
        preset_a = st.columns(4)
        with preset_a[0]:
            if st.button("⚡ MAX", key="fa_max_btn", help="Set all to 10.0"):
                for k in ["fa_cci", "fa_edb", "fa_pfi", "fa_pfe", "fa_ar", "fa_mg"]:
                    st.session_state[k] = 10.0
                st.rerun()
        with preset_a[1]:
            if st.button("⚖️ MID", key="fa_mid_btn", help="Set all to 5.0"):
                for k in ["fa_cci", "fa_edb", "fa_pfi", "fa_pfe", "fa_ar", "fa_mg"]:
                    st.session_state[k] = 5.0
                st.rerun()
        with preset_a[2]:
            _fa_reset_name = st.session_state.get("fa_name", "Methodological Naturalism")
            if st.button("🔄 RESET", key="fa_reset_btn", help=f"Reset to {_fa_reset_name} audited values"):
                try:
                    _reset_a = get_ypa_data(_fa_reset_name)
                    st.session_state["fa_cci"] = _reset_a["levers"]["CCI"]
                    st.session_state["fa_edb"] = _reset_a["levers"]["EDB"]
                    st.session_state["fa_pfi"] = _reset_a["levers"]["PF_instrumental"]
                    st.session_state["fa_pfe"] = _reset_a["levers"]["PF_existential"]
                    st.session_state["fa_ar"]  = _reset_a["levers"]["AR"]
                    st.session_state["fa_mg"]  = _reset_a["levers"]["MG"]
                except Exception:
                    pass
                st.rerun()
        with preset_a[3]:
            if st.button("🚫 MIN", key="fa_min_btn", help="Set all to 0.0"):
                for k in ["fa_cci", "fa_edb", "fa_pfi", "fa_pfe", "fa_ar", "fa_mg"]:
                    st.session_state[k] = 0.0
                st.rerun()
        
        st.markdown("---")
        
        # SLIDERS
        fa_cci = st.slider("CCI - Coherence & Closure", 0.0, 10.0, step=0.1, key="fa_cci",
                          help="**Coherence & Closure Index:** How well the framework's concepts fit together and provide satisfying explanations. Higher = more internally consistent and complete.")
        fa_edb = st.slider("EDB - Explanatory Depth & Breadth", 0.0, 10.0, step=0.1, key="fa_edb",
                          help="**Explanatory Depth & Breadth:** Range and depth of phenomena the framework can explain. Higher = explains more domains (physics, ethics, consciousness) more thoroughly.")
        fa_pf_i = st.slider("PF-Instrumental", 0.0, 10.0, step=0.1, key="fa_pfi",
                           help="**Predictive Fertility (Instrumental):** How well the framework generates testable predictions and technological applications. Higher = more empirical/practical fruitfulness.")
        fa_pf_e = st.slider("PF-Existential", 0.0, 10.0, step=0.1, key="fa_pfe",
                           help="**Predictive Fertility (Existential):** How well the framework addresses meaning, purpose, and existential questions. Higher = more depth on 'why we're here' questions.")
        fa_ar = st.slider("AR - Aesthetic Resonance", 0.0, 10.0, step=0.1, key="fa_ar",
                         help="**Aesthetic Resonance:** How beautiful, elegant, or compelling the framework feels. Higher = greater intellectual/emotional appeal and motivational power.")
        fa_mg = st.slider("MG - Moral Generativity", 0.0, 10.0, step=0.1, key="fa_mg",
                         help="**Moral Generativity:** How well the framework grounds and generates moral norms. Higher = stronger foundation for ethics and values. [Weighted by Parity lever]")

        fa = {
            "name": fa_name,
            "bf_i": {"axioms": fa_axioms, "debts": fa_debts},
            "levers": {"CCI": fa_cci, "EDB": fa_edb, "PF_instrumental": fa_pf_i, "PF_existential": fa_pf_e, "AR": fa_ar, "MG": fa_mg},
            "admits_limits": fa_admits
        }

    # FRAMEWORK B
    with col2:
        st.markdown("### 📕 Framework B")
        st.caption(_get_audit_status("fb", st.session_state.get("fb_name", ""), st.session_state.get("fa_name", "")))
        fb_name = st.selectbox("Worldview", options=_worldview_options(), key="fb_name", on_change=_on_fb_worldview_change, format_func=_wv_label)
        
        with st.expander("🔢 BFI", expanded=False):
            if 'custom_framework_ready' in st.session_state:
                custom = st.session_state['custom_framework_ready']
                if custom.get('target') == 'framework_b':
                    st.info(f"🔔 **Custom framework ready:** {custom['name']}")
                    if st.button("✅ Apply Custom Framework", key="apply_custom_b"):
                        st.session_state.fb_name = custom['name']
                        st.session_state.fb_ax = custom['axioms']
                        st.session_state.fb_db = custom['debts']
                        del st.session_state['custom_framework_ready']
                        st.rerun()
            
            fb_axioms = st.number_input("Axioms", min_value=1, max_value=30, key="fb_ax")
            fb_debts = st.number_input("Debts", min_value=0, max_value=30, key="fb_db")
            fb_admits = st.checkbox("Admits Limits", key="fb_ad")
            
            if st.button("🔍 Go to Brute Ledger", key="goto_ledger_b"):
                # Pass framework name for smart navigation
                st.session_state.ledger_nav_target = st.session_state.get("fb_name", "Classical Theism")
                st.session_state.page = 'brute_ledger'
                st.rerun()
        
        # PER-FRAMEWORK PRESET BUTTONS (ABOVE SLIDERS - WORKING POSITION)
        st.markdown("**⚡ Quick Adjust:**")
        preset_b = st.columns(4)
        with preset_b[0]:
            if st.button("⚡ MAX", key="fb_max_btn", help="Set all to 10.0"):
                for k in ["fb_cci", "fb_edb", "fb_pfi", "fb_pfe", "fb_ar", "fb_mg"]:
                    st.session_state[k] = 10.0
                st.rerun()
        with preset_b[1]:
            if st.button("⚖️ MID", key="fb_mid_btn", help="Set all to 5.0"):
                for k in ["fb_cci", "fb_edb", "fb_pfi", "fb_pfe", "fb_ar", "fb_mg"]:
                    st.session_state[k] = 5.0
                st.rerun()
        with preset_b[2]:
            _fb_reset_name = st.session_state.get("fb_name", "Classical Theism")
            if st.button("🔄 RESET", key="fb_reset_btn", help=f"Reset to {_fb_reset_name} audited values"):
                try:
                    _reset_b = get_ypa_data(_fb_reset_name)
                    st.session_state["fb_cci"] = _reset_b["levers"]["CCI"]
                    st.session_state["fb_edb"] = _reset_b["levers"]["EDB"]
                    st.session_state["fb_pfi"] = _reset_b["levers"]["PF_instrumental"]
                    st.session_state["fb_pfe"] = _reset_b["levers"]["PF_existential"]
                    st.session_state["fb_ar"]  = _reset_b["levers"]["AR"]
                    st.session_state["fb_mg"]  = _reset_b["levers"]["MG"]
                except Exception:
                    pass
                st.rerun()
        with preset_b[3]:
            if st.button("🚫 MIN", key="fb_min_btn", help="Set all to 0.0"):
                for k in ["fb_cci", "fb_edb", "fb_pfi", "fb_pfe", "fb_ar", "fb_mg"]:
                    st.session_state[k] = 0.0
                st.rerun()
        
        st.markdown("---")
        
        # SLIDERS
        fb_cci = st.slider("CCI - Coherence & Closure", 0.0, 10.0, step=0.1, key="fb_cci",
                          help="**Coherence & Closure Index:** How well the framework's concepts fit together and provide satisfying explanations. Higher = more internally consistent and complete.")
        fb_edb = st.slider("EDB - Explanatory Depth & Breadth", 0.0, 10.0, step=0.1, key="fb_edb",
                          help="**Explanatory Depth & Breadth:** Range and depth of phenomena the framework can explain. Higher = explains more domains (physics, ethics, consciousness) more thoroughly.")
        fb_pf_i = st.slider("PF-Instrumental", 0.0, 10.0, step=0.1, key="fb_pfi",
                           help="**Predictive Fertility (Instrumental):** How well the framework generates testable predictions and technological applications. Higher = more empirical/practical fruitfulness.")
        fb_pf_e = st.slider("PF-Existential", 0.0, 10.0, step=0.1, key="fb_pfe",
                           help="**Predictive Fertility (Existential):** How well the framework addresses meaning, purpose, and existential questions. Higher = more depth on 'why we're here' questions.")
        fb_ar = st.slider("AR - Aesthetic Resonance", 0.0, 10.0, step=0.1, key="fb_ar",
                         help="**Aesthetic Resonance:** How beautiful, elegant, or compelling the framework feels. Higher = greater intellectual/emotional appeal and motivational power.")
        fb_mg = st.slider("MG - Moral Generativity", 0.0, 10.0, step=0.1, key="fb_mg",
                         help="**Moral Generativity:** How well the framework grounds and generates moral norms. Higher = stronger foundation for ethics and values. [Weighted by Parity lever]")

        fb = {
            "name": fb_name,
            "bf_i": {"axioms": fb_axioms, "debts": fb_debts},
            "levers": {"CCI": fb_cci, "EDB": fb_edb, "PF_instrumental": fb_pf_i, "PF_existential": fb_pf_e, "AR": fb_ar, "MG": fb_mg},
            "admits_limits": fb_admits
        }

    # Enrich both frameworks with matchup-specific crux rates (used by Crux-Exclude mode)
    fa["crux_rates"] = _get_crux_rates(fa_name, fb_name)
    fb["crux_rates"] = _get_crux_rates(fb_name, fa_name)

    st.markdown("---")

    # CALCULATE
    ya_results, ya_levers, ya_bfi = ypa_scenario_scores(fa, cfg)
    yb_results, yb_levers, yb_bfi = ypa_scenario_scores(fb, cfg)

    # Base lever sums (all-default cfg) for modifier effect row in battle card
    _base_cfg = {"lever_parity": "ON", "fallibilism_bonus": "ON", "pf_type": "Holistic_50_50", "include_crux": True, "bfi_debt_weight": "Equal_1.0x"}
    _, _ya_base_levers, _ = ypa_scenario_scores(fa, _base_cfg)
    _, _yb_base_levers, _ = ypa_scenario_scores(fb, _base_cfg)

    # YPA EXPLANATION (Grok Note #1: Pragmatic Clarity)
    st.info("💡 **YPA = Yield per Axiom:** Efficiency score = Total Lever Score ÷ BFI. Higher YPA = more output per assumption.")

    # Pre-compute guardrail ok flags — used by Guardrails tab grid
    ok1_a, _ = guardrail_lever_coupling(ya_levers["PF"], ya_levers["CCI"])
    ok2_a, _ = guardrail_bfi_sensitivity(ya_results["Neutral"]["YPA"], ya_bfi, ya_results["Empirical"]["YPA"], ya_results["Existential"]["YPA"])
    ok3_a, _ = guardrail_weight_inversion(ya_results, ya_results["Neutral"]["YPA"])
    audit_a_summary = symmetry_audit(fa, cfg)
    ok4_a = max(abs(row[3]) for row in audit_a_summary) <= 0.3

    ok1_b, _ = guardrail_lever_coupling(yb_levers["PF"], yb_levers["CCI"])
    ok2_b, _ = guardrail_bfi_sensitivity(yb_results["Neutral"]["YPA"], yb_bfi, yb_results["Empirical"]["YPA"], yb_results["Existential"]["YPA"])
    ok3_b, _ = guardrail_weight_inversion(yb_results, yb_results["Neutral"]["YPA"])
    audit_b_summary = symmetry_audit(fb, cfg)
    ok4_b = max(abs(row[3]) for row in audit_b_summary) <= 0.3

    # =========================================================================
    # FRAMEWORK COMPARISON HEADER (NEW)
    # =========================================================================
    st.markdown(framework_comparison_header(
        fa["name"], fb["name"],
        ya_results["Neutral"]["YPA"],
        yb_results["Neutral"]["YPA"]
    ), unsafe_allow_html=True)

    st.markdown("""
<style>
.stTabs [data-baseweb="tab-list"] { gap: 2rem; }
.stTabs [data-baseweb="tab"] {
    font-size: 1.05rem;
    font-weight: 500;
    padding-left: 0.75rem;
    padding-right: 0.75rem;
}
</style>
""", unsafe_allow_html=True)

    # TABS (Enhanced with new visualizations)
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Visual", "⚔️ Battle Card", "🔄 Symmetry", "🔬 Trinity Audit"])

    with tab1:
        # YPA Gauge meters
        st.markdown("### 🎯 YPA Performance")
        st.plotly_chart(create_ypa_gauge(
            ya_results["Neutral"]["YPA"],
            yb_results["Neutral"]["YPA"],
            fa["name"], fb["name"]
        ), use_container_width=True, key="chart_ypa_gauge")

        # Radar comparison
        st.markdown("### 🕸️ Lever Profile Radar")
        st.plotly_chart(create_lever_radar_comparison(ya_levers, yb_levers, fa["name"], fb["name"]), use_container_width=True, key="chart_lever_radar")

        # Pie charts for lever contribution
        st.markdown("### 🥧 Lever Contribution Breakdown")
        st.plotly_chart(create_lever_pie_charts(ya_levers, yb_levers, fa["name"], fb["name"]), use_container_width=True, key="chart_lever_pie")

        # Scenario Comparison Bars
        st.markdown("### 📊 Scenario Impact")
        st.plotly_chart(create_scenario_comparison_bars(ya_results, yb_results, fa["name"], fb["name"]), use_container_width=True, key="chart_scenario_bars")

    with tab2:
        # NEW: Battle Card visualization
        st.markdown("### ⚔️ Framework Battle Card")
        st.caption("*Head-to-head comparison showing which framework wins each lever*")

        st.markdown(create_battle_card_html(
            fa["name"], fb["name"],
            fa["levers"], fb["levers"],
            ya_results["Neutral"]["YPA"],
            yb_results["Neutral"]["YPA"],
            cfg={
                **cfg,
                "adj_sum_a":  sum(ya_levers.values()),
                "adj_sum_b":  sum(yb_levers.values()),
                "base_sum_a": sum(_ya_base_levers.values()),
                "base_sum_b": sum(_yb_base_levers.values()),
                "bfi_a":  ya_bfi,
                "bfi_b":  yb_bfi,
                "ax_a":   fa["bf_i"]["axioms"],
                "dbt_a":  fa["bf_i"]["debts"],
                "ax_b":   fb["bf_i"]["axioms"],
                "dbt_b":  fb["bf_i"]["debts"],
            }
        ), unsafe_allow_html=True)
        st.caption("*Modifier effect row: 🟢 green = modifiers helped · 🔴 red = modifiers hurt · gray = no change from defaults*")


        # NEW: Sensitivity Heatmap
        st.markdown("### 🌡️ Toggle Sensitivity Heatmap")
        st.caption("*How much does YPA change when each toggle is flipped?*")

        # Calculate sensitivity matrix (rows=frameworks, cols=toggles as returned by symmetry_audit)
        toggle_labels = [row[0] for row in audit_a_summary]
        sensitivity_matrix = []
        for audit_data in (audit_a_summary, audit_b_summary):
            delta_row = [r[3] for r in audit_data]  # Delta values
            sensitivity_matrix.append(delta_row)

        st.plotly_chart(create_sensitivity_heatmap(
            sensitivity_matrix,
            [fa["name"], fb["name"]],
            toggle_labels
        ), use_container_width=True, key="chart_sensitivity_heatmap")

        st.markdown("""
<div style="background:#12121f;border-left:4px solid #6c757d;padding:0.8rem 1.1rem;border-radius:0 6px 6px 0;margin:0.5rem 0 1rem 0;">
<p style="margin:0 0 0.4rem 0;font-size:0.85rem;color:#a0a0b0;font-weight:600;">How to read this</p>
<p style="margin:0 0 0.4rem 0;font-size:0.82rem;color:#c0c0d0;">
Each cell shows <strong style="color:#e0e0e0;">ΔYPA</strong> — how much that framework's score would shift if the column toggle were flipped from its current setting.
<strong style="color:#90EE90;">Green = score rises</strong>, <strong style="color:#e76f51;">red = score falls</strong>, near-zero = toggle doesn't move the needle.
</p>
<p style="margin:0;font-size:0.82rem;color:#c0c0d0;">
The toggle that moves the two frameworks in <em>opposite directions</em> is your configuration's hidden bias point — it's picking a side.
Here, <strong style="color:#e0e0e0;">PF-type</strong> is that toggle: switching to Instrumental helps MdN (strong on prediction) and hurts CT (strong on existential meaning), or vice versa.
</p>
</div>
""", unsafe_allow_html=True)

    with tab3:
        st.caption("How much does YPA shift when each configuration toggle is flipped? ⚠️ = sensitive (|Δ| > 0.3)")

        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"**{fa['name']}**")
            audit = symmetry_audit(fa, cfg)
            df = pd.DataFrame(audit, columns=["Toggle", "Base", "Flip", "Delta"])
            df["Flag"] = df["Delta"].apply(lambda x: "⚠️" if abs(x) > 0.3 else "✅")
            st.dataframe(df, use_container_width=True, hide_index=True)
            max_delta = max(abs(row[3]) for row in audit)
            sensitive_count = sum(1 for row in audit if abs(row[3]) > 0.3)
            if sensitive_count == 0:
                st.success(f"✅ Balanced — max Δ {max_delta:.2f}")
            elif sensitive_count <= 2:
                st.warning(f"⚠️ {sensitive_count} sensitive toggle(s) — max Δ {max_delta:.2f}")
            else:
                st.error(f"🚨 {sensitive_count} sensitive toggles — max Δ {max_delta:.2f}")

        with c2:
            st.markdown(f"**{fb['name']}**")
            audit = symmetry_audit(fb, cfg)
            df = pd.DataFrame(audit, columns=["Toggle", "Base", "Flip", "Delta"])
            df["Flag"] = df["Delta"].apply(lambda x: "⚠️" if abs(x) > 0.3 else "✅")
            st.dataframe(df, use_container_width=True, hide_index=True)
            max_delta = max(abs(row[3]) for row in audit)
            sensitive_count = sum(1 for row in audit if abs(row[3]) > 0.3)
            if sensitive_count == 0:
                st.success(f"✅ Balanced — max Δ {max_delta:.2f}")
            elif sensitive_count <= 2:
                st.warning(f"⚠️ {sensitive_count} sensitive toggle(s) — max Δ {max_delta:.2f}")
            else:
                st.error(f"🚨 {sensitive_count} sensitive toggles — max Δ {max_delta:.2f}")

        # CT-MdN philosophical callout
        _fa_lower = fa["name"].lower()
        _fb_lower = fb["name"].lower()
        _is_ct_mdn = (
            ("classical theism" in _fa_lower or "classical theism" in _fb_lower) and
            ("methodological naturalism" in _fa_lower or "methodological naturalism" in _fb_lower)
        )
        if _is_ct_mdn:
            st.markdown("""
<div style="background:#12121f;border-left:4px solid #d4a843;padding:0.9rem 1.2rem;border-radius:0 6px 6px 0;margin:1rem 0 0 0;">
<p style="margin:0 0 0.5rem 0;font-size:0.9rem;color:#d4a843;font-weight:600;">⚑ Why is this flag appearing — and is it a problem?</p>
<p style="margin:0 0 0.6rem 0;font-size:0.85rem;color:#c0c0d0;"><strong style="color:#e0e0e0;">Short answer: no.</strong> A sensitive toggle flag means the worldview has a <em>narrow-and-deep</em> profile — it has staked out a strong position rather than distributing strength broadly. Seeing one flag per worldview at comparable magnitude means the audit is detecting real philosophical architecture, not instrument error. The flag marks the <em>hinge point</em> where a worldview's specialization gets tested.</p>
<p style="margin:0 0 0.4rem 0;font-size:0.85rem;color:#c0c0d0;"><strong style="color:#e0e0e0;">CT → Lever-Parity:</strong> CT carries 7 axioms vs 4 debts — a structurally asymmetric ratio. Parity controls how that imbalance is weighted. CT feels it because its axiom-to-debt ratio is a fundamental feature of how it is built, not a measurement artifact.</p>
<p style="margin:0 0 0.4rem 0;font-size:0.85rem;color:#c0c0d0;"><strong style="color:#e0e0e0;">MdN → PF→Instrumental:</strong> MdN's identity is built around explaining, predicting, and intervening in the natural world. Switching to Composite blends in existential fertility — a domain MdN intentionally brackets. MdN scores lower there not because it fails, but because it doesn't try.</p>
<p style="margin:0;font-size:0.8rem;color:#707080;">Both flags appear because both worldviews are <em>specialists</em>, not generalists. That's a diagnostic about the frameworks — not a verdict on the ruler.</p>
</div>
""", unsafe_allow_html=True)
    
    # =========================================================================
    # TAB 4: TRINITY AUDIT (live data from golden batch)
    # =========================================================================
    with tab4:
        trinity_fa = get_trinity_scores(fa["name"], opponent=fb["name"])
        trinity_fb = get_trinity_scores(fb["name"], opponent=fa["name"])

        if not trinity_fa and not trinity_fb:
            st.info(f"🔬 **No Trinity Audit data for {fa['name']} vs {fb['name']} yet.**\n\nRun a golden batch experiment for this pairing to populate this tab.")
        else:
            trinity_ct  = trinity_fa
            trinity_mdn = trinity_fb

            if not trinity_ct and not trinity_mdn:
                st.error("Could not load Trinity scores from YAML profiles.")
            else:
                st.markdown(f"## 🔬 Trinity Audit — {fa['name']} ↔ {fb['name']}")
                st.caption("Golden batch deliberation results. Each framework audited as subject by its lens-aligned advocate.")

                _tab_labels = []
                if trinity_fa: _tab_labels.append(f"📕 {fa['name']} as Subject")
                if trinity_fb: _tab_labels.append(f"📘 {fb['name']} as Subject")
                if trinity_fa and trinity_fb: _tab_labels.append("⚖️ Cross-Stance Symmetry")
                audit_tabs = st.tabs(_tab_labels)
                _tab_idx = 0

                METRIC_ORDER_T = ["BFI", "CA", "IP", "ES", "LS", "MS", "PS"]

                def render_crux_analysis(worldview_prefix):
                    cruxes = load_crux_data(worldview_prefix)
                    if not cruxes:
                        st.caption("No crux data found — golden session JSONs not present.")
                        return
                    golden = [c for c in cruxes if c["condition"] == "external_identity"]
                    n_sessions = len(set(c["session_id"] for c in golden))
                    avg_per = round(len(golden) / n_sessions, 1) if n_sessions else 0
                    st.caption(f"**{avg_per} crux impasses per session** ({len(golden)} total across {n_sessions} golden sessions)")

                    # Summary breakdown — build full-name lookup from crux data
                    metric_full_map = {}
                    by_metric = {}
                    by_class = {}
                    for c in golden:
                        key = c["metric"]
                        by_metric[key] = by_metric.get(key, 0) + 1
                        by_class[c["classification"]] = by_class.get(c["classification"], 0) + 1
                        if key not in metric_full_map and c.get("metric_full"):
                            metric_full_map[key] = c["metric_full"]

                    col_m, col_c = st.columns(2)
                    with col_m:
                        st.markdown("**By Metric**")
                        max_cnt = max(by_metric.values()) if by_metric else 1
                        for metric, cnt in sorted(by_metric.items(), key=lambda x: -x[1]):
                            full = metric_full_map.get(metric, metric)
                            bar = "█" * cnt + "░" * (max_cnt - cnt)
                            lc, rc = st.columns([5, 3])
                            lc.markdown(f"**{full}**")
                            rc.markdown(f"{bar} **{cnt}**")
                    with col_c:
                        st.markdown("**By Classification**")
                        for cls, cnt in sorted(by_class.items(), key=lambda x: -x[1]):
                            st.markdown(f"- **{cls}**: {cnt}")

                    # Grouped by metric — one expander per metric, table inside
                    st.markdown("---")
                    METRIC_ORDER_C = ["BFI", "CA", "IP", "ES", "LS", "MS", "PS"]
                    grouped = {}
                    for c in golden:
                        grouped.setdefault(c["metric"], []).append(c)

                    for metric in METRIC_ORDER_C:
                        if metric not in grouped:
                            continue
                        items = grouped[metric]
                        full_name = metric_full_map.get(metric, metric)
                        cls_summary = {}
                        for c in items:
                            cls_summary[c["classification"]] = cls_summary.get(c["classification"], 0) + 1
                        cls_str = " · ".join(f"{cls} ({n})" for cls, n in sorted(cls_summary.items(), key=lambda x: -x[1]))
                        label = f"⚑ {full_name} — {len(items)} crux{'es' if len(items) != 1 else ''} · {cls_str}"
                        with st.expander(label, expanded=False):
                            rows = []
                            for c in sorted(items, key=lambda x: x["session_id"]):
                                rows.append({
                                    "Session": c["session_id"],
                                    "R": c["round"] if c["round"] is not None else "—",
                                    "Claude": c["claude_score"] if c["claude_score"] is not None else "—",
                                    "Grok": c["grok_score"] if c["grok_score"] is not None else "—",
                                    "Type": c["classification"],
                                    "Deadlock Basis": (c["deadlock"] or c["description"] or "—")[:120],
                                })
                            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

                def render_trinity_tab(trinity, subject_label, claude_role, grok_role, delta_label, delta_claude_key, delta_grok_key, extra_delta_label=None, extra_delta_claude_key=None, extra_delta_grok_key=None, crux_prefix=None):
                    if not trinity:
                        st.info(f"No Trinity data loaded for {subject_label}.")
                        return
                    summary = trinity.get("batch_summary", {})
                    st.caption(
                        f"**Experiment:** {trinity.get('experiment_id', '')}  ·  "
                        f"**Status:** {trinity.get('score_audit_status', '')}"
                    )
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Avg Convergence", f"{summary.get('avg_convergence_pct', 0)}%")
                    col2.metric("Avg Rounds", str(summary.get('avg_rounds', 0)))
                    col3.metric("Crux Impasses/Session", str(summary.get('avg_crux_per_run', '—')))
                    ctrl = summary.get('control_avg_convergence_pct')
                    col4.metric("Control Convergence" if ctrl else "Avg Crux/Run",
                                f"{ctrl}%" if ctrl else str(summary.get('avg_crux_per_run', '—')))

                    st.markdown(f"---\n### Per-Metric Results — {subject_label} (n=10)")
                    st.caption(f"Claude = {claude_role} · Grok = {grok_role}")

                    with st.expander("📖 Metric Definitions — What the auditors scored", expanded=False):
                        st.markdown("""
Each metric was scored 0–10 by both auditors independently, then deliberated to convergence (or crux). Definitions below are what auditors were instructed to evaluate against.

| Metric | Full Name | Scoring Question |
|--------|-----------|-----------------|
| **BFI** | Beings, Foundational Importance | Does this worldview provide a compelling account of *why anything exists at all*? Does it ground being-ness itself, or does existence arrive as a brute fact? |
| **CA** | Causal Attribution | Does this worldview coherently explain causal structure — what causes what, why causal chains hold, and what ultimately grounds the causal order of reality? |
| **IP** | Intellectual Pedigree | Has this worldview generated sustained, rigorous philosophical engagement? Is it anchored in a tradition deep enough that its core claims have been seriously stress-tested? |
| **ES** | Explanatory Scope | How broad is this worldview's explanatory reach across domains — physical, moral, aesthetic, existential? Can it address diverse phenomena without category errors or ad hoc patches? |
| **LS** | Logical Soundness | Are the worldview's core propositions internally consistent? Does it avoid contradiction, question-begging, and logical incoherence under adversarial pressure? |
| **MS** | Moral Substance | Can this worldview ground moral claims in something more than preference or convention? Does it have the ontological resources to make morality *real* rather than merely felt? |
| **PS** | Practical Significance | Does this worldview make a *difference* for how one ought to live? Is it actionable — does it provide genuine orientation for real human decisions and values? |

*Scores are assigned under adversarial identity conditions: the PRO auditor argues from the worldview's strongest case; the ANTI auditor applies the opposing lens. Convergence is required above 98% or a crux is declared.*
                        """)

                    metrics = trinity.get("metrics", {})
                    rows = []
                    for key in METRIC_ORDER_T:
                        if key not in metrics:
                            continue
                        m = metrics[key]
                        cd = m.get(delta_claude_key, 0)
                        gd = m.get(delta_grok_key, 0)
                        row = {
                            "Metric": f"{key} — {m.get('full_name', '')}",
                            "Claude": f"{m.get('claude_mean','?')} ±{m.get('claude_sd','?')}",
                            "Grok": f"{m.get('grok_mean','?')} ±{m.get('grok_sd','?')}",
                            "Spread": m.get("spread", "?"),
                            "Conv %": f"{m.get('convergence_pct','?')}%",
                            "Rounds": m.get("avg_rounds", "?"),
                            f"Claude {delta_label}": f"{'+' if cd >= 0 else ''}{cd}",
                            f"Grok {delta_label}": f"{'+' if gd >= 0 else ''}{gd}",
                            "Layer": m.get("divergence_layer", "?"),
                        }
                        if extra_delta_label and extra_delta_claude_key:
                            ecd = m.get(extra_delta_claude_key, "—")
                            egd = m.get(extra_delta_grok_key, "—")
                            if ecd != "—": ecd = f"{'+' if ecd >= 0 else ''}{ecd}"
                            if egd != "—": egd = f"{'+' if egd >= 0 else ''}{egd}"
                            row[f"Claude {extra_delta_label}"] = ecd
                            row[f"Grok {extra_delta_label}"] = egd
                        rows.append(row)
                    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

                    with st.expander("📐 Divergence Layer Definitions (DBEP Framework)", expanded=False):
                        st.markdown("""
The **Layer** column identifies *where in the epistemic stack* the divergence originates — not just that auditors disagree, but **why** the disagreement is structurally resistant to resolution.

| Layer | What it means | Debate signature |
|-------|---------------|-----------------|
| **Definitions** | Auditors are answering *different questions* — the metric term is underspecified and each auditor samples a different definition | Massive score spread; participants appear to talk past each other; high variance across sessions |
| **Beliefs** | Shared definitions, but different fundamental metaphysical commitments about what is true | Moderate, stable disagreement; communication is possible but convergence stalls at a principled gap |
| **Expectations** | Shared beliefs, different anticipations of what evidence or explanation should look like | "You're ignoring X" arguments; auditors notice different features of the same evidence |
| **Perceptions** | Shared framework, but different evaluative registrations of the same content | Soft disagreements; value-weighting and aesthetic differences in how arguments land |

**DBEP Stack:** Stories → Possibility Space → **Definitions → Beliefs → Expectations → Perceptions** → Evaluation

CFA scores live at *Evaluation*. Divergence can originate at any upstream layer. Tagging the layer turns a disagreement into a diagnostic: *is this an argument about what the words mean, or about what is true, or about what counts as evidence?*

*Source: DBEP framework developed collaboratively across CFA Phase 1 batch analysis (2026-06-29).*
                        """)

                    st.markdown("### Key Findings")
                    for finding in summary.get("key_findings", []):
                        st.markdown(f"- {finding}")

                    with st.expander("⚑ Crux Analysis", expanded=False):
                        if crux_prefix:
                            render_crux_analysis(crux_prefix)
                        else:
                            st.caption("Crux prefix not configured for this tab.")

                    with st.expander("📋 Session IDs", expanded=False):
                        ids = trinity.get("session_ids", {})
                        c1, c2 = st.columns(2)
                        with c1:
                            st.markdown("**Golden (External Identity)**")
                            for s in ids.get("golden", []):
                                st.code(s)
                        with c2:
                            st.markdown("**Control (No Identity)**")
                            for s in ids.get("control", []):
                                st.code(s)
                            if not ids.get("control"):
                                st.caption("No control batch for this experiment.")

                def _has_role_swap(trinity):
                    m = trinity.get("metrics", {}) if trinity else {}
                    return any("role_swap_delta_claude" in v for v in m.values())

                _CRUX_PREFIX = {
                    "Classical Theism": "CT",
                    "Methodological Naturalism": "MdN",
                    "Process Theology": "PT",
                }

                if trinity_fa:
                    with audit_tabs[_tab_idx]:
                        _fa_abbrev = "".join(w[0].upper() for w in fa["name"].split()[:3])
                        _has_rs = _has_role_swap(trinity_fa)
                        render_trinity_tab(trinity_fa, fa["name"], f"PRO-{_fa_abbrev}", f"ANTI-{_fa_abbrev}",
                                           "Role-Swap Δ" if _has_rs else "Identity Δ",
                                           "role_swap_delta_claude" if _has_rs else "identity_delta_claude",
                                           "role_swap_delta_grok" if _has_rs else "identity_delta_grok",
                                           extra_delta_label="Identity Δ" if _has_rs else None,
                                           extra_delta_claude_key="identity_delta_claude" if _has_rs else None,
                                           extra_delta_grok_key="identity_delta_grok" if _has_rs else None,
                                           crux_prefix=_CRUX_PREFIX.get(fa["name"]))
                    _tab_idx += 1

                if trinity_fb:
                    with audit_tabs[_tab_idx]:
                        _fb_abbrev = "".join(w[0].upper() for w in fb["name"].split()[:3])
                        _has_rs = _has_role_swap(trinity_fb)
                        render_trinity_tab(trinity_fb, fb["name"], f"PRO-{_fb_abbrev}", f"ANTI-{_fb_abbrev}",
                                           "Role-Swap Δ" if _has_rs else "Identity Δ",
                                           "role_swap_delta_claude" if _has_rs else "identity_delta_claude",
                                           "role_swap_delta_grok" if _has_rs else "identity_delta_grok",
                                           extra_delta_label="Identity Δ" if _has_rs else None,
                                           extra_delta_claude_key="identity_delta_claude" if _has_rs else None,
                                           extra_delta_grok_key="identity_delta_grok" if _has_rs else None,
                                           crux_prefix=_CRUX_PREFIX.get(fb["name"]))
                    _tab_idx += 1

                if trinity_fa and trinity_fb:
                    with audit_tabs[_tab_idx]:
                        st.markdown("### Cross-Stance Role-Swap Deltas")
                        st.caption("How much each auditor's score shifts when switching from one stance to the other")
                        _cs_fa_m = trinity_fa.get("metrics", {})
                        _cs_fb_m = trinity_fb.get("metrics", {})
                        sym_rows = []
                        for key in METRIC_ORDER_T:
                            if key not in _cs_fa_m or key not in _cs_fb_m:
                                continue
                            _cs_fa = _cs_fa_m[key]
                            _cs_fb = _cs_fb_m[key]

                            def _fmt_delta(a, b):
                                if isinstance(a, (int, float)) and isinstance(b, (int, float)):
                                    d = round(b - a, 2)
                                    return f"+{d}" if d >= 0 else str(d)
                                return "?"

                            sym_rows.append({
                                "Metric": key,
                                f"Claude PRO-{_fa_abbrev}": _cs_fa.get("claude_mean", "?"),
                                f"Claude ANTI-{_fb_abbrev}": _cs_fb.get("claude_mean", "?"),
                                "Claude Δ": _fmt_delta(_cs_fa.get("claude_mean"), _cs_fb.get("claude_mean")),
                                f"Grok ANTI-{_fa_abbrev}": _cs_fa.get("grok_mean", "?"),
                                f"Grok PRO-{_fb_abbrev}": _cs_fb.get("grok_mean", "?"),
                                "Grok Δ": _fmt_delta(_cs_fa.get("grok_mean"), _cs_fb.get("grok_mean")),
                                f"{_fa_abbrev} Conv%": f"{_cs_fa.get('convergence_pct','?')}%",
                                f"{_fb_abbrev} Conv%": f"{_cs_fb.get('convergence_pct','?')}%",
                            })
                        st.dataframe(pd.DataFrame(sym_rows), use_container_width=True, hide_index=True)
                        st.markdown("### Instrument Stability")
                        stab = trinity_fb.get("batch_summary", {}).get("instrument_stability", {})
                        if stab:
                            _fa_k = _fa_abbrev.lower()
                            _fb_k = _fb_abbrev.lower()
                            c1, c2, c3, c4 = st.columns(4)
                            c1.metric(f"{_fa_abbrev} Avg Conv", f"{stab.get(f'{_fa_k}_golden_avg_convergence', stab.get('ct_golden_avg_convergence','?'))}%")
                            c2.metric(f"{_fb_abbrev} Avg Conv", f"{stab.get(f'{_fb_k}_golden_avg_convergence', stab.get('mdn_golden_avg_convergence','?'))}%")
                            c3.metric(f"{_fa_abbrev} Avg Rounds", str(stab.get(f'{_fa_k}_golden_avg_rounds', stab.get('ct_golden_avg_rounds','?'))))
                            c4.metric(f"{_fb_abbrev} Avg Rounds", str(stab.get(f'{_fb_k}_golden_avg_rounds', stab.get('mdn_golden_avg_rounds','?'))))
                            st.caption(stab.get("interpretation", ""))

                        # --- Key Finding: Asymmetric Identity Pressure (CT vs MdN specific) ---
                        _is_ct_mdn_pair = (
                            {fa["name"], fb["name"]} == {"Classical Theism", "Methodological Naturalism"}
                        )
                        if _is_ct_mdn_pair:
                            st.markdown("### Key Finding: Asymmetric Identity Pressure")
                            id_claude = {k: _cs_fa_m[k].get("identity_delta_claude", 0) for k in METRIC_ORDER_T if k in _cs_fa_m}
                            id_grok   = {k: _cs_fa_m[k].get("identity_delta_grok",   0) for k in METRIC_ORDER_T if k in _cs_fa_m}
                            n = len(id_claude)
                            avg_claude_id = round(sum(id_claude.values()) / n, 2) if n else 0
                            avg_grok_id   = round(sum(id_grok.values())   / n, 2) if n else 0
                            grok_harder_ct = sum(
                                1 for k in id_claude
                                if id_grok[k] < 0 and abs(id_grok[k]) > abs(id_claude[k])
                            )
                            largest_gap = max(
                                (abs(id_grok[k]) - abs(id_claude[k]), k) for k in id_claude
                            )
                            metric_full_map_s = {
                                "BFI": "Beings, Foundational Importance",
                                "CA":  "Causal Attribution",
                                "IP":  "Intellectual Pedigree",
                                "ES":  "Explanatory Scope",
                                "LS":  "Logical Soundness",
                                "MS":  "Moral Substance",
                                "PS":  "Practical Significance",
                            }
                            st.markdown(f"""
<div style="background:#1a1a2e;border-left:4px solid #e94560;padding:1rem 1.2rem;border-radius:0 6px 6px 0;margin:0.5rem 0 1rem 0;">
<p style="margin:0 0 0.6rem 0;font-size:0.95rem;color:#e0e0e0;">
<strong style="color:#e94560;">Identity loading deflates the ANTI-CT auditor (Grok) substantially harder than the PRO-CT auditor (Claude)</strong>
across the CT golden batch — on <strong>{grok_harder_ct} of {n} metrics</strong>, Grok's identity-induced deflation is larger in magnitude.
</p>
<p style="margin:0 0 0.6rem 0;font-size:0.9rem;color:#b0b0c0;">
Avg identity Δ — <strong style="color:#7ec8e3;">Claude (PRO-CT): {avg_claude_id:+.2f}</strong> &nbsp;|&nbsp;
<strong style="color:#e94560;">Grok (ANTI-CT): {avg_grok_id:+.2f}</strong> &nbsp;·&nbsp;
Largest gap: <em>{metric_full_map_s.get(largest_gap[1], largest_gap[1])}</em> ({largest_gap[0]:+.2f} pts)
</p>
<p style="margin:0 0 0.4rem 0;font-size:0.85rem;color:#909090;">
<strong style="color:#d4a843;">Why this is a finding about the frameworks, not the instrument:</strong>
CT makes metaphysical claims (PSR, divine simplicity, final causality, teleology) that present rich surface area
for empirical challenge. MdN is itself built on empirical methodology — so an empirical auditor scoring MdN
has less adversarial purchase; the lens and the subject are aligned. The asymmetric pressure is philosophically
principled. The instrument is measuring a real structural fact: CT is a harder target for the empirical lens
than MdN is for the teleological lens.
</p>
</div>
""", unsafe_allow_html=True)

    # deps: preset_modes
    # EPISTEMIC QUIZ SYSTEM
    st.markdown("---")
    with st.expander("🧠 Epistemic Quiz - Find Your Starting Point", expanded=False):
        st.markdown("**Answer 5 questions to auto-detect your bias profile**")
        st.caption("We'll automatically load the preset mode that matches your epistemology")
        
        # Question 1: Evidence Priority
        q1 = st.radio(
            "**Q1:** What matters more in evaluating a worldview?",
            ["Predictive accuracy and testable results", 
             "Both prediction and meaning equally", 
             "Comprehensive explanation and existential depth"],
            key="quiz_q1"
        )
        
        # Question 2: Moral Foundations
        q2 = st.radio(
            "**Q2:** Where do moral truths come from?",
            ["Human consensus and evolutionary adaptation",
             "A mix of objective and subjective factors",
             "Transcendent moral order grounded in ultimate reality"],
            key="quiz_q2"
        )
        
        # Question 3: Uncertainty Tolerance
        q3 = st.radio(
            "**Q3:** How comfortable are you with unanswered questions?",
            ["Very comfortable - some questions may be permanently unanswerable",
             "Somewhat comfortable - we should keep searching",
             "Uncomfortable - ultimate answers exist even if we haven't found them yet"],
            key="quiz_q3"
        )
        
        # Question 4: Success Explanation
        q4 = st.radio(
            "**Q4:** Why does science work so well?",
            ["Evolutionary pressure + methodological discipline",
             "Both method and the nature of reality contribute",
             "Reality is fundamentally intelligible/rational by design"],
            key="quiz_q4"
        )
        
        # Question 5: Starting Assumptions
        q5 = st.radio(
            "**Q5:** How do you feel about taking on additional axioms?",
            ["Minimize assumptions - prefer lean frameworks",
             "Balance parsimony with explanatory power",
             "Accept necessary axioms if they provide comprehensive answers"],
            key="quiz_q5"
        )
        
        if st.button("🎯 Auto-Detect My Profile", use_container_width=True, type="primary"):
            # Scoring logic
            scores = {"skeptic": 0, "diplomat": 0, "seeker": 0, "zealot": 0}
            
            # Q1 scoring
            if "Predictive accuracy" in q1:
                scores["skeptic"] += 2
            elif "Both prediction" in q1:
                scores["diplomat"] += 2
            else:
                scores["zealot"] += 2
            
            # Q2 scoring
            if "Human consensus" in q2:
                scores["skeptic"] += 2
            elif "mix of objective" in q2:
                scores["diplomat"] += 2
            else:
                scores["zealot"] += 2
            
            # Q3 scoring
            if "Very comfortable" in q3:
                scores["skeptic"] += 2
            elif "Somewhat comfortable" in q3:
                scores["diplomat"] += 1
                scores["seeker"] += 1
            else:
                scores["zealot"] += 2
            
            # Q4 scoring
            if "Evolutionary pressure" in q4:
                scores["skeptic"] += 2
            elif "Both method" in q4:
                scores["diplomat"] += 2
            else:
                scores["zealot"] += 2
            
            # Q5 scoring
            if "Minimize assumptions" in q5:
                scores["skeptic"] += 2
            elif "Balance parsimony" in q5:
                scores["diplomat"] += 2
            else:
                scores["seeker"] += 1
                scores["zealot"] += 1
            
            # Determine winner
            winner = max(scores, key=scores.get)
            
            # Load corresponding mode
            if winner == "skeptic":
                st.session_state["lever_parity"] = "OFF"
                st.session_state["pf_type"] = "Instrumental"
                st.session_state["fallibilism_bonus"] = "ON"
                st.session_state["bfi_debt_weight"] = "Heavier_1.2x"
                st.success("✅ **Profile Detected: Skeptic Mode** (MdN-optimized, predictive power focus)")
            elif winner == "diplomat":
                st.session_state["lever_parity"] = "ON"
                st.session_state["pf_type"] = "Holistic_50_50"
                st.session_state["fallibilism_bonus"] = "ON"
                st.session_state["bfi_debt_weight"] = "Equal_1.0x"
                st.success("✅ **Profile Detected: Diplomat Mode** (Balanced bridge, equal weighting)")
            elif winner == "seeker":
                st.session_state["lever_parity"] = "ON"
                st.session_state["pf_type"] = "Composite_70_30"
                st.session_state["fallibilism_bonus"] = "ON"
                st.session_state["bfi_debt_weight"] = "Equal_1.0x"
                st.success("✅ **Profile Detected: Seeker Mode** (CT-leaning, meaning-first)")
            else:  # zealot
                st.session_state["lever_parity"] = "ON"
                st.session_state["pf_type"] = "Holistic_50_50"
                st.session_state["fallibilism_bonus"] = "OFF"
                st.session_state["bfi_debt_weight"] = "Equal_1.0x"
                st.success("✅ **Profile Detected: Zealot Mode** (CT-optimized, existential-first)")
            
            st.info(f"🎯 **Your Score Breakdown:** Skeptic: {scores['skeptic']}, Diplomat: {scores['diplomat']}, Seeker: {scores['seeker']}, Zealot: {scores['zealot']}")
            st.rerun()
        
        st.markdown("---")
        st.caption("💡 **Note:** This quiz is a starting point. You can always adjust toggles manually after!")

    # BOTTOM: IMPORT + EXPORT
    st.markdown("---")
    st.markdown("### 📥 Import / 📤 Export")
    
    bottom_col1, bottom_col2 = st.columns(2)
    
    with bottom_col1:
        st.markdown("**📥 Import Configuration**")
        import_file_bottom = st.file_uploader("Load saved audit", type=["json"], key="import_bottom")
        if import_file_bottom:
            try:
                run = json.load(import_file_bottom)
                if "config" in run and "framework_a" in run:
                    st.success("✅ Valid profile")
                    if st.button("Apply", key="apply_bottom"):
                        apply_loaded_run(run)
                        st.rerun()
            except:
                st.error("Invalid file")
    
    with bottom_col2:
        st.markdown("**📤 Export Current Audit**")
        export = {
            "config": cfg,
            "framework_a": fa,
            "framework_b": fb,
            "results": {
                "a": {"levers": ya_levers, "bfi": ya_bfi, "ypa": {k: v["YPA"] for k, v in ya_results.items()}},
                "b": {"levers": yb_levers, "bfi": yb_bfi, "ypa": {k: v["YPA"] for k, v in yb_results.items()}}
            }
        }
        st.download_button(
            "📥 Download Audit (JSON)",
            json.dumps(export, indent=2),
            "cfa_run.json",
            "application/json",
            use_container_width=True
        )
