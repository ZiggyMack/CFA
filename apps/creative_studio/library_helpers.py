"""Small, offline helpers shared by the Creative Studio and its checks."""

from __future__ import annotations

from datetime import datetime, timezone
from copy import deepcopy
import hashlib
import io
import json
from pathlib import Path
import re
from typing import Any
from urllib.parse import unquote, urlsplit
import zipfile

FAVORITES_FORMAT = "cfa-visual-favorites-v1"
REVIEW_FORMAT = "cfa-visual-review-v1"
HANDOFF_FORMAT = "cfa-shot-handoff-v1"
EXPORT_FORMAT = "cfa-visual-export-v1"
REVIEW_STATUSES = {"keep", "needs_fixes", "remove"}
# Opaque, hash-bound review provenance survives the compact editor. These fields
# do not drive execution or confer approval; unsupported controls remain in the index.
REVIEW_METADATA_FIELDS = {
    "updatedAt", "origin", "source", "sourceIntakeID", "scopeNote", "sourceReviewPath",
    "collectionState", "importEvidence", "archiveReason", "removalState", "handoffPolicy",
    "creativeReview", "supersededBy", "displayTitle", "humanRatingConfirmation", "history",
    "reason", "reasonSource", "scopedPropCorrection", "temporalVariant", "lookSelection",
    "componentSelection", "directUserClarification", "creativeLane", "validationEvidence", "multiverseSelection",
    "shotPlanClearEvidence", "shotPlanUpdatedAt", "fieldUpdatedAt",
}
DESTINATIONS = ("undecided", "Gemini", "Flow", "Grok", "grok_video", "ComfyUI")
DESTINATION_LABELS = {"undecided": "Undecided", "Grok": "Grok stills", "grok_video": "Grok video"}
OUTPUT_KINDS = ("unspecified", "image", "video")
OUTPUT_KIND_LABELS = {"unspecified": "Not specified", "image": "Still image", "video": "Video clip"}


def destination_label(destination: str) -> str:
    return DESTINATION_LABELS.get(destination, destination)


def output_kind_label(kind: str | None) -> str:
    return OUTPUT_KIND_LABELS.get(kind, OUTPUT_KIND_LABELS["unspecified"])


MISSION_PROVIDERS = ("Grok", "Gemini", "Flow", "Panhandler Nova")
MISSION_STATUSES = {"ready", "needs_input", "planned", "in_progress", "done"}
VISUAL_KINDS = {"image", "video", "gif"}


def navigation_reference_count(assets: list[dict], selected_ids=None, *, documents: bool = False) -> int:
    """Count sidebar references without changing the displayed collections."""
    selected = set(selected_ids) if selected_ids is not None else None
    return len({asset["id"] for asset in assets
                if (selected is None or asset["id"] in selected)
                and (asset.get("kind") in {"document", "pdf"}) == documents})


def navigation_storyboard_shot_count(data: dict, project: str) -> int:
    """Count authored parent shots, independent of panels, references and takes."""
    stories = {story["id"]: story for story in data.get("storyboardStories", [])
               if story.get("project") == project and story.get("id")}
    structures = {row["storyID"]: row for row in data.get("storyboardStructure", {}).get("stories", [])
                  if row.get("storyID") and row.get("project", project) == project}
    sequences = {row["id"]: row for row in data.get("storyboardSequences", [])
                 if row.get("id") and row.get("project") == project}
    counted = set()
    for story_id, story in stories.items():
        if story_id in structures:
            shots = structures[story_id].get("shots", [])
        elif story.get("sequenceID"):
            sequence = sequences.get(story["sequenceID"], {})
            shots = sequence.get("shots")
            if shots is None:
                shots = [shot for shot in data.get("shotMaterials", {}).get("shots", [])
                         if shot.get("project") == project
                         and shot.get("independentSequenceID") == story["sequenceID"]]
        else:
            shots = []
        by_id = {}
        for shot in shots:
            shot_id = shot.get("shotID") or shot.get("id")
            if isinstance(shot_id, str) and shot_id:
                by_id.setdefault(shot_id, shot)
        for shot_id, shot in by_id.items():
            parent = shot.get("parent")
            parent_id = (shot.get("parentShotID") or shot.get("parent_shot_id")
                         or (parent.get("shotID") if isinstance(parent, dict) else None))
            if isinstance(parent_id, str) and parent_id != shot_id and parent_id in by_id:
                continue
            counted.add((story_id, shot_id))
    return len(counted)


STORYBOARD_STAGES = {"preliminary": "Preliminary", "detailed_design": "Detailed design",
                     "verification": "Verification", "production": "Production"}
HISTORICAL_TATTOO_IDS = {
    "HD-RETURN-d55b97a3b322", "HD-RETURN-78ad6c79615a", "HD-RETURN-f88ff5ae511e",
    "HD-TATGUIDE-b80e4d006917", "HD-RETURN-d91685dd99cd", "HD-TATGUIDE-d152270ab369",
    "HD-TATGUIDE-ad54ba356e7c", "HD-TATGUIDE-3046dd64faa8", "HD-TATGUIDE-440a8cf5e911",
}


def design_archive_membership(data: dict) -> tuple[set[str], set[str]]:
    """The index's default history policy; explicit review choices are applied later."""
    assets = data.get("assets", [])
    by_id = {asset["id"]: asset for asset in assets}
    characters = data.get("characterBOM", {}).get("characters", [])
    cast = data.get("castCollections", [])
    protected = {character.get("coverAssetID") for character in characters}
    protected.update(entry.get("assetID") for character in characters for entry in character.get("entries", []) if entry.get("recordedSelection"))
    protected.update(asset_id for group in cast for field in ("currentIDs", "workingReferenceIDs") for asset_id in group.get(field, []))
    protected.update(asset["id"] for asset in assets if any(
        approval.get("sourceSHA256") == asset.get("sha256") and approval.get("status") == "user_selected_component"
        for approval in asset.get("componentApprovals", [])))
    retired = {asset_id for album in data.get("albums", []) if album.get("id") in {"hon:scene-ideas", "hon:outfit-ideas"}
               for asset_id in album.get("assetIDs", [])}
    history = {"HD-LIKENESS-02", *HISTORICAL_TATTOO_IDS, *retired}
    history.update(asset_id for character in characters for asset_id in character.get("historyAssetIDs", []))
    history.update(asset_id for group in data.get("sharedReferenceCollections", []) for section in group.get("sections", [])
                   if section.get("history") is True for asset_id in section.get("assetIDs", []))
    history.update(asset_id for group in cast for asset_id in group.get("historicalReferenceIDs", group.get("historyIDs", [])))
    mouth = data.get("mouthCoverage", {})
    historical_looks = {look.get("id") for look in mouth.get("looks", []) if look.get("history") is True or look.get("planStatus") == "History only"}
    history.update(row.get("assetID") for row in mouth.get("items", []) if row.get("lookID") in historical_looks
                   and by_id.get(row.get("assetID"), {}).get("sha256") == row.get("sha256"))
    return history - protected, retired


def asset_archived(asset: dict, reviews: dict[str, dict]) -> bool:
    decision = reviews.get(asset["id"], {})
    choice = decision.get("collectionState")
    if choice in ("archived", "working"):
        return choice == "archived"
    selected = asset.get("_retiredInspiration", False) and (
        (decision.get("workingReference") or {}).get("status") == "approved"
        or decision.get("status") == "keep" and (decision.get("storyboardStage") or asset.get("storyboardStage")) == "production")
    return bool(asset.get("_sourceArchived", asset.get("archived", False))
                or asset.get("_historyArchived", False) and not selected)


