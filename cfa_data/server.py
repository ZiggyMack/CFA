"""
A small read-only JSON API over cfa_data, for any renderer that wants live
data instead of a static bundle.

    python -m cfa_data.server              # http://127.0.0.1:8601
    python -m cfa_data.server --port 9000

Endpoints (all GET, all JSON):
    /api/health
    /api/worldviews                         list, light fields
    /api/worldviews/<code>                  full normalized profile
    /api/matchups?condition=external        every matchup with evidence
    /api/matchups/<subject>/<opponent>      ?condition=external|control
    /api/coverage                           readiness grids
    /api/runs?subject=&opponent=&condition=&phase=   run summaries
    /api/runs/<session_id>                  full run JSON (transcripts)
    /api/sync                               SYNC bridge snapshot
    /api/status                             computed Mission-Control numbers

Codes accept any spelling the repo uses ("OJ", "Orthodox Judaism",
"ORTHODOX_JUDAISM", "vs_orthodox_judaism"). Port 8601 avoids the Streamlit
apps on 8501/8503/8504 and Pathfinder on 8506.
"""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from typing import Any

from flask import Flask, Response, request

from .codes import WORLDVIEWS, code_for
from .matchups import coverage_matrix, get_matchup, list_matchups
from .profiles import load_worldviews
from .runs import load_run, load_run_index
from .status import build_status
from .sync import sync_state


def _json(obj: Any, status: int = 200) -> Response:
    body = json.dumps(obj, ensure_ascii=False, default=str)
    resp = Response(body, status=status, mimetype="application/json; charset=utf-8")
    resp.headers["Access-Control-Allow-Origin"] = "*"      # local renderers only; read-only API
    return resp


def _err(msg: str, status: int = 404) -> Response:
    return _json({"error": msg}, status)


def create_app() -> Flask:
    app = Flask("cfa_data")

    @app.get("/api/health")
    def health():
        from . import paths
        return _json({"ok": True, "worldviews": len(load_worldviews()),
                      "runs_available": paths.runs_available()})

    @app.get("/api/worldviews")
    def worldviews():
        return _json([{
            "code": wv.code, "name": wv.name, "status": wv.status, "tier": wv.tier,
            "version": wv.version, "last_updated": wv.last_updated,
            "axiom_count": wv.axiom_count, "debt_count": wv.debt_count, "bft_standard": wv.bft_standard,
            "canonical_levers": wv.canonical_levers,
            "canonical_levers_provenance": wv.canonical_levers_provenance,
            "canonical_ypa_standard": wv.canonical_ypa_standard,
            "matchups_with_trinity": [b.key for b in wv.trinity_by_matchup.values()],
            "matchups_with_levers": [b.key for b in wv.levers_by_matchup.values() if not b.malformed],
            "depth_pass_pending": wv.depth_pass_pending,
        } for wv in load_worldviews().values()])

    @app.get("/api/worldviews/<code>")
    def worldview(code: str):
        c = code_for(code)
        if not c or c not in load_worldviews():
            return _err(f"unknown worldview {code!r}; known: {list(WORLDVIEWS)}")
        return _json(load_worldviews()[c].to_dict())

    @app.get("/api/matchups")
    def matchups():
        cond = request.args.get("condition")
        return _json([m.to_dict() for m in list_matchups(cond)])

    @app.get("/api/matchups/<subject>/<opponent>")
    def matchup(subject: str, opponent: str):
        cond = request.args.get("condition", "external")
        if cond not in ("external", "control"):
            return _err("condition must be external or control", 400)
        try:
            m = get_matchup(subject, None if opponent.lower() == "pooled" else opponent, cond)
        except KeyError as e:
            return _err(str(e))
        return _json(m.to_dict())

    @app.get("/api/coverage")
    def coverage():
        return _json(coverage_matrix())

    @app.get("/api/runs")
    def runs():
        idx = load_run_index()
        if idx is None:
            return _err("run corpus not reachable; set CFA_RUNS_DIR", 503)
        phase = request.args.get("phase")
        rows = idx.filter(subject=request.args.get("subject"), opponent=request.args.get("opponent"),
                          condition=request.args.get("condition"),
                          phase=int(phase) if phase else None, folder=request.args.get("folder"))
        bucket = request.args.get("bucket")
        if bucket:
            rows = [r for r in rows if r.bucket == bucket]
        return _json({"count": len(rows), "runs": [asdict(r) for r in rows]})

    @app.get("/api/runs/<session_id>")
    def run(session_id: str):
        data = load_run(session_id)
        return _json(data) if data else _err(f"no run {session_id!r}")

    @app.get("/api/sync")
    def sync():
        return _json(sync_state())

    @app.get("/api/status")
    def status():
        return _json(build_status())

    return app


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="cfa_data read-only JSON API")
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--port", type=int, default=8601)
    args = ap.parse_args(argv)
    create_app().run(host=args.host, port=args.port, debug=False)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
