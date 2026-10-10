#!/usr/bin/env python3
"""Build immutable text-only collaborator context releases; verify with --check."""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sys
import uuid
import zipfile

PACK_ROOT = Path(__file__).resolve().parent
ROOT = next(p for p in PACK_ROOT.parents if (p / "AGENTS.md").is_file())
BASE = "docs/notes/explorable_world/comfy/projects/collaborators/"
IDS = ("nova", "grok_chief", "hal", "gemini_master", "gemini_chat", "gemini_studio", "flow", "deepseek", "qwen", "kimi", "claude")
PILOT = {"deepseek", "qwen", "kimi"}
CORE = ("01_CFA_PROJECT_CONTEXT.txt", "02_CURRENT_WORK_AND_REVIEW.txt", "03_COMMUNICATION_AND_IDENTITY_GUIDE.txt", "04_SHARED_WELCOME.md")
REVISION = "CFA-COLLABORATOR-CONTEXT-20261010-v1"

class BuildError(Exception):
    pass

def fail(msg):
    raise BuildError(msg)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def json_bytes(obj):
    return (json.dumps(obj, ensure_ascii=False, indent=2) + "\n").encode("utf-8")

def json_read(data, label):
    try:
        return json.loads(data.decode("utf-8-sig"))
    except (UnicodeError, ValueError):
        fail(f"Invalid JSON: {label}")

def relative(path):
    return Path(path).resolve().relative_to(ROOT).as_posix()

def path_for(name):
    if not isinstance(name, str) or not name or "\\" in name:
        fail("Paths must be repository-relative POSIX strings")
    p = PurePosixPath(name)
    if p.is_absolute() or any(x in (".", "..") for x in p.parts) or ":" in name:
        fail(f"Unsafe path: {name}")
    result = ROOT.joinpath(*p.parts)
    if not result.resolve().is_relative_to(ROOT):
        fail(f"Path escapes CFA: {name}")
    return result

def privacy(data, label):
    try:
        text = data.decode("utf-8-sig")
    except UnicodeError:
        fail(f"Non-text bytes rejected: {label}")
    if "\x00" in text:
        fail(f"Binary bytes rejected: {label}")
    token = Path.home().name.casefold()
    if token and token in text.casefold():
        fail(f"Privacy check failed: {label}; private token is not printed")
    return text

def source_read(name):
    p = path_for(name)
    if p.suffix.lower() not in {".md", ".txt", ".json", ".py"}:
        fail(f"Non-text source rejected: {name}")
    if any(x.lower() in {".git", ".aws", ".codex", ".env", "credentials"} for x in p.relative_to(ROOT).parts):
        fail(f"Credential/runtime source rejected: {name}")
    data = p.read_bytes()
    privacy(data, name)
    return data

def file_record(name, data):
    return {"path": name, "sha256": sha(data), "bytes": len(data)}