def normal_visible(asset: dict | None, reviews: dict[str, dict]) -> bool:
    if not asset or asset_archived(asset, reviews):
        return False
    decision = reviews.get(asset["id"], {})
    return decision.get("status", "remove" if asset.get("_reviewRemoved") else None) != "remove"


def effective_design_data(data: dict, reviews: dict[str, dict]) -> dict:
    """Copy display flags, retaining every original asset and all evidence for history."""
    historical, retired = design_archive_membership(data)
    result = dict(data)
    result["assets"] = []
    for source in data.get("assets", []):
        asset = dict(source)
        asset["_sourceArchived"] = source.get("_sourceArchived", bool(source.get("archived")))
        asset["_historyArchived"] = asset["id"] in historical
        asset["_retiredInspiration"] = asset["id"] in retired
        asset["_reviewRemoved"] = reviews.get(asset["id"], {}).get("status") == "remove"
        asset["archived"] = asset_archived(asset, reviews)
        result["assets"].append(asset)
    return result


def approved_multiverse(asset: dict, reviews: dict[str, dict]) -> bool:
    decision = reviews.get(asset["id"], {})
    rating = decision.get("likenessRating")
    return (normal_visible(asset, reviews) and decision.get("variant", asset.get("variant")) == "multiverse"
            and decision.get("multiverseSelection") == "approved" and type(rating) is int and 2 <= rating <= 5)


def validated_asset_aliases(assets: list[dict], aliases: Any = ()) -> dict[str, dict]:
    """Visual re-encodings are explicit navigation/review aliases, never hash equality."""
    by_id = {asset["id"]: asset for asset in assets}
    result, conflicts = {}, set()
    for alias in aliases if isinstance(aliases, (list, tuple)) else []:
        if not isinstance(alias, dict) or alias.get("kind") != "visual_duplicate_reencoding":
            continue
        old_id, canonical_id = alias.get("id"), alias.get("canonicalID")
        if not isinstance(old_id, str) or not old_id or old_id in by_id or not isinstance(canonical_id, str):
            continue
        target = by_id.get(canonical_id)
        if not target or any(not isinstance(alias.get(key), str) or not re.fullmatch(r"[a-f0-9]{64}", alias[key])
                             for key in ("sha256", "canonicalSHA256")) or target.get("sha256") != alias["canonicalSHA256"]:
            continue
        prior = result.get(old_id)
        if prior and any(prior.get(key) != alias.get(key) for key in ("sha256", "canonicalID", "canonicalSHA256")):
            conflicts.add(old_id)
        result[old_id] = alias
    return {key: value for key, value in result.items() if key not in conflicts}


def resolve_asset_reference(item: Any, assets: list[dict], aliases: Any = (), *, require_hash: bool = True,
                            allow_alias_id: bool = False) -> dict | None:
    by_id = {asset["id"]: asset for asset in assets}
    if isinstance(item, str):
        item = {"id": item}
    if not isinstance(item, dict) or not isinstance(item.get("id"), str):
        return None
    asset = by_id.get(item["id"])
    if asset:
        return asset if (_hash_matches(item, asset) if require_hash else not item.get("sha256") or _hash_matches(item, asset)) else None
    alias = validated_asset_aliases(assets, aliases).get(item["id"])
    if alias and (item.get("sha256") == alias["sha256"] or allow_alias_id and not item.get("sha256")):
        return by_id[alias["canonicalID"]]
    return None


def _review_time(record: dict) -> float:
    try:
        stamp = datetime.fromisoformat(str(record.get("updatedAt", "")).replace("Z", "+00:00"))
        return (stamp if stamp.tzinfo else stamp.replace(tzinfo=timezone.utc)).timestamp()
    except (ValueError, TypeError, KeyError, OverflowError):
        return 0


def _guard_plan_clear(prior: dict, incoming: dict) -> dict:
    """A dated field-only clear must not be undone by an older whole-record import."""
    incoming = dict(incoming)
    before = prior.get("shotPlanClearEvidence")
    after = incoming.get("shotPlanClearEvidence")
    before_time = _review_time(before) if isinstance(before, dict) else 0
    after_time = _review_time(after) if isinstance(after, dict) else 0
    clear_time = max(before_time, after_time)
    if not clear_time:
        return incoming
    if before_time > after_time:
        incoming["shotPlanClearEvidence"] = deepcopy(before)
    if "shotPlan" in incoming:
        incoming_time = max(_review_time(incoming), _review_time({"updatedAt": incoming.get("shotPlanUpdatedAt")}),
                            after_time if incoming["shotPlan"] is None else 0)
        prior_time = max(_review_time(prior), _review_time({"updatedAt": prior.get("shotPlanUpdatedAt")}),
                         before_time if prior.get("shotPlan") is None else 0)
        if ((incoming["shotPlan"] is not None and incoming_time <= clear_time)
                or "shotPlan" in prior and incoming_time < prior_time):
            incoming.pop("shotPlan")
            if "shotPlan" in prior:
                incoming["shotPlanUpdatedAt"] = datetime.fromtimestamp(prior_time, timezone.utc).isoformat()
        else:
            incoming["shotPlanUpdatedAt"] = datetime.fromtimestamp(incoming_time, timezone.utc).isoformat()
    return incoming


def _merge_decision(result: dict, asset_id: str, incoming: dict, alias_ids: set[str]) -> None:
    prior = result.get(asset_id)
    if prior is not None and asset_id in alias_ids:
        before, after = _review_time(prior), _review_time(incoming)
        if after < before or after == before and incoming.get("_visualAliasSource"):
            return
    incoming = _guard_plan_clear(prior or {}, incoming)
    merged = {"status": None, "note": "", "shotPlan": None, **(prior or {}), **incoming}
    if "_visualAliasSource" not in incoming:
        merged.pop("_visualAliasSource", None)
    if merged.get("variant") == "multiverse":
        merged["workingReference"] = None
    result[asset_id] = merged


def merge_review_overrides(existing: dict[str, dict], incoming: dict[str, dict], assets: list[dict], aliases: Any = ()) -> dict[str, dict]:
    """Merge validated/session decisions without letting an older alias win by order."""
    result = deepcopy(existing)
    by_id = {asset["id"]: asset for asset in assets}
    alias_map = validated_asset_aliases(assets, aliases)
    alias_ids = {alias["canonicalID"] for alias in alias_map.values()}
    for asset_id, record in incoming.items():
        if asset_id not in by_id:
            continue
        normalized = normalize_decision(record, partial=True)
        marker = record.get("_visualAliasSource")
        if isinstance(marker, dict):
            alias = alias_map.get(marker.get("id"))
            if not alias or alias["canonicalID"] != asset_id or marker.get("sha256") != alias["sha256"]:
                continue
            normalized.pop("validationEvidence", None)
            normalized["_visualAliasSource"] = deepcopy(marker)
        _merge_decision(result, asset_id, normalized, alias_ids)
    return result


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
    project: str, category: str = "all", album_id: str = "all", query: str = "", include_archived: bool = False,
) -> list[tuple[dict[str, Any], dict[str, Any] | None]]:
    """Follow supplied album and member order, showing each picture once."""
    by_id = {a["id"]: a for a in assets if a.get("project") == project and a.get("kind") in VISUAL_KINDS
             and (include_archived or not a.get("archived") and not a.get("_reviewRemoved"))}
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


