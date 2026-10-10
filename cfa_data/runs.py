"""
The ARMADA run corpus, indexed.

Walks every ``S7_cfa_trinity_*.json`` under the Nyquist runs directory
(top level and ``cfa_trinity/<CODE>/`` folders), reads the small set of
fields a consumer needs, and caches that summary in ``.cache/cfa_data/``
keyed by file mtime and size, so a second load is instant and a changed
file is re-read. Full run JSONs (transcripts included) are loaded on demand
with ``load_run(session_id)``.

Read-only against the Nyquist repo. The only write is the cache file,
which lives under the CFA repo's gitignored ``.cache/``.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional

from . import paths
from .codes import code_for

INDEX_VERSION = 3   # bump whenever RunSummary gains a field, so stale caches are rebuilt
_PATTERN = "S7_cfa_trinity_*.json"


@dataclass
class RunSummary:
    session_id: str
    path: str                        # relative to RUNS_DIR, forward slashes
    folder: str                      # "" for top level, else e.g. "cfa_trinity/OJ"
    timestamp: Optional[str]
    engine_version: Optional[str]
    phase: Optional[int]
    condition: Optional[str]
    stance: Optional[str]
    subject: Optional[str]           # short code
    opponent: Optional[str]          # short code
    subject_name: Optional[str]
    opponent_name: Optional[str]
    deliberation_order: Optional[str]
    identity_augmentation: Optional[bool]
    metrics: Dict[str, Dict[str, Any]]   # metric -> {claude, grok, final, convergence, rounds, crux}
    metric_keys: List[str]
    avg_convergence: Optional[float]
    crux_count: int
    component2_signoffs: Dict[str, Optional[str]]
    auditor_errors: Dict[str, bool]  # auditor -> any "[ERROR]" in baseline/exit survey
    corrupted_flag: bool             # file text mentions CORRUPTED
    size_bytes: int
    duplicate_of: Optional[str] = None   # set on the copy that lost dedupe
    bucket: str = "worldview"        # see bucket_for()
    root: str = "nyquist"            # which scan root: "nyquist" | "cfa_archive"
    aborted: bool = False            # summary.aborted: extraction failed, run exited 0 anyway
    abort_reason: Optional[str] = None
    metrics_scored: Optional[int] = None   # summary.component1.metrics_scored
    data_quality: Optional[Dict[str, Any]] = None   # in-place flags such as CORRUPTED_QUESTION_STALE


def bucket_for(folder: str, root: str = "nyquist") -> str:
    """Classify a run by where ARMADA left it. Mission Control's hand-typed
    "663 worldview runs (+88 calib/legacy)" equals worldview + calibration +
    pre_schema; the unfiled top-level drop zone and the errored/dry-run
    folders are counted nowhere on the dashboard. Runs under CFA's own
    gitignored archive get their own bucket."""
    if root != "nyquist":
        return root
    f = folder.lower()
    if not f:
        return "unfiled"
    if f.startswith(".errored"):
        return "errored"
    if "dryrun" in f:
        return "dryrun"
    if f.endswith("/pre_schema"):
        return "pre_schema"
    if f.endswith("/framework_g"):
        return "calibration"
    return "worldview"


def _auditor_has_error(run: Dict[str, Any], auditor: str) -> bool:
    def _scan(obj) -> bool:
        if isinstance(obj, str):
            return obj.startswith("[ERROR]")
        if isinstance(obj, dict):
            return any(_scan(v) for v in obj.values())
        if isinstance(obj, list):
            return any(_scan(v) for v in obj)
        return False
    base = (run.get("baselines") or {}).get(auditor) or {}
    exit_ = (run.get("exit_surveys") or {}).get(auditor) or {}
    return _scan(base.get("responses")) or _scan(exit_)


def summarize_run(run: Dict[str, Any], rel_path: str, size: int, corrupted: bool,
                  root: str = "nyquist") -> RunSummary:
    c1 = run.get("component1_results") or {}
    summ = run.get("summary") or {}
    c1s = summ.get("component1") if isinstance(summ.get("component1"), dict) else {}
    dq = run.get("data_quality") if isinstance(run.get("data_quality"), dict) else None
    metrics: Dict[str, Dict[str, Any]] = {}
    convs: List[float] = []
    crux = 0
    for m, d in c1.items():
        if not isinstance(d, dict):
            continue
        metrics[m] = {
            "claude": d.get("claude_score"), "grok": d.get("grok_score"),
            "final": d.get("final_score"), "convergence": d.get("convergence"),
            "rounds": d.get("rounds_taken"), "crux": bool(d.get("crux_declared")),
        }
        if isinstance(d.get("convergence"), (int, float)):
            convs.append(float(d["convergence"]))
        if d.get("crux_declared"):
            crux += 1
    c2 = run.get("component2_results") or {}
    folder = str(Path(rel_path).parent).replace("\\", "/")
    folder = "" if folder == "." else folder
    return RunSummary(
        session_id=str(run.get("session_id") or Path(rel_path).stem.replace("S7_cfa_trinity_", "")),
        path=rel_path, folder=folder, bucket=bucket_for(folder, root), root=root,
        aborted=bool(summ.get("aborted")), abort_reason=summ.get("abort_reason"),
        metrics_scored=c1s.get("metrics_scored") if isinstance(c1s.get("metrics_scored"), int) else None,
        data_quality=dq,
        timestamp=run.get("timestamp"), engine_version=str(run.get("engine_version")) if run.get("engine_version") is not None else None,
        phase=run.get("phase"), condition=run.get("condition"), stance=run.get("stance"),
        subject=code_for(run.get("subject_framework") or ""), opponent=code_for(run.get("opponent_framework") or ""),
        subject_name=run.get("subject_framework"), opponent_name=run.get("opponent_framework"),
        deliberation_order=run.get("deliberation_order"),
        identity_augmentation=run.get("identity_augmentation"),
        metrics=metrics, metric_keys=list(c1.keys()),
        avg_convergence=round(sum(convs) / len(convs), 4) if convs else None,
        crux_count=crux,
        component2_signoffs={a: (c2.get(a) or {}).get("sign_off") for a in ("grok", "nova")},
        auditor_errors={a: _auditor_has_error(run, a) for a in ("claude", "grok", "nova")},
        corrupted_flag=corrupted or dq is not None, size_bytes=size,
    )


EXCLUDED_BUCKETS = ("errored", "dryrun")


class RunIndex:
    """``runs`` is the usable corpus: deduplicated, with ARMADA's errored
    and dry-run folders left out. ``all`` keeps every file, flagged."""

    def __init__(self, runs: List[RunSummary], built_at: str, scanned_files: int):
        self.all: List[RunSummary] = runs                       # includes duplicates and excluded buckets
        self.runs: List[RunSummary] = [r for r in runs if not r.duplicate_of and r.bucket not in EXCLUDED_BUCKETS]
        self.by_session: Dict[str, RunSummary] = {r.session_id: r for r in self.runs}
        self.built_at = built_at
        self.scanned_files = scanned_files

    def filter(self, subject: Optional[str] = None, opponent: Optional[str] = None,
               condition: Optional[str] = None, phase: Optional[int] = None,
               folder: Optional[str] = None) -> List[RunSummary]:
        s = code_for(subject) if subject else None
        o = code_for(opponent) if opponent else None
        out = []
        for r in self.runs:
            if s and r.subject != s: continue
            if o and r.opponent != o: continue
            if condition and r.condition != condition: continue
            if phase is not None and r.phase != phase: continue
            if folder is not None and r.folder != folder: continue
            out.append(r)
        return out

    def counts(self, by: Iterable[str] = ("subject", "opponent", "condition")) -> Dict[str, int]:
        by = tuple(by)
        out: Dict[str, int] = {}
        for r in self.runs:
            k = "|".join(str(getattr(r, b)) for b in by)
            out[k] = out.get(k, 0) + 1
        return dict(sorted(out.items()))

    def summary(self) -> Dict[str, Any]:
        dups = [r for r in self.all if r.duplicate_of]
        by_bucket: Dict[str, int] = {}
        for r in self.all:
            if not r.duplicate_of:
                by_bucket[r.bucket] = by_bucket.get(r.bucket, 0) + 1
        dashboard = sum(by_bucket.get(b, 0) for b in ("worldview", "calibration", "pre_schema"))
        return {
            "available": True,
            "built_at": self.built_at,
            "scanned_files": self.scanned_files,
            "distinct_runs": len(self.runs),
            "duplicate_files": len(dups),
            "by_bucket": dict(sorted(by_bucket.items())),
            "excluded_buckets": list(EXCLUDED_BUCKETS),
            "mission_control_equivalent": dashboard,     # worldview + calibration + pre_schema
            "unfiled_top_level": by_bucket.get("unfiled", 0),
            "cfa_archive_only": by_bucket.get("cfa_archive", 0),
            "aborted_runs": sum(1 for r in self.runs if r.aborted),
            "fully_scored_runs": sum(1 for r in self.runs if not r.aborted and r.bucket not in ("calibration", "pre_schema")),
            "by_subject": self.counts(("subject",)),
            "by_condition": self.counts(("condition",)),
            "by_phase": self.counts(("phase",)),
            "by_subject_opponent_condition": self.counts(("subject", "opponent", "condition")),
            "nova_error_runs": sum(1 for r in self.runs if r.auditor_errors.get("nova")),
            "corrupted_flag_runs": sum(1 for r in self.runs if r.corrupted_flag),
            "earliest": min((r.timestamp for r in self.runs if r.timestamp), default=None),
            "latest": max((r.timestamp for r in self.runs if r.timestamp), default=None),
        }


# ---------------------------------------------------------------------------
# cache
# ---------------------------------------------------------------------------

def _cache_file() -> Path:
    return paths.CACHE_DIR / "runs_index.json"


def _read_cache() -> Dict[str, Any]:
    p = _cache_file()
    if not p.exists():
        return {}
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        return data if data.get("version") == INDEX_VERSION else {}
    except (OSError, ValueError):
        return {}


def _write_cache(entries: Dict[str, Any], built_at: str) -> None:
    try:
        paths.CACHE_DIR.mkdir(parents=True, exist_ok=True)
        _cache_file().write_text(json.dumps({"version": INDEX_VERSION, "built_at": built_at, "entries": entries}),
                                 encoding="utf-8")
    except OSError:
        pass  # cache is an optimization, never a requirement


_INDEX: Optional[RunIndex] = None


def load_run_index(force: bool = False) -> Optional[RunIndex]:
    """Index of every run on disk, or None when the Nyquist corpus is not reachable."""
    global _INDEX
    if _INDEX is not None and not force:
        return _INDEX
    if not paths.runs_available() and not paths.CFA_ARCHIVE_RUNS.is_dir():
        return None

    cache = _read_cache().get("entries", {}) if not force else {}
    entries: Dict[str, Any] = {}
    summaries: List[RunSummary] = []
    scanned = 0
    for root, base in ROOTS():
        if not base.is_dir():
            continue
        files = sorted(base.rglob(_PATTERN))
        scanned += len(files)
        for f in files:
            rel = str(f.relative_to(base)).replace("\\", "/")
            key = f"{root}:{rel}"
            st = f.stat()
            hit = cache.get(key)
            if hit and hit.get("mtime") == st.st_mtime and hit.get("size") == st.st_size:
                entries[key] = hit
                summaries.append(RunSummary(**hit["summary"]))
                continue
            try:
                text = f.read_text(encoding="utf-8", errors="replace")
                run = json.loads(text)
            except (OSError, ValueError):
                continue
            s = summarize_run(run, rel, st.st_size, "CORRUPTED" in text, root)
            entries[key] = {"mtime": st.st_mtime, "size": st.st_size, "summary": asdict(s)}
            summaries.append(s)

    # Dedupe by session_id: prefer the Nyquist copy inside a cfa_trinity/<CODE>/ folder.
    def _rank(s: RunSummary) -> int:
        return (2 if s.root == "nyquist" else 0) + (1 if s.folder else 0)
    best: Dict[str, RunSummary] = {}
    for s in summaries:
        s.duplicate_of = None
        cur = best.get(s.session_id)
        if cur is None or _rank(s) > _rank(cur):
            best[s.session_id] = s
    for s in summaries:
        if best[s.session_id] is not s:
            s.duplicate_of = f"{best[s.session_id].root}:{best[s.session_id].path}"

    built = datetime.now().isoformat(timespec="seconds")
    _write_cache(entries, built)
    _INDEX = RunIndex(summaries, built, scanned)
    return _INDEX


def ROOTS():
    """Scan roots in priority order: the Nyquist corpus, then CFA's own archive."""
    return [("nyquist", paths.RUNS_DIR), ("cfa_archive", paths.CFA_ARCHIVE_RUNS)]


def load_run(session_id: str) -> Optional[Dict[str, Any]]:
    """Full JSON for one run (transcripts included)."""
    idx = load_run_index()
    if idx is None:
        return None
    r = idx.by_session.get(session_id)
    if not r:
        return None
    base = dict(ROOTS()).get(r.root, paths.RUNS_DIR)
    try:
        return json.loads((base / r.path).read_text(encoding="utf-8", errors="replace"))
    except (OSError, ValueError):
        return None
