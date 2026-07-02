#!/usr/bin/env python3
"""
raw_to_smv.py — Convert CFA Trinity raw run JSON to SMV scenario format.

Usage:
    python raw_to_smv.py <input_json> [<output_json>]
    python raw_to_smv.py --batch <raw_runs_dir> <output_dir>

Input:  S7_cfa_trinity_v2_YYYYMMDD_HHMMSS.json (from SYNC_IN/pending/raw_runs/)
Output: scenario_CT_MdN_HHMMSS.json (SMV tick format, goes in dashboard/SMV/src/data/)

Notes:
    - drift_trajectory is intentionally skipped — baseline embeddings were stripped at
      serialization time, making the values unreliable. Disabled in future runs.
    - round_scores, transcript[*].content, crux_point, convergence are all clean data.
    - Narrative is regex-extracted: DECISION STAMP section for Round 1, last ## section
      for subsequent rounds, final paragraph for Grok in all rounds.
"""

import json
import re
import sys
from pathlib import Path
from typing import Optional

METRIC_FULL_NAMES = {
    # Phase 1 — Trinity deliberation metrics
    "BFI": "Beings, Foundational Importance",
    "CA": "Causal Attribution",
    "IP": "Intellectual Pedigree",
    "ES": "Explanatory Scope",
    "LS": "Logical Soundness",
    "MS": "Moral Substance",
    "PS": "Practical Significance",
    # Phase 2 — CFA lever metrics
    "CCI": "Collective Coherence Impact",
    "EDB": "Epistemic Debt Burden",
    "PF_I": "Pragmatic Fertility (Instrumental)",
    "PF_E": "Pragmatic Fertility (Existential)",
    "AR": "Asymptotic Realism",
    "MG": "Meta-Governance",
}

METRIC_ORDER_P1 = ["BFI", "CA", "IP", "ES", "LS", "MS", "PS"]
METRIC_ORDER_P2 = ["CCI", "EDB", "PF_I", "PF_E", "AR", "MG"]
METRIC_ORDER = METRIC_ORDER_P1  # legacy default

# Stance abbreviation → (display abbr, full name)
# Add new worldviews here as experiments are run.
STANCE_ABBR = {
    "ct":  ("CT",  "Classical Theism"),
    "mdn": ("MdN", "Methodological Naturalism"),
    "pt":  ("PT",  "Process Theology"),
}


def parse_stance(stance: str):
    """Parse 'subject_vs_opponent' stance string.
    Returns (subject_abbr, subject_full, opponent_abbr, opponent_full,
             claude_stance, grok_stance, worldview_pair).
    """
    parts = stance.lower().split("_vs_")
    if len(parts) != 2:
        return ("CT", "Classical Theism", "MdN", "Methodological Naturalism",
                "PRO", "ANTI", "CT_vs_MdN")
    subj_key, opp_key = parts
    subj_abbr, subj_full = STANCE_ABBR.get(subj_key, (subj_key.upper(), subj_key.upper()))
    opp_abbr, opp_full   = STANCE_ABBR.get(opp_key,  (opp_key.upper(),  opp_key.upper()))
    # Claude is always PRO-subject; Grok is always ANTI-subject
    return (subj_abbr, subj_full, opp_abbr, opp_full, "PRO", "ANTI",
            f"{subj_abbr}_vs_{opp_abbr}")


def convergence_status(conv: float, is_crux: bool, is_last: bool) -> str:
    if is_crux and is_last:
        return "crux_declared"
    if conv >= 0.98:
        return "converged"
    if conv >= 0.92:
        return "near_converged"
    if conv >= 0.85:
        return "converging"
    if conv >= 0.75:
        return "moderate"
    if conv >= 0.60:
        return "diverging"
    return "divergent"