def sort_video_assets(results: list[tuple[dict, dict | None]], order: str) -> list[tuple[dict, dict | None]]:
    """Keep editorial order by default; explicit sorts can cross scene groups."""
    if order == "Recommended":
        return list(results)
    if order in ("Alphabetical", "Alphabetical A–Z"):
        return sorted(results, key=lambda row: str(row[0].get("title", row[0].get("filename", ""))).casefold())
    if order not in ("Longest", "Longest first", "Shortest"):
        raise ValueError("Unknown video order.")
    def key(row):
        duration = row[0].get("duration")
        known = isinstance(duration, (int, float)) and not isinstance(duration, bool) and duration >= 0
        title = str(row[0].get("title", row[0].get("filename", ""))).casefold()
        return (not known, (-duration if order in ("Longest", "Longest first") else duration) if known else 0, title)
    return sorted(results, key=key)


def layout_video_assets(results: list[tuple[dict, dict | None]], layout: str, order: str) -> list[tuple[dict, dict | None]]:
    if layout == "All clips":
        return [(asset, None) for asset, _ in sort_video_assets(results, order)]
    if layout != "Grouped":
        raise ValueError("Unknown video layout.")
    groups: dict[str, list[tuple[dict, dict | None]]] = {}
    for row in results:
        groups.setdefault(row[1].get("id", "") if row[1] else "", []).append(row)
    # Retain the supplied category order, with turnaround references at the end.
    order_ids = sorted(groups, key=lambda key: "turnaround" in (key + " " + str((groups[key][0][1] or {}).get("title", ""))).casefold())
    return [row for key in order_ids for row in sort_video_assets(groups[key], order)]


def collaborator_sections(assets: list[dict]) -> dict[str, list[dict]]:
    sections: dict[str, list[dict]] = {name: [] for name in ("Gemini", "Flow", "Grok", "Shared roles")}
    for asset in assets:
        if asset.get("kind") not in ("document", "pdf"):
            continue
        filename = str(asset.get("filename", "")).casefold()
        context = " ".join(str(asset.get(key, "")) for key in ("id", "album", "title", "filename")).casefold()
        if "historical" in context:
            continue
        if filename == "provider_roles.txt" or "panhandler_return" in filename:
            provider = "Shared roles"
        elif "gemini" in context:
            provider = "Gemini"
        elif re.search(r"(?<![a-z])flow(?![a-z])", context):
            provider = "Flow"
        elif "grok" in context and any(word in context for word in ("instructions", "care package", "grok_20", "revision_queue")):
            provider = "Grok"
        else:
            continue
        sections[provider].append(asset)
    # Put each provider's front-door instructions first, retaining the rest's saved order.
    for provider in sections:
        sections[provider].sort(key=lambda asset: -1 if asset.get("filename") == "grok_design_instructions.txt"
                                else 0 if "start_here" in asset.get("filename", "").casefold() else 1)
    return sections


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


def read_favorites(payload: Any, assets: list[dict[str, Any]], aliases: Any = ()) -> tuple[set[str], dict[str, str], int]:
    """Import known IDs only, and reject mismatched source hashes."""
    if not isinstance(payload, dict) or payload.get("format") != FAVORITES_FORMAT or not isinstance(payload.get("items"), list):
        raise ValueError("Choose a Creative Studio favorites export (cfa-visual-favorites-v1).")
    accepted, skipped = set(), 0
    for item in payload["items"]:
        asset = resolve_asset_reference(item, assets, aliases, require_hash=False, allow_alias_id=True)
        if asset:
            accepted.add(asset["id"])
        else:
            skipped += 1
    raw_notes = payload.get("notes", {})
    note_refs = payload.get("note_refs", {})
    if not isinstance(note_refs, dict):
        note_refs = {}
    notes = {}
    for key, value in raw_notes.items() if isinstance(raw_notes, dict) else []:
        asset = resolve_asset_reference({"id": key, "sha256": note_refs.get(key)}, assets, aliases,
                                        require_hash=False, allow_alias_id=True)
        if asset and isinstance(value, str):
            # A canonical note wins a simultaneous legacy alias note without a timestamp.
            if asset["id"] not in notes or key == asset["id"]:
                notes[asset["id"]] = value[:20000]
    return accepted, notes, skipped


def normalize_plan(value: Any) -> dict[str, Any] | None:
    """Plans are drafts only; never import claims that a provider has run them."""
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError("A shot plan must be an object or null.")
    destinations = value.get("destinations", ["undecided"])
    if not isinstance(destinations, list) or any(d not in DESTINATIONS for d in destinations):
        raise ValueError("Choose Gemini, Flow, Grok stills, Grok video, ComfyUI, or undecided for a shot plan.")
    destinations = [d for d in DESTINATIONS if d in destinations and d != "undecided"] or ["undecided"]
    idea, prompt = value.get("idea", ""), value.get("prompt", "")
    if not isinstance(idea, str) or not isinstance(prompt, str):
        raise ValueError("Shot ideas and prompts must be text.")
    output_kind = value.get("outputKind", "unspecified")
    if output_kind not in OUTPUT_KINDS:
        raise ValueError("Choose image, video, or unspecified for a shot plan's output kind.")
    status = "requested_bounded_test" if value.get("status") == "requested_bounded_test" else "planned"
    plan = {"status": status, "destinations": destinations, "idea": idea[:20000], "prompt": prompt[:40000]}
    if "outputKind" in value:
        plan["outputKind"] = output_kind
    return plan


def normalize_cast_use(value: Any) -> dict | None:
    if value is None:
        return None
    if not isinstance(value, dict):
        raise ValueError("Cast use must be an object or null.")
    result = json.loads(json.dumps(value, allow_nan=False))
    for field in ("roleSelected", "storyboardPlanned"):
        if field in value and type(value[field]) is not bool:
            raise ValueError("Cast role and storyboard choices must be true or false.")
    if "role" in value and (not isinstance(value["role"], str) or len(value["role"]) > 300):
        raise ValueError("A cast role must be text up to 300 characters.")
    links = value.get("storyboardLinks", [])
    if not isinstance(links, list):
        raise ValueError("Cast storyboard links must be a list.")
    unique_links, seen = [], set()
    for link in links:
        if not isinstance(link, dict) or any(not isinstance(link.get(key), str) or not link[key].strip()
                                           or len(link[key]) > 512 for key in ("storyID", "shotID")):
            raise ValueError("A cast storyboard link needs a story and shot identifier.")
        identity = (link["storyID"], link["shotID"])
        if identity not in seen:
            unique_links.append(deepcopy(link)); seen.add(identity)
    result["storyboardLinks"] = unique_links
    return result