def capture():
    controls = [relative(PACK_ROOT / "source" / n) for n in ("recipient_contexts.json", "recipient_inputs.json", "shared_inputs.json", *CORE[:2])]
    data = {n: source_read(n) for n in controls}
    contexts = json_read(data[controls[0]], controls[0])
    audited = json_read(data[controls[1]], controls[1])
    shared = json_read(data[controls[2]], controls[2])
    if set(contexts) != set(IDS):
        fail("Context recipient IDs differ from the eleven canonical IDs")
    names = set(controls)
    names.add(relative(Path(__file__)))
    names.update(BASE + n for n in ("MAILBOX.md", "I_AM.md", "identity/registry.json", "mailbox/registry.json", "mailbox/templates/message.json", "mailbox/templates/receipt.json", "identity/I_AM_TEMPLATE.md"))
    for item in shared["sources"] + audited["sources"]:
        name = item if isinstance(item, str) else item.get("source")
        if not name:
            fail("Input manifest contains no source path")
        names.add(name)
    for rid, entry in contexts.items():
        if set(entry) != {"label", "identitySource", "route", "entryContext", "currentWork", "extraSources"}:
            fail(f"Unexpected context fields: {rid}")
        for key in ("label", "route", "entryContext", "currentWork"):
            if not isinstance(entry[key], str) or not entry[key].strip():
                fail(f"Missing {key}: {rid}")
        if entry["identitySource"]:
            names.add(entry["identitySource"])
        used = set()
        for extra in entry["extraSources"]:
            if set(extra) != {"source", "filename", "kind"} or extra["kind"] not in {"current", "dated_snapshot", "template"}:
                fail(f"Invalid extra: {rid}")
            name = extra["filename"]
            if not re.fullmatch(r"[A-Za-z0-9_.-]+", name) or name.startswith(".") or name in used or name in CORE:
                fail(f"Unsafe or duplicate filename: {rid}")
            used.add(name)
            names.add(extra["source"])
        if rid in PILOT:
            extras = entry["extraSources"]
            if len(extras) != 1 or extras[0]["source"] != BASE + "work_briefs_20261010/SHARED_PILOT.md" or extras[0]["filename"] != "07_PHASE0_ASSIGNMENT.md":
                fail(f"Phase 0 may receive only the assignment extra: {rid}")
    for name in sorted(names):
        if name not in data:
            data[name] = source_read(name)
    registry = json_read(data[BASE + "identity/registry.json"], "identity/registry.json")
    if not isinstance(registry.get("collaborators"), list):
        fail("Identity registry must contain the actual collaborators array")
    by_id = {item["id"]: item for item in registry["collaborators"]}
    warnings = []
    for rid, entry in contexts.items():
        source = entry["identitySource"]
        old = (by_id.get(rid, {}).get("currentIntroduction") or {}).get("source") or {}
        if source:
            if old.get("path") != source:
                fail(f"Canonical identity mapping mismatch: {rid}")
            if old.get("sha256") != sha(data[source]):
                warnings.append(f"{rid}: current source differs from historical registry hash; fresh dated copy preserved, registry/author text unchanged")
        elif old:
            fail(f"Identity incorrectly marked missing: {rid}")
    for item in audited["sources"]:
        if isinstance(item, dict) and item.get("sha256Observed") and item["sha256Observed"] != sha(data[item["source"]]):
            warnings.append(f"Source changed after audit, before capture: {item['source']}; actual fresh bytes recorded")
    return data, contexts, by_id, warnings

def sources_fresh(data):
    for name, original in data.items():
        if source_read(name) != original:
            fail(f"Source changed during packaging; publication aborted: {name}")

def status(entry, reg):
    if not entry["identitySource"]:
        return "missing_self_authored_introduction"
    intro = reg.get("currentIntroduction") or {}
    if "privacy" in intro.get("archiveStatus", ""):
        return "self_authored_privacy_normalized_snapshot"
    if "browser" in intro.get("authorship", ""):
        return "self_authored_browser_response_archived_snapshot"
    if "supplied_by_user" in intro.get("authorship", ""):
        return "self_authored_user_supplied_snapshot"
    return "self_authored_source_snapshot"

def communication(data):
    parts = [b"COMMUNICATION AND IDENTITY GUIDE\nCoordinator assembly of complete source texts. Source authorship/dates remain separate. Paths are metadata, not access or delivery.\n\n"]
    for title, name in (("FULL MAILBOX PROTOCOL", "MAILBOX.md"), ("ACTUAL RECIPIENT REGISTRY", "mailbox/registry.json"), ("MESSAGE TEMPLATE", "mailbox/templates/message.json"), ("RECEIPT TEMPLATE", "mailbox/templates/receipt.json"), ("INTRODUCTION TEMPLATE", "identity/I_AM_TEMPLATE.md")):
        source = BASE + name
        raw = data[source]
        parts += [(f"===== {title} =====\nSource: {source}\nSource SHA-256: {sha(raw)}; bytes: {len(raw)}\nBEGIN EXACT SOURCE TEXT\n").encode("utf-8"), raw, b"\nEND EXACT SOURCE TEXT\n\n"]
    return b"".join(parts)

