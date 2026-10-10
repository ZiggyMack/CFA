"""
The matchup is the fundamental unit of CFA.

A ``Matchup`` is (subject, opponent, condition) together with everything
the repo knows about that pairing: the Phase-1 Trinity scores, the Phase-2
deliberated levers, the per-metric crux rates, and the YPA computed from
those levers. Nothing here is aggregated across opponents.

Two YPA definitions coexist in the repo and both are exposed:

* ``ypa_standard``  = sum of all six levers / BFT. This is what the YAML
  ``calculated.ypa_*`` fields and Mission Control report.
* ``ypa_scenarios`` = the Console formula (utils/calculations.py) with the
  Console's default toggles: composite PF (Holistic 50/50), fallibilism
  bonus ON, lever parity ON, equal debt weight, crux included. It yields
  Neutral / Existential / Empirical scenario values.
They differ by design; do not compare one to the other.
"""

from __future__ import annotations

import sys
from dataclasses import dataclass, asdict, field
from typing import Any, Dict, List, Optional

from . import paths
from .codes import WORLDVIEWS, code_for
from .profiles import LEVER_ORDER, LeverBlock, TrinityBlock, Worldview, load_worldviews

# utils/ lives at the repo root next to this package.
if str(paths.ROOT) not in sys.path:
    sys.path.insert(0, str(paths.ROOT))
try:
    from utils.calculations import ypa_scenario_scores  # type: ignore
except Exception:  # pragma: no cover - utils missing in a partial checkout
    ypa_scenario_scores = None

CONSOLE_DEFAULT_CFG: Dict[str, Any] = {
    "lever_parity": "ON",
    "fallibilism_bonus": "ON",
    "pf_type": "Holistic_50_50",
    "include_crux": True,
    "bft_debt_weight": "Equal_1.0x",
}


@dataclass
class Matchup:
    subject: str
    opponent: Optional[str]
    condition: str                               # "external" | "control"
    trinity: Optional[TrinityBlock]
    levers: Optional[LeverBlock]
    crux_rates: Dict[str, float]
    lever_sum: Optional[float]
    ypa_standard: Optional[float]
    ypa_scenarios: Optional[Dict[str, float]]
    bft_standard: float
    readiness: str                               # trinity+levers | trinity | levers | none
    directional_note: str = "scores describe SUBJECT as judged under OPPONENT's lens; the reverse pairing is a different matchup"

    @property
    def key(self) -> str:
        return f"{self.subject}|{self.opponent or 'pooled'}|{self.condition}"

    def to_dict(self) -> Dict[str, Any]:
        d = asdict(self)
        d["key"] = self.key
        return d


def _find_trinity(wv: Worldview, opponent: Optional[str], condition: str) -> Optional[TrinityBlock]:
    for blk in wv.trinity_by_matchup.values():
        if blk.opponent == opponent and (blk.condition or "external") == condition:
            return blk
    return None


def _find_levers(wv: Worldview, opponent: Optional[str], condition: str) -> Optional[LeverBlock]:
    for blk in wv.levers_by_matchup.values():
        if blk.malformed:
            continue
        if blk.opponent == opponent and (blk.condition or "external") == condition:
            return blk
    return None


def _scenarios(wv: Worldview, levers: Dict[str, float], crux_rates: Dict[str, float]) -> Optional[Dict[str, float]]:
    if ypa_scenario_scores is None or len(levers) != 6:
        return None
    fr = {
        "levers": {
            "CCI": levers["CCI"], "EDB": levers["EDB"],
            "PF_instrumental": levers["PF_I"], "PF_existential": levers["PF_E"],
            "AR": levers["AR"], "MG": levers["MG"],
        },
        "bft": {"axioms": wv.axiom_count, "debts": wv.debt_count},
        "admits_limits": wv.admits_limits,
        "crux_rates": crux_rates,
    }
    results, _, _ = ypa_scenario_scores(fr, CONSOLE_DEFAULT_CFG)
    return {name: round(r["YPA"], 4) for name, r in results.items()}


def build_matchup(wv: Worldview, opponent: Optional[str], condition: str) -> Matchup:
    trinity = _find_trinity(wv, opponent, condition)
    levers = _find_levers(wv, opponent, condition)
    crux = {m: mt.crux_rate for m, mt in (trinity.metrics if trinity else {}).items() if mt.crux_rate is not None}
    lever_sum = ypa_std = scen = None
    if levers and len(levers.levers) == 6:
        lever_sum = round(sum(levers.levers[k] for k in LEVER_ORDER), 4)
        ypa_std = round(lever_sum / wv.bft_standard, 4) if wv.bft_standard else None
        scen = _scenarios(wv, levers.levers, crux)
    readiness = {(True, True): "trinity+levers", (True, False): "trinity",
                 (False, True): "levers", (False, False): "none"}[(trinity is not None, levers is not None)]
    return Matchup(
        subject=wv.code, opponent=opponent, condition=condition,
        trinity=trinity, levers=levers, crux_rates=crux,
        lever_sum=lever_sum, ypa_standard=ypa_std, ypa_scenarios=scen,
        bft_standard=wv.bft_standard, readiness=readiness,
    )


def get_matchup(subject: str, opponent: Optional[str], condition: str = "external") -> Matchup:
    """The pairing ``subject`` judged under ``opponent``'s lens.
    ``opponent=None`` with ``condition="control"`` addresses a pooled control block."""
    wv = load_worldviews()[code_for(subject) or subject]
    opp = code_for(opponent) if opponent else None
    if opponent and not opp:
        raise KeyError(f"unknown opponent: {opponent!r}")
    return build_matchup(wv, opp, condition)


def list_matchups(condition: Optional[str] = None) -> List[Matchup]:
    """Every (subject, opponent, condition) that has any evidence on disk."""
    out: List[Matchup] = []
    for wv in load_worldviews().values():
        seen = set()
        for blk in list(wv.trinity_by_matchup.values()) + [b for b in wv.levers_by_matchup.values() if not b.malformed]:
            cond = blk.condition or "external"
            if condition and cond != condition:
                continue
            k = (blk.opponent, cond)
            if k in seen:
                continue
            seen.add(k)
            out.append(build_matchup(wv, blk.opponent, cond))
    out.sort(key=lambda m: (m.subject, m.opponent or "", m.condition))
    return out


def coverage_matrix() -> Dict[str, Any]:
    """Readiness grid for the external-identity condition, subject × opponent,
    plus the control grid. ``readiness`` strings: trinity+levers, trinity,
    levers, none. The diagonal is always none (a framework is never its own lens)."""
    codes = list(WORLDVIEWS.keys())
    wvs = load_worldviews()
    grids: Dict[str, Dict[str, Dict[str, str]]] = {"external": {}, "control": {}}
    for cond in grids:
        for s in codes:
            row: Dict[str, str] = {}
            for o in codes:
                if s == o or s not in wvs:
                    row[o] = "none"
                else:
                    row[o] = build_matchup(wvs[s], o, cond).readiness
            grids[cond][s] = row
    totals = {cond: {
        r: sum(1 for s in codes for o in codes if grids[cond][s][o] == r)
        for r in ("trinity+levers", "trinity", "levers", "none")
    } for cond in grids}
    return {"subjects": codes, "opponents": codes, "grids": grids, "totals": totals}
