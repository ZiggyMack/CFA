"""Capture CFA files changed since a verified base snapshot, including ignored files."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import zipfile


def stamp():
    return datetime.now(timezone.utc).isoformat()


def extended(path):
    text = str(path)
    if os.name == "nt" and not text.startswith(chr(92) * 2 + "?" + chr(92)):
        text = chr(92) * 2 + "?" + chr(92) + text
    return Path(text)


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(8 * 1024 * 1024):
            result.update(block)
    return result.hexdigest()


def inventory(source):
    files, skipped = {}, []
    def fail(error):
        raise error
    for directory, directories, names in os.walk(source, followlinks=False, onerror=fail):
        directories.sort()
        for name in list(directories):
            child = Path(directory) / name
            if child.is_symlink() or child.is_junction():
                skipped.append(child.relative_to(source).as_posix())
                directories.remove(name)
        for name in sorted(names):
            child = Path(directory) / name
            relative = child.relative_to(source).as_posix()
            info = child.lstat()
            if info.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                skipped.append(relative)
            elif not stat.S_ISREG(info.st_mode):
                raise RuntimeError("Not a regular file: " + relative)
            else:
                files[relative] = {"path": relative, "bytes": info.st_size, "mtimeNs": info.st_mtime_ns}
    return files, sorted(skipped)


def main():
    if sys.version_info < (3, 12):
        raise SystemExit("Use Python 3.12 or newer.")
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-manifest", required=True)
    parser.add_argument("--base-sha256", required=True)
    parser.add_argument("--stage", required=True)
    args = parser.parse_args()
    source_display = Path("D:/Documents/CFA").resolve()
    source = extended(source_display)
    stage = Path(args.stage).resolve()
    staging_root = Path("D:/CFA_Backup_Staging").resolve()
    if not stage.is_relative_to(staging_root) or stage == staging_root:
        raise SystemExit("Choose a new staging folder under D:/CFA_Backup_Staging.")
    if stage.exists():
        raise SystemExit("Staging folder already exists; choose a new one.")
    base = json.loads(Path(args.base_manifest).read_text(encoding="utf-8"))
    if Path(base["source"]).resolve() != source_display or base.get("archiveRoot") != "CFA/":
        raise SystemExit("Base manifest is not the authorized CFA snapshot.")
    expected = {item["path"]: item for item in base["sourceFiles"]}
    current, skipped = inventory(source)
    if skipped:
        raise SystemExit("Reparse points found; review before creating a supplement: " + repr(skipped))
    added = sorted(current.keys() - expected.keys())
    removed = sorted(expected.keys() - current.keys())
    changed = sorted(path for path in current.keys() & expected.keys()
                     if (current[path]["bytes"], current[path]["mtimeNs"])
                     != (expected[path]["bytes"], expected[path]["mtimeNs"]))
    selected = sorted(added + changed)
    stage.mkdir(parents=True)
    archive = stage / (stage.name + ".zip")
    manifest = {
        "format": "cfa-snapshot-supplement-v1", "startedUtc": stamp(),
        "source": str(source_display), "baseManifest": str(Path(args.base_manifest).resolve()),
        "baseArchiveSha256": args.base_sha256, "archiveRoot": "CFA/",
        "selection": "All added files and files whose size or nanosecond modification time changed since base; no Git ignores applied",
        "sourceFileCount": len(current), "sourceBytes": sum(item["bytes"] for item in current.values()),
        "added": added, "changed": changed, "removedSinceBase": removed,
        "files": [], "postInventoryPassed": False,
        "restoreNote": "Extract to a separate new folder and review changes before applying to a newly restored base; never overwrite a live checkout blindly.",
    }
    with zipfile.ZipFile(archive, "x", compression=zipfile.ZIP_STORED, allowZip64=True, strict_timestamps=False) as bundle:
        for relative in selected:
            child = source / relative
            file_hash = digest(child)
            bundle.write(child, "CFA/" + relative)
            info = child.stat()
            if (info.st_size, info.st_mtime_ns) != (current[relative]["bytes"], current[relative]["mtimeNs"]):
                raise RuntimeError("File changed during capture: " + relative)
            manifest["files"].append({**current[relative], "sha256": file_hash})
        after, after_skipped = inventory(source)
        if current != after or skipped != after_skipped:
            raise RuntimeError("Source changed during supplement; keep this attempt as incomplete and use a fresh staging folder.")
        manifest["postInventoryPassed"] = True
        manifest["completedUtc"] = stamp()
        bundle.writestr("_CFA_SUPPLEMENT_MANIFEST.json", json.dumps(manifest, ensure_ascii=False, indent=2))
    with zipfile.ZipFile(archive) as bundle:
        if bad := bundle.testzip():
            raise RuntimeError("ZIP CRC failed: " + bad)
        for item in manifest["files"]:
            result = hashlib.sha256()
            with bundle.open("CFA/" + item["path"]) as stream:
                while block := stream.read(8 * 1024 * 1024):
                    result.update(block)
            if result.hexdigest() != item["sha256"]:
                raise RuntimeError("Archived file hash mismatch: " + item["path"])
    archive_hash = digest(archive)
    manifest_path = stage / "supplement_manifest.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    receipt = {
        "format": "cfa-snapshot-supplement-verification-v1", "archive": str(archive),
        "archiveBytes": archive.stat().st_size, "archiveSha256": archive_hash,
        "baseArchiveSha256": args.base_sha256, "fileCount": len(selected),
        "zipCrcPassed": True, "allIncludedFileHashesPassed": True,
        "postInventoryPassed": True, "removedSinceBase": removed,
        "verifiedUtc": stamp(), "mountedCopyVerified": False, "cloudUploadVerified": False,
    }
    (stage / "supplement_verification.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    (stage / (archive.name + ".sha256")).write_text(archive_hash + "  " + archive.name + "\n", encoding="ascii")
    print(json.dumps(receipt, indent=2), flush=True)


if __name__ == "__main__":
    main()