def launch(rid, entry, release_id, prepared, order):
    lines = ["LOAD THIS COLLABORATOR PROJECT CONTEXT", f"Recipient: {entry['label']} ({rid})", f"Release: {release_id}; prepared UTC: {prepared}", "State: prepared_not_delivered", "", "Extract your ZIP first. ZIPs are transport; upload/paste actual extracted documents, not an archive as though it were project knowledge.", "In this collaborator's actual CFA project/workspace, add the documents using supported project-file/context controls. If project files are unsupported, supply actual text or supported attachments in the conversation. A local pathname alone is not delivery.", "", "EXACT LOAD ORDER"]
    lines += [f"{i:02d}. {name}" for i, name in enumerate(order, 1)]
    lines += ["", "RECIPIENT ENTRY CONTEXT", entry["entryContext"], "", "COPY-PASTE LAUNCH MESSAGE", f"Please load CFA context release {release_id} for canonical recipient {rid}. Read the attached documents in the listed order. State which actual files/text you received and read, identify your actual app/session and visible model (unknown if unavailable), and confirm your canonical mailbox ID. Explain the difference between asset likeness stars, scene readiness and collaborator role grades. Report missing text/media and tool limits. Read 06_YOUR_CURRENT_WORK.txt before starting any assignment. This context refresh itself starts no generation, installation, purchase or public release. Preserve your own authored I_AM; propose a dated refresh if needed rather than adopting another collaborator's identity. Return a concise readback and the next bounded step.", "", "REFRESH AND HANDOFF", "These are dated copies, not a live feed or proven persistent memory. Refresh after reviewed decisions, references, tasks or tools change; preserve previous identities and returns. At closing record actual completed work, IDs/hashes, decisions, blockers and next step. Mailbox files do not wake apps or prove delivery/readback. A courier archive retains author and actual operator attribution.", "", "SOURCE/LINK LIMITS", "Paths and links inside originals identify records; they are metadata until bytes are supplied or local access is actually verified. This text-only pack contains no media, credentials, graph execution or private cloud state. SOURCE_COPY_NOTE.txt and release MANIFEST.json identify source bytes and curator boundaries."]
    if rid in PILOT:
        lines += ["", "PHASE 0 INDEPENDENCE", "Only assignment text is supplied. Baseline JSON/graph bytes, extraction values, COMMON_REQUIREMENTS.md and peer results are deliberately omitted. Freeze your own independent result or honest limitation before courier help supplies bytes or performs the preflight. Delivering the assignment is separate from performing the preflight."]
    return ("\n".join(lines) + "\n").encode("utf-8")

def current_work(entry, release_id, prepared):
    return (f"YOUR CURRENT WORK - COORDINATOR CONTEXT\nRelease: {release_id}\nPrepared UTC: {prepared}\nState: prepared_not_delivered\n\n{entry['currentWork']}\n\nCurated dated wrapper, separate from authored I_AM. Source reports retain attribution; this does not independently verify runtime claims, approve masters, grant access or start jobs. Latest explicit task/verified evidence governs older source paragraphs.\n").encode("utf-8")

def copy_note(rid, entry, reg, data, prepared):
    lines = ["SOURCE COPY NOTE - COORDINATOR METADATA", f"Prepared UTC: {prepared}", f"Canonical recipient: {rid}", "This note is not the collaborator's authored introduction."]
    source = entry["identitySource"]
    if source:
        raw = data[source]
        intro = reg.get("currentIntroduction") or {}
        old = intro.get("source") or {}
        lines += [f"Identity source: {source}", f"Copied bytes: {len(raw)}", f"Copied SHA-256: {sha(raw)}", "05_YOUR_I_AM.md is byte-identical to that source, including original line endings.", f"Registry authorship: {intro.get('authorship', 'not recorded')}", f"Registry archive label: {intro.get('archiveStatus', 'not recorded')}", f"Registry source-hash match at capture: {sha(raw) == old.get('sha256')}", "Correct copy/hash proves bytes, not author tools, model, access, grades or historical open-item claims."]
        if sha(raw) != old.get("sha256"):
            lines += ["Registry describes an older capture. The fresh source hash governs this copy; registry and prior author text were not rewritten."]
    else:
        lines += ["No current self-authored introduction has been collected for this surface.", "05_YOUR_I_AM_TEMPLATE.txt is an explicitly unfilled coordinator-supplied template, not an authored persona or completed onboarding."]
    lines += ["Common/recipient summaries are curated by CFA/Nova. Source paths and hashes are in the manifest. Prepared documents/ZIPs do not prove upload, project installation, readback, persistent memory or automatic refresh."]
    return ("\n".join(lines) + "\n").encode("utf-8")

