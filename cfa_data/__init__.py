"""
cfa_data — the data front door for CFA.

One place that knows how to read every CFA artifact (worldview profiles,
per-matchup Trinity scores and levers, ARMADA run JSONs, the SYNC bridge
inbox) and hand it to any consumer — the Streamlit app, a JSON API, a
static export for a world renderer — as plain Python objects or JSON.

Rules this package enforces (see docs/i_am/I_AM.md v5.0):

* The MATCHUP is the fundamental unit. Lever values and Trinity scores
  belong to (subject, opponent, condition), never to a worldview alone.
  The flat canonical ``levers:`` block is a web-research PRIOR, exposed
  as such and never silently merged with deliberated values.
* Everything here is READ-ONLY. Nothing in cfa_data writes to profiles/,
  docs/REPO_SYNC/ or the Nyquist repo. The only thing it writes is its own
  cache and an optional export bundle, both outside git.

Quick use::

    from cfa_data import load_worldviews, get_matchup, build_status
    wv = load_worldviews()["OJ"]
    m  = get_matchup("OJ", "CT")          # external-identity matchup
    s  = build_status()                   # Mission-Control numbers, computed

Run the JSON server::

    python -m cfa_data.server            # http://127.0.0.1:8601/api/...

Write a static bundle for a renderer::

    python -m cfa_data.export --out .cache/cfa_export
"""

from .codes import WORLDVIEWS, code_for, display_name, matchup_key_to_code
from .profiles import load_worldviews, load_worldview, Worldview
from .matchups import get_matchup, list_matchups, coverage_matrix, Matchup
from .runs import RunIndex, load_run_index, load_run
from .sync import sync_state
from .status import build_status

__all__ = [
    "WORLDVIEWS", "code_for", "display_name", "matchup_key_to_code",
    "load_worldviews", "load_worldview", "Worldview",
    "get_matchup", "list_matchups", "coverage_matrix", "Matchup",
    "RunIndex", "load_run_index", "load_run",
    "sync_state", "build_status",
]