def cast_member_ids(group: dict) -> list[str]:
    """Full character membership, including versions outside the visible cover."""
    ids = []
    def visit(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key in {"representativeID", "coverID", "coverAssetID", "assetID"} and isinstance(value, str):
                    ids.append(value)
                elif key.endswith("IDs") and isinstance(value, list):
                    ids.extend(item for item in value if isinstance(item, str))
                elif isinstance(value, (dict, list)):
                    visit(value)
        elif isinstance(node, list):
            for item in node: visit(item)
    visit(group)
    return list(dict.fromkeys(ids))


def cast_story_targets(data: dict, project: str) -> list[dict]:
    """Only real shots in registered stories from the same project are linkable."""
    structures = {row["storyID"]: row for row in data.get("storyboardStructure", {}).get("stories", [])}
    sequences = {row["id"]: row for row in data.get("storyboardSequences", []) if row.get("project") == project}
    targets = {}
    for story in data.get("storyboardStories", []):
        if story.get("project") != project: continue
        declared = structures.get(story["id"])
        if declared is not None:
            shots = declared.get("shots", [])
        elif story.get("sequenceID"):
            sequence = sequences.get(story["sequenceID"], {})
            shots = sequence.get("shots")
            if shots is None:
                shots = [shot for shot in data.get("shotMaterials", {}).get("shots", [])
                         if shot.get("project") == project and shot.get("independentSequenceID") == story["sequenceID"]]
        else:
            shots = []
        for shot in shots:
            sid = shot.get("shotID") or shot.get("id")
            if not isinstance(sid, str) or not sid: continue
            targets[(story["id"], sid)] = {"storyID": story["id"], "storyTitle": story.get("title", story["id"]),
                "shotID": sid, "shotTitle": shot.get("title") or shot.get("label") or sid}
    return list(targets.values())


def cast_use_state(data: dict, asset: dict, reviews: dict) -> dict:
    groups = [group for group in data.get("castCollections", []) if group.get("project") == asset.get("project")
              and asset["id"] in cast_member_ids(group)]
    raw = reviews.get(asset["id"], {}).get("castUse")
    manual = normalize_cast_use(raw) or {}
    source_selected = asset.get("roleDecision") == "user_assigned" or asset.get("selectionStatus") == "user_selected_visible_golden_reference"
    source_role = asset.get("characterRole") or next((group.get("role") or group.get("title") for group in groups), "") or ""
    role = manual.get("role", source_role)
    selected = manual.get("roleSelected", source_selected)
    choices = cast_story_targets(data, asset.get("project"))
    available = {(row["storyID"], row["shotID"]) for row in choices}
    links = manual.get("storyboardLinks", [])
    valid = [link for link in links if (link["storyID"], link["shotID"]) in available]
    unresolved = [link for link in links if (link["storyID"], link["shotID"]) not in available]
    return {"groups": groups, "sourceSelected": source_selected, "sourceRole": source_role,
            "roleSelected": selected, "role": role, "storyboardPlanned": manual.get("storyboardPlanned", False),
            "storyboardLinks": links, "validLinks": valid, "unresolvedLinks": unresolved, "targets": choices,
            "editable": bool(groups) or asset.get("category") == "cast" or raw is not None,
            "value": {**manual, "roleSelected": selected, "role": role,
                      "storyboardPlanned": manual.get("storyboardPlanned", False), "storyboardLinks": links}}


def normalize_decision(value: Any, *, partial: bool = False, allow_catalog_variant: bool = True) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ValueError("A review decision must be an object.")
    result: dict[str, Any] = {} if partial else {"status": None, "note": "", "shotPlan": None}
    if "status" in value:
        if value["status"] is not None and value["status"] not in REVIEW_STATUSES:
            raise ValueError("A review status must be keep, needs_fixes, remove, or null.")
        result["status"] = value["status"]
    if "note" in value:
        if not isinstance(value["note"], str):
            raise ValueError("Review notes must be text.")
        result["note"] = value["note"][:20000]
    if "shotPlan" in value:
        result["shotPlan"] = normalize_plan(value["shotPlan"])
    if "castUse" in value:
        result["castUse"] = normalize_cast_use(value["castUse"])
    if "variant" in value:
        if value["variant"] not in ("prime", "multiverse"):
            raise ValueError("A reference lane must be prime or multiverse.")
        catalog_origin = value.get("variantSource") == "catalog" or value.get("origin") == "catalog"
        if allow_catalog_variant or not catalog_origin:
            result["variant"] = value["variant"]
            result["variantSource"] = "catalog" if catalog_origin else "user"
    if "workingReference" in value:
        ref = value["workingReference"]
        if ref is not None and (not isinstance(ref, dict) or ref.get("status") not in ("requested", "approved")
                                or ref.get("scope") not in ("complete_look", "identity", "outfit", "scene", "detail")):
            raise ValueError("A working reference needs a valid status and scope.")
        result["workingReference"] = json.loads(json.dumps(ref, allow_nan=False)) if ref else None
    if "storyboardStage" in value:
        if value["storyboardStage"] is not None and value["storyboardStage"] not in STORYBOARD_STAGES:
            raise ValueError("Choose a valid storyboard stage.")
        result["storyboardStage"] = value["storyboardStage"]
    for key in ("likenessRating", "sceneQualityRating"):
        if key in value:
            rating = value[key]
            if rating is not None and (type(rating) is not int or not 1 <= rating <= 5):
                raise ValueError("A review rating must be 1–5 or null.")
            result[key] = rating
    if "workingReferenceScope" in value:
        scope = value["workingReferenceScope"]
        if scope is not None and scope not in ("complete_look", "identity", "outfit", "scene", "detail"):
            raise ValueError("Choose a valid working-reference scope.")
        result["workingReferenceScope"] = scope
    for field, choices in (("collectionState", {"archived", "working"}), ("multiverseSelection", {"candidate", "approved"})):
        if field in value:
            if value[field] is not None and value[field] not in choices:
                raise ValueError(f"Invalid {field} choice.")
            result[field] = value[field]
    for key in REVIEW_METADATA_FIELDS & value.keys():
        result[key] = json.loads(json.dumps(value[key], allow_nan=False))
    return result


def _hash_matches(item: dict, asset: dict) -> bool:
    return (item.get("sha256") or None) == (asset.get("sha256") or None)


def effective_reviews(assets: list[dict], seeds: Any, overrides: dict[str, dict], aliases: Any = ()) -> dict[str, dict]:
    """Overlay session choices on supplied seeds; explicit null survives reruns."""
    by_id = {a["id"]: a for a in assets}
    if isinstance(seeds, dict):
        seeds = seeds.get("items", [])
    alias_map = validated_asset_aliases(assets, aliases)
    alias_ids = {alias["canonicalID"] for alias in alias_map.values()}
    result = {}
    for asset in assets:
        source_fields = {key: asset[key] for key in ("workingReference", "variant") if key in asset}
        if source_fields:
            if "variant" in source_fields:
                source_fields["variantSource"] = "catalog"
            _merge_decision(result, asset["id"], normalize_decision(source_fields), alias_ids)
    for item in seeds if isinstance(seeds, list) else []:
        asset = resolve_asset_reference(item, assets, aliases)
        if not asset:
            continue
        try:
            decision = normalize_decision(item, partial=True)
            if item["id"] in alias_map:
                decision.pop("validationEvidence", None)
                decision["_visualAliasSource"] = {"id": item["id"], "sha256": item["sha256"]}
            if "variant" in decision:
                decision["variantSource"] = "catalog"
            _merge_decision(result, asset["id"], decision, alias_ids)
        except (ValueError, TypeError):
            continue
    # Overrides are session data or already hash-validated imports.
    return merge_review_overrides(result, overrides, assets, aliases)


def reference_record(asset: dict) -> dict:
    return {"id": asset["id"], "sha256": asset.get("sha256") or None,
            "project": asset.get("project"), "filename": asset.get("filename"),
            "path": asset.get("repoPath", asset.get("src")), "role": asset.get("category")}


def review_provenance(payload: dict, existing: dict | None = None, *, strict_takes: bool = True) -> dict:
    """Preserve source reviews/evidence verbatim, without evaluating or rebinding them.

    This is a backup merger, not a validation engine. Evidence keeps its original
    target ID, hash and scope; an alias never makes old evidence current.
    """
    from studio_dependencies import current_module
    takes = current_module("storyboard_takes")
    result = {"validationEvidence": {"format": "cfa-reference-validation-v1", "schemaVersion": 1,
                                     "assessments": [], "legacyReviewArchive": []}, "sceneReviews": [],
              "storyboardTakes": takes.empty(), "storyboardTakeBackups": []}
    envelope = result["validationEvidence"]
    seen_assessments: dict[str, str] = {}

    def stable(value: Any) -> str:
        return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(",", ":"))

    def append_unique(target: list, records: list) -> None:
        seen = {stable(record) for record in target}
        for record in records:
            key = stable(record)
            if key not in seen:
                target.append(deepcopy(record))
                seen.add(key)

    def unread(source: str, value: Any, error: str) -> None:
        append_unique(envelope.setdefault("unreadBackups", []),
                      [{"sourceKey": source, "raw": stable(value), "error": error}])

    for source in (existing or {}, payload):
        if not isinstance(source, dict):
            raise ValueError("Review provenance must be an object.")
        # Take snapshots are immutable. Validate the complete union before this
        # function returns, so callers can reject a conflicting import atomically.
        if "storyboardTakes" in source:
            try:
                result["storyboardTakes"] = takes.merge(result["storyboardTakes"], source["storyboardTakes"])
            except ValueError as error:
                if strict_takes:
                    raise
                append_unique(result["storyboardTakeBackups"], [{"origin": "source review provenance",
                    "reason": str(error), "data": source["storyboardTakes"]}])
        backups = source.get("storyboardTakeBackups", [])
        if not isinstance(backups, list):
            if strict_takes:
                raise ValueError("Storyboard take backups must be a list.")
            append_unique(result["storyboardTakeBackups"], [{"origin": "source review provenance",
                "reason": "Storyboard take backups must be a list.", "data": backups}])
        else:
            append_unique(result["storyboardTakeBackups"], backups)
        raw = source.get("items", source.get("reviewDecisions", []))
        if isinstance(raw, dict):
            raw = raw.get("items", [])
        if isinstance(raw, list):
            append_unique(envelope["legacyReviewArchive"], raw)
        scenes = source.get("sceneReviews", [])
        if isinstance(scenes, list):
            # The native editor does not edit these. Keep source records/order intact.
            append_unique(result["sceneReviews"], scenes)
        elif scenes is not None:
            unread("sceneReviews", scenes, "Unsupported scene-review backup retained.")
        evidence = source.get("validationEvidence")
        if evidence is None and isinstance(source.get("referenceValidation"), dict):
            # Catalog assessments already carry their exact source bindings.
            evidence = {"format": "cfa-reference-validation-v1", "schemaVersion": 1,
                        "assessments": source["referenceValidation"].get("assessments", [])}
        if evidence is None:
            continue
        if (not isinstance(evidence, dict) or evidence.get("format") != "cfa-reference-validation-v1"
                or evidence.get("schemaVersion") != 1 or not isinstance(evidence.get("assessments"), list)
                or not isinstance(evidence.get("legacyReviewArchive", []), list)
                or not isinstance(evidence.get("unreadBackups", []), list)
                or any(not isinstance(row, dict) or not isinstance(row.get("sourceKey"), str)
                       or not isinstance(row.get("raw"), str) or not isinstance(row.get("error"), str)
                       for row in evidence.get("unreadBackups", []))
                or any(not isinstance(row, dict) or not isinstance(row.get("id"), str) or not row["id"]
                       for row in evidence.get("assessments", []))):
            unread("validationEvidence", evidence, "Unsupported validation evidence retained without activation.")
            continue
        if evidence.keys() - {"format", "schemaVersion", "assessments", "legacyReviewArchive", "unreadBackups"}:
            unread("validationEvidence", evidence, "Additional evidence envelope fields retained without interpretation.")
        for record in evidence["assessments"]:
            key = stable(record)
            prior = seen_assessments.get(record["id"])
            if prior is not None and prior != key:
                raise ValueError("Conflicting immutable evidence ID: " + record["id"])
            if prior is None:
                envelope["assessments"].append(deepcopy(record))
                seen_assessments[record["id"]] = key
        append_unique(envelope["legacyReviewArchive"], evidence.get("legacyReviewArchive", []))
        if evidence.get("unreadBackups"):
            append_unique(envelope.setdefault("unreadBackups", []), evidence["unreadBackups"])
    return result