def trim_at_sentence(text: str, limit: int) -> str:
    """Trim text to limit chars at the nearest sentence boundary."""
    if len(text) <= limit:
        return text
    cut = text[:limit].rfind('.')
    return (text[:cut + 1] if cut > limit // 2 else text[:limit]).strip()


# Grok uses **ADVOCACY_SCORE: X** (bold) in some rounds, plain in others.
# This pattern handles both variants.
_SCORE_TAG = re.compile(r'\n\*{0,2}ADVOCACY_SCORE:', re.IGNORECASE)


def _strip_score_tag(content: str) -> str:
    """Return content with ADVOCACY_SCORE line and everything after it removed."""
    return _SCORE_TAG.split(content)[0].strip()


def extract_claude_narrative(content: str, round_num: int) -> Optional[str]:
    """
    Extract key scoring narrative from Claude's transcript entry.

    Round 1: Pulls the '## 5. DECISION STAMP' section (the structured scoring rationale).
    Later rounds: Pulls the last '##' section before ADVOCACY_SCORE (holding/adjustment reasoning).
    """
    if not content:
        return None

    if round_num == 1:
        m = re.search(r'## 5\. DECISION STAMP\n(.*?)(?=\n---|\Z)', content, re.DOTALL)
        if m:
            return trim_at_sentence(m.group(1).strip(), 600)

    body = _strip_score_tag(content)
    sections = re.split(r'\n## ', body)
    if len(sections) > 1:
        last = sections[-1].strip()
        lines = last.split('\n', 1)
        text = lines[1].strip() if len(lines) > 1 else last
        return trim_at_sentence(text, 500)

    return None


def extract_grok_challenge(content: str) -> Optional[str]:
    """
    Extract Grok's core argument from a transcript entry.

    Grok responses are 3-5 short paragraphs. We take the last paragraph before
    ADVOCACY_SCORE as the conclusion of Grok's argument.
    """
    if not content:
        return None

    body = _strip_score_tag(content)
    paragraphs = [p.strip() for p in body.split('\n\n') if p.strip()]
    if not paragraphs:
        return None

    last = paragraphs[-1]
    return trim_at_sentence(last, 400)


def build_ticks(metric: str, metric_data: dict, claude_stance: str = "PRO", grok_stance: str = "ANTI") -> list:
    """Build SMV tick list for a single metric from its raw run data."""
    round_scores = metric_data.get("round_scores", [])
    transcript = metric_data.get("transcript", [])
    crux_declared = metric_data.get("crux_declared", False)
    crux_point = metric_data.get("crux_point") or {}
    rounds_taken = metric_data.get("rounds_taken", len(round_scores))

    # Index transcript entries by (auditor, round)
    tx = {}
    for entry in transcript:
        tx[(entry["auditor"], entry["round"])] = entry.get("content", "")

    ticks = []
    for rs in round_scores:
        # Skip rounds where score extraction failed for either auditor
        if not rs.get("claude_extracted") or not rs.get("grok_extracted"):
            continue

        r = rs["round"]
        claude_score = rs["claude"]
        grok_score = rs["grok"]
        conv = rs["convergence"]
        is_last = (r == rounds_taken)
        is_crux_tick = crux_declared and is_last

        # Tension: normalized absolute score gap
        tension_cg = round(min(1.0, abs(claude_score - grok_score) / 10.0), 2)
        # Volume: how active this edge is — rises with round number and tension
        volume_cg = round(min(1.0, 0.3 + tension_cg * 0.5 + r * 0.04), 2)
        nova_tension = round(tension_cg * 0.4, 2)
        nova_volume = 0.25

        # Nova gets higher tension/volume in crux or potential-crux rounds
        if is_crux_tick or (crux_declared and conv < 0.90 and r >= 3):
            nova_tension = round(min(0.7, nova_tension + 0.2), 2)
            nova_volume = 0.40

        status = convergence_status(conv, is_crux_tick, is_last)

        # Crux state for this tick
        if is_crux_tick:
            crux = {
                "status": "declared",
                "id": crux_point.get("id", f"CRUX_{metric}_{r}"),
                "classification": crux_point.get("type", "unclassified"),
                "description": (
                    f"Crux declared at {conv * 100:.0f}% convergence. "
                    f"Type: {crux_point.get('type', 'unclassified')}. "
                    f"Claude {claude_score} / Grok {grok_score}."
                ),
            }
        elif crux_declared and conv < 0.90 and r >= 3:
            crux = {"status": "potential"}
        else:
            crux = {"status": "none"}

        # Nova edge label
        nova_note = "Nova observing"
        if is_crux_tick:
            nova_note = "Nova issuing crux assessment"
        elif crux_declared and r >= 3:
            nova_note = "Nova monitoring for crux"

        tick = {
            "tick_id": f"tick-{metric}-R{r}",
            "metric": metric,
            "metric_full": METRIC_FULL_NAMES.get(metric, metric),
            "round": r,
            "nodes": [
                {"auditor": "Claude", "score": claude_score, "stance": claude_stance, "bias_overhead": 0.50},
                {"auditor": "Grok",   "score": grok_score,  "stance": grok_stance,   "bias_overhead": 0.40},
                {"auditor": "Nova",   "score": None,         "stance": "FAIRNESS", "bias_overhead": 0.30},
            ],
            "edges": [
                {
                    "pair": "Claude-Grok",
                    "tension": tension_cg,
                    "volume": volume_cg,
                    "notes": f"R{r}: Claude {claude_score} / Grok {grok_score} — {tension_cg * 100:.0f}% gap",
                },
                {"pair": "Claude-Nova", "tension": nova_tension, "volume": nova_volume, "notes": nova_note},
                {"pair": "Grok-Nova",   "tension": nova_tension, "volume": nova_volume, "notes": nova_note},
            ],
            "convergence": {
                "percentage": round(conv * 100, 1),
                "status": status,
            },
            "crux": crux,
        }

        # Attach narrative excerpts if available
        claude_text = extract_claude_narrative(tx.get(("claude", r), ""), r)
        if claude_text:
            tick["claude_narrative"] = claude_text

        grok_text = extract_grok_challenge(tx.get(("grok", r), ""))
        if grok_text:
            tick["grok_challenge"] = grok_text

        # Attach Nova's assessment on the final round if Nova spoke
        nova_content = tx.get(("nova", r), "")
        if nova_content and is_last:
            tick["nova_assessment"] = trim_at_sentence(nova_content, 600)

        ticks.append(tick)

    return ticks


def convert(raw_path: Path, output_path: Optional[Path] = None) -> dict:
    """Convert one raw run JSON to SMV scenario format."""
    with open(raw_path, "r", encoding="utf-8") as f:
        raw = json.load(f)

    session_id = raw.get("session_id", raw_path.stem.split("_", 3)[-1])
    condition = raw.get("condition", "unknown")
    identity_condition = "external_identity" if condition == "external" else "control"
    stance = raw.get("stance", "ct_vs_mdn")
    phase = raw.get("phase", 1)

    subj_abbr, subj_full, opp_abbr, _, claude_stance, grok_stance, worldview_pair = parse_stance(stance)

    # Derive experiment ID from date embedded in session_id (YYYYMMDD_HHMMSS)
    date_part = session_id.split("_")[0] if "_" in session_id else "20260629"
    experiment_id = f"CFA-EXP1-BATCH-{date_part}"

    results = raw.get("component1_results", {})
    metric_order = METRIC_ORDER_P2 if phase == 2 else METRIC_ORDER_P1

    all_ticks = []
    crux_metrics = []
    total_conv = 0.0
    total_rounds = 0
    metric_count = 0

    for metric in metric_order:
        if metric not in results:
            continue
        mdata = results[metric]
        ticks = build_ticks(metric, mdata, claude_stance=claude_stance, grok_stance=grok_stance)
        all_ticks.extend(ticks)

        if mdata.get("crux_declared"):
            crux_metrics.append(metric)
        total_conv += mdata.get("convergence", 0)
        total_rounds += mdata.get("rounds_taken", 0)
        metric_count += 1

    avg_conv = total_conv / metric_count if metric_count else 0.0
    avg_rounds = total_rounds / metric_count if metric_count else 0.0

    scenario = {
        "session_id": session_id,
        "worldview_pair": worldview_pair,
        "subject_framework": raw.get("subject_framework") or subj_full,
        "auditors": ["Claude", "Grok", "Nova"],
        "identity_condition": identity_condition,
        "experiment": experiment_id,
        "phase": phase,
        "session_story": {
            "summary": (
                f"Phase {phase} {identity_condition.replace('_', ' ')} run — "
                f"{subj_abbr} vs {opp_abbr}. "
                f"{metric_count} metrics. "
                f"{len(crux_metrics)} crux declaration(s): {', '.join(crux_metrics) if crux_metrics else 'none'}. "
                f"Avg convergence {avg_conv * 100:.1f}%, avg rounds {avg_rounds:.1f}."
            ),
            "crux_metrics": crux_metrics,
            "avg_convergence_pct": round(avg_conv * 100, 1),
            "avg_rounds": round(avg_rounds, 1),
        },
        "ticks": all_ticks,
    }

    if output_path:
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(scenario, f, indent=2, ensure_ascii=False)
        print(f"  Written: {output_path} ({len(all_ticks)} ticks, phase {phase})")

    return scenario


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    if sys.argv[1] == "--batch":
        if len(sys.argv) < 4:
            print("Usage: raw_to_smv.py --batch <raw_runs_dir> <output_dir>")
            sys.exit(1)
        raw_dir = Path(sys.argv[2])
        out_dir = Path(sys.argv[3])
        files = sorted(raw_dir.glob("S7_cfa_trinity_*.json"))
        if not files:
            print(f"No matching files in {raw_dir}")
            sys.exit(1)
        print(f"Converting {len(files)} files...")
        for json_file in files:
            # Extract HHMMSS suffix from: S7_cfa_trinity_YYYYMMDD_HHMMSS or S7_cfa_trinity_v2_YYYYMMDD_HHMMSS
            parts = json_file.stem.rsplit("_", 1)
            suffix = parts[-1]  # HHMMSS
            # Peek at stance to determine output prefix
            with open(json_file, "r", encoding="utf-8") as _f:
                _raw = json.load(_f)
            subj_abbr, _, opp_abbr, _, _, _, _ = parse_stance(_raw.get("stance", "ct_vs_mdn"))
            out_file = out_dir / f"scenario_{subj_abbr}_{opp_abbr}_{suffix}.json"
            convert(json_file, out_file)
        print("Done.")
    else:
        raw_path = Path(sys.argv[1])
        out_path = Path(sys.argv[2]) if len(sys.argv) >= 3 else None
        if out_path is None:
            import json as _json
            with open(raw_path, "r", encoding="utf-8") as _f:
                _raw = _json.load(_f)
            subj_abbr, _, opp_abbr, _, _, _, _ = parse_stance(_raw.get("stance", "ct_vs_mdn"))
            suffix = raw_path.stem.rsplit("_", 1)[-1]
            out_path = raw_path.parent / f"scenario_{subj_abbr}_{opp_abbr}_{suffix}.json"
        result = convert(raw_path, out_path)
        print(f"Session story: {result['session_story']['summary']}")


if __name__ == "__main__":
    main()
