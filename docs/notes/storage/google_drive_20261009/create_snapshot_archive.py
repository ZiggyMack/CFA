"""Create a complete, verified CFA ZIP64 snapshot outside the working tree."""
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


def stamp() -> str:
    return datetime.now(timezone.utc).isoformat()


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(8 * 1024 * 1024):
            digest.update(block)
    return digest.hexdigest()


def main() -> None:
    if sys.version_info < (3, 12):
        raise SystemExit("This Windows backup requires Python 3.12+ for junction detection.")
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", required=True)
    parser.add_argument("--stage", required=True)
    args = parser.parse_args()
    source, stage = Path(args.source).resolve(), Path(args.stage).resolve()
    if source != Path("D:/Documents/CFA").resolve():
        raise SystemExit("This dated backup is restricted to the authorized CFA project.")
    staging_root = Path("D:/CFA_Backup_Staging").resolve()
    if not stage.is_relative_to(staging_root) or stage == staging_root or stage.is_relative_to(source):
        raise SystemExit("The unique staging directory must be outside CFA, under D:/CFA_Backup_Staging.")
    stage.mkdir(parents=True, exist_ok=True)
    archive = stage / (stage.name + ".zip")
    partial = stage / (stage.name + ".partial.zip")
    if archive.exists() or partial.exists():
        raise SystemExit("A snapshot archive already exists here; choose a new staging directory.")

    source_display = str(source)
    if os.name == "nt":
        # Original media includes paths beyond the legacy Windows MAX_PATH limit.
        # Keep portable names in the manifest; use extended paths for filesystem I/O.
        source = Path(chr(92) * 2 + "?" + chr(92) + source_display)

    manifest = {
        "format": "cfa-full-project-zip64-v1", "source": source_display, "startedUtc": stamp(),
        "targetDesktopAccountObserved": "Stephen Wright (coordinator's installed Drive UI observation)",
        "targetAccountNote": "User specifies the separate higher-capacity desktop account, not Ziggy Mack browser/plugin account.",
        "cloudQuotaVerified": False, "cloudUploadVerified": False,
        "archiveRoot": "CFA/", "compression": "ZIP_STORED; ZIP64 enabled", "pythonVersion": sys.version,
        "scope": "All regular project files, including .git and Git-ignored media; no ignore rules applied.",
        "sourceFiles": [], "skippedReparsePoints": [], "failedReads": [], "changedDuringRead": [],
        "addedAfterArchiving": [], "missingAfterArchiving": [], "changedAfterArchiving": [],
        "reparseInventoryChanged": False,
    }
    files, total_bytes = manifest["sourceFiles"], 0

    def walk_error(error: OSError) -> None:
        manifest["failedReads"].append({"path": str(error.filename), "error": str(error)})

    with zipfile.ZipFile(partial, "x", compression=zipfile.ZIP_STORED, allowZip64=True, strict_timestamps=False) as bundle:
        for directory, directories, names in os.walk(source, followlinks=False, onerror=walk_error):
            directories.sort()
            for child in list(directories):
                child_path = Path(directory) / child
                if child_path.is_symlink() or child_path.is_junction():
                    manifest["skippedReparsePoints"].append(str(child_path.relative_to(source)))
                    directories.remove(child)
            for name in sorted(names):
                path = Path(directory) / name
                relative = path.relative_to(source).as_posix()
                try:
                    before = path.lstat()
                    if before.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                        manifest["skippedReparsePoints"].append(relative)
                        continue
                    if not stat.S_ISREG(before.st_mode):
                        manifest["failedReads"].append({"path": relative, "error": "Not a regular file"})
                        continue
                    bundle.write(path, "CFA/" + relative)
                    after = path.stat()
                    if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
                        manifest["changedDuringRead"].append(relative)
                    files.append({"path": relative, "bytes": before.st_size, "mtimeNs": before.st_mtime_ns})
                    total_bytes += before.st_size
                    if len(files) % 5000 == 0:
                        print(f"Archived {len(files):,} files / {total_bytes:,} source bytes", flush=True)
                except OSError as error:
                    manifest["failedReads"].append({"path": relative, "error": str(error)})

        # Other collaborators may still be writing. Re-enumerate the complete
        # source after reading it, including files added outside our first walk.
        expected = {item["path"]: (item["bytes"], item["mtimeNs"]) for item in files}
        seen, final_reparse = set(), set()
        for directory, directories, names in os.walk(source, followlinks=False, onerror=walk_error):
            for child in list(directories):
                child_path = Path(directory) / child
                if child_path.is_symlink() or child_path.is_junction():
                    final_reparse.add(str(child_path.relative_to(source)))
                    directories.remove(child)
            for name in names:
                path = Path(directory) / name
                relative = path.relative_to(source).as_posix()
                try:
                    current = path.lstat()
                    if current.st_file_attributes & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                        final_reparse.add(relative)
                        continue
                    seen.add(relative)
                    if relative not in expected:
                        manifest["addedAfterArchiving"].append(relative)
                    elif expected[relative] != (current.st_size, current.st_mtime_ns):
                        manifest["changedAfterArchiving"].append(relative)
                except OSError as error:
                    manifest["failedReads"].append({"path": relative, "error": str(error)})
        manifest["missingAfterArchiving"] = sorted(expected.keys() - seen)
        manifest["reparseInventoryChanged"] = final_reparse != set(manifest["skippedReparsePoints"])
        manifest["finalReparsePoints"] = sorted(final_reparse)
        manifest["postArchiveInventoryCheckedUtc"] = stamp()
        manifest.update(sourceFileCount=len(files), sourceBytes=total_bytes, completedUtc=stamp())
        bundle.writestr("_CFA_BACKUP_MANIFEST.json", json.dumps(manifest, ensure_ascii=False, indent=2))
        bundle.writestr("RESTORE_CFA.txt", (
            "CFA complete project snapshot\n\n"
            "Extract the CFA/ folder to a new local directory, preserving all nested paths and .git.\n"
            "Do not overwrite a working checkout without first preserving any newer work.\n"
            "_CFA_BACKUP_MANIFEST.json lists every archived source file, its byte size and original modification time.\n"
            "Read the external verification receipt before relying on this archive. ZIP CRC verification and\n"
            "the source archive SHA-256 were checked locally; a mounted Google Drive copy is not proof that\n"
            "server upload has completed. Independently download from the intended Drive account and compare\n"
            "the external SHA-256 receipt before treating the cloud restore as verified.\n\n"
            "This includes project content and Git history; it does not install applications or restore\n"
            "account sign-ins, credentials stored outside CFA, other projects, or Windows permissions.\n"
        ))

    (stage / "source_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    if any(manifest[key] for key in ("failedReads", "changedDuringRead", "addedAfterArchiving",
                                   "missingAfterArchiving", "changedAfterArchiving", "reparseInventoryChanged")):
        raise SystemExit("Source read failures or concurrent changes detected. Keep the partial archive; do not upload it as complete.")
    print("Checking every ZIP entry's CRC...", flush=True)
    with zipfile.ZipFile(partial) as bundle:
        bad_entry = bundle.testzip()
        if bad_entry:
            raise SystemExit("Archive CRC verification failed: " + bad_entry)
    digest = sha256(partial)
    partial.rename(archive)
    receipt = {
        "format": "cfa-full-project-zip64-verification-v1", "archive": str(archive),
        "archiveBytes": archive.stat().st_size, "archiveSha256": digest,
        "sourceFileCount": len(files), "sourceBytes": total_bytes,
        "zipCrcAllEntriesPassed": True, "failedReads": [], "changedDuringRead": [],
        "postArchiveInventoryPassed": True, "postArchiveInventoryCheckedUtc": manifest["postArchiveInventoryCheckedUtc"],
        "addedAfterArchiving": [], "missingAfterArchiving": [], "changedAfterArchiving": [],
        "skippedReparsePoints": manifest["skippedReparsePoints"], "verifiedUtc": stamp(),
        "mountedDriveCopyVerified": False, "cloudUploadVerified": False, "cloudRestoreVerified": False,
    }
    (stage / "verification_receipt.json").write_text(json.dumps(receipt, indent=2), encoding="utf-8")
    (stage / (archive.name + ".sha256")).write_text(digest + "  " + archive.name + "\n", encoding="ascii")
    print(json.dumps(receipt, indent=2), flush=True)


if __name__ == "__main__":
    main()