def exclusive(path, data):
    if not path.resolve().is_relative_to(PACK_ROOT.resolve()):
        fail("Generated output escapes pack root")
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as stream:
        stream.write(data)

def atomic(path, data):
    temp = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    try:
        exclusive(temp, data)
        os.replace(temp, path)
    finally:
        if temp.exists():
            temp.unlink()

def clean_stage(stage):
    stage = stage.resolve()
    if stage.parent != PACK_ROOT.resolve() or not stage.name.startswith(".building-") or not stage.is_relative_to(ROOT):
        fail("Refusing cleanup outside verified private staging")
    shutil.rmtree(stage)

def make_zip(path, entries, prepared):
    when = dt.datetime.fromisoformat(prepared.replace("Z", "+00:00"))
    stamp = (when.year, when.month, when.day, when.hour, when.minute, when.second)
    path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(path, "x", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for name, raw in sorted(entries.items()):
            pure = PurePosixPath(name)
            if pure.is_absolute() or ".." in pure.parts or "\\" in name:
                fail("Unsafe archive member")
            info = zipfile.ZipInfo(name, stamp)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, raw, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)

def check_zip(path, expected):
    with zipfile.ZipFile(path, "r") as archive:
        names = archive.namelist()
        if len(names) != len(set(names)) or set(names) != set(expected):
            fail(f"ZIP member-set mismatch: {relative(path)}")
        for name in names:
            if archive.read(name) != expected[name]:
                fail(f"ZIP member-byte mismatch: {name}")
        if archive.testzip() is not None:
            fail(f"ZIP CRC failure: {relative(path)}")

def upload_map(packs, release_id, prepared, prefix):
    lines = ["CFA COLLABORATOR PROJECT CONTEXT - HUMAN UPLOAD MAP", f"Release: {release_id}", f"Prepared UTC: {prepared}", "Status: prepared_not_delivered", "", f"All-pack transport ZIP: {prefix}/ALL_COLLABORATOR_PACKS.zip", "", "Extract ZIPs before loading documents. Each individual ZIP contains its recipient's flat document set. The all-pack ZIP includes common files, recipient folders, individual transport ZIPs and release manifest. No direct service ZIP import is claimed.", "For future collaborators, common/ is the default pack; start with its generic 00_LOAD_FIRST.txt, then add a self-authored identity and a bounded current-task supplement for that actual surface.", "", "Open the intended collaborator's CFA project/workspace. Use its 00 launch guide, load documents in the exact sequence below through supported project-file controls, or paste/attach actual text if project files are unsupported. Paths alone are not delivery. Paste the guide's launch message; ask for received/read filenames, canonical recipient, actual surface/model, missing inputs and evidence limits. Record actual delivery/readback separately.", "Refresh dated context after reviewed decisions, reference/task/tool changes and measured returns. Preserve historical identities. Text does not supply visual references; attach exact scoped media separately for a bounded visual assignment."]
    for pack in packs:
        lines += ["", f"{pack['label']} - {pack['recipientID']}", f"Route: {pack['route']}", f"Folder: {pack['folderPath']}", f"ZIP: {pack['zipPath']}", f"Launch: {pack['loadGuidePath']}", f"Identity: {pack['identityStatus']}", "Exact load order:"]
        lines += [f"  {i:02d}. {name}" for i, name in enumerate(pack["loadOrder"], 1)]
    lines += ["", "Prepared/supplied/received/read/visually inspected/accepted/persistent project context are separate evidence states. No delivery follows from ZIP creation. Closed sessions watch nothing. Phase 0 packs contain assignment text only; do not supply baseline bytes or perform a preflight through a courier before independent results freeze."]
    return ("\n".join(lines) + "\n").encode("utf-8")