def review_payload(assets: list[dict], reviews: dict[str, dict], favorites: set[str], basket: set[str] | None = None,
                   *, provenance: dict | None = None) -> dict:
    payload = {"format": REVIEW_FORMAT, "exported": datetime.now(timezone.utc).isoformat(),
            "status": "session review and draft shot plans; no files deleted and no generation submitted",
            "items": [{**reference_record(a), **normalize_decision(reviews[a["id"]])}
                      for a in assets if a["id"] in reviews],
            "favorites": [reference_record(a) for a in assets if a["id"] in favorites]}
    if basket is not None:
        payload["exportBasket"] = [reference_record(a) for a in assets if a["id"] in basket]
    if provenance is not None:
        payload.update(review_provenance({}, provenance))
    return payload


def read_review(payload: Any, assets: list[dict], aliases: Any = ()) -> tuple[dict[str, dict], set[str], int]:
    """Read both formats without changing the catalog, sources, or approvals."""
    if isinstance(payload, dict) and payload.get("format") == FAVORITES_FORMAT:
        favorites, notes, skipped = read_favorites(payload, assets, aliases)
        return {key: {"note": value} for key, value in notes.items()}, favorites, skipped
    if not isinstance(payload, dict) or payload.get("format") != REVIEW_FORMAT or not isinstance(payload.get("items"), list):
        raise ValueError("Choose a CFA review or favorites JSON export.")
    raw_favorites = payload.get("favorites", [])
    if not isinstance(raw_favorites, list):
        raise ValueError("The favorites field must be a list of references.")
    alias_map = validated_asset_aliases(assets, aliases)
    alias_ids = {alias["canonicalID"] for alias in alias_map.values()}
    reviews, favorites, skipped = {}, set(), 0
    for item in payload["items"]:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            skipped += 1
            continue
        asset = resolve_asset_reference(item, assets, aliases)
        if not asset:
            skipped += 1
            continue
        try:
            decision = normalize_decision(item, partial=True, allow_catalog_variant=False)
            if item["id"] in alias_map:
                decision.pop("validationEvidence", None)
                decision["_visualAliasSource"] = {"id": item["id"], "sha256": item["sha256"]}
            # Partial imports must not clear unrelated existing fields.
            prior = reviews.get(asset["id"])
            if asset["id"] in alias_ids and prior is not None:
                if _review_time(decision) < _review_time(prior) or _review_time(decision) == _review_time(prior) and decision.get("_visualAliasSource"):
                    continue
            decision = _guard_plan_clear(prior or {}, decision)
            merged = {**(prior or {}), **decision}
            if "_visualAliasSource" not in decision:
                merged.pop("_visualAliasSource", None)
            reviews[asset["id"]] = merged
        except (ValueError, TypeError):
            skipped += 1
    for item in raw_favorites:
        asset = resolve_asset_reference(item, assets, aliases, require_hash=True, allow_alias_id=True)
        if asset:
            favorites.add(asset["id"])
        else:
            skipped += 1
    return reviews, favorites, skipped


def export_allowed(asset: dict, reviews: dict[str, dict], intent: str = "prime") -> bool:
    if intent not in ("prime", "multiverse_ingredients"):
        raise ValueError("Unknown export intent.")
    decision = reviews.get(asset["id"], {})
    variant = decision.get("variant", asset.get("variant", "prime"))
    return normal_visible(asset, reviews) and (variant != "multiverse" or intent == "multiverse_ingredients")


