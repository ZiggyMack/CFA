"""Audit current repository text for a local-profile token; redact only on request.

Originals are saved outside the repository before atomic replacement. Git history,
external backups and binary media are never changed by this tool.
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
import subprocess
import uuid

ROOT = Path(__file__).resolve().parents[1]


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def find_files(token):
    rg = shutil.which("rg")
    if not rg:
        raise SystemExit("ripgrep is required; no packages are installed automatically.")
    args = [rg, "-l", "-0", "-i", "--hidden", "--no-ignore", "--fixed-strings"]
    for pattern in ("!.git/**", "!**/node_modules/**", "!**/.venv/**", "!**/venv/**", "!**/__pycache__/**", "!**/*.min.js"):
        args.extend(["--glob", pattern])
    result = subprocess.run(args + [token, "."], cwd=ROOT, capture_output=True)
    if result.returncode not in (0, 1):
        raise SystemExit("Text inventory failed; no mutation attempted.")
    return sorted({(ROOT / os.fsdecode(p)).resolve() for p in result.stdout.split(b"\0") if p})


def decode(raw):
    encoding = "utf-16" if raw.startswith((b"\xff\xfe", b"\xfe\xff")) else "utf-8-sig" if raw.startswith(b"\xef\xbb\xbf") else "utf-8"
    return raw.decode(encoding), encoding


def redact(text, token, path):
    escaped = re.escape(token)
    # Executable helpers receive real environment/path expressions, not fake paths.
    if path.suffix == ".cjs":
        quoted = re.compile(r"(['\"])[Cc]:[/\\]+Users[/\\]+" + escaped + r"([^'\"\r\n]*)\1", re.I)
        text = quoted.sub(lambda m: "`${process.env.USERPROFILE}" + m[2].replace("\\\\", "/").replace("\\", "/") + "`", text)
    if path.suffix == ".py":
        quoted = re.compile(r"(?:r)?(['\"])[Cc]:[/\\]+Users[/\\]+" + escaped + r"([^'\"\r\n]*)\1", re.I)
        text = quoted.sub(lambda m: "str(__import__('pathlib').Path.home()) + " + repr(m[2].replace("\\\\", "/").replace("\\", "/")), text)
    text = re.sub(r"[Cc]:[/\\]+Users[/\\]+" + escaped, "%USERPROFILE%", text, flags=re.I)
    text = re.sub(r"\b" + escaped + r"[\w.+-]*@[\w.-]+\b", "[account email omitted]", text, flags=re.I)
    text = re.sub(r"\b" + escaped + r"\s+Wright\b", "backup account (name omitted)", text, flags=re.I)
    text = re.sub(r"\b" + escaped + r"/Lisan\b", "Lisan", text, flags=re.I)
    # Retain public scholarly attribution using its conventional first initial.
    text = re.sub(r"\b" + escaped + r"(?=\s+(?:Hawking|Mumford)\b)", "S.", text, flags=re.I)
    text = re.sub(escaped, "Ziggy", text, flags=re.I)
    text = text.replace("Ziggy (Ziggy)", "Ziggy")
    if path.name == "offload_old_installer.ps1":
        text = text.replace("$sourceLiteral = '%USERPROFILE%\\AppData\\Local\\Temp\\stbc3hr1'", "$sourceLiteral = Join-Path $env:LOCALAPPDATA 'Temp\\stbc3hr1'")
        text = text.replace("$source -notlike '%USERPROFILE%\\AppData\\Local\\Temp\\*'", "$source -notlike (Join-Path $env:LOCALAPPDATA 'Temp\\*')")
    if path.as_posix().endswith("identity/grok_chief/I_AM.md"):
        newline = "\r\n" if "\r\n" in text else "\n"
        text += newline + newline + "Coordinator privacy note: local-profile references in this shared copy were made portable on October 10, 2026. The author's other words are retained. Earlier posting hashes describe the prior capture; see the shared privacy policy and redaction ledger." + newline
    return text


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--token", default=Path.home().name)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--backup-root", type=Path)
    parser.add_argument("--report", type=Path)
    args = parser.parse_args()
    if not args.token or len(args.token) < 3:
        raise SystemExit("Use an explicit nonempty profile token of at least three characters.")
    files = find_files(args.token)
    if not args.apply:
        print(json.dumps({"matchedTextFiles": len(files), "paths": [p.relative_to(ROOT).as_posix() for p in files]}, indent=2))
        return
    if not args.backup_root:
        raise SystemExit("An outside-repository backup directory is required.")
    backup = args.backup_root.resolve()
    if backup.is_relative_to(ROOT) or backup.exists():
        raise SystemExit("Choose a fresh backup folder outside the repository.")
    prepared = []
    for path in files:
        if not path.is_relative_to(ROOT):
            raise SystemExit("A match resolves outside the repository; nothing changed.")
        raw = path.read_bytes()
        text, encoding = decode(raw)
        updated = redact(text, args.token, path).encode(encoding)
        if re.search(re.escape(args.token), updated.decode(encoding), re.I):
            raise SystemExit("Redaction left a token match; nothing changed.")
        prepared.append((path, raw, updated))
    backup.mkdir(parents=True)
    for path, raw, _ in prepared:
        saved = backup / path.relative_to(ROOT)
        saved.parent.mkdir(parents=True, exist_ok=True)
        with saved.open("xb") as stream:
            stream.write(raw)
        if digest(saved.read_bytes()) != digest(raw):
            raise SystemExit("Original backup failed; no shared files changed.")
    records = []
    for path, raw, updated in prepared:
        if path.read_bytes() != raw:
            raise SystemExit("Concurrent source edit detected; remaining changes stopped.")
        temp = path.with_name(path.name + ".privacy." + str(uuid.uuid4()) + ".tmp")
        with temp.open("xb") as stream:
            stream.write(updated)
        temp.replace(path)  # Break hardlinks rather than editing another snapshot in place.
        records.append({"path": path.relative_to(ROOT).as_posix(), "priorSha256": digest(raw), "sharedSha256": digest(updated), "priorBytes": len(raw), "sharedBytes": len(updated)})
    report = {"format": "cfa-shared-privacy-redaction-v1", "createdUtc": datetime.now(timezone.utc).isoformat(), "tokenSha256": digest(args.token.casefold().encode()), "changedTextFiles": len(records), "records": records, "historyAndExternalBackupsChanged": False, "originalsPreservedOutsideRepository": True, "atomicWritesBreakHardlinks": True}
    target = args.report or backup / "redaction_ledger.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("x", encoding="utf-8") as stream:
        json.dump(report, stream, ensure_ascii=False, indent=2)
        stream.write("\n")
    (backup / "redaction_ledger.json").write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8") if target != backup / "redaction_ledger.json" else None
    print(json.dumps({"changedTextFiles": len(records), "ledger": str(target), "originals": str(backup)}))


if __name__ == "__main__":
    main()
