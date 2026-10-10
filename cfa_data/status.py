"""
Mission-Control numbers, computed from the data instead of hand-typed.

``views/mission_control.py`` carries hardcoded run counts, batch
inventories and open-loop cards that drift from the YAMLs and the run
corpus (they already had, by July 2026). ``build_status()`` derives the
same facts from disk so a dashboard, an API or a renderer can show the
truth as of right now.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List

from .codes import WORLDVIEWS, display_name
from .matchups import coverage_matrix, list_matchups
from .profiles import load_worldviews
from .runs import load_run_index
from .sync import sync_state


def _structural_open_loops(wvs) -> List[Dict[str, str]]:
    loops: List[Dict[str, str]] = []
    for wv in wvs.values():
        for key, blk in wv.levers_by_matchup.items():
            if blk.malformed:
                loops.append({
                    "severity": "low", "subject": wv.code,
                    "item": f"levers_by_matchup.{key} is not a lever block (Trinity-shaped data misplaced)",
                    "source": wv.source_file,
                })
        if len(wv.canonical_levers) != 6:
            loops.append({"severity": "high", "subject": wv.code,
                          "item": "flat levers: block is missing or incomplete; the Streamlit loader will raise",
                          "source": wv.source_file})
        if wv.depth_pass_pending:
            loops.append({"severity": "medium", "subject": wv.code,
                          "item": "breadth profile at n=1; n=10 depth pass pending (agreed order: EXST, HIN, ERR, +NULL)",
                          "source": wv.source_file})
        for key, blk in wv.trinity_by_matchup.items():
            if blk.opponent and not any(
                (lb.opponent == blk.opponent and (lb.condition or "external") == (blk.condition or "external"))
                for lb in wv.levers_by_matchup.values() if not lb.malformed
            ):
                loops.append({"severity": "low", "subject": wv.code,
                              "item": f"Trinity scores exist for {key} but no deliberated lever block; Console falls back to canonical levers",
                              "source": wv.source_file})
    return loops


def build_status() -> Dict[str, Any]:
    wvs = load_worldviews()
    matchups = list_matchups()
    cov = coverage_matrix()
    sync = sync_state()
    idx = load_run_index()

    by_status: Dict[str, int] = {}
    for wv in wvs.values():
        by_status[wv.status or "UNKNOWN"] = by_status.get(wv.status or "UNKNOWN", 0) + 1

    readiness: Dict[str, int] = {}
    for m in matchups:
        readiness[m.readiness] = readiness.get(m.readiness, 0) + 1

    status: Dict[str, Any] = {
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "worldviews": {
            "count": len(wvs),
            "by_status": by_status,
            "by_tier": {t: sum(1 for w in WORLDVIEWS.values() if w.tier == t) for t in ("anchor", "breadth")},
            "list": [{
                "code": wv.code, "name": wv.name, "status": wv.status, "tier": wv.tier,
                "version": wv.version, "last_updated": wv.last_updated,
                "trinity_blocks": len(wv.trinity_by_matchup),
                "lever_blocks": sum(1 for b in wv.levers_by_matchup.values() if not b.malformed),
                "depth_pass_pending": wv.depth_pass_pending,
                "canonical_levers_provenance": wv.canonical_levers_provenance,
            } for wv in wvs.values()],
        },
        "matchups": {
            "count": len(matchups),
            "by_readiness": readiness,
            "by_condition": {c: sum(1 for m in matchups if m.condition == c) for c in ("external", "control")},
            "coverage_totals": cov["totals"],
        },
        "runs": idx.summary() if idx else {"available": False, "reason": "Nyquist run corpus not reachable (set CFA_RUNS_DIR)"},
        "sync": {
            "inbox_waiting": sync["inbox_waiting"],
            "inbox_clear": sync["inbox_clear"],
            "newest_processed_in": sync["newest_processed_in"],
            "newest_out": sync["newest_out"],
            "sync_out_pending_count": len(sync["sync_out_pending"]),
        },
        "open_loops_structural": _structural_open_loops(wvs),
    }
    return status