def handoff_payload(assets: list[dict], reviews: dict[str, dict], project: str, destination: str, intent: str = "prime") -> dict:
    if destination not in (*DESTINATIONS, "all"):
        raise ValueError("Unknown shot-plan destination.")
    items = []
    for asset in assets:
        if asset.get("project") != project or not export_allowed(asset, reviews, intent):
            continue
        decision = reviews.get(asset["id"], {})
        plan = normalize_plan(decision.get("shotPlan"))
        if not plan or (destination != "all" and destination not in plan["destinations"]):
            continue
        items.append({**reference_record(asset), "title": asset.get("title", asset.get("filename")),
                      "reviewStatus": decision.get("status"),
                      "variant": decision.get("variant", asset.get("variant", "prime")),
                      "storyboardStage": storyboard_stage(asset, reviews),
                      "note": decision.get("note", ""), "shotPlan": plan})
    return {"format": HANDOFF_FORMAT, "exported": datetime.now(timezone.utc).isoformat(),
            "project": project, "destination": destination, "status": "planned; not sent or generated",
            "exportIntent": intent,
            "attachmentReminder": "This is a reference manifest, not an image ZIP. Attach the named source files and the current approved character/reference kit separately.",
            "items": items}


def handoff_text(payload: dict) -> str:
    lines = ["CFA shot handoff", f"Project: {payload['project']} | Destination: {destination_label(payload['destination'])}",
             "Status: planned; not sent or generated", payload["attachmentReminder"], ""]
    for item in payload["items"]:
        plan = item["shotPlan"]
        lines.extend([f"Reference: {item.get('filename')} | {item['id']}",
                      f"Source SHA256: {item.get('sha256') or 'unavailable'}", f"Path: {item.get('path')}",
                      f"Role: {item.get('role')} | Review: {item.get('reviewStatus') or 'unmarked'}",
                      f"Destinations: {', '.join(map(destination_label, plan['destinations']))}", f"Review note: {item.get('note', '')}",
                      f"Output kind: {output_kind_label(plan.get('outputKind'))}",
                      f"Shot idea: {plan['idea']}", f"Prompt draft: {plan['prompt']}", ""])
    return "\n".join(lines)


def mission_review_gate(value: Any) -> dict | None:
    """Read an explicit, exact-version review scope without shrinking invalid scopes."""
    if not isinstance(value, dict) or not isinstance(value.get("label"), str) or not value["label"].strip():
        return None
    if not isinstance(value.get("targets"), list) or not value["targets"]:
        return None
    targets, seen = [], {}
    for target in value["targets"]:
        if not isinstance(target, dict) or not isinstance(target.get("assetID"), str) or not target["assetID"].strip():
            return None
        digest = target.get("sha256")
        if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", digest):
            return None
        aid, digest = target["assetID"], digest.lower()
        if aid in seen:
            if seen[aid] != digest:
                return None
            continue
        seen[aid] = digest
        targets.append({"assetID": aid, "sha256": digest})
    supplied = value.get("completed", {})
    if not isinstance(supplied, dict):
        return None
    completed = {key: supplied[key] for key in ("title", "statusLabel", "nextAction", "summary")
                 if isinstance(supplied.get(key), str)}
    completed["missing"] = [text for text in supplied.get("missing", []) if isinstance(text, str)] \
        if isinstance(supplied.get("missing", []), list) else []
    return {"label": value["label"], "targets": targets, "completed": completed}


def mission_tasks(value: Any) -> list[dict]:
    """Read saved task cards as data. Local hrefs are intentionally not exposed."""
    if not isinstance(value, dict) or not isinstance(value.get("tasks"), list):
        return []
    tasks, seen = [], set()
    for item in value["tasks"]:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str) or item["id"] in seen:
            continue
        if not isinstance(item.get("provider"), str) or not item["provider"].strip() or item.get("status") not in MISSION_STATUSES:
            continue
        if item.get("project") not in ("hon", "lisan", "shared"):
            continue
        if not all(isinstance(item.get(key), str) for key in ("title", "summary", "nextAction")):
            continue
        task = {key: item[key] for key in ("id", "provider", "project", "title", "status", "summary", "nextAction")}
        task["direction"] = item.get("direction") if item.get("direction") in ("inbound", "outbound", "internal") else "internal"
        task["workKind"] = item.get("workKind") if item.get("workKind") in ("image_new", "image_repair", "video", "planning") else "planning"
        task["missing"] = [s for s in item.get("missing", []) if isinstance(s, str)] if isinstance(item.get("missing", []), list) else []
        for key in ("enablers", "deliverables", "previewAssetIDs", "variantAssetIDs"):
            task[key] = [s for s in item.get(key, []) if isinstance(s, str)] if isinstance(item.get(key), list) else []
        for key in ("priority", "statusLabel", "missingLabel", "laterReview", "groupingBasis"):
            if isinstance(item.get(key), str):
                task[key] = item[key]
        if gate := mission_review_gate(item.get("reviewGate")):
            task["reviewGate"] = gate
        task["comparisonInHistory"] = item.get("comparisonInHistory") is True
        task["links"] = []
        for link in item.get("links", []) if isinstance(item.get("links", []), list) else []:
            if not isinstance(link, dict) or not isinstance(link.get("label", "Reference"), str):
                continue
            reference = {key: link[key] for key in ("assetID", "downloadPath") if isinstance(link.get(key), str)}
            if isinstance(link.get("assetIDs"), list):
                reference["assetIDs"] = [s for s in link["assetIDs"] if isinstance(s, str)]
            if isinstance(link.get("href"), str) and urlsplit(link["href"]).scheme == "https" and urlsplit(link["href"]).netloc:
                reference["href"] = link["href"]
            if isinstance(link.get("unavailableReason"), str):
                reference["unavailableReason"] = link["unavailableReason"]
            if reference:
                task["links"].append({"label": link.get("label", "Reference"), **reference})
        tasks.append(task)
        seen.add(item["id"])
    return tasks


def mission_review_data(base: dict, snapshot: dict) -> dict:
    """Union review identities without expanding ordinary browsing collections."""
    merged = dict(base)
    for key in ("assets", "reviewDecisions"):
        records = {item["id"]: item for item in base.get(key, [])}
        for item in snapshot.get(key, []):
            old = records.get(item["id"])
            if old and old.get("sha256") and item.get("sha256") != old["sha256"] and (
                key == "reviewDecisions" or old.get("kind") not in {"document", "pdf"} or item.get("kind") not in {"document", "pdf"}
            ):
                raise ValueError(f"Mission snapshot changes an existing reference hash: {item['id']}")
            records[item["id"]] = item
        merged[key] = list(records.values())
    return merged


def mission_visible(asset: dict | None, reviews: dict) -> bool:
    return normal_visible(asset, reviews)


def mission_pending_requests(data: dict, reviews: dict, project: str) -> list[str]:
    by_id = {a["id"]: a for a in data.get("assets", [])}
    return list(dict.fromkeys(r["id"] for r in data.get("reviewRequests", [])
        if (a := by_id.get(r.get("id"))) and a.get("project") == project
        and r.get("type") == "missing_decision" and a.get("sha256") and r.get("sha256") == a["sha256"]
        and mission_visible(a, reviews) and reviews.get(a["id"], {}).get("status") not in REVIEW_STATUSES))


