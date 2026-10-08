"""Small, offline helpers shared by the Creative Studio and its checks."""

from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

FAVORITES_FORMAT = "cfa-visual-favorites-v1"
VISUAL_KINDS = {"image", "video", "gif"}


def media_path(library_dir: Path, value: str | None) -> Path | None:
    """Resolve only packaged files; never follow local or remote source paths."""
    if not value or not isinstance(value, str):
        return None
    decoded = unquote(value)
    parsed = urlsplit(decoded)
    if parsed.scheme or parsed.netloc or "\\" in decoded:
        return None
    root = library_dir.resolve()
    target = (root / decoded).resolve()
    if not target.is_relative_to(root) or not target.is_file():
        return None
    return target


def ordered_assets(
    assets: list[dict[str, Any]], albums: list[dict[str, Any]],
    project: str, category: str = "all", album_id: str = "all", query: str = "",
) -> list[tuple[dict[str, Any], dict[str, Any] | None]]:
    """Follow supplied album and member order, showing each picture once."""
    by_id = {a["id"]: a for a in assets if a.get("project") == project and a.get("kind") in VISUAL_KINDS}
    eligible_albums = [a for a in albums if a.get("project") == project
                       and (category == "all" or a.get("category") == category)
                       and (album_id == "all" or a.get("id") == album_id)]
    result, seen = [], set()
    terms = query.casefold().split()

    def append(asset: dict[str, Any], album: dict[str, Any] | None) -> None:
        if asset["id"] in seen:
            return
        haystack = " ".join(str(asset.get(k, "")) for k in ("title", "filename", "note", "beat", "lyric", "tags"))
        if album:
            haystack += " " + str(album.get("title", ""))
        if all(term in haystack.casefold() for term in terms):
            result.append((asset, album))
            seen.add(asset["id"])

    for album in eligible_albums:
        for asset_id in album.get("assetIDs", []):
            if asset_id in by_id:
                append(by_id[asset_id], album)
    if album_id == "all":
        for asset in by_id.values():
            if category == "all" or asset.get("category") == category:
                append(asset, None)
    return result


def favorite_payload(assets: list[dict[str, Any]], favorites: set[str], notes: dict[str, str]) -> dict[str, Any]:
    items = [{"id": a["id"], "project": a.get("project"), "filename": a.get("filename"),
              "path": a.get("repoPath", a.get("src")), "sha256": a.get("sha256") or None,
              "role": a.get("category")}
             for a in assets if a["id"] in favorites]
    valid_ids = {a["id"] for a in assets}
    hashes = {a["id"]: a.get("sha256") for a in assets}
    return {"format": FAVORITES_FORMAT, "exported": datetime.now(timezone.utc).isoformat(),
            "status": "user review shortlist; not automatic final approval", "items": items,
            "notes": {key: value for key, value in notes.items() if key in valid_ids and value.strip()},
            "note_refs": {key: hashes[key] for key, value in notes.items() if key in valid_ids and value.strip()}}


def read_favorites(payload: Any, assets: list[dict[str, Any]]) -> tuple[set[str], dict[str, str], int]:
    """Import known IDs only, and reject mismatched source hashes."""
    if not isinstance(payload, dict) or payload.get("format") != FAVORITES_FORMAT or not isinstance(payload.get("items"), list):
        raise ValueError("Choose a Creative Studio favorites export (cfa-visual-favorites-v1).")
    by_id = {a["id"]: a for a in assets}
    accepted, skipped = set(), 0
    for item in payload["items"]:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            skipped += 1
            continue
        asset = by_id.get(item["id"])
        if asset and (not item.get("sha256") or item["sha256"] == asset.get("sha256")):
            accepted.add(item["id"])
        else:
            skipped += 1
    raw_notes = payload.get("notes", {})
    note_refs = payload.get("note_refs", {})
    if not isinstance(note_refs, dict):
        note_refs = {}
    notes = {key: value[:20000] for key, value in raw_notes.items()
             if key in by_id and isinstance(value, str)
             and (not note_refs.get(key) or note_refs[key] == by_id[key].get("sha256"))} if isinstance(raw_notes, dict) else {}
    return accepted, notes, skipped