def generic_launch(release_id, prepared):
    return (f"CFA COMMON DEFAULT PACK FOR FUTURE COLLABORATORS\nRelease: {release_id}\nPrepared UTC: {prepared}\nStatus: prepared_not_delivered\n\nRead 01_CFA_PROJECT_CONTEXT.txt, 02_CURRENT_WORK_AND_REVIEW.txt, 03_COMMUNICATION_AND_IDENTITY_GUIDE.txt, and 04_SHARED_WELCOME.md in that order. Supply actual texts/attachments to the actual project/chat; ZIPs are transport, not knowledge imports. Name what you actually received/read, your actual app/session/model (unknown if unavailable), current tools/limits and the canonical recipient ID assigned for your surface. Do not borrow an existing identity. Use the included introduction template to author your own I_AM when requested. A courier may archive your exact words with attribution. Add one dated current-task supplement before beginning bounded work. No automatic generation, app wake, background sync, spending or public release follows from this context. Preserve source evidence, separate asset/scene/role grades, refresh after reviewed changes, and leave closing notes. Local paths/links are metadata until bytes are supplied or actual access is verified. No visual media or credentials are supplied.\n").encode("utf-8")

def attributes_ok(raw):
    return [line.strip() for line in raw.decode("utf-8-sig").splitlines() if line.strip() and not line.lstrip().startswith("#")] == ["* -text"]