def mission_storyboard_requests(data: dict, tasks: list[dict], project: str) -> list[dict]:
    """Explicit author-choice packages, never inferred from missing shot fields."""
    stories = {story['id'] for story in data.get('storyboardStories', []) if story.get('project') == project}
    source_tasks = {task.get('id'): task for task in data.get('missionControl', {}).get('tasks', [])}
    result = []
    for task in tasks:
        if task.get('project') != project or task.get('status') != 'needs_input':
            continue
        action = source_tasks.get(task['id'], {}).get('userAction')
        if not isinstance(action, dict) or not isinstance(action.get('links'), list):
            continue
        for link in action['links']:
            if not isinstance(link, dict) or link.get('project') != project or link.get('view') != 'storyboard':
                continue
            album = link.get('album')
            if not isinstance(album, str) or not album.startswith(('structure:', 'story:')):
                continue
            story_id = album.split(':', 1)[1]
            if story_id in stories:
                result.append(dict(id=task['id'], title=task['title'], project=project, storyID=story_id,
                                   structure=album.startswith('structure:')))
                break
    return result


def mission_task_progress(task: dict, assets: list[dict], reviews: dict) -> dict:
    """Refresh explicit review gates; answering does not approve or send anything."""
    task = dict(task)
    if task.get("status") == "done":
        return task
    by_id = {a["id"]: a for a in assets}
    if gate := mission_review_gate(task.get("reviewGate")):
        pending, answered, unavailable = [], [], []
        for target in gate["targets"]:
            aid = target["assetID"]
            asset = by_id.get(aid)
            review = reviews.get(aid, {})
            if (not asset or asset.get("kind") not in {"image", "video"}
                    or str(asset.get("sha256", "")).lower() != target["sha256"]
                    or (review.get("sha256") and str(review["sha256"]).lower() != target["sha256"])):
                unavailable.append(aid)
            elif review.get("status") in REVIEW_STATUSES:
                answered.append(aid)
            elif mission_visible(asset, reviews):
                pending.append(aid)
            else:
                unavailable.append(aid)
        counts = (f"{len(answered)} of {len(gate['targets'])} images or clips have recorded decisions. "
                  f"{len(pending)} await your decision.")
        if unavailable:
            counts += f" {len(unavailable)} references are unavailable or have a different version and need a source check."
        task.update(previewAssetIDs=pending, reviewedPreviewAssetIDs=answered,
                    reviewProgress={"requested": len(gate["targets"]), "answered": len(answered),
                                    "pendingIDs": pending, "reviewedIDs": answered, "unavailableIDs": unavailable})
        completed = gate["completed"]
        if pending:
            task.update(status="needs_input", statusLabel="Needs your input",
                        title=f"{gate['label']} · {len(pending)} awaiting review", summary=counts,
                        nextAction="Review the remaining images or clips. Existing decisions stay saved; recorded defects remain separate follow-up work.",
                        missing=[f"{len(pending)} requested versions have no recorded decision."])
        elif unavailable:
            task.update(status="in_progress", statusLabel="Reference check needed",
                        title=f"{gate['label']} · reference check needed", summary=counts,
                        nextAction="The team needs to resolve the exact missing or mismatched versions before review can continue. Your recorded decisions remain saved.",
                        missing=[*completed.get("missing", []), "Resolve the unavailable exact versions; do not substitute a different image or clip."])
        else:
            task.update(status="in_progress", statusLabel=completed.get("statusLabel") or "Review recorded · team follow-up",
                        priority="normal", title=completed.get("title") or f"{gate['label']} · review recorded",
                        summary=counts + (" " + completed["summary"] if completed.get("summary") else ""),
                        nextAction=completed.get("nextAction", "The review decisions are saved. The team can prepare any recorded follow-up."),
                        missing=list(completed.get("missing", [])))
    elif task["id"] in {"grok-lisan-mouth65-available", "grok-falcon-extension40-available"}:
        pending, answered, unavailable = [], [], []
        for aid in dict.fromkeys(task.get("previewAssetIDs", [])):
            a = by_id.get(aid)
            if not a or a.get("kind") != "image":
                unavailable.append(aid)
            elif reviews.get(aid, {}).get("status") in REVIEW_STATUSES:
                answered.append(aid)
            elif mission_visible(a, reviews):
                pending.append(aid)
            else:
                unavailable.append(aid)
        name = "Lisan mouth" if task["id"] == "grok-lisan-mouth65-available" else "Falcon extension"
        task.update(title=f"{name} shortlist · {len(pending)} awaiting review",
                    status="needs_input" if pending else "in_progress",
                    priority=task.get("priority") if pending or unavailable else "normal",
                    previewAssetIDs=pending, reviewedPreviewAssetIDs=answered,
                    summary=f"{len(answered)} of {len(pending) + len(answered) + len(unavailable)} shortlisted images have recorded decisions. {len(pending)} await your decision."
                            + (f" {len(unavailable)} references are unavailable and need a source check." if unavailable else "")
                            + " The full collection remains available; images outside this shortlist are not new review requests.",
                    nextAction="Review the remaining shortlist. Existing decisions stay saved; recorded defects remain separate correction work." if pending else
                               "The shortlist decisions are saved. The team can follow up on recorded defects; earlier decisions remain available below.")
    elif task["id"] == "favorites-prop-sweep":
        received = [a for a in assets if a.get("project") == "hon" and a.get("kind") == "image"
                    and a.get("sourceIntake") == "HON-GROK-RETURN-20261009" and a.get("propState") == "with_gun" and a.get("outfitAlbumID")]
        visible = [a for a in received if mission_visible(a, reviews)]
        pending = [a["id"] for a in visible if reviews.get(a["id"], {}).get("status") not in REVIEW_STATUSES]
        fixes = sum(reviews.get(a["id"], {}).get("status") == "needs_fixes" for a in visible)
        task.update(title=f"Review outfit gun variants · {len(pending)} unreviewed" if pending else "Outfit gun variant review",
                    status="needs_input" if pending else "in_progress",
                    statusLabel="Needs your input" if pending else "Review recorded · team follow-up",
                    summary=f"{len(received)} distinct gun variants across {len({a['outfitAlbumID'] for a in received})} outfits. {len(visible)} visible; {len(received)-len(visible)} hidden by removal or archive choices. {len(pending)} unreviewed; {fixes} need fixes. Gun approval is separate from character corrections.",
                    nextAction="Review the remaining variants for outfit and character preservation." if pending else "The recorded decisions are saved; character and other recorded fixes remain separate follow-up work.",
                    missing=[], previewAssetIDs=pending,
                    reviewedPreviewAssetIDs=[a["id"] for a in received if reviews.get(a["id"], {}).get("status") in REVIEW_STATUSES])
    return task


def production_workflows(value: Any) -> list[dict]:
    """Concrete workflow records only; Cloud links never launch a run."""
    if not isinstance(value, list):
        return []
    result, seen = [], set()
    for item in value:
        if not isinstance(item, dict) or not all(isinstance(item.get(key), str) for key in
                                               ("id", "provider", "project", "title", "status", "summary", "nextAction")):
            continue
        if item["id"] in seen or item["provider"] != "ComfyUI":
            continue
        record = {key: item[key] for key in ("id", "provider", "project", "title", "status", "summary", "nextAction")}
        for key in ("sourceAssetIDs", "outputAssetIDs", "documentAssetIDs"):
            record[key] = [asset_id for asset_id in item.get(key, []) if isinstance(asset_id, str)] if isinstance(item.get(key, []), list) else []
        url = item.get("cloudURL")
        if isinstance(url, str):
            parsed = urlsplit(url)
            if parsed.scheme == "https" and parsed.netloc == "cloud.comfy.org":
                record["cloudURL"] = url
        result.append(record)
        seen.add(item["id"])
    return result


