"""Link the received BOSS-008 studies without changing selected design or reviews.

Only the two named, hash-pinned source groups are read. Provider observations are
evidence about candidates, not site reviews or new character approvals.
"""
from __future__ import annotations

import csv
import hashlib
import io
import os
from pathlib import Path
import re
from urllib.parse import quote

INTAKE_ID = "HON-CROCODILE-STUDIES-20261027"
COLLECTION_ID = "hon:boss-round01"
ANCHOR_ID = "HD-RETURN-8421e7cfa1a0"
SOURCE_BASE = "docs/notes/explorable_world/comfy/references/From Grok"
SOURCE_PINS = {
    "GROK-HD-ENABLERS-03/MANIFEST.csv": "e12e5f0babe2e42c19002f3eda40d400a407952c12eabffb5fa283c12059c986",
    "GROK-HD-ENABLERS-03/E19-boss-dais/NOTES.md": "5d3564bb8390485c92e755bebef2c95134dd065b4168df7ef949090cf5edf94e",
    "GROK-HD-ENABLERS-03/HD-BUILD-AUDIT.csv": "396e11db721f097bccf5ae71a4517b91a7537cb508fb1e6d1a2519df0cd0583b",
    "GROK-HD-STORY-SET-02/MANIFEST.csv": "79275b789042a2c98717a4937c32ae805687e19e930389b4130a7847abd78f7d",
    "GROK-HD-STORY-SET-02/N08-counting-room/NOTES.md": "a27e99d29b9b15acf0acd63d082d4e97b9a39e6a220c477929c90579a5b8e625",
}
GROUPS = (
    ("GROK-HD-ENABLERS-03", "E19-boss-dais", "hon:crocodile-dais-studies", 20),
    ("GROK-HD-STORY-SET-02", "N08-counting-room", "hon:crocodile-counting-room", 15),
)
OLD_NAMES = {
    "E19-boss-dais-004-v001.jpg", "E19-boss-dais-004-v002.jpg",
    "E19-boss-dais-015-v001.jpg",
}
ALIAS_NAMES = {"E19-boss-dais-004.jpg", "E19-boss-dais-015.jpg"}


def _hash(data):
    return hashlib.sha256(data).hexdigest()


def _unique(items):
    return list(dict.fromkeys(items))


