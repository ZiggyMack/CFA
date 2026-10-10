"""
Write a static JSON bundle any renderer can load without a server.

    python -m cfa_data.export                 # -> .cache/cfa_export/
    python -m cfa_data.export --out some/dir

Files written:
    index.json        manifest: what is in the bundle, when, from which repo HEAD
    worldviews.json   every profile, normalized (see profiles.py)
    matchups.json     every (subject, opponent, condition) with evidence
    coverage.json     readiness grids
    runs_index.json   one summary per distinct run (no transcripts)
    sync.json         SYNC bridge snapshot
    status.json       computed Mission-Control numbers

The default output directory is under the gitignored ``.cache/`` so a
bundle is never committed by accident. Pass ``--out`` to put it where a
world renderer expects it.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from dataclasses import asdict
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from . import paths
from .matchups import coverage_matrix, list_matchups
from .profiles import load_worldviews
from .runs import load_run_index
from .status import build_status
from .sync import sync_state


def _git_head() -> str:
    try:
        return subprocess.check_output(["git", "-C", str(paths.ROOT), "rev-parse", "--short", "HEAD"],
                                       text=True, stderr=subprocess.DEVNULL).strip()
    except Exception:
        return "unknown"


def _dump(path: Path, obj: Any) -> int:
    text = json.dumps(obj, ensure_ascii=False, indent=1, default=str)
    path.write_text(text, encoding="utf-8")
    return len(text.encode("utf-8"))


def export_bundle(out_dir: Path) -> Dict[str, Any]:
    out_dir.mkdir(parents=True, exist_ok=True)
    sizes: Dict[str, int] = {}

    wvs = {code: wv.to_dict() for code, wv in load_worldviews().items()}
    sizes["worldviews.json"] = _dump(out_dir / "worldviews.json", wvs)
    sizes["matchups.json"] = _dump(out_dir / "matchups.json", [m.to_dict() for m in list_matchups()])
    sizes["coverage.json"] = _dump(out_dir / "coverage.json", coverage_matrix())
    idx = load_run_index()
    sizes["runs_index.json"] = _dump(out_dir / "runs_index.json",
                                     {"summary": idx.summary(), "runs": [asdict(r) for r in idx.runs]} if idx
                                     else {"summary": {"available": False}, "runs": []})
    sizes["sync.json"] = _dump(out_dir / "sync.json", sync_state())
    sizes["status.json"] = _dump(out_dir / "status.json", build_status())

    manifest = {
        "bundle": "cfa_data export",
        "generated_at": datetime.now().isoformat(timespec="seconds"),
        "cfa_head": _git_head(),
        "runs_dir": str(paths.RUNS_DIR) if paths.runs_available() else None,
        "files": sizes,
        "rule": "The matchup is the unit. Never aggregate lever values across opponents.",
    }
    sizes["index.json"] = _dump(out_dir / "index.json", manifest)
    return manifest


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="Export a static CFA data bundle")
    ap.add_argument("--out", default=str(paths.ROOT / ".cache" / "cfa_export"))
    args = ap.parse_args(argv)
    m = export_bundle(Path(args.out))
    print(json.dumps(m, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