def basket_payload(assets: list[dict], basket: set[str], reviews: dict[str, dict] | None = None, intent: str = "prime") -> dict:
    return {"format": EXPORT_FORMAT, "exported": datetime.now(timezone.utc).isoformat(),
            "status": "selected references; no approval implied",
            "exportIntent": intent,
            "referenceReminder": "This JSON is a selection list, not a media archive. The separate ZIP contains hosted review copies, not original master files.",
            "items": [reference_record(a) for a in assets if a["id"] in basket and export_allowed(a, reviews or {}, intent)]}


def read_basket(payload: Any, assets: list[dict], aliases: Any = ()) -> tuple[set[str], int]:
    if not isinstance(payload, dict) or payload.get("format") != EXPORT_FORMAT or not isinstance(payload.get("items"), list):
        raise ValueError("Choose a CFA export-basket JSON selection list.")
    accepted, skipped = set(), 0
    for item in payload["items"]:
        if not isinstance(item, dict) or not isinstance(item.get("id"), str):
            skipped += 1
            continue
        asset = resolve_asset_reference(item, assets, aliases)
        if asset:
            accepted.add(asset["id"])
        else:
            skipped += 1
    return accepted, skipped


def basket_zip(library_dir: Path, assets: list[dict], basket: set[str], max_bytes: int = 100 * 1024 * 1024,
               reviews: dict[str, dict] | None = None, intent: str = "prime") -> bytes:
    """Package safe hosted copies in memory; deduplicate bytes and preserve provenance."""
    selected = [asset for asset in assets if asset["id"] in basket and export_allowed(asset, reviews or {}, intent)]
    if not selected:
        raise ValueError("Add at least one reference to the export basket.")
    paths, unique_paths = {}, set()
    for asset in selected:
        source = media_path(library_dir, asset.get("src"))
        if source is None:
            raise ValueError(f"The review copy for {asset.get('filename', asset['id'])} is unavailable. Export the JSON selection list instead.")
        paths[asset["id"]] = source
        unique_paths.add(source)
    if sum(path.stat().st_size for path in unique_paths) > max_bytes:
        raise ValueError("This basket exceeds the 100 MB review-copy limit. Export smaller groups or use the JSON selection list.")
    output = io.BytesIO()
    manifest = basket_payload(assets, basket, reviews, intent)
    manifest["archiveContents"] = "Hosted review copies, not original masters. Source sha256 identifies each original; reviewCopySha256 identifies the packaged copy."
    records, by_hash, total = [], {}, 0
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=1) as archive:
        for asset in selected:
            source = paths[asset["id"]]
            content = source.read_bytes()
            digest = hashlib.sha256(content).hexdigest()
            if digest not in by_hash:
                total += len(content)
                if total > max_bytes:
                    raise ValueError("The selected review copies exceed the ZIP size limit.")
                name = re.sub(r"[^A-Za-z0-9._ -]", "_", Path(asset.get("filename", asset["id"])).stem)[:100] or "reference"
                member = f"review-copies/{digest[:16]}-{name}{source.suffix.lower()}"
                archive.writestr(member, content)
                by_hash[digest] = member
            records.append({**reference_record(asset), "archivePath": by_hash[digest], "reviewCopySha256": digest,
                            "reviewCopyBytes": len(content)})
        manifest["items"] = records
        manifest["uniqueReviewCopies"] = len(by_hash)
        archive.writestr("manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
        archive.writestr("README.txt", "CFA export basket\nThese are hosted review copies, not original master files.\nRead manifest.json for original source references and hashes.\nSelection does not imply production approval.\n")
    return output.getvalue()


def document_tree(assets: list[dict], query: str = "") -> dict[str, dict[str, list[dict]]]:
    parents = {name: {} for name in ("Design & outfit notes", "Story & music", "Collaborator briefs",
                                    "Production & workflows", "Tattoos & details", "History & helpers")}
    terms = query.casefold().split()
    for asset in assets:
        if asset.get("kind") not in ("document", "pdf"):
            continue
        album = str(asset.get("album", "Supporting notes"))
        context = " ".join(str(asset.get(key, "")) for key in ("album", "title", "filename")).casefold()
        if not all(term in (context + " " + str(asset.get("text", "")).casefold()) for term in terms):
            continue
        child = album
        if "design and outfit notes" in album.casefold() or "design & outfit notes" in album.casefold():
            parent = "Design & outfit notes"
            child = album.partition("·")[2]
            child = child.strip() or "General design notes"
        elif any(word in context for word in ("historical", "history", "helper", "quarantine")):
            parent = "History & helpers"
        elif any(word in context for word in ("storyboard", "lyric", "music", "story beat")):
            parent = "Story & music"
        elif any(word in context for word in ("collaborator", "gemini", "grok", "panhandler")) or re.search(r"\bflow\b", context):
            parent = "Collaborator briefs"
        elif any(word in context for word in ("tattoo", "piercing", "stencil", "detail")):
            parent = "Tattoos & details"
        elif any(word in context for word in ("outfit", "design", "casting", "character")):
            parent = "Design & outfit notes"
        else:
            parent = "Production & workflows"
        parents[parent].setdefault(child, []).append(asset)
    return {name: groups for name, groups in parents.items() if groups}


def storyboard_window(results: list[tuple[dict, dict | None]], lower: int, upper: int) -> list[tuple[dict, dict | None]]:
    def within(asset):
        position = asset.get("storyboardPosition")
        if isinstance(position, (int, float)) and not isinstance(position, bool):
            return lower <= position <= upper
        return lower == 0 and upper == 100
    filtered = [row for row in results if within(row[0])]
    return sorted(filtered, key=lambda row: row[0].get("storyboardOrder", float("inf")))


def storyboard_stage(asset: dict, reviews: dict[str, dict]) -> str | None:
    default = "preliminary" if asset.get("category") == "storyboard" else None
    value = reviews.get(asset["id"], {}).get("storyboardStage") or asset.get("storyboardStage", default)
    return value if value in STORYBOARD_STAGES else default


def storyboard_themes(asset: dict, album: dict | None = None) -> list[str]:
    explicit = asset.get("storyboardThemes", asset.get("themes", []))
    values = explicit if isinstance(explicit, list) and explicit else asset.get("tags", [])
    values = [value for value in values if isinstance(value, str) and value.casefold() != "storyboard"
              and not re.fullmatch(r"series\s*\d+", value.casefold())] if isinstance(values, list) else []
    if not values and album and album.get("title"):
        values = [album["title"]]
    return list(dict.fromkeys(values))


def sweep_payload(assets: list[dict], reviews: dict[str, dict], favorites: set[str], basket: set[str],
                  *, provenance: dict | None = None) -> dict:
    payload = review_payload(assets, reviews, favorites, basket, provenance=provenance)
    payload["sweep"] = {"status": "prepared; not sent or executed", "requestedCollaborator": "Panhandler Nova",
                        "instruction": "Review these choices against source hashes. Apply only the stated scopes. Confirm promotion requests and keep Multiverse out of Prime working references. Do not infer deletion from a queue flag.",
                        "promotionQueue": [{**reference_record(asset), "workingReference": reviews[asset["id"]]["workingReference"]}
                                           for asset in assets if (reviews.get(asset["id"], {}).get("workingReference") or {}).get("status") == "requested"
                                           and export_allowed(asset, reviews, "prime")]}
    return payload
