"""Seal received TCM background and set archives for read-only site review.

This is an intake preparation tool, not a creative decision maker.  It
validates every archive member, extracts the preserved archive contents to
their existing intake lane, and writes factual receipts with every human
decision field left empty/false.  Re-running is idempotent: existing files
must match the archive bytes exactly.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import re
import stat
import zipfile
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath

from PIL import Image


HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[5]
PROJECT = "criminal_mind"
CONTROLLER = "baldadoon"
CAST_TASK = "tcm-grok-casting-20261030"
SET_TASK = "tcm-grok-sets-20261030"
CAST_HOME = Path("docs/notes/explorable_world/comfy/references/From Grok/GROK-TCM-CASTING_v001/intake")
SET_HOME = Path("docs/notes/explorable_world/comfy/references/From Grok/GROK-TCM-SETS_v001/intake")
CAST_ROSTER = Path("docs/notes/explorable_world/comfy/projects/the_criminal_mind/handoffs/grok_casting_and_sets_20261030/CASTING_ROSTER_v001.json")
SET_ROSTER = Path("docs/notes/explorable_world/comfy/projects/the_criminal_mind/handoffs/grok_casting_and_sets_20261030/SET_ROSTER_v001.json")
BACKGROUND_AGGREGATE = CAST_HOME / "CFA_CASTING_INTAKE_019-034_SITE_INDEX_v003.json"
SET_AGGREGATE = SET_HOME / "CFA_SET_INTAKE_035-118_SITE_INDEX_v003.json"
BASELINE_CATALOG = Path("docs/notes/explorable_world/comfy/projects/visual_library/catalog.js")


def digest(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def repo_path(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def json_bytes(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def write_verified(path: Path, raw: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        if path.read_bytes() != raw:
            raise ValueError(f"Existing frozen receipt differs; version it instead of overwriting: {path}")
        return
    path.write_bytes(raw)


def safe_member(info: zipfile.ZipInfo) -> PurePosixPath:
    member = PurePosixPath(info.filename.replace("\\", "/"))
    if member.is_absolute() or not member.parts or ".." in member.parts or "." in member.parts:
        raise ValueError(f"Unsafe archive path: {info.filename}")
    if any(":" in part for part in member.parts) or info.flag_bits & 0x1:
        raise ValueError(f"Drive-qualified or encrypted archive member: {info.filename}")
    mode = info.external_attr >> 16
    if mode and stat.S_ISLNK(mode):
        raise ValueError(f"Archive symlink is not allowed: {info.filename}")
    return member


def table_rows(raw: bytes) -> list[dict[str, str]]:
    text = raw.decode("utf-8-sig", errors="replace").replace("\x00", "")
    fields = None
    rows = []
    for line in text.splitlines():
        if not line or line.startswith("#") or "\t" not in line:
            continue
        values = [value.strip() for value in line.split("\t")]
        lowered = [value.lower() for value in values]
        is_header = (("candidate_id" in lowered or "candidateid" in lowered) and
                     ("filename" in lowered or "sha256" in lowered))
        is_header = is_header or (("zip" in lowered or "filename" in lowered) and "sha256" in lowered and
                                  any(key in lowered for key in ("original_count", "still_count", "extra_count", "member_count")))
        if is_header:
            fields = values
            continue
        if fields is None or len(values) != len(fields):
            continue
        rows.append(dict(zip(fields, values)))
    return rows


def row_id(row: dict[str, str]) -> str:
    return row.get("candidate_id") or row.get("candidateID") or row.get("candidate") or ""


def row_sha(row: dict[str, str]) -> str:
    value = row.get("sha256") or row.get("hash") or ""
    match = re.search(r"[0-9a-fA-F]{64}", value)
    return match.group(0).lower() if match else ""


def version_score(name: str) -> tuple[int, int, str]:
    versions = [int(value) for value in re.findall(r"(?:^|[_-])v(\d+)(?:\D|$)", name, re.I)]
    return (10000 if "SCREENING_ROWS" in name.upper() else 0,
            max(versions, default=0), name)


def maker_score(name: str) -> tuple[int, int, str]:
    upper = name.upper()
    return (100 if "MAKER_" in upper else (50 if "HANDOFF" in upper else 0),
            -100 if "DERIVED" in upper else 0, name)


def source_values(value: str) -> list[str]:
    return [part.strip() for part in re.split(r"\s*[;,|]\s*", value or "") if part.strip()]


def image_size(raw: bytes) -> tuple[int, int]:
    with Image.open(io.BytesIO(raw)) as image:
        image.verify()
    with Image.open(io.BytesIO(raw)) as image:
        return image.size


def later_family(candidate_id: str) -> str:
    value = candidate_id
    if value.startswith("TCMSET_B3_"):
        value = value[len("TCMSET_B3_"):]
    if not value.startswith("TCM-SET-"):
        value = "TCM-SET-" + value
    match = re.match(r"^(.*?)(?:-(?:L|X)\d+|-(?:ID)\d+|_(?:L|X)\d+)(?:__|$)", value, re.I)
    if not match:
        raise ValueError(f"Cannot determine set family for {candidate_id}")
    return match.group(1).upper()


def candidate_members(lane: str, archive: Path, members: dict[str, bytes]) -> list[str]:
    images = []
    for name in members:
        base = PurePosixPath(name).name
        if not base.lower().endswith((".jpg", ".jpeg")):
            continue
        if lane == "background" and base.startswith("TCM-BG-"):
            images.append(name)
        elif lane == "base_set" and base.startswith("TCM-SET-"):
            images.append(name)
        elif lane == "set_round" and (base.startswith("TCM-SET-") or base.startswith("TCMSET_")):
            images.append(name)
    expected = 3 if lane == "background" else (10 if lane == "base_set" else None)
    if expected is not None and len(images) != expected:
        raise ValueError(f"{archive.name}: expected {expected} originals, found {len(images)}")
    return sorted(images, key=lambda value: PurePosixPath(value).name)


def evidence_for(candidate_id: str, filename: str, sha256: str, byte_count: int,
                 tables: list[tuple[str, bytes, list[dict[str, str]]]]) -> dict:
    matches: list[tuple[tuple[int, int, str], str, bytes, dict[str, str]]] = []
    maker: list[tuple[tuple[int, int, str], str, bytes, dict[str, str]]] = []
    indexed = False
    for name, raw, rows in tables:
        for row in rows:
            if row_id(row) != candidate_id and Path(row.get("filename", "")).name != filename:
                continue
            declared = row_sha(row)
            if declared and declared != sha256:
                raise ValueError(f"Screening/index hash mismatch for {candidate_id} in {name}")
            declared_bytes = row.get("bytes", "")
            if declared_bytes and declared_bytes.isdigit() and int(declared_bytes) != byte_count:
                raise ValueError(f"Screening/index byte-count mismatch for {candidate_id} in {name}")
            if declared and declared_bytes.isdigit() and int(declared_bytes) == byte_count:
                indexed = True
            if row.get("tag"):
                matches.append((version_score(name), name, raw, row))
            if any(row.get(key) for key in ("look_note", "source_vs_grok_proposal", "source_vs_grok_note",
                                            "defects", "position", "position_id", "light_state", "serves_shots")):
                maker.append((maker_score(name), name, raw, row))
    screening = None
    if matches:
        _, name, raw, row = max(matches, key=lambda item: item[0])
        screening = {
            "tag": row.get("tag") or None,
            "hardTrait": row.get("hard_trait_cited") or None,
            "note": row.get("note") or None,
            "cardVersion": row.get("card_version") or None,
            "judgedAgainst": row.get("judged_against") or None,
            "sourceMember": name,
            "sourceSHA256": digest(raw),
            "isHumanVerdict": False,
        }
    proposal = None
    metadata = None
    if maker:
        _, name, raw, row = max(maker, key=lambda item: item[0])
        proposal = {
            "lookNote": row.get("look_note") or None,
            "sourceVsProposal": row.get("source_vs_grok_proposal") or row.get("source_vs_grok_note") or None,
            "defectNote": row.get("defects") or None,
            "sourceMember": name,
            "sourceSHA256": digest(raw),
        }
        provider_id = row_id(row) or None
        position = row.get("position") or row.get("position_id") or None
        light_state = row.get("light_state") or None
        metadata = {
            "providerCandidateID": provider_id,
            "cameraPositionID": position,
            "lightState": light_state,
            "variant": row.get("variant") or None,
            "variantOf": row.get("variantOf") or row.get("variant_of") or None,
            "carID": row.get("car_id") or None,
            "referenceIDs": source_values(row.get("reference_ids") or ""),
            "servesShotsRaw": row.get("serves_shots") or row.get("serves") or None,
            "servesShotsSourcePresent": "serves_shots" in row or "serves" in row,
            "servesShotIDs": re.findall(r"TCM-\d{2}-\d{2}[A-Z]?", row.get("serves_shots") or row.get("serves") or ""),
            "shotsIDsSourceDetail": source_values(row.get("shots_ids") or ""),
            "sourceMember": name,
            "sourceSHA256": digest(raw),
            "isMakerSupplied": "MAKER_" in name.upper() and "DERIVED" not in name.upper(),
        }
    return {"indexedBytesAndHashes": indexed, "screening": screening,
            "providerProposal": proposal, "providerMetadata": metadata}


def extract_and_receipt(archive: Path, home: Path, lane: str, verified_at: str,
                        background: dict[str, dict], locations: dict[str, dict],
                        required_aggregate: Path) -> tuple[dict, dict, bytes, Path]:
    archive_raw = archive.read_bytes()
    members: dict[str, bytes] = {}
    with zipfile.ZipFile(io.BytesIO(archive_raw)) as zipped:
        bad = zipped.testzip()
        if bad:
            raise ValueError(f"CRC failure in {archive.name}: {bad}")
        for info in zipped.infolist():
            member = safe_member(info)
            if info.is_dir():
                continue
            raw = zipped.read(info)
            members[member.as_posix()] = raw
            target = (home / Path(*member.parts)).resolve()
            if not target.is_relative_to(home.resolve()):
                raise ValueError(f"Archive extraction escaped the intake lane: {info.filename}")
            if target.exists() and target.read_bytes() != raw:
                raise ValueError(f"Existing extracted file differs from archive: {target}")
            if not target.exists():
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(raw)
    tables = [(name, raw, table_rows(raw)) for name, raw in members.items()
              if name.lower().endswith(".tsv")]
    assets = []
    for member_name in candidate_members(lane, archive, members):
        raw = members[member_name]
        filename = PurePosixPath(member_name).name
        candidate_id = Path(filename).stem
        sha256 = digest(raw)
        width, height = image_size(raw)
        target = home / Path(*PurePosixPath(member_name).parts)
        evidence = evidence_for(candidate_id, filename, sha256, len(raw), tables)
        row = {
            "candidateID": candidate_id,
            "project": PROJECT,
            "lane": lane,
            "role": "background_casting_option" if lane == "background" else
                    ("set_design_option" if lane == "base_set" else "set_camera_option"),
            "path": str(target.resolve()),
            "repoPath": repo_path(target),
            "archivePath": repo_path(archive),
            "archiveMember": member_name,
            "sha256": sha256,
            "bytes": len(raw),
            "width": width,
            "height": height,
            "provider": "Grok",
            "stage": "preliminary",
            "reviewControllerID": CONTROLLER,
            "selected": False,
            "humanReview": None,
            "providerScreening": evidence["screening"],
            "providerProposal": evidence["providerProposal"],
            "providerMetadata": evidence["providerMetadata"],
            "indexedBytesAndHashes": evidence["indexedBytesAndHashes"],
        }
        if lane == "background":
            family = candidate_id.rsplit("-C", 1)[0]
            source = background[family]
            row.update(castingGroupID=family, character=source["name"],
                       sourceScenes=source["sourceScenes"], roleContext=source["context"])
        else:
            family = (candidate_id.rsplit("-L", 1)[0] if lane == "base_set" else later_family(candidate_id))
            row["locationFamilyID"] = family
            metadata = evidence["providerMetadata"] or {}
            row["providerCandidateID"] = metadata.get("providerCandidateID")
            row["candidateIDSource"] = "filename_stem_with_provider_mapping"
            row["providerServesShotIDs"] = metadata.get("servesShotIDs", [])
            row["bindingPolicy"] = ("identity_sheet_never_bound" if metadata.get("carID") else
                                    "family_context_only_no_shot_binding_by_intake") if lane == "set_round" else \
                                   "base_look_family_eligibility_only"
            if family in locations:
                source = locations[family]
                row.update(sourceScenes=source["sourceScenes"],
                           eligibleShotIDs=source["linkedShotIDs"] if lane == "base_set" else [],
                           locationTitle=source["title"], sourceConstraints=source["constraints"])
            else:
                row.update(sourceScenes=[], eligibleShotIDs=[], locationTitle=family.removeprefix("TCM-SET-").replace("-", " ").title(),
                           sourceConstraints="Family added by the dated set-camera maps; shot-level binding remains separate.")
        assets.append(row)
    batch_id = archive.stem
    receipt_path = home / batch_id / "CFA_INTAKE_RECEIPT_v003.json"
    prior = json.loads(receipt_path.read_text(encoding="utf-8")) if receipt_path.exists() else {}
    receipt_verified_at = prior.get("verifiedAtUTC", verified_at)
    receipt = {
        "format": "cfa-grok-casting-intake-v1" if lane == "background" else "cfa-grok-image-intake-v1",
        "project": PROJECT,
        "batchID": batch_id,
        "lane": lane,
        "taskID": CAST_TASK if lane == "background" else SET_TASK,
        "intakeRole": "site_index_receipt",
        "sealStatus": "complete_only_when_pinned_by_required_aggregate",
        "requiredAggregatePath": required_aggregate.as_posix(),
        "supersedesReceipt": (home.relative_to(ROOT) / batch_id / "CFA_INTAKE_RECEIPT_v002.json").as_posix(),
        "verifiedAtUTC": receipt_verified_at,
        "receivedAtUTC": None,
        "receivedTimeStatus": "not_recorded_in_archive",
        "archivePath": repo_path(archive),
        "archiveSHA256": digest(archive_raw),
        "archiveBytes": len(archive_raw),
        "archiveMemberCount": len(members),
        "receivedOriginals": len(assets),
        "acceptedOriginals": 0,
        "humanVerdictsCreated": 0,
        "selectedStartingFrames": 0,
        "assets": assets,
        "verification": {
            "zipCRC": True,
            "archiveHash": True,
            "safeMemberPaths": True,
            "noSymlinks": True,
            "noEncryptedMembers": True,
            "uniqueCandidateIDs": len({row["candidateID"] for row in assets}) == len(assets),
            "indexedBytesAndHashes": all(row["indexedBytesAndHashes"] for row in assets),
            "JPEGDecode": True,
            "humanReviewOrAcceptanceCreated": False,
        },
        "note": "Technical receipt for unreviewed originals. It is a completed site intake only when its exact hash is pinned by the required lane aggregate. Provider/V-team screening remains attributed preliminary evidence, never a human verdict or acceptance.",
    }
    raw = json_bytes(receipt)
    record = {
        "batchID": batch_id,
        "lane": lane,
        "receiptPath": repo_path(receipt_path),
        "receiptSHA256": digest(raw),
        "receiptBytes": len(raw),
        "archivePath": repo_path(archive),
        "archiveSHA256": receipt["archiveSHA256"],
        "archiveBytes": receipt["archiveBytes"],
        "archiveMemberCount": receipt["archiveMemberCount"],
        "receivedOriginals": len(assets),
    }
    return record, receipt, raw, receipt_path


def manifest_archives(set_home: Path) -> dict[str, dict]:
    declared: dict[str, dict] = {}
    for path in sorted(set_home.glob("BATCH_*MANIFEST_v001.tsv")):
        for row in table_rows(path.read_bytes()):
            name = row.get("zip") or row.get("filename") or ""
            if not name.lower().endswith(".zip"):
                continue
            item = {
                "manifestPath": repo_path(path),
                "manifestSHA256": digest(path.read_bytes()),
                "bytes": int(row["bytes"]),
                "sha256": row["sha256"].lower(),
                "originals": int(row.get("original_count") or row.get("still_count") or row.get("extra_count") or 0),
            }
            if name in declared and declared[name] != item:
                raise ValueError(f"Conflicting set archive manifest rows: {name}")
            declared[name] = item
    return declared


def seal(verified_at: str) -> dict:
    cast_home = ROOT / CAST_HOME
    set_home = ROOT / SET_HOME
    cast_roster_raw = (ROOT / CAST_ROSTER).read_bytes()
    set_roster_raw = (ROOT / SET_ROSTER).read_bytes()
    cast_roster = json.loads(cast_roster_raw)
    set_roster = json.loads(set_roster_raw)
    if cast_roster["project"] != PROJECT or set_roster["project"] != PROJECT:
        raise ValueError("Unexpected TCM roster project")
    background = {row["groupID"]: row for row in cast_roster["background"]}
    locations = {row["locationFamilyID"]: row for row in set_roster["locations"]}

    background_archives = sorted(cast_home.glob("TCM-INTAKE-BATCH-0*_BG-*_v001.zip"))
    base_archives = sorted(path for path in set_home.glob("TCM-INTAKE-BATCH-0*_SET-*_v001.zip")
                           if 35 <= int(path.name.split("-BATCH-")[1].split("_")[0]) <= 53)
    round_archives = sorted(path for path in set_home.glob("*.zip")
                            if not path.name.startswith("TCM-INTAKE-BATCH-"))
    if (len(background_archives), len(base_archives), len(round_archives)) != (16, 19, 65):
        raise ValueError("Unexpected archive lane counts")

    manifest = manifest_archives(set_home)
    if set(path.name for path in round_archives) != set(manifest):
        raise ValueError("Later set archives do not match the 48 frozen batch manifests")
    for archive in round_archives:
        row = manifest[archive.name]
        raw = archive.read_bytes()
        if len(raw) != row["bytes"] or digest(raw) != row["sha256"]:
            raise ValueError(f"Later set archive changed: {archive.name}")

    background_receipts, background_assets, pending_receipts = [], [], []
    for archive in background_archives:
        record, receipt, raw, receipt_path = extract_and_receipt(
            archive, cast_home, "background", verified_at, background, locations, BACKGROUND_AGGREGATE)
        background_receipts.append(record)
        background_assets.extend(receipt["assets"])
        pending_receipts.append((receipt_path, raw))
    expected_background = {candidate for row in background.values() for candidate in row["candidateIDs"]}
    if {row["candidateID"] for row in background_assets} != expected_background:
        raise ValueError("Background originals do not match the casting roster")

    set_receipts, set_assets = [], []
    for archive in base_archives:
        record, receipt, raw, receipt_path = extract_and_receipt(
            archive, set_home, "base_set", verified_at, background, locations, SET_AGGREGATE)
        set_receipts.append(record)
        set_assets.extend(receipt["assets"])
        pending_receipts.append((receipt_path, raw))
    expected_base = {candidate for family, row in locations.items() if family != "TCM-SET-HENDERSON-EXTERIOR"
                     for candidate in row["candidateIDs"]}
    base_assets = [row for row in set_assets if row["lane"] == "base_set"]
    if {row["candidateID"] for row in base_assets} != expected_base:
        raise ValueError("Base set originals do not match the set roster")
    for archive in round_archives:
        record, receipt, raw, receipt_path = extract_and_receipt(
            archive, set_home, "set_round", verified_at, background, locations, SET_AGGREGATE)
        if record["receivedOriginals"] != manifest[archive.name]["originals"]:
            raise ValueError(f"Original count differs from frozen manifest: {archive.name}")
        set_receipts.append(record)
        set_assets.extend(receipt["assets"])
        pending_receipts.append((receipt_path, raw))

    background_ids = [row["candidateID"] for row in background_assets]
    set_ids = [row["candidateID"] for row in set_assets]
    if len(background_ids) != len(set(background_ids)) or len(set_ids) != len(set(set_ids)):
        raise ValueError("Repeated candidate IDs across receipts")
    if set(background_ids) & set(set_ids):
        raise ValueError("Casting and set candidate IDs overlap")
    background_hashes = [row["sha256"] for row in background_assets]
    set_hashes = [row["sha256"] for row in set_assets]
    if len(set(background_hashes)) != 48:
        raise ValueError("Background candidate bytes are not unique")
    duplicates = {sha: [row["candidateID"] for row in set_assets if row["sha256"] == sha]
                  for sha, count in Counter(set_hashes).items() if count > 1}
    expected_duplicates = {
        "79591a1d3d539137330d86d5e45b4e24b2cc0b47af18416486d5fe81b936868c": [
            "TCM-SET-IMPALA-ID01__P08-LS05", "TCMSET_B3_IMPALA_L52__P08-LS05"],
        "5f79cc4d8b2bae50760b0cb06822ad8628a5e4c664e97ee5314903ef6a427896": [
            "TCM-SET-IMPALA-ID01__P12-LS04", "TCMSET_B3_IMPALA_L55__P12-LS04"],
    }
    if {sha: sorted(ids) for sha, ids in duplicates.items()} != {sha: sorted(ids) for sha, ids in expected_duplicates.items()}:
        raise ValueError("Unexpected duplicate set payload mapping")
    if (len(background_assets), len(set_assets), len(set(set_hashes))) != (48, 946, 944):
        raise ValueError("Unexpected sealed intake totals")
    if not all(row["indexedBytesAndHashes"] for row in background_assets + set_assets):
        missing = [row["candidateID"] for row in background_assets + set_assets if not row["indexedBytesAndHashes"]]
        raise ValueError("Cannot seal originals without matching source hash and byte evidence: " + ", ".join(missing[:20]))
    if not all(row.get("providerCandidateID") for row in set_assets):
        missing = [row["candidateID"] for row in set_assets if not row.get("providerCandidateID")]
        raise ValueError("Cannot seal set originals without their provider candidate-ID mapping: " + ", ".join(missing[:20]))
    later_assets = [row for row in set_assets if row["lane"] == "set_round"]
    assert sum(bool((row.get("providerMetadata") or {}).get("cameraPositionID")) for row in later_assets) == 749
    assert sum(bool((row.get("providerMetadata") or {}).get("lightState")) for row in later_assets) == 749
    assert sum(bool((row.get("providerMetadata") or {}).get("servesShotsSourcePresent")) for row in later_assets) == 749
    bad_screening = [row["candidateID"] for row in set_assets if (row.get("providerScreening") or {}).get("tag", "").endswith(("-LS1", "-LS2", "-LS3", "-LS4", "-LS5"))]
    if bad_screening:
        raise ValueError("Malformed repeated-header screening rows: " + ", ".join(bad_screening))

    baseline_raw = (ROOT / BASELINE_CATALOG).read_bytes()
    common = {
        "project": PROJECT,
        "intakeRole": "site_index_aggregate_receipt",
        "verifiedAtUTC": verified_at,
        "reviewControllerID": CONTROLLER,
        "acceptedOriginals": 0,
        "humanVerdictsCreated": 0,
        "selectedStartingFrames": 0,
        "baselineCatalog": {"path": BASELINE_CATALOG.as_posix(), "sha256": digest(baseline_raw)},
    }
    background_aggregate = {
        "format": "cfa-grok-casting-intake-aggregate-v1",
        **common,
        "taskID": CAST_TASK,
        "lane": "background",
        "receivedOriginals": 48,
        "receivedGroups": 16,
        "uniqueImageHashes": 48,
        "sourceRoster": CAST_ROSTER.as_posix(),
        "sourceRosterSHA256": digest(cast_roster_raw),
        "receipts": background_receipts,
        "candidateIDs": background_ids,
        "supersedes": (CAST_HOME / "CFA_CASTING_INTAKE_019-034_SITE_INDEX_v002.json").as_posix(),
        "verification": {"allArchivesCRCRead": True, "allPathsSafe": True, "allOriginalsDecoded": True,
                         "allBytesAndHashesIndexed": True, "crossLaneDuplicateHashes": False,
                         "humanReviewOrAcceptanceCreated": False},
    }
    set_aggregate = {
        "format": "cfa-grok-image-intake-aggregate-v1",
        **common,
        "taskID": SET_TASK,
        "lane": "sets",
        "receivedOriginals": 946,
        "baseLookOriginals": 190,
        "setRoundOriginals": 756,
        "uniqueImageHashes": 944,
        "receivedBaseFamilies": 19,
        "receivedSetRoundFamilies": 24,
        "sourceRoster": SET_ROSTER.as_posix(),
        "sourceRosterSHA256": digest(set_roster_raw),
        "sourceBatchManifests": sorted({row["manifestPath"]: row["manifestSHA256"] for row in manifest.values()}.items()),
        "receipts": set_receipts,
        "candidateIDs": set_ids,
        "supersedes": (SET_HOME / "CFA_SET_INTAKE_035-118_SITE_INDEX_v002.json").as_posix(),
        "duplicatePayloadMappings": [{"sha256": sha, "candidateIDs": ids,
                                       "note": "Intentional identity-sheet/take-2 reuse; preserve both candidate mappings."}
                                      for sha, ids in expected_duplicates.items()],
        "verification": {"allArchivesCRCRead": True, "allPathsSafe": True, "allOriginalsDecoded": True,
                         "allBytesAndHashesIndexed": True, "laterArchivesMatchFrozenManifests": True,
                         "crossLaneDuplicateHashes": False, "humanReviewOrAcceptanceCreated": False},
    }
    background_raw = json_bytes(background_aggregate)
    set_raw = json_bytes(set_aggregate)
    aggregate_artifacts = [(ROOT / BACKGROUND_AGGREGATE, background_raw), (ROOT / SET_AGGREGATE, set_raw)]
    for path, raw in pending_receipts + aggregate_artifacts:
        if path.exists() and path.read_bytes() != raw:
            raise ValueError(f"Frozen intake artifact differs; version it instead of overwriting: {path}")
    for path, raw in pending_receipts:
        write_verified(path, raw)
    # Aggregate seals are written last. Individual v003 receipts explicitly
    # remain incomplete unless their exact hashes appear in these aggregates.
    for path, raw in aggregate_artifacts:
        write_verified(path, raw)
    return {
        "backgroundAggregate": {"path": BACKGROUND_AGGREGATE.as_posix(), "sha256": digest(background_raw), "bytes": len(background_raw)},
        "setAggregate": {"path": SET_AGGREGATE.as_posix(), "sha256": digest(set_raw), "bytes": len(set_raw)},
        "counts": {"background": 48, "baseSets": 190, "setRound": 756, "setTotal": 946,
                   "setUniqueHashes": 944, "totalOriginalMappings": 994},
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verified-at", required=True,
                        help="UTC timestamp for the first receipt seal, for example 2026-11-04T13:41:07Z")
    args = parser.parse_args()
    print(json.dumps(seal(args.verified_at), indent=2))


if __name__ == "__main__":
    main()