def load_crocodile_sources(repo_root):
    """Validate the bounded sources and return one record per unique image."""
    root = Path(repo_root).resolve()
    base = root / SOURCE_BASE
    texts = {}
    evidence = []
    for relative, expected in SOURCE_PINS.items():
        path = base / relative
        data = path.read_bytes()
        if _hash(data) != expected:
            raise ValueError("Crocodile source evidence changed: " + relative)
        texts[relative] = data.decode("utf-8-sig")
        evidence.append({"repoPath": path.relative_to(root).as_posix(), "sha256": expected})
    records_by_hash = {}
    path_count = 0
    for package, group, album, expected_count in GROUPS:
        rows = list(csv.DictReader(io.StringIO(texts[package + "/MANIFEST.csv"])))
        rows = [r for r in rows if r["path"].startswith(group + "/") and r["path"].endswith(".jpg")]
        if len(rows) != expected_count:
            raise ValueError("Unexpected crocodile source count: " + group)
        notes = texts[package + "/" + group + "/NOTES.md"]
        for row in sorted(rows, key=lambda r: (Path(r["path"]).name in ALIAS_NAMES, r["path"])):
            source = (base / package / row["path"]).resolve()
            if not source.is_relative_to(base.resolve()):
                raise ValueError("Source path escaped the received package")
            data = source.read_bytes()
            sha = _hash(data)
            if sha != row["sha256"] or len(data) != int(row["bytes"]):
                raise ValueError("Crocodile media differs from manifest: " + row["path"])
            path_count += 1
            alias = {"repoPath": source.relative_to(root).as_posix(), "sha256": sha, "bytes": len(data)}
            if sha in records_by_hash:
                records_by_hash[sha]["sourceAliases"].append(alias)
                continue
            name = source.name
            observed = [line.strip() for line in notes.splitlines()
                        if re.search(r"^\|\s*(?:" + re.escape(group) + r"/)?" + re.escape(name) + r"\s*\|", line)
                        or re.search(r"^BUILD AUDIT [^:]+: " + re.escape(name) + r"\s", line)]
            records_by_hash[sha] = {
                "repoPath": alias["repoPath"], "filename": name, "sha256": sha,
                "bytes": len(data), "album": album, "sourceGroup": group,
                "sourceAliases": [alias], "providerObservations": observed,
                "superseded": name in OLD_NAMES,
                "referenceAnchorID": ANCHOR_ID,
                "providerQAStatus": "preliminary",
                "evidence": [x for x in evidence if package + "/" in x["repoPath"]],
                "humanAcceptance": None,
            }
    records = list(records_by_hash.values())
    if path_count != 35 or len(records) != 33:
        raise ValueError("Crocodile intake must contain 35 aliases and 33 distinct images")
    by_name = {r["filename"]: r for r in records}
    audit_rows = csv.DictReader(io.StringIO(texts["GROK-HD-ENABLERS-03/HD-BUILD-AUDIT.csv"]))
    for row in audit_rows:
        if row["category"] != "E19-boss-dais":
            continue
        before, after = Path(row["file"]).name, Path(row["replacement_file"]).name
        if before not in by_name or after not in by_name:
            raise ValueError("Repair relationship names an unavailable crocodile image")
        previous, replacement = by_name[before], by_name[after]
        previous.setdefault("supersededBySHA256", []).append(replacement["sha256"])
        replacement.setdefault("replacesSHA256", []).append(previous["sha256"])
        # A replacement relation does not establish the actual generation input.
        previous.setdefault("buildAudit", []).append(dict(row))
        replacement.setdefault("buildAudit", []).append(dict(row))
    return {"records": records, "evidence": evidence, "sourcePathCount": path_count}


def _preview(source, destination):
    from PIL import Image, ImageOps
    with Image.open(source) as original:
        width, height = original.size
        if not destination.exists():
            destination.parent.mkdir(parents=True, exist_ok=True)
            image = ImageOps.exif_transpose(original).convert("RGB")
            image.thumbnail((600, 600))
            image.save(destination, quality=85)
    return width, height