def build():
    attrs = PACK_ROOT / ".gitattributes"
    if attrs.exists() and not attributes_ok(attrs.read_bytes()):
        fail("Unexpected byte-preservation attributes; refusing overwrite")
    data, contexts, registry, warnings = capture()
    sources = [file_record(n, raw) for n, raw in sorted(data.items())]
    digest = sha(json_bytes({"format": REVISION, "sourceFiles": sources}))
    now = dt.datetime.now(dt.timezone.utc)
    rid = now.strftime("%Y%m%d") + "-" + digest[:12]
    releases = PACK_ROOT / "releases"
    if not releases.resolve().is_relative_to(ROOT):
        fail("Release directory escapes checkout")
    releases.mkdir(exist_ok=True)
    final = releases / rid
    if final.exists():
        prior = json_read((final / "MANIFEST.json").read_bytes(), "existing manifest")
        if prior.get("inputDigest") != digest:
            fail("Content-address collision or altered immutable release")
        prepared = prior["preparedAtUTC"]
    else:
        prepared = now.isoformat(timespec="seconds").replace("+00:00", "Z")
    prefix = relative(final)
    # Inherit project ACLs on Windows; mkdtemp mode 0700 makes the final release private.
    stage = PACK_ROOT / (".building-" + str(uuid.uuid4()))
    if not stage.resolve().is_relative_to(PACK_ROOT.resolve()):
        fail("Build stage escapes context-pack root")
    stage.mkdir(mode=0o777, exist_ok=False)
    payload, packs, identities = {}, [], []
    try:
        common = {CORE[0]: data[relative(PACK_ROOT / "source" / CORE[0])], CORE[1]: data[relative(PACK_ROOT / "source" / CORE[1])], CORE[2]: communication(data), CORE[3]: data[BASE + "I_AM.md"]}
        for name, raw in common.items():
            payload["common/" + name] = raw
        payload["common/00_LOAD_FIRST.txt"] = generic_launch(rid, prepared)
        for recipient in IDS:
            entry = contexts[recipient]
            reg = registry.get(recipient, {})
            source = entry["identitySource"]
            iam_name = "05_YOUR_I_AM.md" if source else "05_YOUR_I_AM_TEMPLATE.txt"
            iam = data[source] if source else (f"UNFILLED ARRIVAL TEMPLATE - NOT A SELF-AUTHORED INTRODUCTION\nCanonical recipient: {recipient}\nNo current introduction has been collected for this surface.\nCoordinator supplied this template; fill placeholders in your own voice when asked.\n\n".encode("utf-8") + data[BASE + "identity/I_AM_TEMPLATE.md"])
            files = {**common, iam_name: iam, "06_YOUR_CURRENT_WORK.txt": current_work(entry, rid, prepared), "SOURCE_COPY_NOTE.txt": copy_note(recipient, entry, reg, data, prepared)}
            extra_records = []
            for extra in entry["extraSources"]:
                if extra["filename"] in files:
                    fail(f"Extra/core filename collision: {recipient}")
                files[extra["filename"]] = data[extra["source"]]
                extra_records.append({**extra, **file_record(extra["source"], data[extra["source"]])})
            order = ["00_LOAD_FIRST.txt", *CORE, iam_name, "06_YOUR_CURRENT_WORK.txt", *[e["filename"] for e in entry["extraSources"]], "SOURCE_COPY_NOTE.txt"]
            files["00_LOAD_FIRST.txt"] = launch(recipient, entry, rid, prepared, order)
            for name, raw in files.items():
                privacy(raw, f"{recipient}/{name}")
                payload[f"packs/{recipient}/{name}"] = raw
            packs.append({"recipientID": recipient, "label": entry["label"], "route": entry["route"], "folderPath": f"{prefix}/packs/{recipient}", "loadGuidePath": f"{prefix}/packs/{recipient}/00_LOAD_FIRST.txt", "zipPath": f"{prefix}/zips/{recipient}.zip", "identityStatus": status(entry, reg), "loadOrder": order, "fileCount": len(files), "bytes": sum(map(len, files.values()))})
            identities.append({"recipientID": recipient, "status": status(entry, reg), "identitySource": source, "copiedPath": f"{prefix}/packs/{recipient}/{iam_name}", "sha256": sha(iam), "bytes": len(iam), "byteExactSourceCopy": bool(source), "sourceSHA256": sha(data[source]) if source else None, "registryAuthorship": (reg.get("currentIntroduction") or {}).get("authorship"), "registrySource": (reg.get("currentIntroduction") or {}).get("source"), "extraSources": extra_records, "claimBoundary": "Exact bytes verified; runtime/model/tool claims remain attributed, missing identities use unfilled coordinator templates"})
        mapping = upload_map(packs, rid, prepared, prefix)
        payload["UPLOAD_MAP.txt"] = mapping
        for name, raw in sorted(payload.items()):
            exclusive(stage / name, raw)
        for pack in packs:
            recipient = pack["recipientID"]
            members = {PurePosixPath(n).name: raw for n, raw in payload.items() if n.startswith(f"packs/{recipient}/")}
            path = stage / "zips" / f"{recipient}.zip"
            make_zip(path, members, prepared)
            check_zip(path, members)
            payload[f"zips/{recipient}.zip"] = path.read_bytes()
        files = [file_record(f"{prefix}/{n}", raw) for n, raw in sorted(payload.items())]
        manifest = {"schemaVersion": 1, "formatRevision": REVISION, "releaseID": rid, "preparedAtUTC": prepared, "status": "prepared_not_delivered", "inputDigest": digest, "releaseAddressMeaning": "SHA-256 of builder revision and exact captured source hashes; releases immutable", "sourceFiles": sources, "files": files, "packs": packs, "identityCopies": identities, "sourceWarnings": warnings, "snapshotBoundary": "Curated wrappers are distinct from authored identities. Source paths in texts are metadata until bytes/access supplied. Text-only preparation proves no upload, readback, persistent memory, generation or acceptance.", "archiveBoundary": "Manifest excludes its own hash, index.json and ALL_COLLABORATOR_PACKS.zip to avoid circular hashes. All-pack archive includes the manifest and explicit release payload. Index adds manifest/archive hashes afterward."}
        manifest_raw = json_bytes(manifest)
        privacy(manifest_raw, "MANIFEST.json")
        exclusive(stage / "MANIFEST.json", manifest_raw)
        all_members = {**payload, "MANIFEST.json": manifest_raw}
        archive = stage / "ALL_COLLABORATOR_PACKS.zip"
        make_zip(archive, all_members, prepared)
        check_zip(archive, all_members)
        sources_fresh(data)
        if final.exists():
            for name, raw in all_members.items():
                if (final / name).read_bytes() != raw:
                    fail(f"Immutable release differs: {name}")
            if (final / "ALL_COLLABORATOR_PACKS.zip").read_bytes() != archive.read_bytes():
                fail("Immutable all-pack ZIP differs")
            clean_stage(stage)
            stage = None
        else:
            stage.rename(final)
            stage = None
        sources_fresh(data)
        exposed = [*files, file_record(f"{prefix}/MANIFEST.json", manifest_raw), file_record(f"{prefix}/ALL_COLLABORATOR_PACKS.zip", (final / "ALL_COLLABORATOR_PACKS.zip").read_bytes()), file_record(relative(PACK_ROOT / "UPLOAD_MAP.txt"), mapping)]
        index = {"schemaVersion": 1, "releaseID": rid, "preparedAtUTC": prepared, "status": "prepared_not_delivered", "uploadMapPath": f"{prefix}/UPLOAD_MAP.txt", "allPacksZipPath": f"{prefix}/ALL_COLLABORATOR_PACKS.zip", "packs": packs, "files": exposed, "manifestPath": f"{prefix}/MANIFEST.json", "sourceWarnings": warnings}
        attrs = PACK_ROOT / ".gitattributes"
        if attrs.exists() and not attributes_ok(attrs.read_bytes()):
            fail("Unexpected byte-preservation attributes; refusing overwrite")
        if not attrs.exists():
            exclusive(attrs, b"* -text\n")
        atomic(PACK_ROOT / "UPLOAD_MAP.txt", mapping)
        atomic(PACK_ROOT / "index.json", json_bytes(index))
        check()
        print(f"Prepared {rid}: {len(packs)} packs; {len(sources)} sources; {len(exposed)} exposed files; {sum(p['bytes'] for p in packs)} recipient-text bytes")
        for warning in warnings:
            print("Source warning: " + warning)
    finally:
        if stage is not None and stage.exists():
            clean_stage(stage)

