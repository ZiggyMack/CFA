"""
The SYNC bridge, as data. Lists what is waiting in SYNC_IN/pending, what has
been processed, and what CFA has in SYNC_OUT, with the From/To/Date/Re header
each message carries. Read-only.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, asdict, field
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

from . import paths

_HEADER_RE = re.compile(r"^\*\*(From|To|Date|Re|Status):\*\*\s*(.+?)\s*$", re.M)
_H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.M)


@dataclass
class SyncMessage:
    folder: str                 # "SYNC_IN/pending" etc.
    filename: str
    size_bytes: int
    modified: str               # ISO date from mtime
    title: Optional[str] = None
    sender: Optional[str] = None
    recipient: Optional[str] = None
    date: Optional[str] = None
    re: Optional[str] = None
    status: Optional[str] = None
    is_dir: bool = False


def _read_headers(p: Path) -> Dict[str, str]:
    try:
        text = p.read_text(encoding="utf-8", errors="replace")[:4000]
    except OSError:
        return {}
    out: Dict[str, str] = {}
    m = _H1_RE.search(text)
    if m:
        out["title"] = m.group(1)
    for k, v in _HEADER_RE.findall(text):
        out.setdefault(k.lower(), v)
    return out


def _scan(folder: Path, label: str) -> List[SyncMessage]:
    if not folder.is_dir():
        return []
    items: List[SyncMessage] = []
    for p in sorted(folder.iterdir(), key=lambda q: q.name):
        if p.name == ".gitkeep":
            continue
        st = p.stat()
        msg = SyncMessage(
            folder=label, filename=p.name, size_bytes=st.st_size,
            modified=datetime.fromtimestamp(st.st_mtime).date().isoformat(),
            is_dir=p.is_dir(),
        )
        if p.is_file() and p.suffix.lower() == ".md":
            h = _read_headers(p)
            msg.title = h.get("title"); msg.sender = h.get("from")
            msg.recipient = h.get("to"); msg.date = h.get("date")
            msg.re = h.get("re"); msg.status = h.get("status")
        items.append(msg)
    return items


def sync_state() -> Dict[str, object]:
    """Snapshot of both directions of the bridge."""
    in_pending = _scan(paths.SYNC_IN_PENDING, "SYNC_IN/pending")
    in_processed = _scan(paths.SYNC_IN_PROCESSED, "SYNC_IN/processed")
    out_pending = _scan(paths.SYNC_OUT_PENDING, "SYNC_OUT/pending")
    out_sent = _scan(paths.SYNC_OUT_SENT, "SYNC_OUT/sent")

    # An empty "runs/" directory in pending is not a waiting delivery.
    waiting = [m for m in in_pending
               if not (m.is_dir and not any((paths.SYNC_IN_PENDING / m.filename).iterdir()))]

    newest_in = max((m.modified for m in in_processed), default=None)
    newest_out = max((m.modified for m in out_pending + out_sent), default=None)

    return {
        "inbox_waiting": len(waiting),
        "inbox_clear": len(waiting) == 0,
        "newest_processed_in": newest_in,
        "newest_out": newest_out,
        "sync_in_pending": [asdict(m) for m in in_pending],
        "sync_in_processed": [asdict(m) for m in in_processed],
        "sync_out_pending": [asdict(m) for m in out_pending],
        "sync_out_sent": [asdict(m) for m in out_sent],
    }
