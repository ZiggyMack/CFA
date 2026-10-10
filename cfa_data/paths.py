"""
Where things live. Every path cfa_data touches is defined here, and each
can be overridden with an environment variable so the package works from a
different checkout, a CI box, or a machine without the Nyquist repo.

Environment overrides:
    CFA_ROOT        repo root (default: parent of this package)
    CFA_RUNS_DIR    ARMADA run JSON root on the Nyquist side
    CFA_CACHE_DIR   where cfa_data may write its index cache (gitignored)
"""

from __future__ import annotations

import os
from pathlib import Path

ROOT = Path(os.environ.get("CFA_ROOT", Path(__file__).resolve().parent.parent))

PROFILES_DIR = ROOT / "profiles" / "worldviews"
COMPARISONS_DIR = ROOT / "profiles" / "comparisons"

REPO_SYNC = ROOT / "docs" / "REPO_SYNC"
SYNC_IN_PENDING = REPO_SYNC / "SYNC_IN" / "pending"
SYNC_IN_PROCESSED = REPO_SYNC / "SYNC_IN" / "processed"
SYNC_IN_ARCHIVED = REPO_SYNC / "SYNC_IN" / "archived"
SYNC_OUT_PENDING = REPO_SYNC / "SYNC_OUT" / "pending"
SYNC_OUT_SENT = REPO_SYNC / "SYNC_OUT" / "sent"

# ARMADA run JSONs live in the Nyquist repo. Read-only; never write here.
_DEFAULT_RUNS = Path(
    "D:/Documents/Nyquist_Consciousness/experiments/temporal_stability/"
    "S7_ARMADA/0_results/runs"
)
RUNS_DIR = Path(os.environ.get("CFA_RUNS_DIR", _DEFAULT_RUNS))

# 80 runs (pt_vs_ct, mdn_vs_pt, July 2026) exist only here, gitignored.
CFA_ARCHIVE_RUNS = REPO_SYNC / ".archive" / "raw_runs"

# .cache/ is already in the repo .gitignore.
CACHE_DIR = Path(os.environ.get("CFA_CACHE_DIR", ROOT / ".cache" / "cfa_data"))


def runs_available() -> bool:
    """True if the Nyquist run corpus is reachable from this machine."""
    return RUNS_DIR.is_dir()
