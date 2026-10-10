<!---
FILE: cfa_data/README.md
PURPOSE: The data front door — one read-only layer over profiles, matchups, runs and the SYNC bridge
VERSION: 0.1.0
STATUS: Active
DEPENDS_ON: profiles/worldviews/*.yaml, utils/calculations.py, docs/REPO_SYNC/, Nyquist 0_results/runs (optional)
NEEDED_BY: views/ (future), any JSON consumer, any world renderer
MOVES_WITH: /cfa_data/
LAST_UPDATE: 2026-10-03
--->

# cfa_data — the data front door

Everything CFA knows, readable from one place, as Python objects or JSON.
Built so the Streamlit app, a JSON API, and a future free-roaming world all
read the same facts instead of each parsing YAML on its own.

**The rule it enforces:** the matchup is the unit. Every score and lever keeps
its `(subject, opponent, condition)`. The flat `levers:` block in each YAML is
exposed as a *canonical* value with a provenance string that says whether it is
a web-research prior (the 8 breadth profiles) or a copy of a deliberated
matchup block (the anchors). Nothing is averaged across opponents.

**Read-only.** The package never writes to `profiles/`, `docs/REPO_SYNC/` or
the Nyquist repo. Its only outputs are a run-index cache and an optional export
bundle, both under the gitignored `.cache/`.

## Use it

```python
from cfa_data import load_worldviews, get_matchup, list_matchups, build_status

wv = load_worldviews()["OJ"]                 # any spelling works via code_for()
m  = get_matchup("OJ", "CT")                 # Orthodox Judaism judged under CT's lens
m.ypa_standard                               # 3.60  (six-lever sum / BFT, the YAML convention)
m.ypa_scenarios                              # Console formula: Neutral / Existential / Empirical
m.trinity.metrics["MS"].crux_rate            # 0.0 .. 1.0
get_matchup("OJ", "CT", "control")           # the base-model control for the same pair
build_status()                               # Mission-Control numbers, computed
```

Run the JSON API (port 8601, read-only, CORS open for local renderers):

```powershell
python -m cfa_data.server
```

| Endpoint | Returns |
|---|---|
| `/api/worldviews` | 13 profiles, light fields |
| `/api/worldviews/<code>` | full normalized profile |
| `/api/matchups?condition=external` | every pairing with evidence |
| `/api/matchups/<subject>/<opponent>?condition=` | one matchup, scores + levers + YPA |
| `/api/coverage` | readiness grids (external and control) |
| `/api/runs?subject=&opponent=&condition=&phase=` | run summaries from the Nyquist corpus |
| `/api/runs/<session_id>` | one full run JSON, transcripts included |
| `/api/sync` | SYNC_IN / SYNC_OUT snapshot with message headers |
| `/api/status` | computed status plus structural open loops |

Write a static bundle a renderer can load with no server:

```powershell
python -m cfa_data.export --out .cache/cfa_export
```

Run the tests from the repo root (they use the real profiles as fixtures and
skip the run-corpus tests if the Nyquist repo is not mounted):

```powershell
python -m unittest discover -s cfa_data/tests -v
```

## What it normalizes

Three historical YAML block shapes become one `TrinityBlock` / `Metric` model:
the breadth n=1 shape (`claude_score`, `convergence`, `crux_declared`), the
batch shape (`claude_mean`, `convergence_pct`, `crux_rate "3/10"`,
`divergence_layer`), and Gnosticism's pooled control. Buddhism's `b_vs_*` keys
and the `control_baseline_*` keys resolve to `(opponent, condition)` through
`codes.matchup_key_to_code`. Process Theology's misplaced `vs_buddhism` lever
block is flagged `malformed` rather than crashing the loader.

Two YPA definitions exist in the repo and both are returned, never mixed:
`ypa_standard` (all six levers / BFT, what the YAML `calculated.*` fields hold)
and `ypa_scenarios` (the Console formula from `utils/calculations.py` with the
Console's default toggles).

## Environment

| Variable | Default | Purpose |
|---|---|---|
| `CFA_ROOT` | parent of this package | repo root |
| `CFA_RUNS_DIR` | the Nyquist `S7_ARMADA/0_results/runs` path on this PC | ARMADA run corpus |
| `CFA_CACHE_DIR` | `.cache/cfa_data/` | run-index cache |

A second scan root is fixed: `docs/REPO_SYNC/.archive/raw_runs/` (gitignored), the
only place 80 July-2026 runs (pt_vs_ct, mdn_vs_pt) exist. Runs are deduplicated
across roots by `session_id`, preferring the Nyquist copy inside a worldview folder.

Every run carries a `bucket` (`worldview`, `calibration`, `pre_schema`, `unfiled`,
`cfa_archive`, `errored`, `dryrun`), an `aborted` flag read from `summary.aborted`
(ARMADA's batch runner reports exit codes only, so aborted runs sit among good
ones), and any in-place `data_quality` flag such as `CORRUPTED_QUESTION_STALE`.
`RunIndex.runs` excludes `errored` and `dryrun`; filter on `aborted` yourself
before averaging anything.

## Not yet here

Museum operators and dig sites (Cognitive Archaeology) live in the Nyquist
`LLM_BOOK` staging area and are the next slice once their file format is
mapped. The Streamlit views still read YAML directly; moving them onto this
layer is a separate change.
