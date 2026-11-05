"""Give two received Grok clips a video home without replacing intake or reviews.

This is a hash-bound discovery adapter, not a new media intake or quality pass.
It can also be applied to a loaded catalog for a bounded, serialized refresh.
"""
from copy import deepcopy
import hashlib
from pathlib import Path


SOURCE_BASE = "docs/notes/explorable_world/comfy/references/From Grok/GROK-VIDEO-TEST_v001"
REVIEW_PATH = SOURCE_BASE + "/REVIEW_gorilla-clips_v001.md"
REVIEW_SHA256 = "b23aa6c28d0b19f516776b8e576d9dc4bd96610c2a6d6d926720773ea1292981"
SOURCE_ALBUM = "hon:intake-grok-video-test"
VIDEO_ALBUM = "hon:video-grok-tests"
CHARACTER = "hon:cast-dj"
CLIPS = (
    {
        "id": "HD-INTAKE-3dc76f7d9d325f21cd1b",
        "filename": "gorilla-stew-booth_v001.mp4",
        "sha256": "3dc76f7d9d325f21cd1b64de4e0e025e32b200cb6c29504aa8593df8441985b8",
        "bytes": 6917044,
        "title": "Chewy · Stew in the booth",
        "scene": "Stew booth",
    },
    {
        "id": "HD-INTAKE-3ea5959c05259fd65f8d",
        "filename": "gorilla-workshop-argument_v001.mp4",
        "sha256": "3ea5959c05259fd65f8d30cb4caa8317245b599e770824c826620c97bfc489c5",
        "bytes": 7157307,
        "title": "Chewy · Workshop argument",
        "scene": "Workshop argument",
    },
)


def apply_grok_video_home(catalog, repo_root):
    """Change discovery metadata only, validating the entire pair first.

    Stable assets, intake families and original album membership are retained.
    Existing human decisions, review histories, reference selection and the
    Chief's frozen findings are never rewritten by this adapter.
    """
    root = Path(repo_root).resolve()
    review_bytes = (root / REVIEW_PATH).read_bytes()
    if hashlib.sha256(review_bytes).hexdigest() != REVIEW_SHA256:
        raise ValueError("Grok video provider evidence changed")
    assets = {asset["id"]: asset for asset in catalog["assets"]}
    if len(assets) != len(catalog["assets"]):
        raise ValueError("Duplicate canonical asset IDs")
    albums = {album["id"]: album for album in catalog["albums"]}
    source_album = albums.get(SOURCE_ALBUM)
    if not source_album or source_album.get("category") != "intake":
        raise ValueError("Grok video intake album is missing")
    groups = {group["id"]: group for group in catalog.get("castCollections", [])}
    group = groups.get(CHARACTER)
    if not group or group.get("project") != "hon":
        raise ValueError("Chewy character collection is missing")
    destination = albums.get(VIDEO_ALBUM)
    if destination and (destination.get("project"), destination.get("category")) != ("hon", "videos"):
        raise ValueError("Grok video destination conflicts with an existing album")
    for clip in CLIPS:
        asset = assets.get(clip["id"])
        expected_path = SOURCE_BASE + "/" + clip["filename"]
        if not asset or any(asset.get(key) != clip[key] for key in ("sha256", "filename", "bytes")):
            raise ValueError("Grok video asset identity changed: " + clip["id"])
        if asset.get("repoPath") != expected_path or (asset.get("project"), asset.get("kind")) != ("hon", "video"):
            raise ValueError("Grok video source location changed: " + clip["id"])
        if (asset.get("category"), asset.get("album")) not in (("intake", SOURCE_ALBUM), ("videos", VIDEO_ALBUM)):
            raise ValueError("Grok video placement needs reconciliation: " + clip["id"])
        if clip["id"] not in source_album["assetIDs"]:
            raise ValueError("Grok video intake association is missing: " + clip["id"])
        raw = (root / expected_path).read_bytes()
        if len(raw) != clip["bytes"] or hashlib.sha256(raw).hexdigest() != clip["sha256"]:
            raise ValueError("Grok video source bytes changed: " + clip["filename"])

    # Construct replacements after validation; no partial placement on failure.
    replacements = {}
    for clip in CLIPS:
        asset = deepcopy(assets[clip["id"]])
        if "discoveryPlacement" not in asset:
            asset["discoveryPlacement"] = {
                "decisionID": "ziggy-grok-video-home-20261029",
                "source": "Ziggy identified the GROK-VIDEO-TEST_v001 folder and requested a site-index home.",
                "scope": "Provider attribution, scene titles and discovery only; reviews and reference selection are unchanged.",
                "original": {key: deepcopy(asset.get(key)) for key in ("category", "album", "title", "note")},
            }
        asset.update(
            title=clip["title"], category="videos", album=VIDEO_ALBUM,
            sourceProvider="Grok", provider="Grok", sourcePackage="GROK-VIDEO-TEST_v001",
            characterCollectionID=CHARACTER, provenancePath=REVIEW_PATH,
            providerEvidence={
                "reviewer": "Chief", "status": "PRELIMINARY", "receivedInHandoff": "2026-10-21",
                "repoPath": REVIEW_PATH, "sha256": REVIEW_SHA256,
                "scope": "Historical provider comparison of these exact clips; not a V-Team verdict or a new benchmark.",
                "capabilityClaims": "Duration, resolution and tool-limit statements describe the supplied review at delivery, not current provider controls.",
            },
            note="Grok video test from Ziggy's Chewy still. Chief's preliminary review was received with the October 21 handoff; it remains historical provider evidence. This clip's saved human review and ratings are separate and unchanged.",
        )
        asset["tags"] = list(dict.fromkeys([*asset.get("tags", []), "Grok", "Grok video", "Chewy", clip["scene"]]))
        replacements[asset["id"]] = asset
    updated_album = deepcopy(destination) if destination else {
        "id": VIDEO_ALBUM, "project": "hon", "category": "videos", "assetIDs": [],
    }
    updated_album.update(
        title="Grok video tests", sourceProvider="Grok", sourcePackage="GROK-VIDEO-TEST_v001",
        description="Grok-generated Chewy scene tests from Ziggy's two stills. These same clips retain their intake evidence and saved reviews.",
    )
    updated_album["assetIDs"] = list(dict.fromkeys([*updated_album["assetIDs"], *(clip["id"] for clip in CLIPS)]))
    updated_group = deepcopy(group)
    updated_group["videoAssetIDs"] = list(dict.fromkeys([*group.get("videoAssetIDs", []), *(clip["id"] for clip in CLIPS)]))
    updated_group["sourceAlbumIDs"] = list(dict.fromkeys([*group.get("sourceAlbumIDs", []), VIDEO_ALBUM]))

    catalog["assets"] = [replacements.get(asset["id"], asset) for asset in catalog["assets"]]
    catalog["albums"] = [updated_album if album["id"] == VIDEO_ALBUM else album for album in catalog["albums"]]
    if destination is None:
        catalog["albums"].append(updated_album)
    catalog["castCollections"] = [updated_group if item["id"] == CHARACTER else item for item in catalog["castCollections"]]
    return [clip["id"] for clip in CLIPS]