def check():
    ip = PACK_ROOT / "index.json"
    index = json_read(ip.read_bytes(), "index.json")
    privacy(ip.read_bytes(), "index.json")
    if index.get("schemaVersion") != 1 or index.get("status") != "prepared_not_delivered" or not re.fullmatch(r"\d{8}-[0-9a-f]{12}", index.get("releaseID", "")):
        fail("Invalid index state/release ID")
    packs = index["packs"]
    if len(packs) != len(IDS) or {p["recipientID"] for p in packs} != set(IDS):
        fail("Index must expose exactly eleven canonical packs")
    records = index["files"]
    if len(records) != len({r["path"] for r in records}):
        fail("Duplicate exposed paths")
    actual = {}
    for item in records:
        path = path_for(item["path"])
        raw = path.read_bytes()
        if sha(raw) != item["sha256"] or len(raw) != item["bytes"]:
            fail(f"Exposed hash/size mismatch: {item['path']}")
        if path.suffix != ".zip":
            privacy(raw, item["path"])
        actual[item["path"]] = raw
    required = {index["uploadMapPath"], index["allPacksZipPath"], index["manifestPath"], relative(PACK_ROOT / "UPLOAD_MAP.txt")}
    for pack in packs:
        required.update((pack["loadGuidePath"], pack["zipPath"]))
        members = {n: actual[f"{pack['folderPath']}/{n}"] for n in pack["loadOrder"]}
        folder = path_for(pack["folderPath"])
        if set(p.name for p in folder.iterdir() if p.is_file()) != set(pack["loadOrder"]):
            fail(f"Folder/load-order mismatch: {pack['recipientID']}")
        if len(members) != pack["fileCount"] or sum(map(len, members.values())) != pack["bytes"]:
            fail(f"Pack counts mismatch: {pack['recipientID']}")
        check_zip(path_for(pack["zipPath"]), members)
    if not required.issubset(actual):
        fail("Exposed link missing hash record")
    manifest = json_read(actual[index["manifestPath"]], "manifest")
    if manifest["releaseID"] != index["releaseID"] or manifest["packs"] != packs or manifest["preparedAtUTC"] != index["preparedAtUTC"]:
        fail("Manifest/index mismatch")
    sources = {i["path"]: source_read(i["path"]) for i in manifest["sourceFiles"]}
    for item in manifest["sourceFiles"]:
        raw = sources[item["path"]]
        if sha(raw) != item["sha256"] or len(raw) != item["bytes"]:
            fail(f"Source freshness mismatch: {item['path']}; prepare a new release")
    digest = sha(json_bytes({"format": REVISION, "sourceFiles": manifest["sourceFiles"]}))
    if digest != manifest["inputDigest"] or not index["releaseID"].endswith(digest[:12]):
        fail("Content address/source digest mismatch")
    for item in manifest["identityCopies"]:
        if item["identitySource"] and (actual[item["copiedPath"]] != sources[item["identitySource"]] or sha(actual[item["copiedPath"]]) != item["sourceSHA256"]):
            fail(f"Authored I_AM copy differs: {item['recipientID']}")
    prefix = relative(path_for(index["manifestPath"]).parent)
    all_members = {i["path"][len(prefix) + 1:]: actual[i["path"]] for i in manifest["files"]}
    all_members["MANIFEST.json"] = actual[index["manifestPath"]]
    check_zip(path_for(index["allPacksZipPath"]), all_members)
    core = {CORE[0]: sources[relative(PACK_ROOT / "source" / CORE[0])], CORE[1]: sources[relative(PACK_ROOT / "source" / CORE[1])], CORE[2]: communication(sources), CORE[3]: sources[BASE + "I_AM.md"]}
    for pack in packs:
        for name, raw in core.items():
            if actual[f"{pack['folderPath']}/{name}"] != raw:
                fail(f"Common snapshot differs: {pack['recipientID']}/{name}")
    contexts = json_read(sources[relative(PACK_ROOT / "source" / "recipient_contexts.json")], "captured contexts")
    for recipient in PILOT:
        pack = next(p for p in packs if p["recipientID"] == recipient)
        permitted = {"00_LOAD_FIRST.txt", *CORE, "05_YOUR_I_AM.md", "06_YOUR_CURRENT_WORK.txt", "SOURCE_COPY_NOTE.txt", "07_PHASE0_ASSIGNMENT.md"}
        if set(pack["loadOrder"]) != permitted or len(contexts[recipient]["extraSources"]) != 1:
            fail(f"Unexpected payload in independent Phase 0 pack: {recipient}")
        source = BASE + "work_briefs_20261010/SHARED_PILOT.md"
        if actual[f"{pack['folderPath']}/07_PHASE0_ASSIGNMENT.md"] != sources[source]:
            fail(f"Phase 0 assignment copy differs: {recipient}")
    attrs = (PACK_ROOT / ".gitattributes").read_bytes()
    if not attributes_ok(attrs):
        fail("Byte-preservation attributes missing")
    sources_fresh(sources)
    print(f"Check passed: {index['releaseID']}; {len(packs)} packs; {len(records)} file hashes; exact identities/ZIP bytes; privacy; fresh sources")
    return index

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Verify current release, exact identity/ZIP bytes, privacy and live source freshness without writing")
    args = parser.parse_args()
    try:
        check() if args.check else build()
    except (BuildError, OSError, KeyError, zipfile.BadZipFile) as exc:
        print("Pack build/check failed: " + str(exc), file=sys.stderr)
        return 1
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