def apply_crocodile_intake(catalog, repo_root):
    """Add exact-byte candidates; preserve every existing asset and review.

    New collection fields are characterStudyIDs (15 latest E19), sceneStudyIDs
    (15 N08), and revisionStudyIDs (3 older repairs). sceneAssetIDs also exposes
    all 33 to the existing hub. The selected anchor and approval fields do not
    change. Returns the newly appended asset records; a second run adds none.
    """
    root = Path(repo_root).resolve()
    loaded = load_crocodile_sources(root)
    group = next(g for g in catalog["castCollections"] if g["id"] == COLLECTION_ID)
    assets_by_hash = {}
    assets_by_id = {a["id"]: a for a in catalog["assets"]}
    for asset in catalog["assets"]:
        if asset.get("sha256"):
            assets_by_hash.setdefault(asset["sha256"], asset)
    here = root / "docs/notes/explorable_world/comfy/projects/visual_library"
    previews = here.parent / "review_previews_crocodile_20261027"

    def url(path):
        return quote(os.path.relpath(path, here).replace("\\", "/"), safe="/")

    added = []
    metadata = {}
    for record in loaded["records"]:
        sha = record["sha256"]
        existing = assets_by_hash.get(sha)
        asset_id = existing["id"] if existing else "HD-CROC-" + sha[:20]
        if asset_id in assets_by_id and assets_by_id[asset_id].get("sha256") != sha:
            raise ValueError("Crocodile asset ID collision: " + asset_id)
        record["assetID"] = asset_id
        metadata[asset_id] = record
        if existing:
            continue
        source = root / record["repoPath"]
        preview = previews / (sha + ".jpg")
        width, height = _preview(source, preview)
        label = record["filename"].removesuffix(".jpg")
        note = "Received crocodile study; provider observations are preliminary. Character and scene acceptance remain open."
        if record["superseded"]:
            note = "Earlier repair version retained for comparison; see its replacement and recorded defects."
        if record["providerObservations"]:
            note += " Provider notes: " + " ".join(record["providerObservations"])
        asset = {
            "id": asset_id, "project": "hon", "kind": "image", "category": "cast",
            "album": record["album"], "title": label + " · Crocodile study",
            "filename": record["filename"], "repoPath": record["repoPath"],
            "src": url(source), "thumb": url(preview), "sha256": sha,
            "bytes": record["bytes"], "width": width, "height": height,
            "sourceIntake": INTAKE_ID, "sourceStatus": "Received candidate · provider QA preliminary",
            "note": note, "sourceAliases": record["sourceAliases"],
            "tags": ["Crocodile boss", "BOSS-008", record["sourceGroup"], "unapproved candidate"],
            "providerObservations": record["providerObservations"],
            "referenceRole": "candidate_scene_study" if record["sourceGroup"].startswith("N08") else "candidate_character_study",
        }
        added.append(asset)
        assets_by_hash[sha] = asset
        assets_by_id[asset_id] = asset
    for record in loaded["records"]:
        record["replacesAssetIDs"] = [assets_by_hash[sha]["id"] for sha in record.get("replacesSHA256", [])]
        record["supersededByAssetIDs"] = [assets_by_hash[sha]["id"] for sha in record.get("supersededBySHA256", [])]
    catalog["assets"].extend(added)
    for package, source_group, album_id, _ in GROUPS:
        album = next((a for a in catalog["albums"] if a["id"] == album_id), None)
        if album is None:
            album = {
                "id": album_id, "project": "hon", "category": "cast",
                "title": "Crocodile · " + ("character and dais studies" if source_group.startswith("E19") else "counting-room candidates"),
                "description": "Received candidates with source QA; inclusion does not approve design or scene.",
                "assetIDs": [],
            }
            catalog["albums"].append(album)
        album["assetIDs"] = _unique(album.get("assetIDs", []) + [r["assetID"] for r in loaded["records"] if r["sourceGroup"] == source_group])
    fields = {
        "characterStudyIDs": [r["assetID"] for r in loaded["records"] if r["sourceGroup"].startswith("E19") and not r["superseded"]],
        "sceneStudyIDs": [r["assetID"] for r in loaded["records"] if r["sourceGroup"].startswith("N08")],
        "revisionStudyIDs": [r["assetID"] for r in loaded["records"] if r["superseded"]],
    }
    for name, ids in fields.items():
        group[name] = _unique(group.get(name, []) + ids)
    all_ids = [r["assetID"] for r in loaded["records"]]
    group["assetIDs"] = _unique(group.get("assetIDs", []) + all_ids)
    group["sceneAssetIDs"] = _unique(group.get("sceneAssetIDs", []) + all_ids)
    group["sourceAlbumIDs"] = _unique(group.get("sourceAlbumIDs", []) + [g[2] for g in GROUPS])
    catalog["crocodileIntake"] = {
        "id": INTAKE_ID, "schemaVersion": 1, "collectionID": COLLECTION_ID,
        "referenceAnchorID": ANCHOR_ID, "records": metadata, "evidence": loaded["evidence"],
        "summary": {"verifiedSourcePaths": 35, "uniqueImages": 33, "exactDuplicateAliases": 2,
                    "characterStudies": 15, "sceneStudies": 15, "olderVersions": 3},
        "authorityNote": "Original BOSS-008 selection is preserved. Source grades and replacement relationships are evidence, not site approval or validation.",
    }
    return added
