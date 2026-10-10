"""
The worldview registry: one row per framework, mapping every spelling the
repo uses (short code, YAML file stem, display name, matchup key, run-folder
name, run-JSON stance token) onto a single canonical short code.

Why this exists: the same framework is spelled five ways across the repo.
Orthodox Judaism is ``OJ`` in Mission Control, ``ORTHODOX_JUDAISM`` on disk,
``vs_orthodox_judaism`` as a matchup key, ``OJ/`` as a run folder, and
``"Orthodox Judaism"`` inside run JSONs. Buddhism's YAML even prefixes its
matchup keys with ``b_vs_``. Everything downstream should speak short codes.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional


@dataclass(frozen=True)
class WorldviewCode:
    code: str            # canonical short code, e.g. "OJ"
    stem: str            # YAML/MD file stem, e.g. "ORTHODOX_JUDAISM"
    name: str            # display name as used inside run JSONs
    run_folder: str      # 0_results/runs/cfa_trinity/<folder>
    tier: str            # "anchor" (deep batches) | "breadth" (n=1 pass) | "control-only"

    @property
    def matchup_key(self) -> str:
        """The ``vs_<stem>`` key used in levers_by_matchup / trinity_scores_by_matchup."""
        return "vs_" + self.stem.lower()


# Order matters only for display. Tier reflects July-2026 status:
#   anchor  = CT, MdN, PT, G (n=10 golden+control batches), B (control batches)
#   breadth = the 8 worldviews populated at n=1 on 2026-07-17
WORLDVIEWS: Dict[str, WorldviewCode] = {
    w.code: w for w in [
        WorldviewCode("CT",   "CLASSICAL_THEISM",          "Classical Theism",          "CT",   "anchor"),
        WorldviewCode("MdN",  "METHODOLOGICAL_NATURALISM", "Methodological Naturalism", "MdN",  "anchor"),
        WorldviewCode("PT",   "PROCESS_THEOLOGY",          "Process Theology",          "PT",   "anchor"),
        WorldviewCode("G",    "GNOSTICISM",                "Gnosticism",                "G",    "anchor"),
        WorldviewCode("B",    "BUDDHISM",                  "Buddhism",                  "B",    "anchor"),
        WorldviewCode("OJ",   "ORTHODOX_JUDAISM",          "Orthodox Judaism",          "OJ",   "breadth"),
        WorldviewCode("LDS",  "MORMONISM",                 "Mormonism",                 "LDS",  "breadth"),
        WorldviewCode("ISL",  "ISLAM",                     "Islam",                     "ISL",  "breadth"),
        WorldviewCode("HIN",  "HINDUISM",                  "Hinduism",                  "HIN",  "breadth"),
        WorldviewCode("EXST", "EXISTENTIALISM",            "Existentialism",            "EXST", "breadth"),
        WorldviewCode("ERR",  "ERROR_THEORY",              "Error Theory",              "ERR",  "breadth"),
        WorldviewCode("NULL", "NULL_HYPOTHESIS",           "Null Hypothesis",           "NULL", "breadth"),
        WorldviewCode("DES",  "DESIDERATA_BELIEVERS",      "Desiderata Believers",      "DES",  "breadth"),
    ]
}

# Opponents that appear in data but are not worldview profiles.
# "Grant Architecture v2" was a calibration opponent in the Framework_G batches.
EXTRA_OPPONENTS: Dict[str, WorldviewCode] = {
    "GA2": WorldviewCode("GA2", "GRANT_ARCHITECTURE_V2", "Grant Architecture v2", "Framework_G", "control-only"),
}

# Special block keys inside trinity_scores_by_matchup / levers_by_matchup that
# are not opponents. They name a CONTROL condition (base model, no identity).
CONTROL_KEYS = {
    "control_baseline_ct": ("CT", "control"),
    "control_baseline_pooled": (None, "control"),   # Gnosticism: pooled CT+MdN controls
}

# ---------------------------------------------------------------------------
# lookups
# ---------------------------------------------------------------------------

_ALL = {**WORLDVIEWS, **EXTRA_OPPONENTS}

_BY_LOWER: Dict[str, str] = {}
for _w in _ALL.values():
    for _alias in (_w.code, _w.stem, _w.name, _w.run_folder, _w.matchup_key):
        _BY_LOWER[_alias.lower()] = _w.code
# legacy aliases the Streamlit loader accepts
_BY_LOWER.update({"ct": "CT", "mdn": "MdN", "oj": "OJ", "lds": "LDS", "mormonism": "LDS"})
# run-JSON stance tokens, e.g. "g_vs_b" → subject "g", opponent "b"
_BY_LOWER.update({
    "ct": "CT", "mdn": "MdN", "pt": "PT", "g": "G", "b": "B",
    "oj": "OJ", "lds": "LDS", "isl": "ISL", "hin": "HIN",
    "exst": "EXST", "err": "ERR", "null": "NULL", "des": "DES",
})


def code_for(anything: str) -> Optional[str]:
    """Resolve any spelling (code, stem, display name, matchup key, folder,
    stance token, ``b_vs_x`` key) to a canonical short code. None if unknown."""
    if not anything:
        return None
    s = anything.strip().lower()
    if s in _BY_LOWER:
        return _BY_LOWER[s]
    # strip "vs_" / "<x>_vs_" prefixes used in matchup keys
    if "_vs_" in s:
        s = s.split("_vs_", 1)[1]
    elif s.startswith("vs_"):
        s = s[3:]
    if s in _BY_LOWER:
        return _BY_LOWER[s]
    s2 = s.replace(" ", "_").replace("-", "_")
    return _BY_LOWER.get(s2)


def matchup_key_to_code(key: str):
    """Translate a YAML block key into (opponent_code, condition).

    * ``vs_classical_theism``       → ("CT", None)      condition comes from the block
    * ``b_vs_process_theology``     → ("PT", None)      Buddhism's prefixed form
    * ``control_baseline_ct``       → ("CT", "control")
    * ``control_baseline_pooled``   → (None, "control")
    """
    if key in CONTROL_KEYS:
        return CONTROL_KEYS[key]
    return (code_for(key), None)


def display_name(code: str) -> str:
    w = _ALL.get(code)
    return w.name if w else code


def stem_for(code: str) -> Optional[str]:
    w = _ALL.get(code)
    return w.stem if w else None
