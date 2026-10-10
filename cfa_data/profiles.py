"""
Worldview profiles, normalized.

Reads every ``profiles/worldviews/*.yaml`` and turns the three historical
block shapes into one model:

* breadth n=1 shape (2026-07-17): ``metrics.BFI.claude_score / grok_score /
  combined_midpoint / convergence / crux_declared``
* batch shape (CT, MdN, PT, G, B): ``metrics.BFI.claude_mean / grok_mean /
  combined_midpoint / convergence_pct / crux_rate "3/10" / divergence_layer``
* pooled control (Gnosticism): ``source / n / status / metrics``

Nothing is averaged across opponents. Every score keeps its matchup key.
The flat ``levers:`` block is exposed as ``canonical_levers`` together with a
``canonical_levers_provenance`` string that says whether it is a web-research
prior or a copy of a deliberated matchup block.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, List, Optional

import yaml

from . import paths
from .codes import WORLDVIEWS, matchup_key_to_code

LEVER_KEYS: Dict[str, str] = {
    "collective_coherence_impact": "CCI",
    "epistemic_debt_burden": "EDB",
    "paternalistic_force_interventionist": "PF_I",
    "paternalistic_force_epistemic": "PF_E",
    "asymmetry_risk": "AR",
    "meta_governance": "MG",
}
LEVER_ORDER = ["CCI", "EDB", "PF_I", "PF_E", "AR", "MG"]
METRIC_ORDER = ["BFI", "CA", "IP", "ES", "LS", "MS", "PS"]


# ---------------------------------------------------------------------------
# models
# ---------------------------------------------------------------------------

@dataclass
class Metric:
    metric: str
    full_name: Optional[str] = None
    claude: Optional[float] = None
    grok: Optional[float] = None
    midpoint: Optional[float] = None
    convergence: Optional[float] = None       # 0..1
    crux_rate: Optional[float] = None         # 0..1
    crux_declared: Optional[bool] = None
    avg_rounds: Optional[float] = None
    spread: Optional[float] = None
    stability: Optional[str] = None
    divergence_layer: Optional[str] = None
    identity_delta_claude: Optional[float] = None
    identity_delta_grok: Optional[float] = None
    notes: Optional[str] = None


@dataclass
class TrinityBlock:
    key: str
    opponent: Optional[str]                   # short code, None for pooled controls
    condition: Optional[str]                  # "external" | "control" | None
    n: Optional[int]
    runs_total: Optional[int]
    batch_id: Optional[str]
    phase: Optional[int]
    score_audit_status: Optional[str]
    identity_condition: Optional[str]
    metrics: Dict[str, Metric]
    notes: Optional[str] = None
    key_finding: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LeverBlock:
    key: str
    opponent: Optional[str]
    condition: Optional[str]
    levers: Dict[str, float]                  # CCI, EDB, PF_I, PF_E, AR, MG
    source: Optional[str] = None
    malformed: bool = False                   # True if the block is not a lever block
    raw: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Worldview:
    code: str
    name: str
    stem: str
    tier: str
    status: Optional[str]
    version: Optional[str]
    last_updated: Optional[str]
    declared_axiom: Optional[str]
    alternate_names: List[str]
    maintainers: List[str]
    axioms: List[Dict[str, str]]
    debts: List[Dict[str, str]]
    axiom_count: int
    debt_count: int
    bft_standard: float
    admits_limits: bool
    canonical_levers: Dict[str, float]
    canonical_levers_provenance: str
    canonical_lever_sum: float
    canonical_ypa_standard: float
    levers_by_matchup: Dict[str, LeverBlock]
    trinity_by_matchup: Dict[str, TrinityBlock]
    phase2: Optional[Dict[str, Any]]
    calculated: Dict[str, Any]
    audit_status: Optional[str]
    depth_pass_pending: bool
    source_file: str

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


# ---------------------------------------------------------------------------
# parsing helpers
# ---------------------------------------------------------------------------

def _f(x) -> Optional[float]:
    try:
        return None if x is None else float(x)
    except (TypeError, ValueError):
        return None


def _crux_rate(raw) -> Optional[float]:
    if raw is None:
        return None
    if isinstance(raw, str) and "/" in raw:
        try:
            num, den = raw.split("/")
            return float(num) / float(den) if float(den) else 0.0
        except (ValueError, ZeroDivisionError):
            return None
    return _f(raw)


def _parse_metric(name: str, d: Dict[str, Any]) -> Metric:
    conv = _f(d.get("convergence"))
    if conv is None and d.get("convergence_pct") is not None:
        conv = _f(d["convergence_pct"]) / 100.0
    crux = _crux_rate(d.get("crux_rate"))
    declared = d.get("crux_declared")
    if crux is None and isinstance(declared, bool):
        crux = 1.0 if declared else 0.0
    return Metric(
        metric=name,
        full_name=d.get("full_name"),
        claude=_f(d.get("claude_score", d.get("claude_mean"))),
        grok=_f(d.get("grok_score", d.get("grok_mean"))),
        midpoint=_f(d.get("combined_midpoint", d.get("final_score"))),
        convergence=conv,
        crux_rate=crux,
        crux_declared=declared if isinstance(declared, bool) else None,
        avg_rounds=_f(d.get("avg_rounds")),
        spread=_f(d.get("spread")),
        stability=d.get("stability"),
        divergence_layer=d.get("divergence_layer"),
        identity_delta_claude=_f(d.get("identity_delta_claude")),
        identity_delta_grok=_f(d.get("identity_delta_grok")),
        notes=d.get("notes"),
    )


def _infer_condition(key: str, d: Dict[str, Any], from_key: Optional[str]) -> Optional[str]:
    if d.get("condition") in ("external", "control"):
        return d["condition"]
    if from_key:
        return from_key
    ic = str(d.get("identity_condition") or "")
    if "external" in ic:
        return "external"
    sid = d.get("session_ids")
    if isinstance(sid, dict) and sid.get("golden"):
        return "external"          # golden = identity-loaded external runs
    src = str(d.get("source") or d.get("calibration_context") or "").lower()
    if "control" in src or "base model" in src:
        return "control"
    if "external" in src or "golden" in src:
        return "external"
    return None


def _parse_trinity_block(key: str, d: Dict[str, Any]) -> TrinityBlock:
    opp, cond_from_key = matchup_key_to_code(key)
    condition = _infer_condition(key, d, cond_from_key)
    sid = d.get("session_ids") if isinstance(d.get("session_ids"), dict) else {}
    n = d.get("runs_good", d.get("n"))
    if n is None and sid.get("golden"):
        n = len(sid["golden"])
    metrics = {
        m: _parse_metric(m, md)
        for m, md in (d.get("metrics") or {}).items()
        if isinstance(md, dict)
    }
    return TrinityBlock(
        key=key, opponent=opp, condition=condition,
        n=int(n) if isinstance(n, (int, float)) else None,
        runs_total=d.get("runs_total"),
        batch_id=d.get("batch_id") or d.get("experiment_id") or d.get("source"),
        phase=d.get("phase"),
        score_audit_status=d.get("score_audit_status") or d.get("status"),
        identity_condition=d.get("identity_condition"),
        metrics=metrics,
        notes=d.get("notes") or d.get("note"),
        key_finding=d.get("key_finding"),
        raw=d,
    )


def _parse_lever_block(key: str, d: Dict[str, Any]) -> LeverBlock:
    opp, cond_from_key = matchup_key_to_code(key)
    levers = {short: _f(d.get(long)) for long, short in LEVER_KEYS.items()}
    malformed = any(v is None for v in levers.values())
    if malformed:
        levers = {k: v for k, v in levers.items() if v is not None}
    return LeverBlock(
        key=key, opponent=opp,
        condition=_infer_condition(key, d, cond_from_key),
        levers=levers,
        source=d.get("source") or d.get("calibration_context") or d.get("calibration_source"),
        malformed=malformed,
        raw=d,
    )


def _same_levers(a: Dict[str, float], b: Dict[str, float]) -> bool:
    return all(k in b and abs(a[k] - b[k]) < 1e-6 for k in LEVER_ORDER) if len(a) == 6 else False


def _provenance(canon: Dict[str, float], blocks: Dict[str, LeverBlock], calc: Dict[str, Any]) -> str:
    for key, blk in blocks.items():
        if not blk.malformed and _same_levers(canon, blk.levers):
            return f"deliberated copy of levers_by_matchup.{key}"
    pw = calc.get("priors_web_research")
    if isinstance(pw, dict):
        return f"web-research prior (lever_sum {pw.get('lever_sum')}, ypa {pw.get('ypa_standard')})"
    return "flat block; provenance not recorded in YAML"


# ---------------------------------------------------------------------------
# loaders
# ---------------------------------------------------------------------------

def _load_yaml(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8-sig") as fh:   # some files carry a BOM
        return yaml.safe_load(fh) or {}


def parse_worldview(code: str, data: Dict[str, Any], source: str) -> Worldview:
    reg = WORLDVIEWS[code]
    prof = data.get("profile") or {}
    calc = data.get("calculated") or {}
    flat = data.get("levers") or {}
    canon = {short: _f(flat.get(long)) for long, short in LEVER_KEYS.items()}
    canon = {k: v for k, v in canon.items() if v is not None}

    lever_blocks = {k: _parse_lever_block(k, v) for k, v in (data.get("levers_by_matchup") or {}).items()
                    if isinstance(v, dict)}
    trinity_blocks = {k: _parse_trinity_block(k, v) for k, v in (data.get("trinity_scores_by_matchup") or {}).items()
                      if isinstance(v, dict)}

    axiom_count = int(calc.get("axiom_count", len(data.get("axioms") or [])))
    debt_count = int(calc.get("debt_count", len(data.get("debts") or [])))
    bft = _f(calc.get("bft_standard")) or float(axiom_count + debt_count)
    lever_sum = sum(canon.values()) if len(canon) == 6 else 0.0
    audit_status = data.get("audit_status")

    return Worldview(
        code=code, name=prof.get("name") or reg.name, stem=reg.stem, tier=reg.tier,
        status=prof.get("status"), version=str(prof.get("version")) if prof.get("version") is not None else None,
        last_updated=str(prof.get("last_updated")) if prof.get("last_updated") else None,
        declared_axiom=prof.get("declared_axiom"),
        alternate_names=list(prof.get("alternate_names") or []),
        maintainers=list(prof.get("maintainers") or []),
        axioms=[{"name": a.get("name", ""), "description": a.get("description", "")} for a in (data.get("axioms") or [])],
        debts=[{"name": d.get("name", ""), "description": d.get("description", "")} for d in (data.get("debts") or [])],
        axiom_count=axiom_count, debt_count=debt_count, bft_standard=bft,
        admits_limits=bool((data.get("behavioral_flags") or {}).get("admits_limits", True)),
        canonical_levers=canon,
        canonical_levers_provenance=_provenance(canon, lever_blocks, calc),
        canonical_lever_sum=round(lever_sum, 4),
        canonical_ypa_standard=round(lever_sum / bft, 4) if bft else 0.0,
        levers_by_matchup=lever_blocks,
        trinity_by_matchup=trinity_blocks,
        phase2=data.get("phase2_lever_scores"),
        calculated=calc,
        audit_status=audit_status,
        depth_pass_pending=bool(audit_status and "depth pass pending" in audit_status),
        source_file=source,
    )


@lru_cache(maxsize=1)
def load_worldviews() -> Dict[str, Worldview]:
    """All 13 profiles keyed by short code. Cached for the process lifetime;
    call ``load_worldviews.cache_clear()`` after editing a YAML."""
    out: Dict[str, Worldview] = {}
    for code, reg in WORLDVIEWS.items():
        p = paths.PROFILES_DIR / f"{reg.stem}.yaml"
        if not p.exists():
            continue
        out[code] = parse_worldview(code, _load_yaml(p), str(p.relative_to(paths.ROOT)))
    return out


def load_worldview(code_or_name: str) -> Worldview:
    from .codes import code_for
    code = code_for(code_or_name)
    if not code or code not in load_worldviews():
        raise KeyError(f"unknown worldview: {code_or_name!r}")
    return load_worldviews()[code]
