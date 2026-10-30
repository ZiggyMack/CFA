"""Package the complete existing HTML dashboard as a separate Streamlit component.

No server, upload, image conversion, or master mutation is performed. Local builds
use hardlinks; --copy-media explicitly makes independent files for a portable copy.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[2]
APP = Path(__file__).resolve().parent
VISUAL = ROOT / "docs/notes/explorable_world/comfy/projects/visual_library"
DEFAULT_OUTPUT = APP / "full_dashboard_bundle"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def read_catalog(raw: bytes) -> dict:
    text = raw.decode("utf-8-sig")
    match = re.fullmatch(r"\s*window\.REVIEW_CATALOG\s*=\s*(.*?)\s*;?\s*", text, re.S)
    if not match:
        raise ValueError("Expected the generated REVIEW_CATALOG assignment, not arbitrary JavaScript.")
    data = json.loads(match.group(1).rstrip(";"))
    if not all(isinstance(data.get(k), list) for k in ("projects", "assets", "albums", "categories")):
        raise ValueError("Dashboard catalog is missing its required lists.")
    return data


def source_file(value: str, source_dir: Path, root: Path) -> Path:
    decoded = unquote(value)
    parsed = urlsplit(decoded)
    if parsed.scheme or parsed.netloc or "\\" in decoded or parsed.query or parsed.fragment:
        raise ValueError(f"Not a relative catalog file: {value}")
    target = (source_dir / decoded).resolve()
    if not target.is_relative_to(root.resolve()) or not target.is_file():
        raise ValueError(f"Missing or out-of-repository dashboard file: {value}")
    return target


def context_pack_references(index: dict | None) -> list[tuple[dict, str, str, dict]]:
    """Return only explicitly listed pack guides/downloads, with required provenance."""
    if index is None:
        return []
    if index.get("schemaVersion") != 1 or index.get("status") != "prepared_not_delivered":
        raise ValueError("Invalid project context pack schema / status.")
    if not isinstance(index.get("packs"), list) or not isinstance(index.get("files"), list):
        raise ValueError("Project context pack lists are missing.")
    records = {}
    prefix = "docs/notes/explorable_world/comfy/projects/collaborators/project_context_packs_20261010/"
    for entry in index["files"]:
        name = entry.get("path", "")
        if (not isinstance(name, str) or not name.startswith(prefix)
                or any(part in ("", ".", "..") for part in name.split("/"))
                or re.search(r"[\\%?#:\x00-\x1f\x7f]", name)):
            raise ValueError("Unsafe project context pack path.")
        if (name in records or not re.fullmatch(r"[0-9a-f]{64}", entry.get("sha256", ""))
                or type(entry.get("bytes")) is not int or entry["bytes"] < 0):
            raise ValueError("Invalid project context pack file provenance.")
        records[name] = entry
    recipients = [pack.get("recipientID") for pack in index["packs"]]
    if len(set(recipients)) != len(recipients):
        raise ValueError("Repeated project context pack recipients.")
    references = [(index, "uploadMapPath", "uploadMapHref", ".txt"),
                  (index, "allPacksZipPath", "allPacksZipHref", ".zip")]
    references.extend((pack, key, href, suffix) for pack in index["packs"]
                      for key, href, suffix in [("loadGuidePath", "loadGuideHref", ".txt"),
                                                ("zipPath", "zipHref", ".zip")])
    result = []
    for owner, key, href, suffix in references:
        name = owner.get(key)
        if name not in records or not name.endswith(suffix):
            raise ValueError("Unverified project context pack link: " + key)
        result.append((owner, key, href, records[name]))
    return result


def write_generated(target: Path, content: bytes) -> None:
    """Replace generated files atomically; never write through a media hardlink."""
    temporary = target.with_name(target.name + ".tmp")
    temporary.write_bytes(content)
    temporary.replace(target)


def build(source_dir: Path = VISUAL, output: Path = DEFAULT_OUTPUT,
          root: Path = ROOT, copy_media: bool = False) -> dict:
    root, source_dir, output = root.resolve(), source_dir.resolve(), output.resolve()
    if not source_dir.is_relative_to(root) or not output.is_relative_to(root):
        raise ValueError("Source and destination must remain inside the repository.")
    if output == source_dir or source_dir.is_relative_to(output):
        raise ValueError("The generated bundle must be separate from dashboard sources.")
    sources = {name: (source_dir / name).read_bytes()
               for name in ("catalog.js", "library.js", "library.css", "source_foundation.js", "storyboard_takes.js")}
    bridge = (APP / "full_dashboard_bridge.js").read_bytes()
    hashes = {name: digest(raw) for name, raw in sources.items()}
    hashes["bridge.js"] = digest(bridge)
    mode = "copy" if copy_media else "hardlink"
    build_id = digest(json.dumps({"sources": hashes, "mode": mode, "format": 2}, sort_keys=True).encode())[:20]
    snapshot = output / "snapshots" / build_id
    snapshot.mkdir(parents=True, exist_ok=True)
    media = snapshot / "media"
    media.mkdir(exist_ok=True)
    if not snapshot.resolve().is_relative_to(output) or not media.resolve().is_relative_to(snapshot):
        raise ValueError("Bundle destination contains an unexpected path redirect.")
    catalog = read_catalog(sources["catalog.js"])
    source_cache: dict[Path, str] = {}
    files: dict[str, dict] = {}

    def package(value: str, expected_hash: str | None = None, inert: bool = False) -> str:
        source = source_file(value, source_dir, root)
        actual = source_cache.get(source)
        if not actual:
            actual = digest(source.read_bytes())
            source_cache[source] = actual
        if expected_hash and actual != expected_hash:
            raise ValueError(f"Original hash mismatch: {source.name}")
        suffix = ".txt" if inert else source.suffix.lower()
        # A component serves files; it never needs executable HTML, JS or Python as media.
        if suffix not in {".jpg", ".jpeg", ".png", ".webp", ".avif", ".gif", ".svg", ".mp4", ".webm", ".mov", ".mp3", ".wav", ".m4a", ".pdf", ".txt", ".json", ".csv", ".md", ".zip"}:
            suffix = ".txt"
        relative = f"media/{actual}{suffix}"
        target = snapshot / relative
        if not target.resolve().is_relative_to(snapshot):
            raise ValueError("Media destination escapes the bundle.")
        if target.exists():
            if digest(target.read_bytes()) != actual:
                raise ValueError(f"Existing bundle media differs: {relative}")
        elif copy_media:
            shutil.copyfile(source, target)
        else:
            try:
                os.link(source, target)
            except OSError as exc:
                raise RuntimeError("A local build needs same-volume hardlink support. Use --copy-media only when an independent portable copy is intended.") from exc
        if relative not in files:
            files[relative] = {"path": relative, "sha256": actual, "bytes": source.stat().st_size,
                               "mode": mode, "sourcePaths": []}
        name = source.relative_to(root).as_posix()
        if name not in files[relative]["sourcePaths"]:
            files[relative]["sourcePaths"].append(name)
        return relative

    for asset in catalog["assets"]:
        asset["src"] = package(asset["src"], asset.get("sha256"), asset.get("kind") == "document")
        if asset.get("thumb"):
            asset["thumb"] = package(asset["thumb"])

    # Mission-control downloads and explicitly opted-in context packs are allowed.
    # Invalid links remain a recorded gap instead of exposing a broad repository server.
    unresolved = []
    for task in catalog.get("missionControl", {}).get("tasks", []):
        for link in task.get("links", []):
            value = link.get("href")
            if not value or value.startswith("#"):
                continue
            parsed = urlsplit(value)
            if parsed.scheme == "https" and parsed.netloc:
                # Preserve external evidence links as data. The existing dashboard
                # applies its own navigation policy; the builder never fetches them.
                continue
            if parsed.path == "../index.html" and parsed.fragment and not parsed.query:
                link["href"] = "index.html#" + parsed.fragment
                continue
            try:
                link["href"] = package(value)
            except (ValueError, OSError) as exc:
                unresolved.append({"taskID": task.get("id"), "label": link.get("label"), "href": value, "reason": str(exc)})
                link.pop("href", None)

    # Opted-in context guides and transport ZIPs are packaged with their exact hashes.
    # Repository locators remain evidence; component hrefs never expose the checkout.
    context_refs = context_pack_references(catalog.get("projectContextPacks"))
    for owner, key, href, entry in context_refs:
        source = source_file(entry["path"], root, root)
        pack_root = root / "docs/notes/explorable_world/comfy/projects/collaborators/project_context_packs_20261010"
        if not source.is_relative_to(pack_root.resolve()) or source.stat().st_size != entry["bytes"]:
            raise ValueError("Project context pack source location / size mismatch.")
        value = os.path.relpath(source, source_dir).replace("\\", "/")
        owner[href] = package(value, entry["sha256"])

    catalog_raw = ("window.REVIEW_CATALOG=" + json.dumps(catalog, ensure_ascii=False, separators=(",", ":")) + ";\n").encode("utf-8")
    index = ("<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">"
             "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">"
             f"<title>CFA Full Visual Library</title><link rel=\"stylesheet\" href=\"library.css?v={hashes['library.css'][:12]}\"></head>"
             "<body><div id=\"app\"></div><script>window.REVIEW_INITIAL={project:'hon',view:'all'};"
             f"window.REVIEW_BUILD='{build_id}';</script><script src=\"bridge.js?v={hashes['bridge.js'][:12]}\"></script>"
             f"<script src=\"catalog.js?v={digest(catalog_raw)[:12]}\"></script>"
             f"<script src=\"source_foundation.js?v={hashes['source_foundation.js'][:12]}\"></script>"
             f"<script src=\"storyboard_takes.js?v={hashes['storyboard_takes.js'][:12]}\"></script>"
             f"<script src=\"library.js?v={hashes['library.js'][:12]}\"></script></body></html>\n").encode()
    for name, raw in {"index.html": index, "library.js": sources["library.js"], "library.css": sources["library.css"],
                      "catalog.js": catalog_raw, "bridge.js": bridge,
                      "source_foundation.js": sources["source_foundation.js"],
                      "storyboard_takes.js": sources["storyboard_takes.js"]}.items():
        write_generated(snapshot / name, raw)
    receipt = {"format": "cfa-full-dashboard-bundle-v1", "buildID": build_id,
               "builtAt": datetime.now(timezone.utc).isoformat(), "sourceHashes": hashes,
               "assetCount": len(catalog["assets"]), "albumCount": len(catalog["albums"]),
               "mediaMode": mode, "fileCount": len(files), "logicalMediaBytes": sum(x["bytes"] for x in files.values()),
               "additionalMediaBytes": sum(x["bytes"] for x in files.values()) if copy_media else 0,
               "unresolvedPreparedLinks": unresolved, "files": list(files.values()),
               "reviewStorage": "Browser storage for this hosted origin; existing JSON import/export retained. No automatic cross-device sync.",
               "deployment": "Prepared locally. No upload or publication performed."}
    write_generated(snapshot / "bundle_manifest.json", (json.dumps(receipt, indent=2) + "\n").encode())
    current = {"format": receipt["format"], "buildID": build_id, "snapshot": f"snapshots/{build_id}",
               "assetCount": receipt["assetCount"], "mediaMode": mode}
    write_generated(output / "current.json", (json.dumps(current, indent=2) + "\n").encode())
    return receipt


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--copy-media", action="store_true", help="Create independent media copies for a portable package; local default is hardlinks.")
    args = parser.parse_args()
    result = build(output=args.output, copy_media=args.copy_media)
    print(json.dumps({k: result[k] for k in ("buildID", "assetCount", "albumCount", "mediaMode", "fileCount", "logicalMediaBytes", "additionalMediaBytes", "unresolvedPreparedLinks")}, indent=2))


if __name__ == "__main__":
    main()
